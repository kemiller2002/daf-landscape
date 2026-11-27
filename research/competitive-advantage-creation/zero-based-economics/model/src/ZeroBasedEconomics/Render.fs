/// Output tables (CSV) and the generated results report (Markdown). Pure: returns file name -> text.
module ZeroBasedEconomics.Render

open System
open System.Globalization
open ZeroBasedEconomics.Domain
open ZeroBasedEconomics.Inputs
open ZeroBasedEconomics.Engine
open ZeroBasedEconomics.Analysis
open ZeroBasedEconomics.Csv

let f0 (x: float) = if Double.IsNaN x then "" else Math.Round(x, 0).ToString("0", CultureInfo.InvariantCulture)
let f2 (x: float) = if Double.IsNaN x then "" else Math.Round(x, 2).ToString("0.00", CultureInfo.InvariantCulture)
let money (x: float) =
    let a = abs x
    let s =
        if a >= 1e6 then (x / 1e6).ToString("0.00", CultureInfo.InvariantCulture) + "M"
        elif a >= 1e3 then (x / 1e3).ToString("0.0", CultureInfo.InvariantCulture) + "k"
        else x.ToString("0", CultureInfo.InvariantCulture)
    if x < 0.0 then "-$" + s.TrimStart('-') else "$" + s
let optInt (o: int option) = o |> Option.map string |> Option.defaultValue ("never (≤" + string scanLimit + ")")
let optAua (o: float option) = o |> Option.map (fun x -> money (x * 1e6)) |> Option.defaultValue "n/a"

let outcomeHeader =
    [ "model"; "customers"; "mix"; "factors"; "tier"; "accounts"; "aua_musd"; "transactions"; "exceptions"; "ef_cash_annual"
      "ef_monthly_burn"; "ef_nonlabor_cash"; "labor_cash"; "founder_hours"; "founder_noncash"; "fully_loaded"; "employees"
      "contract_hours"; "coverage"; "sponsor_cost"; "sponsor_hours"; "revenue_ref"; "margin_cash" ]

let outcomeRow (o: Outcome) =
    [ modelCode o.Model; string o.Scenario.Customers; o.Scenario.MixId; factorCode o.Scenario.Factors; string o.Scenario.Tier
      f0 o.Volume.Accounts; f2 o.Volume.AuaM; f0 o.Volume.Transactions; f0 o.Volume.Exceptions; f0 o.EfCash; f0 (o.EfCash / 12.0)
      f0 o.EfNonLaborCash; f0 o.LaborCash; f0 o.FounderHours; f0 o.FounderNoncash; f0 o.FullyLoaded; string o.Employees
      f0 o.ContractHours
      (o.Coverage |> List.map (fun c -> $"{c.CoverageId}:{c.Choice}") |> fun xs -> String.Join(";", xs))
      f0 o.SponsorCost; f0 o.SponsorHours; f0 o.Revenue; f0 (o.Revenue - o.EfCash) ]

/// Expense activation: first base-mix customer count at which each expense becomes EF cost under each model.
let activation (p: Inputs) =
    let header = [ "expense_id"; "name"; "classification"; "obligation"; "entity" ] @ (allModels |> List.map (fun m -> "first_n_" + modelCode m)) @ [ "base_annual_at_10_L"; "base_annual_at_10_F" ]
    let firstN (e: Expense) m =
        if not (e.EfModels.Contains m) then "-"
        else
            [ 0..200 ]
            |> List.tryFind (fun n -> (evaluate p m (baseSc n)).Lines |> List.exists (fun l -> l.Bearer = EF && l.Expense.Id = e.Id))
            |> Option.map string
            |> Option.defaultValue ">200"
    let at10 (e: Expense) m =
        (evaluate p m (baseSc 10)).Lines |> List.filter (fun l -> l.Bearer = EF && l.Expense.Id = e.Id) |> List.sumBy (fun l -> l.Cash) |> f0
    write header
        [ for e in p.Expenses ->
              [ e.Id; e.Name; classCode e.Class; obligationCode e.Obligation; e.Entity ] @ (allModels |> List.map (firstN e)) @ [ at10 e L; at10 e F ] ]

let workload (p: Inputs) =
    let header = [ "activity_id"; "name"; "role"; "driver"; "ef_models"; "sponsor_models"; "hours_at_1"; "hours_at_10"; "hours_at_100"; "conventional_hours_at_10" ]
    let v n = volume p L (baseSc n)
    write header
        [ for a in p.Activities ->
              let conv = driverUnits (v 10) a.Driver * a.Rate.Base * a.ConventionalMinutes / 60.0
              [ a.Id; a.Name; a.Role; actDriverCode a.Driver
                (a.EfModels |> Set.toList |> List.map modelCode |> fun xs -> String.Join(" ", xs))
                (a.SponsorModels |> Set.toList |> List.map modelCode |> fun xs -> String.Join(" ", xs))
                f2 (activityHours (v 1) a); f2 (activityHours (v 10) a); f2 (activityHours (v 100) a); f2 conv ] ]

