#!/usr/bin/env python3
"""Operating efficiency and scale economies at DAF sponsors, FY2021-FY2024 (task b51-04).

Stdlib only; functional style (pure transforms, I/O at the edges). Nothing in the repository is modified; earlier
scripts are imported read-only:
  mission_sponsor_compensation  panel() (DAFRC panel with applied corrections), top_sponsors(), SEGMENT
  mission_sponsor_governance    population() (top 50 + the b49-05 seeded sample, SEED 4905), scan_xml_cache()
  mission_sponsor_cost_structure extract_cost_stream() (full Part IX, Part I, Schedule D, Schedule I) and cost_row()
                                (repo-standard operating cost = Part IX line 25 less lines 1-4 and 11f)
  mission_990_contractors       number / CSV helpers, XML_URL

Population
  top50        50 largest sponsors by corrected FY2024 DAF assets (same code as b49-05 and the compensation work)
  sample       the b49-05 seeded random sample of 100 smaller sponsors (Random(4905)), reused for comparability
  supplement   a new seeded draw (SUPP_SEED = 5104) of 40 community foundations and 20 other sponsors from the same
               frame with FY2024 corrected DAF assets >= $10m, not already drawn; it offsets the b49-05 sample's lean
               to sponsors under $10m (queue item P-B4905-01)

Returns: every RETURN_TYPE 990 row in IRS index_2021..2026 for those EINs whose tax period ends in 2021-2024
(FY = calendar year in which the period ends, the DAFRC convention). One return per EIN x FY: latest period end in
that year, then highest OBJECT_ID (picks up amendments).

XML: extract caches first (JSON from mission_sponsor_cost_structure, same extractor version), then local XML copies,
then the GivingTuesday S3 mirror (gt990datalake-rawdata; robots.txt 404 = no restrictions).

Output: data/mission-2026-11-14/sponsor-operating-efficiency-2026-11-20.csv
  record_type = sponsor_year | regression | trend | comparison

Usage:
  python3 scripts/mission_sponsor_efficiency.py . --irs-dir IRS --cache-dir CACHE [--extract-cache DIR ...]
          [--xml-cache DIR ...] [--fetch] [--workers 8]
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import statistics
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Callable, Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as m990  # noqa: E402
import mission_sponsor_cost_structure as mcs  # noqa: E402
from mission_sponsor_compensation import SEGMENT, panel  # noqa: E402
from mission_sponsor_governance import population, scan_xml_cache  # noqa: E402

FYS = (2021, 2022, 2023, 2024)
INDEX_YEARS = (2021, 2022, 2023, 2024, 2025, 2026)
SUPP_SEED = 5104
SUPP_CF, SUPP_OTHER, SUPP_MIN_ASSETS = 40, 20, 1e7
GIVINGA_EIN = "474172718"
OUT_NAME = "sponsor-operating-efficiency-2026-11-20.csv"
UA = {"User-Agent": "research-script/1.0 (stdlib urllib)"}
num, ein9, read_csv, write_csv = m990.num, m990.ein9, m990.read_csv, m990.write_csv
TOKEN_STAFF = 5   # 1-5 employees plus documented affiliate evidence = staffed by the affiliate in substance
AFFIL_COMP_FLAGS = ("affiliate_staffed", "paid_by_related", "split_org_and_related")


# ----------------------------------------------------------------------------- small pure helpers
def div(a, b):
    return a / b if a is not None and b not in (None, 0) else None


def med(xs: Iterable) -> float | None:
    v = [x for x in xs if x is not None]
    return statistics.median(v) if v else None


def q(xs: Iterable, p: float) -> float | None:
    return mcs.quantile([x for x in xs if x is not None], p)


def rnd(x, k=4):
    return None if x is None else round(x, k)


def group_by(items: Iterable, key: Callable) -> dict:
    return reduce(lambda acc, it: {**acc, key(it): acc.get(key(it), ()) + (it,)}, items, {})


# ----------------------------------------------------------------------------- population (pure)
def classify(ein: str, pn: Mapping) -> str:
    """Sponsor type used for the regressions (FY2024 DAFRC type plus the compensation-direction segment)."""
    seg = SEGMENT.get(ein, ("", ""))[0]
    v = pn.get((ein, 2024)) or {}
    if seg == "affiliated_commercial":
        return "national_affiliated"
    if v.get("type") == "National":
        return "processor" if v.get("subtype") == "Donation Processor" else "national_other"
    if v.get("type") == "Community Foundation":
        return "community_foundation"
    return "single_issue"


def supplement(pn: Mapping, taken: frozenset) -> tuple[dict, ...]:
    fy24 = sorted(((v.get("assets") or 0, e) for (e, fy), v in pn.items() if fy == 2024), reverse=True)
    rank = {e: i for i, (_, e) in enumerate(fy24, 1)}
    frame = sorted(e for (e, fy), v in pn.items() if fy == 2024 and e not in taken and rank[e] > 50
                   and (v.get("assets") or 0) >= SUPP_MIN_ASSETS)
    cfs = [e for e in frame if pn[(e, 2024)]["type"] == "Community Foundation"]
    oth = [e for e in frame if pn[(e, 2024)]["type"] != "Community Foundation"]
    picks = random.Random(SUPP_SEED).sample(cfs, SUPP_CF) + random.Random(SUPP_SEED + 1).sample(oth, SUPP_OTHER)
    return tuple({"ein": e, "group": "supplement", "rank_fy2024": rank[e], "sponsor_name": pn[(e, 2024)]["name"],
                  "dafrc_type": pn[(e, 2024)]["type"], "dafrc_subtype": pn[(e, 2024)]["subtype"],
                  "fy2024_daf_assets": pn[(e, 2024)].get("assets"),
                  "frame_size": len(cfs) if pn[(e, 2024)]["type"] == "Community Foundation" else len(oth)}
                 for e in picks)


# ----------------------------------------------------------------------------- returns (I/O edge + pure pick)
def load_index(irs_dir: str, eins: frozenset) -> tuple[dict, ...]:
    def rows(y):
        with open(os.path.join(irs_dir, f"index_{y}.csv"), newline="", encoding="latin-1") as fh:
            yield from ({"ein": ein9(r["EIN"]), "tax_period": r["TAX_PERIOD"], "object_id": r["OBJECT_ID"],
                         "return_type": r["RETURN_TYPE"], "index_year": y}
                        for r in csv.DictReader(fh) if ein9(r["EIN"]) in eins)
    return tuple(r for y in INDEX_YEARS for r in rows(y)
                 if r["tax_period"].isdigit() and int(r["tax_period"][:4]) in FYS)


def pick_returns(idx: Sequence[Mapping]) -> tuple[dict, ...]:
    """One 990 per EIN x FY. Where two periods end in one calendar year (an FYE change or short period), prefer the
    period ending in the sponsor's modal FYE month, then the later period, then the higher OBJECT_ID."""
    full = [{**r, "fy": int(r["tax_period"][:4])} for r in idx if r["return_type"] == "990"]
    months = group_by(full, lambda r: r["ein"])
    modal = {e: max(sorted({r["tax_period"][4:] for r in v}), key=lambda m: sum(1 for r in v if r["tax_period"][4:] == m))
             for e, v in months.items()}
    key = lambda r: (r["tax_period"][4:] == modal[r["ein"]], r["tax_period"], r["object_id"])  # noqa: E731
    better = lambda a, b: key(b) > key(a)  # noqa: E731
    best = reduce(lambda acc, r: {**acc, (r["ein"], r["fy"]): r}
                  if (r["ein"], r["fy"]) not in acc or better(acc[(r["ein"], r["fy"])], r) else acc, full, {})
    n_periods = {k: len({r["tax_period"] for r in full if (r["ein"], r["fy"]) == k}) for k in best}
    return tuple(sorted(({**r, "periods_in_fy": n_periods[(r["ein"], r["fy"])]} for r in best.values()),
                        key=lambda r: (r["ein"], r["fy"])))


