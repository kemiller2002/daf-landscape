/// All model outputs as (file name, content). Pure given inputs.
module ZeroBased.Outputs

open CompetitiveDisplacement.Inputs
open ZeroBased.Domain
open ZeroBased.Volume
open ZeroBased.Workload
open ZeroBased.Simulation
open ZeroBased.Infrastructure
open ZeroBased.Revenue
open ZeroBased.Analysis
open ZeroBased.Render

let mcDraws = 300
let aumList = [ 10e6; 25e6; 50e6; 100e6; 250e6; 500e6; 750e6; 1e9; 1.5e9; 2e9; 3e9; 5e9; 10e9; 25e9 ]
let balanceList = [ 5000.0; 10000.0; 25000.0; 50000.0; 100000.0; 250000.0; 500000.0; 1000000.0 ]
let accountList = [ 100.0; 250.0; 500.0; 1000.0; 2500.0; 5000.0; 10000.0; 25000.0; 50000.0; 100000.0; 250000.0; 500000.0; 1000000.0 ]
let bpsList = [ 5.0; 10.0; 15.0; 20.0; 25.0; 30.0; 40.0 ]

/// Sponsor count implied by assets: one sponsor per $500M, at least one, at most 20 (ASSUMPTION used in scale grids).
let sponsorsFor (assets: float) = max 1.0 (min 20.0 (round (assets / 500e6)))

let refConfig = "CFG-5"
let refProgramme = "PG-HNW"

// ------------------------------------------------------------------ baseline

let baselineRows (baseline: CompetitiveDisplacement.Inputs.Inputs) =
    [ "MD-5"; "MD-4"; "MD-6"; "MD-7"; "MD-1" ]
    |> List.map (fun m -> Baseline.reconstruct baseline m 20.0)

let baselineCsv (rs: Baseline.Reconstruction list) =
    csv [ "mode"; "break_even_assets"; "fully_loaded_assets"; "accounts"; "opex_at_break_even"; "fixed"; "sponsor_level"; "variable_per_acct"; "labour_per_acct"; "infra_per_acct"; "external_per_acct"; "ai_per_acct"; "prevention_per_acct"; "failure_per_acct"; "human_min_per_acct"; "build" ]
        (rs |> List.map (fun r ->
            [ r.ModeId; f4 r.BreakEvenAssets; f4 r.FullyLoadedAssets; f4 r.Accounts; f4 r.OpexAtBreakEven; f4 r.Fixed; f4 r.SponsorLevel; f4 r.VariablePerAcct
              f4 r.LabourPerAcct; f4 r.InfraPerAcct; f4 r.ExternalPerAcct; f4 r.AiPerAcct; f4 r.PreventionPerAcct; f4 r.FailurePerAcct; f4 r.HumanMinutesPerAcct; f4 r.Build ]))

// ------------------------------------------------------------------ scenario evaluation helpers

type Ctx = { Inputs: Inputs; Vals: Values; Iv: Values; Bv: Values }

let eval (simulate: bool) (c: Ctx) cfgId progId (accounts: float) (sponsors: float) (balance: float) =
    let p = programme c.Inputs progId
    evaluate simulate Base c.Vals c.Iv c.Inputs (config c.Inputs cfgId) C1 (scenario c.Vals p accounts sponsors balance)

let evalRow (label: string) (e: Eval) =
    [ label; e.Config.Id; e.Scenario.Programme.Id; f4 e.Scenario.Accounts; f4 e.Scenario.Sponsors; f4 e.Scenario.MeanBalance; f4 (assets e.Scenario)
      f4 e.Counts.Grants; f4 e.Counts.Contributions; f4 e.Totals.Events; f4 e.Totals.AutoShare; f4 e.Totals.HumanHours; f4 e.Totals.VendorHours; f4 e.Totals.SponsorHours
      f4 e.Staffing.DedicatedFte; f4 e.Staffing.FractionalHours; f4 (e.Staffing.Pools |> List.sumBy (fun p -> p.FounderHours)); string e.Staffing.NamedPersons; string e.Staffing.IndependentPersons
      f4 e.Views.LabourCash; f4 e.Views.BackupCash; f4 e.Views.InfraCash; f4 e.Views.CharityDataUpkeep; f4 e.Views.ExternalCash; f4 e.Views.FixedIncremental; f4 e.Views.FounderImputed; f4 e.Views.FixedAllocated; f4 e.Views.FixedStandalone
      f4 e.Views.View1; f4 e.Views.View2; f4 e.Views.View3; f4 e.Views.SponsorLabourValue
      f4 (e.Views.View1 / max 1.0 e.Scenario.Accounts); f4 (e.Views.View1 / max 1.0 (assets e.Scenario) * 10000.0); f4 (e.Views.View2 / max 1.0 (assets e.Scenario) * 10000.0); f4 (e.Views.View3 / max 1.0 (assets e.Scenario) * 10000.0) ]

