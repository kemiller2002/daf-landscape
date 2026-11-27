/// Orchestration of the eight models, sensitivity (tornado), correlated Monte Carlo and extreme scenarios. Pure.
module CompetitiveAdvantageCreation.Analysis

open CompetitiveAdvantageCreation.Domain
open CompetitiveAdvantageCreation.Inputs

let setting (i: Inputs) key dflt = Map.tryFind key i.Settings |> Option.defaultValue dflt

// ------------------------------------------------------------------ modelling bases (Revision 3)

/// A modelling basis: engine switches plus the revision-3 corrections and the population cap set.
type ModelBasis =
    { Id: string
      Label: string
      Engine: Cashflow.Basis
      Corrected: bool
      CapSet: string }

let revision2 = { Id = "revision2"; Label = "Revision 2 (conservative)"; Engine = Cashflow.revision2Basis; Corrected = false; CapSet = "all" }
let revision3 = { Id = "revision3"; Label = "Revision 3 (CFO-corrected)"; Engine = Cashflow.revision3Basis; Corrected = true; CapSet = "plausible" }
let modelBases = [ revision2; revision3 ]
let primaryBasis (i: Inputs) = if setting i "basis" "revision3" = "revision2" then revision2 else revision3

// ------------------------------------------------------------------ registry (model 3)

/// A registry configuration: monitoring mode, who performs the human deep review (P3-DEC-MOD005), whether reviews
/// follow demand (REV4003) and whether the review is risk-tiered and attested (REV4004, subject to counsel and V-9).
type RegistryConfig = { Id: string; Mode: string; Performer: Registry.Performer; Demand: bool; Tiered: bool; Label: string }

let registryConfig (id: string) : RegistryConfig =
    match id with
    | "M1-vendor-2pa" -> { Id = id; Mode = "M1"; Performer = Registry.Vendor; Demand = false; Tiered = false; Label = "M1, Echelon performs the deep review, 2 reviews a year (revision 2)" }
    | "M1-vendor-demand" -> { Id = id; Mode = "M1"; Performer = Registry.Vendor; Demand = true; Tiered = false; Label = "M1, Echelon performs the deep review, demand-driven" }
    | "M1T-vendor-demand" -> { Id = id; Mode = "M1T"; Performer = Registry.Vendor; Demand = true; Tiered = true; Label = "M1 risk-tiered attested review, Echelon performs, demand-driven (subject to counsel and V-9)" }
    | "M1-sponsor" -> { Id = id; Mode = "M1"; Performer = Registry.Sponsor; Demand = true; Tiered = false; Label = "M1, sponsor performs the deep review (transferred; P3-DEC-MOD005)" }
    | "M5" -> { Id = id; Mode = "M5"; Performer = Registry.Vendor; Demand = true; Tiered = false; Label = "M5 hybrid (conditional on OD-CDD-02)" }
    | m -> { Id = m; Mode = m; Performer = Registry.Vendor; Demand = false; Tiered = false; Label = m }

let registryConfigIds = [ "M1-vendor-2pa"; "M1-vendor-demand"; "M1T-vendor-demand"; "M1-sponsor"; "M5" ]

/// Governing configuration for compliance-bound figures (no new owner decision assumed).
let registryMode (i: Inputs) = setting i "registry_config" "M1-vendor-demand"
/// Configuration shown only as conditional on OD-CDD-02, V-3 and V-9.
let registryModeConditional (i: Inputs) = setting i "registry_mode_conditional" "M5"

let registryOptions (i: Inputs) (b: ModelBasis) (c: Case) (rc: RegistryConfig) : Registry.Options =
    if not b.Corrected then Registry.revision2Options
    else
        let demand = if rc.Demand then pv i.Params c "review_frequency" / 2.0 else 1.0
        let tier = if rc.Tiered then pv i.Params c "tiered_review_factor" else 1.0
        { ReviewFactor = demand * tier; DeepReviewShared = false }

let registryAtB (i: Inputs) (b: ModelBasis) (c: Case) (cfg: string) (charities: float) (sponsors: float) =
    let rc = registryConfig cfg
    Registry.runCostWith (registryOptions i b c rc) c (pv i.Params c "connectors") i.RegistryComponents rc.Mode { CharitiesPerSponsor = charities; Sponsors = sponsors }

let registryAt (i: Inputs) (c: Case) (cfg: string) (charities: float) (sponsors: float) = registryAtB i (primaryBasis i) c cfg charities sponsors

/// Vendor-borne registry cost (GAP-HI010 rule) for a basis, configuration, charities per sponsor and live sponsors.
let registryAddableForB (i: Inputs) (b: ModelBasis) (c: Case) (cfg: string) (charities: float) (sponsors: float) =
    Registry.addableBy (registryConfig cfg).Performer (Registry.LeanLicensor(pv i.Params c "registry_engineering_absorbed")) (registryAtB i b c cfg charities sponsors)

let registryTransferredB (i: Inputs) (b: ModelBasis) (c: Case) (cfg: string) (charities: float) (sponsors: float) =
    Registry.transferredBy (registryConfig cfg).Performer (registryAtB i b c cfg charities sponsors)

let registryAddableFor (i: Inputs) (c: Case) (cfg: string) (charities: float) (sponsors: float) = registryAddableForB i (primaryBasis i) c cfg charities sponsors

/// One sponsor at the case's default charities in use, governing configuration.
let registryAddable (i: Inputs) (c: Case) = registryAddableFor i c (registryMode i) (pv i.Params c "registry_charities") 1.0

// ------------------------------------------------------------------ sponsor-size panel (SRC-013)

let captive (i: Inputs) = (setting i "captive_categories" "national_standard").Split(';') |> Set.ofArray

