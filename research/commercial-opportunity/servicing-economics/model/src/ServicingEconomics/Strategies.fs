/// Market-entry strategies as monthly cash-flow plans. Pure definitions; every timing and amount is [A].
module ServicingEconomics.Strategies

open ServicingEconomics.Domain
open ServicingEconomics.CashFlow
open ServicingEconomics.Parameters

/// Product build outside the core team (contract engineers, design, security review), per month during the
/// build window. Base $60k/month for 12 months ($0.72M); Unbound's own model assumes $3-15M to build the full
/// platform (ECH pass), so the base deliberately assumes a narrow servicing-only scope. [A]
let buildPerMonthBase = 60000.0
let buildMonthsBase = 12

/// One-time startup costs: legal formation and contracts $80k (CST-C07), money-transmission opinion $40k
/// (CST-C08), SOC readiness $20k (CST-C13), incorporation $2k, brand $15k, migration tooling $40k (CST-ST1-3),
/// recruiting 5 hires x $15k (CST-P16). [S/A CST]
let startupOneTime =
    [ 0, "legal formation, MSA/SLA templates, privacy", 80000.0
      1, "money-transmission / agent-of-payee opinion", 40000.0
      6, "SOC readiness assessment", 20000.0
      0, "incorporation and filings", 2000.0
      3, "brand, website, collateral", 15000.0
      9, "implementation / migration tooling", 40000.0
      0, "recruiting (5 hires)", 75000.0 ]

let private build months perMonth = [ for m in 0 .. months - 1 -> m, "product build (contract engineering)", perMonth ]

/// Model B with staged hiring: founder, CTO and engineer at formation; controller at month 9; operations
/// specialist at month 12 (before the first go-live).
let stagedModelB =
    { modelB with
        Core =
            modelB.Core
            |> List.map (fun r ->
                if r.Title.StartsWith "Controller" then { r with StartMonth = 9 }
                elif r.Title.StartsWith "Grant" then { r with StartMonth = 12 }
                else r) }

/// A software-only organization: founder, CTO, engineer and a support/implementation analyst; no staffed
/// operations, smaller assurance scope (SOC 2 only) and no December servicing. [A from CST lines]
let softwareOrg =
    { modelB with
        Name = "Software-only licensing (4 core)"
        Core =
            [ { Title = "Founder / managing director"; LoadedCost = 200142.0; CashCost = 200142.0; ServicingShare = 0.05; StartMonth = 0 }
              { Title = "CTO / technical lead"; LoadedCost = 222482.0; CashCost = 222482.0; ServicingShare = 0.0; StartMonth = 0 }
              { Title = "Senior software engineer"; LoadedCost = 188958.0; CashCost = 188958.0; ServicingShare = 0.0; StartMonth = 0 }
              { Title = "Implementation / support analyst"; LoadedCost = 127440.0; CashCost = 127440.0; ServicingShare = 0.6; StartMonth = 10 } ]
        NonPersonnelFixed = [ "non-personnel (software scope: SOC 2, insurance, cloud, legal, sales)", 420000.0; "contingency 7.5%", 87000.0 ]
        MinimumAddedServicingFte = 0.0
        StepRules =
            [ { Name = "support analyst per 10 licensed sponsors beyond 4"; On = Sponsors; Free = 4.0; Size = 10.0; CostPerStep = 127440.0 }
              { Name = "engineer per 10 licensed sponsors beyond 4"; On = Sponsors; Free = 4.0; Size = 10.0; CostPerStep = 188958.0 } ] }

/// A licensed sponsor: the sponsor's own staff do the servicing; the vendor carries cloud and data cost and
/// ~100 support hours a year. [A]
let licensedSponsor name accounts balance =
    let s = sponsor name accounts balance
    { s with
        Mix = s.Mix |> List.map (fun a -> { a with Minutes = (fun _ -> 0.0); Payments = (fun _ -> 0.0); External = (fun _ -> 4.0) })
        AnnualSponsorCost = 8000.0
        OnboardingCost = 40000.0 }

let private customer s sign onboarding impl = { Sponsor = s; SignMonth = sign; OnboardingMonths = onboarding; ImplementationFee = impl }

let private basePlan name org price customers =
    { Name = name
      Org = org
      Activities = sponsorActivities
      Approach = AiNative
      Price = price
      Customers = customers
      OneTime = startupOneTime @ build buildMonthsBase buildPerMonthBase
      PreLaunchNonPersonnelShare = 0.4
      CollectionLagMonths = 1
      FinancingRate = 0.10
      CashView = true
      RedesignLagMonths = 12
      Months = 60 }

/// Strategy C (anchor): one $1.5B sponsor (5,000 accounts) signs at month 12, live after 6 months; two $500M
/// sponsors follow at months 24 and 30.
let anchor =
    basePlan "C anchor: $1.5B anchor + two $500M sponsors (admin, 20 bps)" stagedModelB (price 20.0)
        [ customer (sponsor "anchor" 5000.0 300000.0) 12 6 100000.0
          customer (sponsor "second" 2500.0 200000.0) 24 6 50000.0
          customer (sponsor "third" 2500.0 200000.0) 30 6 50000.0 ]

/// Strategy D (multiple smaller): six $300M sponsors (1,500 accounts each) signing every 4 months from month 12.
let multipleSmaller =
    basePlan "D multiple smaller: six $300M sponsors (admin, 20 bps)" stagedModelB (price 20.0)
        [ for i in 0 .. 5 -> customer (sponsor $"s{i + 1}" 1500.0 200000.0) (12 + 4 * i) 6 30000.0 ]

