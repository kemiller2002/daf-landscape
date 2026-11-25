/// Parameter sets for the outcome-designed organizations, layer costs and development baselines.
/// Labels: [S] sourced (cost IDs refer to servicing-economics/data/cost-register.csv), [A] assumption,
/// [D] derived, [E] estimate. Nothing here is a measurement of a running company.
module CapitalMinimization.Designs

open CapitalMinimization.Design
open CapitalMinimization.Layers
open CapitalMinimization.Development

// ---------------------------------------------------------------- loaded rates (CST-R*, role-compensation.csv) [S/D]

let founderLoaded = 200142.0      // CST-R01
let founderCash = 116255.0        // Model A below-market cash salary [A]
let ctoLoaded = 222482.0          // CST-R02
let ctoCash = 127440.0            // Model A below-market cash salary [A]
let engineerLoaded = 188958.0     // CST-R03
let controllerLoaded = 183365.0   // CST-R06
let accountantLoaded = 110662.0   // CST-R07
let opsLoaded = 99478.0           // CST-R09
let complianceLoaded = 121848.0   // CST-R10
let serviceLoaded = 77108.0       // CST-R13
let hours = 1520.0                // productive hours per FTE-year (previous study) [A]

// ---------------------------------------------------------------- skill pools

/// Shares of servicing hours by skill: operations (grants, contributions, exceptions) 0.62, accounting
/// (reconciliation, close, adjustments) 0.20, compliance (charity and sanctions exceptions, fraud review) 0.08,
/// donor/advisor service 0.10. [A] from the ACT activity families; no time study exists.
let pools fractional =
    [ { Name = "operations"; Share = 0.62; LoadedHourly = opsLoaded / hours; ContractPremium = 0.5; MinimumFte = 0.0; Fractional = fractional }
      { Name = "accounting"; Share = 0.20; LoadedHourly = accountantLoaded / hours; ContractPremium = 0.5; MinimumFte = 0.0; Fractional = fractional }
      // A named compliance owner from go-live: at least 0.25 FTE regardless of workload (OPS staffing-capacity). [A]
      { Name = "compliance"; Share = 0.08; LoadedHourly = complianceLoaded / hours; ContractPremium = 0.5; MinimumFte = 0.25; Fractional = fractional }
      { Name = "service"; Share = 0.10; LoadedHourly = serviceLoaded / hours; ContractPremium = 0.5; MinimumFte = 0.0; Fractional = fractional }
      { Name = "engineering"; Share = 0.0; LoadedHourly = engineerLoaded / hours; ContractPremium = 0.5; MinimumFte = 0.0; Fractional = fractional } ]

// ---------------------------------------------------------------- non-personnel bundles (cost-register.csv) [S/A]

/// Assurance and security for a company that touches charitable money: these do not shrink with headcount.
let assurance =
    [ "CST-C09 audit of company financial statements", 35000.0
      "CST-C10 corporate tax returns", 10000.0
      "CST-C11 SOC 2 Type 2", 35000.0
      "CST-C12 SOC 1 Type 2", 40000.0
      "CST-C14 penetration test + retest", 20000.0
      "CST-C15 compliance automation platform", 20000.0
      "CST-C18 DR test + BCP tabletop", 10000.0 ]

let insurance =
    [ "CST-I02 cyber $5M", 30000.0
      "CST-I03 tech E&O $5M", 25000.0
      "CST-I04 D&O", 10000.0
      "CST-I05 commercial crime incl. client funds", 12000.0
      "CST-I06 EPLI", 4000.0
      "CST-I07 GL/umbrella", 3000.0 ]

let specialists =
    [ "CST-C03 fractional vCISO", 48000.0
      "CST-C04 compliance consultant (sanctions, due diligence, independent review)", 25000.0
      "CST-C16 incident response retainer", 7500.0
      "CST-C06 outside counsel 100 h", 45000.0
      "CST-C02 outsourced bookkeeping (company books)", 24000.0
      "CST-C01 fractional CFO review 40 h", 8000.0 ]

