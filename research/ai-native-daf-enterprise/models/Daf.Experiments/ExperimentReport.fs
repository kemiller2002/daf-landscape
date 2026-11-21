/// CSV renderers for experiment results (pure). Written by Daf.Enterprise.Cli to workflow-innovation/08-experiments/results.
module Daf.Experiments.ExperimentReport

open System
open Daf.Experiments.Experiments

let private f2 (x: float) = Math.Round(x, 2).ToString("0.##")
let private q (s: string) = "\"" + s.Replace("\"", "\"\"") + "\""
let private csv header rows = String.Join("\n", header :: rows) + "\n"

let e1 seed =
    E1.run E1.defaults seed
    |> List.map (fun r -> String.Join(",", [ q (sprintf "%A" r.Arch); f2 r.VerificationOps; f2 r.HumanMinutes; string r.IneligibleGrants; string r.Escaped; string r.SourceLatencyFloor; f2 r.MedianLatencySeconds ]))
    |> csv "architecture,verification_ops,human_minutes,ineligible_grants,escaped,source_latency_floor,median_latency_seconds"

let e2Rows (p: E2.Params) label seed =
    E2.archs |> List.map (fun a ->
        let r = E2.run p seed a
        let esc d = r.Escaped.TryFind d |> Option.defaultValue 0 |> string
        String.Join(",", [ q label; q (sprintf "%A" a); f2 (r.HumanMinutes / 60.0); string r.HumanCases; string r.DefectsTotal; string r.EscapedTotal
                           esc E2.Revoked; esc E2.SanctionsHit; esc E2.UndeclaredRelatedParty; esc E2.PledgeOrTicketBenefit; esc E2.AccountTakeover
                           (match r.MisconfigDetectedDay with Some d -> string d | None -> ""); q r.RoutineLatency ]))

let e2 seed =
    let baseRows = e2Rows E2.defaults "base" seed
    let misconfig = e2Rows { E2.defaults with MisconfigWindow = Some(100, 200) } "adversarial: revocation rule silently disabled days 100-199" seed
    let injection = e2Rows { E2.defaults with AiRecall = (function E2.PledgeOrTicketBenefit -> 0.2 | d -> E2.defaults.AiRecall d) } "adversarial: prompt injection lowers AI recall on benefit text to 0.2" seed
    let parity = e2Rows { E2.defaults with AiRecall = E2.defaults.HumanRoutineCatch } "sensitivity: AI recall set equal to human routine catch rates" seed
    let quickReview = e2Rows { E2.defaults with MinutesRoutineReview = 1.0 } "sensitivity: routine manual review takes 1 minute" seed
    csv "scenario,architecture,human_hours,human_cases,defects,escaped_total,escaped_revoked,escaped_sanctions,escaped_related_party,escaped_benefit,escaped_account_takeover,misconfig_detected_day,routine_latency" (baseRows @ misconfig @ injection @ parity @ quickReview)

let e3 seed =
    E3.run E3.defaults seed
    |> List.map (fun r -> String.Join(",", [ q (sprintf "%A" r.Design); string r.Payments; f2 r.PaymentCost; f2 (r.RecipientMinutes / 60.0); f2 r.ExpectedFraudulentChangesUncaught; f2 r.GrantsAffectedByReturns ]))
    |> csv "design,payments,payment_cost_usd,recipient_hours,expected_uncaught_fraudulent_payee_changes,grants_affected_by_returns"

let e4 seed =
    [ E4.defaults, E4.Continuous; E4.defaults, E4.MonthEnd
      { E4.defaults with MinutesPerAgeDay = 0.0 }, E4.Continuous; { E4.defaults with MinutesPerAgeDay = 0.0 }, E4.MonthEnd
      { E4.defaults with FeedOutage = Some(100, 110) }, E4.Continuous
      { E4.defaults with FeedOutage = Some(100, 110); MissingFeedAlarm = false }, E4.Continuous ]
    |> List.map (fun (p, m) ->
        let r = E4.run p seed m
        let label = if p.MinutesPerAgeDay = 0.0 then r.Label + "; sensitivity: no age penalty" else r.Label
        String.Join(",", [ q (sprintf "%A" r.Mode); q label; string r.Breaks; f2 r.MeanAgeAtDetection; string r.MaxAgeAtDetection; f2 (r.Minutes / 60.0) ]))
    |> csv "mode,scenario,breaks,mean_age_days,max_age_days,human_hours"

let e5 () =
    E5.designs |> List.map (E5.evaluate 0.002)
    |> List.map (fun r -> String.Join(",", [ q r.Name; f2 r.CompletionRate; f2 r.DonorMinutes; f2 r.FraudulentAccountsReachingGrantPer10k; f2 r.DataCompleteAtGrant ]))
    |> csv "design,completion_rate,donor_minutes,fraudulent_accounts_reaching_first_grant_per_10k,data_complete_at_grant"

