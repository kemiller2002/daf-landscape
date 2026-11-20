"""P-B43N26-01: validate the in-portal data-provider CSV and print tallies.

Usage: python3 scripts/mission_b43n26_01_in_portal_provider.py .
Pure functions, stdlib only. Prints schema/vocabulary errors and counts by mode.
"""
import csv
import os
import sys
from collections import Counter
from functools import reduce

CSV_REL = "data/mission-2026-11-14/in-portal-data-provider-2026-11-20.csv"
COLUMNS = ["row_id", "sponsor", "sponsor_scope", "portal_vendor", "provider", "integration_mode",
           "evidence_scope", "quote", "source_url", "source_date", "evidence_label", "host_robots",
           "retrieved", "notes"]
MODES = {"embedded", "linked", "eligibility_only", "not_found", "announced", "vendor_claim"}
SCOPES = {"top20", "cf_vendor", "cf_example", "vendor_claim"}
EVIDENCE_SCOPES = {"sponsor_specific", "vendor_level"}
TOP20_TASK = ["National Philanthropic Trust (NPT)", "DAFgiving360 (Schwab Charitable)",
              "Goldman Sachs Philanthropy Fund", "Morgan Stanley GIFT",
              "American Endowment Foundation (AEF)", "National Christian Foundation (NCF)",
              "Jewish Communal Fund (JCF)", "Raymond James Charitable", "The Chicago Community Trust"]
# Order of strength used to pick one in-portal mode per sponsor. Outbound links and vendor
# claims say nothing about the in-portal search, so they do not count as in-portal evidence.
RANK = {"embedded": 3, "eligibility_only": 2, "announced": 1, "not_found": 0}


def read_rows(root):
    with open(os.path.join(root, CSV_REL), encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def row_errors(row):
    checks = [
        (row["integration_mode"] in MODES, "mode"),
        (row["sponsor_scope"] in SCOPES, "sponsor_scope"),
        (row["evidence_scope"] in EVIDENCE_SCOPES, "evidence_scope"),
        (row["integration_mode"] == "not_found" or bool(row["quote"]), "quote missing"),
        (row["integration_mode"] == "not_found" or row["source_url"].startswith("http"), "url"),
    ]
    return list(map(lambda c: f"{row['row_id']}: {c[1]}", filter(lambda c: not c[0], checks)))


def best_mode(rows, sponsor):
    modes = list(filter(lambda m: m in RANK, map(lambda r: r["integration_mode"],
                                                  filter(lambda r: r["sponsor"] == sponsor, rows))))
    return reduce(lambda a, b: b if RANK[b] > RANK[a] else a, modes, "not_found")


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    header, rows = read_rows(root)
    errors = ([] if header == COLUMNS else ["header mismatch"]) + \
        reduce(lambda acc, r: acc + row_errors(r), rows, [])
    ids = list(map(lambda r: r["row_id"], rows))
    errors += [] if len(ids) == len(set(ids)) else ["duplicate row_id"]
    print(f"rows={len(rows)} errors={len(errors)}")
    list(map(print, errors))
    print("rows by integration_mode:", dict(sorted(Counter(map(lambda r: r["integration_mode"], rows)).items())))
    print("rows by evidence_scope:", dict(sorted(Counter(map(lambda r: r["evidence_scope"], rows)).items())))
    per_sponsor = list(map(lambda s: (s, best_mode(rows, s)), TOP20_TASK))
    linked = set(map(lambda r: r["sponsor"], filter(lambda r: r["integration_mode"] == "linked", rows)))
    list(map(lambda p: print(f"  {p[0]}: in-portal={p[1]} outbound_link={'yes' if p[0] in linked else 'no'}"),
             per_sponsor))
    print("named top-20 sponsors by in-portal mode:", dict(sorted(Counter(map(lambda p: p[1], per_sponsor)).items())))
    cf_examples = list(filter(lambda r: r["sponsor_scope"] == "cf_example", rows))
    print("CF examples with in-portal Candid/GuideStar search:",
          sum(map(lambda r: r["integration_mode"] == "embedded", cf_examples)), "of", len(cf_examples))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
