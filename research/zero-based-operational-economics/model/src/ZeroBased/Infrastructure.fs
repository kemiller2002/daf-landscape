/// Resource-based infrastructure cost: provisioned floor plus metered consumption. Pure.
/// Prices and consumption coefficients come from infrastructure-parameters.csv (published prices / assumptions).
module ZeroBased.Infrastructure

open ZeroBased.Volume

/// C1 minimal shared single-region HA; C2 adds a warm DR region; C3 adds isolated databases for large sponsors.
type Deployment =
    | C1
    | C2
    | C3

type InfraCost =
    { Deployment: Deployment
      FloorAnnual: float
      ComputeScaleAnnual: float
      StorageAnnual: float
      LoggingAnnual: float
      MessagingAnnual: float
      AiAnnual: float
      IdentityAnnual: float
      ScanningAnnual: float
      EgressAnnual: float
      NonProdAnnual: float
      IsolationAnnual: float
      Total: float
      StoredGb: float
      PeakVcpu: float }

/// Annual new structured data (GB): journal lines and documents/evidence.
let annualDataGb (iv: Values) (c: Counts) =
    let lines =
        c.Grants * v iv "lines_per_grant" + c.Contributions * v iv "lines_per_contribution"
        + c.Accounts * 12.0 * v iv "lines_per_account_month"
    let eventBytes = c.Accounts * v iv "durable_events_per_acct" * v iv "bytes_per_event"
    let masterBytes = c.Accounts * v iv "master_kb_per_acct" * 1000.0
    let dbGb = (lines * v iv "bytes_per_journal_line" + eventBytes + masterBytes) * v iv "index_overhead" / 1e9
    let objGb =
        (c.Accounts * v iv "docs_per_acct" * v iv "kb_per_doc" + c.Grants * v iv "kb_evidence_per_grant") / 1e6
    dbGb, objGb

/// AI-assisted exceptions are passed in (from the workload) so AI cost follows actual exception volume.
/// Durable events (commands, outbox, ledger postings) drive compute and logs; they are counted per account-year
/// (infrastructure-consumption INF-DB-002), not per operational activity.
let cost (iv: Values) (dep: Deployment) (c: Counts) (_activityEvents: float) (aiExceptions: float) (isolatedSponsors: float) : InfraCost =
    let m = 12.0
    let events = c.Accounts * v iv "durable_events_per_acct"
    let floorMonthly =
        v iv "app_instance_monthly" * v iv "app_instances_min" + v iv "db_base_monthly" + v iv "platform_fixed_monthly"
    let drFactor = match dep with C1 -> 0.0 | C2 | C3 -> v iv "dr_multiplier"
    let floor = floorMonthly * m * (1.0 + drFactor)
    // compute scale-up: peak-hour events against per-vCPU throughput beyond the base tier
    let peakHourEvents = events * v iv "peak_hour_share"
    let vcpu = peakHourEvents / v iv "events_per_vcpu_hour"
    let extraVcpu = max 0.0 (vcpu - v iv "db_base_vcpu")
    let computeScale = extraVcpu * (v iv "db_vcpu_monthly" + v iv "app_vcpu_monthly") * m * (1.0 + drFactor)
    // storage at steady state: retention years of data
    let dbGbYr, objGbYr = annualDataGb iv c
    let years = v iv "retention_years"
    let dbGb, objGb = dbGbYr * years, objGbYr * years
    let storage =
        (dbGb * v iv "db_storage_gb_month" * (1.0 + drFactor) + dbGb * v iv "backup_multiplier" * v iv "backup_gb_month"
         + objGb * v iv "object_gb_month" * (1.0 + drFactor)) * m
    let logging = events / 1000.0 * v iv "log_gb_per_1k_events" * v iv "log_gb_price"
    let messaging = c.Accounts * v iv "emails_per_acct" / 1000.0 * v iv "email_per_1k"
    let ai =
        aiExceptions * (v iv "ai_in_tokens_per_exception" * v iv "ai_input_per_mtok"
                        + v iv "ai_out_tokens_per_exception" * v iv "ai_output_per_mtok") / 1e6
    let mau = c.Accounts * v iv "mau_share"
    let identity = max 0.0 (mau - v iv "identity_free_mau") * v iv "identity_mau_price" * m + c.Accounts * v iv "sms_per_acct" * v iv "sms_price"
    let scanning = (c.Grants * v iv "files_per_grant" + c.Contributions * v iv "files_per_contribution") * v iv "scan_per_file"
    let egress = c.Accounts * v iv "egress_gb_per_acct" * v iv "egress_gb_price"
    let isolation = match dep with C3 -> isolatedSponsors * v iv "isolated_db_monthly" * m | _ -> 0.0
    let prodVariable = computeScale + storage + logging
    let nonprod = (floorMonthly * m + prodVariable * 0.1) * v iv "nonprod_share"
    let total = floor + computeScale + storage + logging + messaging + ai + identity + scanning + egress + nonprod + isolation
    { Deployment = dep
      FloorAnnual = floor
      ComputeScaleAnnual = computeScale
      StorageAnnual = storage
      LoggingAnnual = logging
      MessagingAnnual = messaging
      AiAnnual = ai
      IdentityAnnual = identity
      ScanningAnnual = scanning
      EgressAnnual = egress
      NonProdAnnual = nonprod
      IsolationAnnual = isolation
      Total = total
      StoredGb = dbGb + objGb
      PeakVcpu = vcpu }
