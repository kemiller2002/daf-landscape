"""ACT group: activity-based cost and capacity model for an AI-native DAF servicer.

Research model only. Every parameter is labelled in activities.csv / assumptions.jsonl.
Pure functions; outputs are written once at the end by main().
Run: python3 -I -B act_model.py <output_dir>
"""
import csv
import json
import math
import sys
from pathlib import Path

APPROACHES = ("conventional", "ai_enhanced", "ai_native", "elimination")
LEVELS = ("low", "base", "high")
RATE_PER_HOUR = 50.0            # [A] budget doc line 34
PRODUCTIVE_HOURS = 1600.0       # [A] budget doc line 34; Unbound parameters.json:50
QUEUE_UTILISATION = 0.85        # [A] share of productive hours usable for queue work
CORE_VARIABLE_HOURS = 960.0     # [A] grant/client ops FTE at 60% available for variable work
CORE_CONTROLLER_HOURS = 640.0   # [A] controller 40% available for sponsor close/reconciliation review

# ---------------------------------------------------------------------------
# Archetype drivers per account-year [A unless noted]. grants anchored to the
# observed 5.6-18.5 grants per account (FY2024, EV-ACT-003..012).
# ---------------------------------------------------------------------------
ARCHETYPES = {
    "inactive": dict(label="Dormant / inactive account", balance=20000, new=0.0, ach=0.1, chk=0.05, sec=0.02,
                     complex=0.0, rec_chg=0.0, grants=0.3, check_share=0.33, wire_share=0.0, contacts=0.1,
                     changes=0.1, succession=0.02, exc_mult=1.0),
    "small_recurring": dict(label="Small recurring giver", balance=8000, new=0.15, ach=12.0, chk=0.2, sec=0.0,
                            complex=0.0, rec_chg=0.3, grants=6.0, check_share=0.25, wire_share=0.0, contacts=0.3,
                            changes=0.2, succession=0.01, exc_mult=0.5),
    "typical": dict(label="Typical account", balance=150000, new=0.12, ach=1.0, chk=0.5, sec=1.0,
                    complex=0.003, rec_chg=0.05, grants=9.0, check_share=0.33, wire_share=0.005, contacts=0.5,
                    changes=0.3, succession=0.02, exc_mult=1.0),
    "high_frequency": dict(label="High-frequency grantmaker", balance=400000, new=0.08, ach=2.0, chk=0.5, sec=2.0,
                           complex=0.01, rec_chg=0.1, grants=40.0, check_share=0.33, wire_share=0.01, contacts=1.2,
                           changes=0.4, succession=0.02, exc_mult=0.8),
    "high_value": dict(label="High-value concentrated", balance=3000000, new=0.08, ach=0.5, chk=0.2, sec=2.0,
                       complex=0.05, rec_chg=0.0, grants=15.0, check_share=0.33, wire_share=0.03, contacts=2.0,
                       changes=0.5, succession=0.03, exc_mult=1.8),
    "complex_asset": dict(label="Complex-asset donor", balance=1500000, new=0.10, ach=0.5, chk=0.2, sec=2.0,
                          complex=1.0, rec_chg=0.0, grants=10.0, check_share=0.33, wire_share=0.02, contacts=3.0,
                          changes=0.5, succession=0.03, exc_mult=1.3),
}
MIX = {"inactive": 0.20, "small_recurring": 0.20, "typical": 0.40, "high_frequency": 0.07,
       "high_value": 0.10, "complex_asset": 0.03}   # [A] sponsor book mix

GRANTS_PER_RECIPIENT = {"low": 2.5, "base": 4.0, "high": 13.2}   # [A]/[D]; 13.2 = Fidelity 3.0M/226,823 (EV-ACT-013)
RENEWALS_PER_RECIPIENT = {"conventional": 365 / 150, "ai_enhanced": 365 / 150, "ai_native": 1.2, "elimination": 1.0}
ADVERSE_EVENTS_PER_RECIPIENT = {"low": 0.003, "base": 0.0067, "high": 0.02}  # 1.7/1000 revocations [S] + other [A]
CONTACT_FACTOR = {"conventional": 1.0, "ai_enhanced": 0.85, "ai_native": 0.5, "elimination": 0.5}  # [A]
CHECK_SHARE_ELIM = 0.05      # [A] EFT-default; Chariot pooled 94.6% electronic, Dallas JCF 92% (EV-ACT-015)
CHECK_CONTRIB_ELIM = 0.5     # [A] steer half of check contributions to ACH


