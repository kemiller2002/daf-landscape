# 03 - Charity data licensing and access

Status: research (2026-11-26; revision 2 after adversarial review, see [20](20-adversarial-review.md)). Not legal advice: licence readings below are research findings and **require counsel confirmation before any commercial reliance** (OQ-007, OQ-008). Builds on prior terms work in `research/mission-2026-11-14/b43n26-03-charity-data-terms-ai.md` (Candid and Charity Navigator AI/ML clauses) and PR #88 ([04](../competitive-advantage/charity-network-and-onboarding/04-authoritative-charity-data-inventory.md)).

## 1. Licensing classes

| Class | Sources | What a commercial DAF platform may do | Evidence |
|---|---|---|---|
| **Public domain / US government works** | IRS files (17 USC 105), OFAC SLS, trade.gov CSL, FAC, USAspending, IRS written determinations, CourtListener bulk, CO business entities (explicit dedication). 17 USC 105 does **not** cover state sources: CA AG, NY AG and other state registries carry state-specific terms and need a licence row each (CHL-055). Third-party archives of IRS files (e.g. Urban Institute NCCS) carry their own terms; ingest from the IRS for production | Ingest, store, transform, redistribute, use in automated decisions and AI processing | VERIFIED-FACT (High) |
| **Open with attribution** | UK Sanctions List (OGL v3), Ireland register (CC BY 4.0), NZ register (CC BY 3.0 NZ), CCNI (OGL) | Same, with attribution | VERIFIED-FACT |
| **Open, no rights reserved** | GLEIF (CC0), Wikidata (CC0) | Same; GLEIF implies no endorsement | VERIFIED-FACT |
| **Public but field-restricted** | SAM.gov (D&B-derived fields: no bulk dissemination) | Use exclusion facts; do not redistribute D&B fields in bulk | VERIFIED-FACT |
| **Share-alike** | GivingTuesday 990 data (ODbL/DbCL); OpenCorporates free tier | Internal use possible; any **public derivative database** must be released share-alike. Avoid in a resold layer | VERIFIED-FACT |
| **Non-commercial** | OpenSanctions (CC BY-NC; compliance screening counts as commercial; reseller licence for embedding; price on quote); ProPublica NPE (CC BY-NC-ND; commercial fees possible; Data Store bars redistribution and resale) | Not without a paid licence | VERIFIED-FACT (ProPublica via search-index copy: Medium) |
| **Proprietary / contractual** | Candid APIs and Charity Check; Charity Navigator API (AI/ML consent clause, calculation ban; prior b43n26-03); MSRB EMMA feeds; Official Catholic Directory; state paid bulk data (GA $1,000; IN $9.5k+ to reconfirm) | Per contract; assume no redistribution and no AI training without consent | VERIFIED-FACT / UNKNOWN prices |
| **No licence found** | BBB WGA (give.org), ECFA, CoF National Standards list, Fiscal Sponsor Directory, NASCO reports | Link out or cite manually as evidence; do not ingest for redistribution | VERIFIED-FACT (absence of licence) |

## 2. AI use

No new source names AI or ML use in its terms, except where commercial use is barred anyway (OpenSanctions) and BBB's separate AskGive.org AI terms. Candid and Charity Navigator already restrict AI/ML use (prior b43n26-03). **Working rule (RECOMMENDATION, DEC-004):** public-domain and open-licensed data may be processed by AI; proprietary and non-commercial sources may not be used to train or prompt models in a commercial product without a written licence.

## 3. Consequences for architecture

1. **Separate a redistributable shared layer from per-sponsor licensed enrichment.** A shared multi-sponsor registry ([05](05-charity-registry-economics.md) RA-4) may hold only public-domain and open-licensed facts. A sponsor that licenses Candid or Charity Navigator attaches that evidence to **its own** decisions; it is not pooled.
2. **Store provenance and licence with every fact**, so an export, an API response or an AI prompt can be filtered by rights at query time (TRN-REQ-ST-001 already requires a rights policy per raw input; SRC-006).
3. **A commercially enriched registry (RA-5) is a licence decision, not a data decision.** Prices are not published (ASSUMPTION $25-150k a year, RP-12). It reduces exceptions only modestly in the model (auto-resolution 0.4 vs 0.3) and its terms limit reuse.

## 4. Access constraints

| Constraint | Effect |
|---|---|
| Rate limits (SAM exclusions API 10/day on personal key; CourtListener 5/min) | Use bulk extracts, not per-query APIs |
| Keys and accounts (FAC api.data.gov key; SAM) | Free; operational dependency only |
| Outages (IRS 990 bulk page, Nov 2025) | Archive every release; treat absence of a new file as "unknown", not "no change" |
| Blocked hosts in this session (Florida Sunbiz; Ireland and NZ regulator sites; cfo.gov) | Not verified here; recorded in [21](21-evidence-gaps.md) |
| Per-state paid bulk data | Only for states a sponsor's policy requires (RC-05 optional) |

## 5. Can information be obtained independently of commercial vendors?

**Yes for status facts; no for the full determination or for opinions.** Public charity status, revocation, sanctions and exclusion facts are free and redistributable. The legal minimum for a DAF grant also needs non-public facts in some cases (supporting-organization donor control under 4966(d)(4), expenditure responsibility, equivalency, governmental units), so "free data suffices" is true only for the status layer (CHL-036, CHL-050). Candid's and Charity Navigator's value lies in curated, charity-supplied and analytical content that is licence-restricted; it is optional enrichment, not a dependency.
