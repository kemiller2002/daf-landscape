# Workflow innovation: radical reinvention of DAF business processes

This research area is part of the AI-native DAF enterprise workstream ([`../README.md`](../README.md)). It reinvents each business process from first principles, then tries to disprove the results through independent adversarial review, executable experiments and public data.

**Start here:** [executive synthesis](13-executive-synthesis/executive-synthesis.md), then the [progress checkpoints](PROGRESS.md).

| # | Folder | Contents |
|---|---|---|
| 00 | [methodology](00-methodology/methodology.md) | Methods A–F, the five-design rule, maturity ladder L0–L4, criteria |
| 01 | [existing outcomes](01-existing-outcomes/) | Audit, 64 business outcomes, evidence-ranked top-10 workflows |
| 02 | [creative hypotheses](02-creative-hypotheses/) | 48-innovation register, cross-industry transfers, contrarian hypotheses |
| 03 | [alternative designs](03-alternative-designs/) | 105 competing designs |
| 04 | [cross-enterprise workflows](04-cross-enterprise-workflows/) | XW-01…XW-31 |
| 05 / 06 | [API](05-api-opportunities/) / [agent](06-agent-opportunities/) opportunities | Catalogs |
| 07 | [adversarial reviews](07-adversarial-reviews/) | Independent non-author review and verdicts |
| 08 | [experiments](08-experiments/) | E1–E10 (F#), E7/E7b (public data), validation evidence register |
| 09 | [economic validation](09-economic-validation/) | Design and business-model economics; network economics |
| 10 | [prioritization](10-prioritization/) | Five rankings |
| 11 | [reference architectures](11-reference-architectures/) | Integrated process architecture |
| 12 | [implementation proposals](12-implementation-proposals/) | Waves; framework feedback proposals |
| 13 | [executive synthesis](13-executive-synthesis/) | Conclusions by evidence class |

**Reproduce:**
- F# experiments and outputs: `cd ../models && dotnet test && dotnet run --project Daf.Enterprise.Cli -- ..`
- Public-data overlap: `python3 -I scripts/workflow_innovation_recipient_overlap.py --xml-dir <cache-dir> --fetch` (fetches IRS e-file XML), then `python3 -I scripts/workflow_innovation_costly_overlap.py`. Run both from the repository root.
