/// Beneficium (charity intelligence) zero-based economics and charity-vetting alternatives. Pure.
/// Parameters: beneficium-parameters.csv. Separates zero-customer public-dataset upkeep from
/// incremental verification work that scales with active grant recipients.
module ZeroBased.Beneficium

open ZeroBased.Volume

/// Scenarios are cumulative capability tiers.
type Scenario =
    | PublicDirectory
    | WithHistoricalFilings
    | WithGrantRelationships
    | ContinuousMonitoring
    | AutomatedVerification
    | HumanExceptionVerification
    | PaymentEnrolment
    | FullService

let allScenarios =
    [ PublicDirectory; WithHistoricalFilings; WithGrantRelationships; ContinuousMonitoring
      AutomatedVerification; HumanExceptionVerification; PaymentEnrolment; FullService ]

let rank s = allScenarios |> List.findIndex ((=) s)

let name s =
    match s with
    | PublicDirectory -> "Public directory only"
    | WithHistoricalFilings -> "+ historical filings"
    | WithGrantRelationships -> "+ grant relationship intelligence"
    | ContinuousMonitoring -> "+ continuous regulatory monitoring"
    | AutomatedVerification -> "+ automated verification evidence"
    | HumanExceptionVerification -> "+ human exception verification"
    | PaymentEnrolment -> "+ payment enrolment"
    | FullService -> "Full charity intelligence service"

type Cost =
    { Scenario: Scenario
      ActiveRecipients: float
      StorageGb: float
      Infra: float
      ConnectorHours: float
      OpsHours: float
      ExceptionHours: float
      VerificationHours: float
      EnrolmentHours: float
      ExternalFees: float
      Counsel: float
      OwnerFloorHours: float
      Labour: float
      Total: float
      ZeroCustomer: bool }

/// Annual cost of Beneficium at a capability tier with N active grant recipients (union across sponsors).
let cost (bv: Values) (s: Scenario) (n: float) : Cost =
    let r = rank s
    let at x = r >= rank x
    let gb =
        v bv "dir_gb" + (if at WithHistoricalFilings then v bv "history_gb" else 0.0)
        + (if at WithGrantRelationships then v bv "relationships_gb" else 0.0)
    let infra =
        gb * v bv "storage_gb_month" * 12.0 * v bv "backup_and_replica_factor"
        + v bv "cpu_hours_month" * (if at WithHistoricalFilings then v bv "history_cpu_factor" else 1.0) * v bv "cpu_hour_price" * 12.0
        + v bv "db_floor_monthly" * 12.0 * v bv "db_share"
    let connectors =
        v bv "connectors_directory" + (if at WithHistoricalFilings then v bv "connectors_history" else 0.0)
        + (if at WithGrantRelationships then v bv "connectors_relationships" else 0.0)
        + (if at ContinuousMonitoring then v bv "connectors_monitoring" else 0.0)
        + (if at AutomatedVerification then v bv "connectors_verification" else 0.0)
    let connectorHours = connectors * v bv "connector_hours_per_year"
    let opsHours = v bv "pipeline_ops_hours_per_year" + (if at ContinuousMonitoring then v bv "monitoring_ops_hours_per_year" else 0.0)
    // data-quality exceptions in the public dataset (identity conflicts etc.) that block publication
    let dqHours = v bv "dq_exceptions_per_month" * 12.0 * v bv "dq_auto_resolve_miss" * v bv "dq_minutes" / 60.0
    // recipient-driven work
    let changeHours = if at ContinuousMonitoring then n * v bv "eligibility_change_rate" * v bv "change_review_minutes" / 60.0 else 0.0
    let alertHours = if at ContinuousMonitoring then n * v bv "name_match_alert_rate" * v bv "alert_minutes" / 60.0 else 0.0
    let verificationHours =
        if at HumanExceptionVerification then
            n * v bv "new_recipient_share" * v bv "new_recipient_exception_rate" * v bv "exception_minutes" / 60.0
            + n * v bv "evidence_expiry_share" * v bv "expiry_human_share" * v bv "expiry_minutes" / 60.0
        else 0.0
    let enrolmentHours = if at PaymentEnrolment then n * v bv "new_recipient_share" * v bv "enrol_share" * v bv "enrol_minutes" / 60.0 else 0.0
    let fees =
        (if at PaymentEnrolment then n * v bv "new_recipient_share" * v bv "enrol_share" * v bv "bank_verification_fee" else 0.0)
        + (if s = FullService then v bv "commercial_licence" + v bv "support_desk_cost" else 0.0)
    let counsel = v bv "counsel_hours_recurring" * v bv "counsel_rate"
    let floorHours = v bv "owner_floor_hours"
    let engHours = connectorHours + opsHours
    let compHours = dqHours + changeHours + alertHours + verificationHours + enrolmentHours
    let ownerTopUp = max 0.0 (floorHours - compHours)
    let labour = engHours * v bv "engineering_rate" + (compHours + ownerTopUp) * v bv "compliance_rate"
    { Scenario = s
      ActiveRecipients = n
      StorageGb = gb
      Infra = infra
      ConnectorHours = connectorHours
      OpsHours = opsHours
      ExceptionHours = dqHours + changeHours + alertHours
      VerificationHours = verificationHours
      EnrolmentHours = enrolmentHours
      ExternalFees = fees
      Counsel = counsel
      OwnerFloorHours = floorHours
      Labour = labour
      Total = infra + labour + fees + counsel
      ZeroCustomer = (n = 0.0) }

