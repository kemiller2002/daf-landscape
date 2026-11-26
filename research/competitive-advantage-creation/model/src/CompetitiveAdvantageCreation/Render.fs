/// Renders model results as CSV files, Markdown tables (data/model-outputs/tables/*.md, quoted verbatim by reports
/// 14-19) and generated register fragment rows for agent MOD. Pure: returns (relative path, content) pairs.
module CompetitiveAdvantageCreation.Render

open CompetitiveAdvantageCreation.Domain
open CompetitiveAdvantageCreation.Inputs
open CompetitiveAdvantageCreation.Analysis

let table (header: string list) (rows: string list list) =
    let line cells = "| " + (cells |> List.map (fun (c: string) -> c.Replace("|", "/")) |> String.concat " | ") + " |"
    (line header :: ("|" + (header |> List.map (fun _ -> "---") |> String.concat "|") + "|") :: (rows |> List.map line)) |> String.concat "\n" |> fun s -> s + "\n"

let f = Csv.fmt
let optM (m: int option) = match m with Some v -> string v | None -> "none"
let optF (x: float option) = match x with Some v -> f v | None -> "none"
let mOpt (x: float option) = match x with Some v -> money v | None -> "n/a"
let r0 (x: float) = System.Math.Round(x, 0, System.MidpointRounding.AwayFromZero)

// ------------------------------------------------------------------ capital

let capitalTables (i: Inputs) =
    let fi = [ for v in [ AsPublished; Corrected ] do for s in i.States do for c in cases do yield v, s, c, firstInvoice i v c s ]
    let csvFi =
        Csv.write [ "variant"; "state_id"; "case"; "category"; "cash"; "non_cash"; "fully_loaded" ]
            [ for v, s, c, r in fi do
                  for cat in r.Categories do
                      yield [ capitalVariantName v; s.StateId; caseName c; cat.Category; f cat.Cash; f cat.NonCash; f cat.FullyLoaded ] ]
    let byState v =
        table [ "State"; "Months to first invoice (fav / base / adv)"; "Cash to first invoice (fav / base / adv)"; "Fully loaded (fav / base / adv)"; "Non-cash share (base)" ]
            [ for s in i.States do
                  let rs = cases |> List.map (fun c -> firstInvoice i v c s)
                  let b = rs.[1]
                  let name = if s.StateId = "S7" then s.Name + " (hypothetical: no second revenue-bearing product exists)" else s.Name
                  yield [ s.StateId + " " + name; rs |> List.map (fun r -> num0 r.Months) |> String.concat " / "
                          rs |> List.map (fun r -> money r.Cash) |> String.concat " / "; rs |> List.map (fun r -> money r.FullyLoaded) |> String.concat " / "
                          pct (if b.FullyLoaded > 0.0 then b.NonCash / b.FullyLoaded else 0.0) ] ]
    let s3 = i.States |> List.find (fun s -> s.StateId = "S3")
    let cats =
        let rs = cases |> List.map (fun c -> firstInvoice i Corrected c s3)
        table [ "Category (S3 to first invoice, corrected)"; "Cash fav"; "Cash base"; "Cash adv"; "Non-cash base"; "Fully loaded base" ]
            ((rs.[1].Categories |> List.mapi (fun k cat ->
                [ cat.Category; money rs.[0].Categories.[k].Cash; money cat.Cash; money rs.[2].Categories.[k].Cash; money cat.NonCash; money cat.FullyLoaded ]))
             @ [ [ "**Total**"; money rs.[0].Cash; money rs.[1].Cash; money rs.[2].Cash; money rs.[1].NonCash; money rs.[1].FullyLoaded ] ])
    let ss = [ for s in preRevenueStates i do for c in cases do yield selfSufficiencyAsPublished i c s ]
    // Revision 2: the corrected path is the sequence model (A from S2, A3 from S3), uninterrupted, founder-funded
    let corrected =
        [ for mode in [ registryMode i; registryModeConditional i ] do
              for sid, state in [ "SEQ-A", "S2"; "SEQ-A3", "S3" ] do
                  let m = i.Metas |> List.find (fun x -> x.SeqId = sid)
                  for c in cases do
                      yield mode, state, c, runSeq i (seqGlobalMode i mode c) m c Sequences.FounderFunded (Some None) ]
    let ssTable =
        table [ "State"; "Variant"; "Case"; "Peak cash deficit (to self-sufficiency)"; "Cash payback month"; "Discounted payback (10%)"; "Peak fully loaded deficit"; "Fully loaded payback month" ]
            ([ for x in ss do
                   yield [ x.StateId; "AB as published (AB revenue, no registry)"; caseName x.Case; money x.Summary.PeakDeficit; monthStr x.Summary.PaybackMonth; monthStr x.Summary.DiscountedPaybackMonth
                           money x.Summary.PeakEconomicDeficit; monthStr x.Summary.EconomicPaybackMonth ] ]
             @ [ for mode, state, c, o in corrected do
                     let bl = (primaryBasis i).Label
                     let label = if mode = registryMode i then $"{bl}, registry {mode} (governing)" else $"{bl}, registry {mode} (conditional on OD-CDD-02)"
                     yield [ state; label; caseName c; money o.Summary.PeakDeficit; monthStr o.Summary.PaybackMonth; monthStr o.Summary.DiscountedPaybackMonth
                             money o.Summary.PeakEconomicDeficit; monthStr o.Summary.EconomicPaybackMonth ] ])
    let ssCsv =
        Csv.write [ "variant"; "state_id"; "case"; "peak_cash_deficit"; "peak_month"; "payback_month"; "discounted_payback_month"; "peak_economic_deficit"; "economic_payback_month"; "first_revenue_month" ]
            ([ for x in ss do
                   yield [ "AB as published"; x.StateId; caseName x.Case; f x.Summary.PeakDeficit; string x.Summary.PeakDeficitMonth; optM x.Summary.PaybackMonth; optM x.Summary.DiscountedPaybackMonth
                           f x.Summary.PeakEconomicDeficit; optM x.Summary.EconomicPaybackMonth; optM x.Summary.FirstRevenueMonth ] ]
             @ [ for mode, state, c, o in corrected do
                     yield [ (primaryBasis i).Id + " registry " + mode; state; caseName c; f (r0 o.Summary.PeakDeficit); string o.Summary.PeakDeficitMonth; optM o.Summary.PaybackMonth; optM o.Summary.DiscountedPaybackMonth
                             f (r0 o.Summary.PeakEconomicDeficit); optM o.Summary.EconomicPaybackMonth; optM o.Summary.FirstRevenueMonth ] ])
    let dc = doubleCounts i
    let dcTable = table [ "Route"; "Variant"; "Build-phase burn factor"; "Variable share"; "Capital (deepest deficit)" ] (dc |> List.map (fun d -> [ d.Route; d.Variant; num2 d.BurnFactor; num2 d.VariableShare; money d.Capital ]))
    let dcCsv = Csv.write [ "route_id"; "variant"; "build_phase_burn_factor"; "variable_share"; "capital" ] (dc |> List.map (fun d -> [ d.Route; d.Variant; f d.BurnFactor; f d.VariableShare; f d.Capital ]))
    [ "capital-first-invoice.csv", csvFi
      "capital-self-sufficiency.csv", ssCsv
      "phase2-double-count.csv", dcCsv
      "tables/capital-by-state-as-published.md", byState AsPublished
      "tables/capital-by-state-corrected.md", byState Corrected
      "tables/capital-s3-conditional.md",
      (let rs = cases |> List.map (fun c -> firstInvoiceMode i (registryModeConditional i) Corrected c (i.States |> List.find (fun s -> s.StateId = "S3")))
       table [ "S3 to first invoice, registry " + registryModeConditional i + " (conditional on OD-CDD-02)"; "Favourable"; "Base"; "Adverse" ]
           [ [ "cash"; money rs.[0].Cash; money rs.[1].Cash; money rs.[2].Cash ]; [ "fully loaded"; money rs.[0].FullyLoaded; money rs.[1].FullyLoaded; money rs.[2].FullyLoaded ] ])
      "tables/capital-s3-categories.md", cats
      "tables/capital-self-sufficiency.md", ssTable
      "tables/phase2-double-count.md", dcTable ]

