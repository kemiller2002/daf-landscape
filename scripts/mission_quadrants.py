#!/usr/bin/env python3
"""DAF Evidence Quadrant engine (functional style, stdlib only).

Reads data/mission-2026-11-14/quadrant-scores-*.csv (one file per area / scorer) and writes
  data/mission-2026-11-14/quadrant-positions.csv
  research/mission-2026-11-14/quadrants/<area_id>[-<scorer>].svg
See research/mission-2026-11-14/evidence-quadrant-methodology.md for definitions.
Not affiliated with or derived from Gartner's Magic Quadrant.
"""
import csv
import sys
from collections import defaultdict
from html import escape
from pathlib import Path

WEIGHTS = {
    "X": {"X1": 0.25, "X2": 0.20, "X3": 0.15, "X4": 0.20, "X5": 0.10, "X6": 0.10},
    "Y": {"Y1": 0.25, "Y2": 0.25, "Y3": 0.15, "Y4": 0.15, "Y5": 0.20},
}
AREA_NAMES = {
    "A1": "DAF platform & administration",
    "A2": "Grant disbursement & nonprofit-side rails",
    "A3": "Sponsors for the adviser / wealth channel",
    "A4": "Consumer & digital-first sponsors",
    "A5": "Charity eligibility & verification data",
}
VENDOR_CLAIM_CAP = 2.0
MID = 2.0


def read_scores(directory: Path) -> tuple:
    def rows(path):
        with path.open(newline="", encoding="utf-8") as fh:
            return tuple({**r, "_file": path.name} for r in csv.DictReader(fh))
    return tuple(r for p in sorted(directory.glob("quadrant-scores-*.csv")) for r in rows(p))


def parse_score(row: dict):
    raw = (row.get("score") or "").strip().upper()
    if raw in ("", "U"):
        return None
    value = max(0.0, min(4.0, float(raw)))
    capped = row.get("evidence_class", "").strip() == "vendor_claim"
    return min(value, VENDOR_CLAIM_CAP) if capped else value


def criterion_scores(rows) -> dict:
    """(area, scorer, provider) -> {criterion: score or None}; best admissible score per criterion."""
    acc = defaultdict(dict)
    for r in rows:
        key = (r["area_id"].strip(), (r.get("scorer") or "primary").strip(), r["provider"].strip())
        cid = r["criterion_id"].strip().upper()
        s = parse_score(r)
        prev = acc[key].get(cid)
        acc[key][cid] = s if prev is None else (prev if s is None else max(prev, s))
    return dict(acc)


def axis(scores: dict, weights: dict) -> dict:
    scored = {c: scores.get(c) for c in weights if scores.get(c) is not None}
    sw = sum(weights[c] for c in scored)
    point = sum(weights[c] * scored[c] for c in scored) / sw if sw else None
    low = sum(weights[c] * scored.get(c, 0.0) for c in weights)
    high = sum(weights[c] * scored.get(c, 4.0) for c in weights)
    return {"point": point, "low": low, "high": high, "coverage": sw}


def quadrant(x: dict, y: dict) -> str:
    if x["point"] is None or y["point"] is None:
        return "insufficient evidence"
    if x["coverage"] < 0.5 or y["coverage"] < 0.5:
        return "insufficient evidence"
    crosses = (x["low"] < MID < x["high"] and abs(x["point"] - MID) < 0.25) or \
              (y["low"] < MID < y["high"] and abs(y["point"] - MID) < 0.25)
    name = {(True, True): "Proven Leaders", (True, False): "Scale Operators",
            (False, True): "Forward Builders", (False, False): "Focused Specialists"}[(x["point"] >= MID, y["point"] >= MID)]
    return f"{name} (boundary)" if crosses else name


def positions(cscores: dict) -> tuple:
    return tuple(
        {"area_id": a, "scorer": s, "provider": p,
         **{f"x_{k}": (round(v, 2) if isinstance(v, float) else v) for k, v in axis(sc, WEIGHTS["X"]).items()},
         **{f"y_{k}": (round(v, 2) if isinstance(v, float) else v) for k, v in axis(sc, WEIGHTS["Y"]).items()},
         "quadrant": quadrant(axis(sc, WEIGHTS["X"]), axis(sc, WEIGHTS["Y"]))}
        for (a, s, p), sc in sorted(cscores.items())
    )


