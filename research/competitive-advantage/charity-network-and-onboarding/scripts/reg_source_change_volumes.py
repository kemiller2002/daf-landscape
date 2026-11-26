#!/usr/bin/env python3
"""REG: measure change volumes in public charity-status sources (stdlib only, functional style).

Used by 06-continuous-vetting.md to estimate how many monitoring events a change-driven
vetting design must classify, and how many of them are material.

Sub-commands (all inputs are local copies of public files; this script does no network I/O):

  bmf-diff OLD.csv NEW.csv
      Compare two monthly EO BMF snapshots (IRS layout or the NCCS raw mirror layout,
      https://nccsdata.s3.us-east-1.amazonaws.com/raw/bmf/{YYYY-MM}-BMF.csv) and count
      additions, removals and field changes, classified with the proposed MaterialityTable
      (MATERIALITY below). Only 501(c)(3) rows are counted for the c3_* figures.

  revocations FILE
      Profile the IRS Auto-Revocation List (pipe-delimited data-download-revocation.txt):
      postings per month/year, subsection mix, posting lag, and reinstatement timing
      (retroactive = reinstatement date equal to revocation date).

  bmf-profile PUB78.txt BMF1.csv [BMF2.csv ...]
      Identity-resolution stress statistics for the current IRS EO BMF: shared names,
      shared street addresses, group-exemption subordinates and their absence from Pub 78.

Output: one JSON object on stdout. All functions except main() are pure.
"""
import csv
import collections
import datetime
import json
import re
import sys
from typing import Dict, Iterable, Iterator, List, Mapping, Tuple

# Field -> materiality class for a changed BMF field (proposed; see 06 section 3).
# MA = material-adverse candidate (eligibility/authority/payment impact possible)
# MN = material-neutral (deterministic effect, no case)
# IN = informational (evidence update only)
MATERIALITY: Mapping[str, str] = {
    "SUBSECTION": "MA",      # leaves 501(c)(3)
    "FOUNDATION": "MA",      # public charity -> private foundation / SO type change
    "DEDUCTIBILITY": "MA",   # deductibility code change
    "STATUS": "MA",          # exemption status code change
    "GROUP": "MA",           # joins/leaves a group exemption
    "AFFILIATION": "MA",     # central/subordinate/independent change
    "NAME": "MN",            # legal-name change, same EIN
    "STREET": "MN", "CITY": "MN", "STATE": "MN", "ZIP": "MN",
    "ICO": "IN",             # in-care-of person
    "TAX_PERIOD": "IN", "ASSET_CD": "IN", "INCOME_CD": "IN", "ASSET_AMT": "IN",
    "INCOME_AMT": "IN", "REVENUE_AMT": "IN", "FILING_REQ_CD": "IN", "PF_FILING_REQ_CD": "IN",
    "ACCT_PD": "IN", "NTEE_CD": "IN", "ACTIVITY": "IN", "CLASSIFICATION": "IN",
    "ORGANIZATION": "IN", "RULING": "MA",  # ruling date change implies re-determination
}
ADDRESS_FIELDS = ("STREET", "CITY", "STATE", "ZIP")


def norm_ein(v: str) -> str:
    digits = re.sub(r"\D", "", v or "")
    return digits.zfill(9) if digits else ""


def norm_val(field: str, v: str) -> str:
    v = (v or "").strip().upper()
    if field in ("SUBSECTION", "FOUNDATION", "DEDUCTIBILITY", "STATUS", "AFFILIATION",
                 "GROUP", "FILING_REQ_CD", "PF_FILING_REQ_CD", "ACCT_PD", "ASSET_CD",
                 "INCOME_CD", "ORGANIZATION"):
        v = v.lstrip("0") or "0"
    if field == "ZIP":
        v = v[:5]
    if field in ("ASSET_AMT", "INCOME_AMT", "REVENUE_AMT"):
        v = v.split(".")[0].lstrip("0") or "0"
    return v


def norm_name(v: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9 ]", "", (v or "").upper())).strip()


def snapshot(rows: Iterable[Mapping[str, str]]) -> Dict[str, Tuple[Tuple[str, str], ...]]:
    fields = tuple(MATERIALITY)
    return {
        norm_ein(r["EIN"]): tuple((f, norm_val(f, r.get(f, ""))) for f in fields)
        for r in rows if norm_ein(r.get("EIN", ""))
    }


