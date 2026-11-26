#!/usr/bin/env python3
"""Recipient overlap across the top-50 DAF sponsors: is there a reuse mechanism for a SHARED verification network?

Universe   top-50 DAF sponsors by FY2024 DAF assets (rank_fy2024 <= 50 in
           data/mission-2026-11-14/sponsor-operating-efficiency-2026-11-20.csv, record_type=sponsor_year).
Return     one return per sponsor: FY2023 (as labelled in that file); FY2024 when the FY2023 return is missing,
           unfetchable or has no Schedule I Part II lines. `fiscal_year` records which was used.
Lines      every IRS Form 990 Schedule I Part II RecipientTable line in the public e-file XML (GivingTuesday mirror
           of IRS TEOS). Amount = CashGrantAmt + NonCashAssistanceAmt.
Exclusions self-lines (recipient EIN = filer EIN); DAF-to-DAF lines (recipient EIN with decision `include` in
           daf-to-daf-recipient-whitelist.csv; a blank-EIN line whose normalised name equals exactly one
           whitelisted name) -- the rule of scripts/mission_recipient_sectors.py.
Keys       recipient EIN normalised to 9 digits (key_type=ein); a line with no usable EIN keeps its normalised
           name (mission_net_payout.norm_name) as the key (key_type=name, flagged `no_ein` in the summary).
Metrics    see METRIC_DEFS (also written into the summary CSV).

Stdlib only; functional style (pure transforms; I/O at the edges).

Usage:
  python3 scripts/workflow_innovation_recipient_overlap.py --xml-dir DIR [--fetch] [--workers 3]
"""
from __future__ import annotations

import argparse
import csv
import gzip
import os
import random
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import XML_URL, ein9, local, num  # noqa: E402
from mission_net_payout import norm_name  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPONSORS_CSV = os.path.join(ROOT, "data", "mission-2026-11-14", "sponsor-operating-efficiency-2026-11-20.csv")
WHITELIST = os.path.join(ROOT, "data", "mission-2026-11-14", "daf-to-daf-recipient-whitelist.csv")
OUT_DIR = os.path.join(ROOT, "data", "workflow-innovation")
EDGES = os.path.join(OUT_DIR, "sponsor-recipient-edges-fy2023.csv")
SUMMARY = os.path.join(OUT_DIR, "recipient-overlap-summary.csv")
TOP_N, PREFERRED_FY, FALLBACK_FY = 50, "2023", "2024"
N_SHUFFLES, SEED = 200, 20261120
MAX_EDGES_BYTES = 25 * 1024 * 1024
BUCKETS = (("1", 1, 1), ("2", 2, 2), ("3-5", 3, 5), ("6-10", 6, 10), ("11-25", 11, 25), ("26+", 26, 10 ** 9))
UA = "research-script/1.0 (stdlib urllib)"

METRIC_DEFS = {
    "sponsors_parsed": "top-50 sponsors with >=1 Schedule I Part II line kept after exclusions",
    "sponsors_fy": "sponsors whose edges come from this fiscal year's return",
    "lines_raw": "Schedule I Part II RecipientTable lines in the parsed returns, before exclusions",
    "lines_excluded_self": "lines whose recipient EIN equals the filer EIN",
    "lines_excluded_daf_to_daf": "lines to a whitelisted (decision=include) DAF sponsor EIN, or blank-EIN lines whose "
                                 "normalised name uniquely matches a whitelisted name",
    "lines_kept": "lines kept after exclusions",
    "lines_kept_no_ein": "kept lines with no usable recipient EIN (keyed by normalised name)",
    "amount_kept_usd": "cash + non-cash on kept lines",
    "edges": "distinct sponsor x recipient_key pairs",
    "distinct_recipients": "distinct recipient keys (EIN keys + name keys)",
    "distinct_recipients_ein": "distinct EIN recipient keys",
    "distinct_recipients_name": "distinct name keys (no EIN)",
    "recipients_by_n_sponsors": "recipients whose key appears on the Schedule I of n distinct top-50 sponsors; "
                                "value = count of recipients / kept lines / dollars / share of each",
    "sponsor_share_shared_ge2": "share of the sponsor's kept lines (or dollars) going to recipients also funded by "
                                ">=1 other parsed top-50 sponsor (n_sponsors >= 2)",
    "sponsor_share_shared_ge6": "share of the sponsor's kept lines (or dollars) going to recipients also funded by "
                                ">=5 other parsed top-50 sponsors (n_sponsors >= 6)",
    "reuse_curve": "sponsors join a shared verification network one at a time in the given order. For the k-th "
                   "joiner: line_share = share of its kept lines whose recipient key was already on the Schedule I "
                   "of one of the k-1 earlier joiners; recipient_share = same over its distinct recipient keys; "
                   "dollar_share = same over its dollars; cum_verifications_avoided = 1 - |union of keys of first k| / "
                   "sum of distinct keys of first k (share of per-sponsor verifications a shared record would "
                   "have avoided so far). random = mean over 200 seeded shuffles (seed 20261120), with p10/p90.",
}


