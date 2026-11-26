/// Monthly cash and economic (fully loaded) flows for one revenue stream. Used by the capital model (Unbound by
/// state) and the commercial-sequence model. Pure: a fold over months 1..horizon.
///
/// Conventions (documented in report 18):
/// - cash = money leaving or entering Echelon Foundry's bank account; economic = cash with development at market
///   value instead of its cash cost, founder time at market instead of the founder's cash draw, plus a capital charge
///   on the running cash deficit. Fully loaded = cash + non-cash, by construction.
/// - revenue is gross customer billing; the partner share is deducted before the vendor recognizes revenue, so a
///   channel share is never also counted as a variable cost (see Phase2Check for the Phase II ER-7 question);
///   variable cost is charged on gross volume, so it does not fall when the partner share rises (Revision 2).
/// - working capital is the receivable created by billing in arrears; it is not a separate one-time lump.
module CompetitiveAdvantageCreation.Cashflow

let horizon = 120

/// Economic entity a stream belongs to (echelon-organization-administration strategy/daf-entry/02).
type Entity =
    | E1EchelonFoundry
    | E2Unbound
    | E3CustomerProgramme
    | E4ServicingOrganization
    | E5SharedComponents

let entityCode e =
    match e with
    | E1EchelonFoundry -> "E1"
    | E2Unbound -> "E2"
    | E3CustomerProgramme -> "E3"
    | E4ServicingOrganization -> "E4"
    | E5SharedComponents -> "E5"

let parseEntity (s: string) =
    match s.Trim() with
    | "E1" -> Ok E1EchelonFoundry
    | "E2" -> Ok E2Unbound
    | "E3" -> Ok E3CustomerProgramme
    | "E4" -> Ok E4ServicingOrganization
    | "E5" -> Ok E5SharedComponents
    | x -> Error $"unknown entity '{x}'"

/// Modelling basis switches (Revision 3). `revision2` reproduces the published revision-2 numbers; `revision3`
/// applies the round-2 review corrections (REV4002, REV4007, REV4009, REV4010).
type Basis =
    { /// Contingency applies to one-time and pre-revenue cash and to run and registry cost only in the first N live
      /// months (P3-ASM-AB027 basis); infinity = every live month (revision 2).
      ContingencyLiveMonths: float
      /// At a pause before any customer is live, wind-down is charged at the pre-revenue run (revision 3).
      WindDownAtPreRunIfNotLive: bool
      /// The population cap limits concurrent live customers plus pipeline (churned customers can be replaced);
      /// false = cumulative signings (revision 2).
      CapOnLive: bool
      /// The first customer signs as one whole unit; later signings follow the rate after 12/rate months.
      WholeFirstSigning: bool }

let revision2Basis = { ContingencyLiveMonths = infinity; WindDownAtPreRunIfNotLive = false; CapOnLive = false; WholeFirstSigning = false }
let revision3Basis = { ContingencyLiveMonths = 12.0; WindDownAtPreRunIfNotLive = true; CapOnLive = true; WholeFirstSigning = true }

