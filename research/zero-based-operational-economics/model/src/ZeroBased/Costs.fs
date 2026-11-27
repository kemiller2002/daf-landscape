/// Annual operating cost in three economic views. Pure.
/// View 1 incremental cash: what Echelon spends in cash because Unbound exists.
/// View 2 allocated economic: View 1 + Unbound's measured share of shared Echelon resources + founder time at opportunity cost.
/// View 3 standalone replacement: View 1 + founder workload hours at market cost + full replacement of every shared
/// capability and standalone overhead (leadership beyond activity workload, G&A).
module ZeroBased.Costs

open CompetitiveDisplacement.Inputs
open ZeroBased.Domain
open ZeroBased.Volume
open ZeroBased.Workload

type Ctx = { Cfg: Config; Counts: Counts; VendorOriginatesPayments: bool }

/// Activation rule language: terms joined by '&'. always | never | vendor_controls | standalone |
/// tpsp | config:CFG-1,CFG-2 | sponsors>=N | accounts>=N | grants>=N.
let active (ctx: Ctx) (rule: string) : bool =
    let term (t: string) =
        let t = t.Trim()
        let num (p: string) = System.Double.Parse(t.Substring(p.Length), System.Globalization.CultureInfo.InvariantCulture)
        match t with
        | "" | "always" -> true
        | "never" -> false
        | "vendor_controls" -> ctx.Cfg.VendorRunsControls
        | "not_standalone" -> not ctx.Cfg.Standalone
        | "standalone" -> ctx.Cfg.Standalone
        | "tpsp" -> ctx.VendorOriginatesPayments
        | _ when t.StartsWith "config:" -> t.Substring(7).Split(',') |> Array.exists (fun c -> c.Trim() = ctx.Cfg.Id)
        | _ when t.StartsWith "sponsors>=" -> ctx.Counts.Sponsors >= num "sponsors>="
        | _ when t.StartsWith "accounts>=" -> ctx.Counts.Accounts >= num "accounts>="
        | _ when t.StartsWith "grants>=" -> ctx.Counts.Grants >= num "grants>="
        | other -> failwithf "unknown activation term '%s'" other
    rule.Split('&') |> Array.forall term

type Line = { Id: string; Item: string; Category: string; View: string; Amount: float }

let fixedLines (level: Level) (ctx: Ctx) (fixedCosts: FixedCost list) : Line list =
    fixedCosts
    |> List.filter (fun f -> not f.OneTime && active ctx f.Activation)
    |> List.map (fun f ->
        let amt = pick level f.Annual * (if f.View = "allocated" then f.AllocationShare else 1.0)
        { Id = f.Id; Item = f.Item; Category = f.Category; View = f.View; Amount = amt })

type Views =
    { LabourCash: float
      BackupCash: float
      InfraCash: float
      CharityDataUpkeep: float
      ExternalCash: float
      FixedIncremental: float
      FixedAllocated: float
      FixedStandalone: float
      FounderImputed: float
      SponsorLabourValue: float
      View1: float
      View2: float
      View3: float
      Lines: Line list }

let views (level: Level) (ctx: Ctx) (fixedCosts: FixedCost list) (ls: Load list)
          (labour: float) (backup: float) (founder: float) (infra: float) (charityUpkeep: float) (sponsorRate: float) : Views =
    let lines = fixedLines level ctx fixedCosts
    let sumView vw = lines |> List.filter (fun l -> l.View = vw) |> List.sumBy (fun l -> l.Amount)
    let external = ls |> List.sumBy (fun l -> l.ExternalCost * l.VendorShare)
    let sponsorHours = ls |> List.sumBy (fun l -> (l.Minutes + l.AuthMinutes) * (1.0 - l.VendorShare) / 60.0)
    let inc = sumView "incremental"
    let v1 = labour + backup + infra + charityUpkeep + external + inc
    { LabourCash = labour
      BackupCash = backup
      InfraCash = infra
      CharityDataUpkeep = charityUpkeep
      ExternalCash = external
      FixedIncremental = inc
      FixedAllocated = sumView "allocated"
      FixedStandalone = sumView "standalone"
      FounderImputed = founder
      SponsorLabourValue = sponsorHours * sponsorRate
      View1 = v1
      View2 = v1 + founder + sumView "allocated"
      View3 = v1 + founder + sumView "standalone"
      Lines = lines }

/// One-time investment lines (development, establishment) with their view.
let oneTime (level: Level) (fixedCosts: FixedCost list) =
    fixedCosts |> List.filter (fun f -> f.OneTime) |> List.map (fun f -> f.Id, f.Item, f.View, pick level f.Annual)
