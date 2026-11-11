# DAF Landscape

Research into the donor-advised fund industry, including sponsoring charities, enterprise platforms, financial advisers, disbursement infrastructure, economics, governance and charitable outcomes.

See the [research index](research/README.md).

## Decision Intelligence, with Clarity + EDF

The initial F# CLI validates three **manually reviewed** conclusions, resolves evidence/source references, classifies claims and renders a concise, reproducible report.

- [CLI setup, scope and limitations](src/DecisionIntelligence/README.md)
- [Architecture and framework boundaries](research/decision-intelligence-architecture-2026.md)
- [Three worked conclusions](research/decision-intelligence-pilot-2026-11-11.md)

Requires .NET 10 SDK:

    dotnet run --project src/DecisionIntelligence/DecisionIntelligence.fsproj -- validate .
    dotnet run --project src/DecisionIntelligence/DecisionIntelligence.fsproj -- render .
    dotnet run --project tests/DecisionIntelligence.Tests/DecisionIntelligence.Tests.fsproj

The program is not an autonomous inference engine or a substitute for source verification, donor tax review or investment judgment. CI builds and checks the validator on pull requests.