// ------------------------------------------------------------------ events

let eventTables (i: Inputs) =
    let rows =
        [ for name, c in eventScenarios do
              let t = Events.totals name i.Events
              let r = eventRates i c
              yield name, t, r ]
    let cat =
        table [ "Scenario"; "Conventional min"; "Eliminated"; "Automated"; "Accelerated"; "To customer"; "To partner"; "Mandatory"; "Other residual"; "System cost $/acct-yr"; "Conventional $/acct-yr" ]
            [ for name, t, r in rows do
                  yield [ name; num1 t.Conventional; num1 t.Eliminated; num1 t.Automated; num1 t.Accelerated; num1 t.ToCustomer; num1 t.ToPartner; num1 t.Mandatory; num1 t.ResidualOther
                          money (Events.systemCost r t); money (t.Conventional * r.LabourPerMinute) ] ]
    let _, tb, rb = rows.[1]
    let wf =
        table [ "Step (base, sequential)"; "Minutes before"; "Removed"; "After"; "Residual cost created $"; "System saving $" ]
            (Events.waterfall rb tb |> List.map (fun s -> [ s.Step; num1 s.MinutesBefore; num1 s.MinutesRemoved; num1 s.MinutesAfter; money s.ResidualCost; money s.Saving ]))
    let bp = Events.byParty rb tb
    let party =
        table [ "Who carries the cost afterwards (base, $/account-year)"; "Amount" ]
            [ [ "staffed residual (sponsor or administrator)"; money bp.Staffed ]; [ "platform (automation upkeep)"; money bp.Platform ]; [ "AI cost and oversight"; money bp.Ai ]
              [ "customer (donor, advisor, sponsor self-service)"; money bp.Customer ]; [ "partner (rail, advisor firm, central organisation)"; money bp.Partner ] ]
    let steps, combined, naive = vettingDoubleCount i
    let dbl =
        table [ "Claim on EV-E08 vetting labour (10k-account sponsor, base)"; "Saving if applied sequentially" ]
            ((steps |> List.map (fun (n, x) -> [ n; money x ])) @ [ [ "**Sequential total**"; money combined ]; [ "Naive sum of the two claims"; money naive ] ])
    let csv =
        Csv.write [ "scenario"; "step"; "minutes_before"; "removed"; "after"; "residual_cost"; "saving" ]
            [ for name, t, r in rows do
                  for s in Events.waterfall r t do
                      yield [ name; s.Step; f s.MinutesBefore; f s.MinutesRemoved; f s.MinutesAfter; f s.ResidualCost; f s.Saving ] ]
    let et = eventTornado i
    let tor = table [ "Variable"; "Low"; "High"; "System cost at low"; "System cost at high" ] (et |> List.map (fun (n, l, h, a, b) -> [ n; l; h; money a; money b ]))
    [ "event-waterfall.csv", csv
      "tables/events-categories.md", cat
      "tables/events-waterfall.md", wf
      "tables/events-by-party.md", party
      "tables/events-double-count.md", dbl
      "tables/tornado-events.md", tor ]

// ------------------------------------------------------------------ registry

let registryTables (i: Inputs) =
    let grid =
        [ for c in cases do
              for mode in Registry.modes do
                  for ch in [ 5000.0; 20000.0; 50000.0 ] do
                      for sp in [ 1.0; 10.0; 30.0 ] do
                          yield c, mode, ch, sp, registryAt i c mode ch sp ]
    let csv =
        Csv.write [ "case"; "mode"; "charities_per_sponsor"; "sponsors"; "union"; "engineering"; "counsel"; "shared_labour"; "floor_top_up"; "sponsor_specific_per_sponsor"; "shared"; "total" ]
            (grid |> List.map (fun (c, m, ch, sp, r) -> [ caseName c; m; f ch; f sp; f r.Union; f r.Engineering; f r.Counsel; f r.SharedLabour; f r.FloorApplied; f r.SponsorSpecificPerSponsor; f r.Shared; f r.Total ]))
    let modes =
        table [ "Mode (1 sponsor, 20k charities)"; "Favourable"; "Base"; "Adverse"; "Engineering (base)"; "Labour incl. floor (base)"; "Sponsor-specific (base)" ]
            [ for mode in Registry.modes do
                  let rs = cases |> List.map (fun c -> registryAt i c mode 20000.0 1.0)
                  let b = rs.[1]
                  yield [ mode; money rs.[0].Total; money b.Total; money rs.[2].Total; money b.Engineering; money (b.SharedLabour + b.FloorApplied); money b.SponsorSpecificPerSponsor ] ]
    let mode = registryModeConditional i
    let marg =
        table [ "Charities per sponsor (" + mode + ")"; "From 1 to 2 sponsors"; "From 10 to 11"; "From 30 to 31"; "Average per sponsor at 10" ]
            [ for ch in [ 5000.0; 20000.0 ] do
                  let mc sp = Registry.marginalSponsor BaseCase (pv i.Params BaseCase "connectors") i.RegistryComponents mode { CharitiesPerSponsor = ch; Sponsors = sp }
                  yield [ num0 ch; money (mc 1.0); money (mc 10.0); money (mc 30.0); money ((registryAt i BaseCase mode ch 10.0).Total / 10.0) ] ]
    let gap =
        table [ "Mode"; "Case"; "Registry run (1 sponsor)"; "Added to a Phase II MD mode"; "Added to the lean licensor run (GAP-HI010 rule)"; "Lean addition at 10 sponsors" ]
            [ for md in [ registryMode i; registryModeConditional i ] do
                  for c in cases do
                      let ch = pv i.Params c "registry_charities"
                      let r = registryAt i c md ch 1.0
                      let label = if md = registryMode i then md + " (governing)" else md + " (conditional on OD-CDD-02)"
                      yield [ label; caseName c; money r.Total; money (Registry.addable Registry.PhaseTwoMode r); money (registryAddableFor i c md ch 1.0); money (registryAddableFor i c md ch 10.0) ] ]
    [ "registry-grid.csv", csv; "tables/registry-modes.md", modes; "tables/registry-marginal.md", marg; "tables/registry-gap-hi010.md", gap ]

