#!/usr/bin/env python3
"""Charity-network and onboarding economic model (agent ECO, 2026-11-26).

Functional style: pure functions over immutable data; I/O only in main().
Deterministic. Python 3 stdlib only.

Usage:
  python3 scripts/economic_model.py            # recompute and write data/economic-scenarios-output.csv
  python3 scripts/economic_model.py --check    # recompute and diff against the existing output (exit 1 on drift)
  python3 scripts/economic_model.py --report   # print markdown result tables to stdout

Every input is read from data/economic-parameters.csv (low/base/high).
Conventions:
  * cost_case selects the low/base/high column for cost parameters; for 'benefit' parameters
    (higher = cheaper, e.g. partner_coverage) the column is mirrored.
  * data_quality (clean/typical/poor) selects low/base/high for migration-quality parameters only.
  * grants_case and balance_case select the grants_per_account and balance_<size> columns.
"""
from __future__ import annotations

import csv
import io
import math
import sys
from pathlib import Path
from typing import Callable, Dict, Iterable, Mapping, NamedTuple, Tuple

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
PARAMS_PATH = PKG / "data" / "economic-parameters.csv"
OUTPUT_PATH = PKG / "data" / "economic-scenarios-output.csv"

PARAM_HEADER = ("parameter", "low", "base", "high", "unit", "evidence_class",
                "source_ids_or_internal_path", "notes")
OUTPUT_HEADER = ("record_type", "scenario_id", "accounts", "grants_case", "data_quality",
                 "balance_case", "fee_bps", "cost_case", "history_case", "metric", "value")

CASES = ("low", "base", "high")
QUALITY_TO_CASE = {"clean": "low", "typical": "base", "poor": "high"}
SIZES = (1_000, 10_000, 100_000, 1_000_000)
SIZE_BALANCE_PARAM = {1_000: "balance_s1k", 10_000: "balance_s10k",
                      100_000: "balance_s100k", 1_000_000: "balance_s1m"}
FEES_BPS = (10, 15, 20, 30)
WORKING_FEE_BPS = 20
NETWORK_SIZES = (10_000, 50_000, 200_000, 600_000)
HISTORY_CASES = ("short", "mid", "full")
HISTORY_PARAM = {"short": "history_years_short", "mid": "history_years_mid", "full": "history_years_full"}
DEFAULT_HISTORY = "full"
PRICE_ANCHORS_PER_ACCOUNT = (100, 400)  # USD/account-yr: near cost floor; near Ren/MS GIFT low band (A-ADV-001)

# Parameters where a higher value is favourable (cheaper): mirrored under cost_case.
BENEFIT_PARAMS = frozenset({"partner_coverage", "enroll_instant_share", "registry_reuse_mature",
                            "check_share_target", "sales_cycle_months_saved"})
# Parameters driven by the data-quality dimension rather than cost_case.
QUALITY_PARAMS = frozenset({"mig_account_exception_rate", "mig_txn_exception_rate",
                            "n_custom_integrations", "parallel_cycles", "recon_break_rate"})
# Parameters driven by scenario dimensions (never by cost_case).
DIMENSION_PARAMS = frozenset({"grants_per_account", *SIZE_BALANCE_PARAM.values()})
# Parameters fixed at base for classification policy.
POLICY_PARAMS = frozenset({"term_months", "include_payback_months"})

MIRROR = {"low": "high", "base": "base", "high": "low"}


class Param(NamedTuple):
    name: str
    low: float
    base: float
    high: float
    unit: str
    evidence_class: str
    source: str
    notes: str

    def pick(self, case: str) -> float:
        return {"low": self.low, "base": self.base, "high": self.high}[case]


class Scenario(NamedTuple):
    accounts: int
    grants_case: str
    data_quality: str
    balance_case: str
    fee_bps: int
    cost_case: str
    history: str = DEFAULT_HISTORY

    @property
    def scenario_id(self) -> str:
        return (f"N{self.accounts}-G{self.grants_case}-Q{self.data_quality}"
                f"-B{self.balance_case}-F{self.fee_bps}-C{self.cost_case}-H{self.history}")


Values = Mapping[str, float]


# ---------------------------------------------------------------- parameter resolution (pure)

def parse_params(rows: Iterable[Mapping[str, str]]) -> Tuple[Param, ...]:
    return tuple(Param(r["parameter"], float(r["low"]), float(r["base"]), float(r["high"]),
                       r["unit"], r["evidence_class"], r["source_ids_or_internal_path"], r["notes"])
                 for r in rows)


def resolve(params: Tuple[Param, ...], sc: Scenario) -> Dict[str, float]:
    """Pick one value per parameter for a scenario."""
    def choose(p: Param) -> float:
        if p.name in QUALITY_PARAMS:
            return p.pick(QUALITY_TO_CASE[sc.data_quality])
        if p.name == "grants_per_account":
            return p.pick(sc.grants_case)
        if p.name in SIZE_BALANCE_PARAM.values():
            return p.pick(sc.balance_case)
        if p.name in POLICY_PARAMS:
            return p.base
        if p.name in BENEFIT_PARAMS:
            return p.pick(MIRROR[sc.cost_case])
        return p.pick(sc.cost_case)
    return {p.name: choose(p) for p in params}


