#!/usr/bin/env python3
"""Two-scorer calibration for the DAF Evidence Quadrant (functional style, stdlib only).

Compares scorer="primary" and scorer="blind" for every area that has both, and writes:
  data/mission-2026-11-14/quadrant-calibration-criteria.csv  (criterion-level gaps; flag when |diff| > 1
                                                              or when exactly one scorer used U)
  data/mission-2026-11-14/quadrant-calibration-providers.csv (axis points, quadrant agreement)
Reproduced = same base quadrant (ignoring "(boundary)") and neither scorer "insufficient evidence".
"""
import csv
import importlib.util
import sys
from pathlib import Path


def load_engine(root: Path):
    spec = importlib.util.spec_from_file_location("mq", root / "scripts" / "mission_quadrants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def base(q: str) -> str:
    return q.replace(" (boundary)", "")


def criterion_rows(cs: dict) -> tuple:
    pairs = {(a, p) for (a, s, p) in cs if s == "primary"} & {(a, p) for (a, s, p) in cs if s == "blind"}
    crits = [f"X{i}" for i in range(1, 7)] + [f"Y{i}" for i in range(1, 6)]
    def row(a, p, c):
        sp, sb = cs[(a, "primary", p)].get(c), cs[(a, "blind", p)].get(c)
        diff = None if sp is None or sb is None else round(sb - sp, 2)
        flag = ("one_scorer_unknown" if (sp is None) != (sb is None)
                else "gap_gt_1" if diff is not None and abs(diff) > 1 else "")
        return {"area_id": a, "provider": p, "criterion_id": c,
                "primary": "U" if sp is None else sp, "blind": "U" if sb is None else sb,
                "diff_blind_minus_primary": "" if diff is None else diff, "flag": flag}
    return tuple(row(a, p, c) for a, p in sorted(pairs) for c in crits)


def provider_rows(positions: tuple) -> tuple:
    idx = {(r["area_id"], r["scorer"], r["provider"]): r for r in positions}
    pairs = sorted({(a, p) for (a, s, p) in idx if s == "primary"} & {(a, p) for (a, s, p) in idx if s == "blind"})
    def row(a, p):
        pr, bl = idx[(a, "primary", p)], idx[(a, "blind", p)]
        insufficient = "insufficient" in pr["quadrant"] or "insufficient" in bl["quadrant"]
        same = base(pr["quadrant"]) == base(bl["quadrant"])
        return {"area_id": a, "provider": p,
                "primary_x": pr["x_point"], "blind_x": bl["x_point"],
                "primary_y": pr["y_point"], "blind_y": bl["y_point"],
                "primary_quadrant": pr["quadrant"], "blind_quadrant": bl["quadrant"],
                "status": "insufficient evidence" if insufficient else ("reproduced" if same else "disputed")}
    return tuple(row(a, p) for a, p in pairs)


def write(path: Path, rows: tuple):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    mq = load_engine(root)
    data = root / "data" / "mission-2026-11-14"
    cs = mq.criterion_scores(mq.read_scores(data))
    crit = criterion_rows(cs)
    prov = provider_rows(mq.positions(cs))
    write(data / "quadrant-calibration-criteria.csv", crit)
    write(data / "quadrant-calibration-providers.csv", prov)
    flagged = [r for r in crit if r["flag"]]
    print(f"criterion pairs: {len(crit)}; flagged: {len(flagged)} "
          f"(gap>1: {sum(r['flag']=='gap_gt_1' for r in crit)}, one-U: {sum(r['flag']=='one_scorer_unknown' for r in crit)})")
    for r in prov:
        print(f'{r["area_id"]} {r["provider"][:40]:<40} {r["primary_quadrant"]:<32} | {r["blind_quadrant"]:<32} -> {r["status"]}')
