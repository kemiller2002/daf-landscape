/// Parameter sets. Every value is labelled in its comment: [S] sourced (see evidence register),
/// [A] assumption, [D] derived, [E] estimate. Evidence IDs refer to ../../data/evidence-register.csv.
module ServicingEconomics.Parameters

open ServicingEconomics.Domain

// ---------------------------------------------------------------- prices

let price bps =
    { Bps = bps; MinimumAnnualFee = 0.0; ImplementationFeePerSponsor = 0.0; ExceptionalFeesPerAccountYear = 0.0; PerAccountMinimum = 0.0; PerAccountMaximum = 0.0; PerAccountFee = 0.0; PaymentsPassThrough = true }

let pricePoints = [ 5.0; 10.0; 15.0; 20.0; 25.0; 30.0; 35.0 ]

// ---------------------------------------------------------------- hypothesis H0 (reproduction of the prior memo)

/// The prior memo's model: F = $1,177,750 fixed, v = $75 per account-year, no capacity limits. [A] (prior memo)
let h0Org =
    { Name = "H0 prior memo (5 FTE, $1,177,750)"
      Core = []
      NonPersonnelFixed = [ "prior fixed budget", 1177750.0 ]
      StepRules = []
      ProductiveHours = 1600.0
      Utilisation = 1.0
      MinimumAddedServicingFte = 0.0
      ServicingHourlyLoaded = 0.0
      DecemberShare = 0.0
      PeakPremium = 0.0 }

let h0Activities =
    [ { Id = "H0-V"; Name = "prior $75 per account-year"; Driver = PerAccountYear; Minutes = (fun _ -> 0.0); ExternalCost = 75.0; PassThrough = false } ]

/// A single sponsor with uniform average balance b and assets a (prior memo's N = AUA / B).
let uniformSponsor name (assets: float) (b: float) =
    { Name = name
      Accounts = assets / b
      Mix = [ { Name = "uniform"; ShareOfAccounts = 1.0; AverageBalance = b; Minutes = (fun _ -> 0.0); External = (fun _ -> 0.0); Payments = (fun _ -> 0.0); DecemberShare = 0.0 } ]
      ComplexityMultiplier = 1.0
      AnnualSponsorCost = 0.0
      OnboardingCost = 0.0 }

// ---------------------------------------------------------------- account archetypes (ACT pass)

