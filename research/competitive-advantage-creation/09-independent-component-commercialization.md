# 09 - Independent component commercialization

Status: research (2026-11-26). Track G. Agent key FGJ. Register rows: `data/fragments/FGJ/` (P3-CLM-FGJ001..007, 019; P3-HYP-FGJ003, 007; P3-ASM-FGJ010..015; P3-CMP-FGJ006..010; P3-SEQ-FGJ001..003; P3-DEC-FGJ001..002; P3-GAP-FGJ003, 004, 009, 010). The component inventory with heads, tags and licences is in `data/evidence/FGJ/component-inventory.csv`. Sources: shallow read-only clones of the 19 component repositories (P3-SRC-FGJ001), the Unbound capability assessment of 2026-11-24 (P3-SRC-FGJ002), Transitus (P3-SRC-FGJ003) and Praxis (P3-SRC-FGJ004), plus public pricing evidence (P3-SRC-FGJ020..025). No builds or tests were run, and the GitHub Releases API was unavailable, so maturity rests on git tags and each repository's own status text.

## Answer

1. **The brief's candidate list does not match what the repositories contain.** "Audit-ready logging (Vigila)" does not exist: Vigila is a personal and business **task organizer** at greenfield-pilot stage (P3-CLM-FGJ001). Every DAF-specific candidate is still research or requirements: charity intelligence, migration (Transitus, phase 0), reconciliation, compliance evidence (echelon-assurance, design-stage) and due diligence (research) (P3-CLM-FGJ004). The only components close to sellable are **general-purpose developer tools** (P3-CLM-FGJ005).
2. **Nothing can be sold today.** Almost every component is under PolyForm Noncommercial 1.0.0 with commercial terms "forthcoming" (P3-CLM-FGJ002). The same gate blocks Unbound's own commercial launch (CNV-GOV-007). Echelon Foundry owns all the property it makes (OD-P3-01, 2026-11-26). The gate is therefore the owner's publication of terms, not a third-party licence. External buyers will still require executed written terms, escrow and continuity (P3-CHL-REV1023, P3-CHL-REV3034).
3. **No component can finance Unbound.** The evidence supports $0-$50k a year from component licences at 24 months (P3-CLM-FGJ019), against a G0 of $0.15-0.35M. Seq F fails as a funding route (P3-SEQ-FGJ003).
4. **What components can do is cheaper and more useful than revenue.** Publishing commercial terms is required for Unbound anyway, costs almost nothing, and creates **credibility and diligence evidence**. Public, reproducible repositories show how Echelon builds, which a channel partner's technical review can inspect (P3-HYP-FGJ006).
5. **Short list:** (a) self-serve commercial licences for released developer components, with no SLA and no sales effort; (b) charity eligibility evidence and Transitus migration/reconciliation as **modules and pre-sales tools inside the Unbound partner offer**, not as standalone products; (c) echelon-assurance and echelon-due-diligence as **internal evidence engines** for partner and sponsor diligence. Everything else goes on an explicit "do not commercialize now" list (P3-DEC-FGJ002).

## 1. What each component actually is (verified 2026-11-26)

