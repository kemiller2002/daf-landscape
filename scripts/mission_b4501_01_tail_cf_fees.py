#!/usr/bin/env python3
"""P-B4501-01: enlarge the tail community-foundation (CF) fee sample. Task id b4501-01.

Wrapper around scripts/mission_long_tail_fee_census.py (task b45n33-01), which is imported and NOT modified. Reused from
it unchanged: the frame (tail_frame), the strata (strata), the allocation rule (allocate), the robots-checked crawler
(crawl_site / raw_get / fetch_one, user agent "research-script/1.0"), the fee engine (effective_admin_fee, bps), the
quote verifier (verify), Wilson intervals and the original 60-row draw (draw), whose 31 CFs are excluded here.

Sampling (same seed scheme, CF strata only)
  Frame: the 641 tail CFs (base tail_frame, type4 == cf), strata cf x {t10_50, t1_10, t0_1, zero} at the SAME stratum
  index as the base (0..3). The original draw's 31 CFs are removed. n = 60 is allocated over the four remaining strata
  with the base allocate() (proportional, floor 1, largest remainder). Within stratum i:
  random.Random(SEED_EXT + i).sample(remaining rows sorted by EIN, a_i), SEED_EXT = 20261120 (base: 20261119 + i).
  Homepages: cf-vendor-map-by-ein-v2.csv `homepage` (from the 990 WebsiteAddressTxt), as in the base census.

Tasks
  sample   print the extension draw (stratum, N, n, EIN, name, homepage)
  crawl    base.crawl_site for every drawn CF with a homepage (robots.txt read and logged before any page); --fetch
           required to touch the network; cache in --cache-dir (outside the repo). Writes crawl_summary_ext.json there.
  fetch    base.fetch_one for every verify URL in FEES_EXT (robots-checked) -- needs --fetch.
  hits     print the fee sentences and candidate URLs found per sponsor from the cache (for transcription).
  robots   print the robots.txt verdict logged for every host touched (from the cache; never fetches).
  census   verify quotes, compute fees, write data/mission-2026-11-14/tail-cf-fee-sample-2026-11-20.csv and print every
           table used in research/mission-2026-11-14/b4501-01-tail-cf-fee-sample.md (medians with seeded bootstrap).

Usage (cache outside the repo):
  python3 -I scripts/mission_b4501_01_tail_cf_fees.py . --task sample
  python3 -I scripts/mission_b4501_01_tail_cf_fees.py . --task crawl --cache-dir CACHE --fetch
  python3 -I scripts/mission_b4501_01_tail_cf_fees.py . --task fetch --cache-dir CACHE --fetch
  python3 -I scripts/mission_b4501_01_tail_cf_fees.py . --task census --cache-dir CACHE
"""
from __future__ import annotations

import argparse
import concurrent.futures
import glob
import importlib.util
import json
import os
import random
import re
import statistics
import sys
import urllib.parse
from typing import Mapping, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))