# ----------------------------------------------------------------------------- inputs (I/O)
def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, encoding="utf-8", newline="") as fh:
        return tuple(csv.DictReader(fh))


def candidate_returns(rows: Iterable[Mapping]) -> dict[str, dict]:
    """sponsor EIN -> {rank, name, by_fy: {fy: {object_id, tax_period, xml_url}}} for the top-N sponsors."""
    out: dict[str, dict] = {}
    for r in rows:
        if r.get("record_type") != "sponsor_year" or not r.get("rank_fy2024") or int(r["rank_fy2024"]) > TOP_N:
            continue
        e = ein9(r["ein"])
        s = out.setdefault(e, {"ein": e, "rank": int(r["rank_fy2024"]), "name": r["sponsor_name"], "by_fy": {}})
        if r["object_id"]:
            s["by_fy"][r["fy"]] = {"object_id": r["object_id"], "tax_period": r["tax_period"],
                                   "xml_url": r["xml_url"] or XML_URL.format(oid=r["object_id"])}
    return out


def whitelist_from(rows: Sequence[Mapping]) -> tuple[frozenset, dict]:
    inc = tuple(r for r in rows if r["decision"] == "include")
    eins = frozenset(ein9(r["recipient_ein"]) for r in inc)
    by_name: dict[str, set] = defaultdict(set)
    for r in inc:
        by_name[norm_name(r["recipient_name"])].add(ein9(r["recipient_ein"]))
    return eins, {k: next(iter(v)) for k, v in by_name.items() if k and len(v) == 1}


def fetch_xml(url: str, path: str, retries: int = 4) -> str:
    """Download url to path once (atomic rename); returns status."""
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return "cached"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last = "error"
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=900) as resp, open(path + ".part", "wb") as fh:
                while chunk := resp.read(1 << 20):
                    fh.write(chunk)
            os.replace(path + ".part", path)
            return "fetched"
        except urllib.error.HTTPError as e:
            last = f"http_{e.code}"
            if e.code in (403, 404):
                return last
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last = f"error:{type(e).__name__}"
        time.sleep(5 * 2 ** attempt)
    return last


def parse_sched_i(path: str) -> dict:
    """Stream-parse an e-file XML -> filer EIN, tax period, Schedule I Part II lines [ein, name, amount]."""
    lines, filer, period = [], "", ""
    for _, el in ET.iterparse(path, events=("end",)):
        tag = local(el.tag)
        if tag == "RecipientTable":
            lines.append(line_of(el))
            el.clear()
        elif tag == "Filer" and not filer:
            filer = next((ein9(c.text) for c in el if local(c.tag) == "EIN" and c.text), "")
        elif tag == "TaxPeriodEndDt" and not period:
            period = (el.text or "").strip()
        elif tag.startswith("IRS990") and tag != "IRS990ScheduleI":
            el.clear()
    return {"filer_ein": filer, "period_end": period, "lines": tuple(lines)}


def line_of(el) -> tuple:
    g = {local(c.tag): (c.text or "").strip() for c in el.iter() if c.text}
    name = " ".join((c.text or "").strip() for c in el.iter()
                    if local(c.tag) in ("BusinessNameLine1Txt", "BusinessNameLine2Txt") and c.text)
    e = ein9(g["RecipientEIN"]) if g.get("RecipientEIN") else ""
    return (e if e.strip("0") else "", name, (num(g.get("CashGrantAmt")) or 0.0) + (num(g.get("NonCashAssistanceAmt")) or 0.0))


