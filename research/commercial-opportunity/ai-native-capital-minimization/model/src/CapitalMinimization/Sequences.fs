/// Development and commercial sequences A-G as monthly cash-flow plans over outcome-designed organizations, plus
/// failure modifiers ("cost of being wrong"). Pure functions; months are 0-based from formation. Every timing and
/// amount in the sequence definitions is [A].
module CapitalMinimization.Sequences

open ServicingEconomics.Domain
open ServicingEconomics.Economics
open ServicingEconomics.Parameters
open CapitalMinimization.Design
open CapitalMinimization.Designs
open CapitalMinimization.Development
open CapitalMinimization.Layers

type Customer =
    { Sponsor: Sponsor
      SignMonth: int
      OnboardingMonths: int
      ImplementationFee: float }

type Sequence =
    { Name: string
      /// Organization in force from a month (staged growth); the latest stage at or before a month applies.
      Stages: (int * Design) list
      Price: Price
      /// Handling minutes per account-year once redesign gates are in place, and before (first months live).
      Target: float
      EarlyTarget: float
      RedesignLagMonths: int
      Customers: Customer list
      OneTime: (int * string * float) list
      /// Other cash income (software licences, standalone services, design-partner fees) by month.
      OtherIncome: (int * string * float) list
      /// Other recurring monthly costs outside the design (start month, name, monthly amount).
      Recurring: (int * string * float) list
      /// Platform layers whose recurring cost the servicing company bears (ADV2-006): Echelon share and licence from
      /// formation; non-production, servicing-specific platform and the maintenance gap not covered by the design's
      /// own engineers from the first go-live. Build amortisation is excluded (the build is in OneTime).
      Layers: LayerCosts
      PreLaunchFixedShare: float
      /// Month from which full fixed cost applies even before an administration go-live (e.g. a narrow service that
      /// needs SOC 2, insurance and support from its own launch).
      FullFixedFrom: int option
      CollectionLagMonths: int
      FinancingRate: float
      CashView: bool
      Months: int }

type Row =
    { Month: int
      Live: int
      CashIn: float
      CashOut: float
      Cumulative: float
      AccruedProfit: float
      Headcount: float }

let private goLive (c: Customer) = c.SignMonth + c.OnboardingMonths
let private live (s: Sequence) m = s.Customers |> List.filter (fun c -> goLive c <= m)
let private firstLive (s: Sequence) = s.Customers |> List.map goLive |> List.sort |> List.tryHead

let designAt (s: Sequence) m =
    s.Stages |> List.filter (fun (start, _) -> start <= m) |> List.sortBy fst |> List.last |> snd

/// Each sponsor starts in pre-delegation (three-person release, full calibration) for RedesignLagMonths after its
/// own go-live (ADV2-016; OPS): its minutes are scaled to the early target, later to the steady target.
let private scaledLive (s: Sequence) m =
    live s m
    |> List.map (fun c -> withTarget (if m < goLive c + s.RedesignLagMonths then s.EarlyTarget else s.Target) c.Sponsor)

let platformMonthly (s: Sequence) (d: Design) m =
    let lc = s.Layers
    let launched = live s m |> List.isEmpty |> not
    let always = echelonToUnbound lc
    let afterLaunch = lc.UnboundPlatformOps + lc.ServicingSpecificPlatform + max 0.0 (lc.UnboundMaintenance - embeddedEngineering d)
    (always + (if launched then afterLaunch else 0.0)) / 12.0

let private activePeople (d: Design) m = { d with People = d.People |> List.filter (fun p -> p.StartMonth <= m) }

let private monthlyCosts (s: Sequence) m =
    let d = activePeople (designAt s m) m
    let payroll = d.People |> List.sumBy (fun p -> (if s.CashView then p.CashCost else p.LoadedCost) / 12.0)
    let empty = evaluateDesign d baseMarketMinutes s.Price noStress []
    let launched = live s m |> List.isEmpty |> not
    let early = s.FullFixedFrom |> Option.exists (fun f -> f <= m)
    let fixedShare = if launched || early then 1.0 else s.PreLaunchFixedShare
    let fixedEx = (empty.Base.TotalCost - empty.Base.CorePersonnel) * fixedShare / 12.0
    // sponsors are pre-scaled to their own targets; evaluating at the market-mix minutes leaves them unchanged
    let withSponsors = evaluateDesign d baseMarketMinutes s.Price noStress (scaledLive s m)
    let variable = (withSponsors.Base.TotalCost - empty.Base.TotalCost) / 12.0
    let recurring = (s.Recurring |> List.filter (fun (start, _, _) -> start <= m) |> List.sumBy (fun (_, _, v) -> v)) + platformMonthly s d m
    payroll, fixedEx, variable, recurring, withSponsors.Headcount

