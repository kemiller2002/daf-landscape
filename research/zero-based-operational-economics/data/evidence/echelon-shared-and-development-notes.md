# Echelon shared capabilities and development records: evidence notes

Last reviewed: 2026-11-27. Companion register: [`../registers/shared-capabilities.csv`](../registers/shared-capabilities.csv) (SC-001..SC-032).

**Method.** I read repositories read-only in local clones under `/home/user/kemiller2002/` and in `/home/user/echelon-organization-administration`. Paths below are relative to those roots, written `repo/path`. Eleven repositories were supplied. I cloned ten more with `--depth 1`: summa, fides, tutela, aegis, vigila, project-administration, chrona, dokimos, signal and echelon-assurance. For unbound and ten component repositories I fetched bounded history with `git fetch --depth=500 origin main`. All of these except conditor reached their root commit. I parsed the Praxis telemetry JSON with Python. I ran no builds or tests. Private `time-tracking-data` was not read.

Evidence labels follow `CONVENTIONS.md`. Where I relied on an earlier daf-landscape claim, I say so and give its status.

---

## 1. Verified component responsibilities

What each component actually does can differ from what its name or an earlier note suggests. These corrections matter for allocation.

| Component | Actual responsibility (verified) | Not responsible for | Evidence |
|---|---|---|---|
| Praxis | Repository operating system. It provides the work protocol, provenance, research and decision records, a telemetry schema and validation. Channel version 3.26.0. | Application runtime. **It is not installed in unbound**: there is no `.ros`, `praxis` or `conditor.json`. | `praxis/README.md`; `echelon-registry/sets/echelon-current/1.43.0.json`; `ls unbound` |
| Conditor | Installs the development environment and pins dependencies from a declarative manifest. | Production deployment. | `conditor/README.md` |
| Echelon Registry | Specification for capability discovery, release manifests and channels (MIT). | Installations and credentials. | `echelon-registry/README.md` |
| Transitus | **Phase 0.** Research, architecture and requirements only: "No production code exists yet". The charter is dated 2026-11-26, and the repo has 9 commits on one day. | Job queue, schema governance, observability. | `transitus/README.md`; `transitus/PROJECT-CHARTER.md`; DF-TRN-2026-0018 |
| Strata | PostgreSQL 16 schema compile, plan, deploy and drift (pilot, v0.1.1). Mock interactions exist only as requirements. | Append-only history and ORM. Unbound owns the ledger (CNV-ARC-004). | `strata/README.md`; `unbound/requirements/PLATFORM-UX-API-AND-ASSURANCE-STANDARDS.md` |
| Forma | Zero-runtime HTML/CSS design system (tag 1.1.0; channel 1.0.1). | JavaScript behaviour, app shell, money input, charts. | `forma/README.md`; `forma/PROJECT-CHARTER.md`; `unbound/requirements/convergence/2026-11-24-master/07-ECHELON-CAPABILITY-ASSESSMENT.md` |
| Limen | TypeScript browser kernel plus JSON protocol, with an F# seam (`limen-fsharp`) and an F# CLI. | **Identity/access**: it has no IdP, sessions or tenant tokens. It also cannot be embedded as a widget. | `limen/README.md`; unbound report 07 §1 |
| Fides | Authentication boundary for **GitHub only**. A stateless exchange runs on AWS Lambda. Nothing is deployed. | Sign-in for donors or sponsors. | `fides/README.md`; DF-FIDES-2026-0001, -0002 |
| Folio | Print markup: 21 light-DOM elements plus print CSS. | PDF engine, batch rendering, PDF/UA. | `folio/README.md`; unbound report 07 §3 |
| Arca | Stores records in GitHub repositories and keeps an offline queue in WASM. | Regulated ledger (CNV-ARC-001 requires PostgreSQL). | `arca/README.md` |
| Aegis | Fault capture, classification, redaction and presentation (.NET). | Security, logging, metrics, alerting. | `aegis/README.md`; RP-REG-2026-0001 |
| Tutela | Security posture model and gate (0.1.0). | Scanning. **None of the 11 CI configurations I inspected runs SAST, dependency or secret scanning.** | `tutela/README.md`; `grep` of `*/.github` |
| Summa | Accounting application for invoicing, AR and the double-entry ledger, with books in the browser or in GitHub. It is in development and **its README is stale**: the README describes a project-administration hub. | DAF fund accounting, tax, payroll. | `summa/research/decisions/DF-SUMMA-2026-0009-*.md`; `summa/context/CURRENT-STATE.md` |
| Chrona | Time-tracking application (in development). | — | `chrona/context/CURRENT-STATE.md` |
| Vigila | Follow-up and task organizer, newly initialized. | Observability. An earlier assumption that it was the observability system was refuted. | `vigila/context/CURRENT-STATE.md`; RP-REG-2026-0001 |
| echelon-assurance | Research and control design for SOC 1/SOC 2. Design stage only. | Any production control. | `echelon-assurance/README.md` |
| Echelon.Execution | Durable command queue and outbox on PostgreSQL. It is **incubated inside unbound** (`unbound/execution`, 2,558 F# lines). It has not been benchmarked on a managed instance and is not deployed. | — | `unbound/execution/README.md` |

**Absent.** No Echelon system covers any of the following:
- monitoring, logging, tracing or alerting (owner decision of 2026-11-25 to defer, RP-REG-2026-0001);
- production hosting;
- donor/sponsor identity;
- customer support or a service desk;
- CRM (Mercatus is a domain model only);
- incident paging. Causa supports investigations only.

**Licensing.** Every component I inspected is PolyForm Noncommercial 1.0.0 except echelon-registry, echelon-foundry, transitus and project-administration (MIT) and echelon-assurance (no LICENSE file). **Unbound has no LICENSE file and no CI workflows.**

## 2. Hosting architecture evidence (for infrastructure pricing)

**A cloud provider has not been chosen for Unbound** [VERIFIED-FACT]:
- `echelon-organization-administration/application-governance/availability-architecture/19-UNRESOLVED-DECISIONS.md`, U-09: "Managed hosting platform (container platform, managed PostgreSQL provider, region) | Not chosen anywhere in Unbound … Owner decision".
- `unbound/requirements/discovery/2026-11-26-file-ingestion/14-QUESTIONS-AND-OWNER-DECISIONS.md`, FIL-OD-01 (open, owner route): the recommendation is a provider with native on-upload scanning, either AWS GuardDuty for S3 or Microsoft Defender for Storage. It notes that "the cloud choice is broader than ingestion". FIL-OD-02 proposes object storage for artifact bytes (ADR-ING-002, `07-STORAGE-ARCHITECTURE-EVALUATION.md`, with AWS and Azure prices measured 2026-11-26).

**Specified shape** [VERIFIED-FACT]:
- **Backend.** "The backend SHALL be F# and WASM-first UI integration SHALL use … Limen and Forma" (UNB-PLAT-006, `unbound/requirements/PLATFORM-UX-API-AND-ASSURANCE-STANDARDS.md:10`).
- **Database and workflow.** CNV-ARC-001 (same file, around line 257) requires:
  - one managed PostgreSQL cluster;
  - a schema and database role per sponsor, with RLS;
  - a transactional outbox and durable process-manager rows;
  - in-database state machines with a timer table;
  - a broker or workflow engine only on measured evidence;
  - RTO, RPO, SLO and a cost envelope benchmarked on a realistic managed instance before acceptance.

  This was ratified by OD-P-PLT cut M (`unbound/requirements/convergence/2026-11-24-master/data/owner-decisions.jsonl`).
- **Provisioning and versioning.** CNV-ARC-005 requires declarative provisioning, with "provider-native templates permitted; no Kubernetes or Terraform requirement", expand/contract migrations and migration state per tenant.
- **Change control.** CNV-PLT-010 requires signed builds, two non-author approvers for control-relevant modules, daily external anchoring of the ledger digest and break-glass database administrator roles.
- **Organization-wide default.** `echelon-organization-administration/policies/engineering/reliability-and-cache-readiness-standard.md` §2: "one F# codebase, modular monolith, one managed PostgreSQL … No mandatory broker, microservices, Kubernetes or distributed cache." The mission restrictions in `availability-architecture/MISSION-BRIEF.md` row 21 exclude Redis, Kafka, RabbitMQ, Kubernetes and Terraform.
- **Benchmark.** The benchmark cited as ADR-EVA-001 measured 2,100–3,900 tx/s on PostgreSQL 16 with 4 vCPU, against about 200 tx/s needed (`availability-architecture/01-CAPABILITY-INVENTORY.md`; `parameters.json` infra_per_account source). I did not re-run it.
- **Queue.** Durable execution is database-first: Echelon.Execution uses `FOR UPDATE SKIP LOCKED`. There is no separate queue service.
- **Only explicit cloud decision anywhere.** Fides DF-FIDES-2026-0001 (user decision of 2026-10-08): "AWS first: Lambda behind API Gateway (HTTP API), with the client secret in Secrets Manager or SSM … Azure stays possible". The context says "The user expects to host on AWS and may host on Azure." This covers Fides's token exchange only, and Fides is not used for Unbound identity.
- **Static sites.** These use GitHub Pages (`echelon-foundry/CNAME` = echelonfoundry.com; `deploy-pages.yml`).
- **Transitus.** Its blob port defaults to PostgreSQL, with S3-compatible or Azure Blob storage opt-in (`transitus/docs/architecture/02-storage-architecture.md:36`).
- **Unbound model placeholders.** `infra_base` is $250k/yr ($150k–600k) and `infra_per_account` is $3.0 ($0.5–6.0). Both are labelled A (assumption) in `unbound/requirements/discovery/2026-11-24-simplification-economics/model/parameters.json:257-273`. They are not quotes.

**Pricing implication** [INFERENCE]: price AWS as the base, since it is the only stated expectation and was preferred for scanning, and treat Azure as an alternative. GCP needs a licensed scanner.

## 3. Development records found (measured)

### 3.1 Unbound git history (full history, `origin/main`)

| Measure | Value [MEASURED-FACT] |
|---|---|
| Commits | 400 (376 non-merge, 24 merges), **2026-11-21 to 2026-11-26, 6 active days** (53, 64, 172, 63, 33, 15 per day) |
| Author identities | Owner account 272; `Claude <noreply@anthropic.com>` 128; no other human |
| Agent signals | 123 `Co-Authored-By: Claude` trailers. Only 1 owner-authored commit carries one. 8 distinct Claude Code sessions appear in trailers. |
| Lines inserted / deleted | 287,796 / 30,986. By extension: JSON 109k, Markdown 63k, CSV 38k, F# 27k, JSONL 12.6k, CSS 12k, Python 10.8k (10.0k deleted) |
| Code at HEAD | 139 `.fs` files, 27,032 lines: `tools/fs` 22,092 (requirements, economics and design tooling), `execution/` 2,558, the rest under `requirements/` |
| PRs | About 14 PRs merged on the owner account (8 "Merge pull request" commits plus squash merges #2, #6, #7, #9, #10, #11). The GitHub API was not reachable, so review comments could not be counted. |
| Praxis / telemetry / CI | **None**: unbound has no `.ros`, no telemetry and no `.github/workflows` |

**What this shows.** Unbound is almost entirely a requirements, research and economic-modelling repository. It has one incubating runtime library (Echelon.Execution) and no product application code. A large output was produced in six calendar days, mostly by agent sessions.

**What it does not show:**
- human hours;
- review depth;
- accepted capability;
- defect rate.

Owner-authored commits read like agent output, so author identity does not separate human from agent work. The commit hours are spread across 22 of 24 hours of the day, which is consistent with agent sessions and is not a measure of effort.

### 3.2 Shared component repositories (bounded history; conditor is truncated at depth 500)

| Repo | Commits | Span | Active days | Claude-authored | PR merges | Insertions | Tags |
|---|---|---|---|---|---|---|---|
| praxis | 1,438 | 2026-07-22..11-26 | 60 | 783 | 145 | 1,313,712 | 40 |
| forma | 1,050 | 2026-09-22..11-26 | 41 | 301 | 76 | 718,602 | 21 |
| conditor | 849 (shallow) | 2026-09-24..11-26 | 39 | 274 | 106 | 283,778 | 43 |
| limen | 604 | 2026-08-15..11-26 | 26 | 514 | 37 | 487,213 | 13 |
| echelon-registry | 432 | 2026-09-25..11-26 | 33 | 288 | 95 | 257,661 | — |
| folio | 357 | 2026-09-22..11-26 | 22 | 69 | 21 | 144,721 | 5 |
| arca | 196 | 2026-10-08..11-26 | 9 | 145 | 50 | 144,044 | 10 |
| strata | 178 | 2026-09-11..11-26 | 18 | 129 | 19 | 314,780 | 2 |
| echelon-foundry | 96 | 2025-07-07..2026-10-13 | 25 | 19 | 7 | 41,827 | — |
| transitus | 9 | 2026-11-26 | 1 | 7 | 1 | 30,739 | — |

Across these 11 repositories, including unbound, there are 5,609 commits. Authors are 2,781 by the owner (two e-mail identities), 2,657 by Claude, 167 by bots and 4 by OpenAI ChatGPT. **One human identity.**

Method: `git log origin/main` with `--shortstat` and `--numstat`, author e-mail classification, and grep of trailers. Tags were counted with `git ls-remote --tags`.

### 3.3 Praxis execution telemetry (`<repo>/.ros/telemetry/executions/*.json`)

| Measure | Value [MEASURED-FACT] |
|---|---|
| Records | 1,017 across 10 repos: praxis 354, limen 153, strata 124, forma 120, echelon-registry 88, conditor 85, arca 44, folio 40, echelon-foundry 7, transitus 2. **Unbound 0.** |
| Actors | Mostly `agent`. Some legacy records have no actorKind. Runtimes: anthropic/claude-code (majority), openai/codex 80, github-actions 53. |
| Token observations | **7 records** (all in praxis) carry observed token metrics. Everything else is `supported-unavailable` or `unknown`. |
| Cost or human-time metrics | **0 records** |
| Derived metrics | `git.lines_added` and `git.commits_created` (572 records); `time.wall_ms` (1,003). Wall clock is begin-to-finalize time, so it includes idle and abandoned time. It sums to 1,962 h in praxis and 1,228 h in forma because some executions stayed open for days. **It is not effort.** |

The 7 praxis token records sum to 263k output tokens, 154M cache-read tokens and 808 model requests. These are session-scoped snapshots, so the sum may double-count. The earlier study (ai-native-capital-minimization/05) reported 1,687 records with 3 token-bearing. My counts differ because the repo set and date differ. The conclusion is the same: **agent cost is essentially unrecorded, and human time is entirely unrecorded.**

### 3.4 Status of earlier productivity claims

| Earlier claim | Status after primary check |
|---|---|
| "One human author; ~46.5% agent-authored commits" (05) | **Consistent.** In my 11 repos: 1 human identity, 47% Claude-authored (2,657/5,609). |
| "No human time recorded anywhere" (05) | **Confirmed.** Echelon-assurance's operating model also states that one human holds every role. |
| "No repo runs SAST or dependency scanning" (05) | **Confirmed** for the 11 CI configurations inspected. |
| "Echelon contains no DAF capability" (05) | **Confirmed.** Echelon.Execution is generic and incubated in unbound. Transitus has no code. |
| "Development saving $0–1.1M conditional on measurement" (05) | **Not verifiable.** No accepted Unbound capability exists to measure. |
| "Unbound $5M build" | **Still an assumption**: `parameters.json` build_capex 5,000,000 (3M–15M), label A, "assumption". |
| RA-7 "Echelon reliance cost" (competitive-displacement/05) | Built on 05's assumptions. No primary cost record supports it either way. |

## 4. Owner decisions on DAF expenditure, organization, founder time and staffing

**Unbound** (`unbound/requirements/convergence/2026-11-24-master/data/owner-decisions.jsonl`; all by the "Product owner"):
- **OD-M-08** (2026-11-24, "Record as stated"): "one small, nimble core with two offers": (1) DAF software licensed to sponsors and administrators; (2) "an Unbound-operated administration team" competing with Ren's outsourced administration. This changes SPD-ADV-004 to "software first, staffed administration as a planned second offer" and supersedes the OD-M-04 trigger.
- **OD-P-GOV** (+): "SOC 1 Type 2 readiness, including the start of its observation period, is planned to begin before the first staffed-administration client goes live."
- **OD-M-14** (2026-11-25): "No design-partner sponsor will be available"; the owner chose "build it now". Handling-time evidence will come from "an internal time study of Unbound's own team working a synthetic operating year". **No such study has run.** The plan is in `16-SYNTHETIC-OPERATING-YEAR-AND-INTERNAL-TIME-STUDY.md`, which models about 5,350 h/yr (3.3 FTE) for a 10,000-fund sponsor.
- **OD-M-11, OD-M-13**: prices are set "by the Unbound board"; the product owner acts "as Unbound board". No Unbound entity or board exists apart from the owner.
- **Scope cuts in release 1:**
  - OD-P-PLT (cut M: one PostgreSQL cluster);
  - OD-P-PAY (Chariot, then PayPal, as the first payment-partner adapters);
  - OD-M-07 (investment management delegated to an external manager);
  - OD-M-02 (AP, AR, payroll and similar are not in release 1).

**Organization-wide** (`echelon-assurance/docs/decisions/owner-review-direction-2026-11-25.md`, DF-ASR-2026-0D0F): "do not engage legal counsel or purchase recurring independent review … ODP-09: … no external consulting budget authorized now … ODP-11: … defer external engagement decisions … No expenditure or other repository changes authorized." ODP-02: "no fractional reviewer retainer now".

**Staffing and segregation of duties** (`echelon-assurance/governance/operating-model.md`, status proposed):
- "As of 2026-11-25 one human, the owner, holds every accountable role".
- "Escalate to a second hire only when workload or obligations justify it".
- Segregation-of-duties conflicts with one human are recorded as unresolvable.
- DF-ASR-2026-7B20 (proposed) would allow owner approval of agent-prepared work while there are fewer than two humans. Every such owner approval would be reviewed quarterly by a contracted reviewer, assumed at USD 10–30k/yr. This conflicts with the ODP-02 decision not to retain a reviewer now.

**Founder capacity** (`echelon-assurance/economics/v2/README.md`, hypothetical): "One owner has about 1,800 working hours a year, so capacity, not cash, is likely the binding constraint". The proposed limit for assurance labour is 25% of that capacity, about 450 h/yr. Baseline product engineering is 200–500 h/yr per product.

**Observability**: owner decision of 2026-11-25, "do not build an application-observability system yet" (RP-REG-2026-0001).

**Cost centers and budgets** [VERIFIED-FACT, absence]:
- `echelon-organization-administration/portfolio/initiatives.json`: all 30 initiatives have `internal.resourceEstimate: "not estimated"`. INIT-005 (Unbound) has status `research`.
- The business plan sections 06.x and 15.x were template-generated on 2026-08-15 (`business-plan/WORKLOG.md`). They state policy only, with **no figures, headcount, budget or cost centers**.
- The entity values for Echelon Foundry, LLC are all `TODO`: members, capital, IP assignment (`entities/echelon-foundry/formation/entity-values.md`).
- I found **no decision on a DAF commercialization budget amount**, no Unbound entity and no intercompany agreement.

## 5. Proposed allocation drivers

| Shared cost | Driver | Interim proxy until measured |
|---|---|---|
| Founder time | Timer hours by Praxis work item or initiative tag. Chrona and time-tracking-data, if tagged by project. | Share of non-merge commits in the 11 repos inspected. Unbound was **43% over the last 31 days** (376/883) and **65% over the last 6 days** (376/581). It is output, not effort, and covers only 11 of 57+ repos. |
| Agent compute | Provider usage per work item, ingested through Praxis `tokens.*` metrics | None reliable. The current observation rate is 7/1,017. |
| Shared component maintenance | Praxis work items tagged by the requesting product, or by consumer count in Registry and Conditor manifests | Equal split across consuming products |
| Assurance program | Echelon-assurance econ v2 scaling: 1 + (N−1) × scaling per product | N = number of products in production (currently 0) |
| Cloud infrastructure | Metered resources tagged per product, with a separate account or subscription per product. Tenant schemas inside Unbound. | Unbound bears 100%, since no other production app exists |
| Incubated libraries (Echelon.Execution, Transitus) | 100% Unbound until a second consumer exists (ADR-EAR-004) | Same |

## 6. Capacity constraints

- **Founder hours are finite.** About 1,800 h/yr (hypothetical). The owner competes across 30 initiatives (16 active, 14 research), 57 public and 26 private Echelon repositories (`portfolio/repository-inventory-internal.md`), and a consulting practice (INIT-028).
- **Engineering capacity** [INFERENCE]. At 200–500 h/yr of baseline engineering per product, 1,800 h covers only about 3.6 to 9 products before any assurance, sales, legal or management work.
- **Assurance capacity.** The recommended assurance package (A8, 395–1,070 h at N=1) alone can exceed the 25% threshold.
- **Approver capacity.** CNV-PLT-010 requires two non-author approvers on control-relevant modules. With one human this **cannot be met**, so it is a hard staffing requirement before production, not a cost choice.
- **Release churn.** Praxis has 40 tags in 4 months and conditor 43, and the channel has assessed 12 Praxis minor versions. Every consumer pays an upgrade tax, and one maintainer services all of it.

## 7. Risks of the "shared organization" assumption

1. **Shared but absent.** Observability, hosting, identity for donors, support, CRM, incident paging and production deployment have no Echelon provider. They give zero shared saving and must be costed as Unbound-specific or external.
2. **Transfer, not elimination.** Founder and agent time spent on Echelon components is a cost moved onto Unbound. Echelon.Execution and Transitus have Unbound as their only consumer.
3. **Unfit components.** Arca stores data in GitHub, Fides supports GitHub sign-in only, and Folio has no PDF engine. They do not meet Unbound's regulated requirements (CNV-ARC-001, CNV-PLT-003, CNV-EXP-001).
4. **Licensing and entity gap.** PolyForm Noncommercial on most components, plus CNV-GOV-009, blocks production until an executed licence exists. The licensor entity (Echelon Foundry, LLC) is not formed, and IP assignment is `TODO`.
5. **Key person and segregation of duties.** One human holds every role. A regulated sponsor's due diligence and a SOC 1 auditor will treat that concentration as a limitation (echelon-assurance OQ-701).
6. **No measurement basis.** There are no human-time or cost records, and Unbound has no Praxis telemetry. Productivity multiples cannot be grounded in Echelon's own records today.
7. **Version drift.** The registry channel, the tags and Unbound's vendored copies disagree (Forma 1.0.1 / 1.1.0 / untagged; Folio untagged 0.4.2).

## 8. Suggested memory items (for the main session)

- Unbound has no Praxis installation, no CI and no LICENSE (observed 2026-11-27 in the local clone).
- The cloud provider for Unbound is undecided (U-09, FIL-OD-01). The only explicit cloud decision is Fides AWS-first (DF-FIDES-2026-0001).
- Owner direction DF-ASR-2026-0D0F authorizes no consulting, legal or independent-review expenditure.
