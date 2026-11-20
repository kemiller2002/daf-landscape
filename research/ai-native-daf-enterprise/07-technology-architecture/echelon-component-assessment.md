# Echelon component capability and maturity assessment

Inspection date: 2026-11-20. Scope: 14 public repositories under `github.com/kemiller2002`. `clarity-framework` is private and could not be cloned. It was **not inspected**; see the pinned summary at `research/mission-2026-11-14/clarity-edf-application-guide.md`.

Purpose: to stop the AI-native DAF enterprise architecture from depending on capabilities these components do not have. Everything below comes from repository contents at the listed commits. Absence of evidence is reported as absence of evidence, not as evidence of absence.

## 1. Method

- **How the repositories were read.** Each repository was shallow-cloned with `git clone --depth 50` into a session scratchpad. Content was treated as untrusted data. Files were read with `cat`, `grep`, `wc` and `git log`. No build script, test, installer or CLI was executed, so **no claim below says that code compiles or that tests pass.**
- **How LOC was counted.** LOC is the raw line count (`wc -l`) of tracked files grouped by extension. It includes blank lines, comments, generated files and vendored copies, so read it as an order of magnitude. Large JSON totals are mostly generated registries, telemetry and fixtures, not code.
- **What the commit counts mean.** "Commits" is the number reachable in the depth-50 clone. Depth applies along first-parent history, so merged branch commits push this past 50. It is not the repository's total history. "First date" is the oldest commit in the shallow clone, not the repository's creation date.
- **How tests were counted.**
  - xUnit `[<Fact>]`/`[<Property>]` attributes were counted where they are used.
  - Praxis and Conditor use custom in-repo harnesses, so for them `t "…"` cases or `check` calls were counted.
  - JS/TS `test(`/`it(` calls in test files were counted.
  - These are static counts. Test pass/fail status was **not observed**.
- **CI status was not checked.** Workflow files were listed. Run results on GitHub Actions were **not inspected**: the session's GitHub API scope refused these repositories (HTTP 403). Whether CI is green is unknown.
- **Package registries were not checked.** NuGet and npm publication claims come from READMEs and workflows only. The registries themselves were not queried.

### Commits inspected

| Repository | HEAD SHA | Last commit | Commits in shallow clone | Tags / version marker |
|---|---|---|---|---|
| limen | `743cdb9be8971c0a3a250906a6e2e112170dfae0` | 2026-10-28 | 204 | v0.7.0–v0.9.1; package 0.9.1 |
| forma | `3887eec80668fecc7c6e91e38a782765a71199ff` | 2026-11-10 | 282 | v0.4.1–v1.0.2; package 1.0.2 |
| forma-studio | `904d3b455bf4b9b21a978984774f9746b5a29ea5` | 2026-10-27 | 177 | none; package 0.0.0 |
| folio | `217d644e39b11127620f8d83a1e1ee9dff59ec48` | 2026-10-22 | 168 | v0.3.0–v0.4.1; package 0.4.2 |
| aegis | `2c28b6e20565164b0f604298062ebdfc19d1a2af` | 2026-10-16 | 65 | no git tags; README/consumers cite `Aegis.Core` 1.0.0 on NuGet (registry not verified) |
| dokimos | `6ea86246cb13f141201bc5cae5d84ebe9831d02b` | 2026-11-09 | 172 | dokimos-v0.2.0–v0.11.1 |
| praxis | `12bf9951253fc15e6973c2d3f5b88076f4556245` | 2026-11-03 | 124 | v3.15.0–v3.25.0 |
| echelon-knowledge-store | `35d9cee0df94eed89335712fbaade4d491a45bcd` | 2026-11-17 | 27 (first 2026-11-16) | none; version 0.0.0 |
| echelon-foundry | `8c6b45358fb1bcae4f612534637077d35dd72762` | 2026-10-13 | 69 | none |
| echelon-engineering-system | `4ca2f981ea2c813cd4894f1ce83c7b2c4ece14a6` | 2026-10-28 | 24 | none; package 0.1.0 |
| echelon-diagnostic-framework | `710d54c20e935db8b6f75f9c60ee7217f0cb0e32` | 2026-11-17 | 151 | none; spec "frozen v0.3 working baseline" |
| echelon-design-system | `2c0e82e32a14161e61a73d67aefd0c9a07a8f3e6` | 2026-11-11 | 37 (first 2026-11-09) | v1.0.0, v1.1.0 (theme package) |
| echelon-registry | `fef1f944ccfb2f9975a2183bb770c14fed88cc5f` | 2026-11-09 | 239 | none |
| conditor | `f29d01c36adc65952a8b70bde81cb4cfa2abb32a` | 2026-11-09 | 134 | v0.10.9–v0.10.25 |
| clarity-framework | — | — | — | private; not inspected |

