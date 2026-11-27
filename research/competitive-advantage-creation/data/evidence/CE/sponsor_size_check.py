"""Agent CE scratch check (not a durable model): how many DAF sponsors are large
enough to pay the revenue per customer that Sequence A3 assumes?

Input: data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv (SRC-013,
corrected DAFRC FY2021-24 sponsor panel). Run from the repository root:

    python3 -I research/competitive-advantage-creation/data/evidence/CE/sponsor_size_check.py

Thresholds: accounts needed for a given net revenue per customer at a headline
price per account after a 30% channel share (Phase II ER-7 basis, P3-ASM-AB030:
$150k / $300k / $600k net at $81). Output is written next to this script.
"""
import csv
import os
from collections import Counter, defaultdict

PANEL = "data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sponsor-size-check.csv")
SHARE = 0.30


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def accounts_needed(net_revenue, price):
    return net_revenue / (price * (1 - SHARE))


rows = list(csv.DictReader(open(PANEL, newline="", encoding="utf-8")))
out = []
for price in (81, 120, 150):
    for net in (150_000, 300_000, 600_000):
        thr = accounts_needed(net, price)
        sel = [r for r in rows if num(r["daf_accounts_fy2024"]) >= thr]
        cats = Counter(r["sponsor_category"] for r in sel)
        out.append({
            "headline_price_per_account": price,
            "net_revenue_per_customer": net,
            "accounts_needed": round(thr),
            "sponsors_at_or_above": len(sel),
            "national_standard": cats.get("national_standard", 0),
            "donation_processor": cats.get("donation_processor", 0),
            "religious": cats.get("religious", 0),
            "community_foundation": cats.get("community_foundation", 0),
            "university_or_hospital": cats.get("university_or_hospital", 0),
            "single_issue_other": cats.get("single_issue_other", 0),
        })

totals = defaultdict(lambda: [0, 0.0])
for r in rows:
    t = totals[r["sponsor_category"]]
    t[0] += 1
    t[1] += num(r["daf_accounts_fy2024"])
for cat, (n, a) in sorted(totals.items()):
    out.append({
        "headline_price_per_account": "segment total",
        "net_revenue_per_customer": "",
        "accounts_needed": "",
        "sponsors_at_or_above": n,
        cat: round(a),
    })

fields = list(out[0].keys())
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", restval="")
    w.writeheader()
    for row in out:
        w.writerow(row)
print(open(OUT, encoding="utf-8").read())
