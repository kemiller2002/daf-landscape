/// Staffing, cost and revenue model at multiple scales (deliverable 09).
/// Every parameter carries a basis: Sourced (repository evidence path) or Assumed [A].
/// Accounts and assets under management are modeled separately (brief §11).
module Daf.Enterprise.Economics

open System

type Basis =
    | Sourced of string
    | Assumed of string

type Param = { Name: string; Value: decimal; Basis: Basis }

let private p name value basis = { Name = name; Value = value; Basis = basis }

// ---------- scenario inputs ----------
type Scenario =
    { Label: string
      Accounts: decimal
      AvgBalance: decimal              // AUM per account; AUM = Accounts * AvgBalance
      GrantsPerAccount: decimal
      ContributionsPerAccount: decimal
      ComplexAssetShare: decimal       // share of contributions needing specialist acceptance
      ExceptionRate: decimal           // share of grants routed to a human
      NewAccountShare: decimal }       // new accounts per year as share of book

let aum (s: Scenario) = s.Accounts * s.AvgBalance

// ---------- parameters (all labeled) ----------
type Parameters =
    { MinutesPerException: Param
      HoursPerComplexAsset: Param
      ProductiveHoursPerFte: Param
      BreakRate: Param
      MinutesPerBreak: Param
      HumanContactsPerAccount: Param
      MinutesPerHumanContact: Param
      LoadedCostPerFteAiNative: Param
      InferencePerException: Param
      AiInteractionsPerAccount: Param
      InferencePerInteraction: Param
      InfraBase: Param
      InfraPerAccount: Param
      CustodyBps: Param
      AchShare: Param
      AchCost: Param
      CheckCost: Param
      InsuranceBase: Param
      AuditBase: Param
      AuditBpsOfAum: Param
      LegalBase: Param
      DataProvidersBase: Param
      IdentityPerNewAccount: Param
      CacPerNewAccount: Param
      AgentFamilies: Param
      // conventional comparators (FY2024 Form 990, repository dataset)
      ConvAccountsPerEmployeeEfficient: Param
      ConvAccountsPerEmployeeTypical: Param
      ConvStaffCostPerEmployee: Param
      ConvNonStaffOpexPerAccount: Param
      FrontierAllInPerAccount: Param }

let efficiencyCsv = "data/mission-2026-11-14/sponsor-operating-efficiency-2026-11-20.csv"