### Cross-cutting observations

1. **Very young code.** The oldest commit in any shallow clone is 2025-12 (echelon-foundry). Every component's visible code history falls between 2026-09 and 2026-11. Echelon-knowledge-store and echelon-design-system each span about three days.
2. **One maintainer, mostly AI-written.** Commit authors are one human (Kevin Miller) plus "Claude" and a few bots. In 7 of 14 repositories, Claude-authored commits outnumber human ones. There is no evidence of a second human maintainer, of outside contributors, or of independent code review by another person.
3. **Licensing is a gating issue.** 10 of the 14 repositories carry **PolyForm Noncommercial 1.0.0**: limen, forma, forma-studio, folio, aegis, dokimos, praxis, echelon-knowledge-store, conditor, and echelon-design-system's dependencies via Forma. The READMEs add: "Commercial use requires a separate license from Echelon Foundry… Commercial licensing information is forthcoming."
   - PolyForm NC §"Noncommercial Organizations" does permit use by "any charitable organization". A 501(c)(3) DAF sponsor may therefore qualify.
   - A commercial administrator, a vendor, or a bank-affiliated sponsor would not obviously qualify.
   - This needs legal review before any dependency is taken.
   - echelon-foundry, echelon-registry and echelon-diagnostic-framework are MIT. echelon-design-system and echelon-engineering-system have no LICENSE file in the repository root.
4. **No external production evidence.** Inspection found no deployment by any organization other than the author. The only consumers in evidence are the author's own repositories and websites, for example Limen → `time-entry-state-machine` and Dokimos → aegis.
5. **Governance files may lag the code.** The `context/CURRENT-STATE.md` templates in aegis, conditor, limen, registry and EDF still say "Complete the charter and select the first bounded pilot slice". Several governance records may not reflect actual state.
6. **Overlapping governance tooling.** Most repositories vendor the same Praxis/ROS, Ordo/SDE and Limen tooling (`praxis/`, `ros/`, `.sde/`, `registries/`, `telemetry/`). That is why JSON and Markdown dominate the line counts.

## 2. Summary table

Maturity scale:
- **spec-only**: documents and schemas, no executable product.
- **prototype**: working code, but explicitly early, unreleased or research.
- **usable-with-risk**: released, tested code with a real API, but 0.x, a single maintainer, and no outside production use.
- **production-evidence**: deployed in production by independent users. **None** of these components reach this level.