// ------------------------------------------------------------------ channel, licensing, MVP

let channelTables (i: Inputs) =
    let cs = channelCases i |> List.map (fun (n, x) -> n, x, Channel.evaluate x)
    let t =
        table [ "Case"; "Revenue/yr"; "Life (yr)"; "Share"; "Margin transferred"; "PV"; "Enablement per deal"; "Partner total"; "Direct CAC"; "Break-even share"; "Vendor net revenue/yr" ]
            [ for n, x, r in cs do
                  yield [ n; money x.RevenuePerSponsor; num0 x.LifetimeYears; pct x.PartnerShare; money r.MarginTransferred; money r.MarginTransferredPv; mOpt r.EnablementPerDeal
                          mOpt r.PartnerCost; money r.DirectCac; (match r.BreakEvenShare with Some s -> pct s | None -> "n/a (no deal)"); money r.VendorNetRevenuePerYear ] ]
    let g =
        table [ "Sponsor size"; "Revenue/yr"; "Life"; "Direct CAC"; "Break-even share (undiscounted)"; "Break-even share (PV)" ]
            [ for size, rev, life, cac, r in breakEvenShareGrid i do
                  yield [ size; money rev; num0 life; money cac; (match r.BreakEvenShare with Some s -> pct s | None -> "n/a"); (match r.BreakEvenSharePv with Some s -> pct s | None -> "n/a") ] ]
    let csv =
        Csv.write [ "case"; "revenue"; "life"; "share"; "margin_transferred"; "margin_transferred_pv"; "enablement_per_deal"; "partner_cost"; "direct_cac"; "break_even_share"; "break_even_share_pv"; "months_to_first_partner_deal" ]
            [ for n, x, r in cs do
                  yield [ n; f x.RevenuePerSponsor; f x.LifetimeYears; f x.PartnerShare; f r.MarginTransferred; f r.MarginTransferredPv; optF r.EnablementPerDeal; optF r.PartnerCost; f r.DirectCac; optF r.BreakEvenShare; optF r.BreakEvenSharePv; optF r.MonthsToFirstPartnerDeal ] ]
    [ "channel.csv", csv; "tables/channel.md", t; "tables/channel-break-even-share.md", g ]

let licensingTables (i: Inputs) =
    let m = i.Mvp
    let rows = Licensing.grid m.Fixed m.Variable m.Balances m.Fees
    let csv =
        Csv.write [ "host_model"; "fixed_case"; "fixed_usd"; "var_case"; "var_usd"; "avg_balance"; "fee_rate"; "margin_per_acct"; "breakeven_accounts"; "breakeven_aua_usd" ]
            (rows |> List.map (fun r -> [ r.HostModel; r.FixedCase; f r.FixedUsd; r.VarCase; f r.VarUsd; f r.AvgBalance; f r.FeeRate; f r.MarginPerAccount;
                                          (match r.BreakEvenAccounts with Some n -> string n | None -> "never"); (match r.BreakEvenAua with Some a -> f a | None -> "never") ]))
    let summary =
        table [ "Host model (fixed and variable at base)"; "Balance"; "Fee 0.6%"; "Fee 1.0%"; "Fee 1.5%" ]
            [ for host, _ in m.Fixed do
                  for b in m.Balances do
                      let cell fee =
                          rows |> List.find (fun r -> r.HostModel = host && r.FixedCase = "base" && r.VarCase = "base" && r.AvgBalance = b && r.FeeRate = fee)
                          |> fun r -> match r.BreakEvenAccounts, r.BreakEvenAua with Some n, Some a -> $"{n} accts ({money a})" | _ -> "never"
                      yield [ host; money b; cell m.Fees.[0]; cell m.Fees.[1]; cell m.Fees.[2] ] ]
    let price = i.Params.["price_per_account"].Range
    let minFee = pv i.Params BaseCase "minimum_fee"
    let share = pv i.Params BaseCase "partner_share"
    let lic =
        table [ "Accounts"; "Vendor revenue at $" + num0 price.Low; "at $" + num0 price.Base; "at $" + num0 price.High; "(minimum fee " + money minFee + ", partner share " + pct share + ")" ]
            [ for a in [ 50.0; 250.0; 750.0; 1500.0; 5000.0; 10000.0 ] do
                  yield [ num0 a; money (Licensing.licenceRevenue a price.Low minFee share); money (Licensing.licenceRevenue a price.Base minFee share); money (Licensing.licenceRevenue a price.High minFee share); "" ] ]
    let fee = i.Params.["migration_assessment_fee"].Range
    let impl = i.Params.["impl_later"].Range
    let rec_ = i.Params.["customer_impl_recovery"].Range
    let mig =
        table [ "Migration revenue per engagement"; "Favourable"; "Base"; "Adverse" ]
            [ [ "assessment fee"; money fee.High; money fee.Base; money fee.Low ]
              [ "implementation fee (recovery share x later implementation cost)"; money (impl.Base * rec_.High); money (impl.Base * rec_.Base); money (impl.Base * rec_.Low) ]
              [ "total"; money (Licensing.migrationRevenue fee.High impl.Base rec_.High); money (Licensing.migrationRevenue fee.Base impl.Base rec_.Base); money (Licensing.migrationRevenue fee.Low impl.Base rec_.Low) ] ]
    let mt = mvpTornado i
    let tor = table [ "Variable (partner-hosted programme, others at base)"; "Low"; "High"; "Break-even accounts at low"; "at high" ] (mt |> List.map (fun (n, l, h, a, b) -> [ n; l; h; (match a with Some x -> string x | None -> "never"); (match b with Some x -> string x | None -> "never") ]))
    [ "mvp-grid.csv", csv; "tables/mvp-summary.md", summary; "tables/licensing-revenue.md", lic; "tables/migration-revenue.md", mig; "tables/tornado-mvp.md", tor ]

// ------------------------------------------------------------------ shared infrastructure

