/// Pure renderers that turn model results into CSV text for 09-financial-models and 11-scenarios.
module Daf.Enterprise.Report

open System
open Daf.Enterprise.Economics
open Daf.Enterprise.Twin

let private r0 (x: decimal) = Math.Round(x, 0).ToString("0")
let private r2 (x: decimal) = Math.Round(x, 2).ToString("0.00")
let private csv (header: string) (rows: string list) = String.Join("\n", header :: rows) + "\n"
let private q (s: string) = "\"" + s.Replace("\"", "\"\"") + "\""

let parameterRegister (ps: Parameters) =
    register ps
    |> List.map (fun p ->
        let kind, note = match p.Basis with Sourced s -> "sourced", s | Assumed s -> "assumed", s
        String.Join(",", [ q p.Name; r2 p.Value; kind; q note ]))
    |> csv "parameter,value,basis,note"

let scaleResults (ps: Parameters) (scenarios: Scenario list) =
    scenarios
    |> List.map (fun s ->
        let r = evaluate ps s
        String.Join(",", [ q s.Label; r0 s.Accounts; r0 r.Aum; r0 r.Grants; r0 r.Exceptions; r0 r.AiNativeFte; r0 r.ConvFteEfficient; r0 r.ConvFteTypical; r0 r.AiNativeCost; r0 r.ConvCostEfficient; r0 r.Revenue; r2 (r.AiNativeMargin * 100m); r2 r.AiNativeCostBps; r2 r.ConvCostBpsEfficient; r0 r.AccountsPerFte; r0 r.AiNativeCostPerAccount; r0 r.FrontierCostPerAccount ]))
    |> csv "scenario,accounts,aum_usd,grants_per_year,human_exceptions_per_year,ai_native_fte,conventional_fte_efficient,conventional_fte_typical,ai_native_cost_usd,conventional_cost_efficient_usd,revenue_usd,ai_native_margin_pct,ai_native_cost_bps,conventional_cost_bps,accounts_per_fte,ai_native_cost_per_account,frontier_cost_per_account_fidelity_fy2024"

let fteByRoleTable (ps: Parameters) (scenarios: Scenario list) =
    scenarios
    |> List.collect (fun s -> fteByRole ps s |> List.map (fun (role, n) -> String.Join(",", [ r0 s.Accounts; $"%A{role}"; r0 n ])))
    |> csv "accounts,role,fte"

let costLines (ps: Parameters) (scenarios: Scenario list) =
    scenarios
    |> List.collect (fun s -> aiNativeCosts ps s |> List.map (fun l -> String.Join(",", [ r0 s.Accounts; q l.Line; r0 l.Amount ])))
    |> csv "accounts,cost_line,usd_per_year"

let sensitivityTable (ps: Parameters) (s: Scenario) =
    let baseCost = (evaluate ps s).AiNativeCost
    sensitivity ps s
    |> List.sortByDescending (fun x -> x.High - x.Low)
    |> List.map (fun x -> String.Join(",", [ q x.Factor; r0 baseCost; r0 x.Low; r0 x.High; r2 ((x.High - x.Low) / baseCost * 100m) ]))
    |> csv "factor,base_cost_usd,cost_at_x0.5,cost_at_x2,swing_pct_of_base"

// ---------- Models A/B/C/D on one grid ----------
type ModelRow =
    { Model: string
      Accounts: decimal
      Revenue: decimal
      Cost: decimal
      Fte: decimal
      Note: string }

/// Model A: conventional (efficient) cost with an AI productivity gain on staff [A] plus AI tooling.
let modelA (ps: Parameters) (s: Scenario) =
    let gain = 0.15m // [A] staff productivity from AI enhancements on an unchanged process
    let fte = max 8m (Math.Ceiling(conventionalFte ps Efficient s * (1m - gain)))
    let cost = fte * ps.ConvStaffCostPerEmployee.Value + s.Accounts * ps.ConvNonStaffOpexPerAccount.Value + 150000m
    { Model = "A traditional sponsor + AI"; Accounts = s.Accounts; Revenue = annualRevenue s; Cost = cost; Fte = fte
      Note = "conventional calibration (Vanguard FY2024) x (1 - 15% [A]) + $150k AI tooling [A]" }

let modelB (ps: Parameters) (s: Scenario) =
    let r = evaluate ps s
    { Model = "B AI-native sponsor"; Accounts = s.Accounts; Revenue = r.Revenue; Cost = r.AiNativeCost; Fte = r.AiNativeFte
      Note = "Economics.evaluate" }