def screens(a):
    return a["grants"] + a["ach"] + a["chk"] + a["sec"] + 1.0


def eft_grants(a, check_share):
    return a["grants"] * max(0.0, 1.0 - check_share - a["wire_share"])


def check_share_for(a, approach):
    return CHECK_SHARE_ELIM if approach == "elimination" else a["check_share"]


def recipients(a, lvl="base"):
    return a["grants"] / GRANTS_PER_RECIPIENT[lvl]


# Activity table. minutes = expected servicer minutes per occurrence (averaged over all
# occurrences incl. zero-touch), per approach, (low, base, high). exc = share of base minutes
# that scales with archetype exception multiplier. driver(a, approach) -> occurrences/account-year.
# sponsor = sponsor-retained minutes per occurrence (reserved decisions), conventional vs redesigned.
def T(l, b, h):
    return {"low": l, "base": b, "high": h}


ACTIVITIES = [
    dict(id="ACT-A01", name="Account opening (KYC, agreement, sanctions at onboarding)", driver=lambda a, p: a["new"],
         freq_unit="new accounts per account-year", m={"conventional": T(12, 25, 45), "ai_enhanced": T(5, 10, 20),
         "ai_native": T(1, 3, 8), "elimination": T(0.5, 2, 6)}, exc=0.0, sponsor=(0.5, 0.2), ext=("data_identity", 3.0)),
    dict(id="ACT-A02", name="Contributions: cash/ACH/card", driver=lambda a, p: a["ach"],
         freq_unit="contributions per account-year", m={"conventional": T(1, 3, 6), "ai_enhanced": T(0.4, 1, 2),
         "ai_native": T(0.1, 0.3, 0.8), "elimination": T(0.05, 0.2, 0.5)}, exc=0.0, sponsor=(0, 0), ext=("payments", 0.30)),
    dict(id="ACT-A03", name="Contributions: paper checks", driver=lambda a, p: a["chk"] * (CHECK_CONTRIB_ELIM if p == "elimination" else 1.0),
         freq_unit="check contributions per account-year", m={"conventional": T(3, 6, 10), "ai_enhanced": T(1.5, 3, 5),
         "ai_native": T(0.8, 1.5, 3), "elimination": T(0.8, 1.5, 3)}, exc=0.0, sponsor=(0, 0), ext=("payments", 0.65)),
    dict(id="ACT-A04", name="Contributions: publicly traded securities (DTC/ACATS)", driver=lambda a, p: a["sec"],
         freq_unit="securities transfers per account-year", m={"conventional": T(6, 12, 25), "ai_enhanced": T(2, 5, 10),
         "ai_native": T(0.5, 2, 5), "elimination": T(0.3, 1, 3)}, exc=0.0, sponsor=(0, 0), ext=("payments", 10.0)),
    dict(id="ACT-A05", name="Complex / noncash assets (private stock, LP, real estate, crypto)", driver=lambda a, p: a["complex"],
         freq_unit="complex gifts per account-year", m={"conventional": T(360, 720, 1800), "ai_enhanced": T(240, 480, 1200),
         "ai_native": T(120, 300, 720), "elimination": T(60, 120, 360)}, exc=0.0, sponsor=(60, 45), ext=("other", 350.0)),
    dict(id="ACT-A06", name="Recurring contribution set-up and changes", driver=lambda a, p: a["rec_chg"],
         freq_unit="schedule changes per account-year", m={"conventional": T(4, 8, 15), "ai_enhanced": T(1, 3, 6),
         "ai_native": T(0.2, 0.5, 1.5), "elimination": T(0.2, 0.5, 1.5)}, exc=0.0, sponsor=(0, 0), ext=("none", 0.0)),
    dict(id="ACT-A07", name="Grant recommendation intake", driver=lambda a, p: a["grants"],
         freq_unit="grant recommendations per account-year", m={"conventional": T(0.3, 1.0, 3.0), "ai_enhanced": T(0.1, 0.4, 1.0),
         "ai_native": T(0.02, 0.1, 0.3), "elimination": T(0.01, 0.05, 0.15)}, exc=0.0, sponsor=(0, 0), ext=("none", 0.0)),
    dict(id="ACT-A08", name="Charity verification at approval and release (transaction-time status check)", driver=lambda a, p: a["grants"],
         freq_unit="grants per account-year", m={"conventional": T(0.2, 1.0, 3.0), "ai_enhanced": T(0.1, 0.3, 0.8),
         "ai_native": T(0.01, 0.03, 0.1), "elimination": T(0.005, 0.02, 0.05)}, exc=0.0, sponsor=(0, 0), ext=("data_identity", 0.14)),
    dict(id="ACT-A09", name="180-day charity re-verification (deep review renewal)",
         driver=lambda a, p: recipients(a) * RENEWALS_PER_RECIPIENT[p],
         freq_unit="renewals per account-year (= distinct recipients x renewals per recipient)",
         m={"conventional": T(8, 15, 30), "ai_enhanced": T(2, 5, 10), "ai_native": T(0.15, 0.4, 1.2),
            "elimination": T(0.1, 0.3, 1.0)}, exc=0.0, sponsor=(0, 0), ext=("data_identity", 0.02)),
    dict(id="ACT-A10", name="Event-driven charity monitoring (revocation, name/EIN change, list delta, adverse news)",
         driver=lambda a, p: recipients(a) * ADVERSE_EVENTS_PER_RECIPIENT["base"],
         freq_unit="adverse events per account-year", m={"conventional": T(15, 30, 60), "ai_enhanced": T(10, 20, 45),
         "ai_native": T(10, 15, 45), "elimination": T(10, 15, 45)}, exc=0.0, sponsor=(10, 10), ext=("none", 0.0)),
    dict(id="ACT-A11", name="Grant approval incl. eligibility exceptions (servicer prepares; sponsor decides reserved cases)",
         driver=lambda a, p: a["grants"], freq_unit="grants per account-year",
         m={"conventional": T(1.3, 4.7, 15), "ai_enhanced": T(0.8, 2.7, 9), "ai_native": T(0.5, 1.4, 4.5),
            "elimination": T(0.5, 1.4, 4.5)}, exc=0.75, sponsor=(0.5, 0.32), ext=("cloud", 0.02)),
    dict(id="ACT-A12", name="Purpose / prohibited-benefit review (s4967, pledges, tickets)", driver=lambda a, p: a["grants"],
         freq_unit="grants per account-year", m={"conventional": T(0.05, 0.5, 3.0), "ai_enhanced": T(0.04, 0.36, 2.0),
         "ai_native": T(0.03, 0.27, 1.5), "elimination": T(0.03, 0.27, 1.5)}, exc=1.0, sponsor=(0.1, 0.08), ext=("none", 0.0)),
    dict(id="ACT-A13", name="Non-standard grantee due diligence (foreign, expenditure responsibility, fiscal sponsors)",
         driver=lambda a, p: a["grants"], freq_unit="grants per account-year",
         m={"conventional": T(0.15, 1.0, 7.2), "ai_enhanced": T(0.12, 0.7, 5.0), "ai_native": T(0.1, 0.6, 4.0),
            "elimination": T(0.05, 0.2, 1.5)}, exc=1.0, sponsor=(0.15, 0.1), ext=("none", 0.0)),
    dict(id="ACT-A14", name="Payment processing: EFT/ACH grant", driver=lambda a, p: eft_grants(a, check_share_for(a, p)),
         freq_unit="EFT grants per account-year", m={"conventional": T(0.2, 0.5, 1.5), "ai_enhanced": T(0.1, 0.3, 0.8),
         "ai_native": T(0.03, 0.1, 0.3), "elimination": T(0.03, 0.1, 0.3)}, exc=0.0, sponsor=(0, 0), ext=("payments", 0.30)),
    dict(id="ACT-A15", name="Payment processing: check grant (print, positive pay, mail)", driver=lambda a, p: a["grants"] * check_share_for(a, p),
         freq_unit="check grants per account-year", m={"conventional": T(1.5, 3, 6), "ai_enhanced": T(1, 2, 4),
         "ai_native": T(0.6, 1.2, 2.5), "elimination": T(0.6, 1.2, 2.5)}, exc=0.0, sponsor=(0, 0), ext=("payments", 4.0)),
    dict(id="ACT-A16", name="Payment processing: wire (large / international)", driver=lambda a, p: a["grants"] * a["wire_share"],
         freq_unit="wires per account-year", m={"conventional": T(10, 15, 30), "ai_enhanced": T(6, 10, 20),
         "ai_native": T(4, 6, 12), "elimination": T(4, 6, 12)}, exc=0.0, sponsor=(2, 2), ext=("payments", 25.0)),
    dict(id="ACT-A17", name="Returned / uncashed / voided checks and reissue", driver=lambda a, p: a["grants"] * check_share_for(a, p),
         freq_unit="check grants per account-year (3% become cases)", m={"conventional": T(0.3, 0.9, 3.6), "ai_enhanced": T(0.2, 0.6, 2.4),
         "ai_native": T(0.15, 0.45, 1.8), "elimination": T(0.15, 0.45, 1.8)}, exc=0.0, sponsor=(0, 0), ext=("other", 0.12)),
    dict(id="ACT-A18", name="Reconciliation (bank, custodian, ledger; break resolution)", driver=lambda a, p: screens(a) - 1.0,
         freq_unit="transactions per account-year", m={"conventional": T(0.3, 0.8, 2.0), "ai_enhanced": T(0.15, 0.4, 1.0),
         "ai_native": T(0.03, 0.1, 0.3), "elimination": T(0.03, 0.1, 0.3)}, exc=0.0, sponsor=(0, 0), ext=("none", 0.0)),
    dict(id="ACT-A19", name="Fee calculation and billing", driver=lambda a, p: 1.0, freq_unit="accounts",
         m={"conventional": T(0.2, 1, 3), "ai_enhanced": T(0.1, 0.3, 1), "ai_native": T(0.01, 0.05, 0.2),
            "elimination": T(0.01, 0.05, 0.2)}, exc=0.0, sponsor=(0, 0), ext=("none", 0.0)),
    dict(id="ACT-A20", name="Statements and contribution acknowledgments (s170(f)(8)/(18))", driver=lambda a, p: 1.0, freq_unit="accounts",
         m={"conventional": T(1, 3, 6), "ai_enhanced": T(0.3, 1, 2), "ai_native": T(0.05, 0.2, 0.6),
            "elimination": T(0.02, 0.1, 0.3)}, exc=0.0, sponsor=(0, 0), ext=("other", 0.70)),
    dict(id="ACT-A21", name="Donor / advisor service contacts (human-handled)", driver=lambda a, p: a["contacts"] * CONTACT_FACTOR[p],
         freq_unit="human-handled contacts per account-year", m={"conventional": T(6, 10, 20), "ai_enhanced": T(4, 7, 14),
         "ai_native": T(4, 8, 15), "elimination": T(4, 8, 15)}, exc=0.0, sponsor=(0, 0), ext=("cloud", 0.20)),
    dict(id="ACT-A22", name="Investment interfaces (allocation changes, custodian/advisor feeds)", driver=lambda a, p: 1.0, freq_unit="accounts",
         m={"conventional": T(0.5, 1.5, 4), "ai_enhanced": T(0.2, 0.6, 1.5), "ai_native": T(0.05, 0.2, 0.6),
            "elimination": T(0.05, 0.2, 0.6)}, exc=0.0, sponsor=(0, 0), ext=("none", 0.0)),
    dict(id="ACT-A23", name="Fraud investigation (account takeover, payment redirection, BEC)", driver=lambda a, p: 0.002, freq_unit="attempts per account-year",
         m={"conventional": T(60, 180, 480), "ai_enhanced": T(60, 150, 420), "ai_native": T(60, 120, 360),
            "elimination": T(60, 120, 360)}, exc=0.0, sponsor=(30, 30), ext=("other", 600.0)),
    dict(id="ACT-A24", name="Sanctions screening alert disposition", driver=lambda a, p: screens(a),
         freq_unit="screened events per account-year", m={"conventional": T(0.05, 0.16, 0.42), "ai_enhanced": T(0.035, 0.105, 0.28),
         "ai_native": T(0.0045, 0.0135, 0.036), "elimination": T(0.0045, 0.0135, 0.036)}, exc=0.0, sponsor=(0.002, 0.002),
         ext=("data_identity", 0.01)),
    dict(id="ACT-A25", name="Account changes (address, advisor, bank, contact channel)", driver=lambda a, p: a["changes"],
         freq_unit="changes per account-year", m={"conventional": T(3, 6, 12), "ai_enhanced": T(1, 3, 6),
         "ai_native": T(0.3, 1, 3), "elimination": T(0.3, 1, 3)}, exc=0.0, sponsor=(0, 0), ext=("none", 0.0)),
    dict(id="ACT-A26", name="Succession, death, successor advisors", driver=lambda a, p: a["succession"],
         freq_unit="succession events per account-year", m={"conventional": T(30, 60, 120), "ai_enhanced": T(20, 45, 90),
         "ai_native": T(15, 35, 90), "elimination": T(15, 35, 90)}, exc=0.0, sponsor=(15, 10), ext=("none", 0.0)),
]

