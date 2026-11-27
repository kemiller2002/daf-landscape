module ZeroBasedEconomics.Tests.Tests

open System.IO
open Xunit
open ZeroBasedEconomics
open ZeroBasedEconomics.Domain
open ZeroBasedEconomics.Inputs
open ZeroBasedEconomics.Engine

// ------------------------------------------------------------------------------------------------ fixtures

let r lo b hi = { Low = lo; Base = b; High = hi }

let expense id metric threshold driver amount ef =
    { Id = id; Name = id; Purpose = "p"; Category = "c"; Class = Conditional; Obligation = Operational; Entity = "E1"
      EvidenceIds = [ "SRC-1" ]; TriggerMetric = metric; TriggerThreshold = threshold; Driver = driver; MinAnnual = point 0.0
      Amount = point amount; IncrementalShare = point 1.0; AllocationShare = point 0.0; CapacityLimit = "c"; Alternative = "a"
      Consequence = "x"; Prepaid = false; EfModels = set ef; SponsorModels = Set.empty }

let activity id driver rate share minutes role ef sp =
    { Id = id; Name = id; Why = "w"; LegallyRequired = "N"; ContractuallyRequired = "N"; Preventable = "N"; Deterministic = "N"
      AiAssist = "N"; HumanDecision = "none"; Driver = driver; Rate = point rate; HumanShare = point share; Minutes = point minutes
      ConventionalMinutes = 0.0; Role = role; EfModels = set ef; SponsorModels = set sp; EvidenceIds = [ "SRC-1" ]
      StaffingNote = "n"; MinCustomers = 0 }

let role id loaded hourly founder =
    { Id = id; Name = id; Purpose = "p"; EvidenceIds = [ "SRC-1" ]; LoadedAnnual = point loaded; ContractHourly = point hourly
      FounderEligible = founder; ProductiveHours = 1600.0; HireThresholdHours = 800.0; Qualification = "q"; Alternative = "a"
      Consequence = "c" }

let profile = { Id = "P"; Name = "P"; Accounts = r 50.0 100.0 200.0; AuaPerAccount = point 100000.0; GrantsPerAccount = r 5.0 10.0 20.0
                ContribsPerAccount = point 2.0; ExceptionRate = r 0.5 1.0 2.0; EvidenceIds = [ "SRC-1" ] }

let parameters =
    [ "founder_hours_per_year", 1000.0; "founder_fixed_hours", 0.0; "founder_hours_per_customer", 0.0
      "founder_hours_per_new_customer", 0.0; "founder_imputed_rate", 100.0; "sponsor_staff_rate", 50.0; "new_customer_share", 0.3
      "months_to_first_revenue", 12.0; "qualification_amortization_years", 5.0; "lic_platform_fee", 10000.0; "lic_per_account", 10.0
      "wl_platform_fee", 5000.0; "wl_per_account", 5.0; "tops_per_account", 10.0; "admin_bps_ref", 20.0; "ci_subscription", 1000.0
      "mig_fee_base", 10000.0; "mig_fee_per_account", 2.0; "employee_overhead", 0.0; "contractor_counts_hours", 400.0
      "customers_added_per_year", 1.0; "go_live_lead_months", 6.0 ]
    @ (allModels |> List.map (fun m -> "collection_lag_months_" + modelCode m, 1.0))
    |> List.map (fun (k, v) -> k, point v)
    |> Map.ofList

let baseInputs =
    { Expenses = []
      Activities = []
      Roles = [ role "management" 200000.0 150.0 true; role "engineering" 160000.0 100.0 true ]
      Coverage = []
      Profiles = [ profile ]
      Mixes = [ { Id = "mixed"; Name = "m"; Pattern = [ "P" ] }; { Id = "prior-5x2000"; Name = "p"; Pattern = [ "P" ] } ]
      Params = parameters
      Qualification = []
      Priors = []
      Sources = [ { Id = "SRC-1"; Title = "t"; Location = "l"; EvidenceClass = "INFERENCE" } ] }

let sc n = { Customers = n; MixId = "mixed"; Factors = baseFactors; Tier = 1 }

// ------------------------------------------------------------------------------------------------ volumes

[<Fact>]
let ``mix patterns cycle deterministically`` () =
    let mix = { Id = "x"; Name = "x"; Pattern = [ "A"; "B"; "C" ] }
    Assert.Equal<string list>([ "A"; "B"; "C"; "A"; "B" ], assign mix 5)

