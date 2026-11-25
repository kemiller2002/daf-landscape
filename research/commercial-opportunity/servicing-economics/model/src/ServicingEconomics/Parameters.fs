/// Parameter sets. Every value is labelled in its comment: [S] sourced (see evidence register),
/// [A] assumption, [D] derived, [E] estimate. Evidence IDs refer to ../../data/evidence-register.csv.
module ServicingEconomics.Parameters

open ServicingEconomics.Domain

// ---------------------------------------------------------------- prices

let price bps =
    { Bps = bps; MinimumAnnualFee = 0.0; ImplementationFeePerSponsor = 0.0; ExceptionalFeesPerAccountYear = 0.0 }

let pricePoints = [ 5.0; 10.0; 15.0; 20.0; 25.0; 30.0; 35.0 ]

// ---------------------------------------------------------------- hypothesis H0 (reproduction of the prior memo)

/// The prior memo's model: F = $1,177,750 fixed, v = $75 per account-year, no capacity limits. [A] (prior memo)
let h0Org =
    { Name = "H0 prior memo (5 FTE, $1,177,750)"
      Core = []
      NonPersonnelFixed = [ "prior fixed budget", 1177750.0 ]
      StepRules = []
      ProductiveHours = 1600.0
      ServicingHourlyLoaded = 0.0
      DecemberShare = 0.0
      PeakPremium = 0.0 }

let h0Activities =
    [ { Id = "H0-V"; Name = "prior $75 per account-year"; Driver = PerAccountYear; Minutes = (fun _ -> 0.0); ExternalCost = 75.0; PassThrough = false } ]

/// A single sponsor with uniform average balance b and assets a (prior memo's N = AUA / B).
let uniformSponsor name (assets: float) (b: float) =
    { Name = name
      Accounts = assets / b
      Mix = [ { Name = "uniform"; ShareOfAccounts = 1.0; AverageBalance = b; GrantsPerYear = 0.0; ContributionsPerYear = 0.0; ContactsPerYear = 0.0; ComplexAssetsPerYear = 0.0 } ]
      ComplexityMultiplier = 1.0
      NewAccountRate = 0.0
      AnnualSponsorCost = 0.0
      OnboardingCost = 0.0 }
