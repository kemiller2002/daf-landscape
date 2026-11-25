#!/usr/bin/env python3
"""Sponsor economics dataset + customer-attractiveness model (group SPN, 2026-11-25).

Regenerates, deterministically and only from repository files (no network), every SPN table:

  sponsor-economics.csv          one row per sponsor EIN (all sponsors, incl. exited / merged, flagged)
  customer-attractiveness.csv    scored addressable sponsors (+ weight-scenario and one-at-a-time sensitivity)
  top25-hypotheses.csv           25 highest base-score hypotheses (NOT sales leads) with evidence / uncertainty
  self-sustaining-candidates.csv sponsors whose 20 bps contribution margin alone covers the lean fixed budget
  unattractive-large.csv         large-AUA sponsors that are economically or structurally unattractive, with reasons
  segment-summary.csv            economics by segment and by size band
  cost-to-serve-parameters.csv   every cost / threshold parameter, low/base/high, labelled [A] (replaceable)
  attractiveness-weights.csv     attractiveness dimension weights (base + 4 alternative scenarios)
  evidence.jsonl, assumptions.jsonl, summary-stats.json

Usage:  python3 -I -B build_sponsor_economics.py [REPO_ROOT] [OUT_DIR]
        defaults: REPO_ROOT=/home/user/daf-landscape, OUT_DIR=directory of this script.
If cost-to-serve-parameters.csv / attractiveness-weights.csv already exist in OUT_DIR they are READ (so an integrator can
replace parameter values and re-run); otherwise defaults below are written first and then read back.

Inputs (all read-only; relative to REPO_ROOT/data/mission-2026-11-14 unless noted):
  dafrc-sponsor-schedule-d-fy2019-2024.csv        DAFRC sponsor-year universe (Schedule D Part I, FY2019-2024)
  dafrc-corrections-itemized.csv                  rules R1-R4 (filed replaces imputed, terminated double count,
                                                  990 says no DAFs, closed but filed); applied==1 rows applied
  form990-returns-schedule-d-harvest-full.csv     IRS XML Schedule D FY2022-2025 (fill for EIN-FYs absent in DAFRC)
  form990-harvest-fy2025-refresh.csv              IRS XML FY2025 refresh (preferred for FY2025; other-funds columns)
  daf-sponsor-league-table-fy2021-2025.csv        top-50 corrected values + correction flags (override if different)
  daf-sponsor-league-table-fy2025-refresh.csv     FY2025 flags (fy2025_flags, change_vs_as_built)
  daf-long-tail-sponsors-fy2021-2024.csv          sponsor_category, BMF state/NTEE, exit fields, 990 DAF vendors,
                                                  donor-facing fee bps (context only, never servicer revenue)
  form990-contractors-harvest-full.csv, form990-contractors-fy2025-refresh.csv   Part VII-B vendor payments
  cf-vendor-map-by-ein-v2.csv, cf-vendor-migrations-2022-2026.csv, faith-sponsor-platforms-2026.csv
  sponsor-cost-structure.csv (employees, outside services l11, IT l14, opex), sponsor-pay-per-fte.csv
  sponsor-operating-efficiency-2026-11-20.csv (staffing_model, affiliate_evidence, segment)
  grant-count-denominators-2026-11-20.csv (sponsor-published grant COUNTS; Schedule I rows are never used as counts)
  fund-totals-from-990-2026-11-20.csv (total funds incl. non-DAF, tail CFs)
  cf-consolidation-2021-2026.csv, cf-exits-schedule-n-2021-2026.csv, sponsor-entry-exit-panel.csv (mergers, exits)
  pass-through-sponsors-2026.csv, digital-sponsor-entities-2026.csv, wealth-captive-terms-2026.csv,
  sponsor-audit-notes.csv (captive / affiliate administration evidence)
  daf-to-daf-flows-990.csv, dechomai-share-of-sponsor-contributions-2026-11-19.csv, daf-reclassification-screen.csv
  REPO_ROOT/data/commercial-opportunity/prospects-sponsors.csv (evidenced observed challenges -> buying signals)

Labels: [S] sourced (repo path), [D] derived by stated arithmetic, [A] assumption (parameters CSV), [E] estimate.
Style: pure functions returning new frames; no global mutable state; outputs sorted and rounded for byte stability.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

ASOF = "2026-11-25"
BPS_LIST = (5, 10, 15, 20, 25, 30, 35)
METRICS = ("assets", "accounts", "contributions", "grants")


# ----------------------------------------------------------------------------------------------------------------- io
def paths(repo: str) -> dict:
    m = os.path.join(repo, "data", "mission-2026-11-14")
    j = lambda f: os.path.join(m, f)  # noqa: E731
    return {
        "dafrc": j("dafrc-sponsor-schedule-d-fy2019-2024.csv"),
        "corr": j("dafrc-corrections-itemized.csv"),
        "harvest": j("form990-returns-schedule-d-harvest-full.csv"),
        "refresh": j("form990-harvest-fy2025-refresh.csv"),
        "league": j("daf-sponsor-league-table-fy2021-2025.csv"),
        "league25": j("daf-sponsor-league-table-fy2025-refresh.csv"),
        "longtail": j("daf-long-tail-sponsors-fy2021-2024.csv"),
        "contractors": j("form990-contractors-harvest-full.csv"),
        "contractors25": j("form990-contractors-fy2025-refresh.csv"),
        "vendormap": j("cf-vendor-map-by-ein-v2.csv"),
        "migrations": j("cf-vendor-migrations-2022-2026.csv"),
        "faith": j("faith-sponsor-platforms-2026.csv"),
        "cost": j("sponsor-cost-structure.csv"),
        "payfte": j("sponsor-pay-per-fte.csv"),
        "opeff": j("sponsor-operating-efficiency-2026-11-20.csv"),
        "grantcounts": j("grant-count-denominators-2026-11-20.csv"),
        "fundtotals": j("fund-totals-from-990-2026-11-20.csv"),
        "consolidation": j("cf-consolidation-2021-2026.csv"),
        "schedn": j("cf-exits-schedule-n-2021-2026.csv"),
        "entryexit": j("sponsor-entry-exit-panel.csv"),
        "passthrough": j("pass-through-sponsors-2026.csv"),
        "digital": j("digital-sponsor-entities-2026.csv"),
        "auditnotes": j("sponsor-audit-notes.csv"),
        "d2d": j("daf-to-daf-flows-990.csv"),
        "dechomai": j("dechomai-share-of-sponsor-contributions-2026-11-19.csv"),
        "reclass": j("daf-reclassification-screen.csv"),
        "prospects": os.path.join(repo, "data", "commercial-opportunity", "prospects-sponsors.csv"),
    }


def rel(repo: str, p: str) -> str:
    return os.path.relpath(p, repo)


def read(p: str, ein_cols=("ein",)) -> pd.DataFrame:
    df = pd.read_csv(p, dtype=str, keep_default_na=False, na_values=[""])
    out = df.copy()
    for c in ein_cols:
        if c in out.columns:
            out[c] = out[c].map(norm_ein)
    return out


def norm_ein(x) -> str | None:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    s = re.sub(r"[^0-9]", "", str(x))
    return s.zfill(9) if 1 <= len(s) <= 9 else None


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


# --------------------------------------------------------------------------------------------------------- parameters
DEFAULT_PARAMS = [
    # parameter, low, base, high, unit, label, basis
    ("fixed_per_sponsor_usd", 10000, 25000, 50000, "USD/sponsor/yr", "[A]",
     "Relationship management, sponsor reporting, reconciliation sign-off, audit support per sponsor. Placeholder for activity-cost agent."),
    ("per_account_usd", 15, 25, 45, "USD/account/yr", "[A]",
     "Account maintenance: statements, donor service contacts, identity/KYC refresh, data. Base chosen so base per-account total (~$75 at 7 grants + 1 contribution) reconciles to the $75/fund-yr hypothesis in daf-servicer-bottom-up-operating-budget-2026-11-25.md:34 (not validation)."),
    ("per_grant_usd", 4, 6, 12, "USD/grant", "[A]",
     "Charity validation, payment, acknowledgement, exception share per grant."),
    ("per_contribution_usd", 5, 10, 20, "USD/contribution", "[A]",
     "Receipt, asset receipt and gift acknowledgement per contribution (cash/securities)."),
    ("grant_dollar_review_bps", 0.0, 0.5, 1.0, "bps of grant USD", "[A]",
     "Value-scaled review effort (large-grant due diligence, expenditure responsibility) as bps of grant dollars."),
    ("grants_per_account", 4, 7, 11, "grants/account/yr", "[A]",
     "Used only when no sponsor-published grant count exists. Calibration [D]: published counts / Schedule D accounts for 10 sponsors give ~5.6-18.5 (median ~7); see summary-stats.json grant_count_calibration."),
    ("contributions_per_account", 0.5, 1.0, 2.0, "contributions/account/yr", "[A]",
     "No public contribution-count source found in repo; pure assumption (evidence gap)."),
    ("uplift_cf_nondaf_funds", 0.15, 0.25, 0.40, "multiplier add-on", "[A]",
     "Applied when sponsor is a community foundation (or other) with DAF share of total assets < nondaf_share_threshold: fund-accounting integration, mixed fund types."),
    ("nondaf_share_threshold", 0.5, 0.5, 0.5, "share", "[A]", "DAF assets / total assets below which non-DAF complexity uplift applies."),
    ("uplift_faith", 0.05, 0.10, 0.20, "multiplier add-on", "[A]", "Religiously-affiliated sponsor: recipient eligibility screens, church/ministry recipients."),
    ("uplift_international", 0.10, 0.25, 0.50, "multiplier add-on", "[A]", "International grantmaking vehicle (equivalency determination / expenditure responsibility)."),
    ("uplift_complex_assets", 0.10, 0.25, 0.50, "multiplier add-on", "[A]", "Non-cash / complex-asset processor or Dechomai inflow share >= complex_asset_share_threshold."),
    ("complex_asset_share_threshold", 0.05, 0.05, 0.05, "share", "[A]", "Dechomai share of DAF contributions at/above which complex-asset uplift applies."),
    ("uplift_pass_through_processor", 0.25, 0.50, 1.00, "multiplier add-on", "[A]", "Donation-processor / pass-through sponsors (very high volume, tiny balances)."),
    ("onboarding_fixed_usd", 50000, 100000, 200000, "USD one-time", "[A]", "Implementation, configuration, controls set-up per sponsor."),
    ("onboarding_per_account_usd", 5, 15, 30, "USD/account one-time", "[A]", "Data conversion, reconciliation and donor re-onboarding per account."),
    ("onboarding_custom_platform_uplift", 0.25, 0.50, 1.00, "multiplier add-on", "[A]", "Sponsor on in-house / custom / unknown platform (no known export path)."),
    ("concentration_reference_revenue_usd", 5000000, 5000000, 5000000, "USD/yr", "[A]", "Size of the hypothetical servicer business X for concentration exposure."),
    ("downturn_shock", 0.30, 0.30, 0.30, "share of AUA", "[A]", "Full-year asset shock; accounts and costs unchanged (mirrors budget doc stress)."),
    ("self_sustain_fixed_cost_usd", 1177750, 1177750, 1177750, "USD/yr", "[S]",
     "Lean servicer fixed budget hypothesis: daf-servicer-bottom-up-operating-budget-2026-11-25.md fixed budget total (a hypothesis under test, not a measured cost)."),
    ("self_sustain_bps", 20, 20, 20, "bps", "[A]", "Price at which self-sustaining test is run."),
    ("large_aua_threshold_usd", 1e9, 1e9, 1e9, "USD EOY DAF assets", "[A]", "Threshold for 'large AUA' in unattractive-large screen."),
    ("recent_migration_months", 24, 24, 24, "months before 2026-11-25", "[A]", "Platform migration completed within this window => likely new multi-year contract, low near-term switch probability."),
    ("addressable_min_latest_fy", 2023, 2023, 2023, "fiscal year", "[A]", "Sponsors whose latest DAF data is older are treated as inactive for scoring."),
    ("small_account_balance_usd", 50000, 50000, 50000, "USD", "[A]", "Average balance below which a sponsor counts as small-account tail."),
    ("high_value_balance_usd", 1000000, 1000000, 1000000, "USD", "[A]", "Average balance above which a sponsor counts as concentrated high-value."),
    ("top_n_hypotheses", 25, 25, 25, "count", "[A]", "Number of hypotheses."),
]

DIMENSIONS = [
    # dimension, base, equal, revenue_heavy, risk_heavy, cost_heavy, direction, description
    ("potential_revenue", 0.14, 1, 0.30, 0.08, 0.10, "higher better", "log10 of 20 bps revenue on avg-assets proxy, $10k->0, $10m->1"),
    ("accounts", 0.03, 1, 0.05, 0.02, 0.02, "higher better", "log10 accounts 10->0, 50,000->1 (recurring base; cost captured elsewhere)"),
    ("transaction_intensity", 0.06, 1, 0.03, 0.05, 0.10, "lower intensity better", "est. grants+contributions per $1m avg AUA; 5->1, 1000->0 (log)"),
    ("complexity", 0.05, 1, 0.03, 0.05, 0.08, "lower better", "1 - sum of complexity uplifts (base)"),
    ("service_workload", 0.07, 1, 0.04, 0.05, 0.14, "lower better", "1 - base cost-to-serve / 20 bps revenue (clipped)"),
    ("accounting_complexity", 0.04, 1, 0.02, 0.04, 0.06, "lower better", "DAF share of total assets (1 for nationals); 0.7 when unknown [A]"),
    ("configuration_integration", 0.05, 1, 0.03, 0.05, 0.06, "easier better", "known packaged platform 0.8; Salesforce/custom/in-house 0.4; unknown 0.5 [A]"),
    ("migration_complexity", 0.05, 1, 0.03, 0.08, 0.06, "easier better", "1 - (0.6*account scale + 0.4*custom platform)"),
    ("sales_cycle", 0.05, 1, 0.03, 0.06, 0.04, "shorter better", "segment x size mapping [A]; -0.3 when recently migrated"),
    ("contractual_captive", 0.10, 1, 0.08, 0.16, 0.08, "unconstrained better", "captive / affiliate / vendor-owned / recent migration constraints"),
    ("switching_evidence", 0.07, 1, 0.06, 0.08, 0.05, "more evidence better", "documented vendor attrition family, evidenced buying signal; completed migration lowers"),
    ("strategic_value", 0.06, 1, 0.06, 0.04, 0.04, "higher better", "size, replicable vendor family, segment template value [A]"),
    ("concentration_risk", 0.04, 1, 0.02, 0.10, 0.04, "lower risk better", "1 - 20 bps revenue / reference business revenue X"),
    ("contribution_margin", 0.13, 1, 0.20, 0.08, 0.18, "higher better", "base contribution margin % at 20 bps (negative -> 0)"),
    ("evidence_strength", 0.06, 1, 0.02, 0.06, 0.05, "higher better", "data-quality grade and vendor-evidence confidence"),
]


def default_params_frame() -> pd.DataFrame:
    return pd.DataFrame(DEFAULT_PARAMS, columns=["parameter", "low", "base", "high", "unit", "label", "basis"])


def default_weights_frame() -> pd.DataFrame:
    df = pd.DataFrame(DIMENSIONS, columns=["dimension", "base", "equal", "revenue_heavy", "risk_heavy", "cost_heavy",
                                           "direction", "description"])
    out = df.copy()
    out["equal"] = round(1 / len(df), 6)
    out["label"] = "[A]"
    return out


def load_or_write(path: str, default: pd.DataFrame) -> pd.DataFrame:
    if not os.path.exists(path):
        default.to_csv(path, index=False, lineterminator="\n")
    return pd.read_csv(path)


def params_dict(pf: pd.DataFrame) -> dict:
    return {r.parameter: {"low": float(r.low), "base": float(r.base), "high": float(r.high)} for r in pf.itertuples()}


# --------------------------------------------------------------------------------------------------------- panel
METRIC_MAP = {"daf_assets_eoy": "assets", "daf_accounts_eoy": "accounts", "daf_contributions": "contributions",
              "daf_grants": "grants"}


def dafrc_panel(d: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({
        "ein": d["ein"], "fy": num(d["fiscal_year_end"]).astype(int), "name_dafrc": d["name"],
        "type": d["type"], "subtype": d["subtype"], "operating_status": d["operating_status"],
        "vetted_status": d["vetted_status"],
        "assets": num(d["eoy_daf_assets"]), "accounts": num(d["number_of_daf_accounts"]),
        "contributions": num(d["total_daf_contributions"]), "grants": num(d["total_daf_grants"]),
        "src_assets": d["source_eoy_daf_assets"], "src_accounts": d["source_number_of_accounts"],
        "src_contributions": d["source_total_daf_contributions"], "src_grants": d["source_total_daf_grants"],
    })
    return out


def apply_corrections(p: pd.DataFrame, corr: pd.DataFrame) -> pd.DataFrame:
    c = corr[corr["applied"] == "1"].copy()
    c["fy"] = num(c["fiscal_year"]).astype(int)
    c["m"] = c["metric"].map(METRIC_MAP)
    c["val"] = num(c["corrected_value"])
    c = c.dropna(subset=["m"]).sort_values(["ein", "fy", "m", "rule"]).drop_duplicates(["ein", "fy", "m"], keep="last")
    # add rows for R4 (closed but filed) EIN-FYs not in DAFRC
    keys = set(zip(p["ein"], p["fy"]))
    new_keys = sorted({(e, f) for e, f in zip(c["ein"], c["fy"]) if (e, f) not in keys})
    meta = p.sort_values("fy").drop_duplicates("ein", keep="last").set_index("ein")
    add = pd.DataFrame([{"ein": e, "fy": f, "name_dafrc": meta.at[e, "name_dafrc"] if e in meta.index else None,
                         "type": meta.at[e, "type"] if e in meta.index else None,
                         "subtype": meta.at[e, "subtype"] if e in meta.index else None,
                         "operating_status": "row added by R4 (closed but filed)", "vetted_status": None}
                        for e, f in new_keys])
    q = pd.concat([p, add], ignore_index=True) if len(add) else p.copy()
    q["corr_rules"] = ""
    piv = c.pivot_table(index=["ein", "fy"], columns="m", values="val", aggfunc="first")
    rules = c.groupby(["ein", "fy"])["rule"].apply(lambda s: ";".join(sorted(set(s))))
    q = q.set_index(["ein", "fy"])
    for m in METRICS:
        if m in piv.columns:
            v = piv[m].dropna()
            idx = q.index.intersection(v.index)
            q.loc[idx, m] = v.loc[idx]
            q.loc[idx, "src_" + m] = "corrected:" + c.set_index(["ein", "fy", "m"]).xs(m, level="m").loc[idx, "rule"].astype(str)
    q.loc[q.index.intersection(rules.index), "corr_rules"] = rules.loc[q.index.intersection(rules.index)]
    return q.reset_index()


def harvest_panel(h: pd.DataFrame, refresh: pd.DataFrame) -> pd.DataFrame:
    def prep(df, tag):
        x = df[df["xml_status"] == "ok"].copy()
        x["fy"] = num(x["fiscal_year"]).astype(int)
        x["_ts"] = x["return_ts"].fillna("")
        x = x.sort_values(["ein", "fy", "_ts", "return_object_id"]).drop_duplicates(["ein", "fy"], keep="last")
        has = (num(x["sched_d_present"]).fillna(0) > 0) & x["sched_d_daf_eoy_value"].notna()
        cols = {
            "ein": x["ein"], "fy": x["fy"], "h_name": x["filer_name_990"].fillna(x["sponsor_name"]),
            "h_assets": num(x["sched_d_daf_eoy_value"]).where(has),
            "h_accounts": num(x["sched_d_daf_count"]).where(has),
            "h_contributions": num(x["sched_d_daf_contributions"]).where(has),
            "h_grants": num(x["sched_d_daf_grants"]).where(has),
            "h_total_assets": num(x["total_assets_eoy"]), "h_it": num(x["part_ix_it_total"]),
            "h_object_id": x["return_object_id"], "h_tax_period_end": x["tax_period_end"],
            "h_daf_ind": x["daf_ind_part_iv"], "h_src": tag,
            "h_other_funds_count": num(x["sched_d_other_funds_count"]) if "sched_d_other_funds_count" in x else np.nan,
            "h_other_funds_value": num(x["sched_d_other_funds_eoy_value"]) if "sched_d_other_funds_eoy_value" in x else np.nan,
            "h_amended": x["amended_ind"],
        }
        return pd.DataFrame(cols)
    a = prep(h, "form990-returns-schedule-d-harvest-full.csv")
    b = prep(refresh, "form990-harvest-fy2025-refresh.csv")
    both = pd.concat([b, a], ignore_index=True)  # refresh first => preferred for duplicate EIN-FY
    return both.drop_duplicates(["ein", "fy"], keep="first").reset_index(drop=True)


def merge_panel(dp: pd.DataFrame, hp: pd.DataFrame, league: pd.DataFrame) -> pd.DataFrame:
    m = dp.merge(hp, on=["ein", "fy"], how="outer")
    out = m.copy()
    for k in METRICS:
        fill = out[k].isna() & out["h_" + k].notna()
        out.loc[fill, k] = out.loc[fill, "h_" + k]
        out.loc[fill, "src_" + k] = "irs_xml:" + out.loc[fill, "h_src"]
    # league table corrected (FY2021-2024) override where values differ
    lg = league[league["value_basis"] == "corrected_R1_R4"].copy()
    lg["fy"] = num(lg["fiscal_year"]).astype(int)
    lg = lg.drop_duplicates(["ein", "fy"]).set_index(["ein", "fy"])
    out = out.set_index(["ein", "fy"])
    out["league_override"] = ""
    lmap = {"assets": "daf_assets_eoy", "accounts": "daf_accounts_eoy", "contributions": "daf_contributions",
            "grants": "daf_grants"}
    idx = out.index.intersection(lg.index)
    for k, col in lmap.items():
        lv = num(lg.loc[idx, col])
        diff = lv.notna() & (out.loc[idx, k].isna() | ((out.loc[idx, k] - lv).abs() > 0.5))
        di = diff[diff].index
        out.loc[di, k] = lv.loc[di]
        out.loc[di, "src_" + k] = "league_table_corrected"
        out.loc[di, "league_override"] = out.loc[di, "league_override"] + k + ";"
    out["imputed_metrics"] = ""
    for k in METRICS:
        imp = out["src_" + k].fillna("").eq("Imputed")
        out.loc[imp, "imputed_metrics"] = out.loc[imp, "imputed_metrics"] + k + ";"
    return out.reset_index().sort_values(["ein", "fy"]).reset_index(drop=True)


# --------------------------------------------------------------------------------------------------------- per-EIN
def screen_accounts(assets: float, accounts: float) -> tuple[float, str]:
    if pd.isna(accounts) or accounts <= 0:
        return (np.nan, "accounts_missing_or_zero")
    if accounts > 1000 and pd.notna(assets) and assets / accounts < 5:
        return (np.nan, "accounts_screened_out(>1000 and <$5/account)")
    return (accounts, "")


def cagr(a0, a1, years):
    if pd.isna(a0) or pd.isna(a1) or a0 <= 0 or a1 <= 0:
        return np.nan
    return (a1 / a0) ** (1 / years) - 1


def summarise_ein(g: pd.DataFrame) -> dict:
    g = g.sort_values("fy")
    filed = g[g["assets"].notna() & ~g["src_assets"].fillna("").eq("Imputed")]
    anyv = g[g["assets"].notna()]
    if len(filed):
        lat = filed.iloc[-1]
        latest_basis = "filed"
    elif len(anyv):
        lat = anyv.iloc[-1]
        latest_basis = "imputed_only"
    else:
        lat = g.iloc[-1]
        latest_basis = "no_asset_value"
    lfy = int(lat["fy"])
    prior = g[g["fy"] == lfy - 1]
    pr = prior.iloc[0] if len(prior) else None
    three = g[g["fy"] == lfy - 3]
    a3 = three.iloc[0]["assets"] if len(three) else np.nan
    ser = g.set_index("fy")["assets"]
    yoy = [(ser[f] / ser[f - 1] - 1) for f in ser.index if (f - 1) in ser.index and pd.notna(ser[f]) and pd.notna(ser[f - 1]) and ser[f - 1] > 0]
    cser = g.set_index("fy")["contributions"].dropna()
    acc_s, acc_flag = screen_accounts(lat["assets"], lat["accounts"])
    names = sorted({str(x) for x in list(g["name_dafrc"].dropna()) + list(g["h_name"].dropna())})
    name_latest = (g["h_name"].dropna().iloc[-1] if g["h_name"].notna().any() else g["name_dafrc"].dropna().iloc[-1])
    t = g["type"].dropna()
    st = g["subtype"].dropna()
    ops = g["operating_status"].dropna()
    return {
        "name": name_latest, "name_variants": " | ".join(names) if len(names) > 1 else "",
        "dafrc_type": t.iloc[-1] if len(t) else "", "dafrc_subtype": st.iloc[-1] if len(st) else "",
        "dafrc_operating_status": ops.iloc[-1] if len(ops) else "",
        "first_fy": int(g["fy"].min()), "last_panel_fy": int(g["fy"].max()), "latest_fy": lfy,
        "latest_fy_basis": latest_basis,
        "latest_tax_period_end": lat.get("h_tax_period_end") if pd.notna(lat.get("h_tax_period_end")) else "",
        "latest_return_object_id": lat.get("h_object_id") if pd.notna(lat.get("h_object_id")) else "",
        "daf_assets_eoy": lat["assets"], "accounts_reported": lat["accounts"], "accounts": acc_s,
        "accounts_flag": acc_flag, "contributions": lat["contributions"], "grants": lat["grants"],
        "src_assets": lat["src_assets"], "src_accounts": lat["src_accounts"], "src_contributions": lat["src_contributions"],
        "src_grants": lat["src_grants"], "corr_rules_latest": lat["corr_rules"] if pd.notna(lat["corr_rules"]) else "",
        "imputed_metrics_latest": lat["imputed_metrics"], "league_override_latest": lat["league_override"],
        "prior_fy": lfy - 1 if pr is not None else np.nan,
        "daf_assets_boy": pr["assets"] if pr is not None else np.nan,
        "prior_accounts": pr["accounts"] if pr is not None else np.nan,
        "prior_contributions": pr["contributions"] if pr is not None else np.nan,
        "prior_grants": pr["grants"] if pr is not None else np.nan,
        "prior_imputed_metrics": pr["imputed_metrics"] if pr is not None else "",
        "assets_cagr_3y": cagr(a3, lat["assets"], 3),
        "assets_yoy_vol": float(np.std(yoy, ddof=1)) if len(yoy) >= 3 else np.nan,
        "assets_yoy_min": float(min(yoy)) if len(yoy) else np.nan,
        "n_yoy_obs": len(yoy),
        "contributions_cv": float(cser.std(ddof=1) / cser.mean()) if len(cser) >= 3 and cser.mean() > 0 else np.nan,
        "total_assets_eoy_990": lat.get("h_total_assets") if pd.notna(lat.get("h_total_assets")) else np.nan,
        "other_funds_count_sched_d": lat.get("h_other_funds_count"), "other_funds_value_sched_d": lat.get("h_other_funds_value"),
        "it_part_ix_latest_990": lat.get("h_it"),
        "fy2025_return_no_sched_d_daf": bool(((g["fy"] == 2025) & g["h_object_id"].notna() & g["h_assets"].isna()).any()),
        "panel_years_with_data": int(anyv["fy"].nunique()),
        "fy_list": ";".join(str(int(f)) for f in anyv["fy"]),
    }


def sponsor_base(panel: pd.DataFrame) -> pd.DataFrame:
    rows = [{"ein": e, **summarise_ein(g)} for e, g in panel.groupby("ein", sort=True)]
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------------------------------------- enrichers
def latest_cost(cost: pd.DataFrame) -> pd.DataFrame:
    c = cost.copy()
    c["fyn"] = num(c["fiscal_year"])
    c = c.sort_values(["ein", "fyn", "return_ts"]).drop_duplicates("ein", keep="last")
    return pd.DataFrame({
        "ein": c["ein"], "cost_fy": c["fyn"], "employees": num(c["employees"]),
        "outside_services_l11": num(c["outside_services_l11"]), "it_l14": num(c["it_l14"]),
        "staff_cost_l5_10": num(c["staff_cost_l5_10"]), "operating_cost_ex_invest_mgmt": num(c["operating_cost_ex_invest_mgmt"]),
        "fees_invest_mgmt_l11f": num(c["fees_invest_mgmt_l11f"]), "total_assets_eoy_cost": num(c["total_assets_eoy"]),
        "total_functional_expenses": num(c["total_functional_expenses"]), "cost_quality_flags": c["quality_flags"].fillna(""),
        "sponsor_daf_opex_per_account_alloc_990": num(c["daf_opex_per_account_assets_alloc"]),
        "sponsor_daf_opex_bps_grants_alloc_990": num(c["daf_opex_bps_of_daf_assets_grants_alloc"]),
    })


def opeff_latest(o: pd.DataFrame) -> pd.DataFrame:
    s = o[o["record_type"] == "sponsor_year"].copy()
    s["fyn"] = num(s["fy"])
    s = s.sort_values(["ein", "fyn"]).drop_duplicates("ein", keep="last")
    return pd.DataFrame({"ein": s["ein"], "staffing_model": s["staffing_model"].fillna(""),
                         "affiliate_evidence": s["affiliate_evidence"].fillna(""), "opeff_segment": s["segment"].fillna("")})


def payfte(p: pd.DataFrame) -> pd.DataFrame:
    x = p.copy()
    x["fyn"] = num(x["fiscal_year"])
    x = x.sort_values(["ein", "fyn"]).drop_duplicates("ein", keep="last")
    return pd.DataFrame({"ein": x["ein"], "loaded_cost_per_head_payfte": num(x["loaded_all_per_head"]),
                         "payfte_fy": x["fyn"]})


def longtail_fields(l: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "ein": l["ein"], "sponsor_category": l["sponsor_category"], "bmf_state": l["bmf_state"], "bmf_ntee": l["bmf_ntee"],
        "age_years_at_2024": num(l["age_years_at_2024"]), "lt_exit_kind": l["exit_kind"], "lt_exit_fy": l["exit_fy"],
        "lt_exit_outcome": l["exit_outcome"], "lt_cf_vendor_family": l["cf_vendor_family"],
        "lt_cf_vendor_confidence": l["cf_vendor_confidence"], "vendors_990_daf_relevant_fy2022_25": l["vendors_990_daf_relevant_fy2022_25"],
        "donor_fee_bps_at_100k_context": num(l["fee_bps_100k"]), "donor_fee_source": l["fee_source"],
        "support_cliff_flags": l["support_cliff_flags_fy2021_24"],
    })


DAF_ADMIN_CATS = {"daf_tech_admin_vendor", "giving_platform_or_outsourced_admin"}
DAF_TECH_CATS = {"daf_tech_vendor", "enterprise_software", "investment_accounting_software", "grant_admin_due_diligence"}
IT_CATS = {"technology_services"}


def contractor_vendors(k: pd.DataFrame) -> pd.DataFrame:
    x = k.copy()
    x["comp"] = num(x["compensation"])
    x["fyn"] = num(x["fiscal_year"])
    x = x.drop_duplicates(["ein", "return_object_id", "contractor_name", "compensation"])
    rel_ = x[x["vendor_category"].isin(DAF_ADMIN_CATS | DAF_TECH_CATS | IT_CATS)]

    def fmt(r):
        return f"{r.vendor_group} '{str(r.services)[:40]}' ${int(r.comp):,} FY{int(r.fyn)}"

    rows = []
    for e, g in rel_.groupby("ein", sort=True):
        g = g.sort_values(["fyn", "comp"], ascending=[False, False])
        lf = g["fyn"].max()
        adm = g[g["vendor_category"].isin(DAF_ADMIN_CATS)]
        tec = g[g["vendor_category"].isin(DAF_TECH_CATS)]
        it = g[g["vendor_category"].isin(IT_CATS)]
        lat_adm = adm[adm["fyn"] == adm["fyn"].max()] if len(adm) else adm
        lat_tec = tec[tec["fyn"] == tec["fyn"].max()] if len(tec) else tec
        rows.append({
            "ein": e,
            "vendor990_admin": "; ".join(sorted(set(lat_adm["vendor_group"]))),
            "vendor990_admin_latest_fy": lat_adm["fyn"].max() if len(lat_adm) else np.nan,
            "vendor990_admin_first_fy": adm["fyn"].min() if len(adm) else np.nan,
            "vendor990_tech": "; ".join(sorted(set(lat_tec["vendor_group"]))),
            "vendor990_tech_latest_fy": lat_tec["fyn"].max() if len(lat_tec) else np.nan,
            "vendor990_lines": " | ".join(fmt(r) for r in pd.concat([lat_adm, lat_tec]).head(4).itertuples()),
            "vendor990_it_services_lines": " | ".join(fmt(r) for r in it[it["fyn"] == lf].head(3).itertuples()),
            "vendor990_daf_vendor_usd_latest": float(pd.concat([lat_adm, lat_tec])["comp"].sum()),
            "vendor990_source": "form990 Part VII-B (top-5 contractors > $100k only: floors)",
            "vendor990_url": (pd.concat([lat_adm, lat_tec]).iloc[0]["source_url"] if len(pd.concat([lat_adm, lat_tec])) else ""),
        })
    return pd.DataFrame(rows)


def vendor_map(v: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"ein": v["ein"], "vm_family": v["vendor_family"], "vm_portal": v["portal_vendor"],
                         "vm_confidence": v["confidence"], "vm_evidence_url": v["evidence_url"],
                         "vm_ledger_implied": v["ledger_implied"], "vm_retrieved": v["retrieved"]}).drop_duplicates("ein")


def faith_map(f: pd.DataFrame) -> pd.DataFrame:
    x = f[f["ein"].notna()]
    return pd.DataFrame({"ein": x["ein"], "faith_platform_family": x["platform_family"], "faith_confidence": x["confidence"],
                         "faith_portal": x["donor_portal_platform"].str.slice(0, 160),
                         "faith_admin_evidence": x["admin_or_ledger_vendor_evidence"].str.slice(0, 200),
                         "faith_url": x["portal_evidence_url"]}).drop_duplicates("ein")


EXTRA_MIGRATIONS = [
    # ein, from, to, date, confidence, source (repo path + row), quality
    ("341747398", "multi-system (NPact/PRCGEN builds)", "Ren (full platform)", "2026-04-08", "medium",
     "data/commercial-opportunity/prospects-sponsors.csv PS02: 'Ren: 2026-04-08 release says Ren technology now fully power[s] all of AEF's customers'; cutover spring 2026", "C"),
    ("237343119", "Blackbaud Donor Central", "Foundation Cloud Community Portal + Financial Edge NXT", "2026-09-21", "medium",
     "data/commercial-opportunity/prospects-sponsors.csv PS12: 'launch moved to 2026-09-21'", "B"),
    ("232888152", "Salesforce / UST build", "Give Interactive recordkeeping partnership", "2025-11-04", "medium",
     "data/commercial-opportunity/prospects-sponsors.csv PS04: 'Give Interactive recordkeeping partnership (release 2025-11-04)'", "C"),
]


def migrations(m: pd.DataFrame) -> pd.DataFrame:
    ev = m[(m["record_type"] == "event") & m["to_system"].notna() & ~m["to_system"].fillna("").isin(["n/a", ""])]
    rows = [{"ein": r.ein, "mig_from": r.from_system, "mig_to": r.to_system, "mig_date": r.event_date,
             "mig_date_confidence": r.date_confidence,
             "mig_source": "data/mission-2026-11-14/cf-vendor-migrations-2022-2026.csv", "mig_quality": "B"}
            for r in ev.itertuples()]
    rows += [{"ein": e, "mig_from": a, "mig_to": b, "mig_date": d, "mig_date_confidence": c, "mig_source": s, "mig_quality": q}
             for e, a, b, d, c, s, q in EXTRA_MIGRATIONS]
    df = pd.DataFrame(rows)
    df["mig_date_parsed"] = df["mig_date"].fillna("").str.extract(r"(\d{4}-\d{2}(?:-\d{2})?)")[0]
    return df.sort_values(["ein", "mig_date_parsed"]).drop_duplicates("ein", keep="last")


def months_before_asof(d: str) -> float:
    if not isinstance(d, str) or not re.match(r"\d{4}-\d{2}", d):
        return np.nan
    y, mth = int(d[:4]), int(d[5:7])
    return (2026 - y) * 12 + (11 - mth)


# captive / affiliate classification (EIN -> status, basis, quality). Basis cites repo files only.
CAPTIVE = {
    "110303001": ("captive_inhouse_affiliate", "FMR LLC and affiliates contracted for administrative services (sponsor-audit-notes.csv, Fidelity FY2025 AFS Note 7); segment affiliated_commercial (sponsor-operating-efficiency-2026-11-20.csv)", "A"),
    "311640316": ("captive_inhouse_affiliate", "DAFgiving360 (Schwab): segment affiliated_commercial, affiliate_staffed (sponsor-operating-efficiency-2026-11-20.csv)", "B"),
    "232888152": ("captive_inhouse_affiliate", "Vanguard provides investment recordkeeping and administrative services (sponsor-audit-notes.csv, FY2026 AFS Note 1); Give Interactive recordkeeping partnership 2025-11-04 (prospects-sponsors.csv PS04)", "A"),
    "352129262": ("vendor_captive", "Renaissance Administration LLC 'Administration' $13.49m/$15.54m/$19.23m TY2022-24 (prospects-sponsors.csv PS03); affiliate_staffed", "A"),
    "311774905": ("financial_affiliate_vendor_outsourced", "Goldman Sachs program (wealth-captive-terms-2026.csv); Ren 990 lines (daf-long-tail-sponsors vendors_990)", "B"),
    "113813663": ("financial_affiliate_vendor_outsourced", "Goldman Sachs Charitable Gift Fund: Ren and CAF America 990 lines (daf-long-tail-sponsors vendors_990); name", "B"),
    "527082731": ("financial_affiliate_vendor_outsourced", "Morgan Stanley GIFT (wealth-captive-terms-2026.csv; donor circular on msgift.donorfirstx.com); Ren 990 lines", "B"),
    "046010342": ("financial_affiliate_unknown_platform", "Bank of America CGF (wealth-captive-terms-2026.csv); segment affiliated_commercial; platform not public (CT-only Ren host lead, ren-iphi-attrition-summary.json)", "B"),
    "593652538": ("financial_affiliate_unknown_platform", "Raymond James: segment affiliated_commercial, affiliate_staffed (sponsor-operating-efficiency-2026-11-20.csv)", "B"),
    "311663020": ("financial_affiliate_vendor_outsourced", "segment affiliated_commercial; Ren 990 lines (daf-long-tail-sponsors vendors_990)", "B"),
    "141782466": ("financial_affiliate_vendor_outsourced", "Ayco: segment affiliated_commercial; Ren 990 lines", "B"),
    "137111099": ("financial_affiliate_unknown_platform", "Bessemer: segment affiliated_commercial (sponsor-operating-efficiency-2026-11-20.csv)", "B"),
    "311709466": ("financial_affiliate_vendor_outsourced", "T. Rowe Price: segment affiliated_commercial, token staff; Ren 990 lines", "B"),
    "842049692": ("financial_affiliate_vendor_outsourced", "Stifel: Ren and SS&C 990 lines (daf-long-tail-sponsors vendors_990); name", "C"),
    "300748315": ("financial_affiliate_unknown_platform", "BNY Mellon Charitable Gift Fund: name only", "D"),
    "810739440": ("vendor_captive", "AOGF run by Benevity Inc under a management services agreement (pass-through-sponsors-2026.csv PT-01)", "A"),
    "450931286": ("vendor_captive", "PayPal Inc sole member (pass-through-sponsors-2026.csv PT-03)", "A"),
    "460942102": ("vendor_captive", "Blackbaud Inc Class A member; service agreement (pass-through-sponsors-2026.csv PT-04)", "A"),
    "474172718": ("vendor_captive", "Givinga Inc affiliated vendor (pass-through-sponsors-2026.csv PT-07; digital-sponsor-entities-2026.csv DSE-02)", "A"),
    "873165286": ("vendor_captive", "Goodstack service provider (pass-through-sponsors-2026.csv PT-08)", "B"),
    "462109112": ("vendor_captive", "Submittable via WizeHive related taxable corp (pass-through-sponsors-2026.csv PT-06)", "B"),
    "680480736": ("vendor_captive", "Network for Good: Bonterra Tech LLC contractor; sole member Durable Capital (pass-through-sponsors-2026.csv PT-05)", "B"),
    "611913297": ("inhouse_platform_app_native", "Every.org in-house platform (digital-sponsor-entities-2026.csv DSE-01)", "A"),
    "863177440": ("inhouse_platform_app_native", "Daffy builds own platform (prospects-sponsors.csv PS21)", "B"),
    "844661797": ("inhouse_platform_app_native", "Endaoment own platform and public API (prospects-sponsors.csv PS23; digital-sponsor-entities DSE-04)", "B"),
    "812771871": ("vendor_captive", "Charityvest: Foundation Source acquired Vennfi (Charityvest technology) Oct 2024 [R] (prospects-sponsors.csv PS22)", "C"),
    "431890105": ("vendor_captive", "Servant Foundation (The Signatry): GIVE_INTERACTIVE_OWNED (faith-sponsor-platforms-2026.csv)", "B"),
    "825070897": ("vendor_captive", "The Signatry Charitable Trust: GIVE_INTERACTIVE_OWNED (faith-sponsor-platforms-2026.csv)", "B"),
    "581493949": ("inhouse_platform_custom", "NCF sponsor-built MyGiving portal on Salesforce with Ren component; SF_CAPTIVE (faith-sponsor-platforms-2026.csv; prospects PS18)", "B"),
}
NAME_AFFILIATE_PATTERNS = (r"\bBANK\b", r"COMERICA", r"TOMPKINS", r"FIRST MIDWEST", r"UNIVEST", r"CREDIT UNION", r"CERITY PARTNERS")

RELATED_GROUPS = {
    # group id: (member eins, basis)
    "RG-GKCCF": (("200849590", "431152398"), "Greater Horizons is affiliate of Greater Kansas City CF (prospects-sponsors.csv PS05; opeff segment_note_affiliate)"),
    "RG-DECHOMAI": (("260724604", "061676688"), "Dechomai Asset Trust / Dechomai Foundation (prospects-sponsors.csv PS20)"),
    "RG-SIGNATRY": (("431890105", "825070897"), "Servant Foundation dba The Signatry + Signatry Charitable Trust (faith-sponsor-platforms-2026.csv)"),
    "RG-CCFLA": (("842235389", "383941057"), "CCF-LA Supporting Organization + Catholic Community Foundation (faith-sponsor-platforms-2026.csv; Schedule N transfer 2020 cf-exits-schedule-n)"),
    "RG-NPT": (("237825575", "277059768"), "National Philanthropic Trust + NPT Charitable Asset Trust (name) [D]"),
    "RG-GS": (("311774905", "113813663", "141782466"), "Goldman Sachs-affiliated programs (GS DAF, GS Charitable Gift Fund, Ayco) [D name/affiliation; Ayco link not evidenced in repo]"),
}

INTERNATIONAL_EINS = {"431634280": "CAF America (pass-through-sponsors-2026.csv PT-02)", "710992446": "Kiva Microfunds (name)"}


def merger_map(corr: pd.DataFrame, schedn: pd.DataFrame, cons: pd.DataFrame) -> pd.DataFrame:
    rows = []
    r2 = corr[corr["rule"].fillna("").str.startswith("R2") & corr["note"].notna()].drop_duplicates("ein")
    for r in r2.itertuples():
        hits = re.findall(r"to: ([^()]+?) \(EIN (\d{9}); FMV (\d+)", r.note)
        if hits:
            best = sorted(hits, key=lambda h: -int(h[2]))[0]
            rows.append({"ein": r.ein, "merged_into": best[1], "merged_into_name": best[0].strip(), "merge_basis":
                         f"R2 terminated: {r.note[:160]} (dafrc-corrections-itemized.csv)", "merge_year": (re.search(r"final return FY(\d{4})", r.note).group(1) if re.search(r"final return FY(\d{4})", r.note) else r.fiscal_year),
                         "merge_kind": "terminated_transfer"})
    exiting = set(schedn.loc[schedn["event_class"].isin(["exit_liquidation_schedule_n", "exit_final_return_no_schedule_n_part_i"]), "filer_ein"])
    # for exiting filers, successor = largest-FMV Schedule N transferee across all of that filer's events
    s = schedn[schedn["filer_ein"].isin(exiting) & (schedn["transferee_ein"].notna() | schedn["transferee_name"].notna())].copy()
    s["fmv"] = num(s["fmv_usd"]).fillna(0)
    for e, g in s.groupby("filer_ein", sort=True):
        g = g.sort_values(["fmv", "transferee_ein"], ascending=[False, True])
        t = g.iloc[0]
        if pd.notna(t["transferee_ein"]) or pd.notna(t["transferee_name"]):
            rows.append({"ein": e, "merged_into": t["transferee_ein"] if pd.notna(t["transferee_ein"]) else "",
                         "merged_into_name": t["transferee_name"], "merge_basis": f"Schedule N {t['event_class']} {t['event_year']} FMV ${int(t['fmv']):,} (cf-exits-schedule-n-2021-2026.csv {t['row_id']})",
                         "merge_year": t["event_year"], "merge_kind": "liquidation_transfer"})
    d = schedn[(schedn["event_class"] == "disposition_over_25pct") & ~schedn["filer_ein"].isin(exiting)].copy()
    d["fmv"] = num(d["fmv_usd"]).fillna(0)
    for e, g in d.groupby("filer_ein", sort=True):
        g = g.sort_values(["fmv", "transferee_ein"], ascending=[False, True])
        t = g.iloc[0]
        rows.append({"ein": e, "merged_into": "", "merged_into_name": "",
                     "merge_basis": f"Schedule N disposition >25% {t['event_year']} to {t['transferee_name']} ({t['transferee_ein']}) FMV ${int(t['fmv']):,} (cf-exits-schedule-n {t['row_id']})",
                     "merge_year": t["event_year"], "merge_kind": "partial_disposition_note"})
    for r in cons.itertuples():
        ea = re.search(r"EIN (\d{9})", str(r.party_a))
        eb = re.search(r"EIN (\d{9})", str(r.party_b))
        if ea and str(r.event_type).startswith("schedule_n_liquidation"):
            rows.append({"ein": ea.group(1), "merged_into": eb.group(1) if eb else "", "merged_into_name": re.sub(r"\s*\(EIN.*", "", str(r.party_b)),
                         "merge_basis": f"{r.event_id} {r.event_type} {r.date} (cf-consolidation-2021-2026.csv)", "merge_year": r.year, "merge_kind": "liquidation_transfer"})
    df = pd.DataFrame(rows)
    pri = {"terminated_transfer": 0, "liquidation_transfer": 1, "partial_disposition_note": 2}
    df["_p"] = df["merge_kind"].map(pri)
    agg = (df.sort_values(["ein", "_p", "merge_basis"])
             .groupby("ein", sort=True)
             .agg(merged_into=("merged_into", "first"), merged_into_name=("merged_into_name", "first"),
                  merge_kind=("merge_kind", "first"), merge_year=("merge_year", "first"),
                  merge_basis=("merge_basis", lambda s: " || ".join(dict.fromkeys(s)))))
    return agg.reset_index()


def grant_counts(gc: pd.DataFrame) -> pd.DataFrame:
    x = gc[(gc["is_primary"] == "1") & gc["count_status"].isin(["stated", "derived"])].copy()
    return pd.DataFrame({"ein": x["ein"], "grant_count_published": num(x["grant_count"]),
                         "grant_count_unit": x["count_unit"], "grant_count_period": x["period_label"],
                         "grant_count_period_match": x["period_match"], "grant_count_url": x["url"],
                         "grant_count_status": x["count_status"]}).drop_duplicates("ein")


def fund_totals(ft: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"ein": ft["ein"], "total_funds_990": num(ft["n_total_funds"]), "total_funds_fy": ft["total_fy"],
                         "total_funds_qual": ft["total_qual"]}).drop_duplicates("ein")


def d2d_outbound(d: pd.DataFrame) -> pd.DataFrame:
    x = d.copy()
    x["ein"] = x["grantor_ein"].map(norm_ein)
    x["amt"] = num(x["amount_usd"])
    x["fyn"] = num(x["fiscal_year"])
    s = x.groupby(["ein", "fyn"], as_index=False)["amt"].sum().sort_values(["ein", "fyn"]).drop_duplicates("ein", keep="last")
    return pd.DataFrame({"ein": s["ein"], "daf_to_daf_outbound_usd": s["amt"], "daf_to_daf_fy": s["fyn"]})


def dechomai_share(d: pd.DataFrame) -> pd.DataFrame:
    x = d[(d["row_type"] == "year") & (d["match_variant"] == "primary_ty_t")].copy()
    x["ein"] = x["sponsor_ein"].map(norm_ein)
    x["sh"] = num(x["share_of_sponsor_daf_contributions"])
    s = x.groupby("ein", as_index=False)["sh"].max()
    return pd.DataFrame({"ein": s["ein"], "dechomai_share_contrib_max": s["sh"]})


def reclass_flags(r: pd.DataFrame) -> pd.DataFrame:
    x = r.copy()
    x["flag"] = x.get("classification", pd.Series([""] * len(x))).fillna("") if "classification" in x else ""
    cols = [c for c in x.columns if c.startswith("flag_")]
    keep = x[(x[cols].apply(lambda s: num(s).fillna(0)).sum(axis=1) > 0)] if cols else x
    return pd.DataFrame({"ein": keep["ein"], "count_basis_change_flag":
                         "daf-reclassification-screen.csv FY" + keep["fy_prev"].astype(str) + "->" + keep["fy_cur"].astype(str)
                         + " count " + keep["daf_count_prev"].astype(str) + "->" + keep["daf_count_cur"].astype(str)}).drop_duplicates("ein")


def prospects(p: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for r in p.itertuples():
        for e in re.findall(r"EIN[s]? ?(\d{2}-\d{7})", str(r.organization)) + re.findall(r"/ (\d{2}-\d{7})", str(r.organization)):
            rows.append({"ein": norm_ein(e), "prospect_id": r.prospect_id, "prospect_confidence": r.confidence,
                         "prospect_challenges": str(r.observed_challenges)[:260], "prospect_contradictory": str(r.contradictory_evidence)[:200]})
    return pd.DataFrame(rows).drop_duplicates("ein")


def league_flags(lg: pd.DataFrame, lg25: pd.DataFrame) -> pd.DataFrame:
    a = lg.copy()
    a["fyn"] = num(a["fiscal_year"])
    a = a.sort_values(["ein", "fyn"])
    f1 = a.groupby("ein").agg(league_corrections=("corrections_applied", lambda s: ";".join(sorted({x for x in s.dropna() for x in x.split(";")}))),
                              league_imputed_kept=("imputed_kept_metrics", lambda s: ";".join(sorted({x for x in s.dropna() for x in x.split(";")}))),
                              league_churn=("churn_status", "last"), league_rank_latest=("rank_assets", "last"),
                              league_grants_netted_central=("daf_grants_netted_central", "last"))
    b = lg25.drop_duplicates("ein").set_index("ein")[["fy2025_flags", "change_vs_as_built", "row_type"]].rename(
        columns={"fy2025_flags": "league25_flags", "change_vs_as_built": "league25_change_vs_as_built", "row_type": "league25_row_type"})
    return f1.join(b, how="outer").reset_index()


def entry_exit(ee: pd.DataFrame) -> pd.DataFrame:
    s = ee.sort_values(["ein", "fiscal_year"]).drop_duplicates("ein", keep="last")
    return pd.DataFrame({"ein": s["ein"], "exit_kind": s["sponsor_exit_kind"], "exit_fy": s["sponsor_exit_fy"],
                         "exit_outcome": s["sponsor_exit_outcome"], "exit_outcome_tier": s["sponsor_exit_outcome_tier"]})


# --------------------------------------------------------------------------------------------------------- classify
def segment_of(r) -> str:
    cap = r["captive_status"]
    if cap in ("captive_inhouse_affiliate", "financial_affiliate_vendor_outsourced", "financial_affiliate_unknown_platform", "financial_affiliate_name_inferred"):
        return "national_financial_affiliate"
    if cap == "inhouse_platform_app_native":
        return "digital_app_native"
    if r["dafrc_subtype"] == "Donation Processor" or r["ein"] in PASS_THROUGH_EINS:
        return "donation_processor_pass_through"
    if r["ein"] == "352129262" or (cap == "vendor_captive" and r["dafrc_type"] == "National"):
        return "national_vendor_affiliated"
    t, st = r["dafrc_type"], r["dafrc_subtype"]
    if t == "National":
        return "national_independent"
    if t == "Community Foundation":
        return "community_foundation"
    if st == "Religiously-Affiliated":
        return "faith"
    if st == "Universities and Healthcare":
        return "university_healthcare"
    if st == "Other":
        return "single_issue_other"
    return "unclassified_non_dafrc"


PASS_THROUGH_EINS = {"810739440", "431634280", "450931286", "460942102", "680480736", "462109112", "474172718", "873165286", "611913297"}


def size_band(a) -> str:
    if pd.isna(a):
        return "unknown"
    for lim, lab in ((1e6, "a_<1m"), (1e7, "b_1-10m"), (5e7, "c_10-50m"), (2.5e8, "d_50-250m"), (1e9, "e_250m-1bn"), (5e9, "f_1-5bn")):
        if a < lim:
            return lab
    return "g_>=5bn"


def captive_status(ein: str, name: str, dtype: str, opeff_seg: str) -> tuple[str, str, str]:
    if ein in CAPTIVE:
        return CAPTIVE[ein]
    if opeff_seg == "affiliated_commercial":
        return ("financial_affiliate_unknown_platform", "segment affiliated_commercial (sponsor-operating-efficiency-2026-11-20.csv)", "B")
    if dtype == "National" and any(re.search(p, str(name).upper()) for p in NAME_AFFILIATE_PATTERNS):
        return ("financial_affiliate_name_inferred", "financial-institution name keyword [D]", "D")
    return ("none_found", "", "")


KNOWN_PACKAGES = ("Foundant", "Ren", "akoya", "AKOYA", "Blackbaud", "BLACKBAUD", "REN", "FIDTECH", "DonorSphere", "GiftingNetwork",
                  "GIFTINGNETWORK", "Foundation Cloud", "NPact", "Give Interactive", "GIVE_INTERACTIVE", "Fund-Miner", "Mightycause",
                  "FrontStream", "Northeast Retirement", "TASC", "Total Administrative")
CUSTOM_MARKERS = ("Salesforce", "SF_", "Microsoft Power", "in-house", "inhouse", "donor-portal.org", "Unidentified", "UNKNOWN")


NON_VENDOR = ("Unmapped", "Unidentified portal", "", "n/a", "unknown")


def vendor_resolution(r) -> dict:
    """Pick technology vendor + admin provider with evidence and confidence; precedence documented in report."""
    cands = []
    if isinstance(r.get("mig_to"), str) and r["mig_to"]:
        cands.append((r["mig_to"], f"migration event {r.get('mig_date')} ({r.get('mig_source')})", "medium" if r.get("mig_quality") == "B" else "low", 1))
    if isinstance(r.get("faith_platform_family"), str) and r["faith_platform_family"] not in ("UNKNOWN", ""):
        cands.append((r["faith_platform_family"], f"faith-sponsor-platforms-2026.csv: {r.get('faith_portal')}", str(r.get("faith_confidence")), 2))
    if isinstance(r.get("vm_family"), str) and r["vm_family"] not in NON_VENDOR:
        cands.append((r["vm_family"], f"cf-vendor-map-by-ein-v2.csv portal {r.get('vm_portal')} {r.get('vm_evidence_url')}", str(r.get("vm_confidence")), 3))
    if isinstance(r.get("vendor990_tech"), str) and r["vendor990_tech"]:
        cands.append((r["vendor990_tech"], f"990 Part VII-B: {r.get('vendor990_lines')}", "high (payment); scope per services text", 4))
    if isinstance(r.get("vendor990_admin"), str) and r["vendor990_admin"]:
        cands.append((r["vendor990_admin"], f"990 Part VII-B: {r.get('vendor990_lines')}", "high (payment); scope per services text", 4))
    if isinstance(r.get("lt_cf_vendor_family"), str) and r["lt_cf_vendor_family"] not in NON_VENDOR:
        cands.append((r["lt_cf_vendor_family"], "daf-long-tail-sponsors-fy2021-2024.csv cf_vendor_family", str(r.get("lt_cf_vendor_confidence")), 5))
    if r["captive_status"] in ("captive_inhouse_affiliate", "inhouse_platform_app_native", "inhouse_platform_custom", "vendor_captive"):
        cands.append(("affiliate/in-house: " + r["captive_status"], r["captive_basis"], "per captive basis", 0))
    cands = sorted(cands, key=lambda c: c[3])
    tech, ev, conf = (cands[0][0], cands[0][1], cands[0][2]) if cands else ("unknown", "", "none")
    admin = ""
    if r["captive_status"] in ("captive_inhouse_affiliate", "vendor_captive"):
        admin = "affiliate/vendor under agreement: " + r["captive_basis"][:140]
    elif isinstance(r.get("vendor990_admin"), str) and r["vendor990_admin"]:
        admin = r["vendor990_admin"] + " (990 Part VII-B payee)"
    elif r.get("staffing_model") == "affiliate_staffed":
        admin = "affiliate-staffed (opeff staffing_model); provider not named"
    else:
        admin = "own staff / not evidenced"
    alltxt = " ".join(str(c[0]) for c in cands)
    known = any(k in alltxt for k in KNOWN_PACKAGES)
    custom = any(k in alltxt for k in CUSTOM_MARKERS) or r["captive_status"].startswith("inhouse")
    return {"tech_vendor": tech, "tech_vendor_evidence": ev[:300], "tech_vendor_confidence": conf,
            "tech_vendor_all_signals": " | ".join(sorted({str(c[0]) for c in cands if c[3] > 0}))[:300],
            "admin_provider": admin, "platform_known_package": known, "platform_custom_or_inhouse": custom and not known
            or r["captive_status"].startswith("inhouse")}


ATTRITION_FAMILIES = ("Ren", "REN", "iPhi", "Stellar", "Foundation Cloud", "Blackbaud", "BLACKBAUD", "donor-portal.org")


# --------------------------------------------------------------------------------------------------------- economics
def cost_to_serve(r, P: dict, lvl: str) -> dict:
    p = {k: v[lvl] for k, v in P.items()}
    acc = r["accounts_for_cost"]
    if pd.isna(acc) or pd.isna(r["avg_assets_proxy"]):
        return {"cost": np.nan, "grant_count": np.nan, "contrib_count": np.nan, "uplift": np.nan}
    gcount = r["grant_count_published"] if pd.notna(r.get("grant_count_published")) else acc * p["grants_per_account"]
    ccount = acc * p["contributions_per_account"]
    gdollars = r["grants"] if pd.notna(r["grants"]) else 0.0
    up = (p["uplift_cf_nondaf_funds"] * r["flag_nondaf_complex"] + p["uplift_faith"] * r["flag_faith"]
          + p["uplift_international"] * r["flag_international"] + p["uplift_complex_assets"] * r["flag_complex_assets"]
          + p["uplift_pass_through_processor"] * r["flag_pass_through"])
    var = acc * p["per_account_usd"] + gcount * p["per_grant_usd"] + ccount * p["per_contribution_usd"] + gdollars * p["grant_dollar_review_bps"] / 1e4
    cost = (p["fixed_per_sponsor_usd"] + var) * (1 + up)
    return {"cost": cost, "grant_count": gcount, "contrib_count": ccount, "uplift": up}


def onboarding(r, P: dict, lvl: str) -> float:
    p = {k: v[lvl] for k, v in P.items()}
    acc = r["accounts_for_cost"]
    if pd.isna(acc):
        return np.nan
    base = p["onboarding_fixed_usd"] + acc * p["onboarding_per_account_usd"]
    return base * (1 + p["onboarding_custom_platform_uplift"] * (r["platform_custom_or_inhouse"] or r["tech_vendor"] == "unknown")) * (1 + r["uplift_base"])


def economics(df: pd.DataFrame, P: dict) -> pd.DataFrame:
    out = df.copy()
    for b in BPS_LIST:
        out[f"rev_{b}bps_avg_proxy"] = out["avg_assets_proxy"] * b / 1e4
    out["rev_20bps_eoy_runrate"] = out["daf_assets_eoy"] * 20 / 1e4
    for lvl in ("low", "base", "high"):
        res = out.apply(lambda r: cost_to_serve(r, P, lvl), axis=1, result_type="expand")
        out[f"cost_to_serve_{lvl}"] = res["cost"]
        if lvl == "base":
            out["grant_count_used"] = res["grant_count"]
            out["contribution_count_est"] = res["contrib_count"]
            out["uplift_base"] = res["uplift"]
    out["grant_count_basis"] = np.where(out["grant_count_published"].notna(), "[S] sponsor-published count (grant-count-denominators-2026-11-20.csv; unit as stated)",
                                        np.where(out["accounts_for_cost"].notna(), "[E] accounts x grants_per_account (base)", ""))
    for b in (15, 20, 25):
        out[f"margin_{b}bps_base"] = out[f"rev_{b}bps_avg_proxy"] - out["cost_to_serve_base"]
    out["margin_20bps_low_cost"] = out["rev_20bps_avg_proxy"] - out["cost_to_serve_low"]
    out["margin_20bps_high_cost"] = out["rev_20bps_avg_proxy"] - out["cost_to_serve_high"]
    out["margin_pct_20bps_base"] = out["margin_20bps_base"] / out["rev_20bps_avg_proxy"]
    out["cost_per_account_base"] = out["cost_to_serve_base"] / out["accounts_for_cost"]
    out["breakeven_bps_base"] = out["cost_to_serve_base"] / out["avg_assets_proxy"] * 1e4
    out["onboarding_cost_base"] = out.apply(lambda r: onboarding(r, P, "base"), axis=1)
    out["onboarding_cost_low"] = out.apply(lambda r: onboarding(r, P, "low"), axis=1)
    out["onboarding_cost_high"] = out.apply(lambda r: onboarding(r, P, "high"), axis=1)
    out["onboarding_payback_years_base"] = np.where(out["margin_20bps_base"] > 0, out["onboarding_cost_base"] / out["margin_20bps_base"], np.nan)
    X = P["concentration_reference_revenue_usd"]["base"]
    out["concentration_share_of_X"] = out["rev_20bps_avg_proxy"] / X
    shock = P["downturn_shock"]["base"]
    out["rev_20bps_after_shock"] = out["rev_20bps_avg_proxy"] * (1 - shock)
    out["margin_20bps_after_shock_base"] = out["rev_20bps_after_shock"] - out["cost_to_serve_base"]
    F = P["self_sustain_fixed_cost_usd"]["base"]
    bps = P["self_sustain_bps"]["base"]
    m_ss = out["avg_assets_proxy"] * bps / 1e4 - out["cost_to_serve_base"]
    out["self_sustain_margin"] = m_ss
    out["self_sustaining_base"] = m_ss >= F
    out["self_sustaining_low_cost"] = (out["avg_assets_proxy"] * bps / 1e4 - out["cost_to_serve_low"]) >= F
    out["self_sustaining_high_cost"] = (out["avg_assets_proxy"] * bps / 1e4 - out["cost_to_serve_high"]) >= F
    out["self_sustaining_after_shock"] = out["margin_20bps_after_shock_base"] >= F
    out["self_sustain_coverage_ratio"] = m_ss / F
    return out


# --------------------------------------------------------------------------------------------------------- scoring
def clip01(x):
    return float(min(1.0, max(0.0, x))) if pd.notna(x) else np.nan


def logscale(x, lo, hi):
    if pd.isna(x) or x <= 0:
        return 0.0
    return clip01((math.log10(x) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)))


SALES_CYCLE = {"community_foundation": 0.7, "faith": 0.6, "single_issue_other": 0.6, "university_healthcare": 0.4,
               "national_independent": 0.45, "national_financial_affiliate": 0.3, "national_vendor_affiliated": 0.1,
               "donation_processor_pass_through": 0.3, "digital_app_native": 0.2, "unclassified_non_dafrc": 0.4}
SEGMENT_TEMPLATE = {"community_foundation": 1.0, "faith": 0.8, "national_independent": 0.6, "single_issue_other": 0.5,
                    "university_healthcare": 0.5, "national_financial_affiliate": 0.6, "national_vendor_affiliated": 0.2,
                    "donation_processor_pass_through": 0.2, "digital_app_native": 0.2, "unclassified_non_dafrc": 0.3}
GRADE = {"A": 1.0, "B": 0.75, "C": 0.5, "D": 0.25}


def dim_scores(r, P) -> dict:
    X = P["concentration_reference_revenue_usd"]["base"]
    tx = (r["grant_count_used"] + r["contribution_count_est"]) / (r["avg_assets_proxy"] / 1e6) if r["avg_assets_proxy"] and pd.notna(r["grant_count_used"]) and r["avg_assets_proxy"] > 0 else np.nan
    acc_scale = logscale(r["accounts_for_cost"], 100, 100000)
    custom = 1.0 if r["platform_custom_or_inhouse"] else (0.5 if r["tech_vendor"] == "unknown" else 0.0)
    ab = r["daf_assets_eoy"]
    size_adj = 0.15 if (pd.notna(ab) and ab < 1e7) else (-0.15 if (pd.notna(ab) and ab > 2e9) else 0.0)
    sales = clip01(SALES_CYCLE.get(r["segment"], 0.4) + size_adj - (0.3 if r["recent_migration"] else 0.0))
    cap = r["captive_status"]
    contract = {"captive_inhouse_affiliate": 0.0, "vendor_captive": 0.0, "inhouse_platform_app_native": 0.0,
                "inhouse_platform_custom": 0.25, "financial_affiliate_vendor_outsourced": 0.3,
                "financial_affiliate_unknown_platform": 0.4, "financial_affiliate_name_inferred": 0.6}.get(cap, 1.0)
    if r["recent_migration"]:
        contract = min(contract, 0.2)
    if r["status"] != "active":
        contract = 0.0
    sw = 0.3
    if any(k in str(r["tech_vendor_all_signals"]) + str(r["tech_vendor"]) for k in ATTRITION_FAMILIES):
        sw += 0.3
    if isinstance(r.get("prospect_id"), str) and r["prospect_id"]:
        sw += 0.2
    if r["recent_migration"]:
        sw = 0.1
    fam_size = {"Foundant": 1.0, "Ren": 0.8, "akoya": 0.6, "Blackbaud": 0.6, "Foundation Cloud": 0.6}
    rep = max([v for k, v in fam_size.items() if k.lower() in str(r["tech_vendor"]).lower()] + [0.3])
    strat = clip01(0.4 * logscale(ab, 1e7, 5e9) + 0.3 * rep + 0.3 * SEGMENT_TEMPLATE.get(r["segment"], 0.3))
    accnt = 1.0 if str(r["segment"]).startswith(("national", "digital", "donation")) else (r["daf_share_of_total_assets"] if pd.notna(r["daf_share_of_total_assets"]) else 0.7)
    ev_v = {"high": 1.0, "medium": 0.7, "low": 0.4, "none": 0.1}
    vconf = next((v for k, v in ev_v.items() if str(r["tech_vendor_confidence"]).lower().startswith(k)), 0.4)
    return {
        "s_potential_revenue": logscale(r["rev_20bps_avg_proxy"], 1e4, 1e7),
        "s_accounts": logscale(r["accounts_for_cost"], 10, 50000),
        "s_transaction_intensity": (1 - logscale(tx, 5, 1000)) if pd.notna(tx) else 0.0,
        "s_complexity": clip01(1 - r["uplift_base"]) if pd.notna(r["uplift_base"]) else 0.5,
        "s_service_workload": clip01(1 - r["cost_to_serve_base"] / r["rev_20bps_avg_proxy"]) if r["rev_20bps_avg_proxy"] and r["rev_20bps_avg_proxy"] > 0 else 0.0,
        "s_accounting_complexity": clip01(accnt),
        "s_configuration_integration": 0.4 if r["platform_custom_or_inhouse"] else (0.8 if r["platform_known_package"] else 0.5),
        "s_migration_complexity": clip01(1 - (0.6 * acc_scale + 0.4 * custom)),
        "s_sales_cycle": sales,
        "s_contractual_captive": contract,
        "s_switching_evidence": clip01(sw),
        "s_strategic_value": strat,
        "s_concentration_risk": clip01(1 - r["rev_20bps_avg_proxy"] / X) if pd.notna(r["rev_20bps_avg_proxy"]) else 0.0,
        "s_contribution_margin": clip01(r["margin_pct_20bps_base"]) if pd.notna(r["margin_pct_20bps_base"]) else 0.0,
        "s_evidence_strength": clip01(0.6 * GRADE.get(r["data_quality"], 0.25) + 0.4 * vconf),
        "transactions_per_musd_est": tx,
    }


def score(df: pd.DataFrame, w: pd.Series) -> pd.Series:
    cols = ["s_" + d for d in w.index]
    return (df[cols].values @ w.values) / w.sum() * 100


def rank_desc(s: pd.Series, ein: pd.Series) -> pd.Series:
    tmp = pd.DataFrame({"s": s.round(9), "ein": ein})
    order = tmp.sort_values(["s", "ein"], ascending=[False, True]).index
    r = pd.Series(np.arange(1, len(tmp) + 1), index=order)
    return r.reindex(tmp.index)


def sensitivity(df: pd.DataFrame, W: pd.DataFrame, topn: int) -> tuple[pd.DataFrame, dict]:
    base_w = W.set_index("dimension")["base"].astype(float)
    out = df.copy()
    out["score_base"] = score(out, base_w)
    out["rank_base"] = rank_desc(out["score_base"], out["ein"])
    summ = {}
    for sc in ("equal", "revenue_heavy", "risk_heavy", "cost_heavy"):
        w = W.set_index("dimension")[sc].astype(float)
        out[f"score_{sc}"] = score(out, w)
        out[f"rank_{sc}"] = rank_desc(out[f"score_{sc}"], out["ein"])
        top_b = set(out.loc[out["rank_base"] <= topn, "ein"])
        top_s = set(out.loc[out[f"rank_{sc}"] <= topn, "ein"])
        summ[f"top{topn}_overlap_base_vs_{sc}"] = len(top_b & top_s)
        summ[f"spearman_base_vs_{sc}"] = round(float(np.corrcoef(out["rank_base"], out[f"rank_{sc}"])[0, 1]), 4)
    ranks = []
    for d in base_w.index:
        for f in (0.5, 1.5):
            w = base_w.copy()
            w[d] = w[d] * f
            ranks.append(rank_desc(score(out, w), out["ein"]))
    R = pd.concat(ranks, axis=1)
    out["rank_oat_min"] = R.min(axis=1)
    out["rank_oat_max"] = R.max(axis=1)
    out["share_oat_runs_in_topn"] = (R <= topn).mean(axis=1).round(4)
    summ["oat_runs"] = int(R.shape[1])
    return out, summ


# --------------------------------------------------------------------------------------------------------- assemble
def data_quality(r) -> tuple[str, str]:
    issues = []
    if r["latest_fy_basis"] != "filed":
        issues.append("latest_assets_imputed_or_missing")
    if isinstance(r["imputed_metrics_latest"], str) and r["imputed_metrics_latest"]:
        issues.append("imputed:" + r["imputed_metrics_latest"])
    if pd.isna(r["daf_assets_boy"]):
        issues.append("no_prior_year(boy=eoy proxy)")
    if r["accounts_flag"]:
        issues.append(r["accounts_flag"])
    if isinstance(r.get("count_basis_change_flag"), str) and r["count_basis_change_flag"]:
        issues.append("count_basis_change")
    if isinstance(r.get("src_assets"), str) and ("NPT historical" in r["src_assets"] or "paper" in r["src_assets"]):
        issues.append("assets_from_" + r["src_assets"].replace(" ", "_"))
    if r["fy2025_return_no_sched_d_daf"]:
        issues.append("fy2025_return_without_sched_d_daf_values")
    if r.get("daf_gt_total_assets"):
        issues.append("daf_assets_gt_total_assets")
    if pd.notna(r.get("accounts")) and r["accounts"] <= 5 and pd.notna(r["daf_assets_eoy"]) and r["daf_assets_eoy"] / r["accounts"] >= 5e6:
        issues.append("few_accounts_large_balance_suspect_count")
    n = len(issues)
    severe = {"latest_assets_imputed_or_missing", "few_accounts_large_balance_suspect_count"}
    g = "A" if n == 0 else ("B" if n == 1 and not (set(issues) & severe) else ("C" if r["latest_fy_basis"] == "filed" else "D"))
    return g, ";".join(issues)


def build(repo: str, outdir: str) -> dict:
    P_ = paths(repo)
    pf = load_or_write(os.path.join(outdir, "cost-to-serve-parameters.csv"), default_params_frame())
    wf = load_or_write(os.path.join(outdir, "attractiveness-weights.csv"), default_weights_frame())
    P = params_dict(pf)

    dafrc = read(P_["dafrc"])
    corr = read(P_["corr"])
    panel = merge_panel(apply_corrections(dafrc_panel(dafrc), corr),
                        harvest_panel(read(P_["harvest"]), read(P_["refresh"])), read(P_["league"]))
    base = sponsor_base(panel)

    enrich = [latest_cost(read(P_["cost"])), opeff_latest(read(P_["opeff"])), payfte(read(P_["payfte"])),
              longtail_fields(read(P_["longtail"])),
              contractor_vendors(pd.concat([read(P_["contractors"]), read(P_["contractors25"])], ignore_index=True)),
              vendor_map(read(P_["vendormap"])), faith_map(read(P_["faith"])), migrations(read(P_["migrations"])),
              merger_map(corr, read(P_["schedn"], ("filer_ein", "transferee_ein")), read(P_["consolidation"])),
              grant_counts(read(P_["grantcounts"])), fund_totals(read(P_["fundtotals"])), d2d_outbound(read(P_["d2d"])),
              dechomai_share(read(P_["dechomai"])), reclass_flags(read(P_["reclass"])), prospects(read(P_["prospects"])),
              league_flags(read(P_["league"]), read(P_["league25"])), entry_exit(read(P_["entryexit"]))]
    df = base
    for e in enrich:
        df = df.merge(e, on="ein", how="left")
    # add non-DAFRC entities with no Schedule D panel (pass-through / digital) as flagged rows
    extra = []
    for src, key in ((read(P_["passthrough"]), "legal_name"), (read(P_["digital"]), "legal_name")):
        for r in src.drop_duplicates("ein").itertuples():
            if r.ein and r.ein not in set(df["ein"]) and r.ein not in {x["ein"] for x in extra}:
                extra.append({"ein": r.ein, "name": getattr(r, key), "latest_fy_basis": "no_asset_value", "dafrc_type": "",
                              "dafrc_subtype": "", "accounts_flag": "accounts_missing_or_zero", "imputed_metrics_latest": "",
                              "fy2025_return_no_sched_d_daf": False, "latest_fy": np.nan})
    if extra:
        df = pd.concat([df, pd.DataFrame(extra)], ignore_index=True)

    df = df.copy()
    capt = df.apply(lambda r: captive_status(r["ein"], r["name"], r["dafrc_type"], r.get("opeff_segment")), axis=1, result_type="expand")
    df["captive_status"], df["captive_basis"], df["captive_evidence_grade"] = capt[0], capt[1], capt[2]
    df["segment"] = df.apply(segment_of, axis=1)
    df["related_group_id"] = df["ein"].map({e: g for g, (es, _) in RELATED_GROUPS.items() for e in es}).fillna("")
    df["related_group_basis"] = df["related_group_id"].map({g: b for g, (_, b) in RELATED_GROUPS.items()}).fillna("")

    # status
    def status(r):
        if isinstance(r.get("merge_kind"), str) and r["merge_kind"] in ("terminated_transfer", "liquidation_transfer"):
            return "merged_or_dissolved"
        if isinstance(r.get("exit_outcome_tier"), str) and r["exit_outcome_tier"].startswith("A_"):
            return "dissolved_or_converted"
        if pd.isna(r["latest_fy"]):
            return "no_schedule_d_panel"
        if r["latest_fy"] < P["addressable_min_latest_fy"]["base"]:
            return "inactive_no_recent_data"
        if pd.notna(r["daf_assets_eoy"]) and r["daf_assets_eoy"] <= 0:
            return "no_daf_assets_reported"
        if isinstance(r.get("exit_outcome_tier"), str) and r["exit_outcome_tier"].startswith("B_"):
            return "stopped_reporting_dafs"
        return "active"
    df["status"] = df.apply(status, axis=1)

    # assets, balances, flows
    df["avg_assets_proxy"] = np.where(df["daf_assets_boy"].notna(), (df["daf_assets_boy"] + df["daf_assets_eoy"]) / 2, df["daf_assets_eoy"])
    df["avg_assets_proxy_basis"] = np.where(df["daf_assets_boy"].notna(), "[D] (BOY=prior-year EOY + EOY)/2; PROXY for average billable AUA",
                                            "[D] EOY only (no prior year) - PROXY")
    df["avg_balance_eoy"] = df["daf_assets_eoy"] / df["accounts"]
    df["avg_balance_proxy"] = df["avg_assets_proxy"] / df["accounts"]
    df["payout_rate_boy"] = df["grants"] / df["daf_assets_boy"]
    df["payout_rate_avg_proxy"] = df["grants"] / df["avg_assets_proxy"]
    df["grants_per_account_usd"] = df["grants"] / df["accounts"]
    df["contributions_per_account_usd"] = df["contributions"] / df["accounts"]
    df["daf_to_daf_share_of_grants"] = np.where(df["daf_to_daf_fy"] == df["latest_fy"], df["daf_to_daf_outbound_usd"] / df["grants"], np.nan)
    ta = df["total_assets_eoy_990"].where(df["total_assets_eoy_990"].notna(), df["total_assets_eoy_cost"])
    df["total_assets_eoy"] = ta
    df["daf_share_of_total_assets"] = (df["daf_assets_eoy"] / ta).where(ta > 0)
    df["daf_gt_total_assets"] = df["daf_share_of_total_assets"] > 1.05
    df["non_daf_assets_indicator"] = (ta - df["daf_assets_eoy"]).where(ta > 0)
    df = df.copy()
    thr = P["nondaf_share_threshold"]["base"]
    df["flag_nondaf_complex"] = ((df["daf_share_of_total_assets"] < thr) & ~df["segment"].str.startswith(("national", "digital", "donation"))
                                 | (df["other_funds_count_sched_d"].fillna(0) > 0) & (df["other_funds_value_sched_d"].fillna(0) > 0.5 * df["daf_assets_eoy"].fillna(0))
                                 | (df["total_funds_990"].fillna(0) > 2 * df["accounts_reported"].fillna(1e18))).astype(int)
    df["flag_faith"] = (df["segment"].eq("faith") | df["faith_platform_family"].notna()).astype(int)
    df["flag_international"] = df["ein"].isin(INTERNATIONAL_EINS.keys()).astype(int) | df["name"].fillna("").str.upper().str.contains(r"\bINTERNATIONAL\b|\bGLOBAL\b").astype(int)
    df["flag_complex_assets"] = ((df["dechomai_share_contrib_max"].fillna(0) >= P["complex_asset_share_threshold"]["base"])
                                 | df["related_group_id"].eq("RG-DECHOMAI")).astype(int)
    df["flag_pass_through"] = df["segment"].eq("donation_processor_pass_through").astype(int)
    df["complexity_flags"] = df.apply(lambda r: ";".join(k for k in ("nondaf_complex", "faith", "international", "complex_assets", "pass_through") if r["flag_" + k]), axis=1)
    dq = df.apply(data_quality, axis=1, result_type="expand")
    df["data_quality"], df["data_quality_issues"] = dq[0], dq[1]

    # accounts for cost: screened, else EOY / segment median balance [E]
    med = (df[df["accounts"].notna() & (df["status"] == "active")].assign(b=lambda x: x["daf_assets_eoy"] / x["accounts"])
             .groupby("segment")["b"].median())
    df["segment_median_balance"] = df["segment"].map(med)
    est = df["daf_assets_eoy"] / df["segment_median_balance"]
    df["accounts_for_cost"] = df["accounts"].where(df["accounts"].notna(), est.round(0).where(df["daf_assets_eoy"] > 0))
    df["accounts_basis"] = np.where(df["accounts"].notna(), "[S] Schedule D count (screened)",
                                    np.where(df["accounts_for_cost"].notna(), "[E] EOY / segment median balance", ""))

    # vendor & migration resolution
    vr = df.apply(vendor_resolution, axis=1, result_type="expand")
    df = pd.concat([df, vr], axis=1)
    df["migration_months_ago"] = df["mig_date_parsed"].map(months_before_asof)
    df["recent_migration"] = df["migration_months_ago"].le(P["recent_migration_months"]["base"]).fillna(False).astype(bool)
    df["contractual_constraint_signals"] = df.apply(lambda r: "; ".join(x for x in [
        r["captive_basis"] if r["captive_status"] != "none_found" else "",
        f"recent migration to {r['mig_to']} ({r['mig_date']}) - new contract likely [A]" if r["recent_migration"] else "",
        "governance: management delegated (opeff gov_vi3_delegated_mgmt)" if "gov_vi3_delegated_mgmt" in str(r.get("affiliate_evidence")) else "",
        "affiliate-staffed (opeff)" if r.get("staffing_model") == "affiliate_staffed" and r["captive_status"] == "none_found" else "",
    ] if x), axis=1)
    df["buying_signals"] = df.apply(lambda r: "; ".join(x for x in [
        f"{r['prospect_id']}: {r['prospect_challenges']}" if isinstance(r.get("prospect_id"), str) else "",
        f"platform change {r['mig_from']} -> {r['mig_to']} ({r['mig_date']}, conf {r['mig_date_confidence']})" if isinstance(r.get("mig_to"), str) and r["mig_to"] else "",
    ] if x), axis=1)

    df = economics(df, P)
    df["size_band"] = df["daf_assets_eoy"].map(size_band)
    df["flag_small_account_tail"] = df["avg_balance_eoy"] < P["small_account_balance_usd"]["base"]
    df["flag_high_value_concentrated"] = df["avg_balance_eoy"] >= P["high_value_balance_usd"]["base"]
    df["addressable"] = (df["status"].eq("active") & df["daf_assets_eoy"].gt(0)
                         & ~df["captive_status"].isin(["captive_inhouse_affiliate", "vendor_captive", "inhouse_platform_app_native"]))
    df["addressable_exclusion_reason"] = df.apply(lambda r: "" if r["addressable"] else (
        f"status={r['status']}" if r["status"] != "active" else (f"captive={r['captive_status']}" if r["captive_status"] in ("captive_inhouse_affiliate", "vendor_captive", "inhouse_platform_app_native") else "no positive DAF assets")), axis=1)
    df["source_files"] = "dafrc-sponsor-schedule-d-fy2019-2024.csv+dafrc-corrections-itemized.csv; form990 harvests; see src_* columns"
    df = df.sort_values("ein").reset_index(drop=True)

    # ---------------- scoring (addressable only)
    A = df[df["addressable"]].copy()
    S = A.apply(lambda r: dim_scores(r, P), axis=1, result_type="expand")
    A = pd.concat([A, S], axis=1)
    topn = int(P["top_n_hypotheses"]["base"])
    A, sens = sensitivity(A, wf, topn)
    A = A.sort_values(["rank_base", "ein"]).reset_index(drop=True)

    write_outputs(df, A, wf, pf, P, sens, outdir, repo, P_)
    return sens


# --------------------------------------------------------------------------------------------------------- outputs
ECON_COLS = [
    "ein", "name", "name_variants", "segment", "dafrc_type", "dafrc_subtype", "sponsor_category", "size_band", "status",
    "merged_into", "merged_into_name", "merge_kind", "merge_year", "merge_basis", "related_group_id", "related_group_basis",
    "dafrc_operating_status", "exit_kind", "exit_fy", "exit_outcome", "first_fy", "latest_fy", "latest_fy_basis", "latest_tax_period_end",
    "latest_return_object_id", "prior_fy", "daf_assets_boy", "daf_assets_eoy", "avg_assets_proxy", "avg_assets_proxy_basis",
    "accounts_reported", "accounts", "accounts_flag", "accounts_for_cost", "accounts_basis", "prior_accounts",
    "avg_balance_eoy", "avg_balance_proxy", "contributions", "prior_contributions", "grants", "prior_grants",
    "payout_rate_boy", "payout_rate_avg_proxy", "grants_per_account_usd", "contributions_per_account_usd",
    "grant_count_published", "grant_count_unit", "grant_count_period", "grant_count_period_match", "grant_count_used", "grant_count_basis",
    "contribution_count_est", "assets_cagr_3y", "assets_yoy_vol", "assets_yoy_min", "n_yoy_obs", "contributions_cv",
    "total_assets_eoy", "daf_share_of_total_assets", "non_daf_assets_indicator", "other_funds_count_sched_d", "other_funds_value_sched_d",
    "total_funds_990", "total_funds_fy", "daf_to_daf_outbound_usd", "daf_to_daf_fy", "daf_to_daf_share_of_grants",
    "dechomai_share_contrib_max", "complexity_flags", "cost_fy", "employees", "outside_services_l11", "it_l14", "it_part_ix_latest_990",
    "staff_cost_l5_10", "operating_cost_ex_invest_mgmt", "sponsor_daf_opex_per_account_alloc_990", "sponsor_daf_opex_bps_grants_alloc_990",
    "loaded_cost_per_head_payfte", "staffing_model", "affiliate_evidence",
    "tech_vendor", "tech_vendor_confidence", "tech_vendor_evidence", "tech_vendor_all_signals", "admin_provider",
    "vendor990_lines", "vendor990_it_services_lines", "vendor990_daf_vendor_usd_latest", "mig_from", "mig_to", "mig_date",
    "mig_date_confidence", "mig_source", "recent_migration", "captive_status", "captive_basis", "captive_evidence_grade",
    "contractual_constraint_signals", "buying_signals", "donor_fee_bps_at_100k_context",
] + [f"rev_{b}bps_avg_proxy" for b in BPS_LIST] + [
    "rev_20bps_eoy_runrate", "cost_to_serve_low", "cost_to_serve_base", "cost_to_serve_high", "uplift_base", "cost_per_account_base",
    "breakeven_bps_base", "margin_15bps_base", "margin_20bps_base", "margin_25bps_base", "margin_20bps_low_cost", "margin_20bps_high_cost",
    "margin_pct_20bps_base", "onboarding_cost_low", "onboarding_cost_base", "onboarding_cost_high", "onboarding_payback_years_base",
    "concentration_share_of_X", "rev_20bps_after_shock", "margin_20bps_after_shock_base", "self_sustain_coverage_ratio",
    "self_sustaining_base", "self_sustaining_low_cost", "self_sustaining_high_cost", "self_sustaining_after_shock",
    "flag_small_account_tail", "flag_high_value_concentrated", "addressable", "addressable_exclusion_reason",
    "data_quality", "data_quality_issues", "src_assets", "src_accounts", "src_contributions", "src_grants", "corr_rules_latest",
    "imputed_metrics_latest", "league_override_latest", "league_corrections", "league_imputed_kept", "league25_flags",
    "league25_change_vs_as_built", "count_basis_change_flag", "fy_list", "source_files",
]
DIM_COLS = ["s_" + d[0] for d in DIMENSIONS]


def tidy(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in out.columns:
        if pd.api.types.is_bool_dtype(out[c]):
            out[c] = out[c].map({True: "1", False: "0"})
        elif pd.api.types.is_float_dtype(out[c]):
            s = out[c]
            md = s.abs().median()
            keys = ("s_", "score", "share", "payout", "margin_pct", "cagr", "yoy", "_cv", "concentration", "uplift",
                    "coverage", "dechomai", "per_musd", "payback", "breakeven_bps", "bps_grants")
            if c.startswith(keys) or any(k in c for k in keys[1:]) or (pd.notna(md) and md < 100):
                out[c] = s.round(4)
            else:
                out[c] = s.round(0)
    return out


def write_csv(df: pd.DataFrame, path: str):
    tidy(df).to_csv(path, index=False, lineterminator="\n", float_format="%.10g")


def write_outputs(df, A, wf, pf, P, sens, outdir, repo, P_):
    write_csv(df[ECON_COLS], os.path.join(outdir, "sponsor-economics.csv"))
    ca_cols = (["rank_base", "score_base", "ein", "name", "segment", "size_band", "latest_fy", "daf_assets_eoy", "avg_assets_proxy",
                "accounts_for_cost", "accounts_basis", "avg_balance_eoy", "rev_20bps_avg_proxy", "cost_to_serve_base", "margin_20bps_base",
                "margin_pct_20bps_base", "transactions_per_musd_est", "tech_vendor", "tech_vendor_confidence", "captive_status",
                "recent_migration", "complexity_flags", "data_quality"] + DIM_COLS
               + ["score_equal", "rank_equal", "score_revenue_heavy", "rank_revenue_heavy", "score_risk_heavy", "rank_risk_heavy",
                  "score_cost_heavy", "rank_cost_heavy", "rank_oat_min", "rank_oat_max", "share_oat_runs_in_topn"])
    write_csv(A[ca_cols], os.path.join(outdir, "customer-attractiveness.csv"))

    topn = int(P["top_n_hypotheses"]["base"])
    T = A[~A["recent_migration"] & ~A["captive_status"].isin(["inhouse_platform_custom"]) & A["data_quality"].isin(["A", "B"])].head(topn).copy()
    T["hypothesis_rank"] = np.arange(1, len(T) + 1)
    T["why_attractive"] = T.apply(lambda r: "; ".join(f"{d}={r['s_' + d]:.2f}" for d in sorted(
        [x[0] for x in DIMENSIONS], key=lambda d: -r["s_" + d] * float(wf.set_index("dimension").at[d, "base"]))[:4]), axis=1)
    T["main_uncertainties"] = T.apply(lambda r: "; ".join(x for x in [
        "avg AUA is a (BOY+EOY)/2 proxy, not billable average" ,
        f"accounts {r['accounts_basis']}" if r["accounts_basis"].startswith("[E]") else "",
        f"grant count {('published' if pd.notna(r['grant_count_published']) else 'assumed per account')}",
        "tech vendor unknown" if r["tech_vendor"] == "unknown" else f"vendor evidence: {r['tech_vendor_confidence']}",
        f"data quality {r['data_quality']}: {r['data_quality_issues']}" if r["data_quality"] != "A" else "",
        "cost-to-serve parameters are [A] placeholders", "willingness to outsource / buy unknown (no outreach)",
    ] if x), axis=1)
    T["reasons_to_doubt"] = T.apply(lambda r: "; ".join(x for x in [
        "non-DAF fund complexity" if r["flag_nondaf_complex"] else "",
        f"captive/affiliate: {r['captive_status']}" if r["captive_status"] != "none_found" else "",
        f"margin after 30% shock {r['margin_20bps_after_shock_base']:,.0f}" if r["margin_20bps_after_shock_base"] < 0.25 * r["rev_20bps_avg_proxy"] else "",
        f"concentration {r['concentration_share_of_X']:.0%} of $X business" if r["concentration_share_of_X"] > 0.25 else "",
        f"small-account tail (avg ${r['avg_balance_eoy']:,.0f})" if r["flag_small_account_tail"] else "",
        f"rank unstable under weights (OAT {int(r['rank_oat_min'])}-{int(r['rank_oat_max'])})" if r["rank_oat_max"] - r["rank_oat_min"] > 15 else "",
    ] if x), axis=1)
    T["evidence"] = T.apply(lambda r: f"Schedule D FY{int(r['latest_fy'])} ({r['src_assets']}); vendor: {r['tech_vendor_evidence'][:180]}; signals: {str(r['buying_signals'])[:180]}", axis=1)
    T["label"] = "HYPOTHESIS for desk validation - NOT a sales lead; no willingness-to-pay or mandate inferred"
    tcols = ["hypothesis_rank", "rank_base", "score_base", "ein", "name", "segment", "size_band", "latest_fy", "daf_assets_eoy",
             "avg_assets_proxy", "accounts_for_cost", "avg_balance_eoy", "rev_20bps_avg_proxy", "rev_20bps_eoy_runrate",
             "cost_to_serve_low", "cost_to_serve_base", "cost_to_serve_high", "margin_20bps_base", "margin_pct_20bps_base",
             "margin_20bps_after_shock_base", "onboarding_cost_base", "onboarding_payback_years_base", "concentration_share_of_X",
             "tech_vendor", "tech_vendor_confidence", "captive_status", "complexity_flags", "data_quality",
             "rank_oat_min", "rank_oat_max", "share_oat_runs_in_topn", "rank_equal", "rank_revenue_heavy", "rank_risk_heavy", "rank_cost_heavy",
             "why_attractive", "evidence", "main_uncertainties", "reasons_to_doubt", "label"]
    write_csv(T[tcols], os.path.join(outdir, "top25-hypotheses.csv"))

    F = P["self_sustain_fixed_cost_usd"]["base"]
    SS = df[df["self_sustaining_base"] | df["self_sustaining_high_cost"] | df["self_sustaining_low_cost"]].copy()
    SS = SS.sort_values(["self_sustain_coverage_ratio", "ein"], ascending=[False, True])
    SS["threshold_used"] = f"20 bps on avg-assets proxy minus base cost-to-serve >= self_sustain_fixed_cost_usd = {F:,.0f} [S hypothesis]; parameter in cost-to-serve-parameters.csv"
    sscols = ["ein", "name", "segment", "status", "addressable", "addressable_exclusion_reason", "captive_status", "recent_migration",
              "daf_assets_eoy", "avg_assets_proxy", "accounts_for_cost", "avg_balance_eoy", "rev_20bps_avg_proxy", "cost_to_serve_base",
              "self_sustain_margin", "self_sustain_coverage_ratio", "self_sustaining_low_cost", "self_sustaining_base",
              "self_sustaining_high_cost", "self_sustaining_after_shock", "concentration_share_of_X", "tech_vendor", "data_quality", "threshold_used"]
    write_csv(SS[sscols], os.path.join(outdir, "self-sustaining-candidates.csv"))

    thr = P["large_aua_threshold_usd"]["base"]
    med_addr = A["score_base"].median()
    big = df[(df["daf_assets_eoy"] >= thr) & df["status"].eq("active")].copy()
    sc = A.set_index("ein")["score_base"]
    big["score_base"] = big["ein"].map(sc)

    def reasons(r):
        out = []
        if not r["addressable"]:
            out.append(f"not addressable: {r['captive_status']} ({r['captive_basis'][:120]})")
        elif r["captive_status"] != "none_found":
            out.append(f"constrained: {r['captive_status']}")
        if r["recent_migration"]:
            out.append(f"recent migration {r['mig_from']} -> {r['mig_to']} ({r['mig_date']})")
        if pd.notna(r["margin_pct_20bps_base"]) and r["margin_pct_20bps_base"] < 0.25:
            out.append(f"base margin at 20 bps {r['margin_pct_20bps_base']:.0%}")
        if r["flag_small_account_tail"]:
            out.append(f"small-account tail: avg balance ${r['avg_balance_eoy']:,.0f}")
        if r["flag_nondaf_complex"]:
            out.append("DAF is minority of total assets / non-DAF fund accounting")
        if r["flag_pass_through"] or r["flag_complex_assets"]:
            out.append("pass-through or complex-asset processing")
        conc = (f"concentration: 20 bps revenue = {r['concentration_share_of_X']:.0%} of $X business (single-client dependency)"
                if r["concentration_share_of_X"] > 0.5 else "")
        if r["platform_custom_or_inhouse"]:
            out.append("custom / in-house platform (migration + integration cost)")
        if pd.notna(r["score_base"]) and r["score_base"] < med_addr:
            out.append(f"attractiveness score {r['score_base']:.1f} below addressable median {med_addr:.1f}")
        return "; ".join(out + ([conc] if conc and out else []))
    big["reasons"] = big.apply(reasons, axis=1)
    U = big[big["reasons"] != ""].sort_values(["daf_assets_eoy", "ein"], ascending=[False, True])
    ucols = ["ein", "name", "segment", "daf_assets_eoy", "accounts_for_cost", "avg_balance_eoy", "rev_20bps_avg_proxy", "cost_to_serve_base",
             "margin_pct_20bps_base", "captive_status", "tech_vendor", "recent_migration", "score_base", "reasons", "data_quality"]
    write_csv(U[ucols], os.path.join(outdir, "unattractive-large.csv"))

    # segment summary
    act = df[df["status"].eq("active") & df["daf_assets_eoy"].gt(0)]

    def summarise(g, key, val):
        acc = g["accounts"]
        withacc = g[acc.notna()]
        return {
            "dimension": key, "group": val, "n_sponsors": len(g), "n_addressable": int(g["addressable"].sum()),
            "daf_assets_eoy_sum": g["daf_assets_eoy"].sum(), "avg_assets_proxy_sum": g["avg_assets_proxy"].sum(),
            "accounts_sum_screened": withacc["accounts"].sum(), "n_with_accounts": len(withacc),
            "accounts_for_cost_sum": g["accounts_for_cost"].sum(),
            "pooled_avg_balance_eoy": withacc["daf_assets_eoy"].sum() / withacc["accounts"].sum() if withacc["accounts"].sum() else np.nan,
            "median_sponsor_avg_balance": (withacc["daf_assets_eoy"] / withacc["accounts"]).median(),
            "contributions_sum": g["contributions"].sum(), "grants_sum": g["grants"].sum(),
            "pooled_payout_boy": g["grants"].sum() / g["daf_assets_boy"].sum() if g["daf_assets_boy"].sum() else np.nan,
            "rev_20bps_avg_proxy_sum": g["rev_20bps_avg_proxy"].sum(), "cost_to_serve_base_sum": g["cost_to_serve_base"].sum(),
            "margin_20bps_base_sum": g["margin_20bps_base"].sum(),
            "margin_pct_20bps_base_pooled": g["margin_20bps_base"].sum() / g["rev_20bps_avg_proxy"].sum() if g["rev_20bps_avg_proxy"].sum() else np.nan,
            "n_positive_margin_20bps_base": int((g["margin_20bps_base"] > 0).sum()),
            "n_self_sustaining_base": int(g["self_sustaining_base"].sum()),
            "n_small_account_tail": int(g["flag_small_account_tail"].sum()), "n_high_value_concentrated": int(g["flag_high_value_concentrated"].sum()),
            "median_breakeven_bps_base": g["breakeven_bps_base"].median(), "median_cost_per_account_base": g["cost_per_account_base"].median(),
            "median_assets_cagr_3y": g["assets_cagr_3y"].median(), "median_assets_yoy_vol": g["assets_yoy_vol"].median(),
            "median_employees": g["employees"].median(), "median_it_l14": g["it_l14"].median(),
            "median_sponsor_daf_opex_per_account_alloc_990": g["sponsor_daf_opex_per_account_alloc_990"].median(),
            "median_sponsor_daf_opex_bps_grants_alloc_990": g["sponsor_daf_opex_bps_grants_alloc_990"].median(),
        }
    rows = [summarise(act, "all_active", "all")]
    rows += [summarise(g, "segment", k) for k, g in act.groupby("segment", sort=True)]
    rows += [summarise(g, "size_band", k) for k, g in act.groupby("size_band", sort=True)]
    rows += [summarise(g, "captive_status", k) for k, g in act.groupby("captive_status", sort=True)]
    rows += [summarise(act[act["addressable"]], "addressable", "addressable_all")]
    write_csv(pd.DataFrame(rows), os.path.join(outdir, "segment-summary.csv"))

    write_jsonl_aux(df, A, P, pf, sens, outdir, repo, P_)


def balance_distribution(df: pd.DataFrame) -> list:
    act = df[df["status"].eq("active") & df["accounts"].notna() & df["daf_assets_eoy"].gt(0)].copy()
    bands = [(0, 1e4, "<10k"), (1e4, 5e4, "10k-50k"), (5e4, 2.5e5, "50k-250k"), (2.5e5, 1e6, "250k-1m"), (1e6, 5e6, "1m-5m"), (5e6, 1e18, ">=5m")]
    tot_a, tot_n = act["daf_assets_eoy"].sum(), act["accounts"].sum()
    out = []
    for lo, hi, lab in bands:
        g = act[(act["avg_balance_eoy"] >= lo) & (act["avg_balance_eoy"] < hi)]
        out.append({"sponsor_avg_balance_band": lab, "n_sponsors": int(len(g)), "accounts": float(g["accounts"].sum()),
                    "share_accounts": round(float(g["accounts"].sum() / tot_n), 4), "daf_assets_eoy": float(g["daf_assets_eoy"].sum()),
                    "share_assets": round(float(g["daf_assets_eoy"].sum() / tot_a), 4),
                    "n_addressable": int(g["addressable"].sum()),
                    "n_positive_margin_20bps_base": int((g["margin_20bps_base"] > 0).sum())})
    return out


def concentration_stats(df: pd.DataFrame) -> dict:
    act = df[df["status"].eq("active") & df["daf_assets_eoy"].gt(0)].sort_values("daf_assets_eoy", ascending=False)
    addr = act[act["addressable"]]
    tot = act["daf_assets_eoy"].sum()
    res = {f"top{k}_share_assets_active": round(float(act.head(k)["daf_assets_eoy"].sum() / tot), 4) for k in (4, 10, 50)}
    res.update({f"addressable_top{k}_share_of_addressable_assets": round(float(addr.head(k)["daf_assets_eoy"].sum() / addr["daf_assets_eoy"].sum()), 4) for k in (10, 50)})
    res["captive_inhouse_share_assets_active"] = round(float(act[act["captive_status"].eq("captive_inhouse_affiliate")]["daf_assets_eoy"].sum() / tot), 4)
    res["not_addressable_share_assets_active"] = round(float(act[~act["addressable"]]["daf_assets_eoy"].sum() / tot), 4)
    res["n_addressable_positive_margin_20bps_base"] = int((addr["margin_20bps_base"] > 0).sum())
    res["n_addressable_self_sustaining_base_excl_recent_migration_and_constrained"] = int(
        (addr["self_sustaining_base"] & ~addr["recent_migration"] & addr["captive_status"].eq("none_found")).sum())
    res["addressable_assets_with_positive_margin_share"] = round(float(addr[addr["margin_20bps_base"] > 0]["daf_assets_eoy"].sum() / addr["daf_assets_eoy"].sum()), 4)
    res["min_eoy_assets_positive_margin_base_cf"] = float(act[(act["segment"] == "community_foundation") & (act["margin_20bps_base"] > 0)]["daf_assets_eoy"].min())
    res["median_eoy_assets_at_breakeven_band_cf_10_30m_positive_share"] = round(float(
        (act[(act["segment"] == "community_foundation") & act["daf_assets_eoy"].between(1e7, 3e7)]["margin_20bps_base"] > 0).mean()), 4)
    return res


def write_jsonl_aux(df, A, P, pf, sens, outdir, repo, P_):
    ev = []
    i = 0

    def add(**k):
        nonlocal i
        i += 1
        ev.append({"evidence_id": f"EV-SPN-{i:03d}", "accessed": ASOF, **k})
    for key, p in sorted(P_.items()):
        add(claim=f"Input dataset used: {key}", value=os.path.basename(p), unit="file", source_url_or_path=rel(repo, p),
            source_type="repo", filing_period="see file", quality="B", notes="Repository dataset; values inside are graded per row in outputs")
    gc = df[df["grant_count_published"].notna()]
    for r in gc.sort_values("ein").itertuples():
        add(claim=f"Sponsor-published DAF grant count, {r.name}", value=str(int(r.grant_count_published)), unit=str(r.grant_count_unit),
            source_url_or_path="data/mission-2026-11-14/grant-count-denominators-2026-11-20.csv", source_type="repo",
            filing_period=str(r.grant_count_period), quality="A" if r.grant_count_period_match == "yes" else "B",
            notes=f"period_match={r.grant_count_period_match}; used as grant count (never Schedule I rows)")
    mg = df[df["mig_to"].notna()]
    for r in mg.sort_values("ein").itertuples():
        add(claim=f"Platform change {r.name}: {r.mig_from} -> {r.mig_to}", value=str(r.mig_date), unit="date",
            source_url_or_path=str(r.mig_source), source_type="repo", filing_period=str(r.mig_date), quality="B" if "cf-vendor" in str(r.mig_source) else "C",
            notes=f"date confidence {r.mig_date_confidence}")
    cp = df[df["captive_status"] != "none_found"]
    for r in cp.sort_values("ein").itertuples():
        add(claim=f"Captive/affiliate status {r.name}", value=r.captive_status, unit="class", source_url_or_path=r.captive_basis[:200],
            source_type="repo", filing_period="2021-2026", quality=r.captive_evidence_grade or "D", notes="classification by SPN from repo evidence")
    mm = df[df["merge_kind"].isin(["terminated_transfer", "liquidation_transfer"])]
    for r in mm.sort_values("ein").itertuples():
        add(claim=f"Sponsor merged/dissolved: {r.name} -> {r.merged_into_name}", value=str(r.merged_into), unit="EIN",
            source_url_or_path=str(r.merge_basis)[:240], source_type="990", filing_period=str(r.merge_year), quality="A", notes="Schedule N / final return as recorded in repo")
    with open(os.path.join(outdir, "evidence.jsonl"), "w") as f:
        for e in ev:
            f.write(json.dumps(e, sort_keys=False) + "\n")
    with open(os.path.join(outdir, "assumptions.jsonl"), "w") as f:
        for n, r in enumerate(pf.itertuples(), 1):
            f.write(json.dumps({"assumption_id": f"A-SPN-{n:03d}", "statement": f"{r.parameter}: {r.basis}", "value": str(r.base),
                                "unit": r.unit, "low": str(r.low), "high": str(r.high), "basis": f"{r.label} SPN placeholder; replace with activity-cost agent value",
                                "evidence_ids": [], "sensitivity": "high" if r.parameter in ("per_account_usd", "grants_per_account", "fixed_per_sponsor_usd", "self_sustain_fixed_cost_usd") else "medium"}) + "\n")
    # calibration of grants per account [D]
    cal = df[df["grant_count_published"].notna() & df["accounts"].notna()]
    calib = sorted([(r.name, round(r.grant_count_published / r.accounts, 2)) for r in cal.itertuples()], key=lambda x: x[1])
    stats = {"sensitivity": sens, "grant_count_calibration_grants_per_account": calib,
             "n_sponsors_total": int(len(df)), "n_active": int(df["status"].eq("active").sum()), "n_addressable": int(df["addressable"].sum()),
             "status_counts": df["status"].value_counts().sort_index().to_dict(),
             "latest_fy_counts": df["latest_fy"].value_counts().sort_index().rename(lambda x: str(int(x)) if pd.notna(x) else "na").to_dict(),
             "data_quality_counts": df["data_quality"].value_counts().sort_index().to_dict(),
             "captive_counts": df["captive_status"].value_counts().sort_index().to_dict(),
             "balance_distribution": balance_distribution(df), "concentration": concentration_stats(df)}
    with open(os.path.join(outdir, "summary-stats.json"), "w") as f:
        json.dump(stats, f, indent=1, sort_keys=True, default=str)
        f.write("\n")


if __name__ == "__main__":
    repo_ = sys.argv[1] if len(sys.argv) > 1 else "/home/user/daf-landscape"
    out_ = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
    s = build(repo_, out_)
    print(json.dumps(s, indent=1))