def resolve_cost_case(params: Tuple[Param, ...], cost_case: str) -> Dict[str, float]:
    v = resolve(params, Scenario(1_000, "base", "typical", "base", WORKING_FEE_BPS, cost_case))
    v["history_years"] = v[HISTORY_PARAM[DEFAULT_HISTORY]]
    return v


# ---------------------------------------------------------------- unit costs (pure)

def hours_cost(minutes: float, rate: float) -> float:
    return minutes / 60.0 * rate


def exception_cost(v: Values) -> float:
    return hours_cost(v["exception_minutes"], v["rate_ops"]) + v["ai_dossier_cost"]


def verification_cost_per_new_charity(v: Values) -> float:
    return v["auto_check_cost_per_charity"] + v["p_first_exception"] * exception_cost(v)


def monitoring_cost_per_charity_year(v: Values) -> float:
    return v["auto_check_cost_per_charity"] * 12 + v["status_event_rate"] * exception_cost(v)


def enrollment_cost_per_charity(v: Values) -> float:
    instant = v["enroll_instant_share"] * v["instant_verify_fee"]
    manual = (1 - v["enroll_instant_share"]) * (
        v["microdeposit_cost"] + hours_cost(v["bank_letter_minutes"], v["rate_ops"]))
    return instant + manual + hours_cost(v["outreach_minutes"], v["rate_ops"])


def bank_change_cost_per_enrolled_year(v: Values) -> float:
    return v["bank_change_rate"] * (v["instant_verify_fee"] * v["enroll_instant_share"]
                                    + (1 - v["enroll_instant_share"]) * hours_cost(v["bank_letter_minutes"], v["rate_ops"]))


def ach_rail_cost(v: Values) -> float:
    """Third-party/bank cost per ACH grant (sponsor pass-through under CNV-PAY-001)."""
    return v["ach_fee"] + v["ach_return_rate"] * v["ach_return_fee"]


def check_rail_cost(v: Values) -> float:
    """Third-party cost per check grant incl. reissue of uncashed checks (sponsor pass-through)."""
    return v["check_print_mail"] * (1 + v["uncashed_rate"])


def ach_labour_cost(v: Values) -> float:
    return hours_cost(v["ach_labour_minutes"] + v["ach_return_rate"] * v["ach_return_minutes"], v["rate_ops"])


def check_labour_cost(v: Values) -> float:
    return hours_cost(v["check_labour_minutes"] + v["uncashed_rate"] * v["uncashed_minutes"], v["rate_ops"])


def screening_cost_per_grant(v: Values) -> float:
    return (v["ai_screen_per_grant"] + hours_cost(v["status_check_minutes"], v["rate_ops"])
            + v["grant_exception_rate"] * exception_cost(v))


def unbound_cost_per_grant(v: Values, check_share: float) -> float:
    """Unbound-borne cost per grant: screening + exception share + payment-operations labour."""
    return (screening_cost_per_grant(v) + check_share * check_labour_cost(v)
            + (1 - check_share) * ach_labour_cost(v))


def passthrough_rail_cost_per_grant(v: Values, check_share: float) -> float:
    return check_share * check_rail_cost(v) + (1 - check_share) * ach_rail_cost(v)


def unit_cost_table(v: Values) -> Dict[str, float]:
    return {
        "cost_per_exception": exception_cost(v),
        "verification_cost_per_new_charity": verification_cost_per_new_charity(v),
        "monitoring_cost_per_charity_year": monitoring_cost_per_charity_year(v),
        "epay_enrollment_cost_per_charity": enrollment_cost_per_charity(v),
        "bank_change_reverification_per_enrolled_year": bank_change_cost_per_enrolled_year(v),
        "ach_rail_cost_per_grant_passthrough": ach_rail_cost(v),
        "check_rail_cost_per_grant_passthrough": check_rail_cost(v),
        "ach_labour_cost_per_grant": ach_labour_cost(v),
        "check_labour_cost_per_grant": check_labour_cost(v),
        "screening_cost_per_grant": screening_cost_per_grant(v),
        "unbound_cost_per_grant_at_initial_check_share": unbound_cost_per_grant(v, v["check_share_initial"]),
        "unbound_cost_per_grant_at_target_check_share": unbound_cost_per_grant(v, v["check_share_target"]),
        "allin_cost_per_grant_at_initial_check_share": unbound_cost_per_grant(v, v["check_share_initial"])
            + passthrough_rail_cost_per_grant(v, v["check_share_initial"]),
        "allin_cost_per_grant_at_target_check_share": unbound_cost_per_grant(v, v["check_share_target"])
            + passthrough_rail_cost_per_grant(v, v["check_share_target"]),
        "check_minus_ach_allin_per_grant": (check_rail_cost(v) + check_labour_cost(v))
            - (ach_rail_cost(v) + ach_labour_cost(v)),
    }


