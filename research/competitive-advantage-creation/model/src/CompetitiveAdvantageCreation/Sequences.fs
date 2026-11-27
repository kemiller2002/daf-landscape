/// Model 8: commercial sequences A-F plus evidence-supported variants, at 12/24/36/60/120 months, with funding
/// variants and the kill rule (OD-P3-02, OD-P3-03, OD-P3-04). Pure.
///
/// Kill rule (Phase II CHL-022, DEC-008): no named partner by month 6, or no referenceable live pilot by month 24,
/// pauses the thesis. OD-P3-03/04: both clocks start at the month DAF commercialization becomes its own cost center
/// (operational definition: the first month in which the sequence needs DAF-specific cash spend booked to its own
/// budget, separate from general Echelon Foundry operations). A sequence run entirely inside existing operations never
/// starts the clock; its founder time still counts in fully loaded cost. OD-P3-02: streams marked kill-exempt
/// (Transitus) continue after a pause.
module CompetitiveAdvantageCreation.Sequences

open CompetitiveAdvantageCreation.Domain
open CompetitiveAdvantageCreation.Cashflow

/// Numeric stream fields and which end is adverse.
let fields : (string * Adverse) list =
    [ "start_month", HighIsAdverse
      "dev_cash", HighIsAdverse
      "dev_econ", HighIsAdverse
      "dev_months", HighIsAdverse
      "onetime_cash", HighIsAdverse
      "onetime_lead_months", LowIsAdverse
      "pre_run_annual", HighIsAdverse
      "live_run_annual", HighIsAdverse
      "founder_fte", HighIsAdverse
      "founder_cash_pre_annual", HighIsAdverse
      "founder_cash_live_annual", HighIsAdverse
      "first_signing_month", HighIsAdverse
      "customers_per_year", LowIsAdverse
      "max_customers", LowIsAdverse
      "revenue_per_customer", LowIsAdverse
      "partner_share", HighIsAdverse
      "variable_share", HighIsAdverse
      "var_per_customer_year", HighIsAdverse
      "cac_first", HighIsAdverse
      "cac_later", HighIsAdverse
      "impl_first", HighIsAdverse
      "impl_later", HighIsAdverse
      "churn", HighIsAdverse
      "golive_lag", HighIsAdverse
      "arrears_months", HighIsAdverse
      // Revision 2 fields
      "accounts_per_customer", LowIsAdverse
      "price_per_account", LowIsAdverse
      "var_per_account", HighIsAdverse
      "charities_per_account", HighIsAdverse
      "reachable_share", LowIsAdverse
      "tpsp_annual", HighIsAdverse
      "control_ops_annual", HighIsAdverse
      "control_ops_pre_share", HighIsAdverse
      "impl_first_count", HighIsAdverse
      "soc_type2_months", HighIsAdverse
      "wind_down_months", HighIsAdverse
      "wind_down_fixed", HighIsAdverse
      "incident_reserve", HighIsAdverse
      "sponsor_conversion_cost", HighIsAdverse
      "founder_build_share", LowIsAdverse
      "registry_charities_per_customer", HighIsAdverse
      // Revision 3 fields
      "control_ops_maintenance_overlap", LowIsAdverse
      "tpsp_overlap_in_live_run", HighIsAdverse ]

let adverseOf name = fields |> List.tryFind (fun (n, _) -> n = name) |> Option.map snd |> Option.defaultValue HighIsAdverse

/// Correlation groups for Monte Carlo (report 19 states why): demand variables move together because they all depend
/// on whether a partner or buyer exists; cost variables move together because buyer assurance requirements raise
/// security, compliance, insurance and implementation at once.
let groupOf name =
    match name with
    | "first_signing_month" | "customers_per_year" | "revenue_per_customer" | "churn" | "golive_lag" | "accounts_per_customer" | "reachable_share" -> "demand"
    | "dev_cash" | "dev_econ" | "onetime_cash" | "pre_run_annual" | "live_run_annual" | "cac_first" | "cac_later" | "impl_first" | "impl_later"
    | "tpsp_annual" | "control_ops_annual" | "soc_type2_months" -> "cost"
    | _ -> ""