# Per-sponsor (not per-account) activities: hours per sponsor-year (one-offs flagged).
SPONSOR_ACTIVITIES = [
    dict(id="ACT-S01", name="Financial reporting, monthly close and controller reconciliation sign-off", one_off=False,
         h={"conventional": T(240, 480, 960), "ai_enhanced": T(150, 300, 600), "ai_native": T(80, 150, 300), "elimination": T(80, 150, 300)}),
    dict(id="ACT-S02", name="Sponsor configuration and policy-pack upkeep", one_off=False,
         h={"conventional": T(60, 120, 240), "ai_enhanced": T(45, 90, 180), "ai_native": T(30, 60, 120), "elimination": T(30, 60, 120)}),
    dict(id="ACT-S03", name="Incident response (sponsor-attributable)", one_off=False,
         h={"conventional": T(10, 40, 200), "ai_enhanced": T(10, 40, 200), "ai_native": T(8, 30, 200), "elimination": T(8, 30, 200)}),
    dict(id="ACT-S04", name="Audit support (sponsor audit, 990/Schedule D, SOC bridge letters)", one_off=False,
         h={"conventional": T(60, 120, 240), "ai_enhanced": T(45, 90, 180), "ai_native": T(30, 60, 150), "elimination": T(30, 60, 150)}),
    dict(id="ACT-S05", name="Governance reporting (quarterly delegated-approval board report, decision-quality sampling)", one_off=False,
         h={"conventional": T(20, 40, 80), "ai_enhanced": T(15, 30, 60), "ai_native": T(12, 24, 60), "elimination": T(12, 24, 60)}),
    dict(id="ACT-S06", name="Sponsor onboarding and implementation", one_off=True,
         h={"conventional": T(300, 600, 1500), "ai_enhanced": T(225, 450, 1100), "ai_native": T(150, 300, 800), "elimination": T(150, 300, 800)}),
    dict(id="ACT-S07", name="Migration from incumbent platform (fixed part; plus per-account minutes)", one_off=True,
         h={"conventional": T(150, 300, 800), "ai_enhanced": T(120, 240, 600), "ai_native": T(80, 150, 500), "elimination": T(80, 150, 500)},
         per_account_min={"conventional": T(3, 6, 15), "ai_enhanced": T(2, 4, 10), "ai_native": T(1, 2, 6), "elimination": T(1, 2, 6)}),
]


