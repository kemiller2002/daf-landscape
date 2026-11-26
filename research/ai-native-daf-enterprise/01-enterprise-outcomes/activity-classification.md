# Which inherited activities survive?

**Data:** [`legacy-activity-classification.csv`](legacy-activity-classification.csv) holds 80 activities typical of a conventional DAF sponsor, each given one basis category and one disposition. [`outcome-decisions.csv`](outcome-decisions.csv) holds 81 decision types derived from [the outcome model](outcome-model.md). The counts below are reproduced by the F# model tests (`models/Daf.Enterprise.Tests`, `ActivityCensusTests`).

**What the list is, and its limit:** the activity list is a *design-time enumeration*. It was built from the operating activities described across the repository: the batch 2A–2C grant-workflow studies, the industry report §4 and §11.3–11.5, and the processor rules in g1913. It is not a time-and-motion study. No sponsor publishes activity-level effort (strategic synthesis §0 F, Q-N03). The counts therefore describe *kinds* of work, not hours. Hours are modeled separately, as assumptions, in [`../09-financial-models/`](../09-financial-models/).

## Basis of each inherited activity (the mission's six-way test)

| Basis | Count | Meaning |
|---|---|---|
| Legal obligation | 14 | The law requires the outcome. The method is usually not prescribed |
| Material risk control | 13 | No law requires it, but removing it would expose the enterprise to material loss |
| Industry convention | 14 | Done because peers do it |
| Legacy technology limitation | 39 | Exists because data was on paper, in batch files or in disconnected systems |
| *(Outcome-only and directly eliminable activities are captured through the disposition column)* | | |

## Disposition

| Disposition | Count | Meaning |
|---|---|---|
| Eliminate | 14 | The work disappears because its cause disappears. Examples: re-keying, per-grant status lookups, grant-status inquiries, PBC sample pulls |
| Reduce | 9 | Survives only for a residual population, such as checks for recipients that cannot take electronic payment |
| Automate (deterministic) | 21 | Same outcome, now produced by versioned rules with evidence |
| Transform | 20 | Same outcome, achieved by a different mechanism (for example continuous reconciliation instead of month-end) |
| Retain, human-accountable | 16 | Judgment the law or risk appetite assigns to a person; AI prepares, a person decides |

**Reading:**
- **23 of 80 activities (29%)** are eliminated or reduced to a residual.
- **41 (51%)** keep their outcome but change mechanism: automated or transformed.
- **16 (20%)** remain human-accountable.

Every one of the 16 retained activities is a legal obligation or a material risk control. **None of the conventions or legacy-technology activities survives in its current form.** That is a design assertion to test, not an observed fact: falsification would be a convention that turns out to carry undocumented risk value. Candidates are listed in [`../13-clarity-edf-analysis/`](../13-clarity-edf-analysis/).

## Decisions (81 decision types)

| Type | Count of decision types | Volume profile |
|---|---|---|
| D, deterministic | 37 | Mostly high or very high volume (22 of 37 are high/very high) |
| P, probabilistic (always resolves to D or H before money or legal state changes) | 11 | Mostly high or medium volume |
| H, human-authorized | 33 | 33 of 33 are low or very low volume |

**Key structural finding:** humans own *most of the decision types* but *very little of the decision volume*. That separates a conventional sponsor, where people perform the high-volume D decisions, from the redesigned one, where people own the rules for the D decisions and personally make only the H decisions. It is why headcount can fall without accountability falling. Whether it also lowers *risk* is a separate claim, tested in [`../13-clarity-edf-analysis/`](../13-clarity-edf-analysis/) ("lower headcount always means lower risk" is rejected there).