/// Workload per account-year by archetype and approach, from the activity-based costing pass
/// (servicing-economics/data/activities.csv, capacity-model.csv). Minutes and vendor costs are [D] from [A]
/// activity parameters (no time study exists). Balances are [A] archetype balances; the book mix
/// (20/20/40/7/10/3%) is assumption A-ACT-014. External excludes payment rails (separate line).
let archetypeTable =
    [
      { Name = "inactive"; ShareOfAccounts = 0.2; AverageBalance = 20000
        Minutes = (function | Conventional -> 15.8 | AiEnhanced -> 7.3 | AiNative -> 3 | AiNativeWithElimination -> 2.6)
        External = (function | Conventional -> 4.97 | AiEnhanced -> 5.01 | AiNative -> 5.01 | AiNativeWithElimination -> 5)
        Payments = (function | Conventional -> 0.72 | AiEnhanced -> 0.72 | AiNative -> 0.72 | AiNativeWithElimination -> 0.39)
        DecemberShare = 0.176 }
      { Name = "small_recurring"; ShareOfAccounts = 0.2; AverageBalance = 8000
        Minutes = (function | Conventional -> 168.9 | AiEnhanced -> 70.5 | AiNative -> 21.5 | AiNativeWithElimination -> 16.2)
        External = (function | Conventional -> 6.63 | AiEnhanced -> 7.02 | AiNative -> 6.97 | AiNativeWithElimination -> 6.82)
        Payments = (function | Conventional -> 11.08 | AiEnhanced -> 11.08 | AiNative -> 11.08 | AiNativeWithElimination -> 6.57)
        DecemberShare = 0.242 }
      { Name = "typical"; ShareOfAccounts = 0.4; AverageBalance = 150000
        Minutes = (function | Conventional -> 220.2 | AiEnhanced -> 101 | AiNative -> 38 | AiNativeWithElimination -> 27.3)
        External = (function | Conventional -> 8.16 | AiEnhanced -> 9.07 | AiNative -> 8.99 | AiNativeWithElimination -> 8.67)
        Payments = (function | Conventional -> 25.43 | AiEnhanced -> 25.43 | AiNative -> 25.43 | AiNativeWithElimination -> 15.94)
        DecemberShare = 0.244 }
      { Name = "high_frequency"; ShareOfAccounts = 0.07; AverageBalance = 400000
        Minutes = (function | Conventional -> 832.8 | AiEnhanced -> 376.4 | AiNative -> 133.6 | AiNativeWithElimination -> 94.6)
        External = (function | Conventional -> 16.76 | AiEnhanced -> 20.07 | AiNative -> 19.74 | AiNativeWithElimination -> 18.36)
        Payments = (function | Conventional -> 91.65 | AiEnhanced -> 91.65 | AiNative -> 91.65 | AiNativeWithElimination -> 50.04)
        DecemberShare = 0.242 }
      { Name = "high_value"; ShareOfAccounts = 0.1; AverageBalance = 3e+06
        Minutes = (function | Conventional -> 464.3 | AiEnhanced -> 232.2 | AiNative -> 105 | AiNativeWithElimination -> 74.7)
        External = (function | Conventional -> 25.7 | AiEnhanced -> 28.28 | AiNative -> 28.05 | AiNativeWithElimination -> 27.53)
        Payments = (function | Conventional -> 54.21 | AiEnhanced -> 54.21 | AiNative -> 54.21 | AiNativeWithElimination -> 38.6)
        DecemberShare = 0.26 }
      { Name = "complex_asset"; ShareOfAccounts = 0.03; AverageBalance = 1.5e+06
        Minutes = (function | Conventional -> 1010.2 | AiEnhanced -> 618.7 | AiNative -> 359 | AiNativeWithElimination -> 166)
        External = (function | Conventional -> 8.27 | AiEnhanced -> 9.92 | AiNative -> 9.65 | AiNativeWithElimination -> 9.33)
        Payments = (function | Conventional -> 40.43 | AiEnhanced -> 40.43 | AiNative -> 40.43 | AiNativeWithElimination -> 30)
        DecemberShare = 0.333 }
    ]

/// Mix average balance of the archetype table (438,600 at the assumed balances). [D]
let archetypeMixBalance = archetypeTable |> List.sumBy (fun a -> a.ShareOfAccounts * a.AverageBalance)

/// Workload elasticity to balance: activity rises sub-linearly with balance. ln(105/38) / ln(3,000,000/150,000)
/// = 0.34 from the high-value vs typical archetypes (AI-native). [D from A] (ADV-009)
let workloadElasticity = 0.34

/// The archetype mix rescaled so that its average balance equals a sponsor's observed average balance; minutes
/// and vendor cost scale by (b / mix balance)^0.34 so very high-balance books are not treated as nearly free. [D]
let mixWithAverageBalance (b: float) =
    let k = b / archetypeMixBalance
    let w = k ** workloadElasticity
    archetypeTable
    |> List.map (fun a ->
        { a with
            AverageBalance = a.AverageBalance * k
            Minutes = (fun ap -> a.Minutes ap * w)
            External = (fun ap -> a.External ap * w)
            Payments = (fun ap -> a.Payments ap * w) })

/// Market-mix minutes per account-year low/high relative to base (AI-native: 17.6 / 50.7 / 168.7). [D]
let minutesLowFactor = 17.6 / 50.7
let minutesHighFactor = 168.7 / 50.7

// ---------------------------------------------------------------- sponsor-level activities (ACT S01-S05)

/// Sponsor-level annual minutes (close and reporting, configuration, incidents, audit support, governance
/// reporting): 48,000 / 33,000 / 19,440 / 19,440 minutes per sponsor-year by approach. [D from A]
let sponsorActivities =
    [ { Id = "ACT-S01..S05"
        Name = "sponsor close, reporting, configuration, incidents, audit support, governance"
        Driver = PerSponsorYear
        Minutes = (function Conventional -> 48000.0 | AiEnhanced -> 33000.0 | AiNative -> 19440.0 | AiNativeWithElimination -> 19440.0)
        ExternalCost = 0.0
        PassThrough = false } ]