def occurrences(act, a, approach):
    return act["driver"](a, approach)


def minutes_for(act, a, approach, lvl):
    base = act["m"][approach][lvl]
    scaled = base * (1 - act["exc"]) + base * act["exc"] * a["exc_mult"]
    return occurrences(act, a, approach) * scaled


def account_minutes(a, approach, lvl):
    return {act["id"]: minutes_for(act, a, approach, lvl) for act in ACTIVITIES}


def sponsor_minutes(a, approach):
    idx = 0 if approach in ("conventional", "ai_enhanced") else 1
    return sum(occurrences(act, a, approach) * act["sponsor"][idx] for act in ACTIVITIES)


def ext_costs(a, approach):
    def cost(act):
        cat, unit = act["ext"]
        return cat, occurrences(act, a, approach) * unit
    out = {"payments": 0.0, "data_identity": 0.0, "cloud": 0.0, "other": 0.0}
    for act in ACTIVITIES:
        cat, v = cost(act)
        if cat in out and not (cat == "cloud" and approach == "conventional"):
            out[cat] += v
    # AI dossier cost on exceptions and per-account infrastructure [A]: Unbound parameters.json:248,266
    infra = 3.0
    ai = 0.0 if approach == "conventional" else a["grants"] * 0.08 * a["exc_mult"] * 0.9
    out["cloud"] += infra + ai
    return out