# ----------------------------------------------------------------------------- transforms (pure)
ATTACH_RX = re.compile(r"\b(SEE|PER)\b.*\b(ATTACH\w*|STATEMENT|SCHEDULE|LIST|REPORT)\b|\bATTACHED\b")


def attachment_only(lines: Sequence[Sequence]) -> bool:
    """Schedule I Part II filed as a placeholder ('SEE ATTACHED ...') rather than itemised in the XML."""
    return 0 < len(lines) <= 5 and all(not l[0] and ATTACH_RX.search(l[1].upper()) for l in lines)


def classify_line(line: Sequence, filer: str, wl_eins: frozenset, wl_names: Mapping) -> tuple[str, str, str]:
    """-> (status, key, key_type); status in kept|self|daf_to_daf|no_key."""
    e, name, _ = line
    nm = norm_name(name)
    if e and e == filer:
        return "self", e, "ein"
    if (e and e in wl_eins) or (not e and nm in wl_names):
        return "daf_to_daf", e or nm, "ein" if e else "name"
    if e:
        return "kept", e, "ein"
    return ("kept", nm, "name") if nm else ("no_key", "", "")


def edges_for(sponsor: Mapping, fy: str, parsed: Mapping, wl_eins: frozenset, wl_names: Mapping) -> tuple[tuple, Counter]:
    filer = parsed["filer_ein"] or sponsor["ein"]
    agg: dict[tuple, list] = {}
    stats: Counter = Counter()
    for line in parsed["lines"]:
        st, key, kt = classify_line(line, filer, wl_eins, wl_names)
        stats[f"lines_{st}"] += 1
        stats["lines_raw"] += 1
        if st != "kept":
            stats[f"amount_{st}"] += line[2]
            continue
        stats["amount_kept_usd"] += line[2]
        stats["lines_kept_no_ein"] += kt == "name"
        a = agg.setdefault((key, kt), [0, 0.0])
        a[0] += 1
        a[1] += line[2]
    edges = tuple({"sponsor_ein": sponsor["ein"], "sponsor_rank": sponsor["rank"], "fiscal_year": fy,
                   "recipient_key": k, "key_type": kt, "lines": v[0], "amount_usd": round(v[1], 2)}
                  for (k, kt), v in sorted(agg.items()))
    return edges, stats


def rkey(e: Mapping) -> str:
    return ("E:" if e["key_type"] == "ein" else "N:") + e["recipient_key"]


def by_sponsor(edges: Sequence[Mapping]) -> dict[str, dict[str, tuple[int, float]]]:
    out: dict[str, dict] = defaultdict(dict)
    for e in edges:
        out[e["sponsor_ein"]][rkey(e)] = (e["lines"], e["amount_usd"])
    return dict(out)


def n_sponsors(bys: Mapping[str, Mapping]) -> Counter:
    return Counter(k for m in bys.values() for k in m)


def bucket_of(n: int) -> str:
    return next(b for b, lo, hi in BUCKETS if lo <= n <= hi)


def distribution(bys: Mapping, ns: Mapping, keep=lambda k: True) -> tuple[dict, ...]:
    rec, lines, dollars = Counter(), Counter(), Counter()
    for k, n in ns.items():
        if keep(k):
            rec[bucket_of(n)] += 1
    for m in bys.values():
        for k, (l, a) in m.items():
            if keep(k):
                lines[bucket_of(ns[k])] += l
                dollars[bucket_of(ns[k])] += a
    tot = (sum(rec.values()) or 1, sum(lines.values()) or 1, sum(dollars.values()) or 1)
    return tuple({"bucket": b, "recipients": rec[b], "recipients_share": rec[b] / tot[0], "lines": lines[b],
                  "lines_share": lines[b] / tot[1], "amount_usd": dollars[b], "amount_share": dollars[b] / tot[2]}
                 for b, _, _ in BUCKETS)