let evalHeader =
    [ "label"; "config"; "programme"; "accounts"; "sponsors"; "mean_balance"; "assets"; "grants"; "contributions"; "events"; "auto_share"; "human_hours"; "vendor_hours"; "sponsor_hours"
      "dedicated_fte"; "fractional_hours"; "founder_hours"; "named_persons"; "independent_persons"
      "labour_cash"; "backup_cash"; "infra"; "charity_data_upkeep"; "external"; "fixed_incremental"; "founder_imputed"; "fixed_allocated"; "fixed_standalone"
      "view1_cash"; "view2_allocated"; "view3_standalone"; "sponsor_labour_value"; "view1_per_account"; "view1_bps"; "view2_bps"; "view3_bps" ]

// ------------------------------------------------------------------ break-even (cached cost curves)

type Curve = { Cfg: string; Prog: string; Balance: float; Sponsors: float -> float; Points: (float * Eval) list }

let curve (c: Ctx) cfgId progId (balance: float) (sponsors: float -> float) =
    { Cfg = cfgId; Prog = progId; Balance = balance; Sponsors = sponsors
      Points = breakEvenGrid |> List.map (fun a -> a, eval false c cfgId progId a (sponsors (a * balance)) balance) }

let curveBreakEven (cv: Curve) (view: int) (pricing: Pricing) (amortised: float) =
    let profit = cv.Points |> List.map (fun (a, e) -> a, netRevenue pricing e - viewCost view e - amortised)
    let rec go xs cand =
        match xs with
        | [] -> cand
        | (a, p) :: rest -> if p >= 0.0 then go rest (Option.orElse (Some a) cand) else go rest None
    go profit None |> Option.map (fun a -> a, a * cv.Balance)

let amortisedInvestment (c: Ctx) (view: int) =
    let years = v c.Vals "amortisation_years"
    let lines = Costs.oneTime Base c.Inputs.Fixed
    let cash = lines |> List.filter (fun (_, _, vw, _) -> vw = "incremental") |> List.sumBy (fun (_, _, _, a) -> a)
    let econ = lines |> List.filter (fun (id, _, vw, _) -> vw = "allocated" || (vw = "incremental" && id <> "FC-301")) |> List.sumBy (fun (_, _, _, a) -> a)
    match view with
    | 1 -> cash / years
    | _ -> econ / years

// ------------------------------------------------------------------ outputs

