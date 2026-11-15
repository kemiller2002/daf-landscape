#!/usr/bin/env python3
"""Like-for-like nonprofit-side panel across DAF sponsors and rails (queue item P-NPT-06).

Stdlib only; functional style. Every input is read once into immutable tuples, every panel cell is
a pure function of (entity, field, inputs), and I/O happens only in main().

Inputs (all under data/mission-2026-11-14/):
  sponsor-grant-payment-policies.csv        (key: sponsor)
  sponsor-eft-providers-2026.csv            (key: sponsor)
  bank-program-terms-2026.csv               (key: sponsor + item)
  nonprofit-daf-receipt-fees-2026.csv       (key: route_id)
  nonprofit-receipt-cost-by-rail.csv        (key: rail_id)
  sponsor-fee-schedules.csv                 (key: sponsor + fee_component == min_grant)
  community-foundation-rails-portals-2026-v2.csv (key: foundation)
  nonprofit-side-panel-2026-evidence.csv    (long format; fresh 2026-11-15 reads and curated cells)

Merge rule per (entity, field):
  1. a row in the evidence file wins (it is the latest read and states its own evidence class);
  2. otherwise the first repo rule (in RULES order) that matches the entity supplies the cell;
  3. otherwise the cell is blank (= not researched for this entity in this pass).
  "not found ..." means sources were read and said nothing; it does not count as coverage.

Output: data/mission-2026-11-14/nonprofit-side-panel-2026.csv (one row per entity; for every field a
value, a source-URL cell and an origin cell). Coverage per field is printed to stdout.

Usage: python3 scripts/mission_nonprofit_panel.py [--out PATH]
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Callable, Mapping, NamedTuple, Optional

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "mission-2026-11-14"
OUT_DEFAULT = DATA / "nonprofit-side-panel-2026.csv"

FIELDS = (
    "fee_per_gift",
    "disbursement_cadence",
    "minimum_threshold",
    "default_rail",
    "enrollment_requirement",
    "remittance_donor_identity",
    "remittance_fund_name",
    "void_return_policy",
)

INPUT_FILES = {
    "policies": "sponsor-grant-payment-policies.csv",
    "eft": "sponsor-eft-providers-2026.csv",
    "bank": "bank-program-terms-2026.csv",
    "fees": "nonprofit-daf-receipt-fees-2026.csv",
    "rail": "nonprofit-receipt-cost-by-rail.csv",
    "feesched": "sponsor-fee-schedules.csv",
    "cf": "community-foundation-rails-portals-2026-v2.csv",
    "evidence": "nonprofit-side-panel-2026-evidence.csv",
}


class Entity(NamedTuple):
    entity_id: str
    name: str
    entity_type: str  # national_sponsor | bank_sponsor | challenger_sponsor | intermediary | rail | community_foundation
    keys: Mapping[str, tuple]  # input name -> tuple of key values


def E(entity_id: str, name: str, entity_type: str, **keys: tuple) -> Entity:
    return Entity(entity_id, name, entity_type, {k: tuple(v) for k, v in keys.items()})


ENTITIES = (
    E("fidelity", "Fidelity Charitable", "national_sponsor",
      policies=("Fidelity Charitable",), eft=("Fidelity Charitable",), rail=("R04",),
      feesched=("Fidelity Charitable",)),
    E("dafgiving360", "DAFgiving360 (Schwab Charitable)", "national_sponsor",
      policies=("DAFgiving360 (Schwab Charitable)",), eft=("DAFgiving360 (Schwab Charitable)",)),
    E("vanguard", "Vanguard Charitable", "national_sponsor",
      policies=("Vanguard Charitable",), eft=("Vanguard Charitable",)),
    E("npt", "National Philanthropic Trust (NPT)", "national_sponsor",
      policies=("National Philanthropic Trust (NPT)",), eft=("National Philanthropic Trust (NPT)",)),
    E("aef", "American Endowment Foundation (AEF)", "national_sponsor",
      eft=("American Endowment Foundation (AEF)",)),
    E("rcf_ren", "Renaissance Charitable Foundation / Ren-administered programs", "national_sponsor",
      eft=("Ren-administered sponsors (vendor statement)",)),
    E("ncf", "National Christian Foundation (NCF)", "national_sponsor",
      eft=("National Christian Foundation (NCF)",), bank=("National Christian Foundation (NCCF; EIN 58-1493949)",)),
    E("bofa_cgf", "Bank of America Charitable Gift Fund", "bank_sponsor",
      eft=("Bank of America Charitable Gift Fund",), bank=("Bank of America Charitable Gift Fund (EIN 04-6010342)",)),
    E("ms_gift", "Morgan Stanley GIFT", "bank_sponsor",
      eft=("Morgan Stanley GIFT",), bank=("Morgan Stanley GIFT (EIN 52-7082731)",)),
    E("daffy", "Daffy", "challenger_sponsor",
      policies=("Daffy",), eft=("Daffy",)),
    E("charityvest", "Charityvest", "challenger_sponsor",
      policies=("Charityvest",), eft=("Charityvest",)),
    E("endaoment", "Endaoment", "challenger_sponsor", eft=("Endaoment",)),
    E("everyorg", "Every.org", "intermediary", rail=("R12",)),
    E("ppgf", "PayPal Giving Fund", "intermediary", fees=("F18",), rail=("R14",)),
    E("benevity_aogf", "Benevity / American Online Giving Foundation", "intermediary"),
    E("yourcause_bbgf", "YourCause / Blackbaud Giving Fund", "intermediary"),
    E("chariot_dafpay", "Chariot DAFpay (default terms; DAFpay Network for unclaimed)", "rail",
      fees=("F01",), policies=("Chariot DAFpay Network (intermediary holding unclaimed DAFpay gifts)",)),
    E("chariot_disbursements", "Chariot Disbursements (sponsor payout rail)", "rail",
      policies=("Chariot Disbursements (rail used by partner sponsors)",), eft=("Chariot Disbursements (provider)",),
      rail=("R10",)),
    E("paypal_grant_payments", "PayPal Grant Payments (sponsor payout rail)", "rail",
      eft=("PayPal Grant Payments (provider)",)),
    E("daf_direct", "DAF Direct (widget)", "rail", fees=("F17",), rail=("R11",)),
    # Top 10 community foundations by FY2024 DAF assets, plus three with distinctive 2026 rails.
    *(E(f"cf_{slug}", name, "community_foundation", cf=(name,), **extra)
      for slug, name, extra in (
          ("svcf", "Silicon Valley Community Foundation", {}),
          ("cct", "The Chicago Community Trust", {}),
          ("fftc", "Foundation For The Carolinas", {}),
          ("gkccf", "Greater Kansas City Community Foundation", {}),
          ("columbus", "The Columbus Foundation", {}),
          ("nyct", "The New York Community Trust", {}),
          ("ocf", "Oregon Community Foundation", {"eft": ("Oregon Community Foundation",)}),
          ("tbf", "The Boston Foundation", {}),
          ("ccf", "California Community Foundation", {}),
          ("cfga", "Community Foundation for Greater Atlanta", {}),
          ("seattle", "Seattle Foundation", {}),
          ("spmf", "Saint Paul & Minnesota Foundation", {}),
          ("gwcf", "Greater Washington Community Foundation", {}),
      )),
)


class Cell(NamedTuple):
    value: str
    src: str
    origin: str


EMPTY = Cell("", "", "")

Row = Mapping[str, str]
Tables = Mapping[str, tuple]


# ---------- pure helpers ----------

def read_csv(path: Path) -> tuple:
    with path.open(newline="", encoding="utf-8") as fh:
        return tuple(dict(r) for r in csv.DictReader(fh))


def join_nonempty(parts, sep: str = "; ") -> str:
    return sep.join(p.strip() for p in parts if p and p.strip())


def union_urls(urls) -> str:
    seen: list = []
    for chunk in urls:
        for u in (x.strip() for x in (chunk or "").split(" ; ")):
            if u and u not in seen:
                seen.append(u)
    return " ; ".join(seen)


def rows_for(tables: Tables, source: str, entity: Entity, key_col: str,
             extra: Callable[[Row], bool] = lambda r: True) -> tuple:
    keys = entity.keys.get(source, ())
    return tuple(r for r in tables[source] if r.get(key_col, "") in keys and extra(r))


def cell_from(rows: tuple, value_fn: Callable[[Row], str], url_fn: Callable[[Row], str], origin: str) -> Cell:
    values = tuple(v for v in (value_fn(r) for r in rows) if v)
    if not values:
        return EMPTY
    return Cell(" | ".join(values), union_urls(url_fn(r) for r in rows), origin)


# ---------- repo derivation rules: (field, function(entity, tables) -> Cell) ----------

def rule(source: str, key_col: str, value_fn, url_fn, extra=lambda r: True):
    origin = f"repo:{INPUT_FILES[source]}"
    return lambda ent, t: cell_from(rows_for(t, source, ent, key_col, extra), value_fn, url_fn, origin)


src_url = lambda r: r.get("source_url", "")

RULES = (
    # enrollment: EFT-provider table is more specific than the policies table
    ("enrollment_requirement", rule("eft", "sponsor", lambda r: r["enrollment_requirement"], src_url)),
    ("enrollment_requirement", rule("policies", "sponsor", lambda r: f"EFT required: {r['eft_required']}", src_url)),
    ("default_rail", rule("policies", "sponsor",
                          lambda r: join_nonempty((r["rail_options"], f"unenrolled: {r['fallback_for_unenrolled']}")), src_url)),
    ("default_rail", rule("eft", "sponsor",
                          lambda r: join_nonempty((r["eft_provider"], f"check fallback: {r['check_fallback']}")), src_url)),
    ("default_rail", rule("bank", "sponsor", lambda r: r["finding"], src_url,
                          extra=lambda r: r["item"] == "grant_payment_rail")),
    ("default_rail", rule("cf", "foundation",
                          lambda r: join_nonempty((r["payment_rails"], f"provider: {r['eft_provider']}")),
                          lambda r: r.get("source_urls", ""))),
    ("disbursement_cadence", rule("policies", "sponsor", lambda r: r["stated_timing"], src_url)),
    ("disbursement_cadence", rule("bank", "sponsor", lambda r: r["finding"], src_url,
                                  extra=lambda r: r["item"] == "grant_payment_rail" and "within" in r["finding"])),
    ("void_return_policy", rule("policies", "sponsor", lambda r: r["uncashed_check_policy"], src_url)),
    ("void_return_policy", rule("bank", "sponsor", lambda r: r["quote"], src_url,
                                extra=lambda r: r["item"] == "grant_payment_rail" and "uncashed" in r["quote"].lower())),
    ("remittance_donor_identity", rule("bank", "sponsor", lambda r: f"{r['finding']} (\"{r['quote']}\")", src_url,
                                       extra=lambda r: r["item"] == "remittance_fields")),
    ("remittance_fund_name", rule("bank", "sponsor", lambda r: r["finding"], src_url,
                                  extra=lambda r: r["item"] == "remittance_fields"
                                  and any(w in r["finding"].lower() for w in ("account", "fund")))),
    ("minimum_threshold", rule("feesched", "sponsor", lambda r: f"${r['flat_amount_usd']} minimum grant", src_url,
                               extra=lambda r: r["fee_component"] == "min_grant")),
    ("minimum_threshold", rule("eft", "sponsor", lambda r: r["limits"], src_url,
                               extra=lambda r: "minimum" in r["limits"].lower())),
    ("fee_per_gift", rule("fees", "route_id",
                          lambda r: (f"{r['total_fee_pct_nonprofit_default']}% default "
                                     f"(${r['fee_per_1000_usd_nonprofit_default']} per $1,000); "
                                     f"payer: {r['who_pays_by_default']}; {r['waiver_or_subscription_terms']}"), src_url)),
    ("fee_per_gift", rule("rail", "rail_id", lambda r: r["fee_basis"], lambda r: r.get("fee_source", ""))),
)


def evidence_index(rows: tuple) -> Mapping:
    return {(r["entity_id"], r["field"]): Cell(
        r["value"], r["source_url"], f"fresh:{r['retrieved']} [{r['evidence_class']}]") for r in rows}


def repo_cell(entity: Entity, field: str, tables: Tables) -> Cell:
    return next((c for f, fn in RULES if f == field for c in (fn(entity, tables),) if c.value), EMPTY)


def panel_cell(entity: Entity, field: str, tables: Tables, evidence: Mapping) -> Cell:
    repo = repo_cell(entity, field, tables)
    fresh = evidence.get((entity.entity_id, field))
    if fresh is None:
        return repo
    note = f"; supersedes {repo.origin}" if repo.value else ""
    return fresh._replace(origin=fresh.origin + note)


def status(value: str) -> str:
    v = value.strip().lower()
    if not v:
        return "blank"
    return "not_found" if v.startswith("not found") else "covered"


def panel_row(entity: Entity, tables: Tables, evidence: Mapping) -> dict:
    cells = {f: panel_cell(entity, f, tables, evidence) for f in FIELDS}
    base = {"entity_id": entity.entity_id, "entity": entity.name, "entity_type": entity.entity_type}
    body = {k: v for f, c in cells.items()
            for k, v in ((f, c.value), (f"{f}_src", c.src), (f"{f}_origin", c.origin))}
    covered = sum(status(c.value) == "covered" for c in cells.values())
    return {**base, **body, "fields_covered": f"{covered}/{len(FIELDS)}"}


def coverage(rows: tuple, entity_types: Optional[tuple] = None) -> tuple:
    sel = tuple(r for r in rows if entity_types is None or r["entity_type"] in entity_types)
    return tuple((f, len(sel),
                  sum(status(r[f]) == "covered" for r in sel),
                  sum(status(r[f]) == "not_found" for r in sel),
                  sum(status(r[f]) == "blank" for r in sel)) for f in FIELDS)


def check_keys(tables: Tables) -> tuple:
    """Return entity keys that match no input row (guards against silent mismatches)."""
    key_cols = {"policies": "sponsor", "eft": "sponsor", "bank": "sponsor", "fees": "route_id",
                "rail": "rail_id", "feesched": "sponsor", "cf": "foundation"}
    return tuple(f"{e.entity_id}:{src}:{k}" for e in ENTITIES for src, ks in e.keys.items() for k in ks
                 if not any(r.get(key_cols[src]) == k for r in tables[src]))


# ---------- I/O ----------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = ap.parse_args()

    tables = {name: read_csv(DATA / fn) for name, fn in INPUT_FILES.items()}
    missing = check_keys(tables)
    if missing:
        raise SystemExit(f"unmatched entity keys: {missing}")
    known = {e.entity_id for e in ENTITIES}
    stray = sorted({r["entity_id"] for r in tables["evidence"]} - known)
    bad_fields = sorted({r["field"] for r in tables["evidence"]} - set(FIELDS))
    if stray or bad_fields:
        raise SystemExit(f"evidence rows with unknown entity {stray} or field {bad_fields}")

    evidence = evidence_index(tables["evidence"])
    rows = tuple(panel_row(e, tables, evidence) for e in ENTITIES)
    header = ["entity_id", "entity", "entity_type",
              *(c for f in FIELDS for c in (f, f"{f}_src", f"{f}_origin")), "fields_covered"]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=header)
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {args.out.relative_to(ROOT)}: {len(rows)} entities x {len(FIELDS)} fields")
    groups = (("all entities", None),
              ("sponsors + intermediaries + rails", ("national_sponsor", "bank_sponsor", "challenger_sponsor",
                                                     "intermediary", "rail")),
              ("community foundations", ("community_foundation",)))
    for label, types in groups:
        print(f"\ncoverage, {label} (covered / not_found / blank of n):")
        for f, n, c, nf, b in coverage(rows, types):
            print(f"  {f:28s} {c:3d} / {nf:3d} / {b:3d} of {n}")
    origins = [r[f"{f}_origin"].split(":")[0] for r in rows for f in FIELDS if r[f]]
    print(f"\nnon-blank cells by origin: fresh={origins.count('fresh')} repo={origins.count('repo')}")
    sources_missing = [(r["entity_id"], f) for r in rows for f in FIELDS if r[f] and not r[f"{f}_src"]]
    print(f"non-blank cells without a source URL: {len(sources_missing)} {sources_missing}")
    print("\nper entity:", ", ".join(f"{r['entity_id']}={r['fields_covered']}" for r in rows))


if __name__ == "__main__":
    main()
