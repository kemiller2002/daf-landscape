module CompetitiveAdvantageCreation.Tests

open System.IO
open Xunit
open CompetitiveAdvantageCreation
open CompetitiveAdvantageCreation.Domain

let inputDir = Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "data", "model-inputs")
let realInputs =
    lazy
        (match Inputs.load (fun f -> File.ReadAllText(Path.Combine(inputDir, f))) with
         | Ok i -> i
         | Error es -> failwithf "inputs failed: %A" es)
/// Real inputs with a small Monte Carlo so whole-output tests stay fast.
let smallInputs = lazy { realInputs.Value with Settings = Map.add "mc_draws" "40" realInputs.Value.Settings }

let close (tol: float) (expected: float) (actual: float) = Assert.True(abs (expected - actual) <= tol, $"expected {expected}, got {actual}")

let globals: Cashflow.Globals = { FounderEconAnnual = 222482.0; CapitalChargeAnnual = 0.10 }

/// A simple stream for unit tests.
let stream: Cashflow.Stream =
    { Id = "T"; Name = "test"; Entity = Cashflow.E2Unbound; Dedicated = true; KillExempt = false; StartMonth = 0.0
      DevCash = 120000.0; DevEcon = 350000.0; DevMonths = 6.0; OnetimeCash = 105000.0; OnetimeLeadMonths = 0.0
      PreRunMonthly = 8750.0; LiveRunMonthly = 38750.0; RegistryAnnualOf = (fun n -> 50000.0 * sqrt n); RegistryPreRevenue = false
      FounderFte = 1.0; FounderBuildShare = 0.0; FounderCashPreMonthly = 0.0; FounderCashLiveMonthly = 5000.0
      FirstSigningMonth = 15.0; CustomersPerYear = 3.0; MaxCustomers = infinity; RevenuePerCustomer = 300000.0; Recurring = true
      PartnerShare = 0.0; VariableShare = 0.2143; VarPerCustomerYear = 0.0; CacFirst = 30000.0; CacLater = 30000.0
      ImplFirst = 75000.0; ImplLater = 30000.0; ImplFirstCount = 1.0; ImplRecovery = 0.0; SponsorConversionPerCustomer = 0.0
      IncidentReserve = 0.0; WindDownFixed = 0.0; WindDownRunMonths = 0.0
      Churn = 0.08; GoLiveLag = 6.0; ArrearsMonths = 2.5; Contingency = 0.25; Basis = Cashflow.revision2Basis
      RegistryTransferredOf = (fun _ -> 0.0) }

// ------------------------------------------------------------------ accounting identities

[<Fact>]
let ``first-invoice categories: cash plus non-cash equals fully loaded and reproduces agent AB's S3 figures`` () =
    let i = realInputs.Value
    let s3 = i.States |> List.find (fun s -> s.StateId = "S3")
    let r = Analysis.firstInvoice i Analysis.AsPublished BaseCase s3
    close 1e-6 r.FullyLoaded (r.Cash + r.NonCash)
    close 1e-6 r.Cash (r.Categories |> List.sumBy (fun c -> c.Cash))
    close 1.0 998437.5 r.Cash
    close 1.0 1675144.3 r.FullyLoaded

[<Fact>]
let ``monthly cash cost equals the sum of its categories and net equals collections less cash cost`` () =
    let ms = Cashflow.flows globals stream None
    for m in ms do
        close 1e-6 m.CashCost (m.Variable + m.Run + m.Registry + m.DevCash + m.Onetime + m.Contingency + m.Cac + m.Impl + m.Reserve + m.WindDown + m.Tax + m.FounderCash)
        close 1e-6 m.Net (m.Collected - m.CashCost)

[<Fact>]
let ``fully loaded equals cash plus non-cash development, founder time and capital charge`` () =
    let ms = Cashflow.flows globals stream None
    let sm = Cashflow.summarize globals ms
    let cash = List.last sm.Cumulative
    let nonCash = (ms |> List.sumBy (fun m -> m.DevNonCash + m.FounderNonCash)) + List.sum sm.CapitalCharge
    close 1e-3 (cash - nonCash) (List.last sm.EconomicCumulative)

[<Fact>]
let ``cash versus economic cost: a founder working for no cash still costs the market rate`` () =
    let unpaid = { stream with FounderCashPreMonthly = 0.0; FounderCashLiveMonthly = 0.0; CustomersPerYear = 0.0 }
    let ms = Cashflow.flows globals unpaid None
    Assert.All(ms, fun m -> Assert.Equal(0.0, m.FounderCash))
    close 1e-6 (222482.0 * 10.0) (ms |> List.sumBy (fun m -> m.FounderNonCash))
    let sm = Cashflow.summarize globals ms
    Assert.True(sm.PeakEconomicDeficit > sm.PeakDeficit + 222482.0 * 9.0)

// ------------------------------------------------------------------ double counting and work categories

[<Fact>]
let ``sequential savings never exceed the cost base while a naive sum can`` () =
    let steps, combined, naive = Events.combineSequential 100.0 [ "a", 0.9; "b", 0.6667 ]
    Assert.True(combined <= 100.0)
    Assert.True(naive > 100.0)
    close 1e-9 combined (steps |> List.sumBy snd)

[<Fact>]
let ``vetting labour claimed by the event model and the registry model is not summed`` () =
    let _, combined, naive = Analysis.vettingDoubleCount realInputs.Value
    let e08 = realInputs.Value.Events |> List.find (fun e -> e.EventId = "EV-E08" && e.Scenario = "base")
    let baseCost = e08.Conventional * 1.454 * 10000.0
    Assert.True(combined <= baseCost + 1e-6)
    Assert.True(naive > baseCost)