def other_forms(idx: Sequence[Mapping], have: frozenset) -> dict:
    """{(ein, fy): return types} for EIN-FYs with no full 990 (990EZ / 990PF filers)."""
    rows = [r for r in idx if (r["ein"], int(r["tax_period"][:4])) not in have]
    return {k: "|".join(sorted({r["return_type"] for r in v}))
            for k, v in group_by(rows, lambda r: (r["ein"], int(r["tax_period"][:4]))).items()}


def read_extract(oid: str, extract_dirs: Sequence[str], xml_cache: Mapping, own_dir: str, fetch: bool) -> dict:
    """Cached cost extract (any dir) -> local XML -> GivingTuesday mirror. Writes only into own_dir."""
    for d in (own_dir, *extract_dirs):
        p = os.path.join(d, f"{oid}.json")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                c = json.load(fh)
            if c.get("_v") == mcs.EXTRACT_VERSION and c.get("xml_status") == "ok":
                return {**c, "extract_source": "cache"}
    url = m990.XML_URL.format(oid=oid)

    def save(res: dict) -> dict:
        os.makedirs(own_dir, exist_ok=True)
        with open(os.path.join(own_dir, f"{oid}.json"), "w", encoding="utf-8") as fh:
            json.dump(res, fh)
        return res
    if oid in xml_cache:
        try:
            with open(xml_cache[oid], "rb") as fh:
                res = {**mcs.extract_cost_stream(fh), "xml_status": "ok", "_v": mcs.EXTRACT_VERSION, "xml_url": url}
            if res.get("part_ix"):
                return {**save(res), "extract_source": "local_xml"}
        except ET.ParseError:
            pass
    if not fetch:
        return {"xml_status": "not_fetched", "xml_url": url}
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                res = {**mcs.extract_cost_stream(r), "xml_status": "ok", "_v": mcs.EXTRACT_VERSION, "xml_url": url}
            return {**save(res), "extract_source": "gt_mirror"}
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"xml_status": f"http_{e.code}", "xml_url": url}
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError):
            time.sleep(2 * (attempt + 1))
    return {"xml_status": "error", "xml_url": url}


# ----------------------------------------------------------------------------- side evidence (pure)
def affiliate_evidence(gov: Sequence[Mapping], comp: Sequence[Mapping]) -> dict:
    """{ein: tuple of evidence labels} that staff or costs sit at a related organisation."""
    seg = {e: ("segment_affiliated_commercial",) if s == "affiliated_commercial" else
           ("segment_note_affiliate",) if "affiliate" in note.lower() else () for e, (s, note) in SEGMENT.items()}
    cf = {r["ein"]: ("comp_" + r["flag_affiliate_pay"],) for r in comp
          if any(k in (r.get("flag_affiliate_pay") or "") for k in AFFIL_COMP_FLAGS)}
    gv = {r["ein"]: ("gov_vi3_delegated_mgmt",) for r in gov if r.get("vi_3_delegated_mgmt") == "Y"}
    eins = set(seg) | set(cf) | set(gv)
    return {e: tuple(x for x in seg.get(e, ()) + cf.get(e, ()) + gv.get(e, ()) if x) for e in eins}


def grant_counts(rows: Sequence[Mapping]) -> dict:
    """FY2024 stated grant counts (primary rows only) from grant-count-denominators-2026-11-20.csv."""
    return {ein9(r["ein"]): {"grant_count": num(r["grant_count"]), "gc_row": r["row_id"], "gc_period": r["period_label"],
                              "gc_status": r["count_status"]}
            for r in rows if r["is_primary"] == "1" and num(r["grant_count"])}


