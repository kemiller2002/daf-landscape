"""Infrastructure cost-per-account model (zero-based operational economics), 2026-11-27.
Prices: ../data/registers/infrastructure-prices.csv. Assumptions: ../data/registers/infrastructure-consumption-assumptions.csv.
Run: python3 infrastructure_cost_model.py out.json  (prints per-account-year at 1k/10k/100k/1M accounts). Hours/month = 730.
"""
import json, math
H = 730
S_MO = H * 3600  # 2,628,000 s

# ---------- consumption assumptions (low, base, high) ----------
A = dict(
    contrib=(2, 3, 6), lines_contrib=(3, 4, 8), grants=(5, 10, 25), lines_grant=(4, 6, 10),
    lines_other=(8, 12, 30), bytes_line=(250, 400, 700), events=(80, 150, 400),
    bytes_event=(800, 1500, 3000), misc_kb=(10, 20, 60), overhead=(1.1, 1.25, 1.5),
    retained_years=(3, 7, 12), backup_mult=(1.0, 1.5, 3.0), docs=(6, 12, 30), doc_kb=(50, 100, 250),
    evid_kb_grant=(10, 50, 400), log_gb_per_1k_events=(0.003, 0.01, 0.05), requests=(100, 320, 1500),
    log_kb_req=(0.3, 1.0, 3.0), log_archive_years=(1, 7, 10), egress_mb=(3, 15, 60),
    ai_calls=(0.2, 1.0, 5.0), ai_in=(3000, 8000, 30000), ai_out=(300, 1000, 3000), emails=(8, 20, 60),
    email_kb=(30, 50, 150), mau_share=(0.05, 0.15, 0.40), users_per_acct=(1.0, 1.3, 2.0),
    logins=(2, 4, 12), sms_share=(0.1, 0.3, 0.7), nonprod_share=(0.2, 0.35, 0.7),
    db_cpu_s_per_1k=(1, 4, 10), read_amp=(1.5, 2, 3), peak_day=(5, 10, 15), peak_hour_share=(0.10, 0.15, 0.25),
    db_util_target=(0.6, 0.5, 0.4), hot_months=(0.5, 1, 2), app_cpu_s_per_1k=(0.5, 2, 6),
    app_cpu_s_req=(0.01, 0.02, 0.05), pdf_cpu_s=(0.3, 1, 3), fixed_log_gb_mo=(5, 15, 45),
    large_sponsors=(1, 2, 5), new_acct_share=(0.10, 0.15, 0.25),
)
IDX = {"low": 0, "base": 1, "high": 2}

# ---------- prices ----------
AZ = dict(
    pg_vcore_h=0.089, pg_vcore_1yr=468 / 8760, pg_stor=0.115, pg_backup=0.095,
    aca_vcpu_s=0.000024, aca_gib_s=0.000003, aca_vcpu_idle_s=0.000003, aca_grant=180000 * 0.000024 + 360000 * 0.000003,
    blob_hot_zrs=0.026, blob_cool_zrs=0.019, blob_archive=0.00099, blob_write_10k=0.05,
    defender_acct_mo=0.0134 * H, scan_gb=0.15, egress_gb=0.0825, fd_base=330.0, fd_req_10k=0.009,
    dns_zone=0.50, la_gb=2.30, la_free_gb=5, archive_gb_mo=0.02, kv_mo=1.0, email=0.00025, email_mb=0.00012,
    sms=0.03, mau=0.03, mau_free=50000, inter_region_gb=0.02, ci_mo=18.0,
)
AWS = dict(
    rds_maz={2: 0.337, 4: 0.674, 8: 1.348, 16: 2.696}, rds_saz={2: 0.168, 4: 0.337, 8: 0.674, 16: 1.348},
    rds_maz_1yr={2: 0.2595, 4: 0.519, 8: 1.038, 16: 2.0759}, rds_stor_maz=0.23, rds_stor_saz=0.115, rds_backup=0.095,
    fg_vcpu_h=0.03238, fg_gb_h=0.00356, alb_h=0.0225, lcu_h=0.008,
    s3_std=0.023, s3_ia=0.0125, s3_gir=0.004, s3_put_1k=0.005, scan_gb=0.09, scan_obj=0.000215,
    egress_gb=0.09, waf_acl=5.0, waf_rules=10.0, waf_req_m=0.60, dns_zone=0.50, cw_gb=0.50, cw_store=0.03,
    kms_mo=2.0, secrets_mo=4.0, email=0.0001, sms=0.0128, mau=0.015, mau_free=10000, inter_region_gb=0.01, ci_mo=18.0,
)
AI = dict(low=(0.05, 0.25), base=(2.0, 10.0), high=(4.0, 20.0))  # $/MTok in,out: Haiku 5.5 batch / Sonnet 5.5 / Opus 5.5