# ---------------------------------------------------------------- Track A platform (pure)

def registry_establishment_cost(v: Values) -> Dict[str, float]:
    hours = (v["fed_connector_h"] + v["n_state_registries"] * v["state_connector_h"]
             + v["entity_resolution_h"] + v["registry_ops_tooling_h"])
    eng = hours * v["rate_eng"]
    total = eng + v["state_data_one_time"] + v["backfill_compute_one_time"]
    return {"establish_engineering_hours": hours, "establish_engineering_usd": eng,
            "establish_state_data_usd": v["state_data_one_time"],
            "establish_backfill_compute_usd": v["backfill_compute_one_time"],
            "establish_total_usd": total}


def registry_annual_cost(v: Values) -> Dict[str, float]:
    storage = (v["object_storage_gb"] * v["object_storage_usd_gb_month"] * 12
               + v["registry_db_gb"] * v["db_storage_usd_gb_month"] * 12)
    infra = storage + v["registry_db_instance_annual"] + v["ingestion_compute_annual"]
    data = v["state_data_annual"] + v["sanctions_vendor_annual"]
    maint = v["connector_maint_h"] * v["rate_eng"]
    return {"annual_storage_usd": storage, "annual_infra_total_usd": infra,
            "annual_third_party_data_usd": data, "annual_connector_maintenance_usd": maint,
            "annual_fixed_total_usd": infra + data + maint}


def network_growth_cost(v: Values, charities_in_use: int) -> Dict[str, float]:
    """Variable cost of a network of charities actually receiving grants (not all 1.9M BMF rows)."""
    new = charities_in_use * v["new_recipient_share"]
    monitoring = charities_in_use * monitoring_cost_per_charity_year(v)
    verification = new * verification_cost_per_new_charity(v)
    enrolled = charities_in_use * (1 - v["partner_coverage"]) * v["enroll_target_share"]
    enrol_new = new * (1 - v["partner_coverage"]) * v["enroll_target_share"] * enrollment_cost_per_charity(v)
    bank = enrolled * bank_change_cost_per_enrolled_year(v)
    return {"charities_in_use": float(charities_in_use), "annual_monitoring_usd": monitoring,
            "annual_new_charity_verification_usd": verification,
            "annual_new_enrolment_usd": enrol_new, "annual_bank_change_usd": bank,
            "annual_network_variable_usd": monitoring + verification + enrol_new + bank,
            "one_time_enrol_existing_usd": enrolled * enrollment_cost_per_charity(v)}


# ---------------------------------------------------------------- sponsor scenario (pure)

def decade_scale(accounts: int, per_decade: float) -> float:
    return 1 + math.log10(accounts / 1000) * per_decade


def grants_per_recipient(v: Values, accounts: int) -> float:
    return min(13.2, max(2.5, 2.5 * (accounts / 1000) ** v["gpr_exponent"]))


def recurring_economics(v: Values, sc: Scenario) -> Dict[str, float]:
    n = sc.accounts
    balance = v[SIZE_BALANCE_PARAM[n]]
    aua = n * balance
    grants = n * v["grants_per_account"]
    recipients = grants / grants_per_recipient(v, n)
    revenue = aua * sc.fee_bps / 10_000
    account_based = n * v["per_account_usd"]
    txn_grants = grants * unbound_cost_per_grant(v, v["check_share_initial"])
    recipient_driven = (recipients * monitoring_cost_per_charity_year(v)
                        + recipients * v["new_recipient_share"] * verification_cost_per_new_charity(v))
    transaction_based = txn_grants + recipient_driven
    sponsor_fixed = (v["sponsor_recurring_h"] * decade_scale(n, v["sponsor_scale_per_decade"]) * v["rate_ops"]
                     + v["n_custom_integrations"] * v["custom_integ_maint_h"] * v["rate_eng"])
    cost = account_based + transaction_based + sponsor_fixed
    contribution = revenue - cost
    passthrough = (grants * passthrough_rail_cost_per_grant(v, v["check_share_initial"])
                   + v["positive_pay_monthly"] * 12)
    return {"avg_balance": balance, "aua": aua, "grants_per_year": grants, "recipients": recipients,
            "revenue": revenue, "cost_account_based": account_based,
            "cost_transaction_based": transaction_based, "cost_sponsor_fixed": sponsor_fixed,
            "cost_recurring_total": cost, "contribution": contribution,
            "contribution_margin": contribution / revenue if revenue else 0.0,
            "cost_per_account": cost / n, "cost_per_grant_unbound": cost / grants,
            "sponsor_passthrough_rail_cost": passthrough}