let defaults =
    { MinutesPerException = p "minutes per human exception decision (with AI-prepared dossier)" 45m (Assumed "no sponsor publishes reviewer minutes (GAP-001); 45 min chosen; sensitivity 20-120")
      HoursPerComplexAsset = p "specialist hours per complex asset gift" 12m (Assumed "no public time study; sensitivity 6-30")
      ProductiveHoursPerFte = p "productive hours per FTE per year" 1600m (Assumed "standard planning convention")
      BreakRate = p "reconciliation breaks per transaction" 0.01m (Assumed "GAP-005 reconciliation break cost unmeasured")
      MinutesPerBreak = p "human minutes per break reaching a person" 20m (Assumed "after deterministic and agent triage")
      HumanContactsPerAccount = p "human service contacts per account per year" 0.3m (Assumed "GAP-006 contact volumes unmeasured; most status questions removed by shared state")
      MinutesPerHumanContact = p "minutes per human contact" 20m (Assumed "")
      LoadedCostPerFteAiNative = p "loaded cost per FTE, AI-native (specialist-heavy mix)" 165000m (Assumed "above conventional $124.5k (Vanguard FY2024 staff cost/employee) because the mix is specialists and engineers")
      InferencePerException = p "inference cost per exception dossier (all agents)" 0.90m (Sourced "~$0.45 per heavy review (industry report §7, EV-106) x2 for multiple agents; pricing date per source")
      AiInteractionsPerAccount = p "AI service interactions per account per year" 4m (Assumed "")
      InferencePerInteraction = p "inference cost per grounded service interaction" 0.05m (Assumed "")
      InfraBase = p "infrastructure, base per year" 250000m (Assumed "managed cloud, two regions, observability, security tooling")
      InfraPerAccount = p "infrastructure per account per year" 3m (Assumed "")
      CustodyBps = p "custody and pool administration, bps of AUM" 0.5m (Assumed "institutional mutual-fund/ETF custody; contract-dependent")
      AchShare = p "share of grants paid electronically" 0.9m (Assumed "Fidelity reports 67% of grants via EFT (EV, industry report §2.5); 90% is a design target")
      AchCost = p "cost per electronic grant payment" 0.30m (Assumed "bank ACH pricing is contract-dependent")
      CheckCost = p "all-in cost per check grant" 4m (Assumed "print, postage, positive pay, escheat handling")
      InsuranceBase = p "insurance (D&O, crime, cyber, E&O) base" 150000m (Assumed "")
      AuditBase = p "external audit base" 120000m (Assumed "")
      AuditBpsOfAum = p "external audit scaling, bps of AUM" 0.02m (Assumed "")
      LegalBase = p "outside counsel and filings base" 200000m (Assumed "")
      DataProvidersBase = p "charity data, sanctions screening, identity platform base" 100000m (Assumed "IRS bulk data is free; commercial enrichment is not")
      IdentityPerNewAccount = p "identity verification per new account" 3m (Assumed "")
      CacPerNewAccount = p "customer acquisition cost per new account" 400m (Assumed "advisor-channel; no public DAF CAC (GAP)")
      AgentFamilies = p "agent families in production" 31m (Assumed "19 parent agents + 12 workflow-innovation agent opportunities (reconciled 2026-11-21, OUTSTANDING A2/A7)")
      ConvAccountsPerEmployeeEfficient = p "conventional accounts per employee, efficient (Vanguard Charitable FY2024)" 232.44m (Sourced efficiencyCsv)
      ConvAccountsPerEmployeeTypical = p "conventional accounts per employee, typical (AEF FY2024)" 107.03m (Sourced efficiencyCsv)
      ConvStaffCostPerEmployee = p "conventional staff cost per employee (Vanguard Charitable FY2024: $14,816,404 / 119)" 124507m (Sourced efficiencyCsv)
      ConvNonStaffOpexPerAccount = p "conventional non-staff opex per account (Vanguard FY2024: 16.41 bps x $21.95bn less staff cost, / 27,660 accounts)" 766m (Sourced $"{efficiencyCsv}; derived")
      FrontierAllInPerAccount = p "frontier all-in opex per account (Fidelity Charitable FY2024: 24.41 bps x $66.20bn / 204,614 accounts; affiliate-staffed, so staff sit at FMR and are paid through fees)" 790m (Sourced $"{efficiencyCsv}; derived") }

let register (ps: Parameters) : Param list =
    [ ps.MinutesPerException; ps.HoursPerComplexAsset; ps.ProductiveHoursPerFte; ps.BreakRate; ps.MinutesPerBreak
      ps.HumanContactsPerAccount; ps.MinutesPerHumanContact; ps.LoadedCostPerFteAiNative; ps.InferencePerException
      ps.AiInteractionsPerAccount; ps.InferencePerInteraction; ps.InfraBase; ps.InfraPerAccount; ps.CustodyBps
      ps.AchShare; ps.AchCost; ps.CheckCost; ps.InsuranceBase; ps.AuditBase; ps.AuditBpsOfAum; ps.LegalBase
      ps.DataProvidersBase; ps.IdentityPerNewAccount; ps.CacPerNewAccount; ps.AgentFamilies
      ps.ConvAccountsPerEmployeeEfficient; ps.ConvAccountsPerEmployeeTypical; ps.ConvStaffCostPerEmployee; ps.ConvNonStaffOpexPerAccount; ps.FrontierAllInPerAccount ]

// ---------- revenue: published admin-fee tiers ----------
/// Fidelity Charitable Giving Account tiers (data/mission-2026-11-14/sponsor-fee-schedules.csv), $100 minimum.
let fidelityTiers = [ 0m, 500000m, 0.0060m; 500000m, 1000000m, 0.0030m; 1000000m, 2500000m, 0.0020m; 2500000m, 5000000m, 0.0015m ]

let tieredFee (tiers: (decimal * decimal * decimal) list) (minimum: decimal) (balance: decimal) =
    tiers
    |> List.sumBy (fun (lo, hi, rate) -> (max 0m (min balance hi - lo)) * rate)
    |> max minimum

/// Average-account approximation. Because the tier schedule is concave, applying it to the
/// average balance OVERSTATES revenue when balances are skewed (Jensen); see sensitivity.
let annualRevenue (s: Scenario) = s.Accounts * tieredFee fidelityTiers 100m s.AvgBalance

// ---------- staffing ----------
type Role =
    | Leadership
    | GrantsCompliance
    | ComplexAssets
    | FinanceAndPaymentsOps
    | ServiceRecovery
    | Engineering
    | AgentOwnershipAndEvaluation
    | Security
    | Partnerships
    | PhilanthropicIntelligence