def a(k, c):
    return A[k][IDX[c]]


def per_acct(c):
    lines = a("contrib", c) * a("lines_contrib", c) + a("grants", c) * a("lines_grant", c) + a("lines_other", c)
    db_kb = lines * a("bytes_line", c) / 1000 + a("events", c) * a("bytes_event", c) / 1000 + a("misc_kb", c)
    obj_mb = a("docs", c) * a("doc_kb", c) / 1000 + a("grants", c) * a("evid_kb_grant", c) / 1000
    log_gb = a("events", c) / 1000 * a("log_gb_per_1k_events", c) + a("requests", c) * a("log_kb_req", c) / 1e6
    return dict(lines=lines, db_kb=db_kb, obj_mb=obj_mb, log_gb=log_gb)


def db_vcores(n, c, pa):
    eps = n * a("events", c) / 365 * a("peak_day", c) * a("peak_hour_share", c) / 3600
    cpu = eps * a("db_cpu_s_per_1k", c) / 1000 * a("read_amp", c) / a("db_util_target", c)
    hot_kb = pa["lines"] * a("bytes_line", c) / 1000 + a("misc_kb", c) + 0.15 * a("events", c) * a("bytes_event", c) / 1000
    hot_gb = n * hot_kb * a("overhead", c) / 1e6 * a("hot_months", c) / 12
    ram_vc = hot_gb / 4  # 4 GB RAM per vCore (Ddsv5 / m7g)
    need = max(2, cpu, ram_vc)
    tier = 2
    while tier < need:
        tier *= 2
    return tier, eps, cpu, hot_gb


def prov_storage(gb):
    t = 128
    while t < gb * 1.2:
        t *= 2
    return t