/// One stream at point values (a case or a Monte Carlo draw has already been chosen).
type Stream =
    { Id: string
      Name: string
      Entity: Entity
      /// Spend counts towards the DAF-commercialization cost center (OD-P3-03/04) and is subject to the kill rule.
      Dedicated: bool
      /// Not stopped by the kill rule (OD-P3-02: Transitus).
      KillExempt: bool
      StartMonth: float
      DevCash: float
      DevEcon: float
      DevMonths: float
      OnetimeCash: float
      /// Months before the first signing at which the one-time cost is paid (0 = at the stream's start).
      OnetimeLeadMonths: float
      PreRunMonthly: float
      LiveRunMonthly: float
      /// Vendor-run charity registry cost a year as a function of live sponsors (Revision 2: scales with sponsors).
      RegistryAnnualOf: float -> float
      /// Deep-review labour the sponsor performs (transferred work; reported, never Echelon cost), by live sponsors.
      RegistryTransferredOf: float -> float
      /// Registry also runs before the first go-live (charity-intelligence products).
      RegistryPreRevenue: bool
      FounderFte: float
      /// Share of founder time during development months that is build work already priced inside DevEcon.
      FounderBuildShare: float
      FounderCashPreMonthly: float
      FounderCashLiveMonthly: float
      FirstSigningMonth: float
      CustomersPerYear: float
      MaxCustomers: float
      RevenuePerCustomer: float
      Recurring: bool
      PartnerShare: float
      /// Share of gross customer billing (Revision 2: charged on gross volume, before the partner share).
      VariableShare: float
      VarPerCustomerYear: float
      CacFirst: float
      CacLater: float
      ImplFirst: float
      ImplLater: float
      /// Number of customers charged the first-customer implementation rate (Revision 2: 3, REV3038).
      ImplFirstCount: float
      ImplRecovery: float
      /// Sponsor-side conversion labour per signed customer: transferred work, reported, never an Echelon cost.
      SponsorConversionPerCustomer: float
      /// Incident-retention reserve set aside at the first go-live (agent AB, P3-ASM-AB023).
      IncidentReserve: float
      /// Wind-down when the kill rule pauses a stream that has signed a customer: fixed cost plus months of live run.
      WindDownFixed: float
      WindDownRunMonths: float
      Churn: float
      GoLiveLag: float
      ArrearsMonths: float
      Contingency: float
      Basis: Basis }

type Globals =
    { FounderEconAnnual: float
      CapitalChargeAnnual: float }

type Month =
    { M: int
      Signed: float
      GoLive: float
      CumGoLive: float
      Live: float
      Revenue: float
      PartnerCut: float
      VendorRevenue: float
      Collected: float
      Receivable: float
      Variable: float
      Run: float
      Registry: float
      DevCash: float
      DevNonCash: float
      Onetime: float
      Contingency: float
      Cac: float
      Impl: float
      Reserve: float
      WindDown: float
      Tax: float
      FounderCash: float
      FounderNonCash: float
      TransferredToSponsor: float
      CashCost: float
      Net: float }

type private St = { Signed: float; Live: float; Pipeline: float list; CumGoLive: float; FirstSignedAt: int option }

type private Acc = { M: int; Signing: float; GoLive: float; Live: float; SignedBefore: float; CumGoLive: float; Killed: bool }

/// Signings in a month. Revision 3: the first customer signs whole, and the rate resumes 12/rate months later so the
/// cumulative count matches the rate; the cap applies to live customers plus pipeline when CapOnLive.
let private signingsAt (s: Stream) (st: St) (m: int) (killed: bool) =
    let eligible = not killed && float m > s.FirstSigningMonth
    let capUsed = if s.Basis.CapOnLive then st.Live + List.sum st.Pipeline else st.Signed
    let room = max 0.0 (s.MaxCustomers - capUsed)
    if not eligible || room <= 0.0 || s.CustomersPerYear <= 0.0 then 0.0
    elif s.Basis.WholeFirstSigning then
        match st.FirstSignedAt with
        | None -> min 1.0 room
        | Some f -> if float (m - f) >= 12.0 / s.CustomersPerYear then min (s.CustomersPerYear / 12.0) room else 0.0
    else min (s.CustomersPerYear / 12.0) room

/// Accrued monthly volumes before collection timing. Pure fold.
let private accrue (s: Stream) (killAt: int option) : Acc list =
    let lag = max 0 (int (round s.GoLiveLag))
    let step (st: St) (m: int) =
        let killed = (match killAt with Some k -> m > k | None -> false) && not s.KillExempt
        let signing = signingsAt s st m killed
        let pipeline = st.Pipeline @ [ signing ]
        let goLive, pending = if pipeline.Length > lag then pipeline.Head, pipeline.Tail else 0.0, pipeline
        let goLive = if killed then 0.0 else goLive
        let live = if killed then 0.0 else st.Live * (1.0 - s.Churn / 12.0) + goLive
        let cum = st.CumGoLive + goLive
        { M = m; Signing = signing; GoLive = goLive; Live = live; SignedBefore = st.Signed; CumGoLive = cum; Killed = killed },
        { Signed = st.Signed + signing; Live = live; Pipeline = pending; CumGoLive = cum
          FirstSignedAt = (match st.FirstSignedAt with None when signing > 0.0 -> Some m | x -> x) }
    [ 1..horizon ] |> List.mapFold step { Signed = 0.0; Live = 0.0; Pipeline = []; CumGoLive = 0.0; FirstSignedAt = None } |> fst