let private ceilD (x: decimal) = Math.Ceiling x

let fteByRole (ps: Parameters) (s: Scenario) : (Role * decimal) list =
    let hours = ps.ProductiveHoursPerFte.Value
    let grants = s.Accounts * s.GrantsPerAccount
    let contributions = s.Accounts * s.ContributionsPerAccount
    let exceptions = grants * s.ExceptionRate
    let complex = contributions * s.ComplexAssetShare
    let breaks = (grants + contributions) * ps.BreakRate.Value
    let leadership =
        if s.Accounts < 5000m then 5m      // CEO, CFO/COO, CRCO/GC, CTO, head of grants & client ops
        elif s.Accounts < 50000m then 8m
        else 10m
    let grantsCompliance = max 1m (ceilD (exceptions * ps.MinutesPerException.Value / 60m / hours))
    let complexAssets = max 1m (ceilD (complex * ps.HoursPerComplexAsset.Value / hours))
    // Segregation of duties requires at least two people in finance/payments operations.
    let finance = max 2m (ceilD (breaks * ps.MinutesPerBreak.Value / 60m / hours) + 1m)
    let service = max 1m (ceilD (s.Accounts * ps.HumanContactsPerAccount.Value * ps.MinutesPerHumanContact.Value / 60m / hours))
    let engineering = ceilD (4m + 2m * decimal (Math.Log10(float (max 1000m s.Accounts) / 1000.0)))
    let agentOwners = ceilD (ps.AgentFamilies.Value / 6m) + 1m
    let security = if s.Accounts >= 100000m then 3m else 1m
    let partnerships = max 1m (ceilD (s.Accounts / 20000m))
    let intelligence = if s.Accounts >= 100000m then 3m else 1m
    [ Leadership, leadership; GrantsCompliance, grantsCompliance; ComplexAssets, complexAssets
      FinanceAndPaymentsOps, finance; ServiceRecovery, service; Engineering, engineering
      AgentOwnershipAndEvaluation, agentOwners; Security, security; Partnerships, partnerships
      PhilanthropicIntelligence, intelligence ]

let totalFte ps s = fteByRole ps s |> List.sumBy snd

// ---------- costs ----------
type CostLine = { Line: string; Amount: decimal }

let aiNativeCosts (ps: Parameters) (s: Scenario) : CostLine list =
    let grants = s.Accounts * s.GrantsPerAccount
    let exceptions = grants * s.ExceptionRate
    let newAccounts = s.Accounts * s.NewAccountShare
    let a = aum s
    [ { Line = "staff"; Amount = totalFte ps s * ps.LoadedCostPerFteAiNative.Value }
      { Line = "AI inference"; Amount = exceptions * ps.InferencePerException.Value + s.Accounts * ps.AiInteractionsPerAccount.Value * ps.InferencePerInteraction.Value }
      { Line = "infrastructure"; Amount = ps.InfraBase.Value + s.Accounts * ps.InfraPerAccount.Value }
      { Line = "custody and pool administration"; Amount = a * ps.CustodyBps.Value / 10000m }
      { Line = "payments"; Amount = grants * (ps.AchShare.Value * ps.AchCost.Value + (1m - ps.AchShare.Value) * ps.CheckCost.Value) }
      { Line = "insurance"; Amount = ps.InsuranceBase.Value * (1m + decimal (Math.Log10(float (max 1000m s.Accounts) / 1000.0))) }
      { Line = "external audit"; Amount = ps.AuditBase.Value + a * ps.AuditBpsOfAum.Value / 10000m }
      { Line = "legal, compliance and filings"; Amount = ps.LegalBase.Value * (1m + decimal (Math.Log10(float (max 1000m s.Accounts) / 1000.0))) }
      { Line = "data providers and identity"; Amount = ps.DataProvidersBase.Value + newAccounts * ps.IdentityPerNewAccount.Value }
      { Line = "customer acquisition"; Amount = newAccounts * ps.CacPerNewAccount.Value } ]

let total (lines: CostLine list) = lines |> List.sumBy (fun l -> l.Amount)

type ConventionalVariant =
    | Efficient
    | Typical

/// Conventional comparator calibrated to self-staffed nationals' FY2024 Form 990s.
/// Structural floor of 8 people applies at small scale.
let conventionalFte (ps: Parameters) (v: ConventionalVariant) (s: Scenario) =
    let perEmp =
        match v with
        | Efficient -> ps.ConvAccountsPerEmployeeEfficient.Value
        | Typical -> ps.ConvAccountsPerEmployeeTypical.Value
    max 8m (ceilD (s.Accounts / perEmp))