/// Sponsors counted by a cap set: "all" (revision 2 cap), "excl-captive" (revision 2 report count),
/// "plausible" (excludes processors and presumed own platforms; revision 3 cap), "third-party" (vendor evidence only).
let inCapSet (i: Inputs) (capSet: string) (s: Sponsor) =
    match capSet with
    | "all" -> true
    | "excl-captive" -> not (Set.contains s.Category (captive i))
    | "third-party" -> s.Platform = "third-party platform"
    | _ -> s.Platform = "third-party platform" || s.Platform = "unknown"

let eligibleIn (i: Inputs) (capSet: string) (accounts: float) =
    i.Sponsors |> List.filter (fun s -> s.Accounts >= accounts && inCapSet i capSet s) |> List.length |> float

let capSets = [ "all"; "excl-captive"; "plausible"; "third-party" ]

/// (all sponsors, plausible sponsors) at least `accounts` large.
let eligible (i: Inputs) (accounts: float) = eligibleIn i "all" accounts, eligibleIn i "plausible" accounts

// ------------------------------------------------------------------ capital (model 1)

let capitalGlobals (i: Inputs) : Capital.Globals =
    { Contingency = i.Params.["contingency"].Range; CapitalCharge = i.Params.["capital_charge"].Range }

type CapitalVariant =
    | AsPublished
    | Corrected

let capitalVariantName v = match v with AsPublished -> "AB as published" | Corrected -> "corrected (Revision 2)"

/// Value of a resolved field of the A3 Unbound stream (template TPL-UNB-S3) in a case.
let a3Value (i: Inputs) (c: Case) (field: string) =
    i.Streams |> List.tryFind (fun s -> s.StreamId = "A3-UNB") |> Option.bind (fun s -> Map.tryFind field s.Values)
    |> Option.map (Sequences.casePick c field) |> Option.defaultValue 0.0

/// Revision 2 corrections to AB's first-invoice method: registry at the governing mode for one customer of the A3
/// size; Nacha TPSP audit and fraud monitoring (CNV-PAY-001) and control operations in the live run; control
/// operations during SOC 2 observation in the pre-contract run; contingency without the founder draw; founder time
/// net of build work inside development at market; first conversion and go-live lag per REV3037/REV3039.
let correctionsB (i: Inputs) (b: ModelBasis) (mode: string) (c: Case) : Capital.Corrections =
    let a = a3Value i c
    let registry = registryAddableForB i b c mode (a "accounts_per_customer" * a "charities_per_account") 1.0
    let control = if b.Corrected then max 0.0 (a "control_ops_annual" - a "control_ops_maintenance_overlap") else a "control_ops_annual"
    let tpsp = a "tpsp_annual" - (if b.Corrected then min (a "tpsp_overlap_in_live_run") (a "tpsp_annual") else 0.0)
    { ExtraLiveAnnual = registry + tpsp + control
      ExtraPreAnnual = control * a "control_ops_pre_share"
      ContingencyOnFounder = false
      DevOverlapMonths = a "dev_months"
      FounderBuildShare = a "founder_build_share"
      Impl = Some(a "impl_first")
      GoLive = Some(a "golive_lag") }

let corrections (i: Inputs) (mode: string) (c: Case) = correctionsB i (primaryBasis i) mode c

let firstInvoiceB (i: Inputs) (b: ModelBasis) (mode: string) (v: CapitalVariant) (c: Case) (s: Capital.StateInput) =
    let k = match v with AsPublished -> Capital.asPublished | Corrected -> correctionsB i b mode c
    Capital.firstInvoice (capitalGlobals i) c (pv i.Params c "founder_econ") k s

let firstInvoiceMode (i: Inputs) (mode: string) (v: CapitalVariant) (c: Case) (s: Capital.StateInput) =
    let k = match v with AsPublished -> Capital.asPublished | Corrected -> corrections i mode c
    Capital.firstInvoice (capitalGlobals i) c (pv i.Params c "founder_econ") k s

let firstInvoice (i: Inputs) (v: CapitalVariant) (c: Case) (s: Capital.StateInput) = firstInvoiceMode i (registryMode i) v c s

/// Agent AB's revenue assumptions for the as-published self-sufficiency run.
let capitalRevenue (i: Inputs) : Capital.Revenue =
    let p n = i.Params.[n].Range
    { RevenuePerCustomer = p "revenue_per_customer_channel"; CustomersPerYear = p "customers_per_year_channel"; Churn = p "churn"
      VariableShare = p "ab_variable_share_as_published"; ArrearsMonths = p "arrears_months"; CacLater = p "cac_later"; ImplLater = point 0.0 }

type SelfSufficiency =
    { StateId: string; Variant: CapitalVariant; Case: Case; Summary: Cashflow.Summary }

/// AB's path in this engine (as published). The corrected path is the sequence model (A from S2, A3 from S3).
let selfSufficiencyAsPublished (i: Inputs) (c: Case) (s: Capital.StateInput) =
    let g = capitalGlobals i
    let stream = Capital.toStream c g (capitalRevenue i) 1.0 0.0 s
    let cg: Cashflow.Globals = { FounderEconAnnual = pv i.Params c "founder_econ"; CapitalChargeAnnual = pv i.Params c "capital_charge" }
    { StateId = s.StateId; Variant = AsPublished; Case = c; Summary = Cashflow.flows cg stream None |> Cashflow.summarize cg }

let preRevenueStates (i: Inputs) = i.States |> List.filter (fun s -> s.PreMonths.Base > 0.0)

// ------------------------------------------------------------------ Phase II double counts

type DoubleCountRow = { Route: string; Variant: string; BurnFactor: float; VariableShare: float; Capital: float }