# ----------------------------------------------------------------------------- sponsor-year rows (pure)
def sponsor_year(p: Mapping, x: Mapping, m: Mapping, pn: Mapping, evid: Mapping, gc: Mapping) -> dict:
    d = pn.get((p["ein"], p["fy"])) or {}
    h = {"ein": p["ein"], "sponsor_name": m["sponsor_name"], "type": m["dafrc_type"], "subtype": m["dafrc_subtype"],
         "fiscal_year": p["fy"], "tax_period": p["tax_period"], "return_object_id": p["object_id"],
         "source_url": m990.PP_FILING_URL.format(ein=p["ein"], oid=p["object_id"])}
    c = mcs.cost_row(h, x, {"eoy_daf_assets": d.get("assets"), "number_of_daf_accounts": d.get("accounts")})
    emp = c["employees"]
    opex, tfe = c["operating_cost_ex_invest_mgmt"], c["total_functional_expenses"]
    mg = c["mgmt_col_total"]
    assets, accts = c["daf_assets_eoy"], c["daf_accounts"]
    contrib, grants_usd = c["daf_contributions"], c["daf_grants"]
    share = c["daf_share_of_total_assets"]
    ev = evid.get(p["ein"], ())
    staff_cost = c["staff_cost_l5_10"] or 0
    fee_mgmt = (c["fees_mgmt_l11a"] or 0) + (c["fees_other_l11g"] or 0)
    ev_x = ev + (("990_no_staff_cost_fees_paid",) if emp == 0 and staff_cost == 0 and fee_mgmt > 0 else ())
    model = ("employees_missing" if emp is None else
             "token_staff_affiliate" if 0 < emp <= TOKEN_STAFF and ev else "own_staff" if emp > 0 else
             "affiliate_staffed" if ev_x else "zero_employee_unexplained")
    g = gc.get(p["ein"]) if p["fy"] == 2024 else None
    stype = classify(p["ein"], pn)
    acct_ok = accts not in (None, 0) and assets not in (None, 0) and p["ein"] != GIVINGA_EIN \
        and 1_000 <= assets / accts <= 1e9
    flags = tuple(f for f, cond in (
        ("givinga_undefined_account_unit", p["ein"] == GIVINGA_EIN),
        ("account_count_implausible_or_missing", not acct_ok),
        ("short_period_or_two_returns_in_fy", p["periods_in_fy"] > 1),
        ("opex_nonpositive", opex is not None and opex <= 0),
        ("opex_below_1bp_of_daf_assets", opex is not None and assets and opex / assets < 1e-4),
        ("affiliated_commercial_costs_partly_at_parent", stype == "national_affiliated" and model == "own_staff"),
    ) if cond) + tuple(f for f in (c["quality_flags"] or "").split(";") if f)
    alloc_a = c["daf_alloc_opex_by_assets"]
    return {
        "record_type": "sponsor_year", "ein": p["ein"], "sponsor_name": m["sponsor_name"], "group": m["group"],
        "rank_fy2024": m["rank_fy2024"], "dafrc_type": m["dafrc_type"], "dafrc_subtype": m["dafrc_subtype"],
        "sponsor_type": stype, "segment": SEGMENT.get(p["ein"], ("", ""))[0],
        "fy2024_daf_assets_corrected": m["fy2024_daf_assets"], "fy": p["fy"], "tax_period": p["tax_period"],
        "object_id": p["object_id"], "index_year": p["index_year"], "extract_source": x.get("extract_source", ""),
        "xml_status": x.get("xml_status"), "staffing_model": model, "affiliate_evidence": ";".join(ev_x),
        "employees": emp, "total_functional_expenses": tfe, "mgmt_general_l25c": mg,
        "operating_cost_ex_invest_mgmt": opex, "operating_cost_incl_invest_mgmt": c["operating_cost"],
        "operating_cost_core": None if opex is None else opex - (c["advertising_l12"] or 0) - (c["fees_prof_fundraising_l11e"] or 0),
        "advertising_l12": c["advertising_l12"], "fees_prof_fundraising_l11e": c["fees_prof_fundraising_l11e"],
        "staff_cost_l5_10": c["staff_cost_l5_10"], "fees_mgmt_l11a": c["fees_mgmt_l11a"],
        "fees_other_l11g": c["fees_other_l11g"], "fees_invest_mgmt_l11f": c["fees_invest_mgmt_l11f"],
        "total_assets_eoy": c["total_assets_eoy"],
        "sched_d_daf_accounts": x.get("sched_d_daf_count"), "sched_d_daf_assets_eoy": x.get("sched_d_daf_eoy_value"),
        "sched_d_daf_contributions": x.get("sched_d_daf_contributions"), "sched_d_daf_grants": x.get("sched_d_daf_grants"),
        "daf_accounts_used": accts, "daf_assets_used": assets, "daf_contributions_used": contrib,
        "daf_grants_used": grants_usd, "dafrc_daf_assets_same_fy": d.get("assets"),
        "dafrc_accounts_same_fy": d.get("accounts"), "daf_share_of_total_assets": rnd(share),
        "avg_account_usd": rnd(div(assets, accts), 0) if acct_ok else None,
        "opex_per_daf_account": rnd(div(opex, accts), 1) if acct_ok else None,
        "opex_bps_daf_assets": rnd(div(opex, assets) and div(opex, assets) * 1e4, 2),
        "tfe_bps_daf_assets": rnd(div(tfe, assets) and div(tfe, assets) * 1e4, 2),
        "mg_per_daf_account": rnd(div(mg, accts), 1) if acct_ok else None,
        "mg_bps_daf_assets": rnd(div(mg, assets) and div(mg, assets) * 1e4, 2),
        "daf_opex_alloc_assets": rnd(alloc_a, 0),
        "fees_11a_11g_share_of_opex": rnd(div(fee_mgmt, opex), 4) if opex and opex > 0 else None,
        "daf_opex_alloc_per_account": rnd(div(alloc_a, accts), 1) if acct_ok else None,
        "daf_opex_alloc_bps_daf_assets": rnd(div(alloc_a, assets) and div(alloc_a, assets) * 1e4, 2),
        "daf_assets_per_employee": rnd(div(assets, emp), 0) if model == "own_staff" else None,
        "daf_accounts_per_employee": rnd(div(accts, emp), 2) if model == "own_staff" and acct_ok else None,
        "daf_accounts_per_reported_employee": rnd(div(accts, emp), 2) if emp and acct_ok else None,
        "daf_grants_usd_per_employee": rnd(div(grants_usd, emp), 0) if model == "own_staff" else None,
        "daf_contributions_per_employee": rnd(div(contrib, emp), 0) if model == "own_staff" else None,
        "opex_per_employee": rnd(div(opex, emp), 0) if model == "own_staff" else None,
        "grant_count_fy2024": g and g["grant_count"], "grant_count_row": g and g["gc_row"],
        "grant_count_period": g and g["gc_period"],
        "grants_per_employee": rnd(div(g["grant_count"], emp), 1) if g and model == "own_staff" else None,
        "opex_per_grant": rnd(div(opex, g["grant_count"]), 2) if g else None,
        "sched_i_recipients": c["sched_i_recipients"],
        "sched_i_recipients_per_employee": rnd(div(c["sched_i_recipients"], emp), 1) if model == "own_staff" else None,
        "quality_flags": ";".join(flags), "xml_url": x.get("xml_url"), "source_url": h["source_url"],
    }