let thresholdsCsv (ts: Threshold list) =
    write [ "model"; "mix"; "threshold"; "customers"; "detail" ] [ for t in ts -> [ modelCode t.Model; t.MixId; t.What; optInt t.Customers; t.Detail ] ]

let breakEvenCsv (bs: BreakEven list) =
    write [ "model"; "bps"; "cash_customers"; "loaded_customers"; "cash_aua_musd"; "loaded_aua_musd" ]
        [ for b in bs ->
              [ modelCode b.Model; (b.Bps |> Option.map f0 |> Option.defaultValue "ref price"); optInt b.CashCustomers; optInt b.LoadedCustomers
                (b.CashAuaM |> Option.map f2 |> Option.defaultValue ""); (b.LoadedAuaM |> Option.map f2 |> Option.defaultValue "") ] ]

let pricingCsv (ps: PriceFloor list) =
    write [ "model"; "customers"; "cash_per_customer"; "loaded_per_customer"; "cash_per_account"; "loaded_per_account"; "marginal_per_customer"; "cash_bps"; "loaded_bps" ]
        [ for x in ps ->
              [ modelCode x.Model; string x.Customers; f0 x.CashPerCustomer; f0 x.LoadedPerCustomer; f2 x.CashPerAccount; f2 x.LoadedPerAccount
                f0 x.MarginalPerCustomer; f2 x.CashBps; f2 x.LoadedBps ] ]

let capitalCsv (cs: Capital list) =
    write [ "model"; "level"; "qualification_cash"; "qualification_founder_hours"; "pre_revenue_burn"; "readiness"; "working_capital"; "excluding_qualification"; "total"; "monthly_burn_0"; "monthly_burn_1"; "surplus_1" ]
        [ for c in cs ->
              [ modelCode c.Model; levelCode c.Level; f0 c.QualificationCash; f0 c.QualificationFounderHours; f0 c.PreRevenueBurn; f0 c.Readiness
                f0 c.WorkingCapital; f0 c.ExcludingQualification; f0 c.Total; f0 c.MonthlyBurnZero; f0 c.MonthlyBurnOne; f0 c.SurplusOne ] ]

let priorsCsv (rows: (PriorEstimate * (string * (Level * float) list) list) list) =
    write [ "prior_id"; "name"; "original"; "metric"; "revised_low"; "revised_base"; "revised_high" ]
        [ for pr, ms in rows do
              for mt, vals in ms ->
                  let v l = vals |> List.find (fun (x, _) -> x = l) |> snd
                  [ pr.Id; pr.Name; pr.Value; mt; f0 (v Low); f0 (v Base); f0 (v High) ] ]

let tornadoCsv (rows: TornadoRow list) =
    write [ "metric"; "input"; "base"; "at_low"; "at_high"; "swing" ] [ for r in rows -> [ r.Metric; r.Name; f0 r.Base; f0 r.Low; f0 r.High; f0 (abs (r.High - r.Low)) ] ]

let mcCsv (rows: (string * float * float * float * float) list) =
    write [ "metric"; "rho"; "p10"; "p50"; "p90" ] [ for m, rho, a, b, c in rows -> [ m; f2 rho; f0 a; f0 b; f0 c ] ]

let selfFinCsv (rows: (ModelId * int * float * float) list) =
    write [ "model"; "customers"; "surplus_cash"; "surplus_loaded" ] [ for m, n, a, b in rows -> [ modelCode m; string n; f0 a; f0 b ] ]

// ------------------------------------------------------------------------------------------------ markdown

let table (header: string list) (rows: string list list) =
    let line xs = "| " + String.Join(" | ", (xs: string list)) + " |"
    String.Join("\n", [ line header; line (header |> List.map (fun _ -> "---")) ] @ (rows |> List.map line))

type Bundle =
    { Base: Inputs
      Headline: Outcome list
      Thresholds: Threshold list
      BreakEvens: BreakEven list
      SingleAua: (float * (float option * float option)) list
      Prices: PriceFloor list
      Capital: Capital list
      SelfFin: (ModelId * int * float * float) list
      Priors: (PriorEstimate * (string * (Level * float) list) list) list
      Tornado: TornadoRow list
      Mc: (string * float * float * float * float) list
      GridStats: (ModelId * int * float * float * float) list }

