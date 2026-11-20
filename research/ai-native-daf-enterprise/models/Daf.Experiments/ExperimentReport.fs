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
    csv "scenario,architecture,human_hours,human_cases,defects,escaped_total,escaped_revoked,escaped_sanctions,escaped_related_party,escaped_benefit,escaped_account_takeover,misconfig_detected_day,routine_latency" (baseRows @ misconfig @ injection)

let e3 seed =
    E3.run E3.defaults seed
    |> List.map (fun r -> String.Join(",", [ q (sprintf "%A" r.Design); string r.Payments; f2 r.PaymentCost; f2 (r.RecipientMinutes / 60.0); f2 r.ExpectedFraudulentChangesUncaught; f2 r.GrantsAffectedByReturns ]))
    |> csv "design,payments,payment_cost_usd,recipient_hours,expected_uncaught_fraudulent_payee_changes,grants_affected_by_returns"

let e4 seed =
    [ E4.defaults, E4.Continuous; E4.defaults, E4.MonthEnd
      { E4.defaults with FeedOutage = Some(100, 110) }, E4.Continuous
      { E4.defaults with FeedOutage = Some(100, 110); MissingFeedAlarm = false }, E4.Continuous ]
    |> List.map (fun (p, m) ->
        let r = E4.run p seed m
        String.Join(",", [ q (sprintf "%A" r.Mode); q r.Label; string r.Breaks; f2 r.MeanAgeAtDetection; string r.MaxAgeAtDetection; f2 (r.Minutes / 60.0) ]))
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