def sponsor_shares(m: Mapping, ns: Mapping) -> dict:
    L = sum(l for l, _ in m.values()) or 1
    A = sum(a for _, a in m.values()) or 1
    f = lambda t, i: sum(v[i] for k, v in m.items() if ns[k] >= t)  # noqa: E731
    return {"lines": sum(l for l, _ in m.values()), "amount_usd": sum(a for _, a in m.values()),
            "distinct_recipients": len(m), "share_lines_ge2": f(2, 0) / L, "share_amount_ge2": f(2, 1) / A,
            "share_lines_ge6": f(6, 0) / L, "share_amount_ge6": f(6, 1) / A,
            "share_recipients_ge2": sum(1 for k in m if ns[k] >= 2) / (len(m) or 1)}


def reuse_curve(order: Sequence[str], bys: Mapping) -> tuple[dict, ...]:
    seen: set = set()
    out, cum_sum = [], 0
    for i, s in enumerate(order, 1):
        m = bys[s]
        L = sum(l for l, _ in m.values()) or 1
        A = sum(a for _, a in m.values()) or 1
        hit = [k for k in m if k in seen]
        cum_sum += len(m)
        seen.update(m)
        out.append({"k": i, "sponsor_ein": s, "line_share": sum(m[k][0] for k in hit) / L,
                    "recipient_share": len(hit) / (len(m) or 1), "dollar_share": sum(m[k][1] for k in hit) / A,
                    "cum_verifications_avoided": 1 - len(seen) / (cum_sum or 1)})
    return tuple(out)


def random_curves(sponsors: Sequence[str], bys: Mapping, n: int = N_SHUFFLES, seed: int = SEED) -> tuple[dict, ...]:
    rng = random.Random(seed)
    runs = []
    for _ in range(n):
        order = list(sponsors)
        rng.shuffle(order)
        runs.append(reuse_curve(order, bys))
    mets = ("line_share", "recipient_share", "dollar_share", "cum_verifications_avoided")

    def q(xs, p):
        xs = sorted(xs)
        return xs[min(len(xs) - 1, int(p * (len(xs) - 1) + 0.5))]
    return tuple({"k": k + 1, **{m: statistics.fmean(r[k][m] for r in runs) for m in mets},
                  **{f"{m}_p10": q([r[k][m] for r in runs], 0.10) for m in mets},
                  **{f"{m}_p90": q([r[k][m] for r in runs], 0.90) for m in mets}}
                 for k in range(len(sponsors)))


# ----------------------------------------------------------------------------- summary rows (pure)
FIELDS = ("section", "scope", "order", "k", "sponsor_ein", "sponsor_rank", "sponsor_name", "fiscal_year", "bucket",
          "metric", "value", "definition")


def row(section, metric, value, **kw) -> dict:
    v = round(value, 6) if isinstance(value, float) else value
    return {**{f: "" for f in FIELDS}, "section": section, "metric": metric, "value": v,
            "definition": kw.pop("definition", METRIC_DEFS.get(metric, "")), **kw}


