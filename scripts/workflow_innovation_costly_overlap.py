#!/usr/bin/env python3
"""Does COSTLY verification recur across sponsors? (workflow-innovation ranking-5 experiment 3; audit objection to INN-02)

Uses the FY2023 top-50 sponsor x recipient edges (data/workflow-innovation/sponsor-recipient-edges-fy2023.csv) and two
repository lists of recipients that need human work rather than a free IRS/OFAC lookup:
  - fiscal sponsors (data/mission-2026-11-14/fiscal-sponsor-ein-list-2026-11-19.csv, 433 EINs; review of the hosted project)
  - recipients absent from the IRS EO BMF (data/mission-2026-11-14/non-bmf-recipients-2026-11-20.csv; identity/status must be resolved by a person)
Foreign recipients cannot be tested: Schedule F Part II reports regions, not recipient names.
Metrics per class: recipients, sponsor-recipient pairs, share of recipients with >=2 top-50 funders, and the share of pair-level
verifications a shared record would avoid (1 - distinct recipients / pairs). Stdlib; pure transforms; I/O at the edges.
"""
import csv, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDGES = os.path.join(ROOT, "data/workflow-innovation/sponsor-recipient-edges-fy2023.csv")
FS = os.path.join(ROOT, "data/mission-2026-11-14/fiscal-sponsor-ein-list-2026-11-19.csv")
NB = os.path.join(ROOT, "data/mission-2026-11-14/non-bmf-recipients-2026-11-20.csv")
OUT = os.path.join(ROOT, "data/workflow-innovation/costly-recipient-overlap.csv")

def ein9(x): 
    d = "".join(c for c in (x or "") if c.isdigit())
    return d.zfill(9) if d else ""

def read(path): 
    with open(path, newline="") as f: return list(csv.DictReader(f))

def metrics(name, edges, keys):
    sel = [e for e in edges if keys is None or e["recipient_key"] in keys]
    by = {}
    for e in sel: by.setdefault(e["recipient_key"], set()).add(e["sponsor_ein"])
    pairs = sum(len(v) for v in by.values())
    multi = sum(1 for v in by.values() if len(v) >= 2)
    usd = sum(float(e["amount_usd"]) for e in sel)
    return {"class": name, "recipients": len(by), "pairs": pairs, "lines": sum(int(e["lines"]) for e in sel), "amount_usd": round(usd),
            "share_recipients_ge2_sponsors": round(multi / len(by), 4) if by else 0,
            "share_pair_verifications_avoided": round(1 - len(by) / pairs, 4) if pairs else 0}

def main():
    edges = read(EDGES)
    fs = {ein9(r["ein"]) for r in read(FS) if ein9(r["ein"])}
    nb = {ein9(r["ein"]) for r in read(NB) if r.get("row_type") not in ("aggregate",) and ein9(r.get("ein", ""))}
    rows = [metrics("all recipients", edges, None), metrics("fiscal sponsors (433-EIN list)", edges, fs),
            metrics("recipients absent from IRS EO BMF", edges, nb)]
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(rows)
    for r in rows: print(r)

if __name__ == "__main__":
    sys.exit(main())