def december_profile():
    # share of annual volume in December by work class [E]; method in report.
    return {"grants": 0.25, "contributions": 0.35, "contacts": 0.25, "other": 0.10}


GRANT_ACTS = {"ACT-A07", "ACT-A08", "ACT-A11", "ACT-A12", "ACT-A13", "ACT-A14", "ACT-A15", "ACT-A16", "ACT-A17"}
CONTRIB_ACTS = {"ACT-A02", "ACT-A03", "ACT-A04", "ACT-A05", "ACT-A06", "ACT-A01"}
CONTACT_ACTS = {"ACT-A21"}
DEFERRABLE = {"ACT-A09", "ACT-A19", "ACT-A20", "ACT-A22", "ACT-A25", "ACT-A06"}


def december_share(mins):
    prof = december_profile()
    tot = sum(mins.values()) or 1.0
    def cls(k):
        return "grants" if k in GRANT_ACTS else "contributions" if k in CONTRIB_ACTS else "contacts" if k in CONTACT_ACTS else "other"
    return sum(v * prof[cls(k)] for k, v in mins.items()) / tot


def mixed(fn):
    return sum(MIX[k] * fn(ARCHETYPES[k]) for k in MIX)


def fte_per_1000(min_per_acct):
    return min_per_acct * 1000 / 60 / (PRODUCTIVE_HOURS * QUEUE_UTILISATION)