let sharedTables (i: Inputs) =
    let al = allocations i
    let csv =
        Csv.write [ "rule"; "pool_id"; "product_id"; "entity"; "weight"; "amount" ]
            [ for rule, xs, _ in al do
                  for a in xs do
                      yield [ SharedInfra.ruleName rule; a.PoolId; a.ProductId; Cashflow.entityCode a.Entity; f a.Weight; f a.Amount ] ]
    let t =
        table ([ "Rule" ] @ (i.Products |> List.map (fun p -> p.Id + " (" + Cashflow.entityCode p.Entity + ")")) @ [ "Total allocated"; "Pools total"; "Unbound share (implied S7 factor)" ])
            [ for rule, xs, ps in al do
                  let per pid = xs |> List.filter (fun a -> a.ProductId = pid) |> List.sumBy (fun a -> a.Amount)
                  yield [ SharedInfra.ruleName rule ] @ (i.Products |> List.map (fun p -> money (per p.Id))) @ [ money (xs |> List.sumBy (fun a -> a.Amount)); money (ps |> List.sumBy (fun p -> p.Annual)); num2 (SharedInfra.shareOf "PRD-UNB" xs ps) ] ]
    let ent =
        table [ "Rule"; "Entity"; "Allocated (base)" ]
            [ for rule, xs, _ in al do
                  for e, amt in SharedInfra.byEntity xs do
                      yield [ SharedInfra.ruleName rule; Cashflow.entityCode e; money amt ] ]
    [ "shared-infra.csv", csv; "tables/shared-infra.md", t; "tables/shared-infra-entities.md", ent ]

// ------------------------------------------------------------------ response

let responseTables (i: Inputs) =
    let rs = responseResults i
    let csv =
        Csv.write [ "scenario_id"; "case"; "cost_base"; "headline"; "net_price"; "break_even_accounts"; "accounts_per_year"; "years_to_break_even"; "reached_before_termination" ]
            (rs |> List.map (fun (c, _, r) -> [ r.ScenarioId; caseName c; r.CostBase; f r.Headline; f r.NetPrice; optF r.BreakEvenAccounts; f r.AccountsPerYear; optF r.YearsToBreakEven;
                                            (match r.ReachedBeforeTermination with Some b -> (if b then "yes" else "no") | None -> "n/a") ]))
    let name sid = i.Scenarios |> List.find (fun s -> s.Id = sid) |> fun s -> s.Name
    let t =
        table [ "Scenario"; "Case"; "Cost base"; "Acquisition (accounts/yr)"; "Net price"; "Break-even accounts"; "Years from first contract to break-even"; "Before termination?" ]
            (rs |> List.map (fun (c, acqLabel, r) ->
                [ r.ScenarioId + " " + name r.ScenarioId; caseName c; (if r.CostBase = (md6CostBase i).Name then "MD-6" else "lean"); num0 r.AccountsPerYear + " (" + acqLabel + ")"; "$" + num2 r.NetPrice;
                  (match r.BreakEvenAccounts with Some n -> num0 n | None -> "never"); (match r.YearsToBreakEven with Some y -> num1 y | None -> "not reached");
                  (match r.ReachedBeforeTermination with Some b -> (if b then "yes" else "no") | None -> "") ]))
    let walk =
        table [ "Cost base"; "Fixed/yr"; "Variable/acct"; "Walk-away net price (5 yrs, base acquisition)"; "(10 yrs)" ]
            [ for cb in [ md6CostBase i; leanCostBase i BaseCase; leanCostBaseFounderAtMarket i BaseCase ] do
                  let w h = Response.walkAwayPrice cb (accountsPerYear i) (pv i.Params BaseCase "churn") h
                  yield [ cb.Name; money cb.FixedAnnual; "$" + num2 cb.VariablePerAccount; (match w 5.0 with Some p -> "$" + num2 p | None -> "n/a"); (match w 10.0 with Some p -> "$" + num2 p | None -> "n/a") ] ]
    [ "response.csv", csv; "tables/response.md", t; "tables/response-walk-away.md", walk ]

// ------------------------------------------------------------------ sequences

let label (i: Inputs) sid = i.Metas |> List.find (fun m -> m.SeqId = sid) |> fun m -> m.Label