def usable(r: Mapping) -> bool:
    """Rows used in medians and regressions: positive opex, DAF assets and a plausible account count."""
    return (r["xml_status"] == "ok" and (r["operating_cost_ex_invest_mgmt"] or 0) > 0 and (r["daf_assets_used"] or 0) > 0
            and r["opex_per_daf_account"] is not None and "opex_below_1bp_of_daf_assets" not in r["quality_flags"])


# ----------------------------------------------------------------------------- OLS with sponsor-clustered SEs (pure)
def transpose(a):
    return [list(c) for c in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(r, c)) for c in bt] for r in a]


def inverse(a):
    n = len(a)
    aug = [list(r) + [1.0 if i == j else 0.0 for j in range(n)] for i, r in enumerate(a)]

    def step(m, col):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            raise ValueError("singular")
        m = [m[piv] if i == col else m[col] if i == piv else m[i] for i in range(n)]
        pr = [v / m[col][col] for v in m[col]]
        return [pr if i == col else [v - m[i][col] * w for v, w in zip(m[i], pr)] for i in range(n)]
    return [r[n:] for r in reduce(step, range(n), aug)]


def ols_cluster(y: Sequence[float], X: Sequence[Sequence[float]], cl: Sequence[str]) -> dict | None:
    n, k = len(y), len(X[0]) if X else 0
    G = len(set(cl))
    if n <= k + 2 or G < 5:
        return None
    try:
        xtx_i = inverse(matmul(transpose(X), X))
    except ValueError:
        return None
    b = [r[0] for r in matmul(xtx_i, matmul(transpose(X), [[v] for v in y]))]
    u = [yi - sum(bj * xj for bj, xj in zip(b, xi)) for yi, xi in zip(y, X)]
    scores = group_by(range(n), lambda i: cl[i])
    sg = [[sum(X[i][j] * u[i] for i in idx) for j in range(k)] for idx in scores.values()]
    meat = [[sum(s[a] * s[c] for s in sg) for c in range(k)] for a in range(k)]
    adj = G / (G - 1) * (n - 1) / (n - k)
    V = [[v * adj for v in r] for r in matmul(matmul(xtx_i, meat), xtx_i)]
    my = sum(y) / n
    r2 = 1 - sum(e * e for e in u) / sum((v - my) ** 2 for v in y)
    return {"b": b, "V": V, "n": n, "clusters": G, "r2": r2}


def design(rows: Sequence[Mapping], dep: str, regs: Sequence[str], extra: Sequence[tuple] = ()) -> tuple:
    rs = [r for r in rows if (r.get(dep) or 0) > 0 and all((r.get(x) or 0) > 0 for x in regs)]
    fys = sorted({r["fy"] for r in rs})[1:]
    names = ["const", *[f"ln_{x}" for x in regs], *[f"fy{f}" for f in fys], *[nm for nm, _ in extra]]
    X = [[1.0, *[math.log(r[x]) for x in regs], *[1.0 if r["fy"] == f else 0.0 for f in fys],
          *[fn(r) for _, fn in extra]] for r in rs]
    return [math.log(r[dep]) for r in rs], X, [r["ein"] for r in rs], names


def regression_rows(label: str, sample: str, rows: Sequence[Mapping], dep: str, regs: Sequence[str],
                    extra: Sequence[tuple] = ()) -> list:
    y, X, cl, names = design(rows, dep, regs, extra)
    fit = ols_cluster(y, X, cl) if X else None
    if not fit:
        return [{"record_type": "regression", "model": label, "reg_sample": sample, "dependent": dep, "n_obs": len(y),
                 "note": "too few observations"}]
    se = lambda i: math.sqrt(fit["V"][i][i])  # noqa: E731
    out = [{"record_type": "regression", "model": label, "reg_sample": sample, "dependent": dep, "term": nm,
            "coef": rnd(fit["b"][i]), "se_cluster": rnd(se(i)), "t": rnd(fit["b"][i] / se(i), 2) if se(i) else None,
            "n_obs": fit["n"], "n_sponsors": fit["clusters"], "r2": rnd(fit["r2"])} for i, nm in enumerate(names)]
    ix = [i for i, nm in enumerate(names) if nm.startswith("ln_daf_")]
    if len(ix) >= 1:
        s = sum(fit["b"][i] for i in ix)
        v = sum(fit["V"][i][j] for i in ix for j in ix)
        sd = math.sqrt(v) if v > 0 else None
        out.append({"record_type": "regression", "model": label, "reg_sample": sample, "dependent": dep,
                    "term": "scale_elasticity_sum_daf_terms", "coef": rnd(s), "se_cluster": rnd(sd),
                    "t": rnd((s - 1) / sd, 2) if sd else None, "n_obs": fit["n"], "n_sponsors": fit["clusters"],
                    "r2": rnd(fit["r2"]), "note": "t tests H0: elasticity = 1 (no scale economies)"})
    return out