def build_capacity_rows():
    rows = []
    for key, a in list(ARCHETYPES.items()) + [("market_mix", None)]:
        for p in APPROACHES:
            vals = {lvl: (sum(account_minutes(a, p, lvl).values()) if a else mixed(lambda x: sum(account_minutes(x, p, lvl).values())))
                    for lvl in LEVELS}
            base_mins = account_minutes(a, p, "base") if a else {k: mixed(lambda x: account_minutes(x, p, "base")[k]) for k in (act["id"] for act in ACTIVITIES)}
            spons = sponsor_minutes(a, p) if a else mixed(lambda x: sponsor_minutes(x, p))
            ext = ext_costs(a, p) if a else {c: mixed(lambda x: ext_costs(x, p)[c]) for c in ("payments", "data_identity", "cloud", "other")}
            dec = december_share(base_mins)
            balance = a["balance"] if a else mixed(lambda x: x["balance"])
            top3 = sorted(base_mins.items(), key=lambda kv: -kv[1])[:3]
            labour = vals["base"] * RATE_PER_HOUR / 60
            rows.append({
                "archetype": key, "approach": p,
                "servicer_min_per_acct_yr_low": round(vals["low"], 1), "servicer_min_per_acct_yr_base": round(vals["base"], 1),
                "servicer_min_per_acct_yr_high": round(vals["high"], 1),
                "vs_48min_allowance_base": round(vals["base"] / 48, 2),
                "labour_usd_at_50h_base": round(labour, 2), "labour_usd_at_50h_high": round(vals["high"] * RATE_PER_HOUR / 60, 2),
                "sponsor_retained_min_per_acct_yr_base": round(spons, 1),
                "ext_payments_usd": round(ext["payments"], 2), "ext_data_identity_usd": round(ext["data_identity"], 2),
                "ext_cloud_ai_usd": round(ext["cloud"], 2), "ext_other_usd": round(ext["other"], 2),
                "incremental_total_usd_base": round(labour + sum(ext.values()), 2),
                "vs_75_usd_base": round((labour + sum(ext.values())) / 75, 2),
                "fte_per_1000_accts_base": round(fte_per_1000(vals["base"]), 3),
                "fte_per_1000_accts_high": round(fte_per_1000(vals["high"]), 3),
                "december_share_of_annual_minutes": round(dec, 3),
                "december_daily_load_multiplier": round(dec / (20 / 250), 2),
                "avg_balance_usd_assumed": balance, "revenue_at_20bps_usd": round(balance * 0.002, 2),
                "top3_activities_base": "; ".join(f"{k}={v:.1f}" for k, v in top3),
                "label": "[D] from [A] activity parameters; no time study exists",
            })
    return rows