let sequenceTables (i: Inputs) (mc: McRow list) =
    let all = sequenceOutcomes i
    let outs = all |> List.filter (fun (_, k, _) -> k) |> List.map (fun (m, _, o) -> m, o)
    let freeOuts = all |> List.filter (fun (_, k, _) -> not k) |> List.map (fun (m, _, o) -> m, o)
    let pickO sid c fu = outs |> List.find (fun (m, o) -> m.SeqId = sid && o.Case = c && o.Funding = fu) |> snd
    let pickFree sid c fu = freeOuts |> List.find (fun (m, o) -> m.SeqId = sid && o.Case = c && o.Funding = fu) |> snd
    let h (o: Sequences.Outcome) m = o.Horizons |> List.find (fun x -> x.Month = m)
    let killStr (o: Sequences.Outcome) = match o.Kill.KillMonth with Some k -> $"paused at {k}" | None -> (if o.Kill.CostCenterMonth.IsNone then "clock not started" else "passes")
    let csv =
        Csv.write [ "seq_id"; "kill_rule"; "case"; "funding"; "horizon"; "cumulative_cash"; "peak_deficit_to_date"; "fully_loaded_cost"; "cumulative_economic"; "cac"; "development"; "implementation"; "revenue"; "gross_margin"; "working_capital"; "live_customers"; "signed"; "kill_month"; "kill_reason"; "first_revenue_month"; "sustainability_month"; "payback_month" ]
            [ for m, kill, o in all do
                  for x in o.Horizons do
                      yield [ m.SeqId; (if kill then "applied" else "not applied"); caseName o.Case; Sequences.fundingName o.Funding; string x.Month; f (r0 x.CumulativeCash); f (r0 x.PeakDeficitToDate); f (r0 x.FullyLoadedCost); f (r0 x.CumulativeEconomic)
                              f (r0 x.Cac); f (r0 x.Development); f (r0 x.Implementation); f (r0 x.Revenue); optF x.GrossMargin; f (r0 x.WorkingCapital); f x.LiveCustomers; f x.Signed
                              optM o.Kill.KillMonth; o.Kill.Reason; optM o.FirstRevenueMonth; optM o.SustainabilityMonth; optM o.Summary.PaybackMonth ] ]
    let baseOuts = i.Metas |> List.map (fun m -> m, pickO m.SeqId BaseCase Sequences.FounderFunded)
    let free = i.Metas |> List.map (fun m -> m, pickFree m.SeqId BaseCase Sequences.FounderFunded)
    // Revision 2 (REV2043, REV2018): rank on the kill-rule Monte Carlo median (rho 0.5) against an explicit
    // do-nothing baseline of $0; a sequence that loses less than another still loses.
    let mcOf sid = mc |> List.find (fun r -> r.Sequence = sid && r.KillRule && r.Rho = 0.5)
    let rows = free |> List.map (fun (m, o) -> Some m, Some o, (mcOf m.SeqId).Cum120P50)
    let ranked = ((None, None, 0.0) :: rows) |> List.sortBy (fun (m, _, p50) -> -p50, (match m with Some mm -> mm.SeqId | None -> ""))
    let ranking =
        table [ "Rank"; "Sequence"; "Kill-rule MC m120 P50 (rho 0.5)"; "P10"; "P90"; "Share paused"; "Versus do-nothing"; "Base kill rule"; "Cash at risk if paused"; "Uninterrupted base: first revenue"; "Peak cash"; "m24 / m60 / m120"; "Payback (discounted)" ]
            (ranked |> List.mapi (fun k (mo, oo, p50) ->
                match mo, oo with
                | Some m, Some o ->
                    let r = mcOf m.SeqId
                    let killed = baseOuts |> List.find (fun (mm, _) -> mm.SeqId = m.SeqId) |> snd
                    [ string (k + 1); m.Label + ": " + m.Name; money p50; money r.Cum120P10; money r.Cum120P90; pct r.ShareKilled
                      (if p50 > 0.0 then "better" else "worse"); killStr killed
                      (match killed.Kill.KillMonth with Some _ -> money killed.Summary.PeakDeficit | None -> "-")
                      optM o.FirstRevenueMonth; money o.Summary.PeakDeficit
                      money (h o 24).CumulativeCash + " / " + money (h o 60).CumulativeCash + " / " + money (h o 120).CumulativeCash
                      monthStr o.Summary.PaybackMonth + " (" + monthStr o.Summary.DiscountedPaybackMonth + ")" ]
                | _ -> [ string (k + 1); "Do nothing (no DAF-specific spend; founder time kept for other work)"; "$0"; "$0"; "$0"; "-"; "baseline"; "-"; "-"; "-"; "$0"; "$0 / $0 / $0"; "-" ]))
    let killedT =
        table [ "Seq (base, kill rule applied)"; "Kill rule"; "m24 cum. cash"; "m60"; "m120"; "Peak cash"; "Fully loaded cost to m120"; "Transferred sponsor conversion labour to m120 (not Echelon cost)" ]
            [ for m, o in baseOuts do
                  yield [ m.Label; killStr o; money (h o 24).CumulativeCash; money (h o 60).CumulativeCash; money (h o 120).CumulativeCash; money o.Summary.PeakDeficit
                          money (h o 120).FullyLoadedCost; money o.TransferredToSponsor ] ]
    let horizonsT =
        table [ "Seq (base, uninterrupted)"; "Month"; "Cum. cash"; "Peak to date"; "Fully loaded cost"; "CAC"; "Development"; "Implementation"; "Revenue"; "Gross margin"; "Working capital"; "Live customers" ]
            [ for m, o in free do
                  for x in o.Horizons do
                      yield [ m.Label; string x.Month; money x.CumulativeCash; money x.PeakDeficitToDate; money x.FullyLoadedCost; money x.Cac; money x.Development; money x.Implementation
                              money x.Revenue; (match x.GrossMargin with Some g -> pct g | None -> "n/a"); money x.WorkingCapital; num1 x.LiveCustomers ] ]
    let funding =
        table [ "Seq (base, uninterrupted)"; "Founder-funded peak"; "Customer-funded peak"; "Partner-funded peak"; "Externally funded peak"; "Founder m120 cash"; "Customer m120"; "Partner m120"; "External m120 economic" ]
            [ for m in i.Metas do
                  let o fu = pickFree m.SeqId BaseCase fu
                  yield [ m.Label; money (o Sequences.FounderFunded).Summary.PeakDeficit; money (o Sequences.CustomerFunded).Summary.PeakDeficit; money (o Sequences.PartnerFunded).Summary.PeakDeficit
                          money (o Sequences.ExternallyFunded).Summary.PeakDeficit; money (List.last (o Sequences.FounderFunded).Summary.Cumulative); money (List.last (o Sequences.CustomerFunded).Summary.Cumulative)
                          money (List.last (o Sequences.PartnerFunded).Summary.Cumulative); money (List.last (o Sequences.ExternallyFunded).Summary.EconomicCumulative) ] ]
    let casesT =
        table [ "Seq"; "Case"; "Kill rule"; "Cash at risk if paused"; "Uninterrupted: first revenue"; "Peak cash need"; "Peak fully loaded deficit"; "Cum. cash m120"; "Economic net m120"; "Payback"; "CAC per customer"; "Founder-months" ]
            [ for m in i.Metas do
                  for c in cases do
                      let k = pickO m.SeqId c Sequences.FounderFunded
                      let o = pickFree m.SeqId c Sequences.FounderFunded
                      yield [ m.Label; caseName c; killStr k; (match k.Kill.KillMonth with Some _ -> money k.Summary.PeakDeficit | None -> "-"); optM o.FirstRevenueMonth
                              money o.Summary.PeakDeficit; money o.Summary.PeakEconomicDeficit; money (List.last o.Summary.Cumulative)
                              money (List.last o.Summary.EconomicCumulative); monthStr o.Summary.PaybackMonth; mOpt o.CacPerCustomer; num0 o.MonthsOfFounderTime ] ]
    let qual =
        table [ "Seq"; "Failure band (qualitative)"; "Reversibility"; "Optionality"; "Dependencies"; "Opportunity cost" ]
            (i.Metas |> List.map (fun m -> [ m.Label; m.FailureBand; m.Reversibility; m.Optionality; m.Dependencies; m.OpportunityCost ]))
    let ks = killSensitivity i
    let killT =
        table [ "Seq"; "Cost-center rule"; "Cost-center month"; "Kill month"; "Reason"; "Peak cash"; "Cum. cash m120" ]
            [ for m, name, o in ks do
                  yield [ m.Label; name; (match o.Kill.CostCenterMonth with Some t -> num0 t | None -> "none"); optM o.Kill.KillMonth; o.Kill.Reason; money o.Summary.PeakDeficit; money (List.last o.Summary.Cumulative) ] ]
    let killCsv =
        Csv.write [ "seq_id"; "rule"; "cost_center_month"; "named_partner_month"; "pilot_month"; "kill_month"; "reason"; "peak_deficit"; "cumulative_m120" ]
            [ for m, name, o in ks do
                  yield [ m.SeqId; name; (match o.Kill.CostCenterMonth with Some t -> f t | None -> "none"); f o.Kill.NamedPartnerMonth; optM o.Kill.PilotMonth; optM o.Kill.KillMonth; o.Kill.Reason; f (r0 o.Summary.PeakDeficit); f (r0 (List.last o.Summary.Cumulative)) ] ]
    [ "sequences.csv", csv; "kill-sensitivity.csv", killCsv
      "tables/sequences-ranking.md", ranking; "tables/sequences-kill-rule.md", killedT; "tables/sequences-horizons.md", horizonsT; "tables/sequences-funding.md", funding
      "tables/sequences-cases.md", casesT; "tables/sequences-qualitative.md", qual; "tables/kill-sensitivity.md", killT ], all

// ------------------------------------------------------------------ sensitivity, Monte Carlo, extremes