[<Fact>]
let ``event waterfall savings are residuals and add up to conventional minus system cost`` () =
    let i = realInputs.Value
    for name, c in Analysis.eventScenarios do
        let t = Events.totals name i.Events
        let r = Analysis.eventRates i c
        let steps = Events.waterfall r t
        let conventionalCost = t.Conventional * r.LabourPerMinute
        close 1e-6 (conventionalCost - Events.systemCost r t) (steps |> List.sumBy (fun s -> s.Saving))
        Assert.True((steps |> List.sumBy (fun s -> s.MinutesRemoved)) <= t.Conventional + 1e-9)

[<Fact>]
let ``transferred work is never a saving and moving minutes from eliminated to transferred raises system cost`` () =
    let i = realInputs.Value
    let r = Analysis.eventRates i BaseCase
    let t = Events.totals "base" i.Events
    let steps = Events.waterfall r t
    Assert.All(steps |> List.filter (fun s -> s.Step.StartsWith "transferred"), fun s -> Assert.True(s.Saving <= 0.0))
    let moved = { t with Eliminated = t.Eliminated - 10.0; ToCustomer = t.ToCustomer + 10.0 }
    Assert.True(Events.systemCost r moved > Events.systemCost r t)

[<Fact>]
let ``event categories account for every conventional minute`` () =
    Assert.All(realInputs.Value.Events, fun e -> Assert.True(abs (Events.identityGap e) <= 0.01))
    let bad = { (List.head realInputs.Value.Events) with Eliminated = 99.0 }
    Assert.True(Result.isError (Events.validate 0.01 bad))

// ------------------------------------------------------------------ invalid assumptions

[<Fact>]
let ``ranges must be ordered and non-negative`` () =
    Assert.True(Result.isError (validateRange "x" false { Low = 2.0; Base = 1.0; High = 3.0 }))
    Assert.True(Result.isError (validateRange "x" false { Low = -1.0; Base = 1.0; High = 3.0 }))
    Assert.True(Result.isOk (validateRange "x" true { Low = -1.0; Base = 1.0; High = 3.0 }))
    Assert.True(Result.isError (validateRange "x" false { Low = nan; Base = 1.0; High = 3.0 }))

[<Fact>]
let ``parameter and stream parsers reject invalid assumptions`` () =
    let badParams = "name,low,base,high,unit,adverse,allow_negative,assumption_ids,basis\nx,3,2,1,u,high,N,P3-ASM-MOD001,b\n" |> Csv.parse |> snd
    Assert.True(Result.isError (Inputs.parseParams badParams))
    let badAdverse = "name,low,base,high,unit,adverse,allow_negative,assumption_ids,basis\nx,1,2,3,u,sideways,N,,b\n" |> Csv.parse |> snd
    Assert.True(Result.isError (Inputs.parseParams badAdverse))
    let streams = "seq_id,stream_id,stream,template,entity,dedicated,kill_exempt,recurring,uses_registry\nS,X,x,,E2,Y,N,Y,N\n" |> Csv.parse |> snd
    let unknownField = "stream_id,field,low,base,high,assumption_ids\nX,no_such_field,1,2,3,\n" |> Csv.parse |> snd
    Assert.True(Result.isError (Inputs.parseStreams streams unknownField))
    let negative = "stream_id,field,low,base,high,assumption_ids\nX,dev_cash,-1,2,3,\n" |> Csv.parse |> snd
    Assert.True(Result.isError (Inputs.parseStreams streams negative))
    let badEntity = "seq_id,stream_id,stream,template,entity,dedicated,kill_exempt,recurring,uses_registry\nS,X,x,,E9,Y,N,Y,N\n" |> Csv.parse |> snd
    Assert.True(Result.isError (Inputs.parseStreams badEntity ("stream_id,field,low,base,high,assumption_ids\n" |> Csv.parse |> snd)))

// ------------------------------------------------------------------ boundary conditions and extremes

[<Fact>]
let ``zero customers: no revenue, no payback, deficit equals total cost`` () =
    let s = { stream with CustomersPerYear = 0.0 }
    let ms = Cashflow.flows globals s None
    let sm = Cashflow.summarize globals ms
    Assert.Equal(None, sm.FirstRevenueMonth)
    Assert.Equal(None, sm.PaybackMonth)
    close 1e-6 (ms |> List.sumBy (fun m -> m.CashCost)) sm.PeakDeficit

[<Fact>]
let ``100 percent partner share leaves the vendor no revenue but all its costs`` () =
    let s = { stream with PartnerShare = 1.0 }
    let ms = Cashflow.flows globals s None
    Assert.All(ms, fun m -> Assert.Equal(0.0, m.VendorRevenue))
    Assert.True((ms |> List.sumBy (fun m -> m.Revenue)) > 0.0)
    Assert.True((ms |> List.sumBy (fun m -> m.Cac)) > 0.0)

[<Fact>]
let ``channel boundaries: no partner deal and full share`` () =
    let b: Channel.Inputs = { RevenuePerSponsor = 60000.0; LifetimeYears = 5.0; PartnerShare = 0.25; DirectCac = 125000.0; Enablement = 30000.0; DealsPerPartnerPerYear = 1.0; AgreementYears = 2.0; DiscountRate = 0.10; SalesCycleMonths = 12.0 }
    let r = Channel.evaluate b
    close 1.0 56862.0 r.MarginTransferredPv
    close 1e-3 0.3667 (Option.get r.BreakEvenShare)
    Assert.Equal(None, (Channel.evaluate { b with DealsPerPartnerPerYear = 0.0 }).PartnerCost)
    close 1e-9 0.0 (Channel.evaluate { b with PartnerShare = 1.0 }).VendorNetRevenuePerYear

