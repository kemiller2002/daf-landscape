"""npt-ren-followups (P-B442802-01, P-G0702-03): capture history and Schedule F/R tests.

Usage:
  python3 -I scripts/mission_npt_ren_followups.py . wayback CACHE_DIR OUT_JSON [--fetch]
  python3 -I scripts/mission_npt_ren_followups.py . npt990 NPT_FY2025_XML [FX_RATE_FILE]

wayback: lists Wayback Machine captures of the Ren/RCF donor guides using only the
  archive.org availability API (https://archive.org/wayback/available; archive.org
  robots.txt disallows only /control/ and /report/). The CDX API and snapshot pages live on
  web.archive.org, which reset every connection from this session, so robots.txt there
  could not be read and nothing on that host is requested. The availability API returns
  the single capture closest to a timestamp; captures are enumerated by probing a monthly
  grid and bisecting every interval whose end points return different captures, down to
  a 1-day resolution. Captures inside one day of each other, or that are never the closest
  capture to any probe, can be missed. Responses are cached as JSON per probe so the run
  repeats offline (without --fetch the cache must be complete).
npt990: reads NPT's FY2025 Form 990 XML (object 202601289349302480) and prints the
  Schedule R Part V line-1 indicators (a-s, in schema order), Schedule R Part II/IV rows,
  the Schedule F Part II line distribution and the GBP->USD rates that would make
  GBP 30.939m equal each large Europe line.

Stdlib only; pure functions apart from the I/O wrappers at the edge. UA research-script/1.0.
"""
import json, os, sys, time, hashlib, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from functools import reduce

UA = "research-script/1.0"
API = "https://archive.org/wayback/available?url={url}&timestamp={ts}"
TARGETS = (
    ("S1-rcf", "rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf"),
    ("S1-ubs", "ubs.donorfirstx.com/pdf/UBS/Donor%20User%20Guide.pdf"),
    ("S4-tda-2309", "tda.donorfirstx.com/pdf/tda/RCF%20Donor%20User%20Guide.pdf"),
    ("S5-ubs-2309", "ubs.donorfirstx.com/pdf/UBS/UBS%20Donor%20User%20Guide.pdf"),
    ("S1-ampf", "ampf.donorfirstx.com/pdf/AMPF/Donor%20User%20Guide.pdf"),
    ("S1-rbcrcf", "rbcrcf.donorfirstx.com/pdf/RBC/Donor%20User%20Guide.pdf"),
    ("S1-mdrt", "mdrt.donorfirstx.com/pdf/mdrt/Donor%20User%20Guide.pdf"),
    ("S1-rcfgf", "rcfgivingfund.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf"),
    ("S1-nwm", "northwesternmutual.donorfirstx.com/pdf/NWM/Donor%20User%20Guide.pdf"),
)
GRID_START, GRID_END = (2021, 1), (2026, 11)
EPOCH_FMT = "%Y%m%d%H%M%S"


# ---------- pure helpers ----------
def month_grid(start, end):
    """Timestamps on the 1st of every month from start to end inclusive."""
    months = range(start[0] * 12 + start[1] - 1, end[0] * 12 + end[1])
    return tuple(f"{m // 12:04d}{m % 12 + 1:02d}01000000" for m in months)


def to_epoch(ts):
    return int(time.mktime(time.strptime(ts, EPOCH_FMT)))


def from_epoch(e):
    return time.strftime(EPOCH_FMT, time.localtime(e))


def midpoint(a, b):
    return from_epoch((to_epoch(a) + to_epoch(b)) // 2)


def closest_of(resp):
    snap = (resp or {}).get("archived_snapshots", {}).get("closest")
    return None if not snap else (snap["timestamp"], snap.get("status", ""), snap["url"])


def cache_name(url, ts):
    return hashlib.sha1(f"{url}|{ts}".encode()).hexdigest()[:16] + ".json"


# ---------- I/O edge ----------
def probe(cache, fetch, url, ts):
    path = os.path.join(cache, cache_name(url, ts))
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)["resp"]
    if not fetch:
        raise SystemExit(f"cache miss {url} {ts}; rerun with --fetch")
    req = urllib.request.Request(API.format(url=urllib.parse.quote(url, safe=""), ts=ts), headers={"User-Agent": UA})
    body, err = None, ""
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = json.loads(r.read().decode())
            if closest_of(body) is not None or attempt == 3:
                break  # an empty answer is retried: the API intermittently returns {} for URLs it holds
            time.sleep(2)
        except Exception as exc:  # noqa: BLE001
            time.sleep(3 * (attempt + 1))
            err = repr(exc)
    if body is None:
        raise SystemExit(f"availability API failed for {url} {ts}: {err}")
    with open(path, "w") as fh:
        json.dump({"url": url, "ts": ts, "resp": body, "retrieved": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, fh)
    time.sleep(1.0)
    return body


def bisect(look, a, b, ca, cb, depth=0):
    """Return the set of closest-captures found between probes a and b (inclusive)."""
    if ca == cb or to_epoch(b) - to_epoch(a) <= 86400 or depth > 20:
        return frozenset(x for x in (ca, cb) if x)
    m = midpoint(a, b)
    cm = closest_of(look(m))
    return bisect(look, a, m, ca, cm, depth + 1) | bisect(look, m, b, cm, cb, depth + 1)


def captures_for(cache, fetch, url):
    look = lambda ts: probe(cache, fetch, url, ts)  # noqa: E731
    grid = month_grid(GRID_START, GRID_END)
    first = closest_of(look(grid[0]))
    found = reduce(
        lambda acc, pair: (acc[0] | bisect(look, acc[1], pair[0], acc[2], pair[1]), pair[0], pair[1]),
        ((ts, closest_of(look(ts))) for ts in grid[1:]),
        (frozenset([first]), grid[0], first),
    )[0]
    return tuple(sorted(x for x in found if x))


def run_wayback(cache, out, fetch):
    os.makedirs(cache, exist_ok=True)
    rows = tuple({"target_id": tid, "url": u, "captures": [
        {"timestamp": c[0], "status": c[1], "snapshot_url": c[2]} for c in captures_for(cache, fetch, u)]}
        for tid, u in TARGETS)
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=1)
    tuple(print(r["target_id"], len(r["captures"]), ",".join(c["timestamp"] + ":" + c["status"] for c in r["captures"])) for r in rows)