let doubleCounts (i: Inputs) : DoubleCountRow list =
    let bf = pv i.Params BaseCase "build_phase_burn_factor"
    [ for (r, channel) in i.Routes do
          let direct = i.Routes |> List.tryFind (fun (x, _) -> x.Id = "ER-4") |> Option.map (fun (x, _) -> x.VariableShare) |> Option.defaultValue 0.15
          let perAcct = Phase2Check.perAccountEquivalentShare direct channel
          let variants =
              [ "Phase II as modelled", 1.0, None
                "build-phase burn at P3-ASM-MOD005 base", bf, None ]
              @ (if channel > 0.0 then
                     [ "variable share = direct per-account cost (corrected)", 1.0, Some perAcct
                       "variable share = direct share (AB alternative)", 1.0, Some direct
                       "both corrections", bf, Some perAcct ]
                 else [])
          for name, f, vs in variants do
              let k: Phase2Check.Corrections = { BuildPhaseBurnFactor = f; VariableShare = vs }
              yield { Route = r.Id; Variant = name; BurnFactor = f; VariableShare = defaultArg vs r.VariableShare; Capital = Phase2Check.capital k r } ]

// ------------------------------------------------------------------ events (model 2)

let eventRates (i: Inputs) (c: Case) : Events.Rates =
    { LabourPerMinute = pv i.Params c "labour_per_minute"; AutomationResidualShare = pv i.Params c "automation_residual_share"
      AiCostShare = pv i.Params c "ai_cost_share"; TransferEfficiency = pv i.Params c "transfer_efficiency" }

let eventScenarios = [ "opt", Favourable; "base", BaseCase; "pess", AdverseCase ]

/// Charity vetting (EV-E08) labour per 10k-account sponsor and the claims two models make on it, combined sequentially.
let vettingDoubleCount (i: Inputs) =
    let e08 = i.Events |> List.find (fun e -> e.EventId = "EV-E08" && e.Scenario = "base")
    let rate = pv i.Params BaseCase "labour_per_minute"
    let accounts = pv i.Params BaseCase "accounts_per_sponsor"
    let baseCost = e08.Conventional * rate * accounts
    let eventShare = (e08.Eliminated + e08.Automated + e08.Accelerated) / e08.Conventional
    // Phase II CLM-005: a 180-day full review costs about 3x change-driven monitoring, i.e. monitoring removes 2/3
    Events.combineSequential baseCost [ "event model EV-E08 removal (HI decomposition)", eventShare; "registry change-driven monitoring (CLM-005, 1 - 1/3)", 2.0 / 3.0 ]

// ------------------------------------------------------------------ channel (model 4)

let channelInputs (i: Inputs) (c: Case) : Channel.Inputs =
    { RevenuePerSponsor = pv i.Params c "revenue_per_sponsor"; LifetimeYears = pv i.Params c "licence_life"; PartnerShare = pv i.Params c "partner_share"
      DirectCac = pv i.Params BaseCase "direct_cac"; Enablement = pv i.Params BaseCase "partner_enablement"
      DealsPerPartnerPerYear = pv i.Params BaseCase "partner_deals"; AgreementYears = pv i.Params BaseCase "agreement_years"
      DiscountRate = pv i.Params BaseCase "discount_rate"; SalesCycleMonths = pv i.Params BaseCase "partner_sales_cycle" }

let channelCases (i: Inputs) : (string * Channel.Inputs) list =
    let b = channelInputs i BaseCase
    let p n (sel: Range -> float) = sel i.Params.[n].Range
    [ "small sponsor (revenue low, life low)", { b with RevenuePerSponsor = p "revenue_per_sponsor" (fun r -> r.Low); LifetimeYears = p "licence_life" (fun r -> r.Low) }
      "base", b
      "base at 40% share", { b with PartnerShare = p "partner_share" (fun r -> r.High) }
      "large sponsor (revenue high, life high, direct CAC high)", { b with RevenuePerSponsor = p "revenue_per_sponsor" (fun r -> r.High); LifetimeYears = p "licence_life" (fun r -> r.High); DirectCac = p "direct_cac" (fun r -> r.High) }
      "partner sources no deal", { b with DealsPerPartnerPerYear = 0.0 }
      "100% partner share (boundary)", { b with PartnerShare = 1.0 } ]

/// Break-even partner share by sponsor size and direct CAC.
let breakEvenShareGrid (i: Inputs) =
    let b = channelInputs i BaseCase
    let r = i.Params.["revenue_per_sponsor"].Range
    let l = i.Params.["licence_life"].Range
    let cacs = i.Params.["direct_cac"].Range
    [ for size, rev, life in [ "small", r.Low, l.Low; "base", r.Base, l.Base; "large", r.High, l.High ] do
          for cac in [ cacs.Low; cacs.Base; cacs.High ] do
              let res = Channel.evaluate { b with RevenuePerSponsor = rev; LifetimeYears = life; DirectCac = cac }
              yield size, rev, life, cac, res ]

// ------------------------------------------------------------------ shared infrastructure (model 6)

let pools (i: Inputs) (c: Case) : SharedInfra.Pool list = i.Pools |> List.map (fun p -> { Id = p.Id; Name = p.Name; Annual = cost c p.Annual })

let allocations (i: Inputs) =
    let owner = setting i "allocation_owner" "PRD-UNB"
    [ for rule in [ SharedInfra.Equal; SharedInfra.Usage; SharedInfra.Revenue; SharedInfra.Standalone ] do
          let ps = pools i BaseCase
          yield rule, SharedInfra.allocate rule owner i.Products ps, ps ]

// ------------------------------------------------------------------ response (model 7)

let leanCostBase (i: Inputs) (c: Case) : Response.CostBase =
    let s3 = i.States |> List.find (fun s -> s.StateId = "S3")
    let a = a3Value i c
    { Name = "Phase III lean licensor (AB run + TPSP + control operations + founder draw + registry, governing mode)"
      FixedAnnual = Capital.recurringCash c s3 + (corrections i (registryMode i) c).ExtraLiveAnnual
                    - registryAddableFor i c (registryMode i) (a "accounts_per_customer" * a "charities_per_account") 1.0 + cost c s3.FounderLive.Cash
                    + registryAddableFor i c (registryMode i) (a "accounts_per_customer" * a "charities_per_account") 1.0
      VariablePerAccount = pv i.Params c "var_per_account" }