[<Fact>]
let ``response: break-even is impossible when net price does not exceed variable cost`` () =
    let cb: Response.CostBase = { Name = "x"; FixedAnnual = 1806415.0; VariablePerAccount = 30.89 }
    Assert.Equal(None, Response.breakEvenAccounts cb 30.0)
    close 1.0 36049.0 (Option.get (Response.breakEvenAccounts cb 81.0))
    let full: Response.Scenario = { Id = "S"; Name = "s"; PriceCut = 0.0; WinRateReduction = 0.0; PartnerShare = 1.0; TerminationMonth = None }
    Assert.Equal(None, (Response.evaluate cb 120.0 1000.0 0.08 full).BreakEvenAccounts)

[<Fact>]
let ``extreme scenarios are worse than base when the kill rule is not applied`` () =
    let i = realInputs.Value
    let m = i.Metas |> List.find (fun x -> x.SeqId = "SEQ-A3")
    let run c = Analysis.runSeq i (Analysis.seqGlobal i c) m c Sequences.FounderFunded (Some None)
    let b, a = run BaseCase, run AdverseCase
    Assert.True(List.last a.Summary.Cumulative < List.last b.Summary.Cumulative)
    let zero = Analysis.extremes i |> List.find (fun x -> x.Name = "zero customers ever")
    let z = Analysis.runExtreme i m zero
    Assert.Equal(None, z.Summary.PaybackMonth)

// ------------------------------------------------------------------ kill rule and entities

[<Fact>]
let ``kill rule: clock starts at the cost-center month; none means never`` () =
    Assert.Equal(None, (Sequences.killDecision None 40.0 None).KillMonth)
    Assert.Equal(Some 6, (Sequences.killDecision (Some 0.0) 7.0 (Some 10)).KillMonth)
    Assert.Equal(None, (Sequences.killDecision (Some 0.0) 6.0 (Some 24)).KillMonth)
    Assert.Equal(Some 24, (Sequences.killDecision (Some 0.0) 6.0 (Some 25)).KillMonth)
    Assert.Equal(None, (Sequences.killDecision (Some 12.0) 18.0 (Some 36)).KillMonth)

[<Fact>]
let ``Transitus is not stopped by the kill rule (OD-P3-02)`` () =
    let trn = { stream with Id = "TRN"; Entity = Cashflow.E5SharedComponents; Dedicated = false; KillExempt = true }
    let unb = { stream with Id = "UNB" }
    let after k (ms: Cashflow.Month list) = ms |> List.filter (fun m -> m.M > k) |> List.sumBy (fun m -> m.CashCost)
    Assert.True(after 6 (Cashflow.flows globals trn (Some 6)) > 0.0)
    Assert.Equal(0.0, after 6 (Cashflow.flows globals unb (Some 6)))

[<Fact>]
let ``shared infrastructure allocation conserves totals under every rule, including no drivers`` () =
    let i = realInputs.Value
    let pools = Analysis.pools i BaseCase
    let total = pools |> List.sumBy (fun p -> p.Annual)
    for rule in [ SharedInfra.Equal; SharedInfra.Usage; SharedInfra.Revenue; SharedInfra.Standalone ] do
        close 1e-6 total (SharedInfra.allocate rule "PRD-UNB" i.Products pools |> List.sumBy (fun a -> a.Amount))
    let noDrivers = i.Products |> List.map (fun p -> { p with Drivers = Map.empty; RevenueBearing = false })
    let al = SharedInfra.allocate SharedInfra.Usage "PRD-UNB" noDrivers pools
    close 1e-6 total (al |> List.filter (fun a -> a.ProductId = "PRD-UNB") |> List.sumBy (fun a -> a.Amount))

[<Fact>]
let ``costs are attributed to the product's entity and entities are not combined without justification`` () =
    let i = realInputs.Value
    let al = SharedInfra.allocate SharedInfra.Usage "PRD-UNB" i.Products (Analysis.pools i BaseCase)
    Assert.All(al |> List.filter (fun a -> a.ProductId = "PRD-TRN"), fun a -> Assert.Equal(Cashflow.E5SharedComponents, a.Entity))
    Assert.True(Result.isError (SharedInfra.combineEntities None [ Cashflow.E2Unbound; Cashflow.E5SharedComponents ] al))
    Assert.True(Result.isOk (SharedInfra.combineEntities (Some "owner-accepted group view") [ Cashflow.E2Unbound; Cashflow.E5SharedComponents ] al))

[<Fact>]
let ``registry cost is not added to Phase II modes (GAP-HI010) and reproduces agent HI's base`` () =
    let i = realInputs.Value
    let m5 = Analysis.registryAtB i Analysis.revision2 BaseCase "M5" 20000.0 1.0
    // agent HI computed from unrounded components; its CSV rounds RCH-14/15/16 to 3-4 digits (difference of a few dollars)
    close 5.0 123888.0 m5.Total
    close 5.0 101787.0 (Analysis.registryAtB i Analysis.revision2 BaseCase "M3" 20000.0 1.0).Total
    Assert.Equal(0.0, Registry.addable Registry.PhaseTwoMode m5)
    Assert.True(Registry.addable (Registry.LeanLicensor 1.0) m5 < Registry.addable (Registry.LeanLicensor 0.0) m5)

// ------------------------------------------------------------------ ports and reproductions

[<Fact>]
let ``Phase II route port reproduces ER-7 base capital and AB's corrections`` () =
    let i = realInputs.Value
    let er7, _ = i.Routes |> List.find (fun (r, _) -> r.Id = "ER-7")
    close 0.01 5660825.0128 (Phase2Check.capital Phase2Check.phaseTwo er7)
    close 5000.0 4670000.0 (Phase2Check.capital { BuildPhaseBurnFactor = 0.4; VariableShare = None } er7)
    close 5000.0 5330000.0 (Phase2Check.capital { BuildPhaseBurnFactor = 1.0; VariableShare = Some 0.15 } er7)