REG_TYPES = ("national_other", "national_affiliated", "community_foundation", "single_issue")


def all_regressions(rows: Sequence[Mapping], universe: Sequence[Mapping]) -> list:
    use = [r for r in rows if usable(r)]
    own = [r for r in use if r["staffing_model"] == "own_staff"]
    aff = [r for r in use if r["staffing_model"] != "own_staff"]
    by_type = lambda rs, t: [r for r in rs if r["sponsor_type"] == t]  # noqa: E731
    both = ("daf_assets_used", "daf_accounts_used")
    specs = [
        *[x for t in REG_TYPES for x in regression_rows("M1_opex_assets_accounts", f"own_staff:{t}", by_type(own, t),
                                                         "operating_cost_ex_invest_mgmt", both)],
        *[x for t in REG_TYPES for x in regression_rows("M2_opex_assets_only", f"own_staff:{t}", by_type(own, t),
                                                         "operating_cost_ex_invest_mgmt", ("daf_assets_used",))],
        *[x for t in REG_TYPES for x in regression_rows("M3_mg_assets_accounts", f"own_staff:{t}", by_type(own, t),
                                                         "mgmt_general_l25c", both)],
        *[x for t in REG_TYPES for x in regression_rows("M4_opex_assets_accounts_totalassets", f"own_staff:{t}",
                                                         by_type(own, t), "operating_cost_ex_invest_mgmt",
                                                         (*both, "total_assets_eoy"))],
        *regression_rows("M1_opex_assets_accounts", "affiliate_or_zero_staff:all", aff,
                         "operating_cost_ex_invest_mgmt", both),
        *regression_rows("M1_opex_assets_accounts", "affiliate_or_zero_staff:nationals_ex_processor",
                         [r for r in aff if r["sponsor_type"] in ("national_other", "national_affiliated")],
                         "operating_cost_ex_invest_mgmt", both),
        *regression_rows("M1_opex_assets_accounts", "affiliate_or_zero_staff:cf_and_single_issue",
                         [r for r in aff if r["sponsor_type"] in ("community_foundation", "single_issue")],
                         "operating_cost_ex_invest_mgmt", both),
        *regression_rows("M1_opex_assets_accounts", "all_staffing:national_affiliated",
                         by_type(use, "national_affiliated"), "operating_cost_ex_invest_mgmt", both),
        *regression_rows("M1_opex_assets_accounts", "all_staffing:nationals_ex_processor",
                         [r for r in use if r["sponsor_type"] in ("national_other", "national_affiliated")],
                         "operating_cost_ex_invest_mgmt", both),
        *regression_rows("M2_opex_assets_only", "all_staffing:nationals_ex_processor",
                         [r for r in use if r["sponsor_type"] in ("national_other", "national_affiliated")],
                         "operating_cost_ex_invest_mgmt", ("daf_assets_used",)),
        *regression_rows("M7_core_opex_assets_accounts", "all_staffing:nationals_ex_processor",
                         [r for r in use if r["sponsor_type"] in ("national_other", "national_affiliated")],
                         "operating_cost_core", both),
        *regression_rows("M7_core_opex_assets_accounts", "own_staff:national_other",
                         by_type(own, "national_other"), "operating_cost_core", both),
        *regression_rows("M5_pooled_with_affiliate_dummy", "all_usable", use, "operating_cost_ex_invest_mgmt", both,
                         (("affiliate_or_zero_staff", lambda r: 1.0 if r["staffing_model"] != "own_staff" else 0.0),
                          *((f"type_{t}", (lambda t: lambda r: 1.0 if r["sponsor_type"] == t else 0.0)(t))
                            for t in ("national_affiliated", "community_foundation", "single_issue", "processor")))),
        *regression_rows("M6_employees_assets_accounts", "own_staff:all_ex_processor",
                         [r for r in own if r["sponsor_type"] != "processor"], "employees", both),
        *[x for t in ("community_foundation", "single_issue") for x in regression_rows(
            "M6_employees_assets_accounts", f"own_staff:{t}", by_type(own, t), "employees", both)],
    ]
    uni = [{**r, "daf_accounts_used": num(r["daf_accounts"]), "daf_assets_used": num(r["daf_assets_eoy"]),
            "operating_cost_ex_invest_mgmt": num(r["operating_cost_ex_invest_mgmt"]), "fy": int(r["fiscal_year"])}
           for r in universe if r["fiscal_year"] in ("2022", "2023", "2024") and r["ein"] != GIVINGA_EIN
           and (num(r["employees"]) or 0) > 0 and "givinga" not in (r["quality_flags"] or "")
           and (num(r["daf_assets_eoy"]) or 0) > 0 and (num(r["daf_accounts"]) or 0) > 0
           and 1_000 <= num(r["daf_assets_eoy"]) / num(r["daf_accounts"]) <= 1e9]
    ucat = {"National-Standard": "national_standard", "Community": "community_foundation"}
    robust = [x for cat, lab in ucat.items() for x in regression_rows(
        "R1_full_universe_fy2022_24_opex_assets_accounts", f"cost_structure_universe_employees_gt0:{lab}",
        [r for r in uni if r["category"] == cat], "operating_cost_ex_invest_mgmt", both)] + regression_rows(
        "R1_full_universe_fy2022_24_opex_assets_accounts", "cost_structure_universe_employees_gt0:single_issue",
        [r for r in uni if r["category"].startswith("SingleIssue")], "operating_cost_ex_invest_mgmt", both)
    return specs + robust


# ----------------------------------------------------------------------------- trends and comparisons (pure)
TREND_METRICS = ("opex_per_daf_account", "opex_bps_daf_assets", "mg_bps_daf_assets", "daf_opex_alloc_bps_daf_assets",
                 "daf_opex_alloc_per_account", "daf_assets_per_employee", "daf_accounts_per_employee",
                 "daf_grants_usd_per_employee", "opex_per_employee", "employees", "avg_account_usd")