/// The same with the founder paid at market in cash (REV3005).
let leanCostBaseFounderAtMarket (i: Inputs) (c: Case) : Response.CostBase =
    let b = leanCostBase i c
    let s3 = i.States |> List.find (fun s -> s.StateId = "S3")
    { b with Name = "Lean licensor with founder at market in cash"; FixedAnnual = b.FixedAnnual - cost c s3.FounderLive.Cash + pv i.Params c "founder_econ" }

let md6CostBase (i: Inputs) : Response.CostBase =
    { Name = "Phase II MD-6 technology licensing"; FixedAnnual = pv i.Params BaseCase "md6_fixed"; VariablePerAccount = pv i.Params BaseCase "md6_variable" }

/// Accounts won per year at the A3 sponsor size (customers per year x accounts per customer).
let accountsPerYear (i: Inputs) = pv i.Params BaseCase "customers_per_year_channel" * a3Value i BaseCase "accounts_per_customer"

/// Accounts won per year at sequence H's sponsor size (REV2014: FGJ price-and-size variant).
let accountsPerYearH (i: Inputs) =
    i.Streams |> List.tryFind (fun s -> s.StreamId = "H-UNB")
    |> Option.map (fun s -> s.Values.["customers_per_year"].Base * s.Values.["accounts_per_customer"].Base) |> Option.defaultValue 0.0

let responseResults (i: Inputs) =
    let churn = pv i.Params BaseCase "churn"
    [ for s in i.Scenarios do
          for c in cases do
              let sc: Response.Scenario =
                  { Id = s.Id; Name = s.Name; PriceCut = cost c s.PriceCut; WinRateReduction = cost c s.WinRateReduction
                    PartnerShare = cost c s.PartnerShare; TerminationMonth = s.Termination |> Option.map (gain c) }
              for cb in [ md6CostBase i; leanCostBase i BaseCase ] do
                  for label, acq in [ "A3 size", accountsPerYear i; "H size", accountsPerYearH i ] do
                      yield c, label, Response.evaluate cb (pv i.Params c "headline_price") acq churn sc ]

// ------------------------------------------------------------------ sequences (model 8)

let fundingTerms (i: Inputs) (c: Case) : Sequences.FundingTerms =
    { CustomerImplRecovery = pv i.Params c "customer_impl_recovery"; CustomerAdvanceMonths = pv i.Params c "customer_advance_months"
      PartnerFundedShare = pv i.Params c "partner_funded_share"; PartnerShareUplift = pv i.Params c "partner_share_uplift"
      ExternalCostOfCapital = pv i.Params c "external_cost_of_capital"; ExternalRaiseCost = pv i.Params c "external_raise_cost" }

let seqGlobalFor (i: Inputs) (b: ModelBasis) (mode: string) (c: Case) : Sequences.Global =
    { FounderEcon = pv i.Params c "founder_econ"; CapitalCharge = pv i.Params c "capital_charge"; Contingency = pv i.Params c "contingency"
      RegistryAt = (fun charities sponsors -> registryAddableForB i b c mode charities sponsors)
      RegistryConditionalAt = (fun charities sponsors -> registryAddableForB i b c (registryModeConditional i) charities sponsors)
      RegistryTransferredAt = (fun charities sponsors -> registryTransferredB i b c mode charities sponsors)
      RegistryDefaultCharities = pv i.Params c "registry_charities"
      EligibleSponsors = (fun accounts -> eligibleIn i b.CapSet accounts)
      TaxRate = pv i.Params c "tax_rate"
      CostCenterThreshold = (match System.Double.TryParse(setting i "cost_center_threshold" "0", System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture) with | true, x -> x | _ -> 0.0)
      CostCenterDevCounts = setting i "cost_center_dev_counts" "N" = "Y"
      Basis = b.Engine
      NetControlOverlap = b.Corrected
      FixTpspOverlap = b.Corrected }

let seqGlobalMode (i: Inputs) (mode: string) (c: Case) = seqGlobalFor i (primaryBasis i) mode c
let seqGlobal (i: Inputs) (c: Case) = seqGlobalMode i (registryMode i) c

let streamsOf (i: Inputs) (seqId: string) = i.Streams |> List.filter (fun s -> s.SeqId = seqId)

let runSeq (i: Inputs) (gl: Sequences.Global) (m: Sequences.SequenceMeta) (c: Case) (f: Sequences.Funding) (cc: float option option) =
    Sequences.runCase gl (fundingTerms i c) m (streamsOf i m.SeqId) c f cc

/// Median of the named-partner range (triangular), reported instead of a base equal to the threshold (REV2002).
let triangularMedian (r: Range) = Sampling.triangular r 0.5

/// (meta, kill rule applied, outcome) for every sequence, case and funding variant.
let sequenceOutcomes (i: Inputs) =
    [ for kill in [ true; false ] do
          for m in i.Metas do
              for c in cases do
                  for f in Sequences.fundings do
                      yield m, kill, runSeq i (seqGlobal i c) m c f (if kill then None else Some None) ]