[<Fact>]
let ``minimum viable programme grid reproduces agent CD's evidence rows`` () =
    let m = realInputs.Value.Mvp
    let rows = Licensing.grid m.Fixed m.Variable m.Balances m.Fees
    Assert.Equal(243, rows.Length)
    let first = List.head rows
    Assert.Equal(Some 28, first.BreakEvenAccounts)
    close 1e-6 1400000.0 (Option.get first.BreakEvenAua)
    Assert.Equal(None, (Licensing.breakEven 5000.0 370.0 50000.0 0.006 |> fun (_, n, _) -> n))

// ------------------------------------------------------------------ reproducibility

[<Fact>]
let ``outputs are byte-identical across runs`` () =
    let a = Render.outputs smallInputs.Value
    let b = Render.outputs smallInputs.Value
    Assert.Equal<(string * string) list>(a, b)

[<Fact>]
let ``sampling is deterministic for a seed`` () =
    let vars = [ "a", "demand", HighIsAdverse; "b", "demand", LowIsAdverse; "c", "", HighIsAdverse ]
    Assert.Equal<Map<string, float> list>(Sampling.drawMany 50 7UL 0.5 vars, Sampling.drawMany 50 7UL 0.5 vars)
    // full correlation: a and b take opposite quantiles (both adverse together)
    for d in Sampling.drawMany 50 7UL 1.0 vars do close 1e-12 1.0 (d.["a"] + d.["b"])

// ------------------------------------------------------------------ merge and validation

let header = "claim_id,claim,status,evidence_class,confidence,source_ids,report,notes"

[<Fact>]
let ``merge is deterministic and sorted regardless of fragment order`` () =
    let f1: Registers.Fragment = { Agent = "AB"; File = "claims.csv"; Text = header + "\nP3-CLM-AB002,b,inferred,INFERENCE,Low,,02,\nP3-CLM-AB001,a,inferred,INFERENCE,Low,,02,\n" }
    let f2: Registers.Fragment = { Agent = "CD"; File = "claims.csv"; Text = header + "\nP3-CLM-CD001,\"c, quoted\",confirmed,VERIFIED-FACT,High,,05,\n" }
    let a = Registers.merge [ f1; f2 ]
    let b = Registers.merge [ f2; f1 ]
    match a, b with
    | Ok ra, Ok rb ->
        Assert.Equal<(string * string * int) list>(ra, rb)
        let _, claims, n = ra |> List.find (fun (f, _, _) -> f = "claims.csv")
        Assert.Equal(3, n)
        let ids = Csv.parseRecords claims |> List.tail |> List.map List.head
        Assert.Equal<string list>([ "P3-CLM-AB001"; "P3-CLM-AB002"; "P3-CLM-CD001" ], ids)
        Assert.Equal(Registers.definitions.Length, ra.Length)
        let _, empty, _ = ra |> List.find (fun (f, _, _) -> f = "capital-requirements.csv")
        Assert.Equal(1, Csv.parseRecords empty |> List.length)
    | _ -> failwith "merge failed"

[<Fact>]
let ``merge rejects duplicate ids, header drift and width errors`` () =
    let dup: Registers.Fragment = { Agent = "AB"; File = "claims.csv"; Text = header + "\nP3-CLM-AB001,a,inferred,INFERENCE,Low,,02,\n" }
    Assert.True(Result.isError (Registers.merge [ dup; { dup with Agent = "CD" } ]))
    Assert.True(Result.isError (Registers.merge [ { dup with Text = "claim_id,claim\nP3-CLM-AB001,a\n" } ]))
    Assert.True(Result.isError (Registers.merge [ { dup with Text = header + "\nP3-CLM-AB001,a,inferred\n" } ]))
    Assert.True(Result.isError (Registers.merge [ { dup with File = "stray.csv" } ]))
    Assert.True(Result.isOk (Registers.merge [ { dup with File = "model-anything.csv" } ]))

let emptyRegisters =
    Registers.definitions |> List.map (fun d -> "data/registers/" + d.File, String.concat "," d.Header + "\n")

let fileSet csvs md exists : Validate.FileSet =
    { Csvs = csvs; Markdown = md; Exists = exists; PhaseTwoSources = set [ "SRC-063" ]; ModelOutput = fun _ -> None }

[<Fact>]
let ``validator catches bad ids, vocabularies, unknown references, broken links and decision status`` () =
    let claims = "data/registers/claims.csv", header + "\nCLM-001,a,maybe,INFERENCE,Low,SRC-999,02,\nP3-CLM-ZZ001,b,inferred,GUESS,Low,,02,\n"
    let decisions =
        "data/registers/decisions.csv",
        "decision_id,decision,decision_status,options,recommendation,reversibility,evidence_needed,relates_to,source_ids,report\nP3-DEC-MOD001,d,approved,,,,,,,18\n"
    let csvs = (emptyRegisters |> List.filter (fun (p, _) -> p <> fst claims && p <> fst decisions)) @ [ claims; decisions ]
    let md = [ "14-commercial-sequencing.md", "# 14 - X\n\nStatus: research.\n\nSee P3-CLM-MOD999 and [gone](nowhere.md) and SRC-063.\n" ]
    let r = Validate.validate (fileSet csvs md (fun p -> p = "14-commercial-sequencing.md"))
    let has (s: string) = r.Errors |> List.exists (fun e -> e.Contains s)
    Assert.True(has "lacks prefix")
    Assert.True(has "status='maybe'")
    Assert.True(has "evidence_class='GUESS'")
    Assert.True(has "not P3-<TYPE>-<agent key>")
    Assert.True(has "unknown Phase II source SRC-999")
    Assert.True(has "P3-CLM-MOD999")
    Assert.True(has "broken link nowhere.md")
    Assert.True(has "decision_status='approved'")
    Assert.False(has "SRC-063")
    Assert.Contains("00-executive-summary.md", r.MissingDeliverables)