/// Model C: provider serving existing sponsors. Price per account is a hypothesis [A],
/// deliberately well below the ~$745/account RCF->Ren related-party reference.
let modelC (ps: Parameters) (pricePerAccount: decimal) (s: Scenario) =
    let clients = max 1m (Math.Ceiling(s.Accounts / 20000m))
    let p = { SponsorClients = clients; AccountsServed = s.Accounts; PricePerAccount = pricePerAccount }
    let fte = totalFte ps { s with NewAccountShare = 0m }
    { Model = "C infrastructure to sponsors"; Accounts = s.Accounts; Revenue = providerRevenue p; Cost = providerCost ps p; Fte = fte
      Note = $"price ${pricePerAccount}/account/yr [A]; {clients} sponsor clients at 20k accounts each [A]" }

/// Model D: C's stack plus a partner sponsor-of-record; the operator keeps a share of the
/// sponsor admin fee [A] and bears acquisition cost for its own-distribution accounts.
let modelD (ps: Parameters) (feeShare: decimal) (s: Scenario) =
    let c = modelC ps 0m s
    let newAccts = s.Accounts * s.NewAccountShare
    let sponsorOfRecordFee = 50000m + s.Accounts * 5m // [A] partner sponsor governance, board, filings
    let pct = (feeShare * 100m).ToString("0")
    { Model = "D hybrid: infrastructure + partner sponsor-of-record"; Accounts = s.Accounts
      Revenue = annualRevenue s * feeShare
      Cost = c.Cost + newAccts * ps.CacPerNewAccount.Value + sponsorOfRecordFee
      Fte = c.Fte
      Note = "operator keeps " + pct + " pct of published-tier admin fees [A]; partner fee $50k + $5/account [A]" }

let modelGrid (ps: Parameters) =
    scales
    |> List.map baseScenario
    |> List.collect (fun s -> [ modelA ps s; modelB ps s; modelC ps 150m s; modelD ps 0.5m s ])

let modelTable (rows: ModelRow list) =
    rows
    |> List.map (fun m ->
        let margin = if m.Revenue = 0m then 0m else (m.Revenue - m.Cost) / m.Revenue * 100m
        String.Join(",", [ q m.Model; r0 m.Accounts; r0 m.Revenue; r0 m.Cost; r0 (m.Revenue - m.Cost); r2 margin; r0 m.Fte; q m.Note ]))
    |> csv "model,accounts,revenue_usd,cost_usd,operating_result_usd,margin_pct,fte,note"

let twinTable (ps: Parameters) (s: Scenario) (seed: uint64) =
    stresses
    |> List.collect (fun st ->
        let r = simulate ps s st seed
        r.Queues |> List.map (fun qs ->
            String.Join(",", [ q st.Name; $"%A{qs.Queue}"; r0 qs.Arrived; r0 qs.Served; r0 qs.MaxBacklog; string qs.DaysOverSla; r2 qs.MeanWaitDays; r2 r.MinLiquidityBufferDays; string r.LiquidityExhausted ])))
    |> csv "stress,queue,arrived,served,max_backlog,days_over_sla,mean_wait_days,min_liquidity_buffer_days,liquidity_exhausted"

let rampTable (label: string) (rows: RampYear list) =
    rows
    |> List.map (fun y -> String.Join(",", [ q label; string y.Year; r0 y.Accounts; r0 y.Revenue; r0 y.Cost; r0 (y.Revenue - y.Cost); r0 y.Cumulative ]))

let ramps (ps: Parameters) =
    let bPath = [ 1500m; 4000m; 8000m; 14000m; 22000m ]       // [A] new donor accounts per year
    let cPath = [ 1m; 1m; 2m; 2m; 3m ]                          // [A] sponsor clients signed per year
    let bCalibrated = [ 1000m; 2000m; 4000m; 6000m; 7000m ]      // 20k accounts x $100k = $2.0bn in year 5
    let rows =
        rampTable "B AI-native sponsor, optimistic: $300k avg, 49.5k accounts by yr5 (~$15bn) [A]" (rampB ps 300000m bPath)
        @ rampTable "B AI-native sponsor, calibrated: $100k avg, ~$2bn by yr5 (Daffy-reported scale) [A]" (rampB ps 100000m bCalibrated)
        @ rampTable "C provider at $300/account, 20k-account clients" (rampC ps 300m 20000m cPath)
        @ rampTable "C provider at $150/account, 20k-account clients" (rampC ps 150m 20000m cPath)
        @ rampTable "C provider at $300/account, 5k-account clients" (rampC ps 300m 5000m cPath)
    let peaks =
        [ "B optimistic", peakCapitalNeed (rampB ps 300000m bPath)
          "B calibrated", peakCapitalNeed (rampB ps 100000m bCalibrated)
          "C $300 20k", peakCapitalNeed (rampC ps 300m 20000m cPath)
          "C $150 20k", peakCapitalNeed (rampC ps 150m 20000m cPath)
          "C $300 5k", peakCapitalNeed (rampC ps 300m 5000m cPath) ]
    csv "path,year,accounts_end,revenue_usd,cost_usd,operating_result_usd,cumulative_usd" rows,
    csv "path,peak_capital_need_usd" (peaks |> List.map (fun (n, v) -> q n + "," + r0 v))
