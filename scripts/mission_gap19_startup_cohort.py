#!/usr/bin/env python3
"""DAF startup cohort 2021-2026: denominator for the failed-startup study (P-GAP19-15).

Stdlib only, functional style: pure functions over immutable rows; I/O at the edges.

Inputs (data/mission-2026-11-14/)
  daf-startup-cohort-2021-2026.csv   curated cohort (in_cohort=yes) plus screened-out rows
  sponsor-entry-exit-panel.csv       DAFRC EIN x FY panel (Frame A source)
  sponsor-mortality-summary.csv      verified sponsor exit rates (base-rate comparator)
  failed-daf-startups.csv            purposive-50 case file (comparison)

What it does
  1. Re-derives Frame A (filing frame) from the panel with the pre-registered rule and
     checks it against the cohort file (every rule hit is either in the cohort or screened out
     with a reason; every Frame A cohort row is a rule hit).
  2. Counts outcomes and reports survival proportions with Wilson 95% intervals, the
     unknown-status bounds, company-years of exposure and a rule-of-three hazard bound.
  3. Compares the cohort with the DAFRC verified sponsor exit rate and with the purposive-50.
  4. Cross-tabulates status by channel, funding and strict-window subset.

Output: Markdown tables on stdout (pasted into
research/mission-2026-11-14/gap19-startup-cohort.md). Writes no files.

Usage: python3 scripts/mission_gap19_startup_cohort.py
"""
from __future__ import annotations

import csv
import math
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "mission-2026-11-14"
AS_OF = date(2026, 11, 19)
STATUSES = ("active", "acquired", "pivoted", "shut", "unknown")


# ---------- I/O edges ----------
def load_csv(path: Path) -> tuple[dict, ...]:
    with path.open(newline="", encoding="utf-8") as f:
        return tuple(csv.DictReader(f))


# ---------- pure helpers ----------
def digits(ein: str) -> str:
    return re.sub(r"\D", "", ein or "").zfill(9) if ein else ""


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def fmt_prop(k: int, n: int) -> str:
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {pct(k / n)} (95% Wilson {pct(lo)}-{pct(hi)})" if n else "n/a"


def entry_year_month(entry_date: str) -> tuple[int, int] | None:
    m = re.search(r"(20\d\d)(?:-(\d\d))?", entry_date or "")
    return (int(m.group(1)), int(m.group(2) or 7)) if m else None  # mid-year if month unknown


def exposure_years(entry_date: str, as_of: date = AS_OF) -> float:
    ym = entry_year_month(entry_date)
    if ym is None:
        return 0.0
    y, mth = ym
    return max(0.0, (as_of.year - y) + (as_of.month - mth) / 12)


# ---------- Frame A rule (pre-registered) ----------
def panel_by_ein(panel: tuple[dict, ...]) -> dict[str, tuple[dict, ...]]:
    out: dict[str, list] = {}
    for r in panel:
        out.setdefault(r["ein"], []).append(r)
    return {k: tuple(sorted(v, key=lambda r: int(r["fiscal_year"]))) for k, v in out.items()}


def frame_a_hit(rows: tuple[dict, ...]) -> bool:
    first = rows[0]
    ruling = first["sponsor_irs_ruling"]
    if not ruling or int(ruling) < 202101:
        return False
    filed_accounts = [int(r["number_of_daf_accounts"] or 0) for r in rows if r["source_eoy_daf_assets"] != "Imputed"]
    max_acc = max(filed_accounts or [0])
    return first["type"] == "National" or (first["subtype"] == "Other" and max_acc >= 50)


def frame_a(panel: tuple[dict, ...]) -> dict[str, dict]:
    return {ein: rows[0] for ein, rows in panel_by_ein(panel).items() if frame_a_hit(rows)}