def sponsor_hours(approach, lvl, recurring_only=True):
    return sum(s["h"][approach][lvl] for s in SPONSOR_ACTIVITIES if (not s["one_off"]) or not recurring_only)


def staffing_scenarios(cap_rows):
    mix_min = {r["approach"]: r for r in cap_rows if r["archetype"] == "market_mix"}
    out = []
    for p in ("conventional", "ai_enhanced", "ai_native", "elimination"):
        for accounts in (1000, 2500, 5000, 10000, 25000, 50000):
            for sponsors in (1, 3, 5, 10):
                if accounts / sponsors < 250:
                    continue
                for lvl in ("base", "high"):
                    m = mix_min[p][f"servicer_min_per_acct_yr_{lvl}"]
                    var_h = accounts * m / 60
                    sp_h = sponsors * sponsor_hours(p, lvl)
                    core = CORE_VARIABLE_HOURS + CORE_CONTROLLER_HOURS
                    extra_h = max(0.0, var_h + sp_h - core)
                    hires = math.ceil(extra_h / (PRODUCTIVE_HOURS * QUEUE_UTILISATION)) if extra_h > 0 else 0
                    dec = mix_min[p]["december_share_of_annual_minutes"]
                    dec_fte_same_sla = (var_h * dec) / (PRODUCTIVE_HOURS * QUEUE_UTILISATION * 20 / 250)
                    # deferral policy: grant SLA relaxed to 10 business days, deferrable work moved to January [A]
                    dec_fte_deferral = dec_fte_same_sla * 0.55
                    avg_fte = (var_h + sp_h) / (PRODUCTIVE_HOURS * QUEUE_UTILISATION)
                    out.append({
                        "approach": p, "accounts": accounts, "sponsors": sponsors, "level": lvl,
                        "servicer_min_per_acct_mix": m, "variable_hours": round(var_h), "sponsor_level_hours": round(sp_h),
                        "core_staff_hours_available": round(core), "additional_hours": round(extra_h),
                        "step_fixed_additional_fte_hires": hires,
                        "average_ops_fte_total": round(avg_fte, 2),
                        "december_ops_fte_same_sla": round(dec_fte_same_sla, 2),
                        "december_ops_fte_with_deferral": round(dec_fte_deferral, 2),
                        "labour_budget_at_40_per_acct_hours": round(accounts * 48 / 60),
                        "fits_48min_allowance": "Y" if m <= 48 else "N",
                        "label": "[D] from [A]",
                    })
    return out