let all (inputs: Inputs) (baseline: CompetitiveDisplacement.Inputs.Inputs) : (string * string) list =
    let c = { Inputs = inputs; Vals = baseVals inputs; Iv = infraVals inputs; Bv = benVals inputs }
    let vals = c.Vals
    let bRows = baselineRows baseline
    let md5 = bRows |> List.head

    // 1. headline scenarios at $100M/$250M/$500M/$1B, every configuration, simulated
    let headlineAum = [ 100e6; 250e6; 500e6; 1e9 ]
    let pHnw = programme inputs refProgramme
    let headline =
        [ for a in headlineAum do
            for cfg in inputs.Configs do
                yield eval true c cfg.Id refProgramme (a / pHnw.DefaultBalance) (sponsorsFor a) pHnw.DefaultBalance ]
    let headlineCsv = csv evalHeader (headline |> List.map (fun e -> evalRow $"AUA {money (assets e.Scenario)}" e))
    let headlineStaffCsv =
        csv [ "assets"; "config"; "pool"; "hours"; "founder_hours"; "simulated_fte"; "mode"; "dedicated_fte"; "fractional_hours"; "named_persons"; "cost"; "peak_queue_hours"; "breached_hours" ]
            (headline |> List.collect (fun e ->
                e.Staffing.Pools |> List.map (fun p ->
                    [ f4 (assets e.Scenario); e.Config.Id; p.Pool; f4 p.Hours; f4 p.FounderHours; f4 p.SimulatedFte; p.Mode; f4 p.DedicatedFte; f4 p.FractionalHours; string p.NamedPersons; f4 p.Cost; f4 p.Sim.PeakQueueHours; f4 p.Sim.BreachedHours ])))

    // 2. simulation detail at the reference scenario ($500M; CFG-5)
    let refEval = eval true c refConfig refProgramme (500e6 / pHnw.DefaultBalance) 1.0 pHnw.DefaultBalance
    let simCsv =
        csv [ "pool"; "staff_fte"; "mode"; "dedicated_fte"; "fractional_hours"; "founder_hours"; "arrived_hours"; "incident_hours"; "peak_queue_hours"; "peak_queue_age_days"; "breached_hours"; "utilisation"; "peak_week_hours"; "named_persons"; "cost" ]
            (refEval.Staffing.Pools |> List.map (fun p ->
                [ p.Pool; f4 p.SimulatedFte; p.Mode; f4 p.DedicatedFte; f4 p.FractionalHours; f4 p.FounderHours; f4 p.Sim.ArrivedHours; f4 p.Sim.IncidentHours; f4 p.Sim.PeakQueueHours
                  f4 p.Sim.PeakQueueAgeDays; f4 p.Sim.BreachedHours; f4 p.Sim.Utilisation; f4 p.Sim.PeakWeekHours; string p.NamedPersons; f4 p.Cost ]))
    let refUnit = unitCosts refEval

    // calibration of analytic peak factor: simulated FTE / average-load FTE per pool across headline CFG-5 runs
    let calibration =
        headline |> List.filter (fun e -> e.Config.Id = refConfig)
        |> List.collect (fun e ->
            e.Staffing.Pools |> List.filter (fun p -> p.Hours - p.FounderHours > 0.0)
            |> List.map (fun p -> e.Scenario.Accounts, p.Pool, (p.Hours - p.FounderHours) / productiveHoursPerFte vals, p.SimulatedFte))
    let calibCsv =
        csv [ "accounts"; "pool"; "average_load_fte"; "simulated_fte"; "ratio" ]
            (calibration |> List.map (fun (a, p, avg, sim) -> [ f4 a; p; f4 avg; f4 sim; f4 (if avg > 0.0 then sim / avg else nan) ]))

    // 3. scale grid: assets x balance (CFG-5 and CFG-2, analytic)
    let grid =
        [ for cfg in [ "CFG-2"; "CFG-5" ] do
            for a in aumList do
                for b in balanceList do
                    let accts = a / b
                    if accts >= 20.0 && accts <= 5e6 then yield eval false c cfg refProgramme accts (sponsorsFor a) b ]
    let gridCsv = csv evalHeader (grid |> List.map (evalRow "aua-x-balance"))

    // 4. account-count grid (CFG-5 and CFG-2, 1 and 5 sponsors, default balance)
    let acctGrid =
        [ for cfg in [ "CFG-2"; "CFG-5" ] do
            for s in [ 1.0; 5.0 ] do
                for a in accountList do
                    yield eval false c cfg refProgramme a s pHnw.DefaultBalance ]
    let acctCsv = csv evalHeader (acctGrid |> List.map (evalRow "accounts"))

    // 5. staffing step functions (simulated) by programme
    let stepGrid = [ 100.0; 250.0; 500.0; 1000.0; 2000.0; 3500.0; 5000.0; 7500.0; 10000.0; 15000.0; 25000.0; 40000.0; 60000.0; 100000.0; 175000.0; 250000.0; 500000.0; 1000000.0 ]
    let steps =
        [ for prog in [ "PG-HNW"; "PG-RETAIL"; "PG-INST" ] do
            let p = programme inputs prog
            yield prog, stepFunction true inputs (config inputs refConfig) C1 p (fun a -> sponsorsFor (a * p.DefaultBalance)) stepGrid ]
    let stepsCsv =
        csv [ "programme"; "accounts"; "pool"; "mode"; "dedicated_fte"; "fractional_hours"; "hours"; "simulated_fte" ]
            (steps |> List.collect (fun (prog, rs) -> rs |> List.map (fun r -> [ prog; f4 r.Accounts; r.Pool; r.Mode; f4 r.DedicatedFte; f4 r.FractionalHours; f4 r.Hours; f4 r.SimFte ])))
    let thresholdCsv =
        csv [ "programme"; "pool"; "dedicated_fte_reached"; "first_accounts" ]
            (steps |> List.collect (fun (prog, rs) -> thresholds rs |> List.map (fun (pool, fte, a) -> [ prog; pool; f4 fte; f4 a ])))

    // 6. break-even: config x view x bps x balance (cached curves)
    let beCurves =
        [ for cfg in inputs.Configs do
            for b in balanceList do
                yield curve c cfg.Id refProgramme b sponsorsFor ]
    let beRows =
        [ for cv in beCurves do
            for view in [ 1; 2; 3 ] do
                for bps in bpsList do
                    let op = curveBreakEven cv view (AumBps bps) 0.0
                    let loaded = curveBreakEven cv view (AumBps bps) (amortisedInvestment c view)
                    yield cv.Cfg, cv.Balance, view, bps, op, loaded ]
    let beCsv =
        csv [ "config"; "mean_balance"; "view"; "bps"; "break_even_accounts"; "break_even_assets"; "with_investment_accounts"; "with_investment_assets" ]
            (beRows |> List.map (fun (cfg, b, view, bps, op, ld) ->
                let a o = o |> Option.map fst |> Option.defaultValue infinity
                let s o = o |> Option.map snd |> Option.defaultValue infinity
                [ cfg; f4 b; string view; f4 bps; f4 (a op); f4 (s op); f4 (a ld); f4 (s ld) ]))
    let beLookup cfg b view bps = beRows |> List.tryFind (fun (c', b', v', p', _, _) -> c' = cfg && b' = b && v' = view && p' = bps)

    // 7. programmes and sponsor mixes at $1B (CFG-5)
    let progRows =
        inputs.Programmes |> List.map (fun p -> eval false c refConfig p.Id (1e9 / p.DefaultBalance) (sponsorsFor 1e9) p.DefaultBalance)
    let mixRows =
        [ "One sponsor", 1.0; "Multiple small sponsors (20)", 20.0; "Multiple large sponsors (4)", 4.0; "Many small sponsors (50)", 50.0 ]
        |> List.map (fun (label, s) -> label, eval false c refConfig refProgramme (1e9 / pHnw.DefaultBalance) s pHnw.DefaultBalance)
    let activityRows =
        [ "Low-activity accounts (x0.6)", 0.6; "Base activity", 1.0; "High-activity accounts (x2.06)", 2.06 ]
        |> List.map (fun (label, m) ->
            let vs = Map.add "activity_mult" m vals
            label, evaluate false Base vs c.Iv inputs (config inputs refConfig) C1 (scenario vs pHnw (1e9 / pHnw.DefaultBalance) 2.0 pHnw.DefaultBalance))
    let progCsv =
        csv evalHeader
            ((progRows |> List.map (evalRow "programme $1B")) @ (mixRows |> List.map (fun (l, e) -> evalRow l e)) @ (activityRows |> List.map (fun (l, e) -> evalRow l e)))

    // 8. infrastructure by deployment and scale
    let infraRows =
        [ for dep in [ C1; C2; C3 ] do
            for a in [ 1000.0; 10000.0; 100000.0; 1000000.0 ] do
                let e = eval false c refConfig refProgramme a (max 1.0 (round (a / 20000.0))) pHnw.DefaultBalance
                let aiEx = e.Loads |> List.filter (fun l -> l.Activity.Classification = "AI-ASSISTED") |> List.sumBy (fun l -> l.HumanEvents)
                let iso = if a / max 1.0 (round (a / 20000.0)) >= v vals "isolated_db_accounts_threshold" then max 1.0 (round (a / 20000.0)) else 1.0
                yield cost c.Iv dep e.Counts e.Totals.Events aiEx iso ]
    let infraCsv =
        csv [ "deployment"; "accounts"; "floor"; "compute_scale"; "storage"; "logging"; "messaging"; "ai"; "identity"; "scanning"; "egress"; "nonprod"; "isolation"; "total"; "per_account"; "stored_gb"; "peak_vcpu" ]
            (infraRows |> List.mapi (fun i r ->
                let a = [ 1000.0; 10000.0; 100000.0; 1000000.0 ].[i % 4]
                [ string r.Deployment; f4 a; f4 r.FloorAnnual; f4 r.ComputeScaleAnnual; f4 r.StorageAnnual; f4 r.LoggingAnnual; f4 r.MessagingAnnual; f4 r.AiAnnual
                  f4 r.IdentityAnnual; f4 r.ScanningAnnual; f4 r.EgressAnnual; f4 r.NonProdAnnual; f4 r.IsolationAnnual; f4 r.Total; f4 (r.Total / a); f4 r.StoredGb; f4 r.PeakVcpu ]))

    // 9. Beneficium
    let recipients = [ 0.0; 1000.0; 10000.0; 50000.0; 100000.0; 500000.0 ]
    let benRows = [ for s in Beneficium.allScenarios do for n in recipients do yield Beneficium.cost c.Bv s n ]
    let benCsv =
        csv [ "scenario"; "active_recipients"; "storage_gb"; "infra"; "connector_hours"; "ops_hours"; "exception_hours"; "verification_hours"; "enrolment_hours"; "external_fees"; "counsel"; "labour"; "total"; "fte_equivalent" ]
            (benRows |> List.map (fun r ->
                let fte = (r.ConnectorHours + r.OpsHours + r.ExceptionHours + r.VerificationHours + r.EnrolmentHours) / productiveHoursPerFte vals
                [ Beneficium.name r.Scenario; f4 r.ActiveRecipients; f4 r.StorageGb; f4 r.Infra; f4 r.ConnectorHours; f4 r.OpsHours; f4 r.ExceptionHours; f4 r.VerificationHours
                  f4 r.EnrolmentHours; f4 r.ExternalFees; f4 r.Counsel; f4 r.Labour; f4 r.Total; f4 fte ]))
    let overlap =
        [ 1.0; 3.0; 10.0; 30.0 ] |> List.map (fun s -> s, Beneficium.union c.Bv 20000.0 s, Beneficium.cost c.Bv Beneficium.HumanExceptionVerification (Beneficium.union c.Bv 20000.0 s))
    let overlapCsv =
        csv [ "sponsors"; "recipients_per_sponsor"; "union_recipients"; "total"; "per_sponsor" ]
            (overlap |> List.map (fun (s, u, r) -> [ f4 s; "20000"; f4 u; f4 r.Total; f4 (r.Total / s) ]))
    let bmfC3 = v c.Bv "database_population"
    let vetRows =
        [ for pop, label in [ 1000.0, "active"; 10000.0, "active"; 50000.0, "active"; 100000.0, "active"; bmfC3, "whole database" ] do
            for a in Beneficium.vettingAll do
                let grants = if label = "active" then pop * v c.Bv "grants_per_recipient" else 100000.0 * v c.Bv "grants_per_recipient"
                yield label, Beneficium.vetting c.Bv a pop grants ]
    let vetCsv =
        csv [ "population_basis"; "approach"; "population"; "human_reviews"; "human_hours"; "labour_cost"; "expected_false_negatives"; "false_negative_cost"; "false_positive_holds"; "false_positive_cost"; "total"; "meets_180_day_validity" ]
            (vetRows |> List.map (fun (l, r) ->
                [ l; Beneficium.vettingName r.Approach; f4 r.Population; f4 r.HumanReviews; f4 r.HumanHours; f4 r.LabourCost; f4 r.ExpectedFalseNegatives; f4 r.FalseNegativeCost
                  f4 r.FalsePositiveHolds; f4 r.FalsePositiveCost; f4 r.Total; (if r.Meets180DayValidity then "Y" else "N") ]))

    // 10. revenue models at reference scenarios
    let pricings =
        [ AumBps 20.0; AumBps 10.0; PerAccount 81.0; PerAccount 150.0; PerSponsor 150000.0; Transaction(5.0, 2.0)
          MinimumCommitment(20.0, 150000.0); HybridLicence(75000.0, 10.0); TieredBps [ 250e6, 25.0; 1e9, 15.0; 1e12, 8.0 ]; ExceptionFees(15.0, 25.0) ]
    let revScenarios = [ "$100M / 1 sponsor", 100e6, 1.0; "$250M / 1 sponsor", 250e6, 1.0; "$500M / 2 sponsors", 500e6, 2.0; "$1B / 4 sponsors", 1e9, 4.0 ]
    let revRows =
        [ for label, a, s in revScenarios do
            let e = eval false c refConfig refProgramme (a / pHnw.DefaultBalance) s pHnw.DefaultBalance
            for p in pricings do
                let r = netRevenue p e
                yield label, pricingName p, r, e ]
    let revCsv =
        csv [ "scenario"; "pricing"; "revenue"; "view1_cost"; "view2_cost"; "view3_cost"; "margin_view1"; "margin_view2"; "revenue_per_account"; "revenue_per_sponsor"; "contribution_margin_per_account_view1" ]
            (revRows |> List.map (fun (l, p, r, e) ->
                [ l; p; f4 r; f4 e.Views.View1; f4 e.Views.View2; f4 e.Views.View3; f4 (r - e.Views.View1); f4 (r - e.Views.View2)
                  f4 (r / e.Scenario.Accounts); f4 (r / e.Scenario.Sponsors); f4 ((r - e.Views.View1) / e.Scenario.Accounts) ]))

    // 10a. sponsor unit economics: marginal cost, acquisition and onboarding recovery, minimum viable contract
    let sponsorEcon =
        [ for sizeAum in [ 25e6; 50e6; 100e6; 250e6; 500e6; 1e9 ] do
            let baseE = eval false c refConfig refProgramme (500e6 / pHnw.DefaultBalance) 2.0 pHnw.DefaultBalance
            let plus = eval false c refConfig refProgramme ((500e6 + sizeAum) / pHnw.DefaultBalance) 3.0 pHnw.DefaultBalance
            let marginal = plus.Views.View1 - baseE.Views.View1
            let rev = sizeAum * 20.0 / 10000.0
            let onboardHours = plus.Loads |> List.filter (fun l -> l.Activity.Driver = PerSponsorOnboarding) |> List.sumBy (fun l -> (l.Minutes + l.AuthMinutes) * l.VendorShare / 60.0)
            let onboardCost = onboardHours * 120.0
            let acquire = v vals "cac_cash_per_sponsor"
            let monthly = (rev - marginal) / 12.0
            let payback = if monthly > 0.0 then (onboardCost + acquire) / monthly else infinity
            yield sizeAum, rev, marginal, onboardHours, onboardCost, acquire, payback ]
    let sponsorCsv =
        csv [ "sponsor_assets"; "revenue_20bps"; "marginal_view1_cost"; "onboarding_hours"; "onboarding_cost"; "acquisition_cash"; "payback_months" ]
            (sponsorEcon |> List.map (fun (a, r, m, h, oc, ac, pb) -> [ f4 a; f4 r; f4 m; f4 h; f4 oc; f4 ac; f4 pb ]))

    // 11. sensitivity: tornado on View 1 at $500M, named scenarios, Monte Carlo
    let tor = tornado inputs (config inputs refConfig) C1 pHnw (500e6 / pHnw.DefaultBalance) 1.0 pHnw.DefaultBalance 1
    let torCsv = csv [ "param"; "low"; "high"; "view1_at_low"; "view1_at_high"; "swing" ] (tor |> List.map (fun t -> [ t.Param; f4 t.Low; f4 t.High; f4 t.AtLow; f4 t.AtHigh; f4 t.Swing ]))
    let named =
        [ "optimistic", Low, Low; "expected", Base, Base; "conservative", Base, High; "severe", High, High ]
        |> List.map (fun (label, actLevel, parLevel) ->
            let vs = CompetitiveDisplacement.Sampling.atLevel parLevel inputs.Params
            let vs = if label = "optimistic" then Map.add "founder_hours_per_year" 800.0 (Map.add "productive_hours_per_day" 7.0 vs) else vs
            let vs = if parLevel = High then Map.add "founder_hours_per_year" 0.0 (Map.add "productive_hours_per_day" 6.0 vs) else vs
            let vs = Map.add "mc_mean_balance" 250000.0 vs
            let iv = CompetitiveDisplacement.Sampling.atLevel parLevel inputs.Infra
            let e = evaluate false actLevel vs iv inputs (config inputs refConfig) C1 (scenario vs pHnw (500e6 / pHnw.DefaultBalance) 1.0 pHnw.DefaultBalance)
            label, e)
    let namedCsv = csv evalHeader (named |> List.map (fun (l, e) -> evalRow l e))
    let mcRows =
        [ for a in [ 100e6; 500e6; 1e9 ] do
            for s in mcCost mcDraws 0.0 inputs (config inputs refConfig) C1 pHnw (a / pHnw.DefaultBalance) (sponsorsFor a) pHnw.DefaultBalance do
                yield a, 0.0, s
            for s in mcCost mcDraws 0.5 inputs (config inputs refConfig) C1 pHnw (a / pHnw.DefaultBalance) (sponsorsFor a) pHnw.DefaultBalance do
                yield a, 0.5, s ]
    let mcCsv = csv [ "assets"; "rho"; "metric"; "p10"; "p50"; "p90"; "mean" ] (mcRows |> List.map (fun (a, r, s) -> [ f4 a; f4 r; s.Label; f4 s.P10; f4 s.P50; f4 s.P90; f4 s.Mean ]))
    let mcBe =
        [ for cfg, view, rho in [ "CFG-2", 1, 0.0; "CFG-5", 1, 0.0; "CFG-5", 2, 0.0; "CFG-5", 3, 0.0; "CFG-5", 1, 0.5; "CFG-5", 2, 0.5 ] do
            let xs = mcBreakEven 200 rho inputs (config inputs cfg) C1 pHnw 1.0 view 20.0
            yield cfg, view, rho, summarise "break-even assets" xs, (xs |> List.filter System.Double.IsInfinity |> List.length |> float) / 200.0 ]
    let mcBeCsv = csv [ "config"; "view"; "rho"; "p10"; "p50"; "p90"; "never_share" ] (mcBe |> List.map (fun (cfg, view, rho, s, nv) -> [ cfg; string view; f4 rho; f4 s.P10; f4 s.P50; f4 s.P90; f4 nv ]))

    // 11a. stress: asset decline, loss of the largest sponsor, withdrawals
    let stressBase = eval false c refConfig refProgramme (1e9 / pHnw.DefaultBalance) 4.0 pHnw.DefaultBalance
    let stressCases =
        [ "Base $1B (4 sponsors)", stressBase, 1.0
          "Market decline 30% (accounts unchanged)", eval false c refConfig refProgramme (1e9 / pHnw.DefaultBalance) 4.0 (pHnw.DefaultBalance * 0.7), 1.0
          "Loss of largest sponsor (40% of assets)", eval false c refConfig refProgramme (0.6e9 / pHnw.DefaultBalance) 3.0 pHnw.DefaultBalance, 1.0
          "Net withdrawals 15% of assets", eval false c refConfig refProgramme (1e9 / pHnw.DefaultBalance) 4.0 (pHnw.DefaultBalance * 0.85), 1.0
          "Inactive accounts double (activity x0.6)",
          (let vs = Map.add "activity_mult" 0.6 vals in evaluate false Base vs c.Iv inputs (config inputs refConfig) C1 (scenario vs pHnw (1e9 / pHnw.DefaultBalance) 4.0 pHnw.DefaultBalance)), 1.0 ]
    let stressCsv =
        csv [ "case"; "assets"; "revenue_20bps"; "view1"; "view2"; "margin_view1"; "margin_view2" ]
            (stressCases |> List.map (fun (l, e, _) ->
                let r = netRevenue (AumBps 20.0) e
                [ l; f4 (assets e.Scenario); f4 r; f4 e.Views.View1; f4 e.Views.View2; f4 (r - e.Views.View1); f4 (r - e.Views.View2) ]))

    // 12. comparison with the preserved baseline modes at equal accounts and sponsors
    let compScales = [ 2000.0, 1.0; 4000.0, 2.0; 7695.0, 5.0; 20000.0, 5.0; 40000.0, 5.0 ]
    let compRows =
        [ for accts, s in compScales do
            for mode, cfg in [ "MD-1", "CFG-5"; "MD-2", "CFG-5"; "MD-4", "CFG-5"; "MD-5", "CFG-5"; "MD-6", "CFG-1"; "MD-7", "CFG-4" ] do
                let e = eval false c cfg refProgramme accts s pHnw.DefaultBalance
                yield accts, s, mode, cfg, Baseline.opexAt baseline mode accts s, e ]
    let compCsv =
        csv [ "accounts"; "sponsors"; "baseline_mode"; "zero_based_config"; "baseline_vendor_opex"; "zero_based_view1"; "zero_based_view2"; "zero_based_view3"; "zero_based_vendor_hours"; "zero_based_sponsor_hours" ]
            (compRows |> List.map (fun (a, s, m, cfg, b, e) -> [ f4 a; f4 s; m; cfg; f4 b; f4 e.Views.View1; f4 e.Views.View2; f4 e.Views.View3; f4 e.Totals.VendorHours; f4 e.Totals.SponsorHours ]))

    // 13. requirement economic impact (hours at reference scenario)
    let reqRows = hoursByRequirement refEval.Loads
    let reqCsv = csv [ "unbound_requirement"; "vendor_hours"; "sponsor_hours"; "activities" ] (reqRows |> List.map (fun (r, a, b, ids) -> [ r; f4 a; f4 b; ids ]))

    // 14. activity loads at reference
    let actCsv =
        csv [ "activity_id"; "activity"; "bucket"; "classification"; "role"; "events"; "human_events"; "authorized_events"; "minutes"; "auth_minutes"; "vendor_share"; "external_cost" ]
            (refEval.Loads |> List.map (fun l ->
                [ l.Activity.Id; l.Activity.Name; sprintf "%A" l.Bucket; l.Activity.Classification; l.Activity.Role; f4 l.Events; f4 l.HumanEvents; f4 l.AuthorizedEvents
                  f4 l.Minutes; f4 l.AuthMinutes; f4 l.VendorShare; f4 l.ExternalCost ]))

    // ------------------------------------------------------------------ markdown summary
    let beCell cfg b view bps =
        match beLookup cfg b view bps with
        | Some(_, _, _, _, op, _) -> op |> Option.map (snd >> usd) |> Option.defaultValue "> $5B or never"
        | None -> "n/a"
    let md =
        [ "# Zero-based operational economics: model results"
          ""
          "Generated by `model/src/ZeroBased` from `data/model-inputs/` and `data/registers/operational-activities.csv`. Every figure is conditional on labelled inputs; nothing is measured production performance. The simulation is a theoretical capacity model. Re-running produces byte-identical output."
          ""
          "## 1. Original model reproduced (competitive-displacement, preserved baseline)"
          ""
          table [ "Mode"; "Break-even (20 bps)"; "Fully loaded"; "Accounts"; "Opex at break-even"; "Fixed"; "Sponsor-level"; "Variable/acct"; "Labour/acct"; "Infra/acct"; "Human min/acct" ]
              (bRows |> List.map (fun r -> [ r.ModeId; usd r.BreakEvenAssets; usd r.FullyLoadedAssets; n0 r.Accounts; usd r.OpexAtBreakEven; usd r.Fixed; usd r.SponsorLevel; usd r.VariablePerAcct; usd r.LabourPerAcct; usd r.InfraPerAcct; n1 r.HumanMinutesPerAcct ]))
          ""
          $"MD-5 opex at break-even = fixed {usd md5.Fixed} + sponsor-level {usd md5.SponsorLevel} + {n0 md5.Accounts} accounts x {usd md5.VariablePerAcct} = {usd md5.OpexAtBreakEven}."
          ""
          "## 2. Annual cost at headline scale (PG-HNW, $250k mean balance, simulated staffing, deployment C1)"
          ""
          table [ "AUA"; "Config"; "Accounts"; "Sponsors"; "Vendor hours"; "Dedicated FTE"; "Fractional h"; "Founder h"; "View 1 cash"; "View 2 allocated"; "View 3 standalone"; "View 1 bps" ]
              (headline |> List.map (fun e ->
                  [ usd (assets e.Scenario); e.Config.Id; n0 e.Scenario.Accounts; n0 e.Scenario.Sponsors; n0 e.Totals.VendorHours; n1 e.Staffing.DedicatedFte; n0 e.Staffing.FractionalHours
                    n0 (e.Staffing.Pools |> List.sumBy (fun p -> p.FounderHours)); usd e.Views.View1; usd e.Views.View2; usd e.Views.View3; n1 (e.Views.View1 / assets e.Scenario * 10000.0) ]))
          ""
          "## 3. Break-even assets at 20 bps (sustained; operating, no investment recovery)"
          ""
          table ([ "Config"; "View" ] @ (balanceList |> List.map (fun b -> "$" + money b)))
              [ for cfg in inputs.Configs do
                  for view in [ 1; 2; 3 ] do
                      yield [ cfg.Id; string view ] @ (balanceList |> List.map (fun b -> beCell cfg.Id b view 20.0)) ]
          ""
          "## 4. Reference simulation ($500M, 1 sponsor, CFG-5)"
          ""
          table [ "Pool"; "Hours"; "Founder h"; "Simulated FTE"; "Mode"; "Dedicated"; "Fractional h"; "Peak queue h"; "Peak age (d)"; "Breached h"; "Utilisation"; "Named persons"; "Cost" ]
              (refEval.Staffing.Pools |> List.map (fun p ->
                  [ p.Pool; n0 p.Hours; n0 p.FounderHours; n2 p.SimulatedFte; p.Mode; n1 p.DedicatedFte; n0 p.FractionalHours; n1 p.Sim.PeakQueueHours; n1 p.Sim.PeakQueueAgeDays; n1 p.Sim.BreachedHours; pct p.Sim.Utilisation; string p.NamedPersons; usd p.Cost ]))
          ""
          $"Events {n0 refEval.Totals.Events}; automatically completed {pct refEval.Totals.AutoShare}; human-handled {n0 refEval.Totals.HumanEvents}; independently authorized {n0 refEval.Totals.AuthorizedEvents}; human hours {n0 refEval.Totals.HumanHours} (vendor {n0 refEval.Totals.VendorHours}, sponsor {n0 refEval.Totals.SponsorHours})."
          $"Unit costs (View 1): per account {usd refUnit.PerAccount}; per grant {usd refUnit.PerGrant}; per contribution {usd refUnit.PerContribution}; per sponsor {usd refUnit.PerSponsor}; per human exception {usd refUnit.PerException}."
          ""
          "## 5. Staffing thresholds (first account count at which a pool needs each dedicated FTE; CFG-5, simulated)"
          ""
          table [ "Programme"; "Pool"; "Dedicated FTE"; "First accounts" ]
              (steps |> List.collect (fun (prog, rs) -> thresholds rs |> List.map (fun (pool, fte, a) -> [ prog; pool; n1 fte; n0 a ])))
          ""
          "## 6. Beneficium (annual cost)"
          ""
          table [ "Scenario"; "0 recipients"; "10k"; "100k"; "500k" ]
              (Beneficium.allScenarios |> List.map (fun s ->
                  [ Beneficium.name s ] @ ([ 0.0; 10000.0; 100000.0; 500000.0 ] |> List.map (fun n -> usd (Beneficium.cost c.Bv s n).Total))))
          ""
          "## 7. Monte Carlo break-even at 20 bps (1 sponsor; balance drawn $100k-$500k)"
          ""
          table [ "Config"; "View"; "rho"; "P10"; "P50"; "P90"; "Never" ]
              (mcBe |> List.map (fun (cfg, view, rho, s, nv) -> [ cfg; string view; n1 rho; usd s.P10; usd s.P50; usd s.P90; pct nv ]))
          "" ]
        |> String.concat "\n"
    [ "results.md", md + "\n"
      "baseline-reconstruction.csv", baselineCsv bRows
      "headline-scenarios.csv", headlineCsv
      "headline-staffing.csv", headlineStaffCsv
      "simulation-reference.csv", simCsv
      "simulation-calibration.csv", calibCsv
      "scale-grid-aua-balance.csv", gridCsv
      "scale-grid-accounts.csv", acctCsv
      "staffing-steps.csv", stepsCsv
      "staffing-thresholds.csv", thresholdCsv
      "break-even.csv", beCsv
      "programmes-and-mixes.csv", progCsv
      "infrastructure.csv", infraCsv
      "beneficium-scenarios.csv", benCsv
      "beneficium-overlap.csv", overlapCsv
      "vetting-alternatives.csv", vetCsv
      "revenue-models.csv", revCsv
      "sponsor-unit-economics.csv", sponsorCsv
      "sensitivity-tornado.csv", torCsv
      "named-scenarios.csv", namedCsv
      "monte-carlo-cost.csv", mcCsv
      "monte-carlo-break-even.csv", mcBeCsv
      "stress.csv", stressCsv
      "baseline-comparison.csv", compCsv
      "requirement-hours.csv", reqCsv
      "activity-loads-reference.csv", actCsv ]