def trend_rows(rows: Sequence[Mapping]) -> list:
    use = [r for r in rows if usable(r)]
    full = {e for e, v in group_by(use, lambda r: r["ein"]).items() if {r["fy"] for r in v} == set(FYS)}
    cells = [(panel_lab, model, t) for panel_lab in ("all_usable", "balanced_fy2021_24")
             for model in ("own_staff", "affiliate_or_zero_staff") for t in REG_TYPES]

    def sel(panel_lab, model, t, fy):
        return [r for r in use if r["fy"] == fy and r["sponsor_type"] == t
                and ((r["staffing_model"] == "own_staff") == (model == "own_staff"))
                and (panel_lab == "all_usable" or r["ein"] in full)]
    out = []
    for panel_lab, model, t in cells:
        for fy in FYS:
            rs = sel(panel_lab, model, t, fy)
            if not rs:
                continue
            pooled_opex = sum(r["operating_cost_ex_invest_mgmt"] for r in rs)
            pooled_assets = sum(r["daf_assets_used"] for r in rs)
            pooled_accts = sum(r["daf_accounts_used"] for r in rs)
            out += [{"record_type": "trend", "trend_panel": panel_lab, "staffing_model": model, "sponsor_type": t,
                     "fy": fy, "metric": mt, "n_obs": sum(1 for r in rs if r.get(mt) is not None),
                     "p25": rnd(q((r.get(mt) for r in rs), .25), 2), "median": rnd(med(r.get(mt) for r in rs), 2),
                     "p75": rnd(q((r.get(mt) for r in rs), .75), 2)} for mt in TREND_METRICS
                    if any(r.get(mt) is not None for r in rs)]
            out += [{"record_type": "trend", "trend_panel": panel_lab, "staffing_model": model, "sponsor_type": t,
                     "fy": fy, "metric": "pooled_opex_bps_daf_assets", "n_obs": len(rs),
                     "median": rnd(pooled_opex / pooled_assets * 1e4, 2)},
                    {"record_type": "trend", "trend_panel": panel_lab, "staffing_model": model, "sponsor_type": t,
                     "fy": fy, "metric": "pooled_opex_per_daf_account", "n_obs": len(rs),
                     "median": rnd(pooled_opex / pooled_accts, 1)}]
    # within-sponsor log change FY2021 -> FY2024 (balanced panel)
    by = group_by([r for r in use if r["ein"] in full], lambda r: r["ein"])
    for model in ("own_staff", "affiliate_or_zero_staff"):
        for t in REG_TYPES:
            ss = [v for v in by.values() if v[0]["sponsor_type"] == t and
                  ((next(r for r in v if r["fy"] == 2024)["staffing_model"] == "own_staff") == (model == "own_staff"))]
            if not ss:
                continue
            ch = lambda f: [math.log(next(r for r in v if r["fy"] == 2024)[f] / next(r for r in v if r["fy"] == 2021)[f])  # noqa: E731
                            for v in ss if all((r.get(f) or 0) > 0 for r in v)]
            out += [{"record_type": "trend", "trend_panel": "balanced_fy2021_24", "staffing_model": model,
                     "sponsor_type": t, "fy": "2021->2024", "metric": f"median_log_change:{f}", "n_obs": len(ch(f)),
                     "p25": rnd(q(ch(f), .25)), "median": rnd(med(ch(f))), "p75": rnd(q(ch(f), .75))}
                    for f in ("operating_cost_ex_invest_mgmt", "daf_assets_used", "daf_accounts_used",
                              "opex_bps_daf_assets", "opex_per_daf_account", "employees")]
    return out


CF_BANDS = ((1e9, "A_ge_1bn"), (1e8, "B_100m_1bn"), (1e7, "C_10m_100m"), (0, "D_lt_10m"))
BAND_METRICS = ("opex_bps_daf_assets", "daf_opex_alloc_bps_daf_assets", "mg_bps_daf_assets", "opex_per_daf_account",
                "daf_opex_alloc_per_account", "avg_account_usd", "daf_accounts_per_employee", "daf_assets_per_employee",
                "employees", "daf_share_of_total_assets", "fees_11a_11g_share_of_opex")


def band_of(a) -> str:
    return next(lab for lo, lab in CF_BANDS if (a or 0) >= lo)


def band_rows(rows: Sequence[Mapping]) -> list:
    """Medians by FY2024 size band (corrected DAFRC assets) for FY2021 and FY2024; nationals split by staffing."""
    use = [r for r in rows if usable(r)]
    cells = (
        *((f"community_foundation:{b}", (lambda b: lambda r: r["sponsor_type"] == "community_foundation"
                                         and r["staffing_model"] == "own_staff"
                                         and band_of(r["fy2024_daf_assets_corrected"]) == b)(b)) for _, b in CF_BANDS),
        ("community_foundation:top50", lambda r: r["sponsor_type"] == "community_foundation" and r["group"] == "top50"),
        ("community_foundation:non_top50_lt_50m", lambda r: r["sponsor_type"] == "community_foundation"
         and r["group"] != "top50" and (r["fy2024_daf_assets_corrected"] or 0) < 5e7),
        ("single_issue:own_staff", lambda r: r["sponsor_type"] == "single_issue" and r["staffing_model"] == "own_staff"),
        ("nationals_top50:all_staffing", lambda r: r["group"] == "top50"
         and r["sponsor_type"] in ("national_other", "national_affiliated")),
        ("nationals_top50:own_staff", lambda r: r["group"] == "top50" and r["staffing_model"] == "own_staff"
         and r["sponsor_type"] in ("national_other", "national_affiliated")),
        ("nationals_top50:affiliate_or_zero_staff", lambda r: r["group"] == "top50" and r["staffing_model"] != "own_staff"
         and r["sponsor_type"] in ("national_other", "national_affiliated")),
        ("affiliate_or_zero_staff:non_national", lambda r: r["staffing_model"] != "own_staff"
         and r["sponsor_type"] in ("community_foundation", "single_issue")),
    )
    return [{"record_type": "band", "trend_panel": lab, "fy": fy, "metric": mt,
             "n_obs": sum(1 for r in rs if r.get(mt) is not None),
             "p25": rnd(q((r.get(mt) for r in rs), .25), 2), "median": rnd(med(r.get(mt) for r in rs), 2),
             "p75": rnd(q((r.get(mt) for r in rs), .75), 2)}
            for lab, sel in cells for fy in FYS for rs in [[r for r in use if r["fy"] == fy and sel(r)]]
            for mt in BAND_METRICS if rs]