| Component | Actual purpose (from README/charter) | Maturity | Licence | Unbound Release 1 role (P3-SRC-FGJ002) |
|---|---|---|---|---|
| Strata | Declarative PostgreSQL schema management: compile, diff, judge, deploy | **Pilot**, v0.1.1; PG16 only; signed native binaries; README reports its own unflattering measurements | PolyForm NC | Schema governance where versions match; virtualization (STRATA-DIV-001) is requirements only |
| Vigila | **Task organizer** for personal/business follow-ups and reminders (not audit logging) | Greenfield pilot; no slice selected; no tags | PolyForm NC | None |
| Forma | Zero-runtime, brand-neutral design system (HTML/CSS, tokens, accessibility contracts, brand manifests) | v1.1.0, 21 tags; 28 required components unimplemented | PolyForm NC | UI foundation |
| Folio | Print component system (light-DOM elements, print CSS) for paper/PDF documents | v0.4.3; no renderer or PDF engine | PolyForm NC | Document markup; PDF pipeline is Unbound-owned |
| Limen | Browser kernel plus JSON protocol that separates browser capabilities from application authority | v0.9.1, npm; 0.x protocol may change | PolyForm NC | Hosting boundary |
| Conditor | Installer/scaffolder that builds a governed repository from a manifest with pinned components and a lock file | v0.10.30, 43 tags; native binaries | PolyForm NC | Installation and pinning |
| Fides | Echelon SSO boundary: stateless OAuth exchange plus F# WASM client; **GitHub is the only identity provider** | v0.2.0; nothing deployed | PolyForm NC | Not used for donors or sponsors |
| Signal | Deterministic URL-first survey and assessment engine; also a trial of ROS/Ordo/Limen | No tags; status file says no slice, but 277 .fs files exist (P3-GAP-FGJ010) | PolyForm NC | None |
| Summa | Project-administration hub over ROS repositories, plus Summa.Ledger, a pure F# AR/invoice/payment ledger for Echelon's own billing | First invoice/payment slice runs as a test; contracts tag only | PolyForm NC | None |
| Chrona | Business time recording and billable-time publication (rebuild of a legacy app) | Domain built on Arca; no tags | PolyForm NC | None |
| Aegis | Operational fault capture, redaction, recovery and presentation for .NET (not security) | NuGet packages (1.0.0 per P3-SRC-FGJ002) | PolyForm NC | Fault handling |
| Ordo | State-Directed Engineering methodology and CLI | v1.20.0, native distribution | PolyForm NC | Engineering method |
| Tutela | Security engineering discipline: threat to invariant to control to evidence to release posture; F# posture gate | v0.1.0 foundation | PolyForm NC | Security method, immature tooling |
| Arca | Shared data layer storing authoritative records **in GitHub repositories**; WASM offline queue | v0.7.1; release assets, not yet on nuget.org | PolyForm NC | Not fit for a regulated ledger |
| Dokimos | Evidence-based code-quality measurement with immutable longitudinal observations | dokimos-v0.11.1; public site generated from its own evidence | PolyForm NC | Acceptance evidence (partial) |
| Mercatus | Echelon's own evidence-driven sales and marketing system (not a CRM) | Domain core only; no host or UI | PolyForm NC | None |
| echelon-assurance | Organizational assurance programme: unified requirements, control catalogue, evidence architecture (SOC 1/SOC 2 first) | **Design-stage**; no control above Designed; no compliance claim | No LICENSE file; confidentiality rules | Assurance design; Unbound is the first reference implementation |
| echelon-knowledge-store | Research on delivering repository knowledge to AI agents (keep Markdown canonical, compile it) | Research; no schema or packages | PolyForm NC | None |
| echelon-due-diligence | Evidence-backed knowledge base for customer due-diligence, vendor-risk and security questions (Unbound first) | Research; "nothing here is a customer-facing claim" | No LICENSE file | Diligence evidence |
| Transitus | Proposed embeddable F# data-integration engine (ingest, raw evidence, staging, mapping, reconciliation, domain-API load, verification) | **Phase 0**: 152 proposed requirements, no production code; HEAD f39ff4b (later than the BRIEF baseline d1b97be) | MIT, pending portfolio policy (OQ-12) | Canonical import and rehearsal (DEC-011) |
| Praxis | Repository operating system: work protocol, research records, provenance, validation, CI | Released, 40 tags, native distribution | PolyForm NC | Requirements governance (import deferred) |

**Corrections to the brief's framing.** Vigila is not audit logging. Aegis is not security. Fides and Arca are tied to GitHub, so they are unsuitable for external regulated customers. Summa holds a small ledger, but it is Echelon's own billing ledger, not a fund-accounting product.

## 2. Assessment of every Track G candidate

Revenue ranges are **assumptions** (P3-ASM-FGJ010..015) unless a price source is cited. "Strategic value" means value to Unbound.