def load_base():
    spec = importlib.util.spec_from_file_location("lt_fee_census", os.path.join(HERE, "mission_long_tail_fee_census.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = load_base()
DATA = B.DATA
VMAP_CSV = f"{DATA}/cf-vendor-map-by-ein-v2.csv"
REALISED_CSV = f"{DATA}/tail-realised-fees-all-2026-11-20.csv"
OUT_CSV = f"{DATA}/tail-cf-fee-sample-2026-11-20.csv"
SEED_EXT = 20261120
N_EXT = 60
N_BOOT = 10_000
BOOT_SEED = 4501
RETRIEVED = "2026-11-20"

# ----------------------------------------------------------------------------- transcription (filled after research)
# Same structure as base FEES. status: published_schedule | published_no_admin_fee | published_pre2021 |
# published_unread | partial | no_published_fee | no_website_found | robots_blocked | site_unreachable
_NPF = "no_published_fee"
FEES_EXT: dict[str, dict] = {}


# ----------------------------------------------------------------------------- sampling
def cf_strata(frame: Sequence[Mapping]):
    """(stratum index in the base 16-cell list, key, rows sorted by EIN) for the four CF strata."""
    return tuple((i, k, rows) for i, (k, rows) in enumerate(B.strata(frame)) if k[0] == "cf")


def draw_ext(frame: Sequence[Mapping], exclude: frozenset, n: int = N_EXT, seed: int = SEED_EXT) -> tuple[dict, ...]:
    st = tuple((i, k, rows, tuple(r for r in rows if r["ein"] not in exclude)) for i, k, rows in cf_strata(frame))
    alloc = B.allocate(tuple(len(rem) for *_, rem in st), n)
    return tuple(
        {**r, "stratum": f"{k[0]}|{k[1]}", "stratum_N": len(rows), "stratum_N_remaining": len(rem), "stratum_n": a,
         "stratum_n_orig": len(rows) - len(rem), "weight": len(rows) / a, "weight_pooled": len(rows) / (a + len(rows) - len(rem))}
        for (i, k, rows, rem), a in zip(st, alloc)
        for r in random.Random(seed + i).sample(rem, a)
    )


def homepages(vmap_rows: Sequence[Mapping]) -> dict:
    return {r["ein"]: r["homepage"].strip() for r in vmap_rows if r.get("homepage", "").strip()}


def original_sample(frame):
    return B.draw(frame)


# ----------------------------------------------------------------------------- statistics
def median(xs: Sequence[float]) -> float | None:
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def boot_median(xs: Sequence[float], n_boot: int = N_BOOT, seed: int = BOOT_SEED, alpha: float = 0.05):
    """Percentile bootstrap of the median: (median, lo, hi)."""
    xs = [x for x in xs if x is not None]
    if len(xs) < 2:
        return (xs[0], xs[0], xs[0]) if xs else None
    rng = random.Random(seed)
    meds = sorted(statistics.median(rng.choices(xs, k=len(xs))) for _ in range(n_boot))
    return statistics.median(xs), meds[int(alpha / 2 * n_boot)], meds[int((1 - alpha / 2) * n_boot) - 1]


def boot_share(flags: Sequence[bool], n_boot: int = N_BOOT, seed: int = BOOT_SEED, alpha: float = 0.05):
    flags = list(flags)
    if not flags:
        return None
    rng = random.Random(seed)
    sh = sorted(sum(rng.choices(flags, k=len(flags))) / len(flags) for _ in range(n_boot))
    return sum(flags) / len(flags), sh[int(alpha / 2 * n_boot)], sh[int((1 - alpha / 2) * n_boot) - 1]


def weighted_median(pairs: Sequence[tuple[float, float]]) -> float | None:
    """Lower weighted median of (value, weight) pairs."""
    ps = sorted((v, w) for v, w in pairs if v is not None)
    if not ps:
        return None
    half = sum(w for _, w in ps) / 2
    cum = [sum(w for _, w in ps[:j + 1]) for j in range(len(ps))]
    return next(v for (v, _), c in zip(ps, cum) if c >= half)


def bfmt(t, nd: int = 0) -> str:
    return "–" if t is None else f"{t[0]:,.{nd}f} ({t[1]:,.{nd}f}–{t[2]:,.{nd}f})"


def sfmt(k: int, n: int, flags=None) -> str:
    w = B.wilson(k, n)
    if w is None:
        return "–"
    b = boot_share(flags) if flags is not None else None
    return (f"{k}/{n} = {w[0]*100:.1f}% (Wilson {w[1]*100:.1f}–{w[2]*100:.1f}%"
            + (f"; bootstrap {b[1]*100:.1f}–{b[2]*100:.1f}%)" if b else ")"))


# ----------------------------------------------------------------------------- census rows
def host_of(url: str) -> str:
    return urllib.parse.urlsplit(url).netloc.lower()


def cached_raw(cache: str | None, url: str) -> dict | None:
    if not cache or not url:
        return None
    path = os.path.join(cache, "raw_" + B.cache_key(url) + ".json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def home_log(cache: str | None, home: str) -> str:
    rec = cached_raw(cache, home)
    return "" if rec is None else f"homepage {home}: {rec['robots']}; HTTP {rec['status']}"


def ext_row(r: Mapping, home: str, realised: Mapping, cache: str | None) -> dict:
    s = FEES_EXT.get(r["ein"], {"status": "not_researched"})
    rate = s["status"] in B.RATE_STATUSES
    fees = {b: B.effective_admin_fee(s, b) for b in B.BALANCES} if rate else {}
    rec = B.cached(cache, s["source_url"]) if cache and s.get("source_url") else None
    avg = B.num(r["avg_account_fy2024"])
    fee_avg = B.fee_at_balance(s, avg) if rate else None
    return {
        "ein": r["ein"], "name": r["name"], "sample": "ext_b4501_01", "stratum": r["stratum"],
        "size_band_fy2024": r["size_band_fy2024"], "stratum_N": r["stratum_N"], "stratum_n_orig": r["stratum_n_orig"],
        "stratum_n_ext": r["stratum_n"], "weight_ext": B.fmt(r["weight"], 3), "weight_pooled": B.fmt(r["weight_pooled"], 3),
        "daf_assets_fy2024": r["daf_assets_fy2024"], "accounts_fy2024_screened": r["accounts_fy2024_screened"],
        "avg_account_fy2024": r["avg_account_fy2024"], "website": s.get("website") or home,
        "fee_status": s["status"], "in_2021plus_distribution": "yes" if s["status"] in B.RATE_2021 else "no",
        "fee_basis": s.get("basis", "") if s.get("tiers") else "",
        "admin_tiers": "; ".join(f"{lo:,.0f}-{'' if up is None else f'{up:,.0f}'}: {rt}%" for lo, up, rt in s.get("tiers") or ()),
        "min_annual_fee_usd": B.fmt(s.get("min_fee")), "flat_annual_fee_usd": B.fmt(s.get("flat_fee")),
        "opening_min_usd": B.fmt(s.get("opening_min")), "gift_fee": s.get("gift_fee", ""), "grant_fee": s.get("grant_fee", ""),
        "investment": s.get("investment", ""),
        **{f"admin_bps_{b // 1000}k": B.fmt(B.bps(fees.get(b), b)) for b in B.BALANCES},
        "fee_bps_at_avg_account": B.fmt(B.bps(fee_avg, avg) if fee_avg is not None else None),
        "realised_capture": realised.get("capture", ""), "realised_internal_bps_ta": realised.get("internal_bps_ta", ""),
        "realised_visible_bps_ta": realised.get("visible_bps_ta", ""), "realised_pool_rate_bps": realised.get("pool_rate_bps", ""),
        "source_url": s.get("source_url", ""), "source_date": s.get("source_date", ""),
        "robots": s.get("robots") or (rec or {}).get("robots") or home_log(cache, home),
        "quote_check": B.verify(cache, s) if cache and s.get("quotes") else "", "notes": s.get("notes", ""),
    }


FIELDS = ("ein", "name", "sample", "stratum", "size_band_fy2024", "stratum_N", "stratum_n_orig", "stratum_n_ext", "weight_ext",
          "weight_pooled", "daf_assets_fy2024", "accounts_fy2024_screened", "avg_account_fy2024", "website", "fee_status",
          "in_2021plus_distribution", "fee_basis", "admin_tiers", "min_annual_fee_usd", "flat_annual_fee_usd", "opening_min_usd",
          "gift_fee", "grant_fee", "investment", "admin_bps_25k", "admin_bps_100k", "admin_bps_500k", "fee_bps_at_avg_account",
          "realised_capture", "realised_internal_bps_ta", "realised_visible_bps_ta", "realised_pool_rate_bps",
          "source_url", "source_date", "robots", "quote_check", "notes")

NO_SCHEDULE = ("partial", "no_published_fee", "no_website_found")       # site (or its absence) read: no fee schedule public
UNKNOWN_EXT = ("robots_blocked", "site_unreachable")


def is_rate(r):
    return r["fee_status"] in B.RATE_2021


def known(r):
    return r["fee_status"] not in UNKNOWN_EXT


# ----------------------------------------------------------------------------- report
def report(ext: Sequence[Mapping], orig_cf: Sequence[Mapping], frame_cf: Sequence[Mapping], realised_all: Sequence[Mapping]) -> str:
    out = []
    T = B.table
    # T1 design
    by = {}
    for r in ext:
        by.setdefault(r["stratum"], []).append(r)
    out.append("## E1 Extension design\n\n" + T(
        ("Stratum", "Frame N", "Original n", "Remaining", "Extension n", "Weight (ext)", "Weight (pooled)"),
        ((k, rs[0]["stratum_N"], rs[0]["stratum_n_orig"], int(rs[0]["stratum_N"]) - int(rs[0]["stratum_n_orig"]), len(rs),
          rs[0]["weight_ext"], rs[0]["weight_pooled"]) for k, rs in sorted(by.items(), key=lambda kv: B.TAIL_BANDS.index(kv[0].split("|")[1])))))
    # E2 status
    sts = ("published_schedule", "published_no_admin_fee", "published_pre2021", "published_unread", "partial",
           "no_published_fee", "no_website_found", "robots_blocked", "site_unreachable")
    groups = (("Extension (60)", ext), ("Original CFs (31)", orig_cf), ("Pooled CFs (91)", tuple(ext) + tuple(orig_cf))) + tuple(
        (f"ext band {b}", tuple(r for r in ext if r["size_band_fy2024"] == b)) for b in B.TAIL_BANDS)
    out.append("## E2 Fee status\n\n" + T(("Group", "n") + sts,
                                         ((g, len(rs)) + tuple(sum(r["fee_status"] == s for r in rs) for s in sts) for g, rs in groups)))
    # E3 rates
    def rate_rows():
        for g, rs in groups:
            kn = [r for r in rs if known(r)]
            yield (g, sfmt(sum(map(is_rate, rs)), len(rs), [is_rate(r) for r in rs]),
                   sfmt(sum(map(is_rate, kn)), len(kn), [is_rate(r) for r in kn]),
                   sfmt(sum(r["fee_status"] in B.ANY_TERM for r in rs), len(rs), [r["fee_status"] in B.ANY_TERM for r in rs]),
                   sfmt(sum(r["fee_status"] in NO_SCHEDULE for r in kn), len(kn), [r["fee_status"] in NO_SCHEDULE for r in kn]),
                   sfmt(sum(r["fee_status"] in NO_SCHEDULE + UNKNOWN_EXT for r in rs), len(rs),
                        [r["fee_status"] in NO_SCHEDULE + UNKNOWN_EXT for r in rs]))
    out.append("## E3 Found-schedule rate and no-public-schedule share\n\n" + T(
        ("Group", "2021+ rate found (all)", "2021+ rate found (readable sites)", "Any fee term or linked schedule",
         "No public fee schedule (readable sites)", "No public fee schedule incl. unreadable"), rate_rows()))
    pooled = tuple(ext) + tuple(orig_cf)
    w_ext = sum(float(r["weight_pooled"]) * is_rate(r) for r in pooled) / sum(float(r["weight_pooled"]) for r in pooled)
    out.append(f"Design-weighted 2021+ rate, pooled 91 CFs (weights N/(n_orig+n_ext)): {w_ext*100:.1f}%")
    # E4 medians
    def bpsv(r, b):
        return B.num(r[f"admin_bps_{b // 1000}k"])
    sets = (("Extension only", [r for r in ext if is_rate(r)]), ("Original 6", [r for r in orig_cf if is_rate(r)]),
            ("Pooled", [r for r in pooled if is_rate(r)]),
            ("Pooled, excl. 0% schedules", [r for r in pooled if is_rate(r) and (bpsv(r, 100_000) or 0) > 0]))
    out.append("## E4 Effective annual admin fee, bps: median (95% percentile bootstrap, 10,000 draws, seed 4501)\n\n" + T(
        ("Set", "n", "$25k", "$100k", "$500k", "IQR $100k", "Design-weighted median $25k / $100k / $500k"),
        ((g, len(rs)) + tuple(bfmt(boot_median([bpsv(r, b) for r in rs])) for b in B.BALANCES)
         + (B.qfmt([bpsv(r, 100_000) for r in rs]),
            " / ".join(B.fmt(weighted_median([(bpsv(r, b), float(r.get("weight_pooled") or r.get("weight") or 1)) for r in rs]), 0)
                       for b in B.BALANCES)) for g, rs in sets)))
    # E5 schedules
    out.append("## E5 Extension CFs publishing any fee term\n\n" + T(
        ("EIN", "Sponsor", "Band", "Status", "Tiers", "Min fee $", "Opening min $", "$25k", "$100k", "$500k", "Realised internal bps", "Source date", "Quotes"),
        ((r["ein"], r["name"][:40], r["size_band_fy2024"], r["fee_status"], r["admin_tiers"] or "–", r["min_annual_fee_usd"] or "–",
          r["opening_min_usd"] or "–", r["admin_bps_25k"] or "–", r["admin_bps_100k"] or "–", r["admin_bps_500k"] or "–",
          r["realised_internal_bps_ta"] or "–", r["source_date"], r["quote_check"] or "–")
         for r in ext if r["fee_status"] in B.ANY_TERM)))
    # E6 opening minimums
    om = lambda rs: [B.num(r["opening_min_usd"]) for r in rs if r["opening_min_usd"] != ""]  # noqa: E731
    out.append("## E6 Opening minimum (where stated): median (bootstrap 95%)\n\n" + T(
        ("Set", "n stating", "Median $"), ((g, len(om(rs)), bfmt(boot_median(om(rs)))) for g, rs in
                                            (("Extension", ext), ("Original CFs", orig_cf), ("Pooled", pooled)))))
    # E7 pools
    out.append(pool_section(pooled, frame_cf, realised_all, bpsv))
    return "\n\n".join(out)


def pool_section(pooled, frame_cf, realised_all, bpsv) -> str:
    """Schedule-ceiling CF pool at the pooled median schedule (each CF at its own avg account) vs the realised pool."""
    T = B.table
    rates = [r for r in pooled if is_rate(r)]
    assets = sum(B.num(r["daf_assets_fy2024"]) or 0 for r in frame_cf)
    med100 = median([bpsv(r, 100_000) for r in rates])
    bm = boot_median([bpsv(r, 100_000) for r in rates])
    real = [r for r in realised_all if r.get("part") == "B_tail_cf"]
    real_pool = sum(B.num(r["pool_central_usd"]) or 0 for r in real)
    # realised vs published, for every sampled CF with a 2021+ rate and an observed internal rate
    pairs = [(r["name"][:34], bpsv(r, 100_000), B.num(r.get("realised_internal_bps_ta", ""))) for r in rates]
    obs = [(n, p, q) for n, p, q in pairs if q is not None]
    return ("## E7 Fee pools (tail CFs, FY2024 DAF assets)\n\n" + T(
        ("Measure", "Value"),
        (("Tail CF DAF assets FY2024 (641 CFs)", f"${assets/1e6:,.1f}m"),
         ("Realised all-fund pool, b4427b-0405 (sum of pool_central_usd; unchanged by this sample)", f"${real_pool/1e6:,.1f}m"),
         ("Pooled published median at $100k, bps (bootstrap 95%)", bfmt(bm)),
         ("Flat schedule ceiling at the pooled $100k median", f"${assets*med100/1e4/1e6:,.1f}m" if med100 is not None else "–"),
         ("Flat schedule ceiling, bootstrap bounds", f"${assets*bm[1]/1e4/1e6:,.1f}m–${assets*bm[2]/1e4/1e6:,.1f}m" if bm else "–")))
        + "\n\nPublishers with an observed realised internal rate (b4427b-0405):\n\n"
        + T(("Sponsor", "Published bps at $100k", "Realised internal bps of total assets"),
            ((n, B.fmt(p, 0), B.fmt(q, 1)) for n, p, q in obs)))


# ----------------------------------------------------------------------------- tasks
def robots_log(cache: str) -> tuple[tuple[str, str, str], ...]:
    recs = []
    for p in sorted(glob.glob(os.path.join(cache, "*.json"))):
        if p.endswith("crawl_summary_ext.json"):
            continue
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
        if isinstance(d, dict) and "robots" in d and "url" in d:
            recs.append((host_of(d["url"]), d["robots"], d["url"]))
    first = {}
    for h, v, u in recs:
        first.setdefault(h, (h, v, u))
    return tuple(sorted(first.values()))


def all_urls() -> tuple[str, ...]:
    return tuple(dict.fromkeys(u for s in FEES_EXT.values() for u in (s.get("verify_urls") or (s.get("source_url"),)) if u))


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--task", choices=("sample", "crawl", "fetch", "hits", "robots", "census"), required=True)
    ap.add_argument("--cache-dir")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--ein", action="append", default=[])
    ap.add_argument("--url", action="append", default=[])
    a = ap.parse_args(argv)
    os.chdir(a.root)
    frame = B.tail_frame(B.read_csv(B.LT_CSV))
    orig = original_sample(frame)
    orig_cf_eins = frozenset(r["ein"] for r in orig if r["type4"] == "cf")
    ext = draw_ext(frame, orig_cf_eins)
    hp = homepages(B.read_csv(VMAP_CSV))
    if a.task == "sample":
        print("stratum|N|N_remaining|n_ext|ein|name|daf_assets_fy2024|homepage")
        print("\n".join(f"{r['stratum']}|{r['stratum_N']}|{r['stratum_N_remaining']}|{r['stratum_n']}|{r['ein']}|{r['name']}|"
                        f"{r['daf_assets_fy2024']}|{hp.get(r['ein'], '')}" for r in ext))
        return 0
    if a.task in ("crawl", "fetch") and not (a.fetch and a.cache_dir):
        print(f"{a.task} needs --fetch and --cache-dir", file=sys.stderr)
        return 2
    if a.task == "crawl":
        os.makedirs(a.cache_dir, exist_ok=True)
        targets = [(r["ein"], hp[r["ein"]]) for r in ext if r["ein"] in hp and (not a.ein or r["ein"] in a.ein)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            res = list(ex.map(lambda t: B.crawl_site(a.cache_dir, *t), targets))
        with open(os.path.join(a.cache_dir, "crawl_summary_ext.json"), "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("\n".join(f"{r['ein']}\t{r['home_status']}\t{r['robots']}\t{r['n_candidates']}\t{len(r['hits'])}\t{r['home']}" for r in res))
        return 0
    if a.task == "fetch":
        os.makedirs(a.cache_dir, exist_ok=True)
        recs = [B.fetch_one(a.cache_dir, u) for u in (a.url or all_urls())]
        print("\n".join(f"{r['status']}\t{r['robots']}\t{len(r['text'])}\t{r['url']}" for r in recs))
        return 0
    if a.task == "robots":
        print("host\tverdict\tfirst_url")
        print("\n".join("\t".join(t) for t in robots_log(a.cache_dir)))
        return 0
    if a.task == "hits":
        with open(os.path.join(a.cache_dir, "crawl_summary_ext.json"), encoding="utf-8") as fh:
            res = json.load(fh)
        for c in res:
            if a.ein and c["ein"] not in a.ein:
                continue
            print(f"=== {c['ein']} {c['home']} | {c['robots']} | HTTP {c['home_status']} | fetched {len(c['fetched'])}")
            print("  pages: " + " ".join(c["fetched"]))
            for u, sn in c["hits"]:
                print(f"  - [{u}] {sn}")
        return 0
    realised = {r["ein"]: r for r in B.read_csv(REALISED_CSV)}
    rows = tuple(ext_row(r, hp.get(r["ein"], ""), realised.get(r["ein"], {}), a.cache_dir) for r in ext)
    B.write_csv(OUT_CSV, rows, FIELDS)
    orig_rows = tuple(r for r in B.read_csv(B.OUT_CSV) if r["type4"] == "cf")
    orig_cf = tuple({**r, "realised_internal_bps_ta": realised.get(r["ein"], {}).get("internal_bps_ta", "")} for r in orig_rows)
    frame_cf = tuple(r for r in frame if r["type4"] == "cf")
    print(report(rows, orig_cf, frame_cf, tuple(realised.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