let private feeCash (s: Sequence) m =
    s.Customers
    |> List.sumBy (fun c ->
        let since = m - s.CollectionLagMonths - goLive c + 1
        if since >= 3 && since % 3 = 0 then (let a, t, o = sponsorRevenue s.Price 1.0 c.Sponsor in (a + t + o) / 4.0) else 0.0)

let private accrued (s: Sequence) m =
    live s m |> List.sumBy (fun c -> let a, t, o = sponsorRevenue s.Price 1.0 c.Sponsor in (a + t + o) / 12.0)

let private implementationCash (s: Sequence) m =
    s.Customers
    |> List.sumBy (fun c -> (if m = c.SignMonth then c.ImplementationFee / 2.0 else 0.0) + (if m = goLive c then c.ImplementationFee / 2.0 else 0.0))

let private onboarding (s: Sequence) m =
    s.Customers
    |> List.filter (fun c -> m >= c.SignMonth && m < goLive c)
    |> List.sumBy (fun c -> c.Sponsor.OnboardingCost / float (max 1 c.OnboardingMonths))

let private at (items: (int * string * float) list) m = items |> List.filter (fun (x, _, _) -> x = m) |> List.sumBy (fun (_, _, v) -> v)

let simulate (s: Sequence) =
    let step prev m =
        let payroll, fixedEx, variable, recurring, heads = monthlyCosts s m
        let financing = if prev < 0.0 then -prev * s.FinancingRate / 12.0 else 0.0
        let cashIn = feeCash s m + implementationCash s m + at s.OtherIncome m
        let cashOut = payroll + fixedEx + variable + recurring + onboarding s m + at s.OneTime m + financing
        { Month = m
          Live = List.length (live s m)
          CashIn = cashIn
          CashOut = cashOut
          Cumulative = prev + cashIn - cashOut
          AccruedProfit = accrued s m + at s.OtherIncome m - (payroll + fixedEx + variable + recurring)
          Headcount = heads }
    [ 0 .. s.Months - 1 ]
    |> List.scan (fun (acc: Row option) m -> Some (step (acc |> Option.map (fun r -> r.Cumulative) |> Option.defaultValue 0.0) m)) None
    |> List.choose id

let capitalRequired (rows: Row list) = rows |> List.map (fun r -> r.Cumulative) |> List.fold min 0.0 |> (~-)

/// Equity need: the cash trough with no financing cost on the deficit (ADV2-009); capitalRequired with financing is
/// the debt-financed case.
let equityNeed (s: Sequence) = capitalRequired (simulate { s with FinancingRate = 0.0 })

/// Net present value at an annual discount rate of the monthly net cash flows over the horizon (no financing), plus
/// a terminal value of the final-year profit after a 21% tax rate as a perpetuity at the same rate. [A]
let npv (rate: float) (s: Sequence) =
    let rows = simulate { s with FinancingRate = 0.0 }
    let monthly = (1.0 + rate) ** (1.0 / 12.0) - 1.0
    let flows = rows |> List.sumBy (fun r -> (r.CashIn - r.CashOut) / ((1.0 + monthly) ** float (r.Month + 1)))
    let p = rows |> List.rev |> List.truncate 12 |> List.sumBy (fun r -> r.AccruedProfit)
    let terminal = (if p > 0.0 then p * (1.0 - 0.21) else p) / rate / ((1.0 + rate) ** (float s.Months / 12.0))
    flows + terminal

let monthsToProfit (rows: Row list) =
    match List.tryLast rows with
    | Some r when r.AccruedProfit >= 0.0 -> rows |> List.rev |> List.takeWhile (fun r -> r.AccruedProfit >= 0.0) |> List.tryLast |> Option.map (fun r -> r.Month)
    | _ -> None

/// Annual accrued profit in the final 12 months of the horizon.
let finalYearProfit (rows: Row list) = rows |> List.rev |> List.truncate 12 |> List.sumBy (fun r -> r.AccruedProfit)

/// Return on invested capital in the final year: final-year profit after a 21% federal rate on positive profit,
/// divided by capital required (cash trough). None when no capital was required.
let roic (rows: Row list) =
    let cap = capitalRequired rows
    let p = finalYearProfit rows
    let after = if p > 0.0 then p * (1.0 - 0.21) else p
    if cap > 0.0 then Some (after / cap) else None

// ---------------------------------------------------------------- sequence definitions [A]