def frame_a_check(cohort: tuple[dict, ...], hits: dict[str, dict]) -> list[str]:
    eins = {digits(e): r for r in cohort for e in r["ein"].split(";") if digits(e)}
    problems = [f"rule hit {e} {h['name']} not in cohort file" for e, h in hits.items() if e not in eins]
    problems += [
        f"cohort row {r['cohort_id']} claims Frame A but EIN {r['ein']} is not a rule hit"
        for r in cohort
        if r["in_cohort"] == "yes" and "A" in r["frames"].split(";") and digits(r["ein"]) not in hits
    ]
    return problems


# ---------- survival ----------
def members(cohort: tuple[dict, ...]) -> tuple[dict, ...]:
    return tuple(r for r in cohort if r["in_cohort"] == "yes")


def status_counts(rows: tuple[dict, ...]) -> Counter:
    return Counter(r["status"] for r in rows)


def survival_table(rows: tuple[dict, ...]) -> list[tuple[str, str]]:
    c = status_counts(rows)
    n = len(rows)
    unknown = c["unknown"]
    resolved = n - unknown
    operating = c["active"] + c["pivoted"] + c["acquired"]  # product or company continues
    independent = c["active"] + c["pivoted"]
    yrs = sum(exposure_years(r["entry_date"]) for r in rows)
    return [
        ("Cohort size", str(n)),
        ("Status counts", ", ".join(f"{s} {c[s]}" for s in STATUSES)),
        ("Not shut, among resolved (excludes unknown)", fmt_prop(resolved - c["shut"], resolved)),
        ("Operating in any form, unknown counted as failed (lower bound)", fmt_prop(operating, n)),
        ("Operating in any form, unknown counted as surviving (upper bound)", fmt_prop(n - c["shut"], n)),
        ("Independent and operating (active + pivoted) / all", fmt_prop(independent, n)),
        ("Active with dated evidence <=12 months / all", fmt_prop(c["active"], n)),
        ("Exit by acquisition / all", fmt_prop(c["acquired"], n)),
        ("Status unknown / all", fmt_prop(unknown, n)),
        ("Company-years of exposure (entry to 2026-11-19)", f"{yrs:.1f}"),
        ("Observed shutdowns per company-year", f"{c['shut']}/{yrs:.1f}"),
        ("Rule-of-three 95% upper bound on annual shutdown hazard (if 0 shut)",
         pct(3 / yrs) if c["shut"] == 0 and yrs else "n/a"),
        ("Crude annual shutdown rate if every unknown were a shutdown (point estimate)", pct((c['shut'] + unknown) / yrs) if yrs else "n/a"),
    ]


def filing_survival(rows: tuple[dict, ...]) -> list[tuple[str, str]]:
    a = tuple(r for r in rows if "A" in r["frames"].split(";"))
    filed24 = sum(1 for r in a if r["last_990_period_propublica"] == "202412")
    no_exit = sum(1 for r in a if r["dafrc_exit_flag"] == "none")
    return [
        ("Frame A sponsors (filing frame)", str(len(a))),
        ("No DAFRC exit flag through FY2024", fmt_prop(no_exit, len(a))),
        ("Tax-period 2024-12 return listed on ProPublica", fmt_prop(filed24, len(a))),
    ]


def base_rate_comparison(rows: tuple[dict, ...], summary: tuple[dict, ...]) -> list[tuple[str, str]]:
    a = tuple(r for r in rows if "A" in r["frames"].split(";"))
    # sponsor-years at risk inside the DAFRC panel window (entry FY to FY2024)
    years = sum(max(0, 2024 - (entry_year_month(r["entry_date"]) or (2024, 1))[0]) for r in a)
    rates = {
        r["group"]: float(r["value"])
        for r in summary
        if r["dimension"] == "verified" and r["measure"] == "annual_exit_rate_count"
    }
    out = [("Frame A sponsor-years at risk, entry year to FY2024", str(years))]
    for g in ("lower_A_org_ceased_or_converted", "central_A_plus_B_no_dafs_reported", "upper_A_B_plus_C_unresolved"):
        if g in rates:
            exp = rates[g] * years
            out.append((f"Expected exits at DAFRC verified rate {g} ({pct(rates[g])}/yr)",
                        f"{exp:.2f} (P(0 exits) = {math.exp(-exp):.2f})"))
    out.append(("Observed Frame A exits", str(sum(1 for r in a if r["dafrc_exit_flag"] not in ("none", "n/a", "")))))
    return out