[<Fact>]
let ``validator accepts a clean package and checks the report header convention`` () =
    let md = Validate.requiredReports |> List.map (fun r -> r, "# " + r.Substring(0, 2) + " - Title\n\nStatus: research (2026-11-26).\n")
    let ok = Validate.validate (fileSet emptyRegisters md (fun _ -> true))
    Assert.Empty(ok.Errors)
    Assert.Empty(ok.MissingDeliverables)
    let bad = ("14-commercial-sequencing.md", "# Fourteen\n") :: (md |> List.filter (fun (p, _) -> p <> "14-commercial-sequencing.md"))
    Assert.NotEmpty((Validate.validate (fileSet emptyRegisters bad (fun _ -> true))).Errors)

[<Fact>]
let ``quoted model tables must match the generated table`` () =
    let lookup n = if n = "tables/x.md" then Some "| a |\n" else None
    let doc = "intro\n<!-- model-output: tables/x.md -->\nold\n<!-- /model-output -->\n"
    Assert.NotEmpty(Quote.check "r.md" lookup doc)
    let filled, missing = Quote.fill lookup doc
    Assert.Empty(missing)
    Assert.Empty(Quote.check "r.md" lookup filled)

// ------------------------------------------------------------------ Revision 2 (adversarial review): one test per fix

let seqMeta : Sequences.SequenceMeta =
    { SeqId = "T"; RegisterId = "P3-SEQ-MOD999"; Label = "T"; Name = "t"; StartState = "S3"; NamedPartnerMonth = point 6.0
      CostCenter = Sequences.Fixed(point 0.0); FailureBand = "high"; Reversibility = ""; Optionality = ""; Dependencies = ""; OpportunityCost = ""; AssumptionIds = [] }

[<Fact>]
let ``fix 1: the referenceable pilot is one whole live Unbound customer, not a fractional go-live`` () =
    let ms = Cashflow.flows globals stream None
    let firstGoLive = ms |> List.find (fun m -> m.GoLive > 0.0)
    Assert.True(firstGoLive.CumGoLive < 1.0)
    let pilot = Sequences.pilotMonth [ stream, ms ]
    Assert.True(pilot.Value > firstGoLive.M)
    Assert.True((ms |> List.find (fun m -> m.M = pilot.Value)).CumGoLive >= 1.0 - 1e-9)
    // a dedicated non-Unbound stream (e.g. a charity-intelligence API) never provides the DAF pilot
    let api = { stream with Entity = Cashflow.E5SharedComponents }
    Assert.Equal(None, Sequences.pilotMonth [ api, Cashflow.flows globals api None ])

[<Fact>]
let ``fix 2: named-partner comparison is explicit and inclusive; the median of the range pauses`` () =
    Assert.True(Sequences.namedInTime 0.0 6.0)
    Assert.False(Sequences.namedInTime 0.0 6.01)
    let median = Analysis.triangularMedian { Low = 3.0; Base = 6.0; High = 12.0 }
    Assert.True(median > 6.0)
    Assert.Equal(Some 6, (Sequences.killDecision (Some 0.0) median (Some 20)).KillMonth)

[<Fact>]
let ``fix 3: contingency is applied on one base that includes the live run`` () =
    let ms = Cashflow.flows globals stream None
    for m in ms do
        close 1e-6 (0.25 * (m.DevCash + m.Onetime + m.Run + m.Registry + m.Cac + m.Impl + m.Reserve)) m.Contingency
    Assert.True(ms |> List.exists (fun m -> m.Run = stream.LiveRunMonthly && m.Contingency > 0.0))
    // first-invoice corrections exclude the founder draw from the contingency base, as the engine does
    let i = realInputs.Value
    let s3 = i.States |> List.find (fun s -> s.StateId = "S3")
    let k = { Capital.asPublished with ContingencyOnFounder = false }
    let a = Capital.firstInvoice (Analysis.capitalGlobals i) BaseCase 222482.0 Capital.asPublished s3
    let b = Capital.firstInvoice (Analysis.capitalGlobals i) BaseCase 222482.0 k s3
    let founderCash = (a.Categories |> List.find (fun c -> c.Category = "founder compensation")).Cash
    close 1e-6 (0.25 * founderCash) (a.Cash - b.Cash)

[<Fact>]
let ``fix 4: variable cost is charged on gross volume and does not fall when the partner share rises`` () =
    let s0 = { stream with VariableShare = 0.2; PartnerShare = 0.0 }
    let s1 = { s0 with PartnerShare = 0.4 }
    let v s = Cashflow.flows globals s None |> List.sumBy (fun m -> m.Variable)
    close 1e-6 (v s0) (v s1)

[<Fact>]
let ``fix 5: registry cost scales with live sponsors`` () =
    let ms = Cashflow.flows globals { stream with CustomersPerYear = 6.0 } None
    let early = ms |> List.find (fun m -> m.Live > 0.0)
    let late = List.last ms
    Assert.True(late.Registry > early.Registry)
    let i = realInputs.Value
    Assert.True(Analysis.registryAddableFor i BaseCase "M5" 10000.0 10.0 > Analysis.registryAddableFor i BaseCase "M5" 10000.0 1.0)

[<Fact>]
let ``fix 6: founder build time inside development at market is not charged twice`` () =
    let econ s = Cashflow.flows globals s None |> List.filter (fun m -> m.DevCash > 0.0) |> List.sumBy (fun m -> m.FounderCash + m.FounderNonCash)
    close 1e-6 (econ stream * 0.3) (econ { stream with FounderBuildShare = 0.7 })