let platformAndData =
    [ "CST-T01/T02/T05/T07/T08 cloud, DR replica, monitoring", 35564.0
      "CST-T14 AI evaluation, red-team, development usage", 12000.0
      "CST-D03/D04 Candid charity data", 7750.0
      "CST-D05 sanctions/PEP screening", 8000.0
      "CST-ID1 identity verification", 3000.0
      "CST-PY8/PY6 bank treasury services, print-mail", 6720.0
      "CST-CM4/CM5 e-signature, document generation", 5000.0 ]

let salesAndGa =
    [ "CST-SM1 conferences, travel, events", 40000.0
      "CST-SM2 marketing, website, content", 20000.0
      "CST-S08 CRM", 2000.0
      "CST-G01/G02/G03/S06 filings, bank fees, meeting space, company accounting software", 13200.0 ]

/// Agent compute for operations and continuous development beyond CST-T14 (no measured figure exists). [A]
let agentCompute = [ "agent compute: operations and continuous development [A]", 36000.0 ]

let withContingency (items: (string * float) list) =
    items @ [ "contingency 7.5% (CST-G04)", 0.075 * (items |> List.sumBy snd) ]

/// Per-person overhead: seats, equipment, PEO, training, security tooling, travel, helpdesk (CST-S01..S05, P17-P21,
/// T11, TR1, S07): about $11.1k per person-year. [D]
let perPerson = 11100.0

// ---------------------------------------------------------------- organizations by size

let private person title loaded cash pool share money = { Title = title; LoadedCost = loaded; CashCost = cash; Pool = pool; QueueShare = share; StartMonth = 0; MoneyAuthority = money }

let private design name people fractional contracted reviewer sponsorApprover =
    { Name = name
      People = people
      Pools = pools fractional
      Contracted = contracted
      NonPersonnel = withContingency (assurance @ insurance @ specialists @ platformAndData @ salesAndGa @ agentCompute)
      PerPersonOverhead = perPerson
      // Previous study: 19,440 sponsor-level minutes per sponsor-year AI-native (ACT S01-S05). [D from A]
      SponsorMinutes = 19440.0
      // Relationship, change requests and quarterly reviews per sponsor-year. [A]
      RelationshipHours = 60.0
      // Integration upkeep for the first sponsor 300 h a year (previous step costs imply ~315 h of engineer and
      // analyst time per sponsor); 0.85 per doubling as reusable connectors mature. [A]
      IntegrationFirstSponsorHours = 300.0
      IntegrationLearningRate = 0.85
      IntegrationPool = "engineering"
      // Coordination: 0.5 h per pair of people per week (meetings, handoffs, status). [A] (0.25-1.5)
      CoordinationHoursPerPairWeek = 0.5
      ProductiveHours = hours
      Utilisation = 0.9
      DecemberShare = 0.10
      // December excess is bought at +50%: prep-only temporary staff cannot release payments, so the excess falls to
      // overtime and pre-contracted releasers (OPS workload-tails; previous report 03). [A]
      PeakPremium = 0.5
      SponsorApprover = sponsorApprover
      ContractedIndependentReviewer = reviewer }

/// Contracted engineering capacity for designs without an employed engineer: an on-call contractor retainer
/// (CST-C05 base $30k) plus 400 h a year at the engineer rate with the 50% contract premium. [A]
let contractEngineering = [ "CST-C05 engineering retainer + 400 h contracted engineering", 30000.0 + 400.0 * engineerLoaded / hours * 1.5 ]

/// Control-relevant code needs an author and two approvers who are not the author (OPS; CNV-PLT-010): designs with
/// fewer than three engineering people contract the missing approvers at $45k a year each (about 240 h at the
/// engineer contract rate). [A]
let codeReviewers n = [ $"contracted independent code approvers x{n} (CNV-PLT-010 two-approver rule)", 45000.0 * float n ]