# ---------- NPT FY2025 990 ----------
NS = "{http://www.irs.gov/efile}"


def local(tag):
    return tag.split("}")[-1]


def find_sched(root, name):
    return next((e for e in root.iter() if local(e.tag) == name), None)


def run_npt(xml_path, rate_file=None):
    root = ET.parse(xml_path).getroot()
    r = find_sched(root, "IRS990ScheduleR")
    f = find_sched(root, "IRS990ScheduleF")
    letters = "abcdefghijklmnopqrs"
    inds = tuple(e for e in r if local(e.tag).endswith("Ind") and local(e.tag) not in ("DisregardedEntityInd",)) if r is not None else ()
    print("Schedule R Part V line-1 indicators (schema order):")
    tuple(print(f"  1{letters[i] if i < 19 else '?'}", local(e.tag), e.text) for i, e in enumerate(inds))
    print("Schedule R Part II / IV / I rows:")
    tuple(print("  ", local(g.tag), "|", " | ".join(f"{local(c.tag)}={(c.text or '').strip()}" for c in g.iter() if (c.text or '').strip())[:600])
          for g in r if local(g.tag) in ("IdDisregardedEntitiesGrp", "IdRelatedTaxExemptOrgGrp", "IdRelatedOrgTxblPartnershipGrp", "IdRelatedOrgTxblCorpTrGrp", "TransactionsRelatedOrgGrp"))
    part_ix(root)
    lines = tuple({local(c.tag): (c.text or "").strip() for c in g} for g in f if local(g.tag) == "GrantsToOrgOutsideUSGrp")
    cash = lambda d: float(d.get("CashGrantAmt") or 0)  # noqa: E731
    big = tuple(sorted((l for l in lines if cash(l) >= 10_000_000), key=cash, reverse=True))
    print(f"Schedule F Part II lines: {len(lines)}; total cash {sum(map(cash, lines)):,.0f}")
    tuple(print("  >=10m", l.get("RegionTxt"), l.get("PurposeOfGrantTxt"), f"{cash(l):,.0f}", l.get("MannerOfCashDisbursementTxt")) for l in big)
    europe = tuple(l for l in lines if "EUROPE" in (l.get("RegionTxt") or "").upper())
    print(f"Europe Part II lines: {len(europe)}; total {sum(map(cash, europe)):,.0f}; count >= 1m: {sum(1 for l in europe if cash(l) >= 1e6)}")
    gbp = 30_939_000
    tuple(print(f"  implied USD/GBP if {cash(l):,.0f} = GBP 30.939m: {cash(l) / gbp:.4f}") for l in big[:3])
    sums = tuple(sorted(cash(l) for l in europe))
    print("Europe lines sorted (top 8):", [f"{x:,.0f}" for x in sums[-8:]])
    over1m = tuple(l for l in lines if cash(l) >= 1_000_000)
    round100k = tuple(l for l in over1m if cash(l) % 100_000 == 0)
    print(f"Part II lines >= $1m: {len(over1m)}; of which exact multiples of $100,000: {len(round100k)}")
    eur1m = tuple(l for l in europe if cash(l) >= 1_000_000)
    print(f"Europe lines >= $1m: {len(eur1m)}; exact multiples of $100,000: {sum(1 for l in eur1m if cash(l) % 100_000 == 0)}")
    if rate_file:
        h10 = read_h10(rate_file)
        fy = tuple((d, v) for d, v in h10 if "20240701" <= d <= "20250630")
        implied = 39_100_000 / gbp
        # GBP 30.939m is rounded to GBP 1k, so the implied rate band is 39.1m / (30.9395m .. 30.9385m)
        lo, hi = 39_100_000 / 30_939_500, 39_100_000 / 30_938_500
        near = tuple((d, v) for d, v in fy if abs(v - implied) <= 0.0025)
        print(f"FY2025 H.10 days: {len(fy)}; mean {sum(v for _, v in fy) / len(fy):.4f}; min {min(v for _, v in fy):.4f}; max {max(v for _, v in fy):.4f}")
        print(f"implied rate {implied:.5f} (band {lo:.5f}-{hi:.5f}); H.10 days within +/-0.0025: {len(near)}")
        print("  ", " ".join(f"{d}:{v:.4f}" for d, v in near))
        print(f"GBP 30.939m at FY mean = ${gbp * sum(v for _, v in fy) / len(fy):,.0f}; at FY min = ${gbp * min(v for _, v in fy):,.0f}; at FY max = ${gbp * max(v for _, v in fy):,.0f}")