/// Union of recipients across S sponsors each with n recipients (heavy overlap among large recipients).
let union (bv: Values) (perSponsor: float) (sponsors: float) = perSponsor * sponsors ** v bv "union_exponent"

// ------------------------------------------------------------------ vetting alternatives

type Vetting =
    | FullManualPeriodic
    | AutomatedPeriodic
    | Continuous
    | ChangeDriven
    | GrantTriggered
    | RiskTiered
    | Hybrid

let vettingAll = [ FullManualPeriodic; AutomatedPeriodic; Continuous; ChangeDriven; GrantTriggered; RiskTiered; Hybrid ]

let vettingName x =
    match x with
    | FullManualPeriodic -> "Full manual review every 180 days"
    | AutomatedPeriodic -> "Automated re-evaluation every 180 days"
    | Continuous -> "Continuous authoritative monitoring"
    | ChangeDriven -> "Change-driven investigation"
    | GrantTriggered -> "Grant-triggered review (evidence older than 180 days)"
    | RiskTiered -> "Risk-tiered review"
    | Hybrid -> "Hybrid: continuous + 180-day automated re-evaluation + risk-tiered human review"

type VettingResult =
    { Approach: Vetting
      Population: float
      HumanReviews: float
      HumanHours: float
      LabourCost: float
      ExpectedFalseNegatives: float
      FalseNegativeCost: float
      FalsePositiveHolds: float
      FalsePositiveCost: float
      StaleEvidenceShare: float
      Total: float
      Meets180DayValidity: bool }

/// n: charities reviewed (active recipients or whole database); g: grants per year to them.
/// False negatives: grants paid to an organisation that became ineligible and was not yet detected.
/// Exposure window = mean detection latency; P(FN per grant) = ineligibility rate x window/365 x (1 - detection).
let vetting (bv: Values) (approach: Vetting) (n: float) (g: float) : VettingResult =
    let rate = v bv "compliance_rate"
    let inel = v bv "ineligibility_rate"            // eligibility-ending events per charity-year
    let full = v bv "full_review_minutes"
    let latencySrc = v bv "source_latency_days"     // authoritative source publication lag
    let autoEx = v bv "auto_reeval_exception_rate"
    let humanMiss = v bv "human_review_miss_rate"
    let autoMiss = v bv "auto_detection_miss_rate"
    let change = v bv "eligibility_change_rate"
    let cycleAuto = v bv "auto_refresh_days"         // next automated re-check after a missed detection
    let reviews, minutesEach, window, miss, cycle, staleShare, valid180 =
        match approach with
        | FullManualPeriodic -> n * 2.0, full, 90.0 + latencySrc, humanMiss, 180.0, 0.0, true
        | AutomatedPeriodic -> n * 2.0 * autoEx, full, 90.0 + latencySrc, autoMiss, 180.0, 0.0, true
        | Continuous -> n * change, v bv "change_review_minutes", latencySrc, autoMiss, cycleAuto, v bv "stale_source_share", false
        | ChangeDriven -> n * change, full, latencySrc, humanMiss, cycleAuto, v bv "stale_source_share", false
        | GrantTriggered -> min g (n * 2.0) * autoEx, full, 90.0 + latencySrc, autoMiss, 180.0, 0.0, true
        | RiskTiered ->
            let hi, med = v bv "tier_high_share", v bv "tier_med_share"
            n * (hi * 2.0 + med) + n * (1.0 - hi - med) * 2.0 * autoEx, full, 60.0 + latencySrc, (humanMiss + autoMiss) / 2.0, 180.0, 0.0, true
        | Hybrid ->
            n * change + n * 2.0 * autoEx + n * v bv "tier_high_share", full, latencySrc, min autoMiss humanMiss, cycleAuto, 0.0, true
    let hours = reviews * minutesEach / 60.0
    // undetected ineligible time per charity-year: detection latency plus missed detections until the next check
    let pFn = inel * (window + miss * cycle) / 365.0
    let fn = g * pFn
    let fnCost = fn * v bv "false_negative_cost"
    let fpHolds = g * v bv "false_positive_rate" * (match approach with Continuous | ChangeDriven | Hybrid -> 1.0 | _ -> 0.6)
    let fpCost = fpHolds * v bv "false_positive_minutes" / 60.0 * rate
    { Approach = approach
      Population = n
      HumanReviews = reviews
      HumanHours = hours
      LabourCost = hours * rate
      ExpectedFalseNegatives = fn
      FalseNegativeCost = fnCost
      FalsePositiveHolds = fpHolds
      FalsePositiveCost = fpCost
      StaleEvidenceShare = staleShare
      Total = hours * rate + fnCost + fpCost
      Meets180DayValidity = valid180 }