def verification_180_rows():
    out = []
    policies = [
        ("V1 conventional human deep review every 180 days (refresh 30 days early)", "conventional"),
        ("V2 AI-assembled evidence packet, human signs each renewal", "ai_enhanced"),
        ("V3 continuous monitoring + automated renewal + exception-only human + 1% sampling; renew only recipients with pending/scheduled grants", "ai_native"),
        ("V4 event-driven assurance + transaction-time critical checks, no scheduled deep review unless sponsor/class requires", "elimination"),
    ]
    act9 = next(x for x in ACTIVITIES if x["id"] == "ACT-A09")
    act10 = next(x for x in ACTIVITIES if x["id"] == "ACT-A10")
    a = ARCHETYPES["typical"]
    for name, p in policies:
        for gpr_lvl in LEVELS:
            rec = a["grants"] / GRANTS_PER_RECIPIENT[gpr_lvl]
            ren = rec * RENEWALS_PER_RECIPIENT[p]
            for lvl in LEVELS:
                mins_per = act9["m"][p][lvl]
                ev = rec * ADVERSE_EVENTS_PER_RECIPIENT[lvl] * act10["m"][p][lvl]
                per_acct = ren * mins_per + ev
                cost_per_ver = mins_per * RATE_PER_HOUR / 60 + 0.02
                out.append({
                    "policy": name, "approach": p, "grants_per_recipient_level": gpr_lvl,
                    "grants_per_recipient": GRANTS_PER_RECIPIENT[gpr_lvl], "minutes_level": lvl,
                    "distinct_recipients_per_typical_account": round(rec, 2),
                    "renewals_per_recipient_year": round(RENEWALS_PER_RECIPIENT[p], 2),
                    "renewals_per_account_year": round(ren, 2),
                    "human_minutes_per_renewal": mins_per,
                    "cost_per_verification_usd": round(cost_per_ver, 2),
                    "event_monitoring_min_per_account": round(ev, 3),
                    "minutes_per_account_year": round(per_acct, 2),
                    "usd_per_account_year": round(per_acct * RATE_PER_HOUR / 60 + ren * 0.02, 2),
                    "label": "[D] from [A]; replay rates [S] Unbound 14-PUBLIC-DATA-REPLAY.md:36-42",
                })
    return out


def tail_rows():
    """Share of servicer minutes from each archetype in the market mix."""
    out = []
    for p in APPROACHES:
        tot = mixed(lambda x: sum(account_minutes(x, p, "base").values()))
        for k in MIX:
            m = sum(account_minutes(ARCHETYPES[k], p, "base").values())
            out.append({"approach": p, "archetype": k, "mix_share_of_accounts": MIX[k],
                        "min_per_acct": round(m, 1), "share_of_total_minutes": round(MIX[k] * m / tot, 3),
                        "ratio_to_mix_average": round(m / tot, 2)})
    return out


def activities_typical_rows():
    a = ARCHETYPES["typical"]
    rows = []
    for act in ACTIVITIES:
        occ = {p: act["driver"](a, p) for p in APPROACHES}
        rows.append({"id": act["id"], "occ_conv": occ["conventional"], "occ_native": occ["ai_native"],
                     **{f"{p}_{lvl}": act["m"][p][lvl] for p in APPROACHES for lvl in LEVELS},
                     **{f"min_per_acct_{p}": round(minutes_for(act, a, p, "base"), 3) for p in APPROACHES}})
    return rows


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main(out_dir):
    out = Path(out_dir)
    cap = build_capacity_rows()
    write_csv(out / "capacity-model.csv", cap)
    write_csv(out / "staffing-steps.csv", staffing_scenarios(cap))
    write_csv(out / "verification-180.csv", verification_180_rows())
    write_csv(out / "workload-tails.csv", tail_rows())
    write_csv(out / "model" / "activity-minutes-typical.csv", activities_typical_rows())
    print(json.dumps({"sponsor_hours_recurring": {p: {l: sponsor_hours(p, l) for l in LEVELS} for p in APPROACHES}}))


if __name__ == "__main__":
    main(sys.argv[1])