| Component | Stated purpose (README) | Evidence of working code | Tests (static count) | Maturity | Plausible DAF role | Dependency risk |
|---|---|---|---|---|---|---|
| **Limen** | Browser library separating a browser "kernel" (DOM, fetch, storage) from an application "engine" that owns state. Engines exchange JSON only. Includes a lifecycle CLI. | Yes: about 47k TS (kernel, protocol), 22k F# (CLI, site engine, routing), 12.7k C#, 12.9k Rust guests. | ~763 JS/TS cases, ~125 F# attributes; CI workflows present | usable-with-risk (0.x; CHANGELOG: "protocol may change in a minor release") | Front-end state/effect boundary and URL routing for donor and grant UIs. It is **not** a server-side WASM execution or sandbox runtime. | High: 0.x protocol, PolyForm NC, single maintainer |
| **Forma** | Zero-runtime, brand-neutral design system: semantic HTML, CSS, tokens, accessibility contracts | Yes: about 11k CSS, 36k HTML patterns, 57k mjs tooling/tests, 13k F# (compilers, codemod) | ~827 JS/TS cases (Playwright: Chromium, Firefox, WebKit, axe) | usable-with-risk (1.0.2; semver claimed) | UI presentation layer (CSS and markup) for staff and donor portals | Medium: CSS-only, so it is easy to replace or fork. License is the main risk. |
| **Forma Studio** | Visual page/diagram specification editor that exports a typed spec | Partial: about 8.3k F# engine, schema, examples | ~113 F# cases, ~55 JS | prototype (version 0.0.0, no tags) | Design-time tool only. Not a runtime dependency. | High if depended on. Low if not used. |
| **Folio** | Print component system: light-DOM web components and print CSS for HTML→PDF documents | Yes: about 10.5k mjs, 9.4k CSS, 21 `ef-print-*` components | ~46 JS cases; print experiment workflows | usable-with-risk / prototype boundary (0.4.x; "first vertical slice" language) | Document rendering for grant letters, donor statements and tax receipts (HTML→PDF via Chromium). It is **not** a reporting engine, data warehouse or BI tool. | Medium–High: 0.x, Chromium-tier rendering, PolyForm NC |
| **Aegis** | .NET/F# library for capturing, classifying, redacting and recovering from **unexpected operational failures** at boundaries | Yes: about 4.1k F# in src, NuGet publish workflow | ~330 xUnit attributes; requirements trace 137 done / 4 partial / 2 not started | usable-with-risk (claims Core 1.0.0; no git tags) | Fault and resilience handling at integration boundaries, with redaction of diagnostic context. **Not a security product**: no authn/authz, secrets, crypto or threat detection. | Medium: no third-party dependencies, small; license and maintainer risk |
| **Dokimos** | Evidence-based **code-quality** measurement with longitudinal history, regressions, hotspots | Yes: about 17.7k F# in src (Core, Domain, CLI), released .NET tool | ~567 xUnit attributes, ~62 JS | usable-with-risk (v0.11.1; self-described "operational" on its own and one other repository) | Engineering code-quality evidence in the SDLC. **Not** regulatory or compliance verification. | Medium: SDLC-only, not in the production path |
| **Praxis** | Repository operating system: work protocol, research records, telemetry, agent provenance, validation, CI | Yes: about 104k F# in src (largest codebase), native bundles, dotnet tool | ~892 custom-harness cases | usable-with-risk (v3.25.0; frequent releases) | Engineering governance and agent-work provenance for the delivery team's own repositories | Medium: developer tooling, not runtime; heavy repository footprint and lock-in to its conventions |
| **Echelon Knowledge Store** | Research into storing and delivering knowledge to AI agents; experimental Markdown→artifact compiler | Partial: about 5k F# (Core, Compiler, CLI `eks`) | ~108 xUnit attributes; benchmark workflow | prototype / research ("research phase… No stable schema, no released packages") | Possible future: compile governed Markdown policies into machine-readable packages for agents | High: unreleased, unstable schema, ~3-day history |
| **Echelon Foundry** | Company/site repository; "greenfield pilot running Praxis 3.7.1" | Static website (JS build, HTML) | ~18 Playwright cases (UI conformance) | spec-only (as standards) | Source of engineering standards (see §4). Contains no product code. | n/a: standards text, not a runtime |
| **Echelon Engineering System** | Static F# publisher documenting Echelon architecture and method | Yes, but small (572 F#) | ~17 Playwright cases | prototype (documentation site) | Reference documentation only | Low (not a dependency) |
| **Echelon Diagnostic Framework (EDF)** | "Working diagnostic grammar" for explicit system diagnoses | No application runtime ("intentionally has no application framework"); integrity scripts only | ~17 Node integrity tests | spec-only (frozen v0.3 working baseline; self-states unvalidated claims) | Possible analytical method for architecture and incident diagnosis. Not software. | Low as a method. Do not cite as validated. |
| **Echelon Design System** | Versioned brand/design contracts and the Echelon theme package for Forma | Theme CSS, tokens, Python build tooling (~2.7k) | ~36 test files (Python validators, Playwright) | prototype ("Bootstrap / brand source audit… owner approval pending"; candidate palette "unverified") | Not relevant to a DAF (it is Echelon's own brand) | n/a |
| **Echelon Registry** | Discovery and interoperability **specification** for Echelon systems (capability resolution, release manifests) | Specification, JSON Schemas, ~2.6k F# script validators | conformance workflow; no unit test project | spec-only (normative specs plus schemas) | Pattern reference for capability-based integration. Not a runtime service registry. | Low if used as a pattern. High if treated as infrastructure. |
| **Conditor** | CLI that bootstraps a governed repository from a manifest (installs pinned Echelon components, scaffolds) | Yes: about 22.9k F# in src | ~933 `check` assertions (custom harness) | usable-with-risk (v0.10.25), for Echelon-ecosystem bootstrapping only | Repository scaffolding for the delivery team, if it adopts Echelon tooling | Medium: dev-time only, couples to the Echelon toolchain |

## 3. Per-component findings

### 3.1 Limen

The README answers "Where is the WebAssembly?" directly: "The **npm package is still a TypeScript browser boundary** and does not ship a WASM application engine."

- **What WASM exists.** `docs/17-wasm-migration.md` lists two real F#/.NET WebAssembly *consumers*: the Limen product site and the separate `time-entry-state-machine` repository. Limen does not provide general WASM execution.
- **Other-language guests.** `guests/` holds Rust (about 12.9k lines), C# and F# guest examples. There is also an unreleased `limen wasm-check` static check for .NET guest frame-size limits.
- **Key concepts.**
  - BrowserKernel: knows six HTML attributes and no application vocabulary.
  - Engine: owns state, transitions, validation and capabilities.
  - JSON-only `EngineTransport`.
  - Lifecycle CLI: `init`, `status`, `verify`, `upgrade`, `doctor`.
  - Routing module: `@echelon-foundry/limen/routing` and F# `EchelonFoundry.Limen.Routing`, implementing the portfolio URL-state standard (SAF-URL-1..10).
- **Maturity.** 0.9.1. CHANGELOG: "**`0.x` caveat.** The protocol may change in a minor release. Pin an exact version." The package was renamed at 0.7.0.
- **DAF role.** A *browser-side* architecture pattern (engine/kernel separation, URL-as-truth). It is **not** a server-side WASM plugin host, sandbox or policy-execution runtime. An architecture that assumes "Limen executes WASM modules (rules, plugins) safely" depends on a capability that **does not exist** in this repository.
- **Absent:** no evidence of a server runtime, sandboxing or resource isolation, a security review of the kernel, or third-party production use.

### 3.2 Forma

- **What it is.** Zero-runtime CSS, HTML pattern and token design system: "Behavior beyond browser-native interaction belongs to the consuming application, normally through Limen." It ships no JS component runtime. `<forma-*>` tags are inert wrappers.
- **Testing and catalog.** Strongest test evidence in the set: Playwright across Chromium, Firefox and WebKit, axe accessibility checks, and conformance and site-validation workflows (25 workflow files). It has a component catalog and a consumption guide (`docs/CONSUMING-FORMA.md`) that requires pinned releases.
- **Maturity.** 1.0.2 with semantic-versioning claims. 1.0.0 introduced a namespace rename (`ef-` → `forma-`) with a codemod, so breaking changes happened within weeks of release.
- **DAF role.** A reasonable CSS foundation for internal UIs. It is easy to vendor or replace because it is just CSS and HTML. Accessibility testing is a plus, but WCAG conformance for a DAF product must still be verified on the product itself.

### 3.3 Forma Studio

- **What it is.** An editor and specification environment. F# engine with Aegis Core 1.0.0 pinned. Requirements are extensive.
- **Maturity.** Version 0.0.0, no tags. The README describes a "greenfield baseline tracked by GitHub issue #1."
- **DAF role.** At most an optional design-time tool. Not a runtime dependency.

### 3.4 Folio

- **What it is.** 21 registered `ef-print-*` light-DOM components: document, title page, header/footer, page number, table, TOC, metric, finding, and others. Package `@echelon-foundry/print-components` 0.4.2, "zero runtime dependencies and CSS-first print behavior."
- **Renderer tiers.** P0 portable browser; P1 Chromium margin boxes; P2 deterministic Chromium PDF; P3 optional paged-media engine.
- **What it is not.** A reporting or analytics engine. It has no data access, query, aggregation, scheduling or report-definition model. It formats HTML that the application has already composed.
- **DAF role.** A template layer for donor statements, grant award letters and tax acknowledgments rendered to PDF by headless Chromium.
- **Before relying on it,** regulated documents (IRS contemporaneous written acknowledgments, for example) need deterministic, archivable output: PDF/A, fonts embedded and pinned. The search found no PDF/A, archival or e-signature support.

### 3.5 Aegis

- **What it is.** Despite the name, Aegis is **not a security component.** It is an operational-fault handling library. The README says "Aegis is not a logging framework, a metrics platform, a tracing product, an analytics system or a monitoring tool", and that expected business outcomes ("`InvoiceAlreadyPaid`…") "belong in discriminated unions, `Result`, or SDE transitions. Aegis is for the GitHub outage, not the business rule."
- **Features.** Fault model, capture API, redaction of context, lifecycle, recovery and escalation, presentation, containment, and sinks.
- **Shipped adapters.** Only a GitHub event store and a GitHub integration. Database adapters "are built elsewhere". No DB adapter was found in this repository.
- **Requirements status.** `docs/aegis/REQUIREMENTS-STATUS.md` (status: draft) records 137 done, 4 partial and 2 not started.
- **Where security lives instead.** Dokimos's README says "Security remains owned by Aegis/Tutors". Conditor and Folio reference a separate security component, **Tutela**. Tutela is not in the inspected set. Its existence and maturity were **not inspected**.
- **DAF role.** Optional resilience pattern for .NET boundary calls.
- **Gaps for a regulated system.** It provides none of: identity, access control, encryption, key management, audit logging fit for regulators, or fraud/AML controls. Mapping "Aegis = security layer" in the architecture would be an error.

### 3.6 Dokimos

- **What it is.** Code-quality measurement over time: immutable observations, baselines, ratchets, Git churn and hotspots, a "first conservative F# structural source analyzer", and one candidate rule (DOK-FS-001). Released as .NET tool `EchelonFoundry.Dokimos.Cli` with native archives. Operational on its own repository and on aegis.
- **What it is not.** The README places security, process telemetry and state legality outside its scope. It has **no** regulatory or compliance-rule verification: no control mapping, policy-as-code over business data, or audit evidence for SOC 2 or IRS rules.
- **DAF role.** An optional SDLC quality-evidence tool. "Testing/compliance verification" for a DAF's business rules is not provided.

### 3.7 Praxis

- **What it is.** The largest and most actively released codebase: about 104k F# in src, v3.15→v3.25 tagged within about two weeks. It provides:
  - a work protocol with legal transitions and completion evidence;
  - canonical research and decision records;
  - execution telemetry that "distinguishes unavailable from zero";
  - agent identity and provenance;
  - validation and CI.
- **Distribution.** Native bundle via `curl … install-native.sh | sh` or `dotnet tool install -g EchelonFoundry.Praxis`.
- **Shared requirements.** It owns the portfolio-wide shared application requirements (`requirements/SHARED-APPLICATION-FOUNDATIONS.md`) covering Aegis, Forma, Folio and the URL-state standard.
- **DAF role.** Engineering governance and AI-agent provenance for the team building the DAF platform. That is useful for an auditable AI-assisted SDLC, but it is a delivery-process tool, not a runtime governance product for grants or donors.
- **Risks.**
  - Very high release cadence. Its own tests use a custom harness rather than a standard framework.
  - The README install path pipes a remote script to `sh`.
  - Its own pilot language (echelon-foundry README): "The operating system is itself under evaluation. Do not infer that Echelon Foundry is a validated discipline, method, or product merely because the repository follows a rigorous process."

### 3.8 Echelon Knowledge Store

- **Status.** "**Status:** research phase… No stable schema, no released packages."
- **Code.** About 5k F#. The `eks` CLI does `validate`, `compile --out` (writes `index.md`, `records.jsonl`, `diagnostics.json`, `precomputed.json`, `manifest.json`), `verify`, `query`, `explain`, `context`, and `evidence`.
- **Finding** (executive report, "PARTIALLY COMPLETE"): "keep Markdown with front matter canonical… compile it… Do not replace it with a new format." It explicitly rejects a "graph DB, service and central repository."
- **What the experiment found.** "compiler feedback did not prevent fabrication" by agents, but an explicit integrity policy did. The tests covered one model family only, with no multi-step tasks.
- **DAF role.** This is the closest match to "structured knowledge compiled to machine-readable artifacts". It is a research prototype about three days old (commits 2026-11-16..17). Treat it as a design input, not a dependency.

### 3.9 Echelon Foundry (standards source)

The repository is the company website plus a Praxis pilot. Its project charter is draft: "Intended users: Not yet established… First bounded outcome: Not yet selected." Its standards are covered in §4.

### 3.10 Echelon Engineering System

A static F# site that documents the architecture (572 lines F#). It notes: "Essential content has no JavaScript application runtime and does not require WebAssembly. Limen is intentionally absent until a stateful browser requirement justifies it." That is a useful precedent: the ecosystem itself does not apply WASM by default.

### 3.11 Echelon Diagnostic Framework

- **What it is.** A specification and research corpus with no runtime.
- **Its own maturity statement.** It "does not yet establish cross-executor reproducibility, incremental value over matched neutral structure, evidence-sensitive updating, better intervention quality, or routine-use speed/learnability." The confirmatory experiment EX-EDF-001 is preregistered but "intentionally blocked".
- **Use.** Usable as a structured diagnostic vocabulary. It must not be presented as a validated method.

### 3.12 Echelon Design System

Echelon's own brand and theme for Forma (theme 1.1.0). Status: "owner approval pending… Do not publish candidate values as final brand tokens." A DAF would use its own brand theme on top of Forma, so this repository is not a DAF dependency.

### 3.13 Echelon Registry

- **What it is.** A normative specification with JSON Schemas (`echelon.system/v1,v2`, `echelon.release/v1,v2`, profiles, resolved release sets).
- **Invariant:** "An Echelon system MUST remain installable… and able to perform its core functions when any optional Echelon provider is absent." Capability resolution is `available` / `unavailable` / `misconfigured`.
- **What it is not.** A running service. It is a Git-hosted catalog with validators.
- **DAF role.** A good *pattern* for optional-capability integration and supply-chain release metadata. It is not infrastructure.

### 3.14 Conditor

- **What it is.** An F# CLI (about 22.9k lines) that turns `conditor.json` into a deterministic install plan. It installs pinned Echelon lifecycle components, verifies them, and writes `.conditor/lock.json`. Scaffolds include `fsharp-nuget-library` with Trusted Publishing release workflows.
- **Scope.** "Its first target is the Indy Init demonstration."
- **DAF role.** Only relevant if the delivery team adopts the Echelon toolchain wholesale.

## 4. Architectural constraints from Echelon Foundry standards

**The search found no Foundry standard that mandates F#-first, WASM-first, a modular monolith, or Kubernetes/Terraform.** The search grepped all Markdown across the 14 repositories for "F#-first", "WASM-first", "modular monolith", "Kubernetes" and "Terraform".

The canonical Foundry standard is `echelon-foundry/docs/00-governance/Engineering-Standards.md` (GV-ENG-001 v1.2.0, status canonical). It says the opposite of a stack mandate:

> "No stack-specific standard is canonical in Phase 1 because the repository contains no implementation or supported stack evidence."

Its constraining principles are generic: "Prefer clarity over cleverness, simple solutions before abstractions, explicit contracts, reversible evolution, and evidence-driven architecture." A `DF-` decision record is required for "system boundaries, persistent data shape, public contracts, security model, core dependency/platform…" The definition of done requires the final state to be "committed, pushed, and recorded as a verified durable checkpoint."

Stack-related statements exist elsewhere, but **each is scoped to one repository, not the enterprise**:

| Source | Text | Scope |
|---|---|---|
| `echelon-design-system/README.md` §Governance | "F# first and WASM-first where applicable." | That repository's governance |
| `echelon-knowledge-store/AGENTS.md` | "**F# only** for implementation code… Write functional F#: immutable data, pure functions, effects at the edges." | That repository |
| `echelon-knowledge-store/AGENTS.md` | "**No new infrastructure** (no database, Kubernetes, Terraform or service) without recorded evidence that it is needed." | That repository |
| `praxis/research/requirements/RQ-ROS-2026-A031` | "Do not mandate Kubernetes or external orchestration." | Praxis visual-evidence verification |
| `praxis/requirements/SHARED-APPLICATION-FOUNDATIONS.md` | Native boundaries "MUST use Aegis for unexpected operational failure"; web UI "MUST consume a pinned Forma release"; Folio required once printable surfaces exist; "Shared dependencies MUST use released versions or immutable artifacts." | Praxis, plus the URL-state section, which is declared "portfolio-wide… every Echelon web application" |
| SAF-URL-5 (same file) | URLs never carry "names, e-mail addresses, government or tax IDs, account or card numbers"; reserved parameter names are refused | Portfolio-wide web standard. Directly relevant to donor and financial data. |
| SAF-URL-6 | Static hosting uses hash-mode routing | Portfolio-wide web standard |
| `.sde/architecture/FOUR-TIER-ARCHITECTURE.md` (Ordo/SDE doctrine, vendored) | Tier 1 Semantic Model "Must not know about: Postgres, HTTP, JSON, frameworks, browser APIs…"; Tier 4 Host "Owns database, network… and WASM/browser interop." Status: "`supported` theory… REQUIRED as SDE's canonical architectural layering." | SDE-governed repositories. Evidence is drawn from one application (HelixNote). |
| `echelon-engineering-system/README.md` | "Limen is intentionally absent until a stateful browser requirement justifies it." | Practice example: WASM only when justified |

**Implications for the DAF architecture.**
- An "F#-first / WASM-first / modular monolith / Kubernetes+Terraform" posture **cannot be justified by citing Echelon Foundry standards**. Those standards are either silent or scoped to single repositories.
- The closest real constraints are four:
  1. **Domain core free of infrastructure** (SDE four-tier).
  2. **Pinned, released, immutable dependencies.**
  3. **URL-state and no-sensitive-data-in-URL rules.**
  4. **Evidence before new infrastructure** (EKS's rule against Kubernetes/Terraform without recorded need, which is local but indicative).
- If the DAF adopts F#, WASM, a modular monolith or Kubernetes/Terraform, record each as a DAF architecture decision with its own evidence. Do not record it as inherited from Foundry.

## 5. Recommendations for a regulated financial/charitable (DAF) system

Recommendations assume the system handles donor PII, gift and grant funds, IRS substantiation, and AML/OFAC screening, and needs auditability.

| Component | Recommendation | Rationale / conditions |
|---|---|---|
| Forma | **Evaluate-later**, closest to safe | CSS/HTML only, well tested, easy to fork or replace. Safe to adopt only after the PolyForm NC licensing question is resolved, and with a pinned version and a vendored copy. |
| Limen | **Evaluate-later** (front-end only) | Real and tested, but 0.x with an unstable protocol. Never treat it as a WASM execution or sandbox layer. If adopted, isolate it behind the app's own UI boundary so it can be replaced. |
| Folio | **Evaluate-later** | Viable for HTML→PDF templates. Requires a PDF/A and archival-determinism assessment before it produces tax-receipt or legal documents. |
| Aegis | **Evaluate-later** (resilience pattern only) | Small and dependency-free, but **not security**. Do not count it toward security, audit or compliance controls. Database adapters do not exist in this repository. |
| Praxis | **Evaluate-later** (SDLC governance only) | Potentially valuable for AI-agent provenance in the delivery process. Must not sit in the runtime path. Assess its repository footprint and how fast its releases change before adopting. |
| Dokimos | **Evaluate-later** (SDLC only) | Code-quality evidence. Provides no compliance verification for business rules. |
| Conditor | **Do-not-depend** (for the DAF runtime); optional dev convenience | Bootstraps Echelon repositories. Not needed for a DAF architecture. |
| Echelon Registry | **Do-not-depend** as infrastructure; **reuse as pattern** | Spec only. Borrow the capability-resolution ideas (`available`/`unavailable`/`misconfigured`) and the release-manifest ideas. |
| Echelon Knowledge Store | **Do-not-depend** (track as research) | Research phase, no releases, unstable schema. Its finding (compile governed Markdown, don't replace it) is reusable as a design idea. |
| Forma Studio | **Do-not-depend** | Version 0.0.0, a design-time tool. |
| Echelon Design System | **Do-not-depend** | Echelon's own brand. Not applicable to the DAF. |
| EDF | **Do-not-depend** as validated method; may use as optional vocabulary | It states its own claims are not yet validated. |
| Echelon Foundry / Engineering System | **Reference only** | Standards text and documentation. Cite accurately (see §4). |
| clarity-framework | **Not inspected** | Private. Rely only on the pinned summary and mark it unverified. |

**Safe-to-depend** for a regulated runtime: **none of the components today.** Every component falls short on at least one of these:
- non-commercial licensing that is ambiguous for some DAF sponsor types;
- a single maintainer with predominantly AI-authored commits;
- 0.x or weeks-old history;
- no independent production use;
- no security review evidence;
- CI pass status unverified in this inspection.

**Mitigations if the business still chooses to use them:**
- pin exact versions and vendor the artifacts;
- keep every component behind an application-owned interface;
- obtain a commercial license or written confirmation of charitable-use eligibility;
- run an independent code and security review;
- keep a documented exit plan, such as plain CSS for Forma and an in-house PDF renderer for Folio.

## 6. Capability gaps: what the architecture must NOT assume exists

| Assumed capability | Reality |
|---|---|
| A WASM execution or sandbox runtime (Limen) | Not present. Limen is a TypeScript browser kernel with F#/.NET WASM *consumer* examples. |
| A security, authn/authz or secrets layer (Aegis) | Not present. Aegis handles operational faults. Security is attributed to "Tutela", which was not inspected. |
| Compliance or regulatory verification (Dokimos) | Not present. Dokimos measures code quality. |
| A reporting or analytics engine (Folio) | Not present. Folio provides print-layout components. |
| A knowledge base service or graph (EKS) | Not present, and explicitly rejected ("reject… graph DB, service and central repository"). |
| A service registry or discovery runtime (Echelon Registry) | Not present. The registry is a specification plus Git-hosted catalog. |
| Foundry mandates for F#/WASM/monolith/K8s/Terraform | Not present (see §4). |
| Database adapters for Aegis | Out of scope for the repository: "built elsewhere". None were inspected. |

## 7. Open questions

1. **Licensing.** Does the intended DAF operator qualify as a "charitable organization" under PolyForm NC? What will the "forthcoming" commercial terms be, and on what timeline? What license applies to echelon-design-system and echelon-engineering-system, which have no LICENSE file?
2. **CI health.** Are the CI workflows passing on `main` for each component? This needs GitHub API access the session did not have.
3. **Package publication.** Do NuGet and npm artifacts exist with provenance and attestations (Aegis.Core 1.0.0, Limen 0.9.1, Forma 1.0.2, Dokimos, Praxis)? Registries were not queried.
4. **Tutela.** What are its scope, repository visibility and maturity? It is the security component referenced by Dokimos, Conditor and Folio.
5. **Release cadence.** Is there a stability or LTS policy? Praxis had 11 minor releases in about two weeks, and Forma renamed its namespace at 1.0.
6. **Maintainership.** Is there any second human maintainer, bus-factor plan, or security-disclosure process (`SECURITY.md` was not observed in the READMEs reviewed)?
7. **Folio output.** Does it produce PDF/A or tagged, archivable PDFs suitable for IRS substantiation records?
8. **Database adapters.** Do Aegis database adapters exist anywhere, and has any Echelon component been used with a relational system of record?
9. **clarity-framework.** What does it actually contain and how mature is it? It is private and was not inspected.
10. **External adoption.** Is there any production deployment by an organization other than the author?