type StreamInput =
    { SeqId: string
      StreamId: string
      Name: string
      Entity: Entity
      Dedicated: bool
      KillExempt: bool
      Recurring: bool
      /// "N", "live" (added to the live run), "all" (added to pre-revenue and live run) or "all-conditional" (as
      /// "all" at the conditional registry mode: a data product not bound by the sponsor 180-day human review).
      UsesRegistry: string
      Values: Map<string, Range>
      AssumptionIds: string list }

/// How the cost-center month (OD-P3-04) is set for a sequence.
type CostCenter =
    /// First month with dedicated DAF-specific cash spend above the threshold (Global.CostCenterThreshold).
    | Derived
    /// Run inside existing Echelon operations: the kill-rule clock never starts.
    | NoCostCenter
    | Fixed of Range

type SequenceMeta =
    { SeqId: string
      RegisterId: string
      Label: string
      Name: string
      StartState: string
      NamedPartnerMonth: Range
      CostCenter: CostCenter
      FailureBand: string
      Reversibility: string
      Optionality: string
      Dependencies: string
      OpportunityCost: string
      AssumptionIds: string list }

type Global =
    { FounderEcon: float
      CapitalCharge: float
      Contingency: float
      /// Vendor-run registry cost a year for (charities in use per sponsor, live sponsors) (Registry.addable).
      RegistryAt: float -> float -> float
      /// The same at the conditional mode (OD-CDD-02), used by streams marked "all-conditional".
      RegistryConditionalAt: float -> float -> float
      /// Deep-review labour performed by the sponsor (transferred), for (charities per sponsor, live sponsors).
      RegistryTransferredAt: float -> float -> float
      Basis: Basis
      /// Revision 3: net control operations against the code approvers already in maintenance (REV4005).
      NetControlOverlap: bool
      /// Revision 3: remove the TPSP audit already inside the adverse compliance line (REV4005).
      FixTpspOverlap: bool
      /// Charities in use for registry streams that are not sized by accounts.
      RegistryDefaultCharities: float
      /// FY2024 sponsors (SRC-013 panel) with at least this many accounts.
      EligibleSponsors: float -> float
      TaxRate: float
      CostCenterThreshold: float
      CostCenterDevCounts: bool }

let private v (values: Map<string, Range>) (pickF: string -> Range -> float) name =
    match Map.tryFind name values with
    | Some r -> pickF name r
    | None -> 0.0

