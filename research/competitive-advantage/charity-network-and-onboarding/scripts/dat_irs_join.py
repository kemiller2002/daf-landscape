"""DAT cross-file consistency checks on IRS bulk files (stdlib only).

Usage: python3 -I dat_irs_join.py <dir containing eo1-eo4.csv, data-download-pub78.txt,
       data-download-revocation.txt>

Pure functions compute everything; I/O is confined to the loaders and main().

Open-revoked definition (order-independent, used in 04): an EIN is open-revoked if
no revocation row for it carries a reinstatement date on or after its latest
revocation date. Posting-lag figures are computed per row (each posting event).
"""
import collections
import csv
import datetime as dt
import os
import pprint
import sys
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

BMF_FILES = ("eo1.csv", "eo2.csv", "eo3.csv", "eo4.csv")  # never add eo_pr/eo_xx: they duplicate eo4

RevRow = Tuple[Optional[dt.date], Optional[dt.date], Optional[dt.date]]  # (revocation, posting, reinstatement)


# ---------- I/O edges ----------
def load_bmf(d: str) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    for fn in BMF_FILES:
        with open(os.path.join(d, fn), newline="", encoding="latin-1") as f:
            for r in csv.DictReader(f):
                out[r["EIN"]] = r
    return out


def load_pipe(path: str) -> List[List[str]]:
    with open(path, encoding="latin-1") as f:
        return [l.rstrip("\n").split("|") for l in f if l.strip()]


# ---------- pure functions ----------
def parse_date(s: str) -> Optional[dt.date]:
    try:
        return dt.datetime.strptime(s.strip(), "%d-%b-%Y").date()
    except ValueError:
        return None


def ruling_date(s: str) -> Optional[dt.date]:
    return dt.date(int(s[:4]), int(s[4:6]), 1) if len(s) == 6 and s.isdigit() and s[4:6] != "00" else None


def group_revocations(rows: Iterable[List[str]]) -> Dict[str, Tuple[RevRow, ...]]:
    acc: Dict[str, list] = collections.defaultdict(list)
    for r in rows:
        acc[r[0]].append((parse_date(r[9]), parse_date(r[10]), parse_date(r[11])))
    return {e: tuple(v) for e, v in acc.items()}


def open_revocation(rs: Tuple[RevRow, ...]) -> Tuple[Optional[dt.date], bool]:
    latest = max((x[0] for x in rs if x[0]), default=None)
    reinstated = latest is not None and any(x[2] and x[2] >= latest for x in rs)
    return latest, (latest is not None and not reinstated)


def quantiles(xs: List[int]) -> Optional[Tuple[int, int, int, int]]:
    s = sorted(xs)
    return (s[len(s) // 10], s[len(s) // 2], s[9 * len(s) // 10], len(s)) if s else None


def coverage_stats(bmf: Mapping[str, dict], p78: Mapping[str, list]) -> dict:
    c3 = {e: r for e, r in bmf.items() if r["SUBSECTION"] == "03"}
    missing = [e for e in c3 if e not in p78]
    return {
        "c3_in_bmf": len(c3),
        "c3_in_pub78": len(c3) - len(missing),
        "c3_not_in_pub78_by_affil": collections.Counter(c3[e]["AFFILIATION"] for e in missing).most_common(),
        "c3_not_in_pub78_by_found": collections.Counter(c3[e]["FOUNDATION"] for e in missing).most_common(8),
        "c3_affil9": sum(1 for r in c3.values() if r["AFFILIATION"] == "9"),
        "c3_affil9_in_pub78": sum(1 for e, r in c3.items() if r["AFFILIATION"] == "9" and e in p78),
        "pub78_not_in_bmf": sum(1 for e in p78 if e not in bmf),
        "pub78_not_in_bmf_codes": collections.Counter(p78[e][5] for e in p78 if e not in bmf).most_common(6),
        "pub78_names_over70_also_in_bmf": sum(1 for e in p78 if e in bmf and len(p78[e][1]) > 70),
        "bmf_c3_status": collections.Counter(r["STATUS"] for r in c3.values()).most_common(),
    }


def revocation_stats(bmf: Mapping[str, dict], p78: Mapping[str, list],
                     revs: Mapping[str, Tuple[RevRow, ...]]) -> dict:
    status = {e: open_revocation(rs) for e, rs in revs.items()}
    open_eins = [e for e, (_, o) in status.items() if o]
    in_bmf = [e for e in open_eins if e in bmf]
    later_ruling = [e for e in in_bmf
                    if ruling_date(bmf[e]["RULING"]) and ruling_date(bmf[e]["RULING"]) > status[e][0]]
    lags = [(p.month, (p - r).days) for rs in revs.values() for (r, p, _) in rs if r and p and p.year == 2026]
    return {
        "open_revoked_eins": len(open_eins),
        "open_revoked_in_bmf": len(in_bmf),
        "open_revoked_in_pub78": sum(1 for e in open_eins if e in p78),
        "open_revoked_in_bmf_and_pub78": sum(1 for e in in_bmf if e in p78),
        "open_revoked_in_bmf_ruling_after_revocation": len(later_ruling),
        "open_revoked_in_bmf_residual_for_review": len(in_bmf) - len(later_ruling),
        "posting_lag_2026_august_p10_p50_p90_n": quantiles([x for m, x in lags if m == 8]),
        "posting_lag_2026_other_months_p10_p50_p90_n": quantiles([x for m, x in lags if m != 8]),
    }


def main(d: str) -> None:
    bmf = load_bmf(d)
    p78 = {r[0]: r for r in load_pipe(os.path.join(d, "data-download-pub78.txt"))}
    revs = group_revocations(load_pipe(os.path.join(d, "data-download-revocation.txt")))
    pprint.pprint({**coverage_stats(bmf, p78), **revocation_stats(bmf, p78, revs)}, width=150)


if __name__ == "__main__":
    main(sys.argv[1])
