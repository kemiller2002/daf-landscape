/// Model 4: customer acquisition and channel economics, direct versus partner (agent FGJ's inputs P3-ASM-FGJ001..017,
/// report 12 section 2). Pure.
module CompetitiveAdvantageCreation.Channel

type Inputs =
    { RevenuePerSponsor: float
      LifetimeYears: float
      PartnerShare: float
      DirectCac: float
      Enablement: float
      DealsPerPartnerPerYear: float
      AgreementYears: float
      DiscountRate: float
      SalesCycleMonths: float }

/// Present value of an annuity of 1 a year for n years at rate r (end-of-year), fractional years pro rata.
let annuity (r: float) (n: float) =
    if n <= 0.0 then 0.0
    elif r = 0.0 then n
    else
        let whole = floor n
        let pvWhole = (1.0 - (1.0 + r) ** (-whole)) / r
        pvWhole + (n - whole) * (1.0 + r) ** (-(whole + 1.0))

type Result =
    { MarginTransferred: float
      MarginTransferredPv: float
      EnablementPerDeal: float option
      PartnerCost: float option
      PartnerCostPv: float option
      DirectCac: float
      BreakEvenShare: float option
      BreakEvenSharePv: float option
      MonthsToFirstPartnerDeal: float option
      VendorNetRevenuePerYear: float }

/// Partner cost per sponsor = share x revenue x life + enablement / deals over the agreement.
/// Break-even share s* = (direct CAC - enablement per deal) / (revenue x life). None when the partner sources no deal.
let evaluate (i: Inputs) : Result =
    let deals = i.DealsPerPartnerPerYear * i.AgreementYears
    let enablementPerDeal = if deals > 0.0 then Some(i.Enablement / deals) else None
    let transferred = i.PartnerShare * i.RevenuePerSponsor * i.LifetimeYears
    let pvFactor = annuity i.DiscountRate i.LifetimeYears
    let transferredPv = i.PartnerShare * i.RevenuePerSponsor * pvFactor
    let lifetimeRevenue = i.RevenuePerSponsor * i.LifetimeYears
    { MarginTransferred = transferred
      MarginTransferredPv = transferredPv
      EnablementPerDeal = enablementPerDeal
      PartnerCost = enablementPerDeal |> Option.map (fun e -> transferred + e)
      PartnerCostPv = enablementPerDeal |> Option.map (fun e -> transferredPv + e)
      DirectCac = i.DirectCac
      BreakEvenShare = enablementPerDeal |> Option.bind (fun e -> if lifetimeRevenue > 0.0 then Some((i.DirectCac - e) / lifetimeRevenue) else None)
      BreakEvenSharePv = enablementPerDeal |> Option.bind (fun e -> if pvFactor * i.RevenuePerSponsor > 0.0 then Some((i.DirectCac - e) / (i.RevenuePerSponsor * pvFactor)) else None)
      MonthsToFirstPartnerDeal = if i.DealsPerPartnerPerYear > 0.0 then Some(i.SalesCycleMonths + 12.0 / i.DealsPerPartnerPerYear) else None
      VendorNetRevenuePerYear = i.RevenuePerSponsor * (1.0 - i.PartnerShare) }

/// Partner route is cheaper than direct acquisition when its cost per sponsor is below the direct CAC.
let partnerCheaper (r: Result) = r.PartnerCost |> Option.map (fun c -> c < r.DirectCac)