/// Portion of this month's signings that fall below a cumulative count (for first-customer rates).
let firstPortion (signedBefore: float) (signing: float) (count: float) = max 0.0 (min signing (count - signedBefore))

/// Monthly flows for a stream under an optional kill month (streams not kill-exempt stop after it).
let flows (g: Globals) (s: Stream) (killAt: int option) : Month list =
    let acc = accrue s killAt
    let revenueOf (a: Acc) = if s.Recurring then a.Live * s.RevenuePerCustomer / 12.0 else a.GoLive * s.RevenuePerCustomer
    let vendorRev = acc |> List.map (fun a -> revenueOf a * (1.0 - s.PartnerShare)) |> Array.ofList
    // collected(m) = vendor revenue accrued at month m - arrears (negative arrears = billing in advance)
    let shift = int (round s.ArrearsMonths)
    let collectedAt m = let i = m - 1 - shift in if i >= 0 && i < vendorRev.Length then vendorRev.[i] else 0.0
    let devMonths = max 1.0 s.DevMonths
    let firstLiveMonth = acc |> List.tryFind (fun a -> a.GoLive > 0.0) |> Option.map (fun a -> a.M)
    let onetimeMonth =
        if s.OnetimeLeadMonths > 0.0 && not (System.Double.IsInfinity s.FirstSigningMonth) then max (floor s.StartMonth + 1.0) (floor s.FirstSigningMonth + 1.0 - s.OnetimeLeadMonths)
        else floor s.StartMonth + 1.0
    let signedBy m = acc |> List.filter (fun a -> a.M <= m) |> List.sumBy (fun a -> a.Signing)
    let rows, _ =
        acc
        |> List.mapFold
            (fun (cumAccrued, cumCollected) (a: Acc) ->
                let m = a.M
                let mf = float m
                let active = mf > s.StartMonth && not a.Killed
                let isLive = match firstLiveMonth with Some f -> m >= f | None -> false
                let revenue = revenueOf a
                let vr = vendorRev.[m - 1]
                let collected = if a.Killed then 0.0 else collectedAt m
                let cumA = cumAccrued + vr
                let cumC = cumCollected + collected
                let inDev = active && mf <= s.StartMonth + devMonths
                let devCash = if inDev then s.DevCash / devMonths else 0.0
                let devNonCash = if inDev then (s.DevEcon - s.DevCash) / devMonths else 0.0
                let onetime = if active && mf = onetimeMonth then s.OnetimeCash else 0.0
                let run = if not active then 0.0 elif isLive then s.LiveRunMonthly else s.PreRunMonthly
                let registry =
                    if not active then 0.0
                    elif isLive then s.RegistryAnnualOf (max 1.0 a.Live) / 12.0
                    elif s.RegistryPreRevenue then s.RegistryAnnualOf 1.0 / 12.0
                    else 0.0
                let firstCac = firstPortion a.SignedBefore a.Signing 1.0
                let cac = firstCac * s.CacFirst + (a.Signing - firstCac) * s.CacLater
                let firstImpl = firstPortion a.SignedBefore a.Signing (max 1.0 s.ImplFirstCount)
                let impl = (firstImpl * s.ImplFirst + (a.Signing - firstImpl) * s.ImplLater) * (1.0 - s.ImplRecovery)
                let reserve = if active && Some m = firstLiveMonth then s.IncidentReserve else 0.0
                let liveBy k = match firstLiveMonth with Some f -> f <= k | None -> false
                let windDown =
                    match killAt with
                    | Some k when m = k && not s.KillExempt && signedBy k > 0.0 ->
                        let runBase = if s.Basis.WindDownAtPreRunIfNotLive && not (liveBy k) then s.PreRunMonthly else s.LiveRunMonthly
                        s.WindDownFixed + s.WindDownRunMonths * runBase
                    | _ -> 0.0
                let liveMonthIndex = match firstLiveMonth with Some f when m >= f -> float (m - f + 1) | _ -> 0.0
                let recurringInBase = if not isLive || liveMonthIndex <= s.Basis.ContingencyLiveMonths then run + registry else 0.0
                let contingency = s.Contingency * (devCash + onetime + recurringInBase + cac + impl + reserve)
                let transferredReview = if active && isLive then s.RegistryTransferredOf (max 1.0 a.Live) / 12.0 else 0.0
                let variable = if a.Killed then 0.0 else revenue * s.VariableShare + a.Live * s.VarPerCustomerYear / 12.0
                let founderCash = if not active then 0.0 elif isLive then s.FounderCashLiveMonthly else s.FounderCashPreMonthly
                let founderEcon = if active then s.FounderFte * g.FounderEconAnnual / 12.0 * (if inDev then 1.0 - s.FounderBuildShare else 1.0) else 0.0
                let cashCost = variable + run + registry + devCash + onetime + contingency + cac + impl + reserve + windDown + founderCash
                { M = m; Signed = a.Signing; GoLive = a.GoLive; CumGoLive = a.CumGoLive; Live = a.Live; Revenue = revenue
                  PartnerCut = revenue - vr; VendorRevenue = vr; Collected = collected; Receivable = cumA - cumC
                  Variable = variable; Run = run; Registry = registry; DevCash = devCash; DevNonCash = devNonCash; Onetime = onetime
                  Contingency = contingency; Cac = cac; Impl = impl; Reserve = reserve; WindDown = windDown; Tax = 0.0
                  FounderCash = founderCash; FounderNonCash = founderEcon - founderCash
                  TransferredToSponsor = a.Signing * s.SponsorConversionPerCustomer + transferredReview
                  CashCost = cashCost; Net = collected - cashCost },
                (cumA, cumC))
            (0.0, 0.0)
    rows