let results (b: Bundle) =
    let hl tier m n = b.Headline |> List.find (fun o -> o.Scenario.Tier = tier && o.Model = m && o.Scenario.Customers = n)
    let sec1 =
        table ([ "Model" ] @ (counts |> List.map (fun n -> $"{n}")))
            [ for m in allModels -> [ $"{modelCode m} {modelName m}" ] @ (counts |> List.map (fun n -> money (hl 1 m n).EfCash)) ]
    let secLoaded =
        table ([ "Model" ] @ (counts |> List.map (fun n -> $"{n}")))
            [ for m in allModels -> [ modelCode m ] @ (counts |> List.map (fun n -> money (hl 1 m n).FullyLoaded)) ]
    let secTier =
        table [ "Model"; "Tier 0 (mandatory only), 1 customer"; "Tier 1 (typical contract)"; "Tier 2 (demanding)"; "Tier 0, 10 customers"; "Tier 1"; "Tier 2" ]
            [ for m in allModels -> [ modelCode m; money (hl 0 m 1).EfCash; money (hl 1 m 1).EfCash; money (hl 2 m 1).EfCash; money (hl 0 m 10).EfCash; money (hl 1 m 10).EfCash; money (hl 2 m 10).EfCash ] ]
    let secStaff =
        table [ "Model"; "Customers"; "Founder hours"; "Employees"; "Contract hours"; "Coverage" ]
            [ for m in allModels do
                  for n in counts ->
                      let o = hl 1 m n
                      [ modelCode m; string n; f0 o.FounderHours; string o.Employees; f0 o.ContractHours
                        (o.Coverage |> List.map (fun c -> $"{c.CoverageId} {c.Choice} {money c.Annual}") |> fun xs -> String.Join("; ", xs)) ] ]
    let secThr =
        table [ "Model"; "Mix"; "Threshold"; "Customers"; "Detail" ]
            [ for t in b.Thresholds |> List.filter (fun t -> t.What <> "founder fully utilised" || true) -> [ modelCode t.Model; t.MixId; t.What; optInt t.Customers; t.Detail ] ]
    let secBe =
        table [ "Model"; "Fee"; "Cash break-even customers"; "Fully loaded"; "Cash AUA"; "Loaded AUA" ]
            [ for x in b.BreakEvens -> [ modelCode x.Model; (x.Bps |> Option.map (fun v -> f0 v + " bps") |> Option.defaultValue "reference price"); optInt x.CashCustomers; optInt x.LoadedCustomers; optAua x.CashAuaM; optAua x.LoadedAuaM ] ]
    let secSingle =
        table [ "Fee (bps)"; "One customer: cash break-even AUA"; "Fully loaded" ] [ for bps, (c, l) in b.SingleAua -> [ f0 bps; optAua c; optAua l ] ]
    let secPrice =
        table [ "Model"; "Customers"; "Cash $/customer"; "Loaded $/customer"; "Cash $/account"; "Loaded $/account"; "Marginal $/customer"; "Cash bps"; "Loaded bps" ]
            [ for x in b.Prices -> [ modelCode x.Model; string x.Customers; money x.CashPerCustomer; money x.LoadedPerCustomer; f2 x.CashPerAccount; f2 x.LoadedPerAccount; money x.MarginalPerCustomer; f2 x.CashBps; f2 x.LoadedBps ] ]
    let secCap =
        table [ "Model"; "Level"; "Qualification cash"; "Founder hours to qualify"; "Pre-revenue burn"; "Readiness"; "Working capital"; "Capital excl. qualification"; "Total"; "Burn/mo at 0"; "Burn/mo at 1"; "Surplus at 1" ]
            [ for c in b.Capital -> [ modelCode c.Model; levelCode c.Level; money c.QualificationCash; f0 c.QualificationFounderHours; money c.PreRevenueBurn; money c.Readiness; money c.WorkingCapital; money c.ExcludingQualification; money c.Total; money c.MonthlyBurnZero; money c.MonthlyBurnOne; money c.SurplusOne ] ]
    let secSelf =
        table ([ "Model" ] @ ([ 1..10 ] |> List.map string))
            [ for m in allModels -> [ modelCode m ] @ (b.SelfFin |> List.filter (fun (x, _, _, _) -> x = m) |> List.map (fun (_, _, s, _) -> money s)) ]
    let secPriors =
        table [ "Prior"; "Original"; "Comparable"; "Revised low"; "Base"; "High" ]
            [ for pr, ms in b.Priors do
                  for mt, vals in ms ->
                      let v l = vals |> List.find (fun (x, _) -> x = l) |> snd
                      [ $"{pr.Id} {pr.Name}"; pr.Value; mt; money (v Low); money (v Base); money (v High) ] ]
    let secMc =
        table [ "Metric"; "ρ"; "P10"; "P50"; "P90" ] [ for m, rho, a, c, d in b.Mc -> [ m; f2 rho; f2 a; f2 c; f2 d ] ]
    let secTor =
        table [ "Metric"; "Input"; "At low"; "At high"; "Swing" ] [ for r in b.Tornado |> List.truncate 30 -> [ r.Metric; r.Name; money r.Low; money r.High; money (abs (r.High - r.Low)) ] ]
    let secGrid =
        table [ "Model"; "Customers"; "Min EF cash (81 factor combos × mixes)"; "Median"; "Max" ]
            [ for m, n, a, c, d in b.GridStats -> [ modelCode m; string n; money a; money c; money d ] ]
    String.concat "\n\n"
        [ "# Zero-based operating economics: generated results"
          "Generated by `model/` from `data/inputs/`. Do not edit by hand: `run` regenerates it and `check` verifies byte-identical reproduction. Base case: mix `mixed`, base volume factors, contract tier 1 (typical institutional contract), base cost levels. Money is annual USD unless stated."
          "## 1. Echelon Foundry annual cash operating cost by customer count (tier 1)"
          sec1
          "## 2. Fully loaded economic cost (cash + allocated shared cost + founder labour at market rate + amortised qualification)"
          secLoaded
          "## 3. Mandatory obligations versus contractual expectations (annual EF cash)"
          secTier
          "## 4. Staffing by model and customer count (tier 1)"
          secStaff
          "## 5. Staffing thresholds by mix"
          secThr
          "## 6. Independent variation of accounts, assets, transactions and exceptions (all mixes, 81 combinations each)"
          secGrid
          "## 7. Break-even at reference prices; full-service administration by fee"
          secBe
          "## 8. Single-customer break-even assets for full-service administration"
          secSingle
          "## 9. Break-even prices (what each customer must pay for revenue to equal cost)"
          secPrice
          "## 10. Capital before first revenue (production qualification shown separately; low = all inputs favourable, high = all adverse)"
          secCap
          "## 11. Annual surplus at 1-10 customers (reference prices): can the first customer finance the next?"
          secSelf
          "## 12. Prior estimates and zero-based comparables (low = all inputs favourable, high = all adverse)"
          secPriors
          "## 13. Monte Carlo (2,000 draws, seed 20261127; independent and ρ=0.5 adverse-correlated)"
          secMc
          "## 14. Tornado (top inputs by swing)"
          secTor ]
    + "\n"