[<Fact>]
let ``fix 7: wind-down at a pause with a signed customer, incident reserve at go-live, tax only above the loss high-water mark`` () =
    let s = { stream with WindDownFixed = 50000.0; WindDownRunMonths = 6.0; IncidentReserve = 25000.0 }
    let paused = Cashflow.flows globals s (Some 30)
    close 1e-6 (50000.0 + 6.0 * s.LiveRunMonthly) (paused |> List.sumBy (fun m -> m.WindDown))
    let noSigning = Cashflow.flows globals s (Some 10)
    Assert.Equal(0.0, noSigning |> List.sumBy (fun m -> m.WindDown))
    close 1e-6 25000.0 (Cashflow.flows globals s None |> List.sumBy (fun m -> m.Reserve))
    let ms = [ for k in 1..Cashflow.horizon -> { (List.head (Cashflow.flows globals s None)) with M = k; Net = (if k <= 10 then -100.0 else 50.0) } ]
    let taxed = Cashflow.applyTax 0.2 ms
    let pre = ms |> List.sumBy (fun m -> m.Net)
    close 1e-6 (0.2 * pre) (taxed |> List.sumBy (fun m -> m.Tax))
    Assert.All(taxed |> List.take 30, fun m -> Assert.Equal(0.0, m.Tax))

[<Fact>]
let ``fix 8: sequences are ranked against an explicit do-nothing baseline`` () =
    let files = Render.outputs smallInputs.Value
    let ranking = files |> List.find (fun (p, _) -> p = "tables/sequences-ranking.md") |> snd
    Assert.Contains("Do nothing", ranking)
    Assert.Contains("Versus do-nothing", ranking)

[<Fact>]
let ``fix 9 and 12: Nacha TPSP obligations and control operations are in the base live run`` () =
    let i = realInputs.Value
    let a3 = i.Streams |> List.find (fun s -> s.StreamId = "A3-UNB")
    let st = Sequences.toStream (Analysis.seqGlobal i BaseCase) (Sequences.casePick BaseCase) a3
    let control = a3.Values.["control_ops_annual"].Base - a3.Values.["control_ops_maintenance_overlap"].Base
    close 1e-6 ((a3.Values.["live_run_annual"].Base + a3.Values.["tpsp_annual"].Base + control) / 12.0) st.LiveRunMonthly
    Assert.True(st.PreRunMonthly > a3.Values.["pre_run_annual"].Base / 12.0)

[<Fact>]
let ``fix 10: the governing registry mode is M1 and M5 is conditional`` () =
    let i = realInputs.Value
    Assert.Equal("M1", (Analysis.registryConfig (Analysis.registryMode i)).Mode)
    Assert.Equal("M5", Analysis.registryModeConditional i)
    Assert.True(Analysis.registryAddableFor i BaseCase "M1" 20000.0 1.0 > Analysis.registryAddableFor i BaseCase "M5" 20000.0 1.0)

[<Fact>]
let ``fix 11: revenue per customer and reachable customers both follow sponsor size`` () =
    let i = realInputs.Value
    let a3 = i.Streams |> List.find (fun s -> s.StreamId = "A3-UNB")
    let gl = Analysis.seqGlobal i BaseCase
    let at a = Sequences.toStream gl (Sequences.casePick BaseCase) (Analysis.sizeOverride a a3)
    let small, big = at 750.0, at 5291.0
    close 1e-6 (750.0 * 81.0) small.RevenuePerCustomer
    Assert.True(big.MaxCustomers < small.MaxCustomers)
    // revision 3 caps on plausible sponsors (excluding processors and presumed own platforms)
    close 1e-9 (floor (Analysis.eligibleIn i "plausible" 5291.0 * 0.4)) big.MaxCustomers
    Assert.Equal(25.0, fst (Analysis.eligible i 5291.0))

[<Fact>]
let ``fix 13: first three customers at the first-conversion rate; sponsor conversion labour is transferred, not cash`` () =
    let s = { stream with ImplFirstCount = 3.0; SponsorConversionPerCustomer = 40000.0; MaxCustomers = 5.0 }
    let ms = Cashflow.flows globals s None
    close 1e-6 (3.0 * 75000.0 + 2.0 * 30000.0) (ms |> List.sumBy (fun m -> m.Impl))
    close 1e-6 (5.0 * 40000.0) (ms |> List.sumBy (fun m -> m.TransferredToSponsor))
    let withoutTransfer = Cashflow.flows globals { s with SponsorConversionPerCustomer = 0.0 } None
    close 1e-6 (withoutTransfer |> List.sumBy (fun m -> m.CashCost)) (ms |> List.sumBy (fun m -> m.CashCost))

[<Fact>]
let ``fix 14: A3 with the S2-to-S3 build carries the build cash whether inside or outside the cost center`` () =
    let i = realInputs.Value
    let run sid = Analysis.runSeq i (Analysis.seqGlobal i BaseCase) (i.Metas |> List.find (fun m -> m.SeqId = sid)) BaseCase Sequences.FounderFunded (Some None)
    let dev (o: Sequences.Outcome) = (List.last o.Horizons).Development
    let a3, inside, outside = run "SEQ-A3", run "SEQ-A3B", run "SEQ-A3X"
    close 1.0 (dev inside) (dev outside)
    Assert.True(dev inside > dev a3 + 400000.0)
    let killed sid = Analysis.runSeq i (Analysis.seqGlobal i BaseCase) (i.Metas |> List.find (fun m -> m.SeqId = sid)) BaseCase Sequences.FounderFunded None
    Assert.Equal(Some 0.0, (killed "SEQ-A3B").Kill.CostCenterMonth)
    Assert.True((killed "SEQ-A3X").Kill.CostCenterMonth.Value >= 9.0)

