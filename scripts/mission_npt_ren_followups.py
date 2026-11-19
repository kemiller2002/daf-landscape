"""npt-ren-followups (P-B442802-01, P-G0702-03): capture history and Schedule F/R tests.

Usage:
  python3 -I scripts/mission_npt_ren_followups.py . wayback CACHE_DIR OUT_JSON [--fetch]
  python3 -I scripts/mission_npt_ren_followups.py . npt990 NPT_FY2025_XML [FX_RATE_FILE]
  python3 -I scripts/mission_npt_ren_followups.py . csv WAYBACK_JSON NPT_FY2025_XML NPT_FY2024_XML FX_RATE_FILE OUT_CSV

wayback: lists Wayback Machine captures of the Ren/RCF donor guides using only the
  archive.org availability API (https://archive.org/wayback/available; archive.org
  robots.txt disallows only /control/ and /report/). The CDX API and snapshot pages live on
  web.archive.org, which reset every connection from this session, so robots.txt there
  could not be read and nothing on that host is requested. The availability API returns
  the single capture closest to a timestamp; captures are enumerated by probing a monthly
  grid and bisecting every interval whose end points return different captures, down to
  a 1-day resolution. A URL with no answer at three spread-out pilot probes is recorded as
  having no listed capture. Captures inside one day of each other, or that are never the closest
  capture to any probe, can be missed. Responses are cached as JSON per probe so the run
  repeats offline (without --fetch the cache must be complete).
csv: assembles data/mission-2026-11-14/npt-ren-followups-2026-11-19.csv from the wayback
  JSON, both NPT XMLs, the H.10 page and the quoted constants below.
npt990: reads NPT's FY2025 Form 990 XML (object 202601289349302480) and prints the
  Schedule R Part V line-1 indicators (a-s, in schema order), Schedule R Part II/IV rows,
  the Schedule F Part II line distribution and the GBP->USD rates that would make
  GBP 30.939m equal each large Europe line.

Stdlib only; pure functions apart from the I/O wrappers at the edge. UA research-script/1.0.
"""
import csv, json, os, re, sys, time, hashlib, urllib.parse, urllib.request
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
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = json.loads(r.read().decode())
            if closest_of(body) is not None or attempt == 2:
                break  # an empty answer is retried: the API intermittently returns {} for URLs it holds
            time.sleep(2)
        except Exception as exc:  # noqa: BLE001
            # back off politely; HTTP 429 (rate limit) waits a full minute or more
            time.sleep(60 * (attempt + 1) if "429" in repr(exc) else 3 * (attempt + 1))
            err = repr(exc)
    if body is None:
        raise SystemExit(f"availability API failed for {url} {ts}: {err}")
    with open(path, "w") as fh:
        json.dump({"url": url, "ts": ts, "resp": body, "retrieved": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, fh)
    time.sleep(3.0)
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
    # The API answers with the capture closest to the timestamp at any distance, so a URL that
    # returns nothing at three spread-out probes (each retried) has no listed capture.
    pilots = tuple(closest_of(look(ts)) for ts in (grid[0], grid[len(grid) // 2], grid[-1]))
    if not any(pilots):
        return ()
    first = pilots[0]
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


# ---------- CSV build ----------
RET = "2026-11-19"
COLS = ("item", "row_type", "subject", "date", "value", "unit", "sha1", "quote", "source_url", "evidence", "note", "retrieved")
G26Q = "By default, this includes the grant advisor's name, email, and address"
G23Q = "The default is “Fund Name Only”."
LIVE = (  # (target_id, url, sha1, pdf_created, pdf_modified, last_modified_http, etag, quote)
    ("S1-rcf", "https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf", "93d97b49e84aa447f59b631dea1faee9e53c65ac",
     "2026-10-06T20:35:40Z", "2026-10-06T20:35:40Z", "Tue, 10 Nov 2026 19:59:13 GMT", '"34726ef54d71dd1:0"', G26Q),
    ("S1-ubs", "https://ubs.donorfirstx.com/pdf/UBS/Donor%20User%20Guide.pdf", "93d97b49e84aa447f59b631dea1faee9e53c65ac",
     "2026-10-06T20:35:40Z", "2026-10-06T20:35:40Z", "Tue, 10 Nov 2026 19:59:13 GMT", '"34726ef54d71dd1:0"', G26Q),
    ("S4-tda-2309", "https://tda.donorfirstx.com/pdf/tda/RCF%20Donor%20User%20Guide.pdf", "789efac9bf3ba248d4bb154184ffb3c16d595013",
     "2023-09-06T01:26:30Z", "2024-07-12T19:10:03Z", "Fri, 12 Jul 2024 19:24:56 GMT", '"4a9d32d91d4da1:0"', G23Q),
    ("S5-ubs-2309", "https://ubs.donorfirstx.com/pdf/UBS/UBS%20Donor%20User%20Guide.pdf", "0025f0fe726a4f2dec6b7df97b2f37dddad1c2b5",
     "2023-09-06T01:26:30Z", "2024-06-14T02:31:06Z", "Wed, 26 Jun 2024 13:22:53 GMT", '"d73b41f3cbc7da1:0"', G23Q),
)
HEAD_ONLY = ("ampf.donorfirstx.com/pdf/AMPF", "rbcrcf.donorfirstx.com/pdf/RBC", "mdrt.donorfirstx.com/pdf/mdrt",
              "rcfgivingfund.donorfirstx.com/pdf/RCF", "northwesternmutual.donorfirstx.com/pdf/NWM")
NPT25 = "https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf"
NPT24 = "https://www.nptrust.org/wp-content/uploads/2025/10/Consolidated-Statements-2024-NPT.pdf"
STATEMENTS = (  # (subject, fy, value_usd_thousands, quote, url, sha1, note)
    ("Investments, fair value", "FY2025", 47837978, "Investments, fair value 47,837,978", NPT25, "e7529055f11cff15942e93076c023d62c617aa6e", "no split by pooled/segregated"),
    ("Investments, fair value", "FY2024", 36915275, "Investments, fair value 36,915,275 23,080,890", NPT24, "ddfc47eeea7af36a33b2251b559e66e893282b8b", "FY2024 PDF"),
    ("Expense row captioned 'Asset management fees payable'", "FY2025", 116260, "Asset management fees payable 116,260 94,289", NPT25, "e7529055f11cff15942e93076c023d62c617aa6e", "caption reused from liabilities; same FY2024 figure is 'Program services' in the FY2024 PDF"),
    ("Program services (FY2024 PDF caption)", "FY2024", 94289, "Program services 94,289 71,021", NPT24, "ddfc47eeea7af36a33b2251b559e66e893282b8b", "so 116,260 (FY2025) is program services excluding grants"),
    ("Balance-sheet liability 'Asset management fees payable'", "FY2025", 400, "Asset management fees payable 400 353", NPT25, "e7529055f11cff15942e93076c023d62c617aa6e", "the real fee payable"),
    ("Total expenses", "FY2025", 6572593, "Total Expenses 6,572,593 5,751,932", NPT25, "e7529055f11cff15942e93076c023d62c617aa6e", "= 6,408,840 + 116,260 + 13,230 + 34,263"),
)
QUOTES = (  # (item, row_type, subject, date, quote, url, sha1, note)
    ("P-G0702-05", "npt_fee_doc", "Model portfolio advisory fee (Impact)", "2026-09-14", "In addition to the underlying investment costs, there is a 0.15% investment advisory fee.",
     "https://www.nptrust.org/wp-content/uploads/2024/09/Investment-Descriptions-and-Performance-NPT.pdf", "3a6ca8e98fdf", "PDF ModDate; sha1 prefix"),
    ("P-G0702-05", "npt_fee_doc", "Model portfolio advisory fee (actively managed and index)", "2026-09-14", "there is a 0.10% investment advisory fee and trading/transaction costs up to 4",
     "https://www.nptrust.org/wp-content/uploads/2024/09/Investment-Descriptions-and-Performance-NPT.pdf", "3a6ca8e98fdf", ""),
    ("P-G0702-05", "npt_fee_doc", "Segregated account fee set per account", "2024-01-31", "List all account numbers associated with this DAF and the investment advisory fee for each account, as applicable.",
     "https://www.nptrust.org/wp-content/uploads/2023/09/DAF-Segregated-Account-Investment-Information-NPT.pdf", "66f62882dd7b", "no published rate; no asset total"),
    ("P-G0702-03", "irs_instruction", "Schedule R disregarded entity exception", "2025-01-08",
     "Disregarded entities are treated as related organizations for purposes of reporting on Schedule R (Form 990), Part I, but not for purposes of reporting transactions with related organizations in Part V, or otherwise on Form 990.",
     "https://www.irs.gov/pub/irs-pdf/i990sr.pdf", "509585485fc9cba795e72c07cc88ab9c5b43239a", "Rev. December 2024"),
    ("P-G0702-03", "irs_instruction", "Schedule R Part V line 1", "2025-01-08",
     "Check “Yes” in the appropriate boxes of line 1 if the filing organization engaged in any of the transactions listed in Part V with any related organizations (other than disregarded entities listed in Part I).",
     "https://www.irs.gov/pub/irs-pdf/i990sr.pdf", "509585485fc9cba795e72c07cc88ab9c5b43239a", ""),
    ("P-G0702-03", "irs_instruction", "Form 990 Appendix F", "2025-12-11",
     "The organization must also report the activities of a disregarded entity in the appropriate parts (including schedules) of the Form 990.",
     "https://www.irs.gov/pub/irs-pdf/i990.pdf", "63250e5a536803362ab7ba874628077c0433635f", "2025 Instructions for Form 990"),
    ("P-G0702-03", "affiliate_accounts", "NPT Transatlantic note 19", "2025-06-30",
     "NPT Transatlantic also granted £30.9m to National Philanthropic Trust UK Limited (NPT UK), which will be used by donors for ongoing granting to charities.",
     "https://www.nptuk.org/transatlantic-annual-report-and-accounts-2025/", "", "grant table: 30,939 (GBP'000)"),
    ("P-G0702-03", "affiliate_accounts", "NPT UK note 14", "2025-06-30",
     "Contributions of £30.9M were received from NPT Transatlantic and £30.9M from National Philanthropic Trust.",
     "https://www.nptuk.org/npt-uk-annual-report-and-accounts-2025/", "", "one transfer described twice, or two transfers: not stated"),
)


def R(**k):
    return {**{c: "" for c in COLS}, "retrieved": RET, **k}


def wayback_rows(path):
    with open(path) as fh:
        data = json.load(fh)
    return tuple(
        R(item="P-B442802-01", row_type="wayback_capture", subject=t["url"], date=c["timestamp"], value=c["status"], unit="http_status",
          source_url=c["snapshot_url"], evidence="H", note="availability API only; snapshot not opened (web.archive.org unreachable); no digest")
        for t in data for c in t["captures"]) + tuple(
        R(item="P-B442802-01", row_type="wayback_none", subject=t["url"], value="0", unit="count",
          source_url="https://archive.org/wayback/available?url=" + t["url"], evidence="H", note="no capture returned at three spread-out pilot probes (2021-01, 2023-12, 2026-11), each retried up to 3 times")
        for t in data if not t["captures"])


def live_rows():
    return tuple(R(item="P-B442802-01", row_type="live_file", subject=tid, date=f"created {cr}; modified {md}; HTTP Last-Modified {lm}",
                   value=et, unit="etag", sha1=sha, quote=q, source_url=u, evidence="F") for tid, u, sha, cr, md, lm, et, q in LIVE) + tuple(
        R(item="P-B442802-01", row_type="live_file", subject=h + "/Donor%20User%20Guide.pdf", date="HTTP Last-Modified Tue, 10 Nov 2026 19:59:13 GMT",
          value='"34726ef54d71dd1:0"', unit="etag", source_url="https://" + h + "/Donor%20User%20Guide.pdf", evidence="F",
          note="HEAD only; Content-Length 5923340, same as the rcf copy (SHA-1 93d97b49e84a per b4428-02)") for h in HEAD_ONLY)


def npt_xml_rows(xml25, xml24, h10path):
    r25, r24 = ET.parse(xml25).getroot(), ET.parse(xml24).getroot()
    src = lambda oid: f"https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"  # noqa: E731
    sr = find_sched(r25, "IRS990ScheduleR")
    inds = tuple(e for e in sr if local(e.tag).endswith("Ind"))
    ind_rows = tuple(R(item="P-G0702-03", row_type="sched_r_indicator", subject=f"Schedule R Part V line 1{'abcdefghijklmnopqrs'[i]} {local(e.tag)}",
                       date="FY2025 (2024-07-01 to 2025-06-30)", value=e.text, unit="indicator", source_url=src("202601289349302480"), evidence="F",
                       note="line 1b should read Yes under the instructions if Transatlantic's grant to NPT UK is NPT's [I]" if i == 1 else "")
                     for i, e in enumerate(inds[:19]))
    orgs = tuple(g for g in sr if local(g.tag) in ("IdDisregardedEntitiesGrp", "IdRelatedTaxExemptOrgGrp"))
    name = lambda g: next((c.text for c in g.iter() if local(c.tag) == "BusinessNameLine1Txt"), "")  # noqa: E731
    field = lambda g, t: next((c.text for c in g.iter() if local(c.tag) == t), "")  # noqa: E731
    org_rows = tuple(R(item="P-G0702-03", row_type="sched_r_org", subject=f"{local(g.tag)}: {name(g)}", date="FY2025",
                       value=field(g, "TotalIncomeAmt") or field(g, "ControlledOrganizationInd"),
                       unit="usd total income" if local(g.tag) == "IdDisregardedEntitiesGrp" else "controlled indicator",
                       source_url=src("202601289349302480"), evidence="F",
                       note=f"EOY assets {field(g, 'EndOfYearAssetsAmt')}" if local(g.tag) == "IdDisregardedEntitiesGrp" else "exempt code section blank; direct controller NPT")
                     for g in orgs if re.search("TRANSATLANTIC|TRUST UK", name(g)))
    ix = tuple(R(item="P-G0702-05", row_type="npt_part_ix", subject=k, date=fy, value=f"{v:.0f}", unit="usd", source_url=src(oid), evidence="C",
                 note=f"{v / ex:.1%} of 990 program services excluding grants ({ex:,.0f})")
               for fy, oid, root in (("FY2025", "202601289349302480", r25), ("FY2024", "202511339349301311", r24))
               for ex, agg in (part_ix_data(root),) for k, v in sorted(agg.items(), key=lambda kv: -kv[1]))
    f = find_sched(r25, "IRS990ScheduleF")
    lines = tuple({local(c.tag): (c.text or "").strip() for c in g} for g in f if local(g.tag) == "GrantsToOrgOutsideUSGrp")
    cash = lambda d: float(d.get("CashGrantAmt") or 0)  # noqa: E731
    big = tuple(sorted((l for l in lines if cash(l) >= 10_000_000), key=cash, reverse=True))
    f_rows = tuple(R(item="P-G0702-03", row_type="sched_f_line", subject=f"{l.get('RegionTxt')} | {l.get('PurposeOfGrantTxt')} | {l.get('MannerOfCashDisbursementTxt')}",
                     date="FY2025", value=f"{cash(l):.0f}", unit="usd", source_url=src("202601289349302480"), evidence="F",
                     note=f"implied USD/GBP if = GBP 30.939m: {cash(l) / 30_939_000:.5f}") for l in big)
    over1m = tuple(l for l in lines if cash(l) >= 1e6)
    eur = tuple(l for l in lines if "EUROPE" in (l.get("RegionTxt") or "").upper())
    tests = (
        ("Part II lines (all)", len(lines), "count", f"total {sum(map(cash, lines)):,.0f}"),
        ("Part II Europe lines", len(eur), "count", f"total {sum(map(cash, eur)):,.0f}"),
        ("Part II lines >= $1m", len(over1m), "count", f"exact $100k multiples: {sum(1 for l in over1m if cash(l) % 100000 == 0)}"),
        ("Part II Europe lines >= $1m", sum(1 for l in eur if cash(l) >= 1e6), "count", f"exact $100k multiples: {sum(1 for l in eur if cash(l) >= 1e6 and cash(l) % 100000 == 0)}"),
    )
    t_rows = tuple(R(item="P-G0702-03", row_type="sched_f_test", subject=s_, date="FY2025", value=str(v), unit=u, source_url=src("202601289349302480"), evidence="C", note=n)
                   for s_, v, u, n in tests)
    h10 = read_h10(h10path)
    fy = tuple((d, v) for d, v in h10 if "20240701" <= d <= "20250630")
    imp = 39_100_000 / 30_939_000
    mean = sum(v for _, v in fy) / len(fy)
    near = tuple(d for d, v in fy if abs(v - imp) <= 0.0025)
    h10u = "https://www.federalreserve.gov/releases/h10/hist/dat00_uk.htm"
    fx = (("implied USD/GBP for $39,100,000 = GBP 30,939k", f"{imp:.5f}", "usd_per_gbp", ""),
          ("FY2025 H.10 mean / min / max", f"{mean:.4f} / {min(v for _, v in fy):.4f} / {max(v for _, v in fy):.4f}", "usd_per_gbp", f"{len(fy)} days"),
          ("GBP 30.939m at FY2025 mean rate", f"{30_939_000 * mean:.0f}", "usd", ""),
          ("H.10 days within +/-0.0025 of implied rate", str(len(near)), "count", " ".join(near)))
    fx_rows = tuple(R(item="P-G0702-03", row_type="fx_test", subject=s_, date="FY2025", value=v, unit=u, source_url=h10u, evidence="C", note=n) for s_, v, u, n in fx)
    return ind_rows + org_rows + ix + f_rows + t_rows + fx_rows


def part_ix_data(root):
    f = find_sched(root, "IRS990")
    rows = tuple((local(g.tag), {local(c.tag): (c.text or "") for c in g}) for g in f
                 if len(g) and any(local(c.tag) == "ProgramServicesAmt" for c in g))
    prog = lambda d: float(d.get("ProgramServicesAmt") or 0)  # noqa: E731
    total = next(prog(d) for n, d in rows if n == "TotalFunctionalExpensesGrp")
    grants = sum(prog(d) for n, d in rows if n in GRANT_GRPS)
    body = tuple((n, d) for n, d in rows if n not in GRANT_GRPS + ("TotalFunctionalExpensesGrp",))
    key = lambda n, d: ("11f investment management fees" if n == "FeesForSrvcInvstMgmntFeesGrp" else  # noqa: E731
                        "staff (comp, wages, benefits, payroll tax)" if n in STAFF_GRPS else
                        "program fees (other expenses)" if d.get("Desc") == "PROGRAM FEES" else
                        "information technology" if n == "InformationTechnologyGrp" else "all other program-column lines")
    return total - grants, reduce(lambda acc, nd: {**acc, key(*nd): acc.get(key(*nd), 0.0) + prog(nd[1])}, body, {})


def static_rows():
    st = tuple(R(item="P-G0702-05", row_type="npt_statement", subject=s_, date=fy, value=str(v), unit="usd_thousands", sha1=sha, quote=q, source_url=u, evidence="F", note=n)
               for s_, fy, v, q, u, sha, n in STATEMENTS)
    qs = tuple(R(item=i, row_type=t, subject=s_, date=d, quote=q, source_url=u, sha1=sha, evidence="F", note=n, unit="text") for i, t, s_, d, q, u, sha, n in QUOTES)
    return st + qs


def run_csv(wb_json, xml25, xml24, h10, out):
    rows = wayback_rows(wb_json) + live_rows() + static_rows() + npt_xml_rows(xml25, xml24, h10)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        tuple(map(w.writerow, rows))
    print(f"wrote {len(rows)} rows to {out}")


def main(argv):
    if len(argv) < 3:
        raise SystemExit(__doc__)
    mode = argv[2]
    if mode == "wayback":
        return run_wayback(argv[3], argv[4], "--fetch" in argv)
    if mode == "csv":
        return run_csv(*argv[3:8])
    if mode == "npt990":
        return run_npt(argv[3], argv[4] if len(argv) > 4 else None)
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