def summary_rows(sponsors: Mapping, chosen: Mapping, stats: Mapping, edges: Sequence[Mapping]) -> list[dict]:
    bys = by_sponsor(edges)
    ns = n_sponsors(bys)
    tot: Counter = sum(stats.values(), Counter())
    out = [row("coverage", "sponsors_parsed", len(bys))]
    out += [row("coverage", "sponsors_fy", c, fiscal_year=fy) for fy, c in sorted(Counter(chosen[s]["fy"] for s in bys).items())]
    out += [row("coverage", label, tot[m]) for label, m in (
        ("lines_raw", "lines_raw"), ("lines_excluded_self", "lines_self"),
        ("lines_excluded_daf_to_daf", "lines_daf_to_daf"), ("lines_kept", "lines_kept"),
        ("lines_kept_no_ein", "lines_kept_no_ein"))]
    out += [row("coverage", "lines_dropped_no_key", tot["lines_no_key"],
                definition="lines with neither a usable EIN nor a name (dropped)"),
row("coverage", "amount_kept_usd", round(tot["amount_kept_usd"], 2)),
            row("coverage", "amount_excluded_daf_to_daf_usd", round(tot["amount_daf_to_daf"], 2),
                definition="dollars on DAF-to-DAF lines (excluded)"),
            row("coverage", "edges", len(edges)),
            row("coverage", "distinct_recipients", len(ns)),
            row("coverage", "distinct_recipients_ein", sum(1 for k in ns if k.startswith("E:"))),
            row("coverage", "distinct_recipients_name", sum(1 for k in ns if k.startswith("N:")))]
    scopes = (("all_keys", lambda k: True), ("ein_keys_only", lambda k: k.startswith("E:")))
    for scope, keep in scopes:
        for d in distribution(bys, ns, keep):
            out += [row("distribution", f"recipients_by_n_sponsors.{m}", d[m], scope=scope, bucket=d["bucket"],
                        definition=METRIC_DEFS["recipients_by_n_sponsors"])
                    for m in ("recipients", "recipients_share", "lines", "lines_share", "amount_usd", "amount_share")]
    for s in sorted(bys, key=lambda s: sponsors[s]["rank"]):
        sh = sponsor_shares(bys[s], ns)
        base = {"sponsor_ein": s, "sponsor_rank": sponsors[s]["rank"], "sponsor_name": sponsors[s]["name"],
                "fiscal_year": chosen[s]["fy"]}
        out += [row("sponsor", m, v, **base, definition=METRIC_DEFS.get(
            "sponsor_share_shared_ge2" if "ge2" in m else "sponsor_share_shared_ge6" if "ge6" in m else "", ""))
            for m, v in sh.items()]
        out += [row("sponsor", m, stats[s][m], **base, definition=METRIC_DEFS.get(m, ""))
                for m in ("lines_raw", "lines_self", "lines_daf_to_daf", "lines_kept_no_ein")]
    # pooled shares: all sponsors, and a sensitivity without the largest (rank-1) sponsor
    largest = min(bys, key=lambda s: sponsors[s]["rank"])
    out += pooled_rows(bys, ns, "all_sponsors", "all parsed sponsors pooled")
    rest = {s: m for s, m in bys.items() if s != largest}
    out += pooled_rows(rest, n_sponsors(rest), "excl_rank1",
                       f"sensitivity: {sponsors[largest]['name']} removed from the network and the counts")
    desc = sorted(bys, key=lambda s: sponsors[s]["rank"])
    curve_mets = ("line_share", "recipient_share", "dollar_share", "cum_verifications_avoided")
    for order_name, order in (("descending_assets", desc), ("ascending_assets", desc[::-1])):
        for c in reuse_curve(order, bys):
            s = c["sponsor_ein"]
            out += [row("reuse_curve", m, c[m], order=order_name, k=c["k"], sponsor_ein=s, sponsor_rank=sponsors[s]["rank"],
                        sponsor_name=sponsors[s]["name"], definition=METRIC_DEFS["reuse_curve"]) for m in curve_mets]
    for c in random_curves(desc, bys):
        out += [row("reuse_curve", m, c[m], order=f"random_mean_{N_SHUFFLES}", k=c["k"], definition=METRIC_DEFS["reuse_curve"])
                for m in c if m != "k"]
    return out


def pooled_rows(bys: Mapping, ns: Mapping, scope: str, label: str) -> list[dict]:
    L = sum(l for m in bys.values() for l, _ in m.values()) or 1
    A = sum(a for m in bys.values() for _, a in m.values()) or 1
    return [r for t, lab in ((2, "ge2"), (6, "ge6")) for r in (
        row("pooled", f"share_lines_{lab}", sum(l for m in bys.values() for k, (l, _) in m.items() if ns[k] >= t) / L,
            scope=scope, definition=f"{label}: share of kept lines to recipients with n_sponsors >= {t}"),
        row("pooled", f"share_amount_{lab}", sum(a for m in bys.values() for k, (_, a) in m.items() if ns[k] >= t) / A,
            scope=scope, definition=f"{label}: share of kept dollars to recipients with n_sponsors >= {t}"),
        row("pooled", f"share_recipients_{lab}", sum(1 for k in ns if ns[k] >= t) / (len(ns) or 1),
            scope=scope, definition=f"{label}: share of distinct recipients with n_sponsors >= {t}"))]


