# Knowledge architecture and IP protection for the DAF research

**Date:** 2026-11-21.

**Facts checked** on 2026-11-21:
- GitHub API;
- the repository tree;
- `kemiller2002/echelon-knowledge-store` at `35d9cee`: `README.md`, `research/2026-knowledge-representation/strategy/*.md` and `docs/decisions/0001-license.md`.

## 1. Current state (facts)

| Item | Finding |
|---|---|
| Repository visibility | **Public** (`private: false`). Created 2026-11-11. 0 stars, 0 forks, 0 watchers on 2026-11-21. The owner confirmed on 2026-11-21 that public is acceptable for all material, including the commercial package |
| Licence | **None.** No LICENSE or NOTICE file, and the GitHub API reports `license: null`. Under default copyright the text and datasets are viewable but carry no reuse grant. The underlying facts (990 figures, statutes, public pages) are not copyrightable, so this protects expression and compilation only [I; not legal advice] |
| Echelon licence policy | Other Echelon repositories use **PolyForm Noncommercial 1.0.0** with a standard NOTICE. EKS ADR 0001 lists aegis, arca, dokimos, fides, forma, mercatus, percepta, praxis and signal; echelon-diagnostic-framework is MIT |
| Size | 411 commits. About 430 research documents (1.6m words) and about 800 CSVs. Repository size about 42.8 MB per the API |
| Structured knowledge already present | Evidence registers with IDs (DE, INV, DS, CP, PS/PW/PV, V-wave registers). Validation registers covering 2,500+ rows. Research priority queue with a scoring script. Clarity and EDF claim states and confidence labels. Validators (`dafcp_validate.py`, `commercial_validate.py`, `mission_validate_grant_record.py`). Source monitors (`mission_watchlist.py`, `mission_terms_monitor.py`, `mission_link_health.py`, `owner_refetch.py`) |
| Missing | No YAML front matter on research documents. No machine-readable *findings* registry linking conclusions to evidence IDs and to the files they supersede or contradict. No generated index. Superseding happens through appended "Validation corrections — governing" prose sections, which agents and readers must reconcile by hand |

## 2. What can and cannot be proprietary

| Asset | Already public? | Protectable? | Commercial value lies in |
|---|---|---|---|
| Underlying facts (990 lines, audits, statutes, vendor pages) | Yes, from their sources | No (facts) | — |
| Computed datasets (vendor footprint, fee censuses, exception proxies, cost structure) | **Yes, published in this repository** | Thin compilation copyright at most; competitors can recompute from the same filings | **Freshness and maintenance**: re-harvesting each 990 cycle, catching changes first |
| Methods and scripts | Yes (public repository) | Code copyright; no licence granted | Speed of reproduction for Echelon rather than exclusivity |
| Conclusions and synthesis | Yes | Ideas are not protectable | Trust, track record, being first |
| Validation registers and provenance | Yes | — | Credibility. Rare in industry research and hard to fake |
| Prospect profiles and commercial plan | Yes (owner accepted) | — | Low as IP; the value is in executing them |
| **Not yet created**: client-specific engagement data, consented operating benchmarks, interview notes, contract terms | No | Contractual confidentiality | **This is the only durable proprietary asset class open to Echelon.** It must never enter this public repository |

**Implication [I].** Publishing the research makes it a marketing and credibility asset rather than a saleable information asset. Anything a buyer pays for must be one of three things:
1. **fresher** than the public repository (monitoring, alerts);
2. **applied** to the buyer's own situation (consulting, assessments);
3. built on **non-public data** collected under contract (benchmarks, interviews).

## 3. Recommended architecture (aligned with EKS findings)

The EKS research (2026-11-16) found that Markdown with YAML front matter, compiled into registries, gives the best agent results. It rejected a graph database, a custom DSL, F# storage and JSON as the source format. This repository should follow that recommendation rather than invent its own.

| Capability | Recommendation | Lives in |
|---|---|---|
| Findings registry | Add one Markdown file per material finding, with front matter: `id`, `status` (claim state), `confidence`, `supports`, `contradicts`, `supersedes`, `superseded_by`, `supporting_evidence` (evidence IDs) and `as_of`. The Praxis field names are used. Start with the top-10 findings in this audit and the governing corrections | `daf-landscape/findings/` |
| Evidence records | Keep the existing CSV registers. Add stable IDs where any are missing | `daf-landscape/data/` |
| Provenance | Keep URL, access date, tag and validation wave per row (already practised). Add content hashes for snapshots that are fetched (practised for syllabi and terms snapshots) | daf-landscape |
| Change tracking | Turn governing correction sections into `superseded_by` links in the findings registry. The compiler then derives the current authority, as in EKS stage 1 | EKS compiler |
| Compiler and validation | Run the EKS / Praxis compiler (`eks validate`, `eks context`) over daf-landscape once findings carry front matter. Keep the domain validators in daf-landscape | Reusable: echelon-knowledge-store. Domain rules: daf-landscape |
| Source monitoring | Generalise `mission_watchlist.py`, `mission_terms_monitor.py`, `mission_link_health.py` and `owner_refetch.py` into one scheduled monitor that emits change records | Generic monitor: Echelon system. DAF target lists: daf-landscape |
| Agent interface | `eks context <finding-id>` task packages for agents answering client questions. No hosted service yet (EKS rejected a service) | EKS |
| Integrity policy | EKS write-path trials showed agents fabricating sources even with compiler feedback, and an explicit integrity policy prevented it. Add that policy to this repository's agent instructions before agents edit findings | daf-landscape `AGENTS.md` / `CLAUDE.md` |
| Access control and licensing | **Owner decision.** Add PolyForm Noncommercial 1.0.0 plus NOTICE for consistency with Echelon policy. Commercial use by others would then need a licence. Keep client and engagement data in a **separate private repository** | Licence: daf-landscape. Private data: a new private repository (needs the owner to create it) |

## 4. Risks

- **Public by design, so competitors can copy.** The mitigation is speed and maintenance, not secrecy.
- **Engagement data leakage.** Any consulting work must start with a private repository and a rule that confidential data never goes into daf-landscape.
- **Fabricated provenance by agents** (EKS finding). Mitigated by the integrity policy plus validators that resolve evidence IDs (the DAFCP and commercial validators already do this).
- **Licence absence.** Others' commercial reuse of the expression in this repository is legally unclear. An owner decision is needed.

## 5. Decisions needed from the owner

1. Add a PolyForm Noncommercial licence, or another chosen licence, to daf-landscape.
2. Create a private repository for engagement and interview data before any client work begins.
3. Approve a pilot findings registry (top-10 findings) compiled with EKS.
