# F# Decision Intelligence CLI

This is an **executable validation and deterministic rendering layer** for the Clarity + EDF DAF pilot. It does not replace either framework and does not autonomously generate or validate causal theories.

## Run from the repository root

Requires .NET 10 SDK. No third-party NuGet packages, credentials, cloud services or database.

    dotnet run --project src/DecisionIntelligence/DecisionIntelligence.fsproj -- validate .
    dotnet run --project src/DecisionIntelligence/DecisionIntelligence.fsproj -- render . > decision-report.md
    dotnet run --project tests/DecisionIntelligence.Tests/DecisionIntelligence.Tests.fsproj

CI restores, builds with warnings as errors, runs adversarial tests, validates data, and renders the report.

## Data contract

The manually authored v0 conclusions are preserved unchanged. The **v1** decision data adds verdict types plus supported, limited and rejected claim IDs. The compiler reads existing atomic claim CSVs, market-demand metrics, B/F/V source registers, and a two-row financial evidence crosswalk to the original 2024 Ren payment and Charityvest non-grant expenses.

Validation covers missing sources or metric IDs, claim-role mismatches, duplicate results/references, framework metadata inconsistencies, unavailable next actions or reassessment triggers, malformed SHA pins, and two explicitly scoped financial references matched to the underlying repository CSV cells. Results are rendered with their objection, source links and next-review condition.

**Important limitation:** This validator cannot establish that a publication is true, that the original public audit was transcribed faithfully, that a free-text conclusion follows logically from evidence, or that any product caused an outcome. It checks structured evidence **consistency**, not independent fact verification. Git SHA pins are checked for format, not verified remotely. Source URLs are not fetched during runs. The tests cover structural and metadata rules, **not all 20 semantic challenge prompts** from the previous research work. We do not claim independent expert validation.

It is not a tax engine, profitability scorer, autonomous EDF diagnostic system, or a working Limen/Forma website. It is a reusable F# evidence/result contract with three pre-reviewed domain examples.

## Next gates

1. Add general typed measurement and source-period semantics beyond the current two financial crosswalks.
2. Execute the research adversarial challenge set in a reviewed semantic evaluation pipeline; do not promote artificial model agreement to independent proof.
3. Build a small WASM-first F#/Forma presentation of **Conclusion / Why / Objection / Next Action / Reconsideration** only after the core data passes.
4. Run a blinded user study comparing judgment accuracy against simple data tables and generic AI summaries.