def diff(old: Mapping[str, tuple], new: Mapping[str, tuple]) -> dict:
    def is_c3(rec: tuple) -> bool:
        return dict(rec).get("SUBSECTION") == "3"

    added = [e for e in new if e not in old]
    removed = [e for e in old if e not in new]
    per_field = collections.Counter()
    per_class_orgs = collections.Counter()
    c3_per_field = collections.Counter()
    c3_per_class_orgs = collections.Counter()
    changed_orgs = 0
    c3_changed_orgs = 0
    for e in (k for k in new if k in old):
        a, b = dict(old[e]), dict(new[e])
        fields = [f for f in MATERIALITY if a.get(f) != b.get(f)]
        if not fields:
            continue
        changed_orgs += 1
        classes = {MATERIALITY[f] for f in fields}
        top = "MA" if "MA" in classes else ("MN" if "MN" in classes else "IN")
        per_class_orgs[top] += 1
        per_field.update(fields)
        if is_c3(old[e]) or is_c3(new[e]):
            c3_changed_orgs += 1
            c3_per_class_orgs[top] += 1
            c3_per_field.update(fields)
    return {
        "old_rows": len(old), "new_rows": len(new),
        "added": len(added), "removed": len(removed),
        "c3_added": sum(1 for e in added if is_c3(new[e])),
        "c3_removed": sum(1 for e in removed if is_c3(old[e])),
        "changed_orgs": changed_orgs, "changed_orgs_by_top_class": dict(per_class_orgs),
        "c3_changed_orgs": c3_changed_orgs, "c3_changed_orgs_by_top_class": dict(c3_per_class_orgs),
        "c3_field_change_counts": dict(c3_per_field.most_common()),
        "field_change_counts": dict(per_field.most_common()),
    }


def parse_date(s: str):
    try:
        return datetime.datetime.strptime(s.strip(), "%d-%b-%Y").date()
    except ValueError:
        return None


def revocation_rows(lines: Iterable[str]) -> Iterator[Tuple[str, str, object, object, object]]:
    for line in lines:
        p = line.rstrip("\n").split("|")
        if len(p) >= 12:
            yield (p[0], p[8], parse_date(p[9]), parse_date(p[10]), parse_date(p[11]))


def profile_revocations(rows: List[tuple]) -> dict:
    by_month = collections.Counter(r[3].strftime("%Y-%m") for r in rows if r[3])
    by_year = collections.Counter(r[3].year for r in rows if r[3])
    c3_by_year = collections.Counter(r[3].year for r in rows if r[3] and r[1] == "03")
    reinst = [r for r in rows if r[4] and r[2]]
    retro = sum(1 for r in reinst if r[4] <= r[2])
    lags = sorted((r[3] - r[2]).days for r in rows if r[2] and r[3] and r[3].year == 2025)
    pct = lambda xs, q: xs[int(q * (len(xs) - 1))] if xs else None
    eins = collections.Counter(r[0] for r in rows)
    return {
        "rows": len(rows),
        "postings_by_year": dict(sorted(by_year.items())),
        "c3_postings_by_year": dict(sorted(c3_by_year.items())),
        "postings_by_month_2023_on": {k: v for k, v in sorted(by_month.items()) if k >= "2023"},
        "posting_lag_days_2025": {"p10": pct(lags, .1), "p50": pct(lags, .5), "p90": pct(lags, .9)},
        "reinstated_rows": len(reinst),
        "reinstated_retroactive_rows": retro,
        "reinstated_prospective_rows": len(reinst) - retro,
        "eins": len(eins), "eins_with_multiple_rows": sum(1 for v in eins.values() if v > 1),
    }


def profile_bmf(pub78: Mapping[str, str], rows: Iterable[Mapping[str, str]]) -> dict:
    c = collections.Counter()
    names, addrs, groups = collections.Counter(), collections.Counter(), collections.Counter()
    eins = collections.Counter()
    for r in rows:
        ein = norm_ein(r["EIN"])
        eins[ein] += 1
        if norm_val("SUBSECTION", r["SUBSECTION"]) != "3":
            continue
        c["c3"] += 1
        in78 = ein in pub78
        c["c3_not_in_pub78"] += not in78
        if norm_val("AFFILIATION", r["AFFILIATION"]) == "9":
            c["c3_subordinate"] += 1
            c["c3_subordinate_not_in_pub78"] += not in78
        if norm_val("GROUP", r["GROUP"]) != "0":
            groups[norm_val("GROUP", r["GROUP"])] += 1
        if norm_val("FOUNDATION", r["FOUNDATION"]) == "10":
            c["c3_church_fc10"] += 1
            c["c3_church_fc10_not_in_pub78"] += not in78
        names[norm_name(r["NAME"])] += 1
        street = norm_name(r["STREET"])
        if street:
            addrs[(street, (r["ZIP"] or "")[:5])] += 1
    shared_names = [v for v in names.values() if v > 1]
    shared_addrs = [v for v in addrs.values() if v > 1]
    return {
        "rows": sum(eins.values()), "unique_eins": len(eins),
        "eins_on_multiple_rows": sum(1 for v in eins.values() if v > 1),
        **dict(c),
        "c3_group_codes": len(groups), "largest_groups": groups.most_common(5),
        "c3_names_shared": len(shared_names), "c3_orgs_with_shared_name": sum(shared_names),
        "c3_top_shared_names": names.most_common(5),
        "c3_addresses_shared": len(shared_addrs), "c3_orgs_at_shared_address": sum(shared_addrs),
        "c3_addresses_with_10plus_orgs": sum(1 for v in shared_addrs if v >= 10),
        "pub78_rows": len(pub78),
    }