let stressTables (i: Inputs) (mc: McRow list) =
    let tor = tornado i "SEQ-A3"
    let torT =
        table [ "Variable (sequence A3, base, uninterrupted)"; "Low"; "High"; "Peak cash at low"; "Peak cash at high"; "Economic m120 at low"; "at high" ]
            (tor |> List.map (fun t -> [ t.Variable; t.Low; t.High; money t.PeakAtLow; money t.PeakAtHigh; money t.EconAtLow; money t.EconAtHigh ]))
    let torCsv = Csv.write [ "sequence"; "variable"; "low"; "high"; "peak_at_low"; "peak_at_high"; "economic_m120_at_low"; "economic_m120_at_high" ] (tor |> List.map (fun t -> [ t.Sequence; t.Variable; t.Low; t.High; f t.PeakAtLow; f t.PeakAtHigh; f t.EconAtLow; f t.EconAtHigh ]))
    let mcT =
        table [ "Seq"; "Kill rule"; "rho"; "Peak cash P10"; "P50"; "P90"; "Cum. cash m120 P10"; "P50"; "P90"; "Economic m120 P50"; "Share no payback in 120 m"; "Share paused (kill rule) or partner terminated"; "Payback P50" ]
            (mc |> List.map (fun r -> [ label i r.Sequence; (if r.KillRule then "applied" else "not applied"); num1 r.Rho; money r.PeakP10; money r.PeakP50; money r.PeakP90; money r.Cum120P10; money r.Cum120P50; money r.Cum120P90; money r.EconP50; pct r.ShareNoPayback; pct r.ShareKilled; (if System.Double.IsInfinity r.PaybackP50 then "none" else num0 r.PaybackP50) ]))
    let mcCsv =
        Csv.write [ "seq_id"; "kill_rule"; "rho"; "peak_p10"; "peak_p50"; "peak_p90"; "cum120_p10"; "cum120_p50"; "cum120_p90"; "economic120_p50"; "share_no_payback"; "share_killed"; "payback_p50" ]
            (mc |> List.map (fun r -> [ r.Sequence; (if r.KillRule then "applied" else "not applied"); f r.Rho; f (r0 r.PeakP10); f (r0 r.PeakP50); f (r0 r.PeakP90); f (r0 r.Cum120P10); f (r0 r.Cum120P50); f (r0 r.Cum120P90); f (r0 r.EconP50); f r.ShareNoPayback; f r.ShareKilled; f r.PaybackP50 ]))
    let xs = extremes i
    let ex = [ for kill in [ false; true ] do for m in i.Metas do for x in xs do yield kill, m, x, runExtremeWith kill i m x ]
    let exTable kill title =
        table ([ title ] @ (i.Metas |> List.map (fun m -> m.Label + " peak / m120")))
            [ for x in xs do
                  yield [ x.Name ] @ (i.Metas |> List.map (fun m ->
                      let _, _, _, o = ex |> List.find (fun (k, mm, xx, _) -> k = kill && mm.SeqId = m.SeqId && xx.Name = x.Name)
                      money o.Summary.PeakDeficit + " / " + money (List.last o.Summary.Cumulative))) ]
    let exT = exTable false "Scenario (uninterrupted)"
    let exK = exTable true "Scenario (kill rule applied)"
    let exCsv =
        Csv.write [ "seq_id"; "kill_rule"; "scenario"; "peak_deficit"; "cumulative_m120"; "economic_m120"; "payback_month"; "kill_month" ]
            [ for kill, m, x, o in ex do yield [ m.SeqId; (if kill then "applied" else "not applied"); x.Name; f (r0 o.Summary.PeakDeficit); f (r0 (List.last o.Summary.Cumulative)); f (r0 (List.last o.Summary.EconomicCumulative)); optM o.Summary.PaybackMonth; optM o.Kill.KillMonth ] ]
    [ "tornado.csv", torCsv; "monte-carlo.csv", mcCsv; "extremes.csv", exCsv
      "tables/tornado-sequence-a3.md", torT; "tables/monte-carlo.md", mcT; "tables/extremes.md", exT; "tables/extremes-kill-rule.md", exK ]

// ------------------------------------------------------------------ generated fragments (agent MOD)

let fragmentRows (i: Inputs) (all: (Sequences.SequenceMeta * bool * Sequences.Outcome) list) =
    let capHeader = [ "capital_id"; "state_or_stage"; "cost_category"; "cash_low"; "cash_base"; "cash_high"; "fully_loaded_low"; "fully_loaded_base"; "fully_loaded_high"; "removed_cost_replacement_mechanism"; "residual_risk"; "evidence_required"; "source_ids"; "report" ]
    let s3 = i.States |> List.find (fun s -> s.StateId = "S3")
    let fiRows =
        preRevenueStates i
        |> List.map (fun s ->
            let rs = cases |> List.map (fun c -> firstInvoice i Corrected c s)
            s.StateId + " to first referenceable invoice", "total (" + (primaryBasis i).Label + ": registry " + registryMode i + "; TPSP; control operations)", rs |> List.map (fun r -> r.Cash), rs |> List.map (fun r -> r.FullyLoaded),
            "Lean licensor run plus funded control operations; partner first line", "Registry review and control floors remain; sales cycle dominates", "V-6 named partner; broker indications; OD-CDD-02")
    let catRows =
        let rs = cases |> List.map (fun c -> firstInvoice i Corrected c s3)
        rs.[1].Categories |> List.mapi (fun k cat ->
            "S3 to first referenceable invoice", cat.Category, rs |> List.map (fun r -> r.Categories.[k].Cash), rs |> List.map (fun r -> r.Categories.[k].FullyLoaded),
            "See report 02 section 5 (agent AB) for the replacement mechanism of each removed conventional cost", "As AB", "As AB")
    let ssRows =
        [ "SEQ-A", "S2"; "SEQ-A3", "S3" ]
        |> List.map (fun (sid, state) ->
            let m = i.Metas |> List.find (fun x -> x.SeqId = sid)
            let rs = cases |> List.map (fun c -> runSeq i (seqGlobal i c) m c Sequences.FounderFunded (Some None))
            state + " to self-sufficiency (deepest cumulative deficit; " + (primaryBasis i).Label + ", registry " + registryMode i + ")", "total (sequence " + m.Label + ", uninterrupted)",
            rs |> List.map (fun r -> r.Summary.PeakDeficit), rs |> List.map (fun r -> r.Summary.PeakEconomicDeficit),
            "Channel licensing at the A3 sponsor size, capped by the FY2024 sponsor population", "Not finite where no payback within 120 months; bounded by the kill rule", "Partner throughput (V-6); sponsor-size evidence (P3-GAP-MOD003)")
    let capRows =
        (fiRows @ catRows @ ssRows)
        |> List.mapi (fun k (stage, cat, cash: float list, fl: float list, mech, risk, ev) ->
            [ sprintf "P3-CAP-MOD%03d" (k + 1); stage; cat; f (r0 cash.[0]); f (r0 cash.[1]); f (r0 cash.[2]); f (r0 fl.[0]); f (r0 fl.[1]); f (r0 fl.[2]); mech; risk; ev
              "P3-ASM-AB001;P3-ASM-AB018;P3-ASM-AB027;P3-ASM-AB028;P3-ASM-MOD010;P3-ASM-MOD040;P3-ASM-MOD041;P3-ASM-MOD049"; "18" ])
    let seqHeader = [ "sequence_id"; "sequence"; "steps"; "time_to_first_revenue_months"; "incremental_cash"; "fully_loaded_cost"; "failure_band"; "reversibility"; "dependencies"; "funding_route"; "source_ids"; "report" ]
    let seqRows =
        i.Metas
        |> List.map (fun m ->
            let pick kill c fu = all |> List.find (fun (mm, k, x) -> mm.SeqId = m.SeqId && k = kill && x.Case = c && x.Funding = fu) |> fun (_, _, x) -> x
            let o = pick false
            let kb = pick true BaseCase Sequences.FounderFunded
            let killNote = match kb.Kill.KillMonth with Some k -> $"; base under the kill rule: paused at month {k} with {money kb.Summary.PeakDeficit} spent" | None -> ""
            let fr = cases |> List.map (fun c -> optM (o c Sequences.FounderFunded).FirstRevenueMonth) |> String.concat " / "
            let peak = cases |> List.map (fun c -> money (o c Sequences.FounderFunded).Summary.PeakDeficit) |> String.concat " / "
            let fl = cases |> List.map (fun c -> money (o c Sequences.FounderFunded).Summary.PeakEconomicDeficit) |> String.concat " / "
            let best = Sequences.fundings |> List.minBy (fun fu -> (o BaseCase fu).Summary.PeakDeficit, Sequences.fundingName fu)
            let ids = (m.AssumptionIds @ (streamsOf i m.SeqId |> List.collect (fun s -> s.AssumptionIds))) |> List.distinct |> List.sort |> String.concat ";"
            [ m.RegisterId; m.Label + ": " + m.Name; "Modelled streams: " + (streamsOf i m.SeqId |> List.map (fun s -> s.Name) |> String.concat " + ")
              "uninterrupted fav / base / adv: " + fr; "uninterrupted peak cash need fav / base / adv: " + peak + killNote; "uninterrupted peak fully loaded deficit fav / base / adv: " + fl
              m.FailureBand; m.Reversibility; m.Dependencies; $"lowest base peak: {Sequences.fundingName best} (all four variants in report 14)"; ids; "14" ])
    [ "fragment-capital-requirements.csv", Csv.write capHeader capRows; "fragment-commercial-sequences.csv", Csv.write seqHeader seqRows ]