/// Kill-rule sensitivity (OD-P3-03/04): threshold and development-counting variants, and explicit cost-center months.
let killSensitivity (i: Inputs) =
    let gl = seqGlobal i BaseCase
    let variants =
        [ "derived, threshold $0/month, development excluded (base)", gl, None
          "derived, threshold $10k/month", { gl with CostCenterThreshold = 10000.0 }, None
          "derived, threshold $25k/month", { gl with CostCenterThreshold = 25000.0 }, None
          "derived, development counts", { gl with CostCenterDevCounts = true }, None
          "cost center from month 0", gl, Some(Some 0.0)
          "cost center from month 6", gl, Some(Some 6.0)
          "cost center from month 12", gl, Some(Some 12.0)
          "cost center from month 18", gl, Some(Some 18.0)
          "no cost center (inside existing operations)", gl, Some None ]
    [ for m in i.Metas do
          for name, g, cc in variants do
              yield m, name, runSeq i g m BaseCase Sequences.FounderFunded cc
          for np in (if m.NamedPartnerMonth.High > 0.0 then [ 3.0; 6.0; triangularMedian m.NamedPartnerMonth; 12.0 ] else []) do
              let label = if np = triangularMedian m.NamedPartnerMonth then $"named partner at month {num1 np} (median of range)" else $"named partner at month {num0 np}"
              yield m, label, Sequences.runCaseWith gl (fundingTerms i BaseCase) m (streamsOf i m.SeqId) BaseCase Sequences.FounderFunded None (Some np) ]

// ------------------------------------------------------------------ tornado

let private setField (field: string) (value: float) (s: Sequences.StreamInput) =
    if Map.containsKey field s.Values then { s with Values = Map.add field (point value) s.Values } else s

let private scaleField (field: string) (f: float -> float) (s: Sequences.StreamInput) =
    match Map.tryFind field s.Values with
    | Some r -> { s with Values = Map.add field (point (f r.Base)) s.Values }
    | None -> s

type TornadoItem =
    { Variable: string
      Low: string
      High: string
      LowStreams: Sequences.StreamInput list -> Sequences.StreamInput list
      HighStreams: Sequences.StreamInput list -> Sequences.StreamInput list
      LowGlobal: Sequences.Global -> Sequences.Global
      HighGlobal: Sequences.Global -> Sequences.Global }

let tornadoItems (i: Inputs) (streams: Sequences.StreamInput list) : TornadoItem list =
    let s3 = i.States |> List.find (fun s -> s.StateId = "S3")
    let tplRange field = streams |> List.tryPick (fun s -> Map.tryFind field s.Values) |> Option.defaultValue (point 0.0)
    let field name label =
        let r = tplRange name
        let fmt (x: float) = if abs x >= 1000.0 then money x else num2 x
        { Variable = label; Low = fmt r.Low; High = fmt r.High
          LowStreams = List.map (setField name r.Low); HighStreams = List.map (setField name r.High); LowGlobal = id; HighGlobal = id }
    let liveComponent (cat: string) label =
        let l = s3.Recurring |> List.find (fun (n, _) -> n = cat) |> snd
        let d lo = (fun (x: float) -> x + lo - l.Cash.Base)
        { Variable = label; Low = money l.Cash.Low; High = money l.Cash.High
          LowStreams = List.map (scaleField "live_run_annual" (d l.Cash.Low)); HighStreams = List.map (scaleField "live_run_annual" (d l.Cash.High))
          LowGlobal = id; HighGlobal = id }
    let founder = i.Params.["founder_econ"].Range
    let condMode = registryModeConditional i
    let maint = i.Params.["conventional_maintenance_extra"].Range
    [ field "customers_per_year" "customers per year"
      field "accounts_per_customer" "sponsor size (accounts per customer; AUA does not drive licence revenue)"
      field "price_per_account" "licence price per account"
      field "reachable_share" "reachable share of FY2024 sponsors of that size"
      field "charities_per_account" "charities in use per account (registry volume)"
      { Variable = "registry mode " + condMode + " instead of " + registryMode i + " (conditional on OD-CDD-02)"; Low = condMode; High = registryMode i
        LowStreams = id; HighStreams = id; LowGlobal = (fun g -> { g with RegistryAt = (fun ch n -> registryAddableFor i BaseCase condMode ch n) }); HighGlobal = id }
      field "tpsp_annual" "Nacha TPSP audit and fraud monitoring"
      field "control_ops_annual" "control operations (two-approver change control, break-glass, SoD)"
      { Variable = "conventional maintenance (1-2 engineers) added"; Low = "$0"; High = money maint.High
        LowStreams = id; HighStreams = List.map (scaleField "live_run_annual" (fun x -> x + maint.High)); LowGlobal = id; HighGlobal = id }
      field "soc_type2_months" "SOC 2 Type 2 observation before first signing"
      field "first_signing_month" "sales cycle (month of first contract)"
      field "churn" "churn"
      field "partner_share" "partner revenue share"
      field "cac_first" "CAC (first customer)"
      field "cac_later" "CAC (later customers)"
      field "impl_first" "implementation (first customer)"
      field "impl_later" "implementation (later customers)"
      liveComponent "infrastructure" "infrastructure cost"
      liveComponent "compliance_recurring" "regulatory requirements (recurring compliance)"
      liveComponent "support" "support obligations"
      liveComponent "security" "security programme"
      liveComponent "insurance" "insurance"
      field "dev_cash" "development productivity (remaining development cash)"
      field "var_per_account" "variable cost per account (incl. AI processing)"
      { Variable = "tax rate"; Low = pct (i.Params.["tax_rate"].Range.Low); High = pct (i.Params.["tax_rate"].Range.High)
        LowStreams = id; HighStreams = id; LowGlobal = (fun g -> { g with TaxRate = i.Params.["tax_rate"].Range.Low }); HighGlobal = (fun g -> { g with TaxRate = i.Params.["tax_rate"].Range.High }) }
      { Variable = "compensation (founder at market; fully loaded only)"; Low = money founder.Low; High = money founder.High
        LowStreams = id; HighStreams = id; LowGlobal = (fun g -> { g with FounderEcon = founder.Low }); HighGlobal = (fun g -> { g with FounderEcon = founder.High }) }
    ]