let private sp name assets = sponsor name (assets / 250000.0) 250000.0
let private customer s sign onboarding fee = { Sponsor = s; SignMonth = sign; OnboardingMonths = onboarding; ImplementationFee = fee }
let private spread name total months start = [ for m in start .. start + months - 1 -> m, name, total / float months ]

/// One-time startup costs reused from the previous study (legal, money-transmission opinion, SOC readiness, filings,
/// brand, migration tooling) without recruiting; recruiting is added per hire. [S/A CST]
let startup =
    [ 0, "legal formation, MSA/SLA templates, privacy", 80000.0
      1, "money-transmission / agent-of-payee opinion", 40000.0
      6, "SOC readiness assessment", 20000.0
      0, "incorporation and filings", 2000.0
      3, "brand, website, collateral", 15000.0
      9, "implementation / migration tooling", 40000.0 ]

/// Base productivity multiple for agent-assisted construction 1.5x (DEV planning range 1.5-3x; 2-3x are upside to be
/// earned by measurement, ADV2-007) [A; unmeasured, see 05]; minimum safe servicing
/// product cost from the development model (Development.fs, Designs.unboundBaseline).
let baseMultiple = 1.5
let minimumBuild = minimumProductCost unboundBaseline baseMultiple

/// Narrow non-custodial service (charity verification and grant-request processing, no money movement): 8% of the
/// full conventional scope plus a $60k safety floor (pen test, SOC 2 readiness, accessibility audit). [A]
let narrowBuild = effectiveCost unboundBaseline 0.08 baseMultiple + 60000.0

/// Extending the narrow service to full administration: the minimum product less the narrow scope already built. [D]
let extensionBuild = minimumBuild - (narrowBuild - 60000.0)

/// Annual delivery cost per standalone-service sponsor: data, support and exception hours (~60 h). [A]
let narrowServiceCostPerSponsor = 8000.0

let recruiting hires month = [ month, $"recruiting ({hires} hires x $15k, CST-P16)", 15000.0 * float hires ]

/// Deferred scope (ADV2-008): the minimum product is 44% of the conventional scope; DEV defers capabilities whose
/// absence pushes labour to operations and sponsors. A tranche of 15% of the conventional scope is built over the
/// 12 months after the second sponsor's go-live. [A]
let deferredTranche (customers: Customer list) =
    match customers |> List.map goLive |> List.sort with
    | _ :: second :: _ -> spread "deferred scope build (tranche)" (effectiveCost unboundBaseline 0.15 baseMultiple) 12 second
    | _ -> []

let private baseSeq name stages customers oneTime =
    { Name = name
      Stages = stages
      Price = price 20.0
      Target = 50.0
      EarlyTarget = 101.0 * 50.0 / baseMarketMinutes // AI-enhanced market mix (prior study) until gates are in place
      RedesignLagMonths = 12
      Customers = customers
      OneTime = oneTime @ deferredTranche customers
      OtherIncome = []
      Recurring = []
      Layers = baseLayers
      PreLaunchFixedShare = 0.4
      FullFixedFrom = None
      CollectionLagMonths = 1
      FinancingRate = 0.10
      CashView = true
      Months = 60 }

/// A conventional: five core with controller and operations hired at month 18, Unbound-scale $5M contracted build
/// over 24 months, first sponsor signs at month 18 and goes live at month 24; $1.5B in three sponsors.
let staged (d: Design) month =
    { d with People = d.People |> List.map (fun p -> if p.MoneyAuthority && not (p.Title.StartsWith "Founder") then { p with StartMonth = month } else p) }
let seqA =
    baseSeq "A conventional: F5 staged, $5M contracted build over 24 months, three $500M sponsors"
        [ 0, staged f5 18 ]
        [ customer (sp "a1" 0.5e9) 18 6 50000.0; customer (sp "a2" 0.5e9) 28 6 50000.0; customer (sp "a3" 0.5e9) 36 6 50000.0 ]
        (startup @ recruiting 5 0 @ spread "build (Unbound base, contracted)" 5.0e6 24 0)
    |> fun s -> { s with OneTime = s.OneTime |> List.filter (fun (_, n, _) -> not (n.StartsWith "deferred")) }

/// B product-first: two founders build the minimum safe product with agents (development model cost at 2x, 12 months),
/// sell from month 12, grow to five core at the first go-live.
let seqB =
    baseSeq "B product-first: F2 builds minimum product (12 months), F5 from first go-live"
        [ 0, f2; 18, f5 ]
        [ customer (sp "b1" 0.5e9) 12 6 50000.0; customer (sp "b2" 0.5e9) 24 6 50000.0; customer (sp "b3" 0.5e9) 30 6 50000.0 ]
        (startup @ recruiting 3 17 @ spread "minimum product build (agents + contractors)" minimumBuild 12 0)

