"""COM part 1: sponsor value and pricing-structure economics.

Pure functions over repository CSVs (read-only). Writes sponsor-value.csv and
pricing-structures.csv to the output directory given as argv[1].
Run: python3 -I -B sponsor_value.py <outdir>
"""
import math
import sys

import pandas as pd

R = "/home/user/daf-landscape/data"
SE = f"{R}/commercial-opportunity/servicing-economics"
MS = f"{R}/mission-2026-11-14"

# ---------------------------------------------------------------- assumptions
# Replaceable (equivalent-scope) share of DAF-allocated opex, by service group [A]
# (low, base, high). Basis in assumptions.jsonl A-COM-003.
REPL_SHARE = {
    "outsourced_0emp": (0.70, 0.80, 0.90),
    "independent_national": (0.40, 0.55, 0.70),
    "faith": (0.30, 0.45, 0.60),
    "community_foundation": (0.15, 0.30, 0.45),
    "affiliate_inhouse": (0.45, 0.60, 0.75),
    "other": (0.30, 0.45, 0.60),
}
# Realisation factor: realised donor-fee bps / published schedule bps at the mean balance [E]
REAL_FACTOR = (0.40, 0.60, 0.75)
# Headline schedule bps where the sponsor's own schedule is not in the repo [A]
DEFAULT_HEADLINE_BPS = {
    "community_foundation": 90.0, "independent_national": 60.0, "faith": 60.0,
    "affiliate_inhouse": 60.0, "outsourced_0emp": 60.0, "other": 75.0,
}
CONV_USD_PER_ACCT = {"typical": 217.13, "market_mix": 262.36, "high_value": 466.83}  # [S] capacity-model.csv conventional
MGMT_OVERHEAD = 1.35        # [A] supervision, occupancy, QA on top of incremental conventional labour/external
SPONSOR_LEVEL_USD = 100_000  # [A] close, audit support, governance reporting (ACT-S01/S04/S05) conventional
SW_FLOOR_USD = 150_000       # [S-derived] Ren/Stellar small-client floor $118-175k (report 01)
SW_BPS = 3.0                 # [A] mid of software-only band 0.5-9 bps
OVERSIGHT_FIXED = 60_000     # [A] sponsor vendor management + reserved decisions after outsourcing
OVERSIGHT_PER_ACCT = 7.5     # [D] 7.0 sponsor-retained min/acct-yr (capacity-model market_mix) x $61.35/h (CF_1BN rate)
MIGRATION_FIXED = 150_000    # [A] sponsor-side migration effort (data cleanup, comms, parallel run)
MIGRATION_PER_ACCT = 20.0    # [A]
AMORT_YEARS = 5              # [A]

STRUCTURES = {
    "S1_flat_20bps": "0.0020 x average billable assets (payout-neutral: approved-unpaid grants excluded)",
    "S2_per_account_737": "$737 x accounts (Ren at MS GIFT realised per-account price)",
    "S3_per_account_150_plus_7.5bps": "$150 x accounts + 0.00075 x assets (report 05 cost-reflective centre)",
    "S4_tiered_bps_floor": "marginal on sponsor AUA: 20 bps to $500M, 12 bps $0.5-2B, 6 bps above $2B; floor $250/account",
    "S5_value_share_50pct": "max(servicer AI-native high-case cost, 50% x equivalent-scope avoided cost)",
    "S6_per_account_350_plus_3bps_cap20": "min($350 x accounts + 0.0003 x assets, 0.0020 x assets) (per-account-led hybrid, capped at 20 bps)",
}