def onboarding_economics(v: Values, sc: Scenario, recipients: float) -> Dict[str, float]:
    n = sc.accounts
    scale = decade_scale(n, v["sponsor_scale_per_decade"])
    impl = v["impl_h"] * scale * v["rate_impl"]
    eng_config = v["eng_config_h"] * v["rate_eng"]
    integ_std = v["n_std_integrations"] * v["std_integ_h"] * v["rate_eng"]
    integ_custom = v["n_custom_integrations"] * v["custom_integ_h"] * v["rate_eng"]
    eng_hours = (v["eng_config_h"] + v["n_std_integrations"] * v["std_integ_h"]
                 + v["n_custom_integrations"] * v["custom_integ_h"])
    per_account = n * (v["mig_auto_per_account"] + v["mig_account_exception_rate"]
                       * hours_cost(v["mig_account_exception_minutes"], v["rate_ops"]))
    txns = n * (v["grants_per_account"] + v["contribs_per_account"]) * effective_history_years(v)
    per_txn = txns * (v["mig_auto_per_txn"] + v["mig_txn_exception_rate"]
                      * hours_cost(v["mig_txn_exception_minutes"], v["rate_ops"]))
    recon = (v["parallel_cycles"] * v["recon_cycle_h"] * scale * v["rate_ops"]
             + n * v["recon_break_rate"] * hours_cost(v["recon_break_minutes"], v["rate_ops"]))
    donor = n * (v["donor_contact_share"] * hours_cost(v["donor_contact_minutes"], v["rate_ops"])
                 + v["reproof_share"] * v["idv_fee"])
    direct_enrol = recipients * (1 - v["partner_coverage"]) * v["enroll_target_share"]
    enrol = direct_enrol * enrollment_cost_per_charity(v)
    third = v["third_party_onboarding"]
    rehearsal = v["rehearsal_runs"] * v["rehearsal_h"] * scale * v["rate_ops"]
    legal = v["unbound_legal_per_sponsor"]
    direct = (impl + eng_config + integ_std + integ_custom + per_account + per_txn + recon + donor
              + enrol + third + rehearsal + legal)
    reserve = direct * v["failure_reserve_share"]
    total = direct + reserve
    ttp_weeks = (v["ttp_base_weeks"] + v["n_custom_integrations"] * v["ttp_weeks_per_custom"]
                 + v["rehearsal_runs"] * v["rehearsal_weeks"]
                 + v["parallel_cycles"] * 4.35 + 2 * math.log10(n / 1000))
    sponsor_h = (v["sponsor_project_fte"] * scale * 1600 * ttp_weeks / 52
                 + v["rehearsal_runs"] * v["sponsor_rehearsal_approval_h"]
                 + n * v["mig_account_exception_rate"] * v["sponsor_cleanup_minutes"] / 60
                 + v["n_custom_integrations"] * v["sponsor_it_h_per_custom"])
    sponsor_staff = sponsor_h * v["rate_sponsor"]
    consultant = v["sponsor_consultant"] * min(1.0, 0.25 + 0.75 * math.log10(n / 1000))
    buyer_tco = (sponsor_staff + consultant + v["incumbent_tail_fee"] + v["sponsor_auditor_uplift"]
                 + v["sponsor_legal"] + v["sponsor_comms_fixed"])
    return {"onb_implementation": impl, "onb_engineering_config": eng_config,
            "onb_integration_standard": integ_std, "onb_integration_custom": integ_custom,
            "onb_engineering_hours": eng_hours, "onb_per_account_migration": per_account,
            "onb_migrated_transactions": txns, "onb_per_transaction_migration": per_txn,
            "onb_reconciliation": recon, "onb_donor_reonboarding": donor,
            "onb_charity_enrolment": enrol, "onb_direct_enrolments": direct_enrol,
            "onb_third_party": third, "onb_rehearsals": rehearsal, "onb_unbound_legal": legal,
            "onb_failure_reserve": reserve, "onb_total_unbound": total,
            "onb_per_account": total / n, "onb_per_migrated_txn": total / txns,
            "cac_per_sponsor": v["cac_per_sponsor"],
            "acquisition_and_onboarding_total": total + v["cac_per_sponsor"],
            "onb_sponsor_hours": sponsor_h, "onb_sponsor_cost": sponsor_staff,
            "buyer_consultant": consultant, "buyer_incumbent_tail_fee": v["incumbent_tail_fee"],
            "buyer_auditor_uplift": v["sponsor_auditor_uplift"], "buyer_legal": v["sponsor_legal"],
            "buyer_comms": v["sponsor_comms_fixed"], "buyer_switching_tco": buyer_tco,
            "time_to_production_weeks": ttp_weeks}


def effective_history_years(v: Values) -> float:
    """Volume-ramped history: year k back carries (1+g)^-k of current volume."""
    years, g = v["history_years"], v["history_volume_growth"]
    whole = int(math.floor(years))
    full = sum((1 + g) ** -k for k in range(whole))
    return full + (years - whole) * (1 + g) ** -whole


def payback(investment: float, annual_contribution: float) -> float:
    return investment / (annual_contribution / 12) if annual_contribution > 0 else math.inf