let e6 seed =
    [ E6.SeparatePools; E6.SharedPool; E6.SeparateWithSmoothing; E6.SharedWithSmoothing ]
    |> List.map (fun d ->
        let r = E6.run E6.defaults seed d
        let minFte = E6.minFteForSla E6.defaults seed d |> Option.map string |> Option.defaultValue ">400"
        String.Join(",", [ q (sprintf "%A" d); f2 r.Fte; string r.DaysOverSla; f2 r.MaxBacklogDays; minFte ]))
    |> csv "design,fte_at_25pct_headroom,sponsor_days_over_sla,max_backlog_days,min_fte_meeting_sla_every_day"

let e9 () =
    [ for d in E9.designs do
        for c in E9.crashPoints do
            let (n, committed) = E9.executions d c
            yield String.Join(",", [ q (sprintf "%A" d); q (sprintf "%A" c); string n; string committed; q (sprintf "%A" (E9.classify d c)) ]) ]
    |> csv "design,crash_point,bank_executions,approval_committed,outcome"

let e10 seed =
    let p = E10.defaults
    let shifted = { p with ShiftedShare = 0.3 }
    let row label (r: E10.Result) = String.Join(",", [ q label; q r.Policy; (if Double.IsNaN r.Threshold then "" else f2 r.Threshold); f2 (r.Minutes / 60.0); string r.AutoClosed; string r.EscapedDefects; string r.Defects ])
    let thresholds = [ -1.0; -0.5; 0.0; 0.5; 1.0 ]
    [ yield row "base" (E10.flagOnly p seed)
      for t in thresholds do yield row "base" (E10.autoClose p seed t)
      yield row "distribution shift: 30% of defects are a new weak-signal pattern" (E10.flagOnly shifted seed)
      for t in thresholds do yield row "distribution shift: 30% of defects are a new weak-signal pattern" (E10.autoClose shifted seed t) ]
    |> csv "scenario,policy,threshold,human_hours,auto_closed,escaped_defects,defects"

let e8 () =
    Migration.compare 5 2
    |> List.map (fun r -> String.Join(",", [ q r.Method; string r.GrantsVisible; string r.ContributionsVisible; string r.FundBalance; string r.ScheduleDGrantsAllYears; f2 r.HistoryCompleteness ]))
    |> csv "method,grants_visible,contributions_visible,fund_balance,schedule_d_grants_paid_visible,history_completeness"

let network (summaryPath: string) =
    let (curve, sponsors) = NetworkEconomics.load summaryPath
    let p = NetworkEconomics.defaults
    let rows order = if order = "random_mean_200" then NetworkEconomics.joinCurveRandom p curve sponsors else NetworkEconomics.joinCurve p curve sponsors order
    let orders = [ "descending_assets"; "ascending_assets"; "random_mean_200" ]
    let body =
        orders |> List.collect (fun o ->
            rows o |> List.map (fun r -> String.Join(",", [ q r.Order; string r.K; f2 r.MemberSavings; f2 r.CumulativeOperatorRevenue; string r.OperatorBreakEven ])))
    let curveCsv = csv "join_order,k,member_annual_savings_usd,cumulative_operator_revenue_usd,operator_break_even" body
    let total o = rows o |> List.sumBy (fun r -> r.MemberSavings)
    let sens =
        [ for v in [ 67.5; 270.0; 1080.0 ] do
            for h in [ 0.08; 0.2 ] do
                let p' = { p with CostPerDetermination = v; HumanDeterminationShare = h }
                let r = NetworkEconomics.joinCurve p' curve sponsors "descending_assets"
                let tot = r |> List.sumBy (fun x -> x.MemberSavings)
                yield String.Join(",", [ f2 v; f2 h; f2 tot; f2 (tot * p.FeeShareOfSavings); (match NetworkEconomics.firstBreakEven r with Some k -> string k | None -> "never") ]) ]
    let summary =
        csv "cost_per_determination_usd,human_determination_share,total_member_savings_usd,operator_revenue_usd,break_even_k_descending" sens
    let models =
        [ NetworkEconomics.grantInfrastructure 10 80000.0 1.0; NetworkEconomics.grantInfrastructure 30 80000.0 1.0
          NetworkEconomics.grantInfrastructure 10 80000.0 3.0; NetworkEconomics.sharedCompliance 20 60000.0
          NetworkEconomics.sharedCompliance 60 60000.0; NetworkEconomics.sharedCompliance 150 30000.0 ]
        |> List.map (fun m -> String.Join(",", [ q m.Model; string m.Customers; f2 m.Revenue; f2 m.Cost; f2 (m.Revenue - m.Cost); q m.Note ]))
        |> csv "model,customers,revenue_usd,cost_usd,operating_result_usd,note"
    curveCsv, summary, models, (orders |> List.map (fun o -> o, total o))