def model(provider, cfg, n, c, reserved=False):
    pa = per_acct(c)
    vc, eps, cpu, hot = db_vcores(n, c, pa)
    db_gb = n * pa["db_kb"] * a("overhead", c) * a("retained_years", c) / 1e6
    stor = prov_storage(db_gb)
    obj_gb = n * pa["obj_mb"] * a("retained_years", c) / 1000
    obj_new_gb_mo = n * pa["obj_mb"] / 1000 / 12
    evid_gb_mo = n * a("grants", c) * a("evid_kb_grant", c) / 1e6 / 12
    log_gb_mo = n * pa["log_gb"] / 12 + a("fixed_log_gb_mo", c)
    egress_gb_mo = n * a("egress_mb", c) / 1000 / 12
    req_mo = n * a("requests", c) / 12
    mau = n * a("mau_share", c) * a("users_per_acct", c)
    app_cpu_s_mo = n / 12 * (a("events", c) / 1000 * a("app_cpu_s_per_1k", c) + a("requests", c) * a("app_cpu_s_req", c) + a("docs", c) * a("pdf_cpu_s", c))
    L = {}
    if provider == "Azure":
        p = AZ
        vrate = p["pg_vcore_1yr"] if reserved else p["pg_vcore_h"]
        L["db_compute_HA"] = vc * vrate * 2 * H
        L["db_storage_HA"] = stor * p["pg_stor"] * 2
        L["db_backup"] = max(0, a("backup_mult", c) * db_gb - stor) * p["pg_backup"]
        L["db_ltr_archive"] = db_gb * 0.3 * 22 * p["blob_archive"]
        rep_vcpu = 0.5 if n <= 100000 else 1.0
        base_app = 2 * (rep_vcpu * p["aca_vcpu_s"] + 2 * rep_vcpu * p["aca_gib_s"]) * S_MO - p["aca_grant"]
        L["app_compute"] = base_app + app_cpu_s_mo * (p["aca_vcpu_s"] + 2 * p["aca_gib_s"])
        hot_gb = min(obj_gb, n * pa["obj_mb"] / 1000)
        L["object_storage"] = hot_gb * p["blob_hot_zrs"] + (obj_gb - hot_gb) * p["blob_cool_zrs"] + n * (a("docs", c) + a("grants", c) * 0.2) / 12 / 1e4 * p["blob_write_10k"]
        L["malware_scan"] = p["defender_acct_mo"] + evid_gb_mo * p["scan_gb"]
        L["edge_waf_egress"] = p["fd_base"] + req_mo / 1e4 * p["fd_req_10k"] + egress_gb_mo * p["egress_gb"]
        L["dns"] = p["dns_zone"]
        L["logs"] = max(0, log_gb_mo - p["la_free_gb"]) * p["la_gb"] + log_gb_mo * 12 * a("log_archive_years", c) * p["archive_gb_mo"]
        L["keys_secrets"] = p["kv_mo"]
        L["email"] = n * a("emails", c) / 12 * (p["email"] + a("email_kb", c) / 1000 * p["email_mb"])
        L["sms_mfa"] = n * a("logins", c) * a("sms_share", c) / 12 * p["sms"]
        L["identity_mau"] = max(0, mau - p["mau_free"]) * p["mau"]
        dr = {}
        if cfg in ("C2", "C3"):
            dr["dr_db_replica"] = vc * vrate * H + stor * p["pg_stor"]
            dr["dr_replication_transfer"] = (n * pa["db_kb"] / 1e6 / 12 * 3) * p["inter_region_gb"]  # WAL ~3x logical bytes
            dr["dr_app_warm"] = 1 * (0.5 * p["aca_vcpu_idle_s"] + 1 * p["aca_gib_s"]) * S_MO
            dr["dr_blob_geo"] = obj_gb * (0.0458 - 0.026)  # GRS uplift proxy
            dr["dr_keyvault_logs"] = 1 + 5 * p["la_gb"]
        iso = {}
        if cfg == "C3":
            k = a("large_sponsors", c)
            per = 2 * p["pg_vcore_h" if not reserved else "pg_vcore_1yr"] * 2 * H + 128 * p["pg_stor"] * 2 \
                + 2 * vrate * H + 128 * p["pg_stor"] + 1.0 + p["defender_acct_mo"] + 5 * p["la_gb"]
            iso["isolated_sponsor_db_dr"] = k * per
    else:
        p = AWS
        tbl = p["rds_maz_1yr"] if reserved else p["rds_maz"]
        L["db_compute_HA"] = tbl.get(vc, tbl[16] * vc / 16) * H
        L["db_storage_HA"] = stor * p["rds_stor_maz"]
        L["db_backup"] = max(0, a("backup_mult", c) * db_gb - stor) * p["rds_backup"]
        L["db_ltr_archive"] = db_gb * 0.3 * 22 * p["s3_gir"]
        rep_vcpu = 0.5 if n <= 100000 else 1.0
        L["app_compute"] = 2 * (rep_vcpu * p["fg_vcpu_h"] + 2 * rep_vcpu * p["fg_gb_h"]) * H + app_cpu_s_mo / 3600 * (p["fg_vcpu_h"] + 2 * p["fg_gb_h"]) + (p["alb_h"] + p["lcu_h"]) * H
        hot_gb = min(obj_gb, n * pa["obj_mb"] / 1000)
        L["object_storage"] = hot_gb * p["s3_std"] + (obj_gb - hot_gb) * p["s3_ia"] + n * (a("docs", c) + a("grants", c) * 0.2) / 12 / 1000 * p["s3_put_1k"]
        L["malware_scan"] = evid_gb_mo * p["scan_gb"] + n * a("grants", c) * 0.2 / 12 * p["scan_obj"]
        L["edge_waf_egress"] = p["waf_acl"] + p["waf_rules"] + req_mo / 1e6 * p["waf_req_m"] + egress_gb_mo * p["egress_gb"]
        L["dns"] = p["dns_zone"]
        L["logs"] = max(0, log_gb_mo - 5) * p["cw_gb"] + log_gb_mo * 12 * a("log_archive_years", c) * p["cw_store"]
        L["keys_secrets"] = p["kms_mo"] + p["secrets_mo"]
        L["email"] = n * a("emails", c) / 12 * p["email"]
        L["sms_mfa"] = n * a("logins", c) * a("sms_share", c) / 12 * p["sms"]
        L["identity_mau"] = max(0, mau - p["mau_free"]) * p["mau"]
        dr = {}
        if cfg in ("C2", "C3"):
            dr["dr_db_replica"] = p["rds_saz"].get(vc, p["rds_saz"][16] * vc / 16) * H + stor * p["rds_stor_saz"]
            dr["dr_replication_transfer"] = (n * pa["db_kb"] / 1e6 / 12 * 3) * p["inter_region_gb"]
            dr["dr_app_warm"] = (0.5 * p["fg_vcpu_h"] + 1 * p["fg_gb_h"]) * H + p["alb_h"] * H
            dr["dr_blob_geo"] = obj_gb * p["s3_std"] * 0.5 + obj_gb * 0.02 / max(1, a("retained_years", c))
            dr["dr_keyvault_logs"] = p["kms_mo"] + 5 * p["cw_gb"]
        iso = {}
        if cfg == "C3":
            k = a("large_sponsors", c)
            per = (p["rds_maz_1yr"] if reserved else p["rds_maz"])[2] * H + 128 * p["rds_stor_maz"] + p["rds_saz"][2] * H + 128 * p["rds_stor_saz"] + 1.0 + 5 * p["cw_gb"]
            iso["isolated_sponsor_db_dr"] = k * per
    L.update(dr); L.update(iso)
    ai = n * a("ai_calls", c) / 12 * (a("ai_in", c) * AI[c][0] + a("ai_out", c) * AI[c][1]) / 1e6
    prod = sum(L.values())
    core_prod = prod - L["db_backup"] * 0  # keep
    # nonprod share applied to C1-style fixed prod (exclude per-user services and DR/isolation)
    np_base = sum(v for k, v in L.items() if k in ("db_compute_HA", "db_storage_HA", "app_compute", "edge_waf_egress", "logs", "keys_secrets", "malware_scan", "dns"))
    nonprod = a("nonprod_share", c) * np_base
    ci = p["ci_mo"]
    total_mo = prod + nonprod + ci + ai
    return dict(provider=provider, cfg=cfg, n=n, case=c, reserved=reserved, vcores=vc, peak_eps=eps, db_cpu_need=cpu, hot_gb=hot,
                db_gb=db_gb, stor_gb=stor, obj_gb=obj_gb, log_gb_mo=log_gb_mo, mau=mau, lines=L, prod=prod, nonprod=nonprod, ci=ci, ai=ai,
                total_mo=total_mo, per_acct_yr=total_mo * 12 / n, per_acct_yr_ex_ai=(total_mo - ai) * 12 / n)


if __name__ == "__main__":
    import sys
    out = []
    for prov in ("Azure", "AWS"):
        for cfg in ("C1", "C2", "C3"):
            for c in ("low", "base", "high"):
                for n in (1000, 10000, 100000, 1000000):
                    for r in (False, True):
                        out.append(model(prov, cfg, n, c, r))
    json.dump(out, open(sys.argv[1], "w"), indent=1, default=float)
    for c in ("low", "base", "high"):
        print(c, per_acct(c))
    for prov in ("Azure", "AWS"):
        for cfg in ("C1", "C2", "C3"):
            row = [f"{prov:5} {cfg}"]
            for c in ("low", "base", "high"):
                vals = [m for m in out if m["provider"] == prov and m["cfg"] == cfg and m["case"] == c and not m["reserved"]]
                row.append(c + ":" + "/".join(f"{m['per_acct_yr']:.2f}" for m in vals))
            print("  ".join(row))