let private zeroMonth m =
    { M = m; Signed = 0.0; GoLive = 0.0; CumGoLive = 0.0; Live = 0.0; Revenue = 0.0; PartnerCut = 0.0; VendorRevenue = 0.0; Collected = 0.0
      Receivable = 0.0; Variable = 0.0; Run = 0.0; Registry = 0.0; DevCash = 0.0; DevNonCash = 0.0; Onetime = 0.0; Contingency = 0.0
      Cac = 0.0; Impl = 0.0; Reserve = 0.0; WindDown = 0.0; Tax = 0.0; FounderCash = 0.0; FounderNonCash = 0.0; TransferredToSponsor = 0.0
      CashCost = 0.0; Net = 0.0 }

/// Sum several streams month by month.
let combine (streams: Month list list) : Month list =
    let add (a: Month) (b: Month) =
        { a with
            Signed = a.Signed + b.Signed; GoLive = a.GoLive + b.GoLive; CumGoLive = a.CumGoLive + b.CumGoLive; Live = a.Live + b.Live
            Revenue = a.Revenue + b.Revenue; PartnerCut = a.PartnerCut + b.PartnerCut; VendorRevenue = a.VendorRevenue + b.VendorRevenue
            Collected = a.Collected + b.Collected; Receivable = a.Receivable + b.Receivable; Variable = a.Variable + b.Variable
            Run = a.Run + b.Run; Registry = a.Registry + b.Registry; DevCash = a.DevCash + b.DevCash; DevNonCash = a.DevNonCash + b.DevNonCash
            Onetime = a.Onetime + b.Onetime; Contingency = a.Contingency + b.Contingency; Cac = a.Cac + b.Cac; Impl = a.Impl + b.Impl
            Reserve = a.Reserve + b.Reserve; WindDown = a.WindDown + b.WindDown; Tax = a.Tax + b.Tax
            FounderCash = a.FounderCash + b.FounderCash; FounderNonCash = a.FounderNonCash + b.FounderNonCash
            TransferredToSponsor = a.TransferredToSponsor + b.TransferredToSponsor
            CashCost = a.CashCost + b.CashCost; Net = a.Net + b.Net }
    let arrays = streams |> List.map Array.ofList
    [ 1..horizon ] |> List.map (fun m -> arrays |> List.map (fun s -> s.[m - 1]) |> List.fold add (zeroMonth m))

