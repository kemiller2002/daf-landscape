# 02 - Charity intelligence beyond the BMF: sources

Status: research (2026-11-26; revision 2 after adversarial review, see [20](20-adversarial-review.md)). Public sources only, accessed 2026-11-26. Register: [charity-data-sources.csv](data/registers/charity-data-sources.csv) (68 sources: 30 carried from PR #88, 38 new). Full per-source fields (ownership, accessibility, licensing, cost, coverage, fields, frequency, history, API/bulk, quality, identity-resolution issues, commercial use, operational value, vetting role): [trackA-sources.csv](data/evidence/trackA-sources.csv) and [trackA-notes.md](data/evidence/trackA-notes.md) (SRC-064), plus the prior inventory [04](../competitive-advantage/charity-network-and-onboarding/04-authoritative-charity-data-inventory.md) (SRC-001).

## Answer in brief

1. **A credible status and screening layer can be built entirely from free, commercially usable public data** (CLM-006), covering IRS status, revocation, sanctions and exclusion facts, **but not the full DAF eligibility determination** (CLM-042; CHL-036, CHL-050): governmental units (170(c)(1)), newly recognised charities not yet in the files, supporting-organization donor-control facts (4966(d)(4), certification needed), expenditure responsibility and foreign equivalency all need non-public evidence. The layer is built from: IRS files (BMF, Pub 78, auto-revocation, 990-N, 990 XML), OFAC plus the trade.gov **Consolidated Screening List** (11 US lists, 26,339 rows, daily, no key), the **UK Sanctions List** (OGL), UN and EU lists, **SAM.gov exclusions**, and the **Federal Audit Clearinghouse** (going-concern and material-weakness flags; one of the few public joins of EIN to UEI).
2. **The free layer has three structural holes that no public source fills**: churches and group-ruling subordinates (0 of 237,380 c3 subordinates appear in Pub 78; the Catholic group letter says the IRS does not verify inclusion), state charity registration (about 40 states plus DC; no national dataset; the multistate Single Portal is paused, CLM-008), and identity binding for sources that carry no EIN (state corporate registries, USAspending, GLEIF, most foreign registries).
3. **Third-party ratings and aggregators inform but cannot be redistributed** (CLM-007, report [03](03-charity-data-licensing-and-access.md)).
4. **Automated vetting can rest on eight source families; everything else is evidence a person or a rule cites, not a determination.**

## 1. Source families and their role

| Family | Examples | Authority | Vetting role | Independent of commercial vendors |
|---|---|---|---|---|
| Federal exemption status | IRS BMF, Pub 78, auto-revocation, 990-N, 501(p), revocations | Authoritative | **Supports automated vetting** | Yes |
| Federal filings | 990/990-EZ/990-PF XML; SOI extract | Authoritative (self-reported content) | Supports automated flags (filing presence, Schedule data); content informs | Yes |
| Sanctions and export control | OFAC SLS; trade.gov CSL; UK Sanctions List; UN; EU FSF | Authoritative | **Supports automated screening** | Yes |
| Federal exclusion and audit | SAM exclusions; FAC single audits | Authoritative | Supports automated flags (exclusion; going concern; material weakness) | Yes (SAM D&B fields excepted) |
| Federal spending | USAspending; SAM entity | Official secondary | Informs (no EIN; UEI only) | Yes |
| State charity regulation | CA AG "may not operate"; NY AG; ~40 state registries; NASCO reports | Authoritative per state | CA list supports automation; others inform | Yes; coverage fragmented |
| State corporate status | CO (public domain, dissolved/revoked); NY open data (288,708 not-for-profit corporations); GA paid bulk ($1,000) | Authoritative | CO-style status can flag; others inform | Yes; no EIN |
| Enforcement and litigation | State AG actions; IRS EO litigation; CourtListener (public domain bulk); PACER (fees; $0.12/page from 2027) | Authoritative records | Informs only (name-matched) | Yes |
| Accreditation and directories | CoF National Standards (>500 CFs); ECFA (2,700+ members); Fiscal Sponsor Directory (376 sponsors, 20,566 projects); Official Catholic Directory | Third-party assertion / self-reported | Informs only; OCD is the de facto evidence for Catholic subordinates | No licence found / proprietary |
| Ratings and aggregators | Candid; Charity Navigator; BBB WGA; ProPublica; GivingTuesday 990; Open990 (unreachable 2026-11-26) | Aggregator / assertion | Informs only | No |
| International registries | CCEW; OSCR; CRA; ACNC; Ireland (CC BY 4.0); New Zealand (CC BY 3.0, open OData); CCNI | Authoritative abroad | Informs (registration is not US equivalency) | Yes |
| Open identifiers | GLEIF (CC0); Wikidata (CC0; 17,428 items carry an EIN, 369 also an LEI) | Official secondary / aggregator | Crosswalk only | Yes |
| Municipal disclosure | MSRB EMMA | Authoritative | Informs; feeds restricted ($45k/yr in 2017 list) | No for redistribution |
| Charity payment networks | PayPal Giving Fund, Chariot, Bonterra, Benevity | Closed systems | Not usable as a feed; competitor benchmarks | No |
| Charity-provided | Websites, annual reports, audited statements, bank letters | Self-reported | Evidence attached to a decision; never authoritative status | Yes |

## 2. What the new sources change

| Change | Why it matters | Evidence |
|---|---|---|
| Screen against the full CSL, not OFAC alone | BIS Entity List (3,427), Denied Persons (1,596), ITAR-debarred (801) and non-SDN lists in one free file | VERIFIED-FACT (downloaded) |
| Replace "OFSI" with the FCDO UK Sanctions List | OFSI list closed 2026-01-28; new identifier scheme means pipelines keyed on old IDs miss new designations (CLM-009) | VERIFIED-FACT |
| Add SAM exclusions and FAC flags as monitoring signals | Debarment, going concern and material weakness are change events worth a human look | VERIFIED-FACT |
| Archive every IRS release from day one | The IRS publishes current snapshots only, and the 990 bulk page had a roughly month-long outage in November 2025 | VERIFIED-FACT (secondary for outage) |
| Treat religious and subordinate eligibility as an evidence problem, not a data feed | Only proprietary OCD and ECFA lists exist; the group exemption letter disclaims verification | VERIFIED-FACT |
| Do not expect a national state-registration dataset | Single Portal paused; Georgia fined an unregistered DAF $100,000 (NASCO, secondary) | VERIFIED-FACT (secondary) |

## 3. Identity resolution challenges by source

| Issue | Sources affected | Approach |
|---|---|---|
| No EIN | State corporate registries, USAspending (UEI/DUNS), GLEIF, CSL, sanctions lists | Bind by name, address, registered agent; keep as **candidate links** with scores until confirmed (never auto-merge) |
| One charity across many EINs (conversions, mergers, reincorporations); the IRS does not reassign EINs (corrected, CHL-053) | BMF (silent removal on revocation; no tombstone) | Temporal identity records; successor links as candidates |
| One EIN for many units (fiscal-sponsor projects, chapters, subordinates) | BMF, Pub 78 | Unit-level aliases under one EIN; donor-name-to-EIN resolution |
| Group subordinates | Listed in the BMF with a group exemption number and affiliation codes, absent from Pub 78 | Automatable via GEN for listed subordinates (Candid already does this); evidence workflow only for unlisted church and Catholic units (CHL-054) |
| DBA and truncated names | BMF (70-character names) | Alias table; charity-provided names as assertions |
| Foreign equivalency | Foreign registries | Registration informs; equivalency determination or expenditure responsibility remains a sponsor decision |
| UEI-EIN bridge | FAC carries both (plus `additional_eins`) | Use FAC as a crosswalk for federal grantees |

## 4. Independent of commercial vendors?

Yes, for **status, revocation, sanctions, exclusion, audit-flag and filing-presence facts**. No, for the parts of eligibility that turn on non-public facts (above), and for **qualitative judgements** (ratings, accountability scores, program effectiveness) and **church/subordinate inclusion**, where the only structured lists are proprietary. An independent intelligence layer is feasible; it is a vetting layer, not a ratings business.

## 5. Can monitoring reduce the 180-day cycle cost?

Yes, materially: see [05](05-charity-registry-economics.md) §4 and [04](04-charity-intelligence-architecture.md) §5. Monthly and daily feeds above turn re-vetting into **change detection plus evidence-expiry refresh**. A full re-review every 180 days costs about four times as much (CLM-005).

## 6. Could a charity intelligence platform be a product?

Unlikely as a standalone business. **Candid Charity Check starts at $2,750 a year** and already combines BMF, Pub 78, IRB, auto-revocation, OFAC, 501(p), a subordinate indicator, church messages and California data; Pactman offers a free tier; Treasury Do Not Pay monitors Pub 78 free for federal agencies (CHL-051). An eligibility evidence service is a **component** of a platform, not a product. Other constraints: redistribution limits on aggregators ([03](03-charity-data-licensing-and-access.md)); an incumbent paid market (Candid Charity Check; OQ-008); and buyers who built their own (PayPal Giving Fund, Chariot, Benevity). Economics are in [15](15-capital-and-break-even-reassessment.md) (route ER-1) and the buyer test is HYP-007.