let conventionalCost (ps: Parameters) (v: ConventionalVariant) (s: Scenario) =
    conventionalFte ps v s * ps.ConvStaffCostPerEmployee.Value + s.Accounts * ps.ConvNonStaffOpexPerAccount.Value

// ---------- results ----------
type Result =
    { Scenario: Scenario
      Aum: decimal
      Grants: decimal
      Exceptions: decimal
      AiNativeFte: decimal
      ConvFteEfficient: decimal
      ConvFteTypical: decimal
      AiNativeCost: decimal
      ConvCostEfficient: decimal
      Revenue: decimal
      AiNativeMargin: decimal
      AiNativeCostBps: decimal
      ConvCostBpsEfficient: decimal
      AccountsPerFte: decimal
      AiNativeCostPerAccount: decimal
      FrontierCostPerAccount: decimal }

let evaluate (ps: Parameters) (s: Scenario) : Result =
    let costs = aiNativeCosts ps s |> total
    let rev = annualRevenue s
    let a = aum s
    let fte = totalFte ps s
    { Scenario = s
      Aum = a
      Grants = s.Accounts * s.GrantsPerAccount
      Exceptions = s.Accounts * s.GrantsPerAccount * s.ExceptionRate
      AiNativeFte = fte
      ConvFteEfficient = conventionalFte ps Efficient s
      ConvFteTypical = conventionalFte ps Typical s
      AiNativeCost = costs
      ConvCostEfficient = conventionalCost ps Efficient s
      Revenue = rev
      AiNativeMargin = if rev = 0m then 0m else (rev - costs) / rev
      AiNativeCostBps = if a = 0m then 0m else costs / a * 10000m
      ConvCostBpsEfficient = if a = 0m then 0m else conventionalCost ps Efficient s / a * 10000m
      AccountsPerFte = s.Accounts / fte
      AiNativeCostPerAccount = costs / s.Accounts
      FrontierCostPerAccount = ps.FrontierAllInPerAccount.Value }

/// Base scenario at a given account count. GrantsPerAccount 8 sits inside the FY2024
/// observed range 6.2 (RCF) to 13.0 (Fidelity) computed from the efficiency dataset.
/// ExceptionRate 8% sits at the per-grant core proxy (~7–8.5% of grants, EV-079 / strategic synthesis §0 A).
let baseScenario accounts =
    { Label = $"{accounts:N0} accounts"
      Accounts = accounts
      AvgBalance = 300000m           // FY2024 avg account: Fidelity $324k, RCF $229k, AEF $525k, Vanguard $794k (efficiency dataset)
      GrantsPerAccount = 8m
      ContributionsPerAccount = 2m   // [A]
      ComplexAssetShare = 0.02m      // [A]
      ExceptionRate = 0.08m
      NewAccountShare = 0.15m }      // [A]

let scales = [ 1000m; 10000m; 100000m; 1000000m ]

/// Smallest account count (to 1,000-account resolution, up to 2m) at which revenue covers cost.
let breakEvenAccounts (ps: Parameters) (template: decimal -> Scenario) =
    [ 1000m .. 1000m .. 2000000m ]
    |> List.tryFind (fun n -> let r = evaluate ps (template n) in r.Revenue >= r.AiNativeCost)

// ---------- sensitivity ----------
type Sensitivity = { Factor: string; Low: decimal; High: decimal }

/// One-at-a-time sensitivity of AI-native cost at a given scale: each factor x0.5 and x2.
let sensitivity (ps: Parameters) (s: Scenario) : Sensitivity list =
    let scaleParam (f: Param) k = { f with Value = f.Value * k }
    let run (ps': Parameters) (s': Scenario) = (evaluate ps' s').AiNativeCost
    let cases : (string * (decimal -> Parameters * Scenario)) list =
        [ "minutes per exception", (fun k -> { ps with MinutesPerException = scaleParam ps.MinutesPerException k }, s)
          "exception rate", (fun k -> ps, { s with ExceptionRate = s.ExceptionRate * k })
          "loaded cost per FTE", (fun k -> { ps with LoadedCostPerFteAiNative = scaleParam ps.LoadedCostPerFteAiNative k }, s)
          "human contacts per account", (fun k -> { ps with HumanContactsPerAccount = scaleParam ps.HumanContactsPerAccount k }, s)
          "complex asset share", (fun k -> ps, { s with ComplexAssetShare = s.ComplexAssetShare * k })
          "customer acquisition cost", (fun k -> { ps with CacPerNewAccount = scaleParam ps.CacPerNewAccount k }, s)
          "inference cost (x0.5 / x10)", (fun k -> { ps with InferencePerException = scaleParam ps.InferencePerException (if k > 1m then 10m else k); InferencePerInteraction = scaleParam ps.InferencePerInteraction (if k > 1m then 10m else k) }, s)
          "grants per account", (fun k -> ps, { s with GrantsPerAccount = s.GrantsPerAccount * k })
          "infrastructure", (fun k -> { ps with InfraBase = scaleParam ps.InfraBase k; InfraPerAccount = scaleParam ps.InfraPerAccount k }, s) ]
    cases
    |> List.map (fun (name, mk) ->
        let (pl, sl) = mk 0.5m
        let (ph, sh) = mk 2m
        { Factor = name; Low = run pl sl; High = run ph sh })

