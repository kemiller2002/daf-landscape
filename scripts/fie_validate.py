#!/usr/bin/env python3
"""Quality gates and renderer for research/file-ingestion-and-straight-through-processing (2026-11-26).

Every gate is a pure function returning a tuple of issue strings; main() is the only function with effects.

Gates:
  F1  evidence ids unique and well formed (FIE-[ABC]-nnn); classification in {confirmed, inferred, proposed};
      every evidence row has a source
  F2  source register: ids unique; every evidence source appears in it; every source cites existing evidence
  F3  workflow inventory: ids unique (FIW-*), numeric drivers parse, controlled vocabularies, evidence ids resolve,
      'confirmed' practice has at least one confirmed evidence row
  F4  no product contamination: industry data and chapters contain no Unbound requirement ids or product names
  F5  every FIE-* id cited in the package's Markdown resolves
  F6  economics outputs are current (scripts/fie_economics.py --check) and every parameter is labelled
  F7  generated Markdown sections are current (only with --check)

Usage:
  python3 -I -B scripts/fie_validate.py            validate + rewrite generated sections
  python3 -I -B scripts/fie_validate.py --check    validate + fail if generated sections are stale
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence, Tuple

PKG = Path("research/file-ingestion-and-straight-through-processing")
DATA = Path("data/file-ingestion-2026-11")
EVIDENCE, SOURCES, INVENTORY = DATA / "evidence.csv", DATA / "sources.csv", DATA / "workflow-inventory.csv"
FORMATS, PARAMETERS = DATA / "formats.csv", DATA / "economics-parameters.csv"
RESULTS, ONBOARDING = DATA / "economics-results.csv", DATA / "economics-onboarding.csv"

Row = Mapping[str, str]
Issues = Tuple[str, ...]

FIE = re.compile(r"\bFIE-[ABC]-\d{3}\b")
FIW = re.compile(r"^FIW-[A-Z]{2,3}-\d{2}$")
CONTAMINATION = re.compile(r"\bUnbound\b|\bUNB-[A-Z]+-|\bCNV-[A-Z]+-\d|\bFIL-OD-")
CLASSIFICATIONS = ("confirmed", "inferred", "proposed")
DISPOSITIONS = ("keep", "redesign", "eliminate-file", "challenge", "defer", "merge")
LEVELS = ("high", "medium", "low")
BASES = ("measured", "sourced", "assumed", "scenario", "decision")


def read_csv(path: Path) -> Tuple[Row, ...]:
    with path.open(newline="", encoding="utf-8") as f:
        return tuple(csv.DictReader(f))


def dupes(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(sorted(v for v, n in Counter(values).items() if n > 1))


def f1(evidence: Sequence[Row]) -> Issues:
    ids = [e["evidence_id"] for e in evidence]
    return (tuple(f"F1 duplicate evidence id {i}" for i in dupes(ids))
            + tuple(f"F1 malformed id {i}" for i in ids if not FIE.fullmatch(i))
            + tuple(f"F1 {e['evidence_id']} classification '{e['classification']}'" for e in evidence if e["classification"] not in CLASSIFICATIONS)
            + tuple(f"F1 {e['evidence_id']} has no source" for e in evidence if not e["source"].strip()))


def split(value: str) -> Tuple[str, ...]:
    return tuple(s.strip() for s in value.split(";") if s.strip())


def f2(evidence: Sequence[Row], sources: Sequence[Row]) -> Issues:
    registered = {s["source"] for s in sources}
    ev_ids = {e["evidence_id"] for e in evidence}
    return (tuple(f"F2 duplicate source id {i}" for i in dupes(s["source_id"] for s in sources))
            + tuple(f"F2 {e['evidence_id']} source not registered: {u}" for e in evidence for u in split(e["source"]) if u not in registered)
            + tuple(f"F2 {s['source_id']} cites unknown evidence {i}" for s in sources for i in split(s["evidence_ids"]) if i not in ev_ids))


def number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def f3(inventory: Sequence[Row], evidence: Sequence[Row]) -> Issues:
    by_id = {e["evidence_id"]: e for e in evidence}
    numeric = ("files_per_year_fixed", "files_per_fund_per_year", "records_per_fund_per_year",
               "conventional_minutes_per_record", "conventional_minutes_per_file", "human_decision_floor")
    def row_issues(w: Row) -> Issues:
        wid, refs = w["workflow_id"], split(w["evidence_ids"])
        return (tuple(f"F3 {wid} malformed id" for _ in [0] if not FIW.fullmatch(wid))
                + tuple(f"F3 {wid} {k} not numeric" for k in numeric if not number(w[k]))
                + tuple(f"F3 {wid} disposition '{w['redesign_disposition']}'" for _ in [0] if w["redesign_disposition"] not in DISPOSITIONS)
                + tuple(f"F3 {wid} automation '{w['automation_potential']}'" for _ in [0] if w["automation_potential"] not in LEVELS)
                + tuple(f"F3 {wid} unknown evidence {r}" for r in refs if r not in by_id)
                + tuple(f"F3 {wid} confirmed without confirmed evidence" for _ in [0]
                        if w["practice_classification"] == "confirmed" and not any(by_id.get(r, {}).get("classification") == "confirmed" for r in refs)))
    return tuple(f"F3 duplicate workflow {i}" for i in dupes(w["workflow_id"] for w in inventory)) + tuple(i for w in inventory for i in row_issues(w))


def f4(texts: Mapping[str, str]) -> Issues:
    """Product names and requirement ids may appear only inside cross-repository URLs, never as research content."""
    without_links = lambda t: re.sub(r"https://github\.com/kemiller2002/\S+", "", t)
    return tuple(f"F4 product-specific reference in {name}: '{m.group(0)}'" for name, text in texts.items()
                 for m in CONTAMINATION.finditer(without_links(text)))


def f5(markdown: Mapping[str, str], evidence: Sequence[Row]) -> Issues:
    ids = {e["evidence_id"] for e in evidence}
    ranges = re.compile(r"FIE-([ABC])-(\d{3})\.\.(\d{3})")
    def cited(text: str) -> Iterable[str]:
        expanded = [f"FIE-{a}-{n:03d}" for a, lo, hi in ranges.findall(text) for n in range(int(lo), int(hi) + 1)]
        return list(FIE.findall(text)) + expanded
    return tuple(sorted({f"F5 {name} cites unknown {i}" for name, text in markdown.items() for i in cited(text) if i not in ids}))


def f6(parameters: Sequence[Row], economics_current: bool) -> Issues:
    return (tuple(f"F6 parameter {p['parameter']} basis '{p['basis']}' must start with one of {BASES}" for p in parameters
                  if not p["basis"].startswith(BASES))
            + tuple(f"F6 parameter {p['parameter']} has no source" for p in parameters if not p["source"].strip())
            + (() if economics_current else ("F6 economics outputs are stale: run scripts/fie_economics.py",)))


# ---------------------------------------------------------------------------------------------------------------
# Rendering (pure)

def table(header: Sequence[str], rows: Iterable[Sequence[object]]) -> str:
    cell = lambda v: str(v).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return "\n".join(lines + ["| " + " | ".join(cell(v) for v in r) + " |" for r in rows])


def dispositions(inventory: Sequence[Row]) -> str:
    return table(("Disposition", "Workflows"), sorted(Counter(w["redesign_disposition"] for w in inventory).items(), key=lambda kv: -kv[1]))


def inventory_section(inventory: Sequence[Row]) -> str:
    domains = sorted({w["domain"] for w in inventory})
    summary = table(("Domain", "Workflows", "High automation", "Confirmed practice", "Eliminate-file"),
                    [(d, sum(1 for w in inventory if w["domain"] == d),
                      sum(1 for w in inventory if w["domain"] == d and w["automation_potential"] == "high"),
                      sum(1 for w in inventory if w["domain"] == d and w["practice_classification"] == "confirmed"),
                      sum(1 for w in inventory if w["domain"] == d and w["redesign_disposition"] == "eliminate-file")) for d in domains]
                    + [("total", len(inventory), sum(w["automation_potential"] == "high" for w in inventory),
                        sum(w["practice_classification"] == "confirmed" for w in inventory),
                        sum(w["redesign_disposition"] == "eliminate-file" for w in inventory))])
    detail = table(("ID", "Information", "Supplier", "Delivery", "Format", "Class", "Automation", "AI", "Residual human role", "Redesign", "Practice", "Evidence"),
                   [(w["workflow_id"], w["information"], w["supplier"], w["delivery_mechanism"], w["format"], w["artifact_class"],
                     w["automation_potential"], w["ai_applicability"], w["residual_human_role"],
                     f"{w['redesign_disposition']}: {w['redesign_option']}", w["practice_classification"], w["evidence_ids"].replace(";", "; "))
                    for w in inventory])
    return summary + "\n\n" + detail


def money(v: str) -> str:
    return f"${float(v):,.0f}"


def economics_section(results: Sequence[Row], onboarding: Sequence[Row]) -> str:
    def pick(case: str, prevention: str = "none") -> list:
        return [r for r in results if r["case"] == case and r["prevention"] == prevention]
    def grid(rows: Sequence[Row], metric: str, fmt: Callable[[str], str]) -> str:
        funds = sorted({int(r["funds"]) for r in rows})
        rates = sorted({float(r["stp_rate"]) for r in rows})
        val = {(int(r["funds"]), float(r["stp_rate"])): r[metric] for r in rows}
        return table(["Funds"] + [f"STP {int(s * 100)}%" for s in rates], [[f"{n:,}"] + [fmt(val[(n, s)]) for s in rates] for n in funds])
    pct = lambda v: f"{float(v) * 100:.1f}%"
    usd = lambda v: f"${float(v):,.2f}"
    at90 = lambda case, prevention="none": {r["funds"]: r for r in pick(case, prevention) if r["stp_rate"] == "0.9"}
    funds = sorted({r["funds"] for r in results}, key=int)
    balance = table(("Funds", "Case", "Prevention", "$50k book", "$150k book", "$300k book", "Standalone at $150k", "Dashboard STP"),
                    [(f"{int(n):,}", c, v, pct(at90(c, v)[n]["pooled_share_of_20bps_at_50k"]), pct(at90(c, v)[n]["pooled_share_of_20bps_at_150k"]),
                      pct(at90(c, v)[n]["pooled_share_of_20bps_at_300k"]), pct(at90(c, v)[n]["standalone_share_of_20bps_at_150k"]),
                      pct(at90(c, v)[n]["dashboard_stp"]))
                     for c in ("low", "mode", "high") for v in ("none", "scenario") for n in funds if n in ("1000", "10000", "100000", "1000000")])
    conv = table(("Funds", "Conventional FTE (low / mode / high)", "Residual FTE at 90% routine STP (low / mode / high)"),
                 [(f"{int(n):,}", " / ".join(at90(c)[n]["conventional_fte"] for c in ("low", "mode", "high")),
                   " / ".join(at90(c)[n]["residual_fte"] for c in ("low", "mode", "high"))) for n in funds])
    onb = table(("Case", "Bespoke (days / cost)", "New mapping on shared infrastructure", "Reuse of an existing mapping", "Shadow run (business days elapsed)"),
                [(o["case"], f"{float(o['bespoke_days']):g} / {money(o['bespoke_usd'])}", f"{float(o['new_profile_days']):g} / {money(o['new_profile_usd'])}",
                  f"{float(o['reused_profile_days']):g} / {money(o['reused_profile_usd'])}", f"{float(o['shadow_run_days_elapsed']):g}") for o in onboarding])
    return "\n\n".join([
        "**A. Share of 20 bps servicing revenue consumed by ingestion, at 90% routine STP, by book balance** (pooled = multi-tenant operator reusing mappings; standalone = sponsor alone with bespoke integrations and a 0.5–1 FTE staffing floor)", balance,
        "**B. Pooled ingestion cost per fund per year, mode case, no prevention**", grid(pick("mode"), "pooled_cost_per_fund_usd", usd),
        "**C. Same, mode case with the prevention scenario (50% of investigations prevented at $1 per fund)**", grid(pick("mode", "scenario"), "pooled_cost_per_fund_usd", usd),
        "**D. Dashboard-definition STP (units with no human action ÷ all units), mode case, no prevention** — the model's routine STP rate excludes investigations and policy decisions; this is what a dashboard would show", grid(pick("mode"), "dashboard_stp", pct),
        "**E. Fully manual reference (every record keyed) versus residual staff** — the manual reference is a straw man, not current practice at sponsors that already use reconciliation tools", conv,
        "**F. Marginal onboarding cost of one more institution**", onb])


def sources_section(evidence: Sequence[Row], sources: Sequence[Row]) -> str:
    counts = Counter((e["stream"], e["classification"]) for e in evidence)
    streams = sorted({e["stream"] for e in evidence})
    t1 = table(("Stream", "Confirmed", "Inferred", "Proposed", "Total"),
               [(s, counts[(s, "confirmed")], counts[(s, "inferred")], counts[(s, "proposed")], sum(counts[(s, c)] for c in CLASSIFICATIONS)) for s in streams]
               + [("total",) + tuple(sum(counts[(s, c)] for s in streams) for c in CLASSIFICATIONS) + (len(evidence),)])
    t2 = table(("Source id", "Source", "Title", "Publisher", "Kind", "Evidence"),
               [(s["source_id"], s["source"], s["title"], s["publisher"], s["kind"], s["evidence_ids"].replace(";", "; ")) for s in sources])
    return t1 + "\n\n" + t2


BEGIN, END = "<!-- BEGIN GENERATED: {} -->", "<!-- END GENERATED: {} -->"


def splice(doc: str, name: str, body: str) -> str | None:
    b, e = BEGIN.format(name), END.format(name)
    i, j = doc.find(b), doc.find(e)
    return None if i < 0 or j < i else doc[: i + len(b)] + "\n" + body + "\n" + doc[j:]


def main(argv: Sequence[str]) -> int:
    evidence, sources, inventory = read_csv(EVIDENCE), read_csv(SOURCES), read_csv(INVENTORY)
    parameters, results, onboarding = read_csv(PARAMETERS), read_csv(RESULTS), read_csv(ONBOARDING)
    markdown = {p.name: p.read_text(encoding="utf-8") for p in sorted(PKG.glob("*.md"))}
    industry_data = {p.name: p.read_text(encoding="utf-8") for p in (INVENTORY, FORMATS, EVIDENCE, SOURCES)}
    economics_current = subprocess.run([sys.executable, "-I", "-B", "scripts/fie_economics.py", "--check"], capture_output=True).returncode == 0
    issues = (f1(evidence) + f2(evidence, sources) + f3(inventory, evidence) + f4({**markdown, **industry_data})
              + f5(markdown, evidence) + f6(parameters, economics_current))
    sections = (("03-DAF-INGESTION-WORKFLOW-INVENTORY.md", "inventory", inventory_section(inventory)),
                ("08-STP-OPPORTUNITIES.md", "dispositions", dispositions(inventory)),
                ("09-ECONOMIC-ANALYSIS.md", "economics", economics_section(results, onboarding)),
                ("12-SOURCE-REGISTER.md", "sources", sources_section(evidence, sources)))
    rendered = {}
    for name, sec, body in sections:
        current = rendered.get(name, markdown.get(name, ""))
        nxt = splice(current, sec, body)
        if nxt is None:
            issues += (f"F7 {name}: markers for '{sec}' missing",)
        else:
            rendered[name] = nxt
    stale = tuple(n for n, t in rendered.items() if t != markdown.get(n))
    for i in issues:
        print(i, file=sys.stderr)
    if "--check" in argv:
        for n in stale:
            print(f"F7 stale generated sections: {PKG / n}", file=sys.stderr)
        print(f"{len(issues)} issue(s); {len(stale)} stale document(s)")
        return 1 if issues or stale else 0
    for n in stale:
        (PKG / n).write_text(rendered[n], encoding="utf-8")
    print(f"{len(issues)} issue(s); rewrote {len(stale)} document(s)")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