type TornadoRow = { Sequence: string; Variable: string; Low: string; High: string; PeakAtLow: float; PeakAtHigh: float; EconAtLow: float; EconAtHigh: float; Swing: float }

let tornado (i: Inputs) (seqId: string) : TornadoRow list =
    let m = i.Metas |> List.find (fun x -> x.SeqId = seqId)
    let streams = streamsOf i seqId
    let gl = seqGlobal i BaseCase
    let terms = fundingTerms i BaseCase
    // uninterrupted: the kill rule would otherwise truncate the adverse end of timing variables
    let eval sts g = Sequences.runCase g terms m sts BaseCase Sequences.FounderFunded (Some None)
    tornadoItems i streams
    |> List.map (fun t ->
        let lo = eval (t.LowStreams streams) (t.LowGlobal gl)
        let hi = eval (t.HighStreams streams) (t.HighGlobal gl)
        let e (o: Sequences.Outcome) = (List.last o.Horizons).CumulativeEconomic
        { Sequence = seqId; Variable = t.Variable; Low = t.Low; High = t.High; PeakAtLow = lo.Summary.PeakDeficit; PeakAtHigh = hi.Summary.PeakDeficit
          EconAtLow = e lo; EconAtHigh = e hi; Swing = abs (lo.Summary.PeakDeficit - hi.Summary.PeakDeficit) })
    |> List.sortByDescending (fun r -> r.Swing, r.Variable)

/// Programme break-even (model 5) tornado over balance (AUA), fee, programme variable cost (grant frequency and
/// exception rates drive it) and fixed cost, for a programme hosted on an existing sponsor.
let mvpTornado (i: Inputs) =
    let fx = i.Mvp.Fixed |> List.find (fun (h, _) -> h = "partner_hosted") |> snd
    let get xs k = xs |> List.find (fun (a, _) -> a = k) |> snd
    let var = i.Mvp.Variable
    let b = i.Mvp.Balances
    let f = i.Mvp.Fees
    let be fixedV varV bal fee = Licensing.breakEven fixedV varV bal fee |> fun (_, n, _) -> n
    let baseArgs = get fx "base", get var "base", b.[1], f.[1]
    let (bf, bv, bb, bfe) = baseArgs
    [ "average balance (AUA per account)", money b.[0], money b.[2], be bf bv b.[0] bfe, be bf bv b.[2] bfe
      "programme fee rate", num2 (f.[0] * 100.0) + "%", num2 (f.[2] * 100.0) + "%", be bf bv bb f.[0], be bf bv bb f.[2]
      "programme variable cost (grant frequency, exception rates, licence)", money (get var "low"), money (get var "high"), be bf (get var "low") bb bfe, be bf (get var "high") bb bfe
      "programme fixed cost", money (get fx "low"), money (get fx "high"), be (get fx "low") bv bb bfe, be (get fx "high") bv bb bfe ]

/// Event system-cost tornado (per account-year, base decomposition) over the rate parameters and the scenario
/// decompositions (exception rates and automation effectiveness move together in HI's pessimistic/optimistic sets).
let eventTornado (i: Inputs) =
    let t = Events.totals "base" i.Events
    let r = eventRates i BaseCase
    let sc rr tt = Events.systemCost rr tt
    let p n = i.Params.[n].Range
    [ "labour rate", money (p "labour_per_minute").Low, money (p "labour_per_minute").High, sc { r with LabourPerMinute = (p "labour_per_minute").Low } t, sc { r with LabourPerMinute = (p "labour_per_minute").High } t
      "automation residual cost (automation effectiveness)", pct (p "automation_residual_share").Low, pct (p "automation_residual_share").High, sc { r with AutomationResidualShare = (p "automation_residual_share").Low } t, sc { r with AutomationResidualShare = (p "automation_residual_share").High } t
      "AI processing cost", pct (p "ai_cost_share").Low, pct (p "ai_cost_share").High, sc { r with AiCostShare = (p "ai_cost_share").Low } t, sc { r with AiCostShare = (p "ai_cost_share").High } t
      "transfer efficiency", num1 (p "transfer_efficiency").Low, num1 (p "transfer_efficiency").High, sc { r with TransferEfficiency = (p "transfer_efficiency").Low } t, sc { r with TransferEfficiency = (p "transfer_efficiency").High } t
      "exception rates and grant activity (HI optimistic/pessimistic decomposition)", "opt", "pess", sc r (Events.totals "opt" i.Events), sc r (Events.totals "pess" i.Events) ]

// ------------------------------------------------------------------ Monte Carlo

type McRow =
    { Sequence: string
      Rho: float
      KillRule: bool
      PeakP10: float
      PeakP50: float
      PeakP90: float
      Cum120P10: float
      Cum120P50: float
      Cum120P90: float
      EconP50: float
      ShareNoPayback: float
      ShareKilled: float
      PaybackP50: float }