/// Fractional controller acting as independent reviewer of reconciliations and payment releases: 200 h at
/// CST-C01 $200/h. [A]
let independentReviewer = [ "independent fractional controller review 200 h (CST-C01)", 40000.0 ]

let f1 =
    design "F1 one founder + agents + contractors"
        [ person "Founder (operations, sponsor relationships, governance)" founderLoaded founderCash "operations" 0.4 true ]
        true (contractEngineering @ independentReviewer @ codeReviewers 2) true true

let f2 =
    design "F2 two founders"
        [ person "Founder (operations, finance, sponsor relationships)" founderLoaded founderCash "operations" 0.35 true
          person "Technical founder (platform, security; no bank access)" ctoLoaded ctoCash "engineering" 0.3 false ]
        true (independentReviewer @ codeReviewers 2) true true

let f3 =
    design "F3 three core"
        [ person "Founder / managing director" founderLoaded founderCash "operations" 0.15 true
          person "CTO (platform, security; no bank access)" ctoLoaded ctoCash "engineering" 0.25 false
          person "Controller / head of financial operations" controllerLoaded controllerLoaded "accounting" 0.6 true ]
        true (independentReviewer @ codeReviewers 2) true false

let f5 =
    design "F5 five core"
        [ person "Founder / managing director" founderLoaded founderLoaded "operations" 0.1 true
          person "CTO" ctoLoaded ctoLoaded "engineering" 0.2 false
          person "Senior software engineer" engineerLoaded engineerLoaded "engineering" 0.3 false
          person "Controller" controllerLoaded controllerLoaded "accounting" 0.5 true
          person "Grant & client operations specialist" opsLoaded opsLoaded "operations" 0.85 true ]
        false (codeReviewers 1) false false

let f6 =
    design "F6 six core"
        [ person "Founder / managing director" founderLoaded founderLoaded "operations" 0.1 true
          person "CTO" ctoLoaded ctoLoaded "engineering" 0.2 false
          person "Senior software engineer" engineerLoaded engineerLoaded "engineering" 0.3 false
          person "Controller" controllerLoaded controllerLoaded "accounting" 0.5 true
          person "Grant & client operations specialist" opsLoaded opsLoaded "operations" 0.85 true
          person "Compliance and donor service specialist" complianceLoaded complianceLoaded "compliance" 0.8 true ]
        false (codeReviewers 1) false false

let f8 =
    design "F8+ nine core (specialised)"
        [ person "Founder / managing director" founderLoaded founderLoaded "operations" 0.05 true
          person "CTO" ctoLoaded ctoLoaded "engineering" 0.1 false
          person "Senior software engineer" engineerLoaded engineerLoaded "engineering" 0.3 false
          person "Senior software engineer" engineerLoaded engineerLoaded "engineering" 0.3 false
          person "Controller" controllerLoaded controllerLoaded "accounting" 0.4 true
          person "Fund / grant accountant" accountantLoaded accountantLoaded "accounting" 0.85 false
          person "Grant & client operations specialist" opsLoaded opsLoaded "operations" 0.85 true
          person "Grant & client operations specialist" opsLoaded opsLoaded "operations" 0.85 true
          person "Compliance officer" complianceLoaded complianceLoaded "compliance" 0.7 false ]
        false [] false false

let designs = [ f1; f2; f3; f5; f6; f8 ]

/// Outcome-designed variant (OPS pass): sponsor-level minutes 19,440 -> 12,720 a year by generated reporting and
/// continuous reconciliation; coordination gain about 1.25 h per person-week (3% of capacity) by a shared case/event
/// model; account minutes fall to about 30 (applied through the handling target). Unproven: no observed operation. [A]
let outcomeDesignedTarget = 30.1
let outcomeDesigned (d: Design) =
    { d with
        Name = d.Name + " | outcome-designed (OPS: sponsor work 12,720 min, +3% capacity) [unproven]"
        SponsorMinutes = 12720.0
        ProductiveHours = d.ProductiveHours * 1.03 }