# ----------------------------------------------------------------------------- main (I/O)
def choose_and_parse(sponsors: Mapping, xml_dir: str, fetch: bool, workers: int) -> tuple[dict, dict]:
    """Fetch (cached) and parse the preferred return, falling back to FY2024. -> (chosen, attempts log)."""
    def path_for(oid):
        return os.path.join(xml_dir, f"{oid}_public.xml")

    def get(s, fy):
        ret = sponsors[s]["by_fy"].get(fy)
        if not ret:
            return {"fy": fy, "status": "no_return_in_input"}
        st = fetch_xml(ret["xml_url"], path_for(ret["object_id"])) if fetch else (
            "cached" if os.path.exists(path_for(ret["object_id"])) else "not_fetched")
        if st not in ("cached", "fetched"):
            return {"fy": fy, **ret, "status": st}
        try:
            p = parse_sched_i(path_for(ret["object_id"]))
        except ET.ParseError as e:
            return {"fy": fy, **ret, "status": f"parse_error:{e}"}
        st = "ok" if p["lines"] else "no_schedule_i_part_ii_lines"
        st = "attachment_only" if attachment_only(p["lines"]) else st
        return {"fy": fy, **ret, "status": st, "parsed": p}

    def one(s):
        a = get(s, PREFERRED_FY)
        if a["status"] == "ok":
            return s, a, [a]
        b = get(s, FALLBACK_FY)
        return s, (b if b["status"] == "ok" else None), [a, b]

    with ThreadPoolExecutor(max_workers=max(1, min(4, workers))) as ex:
        res = list(ex.map(one, sorted(sponsors, key=lambda s: sponsors[s]["rank"])))
    return ({s: c for s, c, _ in res if c}, {s: log for s, _, log in res})


def write_edges(edges: Sequence[Mapping]) -> str:
    fields = ("sponsor_ein", "sponsor_rank", "fiscal_year", "recipient_key", "key_type", "lines", "amount_usd")
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(EDGES, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(edges)
    if os.path.getsize(EDGES) <= MAX_EDGES_BYTES:
        return EDGES
    with open(EDGES, "rb") as src, gzip.open(EDGES + ".gz", "wb", compresslevel=9) as dst:
        dst.write(src.read())
    os.remove(EDGES)
    return EDGES + ".gz"


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xml-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args(argv)
    os.makedirs(a.xml_dir, exist_ok=True)
    sponsors = candidate_returns(read_csv(SPONSORS_CSV))
    wl_eins, wl_names = whitelist_from(read_csv(WHITELIST))
    chosen, log = choose_and_parse(sponsors, a.xml_dir, a.fetch, a.workers)
    built = {s: edges_for(sponsors[s], c["fy"], c["parsed"], wl_eins, wl_names) for s, c in chosen.items()}
    edges = tuple(e for s in sorted(built, key=lambda s: sponsors[s]["rank"]) for e in built[s][0])
    stats = {s: v[1] for s, v in built.items()}
    path = write_edges(edges)
    rows = summary_rows(sponsors, chosen, stats, edges)
    # attempt log (coverage, incl. failures) as summary rows
    for s in sorted(log, key=lambda s: sponsors[s]["rank"]):
        for at in log[s]:
            rows.append(row("attempt", "return_status", at["status"], sponsor_ein=s, sponsor_rank=sponsors[s]["rank"],
                            sponsor_name=sponsors[s]["name"], fiscal_year=at["fy"],
                            scope=at.get("object_id", ""), order=at.get("tax_period", ""),
                            bucket=str(len(at["parsed"]["lines"])) if "parsed" in at else "",
                            definition="fetch/parse outcome; scope=object_id, order=tax_period, bucket=raw Part II lines"))
    with open(SUMMARY, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"sponsors parsed {len(chosen)}/{len(sponsors)}; edges {len(edges)} -> {path}; summary -> {SUMMARY}")
    for s in sorted(log, key=lambda s: sponsors[s]["rank"]):
        print(sponsors[s]["rank"], sponsors[s]["name"][:40], [(x["fy"], x["status"]) for x in log[s]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