/// C customer-funded: a design partner signs at month 3, prepays a $250k implementation fee and a $150k minimum
/// annual fee; minimum product over 12 months; F3 until go-live, F5 after.
let seqC =
    { baseSeq "C customer-funded: design partner prepays $250k, F3 then F5"
        [ 0, f3; 15, f5 ]
        [ customer (sp "partner" 0.5e9) 3 12 250000.0; customer (sp "c2" 0.5e9) 21 6 50000.0; customer (sp "c3" 0.5e9) 27 6 50000.0 ]
        (startup @ recruiting 1 0 @ recruiting 2 14 @ spread "minimum product build (agents + contractors)" minimumBuild 12 0)
        with Price = { (price 20.0) with MinimumAnnualFee = 150000.0 } }

/// D narrow entry: two founders sell a non-custodial charity-verification and grant-processing service (no money
/// movement) at $40k a year to six sponsors from month 6, then administration from month 24.
let narrowF2 = { f2 with Name = "F2 narrow entry (non-custodial)"; NonPersonnel = narrowEntryNonPersonnel }
let seqD =
    { baseSeq "D narrow entry: non-custodial service at $40k/sponsor, administration from month 24"
        [ 0, narrowF2; 30, f5 ]
        [ customer (sp "d1" 0.5e9) 24 6 50000.0; customer (sp "d2" 0.5e9) 30 6 50000.0; customer (sp "d3" 0.5e9) 36 6 50000.0 ]
        (startup @ recruiting 3 29 @ spread "narrow service build" narrowBuild 6 0 @ spread "administration extension build" extensionBuild 12 12)
        with
            FullFixedFrom = Some 6
            OtherIncome = [ for i in 0 .. 5 do for m in 6 + 3 * i .. 59 do if (m - (6 + 3 * i)) % 12 = 0 then yield m, $"standalone service sponsor {i + 1} (annual in advance)", 40000.0 ]
            Recurring = [ for i in 0 .. 5 -> 6 + 3 * i, $"standalone service delivery {i + 1}", narrowServiceCostPerSponsor / 12.0 ] }

/// E provider partnership: an existing administrator or bank partner carries money movement, custody and SOC 1 scope
/// and brings three $500M programs (months 12, 18, 24); the partner keeps 30% of fees (14 bps net). F3 throughout.
let partnerF3 =
    { f3 with
        Name = "F3 with partner-provided money movement"
        NonPersonnel = withContingency ((assurance |> List.filter (fun (n, _) -> not (n.StartsWith "CST-C12"))) @ insurance @ specialists @ platformAndData @ salesAndGa @ agentCompute) }
let seqE =
    { baseSeq "E provider partnership: partner programs at 14 bps net, F3"
        [ 0, partnerF3 ]
        [ for i in 0 .. 2 -> customer (sp $"e{i + 1}" 0.5e9) (12 + 6 * i) 6 0.0 ]
        (startup @ recruiting 1 0 @ spread "minimum product build (agents + contractors)" minimumBuild 12 0)
        with Price = price 14.0 }

/// F founder-led: one founder with agents and contractors builds the minimum product over 12 months and moves
/// to F3 at the anchor's go-live (month 18).
let seqF =
    baseSeq "F founder-led: F1 then F3, $1.0B anchor + $500M"
        [ 0, f1; 18, f3 ]
        [ customer (sp "anchor" 1.0e9) 12 6 100000.0; customer (sp "f2" 0.5e9) 30 6 50000.0 ]
        (startup @ recruiting 2 17 @ spread "minimum product build (agents + contractors)" minimumBuild 12 0)

/// G hybrid: narrow-entry service revenue from month 6 (three sponsors), a design partner at month 9 with a $250k
/// prepaid implementation and $150k minimum, staged F2 -> F3 -> F5 at go-lives.
let seqG =
    { baseSeq "G hybrid: narrow service + design partner + staged F2/F3/F5"
        [ 0, narrowF2; 9, f3; 27, f5 ]
        [ customer (sp "partner" 0.5e9) 9 12 250000.0; customer (sp "g2" 0.5e9) 27 6 50000.0; customer (sp "g3" 0.5e9) 33 6 50000.0 ]
        (startup @ recruiting 1 9 @ recruiting 2 26 @ spread "narrow service build" narrowBuild 6 0 @ spread "administration extension build" extensionBuild 12 6)
        with
            Price = { (price 20.0) with MinimumAnnualFee = 150000.0 }
            FullFixedFrom = Some 6
            OtherIncome = [ for i in 0 .. 2 do for m in 6 + 3 * i .. 59 do if (m - (6 + 3 * i)) % 12 = 0 then yield m, $"standalone service sponsor {i + 1}", 40000.0 ]
            Recurring = [ for i in 0 .. 2 -> 6 + 3 * i, $"standalone service delivery {i + 1}", narrowServiceCostPerSponsor / 12.0 ] }