let keyFigures (i: Inputs) (mc: McRow list) =
    let bl = (primaryBasis i).Label
    let s3 = i.States |> List.find (fun s -> s.StateId = "S3")
    let fi mode v = cases |> List.map (fun c -> firstInvoiceMode i mode v c s3)
    let gov, cond = registryMode i, registryModeConditional i
    let seq mode sid c = runSeq i (seqGlobalMode i mode c) (i.Metas |> List.find (fun x -> x.SeqId = sid)) c Sequences.FounderFunded (Some None)
    let tri (xs: float list) = xs |> List.map money |> String.concat " / "
    let triO mode sid (f: Sequences.Outcome -> string) = cases |> List.map (fun c -> f (seq mode sid c)) |> String.concat " / "
    let mcA3 = mc |> List.find (fun r -> r.Sequence = "SEQ-A3" && r.KillRule && r.Rho = 0.5)
    let killedA = runSeq i (seqGlobal i BaseCase) (i.Metas |> List.find (fun x -> x.SeqId = "SEQ-A")) BaseCase Sequences.FounderFunded None
    table [ "Measure"; "Favourable / base / adverse" ]
        [ [ "S3 cash to first referenceable invoice, AB method as published"; tri (fi gov AsPublished |> List.map (fun r -> r.Cash)) ]
          [ $"S3 cash to first invoice, {bl}, registry {gov} (governing)"; tri (fi gov Corrected |> List.map (fun r -> r.Cash)) ]
          [ $"S3 fully loaded to first invoice, {bl}, registry {gov}"; tri (fi gov Corrected |> List.map (fun r -> r.FullyLoaded)) ]
          [ $"S3 cash to first invoice, {bl}, registry {cond} (conditional on OD-CDD-02)"; tri (fi cond Corrected |> List.map (fun r -> r.Cash)) ]
          [ $"A3 peak cash (uninterrupted), registry {gov}"; triO gov "SEQ-A3" (fun o -> money o.Summary.PeakDeficit) ]
          [ $"A3 cash payback month, registry {gov}"; triO gov "SEQ-A3" (fun o -> monthStr o.Summary.PaybackMonth) ]
          [ $"A3 peak cash (uninterrupted), registry {cond}"; triO cond "SEQ-A3" (fun o -> money o.Summary.PeakDeficit) ]
          [ $"A3 cash payback month (discounted), registry {cond}"; triO cond "SEQ-A3" (fun o -> monthStr o.Summary.PaybackMonth + " (" + monthStr o.Summary.DiscountedPaybackMonth + ")") ]
          [ $"A3 peak fully loaded deficit, registry {cond}"; triO cond "SEQ-A3" (fun o -> money o.Summary.PeakEconomicDeficit) ]
          [ "A3 with the S2-to-S3 build inside the cost center (A3B), peak cash, registry " + gov; triO gov "SEQ-A3B" (fun o -> money o.Summary.PeakDeficit) ]
          [ "A3 kill-rule Monte Carlo (rho 0.5): share paused / share with no payback / m120 P50"; pct mcA3.ShareKilled + " / " + pct mcA3.ShareNoPayback + " / " + money mcA3.Cum120P50 ]
          [ "From today (A), base under the kill rule"; (match killedA.Kill.KillMonth with Some k -> $"paused at month {k} after {money killedA.Summary.PeakDeficit}" | None -> "passes") ]
          [ $"Registry added to the lean licensor, one sponsor at default charities, {gov}"; tri (cases |> List.map (registryAddable i)) ] ]

let sizeTables (i: Inputs) =
    let sizes = [ 250.0; 750.0; 1500.0; 2646.0; 5291.0; 10582.0 ]
    let rows = sizeTable i sizes
    let t =
        table [ "Registry mode"; "Accounts per customer"; "Net revenue per customer"; "FY2024 sponsors this large (all / plausible)"; "Reachable customers (cap on the active basis)"; "Peak cash (uninterrupted)"; "m120 cash (uninterrupted)"; "Payback"; "Under the kill rule" ]
            [ for r in rows do
                  let label = if r.Mode = registryMode i then r.Mode + " (governing)" else r.Mode + " (conditional)"
                  yield [ label; num0 r.Accounts; money r.NetRevenue; num0 r.Eligible + " / " + num0 r.NonCaptive; num0 r.MaxCustomers
                          money r.Uninterrupted.Summary.PeakDeficit; money (List.last r.Uninterrupted.Summary.Cumulative); monthStr r.Uninterrupted.Summary.PaybackMonth
                          (match r.WithKill.Kill.KillMonth with Some k -> $"paused at {k}" | None -> "passes") ] ]
    let price = a3Value i BaseCase "price_per_account"
    let share = a3Value i BaseCase "partner_share"
    let be =
        table [ "Registry mode"; "Break-even sponsor size (accounts; uncapped population, uninterrupted)"; "Break-even net revenue per customer"; "FY2024 sponsors at least that large (all / plausible)" ]
            [ for md in [ registryMode i; registryModeConditional i ] do
                  match breakEvenAccounts i md with
                  | Some a -> let all, nc = eligible i a in yield [ md; num0 a; money (a * price * (1.0 - share)); num0 all + " / " + num0 nc ]
                  | None -> yield [ md; "not reached below 100,000 accounts"; "none"; "0 / 0" ] ]
    let csv =
        Csv.write [ "registry_mode"; "accounts"; "net_revenue"; "eligible_all"; "eligible_non_captive"; "max_customers"; "peak_uninterrupted"; "m120_uninterrupted"; "payback"; "kill_month" ]
            [ for r in rows do yield [ r.Mode; f r.Accounts; f r.NetRevenue; f r.Eligible; f r.NonCaptive; f r.MaxCustomers; f (r0 r.Uninterrupted.Summary.PeakDeficit); f (r0 (List.last r.Uninterrupted.Summary.Cumulative)); optM r.Uninterrupted.Summary.PaybackMonth; optM r.WithKill.Kill.KillMonth ] ]
    [ "sponsor-size.csv", csv; "tables/sponsor-size.md", t; "tables/break-even-revenue.md", be ]

