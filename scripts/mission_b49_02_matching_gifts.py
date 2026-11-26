"""b49-02: tally corporate matching-gift treatment of DAF grants.

Reads data/mission-2026-11-14/matching-gifts-dafs-2026-11-20.csv and prints the
counts and shares used in research/mission-2026-11-14/b49-02-matching-gifts-dafs.md.

Usage: python3 scripts/mission_b49_02_matching_gifts.py .

Functional style, stdlib only, no network.
"""
import csv
import sys
from collections import Counter
from functools import reduce

CSV_REL = "data/mission-2026-11-14/matching-gifts-dafs-2026-11-20.csv"
ELIGIBLE = ("eligible", "eligible_conditional")
ORDER = ("eligible", "eligible_conditional", "excluded", "silent", "no_public_text")


def load(root):
    with open(f"{root}/{CSV_REL}", newline="") as fh:
        return tuple(csv.DictReader(fh))


def companies(rows):
    return tuple(r for r in rows if r["record_type"] == "frame_company")


def sample(rows):
    return tuple(r for r in companies(rows) if r["in_sample"] == "1")


def recent_only(r):
    """Evidence dated 2021+ only: older text is treated as not found."""
    return r["daf_grant_policy"] if r["recency_ok_2021plus"] == "1" or r["daf_grant_policy"] == "no_public_text" else "no_public_text"


def bofa_as_excluded(r):
    return "excluded" if r["entity"] == "Bank of America" else r["daf_grant_policy"]


def collapse(policy):
    return "eligible_any" if policy in ELIGIBLE else policy


def share_table(label, policies, denom_filter=lambda p: True):
    kept = tuple(p for p in policies if denom_filter(p))
    counts = Counter(map(collapse, kept))
    n = len(kept)
    keys = ("eligible_any", "excluded", "silent", "no_public_text")
    lines = [f"  {k:16s} {counts.get(k, 0):3d}  {100.0 * counts.get(k, 0) / n:5.1f}%" for k in keys if k in counts or k != "no_public_text"]
    return "\n".join([f"{label} (n={n})"] + lines)


def detail_counts(policies):
    c = Counter(policies)
    return ", ".join(f"{k}={c.get(k, 0)}" for k in ORDER)


def by_recency(rows, policy_set):
    hits = tuple(r for r in rows if collapse(r["daf_grant_policy"]) == policy_set)
    c = Counter(r["recency_ok_2021plus"] for r in hits)
    return f"{policy_set}: {len(hits)} total; dated 2021+ = {c.get('1', 0)}; pre-2021 or undated = {c.get('0', 0)}"


def report(rows):
    comp = companies(rows)
    smp = sample(rows)
    dtd = Counter((r["dtd_status"], r["dtd_matching_eligible"]) for r in comp)
    policies = tuple(r["daf_grant_policy"] for r in smp)
    with_text = lambda p: p != "no_public_text"
    sections = [
        f"Frame: {len(comp)} companies (Fortune 500 2025 ranks 1-100)",
        f"DtD screen: found+Yes={dtd.get(('found', 'Yes'), 0)}, found+No={dtd.get(('found', 'No'), 0)}, not_found={dtd.get(('not_found', ''), 0)}",
        f"Sample (DtD 'Matching gift eligible? Yes'): {len(smp)}",
        f"DtD company summaries mentioning DAFs in sample: {sum(r['dtd_summary_mentions_daf'] == '1' for r in smp)}",
        f"Public text found: {sum(r['public_text_found'] == '1' for r in smp)}; of which dated 2021+: {sum(r['recency_ok_2021plus'] == '1' for r in smp)}",
        "Detail (all dates): " + detail_counts(policies),
        share_table("A. All sample, best public evidence of any date", policies),
        share_table("B. Sample companies with a readable public text, any date", policies, with_text),
        share_table("C. All sample, 2021+ evidence only", tuple(map(recent_only, smp))),
        share_table("D. Sample with readable 2021+ text", tuple(map(recent_only, smp)), with_text),
        share_table("E. Sensitivity: B with Bank of America coded excluded", tuple(map(bofa_as_excluded, smp)), with_text),
        "Recency split:\n  " + "\n  ".join(by_recency(smp, k) for k in ("eligible_any", "excluded", "silent")),
        "Gifts INTO a DAF (sample): " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(r["gift_into_daf_policy"] for r in smp).items())),
        "Source types (sample with text): " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(r["source_type"] for r in smp if r["public_text_found"] == "1").items())),
        "Bounds on share of sample where a DAF grant can be matched:\n"
        + f"  documented eligible / sample = {sum(p in ELIGIBLE for p in policies)}/{len(smp)} = {100.0 * sum(p in ELIGIBLE for p in policies) / len(smp):.1f}% (floor)\n"
        + f"  not documented excluded / sample = {len(smp) - policies.count('excluded')}/{len(smp)} = {100.0 * (len(smp) - policies.count('excluded')) / len(smp):.1f}% (ceiling)",
        "Sponsors: " + "; ".join(f"{r['entity']}={r['daf_grant_policy']}" for r in rows if r["record_type"] == "daf_sponsor"),
    ]
    return "\n\n".join(sections)


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(report(load(root)))