// ---------- Model C: infrastructure provider economics ----------
/// Incumbent price reference: RCF paid Ren $19,225,546 in FY2024 (audited) for 25,824 accounts
/// (= ~$745 per account; ~32.5 bps of RCF's $5.91bn DAF assets). Repository: data/rcf-ren-audited-admin-payments-2020-2024.csv
/// and the efficiency dataset. This is one related-party contract, not a market price.
let rcfRenPaymentFy2024 = 19225546m
let rcfAccountsFy2024 = 25824m

type ProviderScenario =
    { SponsorClients: decimal
      AccountsServed: decimal
      PricePerAccount: decimal }      // [A] hypothesis; compare with ~$745 incumbent reference

/// Provider cost = AI-native operating stack minus sponsor-only functions (board, investment
/// committee, sponsor legal, CAC borne by sponsors), plus per-client onboarding and support.
let providerCost (ps: Parameters) (p: ProviderScenario) =
    let s = { baseScenario p.AccountsServed with NewAccountShare = 0m }
    let lines = aiNativeCosts ps s
    let excluded = set [ "customer acquisition"; "custody and pool administration" ]
    let shared = lines |> List.filter (fun l -> not (excluded.Contains l.Line)) |> total
    shared + p.SponsorClients * 60000m // [A] per-client implementation, support and contract management

let providerRevenue (p: ProviderScenario) = p.AccountsServed * p.PricePerAccount

// ---------- five-year ramp: time to scale and capital need ----------
type RampYear = { Year: int; Accounts: decimal; Revenue: decimal; Cost: decimal; Cumulative: decimal }

/// B grows by acquiring donor accounts one at a time (CAC applies); C signs sponsor clients
/// that bring existing books (no donor CAC, onboarding cost per client). Paths are [A].
let rampB (ps: Parameters) (avgBalance: decimal) (newAccountsByYear: decimal list) =
    newAccountsByYear
    |> List.mapi (fun i n -> i + 1, n)
    |> List.fold (fun (acc: RampYear list, book, cum) (y, n) ->
        let book' = book + n
        let s = { baseScenario book' with AvgBalance = avgBalance; NewAccountShare = (if book' = 0m then 0m else n / book') }
        let r = evaluate ps s
        let cum' = cum + r.Revenue - r.AiNativeCost
        (acc @ [ { Year = y; Accounts = book'; Revenue = r.Revenue; Cost = r.AiNativeCost; Cumulative = cum' } ], book', cum')) ([], 0m, 0m)
    |> fun (rows, _, _) -> rows

let rampC (ps: Parameters) (pricePerAccount: decimal) (accountsPerClient: decimal) (clientsByYear: decimal list) =
    clientsByYear
    |> List.mapi (fun i n -> i + 1, n)
    |> List.fold (fun (acc: RampYear list, clients, cum) (y, n) ->
        let clients' = clients + n
        let accounts = max 1000m (clients' * accountsPerClient)
        // new clients onboard mid-year: half-year revenue in the signing year
        let billable = (clients + n / 2m) * accountsPerClient
        let pr = { SponsorClients = max 1m clients'; AccountsServed = accounts; PricePerAccount = pricePerAccount }
        let rev = billable * pricePerAccount
        let cost = providerCost ps pr
        let cum' = cum + rev - cost
        (acc @ [ { Year = y; Accounts = clients' * accountsPerClient; Revenue = rev; Cost = cost; Cumulative = cum' } ], clients', cum')) ([], 0m, 0m)
    |> fun (rows, _, _) -> rows

let peakCapitalNeed (rows: RampYear list) = rows |> List.map (fun r -> r.Cumulative) |> List.fold min 0m |> abs