[<Fact>]
let ``factors vary dimensions independently`` () =
    let v f = customerVolume f profile
    let b = v baseFactors
    let hiExc = v { baseFactors with Exc = High }
    Assert.Equal(b.Accounts, hiExc.Accounts)
    Assert.Equal(b.Grants, hiExc.Grants)
    Assert.Equal(2.0 * b.Exceptions, hiExc.Exceptions, 6)
    let hiTxn = v { baseFactors with Txn = High }
    Assert.Equal(b.Accounts, hiTxn.Accounts)
    Assert.Equal(2.0 * b.Grants, hiTxn.Grants, 6)
    Assert.Equal(81, allFactors.Length)

[<Fact>]
let ``exception-driven activities scale with exception intensity, not only volume`` () =
    let a = activity "A" PerGrantException 1.0 0.1 60.0 "engineering" [ L ] []
    let v f = volume baseInputs L { sc 1 with Factors = f }
    Assert.Equal(2.0 * activityHours (v baseFactors) a, activityHours (v { baseFactors with Exc = High }) a, 6)

[<Fact>]
let ``activities gated by a customer minimum vanish at zero customers`` () =
    let a = { activity "A" FixedYear 1.0 1.0 600.0 "engineering" [ L ] [] with MinCustomers = 1 }
    Assert.Equal(0.0, activityHours (volume baseInputs L (sc 0)) a)
    Assert.Equal(10.0, activityHours (volume baseInputs L (sc 1)) a, 6)

// ------------------------------------------------------------------------------------------------ expenses

[<Fact>]
let ``expenses trigger at their threshold and scale by driver`` () =
    let inp =
        { baseInputs with
            Expenses =
                [ expense "FIX" Always 0.0 Fixed 1000.0 [ L ]
                  expense "CUST" Customers 2.0 Fixed 500.0 [ L ]
                  expense "PER" Customers 1.0 (Per Accounts) 2.0 [ L ]
                  expense "STEP" Always 0.0 (Step(Accounts, 150.0)) 300.0 [ L ] ] }
    let cash n = (evaluate inp L (sc n)).EfNonLaborCash
    Assert.Equal(1000.0 + 300.0, cash 0, 6)
    Assert.Equal(1000.0 + 200.0 + 300.0, cash 1, 6) // 100 accounts x $2; one step
    Assert.Equal(1000.0 + 500.0 + 400.0 + 600.0, cash 2, 6) // 200 accounts: two steps

[<Fact>]
let ``sponsor-borne expenses never enter Echelon Foundry cost`` () =
    let e = { expense "SP" Customers 1.0 (Per Accounts) 1.0 [] with SponsorModels = set [ L ] }
    let o = evaluate { baseInputs with Expenses = [ e ] } L (sc 1)
    Assert.Equal(0.0, o.EfCash)
    Assert.Equal(100.0, o.SponsorCost, 6)

[<Fact>]
let ``shared expenses split incremental cash from fully loaded allocation`` () =
    let e = { expense "SH" Always 0.0 Fixed 1000.0 [ L ] with Class = Shared; IncrementalShare = point 0.2; AllocationShare = point 0.5 }
    let o = evaluate { baseInputs with Expenses = [ e ] } L (sc 0)
    Assert.Equal(200.0, o.EfNonLaborCash, 6)
    Assert.Equal(500.0, o.EfNonLaborAllocated, 6)

[<Fact>]
let ``contract tiers separate mandatory obligations from contractual expectations`` () =
    let e = { expense "SOC" Customers 1.0 Fixed 1000.0 [ L ] with Obligation = ContractTypical }
    let inp = { baseInputs with Expenses = [ e ] }
    Assert.Equal(0.0, (evaluate inp L { sc 1 with Tier = 0 }).EfCash)
    Assert.Equal(1000.0, (evaluate inp L { sc 1 with Tier = 1 }).EfCash, 6)

// ------------------------------------------------------------------------------------------------ staffing

[<Fact>]
let ``founder absorbs work first, then contracts, then employs`` () =
    let eng = role "engineering" 160000.0 100.0 true
    let a = staffRole 100.0 0.0 eng 900.0 1000.0 0
    Assert.Equal(900.0, a.FounderHours)
    Assert.Equal(0.0, a.Cash)
    let b = staffRole 100.0 0.0 eng 1500.0 1000.0 0 // 500 h residual: contracted
    Assert.Equal(0, b.Employees)
    Assert.Equal(50000.0, b.Cash, 6)
    let c = staffRole 100.0 0.0 eng 2900.0 1000.0 0 // 1900 h residual: 1 FTE + 300 h contracted
    Assert.Equal(1, c.Employees)
    Assert.Equal(300.0, c.ContractHours, 6)
    let d = staffRole 100.0 0.0 eng 3900.0 1000.0 0 // 2900 h: 1 FTE + 1300 h remainder above threshold -> 2 FTE
    Assert.Equal(2, d.Employees)
    Assert.Equal(0.0, d.ContractHours)