/// Build a point stream. pickF chooses a value for each named field (case or Monte Carlo quantile).
/// Revision 2: account-sized streams derive revenue (accounts x price, gross), variable cost (accounts x cost per
/// account) and the reachable customer count (FY2024 sponsors at least that large x reachable share) from one
/// sponsor size, so revenue per customer and the number of such customers are linked (REV2012, REV3030).
let toStream (g: Global) (pickF: string -> Range -> float) (s: StreamInput) : Stream =
    let f = v s.Values pickF
    let accounts = f "accounts_per_customer"
    let revenue = if accounts > 0.0 then accounts * f "price_per_account" else f "revenue_per_customer"
    let reachable = f "reachable_share"
    let capByPopulation = if accounts > 0.0 && reachable > 0.0 then floor (g.EligibleSponsors accounts * reachable) else infinity
    let maxCustomers = min capByPopulation (match Map.tryFind "max_customers" s.Values with Some r -> pickF "max_customers" r | None -> infinity)
    let charities =
        if accounts > 0.0 then accounts * f "charities_per_account"
        elif f "registry_charities_per_customer" > 0.0 then f "registry_charities_per_customer"
        else g.RegistryDefaultCharities
    let usesRegistry = s.UsesRegistry <> "N"
    let registryAt = if s.UsesRegistry = "all-conditional" then g.RegistryConditionalAt else g.RegistryAt
    let control = if g.NetControlOverlap then max 0.0 (f "control_ops_annual" - f "control_ops_maintenance_overlap") else f "control_ops_annual"
    let tpspOverlap = if g.FixTpspOverlap then min (f "tpsp_overlap_in_live_run") (f "tpsp_annual") else 0.0
    let soc = f "soc_type2_months"
    let firstSigning = if soc > 0.0 then max (f "first_signing_month") (f "start_month" + f "dev_months" + soc) else f "first_signing_month"
    { Id = s.StreamId; Name = s.Name; Entity = s.Entity; Dedicated = s.Dedicated; KillExempt = s.KillExempt
      StartMonth = f "start_month"; DevCash = f "dev_cash"; DevEcon = max (f "dev_econ") (f "dev_cash"); DevMonths = f "dev_months"
      OnetimeCash = f "onetime_cash"; OnetimeLeadMonths = f "onetime_lead_months"
      PreRunMonthly = (f "pre_run_annual" + control * f "control_ops_pre_share") / 12.0
      LiveRunMonthly = (f "live_run_annual" + f "tpsp_annual" - tpspOverlap + control) / 12.0
      RegistryAnnualOf = (if usesRegistry then (fun n -> registryAt charities n) else (fun _ -> 0.0))
      RegistryTransferredOf = (if usesRegistry && s.UsesRegistry <> "all-conditional" then (fun n -> g.RegistryTransferredAt charities n) else (fun _ -> 0.0))
      RegistryPreRevenue = (s.UsesRegistry = "all" || s.UsesRegistry = "all-conditional")
      FounderFte = f "founder_fte"; FounderBuildShare = f "founder_build_share"; FounderCashPreMonthly = f "founder_cash_pre_annual" / 12.0
      FounderCashLiveMonthly = f "founder_cash_live_annual" / 12.0; FirstSigningMonth = firstSigning
      CustomersPerYear = f "customers_per_year"; MaxCustomers = maxCustomers
      RevenuePerCustomer = revenue; Recurring = s.Recurring; PartnerShare = min 1.0 (f "partner_share")
      VariableShare = f "variable_share"; VarPerCustomerYear = f "var_per_customer_year" + accounts * f "var_per_account"
      CacFirst = f "cac_first"; CacLater = f "cac_later"
      ImplFirst = f "impl_first"; ImplLater = f "impl_later"; ImplFirstCount = max 1.0 (f "impl_first_count"); ImplRecovery = 0.0
      SponsorConversionPerCustomer = f "sponsor_conversion_cost"; IncidentReserve = f "incident_reserve"
      WindDownFixed = f "wind_down_fixed"; WindDownRunMonths = f "wind_down_months"
      Churn = f "churn"; GoLiveLag = f "golive_lag"; ArrearsMonths = f "arrears_months"; Contingency = g.Contingency; Basis = g.Basis }

let casePick (c: Case) = fun name r -> pickCase c (adverseOf name) r

type Funding =
    | FounderFunded
    | CustomerFunded
    | PartnerFunded
    | ExternallyFunded

let fundingName f =
    match f with
    | FounderFunded -> "founder-funded"
    | CustomerFunded -> "customer-funded"
    | PartnerFunded -> "partner-funded"
    | ExternallyFunded -> "externally funded"

let fundings = [ FounderFunded; CustomerFunded; PartnerFunded; ExternallyFunded ]

type FundingTerms =
    { CustomerImplRecovery: float
      CustomerAdvanceMonths: float
      PartnerFundedShare: float
      PartnerShareUplift: float
      ExternalCostOfCapital: float
      ExternalRaiseCost: float }

/// Apply a funding variant to dedicated revenue streams. Externally funded leaves cash flows unchanged except the
/// raise cost; its cost of capital replaces the capital charge in the economic view.
let applyFunding (t: FundingTerms) (f: Funding) (streams: Stream list) : Stream list =
    match f with
    | FounderFunded -> streams
    | CustomerFunded ->
        // Revision 2 (REV3031): only where Echelon bills the customer; a partner that bills and remits is not changed
        streams |> List.map (fun s -> if s.Dedicated && s.RevenuePerCustomer > 0.0 && s.PartnerShare = 0.0 then { s with ImplRecovery = t.CustomerImplRecovery; ArrearsMonths = -t.CustomerAdvanceMonths } else s)
    | PartnerFunded ->
        streams
        |> List.map (fun s ->
            if s.Dedicated && s.Entity = E2Unbound then
                let funded = t.PartnerFundedShare * (s.DevCash + s.OnetimeCash)
                { s with
                    DevCash = s.DevCash * (1.0 - t.PartnerFundedShare)
                    DevEcon = s.DevEcon - t.PartnerFundedShare * s.DevCash
                    OnetimeCash = s.OnetimeCash * (1.0 - t.PartnerFundedShare)
                    PartnerShare = min 1.0 (s.PartnerShare + (if funded > 0.0 then t.PartnerShareUplift else 0.0)) }
            else s)
    | ExternallyFunded ->
        match streams with
        | first :: rest -> { first with OnetimeCash = first.OnetimeCash + t.ExternalRaiseCost } :: rest
        | [] -> []