# Human-review workload model for change-driven vetting (06 section 8).
# Each parameter: (low, central, high, evidence class, basis). Rates are per charity unless noted.
REVIEW_PARAMS: Mapping[str, tuple] = {
    "monitored_charities": (60000, 60000, 60000, "ASSUMPTION",
        "120,000 deep reviews/yr at 180 days at 100k accounts (unbound 04-MINIMUM-TOUCH SPW-051 [A])"),
    "grants_per_year": (400000, 400000, 400000, "ASSUMPTION",
        "800,000 approval+release checks/yr = 400,000 grants (SPW-050 [A])"),
    "new_charities_per_year": (10000, 10000, 10000, "ASSUMPTION", "SPW-049 [A]"),
    "revocation_rate_per_year": (0.002, 0.003, 0.005, "INFERENCE",
        "1,505 of 170,569 top-50 recipient EINs revoked during/after FY2023-24 over ~3 years"),
    "share_revocations_needing_human": (0.0, 0.05, 0.15, "ASSUMPTION",
        "revocation is deterministic; human only for successor/name-variance disputes"),
    "adverse_bmf_change_rate_per_month": (0.000054, 0.000054, 0.000244, "VERIFIED-FACT",
        "2026-06->07 BMF diff: ~90 strictly adverse (low/central) to 405 MA-candidate (high) of 1.66m c3 orgs"),
    "share_adverse_bmf_needing_human": (0.1, 0.3, 0.6, "ASSUMPTION",
        "SO-type, PF reclassification and group exit need policy reading; most are deterministic"),
    "sanctions_potential_match_rate_per_charity_year": (0.0005, 0.002, 0.01, "ASSUMPTION",
        "no public false-positive rate; EIN/country-aware matching assumed; ~110-130 SDN update days/yr"),
    "new_charity_human_share": (0.02, 0.05, 0.10, "ASSUMPTION",
        "core exception proxy 7.4% of lines incl. 4.8% recent rulings that are deterministic; entity-type matrix clears churches/subordinates"),
    "renewal_failure_human_share": (0.005, 0.01, 0.03, "ASSUMPTION",
        "renewal after automated evidence gathering; no measured rate"),
    "deep_reviews_per_charity_year": (2.0, 2.0, 2.0, "VERIFIED-FACT", "180-day default, CNV-GRT-003"),
    "identity_dispute_rate_per_charity_year": (0.001, 0.003, 0.01, "ASSUMPTION",
        "charity disputes/corrections reaching a human (SPW-058: 300/yr at 100k accounts [A])"),
}


def review_load(scenario: int, p: Mapping[str, tuple] = REVIEW_PARAMS) -> dict:
    v = {k: t[scenario] for k, t in p.items()}
    g = v["monitored_charities"]
    per_year = {
        "revocation_cases": g * v["revocation_rate_per_year"] * v["share_revocations_needing_human"],
        "adverse_bmf_change_cases": g * v["adverse_bmf_change_rate_per_month"] * 12
                                    * v["share_adverse_bmf_needing_human"],
        "sanctions_potential_matches": g * v["sanctions_potential_match_rate_per_charity_year"],
        "new_charity_cases": v["new_charities_per_year"] * v["new_charity_human_share"],
        "renewal_failures": g * v["deep_reviews_per_charity_year"] * v["renewal_failure_human_share"],
        "identity_disputes": g * v["identity_dispute_rate_per_charity_year"],
    }
    total = sum(per_year.values())
    reviews_conventional = g * v["deep_reviews_per_charity_year"] + v["new_charities_per_year"]
    return {
        "scenario": ("low", "central", "high")[scenario],
        "human_cases_per_year": {k: round(x, 1) for k, x in per_year.items()},
        "total_human_cases_per_year": round(total),
        "per_1000_grants": round(1000 * total / v["grants_per_year"], 2),
        "conventional_review_events_per_year": round(reviews_conventional),
        "share_of_conventional": round(total / reviews_conventional, 4),
    }


def read_csv(path: str) -> Iterator[Mapping[str, str]]:
    with open(path, encoding="latin-1", newline="") as f:
        yield from csv.DictReader(f)


def main(argv: List[str]) -> int:
    cmd, args = argv[1], argv[2:]
    if cmd == "bmf-diff":
        out = diff(snapshot(read_csv(args[0])), snapshot(read_csv(args[1])))
    elif cmd == "revocations":
        with open(args[0], encoding="latin-1") as f:
            out = profile_revocations(list(revocation_rows(f)))
    elif cmd == "bmf-profile":
        with open(args[0], encoding="latin-1") as f:
            pub78 = {norm_ein(l.split("|")[0]): l for l in f if "|" in l}
        rows = (r for p in args[1:] for r in read_csv(p))
        out = profile_bmf(pub78, rows)
    elif cmd == "review-load":
        out = {"params": {k: list(t) for k, t in REVIEW_PARAMS.items()},
               "results": [review_load(i) for i in range(3)]}
    else:
        raise SystemExit(__doc__)
    json.dump(out, sys.stdout, indent=1, default=str)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