def crosstab(rows: tuple[dict, ...], key) -> list[tuple[str, int, int, int]]:
    groups: dict[str, list] = {}
    for r in rows:
        groups.setdefault(key(r), []).append(r)
    return sorted(
        ((g, len(v), sum(1 for r in v if r["status"] == "active"), sum(1 for r in v if r["status"] != "active"))
         for g, v in groups.items()),
        key=lambda t: (-t[1], t[0]),
    )


def channel_key(r: dict) -> str:
    ch = r["channel"].lower()
    if "b2c at launch" in ch:
        return "B2C then B2B (pivot)"
    if ch.startswith("b2c") or "community" in ch:
        return "B2C / community"
    if "embedded" in ch:
        return "embedded in another consumer app"
    return "B2B (employer, nonprofit, bank, platform)"


def venture_key(r: dict) -> str:
    v = r["venture_backed"].lower()
    return "venture or angel backed" if v.startswith("yes") else ("not venture" if v.startswith("no") else "funding unknown")


def strict_key(r: dict) -> str:
    return {"yes": "company founded in window", "no": "parent/company predates window"}.get(r["strict_window_subset"], "founding date unknown")


def purposive_counts(fifty: tuple[dict, ...]) -> Counter:
    return Counter(r["outcome_group"] for r in fifty)


# ---------- rendering ----------
def md_kv(title: str, rows: list[tuple[str, str]]) -> str:
    return "\n".join([f"**{title}**", "", "| Measure | Value |", "|---|---|"] + [f"| {k} | {v} |" for k, v in rows]) + "\n"


def md_xtab(title: str, rows: list[tuple[str, int, int, int]]) -> str:
    lines = [f"**{title}**", "", "| Group | n | active | not active (acquired, pivoted, shut, unknown) |", "|---|---|---|---|"]
    return "\n".join(lines + [f"| {g} | {n} | {a} | {na} |" for g, n, a, na in rows]) + "\n"


def main() -> None:
    cohort = load_csv(DATA / "daf-startup-cohort-2021-2026.csv")
    panel = load_csv(DATA / "sponsor-entry-exit-panel.csv")
    summary = load_csv(DATA / "sponsor-mortality-summary.csv")
    fifty = load_csv(DATA / "failed-daf-startups.csv")

    hits = frame_a(panel)
    problems = frame_a_check(cohort, hits)
    m = members(cohort)
    strict = tuple(r for r in m if r["strict_window_subset"] == "yes")

    print(f"Frame A rule hits: {len(hits)} -> " + "; ".join(sorted(h['name'] for h in hits.values())))
    print("Frame A consistency: " + ("OK" if not problems else " | ".join(problems)) + "\n")
    print(md_kv("Survival, full cohort", survival_table(m)))
    print(md_kv("Survival, strict subset (company founded 2021 or later)", survival_table(strict)))
    print(md_kv("Filing survival, Frame A sponsors", filing_survival(m)))
    print(md_kv("Frame A against the DAFRC verified sponsor exit rate", base_rate_comparison(m, summary)))
    print(md_xtab("Status by distribution channel", crosstab(m, channel_key)))
    print(md_xtab("Status by funding", crosstab(m, venture_key)))
    print(md_xtab("Status by founding window", crosstab(m, strict_key)))
    pc = purposive_counts(fifty)
    print(md_kv("Purposive-50 outcome groups (failed-daf-startups.csv)", [(k, str(v)) for k, v in pc.most_common()]))
    print(md_kv("Screened out", [(r["entity_name"], r["exclusion_reason"]) for r in cohort if r["in_cohort"] == "no"]))


if __name__ == "__main__":
    main()