GRANT_GRPS = ("GrantsToDomesticOrgsGrp", "GrantsToDomesticIndividualsGrp", "ForeignGrantsGrp")
STAFF_GRPS = ("CompCurrentOfcrDirectorsGrp", "CompDisqualPersonsGrp", "OtherSalariesAndWagesGrp",
              "PensionPlanContributionsGrp", "OtherEmployeeBenefitsGrp", "PayrollTaxesGrp")


def part_ix(root):
    """Form 990 Part IX column B (program services) excluding grants, grouped."""
    f = find_sched(root, "IRS990")
    rows = tuple((local(g.tag), {local(c.tag): (c.text or "") for c in g}) for g in f
                 if len(g) and any(local(c.tag) == "ProgramServicesAmt" for c in g))
    prog = lambda d: float(d.get("ProgramServicesAmt") or 0)  # noqa: E731
    total = next(prog(d) for n, d in rows if n == "TotalFunctionalExpensesGrp")
    grants = sum(prog(d) for n, d in rows if n in GRANT_GRPS)
    body = tuple((n, d) for n, d in rows if n not in GRANT_GRPS + ("TotalFunctionalExpensesGrp",))
    bucket = lambda n, d: ("11f investment management fees" if n == "FeesForSrvcInvstMgmntFeesGrp" else  # noqa: E731
                           "staff (comp, wages, benefits, payroll tax)" if n in STAFF_GRPS else
                           f"other: {d.get('Desc') or n}")
    agg = reduce(lambda acc, nd: {**acc, bucket(*nd): acc.get(bucket(*nd), 0.0) + prog(nd[1])}, body, {})
    ex = total - grants
    print(f"Part IX col B total {total:,.0f}; grants {grants:,.0f}; program services ex grants {ex:,.0f}")
    tuple(print(f"  {k:55s} {v:>14,.0f} {v / ex:6.1%}") for k, v in sorted(agg.items(), key=lambda kv: -kv[1]))
    print(f"  check sum {sum(agg.values()):,.0f}")
    inv = tuple({local(c.tag): float(c.text or 0) for c in g} for g in f
                if local(g.tag) in ("InvestmentsPubTradedSecGrp", "InvestmentsOtherSecuritiesGrp"))
    boy, eoy = sum(d.get("BOYAmt", 0) for d in inv), sum(d.get("EOYAmt", 0) for d in inv)
    mean = (boy + eoy) / 2
    f11 = next(prog(d) for n, d in rows if n == "FeesForSrvcInvstMgmntFeesGrp")
    print(f"Part X lines 11+12 investments BOY {boy:,.0f} EOY {eoy:,.0f} mean {mean:,.0f}; 11f(col B)/mean = {f11 / mean * 1e4:.1f} bps")
    tuple(print(f"  scenario: NPT model advisory fee {r:.2%} on ALL mean investments = {mean * r:,.0f}; 11f col B residual = {f11 - mean * r:,.0f}")
          for r in (0.0010, 0.0015))


MONTHS = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}


def read_h10(path):
    """(yyyymmdd, usd_per_gbp) from a saved Fed H.10 historical page (dat00_uk.htm); ND rows dropped."""
    import re
    with open(path, encoding="utf-8", errors="replace") as fh:
        t = fh.read()
    pairs = re.findall(r"<th[^>]*>\s*(\d{1,2})-([A-Z]{3})-(\d{2})\s*</th>\s*<td[^>]*>\s*([\d.]+)", t)
    return tuple((f"20{y}{MONTHS[m]:02d}{int(d):02d}", float(v)) for d, m, y, v in pairs)


def main(argv):
    if len(argv) < 3:
        raise SystemExit(__doc__)
    mode = argv[2]
    if mode == "wayback":
        return run_wayback(argv[3], argv[4], "--fetch" in argv)
    if mode == "npt990":
        return run_npt(argv[3], argv[4] if len(argv) > 4 else None)
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