/// Strategy B (administration first, realistic pace): three $500M sponsors over three years.
let adminFirst =
    basePlan "B administration first: three $500M sponsors (admin, 20 bps)" stagedModelB (price 20.0)
        [ customer (sponsor "a" 2500.0 200000.0) 12 6 50000.0
          customer (sponsor "b" 2500.0 200000.0) 24 6 50000.0
          customer (sponsor "c" 2500.0 200000.0) 36 6 50000.0 ]

/// Strategy A (software first): licences at 4 bps with an $80k annual floor to $300M-$1B sponsors, eight
/// sponsors over four years; implementation fee $60k each.
let softwareFirst =
    let p = { price 4.0 with MinimumAnnualFee = 80000.0 }
    { basePlan "A software first: eight licences at 4 bps, $80k minimum" softwareOrg p
        [ for i in 0 .. 7 -> customer (licensedSponsor $"l{i + 1}" 2000.0 250000.0) (12 + 5 * i) 4 60000.0 ]
        with Activities = [] }

/// Strategy E (partnership distribution): an advisor/wealth partner brings three $400M programs; the partner
/// keeps 30% of the 20 bps fee (modelled as 14 bps net) and sales cost is lower (no separate CAC modelled).
let partnership =
    basePlan "E partnership: three $400M partner programs at 14 bps net" stagedModelB (price 14.0)
        [ for i in 0 .. 2 -> customer (sponsor $"p{i + 1}" 2700.0 150000.0) (12 + 6 * i) 6 0.0 ]

/// Strategy F (combined): software licences fund the build, then two administration clients from month 24.
/// Modelled as two plans whose cash flows are summed by the caller (organization cost counted once:
/// software org runs months 0-23, staffed Model B from month 24; see 06-capital-and-runway.md).
let combinedSoftware =
    let p = { price 4.0 with MinimumAnnualFee = 80000.0 }
    { basePlan "F combined (software leg)" softwareOrg p
        [ for i in 0 .. 3 -> customer (licensedSponsor $"l{i + 1}" 2000.0 250000.0) (12 + 4 * i) 4 60000.0 ]
        with Activities = [] }

/// Strategy C with the founder-led Model A (founder and CTO on below-market cash salaries).
let anchorFounderLed =
    { anchor with
        Name = "C anchor, founder-led Model A (cash)"
        Org = { modelA with Core = modelA.Core |> List.map (fun r -> if r.Title.StartsWith "Controller" then { r with StartMonth = 9 } else r) } }

let strategies = [ anchor; anchorFounderLed; multipleSmaller; adminFirst; softwareFirst; partnership ]

/// Variants for sensitivity: slower sales (sign dates +6 months), costlier build (2.5x), economic (not cash) view.
let delayed (p: Plan) = { p with Name = p.Name + " | signings +6 months"; Customers = p.Customers |> List.map (fun c -> { c with SignMonth = c.SignMonth + 6 }) }
let costlyBuild (p: Plan) =
    { p with
        Name = p.Name + " | build x2.5 over 18 months"
        OneTime = startupOneTime @ [ for m in 0 .. 17 -> m, "product build (contract engineering)", buildPerMonthBase * 2.5 * 12.0 / 18.0 ] }
let economicView (p: Plan) = { p with Name = p.Name + " | economic cost (founders at market)"; CashView = false }
let aiEnhancedOnly (p: Plan) = { p with Name = p.Name + " | AI-enhanced only (redesign not achieved)"; Approach = AiEnhanced }
let hybridPriced (p: Plan) = { p with Name = p.Name + " | 20 bps + $250/account floor, payments passed through"; Price = { p.Price with PerAccountMinimum = 250.0; PaymentsPassThrough = true } }
let unboundScaleBuild (p: Plan) =
    { p with
        Name = p.Name + " | Unbound-scale build $5M over 24 months"
        OneTime = startupOneTime @ [ for m in 0 .. 23 -> m, "product build (Unbound base $5M)", 5.0e6 / 24.0 ] }
let noRedesignLag (p: Plan) = { p with Name = p.Name + " | AI-native from first go-live (no gate lag)"; RedesignLagMonths = 0 }
let servicerPaysRails (p: Plan) = { p with Name = p.Name + " | servicer pays payment rails"; Price = { p.Price with PaymentsPassThrough = false } }
let perAccountPriced (p: Plan) = { p with Name = p.Name + " | 10 bps + $150 per account"; Price = { p.Price with Bps = 10.0; PerAccountFee = 150.0 } }
let renCapped (p: Plan) = { p with Name = p.Name + " | buyer cap: lesser of 20 bps or $737/account"; Price = { p.Price with PerAccountMaximum = 737.0 } }

/// Normalized comparison (ADV-013): every administration plan reaches $1.5B of average assets at a $250k average
/// balance, so differences reflect sponsor count and timing only.
let normalized =
    let sp name assets = sponsor name (assets / 250000.0) 250000.0
    [ basePlan "N-C anchor: $1.0B anchor + one $500M" stagedModelB (price 20.0)
        [ customer (sp "anchor" 1.0e9) 12 6 100000.0; customer (sp "second" 0.5e9) 24 6 50000.0 ]
      basePlan "N-B three $500M sponsors" stagedModelB (price 20.0)
        [ for i in 0 .. 2 -> customer (sp $"b{i + 1}" 0.5e9) (12 + 8 * i) 6 50000.0 ]
      basePlan "N-D five $300M sponsors" stagedModelB (price 20.0)
        [ for i in 0 .. 4 -> customer (sp $"d{i + 1}" 0.3e9) (12 + 5 * i) 6 30000.0 ]
      basePlan "N-E partnership: three $500M programs at 14 bps net" stagedModelB (price 14.0)
        [ for i in 0 .. 2 -> customer (sp $"p{i + 1}" 0.5e9) (12 + 8 * i) 6 0.0 ] ]