let all (inp: Inputs) : (string * string) list =
    let p = realize (atLevel Base) inp
    let hl = headline p
    let gridRows = grid p
    let gridStats =
        [ for m in allModels do
              for n in counts ->
                  let xs = gridRows |> List.filter (fun o -> o.Model = m && o.Scenario.Customers = n) |> List.map (fun o -> o.EfCash)
                  m, n, List.min xs, Sampling.percentile 0.5 xs, List.max xs ]
    let thr = staffingThresholds p
    let bes = breakEvens p
    let single = bpsGrid |> List.map (fun b -> b, singleCustomerBreakEvenAua p b)
    let prices = priceFloors p
    let cap = capital inp
    let sf = selfFinancing p
    let pri = priorComparables inp
    let tor =
        [ "L first-customer annual cash"; "F first-customer annual cash"; "F cash break-even bps at 10 customers" ]
        |> List.collect (tornado inp)
    let mc = monteCarlo inp 2000 20261127UL
    let bundle =
        { Base = p; Headline = hl; Thresholds = thr; BreakEvens = bes; SingleAua = single; Prices = prices; Capital = cap; SelfFin = sf
          Priors = pri; Tornado = tor; Mc = mc; GridStats = gridStats }
    [ "headline.csv", write outcomeHeader (hl |> List.map outcomeRow)
      "scenario-grid.csv", write outcomeHeader (gridRows |> List.map outcomeRow)
      "expense-activation.csv", activation p
      "workload.csv", workload p
      "staffing-thresholds.csv", thresholdsCsv thr
      "break-even.csv", breakEvenCsv bes
      "price-floors.csv", pricingCsv prices
      "capital.csv", capitalCsv cap
      "self-financing.csv", selfFinCsv sf
      "prior-estimates-revised.csv", priorsCsv pri
      "tornado.csv", tornadoCsv tor
      "monte-carlo.csv", mcCsv mc
      "results.md", results bundle ]