| Candidate | What exists | Target market / buyer | Problem severity | Competitors and pricing (public) | Distribution | Required development | Support / security / regulatory | Marginal cost | Revenue range (24 months) | Strategic value to Unbound |
|---|---|---|---|---|---|---|---|---|---|---|
| **Transitus migration tooling** | Requirements only (phase 0) | DAF sponsors migrating; administrators | High at migration time, rare otherwise | Generic ELT is cheap (Fivetran, Airbyte; SRC-005); receiving vendors scope free; Foundant free PoC (CHL-068) | Only through a platform sale | Phase 1 engine + packages (DEC-011) | Handles donor PII; security review before install (CHL-070) | High per engagement | $0 standalone (P3-ASM-FGJ013) | **High as pre-sales and onboarding**, not revenue (Phase II 16 s.4) |
| **Charity intelligence / eligibility evidence** | Requirements and Phase II design; registry not implemented | Sponsors, administrators, CSR/employee-giving platforms | Medium (vetting is mandatory, but alternatives exist) | Candid Charity Check from $2,750; Essentials from $4,800 (P3-CLM-FGJ006); free IRS data (CLM-001) | Direct or inside Unbound | Registry, API, licensing controls (DEC-004) | Media/defamation exposure if publishing; 4966 reliance questions (CHL-036) | Low per customer once built; $90-170k/yr run cost (CLM-004) | $0-$45k (0-3 customers x $2.75k-$15k) | **High as a module**; weak alone (CLM-028) |
| **File ingestion** | Research (SRC-004) and Transitus requirements | Sponsors, administrators | Medium | Flatfile ~$9.8k median; OneSchema ~$19.9k-$38.7k (P3-CMP-FGJ010) | Inside platform | Transitus formats/checks | PII handling | Low once built | $0 standalone | Medium (prevention value) |
| **Financial reconciliation** | Requirements (Unbound, Transitus) | Sponsors at migration; auditors | High at migration; continuing need is met by fund-accounting suites | BlackLine/Trintech-class tools (not priced here); suites' built-in reconciliation | Inside platform; possibly "independent reconciliation report" (untested; SRC-005 F4) | Reconciliation engine + evidence package | SOC 1 relevance if relied on | Medium | $0-$20k (untested assurance-style reports) | High (core of the migration promise) |
| **Compliance evidence generation** | echelon-assurance design-stage; no operating control | Other small software vendors seeking SOC 2 | High for vendors selling to institutions | Vanta, Drata (+SafeBase ~$250M), Secureframe at ~$7k-$30k+ a year (P3-CLM-FGJ007) | Would need its own GTM | Productization of a programme that is not yet operating | Must itself be audited; high trust bar | Medium-high | $0 | **High internally** (Unbound SOC path); none as a product |
| **Operational event analytics** | Phase II event model (EV-E01..25) in F# research model | Sponsors, administrators | Low-medium | BI tools; incumbent reporting | Inside platform | Instrumentation in Unbound | Low | Low | $0 standalone | Medium (proves cost claims later) |
| **Automated requirements validation** (Praxis, Ordo, Dokimos, Conditor) | Released tools | Software teams using AI agents | Medium, new category | Free conventions and OSS (AGENTS.md patterns, scaffolders, SonarQube-class quality tools; not priced here) | Developer self-serve | Docs and packaging | Issue-driven support | Very low | $0-$30k | Medium (credibility, internal productivity) |
| **Decision intelligence** (EDF, Clarity, research models) | Frameworks; EDF MIT; Clarity private | Executives, consultancies | Low-medium | Consulting firms | Founder-led advisory (business plan 05.02 paid diagnostics) | Packaging | Professional liability | High (founder time) | Unknown; competes for founder time | **Negative if pursued now** (distraction) |
| **Audit-ready logging (Vigila)** | **Does not exist** (P3-CLM-FGJ001) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | $0 | None |
| **AI-readable application documentation** (knowledge store, Praxis records) | Research | AI-tooling teams | Low-medium | Emerging and free conventions | Publication | Research outcome first | Low | Very low | $0 | Low-medium (credibility) |
| **Strata** (schema governance) | Pilot v0.1.1 | PostgreSQL teams | Medium | Flyway Community $0 / Enterprise by quote; Liquibase Secure ~$5k/yr; Atlas ~$9/seat/month (P3-CMP-FGJ007) | Self-serve | Multi-major PG support; docs | Issue support; no SLA | Very low | $0-$25k | Medium (validates release pipeline; licence clarity) |
| **Limen / Forma / Folio** | Released 0.x-1.x | Web teams wanting WASM boundaries, white-label CSS, print CSS | Low-medium | Free frameworks (React, Bootstrap, USWDS); Prince $3,800/server and DocRaptor from ~$15/month for PDF (P3-CMP-FGJ008) | Self-serve | Gaps listed in Unbound 07 (embed mount, money component, PDF engine) | Issue support | Very low | $0-$20k | Medium (licence needed for Unbound anyway) |
| **Aegis** | NuGet packages | .NET/F# teams | Low | Free libraries; Sentry-class services (not priced here) | Self-serve | Docs | Low | Very low | $0-$5k | Low |
| **Tutela** | v0.1.0 | Security teams | Medium | Threat-modelling tools (not priced here) | n/a | Large | Credibility risk if immature | Medium | $0 | Medium internally |
| **Fides / Arca** | 0.x; GitHub-bound | Echelon apps | n/a | n/a | n/a | Managed IdP and DB replacements | Not fit for external regulated use | n/a | $0 | None for Unbound (P3-SRC-FGJ002) |
| **Chrona / Summa / Vigila / Signal / Mercatus** | Internal business applications | Small firms (time, invoicing, tasks, surveys, marketing) | Low | Harvest/Toggl, QuickBooks, Todoist, SurveyMonkey, HubSpot class: crowded, low price (not priced here) | Consumer-style SaaS GTM | Hosting, identity, support, billing | Consumer support load | Medium | $0 | **Negative** (pulls focus away from Unbound) |
| **echelon-due-diligence** | Research | Echelon's own prospects; other vendors | High for vendors facing questionnaires | SafeBase (Drata), Vanta/Secureframe trust centers (P3-CMP-FGJ009) | n/a | Productization | Must be truthful by design | Medium | $0 | **High internally** (answers partner and sponsor diligence) |