def comparison_rows(rows: Sequence[Mapping], gov: Sequence[Mapping], comp: Sequence[Mapping],
                    tail: Sequence[Mapping]) -> list:
    sy = {r["object_id"]: r for r in rows}
    gmatch = [(g, sy[g["object_id"]]) for g in gov if g["object_id"] in sy and g.get("i_5_employees") not in ("", None)]
    g_same = sum(1 for g, r in gmatch if num(g["i_5_employees"]) == r["employees"])
    cmatch = [(c, sy[c["object_id"]]) for c in comp if c["object_id"] in sy and c.get("employees_part_i_5") not in ("", None)]
    c_same = sum(1 for c, r in cmatch if num(c["employees_part_i_5"]) == r["employees"])
    c_l25 = sum(1 for c, r in cmatch if num(c["l25_total_expenses"]) == r["total_functional_expenses"])
    g_zero = {g["ein"] for g in gov if g.get("tax_year") == "2024" and num(g.get("i_5_employees")) == 0}
    mine_zero24 = {r["ein"] for r in rows if r["fy"] == 2024 and r["employees"] == 0}
    tl = {r["return_object_id"]: r for r in tail if r.get("usable") in ("1", "True", "yes")}
    tmatch = [(t, sy[o]) for o, t in tl.items() if o in sy and t.get("opex_ex_11f")]
    t_same = sum(1 for t, r in tmatch if abs((num(t["opex_ex_11f"]) or 0) - (r["operating_cost_ex_invest_mgmt"] or 0)) < 1)
    rec = lambda k, n, v, note: {"record_type": "comparison", "metric": k, "n_obs": n, "median": v, "note": note}  # noqa: E731
    return [
        rec("governance_employees_same_return_match", len(gmatch), g_same,
            "b49-05 i_5_employees vs this Part I line 5, same object_id: matches (median col) of n"),
        rec("compensation_employees_same_return_match", len(cmatch), c_same,
            "compensation employees_part_i_5 vs this Part I line 5, same object_id: matches of n"),
        rec("compensation_l25_same_return_match", len(cmatch), c_l25, "compensation l25_total_expenses vs this line 25"),
        rec("governance_zero_employee_tY2024_in_this_fy2024_zero", len(g_zero), len(g_zero & mine_zero24),
            "b49-05 zero-employee sponsors (TY2024) that are also zero here in FY2024 (FY and TY differ for non-calendar filers)"),
        rec("long_tail_opex_same_return_match", len(tmatch), t_same,
            "b45n33 opex_ex_11f vs this operating_cost_ex_invest_mgmt, same object_id (to $1)"),
    ]


# ----------------------------------------------------------------------------- report printing
def fmt(v, k=0):
    return "" if v is None else f"{v:,.{k}f}"


def print_report(rows, regs, trends, comps, pop, picks, other):
    by_fy = group_by(rows, lambda r: r["fy"])
    print("## Coverage")
    print("population", len(pop), {g: sum(1 for m in pop if m["group"] == g) for g in ("top50", "sample", "supplement")})
    print("returns picked", len(picks), {fy: len(by_fy.get(fy, ())) for fy in FYS})
    print("xml_status", {k: len(v) for k, v in group_by(rows, lambda r: r["xml_status"]).items()})
    print("extract_source", {k: len(v) for k, v in group_by(rows, lambda r: r["extract_source"]).items()})
    print("usable", {fy: sum(1 for r in by_fy.get(fy, ()) if usable(r)) for fy in FYS})
    print("no full 990 EIN-FY", len(other), sorted(set(other.values())))
    print("staffing_model x fy", {(k, fy): sum(1 for r in v if r["fy"] == fy)
                                  for k, v in group_by(rows, lambda r: r["staffing_model"]).items() for fy in FYS})
    print("type x group (FY2024 rows)", {k: len(v) for k, v in group_by(
        [r for r in rows if r["fy"] == 2024], lambda r: (r["sponsor_type"], r["group"])).items()})
    print("\n## Zero-employee sponsors (any FY)")
    for e, v in sorted(group_by([r for r in rows if r["staffing_model"] != "own_staff"], lambda r: r["ein"]).items()):
        print(e, v[0]["sponsor_name"][:40], v[0]["group"], v[0]["sponsor_type"], [r["fy"] for r in v],
              v[-1]["staffing_model"], v[-1]["affiliate_evidence"], "opex", fmt(v[-1]["operating_cost_ex_invest_mgmt"]),
              "bps", v[-1]["opex_bps_daf_assets"], "11a+11g", fmt((v[-1]["fees_mgmt_l11a"] or 0) + (v[-1]["fees_other_l11g"] or 0)))
    print("\n## Regressions")
    for r in regs:
        if r.get("term") in (None, "ln_daf_assets_used", "ln_daf_accounts_used", "ln_total_assets_eoy",
                             "scale_elasticity_sum_daf_terms", "affiliate_or_zero_staff"):
            print(r["model"], r["reg_sample"], r.get("dependent"), r.get("term"), r.get("coef"), r.get("se_cluster"),
                  r.get("t"), r["n_obs"], r.get("n_sponsors"), r.get("r2"), r.get("note", ""))
    print("\n## Trends")
    for r in trends:
        if r["metric"] in ("opex_bps_daf_assets", "opex_per_daf_account", "daf_assets_per_employee",
                           "daf_accounts_per_employee", "pooled_opex_bps_daf_assets", "mg_bps_daf_assets",
                           "daf_opex_alloc_bps_daf_assets", "daf_grants_usd_per_employee", "employees") \
                or r["metric"].startswith("median_log_change"):
            print(r["trend_panel"], r["staffing_model"], r["sponsor_type"], r["fy"], r["metric"], r["n_obs"],
                  r.get("p25"), r["median"], r.get("p75"))
    print("\n## Comparisons")
    for r in comps:
        print(r["metric"], r["n_obs"], r["median"], r["note"])
    print("\n## Grant counts per employee (FY2024)")
    for r in rows:
        if r["grant_count_fy2024"]:
            print(r["sponsor_name"][:40], r["staffing_model"], r["employees"], fmt(r["grant_count_fy2024"]),
                  r["grant_count_period"], "grants/emp", r["grants_per_employee"], "opex/grant", r["opex_per_grant"],
                  "acc/emp", r["daf_accounts_per_employee"], "assets/emp", fmt(r["daf_assets_per_employee"]))