def classify(payback_months: float, contribution: float, v: Values) -> str:
    if contribution <= 0 or payback_months > v["term_months"]:
        return "UNECONOMIC"
    if payback_months <= v["include_payback_months"]:
        return "INCLUDE_IN_FEE"
    return "SEPARATE_ONBOARDING_FEE"


def value_of_tracks(v: Values, rec: Mapping[str, float], onb: Mapping[str, float]) -> Dict[str, float]:
    shift = max(0.0, v["check_share_initial"] - v["check_share_target"])
    grants = rec["grants_per_year"]
    sponsor_saving = grants * shift * (check_rail_cost(v) - ach_rail_cost(v))
    unbound_saving = grants * shift * (check_labour_cost(v) - ach_labour_cost(v))
    network_avoided = onb["onb_charity_enrolment"] * v["registry_reuse_mature"]
    monthly = max(0.0, rec["contribution"]) / 12
    sales = v["sales_cycle_months_saved"] * monthly
    return {"value_epay_sponsor_passthrough_saving_yr": sponsor_saving,
            "value_epay_unbound_labour_saving_yr": unbound_saving,
            "value_network_enrolment_avoided_at_onboarding": network_avoided,
            "value_sales_cycle_reduction": sales}


def evaluate(params: Tuple[Param, ...], sc: Scenario) -> Dict[str, float | str]:
    v = resolve(params, sc)
    v["history_years"] = v[HISTORY_PARAM[sc.history]]
    rec = recurring_economics(v, sc)
    onb = onboarding_economics(v, sc, rec["recipients"])
    contrib = rec["contribution"]
    invest = onb["acquisition_and_onboarding_total"]
    pb = payback(invest, contrib)
    pb_onb_only = payback(onb["onb_total_unbound"], contrib)
    term_years = v["term_months"] / 12
    amort = invest / term_years
    anchors = {f"payback_months_at_{p}_per_account": payback(invest, p * sc.accounts - rec["cost_recurring_total"])
               for p in PRICE_ANCHORS_PER_ACCOUNT}
    be_bps = rec["cost_recurring_total"] / rec["aua"] * 10_000
    be_bps_onb = (rec["cost_recurring_total"] + amort) / rec["aua"] * 10_000
    be_balance = (rec["cost_recurring_total"] + amort) / (sc.accounts * sc.fee_bps / 10_000)
    fee_needed = max(0.0, invest - max(0.0, contrib) * v["include_payback_months"] / 12)
    out: Dict[str, float | str] = {}
    out.update(rec)
    out.update(onb)
    out.update(anchors)
    out.update({"payback_months": pb, "payback_months_onboarding_only": pb_onb_only,
                "unamortised_recovery_at_12m_prorata": invest * max(0.0, 1 - 12 / v["term_months"]),
                "unamortised_recovery_at_36m_prorata": invest * max(0.0, 1 - 36 / v["term_months"]),
                "breakeven_bps_recurring": be_bps,
                "breakeven_bps_incl_onboarding_amortised": be_bps_onb,
                "breakeven_balance_at_fee": be_balance,
                "revenue_per_account": rec["revenue"] / sc.accounts,
                "breakeven_price_per_account_incl_onboarding": (rec["cost_recurring_total"] + amort) / sc.accounts,
                "onboarding_fee_to_meet_include_threshold": fee_needed,
                "term_contribution_after_onboarding": contrib * term_years - invest,
                "classification": classify(pb, contrib, v)})
    out.update(value_of_tracks(v, rec, onb))
    return out


def scenario_grid() -> Tuple[Scenario, ...]:
    base = tuple(Scenario(n, g, q, b, f, "base") for n in SIZES for g in CASES
                 for q in QUALITY_TO_CASE for b in CASES for f in FEES_BPS)
    bounds = tuple(Scenario(n, g, q, b, WORKING_FEE_BPS, c) for c in ("low", "high") for n in SIZES
                   for g in CASES for q in QUALITY_TO_CASE for b in CASES)
    history = tuple(Scenario(n, "base", q, "base", WORKING_FEE_BPS, "base", h) for h in ("short", "mid")
                    for n in SIZES for q in QUALITY_TO_CASE)
    return base + bounds + history


# ---------------------------------------------------------------- formatting (pure)

def fmt(x: float | str) -> str:
    if isinstance(x, str):
        return x
    if math.isinf(x):
        return "inf"
    return f"{x:.4f}" if abs(x) < 100 else f"{x:.2f}"