type Kill =
    { CostCenterMonth: float option
      NamedPartnerMonth: float
      PilotMonth: int option
      KillMonth: int option
      Reason: string }

/// Named-partner test (CHL-022): passes when a partner is named no later than cost-center month + 6 (inclusive).
/// Revision 2: the comparison is explicit, and results are reported at named-partner months 3, 6 and 12 and at the
/// median of the assumed range rather than relying on a base value equal to the threshold (REV2002).
let namedInTime (costCenter: float) (namedPartner: float) = namedPartner <= costCenter + 6.0

/// Kill decision from the cost-center month T, named-partner month N and the referenceable pilot month P (the first
/// month in which one whole Unbound sponsor customer is live; its buyer security review is passed at contract,
/// which the SOC 2 Type 2 lag before first signing provides; REV2001, REV2044).
let killDecision (t: float option) (namedPartner: float) (pilot: int option) : Kill =
    match t with
    | None -> { CostCenterMonth = None; NamedPartnerMonth = namedPartner; PilotMonth = pilot; KillMonth = None; Reason = "clock not started (inside existing operations)" }
    | Some tc ->
        let k1 = int (ceil (tc + 6.0))
        let k2 = int (ceil (tc + 24.0))
        if not (namedInTime tc namedPartner) then
            { CostCenterMonth = t; NamedPartnerMonth = namedPartner; PilotMonth = pilot; KillMonth = Some k1; Reason = "no named partner by cost-center month + 6" }
        else
            match pilot with
            | Some p when float p <= tc + 24.0 -> { CostCenterMonth = t; NamedPartnerMonth = namedPartner; PilotMonth = pilot; KillMonth = None; Reason = "passes" }
            | _ -> { CostCenterMonth = t; NamedPartnerMonth = namedPartner; PilotMonth = pilot; KillMonth = Some k2; Reason = "no referenceable live pilot by cost-center month + 24" }

/// First month with one whole live customer on a dedicated Unbound (E2) stream.
let pilotMonth (pairs: (Stream * Month list) list) : int option =
    pairs
    |> List.filter (fun (s, _) -> s.Dedicated && s.Entity = E2Unbound)
    |> List.choose (fun (_, ms) -> ms |> List.tryFind (fun m -> m.CumGoLive >= 1.0 - 1e-9) |> Option.map (fun m -> m.M))
    |> function [] -> None | xs -> Some(List.min xs)

/// Cost-center month derived from the streams: first month with dedicated cash spend above a monthly threshold
/// (development counted only if devCounts). None if no dedicated stream ever spends above the threshold.
let derivedCostCenter (g: Globals) (threshold: float) (devCounts: bool) (streams: Stream list) : float option =
    let dedicated = streams |> List.filter (fun s -> s.Dedicated)
    if List.isEmpty dedicated then None
    else
        let ms = dedicated |> List.map (fun s -> flows g s None) |> combine
        ms
        |> List.tryFind (fun m -> (m.CashCost - (if devCounts then 0.0 else m.DevCash + m.Contingency) - m.FounderCash) > threshold)
        |> Option.map (fun m -> float (m.M - 1))

type Horizon =
    { Month: int
      CumulativeCash: float
      PeakDeficitToDate: float
      FullyLoadedCost: float
      CumulativeEconomic: float
      Cac: float
      Development: float
      Implementation: float
      Revenue: float
      GrossMargin: float option
      WorkingCapital: float
      LiveCustomers: float
      Signed: float }

type Outcome =
    { SeqId: string
      Case: Case
      Funding: Funding
      Kill: Kill
      Summary: Summary
      Horizons: Horizon list
      CacPerCustomer: float option
      FirstRevenueMonth: int option
      SustainabilityMonth: int option
      MonthsOfFounderTime: float
      /// Sponsor-side conversion labour (transferred work; reported, never in Echelon cost).
      TransferredToSponsor: float }

let horizons = [ 12; 24; 36; 60; 120 ]