/// Income tax on the combined entity's cash result with full loss carry-forward: tax is due only on cumulative
/// pre-tax cash above its previous high-water mark (a simplification of NOL use; payroll and sales taxes are not
/// modelled: SaaS sales tax is collected and remitted, and founder payroll tax is inside the founder draw).
let applyTax (rate: float) (ms: Month list) : Month list =
    ms
    |> List.mapFold
        (fun (cumPre, highWater) (m: Month) ->
            let cum = cumPre + m.Net
            let taxable = max 0.0 (cum - max 0.0 highWater)
            let tax = rate * taxable
            { m with Tax = tax; CashCost = m.CashCost + tax; Net = m.Net - tax }, (cum, max highWater cum))
        (0.0, 0.0)
    |> fst

/// Summary measures of a combined monthly series.
type Summary =
    { FirstRevenueMonth: int option
      FirstGoLiveMonth: int option
      PeakDeficit: float
      PeakDeficitMonth: int
      PaybackMonth: int option
      DiscountedPaybackMonth: int option
      OperatingBreakEvenMonth: int option
      PeakEconomicDeficit: float
      EconomicPaybackMonth: int option
      Cumulative: float list
      EconomicCumulative: float list
      CapitalCharge: float list }

/// Economic view: cash net minus non-cash development and founder time, minus a capital charge on the running
/// cash deficit (charged monthly at the annual rate / 12). Discounted payback uses the capital-charge rate.
let summarize (g: Globals) (ms: Month list) : Summary =
    let cum = ms |> List.scan (fun a m -> a + m.Net) 0.0 |> List.tail
    let charges = cum |> List.map (fun c -> max 0.0 (-c) * g.CapitalChargeAnnual / 12.0)
    let econNet = List.map2 (fun (m: Month) ch -> m.Net - m.DevNonCash - m.FounderNonCash - ch) ms charges
    let econCum = econNet |> List.scan (+) 0.0 |> List.tail
    let discounted = ms |> List.mapi (fun k m -> m.Net / ((1.0 + g.CapitalChargeAnnual) ** (float (k + 1) / 12.0))) |> List.scan (+) 0.0 |> List.tail
    let trough = List.min (0.0 :: cum)
    let troughIdx = cum |> List.tryFindIndex (fun c -> c = trough) |> Option.defaultValue 0
    let payback xs troughAt = xs |> List.indexed |> List.skip troughAt |> List.tryFind (fun (_, c) -> c >= 0.0) |> Option.map (fun (i, _) -> i + 1)
    let eTrough = List.min (0.0 :: econCum)
    let eIdx = econCum |> List.tryFindIndex (fun c -> c = eTrough) |> Option.defaultValue 0
    let dTrough = List.min (0.0 :: discounted)
    let dIdx = discounted |> List.tryFindIndex (fun c -> c = dTrough) |> Option.defaultValue 0
    let arr = Array.ofList ms
    // first month with revenue from which monthly net cash never turns negative again
    let lastNegative = arr |> Array.tryFindIndexBack (fun m -> m.Net < 0.0)
    let opBe =
        match lastNegative with
        | None -> arr |> Array.tryFind (fun m -> m.VendorRevenue > 0.0) |> Option.map (fun m -> m.M)
        | Some i when i + 1 < arr.Length && arr.[i + 1].VendorRevenue > 0.0 -> Some(i + 2)
        | Some _ -> None
    { FirstRevenueMonth = ms |> List.tryFind (fun m -> m.VendorRevenue > 0.0) |> Option.map (fun m -> m.M)
      FirstGoLiveMonth = ms |> List.tryFind (fun m -> m.GoLive > 0.0) |> Option.map (fun m -> m.M)
      PeakDeficit = -trough
      PeakDeficitMonth = troughIdx + 1
      PaybackMonth = if trough < 0.0 then payback cum troughIdx else None
      DiscountedPaybackMonth = if dTrough < 0.0 then payback discounted dIdx else None
      OperatingBreakEvenMonth = opBe
      PeakEconomicDeficit = -eTrough
      EconomicPaybackMonth = if eTrough < 0.0 then payback econCum eIdx else None
      Cumulative = cum
      EconomicCumulative = econCum
      CapitalCharge = charges }