let sequences = [ seqA; seqB; seqC; seqD; seqE; seqF; seqG ]

// ---------------------------------------------------------------- failure modifiers (cost of being wrong)

let private isBuild (_, (n: string), _) = n.Contains "build"

/// Build at 1x instead of the base multiple: build lines scale by the cost ratio (1.25 at 1.5x base). Sequence A's
/// contracted $5M build is scaled by the same ratio for comparability.
let productivityHalved (s: Sequence) =
    let ratio = minimumProductCost unboundBaseline 1.0 / minimumProductCost unboundBaseline baseMultiple
    { s with Name = s.Name + " | build at 1x (no productivity gain)"; OneTime = s.OneTime |> List.map (fun ((m, n, v) as x) -> if isBuild x then m, n, v * ratio else x) }

let developmentTwiceAsLong (s: Sequence) =
    let builds = s.OneTime |> List.filter isBuild
    let months = builds |> List.map (fun (m, _, _) -> m) |> List.distinct |> List.length
    { s with
        Name = s.Name + " | development 2x longer (go-lives later, burn continues)"
        OneTime = (s.OneTime |> List.filter (isBuild >> not)) @ (builds |> List.collect (fun (m, n, v) -> [ m, n, v; m + months, n, v ]))
        Customers = s.Customers |> List.map (fun c -> { c with SignMonth = c.SignMonth + months }) }

let acquisitionTwiceAsLong (s: Sequence) =
    { s with Name = s.Name + " | sales cycles 2x"; Customers = s.Customers |> List.map (fun c -> { c with SignMonth = 2 * c.SignMonth }) }

let humanReviewNotReduced (s: Sequence) =
    { s with Name = s.Name + " | handling stays AI-enhanced (101 min)"; Target = 101.0 * 50.0 / baseMarketMinutes; EarlyTarget = 101.0 * 50.0 / baseMarketMinutes }

let partnerWithdraws (s: Sequence) =
    match s.Customers with
    | [] -> s
    | _ :: rest -> { s with Name = s.Name + " | first customer (design partner) withdraws: never signs"; Customers = rest @ [ { (List.head s.Customers) with SignMonth = 999 } ] }

let assuranceHigher (s: Sequence) =
    { s with Name = s.Name + " | assurance +$150k/yr from month 12"; Recurring = s.Recurring @ [ 12, "assurance overrun", 150000.0 / 12.0 ] }

let securityIncident (s: Sequence) =
    { s with Name = s.Name + " | security incident $500k at month 30"; OneTime = s.OneTime @ [ 30, "security incident", 500000.0 ] }

let echelonLicence (s: Sequence) =
    { s with Name = s.Name + " | Echelon licence at LYR cost-plus $350k/yr (base $60k)"; Layers = { s.Layers with EchelonLicence = 350843.0 } }

let customisation (s: Sequence) =
    { s with
        Name = s.Name + " | customer customisation: onboarding x3, sponsor upkeep x2"
        Customers = s.Customers |> List.map (fun c -> { c with Sponsor = { c.Sponsor with OnboardingCost = c.Sponsor.OnboardingCost * 3.0; AnnualSponsorCost = c.Sponsor.AnnualSponsorCost * 2.0 } }) }

/// Correlated failures (ADV2-027): low productivity and slow sales tend to arrive together, often with review that
/// cannot be reduced.
let jointBuildAndSales (s: Sequence) = s |> productivityHalved |> acquisitionTwiceAsLong
let jointBuildSalesReview (s: Sequence) = s |> productivityHalved |> acquisitionTwiceAsLong |> humanReviewNotReduced

let failures =
    [ productivityHalved; developmentTwiceAsLong; acquisitionTwiceAsLong; humanReviewNotReduced; partnerWithdraws
      assuranceHigher; securityIncident; echelonLicence; customisation; jointBuildAndSales; jointBuildSalesReview ]

let economic (s: Sequence) = { s with Name = s.Name + " | economic view (founders at market)"; CashView = false }