def svg(area: str, scorer: str, pos: tuple) -> str:
    W, H, M = 720, 720, 70
    sx = lambda v: M + (W - 2 * M) * v / 4
    sy = lambda v: H - M - (H - 2 * M) * v / 4
    css = ("<style>:root{--fg:#1f2328;--muted:#59636e;--grid:#d0d7de;--box:rgba(9,105,218,.12);--dot:#0969da}"
           "@media (prefers-color-scheme: dark){:root{--fg:#e6edf3;--muted:#9198a1;--grid:#3d444d;"
           "--box:rgba(88,166,255,.18);--dot:#58a6ff}}text{fill:var(--fg);font:12px system-ui,sans-serif}"
           ".m{fill:var(--muted)}</style>")
    labels = [("Proven Leaders", 3, 3.85), ("Forward Builders", 1, 3.85), ("Scale Operators", 3, 0.15), ("Focused Specialists", 1, 0.15)]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
             f'aria-label="DAF Evidence Quadrant {escape(area)}">', css,
             f'<rect x="{M}" y="{M}" width="{W-2*M}" height="{H-2*M}" fill="none" stroke="var(--grid)"/>',
             f'<line x1="{sx(MID)}" y1="{M}" x2="{sx(MID)}" y2="{H-M}" stroke="var(--grid)"/>',
             f'<line x1="{M}" y1="{sy(MID)}" x2="{W-M}" y2="{sy(MID)}" stroke="var(--grid)"/>',
             f'<text x="{W/2}" y="30" text-anchor="middle" style="font-weight:600">DAF Evidence Quadrant — '
             f'{escape(AREA_NAMES.get(area, area))} ({escape(scorer)})</text>',
             f'<text x="{W/2}" y="{H-25}" text-anchor="middle" class="m">Evidenced Execution →</text>',
             f'<text x="22" y="{H/2}" text-anchor="middle" class="m" transform="rotate(-90 22 {H/2})">'
             f'Evidenced Forward Capability →</text>']
    parts += [f'<text x="{sx(x)}" y="{sy(y)}" text-anchor="middle" class="m">{t}</text>' for t, x, y in labels]
    for p in pos:
        if p["x_point"] is None or p["y_point"] is None:
            continue
        hollow = "insufficient" in p["quadrant"]
        parts.append(f'<rect x="{sx(p["x_low"])}" y="{sy(p["y_high"])}" width="{sx(p["x_high"])-sx(p["x_low"])}" '
                     f'height="{sy(p["y_low"])-sy(p["y_high"])}" fill="var(--box)"/>')
        parts.append(f'<circle cx="{sx(p["x_point"])}" cy="{sy(p["y_point"])}" r="6" '
                     f'fill="{"none" if hollow else "var(--dot)"}" stroke="var(--dot)" stroke-width="2"/>')
        parts.append(f'<text x="{sx(p["x_point"])+9}" y="{sy(p["y_point"])-8}">{escape(p["provider"])}</text>')
    parts.append(f'<text x="{M}" y="{H-8}" class="m">Boxes = range if unknown criteria scored 0–4; hollow = evidence '
                 f'coverage &lt; 0.5. Not a Gartner Magic Quadrant.</text></svg>')
    return "\n".join(parts)


def write_csv(path: Path, rows: tuple):
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    data = root / "data" / "mission-2026-11-14"
    out_dir = root / "research" / "mission-2026-11-14" / "quadrants"
    pos = positions(criterion_scores(read_scores(data)))
    if not pos:
        sys.exit("no quadrant-scores-*.csv files found")
    write_csv(data / "quadrant-positions.csv", pos)
    out_dir.mkdir(parents=True, exist_ok=True)
    groups = defaultdict(list)
    for p in pos:
        groups[(p["area_id"], p["scorer"])].append(p)
    for (a, s), ps in groups.items():
        (out_dir / f"{a}-{s}.svg").write_text(svg(a, s, tuple(ps)), encoding="utf-8")
    for p in pos:
        print(f'{p["area_id"]} {p["scorer"]:<10} {p["provider"]:<32} X={p["x_point"]} Y={p["y_point"]} '
              f'cov=({p["x_coverage"]},{p["y_coverage"]}) {p["quadrant"]}')