[<Fact>]
let ``a role the founder cannot hold is never absorbed by the founder`` () =
    let o = staffRole 100.0 0.0 (role "x" 100000.0 50.0 false) 100.0 1000.0 0
    Assert.Equal(0.0, o.FounderHours)
    Assert.Equal(5000.0, o.Cash, 6)

[<Fact>]
let ``coverage picks the cheaper of hiring and retainer and meets every requirement`` () =
    let cov id minP alt =
        { Id = id; Description = id; Basis = "b"; Obligation = Operational; Models = set [ L ]; TriggerCustomers = 1; MinPeople = minP
          Role = "engineering"; AltAllowed = true; AltDescription = "a"; AltAnnual = point alt; EvidenceIds = [ "SRC-1" ] }
    // the founder works 100 h of engineering, so counts as one engineering person
    let work = activity "W" FixedYear 1.0 1.0 6000.0 "engineering" [ L ] []
    let inp = { baseInputs with Activities = [ work ]; Coverage = [ cov "CHG" 3 20000.0; cov "ONC" 2 30000.0 ] }
    let o = evaluate inp L (sc 1)
    // founder counts as one: CHG short 2 (2 x 20k), ONC short 1 (30k): 70k of retainers < hiring 160k+
    Assert.Equal(0, o.Employees)
    Assert.Equal(70000.0, o.LaborCash, 6)
    Assert.Equal(2, o.Coverage.Length)
    // with costly retainers the optimum mixes: one hire ($160k) meets ONC and half of CHG; one CHG retainer remains
    // (k=0: 450k; k=1: 160k + 150k = 310k; k=2: 320k)
    let costly = { inp with Coverage = [ cov "CHG" 3 150000.0; cov "ONC" 2 150000.0 ] }
    let o2 = evaluate costly L (sc 1)
    Assert.Equal(1, o2.Employees)
    Assert.Equal(310000.0, o2.LaborCash, 6)

[<Fact>]
let ``coverage without a permitted alternative forces a hire`` () =
    let c = { Id = "C"; Description = "c"; Basis = "b"; Obligation = Operational; Models = set [ F ]; TriggerCustomers = 1; MinPeople = 2
              Role = "engineering"; AltAllowed = false; AltDescription = "-"; AltAnnual = point 1.0; EvidenceIds = [ "SRC-1" ] }
    // the founder works no engineering hours, so does not count: both people are hires
    let o = evaluate { baseInputs with Coverage = [ c ] } F (sc 1)
    Assert.Equal(2, o.Employees)

[<Fact>]
let ``sponsor activities never create Echelon Foundry hours`` () =
    let a = activity "S" PerGrant 1.0 1.0 10.0 "engineering" [] [ L ]
    let o = evaluate { baseInputs with Activities = [ a ] } L (sc 1)
    Assert.Equal(0.0, o.FounderHours)
    Assert.True(o.SponsorHours > 0.0)

[<Fact>]
let ``the founder counts for coverage only in a role the founder works`` () =
    let c = { Id = "OPS"; Description = "c"; Basis = "b"; Obligation = Operational; Models = set [ F ]; TriggerCustomers = 1; MinPeople = 2
              Role = "engineering"; AltAllowed = true; AltDescription = "a"; AltAnnual = point 10000.0; EvidenceIds = [ "SRC-1" ] }
    let idle = evaluate { baseInputs with Coverage = [ c ] } F (sc 1)
    Assert.Equal(20000.0, idle.LaborCash, 6) // founder has no engineering hours: two retainers
    let busy = evaluate { baseInputs with Coverage = [ c ]; Activities = [ activity "W" FixedYear 1.0 1.0 600.0 "engineering" [ F ] [] ] } F (sc 1)
    Assert.Equal(10000.0, busy.LaborCash, 6)

[<Fact>]
let ``a regular contractor counts as a distinct person`` () =
    let c = { Id = "ONC"; Description = "c"; Basis = "b"; Obligation = Operational; Models = set [ L ]; TriggerCustomers = 1; MinPeople = 2
              Role = "engineering"; AltAllowed = true; AltDescription = "a"; AltAnnual = point 10000.0; EvidenceIds = [ "SRC-1" ] }
    // 1,500 h of engineering: founder 1,000 h, contractor 500 h (>= 400): two people, no retainer
    let o = evaluate { baseInputs with Coverage = [ c ]; Activities = [ activity "W" FixedYear 1.0 1.0 90000.0 "engineering" [ L ] [] ] } L (sc 1)
    Assert.Empty(o.Coverage)