let monteCarlo (i: Inputs) (n: int) (seed: uint64) (rho: float) (killRule: bool) (m: Sequences.SequenceMeta) : McRow =
    let streams = streamsOf i m.SeqId
    let vars =
        [ for s in streams do
              for KeyValue(f, r) in s.Values do
                  if r.High > r.Low then yield s.StreamId + "." + f, Sequences.groupOf f, Sequences.adverseOf f ]
        @ (if m.NamedPartnerMonth.High > m.NamedPartnerMonth.Low then [ "named_partner", "demand", HighIsAdverse ] else [])
        @ [ "partner_termination", "", HighIsAdverse ]
    let gl = seqGlobal i BaseCase
    let termRate = pv i.Params BaseCase "partner_termination_rate"
    let g: Cashflow.Globals = { FounderEconAnnual = gl.FounderEcon; CapitalChargeAnnual = gl.CapitalCharge }
    let terms = fundingTerms i BaseCase
    let outcomes =
        Sampling.drawMany n seed rho vars
        |> List.map (fun q ->
            let pick (s: Sequences.StreamInput) = fun field (r: Range) -> match Map.tryFind (s.StreamId + "." + field) q with Some u -> Sampling.triangular r u | None -> r.Base
            let sts = streams |> List.map (fun s -> Sequences.toStream gl (pick s) s) |> Sequences.applyFunding terms Sequences.FounderFunded
            let np = match Map.tryFind "named_partner" q with Some u -> Sampling.triangular m.NamedPartnerMonth u | None -> m.NamedPartnerMonth.Base
            let cc =
                match m.CostCenter with
                | _ when not killRule -> None
                | Sequences.NoCostCenter -> None
                | Sequences.Fixed r -> Some r.Base
                | Sequences.Derived -> Sequences.derivedCostCenter g gl.CostCenterThreshold gl.CostCenterDevCounts sts
            // partner termination hazard (REV2016): exponential time to termination for partner-delivered sequences
            let partnerDelivered = sts |> List.exists (fun s -> s.Dedicated && s.PartnerShare > 0.0)
            let forced =
                match Map.tryFind "partner_termination" q with
                | Some u when partnerDelivered && termRate > 0.0 -> let t = -(log (1.0 - u)) / termRate * 12.0 in if t < 120.0 then Some(max 1 (int (ceil t))) else None
                | _ -> None
            Sequences.simulateWith forced gl.TaxRate g m sts cc np BaseCase Sequences.FounderFunded gl.CapitalCharge)
    let peaks = outcomes |> List.map (fun o -> o.Summary.PeakDeficit)
    let cums = outcomes |> List.map (fun o -> List.last o.Summary.Cumulative)
    let econ = outcomes |> List.map (fun o -> List.last o.Summary.EconomicCumulative)
    let paybacks = outcomes |> List.map (fun o -> match o.Summary.PaybackMonth with Some p -> float p | None -> infinity)
    let nf = float (List.length outcomes)
    { Sequence = m.SeqId; Rho = rho; KillRule = killRule
      PeakP10 = Sampling.percentile 0.1 peaks; PeakP50 = Sampling.percentile 0.5 peaks; PeakP90 = Sampling.percentile 0.9 peaks
      Cum120P10 = Sampling.percentile 0.1 cums; Cum120P50 = Sampling.percentile 0.5 cums; Cum120P90 = Sampling.percentile 0.9 cums
      EconP50 = Sampling.percentile 0.5 econ
      ShareNoPayback = (paybacks |> List.filter System.Double.IsInfinity |> List.length |> float) / nf
      ShareKilled = (outcomes |> List.filter (fun o -> o.Kill.KillMonth.IsSome) |> List.length |> float) / nf
      PaybackP50 = Sampling.percentile 0.5 paybacks }

// ------------------------------------------------------------------ extreme scenarios

type Extreme = { Name: string; Streams: Sequences.StreamInput list -> Sequences.StreamInput list; Global: Sequences.Global -> Sequences.Global; Case: Case; KillOverride: int option }

let extremes (i: Inputs) : Extreme list =
    let all f = List.map f
    let founder = pv i.Params BaseCase "founder_econ"
    let md6 = pv i.Params BaseCase "md6_fixed"
    [ { Name = "base"; Streams = id; Global = id; Case = BaseCase; KillOverride = None }
      { Name = "zero customers ever"; Streams = all (setField "customers_per_year" 0.0); Global = id; Case = BaseCase; KillOverride = None }
      { Name = "100% partner share"; Streams = all (fun s -> { s with Values = Map.add "partner_share" (point 1.0) s.Values }); Global = id; Case = BaseCase; KillOverride = None }
      { Name = "every input adverse"; Streams = id; Global = id; Case = AdverseCase; KillOverride = None }
      { Name = "aggressive incumbent (-30% price, -50% wins) and partner acquired at month 36"
        Streams = all (scaleField "revenue_per_customer" (fun x -> x * 0.7) >> scaleField "price_per_account" (fun x -> x * 0.7) >> scaleField "customers_per_year" (fun x -> x * 0.5)); Global = id; Case = BaseCase; KillOverride = Some 36 }
      { Name = "conventional run rate (Phase II MD-6 fixed cost as live run)"; Streams = all (fun s -> if Map.containsKey "live_run_annual" s.Values && s.Entity = Cashflow.E2Unbound then setField "live_run_annual" md6 s else s); Global = id; Case = BaseCase; KillOverride = None }
      { Name = "SOC 1 Type 2 required (+$120k a year)"; Streams = all (fun s -> if s.Entity = Cashflow.E2Unbound then scaleField "live_run_annual" (fun x -> x + 120000.0) s else s); Global = id; Case = BaseCase; KillOverride = None }
      { Name = "conventional maintenance (1-2 engineers) added"; Streams = all (fun s -> if s.Entity = Cashflow.E2Unbound then scaleField "live_run_annual" (fun x -> x + pv i.Params BaseCase "conventional_maintenance_extra") s else s); Global = id; Case = BaseCase; KillOverride = None }
      { Name = "registry " + registryModeConditional i + " (conditional on OD-CDD-02)"; Streams = id; Global = (fun g -> { g with RegistryAt = (fun ch n -> registryAddableFor i BaseCase (registryModeConditional i) ch n) }); Case = BaseCase; KillOverride = None }
      { Name = "founder paid market salary in cash"; Streams = all (fun s -> if Map.containsKey "founder_fte" s.Values then (setField "founder_cash_pre_annual" (founder * s.Values.["founder_fte"].Base) >> setField "founder_cash_live_annual" (founder * s.Values.["founder_fte"].Base)) s else s); Global = id; Case = BaseCase; KillOverride = None } ]

