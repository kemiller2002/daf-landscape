/// Three economic layers: A Echelon Foundry (shared engineering capability), B Unbound (DAF platform),
/// C DAF servicing (the operating company). Pure functions. Shared resources are never free: every view states
/// which layer bears which cost, and the consolidated view counts each cost exactly once.
module CapitalMinimization.Layers

open CapitalMinimization.Design

type LayerCosts =
    { /// Layer A annual cost of shared engineering capability (people time, agent compute, infrastructure, governance).
      EchelonAnnual: float
      /// Share of Layer A consumed by Unbound (allocation key: engineering hours or compute on Unbound work).
      EchelonShareToUnbound: float
      /// Commercial licence for Echelon components paid by Unbound (internal if the owners are common).
      EchelonLicence: float
      /// Layer B one-time build (capitalised) and useful life in years.
      UnboundBuild: float
      UnboundLifeYears: float
      /// Layer B annual maintenance (people and agent time) and platform operations (hosting, monitoring, security).
      UnboundMaintenance: float
      UnboundPlatformOps: float
      /// Layer B external licence revenue from sponsors other than the servicing company (software customers).
      UnboundExternalRevenue: float
      /// Share of Unbound's use attributable to the servicing company (allocation key: accounts or sponsors served).
      ServicingShareOfUnbound: float
      /// Platform cost caused only by the servicing operation (dedicated environments, SOC 1 platform scope).
      ServicingSpecificPlatform: float }

type View =
    /// Servicing bears all of Unbound and Unbound's share of Echelon (no other customer of either).
    | Standalone
    /// Unbound and Echelon exist anyway; servicing bears only the platform cost it causes.
    | Incremental
    /// Unbound's and Echelon's costs are shared by use: servicing bears its allocation share.
    | FullyAllocated

let unboundAnnual (lc: LayerCosts) = lc.UnboundBuild / lc.UnboundLifeYears + lc.UnboundMaintenance + lc.UnboundPlatformOps
let echelonToUnbound (lc: LayerCosts) = lc.EchelonAnnual * lc.EchelonShareToUnbound + lc.EchelonLicence

/// Annual platform charge borne by the servicing layer under a view (economic, not cash).
let platformCharge (view: View) (lc: LayerCosts) =
    match view with
    | Standalone -> unboundAnnual lc + echelonToUnbound lc + lc.ServicingSpecificPlatform
    | Incremental -> lc.ServicingSpecificPlatform
    | FullyAllocated -> (unboundAnnual lc + echelonToUnbound lc) * lc.ServicingShareOfUnbound + lc.ServicingSpecificPlatform

/// Incremental cost of Unbound given Echelon exists: Unbound's own build, maintenance and operations plus the part of
/// Echelon it consumes only if that use displaces other paid Echelon work (opportunity cost) — passed as a flag.
let unboundIncremental (lc: LayerCosts) (echelonCapacityDisplaced: bool) =
    unboundAnnual lc + (if echelonCapacityDisplaced then echelonToUnbound lc else 0.0)

/// Consolidated annual profit of the three layers: every external revenue less every cost counted once.
/// Internal charges (licence fees from C to B, service charges from B to A) cancel and are excluded.
let consolidated (lc: LayerCosts) (servicingRevenue: float) (servicingCostExPlatform: float) =
    servicingRevenue + lc.UnboundExternalRevenue
    - servicingCostExPlatform - unboundAnnual lc - lc.ServicingSpecificPlatform - lc.EchelonAnnual
    // the licence is an internal charge between commonly owned layers and cancels

/// Internal transfer price under cost-plus: the servicing layer's charge marked up (the markup is profit of B,
/// a cost of C, and zero consolidated).
let costPlusTransfer (view: View) (lc: LayerCosts) (markup: float) = platformCharge view lc * (1.0 + markup)

/// Engineering cost a design already carries (engineering-pool people outside their queue share, and contracted
/// engineering): in the standalone view this is Unbound maintenance performed inside the servicing company.
let embeddedEngineering (d: Design) =
    (d.People |> List.filter (fun p -> p.Pool = d.IntegrationPool) |> List.sumBy (fun p -> p.LoadedCost * (1.0 - p.QueueShare)))
    + (d.Contracted |> List.filter (fun (n, _) -> n.Contains "engineering") |> List.sumBy snd)

/// The servicing company alone, when Unbound (Layer B) employs the engineers: engineering people and contracted
/// engineering move to Layer B; integration upkeep is bought from Layer B as fractional engineering capacity.
let servicingOnly (d: Design) =
    { d with
        Name = d.Name + " (engineering in Layer B)"
        People = d.People |> List.filter (fun p -> p.Pool <> d.IntegrationPool)
        Contracted = d.Contracted |> List.filter (fun (n, _) -> not (n.Contains "engineering")) // code approvers are a platform control (ADV2-018)
        Pools = d.Pools |> List.map (fun p -> if p.Name = d.IntegrationPool then { p with Fractional = true } else p) }

/// Annual cost of the servicing layer under a view, from a design evaluation function (design -> total cost).
/// Standalone: the full design (with its engineers) plus Unbound build amortisation, Echelon's Unbound share and any
/// maintenance not already performed by the design's own engineers. Incremental: the servicing-only design plus the
/// platform cost servicing causes. Fully allocated: servicing-only plus its share of Layers A and B.
let servicingCost (view: View) (lc: LayerCosts) (totalOf: Design -> float) (d: Design) =
    match view with
    | Standalone ->
        totalOf d + lc.UnboundBuild / lc.UnboundLifeYears + echelonToUnbound lc + lc.UnboundPlatformOps
        + max 0.0 (lc.UnboundMaintenance - embeddedEngineering d) + lc.ServicingSpecificPlatform
    | Incremental -> totalOf (servicingOnly d) + lc.ServicingSpecificPlatform
    | FullyAllocated -> totalOf (servicingOnly d) + (unboundAnnual lc + echelonToUnbound lc) * lc.ServicingShareOfUnbound + lc.ServicingSpecificPlatform