def interp_bps(b, p100k, p1m, p10m):
    """Log-balance interpolation of a schedule's effective bps at balance b."""
    pts = [(1e5, p100k), (1e6, p1m), (1e7, p10m)]
    pts = [(x, y) for x, y in pts if pd.notna(y)]
    if not pts:
        return float("nan")
    if b <= pts[0][0]:
        return pts[0][1]
    if b >= pts[-1][0]:
        return pts[-1][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= b <= x1:
            t = (math.log(b) - math.log(x0)) / (math.log(x1) - math.log(x0))
            return y0 + t * (y1 - y0)
    return pts[-1][1]


def tiered_price(a, n):
    tiers = [(0, 5e8, 0.0020), (5e8, 2e9, 0.0012), (2e9, float("inf"), 0.0006)]
    p = sum(max(0.0, min(a, hi) - lo) * r for lo, hi, r in tiers)
    return max(p, 250.0 * n)


def service_group(row):
    if row.get("employees", 1) == 0 and pd.notna(row.get("vendor990_daf_vendor_usd_latest")) and row.get("vendor990_daf_vendor_usd_latest", 0) > 0:
        return "outsourced_0emp"
    seg = row["segment"]
    if seg == "community_foundation":
        return "community_foundation"
    if seg == "national_independent":
        return "independent_national"
    if seg == "faith":
        return "faith"
    if seg in ("national_financial_affiliate", "national_vendor_affiliated"):
        return "affiliate_inhouse"
    return "other"


def balance_archetype(b):
    return "typical" if b < 250_000 else ("market_mix" if b < 1_000_000 else "high_value")


def load():
    se = pd.read_csv(f"{SE}/sponsor-economics.csv", low_memory=False)
    sme = pd.read_csv(f"{SE}/sponsor-model-economics.csv")
    fr = pd.read_csv(f"{MS}/sponsor-fee-revenue-margin-2026-11-19.csv")
    cen = pd.read_csv(f"{MS}/cf-daf-fee-census-2026.csv")
    eff = pd.read_csv(f"{MS}/sponsor-operating-efficiency-2026-11-20.csv", low_memory=False)
    return se, sme, fr, cen, eff


def realised_fee_table(fr):
    f = fr[fr.internal_fee_bps_of_avg_daf_value.notna()].sort_values("fiscal_year").groupby("ein").tail(1)
    return {int(r.ein): (float(r.internal_daf_fee_usd), float(r.internal_fee_bps_of_avg_daf_value), int(r.fiscal_year), r.fee_recognition)
            for r in f.itertuples()}


def census_table(cen):
    c = cen[cen.admin_bps_100k.notna() | cen.admin_bps_1000k.notna()]
    return {int(r.ein): (r.admin_bps_100k, r.admin_bps_1000k, r.admin_bps_10000k, r.source_url) for r in c.itertuples() if pd.notna(r.ein)}


# national schedules from sponsor-fee-schedules.csv expressed as 100k/1M/10M bps [D]
NATIONAL_SCHED = {
    341747398: (70.0, 70.0, 70.0, "sponsor-fee-schedules.csv AEF 0.70% headline (tiers not published)"),
    527082731: (27.0, 27.0, 18.9, "price-observations.csv PRC-O-004 MS GIFT TPA 27->9 bps (TPA only; excludes MSSB 7 bps)"),
    46010342: (90.0, 66.0, 25.6, "sponsor-fee-schedules.csv BofA CGF 0.90/0.75/0.50/... marginal [D]"),
    352129262: (65.0, 50.0, 26.5, "sponsor-fee-schedules.csv RCF 0.65/0.35/0.25/0.20 marginal [D]"),
    232888152: (60.0, 45.0, 14.6, "sponsor-fee-schedules.csv Vanguard Charitable 0.60/0.30/0.12/0.10 [D]"),
    110303001: (60.0, 45.0, 21.0, "sponsor-fee-schedules.csv Fidelity 0.60/0.30/0.20/0.15 [D]"),
    311640316: (60.0, 45.0, 21.0, "sponsor-fee-schedules.csv DAFgiving360 0.60/0.30/0.20/0.15 [D]"),
}


def eff_latest(eff):
    e = eff[eff.record_type == "sponsor_year"].sort_values("fy").groupby("ein").tail(1)
    return {int(r.ein): (r.advertising_l12 if pd.notna(r.advertising_l12) else 0.0,
                         r.fees_prof_fundraising_l11e if pd.notna(r.fees_prof_fundraising_l11e) else 0.0) for r in e.itertuples()}


def fee_revenue(row, rf, cen, grp, a, b):
    ein = int(row["ein"])
    if ein in rf:
        usd, bps, fy, rec = rf[ein]
        return usd, usd, usd, f"[S] realised internal DAF fee FY{fy} ({rec}) sponsor-fee-revenue-margin-2026-11-19.csv; {bps} bps", "realised"
    if grp == "outsourced_0emp":
        # 0-employee pass-through: donor fees fund the vendor + small GOE; fee revenue ~ opex [A]
        op = row["operating_cost_ex_invest_mgmt"] * row["daf_share_of_total_assets"]
        extra = ""
        if ein == 527082731:
            extra = "; MS GIFT donors also pay MSSB 7 bps admin outside the sponsor (price-observations PRC-O-004)"
        return op * 0.95, op, op * 1.05, f"[A] fee revenue ~= DAF opex for 0-employee pass-through sponsor{extra}", "pass_through_assumed"
    if ein in NATIONAL_SCHED:
        p = NATIONAL_SCHED[ein]
        src = p[3]
    elif ein in cen:
        p = cen[ein]
        src = f"cf-daf-fee-census-2026.csv {p[3]}"
    else:
        h = DEFAULT_HEADLINE_BPS[grp]
        p = (h, h, h * 0.6)
        src = f"[A] default headline {h} bps for {grp} (no schedule in repo)"
    head = interp_bps(b, p[0], p[1], p[2])
    lo, base, hi = (a * head * f / 1e4 for f in REAL_FACTOR)
    return lo, base, hi, f"[E] schedule {head:.1f} bps at mean balance x realisation {REAL_FACTOR}; {src}", "schedule_estimated"


def row_economics(row, ctx):
    rf, cen, effd, smed = ctx
    a = float(row["avg_assets_proxy"])
    n = float(row["accounts_for_cost"])
    b = a / n
    grp = service_group(row)
    ein = int(row["ein"])
    adv, fund = effd.get(ein, (0.0, 0.0))
    share = float(row["daf_share_of_total_assets"]) if pd.notna(row["daf_share_of_total_assets"]) else 1.0
    opex_all = float(row["operating_cost_ex_invest_mgmt"]) if pd.notna(row["operating_cost_ex_invest_mgmt"]) else float("nan")
    daf_opex = opex_all * share
    daf_opex_ex_mkt = (opex_all - adv - fund) * share
    fr_lo, fr_base, fr_hi, fr_src, fr_kind = fee_revenue(row, rf, cen, grp, a, b)
    vendor = row.get("vendor990_daf_vendor_usd_latest")
    vendor = float(vendor) if pd.notna(vendor) else 0.0
    rs = REPL_SHARE[grp]
    if grp == "outsourced_0emp":
        td = (vendor, vendor, vendor)
    else:
        td = tuple(daf_opex_ex_mkt * s for s in rs)
    arch = balance_archetype(b)
    sw = max(vendor, SW_FLOOR_USD, SW_BPS * a / 1e4) if grp != "outsourced_0emp" else 0.0
    bu = n * CONV_USD_PER_ACCT[arch] * MGMT_OVERHEAD + SPONSOR_LEVEL_USD + sw
    if grp == "outsourced_0emp":
        bu = vendor
    value = (min(td[0], bu), min(td[1], bu), td[1])  # high = top-down base unbounded by bottom-up
    v = value[1]
    retained = daf_opex - v
    oversight = OVERSIGHT_FIXED + OVERSIGHT_PER_ACCT * n
    migr = (MIGRATION_FIXED + MIGRATION_PER_ACCT * n) / AMORT_YEARS
    sm = smed.get(ein, {})
    svc_cost = sm.get("annual_cost_ai_native_base", float("nan"))
    svc_cost_hi = sm.get("annual_cost_ai_native_high", float("nan"))
    prices = {
        "S1_flat_20bps": 0.002 * a,
        "S2_per_account_737": 737.0 * n,
        "S3_per_account_150_plus_7.5bps": 150.0 * n + 0.00075 * a,
        "S4_tiered_bps_floor": tiered_price(a, n),
        "S5_value_share_50pct": max(svc_cost_hi if pd.notna(svc_cost_hi) else 0.0, 0.5 * v),
        "S6_per_account_350_plus_3bps_cap20": min(350.0 * n + 0.0003 * a, 0.002 * a),
    }
    margin_now = fr_base - daf_opex
    vmax = value[2]
    out = {
        "ein": ein, "name": row["name"], "segment": row["segment"], "service_group": grp,
        "captive_status": row.get("captive_status"), "recent_migration": row.get("recent_migration"),
        "avg_assets_usd": round(a), "accounts": int(n), "avg_balance_usd": round(b), "balance_archetype": arch,
        "employees": row.get("employees"),
        "donor_fee_revenue_low_usd": round(fr_lo), "donor_fee_revenue_base_usd": round(fr_base), "donor_fee_revenue_high_usd": round(fr_hi),
        "donor_fee_revenue_bps_base": round(fr_base / a * 1e4, 1), "donor_fee_revenue_kind": fr_kind, "donor_fee_revenue_basis": fr_src,
        "daf_opex_alloc_usd": round(daf_opex), "daf_opex_ex_marketing_fundraising_usd": round(daf_opex_ex_mkt),
        "daf_opex_bps": round(daf_opex / a * 1e4, 1), "daf_opex_per_account_usd": round(daf_opex / n),
        "current_daf_vendor_payment_usd": round(vendor),
        "replaceable_share_low_base_high": f"{rs[0]}/{rs[1]}/{rs[2]}" if grp != "outsourced_0emp" else "vendor payment",
        "avoided_cost_topdown_base_usd": round(td[1]), "avoided_cost_bottomup_usd": round(bu),
        "value_delivered_low_usd": round(value[0]), "value_delivered_base_usd": round(v), "value_delivered_high_usd": round(value[2]),
        "value_delivered_bps": round(v / a * 1e4, 1), "value_delivered_per_account_usd": round(v / n),
        "sponsor_retained_opex_usd": round(retained), "sponsor_oversight_cost_usd": round(oversight),
        "sponsor_migration_annualised_usd": round(migr),
        "sponsor_margin_now_usd": round(margin_now),
        "servicer_cost_ai_native_base_usd": round(svc_cost) if pd.notna(svc_cost) else "",
        "servicer_cost_ai_native_high_usd": round(svc_cost_hi) if pd.notna(svc_cost_hi) else "",
    }
    out["max_value_price_base_usd"] = round(v - oversight - migr)
    out["max_value_price_base_bps"] = round((v - oversight - migr) / a * 1e4, 1)
    out["max_value_price_base_per_account"] = round((v - oversight - migr) / n)
    out["max_value_price_high_usd"] = round(vmax - oversight - migr)
    out["max_value_price_high_bps"] = round((vmax - oversight - migr) / a * 1e4, 1)
    out["max_value_price_high_per_account"] = round((vmax - oversight - migr) / n)
    for k, p in prices.items():
        out[f"{k}_price_usd"] = round(p)
        out[f"{k}_price_bps"] = round(p / a * 1e4, 1)
        out[f"{k}_price_per_account"] = round(p / n)
        out[f"{k}_sponsor_net_value_usd"] = round(v - oversight - migr - p)
        out[f"{k}_sponsor_net_value_high_usd"] = round(vmax - oversight - migr - p)
        out[f"{k}_sponsor_margin_after_usd"] = round(fr_base - retained - oversight - migr - p)
        out[f"{k}_price_share_of_value"] = round(p / v, 2) if v > 0 else ""
        out[f"{k}_servicer_contribution_usd"] = round(p - svc_cost) if pd.notna(svc_cost) else ""
    out["labels"] = ("avg assets/accounts [S] sponsor-model-economics.csv; opex [S] sponsor-economics.csv x DAF asset share [D]; "
                     "value = min(top-down replaceable opex [A share], bottom-up conventional equivalent-scope cost [D from S capacity-model + A overhead]); "
                     "prices [D] from [A] structures")
    return out


ARCHETYPES = {
    "ARCH-independent-national": lambda d: (d.segment == "national_independent") & d.avg_assets_proxy.between(5e8, 1e10),
    "ARCH-faith-federation": lambda d: (d.segment == "faith") & d.avg_assets_proxy.between(3e8, 5e9),
    "ARCH-large-CF": lambda d: (d.segment == "community_foundation") & (d.avg_assets_proxy >= 1e9),
    "ARCH-mid-CF": lambda d: (d.segment == "community_foundation") & d.avg_assets_proxy.between(2.5e8, 1e9),
    "ARCH-advisor-program": lambda d: d.captive_status.isin(["financial_affiliate_vendor_outsourced", "financial_affiliate_unknown_platform", "financial_affiliate_name_inferred"]) & d.avg_assets_proxy.between(3e8, 1.2e10),
}


def archetype_row(name, sub, ctx):
    """Median-input archetype: medians of assets, accounts, opex inputs; segment of the mode."""
    med = sub[["avg_assets_proxy", "accounts_for_cost", "operating_cost_ex_invest_mgmt", "daf_share_of_total_assets", "employees",
               "vendor990_daf_vendor_usd_latest"]].median(numeric_only=True)
    r = {
        "ein": 0, "name": f"{name} (median of n={len(sub)})", "segment": sub.segment.mode().iat[0],
        "captive_status": "archetype", "recent_migration": "",
        "avg_assets_proxy": med.avg_assets_proxy, "accounts_for_cost": med.accounts_for_cost,
        "operating_cost_ex_invest_mgmt": med.operating_cost_ex_invest_mgmt,
        "daf_share_of_total_assets": med.daf_share_of_total_assets,
        "employees": med.employees if name != "ARCH-advisor-program" else 0,
        "vendor990_daf_vendor_usd_latest": med.vendor990_daf_vendor_usd_latest if name == "ARCH-advisor-program" else float("nan"),
    }
    rf, cen, effd, smed = ctx
    # servicer cost for archetype: median of members
    sc = sub.ein.map(lambda e: smed.get(int(e), {}).get("annual_cost_ai_native_base")).median()
    sch = sub.ein.map(lambda e: smed.get(int(e), {}).get("annual_cost_ai_native_high")).median()
    smed2 = dict(smed)
    smed2[0] = {"annual_cost_ai_native_base": sc, "annual_cost_ai_native_high": sch}
    out = row_economics(r, (rf, cen, effd, smed2))
    out["ein"] = ""
    out["members"] = "; ".join(sub.sort_values("avg_assets_proxy", ascending=False).name.head(12))
    return out


def main(outdir):
    se, sme, fr, cen, eff = load()
    rf = realised_fee_table(fr)
    cent = census_table(cen)
    effd = eff_latest(eff)
    smed = {int(r.ein): {"annual_cost_ai_native_base": r.annual_cost_ai_native_base, "annual_cost_ai_native_high": r.annual_cost_ai_native_high}
            for r in sme.itertuples()}
    ctx = (rf, cent, effd, smed)
    act = se[(se.status == "active") & se.avg_assets_proxy.notna() & (se.accounts_for_cost > 0) & se.operating_cost_ex_invest_mgmt.notna()].copy()
    act["ein"] = act.ein.astype(int)
    named = act.sort_values("avg_assets_proxy", ascending=False).head(30)
    rows = [archetype_row(k, act[f(act)], ctx) for k, f in ARCHETYPES.items()]
    rows += [row_economics(r, ctx) for _, r in named.iterrows()]
    sv = pd.DataFrame(rows)
    sv.insert(0, "row_type", ["archetype"] * len(ARCHETYPES) + ["named_sponsor"] * len(named))
    sv.to_csv(f"{outdir}/sponsor-value.csv", index=False)
    # pricing-structures long format
    recs = []
    for k, desc in STRUCTURES.items():
        for _, r in sv.iterrows():
            recs.append({
                "structure": k, "definition": desc, "row_type": r.row_type, "sponsor_or_archetype": r["name"],
                "service_group": r.service_group, "avg_balance_usd": r.avg_balance_usd, "accounts": r.accounts,
                "price_usd": r[f"{k}_price_usd"], "price_bps": r[f"{k}_price_bps"], "price_per_account_usd": r[f"{k}_price_per_account"],
                "value_delivered_base_usd": r.value_delivered_base_usd,
                "price_share_of_value": r[f"{k}_price_share_of_value"],
                "sponsor_net_value_usd": r[f"{k}_sponsor_net_value_usd"],
                "sponsor_net_value_if_topdown_value_usd": r[f"{k}_sponsor_net_value_high_usd"],
                "sponsor_margin_now_usd": r.sponsor_margin_now_usd,
                "sponsor_margin_after_usd": r[f"{k}_sponsor_margin_after_usd"],
                "servicer_contribution_usd": r[f"{k}_servicer_contribution_usd"],
                "sponsor_better_off": (r[f"{k}_sponsor_net_value_usd"] > 0),
                "servicer_covers_marginal_cost": (r[f"{k}_servicer_contribution_usd"] != "" and float(r[f"{k}_servicer_contribution_usd"]) > 0),
                "label": "[D] from [S] inputs and [A] structure parameters; see sponsor-value.csv labels",
            })
    pd.DataFrame(recs).to_csv(f"{outdir}/pricing-structures.csv", index=False)
    return sv


if __name__ == "__main__":
    sv = main(sys.argv[1])
    pd.set_option("display.width", 250)
    cols = ["name", "service_group", "avg_balance_usd", "accounts", "donor_fee_revenue_bps_base", "daf_opex_bps", "value_delivered_bps",
            "value_delivered_per_account_usd", "value_delivered_high_usd", "max_value_price_base_bps", "max_value_price_base_per_account", "max_value_price_high_bps", "S1_flat_20bps_price_per_account", "S1_flat_20bps_servicer_contribution_usd"]
    print(sv[cols].to_string())