[<Fact>]
let ``fix 15: four-digit challenge IDs resolve and adversarial challenges are a validated register`` () =
    let chlHeader = "challenge_id,reviewer_perspective,round,target,challenge,severity,evidence,proposed_change,disposition,disposition_rationale,changed_artifacts"
    let chl = "data/registers/adversarial-challenges.csv", chlHeader + "\nP3-CHL-REV1001,CFO,1,14,c,high,e,p,,,\nP3-CHL-REV2002,CFO,1,14,c,severe,e,p,,,\n"
    let csvs = (emptyRegisters |> List.filter (fun (p, _) -> p <> fst chl)) @ [ chl ]
    let md = [ "14-commercial-sequencing.md", "# 14 - X\n\nStatus: research.\n\nResolves P3-CHL-REV1001 and P3-CHL-REV9999.\n" ]
    let r = Validate.validate (fileSet csvs md (fun _ -> true))
    let has (s: string) = r.Errors |> List.exists (fun e -> e.Contains s)
    Assert.False(has "P3-CHL-REV1001")
    Assert.True(has "P3-CHL-REV9999")
    Assert.True(has "severity='severe'")
    let settings = "data/model-inputs/settings.csv", "key,value,assumption_ids,basis\nrequire_dispositions,Y,,\n"
    let r2 = Validate.validate (fileSet (settings :: csvs) md (fun _ -> true))
    Assert.True(r2.Errors |> List.exists (fun e -> e.Contains "has no disposition"))
    Assert.Contains(Registers.definitions, fun d -> d.File = "adversarial-challenges.csv")

[<Fact>]
let ``fix 15b: disposition overlays fill the adversarial register deterministically and reject conflicts`` () =
    let chlHeader = "challenge_id,reviewer_perspective,round,target,challenge,severity,evidence,proposed_change,disposition,disposition_rationale,changed_artifacts"
    let reg: Registers.Fragment = { Agent = "REV1"; File = "adversarial-challenges.csv"; Text = chlHeader + "\nP3-CHL-REV1001,CFO,1,14,c,high,e,p,,,\n" }
    let ovH = "challenge_id,disposition,disposition_rationale,changed_artifacts\n"
    let mod_: Registers.Fragment = { Agent = "MOD"; File = Registers.overlayFile; Text = ovH + "P3-CHL-REV1001,,model changed,Sequences.fs\n" }
    let recon: Registers.Fragment = { Agent = "RECON"; File = Registers.overlayFile; Text = ovH + "P3-CHL-REV1001,accepted,report changed,14\n" }
    match Registers.merge [ reg; recon; mod_ ], Registers.merge [ mod_; reg; recon ] with
    | Ok a, Ok b ->
        Assert.Equal<(string * string * int) list>(a, b)
        let _, t, _ = a |> List.find (fun (f, _, _) -> f = "adversarial-challenges.csv")
        let row = Csv.parseRecords t |> List.item 1
        Assert.Equal("accepted", row.[8])
        Assert.Equal("model changed | report changed", row.[9])
    | _ -> failwith "overlay merge failed"
    let conflict: Registers.Fragment = { mod_ with Text = ovH + "P3-CHL-REV1001,rejected,,\n" }
    Assert.True(Result.isError (Registers.merge [ reg; recon; conflict ]))
    Assert.True(Result.isError (Registers.merge [ reg; { mod_ with Text = ovH + "P3-CHL-REV9999,,x,\n" } ]))

// ------------------------------------------------------------------ Revision 3 (round-2 review): one test per fix

let r3 = { stream with Basis = Cashflow.revision3Basis }

[<Fact>]
let ``r3 fix 1: contingency covers one-time and pre-revenue cash and only the first 12 live months of run`` () =
    let ms = Cashflow.flows globals r3 None
    let firstLive = (ms |> List.find (fun m -> m.GoLive > 0.0)).M
    let late = ms |> List.filter (fun m -> m.M >= firstLive + 12 && m.Signed = 0.0 && m.Onetime = 0.0) |> List.tryHead
    let lateWithSignings = ms |> List.filter (fun m -> m.M >= firstLive + 12)
    for m in lateWithSignings do close 1e-6 (0.25 * (m.DevCash + m.Onetime + m.Cac + m.Impl + m.Reserve)) m.Contingency
    let early = ms |> List.find (fun m -> m.M = firstLive)
    Assert.True(early.Contingency >= 0.25 * (early.Run + early.Registry) - 1e-6)
    Assert.True(late.IsNone || late.Value.Contingency = 0.0)

[<Fact>]
let ``r3 fix 2: wind-down before any go-live is charged at the pre-revenue run`` () =
    let s = { r3 with WindDownFixed = 50000.0; WindDownRunMonths = 6.0; GoLiveLag = 9.0 }
    let firstSign = (Cashflow.flows globals s None |> List.find (fun m -> m.Signed > 0.0)).M
    let paused = Cashflow.flows globals s (Some(firstSign + 1))
    close 1e-6 (50000.0 + 6.0 * s.PreRunMonthly) (paused |> List.sumBy (fun m -> m.WindDown))

[<Fact>]
let ``r3 fix 3: sponsors are classified by platform and the cap excludes processors and presumed own platforms`` () =
    Assert.Equal("processor", Inputs.platformClass "donation_processor" "Ren" "")
    Assert.Equal("third-party platform", Inputs.platformClass "national_standard" "Ren (incl. Stellar/iPhi)" "")
    Assert.Equal("own platform (presumed)", Inputs.platformClass "national_standard" "" "")
    Assert.Equal("third-party platform", Inputs.platformClass "community_foundation" "" "Foundant")
    Assert.Equal("unknown", Inputs.platformClass "community_foundation" "" "Unmapped")
    let i = realInputs.Value
    Assert.True(Analysis.eligibleIn i "plausible" 5291.0 < Analysis.eligibleIn i "all" 5291.0)
    Assert.True(i.Sponsors |> List.filter (fun x -> x.Accounts >= 5291.0 && Analysis.inCapSet i "plausible" x) |> List.forall (fun x -> x.Category <> "donation_processor"))

