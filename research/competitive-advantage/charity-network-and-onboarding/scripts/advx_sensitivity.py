"""ADVX sensitivity runs. Loads the package model read-only via importlib; never writes package files.
Pure functions; I/O only in main. Python 3 stdlib."""
import importlib.util, math, sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent

def load_model():
    spec = importlib.util.spec_from_file_location("eco", PKG / "scripts" / "economic_model.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def override(params, changes):
    """Return new params tuple with base/low/high replaced for named params (all three set to value)."""
    return tuple(p._replace(low=changes[p.name], base=changes[p.name], high=changes[p.name])
                 if p.name in changes else p for p in params)

def run(m, params, n, fee, changes=None, q="typical", b="base", g="base", c="base"):
    ps = override(params, changes or {})
    return m.evaluate(ps, m.Scenario(n, g, q, b, fee, c))

def per_account_payback(r, n, price):
    margin = price * n - r["cost_recurring_total"]
    return r["acquisition_and_onboarding_total"] / (margin / 12) if margin > 0 else math.inf

def fm(x):
    return "never" if x == math.inf else f"{x:,.1f}"

def main():
    m = load_model()
    params = m.read_params(m.PARAMS_PATH)
    out = []
    # 1. Fee sensitivity for 10k and 1k, base and high cost
    for n in (1_000, 10_000):
        for fee in (5, 10, 12.5, 15, 20):
            for c in ("base", "high"):
                r = run(m, params, n, fee, c=c)
                out.append(("fee", n, fee, c, round(r["revenue"]), round(r["contribution"]),
                            round(r["acquisition_and_onboarding_total"]), fm(r["payback_months"]), r["classification"]))
    # 2. Per-account price anchors (observed: Ren software $34-81 at NCF/Thrivent; $236-611 other software; staffed $389-815)
    for n in (1_000, 10_000):
        for c in ("base", "high"):
            r = run(m, params, n, 20, c=c)
            for price in (60, 81, 150, 250, 437, 737):
                out.append(("per_account", n, price, c, round(price * n), round(price * n - r["cost_recurring_total"]),
                            round(r["acquisition_and_onboarding_total"]), fm(per_account_payback(r, n, price)), ""))
    # 3. 08-consistent network parameters
    for label, ch in (("pkg_base", {}),
                      ("08_consistent", {"partner_coverage": 0.08, "check_share_target": 0.30}),
                      ("08_cov_only", {"partner_coverage": 0.08})):
        r = run(m, params, 10_000, 20, ch)
        out.append(("network", 10_000, label, "base", round(r["onb_charity_enrolment"]),
                    round(r["value_epay_sponsor_passthrough_saving_yr"] + r["value_epay_unbound_labour_saving_yr"]),
                    round(r["value_network_enrolment_avoided_at_onboarding"]), fm(r["payback_months"]), r["classification"]))
    # 4. Track A omitted platform opex (ADVX ASSUMPTIONS), per grant at network sizes
    # ECO revision 3 folded these items into registry_annual_cost; subtract them to keep the pre-revision baseline.
    _reg = m.registry_annual_cost(m.resolve_cost_case(params, "base"))
    base_reg = _reg["annual_fixed_total_usd"] - _reg.get("annual_registry_ops_compliance_usd", 0.0)
    omitted = {  # low, base, high USD/yr; ASSUMPTION ranges anchored on servicing-economics cost-register rows
        "registry_stewardship_compliance_fte(CST-R10 0.5-1.0 FTE)": (60924, 121848, 147744),
        "charity_support_desk(CST-R13 0.25-1.0 FTE)": (19277, 38554, 77108),
        "counsel_eligibility_rules_review(CST-C06 $450/h x 40-130h)": (12000, 36000, 104000),
        "nacha_tpsp_rules_compliance_audit+risk_assessment": (8000, 15000, 30000),
        "verification_vendor_minimums(EWS/Plaid/Phixius 2 vendors)": (0, 24000, 60000),
        "media/defamation liability rider if publishing": (0, 5000, 15000),
    }
    for i, case in enumerate(("low", "base", "high")):
        add = sum(v[i] for v in omitted.values())
        for grants in (70_000, 210_000, 700_000):
            out.append(("trackA", grants, case, "", round(base_reg), round(add), round(base_reg + add),
                        f"{base_reg/grants:.2f}->{(base_reg+add)/grants:.2f}", ""))
    for row in out:
        print(",".join(str(x) for x in row))
    return 0


def company_level(m, params, org_fixed=1_660_006, build_amort=1_000_000):
    """First-sponsor view: contribution must also carry org fixed (servicing-economics 03 base) and build amortisation
    (servicing-economics 06 / Unbound $5M over 5 yrs). Returns rows."""
    rows = []
    for n in (1_000, 10_000):
        for fee in (10, 12.5, 15, 20):
            for c in ("base", "high"):
                r = run(m, params, n, fee, c=c)
                net = r["contribution"] - org_fixed - build_amort
                pb = r["acquisition_and_onboarding_total"] / (net / 12) if net > 0 else math.inf
                rows.append(("company_first_sponsor", n, fee, c, round(r["contribution"]), round(net),
                             round(r["acquisition_and_onboarding_total"]), fm(pb), ""))
    return rows

if __name__ == "__main__" and "--company" in sys.argv:
    mm = load_model(); pp = mm.read_params(mm.PARAMS_PATH)
    for row in company_level(mm, pp):
        print(",".join(str(x) for x in row))

if __name__ == "__main__" and "--company" not in sys.argv:
    raise SystemExit(main())