let private horizonAt (ms: Month array) (sm: Summary) (h: int) : Horizon =
    let upto = ms.[0 .. h - 1]
    let sum f = upto |> Array.sumBy f
    let rev = sum (fun m -> m.VendorRevenue)
    let var = sum (fun m -> m.Variable)
    let cum = sm.Cumulative |> List.item (h - 1)
    let charges = sm.CapitalCharge |> List.take h |> List.sum
    { Month = h
      CumulativeCash = cum
      PeakDeficitToDate = -(List.min (0.0 :: (sm.Cumulative |> List.take h)))
      FullyLoadedCost = sum (fun m -> m.CashCost + m.DevNonCash + m.FounderNonCash) + charges
      CumulativeEconomic = sm.EconomicCumulative |> List.item (h - 1)
      Cac = sum (fun m -> m.Cac)
      Development = sum (fun m -> m.DevCash)
      Implementation = sum (fun m -> m.Impl)
      Revenue = rev
      GrossMargin = if rev > 0.0 then Some((rev - var) / rev) else None
      WorkingCapital = ms.[h - 1].Receivable
      LiveCustomers = ms.[h - 1].Live
      Signed = sum (fun m -> m.Signed) }

/// Simulate a sequence at point values. costCenter overrides the meta's cost-center month when given.
let simulateWith (forced: int option) (taxRate: float) (g: Globals) (meta: SequenceMeta) (streams: Stream list) (costCenter: float option) (namedPartner: float) (c: Case) (f: Funding) (capitalCharge: float) : Outcome =
    let unkilled = streams |> List.map (fun s -> flows g s None)
    let pilot = pilotMonth (List.zip streams unkilled)
    let rule = killDecision costCenter namedPartner pilot
    // a forced stop (partner acquired or terminated) applies when earlier than the kill rule's pause
    let kill =
        match forced, rule.KillMonth with
        | Some k, Some r when r <= k -> rule
        | Some k, _ -> { rule with KillMonth = Some k; Reason = "revenue terminated (partner acquired or terminated)" }
        | None, _ -> rule
    let ms = streams |> List.map (fun s -> flows g s kill.KillMonth) |> combine |> applyTax taxRate
    let sm = summarize { g with CapitalChargeAnnual = capitalCharge } ms
    let arr = Array.ofList ms
    let signed = arr |> Array.sumBy (fun m -> m.Signed)
    let cac = arr |> Array.sumBy (fun m -> m.Cac)
    { SeqId = meta.SeqId; Case = c; Funding = f; Kill = kill; Summary = sm
      Horizons = horizons |> List.map (horizonAt arr sm)
      CacPerCustomer = if signed > 0.0 then Some(cac / signed) else None
      FirstRevenueMonth = sm.FirstRevenueMonth
      SustainabilityMonth = sm.OperatingBreakEvenMonth
      MonthsOfFounderTime = arr |> Array.sumBy (fun m -> if g.FounderEconAnnual > 0.0 then (m.FounderCash + m.FounderNonCash) / (g.FounderEconAnnual / 12.0) else 0.0)
      TransferredToSponsor = arr |> Array.sumBy (fun m -> m.TransferredToSponsor) }

let simulate taxRate g meta streams costCenter namedPartner c f capitalCharge = simulateWith None taxRate g meta streams costCenter namedPartner c f capitalCharge

/// Case run with the sequence's own cost-center and named-partner months (either may be overridden).
let runCaseWith (gl: Global) (terms: FundingTerms) (meta: SequenceMeta) (inputs: StreamInput list) (c: Case) (f: Funding) (costCenterOverride: float option option) (namedPartnerOverride: float option) : Outcome =
    let g = { FounderEconAnnual = gl.FounderEcon; CapitalChargeAnnual = gl.CapitalCharge }
    let streams = inputs |> List.map (toStream gl (casePick c)) |> applyFunding terms f
    let cc =
        match costCenterOverride, meta.CostCenter with
        | Some o, _ -> o
        | None, NoCostCenter -> None
        | None, Fixed r -> Some(cost c r)
        | None, Derived -> derivedCostCenter g gl.CostCenterThreshold gl.CostCenterDevCounts streams
    let charge = if f = ExternallyFunded then terms.ExternalCostOfCapital else gl.CapitalCharge
    simulate gl.TaxRate g meta streams cc (defaultArg namedPartnerOverride (cost c meta.NamedPartnerMonth)) c f charge

let runCase gl terms meta inputs c f costCenterOverride = runCaseWith gl terms meta inputs c f costCenterOverride None