[<Fact>]
let ``employees forced by coverage absorb work before the founder`` () =
    let eng = role "engineering" 160000.0 100.0 true
    let o = staffRole 100.0 0.0 eng 1000.0 1000.0 1
    Assert.Equal(1, o.Employees)
    Assert.Equal(0.0, o.FounderHours)

[<Fact>]
let ``run-rate onboarding is the expected value, not one customer every year`` () =
    Assert.Equal(0.3, newCustomers baseInputs L 1, 6)
    Assert.Equal(3.0, newCustomers baseInputs L 10, 6)
    Assert.Equal(4.0, newCustomers baseInputs M 4, 6)

[<Fact>]
let ``persistent break-even ignores a temporary crossing`` () =
    let ok n = n = 2 || n >= 5
    Assert.Equal(Some 5, Analysis.persistentFrom 10 ok)
    Assert.Equal(None, Analysis.persistentFrom 10 (fun n -> n < 9))

// ------------------------------------------------------------------------------------------------ revenue and analysis

[<Fact>]
let ``full-service revenue is basis points of assets`` () =
    let v = volume baseInputs F (sc 1) // 100 accounts x $100k = $10M
    Assert.Equal(20000.0, revenueAt baseInputs F 20.0 v, 6)

[<Fact>]
let ``oriented levels put favourable and adverse ends together`` () =
    Assert.Equal(1900.0, atOriented Low "PAR:founder_hours_per_year" (r 900.0 1400.0 1900.0))
    Assert.Equal(900.0, atOriented High "PAR:founder_hours_per_year" (r 900.0 1400.0 1900.0))
    Assert.Equal(10.0, atOriented Low "EXP:X:amount" (r 10.0 20.0 30.0))
    Assert.Equal(30.0, atOriented High "EXP:X:amount" (r 10.0 20.0 30.0))

[<Fact>]
let ``sampling is deterministic and triangular draws stay in range`` () =
    let a = Sampling.quantileDraws 50 7UL 0.5 (fun _ -> false) [ "a"; "b" ]
    let b = Sampling.quantileDraws 50 7UL 0.5 (fun _ -> false) [ "a"; "b" ]
    Assert.Equal<Map<string, float> list>(a, b)
    let xs = a |> List.map (fun q -> Sampling.triangular (r 1.0 2.0 5.0) q.["a"])
    Assert.True(xs |> List.forall (fun x -> x >= 1.0 && x <= 5.0))

// ------------------------------------------------------------------------------------------------ validation gates

[<Fact>]
let ``validation rejects a role with no workload and no coverage`` () =
    let inp = { baseInputs with Roles = baseInputs.Roles @ [ role "chief-of-staff" 150000.0 100.0 false ] }
    let issues = Validate.gRoles inp
    Assert.Contains(issues, fun i -> i.Gate = "V6" && i.Subject = "chief-of-staff")

[<Fact>]
let ``validation rejects a sponsor-reserved decision borne by Echelon Foundry`` () =
    let a = { activity "D" PerGrant 1.0 1.0 1.0 "engineering" [ F ] [] with HumanDecision = "sponsor" }
    Assert.Contains(Validate.gActivity a, fun i -> i.Gate = "V4")

[<Fact>]
let ``validation rejects a required human control modelled to zero`` () =
    let a = { activity "C" PerGrant 1.0 0.0 1.0 "engineering" [] [ L ] with LegallyRequired = "Y"; HumanDecision = "sponsor"; HumanShare = r 0.0 0.1 0.2 }
    Assert.Contains(Validate.gControls a, fun i -> i.Gate = "V5")

[<Fact>]
let ``validation requires every expense attribute`` () =
    let e = { expense "E" Always 0.0 Fixed 1.0 [ L ] with Alternative = ""; Entity = "E9" }
    let issues = Validate.gExpenseFields e |> List.map (fun i -> i.Message)
    Assert.Contains("missing or invalid alternative approach", issues)
    Assert.Contains(issues, fun m -> m.Contains "accountable entity")

// ------------------------------------------------------------------------------------------------ package

let packageRoot =
    let rec up (d: DirectoryInfo) =
        if isNull d then failwith "package root not found"
        elif File.Exists(Path.Combine(d.FullName, "data", "inputs", "expenses.csv")) then d.FullName
        else up d.Parent
    up (DirectoryInfo(System.AppContext.BaseDirectory))

[<Fact>]
let ``the published inputs parse, validate and reproduce the published outputs`` () =
    match Program.readInputs (Path.Combine(packageRoot, "data", "inputs")) with
    | Error e -> failwith e
    | Ok inp ->
        Assert.Empty(Validate.all inp [] (fun _ _ -> true))
        let outputs = Render.all inp
        for (name, text) in outputs do
            Assert.Equal(File.ReadAllText(Path.Combine(packageRoot, "data", "outputs", name)), text)