/// One-time onboarding per sponsor: configuration $30k (CST-OM1, $10-75k) + migration with parallel run
/// $75k (CST-OM2, $25-250k). [A]
let onboardingBase = 105000.0
let onboardingLow = 35000.0
let onboardingHigh = 325000.0

/// Annual sponsor-specific non-labour cost: sandbox/non-production environment (CST-T06 $8k) plus bank and
/// custodian connection upkeep ($4k). [A]
let annualSponsorCostBase = 12000.0

/// A sponsor with a given number of accounts and observed average balance, market archetype mix.
let sponsor name (accounts: float) (averageBalance: float) =
    { Name = name
      Accounts = accounts
      Mix = mixWithAverageBalance averageBalance
      ComplexityMultiplier = 1.0
      AnnualSponsorCost = annualSponsorCostBase
      OnboardingCost = onboardingBase }

/// Complex-asset intermediary fees are fund-borne (OD-M-09) and payment rails are sponsor-originated and passed
/// through at cost in the base price (ADV-020; CST, ACT). The complex-asset External line keeps only data, cloud
/// and typical other cost. [A]

// ---------------------------------------------------------------- organizations (CST pass)

let private role title loaded cash share start = { Title = title; LoadedCost = loaded; CashCost = cash; ServicingShare = share; StartMonth = start }

/// Productive hours per FTE-year: 2,080 less ~12% leave/training less ~15% meetings and admin (CST). [A]
let productiveHours = 1520.0

/// Share of productive hours usable for queue work: 1,368 of 1,520 hours (ADV-006). [A]
let queueUtilisation = 0.9

/// Loaded hourly rate of an added grant & client operations specialist: $99,478 / 1,520 h. [D from S: OEWS, ECEC]
let opsHourly = 99478.0 / productiveHours

let private steps =
    [ { Name = "grant operations manager per 6 added ops staff beyond 4"; On = ServicingFte; Free = 4.0; Size = 6.0; CostPerStep = 149810.0 }
      // Steady-state sponsor upkeep (feeds, configuration changes, relationship); onboarding labour is in the
      // one-time onboarding cost. Triggers adapted from CST hiring triggers to live-sponsor counts. [A]
      { Name = "integration engineer per 8 live sponsors beyond 4"; On = Sponsors; Free = 4.0; Size = 8.0; CostPerStep = 188958.0 }
      { Name = "implementation / client success analyst per 8 live sponsors beyond 3"; On = Sponsors; Free = 3.0; Size = 8.0; CostPerStep = 127440.0 }
      { Name = "fund accountant per 15,000 accounts beyond 5,000"; On = Accounts; Free = 5000.0; Size = 15000.0; CostPerStep = 110662.0 } ]

/// Model A founder-led: 3 core (founder, CTO, controller). Founder and CTO take below-market cash salaries
/// (economic cost shown at market). Needs two operations staff for dual control once live. [S/A CST]
let modelA =
    { Name = "Model A founder-led (3 core)"
      Core =
        [ role "Founder / managing director" 200142.0 116255.0 0.05 0
          role "CTO / technical lead" 222482.0 127440.0 0.0 0
          role "Controller / head of financial operations" 183365.0 183365.0 0.0 0 ]
      NonPersonnelFixed = [ "non-personnel and contracted (ex December temps)", 598363.0; "contingency 7.5%", 91262.0 ]
      StepRules = steps @ [ { Name = "compliance officer above 10,000 accounts (ADV-008: not asset-triggered)"; On = Accounts; Free = 10000.0; Size = 1.0e12; CostPerStep = 121848.0 } ]
      ProductiveHours = productiveHours
      Utilisation = queueUtilisation
      MinimumAddedServicingFte = 2.0
      ServicingHourlyLoaded = opsHourly
      DecemberShare = 0.10
      PeakPremium = 0.0 }