[<Fact>]
let ``r3 fix 4: the cap limits live customers, so churned customers are replaced`` () =
    let s = { r3 with MaxCustomers = 2.0; Churn = 0.3; CustomersPerYear = 6.0 }
    let ms = Cashflow.flows globals s None
    Assert.True((ms |> List.sumBy (fun m -> m.Signed)) > 2.0)
    Assert.All(ms, fun m -> Assert.True(m.Live <= 2.0 + 1e-9))
    let cumulative = Cashflow.flows globals { s with Basis = Cashflow.revision2Basis } None
    close 1e-9 2.0 (cumulative |> List.sumBy (fun m -> m.Signed))

[<Fact>]
let ``r3 fix 5: the first customer signs whole and the pilot follows the go-live lag`` () =
    let ms = Cashflow.flows globals r3 None
    let first = ms |> List.find (fun m -> m.Signed > 0.0)
    close 1e-12 1.0 first.Signed
    Assert.Equal(Some(first.M + 6), Sequences.pilotMonth [ r3, ms ])
    let rows = Analysis.killTiming realInputs.Value
    Assert.Equal(24, rows.Length)

[<Fact>]
let ``r3 fix 6: deep reviews are demand-driven or tiered, allocated to a performer, and not shared across sponsors`` () =
    let i = realInputs.Value
    let b = Analysis.revision3
    let deep cfg n = (Analysis.registryAtB i b BaseCase cfg 10000.0 n).DeepReview
    close 1e-6 (deep "M1-vendor-2pa" 1.0 * 0.6) (deep "M1-vendor-demand" 1.0)
    close 1e-6 (deep "M1-vendor-demand" 1.0 * 0.4) (deep "M1T-vendor-demand" 1.0)
    close 1e-6 (deep "M1-vendor-demand" 1.0 * 10.0) (deep "M1-vendor-demand" 10.0)
    let vendor = Analysis.registryAddableForB i b BaseCase "M1-vendor-demand" 10000.0 1.0
    let sponsor = Analysis.registryAddableForB i b BaseCase "M1-sponsor" 10000.0 1.0
    close 1e-6 (deep "M1-sponsor" 1.0) (vendor - sponsor)
    close 1e-6 (deep "M1-sponsor" 1.0) (Analysis.registryTransferredB i b BaseCase "M1-sponsor" 10000.0 1.0)
    Assert.Equal(0.0, Analysis.registryTransferredB i b BaseCase "M1-vendor-demand" 10000.0 1.0)

[<Fact>]
let ``r3 fix 7: control operations are net of maintenance code approvers and the adverse TPSP audit is not counted twice`` () =
    let i = realInputs.Value
    let a3 = i.Streams |> List.find (fun s -> s.StreamId = "A3-UNB")
    let live b c = (Sequences.toStream (Analysis.seqGlobalFor i b "M1-vendor-demand" c) (Sequences.casePick c) a3).LiveRunMonthly * 12.0
    close 1e-6 (a3.Values.["control_ops_maintenance_overlap"].Base) (live Analysis.revision2 BaseCase - live Analysis.revision3 BaseCase)
    // the overlap is favourable-high, so the adverse case nets its low end; the TPSP overlap sits at the adverse end
    close 1e-6 (a3.Values.["control_ops_maintenance_overlap"].Low + a3.Values.["tpsp_overlap_in_live_run"].High) (live Analysis.revision2 AdverseCase - live Analysis.revision3 AdverseCase)

[<Fact>]
let ``r3 fix 8 and 9: a partner-book stream exists without a sponsor-population cap and the gate is stated in book accounts`` () =
    let i = realInputs.Value
    let pb = i.Streams |> List.find (fun s -> s.StreamId = "PB-UNB")
    let st = Sequences.toStream (Analysis.seqGlobal i BaseCase) (Sequences.casePick BaseCase) pb
    close 1e-9 3.0 st.MaxCustomers
    close 1e-6 (20000.0 * 81.0) st.RevenuePerCustomer
    let gate = Render.outputs smallInputs.Value |> List.find (fun (p, _) -> p = "tables/gate-break-even.md") |> snd
    Assert.Contains("partner-book", gate)

[<Fact>]
let ``r3 fix 10: both bases are published and revision 2 still reproduces its A3 base`` () =
    let i = realInputs.Value
    let o = Analysis.runFor i Analysis.revision2 "M1-vendor-2pa" "SEQ-A3" (Some None)
    close 5000.0 8700000.0 o.Summary.PeakDeficit
    let bases = Render.outputs smallInputs.Value |> List.find (fun (p, _) -> p = "tables/bases.md") |> snd
    Assert.Contains("Revision 2 (conservative)", bases)
    Assert.Contains("Revision 3 (CFO-corrected)", bases)

[<Fact>]
let ``r3 fix 11: sequence H failure band is high`` () =
    Assert.Equal("high", (realInputs.Value.Metas |> List.find (fun m -> m.SeqId = "SEQ-H")).FailureBand)

[<Fact>]
let ``r3 fix 12: REV4 challenge IDs are valid agent IDs`` () =
    let chlHeader = "challenge_id,reviewer_perspective,round,target,challenge,severity,evidence,proposed_change,disposition,disposition_rationale,changed_artifacts"
    let chl = "data/registers/adversarial-challenges.csv", chlHeader + "\nP3-CHL-REV4001,CFO,2,14,c,high,e,p,,,\n"
    let csvs = (emptyRegisters |> List.filter (fun (p, _) -> p <> fst chl)) @ [ chl ]
    let r = Validate.validate (fileSet csvs [] (fun _ -> true))
    Assert.False(r.Errors |> List.exists (fun e -> e.Contains "REV4001"))