/// Narrow-entry design: non-custodial software service (no money movement): no SOC 1, no crime cover, smaller
/// compliance scope. [A]
let narrowEntryNonPersonnel =
    withContingency (
        (assurance |> List.filter (fun (n, _) -> not (n.StartsWith "CST-C12")))
        @ (insurance |> List.filter (fun (n, _) -> not (n.StartsWith "CST-I05")))
        @ (specialists |> List.filter (fun (n, _) -> not (n.StartsWith "CST-C04")))
        @ platformAndData @ salesAndGa @ agentCompute)

// ---------------------------------------------------------------- handling-time targets

let handlingTargets = [ 10.0; 20.0; 30.0; 50.0; 75.0; 100.0 ]

// ---------------------------------------------------------------- development baselines [A]

/// Unbound's $5M base build (simplification model parameters) as the conventional full scope. Minimum safe servicing
/// scope 35% of it [A]; construction 45% of conventional effort [A: requirements, design, review, testing
/// strategy, certification, migration and assurance make up the rest]; agent compute 10% of the human construction
/// cost it replaces [A]; safety floor $220k (pen test $20k, SOC readiness $20k, accessibility audit $15k,
/// bank/custodian certification and payment-flow legal review $65k, migration rehearsal tooling $40k, independent
/// code/security review $60k) [A from CST lines].
let unboundBaseline =
    { Name = "Unbound $5M conventional scope"
      ConventionalFullScope = 5.0e6
      MinimumScopeShare = 0.35
      ConstructionShare = 0.45
      SafetyFloor = 220000.0
      ComputeShareOfReplaced = 0.10 }

let investmentScenarios = [ 100000.0; 250000.0; 500000.0; 1.0e6; 1.8e6; 5.0e6 ]
let productivityMultiples = [ 1.0; 1.5; 2.0; 3.0; 5.0; 10.0 ]

// ---------------------------------------------------------------- layer costs [A]

/// Base layer costs. Echelon annual $150k is an assumption standing in for the owner's shared engineering
/// capability (no ledger of Echelon cost exists in the repositories); 30% consumed by Unbound. Unbound minimum safe
/// build from the development model at 2x productivity (about $1.6M) over 5 years; maintenance $200k a year (one engineer-equivalent with agents) [A]; non-production and CI
/// environments $24k (production hosting is already in the servicing design's platform line); servicing-specific
/// platform (SOC 1 platform scope, sponsor sandboxes beyond the per-sponsor $12k) $30k. [A]
let baseLayers =
    { EchelonAnnual = 150000.0
      EchelonShareToUnbound = 0.3
      UnboundBuild = minimumProductCost unboundBaseline 2.0
      UnboundLifeYears = 5.0
      UnboundMaintenance = 200000.0
      UnboundPlatformOps = 24000.0
      UnboundExternalRevenue = 0.0
      ServicingShareOfUnbound = 1.0
      ServicingSpecificPlatform = 30000.0 }

/// Conservative layer costs from the LYR pass (layer-costs.csv): build $4.6M amortised over 5 years ($920k), a platform
/// team of technical lead plus three engineers ($789k), production and non-production hosting $60k, and Echelon
/// reliance cost caused by Unbound (second maintainer, component security review, licence programme, licensor
/// insurance, maintainer time) about $300k with 90% attributable to Unbound. [A, LYR]
let lyrLayers =
    { EchelonAnnual = 300000.0
      EchelonShareToUnbound = 0.9
      UnboundBuild = 4.6e6
      UnboundLifeYears = 5.0
      UnboundMaintenance = 222482.0 + 566874.0
      UnboundPlatformOps = 59731.0
      UnboundExternalRevenue = 0.0
      ServicingShareOfUnbound = 1.0
      ServicingSpecificPlatform = 60000.0 }