## 3. Which candidates serve which purpose

| Purpose | Candidates the evidence supports | Comment |
|---|---|---|
| Early revenue | Self-serve commercial licences for Strata, Limen, Forma/Folio, Aegis | Small ($0-$50k a year; P3-HYP-FGJ003 is low-confidence) |
| Finance Unbound | **None** | P3-CLM-FGJ019 |
| Build institutional relationships | Charity eligibility evidence and migration readiness, inside the partner pilot | Relationship value comes from DAF-specific work, not developer tools |
| Validate shared infrastructure | Strata, Conditor, Forma, Limen used by Unbound and external licensees | External use surfaces defects early; it also creates support load |
| Reduce CAC | Migration readiness assessment (free) and published reconciliation evidence | It is CAC itself (Phase II), but it shortens qualification if HYP-004 holds |
| Create reusable evidence | echelon-assurance, echelon-due-diligence, Dokimos, Praxis provenance | Diligence answers built once, reused across partners |
| Add credibility | Public repositories with honest status sections (Strata README; due-diligence "no claim" rule), public research | Credibility comes from candour plus reproducibility, not breadth |

## 4. Challenges

- **Distraction.** Fifteen-plus repositories for a founder-led firm already split attention. Every commercial licence creates an implicit support promise. At the assumed 5-80 hours per licensee per year (P3-ASM-FGJ015), three licensees could cost more founder time than they pay for.
- **Support burden.** Enterprise buyers of developer tools expect SLAs, security questionnaires and indemnities. Self-serve terms must exclude SLAs explicitly, or the economics reverse.
- **Fragmented positioning.** Selling a design system, a schema tool and a DAF platform under one name confuses institutional buyers who need to believe Echelon is a dependable DAF technology vendor. Mitigation: present the developer components as **"the open engineering behind Unbound"** (evidence), not as separate product lines.
- **Licence choice cuts both ways.** A permissive licence would increase adoption and credibility but remove any licence revenue, and it would let incumbents use Echelon components. Noncommercial terms protect optionality but deter adoption. This is an owner decision (P3-DEC-FGJ001), not a research conclusion.
- **Commodity pressure.** Every developer-tool competitor has a free tier (P3-CLM-FGJ005). An unknown entrant's realistic price is near zero until there is adoption.

## 5. Recommendation

**Short list (do now, $0 cash):**
1. Decide the portfolio licensing policy (P3-DEC-FGJ001). Unbound needs it anyway. If the owner chooses, publish self-serve commercial terms with **no SLA and no support offer** for released developer components only. Price at $5k or more if any support is offered. Sequence F has a gross margin of about −18% at the assumed support load (support ~$2,360 against revenue ~$2,000 per licensee-year). Terms are therefore a credibility and diligence measure, not a revenue line, and F should not be read as a ranked commercial option (Revision 2, P3-CHL-REV2028, P3-CHL-REV2042).
2. Keep charity eligibility evidence and Transitus migration/reconciliation as **modules and pre-sales tools inside the partner-embedded Unbound offer** (consistent with DEC-004, DEC-011 and Phase II 16 s.4).
3. Use echelon-assurance and echelon-due-diligence as **internal evidence engines** for V-6 partner diligence. Do not sell them.

**Do not commercialize now (P3-DEC-FGJ002):** Vigila, Chrona, Summa, Signal, Mercatus (internal business applications); Fides and Arca (GitHub-bound); Tutela and Dokimos as products; echelon-knowledge-store (research); echelon-assurance and echelon-due-diligence as products (crowded, consolidating category; no operating controls); charity intelligence as a **standalone** API (Candid floor; CLM-028); Transitus as a **standalone** migration service (DEC-011 scope; no buyer); decision-intelligence consulting (founder time). Revisit only when a named buyer brings a funded problem, or when Unbound reaches G2.