// ---------------- charity-vetting-ai: public-data benchmarks ----------------
let vettingResolution (bmfDir: string) (samplePath: string) =
    let orgs = Vetting.loadBmf bmfDir
    let ix = Vetting.buildIndex orgs
    let qs = Vetting.loadQueries samplePath
    // label consistency: is the filed EIN a current BMF record, and does its name agree with the filed name?
    let inBmf = qs |> List.filter (fun q -> ix.ByEin.ContainsKey q.FiledEin)
    let nameAgrees =
        inBmf |> List.filter (fun q ->
            let o = ix.ByEin.[q.FiledEin]
            let a = Vetting.keyTokens q.Name |> Set.ofList
            let b = Vetting.keyTokens o.Name |> Set.ofList
            not (Set.isEmpty (Set.intersect a b)) || Vetting.exactKey q.Name = Vetting.exactKey o.Name)
    let evalQs = inBmf   // ground truth usable only where the filed EIN is a current BMF record
    let ambiguity (q: Vetting.Query) = ix.ByExact.TryFind(Vetting.exactKey q.Name) |> Option.map List.length |> Option.defaultValue 0
    let strata =
        [ "all", (fun (_: Vetting.Query) -> true)
          "name unique nationally (exact key appears once)", (fun q -> ambiguity q = 1)
          "name shared by 2-5 orgs", (fun q -> let a = ambiguity q in a >= 2 && a <= 5)
          "name shared by 6+ orgs", (fun q -> ambiguity q >= 6)
          "exact key absent from BMF (spelling/format differs)", (fun q -> ambiguity q = 0) ]
    let methods =
        [ "exact name, national", Vetting.ExactNameNational
          "exact name + state", Vetting.ExactNameState
          "exact name + state, city/zip tie-break", Vetting.ExactNameStateCityZip
          "fuzzy TF-IDF, accept >=0.85 & margin >=0.10", Vetting.FuzzyTfIdf(0.85, 0.10)
          "fuzzy TF-IDF, accept >=0.95 & margin >=0.20", Vetting.FuzzyTfIdf(0.95, 0.20)
          "cascade: deterministic, then fuzzy 0.95/0.20, else refer", Vetting.Cascade ]
    let rows =
        [ for (sname, sf) in strata do
            let sq = evalQs |> List.filter sf
            for (mname, m) in methods do
                let s = Vetting.score mname ix m sq
                yield String.Join(",", [ q sname; q s.Method; string s.Queries; string s.Resolved; string s.Correct; string s.Wrong
                                         string s.Referred; string s.NoMatch; f2 (s.Precision * 100.0); f2 (s.Coverage * 100.0); string s.TruthInReferredCandidates ]) ]
    let header = "stratum,method,queries,resolved,correct,wrong,referred,no_match,precision_pct,coverage_pct,truth_in_referred_top_candidates"
    let consistency =
        csv "metric,value"
            [ "sample_lines," + string qs.Length
              "filed_ein_is_current_bmf_record," + string inBmf.Length
              "filed_ein_not_in_current_bmf," + string (qs.Length - inBmf.Length)
              "filed_ein_in_bmf_but_name_shares_no_token," + string (inBmf.Length - nameAgrees.Length)
              "bmf_records_loaded," + string ix.N ]
    csv header rows, consistency, ix

let vettingScreening (ix: Vetting.BmfIndex) (ofacDir: string) (fullLinesPath: string) =
    let entries = Vetting.loadOfac ofacDir
    let si = Vetting.buildScreenIndex entries
    let names =
        System.IO.File.ReadLines fullLinesPath |> Seq.skip 1 |> Seq.map Vetting.loadQueriesLine |> Seq.map (fun q -> q.Name)
        |> Seq.filter (fun n -> n <> "") |> Seq.distinctBy Vetting.exactKey |> List.ofSeq
    let matched = Vetting.matchAll si names
    let rows =
        [ 0.88; 0.92; 0.95; 0.98; 1.0 ]
        |> List.map (fun t ->
            let r = Vetting.screenMatched matched t
            let byType = r.AlertsByEntryType |> List.map (fun (k, v) -> k + "=" + string v) |> String.concat "; "
            String.Join(",", [ f2 t; string r.NamesScreened; string r.Alerts; string r.AlertsEntityTypeOnly; string r.AlertsAfterTokenCoverageRule
                               f2 (100.0 * float r.Alerts / float r.NamesScreened); string r.AlertsPersonLikeRecipient; q byType ]))
    csv "jaro_winkler_threshold,distinct_recipient_names,alerts,alerts_on_entity_entries,alerts_after_token_coverage_rule,alert_rate_pct,alerts_where_recipient_name_is_person_like,alerts_by_list_entry_type" rows,
    entries.Length