FIELDS = ("record_type", "ein", "sponsor_name", "group", "rank_fy2024", "dafrc_type", "dafrc_subtype", "sponsor_type",
          "segment", "fy2024_daf_assets_corrected", "fy", "tax_period", "object_id", "index_year", "extract_source",
          "xml_status", "staffing_model", "affiliate_evidence", "employees", "total_functional_expenses",
          "mgmt_general_l25c", "operating_cost_ex_invest_mgmt", "operating_cost_incl_invest_mgmt", "operating_cost_core",
          "advertising_l12", "fees_prof_fundraising_l11e", "staff_cost_l5_10", "fees_mgmt_l11a", "fees_other_l11g", "fees_invest_mgmt_l11f", "total_assets_eoy", "sched_d_daf_accounts",
          "sched_d_daf_assets_eoy", "sched_d_daf_contributions", "sched_d_daf_grants", "daf_accounts_used",
          "daf_assets_used", "daf_contributions_used", "daf_grants_used", "dafrc_daf_assets_same_fy",
          "dafrc_accounts_same_fy", "daf_share_of_total_assets", "avg_account_usd", "opex_per_daf_account",
          "opex_bps_daf_assets", "tfe_bps_daf_assets", "mg_per_daf_account", "mg_bps_daf_assets",
          "daf_opex_alloc_assets", "fees_11a_11g_share_of_opex", "daf_opex_alloc_per_account", "daf_opex_alloc_bps_daf_assets",
          "daf_assets_per_employee", "daf_accounts_per_employee", "daf_accounts_per_reported_employee",
          "daf_grants_usd_per_employee", "daf_contributions_per_employee", "opex_per_employee", "grant_count_fy2024", "grant_count_row",
          "grant_count_period", "grants_per_employee", "opex_per_grant", "sched_i_recipients",
          "sched_i_recipients_per_employee", "usable", "quality_flags", "xml_url", "source_url",
          "model", "reg_sample", "dependent", "term", "coef", "se_cluster", "t", "n_obs", "n_sponsors", "r2",
          "trend_panel", "metric", "p25", "median", "p75", "note")


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--cache-dir", required=True, help="own extract cache (JSON written here only)")
    ap.add_argument("--extract-cache", action="append", default=[], help="read-only extract990cost dirs")
    ap.add_argument("--xml-cache", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args(argv)
    data = os.path.join(os.path.abspath(a.root), "data", "mission-2026-11-14")
    pn = panel(read_csv(os.path.join(data, "dafrc-sponsor-schedule-d-fy2019-2024.csv")),
               read_csv(os.path.join(data, "dafrc-corrections-itemized.csv")))
    base = population(pn)
    pop = tuple(base) + supplement(pn, frozenset(m["ein"] for m in base))
    meta = {m["ein"]: m for m in pop}
    idx = load_index(a.irs_dir, frozenset(meta))
    picks = pick_returns(idx)
    other = other_forms(idx, frozenset((p["ein"], p["fy"]) for p in picks))
    xml_cache = scan_xml_cache(a.xml_cache) if a.xml_cache else {}
    with ThreadPoolExecutor(a.workers) as ex:
        exts = dict(zip((p["object_id"] for p in picks), ex.map(
            lambda p: read_extract(p["object_id"], a.extract_cache, xml_cache, a.cache_dir, a.fetch), picks)))
    gov = [r for r in read_csv(os.path.join(data, "sponsor-governance-quality-2026-11-20.csv")) if r["record_type"] == "sponsor_year"]
    comp = [r for r in read_csv(os.path.join(data, "sponsor-executive-compensation-2021-2025.csv")) if r["record_type"] == "sponsor_year"]
    gc = grant_counts(read_csv(os.path.join(data, "grant-count-denominators-2026-11-20.csv")))
    evid = affiliate_evidence(gov, comp)
    rows = [sponsor_year(p, exts[p["object_id"]], meta[p["ein"]], pn, evid, gc) for p in picks]
    rows = [{**r, "usable": int(usable(r))} for r in rows]
    universe = read_csv(os.path.join(data, "sponsor-cost-structure.csv"))
    regs = all_regressions(rows, universe)
    trends = trend_rows(rows)
    tail = read_csv(os.path.join(data, "long-tail-operating-cost-2026-11-19.csv"))
    comps = comparison_rows(rows, gov, comp, tail)
    bands = band_rows(rows)
    write_csv(os.path.join(data, OUT_NAME), rows + regs + trends + bands + comps, FIELDS)
    print("\n## Bands")
    for r in bands:
        if r["fy"] in (2021, 2024):
            print(r["trend_panel"], r["fy"], r["metric"], r["n_obs"], r["p25"], r["median"], r["p75"])
    print_report(rows, regs, trends, comps, pop, picks, other)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
