# 01 — Research methodology

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26).

## Questions

For each organization and workflow: what information enters; who supplies it; how it is delivered; structured or not;
what processing follows; what human intervention is required; which financial or compliance controls apply; which
downstream systems consume it; which exceptions occur; and whether the workflow can be eliminated or redesigned.

## Streams

| Stream | Scope | Output |
|---|---|---|
| A — DAF industry | Fidelity Charitable, NPT, DAFgiving360, AEF, Ren/iPhi, Vanguard Charitable, BofA, Morgan Stanley GIFT, Goldman Sachs, Edward Jones/RCF, TIFIN Give family, Chariot, community foundations and their software, independent sponsors, corporate giving platforms, custodians (≈48 organizations) | 142 evidence rows (FIE-A) and [02](02-INDUSTRY-EVIDENCE-CATALOG.md) |
| B — Formats and adjacent industries | 33 formats; delivery mechanisms; banking, custody, payments, fund administration, insurance, payroll, AP, AR, treasury, mortgage, healthcare, government, tax, regulatory reporting, data migration | 66 evidence rows (FIE-B), [`formats.csv`](../../data/file-ingestion-2026-11/formats.csv), [04](04-ADJACENT-INDUSTRY-ANALYSIS.md)–[06](06-DELIVERY-MECHANISMS.md) |
| C — Security, storage, AI | Managed malware scanning, storage options and prices, parser risks, AI document processing prices and controls | 55 evidence rows (FIE-C), [13](13-SECURITY-STORAGE-AND-AI-EVIDENCE.md) |
| Synthesis | Workflow inventory, STP opportunities, economics model, competitor comparison, gaps | [03](03-DAF-INGESTION-WORKFLOW-INVENTORY.md), [08](08-STP-OPPORTUNITIES.md)–[11](11-EVIDENCE-GAPS.md) |

The repository's existing research was searched first and cited by path rather than repeated.

## Evidence rules

- **Confirmed**: read on a public source (URL recorded with access date) or measured from a machine-readable price API.
- **Inferred**: reasoned from confirmed facts, or read only in a search snippet because the site blocks automated
  readers; the reasoning or limitation is in `notes`.
- **Proposed**: an innovation not observed in practice.
- No private specification was obtained or reconstructed; where a specification is contract-only it is recorded as
  such. No proprietary client records or personal data were collected.
- A workflow is marked *confirmed* only if at least one mapped evidence row is itself confirmed (gate F3).

## Saturation

The inventory was expanded domain by domain until a further pass produced no materially distinct workflow (03).

## Independent review

Three adversarial reviewers, given the artifacts but not the authors' conclusions, reviewed integrity and security,
architecture and AI, and economics and regulation. Their findings and the resulting revisions are recorded in the
[research ledger](RESEARCH-LEDGER.md); product-specific findings are recorded in the product repository.

## Reproducibility

```bash
python3 -I -B scripts/fie_economics.py --check   # economics outputs current
python3 -I -B scripts/fie_validate.py --check    # gates F1-F7 (ids, sources, inventory, no product contamination, citations, parameters, generated sections)
```