/// Model B lean independent: 5 core (founder, CTO, engineer, controller, one ops specialist). [S/A CST]
let modelB =
    { Name = "Model B lean (5 core)"
      Core =
        [ role "Founder / managing director" 200142.0 200142.0 0.05 0
          role "CTO / technical lead" 222482.0 222482.0 0.0 0
          role "Senior software engineer" 188958.0 188958.0 0.0 0
          role "Controller / head of financial operations" 183365.0 183365.0 0.0 0
          role "Grant & client operations specialist" 99478.0 99478.0 0.8 0 ]
      NonPersonnelFixed = [ "non-personnel and contracted (ex December temps)", 631048.0; "contingency 7.5%", 115814.0 ]
      StepRules = steps @ [ { Name = "compliance officer above 10,000 accounts (ADV-008: not asset-triggered)"; On = Accounts; Free = 10000.0; Size = 1.0e12; CostPerStep = 121848.0 } ]
      ProductiveHours = productiveHours
      Utilisation = queueUtilisation
      MinimumAddedServicingFte = 1.0
      ServicingHourlyLoaded = opsHourly
      DecemberShare = 0.10
      PeakPremium = 0.0 }

/// Model C established: 12 core with specialization and redundancy. [S/A CST]
let modelC =
    { Name = "Model C established (12 core)"
      Core =
        [ role "Founder / managing director" 200142.0 200142.0 0.05 0
          role "CTO / technical lead" 222482.0 222482.0 0.0 0
          role "Senior software engineer" 188958.0 188958.0 0.0 0
          role "Senior software engineer" 188958.0 188958.0 0.0 0
          role "Security / infrastructure engineer" 177772.0 177772.0 0.0 0
          role "Controller / head of financial operations" 183365.0 183365.0 0.0 0
          role "Fund / grant accountant" 110662.0 110662.0 0.7 0
          role "Grant operations manager" 149810.0 149810.0 0.5 0
          role "Grant & client operations specialist" 99478.0 99478.0 0.8 0
          role "Grant & client operations specialist" 99478.0 99478.0 0.8 0
          role "Compliance officer" 121848.0 121848.0 0.5 0
          role "Implementation / client success analyst" 127440.0 127440.0 0.5 0 ]
      NonPersonnelFixed = [ "non-personnel and contracted (ex December temps)", 746226.0; "contingency 7.5%", 198118.0 ]
      StepRules =
        [ { Name = "grant operations manager per 8 added ops staff"; On = ServicingFte; Free = 6.0; Size = 8.0; CostPerStep = 149810.0 }
          { Name = "integration engineer per 8 live sponsors beyond 8"; On = Sponsors; Free = 8.0; Size = 8.0; CostPerStep = 188958.0 }
          { Name = "implementation analyst per 8 live sponsors beyond 8"; On = Sponsors; Free = 8.0; Size = 8.0; CostPerStep = 127440.0 }
          { Name = "fund accountant per 15,000 accounts beyond 15,000"; On = Accounts; Free = 15000.0; Size = 15000.0; CostPerStep = 110662.0 } ]
      ProductiveHours = productiveHours
      Utilisation = queueUtilisation
      MinimumAddedServicingFte = 0.0
      ServicingHourlyLoaded = opsHourly
      DecemberShare = 0.10
      PeakPremium = 0.0 }

/// The controller reviews and releases, so its hours are not counted as preparation capacity (ADV-023). [A]

/// December: archetype December shares are already in the table; temporary staff for the excess cost
/// $39/h agency (CST-P14) against $65.45/h loaded: no premium over the loaded rate is applied. [A]
let organizations = [ modelA; modelB; modelC ]

/// Fully loaded variant: adds platform build amortisation ($1.0M a year: Unbound's $5M base over 5 years) and
/// sales/customer acquisition ($250k a year). [A] (ADV, ECH)
let fullyLoaded (org: Organization) =
    { org with
        Name = org.Name + " + build amortisation and sales"
        NonPersonnelFixed = org.NonPersonnelFixed @ [ "platform build amortisation", 1.0e6; "sales and customer acquisition", 250000.0 ] }
