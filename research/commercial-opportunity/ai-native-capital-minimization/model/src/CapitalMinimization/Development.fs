/// Development cost under AI-assisted productivity. Pure functions.
/// A productivity multiple accelerates only the share of effort that is construction (writing and changing code
/// and tests). Requirements decisions, human review, independent security testing, bank/custodian certification,
/// migration rehearsals and assurance do not scale with code-generation speed (an Amdahl's-law bound).
module CapitalMinimization.Development

type DevBaseline =
    { Name: string
      /// Conventional cost of the full scope (e.g. Unbound's $5M base) in dollars.
      ConventionalFullScope: float
      /// Share of the full scope needed for a minimum servicing product that is safe with live money.
      MinimumScopeShare: float
      /// Share of conventional effort that is construction and accelerates with the productivity multiple.
      ConstructionShare: float
      /// Fixed, non-scalable cost for a safe launch: independent penetration test, SOC readiness, bank and custodian
      /// certification, migration rehearsal, accessibility audit, legal review of payment flows.
      SafetyFloor: float
      /// Agent compute as a share of the human construction cost it replaces.
      ComputeShareOfReplaced: float }

/// Effective cost of a scope share at a productivity multiple (>= 1).
let effectiveCost (b: DevBaseline) (scopeShare: float) (multiple: float) =
    let conv = b.ConventionalFullScope * scopeShare
    let construction = conv * b.ConstructionShare
    let replaced = construction - construction / multiple
    conv * (1.0 - b.ConstructionShare) + construction / multiple + replaced * b.ComputeShareOfReplaced

/// The largest bound on savings: cost ratio as multiple -> infinity.
let savingsCeiling (b: DevBaseline) = 1.0 - ((1.0 - b.ConstructionShare) + b.ConstructionShare * b.ComputeShareOfReplaced)

/// Total cost of the minimum safe product at a multiple, including the non-scalable safety floor.
let minimumProductCost (b: DevBaseline) (multiple: float) = effectiveCost b b.MinimumScopeShare multiple + b.SafetyFloor

/// Share of the full scope an investment can deliver at a multiple after paying the safety floor (0 if the floor
/// is not covered; the product is then not safe to operate with live money).
let deliverableScope (b: DevBaseline) (investment: float) (multiple: float) =
    let available = investment - b.SafetyFloor
    if available <= 0.0 then 0.0
    else min 1.0 (available / effectiveCost b 1.0 multiple)

/// Whether an investment covers the minimum safe product at a multiple.
let safeToOperate (b: DevBaseline) (investment: float) (multiple: float) = investment >= minimumProductCost b multiple

/// Annual maintenance as a share of cumulative build (conventional rule of thumb, scaled the same way).
let annualMaintenance (b: DevBaseline) (maintenanceShare: float) (scopeShare: float) (multiple: float) =
    effectiveCost b scopeShare multiple * maintenanceShare