/// Revision 3 tables: bases side by side, gate break-evens, cap sensitivity, kill timing, platform classes.
let revision3Tables (i: Inputs) =
    let s3 = i.States |> List.find (fun s -> s.StateId = "S3")
    let killStr (o: Sequences.Outcome) = match o.Kill.KillMonth with Some k -> $"paused at {k} ({money o.Summary.PeakDeficit})" | None -> "passes"
    let grid = basisConfigs i
    let bases =
        table [ "Basis"; "Registry configuration"; "S3 cash / fully loaded to first invoice"; "A3 peak / m120 / payback"; "A3 kill rule"; "A peak / m120 / payback"; "A kill rule"; "Partner book peak / m120 / payback"; "Partner book kill rule" ]
            [ for b, cfg in grid do
                  let fi = firstInvoiceB i b cfg Corrected BaseCase s3
                  let free sid = runFor i b cfg sid (Some None)
                  let killed sid = runFor i b cfg sid None
                  let ppp (o: Sequences.Outcome) = money o.Summary.PeakDeficit + " / " + money (List.last o.Summary.Cumulative) + " / " + monthStr o.Summary.PaybackMonth
                  yield [ b.Label; (registryConfig cfg).Label; money fi.Cash + " / " + money fi.FullyLoaded
                          ppp (free "SEQ-A3"); killStr (killed "SEQ-A3"); ppp (free "SEQ-A"); killStr (killed "SEQ-A"); ppp (free "SEQ-PB"); killStr (killed "SEQ-PB") ] ]
    let price = a3Value i BaseCase "price_per_account"
    let share = a3Value i BaseCase "partner_share"
    let gate =
        table [ "Basis"; "Registry configuration"; "Break-even single-sponsor size (accounts)"; "Net revenue per sponsor at break-even"; "FY2024 sponsors that large (all / plausible)"; "Break-even partner-book size (accounts)" ]
            [ for b, cfg in grid do
                  let sp = breakEvenFor i b cfg "SEQ-A3"
                  let pb = breakEvenFor i b cfg "SEQ-PB"
                  yield [ b.Label; (registryConfig cfg).Label
                          (match sp with Some a -> num0 a | None -> "not reached below 100,000")
                          (match sp with Some a -> money (a * price * (1.0 - share)) | None -> "none")
                          (match sp with Some a -> num0 (eligibleIn i "all" a) + " / " + num0 (eligibleIn i "plausible" a) | None -> "0 / 0")
                          (match pb with Some a -> num0 a | None -> "not reached below 100,000") ] ]
    let sizes = [ 2646.0; 3000.0; 5291.0; 10582.0 ]
    let platforms =
        table ([ "Cap set (rule)" ] @ (sizes |> List.map (fun a -> ">= " + num0 a + " accounts")))
            [ for cs, label in [ "all", "all sponsors (revision 2 cap)"; "excl-captive", "excluding national standard (revision 2 report count)"
                                 "plausible", "excluding processors and presumed own platforms (revision 3 cap)"; "third-party", "third-party platform evidence only" ] do
                  yield [ label ] @ (sizes |> List.map (fun a -> num0 (eligibleIn i cs a))) ]
    let capT =
        table [ "Cap set"; "A3 reachable customers (cap)"; "A3 peak (uninterrupted)"; "A3 m120"; "Live customers m120" ]
            [ for cs, o in capSensitivity i do
                  let reach = a3Value i BaseCase "reachable_share"
                  yield [ cs; num0 (floor (eligibleIn i cs (a3Value i BaseCase "accounts_per_customer") * reach)); money o.Summary.PeakDeficit; money (List.last o.Summary.Cumulative); num1 (List.last o.Horizons).LiveCustomers ] ]
    let timing =
        table [ "Go-live lag (months)"; "First signing"; "Cost center month 0"; "6"; "12" ]
            (killTiming i
             |> List.groupBy (fun (lag, whole, _, _) -> lag, whole)
             |> List.map (fun ((lag, whole), xs) ->
                 [ num0 lag; (if whole then "whole first customer" else "fractional (revision 2)") ]
                 @ (xs |> List.map (fun (_, _, _, o) -> (match o.Kill.KillMonth with Some k -> $"paused at {k}" | None -> "passes") + " (pilot " + optM o.Kill.PilotMonth + ")"))))
    [ "tables/bases.md", bases; "tables/gate-break-even.md", gate; "tables/platform-classes.md", platforms; "tables/cap-sensitivity.md", capT; "tables/kill-timing.md", timing ]

/// Every output file. Pure given inputs.
let outputs (i: Inputs) : (string * string) list =
    let n = match System.Int32.TryParse(setting i "mc_draws" "2000") with | true, x -> x | _ -> 2000
    let seed = match System.UInt64.TryParse(setting i "seed" "20261126") with | true, x -> x | _ -> 20261126UL
    let mc = [ for kill in [ false; true ] do for rho in [ 0.0; 0.5 ] do for m in i.Metas do yield monteCarlo i n seed rho kill m ]
    let seqFiles, allOuts = sequenceTables i mc
    let files =
        capitalTables i @ eventTables i @ registryTables i @ channelTables i @ licensingTables i @ sharedTables i @ responseTables i
        @ seqFiles @ stressTables i mc @ sizeTables i @ revision3Tables i @ fragmentRows i allOuts @ [ "tables/key-figures.md", keyFigures i mc ]
    let tables = files |> List.filter (fun (p, _) -> p.StartsWith "tables/") |> List.sortBy fst
    let results =
        "# Model results (generated)\n\nGenerated by `model/` (`run`); do not edit. Every number is conditional on the assumption ranges in `data/model-inputs/`. Tables are also written one per file under `tables/` for quoting in reports.\n\n"
        + (tables |> List.map (fun (p, t) -> "## " + p.Substring(7).Replace(".md", "") + "\n\n" + t) |> String.concat "\n")
    files @ [ "results.md", results ]