def build_rows(params: Tuple[Param, ...]) -> Tuple[Tuple[str, ...], ...]:
    rows = []
    for case in CASES:
        v = resolve_cost_case(params, case)
        blocks = (("unit_cost", unit_cost_table(v)),
                  ("platform_establishment", registry_establishment_cost(v)),
                  ("platform_annual", registry_annual_cost(v)))
        for rtype, d in blocks:
            rows.extend((rtype, f"{rtype}-C{case}", "", "", "", "", "", case, "", k, fmt(val))
                        for k, val in d.items())
        for size in NETWORK_SIZES:
            rows.extend(("network_growth", f"network-{size}-C{case}", "", "", "", "", "", case, "", k, fmt(val))
                        for k, val in network_growth_cost(v, size).items())
    for sc in scenario_grid():
        res = evaluate(params, sc)
        rows.extend(("sponsor_scenario", sc.scenario_id, str(sc.accounts), sc.grants_case, sc.data_quality,
                     sc.balance_case, str(sc.fee_bps), sc.cost_case, sc.history, k, fmt(val))
                    for k, val in res.items())
    return tuple(rows)


def to_csv(rows: Tuple[Tuple[str, ...], ...]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(OUTPUT_HEADER)
    w.writerows(rows)
    return buf.getvalue()


def diff_lines(old: str, new: str) -> Tuple[str, ...]:
    a, b = old.splitlines(), new.splitlines()
    head = () if len(a) == len(b) else (f"row count {len(a)} != {len(b)}",)
    return head + tuple(f"line {i + 1}: '{x}' != '{y}'" for i, (x, y) in enumerate(zip(a, b)) if x != y)


# ---------------------------------------------------------------- report tables (pure)

def money(x: float) -> str:
    if math.isinf(x):
        return "n/a"
    sign = "-" if x < 0 else ""
    x = abs(x)
    if x >= 1e9:
        return f"{sign}${x / 1e9:.2f}B"
    if x >= 1e6:
        return f"{sign}${x / 1e6:.2f}M"
    if x >= 1e4:
        return f"{sign}${x / 1e3:.0f}k"
    if x >= 100:
        return f"{sign}${x:,.0f}"
    return f"{sign}${x:.2f}"


def months(x: float) -> str:
    return "never" if math.isinf(x) else f"{x:.1f}"


def table(header: Tuple[str, ...], body: Iterable[Tuple[str, ...]]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(r) + " |" for r in body]
    return "\n".join(lines)


def report(params: Tuple[Param, ...]) -> str:
    vs = {c: resolve_cost_case(params, c) for c in CASES}
    out = []
    uc = {c: unit_cost_table(vs[c]) for c in CASES}
    out.append("### R1 Unit costs (low / base / high cost case)\n")
    out.append(table(("Unit cost", "Low", "Base", "High"),
                     ((k, money(uc["low"][k]), money(uc["base"][k]), money(uc["high"][k])) for k in uc["base"])))
    est = {c: registry_establishment_cost(vs[c]) for c in CASES}
    ann = {c: registry_annual_cost(vs[c]) for c in CASES}
    out.append("\n\n### R2 Registry establishment and annual fixed cost\n")
    out.append(table(("Item", "Low", "Base", "High"),
                     [(k, f"{est['low'][k]:,.0f}" if 'hours' in k else money(est['low'][k]),
                       f"{est['base'][k]:,.0f}" if 'hours' in k else money(est['base'][k]),
                       f"{est['high'][k]:,.0f}" if 'hours' in k else money(est['high'][k])) for k in est["base"]]
                     + [(k, money(ann["low"][k]), money(ann["base"][k]), money(ann["high"][k])) for k in ann["base"]]))
    out.append("\n\n### R3 Network growth (base cost case): variable cost by charities in use\n")
    out.append(table(("Charities in use", "Monitoring/yr", "New verification/yr", "New enrolment/yr",
                      "Bank-change/yr", "Variable total/yr", "One-time enrol of existing"),
                     ((f"{s:,}",) + tuple(money(network_growth_cost(vs['base'], s)[k]) for k in
                      ("annual_monitoring_usd", "annual_new_charity_verification_usd", "annual_new_enrolment_usd",
                       "annual_bank_change_usd", "annual_network_variable_usd", "one_time_enrol_existing_usd"))
                      for s in NETWORK_SIZES)))

    def ev(n, g="base", q="typical", b="base", f=WORKING_FEE_BPS, c="base", h=DEFAULT_HISTORY):
        return evaluate(params, Scenario(n, g, q, b, f, c, h))

    out.append("\n\n### R4 Representative sponsors at 20 bps (base grants, typical data, base balance, base cost)\n")
    keys = (("avg_balance", money), ("aua", money), ("grants_per_year", lambda x: f"{x:,.0f}"),
            ("recipients", lambda x: f"{x:,.0f}"), ("revenue", money), ("cost_account_based", money),
            ("cost_transaction_based", money), ("cost_sponsor_fixed", money), ("contribution", money),
            ("contribution_margin", lambda x: f"{x * 100:.0f}%"), ("cost_per_account", money),
            ("cost_per_grant_unbound", money), ("sponsor_passthrough_rail_cost", money),
            ("onb_total_unbound", money), ("cac_per_sponsor", money), ("acquisition_and_onboarding_total", money),
            ("onb_per_account", money), ("onb_per_migrated_txn", money),
            ("onb_engineering_hours", lambda x: f"{x:,.0f}"), ("onb_charity_enrolment", money),
            ("onb_sponsor_hours", lambda x: f"{x:,.0f}"), ("onb_sponsor_cost", money),
            ("buyer_switching_tco", money),
            ("time_to_production_weeks", lambda x: f"{x:.0f}"), ("payback_months", months),
            ("payback_months_onboarding_only", months), ("payback_months_at_100_per_account", months),
            ("payback_months_at_400_per_account", months),
            ("breakeven_bps_recurring", lambda x: f"{x:.1f}"),
            ("breakeven_bps_incl_onboarding_amortised", lambda x: f"{x:.1f}"),
            ("breakeven_balance_at_fee", money), ("revenue_per_account", money),
            ("breakeven_price_per_account_incl_onboarding", money), ("classification", str))
    res = {n: ev(n) for n in SIZES}
    out.append(table(("Metric",) + tuple(f"{n:,} accts" for n in SIZES),
                     ((k,) + tuple(f(res[n][k]) for n in SIZES) for k, f in keys)))
    out.append("\n\n### R5 Onboarding components (base case, typical data)\n")
    comp = ("onb_implementation", "onb_engineering_config", "onb_integration_standard", "onb_integration_custom",
            "onb_per_account_migration", "onb_per_transaction_migration", "onb_reconciliation",
            "onb_donor_reonboarding", "onb_charity_enrolment", "onb_third_party", "onb_rehearsals",
            "onb_unbound_legal", "onb_failure_reserve", "onb_total_unbound", "cac_per_sponsor",
            "acquisition_and_onboarding_total")
    out.append(table(("Component",) + tuple(f"{n:,}" for n in SIZES),
                     ((k,) + tuple(money(res[n][k]) for n in SIZES) for k in comp)))
    out.append("\n\n### R6 Fee sensitivity: payback months (base grants, typical data, base balance)\n")
    out.append(table(("Accounts",) + tuple(f"{f} bps" for f in FEES_BPS),
                     ((f"{n:,}",) + tuple(f"{months(ev(n, f=f)['payback_months'])} ({ev(n, f=f)['classification']})"
                                         for f in FEES_BPS) for n in SIZES)))
    out.append("\n\n### R7 Data quality: onboarding cost / payback months / time to production (20 bps, base)\n")
    out.append(table(("Accounts", "Clean", "Typical", "Poor"),
                     ((f"{n:,}",) + tuple(f"{money(ev(n, q=q)['onb_total_unbound'])} / {months(ev(n, q=q)['payback_months'])} mo / {ev(n, q=q)['time_to_production_weeks']:.0f} wk"
                                         for q in QUALITY_TO_CASE) for n in SIZES)))
    out.append("\n\n### R8 Balance case: contribution and payback (20 bps, typical, base grants)\n")
    out.append(table(("Accounts", "Low balance", "Base balance", "High balance"),
                     ((f"{n:,}",) + tuple(f"{money(ev(n, b=b)['avg_balance'])}: {money(ev(n, b=b)['contribution'])} / {months(ev(n, b=b)['payback_months'])} mo"
                                         for b in CASES) for n in SIZES)))
    out.append("\n\n### R9 Grant volume: Unbound cost per account and contribution (20 bps, typical, base balance)\n")
    out.append(table(("Accounts", "Low grants (5.6)", "Base (7.0)", "High (12.3)"),
                     ((f"{n:,}",) + tuple(f"{money(ev(n, g=g)['cost_per_account'])}/acct; {money(ev(n, g=g)['contribution'])}"
                                         for g in CASES) for n in SIZES)))
    out.append("\n\n### R10 Cost case at 20 bps (typical data, base grants/balance): payback months\n")
    out.append(table(("Accounts", "Low cost", "Base cost", "High cost"),
                     ((f"{n:,}",) + tuple(f"{months(ev(n, c=c)['payback_months'])} ({money(ev(n, c=c)['onb_total_unbound'])})"
                                         for c in CASES) for n in SIZES)))
    grid = [sc for sc in scenario_grid() if sc.cost_case == "base" and sc.history == DEFAULT_HISTORY]
    counts: Dict[Tuple[int, int, str], int] = {}
    for sc in grid:
        k = (sc.accounts, sc.fee_bps, evaluate(params, sc)["classification"])
        counts[k] = counts.get(k, 0) + 1
    out.append("\n\n### R11 Classification counts across 27 grants x quality x balance combinations (base cost)\n")
    labels = ("INCLUDE_IN_FEE", "SEPARATE_ONBOARDING_FEE", "UNECONOMIC")
    out.append(table(("Accounts", "Fee bps") + labels,
                     ((f"{n:,}", str(f)) + tuple(str(counts.get((n, f, l), 0)) for l in labels)
                      for n in SIZES for f in FEES_BPS)))
    out.append("\n\n### R12 Value of the two tracks to Unbound (20 bps, base case, typical data)\n")
    vk = ("value_epay_sponsor_passthrough_saving_yr", "value_epay_unbound_labour_saving_yr",
          "value_network_enrolment_avoided_at_onboarding", "value_sales_cycle_reduction",
          "onboarding_fee_to_meet_include_threshold", "term_contribution_after_onboarding")
    out.append(table(("Value item",) + tuple(f"{n:,}" for n in SIZES),
                     ((k,) + tuple(money(res[n][k]) for n in SIZES) for k in vk)))
    worst = ev(1_000, g="high", q="poor", b="low", f=WORKING_FEE_BPS)
    out.append("\n\n### R13 Stress case: 1,000 accounts, high grants, poor data, low balance, 20 bps\n")
    out.append(table(("Metric", "Value"), ((k, f(worst[k])) for k, f in keys)))
    out.append("\n\n### R14 Non-included combinations for small sponsors (1,000 accounts, base cost)\n")
    small = [sc for sc in grid if sc.accounts == 1_000 and sc.fee_bps in (10, 20)]
    rows14 = []
    for sc in small:
        r = evaluate(params, sc)
        if r["classification"] != "INCLUDE_IN_FEE":
            rows14.append((str(sc.fee_bps), sc.grants_case, sc.data_quality, sc.balance_case,
                           money(r["contribution"]), money(r["onb_total_unbound"]), months(r["payback_months"]),
                           money(r["onboarding_fee_to_meet_include_threshold"]), r["classification"]))
    out.append(table(("Fee bps", "Grants", "Data", "Balance", "Contribution/yr", "Onboarding (excl. CAC)", "Payback mo (incl. CAC)",
                      "Fee to reach 24 mo (incl. CAC)", "Class"), rows14))
    out.append("\n\n### R16 History depth: onboarding cost / per-transaction share / payback (20 bps, base, typical data)\n")
    out.append(table(("Accounts", "Short (33 months, AEF)", "Mid (7 years, GWCF)", "Full (20 years ramped)"),
                     ((f"{n:,}",) + tuple(
                         f"{money(r['onb_total_unbound'])} / {r['onb_per_transaction_migration'] / r['onb_total_unbound'] * 100:.0f}% / {months(r['payback_months'])} mo"
                         for r in (ev(n, h=h) for h in HISTORY_CASES)) for n in SIZES)))
    out.append("\n\n### R17 Buyer switching TCO, outside Unbound's P&L (base, typical data, full history)\n")
    bk = ("onb_sponsor_hours", "onb_sponsor_cost", "buyer_consultant", "buyer_incumbent_tail_fee",
          "buyer_auditor_uplift", "buyer_legal", "buyer_comms", "buyer_switching_tco")
    out.append(table(("Item",) + tuple(f"{n:,}" for n in SIZES),
                     ((k,) + tuple((f"{res[n][k]:,.0f}" if k == "onb_sponsor_hours" else money(res[n][k])) for n in SIZES)
                      for k in bk)))
    hi = {n: ev(n, c="high", q="poor") for n in SIZES}
    out.append("\n\nHigh cost case, poor data: buyer switching TCO " + "; ".join(
        f"{n:,}: {money(hi[n]['buyer_switching_tco'])}" for n in SIZES) + ".\n")
    out.append("\n\n### R15 Registry fixed cost per grant by network grant volume (annual fixed + establishment over 5 yrs)\n")
    rows15 = []
    for g in (70_000, 700_000, 3_000_000, 7_000_000):
        rows15.append((f"{g:,}",) + tuple(
            money((registry_annual_cost(vs[c])["annual_fixed_total_usd"]
                   + registry_establishment_cost(vs[c])["establish_total_usd"] / 5) / g) for c in CASES))
    out.append(table(("Network grants/yr", "Low", "Base", "High"), rows15))
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- I/O edge

def read_params(path: Path) -> Tuple[Param, ...]:
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != PARAM_HEADER:
            raise SystemExit(f"bad parameter header: {reader.fieldnames}")
        rows = list(reader)
    bad = [r["parameter"] for r in rows if None in r or any(v is None for v in r.values())]
    if bad:
        raise SystemExit(f"malformed parameter rows: {bad}")
    return parse_params(rows)


def main(argv: Tuple[str, ...]) -> int:
    params = read_params(PARAMS_PATH)
    if "--report" in argv:
        sys.stdout.write(report(params))
        return 0
    text = to_csv(build_rows(params))
    if "--check" in argv:
        old = OUTPUT_PATH.read_text() if OUTPUT_PATH.exists() else ""
        diffs = diff_lines(old, text)
        for d in diffs[:20]:
            print(d)
        print("check: OK (output reproduces)" if not diffs else f"check: FAIL ({len(diffs)} differences)")
        return 0 if not diffs else 1
    OUTPUT_PATH.write_text(text)
    print(f"wrote {OUTPUT_PATH} ({text.count(chr(10)) - 1} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(tuple(sys.argv[1:])))