let runExtremeWith (killRule: bool) (i: Inputs) (m: Sequences.SequenceMeta) (x: Extreme) =
    let gl = x.Global (seqGlobal i x.Case)
    let streams = streamsOf i m.SeqId |> x.Streams
    match x.KillOverride with
    | None -> Sequences.runCase gl (fundingTerms i x.Case) m streams x.Case Sequences.FounderFunded (if killRule then None else Some None)
    | Some k ->
        let g: Cashflow.Globals = { FounderEconAnnual = gl.FounderEcon; CapitalChargeAnnual = gl.CapitalCharge }
        let sts = streams |> List.map (Sequences.toStream gl (Sequences.casePick x.Case))
        Sequences.simulateWith (Some k) gl.TaxRate g m sts None 0.0 x.Case Sequences.FounderFunded gl.CapitalCharge

let runExtreme i m x = runExtremeWith true i m x

// ------------------------------------------------------------------ sponsor size (REV2012, REV3030)

type SizeRow =
    { Accounts: float; NetRevenue: float; Eligible: float; NonCaptive: float; MaxCustomers: float
      Mode: string; Uninterrupted: Sequences.Outcome; WithKill: Sequences.Outcome }

let sizeOverride (accounts: float) (s: Sequences.StreamInput) =
    if Map.containsKey "accounts_per_customer" s.Values && s.Values.["accounts_per_customer"].Base > 0.0
    then { s with Values = Map.add "accounts_per_customer" (point accounts) s.Values } else s

/// Sequence A3 at named sponsor sizes, in the governing and the conditional registry mode.
let sizeTable (i: Inputs) (sizes: float list) : SizeRow list =
    let m = i.Metas |> List.find (fun x -> x.SeqId = "SEQ-A3")
    let price = a3Value i BaseCase "price_per_account"
    let share = a3Value i BaseCase "partner_share"
    let reach = a3Value i BaseCase "reachable_share"
    [ for mode in [ registryMode i; registryModeConditional i ] do
          for a in sizes do
              let gl = seqGlobalMode i mode BaseCase
              let sts = streamsOf i m.SeqId |> List.map (sizeOverride a)
              let run cc = Sequences.runCase gl (fundingTerms i BaseCase) m sts BaseCase Sequences.FounderFunded cc
              let all, nc = eligible i a
              yield { Accounts = a; NetRevenue = a * price * (1.0 - share); Eligible = all; NonCaptive = nc; MaxCustomers = floor (eligibleIn i (primaryBasis i).CapSet a * reach)
                      Mode = mode; Uninterrupted = run (Some None); WithKill = run None } ]

/// Smallest customer size (accounts) at which a sequence has non-negative cumulative cash at month 120, uninterrupted,
/// for a basis and registry configuration; the sponsor-population cap is lifted (pure unit economics). None if not
/// reached below 100,000 accounts. Used for A3 (single sponsor) and PB (partner book).
let breakEvenFor (i: Inputs) (b: ModelBasis) (cfg: string) (seqId: string) : float option =
    let m = i.Metas |> List.find (fun x -> x.SeqId = seqId)
    let gl = { seqGlobalFor i b cfg BaseCase with EligibleSponsors = (fun _ -> infinity) }
    let at a =
        let sts = streamsOf i m.SeqId |> List.map (sizeOverride a)
        List.last (Sequences.runCase gl (fundingTerms i BaseCase) m sts BaseCase Sequences.FounderFunded (Some None)).Summary.Cumulative
    let rec bisect lo hi k = if k = 0 then hi else let mid = (lo + hi) / 2.0 in if at mid >= 0.0 then bisect lo mid (k - 1) else bisect mid hi (k - 1)
    if at 100000.0 < 0.0 then None else Some(ceil (bisect 50.0 100000.0 40))

let breakEvenAccounts (i: Inputs) (mode: string) = breakEvenFor i (primaryBasis i) mode "SEQ-A3"

/// The basis-by-configuration grid (REV4019): which configurations each basis is shown under.
let basisConfigs (i: Inputs) =
    [ revision2, "M1-vendor-2pa"; revision2, registryModeConditional i ]
    @ (registryConfigIds |> List.map (fun c -> revision3, c))

let runFor (i: Inputs) (b: ModelBasis) (cfg: string) (seqId: string) (cc: float option option) =
    let m = i.Metas |> List.find (fun x -> x.SeqId = seqId)
    Sequences.runCase (seqGlobalFor i b cfg BaseCase) (fundingTerms i BaseCase) m (streamsOf i seqId) BaseCase Sequences.FounderFunded cc

/// Kill-rule timing sensitivity for A3 (REV4009): go-live lag x first-signing style x cost-center month.
let killTiming (i: Inputs) =
    let m = i.Metas |> List.find (fun x -> x.SeqId = "SEQ-A3")
    [ for lag in [ 6.0; 8.0; 9.0; 12.0 ] do
          for whole in [ true; false ] do
              for cc in [ 0.0; 6.0; 12.0 ] do
                  let b = primaryBasis i
                  let gl = { seqGlobalFor i b (registryMode i) BaseCase with Basis = { b.Engine with WholeFirstSigning = whole } }
                  let sts = streamsOf i m.SeqId |> List.map (setField "golive_lag" lag)
                  yield lag, whole, cc, Sequences.runCase gl (fundingTerms i BaseCase) m sts BaseCase Sequences.FounderFunded (Some(Some cc)) ]

/// A3 base (uninterrupted) under each population cap set (REV4006).
let capSensitivity (i: Inputs) =
    let m = i.Metas |> List.find (fun x -> x.SeqId = "SEQ-A3")
    [ for cs in capSets do
          let gl = { seqGlobal i BaseCase with EligibleSponsors = (fun a -> eligibleIn i cs a) }
          yield cs, Sequences.runCase gl (fundingTerms i BaseCase) m (streamsOf i m.SeqId) BaseCase Sequences.FounderFunded (Some None) ]
