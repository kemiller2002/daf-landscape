#!/usr/bin/env python3
"""Community-foundation local share for the 100 largest community foundations, FY2023-FY2024 (queue item P-B42N21-02).

Extends the own-state / own-metro measure of scripts/mission_grant_geography.py (P-NEW-GEO-01; 22 top-50 CFs) to the
100 community foundations of data/mission-2026-11-14/cf-daf-fee-census-2026.csv (ranks 1-100 by FY2024 DAF assets,
DAFRC panel), and asks whether the local share falls as the DAF share of grants rises.

Definitions (unchanged from P-NEW-GEO-01)
  returns        one return per EIN x fiscal year (calendar year of tax-period end) via mission_daf_to_daf.pick_returns
                 over the netpayout990/ cache; FY2023-FY2024 (tax years 2022-2024); Schedule I must itemise
                 (mission_net_payout.itemized).
  lines          every Schedule I Part II RecipientTable line (cash + non-cash), re-read in full from the e-file XML
                 (local copy, else GivingTuesday mirror of IRS TEOS). A return is used only when its re-read line count
                 equals the cache's sched_i_lines and the dollar total is within 0.5% of sched_i_total.
  DAF-to-DAF     lines to `include` EINs of daf-to-daf-recipient-whitelist.csv, self-lines and blank-EIN lines whose
                 name matches one whitelisted sponsor are removed (mission_recipient_sectors.annotate, unchanged).
  state / CBSA   mission_grant_geography.geo_line, unchanged: Schedule I state (else BMF state); ZIP5 -> 2020 ZCTA ->
                 largest-land-overlap county -> 2023 CBSA, ZIP3 fallback for non-ZCTA ZIPs.
  home           sponsor EO BMF STATE/ZIP (else the return's Filer address).
  own_state      dollars to recipients in the home state / US-located dollars.
  own_metro      dollars to the home CBSA / CBSA-resolved dollars.
  own_county     (added here) dollars to the home county / county-resolved dollars (ZCTA lines only).

DAF vs discretionary split
  Schedule I purpose text is scanned for explicit DAF markers and explicit discretionary markers (regexes below).
  A split local share (DAF-flagged lines vs all other lines) is reported for a CF only when DAF-flagged lines hold
  between SPLIT_MIN and SPLIT_MAX of its US dollars, i.e. when the filer labels DAF grants line by line.
  The covariate used for every CF is the Schedule D DAF share of grants (sponsor-cost-structure.csv
  daf_grants / grants_part_ix_l1_3, pooled over the CF's itemised FYs, capped at 1). A CF-year with negative
  Schedule D DAF grants (a filing sign error) leaves the covariate blank and is flagged.

Statistics: Pearson r with Fisher-z 95% CI; Spearman rho with a percentile bootstrap CI (2,000 resamples, fixed seed);
OLS of each share on DAF share with log10 DAF assets and log10 US Schedule I dollars, classical and HC1 SEs.

Stdlib only; functional style (pure transforms, I/O at the edges).

Usage:
  python3 scripts/mission_cf_local_share_top100.py . --np-cache NPCACHE --bmf-dir BMF --census-dir CENSUS \
      --line-cache LC --xml-list FILE [--fetch] [--summary OUT.json]
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, load_np, pick_returns  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import WHITELIST, annotate  # noqa: E402
from mission_grant_geography import (US_CODES, cbsa_of, cbsa_tables, geo_line, scan_bmf, zcta_county,  # noqa: E402
                                     zip3_fallback)

LINES_V = 1
SPLIT_MIN, SPLIT_MAX = 0.10, 0.90
UA = "research-script/1.0"
DAF_RX = re.compile(r"DONOR[- ]?ADVISED|\bDAF\b|ADVISED FUND|DONOR[- ]ADVISOR|ADVISED GRANT")
DISC_RX = re.compile(r"DISCRETIONARY|COMPETITIVE|RESPONSIVE GRANT|COMMUNITY GRANT|BOARD[- ]DESIGNATED|"
                     r"FIELD[- ]OF[- ]INTEREST|UNRESTRICTED FUND|IMPACT GRANT|STRATEGIC INITIATIVE")
SOURCE = ("IRS Form 990 Schedule I Part II e-file XML (GivingTuesday mirror of IRS TEOS), FY2023-2024, DAF-to-DAF "
          "lines excluded; universe cf-daf-fee-census-2026.csv ranks 1-100 (DAFRC FY2024 DAF assets); IRS EO BMF "
          "2026-11; Census rel2020 ZCTA520-county and cbsa-est2024-alldata (2023 delineations); DAF share of grants "
          "from sponsor-cost-structure.csv (Schedule D Part I / Part IX lines 1-3)")


# ----------------------------------------------------------------------------- 1. parse
def line_of(el) -> list:
    """-> [ein, name, where, irc, cash, noncash, zip5, city, purpose] (first six as mission_recipient_sectors)."""
    g = {local(c.tag): c for c in el.iter()}
    t = lambda k: (g[k].text or "").strip() if k in g and g[k].text else ""  # noqa: E731
    name = " ".join((c.text or "").strip() for c in el.iter()
                    if local(c.tag) in ("BusinessNameLine1Txt", "BusinessNameLine2Txt") and c.text)
    where = t("StateAbbreviationCd") or ("F:" + t("CountryCd") if t("CountryCd") else "")
    e = ein9(t("RecipientEIN")) if t("RecipientEIN") else ""
    return [e if e.strip("0") else "", name[:90], where, t("IRCSectionDesc")[:30],
            num(t("CashGrantAmt")) or 0.0, num(t("NonCashAssistanceAmt")) or 0.0,
            t("ZIPCd")[:5] if "USAddress" in g else "", t("CityNm")[:40], t("PurposeOfGrantTxt")[:160]]


def parse(stream) -> dict:
    lines, filer = [], {}
    for _, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        if tag == "RecipientTable":
            lines.append(line_of(el))
            el.clear()
        elif tag == "Filer" and not filer:
            g = {local(c.tag): (c.text or "").strip() for c in el.iter() if c.text}
            filer = {"ein": ein9(g.get("EIN", "")), "state": g.get("StateAbbreviationCd", ""), "zip5": g.get("ZIPCd", "")[:5]}
        elif tag.startswith("IRS990") and tag != "IRS990ScheduleI":
            el.clear()
    return {"lines": lines, "filer": filer}


def check(r: Mapping, x: Mapping) -> str:
    n, tot = len(r["lines"]), sum(l[4] + l[5] for l in r["lines"])
    want_n, want_t = x.get("sched_i_lines") or 0, x.get("sched_i_total") or 0.0
    if n != want_n:
        return f"count_mismatch:{n}!={want_n}"
    return "ok" if abs(tot - want_t) <= max(1.0, 0.005 * abs(want_t)) else f"total_mismatch:{tot:.0f}!={want_t:.0f}"


def save(path: str, obj: dict) -> dict:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh)
    return obj


def load_return(x: Mapping, cache: str, local_paths: Mapping, fetch: bool) -> dict:
    oid = x["oid"]
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == LINES_V:
            return c

    def try_local(acc, p):
        if acc:
            return acc
        try:
            with open(p, "rb") as fh:
                r = parse(fh)
        except (ET.ParseError, OSError):
            return None
        return {**r, "status": check(r, x), "via": "local", "path": p} if check(r, x) == "ok" else None
    hit = reduce(try_local, local_paths.get(oid, ()), None)
    if hit:
        return save(path, {**hit, "_v": LINES_V})
    if not fetch:
        return {"status": "not_fetched", "lines": [], "filer": {}}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                r = parse(resp)
            return save(path, {**r, "status": check(r, x), "via": "mirror", "_v": LINES_V})
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"status": f"http_{e.code}", "lines": [], "filer": {}}
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError):
            time.sleep(3 * (attempt + 1))
    return {"status": "error", "lines": [], "filer": {}}


# ----------------------------------------------------------------------------- 2. statistics (pure)
def mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs)


def median(xs: Sequence[float]) -> float | None:
    s = sorted(xs)
    n = len(s)
    return None if not n else (s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2)


def pearson(x: Sequence[float], y: Sequence[float]) -> float:
    mx, my = mean(x), mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))


def ranks(x: Sequence[float]) -> list:
    order = sorted(range(len(x)), key=lambda i: x[i])
    out = [0.0] * len(x)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def spearman(x, y) -> float:
    return pearson(ranks(x), ranks(y))


def fisher_ci(r: float, n: int) -> tuple[float, float]:
    z, se = math.atanh(r), 1 / math.sqrt(n - 3)
    return math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)


def boot_ci(x, y, f, b: int = 2000, seed: int = 2026111902) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(x)
    idx = [[rng.randrange(n) for _ in range(n)] for _ in range(b)]
    vals = sorted(v for v in (safe(f, [x[i] for i in ii], [y[i] for i in ii]) for ii in idx) if v is not None)
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def safe(f, a, b):
    try:
        return f(a, b)
    except ZeroDivisionError:
        return None


def inv(m: Sequence[Sequence[float]]) -> list:
    n = len(m)
    a = [list(r) + [1.0 if i == j else 0.0 for j in range(n)] for i, r in enumerate(m)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        pv = a[c][c]
        a[c] = [v / pv for v in a[c]]
        for r in range(n):
            if r != c:
                f = a[r][c]
                a[r] = [v - f * w for v, w in zip(a[r], a[c])]
    return [r[n:] for r in a]


def ols(y: Sequence[float], xs: Sequence[Sequence[float]], names: Sequence[str]) -> dict:
    """y on [1, xs...]; classical and HC1 standard errors; normal 95% intervals."""
    X = [[1.0] + list(r) for r in zip(*xs)]
    n, k = len(X), len(X[0])
    xtx = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    xi = inv(xtx)
    xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)]
    beta = [sum(xi[a][b] * xty[b] for b in range(k)) for a in range(k)]
    e = [y[i] - sum(beta[a] * X[i][a] for a in range(k)) for i in range(n)]
    s2 = sum(v * v for v in e) / (n - k)
    meat = [[sum(X[i][a] * X[i][b] * e[i] ** 2 for i in range(n)) for b in range(k)] for a in range(k)]
    hc = [[sum(xi[a][c] * meat[c][d] * xi[d][b] for c in range(k) for d in range(k)) * n / (n - k)
           for b in range(k)] for a in range(k)]
    my = mean(y)
    r2 = 1 - sum(v * v for v in e) / sum((v - my) ** 2 for v in y)
    return {"n": n, "r2": round(r2, 4), "coef": {nm: {"b": round(beta[a], 4), "se": round(math.sqrt(s2 * xi[a][a]), 4),
                                                       "se_hc1": round(math.sqrt(hc[a][a]), 4),
                                                       "ci95_hc1": (round(beta[a] - 1.96 * math.sqrt(hc[a][a]), 4),
                                                                    round(beta[a] + 1.96 * math.sqrt(hc[a][a]), 4))}
                                             for a, nm in enumerate(("const",) + tuple(names))}}


def assoc(rows: Sequence[Mapping], ycol: str, xcol: str = "daf_share_of_grants") -> dict:
    rs = [r for r in rows if r[ycol] is not None and r[xcol] is not None]
    x, y = [r[xcol] for r in rs], [r[ycol] for r in rs]
    if len(rs) < 8:
        return {"n": len(rs)}
    r = pearson(x, y)
    rho = spearman(x, y)
    la = [math.log10(r_["fy2024_daf_assets_usd"]) for r_ in rs]
    lu = [math.log10(max(r_["us_located_usd"], 1.0)) for r_ in rs]
    return {"n": len(rs), "pearson_r": round(r, 4), "pearson_ci95_fisher": tuple(round(v, 4) for v in fisher_ci(r, len(rs))),
            "pearson_ci95_boot": tuple(round(v, 4) for v in boot_ci(x, y, pearson)),
            "spearman_rho": round(rho, 4), "spearman_ci95_boot": tuple(round(v, 4) for v in boot_ci(x, y, spearman)),
            "ols_bivariate": ols(y, [x], ["daf_share"]),
            "ols_size_controls": ols(y, [x, la, lu], ["daf_share", "log10_daf_assets", "log10_us_sched_i_usd"])}


# ----------------------------------------------------------------------------- 3. per-CF rows
def share(a: float, b: float):
    return a / b if b else None


def cf_row(cf: Mapping, rs: Sequence[Mapping], home: Mapping, zc_of, z2c: Mapping, cb: Mapping, d2d: float,
           dafsh: Mapping, fys: Sequence[int], status: Mapping, in_top50: Mapping) -> dict:
    st, hz = home["state"], home["zip5"]
    hc, hcounty = zc_of(hz), z2c.get(hz, "")
    dom = [r for r in rs if r["state"] in US_CODES]
    tot_dom = sum(r["amount"] for r in dom)
    own = sum(r["amount"] for r in dom if r["state"] == st)
    cbk = [r for r in dom if r["cbsa"]]
    tot_cb = sum(r["amount"] for r in cbk)
    own_cb = sum(r["amount"] for r in cbk if r["cbsa"] == hc) if hc else 0.0
    cok = [r for r in dom if r["zip5"] in z2c]
    tot_co = sum(r["amount"] for r in cok)
    own_co = sum(r["amount"] for r in cok if z2c[r["zip5"]] == hcounty) if hcounty else 0.0
    by_st = reduce(lambda acc, r: {**acc, r["state"]: acc.get(r["state"], 0.0) + r["amount"]}, dom, {})
    out_st = sorted(((k, v) for k, v in by_st.items() if k != st), key=lambda kv: -kv[1])
    pull = sum(by_st.get(s, 0.0) for s in ("DC", "NY", "MA", "CA") if s != st)

    def flagged(rx):
        f = [r for r in dom if rx.search((r["purpose"] or "").upper())]
        return f, sum(r["amount"] for r in f)
    fd, fd_usd = flagged(DAF_RX)
    fn, fn_usd = flagged(DISC_RX)
    split_ok = bool(tot_dom) and SPLIT_MIN <= fd_usd / tot_dom <= SPLIT_MAX
    rest = [r for r in dom if not DAF_RX.search((r["purpose"] or "").upper())]
    rest_usd = sum(r["amount"] for r in rest)
    by_fy = {fy: [r for r in dom if r["_fy"] == fy] for fy in fys}
    dg = sum(dafsh.get((cf["ein"], fy), (None, None))[0] or 0.0 for fy in fys)
    gg = sum(dafsh.get((cf["ein"], fy), (None, None))[1] or 0.0 for fy in fys)
    have_d = all(dafsh.get((cf["ein"], fy), (None, None))[0] is not None for fy in fys)
    neg_d = any((dafsh.get((cf["ein"], fy), (None, None))[0] or 0.0) < 0 for fy in fys)
    return {
        "cf_rank_fy2024": int(cf["rank"]), "sponsor_ein": cf["ein"], "sponsor_name": cf["name"],
        "fy2024_daf_assets_usd": float(cf["fy2024_daf_assets_usd"]), "in_top50_geo_study": int(in_top50.get(cf["ein"], 0)),
        "sponsor_state": st, "sponsor_home_source": home["src"], "sponsor_county_fips": hcounty, "sponsor_cbsa": hc,
        "sponsor_cbsa_name": cb.get(hc, {}).get("name", ""), "fiscal_years": ";".join(map(str, fys)),
        "return_status": ";".join(f"FY{k}:{v}" for k, v in sorted(status.items())),
        "lines_net": len(rs), "net_usd": round(sum(r["amount"] for r in rs)), "d2d_excluded_usd": round(d2d),
        "us_located_usd": round(tot_dom),
        "own_state_usd": round(own), "own_state_share": share(own, tot_dom),
        "own_state_share_fy2023": share(sum(r["amount"] for r in by_fy.get(2023, []) if r["state"] == st),
                                        sum(r["amount"] for r in by_fy.get(2023, []))) if 2023 in by_fy else None,
        "own_state_share_fy2024": share(sum(r["amount"] for r in by_fy.get(2024, []) if r["state"] == st),
                                        sum(r["amount"] for r in by_fy.get(2024, []))) if 2024 in by_fy else None,
        "cbsa_resolved_usd": round(tot_cb), "own_cbsa_usd": round(own_cb),
        "own_cbsa_share_of_resolved": share(own_cb, tot_cb) if hc else None,
        "county_resolved_usd": round(tot_co), "own_county_usd": round(own_co),
        "own_county_share_of_resolved": share(own_co, tot_co) if hcounty else None,
        "states_reached": len(by_st), "top_other_state": out_st[0][0] if out_st else "",
        "dc_ny_ma_ca_out_of_state_share": share(pull, tot_dom),
        "daf_grants_sched_d_usd": round(dg) if have_d else "", "total_grants_part_ix_usd": round(gg) if have_d else "",
        "daf_share_of_grants": min(1.0, dg / gg) if have_d and gg and not neg_d else None,
        "daf_share_flag": "negative_sched_d_daf_grants" if neg_d else ("capped_at_1" if have_d and gg and dg > gg else
                                                                       ("" if have_d and gg else "missing")),
        "purpose_daf_flag_usd": round(fd_usd), "purpose_disc_flag_usd": round(fn_usd),
        "purpose_flag_coverage": share(fd_usd + fn_usd, tot_dom),
        "own_state_share_daf_flagged": share(sum(r["amount"] for r in fd if r["state"] == st), fd_usd) if split_ok else None,
        "own_state_share_not_daf_flagged": share(sum(r["amount"] for r in rest if r["state"] == st), rest_usd) if split_ok else None,
        "own_cbsa_share_daf_flagged": share(sum(r["amount"] for r in fd if r["cbsa"] == hc), sum(r["amount"] for r in fd if r["cbsa"]))
        if split_ok and hc else None,
        "own_cbsa_share_not_daf_flagged": share(sum(r["amount"] for r in rest if r["cbsa"] == hc), sum(r["amount"] for r in rest if r["cbsa"]))
        if split_ok and hc else None,
        "source": SOURCE}


FIELDS = ("cf_rank_fy2024", "sponsor_ein", "sponsor_name", "fy2024_daf_assets_usd", "in_top50_geo_study",
          "sponsor_state", "sponsor_home_source", "sponsor_county_fips", "sponsor_cbsa", "sponsor_cbsa_name",
          "fiscal_years", "return_status", "lines_net", "net_usd", "d2d_excluded_usd", "us_located_usd",
          "own_state_usd", "own_state_share", "own_state_share_fy2023", "own_state_share_fy2024",
          "cbsa_resolved_usd", "own_cbsa_usd", "own_cbsa_share_of_resolved", "county_resolved_usd", "own_county_usd",
          "own_county_share_of_resolved", "states_reached", "top_other_state", "dc_ny_ma_ca_out_of_state_share",
          "daf_grants_sched_d_usd", "total_grants_part_ix_usd", "daf_share_of_grants", "daf_share_flag",
          "purpose_daf_flag_usd", "purpose_disc_flag_usd", "purpose_flag_coverage", "own_state_share_daf_flagged",
          "own_state_share_not_daf_flagged", "own_cbsa_share_daf_flagged", "own_cbsa_share_not_daf_flagged", "source")


def r4(x):
    return round(x, 4) if isinstance(x, float) else x


def describe(rows: Sequence[Mapping], col: str) -> dict:
    v = [r[col] for r in rows if r[col] is not None]
    return {"n": len(v), "median": r4(median(v)), "mean": r4(mean(v)) if v else None,
            "min": r4(min(v)) if v else None, "max": r4(max(v)) if v else None}


def pooled(rows, num_c, den_c):
    d = sum(r[den_c] for r in rows if r[num_c] is not None)
    return r4(sum(r[num_c] for r in rows if r[num_c] is not None) / d) if d else None


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--census-dir", required=True)
    ap.add_argument("--line-cache", required=True)
    ap.add_argument("--xml-list", default="")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--summary", default="")
    a = ap.parse_args(argv)
    data = os.path.join(os.path.abspath(a.root), "data", "mission-2026-11-14")
    out_csv = os.path.join(data, "cf-local-share-top100-2026-11-19.csv")

    cfs = tuple({**r, "ein": ein9(r["ein"])} for r in read_csv(os.path.join(data, "cf-daf-fee-census-2026.csv"))
                if r["rank"].isdigit())
    panel = panel_from(read_csv(DAFRC_CSV))
    prior = {ein9(r["sponsor_ein"]): r for r in read_csv(os.path.join(data, "daf-grant-geography-cf-local-share.csv"))
             if r["segment"] == "community_foundation"}
    chosen = pick_returns(load_np(a.np_cache))
    want = {(c["ein"], fy): chosen[(c["ein"], fy)] for c in cfs for fy in FYS if (c["ein"], fy) in chosen}
    item = {k: x for k, x in want.items() if itemized(x)}
    not_item = sorted(f"{panel.get(k[0], {}).get('name', k[0])} FY{k[1]}" for k in want if k not in item)
    missing = sorted(f"{c['name']} FY{fy}" for c in cfs for fy in FYS if (c["ein"], fy) not in chosen)

    local_paths = {}
    if a.xml_list:
        with open(a.xml_list, encoding="utf-8") as fh:
            ps = [l.strip() for l in fh if l.strip()]
        local_paths = _group_by_fast(ps, lambda p: os.path.basename(p).replace("_public.xml", "").replace(".xml", ""))
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        keys = sorted(item)
        got = dict(zip(keys, ex.map(lambda k: load_return(item[k], a.line_cache, local_paths, a.fetch), keys)))
    good = {k: v for k, v in got.items() if v["status"] == "ok"}
    bad = {f"{panel.get(k[0], {}).get('name', k[0])} FY{k[1]}": v["status"] for k, v in got.items() if v["status"] != "ok"}

    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    names = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in names.items() if k and len(v) == 1}
    eins = frozenset(l[0] for v in good.values() for l in v["lines"] if l[0]) | frozenset(c["ein"] for c in cfs)
    bmf, _, _ = scan_bmf(a.bmf_dir, eins)

    cb, county_cbsa = cbsa_tables(os.path.join(a.census_dir, "cbsa-est2024-alldata.csv"))
    z2c = zcta_county(os.path.join(a.census_dir, "tab20_zcta520_county20_natl.txt"))
    zip_cbsa = {z: county_cbsa[c] for z, c in z2c.items() if c in county_cbsa}
    zctas = frozenset(z2c)
    z3 = zip3_fallback(zip_cbsa, zctas)
    zc_of = lambda z: cbsa_of(z, zip_cbsa, zctas, z3)[0]  # noqa: E731

    def ann(k, v):
        rows = annotate(k[0], [l[:6] for l in v["lines"]], bmf, wl_eins, wl_names)
        return tuple({**geo_line(r, [l[6], l[7]], bmf, zip_cbsa, zctas, z3), "_fy": k[1], "purpose": l[8]}
                     for r, l in zip(rows, v["lines"]))
    annotated = {k: ann(k, v) for k, v in good.items()}

    cost = read_csv(os.path.join(data, "sponsor-cost-structure.csv"))
    dafsh = {(ein9(r["ein"]), int(r["fiscal_year"])): (num(r["daf_grants"]), num(r["grants_part_ix_l1_3"])) for r in cost}

    def home_of(c):
        b = bmf.get(c["ein"])
        if b and b.get("bmf_state"):
            return {"state": b["bmf_state"], "zip5": b["bmf_zip"], "src": "bmf"}
        f = next((v["filer"] for k, v in sorted(good.items(), key=lambda kv: -kv[0][1]) if k[0] == c["ein"]), {})
        return {"state": f.get("state", ""), "zip5": f.get("zip5", ""), "src": "filer_header"}

    def row(c):
        ks = sorted(k for k in annotated if k[0] == c["ein"])
        if not ks:
            return None
        rs = tuple(r for k in ks for r in annotated[k])
        net = tuple(r for r in rs if not r["d2d"])
        st = {k[1]: f'{got[k]["status"]}:{item[k]["oid"]}' for k in got if k[0] == c["ein"]}
        return cf_row(c, net, home_of(c), zc_of, z2c, cb, sum(r["amount"] for r in rs if r["d2d"]), dafsh,
                      [k[1] for k in ks], st, {e: 1 for e in prior})
    rows = tuple(r for r in map(row, cfs) if r is not None)
    write_csv(out_csv, [{k: r4(v) for k, v in r.items()} for r in rows], FIELDS)

    # ------------------------------------------------------------- checks and summary
    repro = [(p["sponsor_name"][:30], r4(float(p["own_state_share"])), r4(r["own_state_share"]),
              r4(float(p["own_cbsa_share_of_resolved"])) if p["own_cbsa_share_of_resolved"] else None,
              r4(r["own_cbsa_share_of_resolved"]))
             for r in rows for e, p in prior.items() if e == r["sponsor_ein"]]
    max_diff = max((abs(x[1] - x[2]) for x in repro if x[2] is not None), default=None)
    svcf = "205205488"
    sub = {"all": rows, "ex_svcf": [r for r in rows if r["sponsor_ein"] != svcf],
           "not_in_geo01": [r for r in rows if not r["in_top50_geo_study"]],
           "top50_cfs": [r for r in rows if r["in_top50_geo_study"]],
           "ranks_1_50": [r for r in rows if r["cf_rank_fy2024"] <= 50],
           "ranks_51_100": [r for r in rows if r["cf_rank_fy2024"] > 50],
           "ex_multistate_cbsa": [r for r in rows if "-" not in r["sponsor_cbsa_name"].rsplit(",", 1)[-1]]}
    terc = sorted((r for r in rows if r["daf_share_of_grants"] is not None), key=lambda r: r["daf_share_of_grants"])
    t = len(terc)
    tert = {f"T{i + 1}": terc[i * t // 3:(i + 1) * t // 3] for i in range(3)}
    split_rows = [r for r in rows if r["own_state_share_daf_flagged"] is not None]
    summary = {
        "universe_cfs": len(cfs), "sponsor_years_found": len(want), "missing_sponsor_years": missing,
        "not_itemised": not_item, "returns_itemised": len(item), "returns_ok": len(good), "return_problems": bad,
        "via": {s: sum(1 for v in good.values() if v.get("via") == s) for s in ("local", "mirror")},
        "cfs_with_rows": len(rows), "lines_total": sum(r["lines_net"] for r in rows),
        "net_usd_total": sum(r["net_usd"] for r in rows), "d2d_excluded_total": sum(r["d2d_excluded_usd"] for r in rows),
        "home_from_filer": [r["sponsor_name"] for r in rows if r["sponsor_home_source"] != "bmf"],
        "no_home_cbsa": [r["sponsor_name"] for r in rows if not r["sponsor_cbsa"]],
        "reproduction_vs_geo01": {"n": len(repro), "max_abs_diff_own_state": r4(max_diff), "rows": repro},
        "describe": {k: {c: describe(v, c) for c in ("own_state_share", "own_cbsa_share_of_resolved",
                                                     "own_county_share_of_resolved", "daf_share_of_grants")}
                     | {"pooled_own_state": pooled(v, "own_state_usd", "us_located_usd"),
                        "pooled_own_cbsa": pooled(v, "own_cbsa_usd", "cbsa_resolved_usd")}
                     for k, v in sub.items()},
        "tertiles_by_daf_share": {k: {"n": len(v), "daf_share_range": (r4(v[0]["daf_share_of_grants"]), r4(v[-1]["daf_share_of_grants"])),
                                      "median_own_state": r4(median([r["own_state_share"] for r in v if r["own_state_share"] is not None])),
                                      "median_own_cbsa": r4(median([r["own_cbsa_share_of_resolved"] for r in v if r["own_cbsa_share_of_resolved"] is not None])),
                                      "median_daf_assets": median([r["fy2024_daf_assets_usd"] for r in v])}
                                  for k, v in tert.items() if v},
        "assoc": {k: {y: assoc(v, y) for y in ("own_state_share", "own_cbsa_share_of_resolved", "own_county_share_of_resolved")}
                  for k, v in sub.items() if k in ("all", "ex_svcf", "not_in_geo01", "ex_multistate_cbsa")},
        "multistate_cbsa_cfs": [(r["sponsor_name"][:34], r["sponsor_cbsa_name"]) for r in rows
                                if "-" in r["sponsor_cbsa_name"].rsplit(",", 1)[-1]],
        "purpose_split": {"cfs_with_any_daf_flag": sum(1 for r in rows if r["purpose_daf_flag_usd"]),
                          "cfs_with_any_disc_flag": sum(1 for r in rows if r["purpose_disc_flag_usd"]),
                          "daf_flag_usd_total": sum(r["purpose_daf_flag_usd"] for r in rows),
                          "disc_flag_usd_total": sum(r["purpose_disc_flag_usd"] for r in rows),
                          "us_usd_total": sum(r["us_located_usd"] for r in rows),
                          "cfs_split_ok": [(r["sponsor_name"][:30], r["purpose_daf_flag_usd"], r["us_located_usd"],
                                            r4(r["own_state_share_daf_flagged"]), r4(r["own_state_share_not_daf_flagged"]),
                                            r4(r["own_cbsa_share_daf_flagged"]), r4(r["own_cbsa_share_not_daf_flagged"]))
                                           for r in split_rows],
                          "daf_share_flags": [(r["sponsor_name"][:34], r["daf_share_flag"]) for r in rows if r["daf_share_flag"]],
                          "top_flag_coverage": sorted(((r["sponsor_name"][:30], r4(r["purpose_flag_coverage"]), r["purpose_daf_flag_usd"],
                                                        r["purpose_disc_flag_usd"]) for r in rows if r["purpose_flag_coverage"]),
                                                      key=lambda t_: -t_[1])[:12]},
        "lowest_own_state": [(r["cf_rank_fy2024"], r["sponsor_name"][:34], r["sponsor_state"], r4(r["own_state_share"]),
                              r4(r["own_cbsa_share_of_resolved"]), r4(r["daf_share_of_grants"]), r["top_other_state"])
                             for r in sorted(rows, key=lambda r: r["own_state_share"] if r["own_state_share"] is not None else 9)[:12]],
        "highest_own_state": [(r["cf_rank_fy2024"], r["sponsor_name"][:34], r["sponsor_state"], r4(r["own_state_share"]),
                               r4(r["own_cbsa_share_of_resolved"]), r4(r["daf_share_of_grants"]))
                              for r in sorted(rows, key=lambda r: -(r["own_state_share"] or 0))[:8]],
        "daf_share_extremes": [(r["cf_rank_fy2024"], r["sponsor_name"][:34], r4(r["daf_share_of_grants"]), r4(r["own_state_share"]))
                               for r in terc[:5] + terc[-5:]],
    }
    txt = json.dumps(summary, indent=1, default=str)
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as fh:
            fh.write(txt)
    print(txt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
