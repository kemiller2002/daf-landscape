# Gap 19-06: relationship graph consolidation and red team

**Date:** 2026-11-19. **Queue item:** P-GAP19-06. **Script:** `scripts/mission_graph_consolidate.py run` (stdlib only). **Status:** public-source evidence only; no logins, forms or outreach; robots.txt read before every host and every redirect hop; crt.sh never contacted.

**Outputs:** [`relationship-graph-edges-consolidated-2026-11-19.csv`](../../data/mission-2026-11-14/relationship-graph-edges-consolidated-2026-11-19.csv) (one row per consolidated edge; originals kept unchanged); [`relationship-graph-redteam-2026-11-19.csv`](../../data/mission-2026-11-14/relationship-graph-redteam-2026-11-19.csv) (one row per tested edge); [`queue-proposals-g06.csv`](../../data/mission-2026-11-14/queue-proposals-g06.csv).

## 1. Summary

- **Merge.** 1110 rows from 27 files (the base file and 26 additions files, including `-26`, EZ001–EZ022, added 2026-11-19) become 1059 consolidated edges: 44 groups absorbed 51 duplicate rows (3 of them reversed-direction duplicates), and 8 edges became alias self-loops (for example Fusion Laboratories LLC controls NPact) and are kept in the file but left out of the statistics. That leaves **1051 edges** between **893 nodes** (plus 6 placeholder nodes such as "Unknown sponsor").
- **Names.** 1035 raw entity spellings collapse to 899 nodes (EIN first, then an alias table, then a normalised name key). 771 of the 893 nodes have no record in `relationship-graph-nodes.csv` (131 rows).
- **Red team.** All 109 edges whose evidence class is inferred, unknown, reported, probable, pending, vendor claim or crt.sh-sourced got one independent public check: **41 confirmed, 16 weakened, 52 unverified leads, 0 contradicted**. The main findings:
  - Blackbaud is the wrong vendor on the DonorCentral edges: NPact bought DonorCentral NXT and FIMS from Blackbaud in September 2022. 7 consolidated Blackbaud edges cite DonorCentral and should be re-attributed to NPact.
  - Three Give Interactive implementation tenants (ImpactAssets, The Minneapolis Foundation, Thrivent Charitable) still send donors to Ren iPhi log-ins. Give Interactive is therefore not yet their live platform.
  - Ren's administration of BofA's fund (E083) is weakened: BofA's 2024 Program Guidelines name Bank of America Private Bank as administrator and do not mention Ren. BNY Mellon's iPhi tenant (EK022) is historical, because BNY CGF stopped operating its DAF program on 2024-12-24. DAF Direct still lists BNY (ES016).
  - The NPact Foundation Cloud tenants are confirmed. Every tenant fetched serves "Foundation Cloud Community Portal", and NPact's own customer stories identify the product as NPact's, so the [R] owner caveat no longer applies.
  - The explicit negatives hold on independent pages (Edward Jones private DAF sponsor, Wells Fargo sponsor, U.S. Bank, Pave, Fidelity–Ren, TIFIN's LLM vendor). The Edward Jones private DAF must still not be assigned to RCF or Ren.
- **Status after consolidation and red team:** confirmed 958, inferred 47, historically_confirmed 23, unknown 11, reported 5, probable 3, unverified_lead 2, pending 1, rejected 1 (raw rows: confirmed 971, inferred 81, historically_confirmed 30, unknown 17, reported 6, probable 3, pending 1, rejected 1).
- **Concentration figures.** Sponsor-asset concentration is unchanged because it does not depend on the graph. Recomputed from the DAFRC FY2024 file: CR3 45.5%, CR5 55.8%, HHI 830. **The Ren-linked asset share changes:** 32.2% ($105.62bn, 54 sponsors) on confirmed edges, against the report's 28% ($91.6bn). Restricted to sources dated 2024 or later it is 31.6%.

## 2. Method

1. **Inputs.** `relationship-graph-edges.csv` and every `relationship-graph-edges-additions*.csv` (all share one 12-column schema). `-26` was added on coordinator instruction (2026-11-19).
2. **Entity normalisation.** In order: (a) an EIN written in the name; (b) an alias table (`ALIASES` in the script) that folds product and legal-entity variants into one corporate or sponsor node. Examples: Ren / Ren (Stellar) iPhi / Stellar Technology Solutions (iPhi) / Ren for Charities → *Ren (incl. Stellar/iPhi)*; NPact / Fusion Laboratories LLC / NPact (Foundation Cloud) → *NPact*; NATL CHRISTIAN CHARITABLE FDN INC / National Christian Foundation → *NCF*; DAFgiving360 / Schwab Charitable Fund → *DAFgiving360*; (c) a normalised name key (parentheticals, legal suffixes and punctuation removed), which inherits an EIN when another spelling or a DAFRC FY2024 row carries one. Raw names are kept in `source_entity_original` / `target_entity_original`. Firms and their charities stay separate nodes (Fidelity Charitable vs FMR; Edward Jones vs its programs).
3. **Relationship types.** `general_ledger`→`ledger_provider`; `portal_provider`→`technology_provider`; `lead_investor`/`shareholder`→`investor`; `acquired`→`acquirer`; `owns`→`controls`; `acquired_by` is reversed to `acquirer`. The original type is kept.
4. **Governing corrections** (§5): edge-ID corrections from validation and red-team reports, applied in the consolidated file only. Supersession notes inside the edge files are also applied. A superseded edge is listed under its successor and never chosen as head, even when the successor is weaker (EH005 downgrades EG008).
5. **Deduplication.** Edges are grouped on (unordered endpoints, normalised type). The head is the strongest non-superseded member, ranked by status (confirmed > historically_confirmed > reported > probable = pending > inferred > unknown), then primary-filing URL, then latest access date. `merged_edge_ids` lists every member.
6. **Red team.** The set is every non-superseded edge with status inferred, unknown, reported, probable or pending, a crt.sh source URL, or a vendor-claim label. Each gets one check (`CHECKS` in the script) that is independent of the edge's own source where one could be found: the sponsor's own page instead of a vendor list, the filing instead of an aggregator, the tenant itself instead of a search-index capture, or public DNS for crt.sh-only leads, as the compliance note allows.
   - Outcome rules: a regex hit gives the check's `on_find` outcome; a fetched page without the hit gives `on_absent`.
   - If a page could not be read (robots.txt unreadable or disallowing, Cloudflare 403, network error), the edge is an unverified lead. A wrong URL never weakens an edge; only named liveness checks treat 404 or NXDOMAIN as weakening.
   - For `unknown` edges (explicit negatives), **confirmed** means the slot is still unfilled on the independent source.
   - Where no independent route exists, the check is a dated re-observation, and the table says so.
   - Edges whose only source is crt.sh (EB009, ED008, EH014) get `status = unverified_lead` unless the check confirms them (compliance note 2026-11-15).
7. **Network use.** 236 responses (robots.txt files, pages, DNS lookups) were collected for this pass and cached in the session scratchpad; the final run sent 0 new requests. Requests were at least 1 s apart per host, with a generic User-Agent.

## 3. Graph statistics

| Measure | Value |
|---|---|
| Edge rows read (27 files) | 1110 |
| Consolidated edges (incl. self-loops) | 1059 |
| Edges used for statistics | 1051 |
| Duplicate rows merged | 51 |
| Nodes (excl. placeholders) | 893 |
| Nodes missing from relationship-graph-nodes.csv | 771 |

**Edges by status (after consolidation and red team)**

| Status | Edges |
|---|---|
| confirmed | 958 |
| inferred | 47 |
| historically_confirmed | 23 |
| unknown | 11 |
| reported | 5 |
| probable | 3 |
| unverified_lead | 2 |
| pending | 1 |
| rejected | 1 |

**Edges by relationship type (normalised; top 20)**

| Type | Edges |
|---|---|
| technology_provider | 686 |
| administers | 51 |
| sponsor_of | 41 |
| distributor_white_label | 33 |
| payment_processor | 32 |
| investor | 22 |
| investment_manager | 21 |
| corporate_daf_at | 18 |
| ledger_provider | 17 |
| acquirer | 16 |
| grant_to | 13 |
| controls | 11 |
| lender | 8 |
| disbursement_partner | 6 |
| integration_partner | 6 |
| charity_verification | 5 |
| api_partner | 5 |
| auditor | 4 |
| operates | 4 |
| data_feed | 4 |

52 types in all.

**Hub degree** (number of consolidated edges touching the node; self-loops excluded). The original doc counted Ren in 34 and RCF in 22 base edges.

| Node | Raw rows mentioning | Degree (all) | Degree (confirmed) | Degree (confirmed + historical) | Degree within base-file edges |
|---|---|---|---|---|---|
| Ren (incl. Stellar/iPhi) | 145 | 131 | 112 | 119 | 36 |
| Foundant Technologies | 367 | 365 | 365 | 365 | 0 |
| Chariot | 19 | 18 | 18 | 18 | 12 |
| Fidelity Charitable | 27 | 26 | 23 | 24 | 7 |
| Fidelity group (Fidelity Charitable + FMR) | 27 | 26 | 23 | 24 | 7 |
| Renaissance Charitable Foundation (RCF) | 31 | 29 | 24 | 26 | 22 |
| Edward Jones (firm) | 5 | 4 | 3 | 3 | 3 |
| Edward Jones cluster (firm + CGF + private DAF + Generations) | 18 | 12 | 8 | 8 | 8 |
| Blackbaud | 26 | 24 | 11 | 12 | 3 |
| NPact (Fusion Laboratories LLC) | 34 | 28 | 26 | 27 | 0 |
| Give Interactive | 16 | 13 | 4 | 5 | 0 |

Foundant's degree is almost entirely its own client list (vendor-stated). Edward Jones has 4 edges as a firm and 12 across its cluster; every edge on the private DAF's sponsor is an explicit negative (unknown).

## 4. Dependency and concentration figures

**Sponsor assets (not graph-derived; unchanged).** Recomputed from `dafrc-sponsor-schedule-d-fy2019-2024.csv` (FY2024, 1512 sponsors, $327.87bn): CR3 45.5%, CR4 52.2%, CR5 55.8%, HHI 830. These match the report's CR3 45.5%, CR5 55.8% and HHI ≈ 830, so no change.

**Ren-linked share of FY2024 DAF assets (graph-derived; changes).** This counts DAFRC sponsors (matched by EIN) that have at least one Ren/Stellar/iPhi technology, administration, ledger, payment, data-feed or export edge.

| Tier | Sponsors | Assets | Share of $327.87bn |
|---|---|---|---|
| A confirmed | 54 | $105.62bn | 32.2% |
| A2 confirmed source dated 2024 or later | 47 | $103.64bn | 31.6% |
| B plus inferred reported | 55 | $105.63bn | 32.2% |
| C plus historical | 60 | $114.84bn | 35.0% |

The largest contributors to the confirmed tier: NATIONAL PHILANTHROPIC TRUST $42.12bn; GS DONOR ADVISED PHILANTHROPY FUND $11.84bn; AMERICAN ENDOWMENT FOUNDATION $9.48bn; MORGAN STANLEY GLOBAL IMPACT FUNDING TRUST INC $9.43bn; Renaissance Charitable Foundation Inc $5.63bn; NATL CHRISTIAN CHARITABLE FDN INC $5.46bn; BANK OF AMERICA CHARITABLE GIFT FD $5.11bn; IMPACTASSETSINC $3.63bn; Combined Jewish Philanthropies of Greater Boston Inc $1.93bn; RAYMOND JAMES CHARITABLE ENDOWMENT FUND $1.89bn; THE AYCO CHARITABLE FOUNDATION $1.38bn; THE US CHARITABLE GIFT TRUST $1.36bn.

- The report's **28% ($91.6bn)** was built from wave-3 evidence. The seven Ren sponsors that wave-3 text names (NPT, GS PWM DAF, GS Gives, AEF, MS GIFT, RCF, BofA CGF) hold $84.13bn here. The consolidated confirmed tier adds 47 more sponsors ($21.49bn), mostly from 990 payee harvests and iPhi/DFX tenant sweeps. The largest are NATL CHRISTIAN CHARITABLE FDN INC $5.46bn; IMPACTASSETSINC $3.63bn; Combined Jewish Philanthropies of Greater Boston Inc $1.93bn; RAYMOND JAMES CHARITABLE ENDOWMENT FUND $1.89bn; THE AYCO CHARITABLE FOUNDATION $1.38bn; THE US CHARITABLE GIFT TRUST $1.36bn.
- Restricting to edges whose source is dated 2024 or later drops 7 sponsors ($1.98bn): THE AYCO CHARITABLE FOUNDATION $1.38bn; BRADLEY IMPACT FUND INC $0.21bn; Greater Miami Jewish Federation Inc $0.20bn; BATON ROUGE AREA FOUNDATION $0.10bn; RSF SOCIAL FINANCE INC $0.03bn; COMMUNITY FOUNDATION OF GREATER FLINT $0.03bn; SOUTHWEST FLORIDA COMMUNITY FOUNDATION $0.03bn.
- NPT ($42.12bn) is 39.9% of the confirmed tier and still rests on hosting evidence only. The gap19 second-source pass found no NPT document naming Ren.
- Ren's ">60%" claim remains unsupported.

**Vendor client concentration (graph-derived, new).** These are distinct DAFRC sponsors per vendor on confirmed technology/admin/ledger/payment edges. Sponsors multi-home and vendor lists are self-reported, so treat the counts as evidence counts, not market shares.

| Vendor | Sponsors | Their FY2024 DAF assets |
|---|---|---|
| Foundant Technologies | 359 | $19.91bn |
| Ren (incl. Stellar/iPhi) | 54 | $105.62bn |
| Akoya | 49 | $2.86bn |
| Salesforce | 23 | $109.74bn |
| NPact (Fusion Laboratories LLC) | 21 | $18.10bn |
| Foundation Partners LLC (Fund 360) | 13 | $7.32bn |
| FidTech Partners (Fiduciary Technology Partners LLC) | 7 | $0.99bn |
| Blackbaud | 6 | $3.66bn |
| DonorSphere | 6 | $1.72bn |
| PayPal | 5 | $64.49bn |
| Redpath Consulting Group | 4 | $0.98bn |
| Chariot | 3 | $41.62bn |

- CR3 by sponsor links (top three vendors' share of 630 vendor–sponsor links): 73.3%. This is driven by Foundant's client list.
- 542 of 1512 DAFRC sponsors have at least one confirmed vendor edge, holding $299.69bn.
- Asset sums double-count multi-homed sponsors. Salesforce and PayPal reach Fidelity, Vanguard and NPT only through marketing or payment edges.

**Single-point-of-failure exposure (count of distinct counterparties on confirmed edges).**

| SPOF / vendor | Counterparties |
|---|---|
| S1 RCF sponsor/administrator: programs | 16 |
| S2 Ren technology/admin clients (all tenants, programs, sponsors) | 98 |
| S3 Foundation Source technology clients | 5 |
| S4 Chariot payment clients | 14 |
| S5 GiveClear sponsored programs | 2 |
| NPact technology clients | 21 |
| Foundant technology clients | 348 |
| Give Interactive technology clients (confirmed) | 3 |

Compare these counts with the program lists in `vendor-dependency-concentration.md` §6 (S1–S6). Ren's DFX/iPhi family (S2) now has far more evidenced counterparties than the four sponsors named there. GiveClear's count covers only programs with a confirmed sponsor_of edge in the graph. Give Interactive's confirmed live footprint is still small, because most of its tenants are implementation-stage.

## 5. Governing corrections applied

| Edge | Operation | Value | Source | Result |
|---|---|---|---|---|
| EN001 | set_type | technology_provider | validation-wave14-report.md l.138 (V14-01) | applied in consolidated file |
| EN001 | add_note | fund-accounting overlay on the NetSuite GL | validation-wave14-report.md l.138 (V14-01) | applied in consolidated file |
| EN011 | set_status | reported | validation-wave14-report.md l.139 | applied in consolidated file |
| EN011 | add_note | donor-portal.org portal tenant (first-party link); back-office service not shown | validation-wave14-report.md l.139 | applied in consolidated file |
| ER017 | add_note | superseded by the FireAid App. B circular (ratios as of 2024-09-30), which names Goldman Sachs Wealth Services | validation-wave18-report.md l.185 | applied in consolidated file |
| ER015 | add_note | report wording varies: '$535 million ... since inception' vs 'In 2023: ... assets under care'; V18-27 | validation-wave18-report.md l.186 | applied in consolidated file |
| ES016 | add_note | the source text is in Schedule N Part II as well as Schedule O (V19) | validation-wave19-report.md l.132 | applied in consolidated file |
| ES006 | add_note | Sch R also lists codes C $2,209,075, L $1,742,154, O $689,031, P $307,024 (V19) | validation-wave19-report.md l.133 | applied in consolidated file |
| EU013 | add_note | GS & Co's payee label is 'TECH & INV ADV FEES', so technology_provider is a partial reading; investment adviso | validation-wave22-report.md l.177 | applied in consolidated file |
| EV002 | add_note | posting not re-observable (wave 23) | validation-wave23-report.md l.243 | applied in consolidated file |
| EV003 | add_note | terms not re-read in wave 23 (npact.com unreachable) | validation-wave23-report.md l.244 | applied in consolidated file |
| EV006 | add_note | the five CT-discovered clients ($9.81bn) are DNS-confirmed implementation hosts, not live portals (V23) | validation-wave23-report.md l.245 | applied in consolidated file |
| EV001 | add_note | cite the fcjc.fftc.org page and the fftc.org link rather than daf.fftc.org/m/login (robots intent; V23) | validation-wave23-report.md l.246 | applied in consolidated file |
| EW020 | replace_note | file built 2014 -> created 2014-11-18, modified 2023-01-02 | validation-wave25b-report.md l.169-170 | old text not present in source file (nothing to replace) |
| EW020 | replace_note | file metadata 2014 -> created 2014-11-18, modified 2023-01-02 | validation-wave25b-report.md l.169-170 | old text not present in source file (nothing to replace) |
| EW019 | add_note | amended FY6/22 return (filed 2024); also $197,000 cash to Dechomai Foundation (V25B) | validation-wave25b-report.md l.171-172 | applied in consolidated file |
| EX001 | add_note | Fidelity named in the 2026 proxy only; not in the 2025 10-K (V26) | validation-wave26-report.md l.171 | applied in consolidated file |
| E086 | set_status | confirmed | red-team-wave2b-graph-data-incentives.md l.204 | already applied in source file |
| E151 | add_note | scope=donor_checkout | red-team-wave2b-graph-data-incentives.md l.205 | already applied in source file |
| E093 | set_status | reported | gap19-edward-jones-wealth-channels.md l.34, l.209-210 (EZ012) | applied in consolidated file |
| E093 | add_note | not re-confirmed 2026-11-19: source URL redirects to the Private Wealth hub; live Wells Fargo DAF pages name n | gap19-edward-jones-wealth-channels.md l.34, l.209-210 (EZ012) | applied in consolidated file |
| E094 | set_status | reported | gap19-edward-jones-wealth-channels.md l.209-210 | applied in consolidated file |
| E094 | add_note | not re-confirmed 2026-11-19 (same redirected source as E093); search-excerpt evidence only | gap19-edward-jones-wealth-channels.md l.209-210 | applied in consolidated file |
| E018 | add_note | explicit negatives EZ001-EZ003 (10-Ks, ADV 2A, RCF audits): do not assume RCF or Ren | gap19-edward-jones-wealth-channels.md l.23 | applied in consolidated file |
| EA027 | add_note | [gap19-06] superseded by EK021 | edge-file supersession note | applied in consolidated file |
| EA032 | add_note | [gap19-06] superseded by EK030/ED002 | edge-file supersession note | applied in consolidated file |
| EJ032 | add_note | [gap19-06] superseded by EM033 | edge-file supersession note | applied in consolidated file |
| EH013 | add_note | [gap19-06] superseded by ER005 | edge-file supersession note | applied in consolidated file |
| E034 | add_note | [gap19-06] superseded by EF001 | edge-file supersession note | applied in consolidated file |
| EG008 | add_note | [gap19-06] superseded by EH004/EH005 | edge-file supersession note | applied in consolidated file |
| E161 | add_note | [gap19-06] superseded by EA010 | edge-file supersession note | applied in consolidated file |
| E092 | add_note | [gap19-06] superseded by EA016 | edge-file supersession note | applied in consolidated file |
| E120 | add_note | [gap19-06] superseded by EA017 | edge-file supersession note | applied in consolidated file |
| E162 | add_note | [gap19-06] superseded by EA025 | edge-file supersession note | applied in consolidated file |
| E077 | add_note | [gap19-06] superseded by EA022 | edge-file supersession note | applied in consolidated file |
| EJ005 | add_note | [gap19-06] read with EP001 (note-level reference) | edge-file cross-reference | applied in consolidated file |
| EA002 | add_note | [gap19-06] read with EB001 (note-level reference) | edge-file cross-reference | applied in consolidated file |
| EN004 | add_note | [gap19-06] read with EV001 (note-level reference) | edge-file cross-reference | applied in consolidated file |
| EJ007 | add_note | [gap19-06] read with EM001 (note-level reference) | edge-file cross-reference | applied in consolidated file |
| E045 | add_note | [gap19-06] read with EZ008 (note-level reference) | edge-file cross-reference | applied in consolidated file |
| EA016 | add_note | [gap19-06] read with EE001 (note-level reference) | edge-file cross-reference | applied in consolidated file |

Supersessions applied (superseded ← superseding): EA027 ← EK021; EA032 ← EK030/ED002; EJ032 ← EM033; EH013 ← ER005; E034 ← EF001; EG008 ← EH004/EH005; E161 ← EA010; E092 ← EA016; E120 ← EA017; E162 ← EA025; E077 ← EA022. Note-level references were annotated only: EJ005 (see EP001); EA002 (see EB001); EN004 (see EV001); EJ007 (see EM001); E045 (see EZ008); EA016 (see EE001).

## 6. Red-team results

| Evidence class | n | confirmed | weakened | unverified-lead | contradicted |
|---|---|---|---|---|---|
| crt.sh-sourced | 1 | 1 | 0 | 0 | 0 |
| inferred | 76 | 24 | 15 | 37 | 0 |
| pending | 1 | 1 | 0 | 0 | 0 |
| probable | 3 | 0 | 0 | 3 | 0 |
| reported | 9 | 4 | 1 | 4 | 0 |
| unknown | 14 | 11 | 0 | 3 | 0 |
| vendor_claim | 5 | 0 | 0 | 5 | 0 |

| Edge | Class | Edge as filed | Check | Result | Outcome | Status proposed |
|---|---|---|---|---|---|---|
| E014 | inferred | Ren → Edward Jones Charitable Gift Fund (administers) | EJ portal Terms of Service (a Renaissance Acquisition Company LLC agreement): does it give Ren an administration role? <https://edwardjones.donorfirstx.com/Terms%20of%20Service.pdf> | fetched 200; no match | unverified-lead | inferred |
| E016 | inferred | Edward Jones → Edward Jones Charitable Gift Fund (investment_manager) | EJ CGF portal: who manages the portfolios? <https://edwardjones.donorfirstx.com/> | fetched 200; no match | unverified-lead | inferred |
| E018 | unknown | Unknown sponsor → Edward Jones private DAF (Generations) (sponsor_of) | EJ DAF product page: is a sponsor named for the private DAF? <https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-fu> | fetched 200; no match | confirmed | unknown |
| E058 | unknown | Renaissance Charitable Foundation → Franklin Charitable Giving Program (sponsor_of) | Franklin portal re-read (no other public program document found): RCF named as sponsor? <https://ft.donorfirstx.com/> | fetched 200; no match | unverified-lead | unknown |
| E069 | inferred | TD Ameritrade (legacy channel) → RCF TDA-coded portal (legacy TD Ameritrade ch (distributor_white_label) | TDA-coded portal: does the page itself name TD Ameritrade? <https://tda.donorfirstx.com/> | fetched 200; no match | unverified-lead | inferred |
| E083 | inferred | Ren → Bank of America Charitable Gift Fund (administers) | BofA CGF Program Guidelines v3.2024: is Ren named? (Guidelines say the fund 'is currently administered by Bank of America Private Bank') <https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf> | fetched 200; no match | weakened | inferred |
| E087 | inferred | Blackbaud → American Endowment Foundation (technology_provider) | PR Newswire 2022-09-12: NPact acquired DonorCentral from Blackbaud, so AEF's DonorCentral vendor after 2022-09 was NPact (cf. EA024 NPact payee) <https://prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-fro> | fetched -> https://www.prnewswire.com/news-releases/npact-ac 200; matched: “NPact Acquires FIMS and DonorCentral® NXT Products from Blackbaud Accessibility Statement ” | weakened | inferred |
| E088 | inferred | Ren → Gulf Coast Community Foundation (technology_provider) | Direct fetch of the DFX tenant (edge rested on search index only) <https://gccf.donorfirstx.com/> | fetched 200; matched: “nId: datadogApplicationId, site: 'datadoghq.com', service: 'dfx', env: datadogEnvironment,” | confirmed | confirmed |
| E089 | inferred | Ren → Southeast Missouri State University Foundatio (technology_provider) | Direct fetch of the DFX tenant <https://semo.donorfirstx.com/> | not fetched: robots unreadable (500); no match | unverified-lead | inferred |
| E090 | inferred | Ren → Jewish Community Federation (donorfirst.org p (technology_provider) | Direct fetch of the DonorFirst tenant <https://jewishfed.donorfirst.org/> | not fetched: robots unreadable (URLError: <urlopen error Tun; no match | unverified-lead | inferred |
| E093 | reported | National Philanthropic Trust → Wells Fargo DAF program (sponsor_of) | NPT home page: does NPT name a Wells Fargo program? <https://www.nptrust.org/> | fetched 200; no match | unverified-lead | reported |
| E094 | reported | Wells Fargo → Wells Fargo DAF program (investment_manager) | Live WF Advisors DAF page: does WF say it manages the DAF investments? <https://www.wellsfargoadvisors.com/private-wealth/conversations/philanthropy/donor-advised> | fetched 200; no match | unverified-lead | reported |
| E113 | inferred | BNY Mellon N.A. → BNY Mellon Charitable Gift Fund (administers) | BNY CGF CY2024 Form 990 (e-file XML) instead of the CauseIQ aggregator: BNY Mellon N.A. named? <https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541919349300514_publi> | fetched 200; matched: “CT 06103 990 2024-01-01 300748315 BNY MELLON CHARITABLE GIFT FUND C/O BNY MELLON NA BNYM 6” | confirmed | confirmed |
| E155 | vendor_claim | Candid → Groundswell (charity_verification) | Candid side of the claimed integration <https://www.candid.org/> | not fetched: robots unreadable (URLError: <urlopen error Tun; no match | unverified-lead | confirmed |
| E157 | unknown | Unknown LLM vendor → TIFIN Give (ai_provider) | Louise launch page re-read (tifingive.com unreachable): model vendor named? <https://tifin.com/news/tifin-give-launches-louise-the-ai-platform-for-philanthropy/19124/> | fetched 200; no match | confirmed | unknown |
| EA001 | vendor_claim | Give Interactive → Vanguard Charitable (technology_provider) | Vanguard Charitable home page / login links: any Give Interactive reference? <https://www.vanguardcharitable.org/> | fetched 200; no match | unverified-lead | confirmed |
| EA005 | inferred | Give Interactive → Chicago Community Trust (technology_provider) | Chicago Community Trust home page: login link to a Give Interactive tenant? <https://www.cct.org/> | fetched 403; no match | unverified-lead | inferred |
| EA006 | inferred | Give Interactive → Jewish Communal Fund (technology_provider) | JCF home page: client login link (login.jcfny.org) - Give Interactive? <https://jcfny.org/> | fetched 200; no match | unverified-lead | inferred |
| EA007 | inferred | Give Interactive → ImpactAssets (technology_provider) | ImpactAssets home page: client login still on Ren iPhi (iphi.stellartechsol.com/calvert)? <https://impactassets.org/> | fetched 200; no match | weakened | inferred |
| EA009 | inferred | Give Interactive → The Minneapolis Foundation (technology_provider) | Minneapolis Foundation home page: donor login still tmf.iphiview.com? <https://www.minneapolisfoundation.org/> | fetched 200; no match | weakened | inferred |
| EA011 | inferred | Give Interactive → Thrivent Charitable (technology_provider) | Thrivent Charitable home page: log-in still infaith.iphiview.com? <https://www.thriventcharitable.com/> | fetched -> https://thriventcharitable.thrivent.com/ 200; no match | weakened | inferred |
| EA013 | inferred | Give Interactive → Stifel Charitable Inc. (technology_provider) | Stifel Charitable home page: login link <https://www.stifelcharitable.org/> | not fetched: robots unreadable (URLError: <urlopen error Tun; no match | unverified-lead | inferred |
| EA015 | inferred | Give Interactive → National Heritage Foundation (unconfirmed) (technology_provider) | National Heritage Foundation home page: login link <https://www.nhf.org/> | not fetched: robots unreadable (URLError: <urlopen error [SS; no match | unverified-lead | inferred |
| EB009 | inferred | Give Interactive → John MacArthur Charitable Trust (unconfirmed) (technology_provider) | Public DNS (admissible re-source of a crt.sh-only lead): host resolves; identity still a slug match <dns:jmacarthurtrust.giveinteractive.com> | DNS ok cname=- ips=34.160.124.107; matched: “ 34.160.124.107” | unverified-lead | unverified_lead |
| ED007 | pending | The Vanguard Group → Altruist (acquirer) | Altruist home page: closing announced? (absent = still pending) <https://altruist.com/> | fetched 200; no match | confirmed | pending |
| ED008 | inferred | Give Interactive → Vanguard Charitable (technology_provider) | Public DNS: host resolves (to an AWS API Gateway); name says nothing about the vendor <dns:api-give.vanguardcharitable.org> | DNS ok cname=d-s8mdizdfu5.execute-api.us-east-1.amazonaws.co; matched: “d-s8mdizdfu5.execute-api.us-east-1.amazonaws.com 3.232.59.76 32.198.169.141 34.204.252.78” | unverified-lead | unverified_lead |
| EE001 | inferred | Ren (Stellar iPhi) → National Philanthropic Trust (technology_provider) | NPT GivingPoint front page: iPhi/DonorView/Ren markers? <https://www.nptgivingpoint.org/> | fetched 200; no match | unverified-lead | inferred |
| EE007 | inferred | RSM US LLP → National Philanthropic Trust (auditor) | NPT 2025 annual report page: auditor named? <https://www.nptrust.org/annual-reports/npt-annual-report/> | fetched 200; no match | unverified-lead | inferred |
| EE009 | inferred | Ernst & Young US LLP → Morgan Stanley GIFT (auditor) | MS GIFT 'How it works' PDF: auditor named? <https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gi> | fetched 200; no match | unverified-lead | inferred |
| EG003 | inferred | NPact (Foundation Cloud) → Greater Washington Community Foundation (technology_provider) | GWCF tenant page; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN004 FFTC, EN005 C <https://thecommunityfoundation.spectrumportal.net/> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EH003 | inferred | DonorSphere → Delaware Community Foundation (technology_provider) | DCF home page (first-party) links its Login Portal to delcf.donorsphere.org? <https://delcf.org/> | fetched 200; matched: “-item-object-custom menu-item-54878"><a target="_blank" href="https://delcf.donorsphere.or” | confirmed | confirmed |
| EH005 | unknown | DonorSphere → The Pittsburgh Foundation (technology_provider) | Pittsburgh Foundation home page: any DonorSphere link? <https://pittsburghfoundation.org/> | fetched 403; no match | unverified-lead | unknown |
| EH014 | inferred | DonorSphere → Jewish Federation of Northern New Jersey (technology_provider) | JFNNJ home page: DonorSphere login link? <https://www.jfnnj.org/> | fetched 200; no match | unverified-lead | unverified_lead |
| EH015 | unknown | DonorSphere → National Christian Foundation (technology_provider) | NCF home page: any DonorSphere link (absent = no current use shown)? <https://www.ncfgiving.com/> | fetched 200; no match | confirmed | unknown |
| EI001 | inferred | NPact (Foundation Cloud) → The San Diego Foundation (EIN 95-2942582; sdf (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://sdfoundation.spectrumportal.net/> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI002 | inferred | NPact (Foundation Cloud) → Tulsa Community Foundation (EIN 73-1554474; t (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://tcf.spectrumportal.net/accounts/signin> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI030 | inferred | Blackbaud → Princeton Area Community Foundation Inc (EIN  (technology_provider) | Direct fetch of the vendor tenant; tenant live on donorcentral.com, but NPact acquired DonorCentral NXT and FIMS from Blackbaud (PR Newswire 2022-09-1 <https://pacf.donorcentral.com/#/> | fetched 200; matched: “ral <!DOCTYPE html><html lang="en"><head> <meta charset="utf-8"> <title>Donorcentral</titl” | weakened | inferred |
| EI031 | inferred | NPact (Foundation Cloud) → SANTA BARBARA FOUNDATION (EIN 95-1866094; sbf (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://donorportal-sbfoundation.spectrumportal.net/accounts/signin> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI038 | inferred | NPact (Foundation Cloud) → NEVADA COMMUNITY FOUNDATION INC (EIN 88-02414 (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://nevadacf.spectrumportal.net/accounts/register> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI070 | inferred | NPact (Foundation Cloud) → KALAMAZOO COMMUNITY FOUNDATION (EIN 38-333320 (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://kalfound.spectrumportal.net/> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI074 | inferred | Blackbaud → THE COMMUNITY FOUNDATION FOR GREATER NEW (EIN (technology_provider) | Direct fetch of the vendor tenant; tenant live on donorcentral.com, but NPact acquired DonorCentral NXT and FIMS from Blackbaud (PR Newswire 2022-09-1 <https://cfgnh.donorcentral.com/> | fetched 200; matched: “ral <!DOCTYPE html><html lang="en"><head> <meta charset="utf-8"> <title>Donorcentral</titl” | weakened | inferred |
| EI083 | inferred | Blackbaud → Community Foundation of St Joseph County Inc  (technology_provider) | Direct fetch of the vendor tenant; tenant live on donorcentral.com, but NPact acquired DonorCentral NXT and FIMS from Blackbaud (PR Newswire 2022-09-1 <https://cfsjc.donorcentral.com/> | fetched 200; matched: “ral <!DOCTYPE html><html lang="en"><head> <meta charset="utf-8"> <title>Donorcentral</titl” | weakened | inferred |
| EI111 | inferred | NPact (Foundation Cloud) → AMARILLO AREA FOUNDATION INC (EIN 75-0978220; (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://aaf.spectrumportal.net/> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI113 | inferred | NPact (Foundation Cloud) → MONTANA COMMUNITY FOUNDATION INC (EIN 81-0450 (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://mtcf.spectrumportal.net/#/accounts/signin> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI155 | inferred | NPact (Foundation Cloud) → COMMUNITY FOUNDATION OF THE EASTERN SHOR (EIN (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://cfes.spectrumportal.net/accounts/signin> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI178 | inferred | NPact (Foundation Cloud) → THE COMMUNITY FOUNDATION OF FREDERICK (EIN 52 (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://frederickcountygives.spectrumportal.net/accounts/signin> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI205 | inferred | NPact (Foundation Cloud) → DOOR COUNTY COMMUNITY FOUNDATION INC (EIN 39- (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <http://doorcountycommunityfoundation.spectrumportal.net/accounts/signin> | fetched -> https://doorcountycommunityfoundation.spectrumpor 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI210 | inferred | Blackbaud → FOUNDATION FOR APPALACHIAN OHIO (EIN 31-16204 (technology_provider) | Direct fetch of the vendor tenant; tenant live on donorcentral.com, but NPact acquired DonorCentral NXT and FIMS from Blackbaud (PR Newswire 2022-09-1 <https://ffao.donorcentral.com/#/> | fetched 200; matched: “ral <!DOCTYPE html><html lang="en"><head> <meta charset="utf-8"> <title>Donorcentral</titl” | weakened | inferred |
| EI229 | inferred | Blackbaud → THE NORTHERN CINCINNATI FOUNDATION (EIN 31-16 (technology_provider) | Direct fetch of the vendor tenant; tenant live on donorcentral.com, but NPact acquired DonorCentral NXT and FIMS from Blackbaud (PR Newswire 2022-09-1 <https://northerncincinnati.donorcentral.com/> | fetched 200; matched: “ral <!DOCTYPE html><html lang="en"><head> <meta charset="utf-8"> <title>Donorcentral</titl” | weakened | inferred |
| EI230 | inferred | Blackbaud → THE VALLEY COMMUNITY FOUNDATION INC (EIN 84-1 (technology_provider) | Direct fetch of the vendor tenant; tenant live on donorcentral.com, but NPact acquired DonorCentral NXT and FIMS from Blackbaud (PR Newswire 2022-09-1 <https://vcf.donorcentral.com/> | fetched 200; matched: “ral <!DOCTYPE html><html lang="en"><head> <meta charset="utf-8"> <title>Donorcentral</titl” | weakened | inferred |
| EI245 | inferred | Akoya → MIDLAND AREA COMMUNITY FOUNDATION (EIN 38-202 (technology_provider) | Direct fetch of the vendor tenant; tenant serves an akoyaGO module (GOfund/GOapply/GOdonate); scope may be grants or donations, not DAF <https://goapply2.akoyago.com/midland/Identity/Account/Login?ReturnUrl=%2Fmidland%2Fopportu> | fetched 200; matched: “Sign in - GOapply Sign in to your account Or create a new account Your Email Your Passw” | confirmed | confirmed |
| EI269 | inferred | Akoya → Emporia Community Foundation (EIN 48-1169158; (technology_provider) | Direct fetch of the vendor tenant; tenant serves an akoyaGO module (GOfund/GOapply/GOdonate); scope may be grants or donations, not DAF <https://gofund.akoyago.com/emporiacf> | fetched -> https://gofund.akoyago.com/emporiacf/Identity/Acc 200; matched: “Sign In - GOfund Please sign in with your username and password. Passwords must be 10” | confirmed | confirmed |
| EI271 | inferred | NPact (Foundation Cloud) → NORTHWEST MINNESOTA FOUNDATION (EIN 41-155601 (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://nwmf.spectrumportal.net/accounts/signin> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI300 | inferred | NPact (Foundation Cloud) → INITIATIVE FOUNDATION (EIN 36-3451562; ifound (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://ifound.spectrumportal.net/accounts/signin> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI307 | inferred | NPact (Foundation Cloud) → NEW MEXICO COMMUNITY FOUNDATION (EIN 85-03112 (technology_provider) | Direct fetch of the vendor tenant; tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own customer stories (EN <https://nmcf.spectrumportal.net/accounts/signin> | fetched 200; matched: “--> --> --> Foundation Cloud Community Portal ⚠️ Loading... Loading... <!DOCTYPE html> <ht” | confirmed | confirmed |
| EI337 | inferred | Akoya → COMMUNITY FOUNDATION OF CHIPPEWA CO (EIN 39-2 (technology_provider) | Direct fetch of the vendor tenant; tenant serves an akoyaGO module (GOfund/GOapply/GOdonate); scope may be grants or donations, not DAF <https://goapply2.akoyago.com/yourlegacy> | fetched -> https://goapply2.akoyago.com/yourlegacy/Identity/ 200; matched: “Sign in - GOapply &nbsp; Powered by GO apply Sign in to your account Or create a new ac” | confirmed | confirmed |
| EI410 | inferred | Akoya → GRANT COUNTY COMMUNITY FOUNDATION INCORPORATE (technology_provider) | Direct fetch of the vendor tenant; tenant serves an akoyaGO module (GOfund/GOapply/GOdonate); scope may be grants or donations, not DAF <https://godonate.akoyago.com/grantccf> | fetched 200; matched: “ty Development Education General Health Other Youth &copy; Powered by akoyaGO - 2026.11.11” | confirmed | confirmed |
| EJ005 | inferred | NPact (Fusion Laboratories LLC) → SANTA BARBARA FOUNDATION (EIN 95-1866094) (technology_provider) | SBF home page links its Donor Portal to an NPact Foundation Cloud tenant (consistent with 'hosted infrastructure') <https://sbfoundation.org/> | fetched 200; matched: “ject-custom menu-item-4223"><a href="https://donorportal-sbfoundation.spectrumportal.net/a” | confirmed | confirmed |
| EJ020 | inferred | Greater Kansas City Community Foundation → INDIAN RIVER COMMUNITY FOUNDATION INC (EIN 20 (technology_provider) | IRCF 'My Fund has been Upgraded!' page: fund access moved to Foundant? <https://ircommunityfoundation.org/my-fund-has-been-upgraded/> | fetched 200; matched: “a id="link_text-44-21" class="ct-link-text" href="https://indianriver.fcsuite.com/erp/dona” | weakened | inferred |
| EJ025 | inferred | Armanino LLP → THE VERMONT COMMUNITY FOUNDATION (EIN 22-2712 (technology_provider) | Direct read of the Armanino case study (edge used search capture) <https://www.armanino.com/case-studies/transforming-nonprofit-technology-for-greater-impact> | fetched 403; no match | unverified-lead | inferred |
| EJ026 | unknown | Slalom LLC → Silicon Valley Community Foundation (EIN 20-5 (technology_provider) | Slalom customer stories: SVCF named? <https://www.slalom.com/us/en/customer-stories> | fetched 200; no match | unverified-lead | unknown |
| EJ028 | inferred | FundMiner → Warren County Foundation (technology_provider) | FundMiner community page re-read: Warren County still listed? (no CF page identified) <https://www.fundminer.com/community> | fetched 200; matched: “:500px;border-width:0px;border:0px;width: inherit;;" width="500" alt="Warren County Founda” | unverified-lead | inferred |
| EK018 | inferred | Ren (Stellar) iPhi → KeyBank (product not stated) (technology_provider) | Live re-observation of the iPhi tenant (no KeyBank page links it) <https://keybank.iphiview.com/keybank/> | not fetched: robots disallow; no match | unverified-lead | inferred |
| EK022 | inferred | Ren (Stellar) iPhi → BNY Mellon Charitable Gift Fund (EIN 30-07483 (technology_provider) | BNY CGF CY2024 990: DAF program wound down (2024-12-24), so the iPhi tenant is historical at most <https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541919349300514_publi> | fetched 200; matched: “ULE N, PART II: ON DECEMBER 24, 2024, THE BOARD OF DIRECTORS VOTED TO NO LONGER OPERATE TH” | weakened | inferred |
| EK032 | inferred | Blackbaud → Kalamazoo Community Foundation (EIN 38-333320 (technology_provider) | Live re-observation of kzcf.org Blackbaud NXT donation form (CRM/ledger still only implied) <https://kzcf.org/> | fetched 200; matched: “b_button et_pb_button_5 et_pb_bg_layout_light" href="https://host.nxt.blackbaud.com/donor-” | confirmed | confirmed |
| EK033 | inferred | Ren → Renaissance Charitable Foundation (EIN 35-212 (payment_processor) | Ren help centre: Ren sends ACH grant payments for its DAF programs <https://intercom.help/rengiving/en/articles/6232119-charity-ach-setup-step-by-step> | fetched 200; matched: “ing you that you can upload in the portal as well. Once approved, all ACH grant payments f” | confirmed | confirmed |
| EL027 | inferred | Nuance → Fidelity Charitable (technology_provider) | Public DNS: does the host CNAME to a Nuance domain? (Akamai CNAME says nothing about the vendor) <dns:nuance.fidelitycharitable.org> | DNS ok cname=e80688.x.akamaiedge.net ips=23.52.42.137,23.52.; no match | unverified-lead | inferred |
| EL028 | unknown | Ren → Fidelity Charitable (technology_provider) | Fidelity Charitable nonprofit FAQ: any Ren marker? <https://www.fidelitycharitable.org/nonprofits/faqs.html> | fetched 200; no match | confirmed | unknown |
| EM001 | vendor_claim | Foundation Partners LLC (Fund 360) → THE DAYTON FOUNDATION (EIN 31-6027287) (ledger_provider) | Dayton Foundation home page: Fund 360 / Foundation Partners named? <https://www.daytonfoundation.org/> | fetched 200; no match | unverified-lead | confirmed |
| EM013 | inferred | Sage Intacct → THE VERMONT COMMUNITY FOUNDATION (EIN 22-2712 (ledger_provider) | VCF donor-portal page: Sage/Salesforce markers? <https://vermontcf.org/donor-portal/> | fetched 200; no match | unverified-lead | inferred |
| EM014 | inferred | Sage Intacct → THE NEW YORK COMMUNITY TRUST (EIN 13-3062214) (ledger_provider) | NYCT home page: Sage Intacct named? <https://thenytrust.org/> | fetched 200; no match | unverified-lead | inferred |
| EM015 | inferred | Salesforce → THE NEW YORK COMMUNITY TRUST (EIN 13-3062214) (technology_provider) | NYCT home page: Salesforce-hosted portal link? <https://thenytrust.org/> | fetched 200; no match | unverified-lead | inferred |
| EM016 | inferred | Blackbaud (Financial Edge) → CALIFORNIA COMMUNITY FOUNDATION (EIN 95-35100 (ledger_provider) | CCF home page: Financial Edge named? <https://www.calfund.org/> | fetched 200; no match | unverified-lead | inferred |
| EM017 | inferred | Oracle NetSuite → THE PITTSBURGH FOUNDATION (EIN 25-0965466) (ledger_provider) | Direct read of the first-party posting (edge used search capture) <https://pittsburghfoundation.org/systems-solutions-architect> | fetched 403; no match | unverified-lead | inferred |
| EM018 | inferred | Salesforce → THE PITTSBURGH FOUNDATION (EIN 25-0965466) (technology_provider) | Direct read of the first-party posting <https://pittsburghfoundation.org/systems-solutions-architect> | fetched 403; no match | unverified-lead | inferred |
| EM019 | inferred | Oracle NetSuite → Silicon Valley Community Foundation (EIN 20-5 (ledger_provider) | SVCF careers page (first-party): NetSuite named? <https://www.svcf.org/about/join-our-team> | fetched 200; no match | unverified-lead | inferred |
| EM021 | inferred | Oracle NetSuite → NATL CHRISTIAN CHARITABLE FDN INC (EIN 58-149 (ledger_provider) | NCF careers page: NetSuite named? <https://www.ncfgiving.com/about/careers/> | fetched -> https://www.ncfgiving.com/about/careers 200; no match | unverified-lead | inferred |
| EM034 | inferred | The Cambria Group → NPact (Fusion Laboratories LLC) (investor) | BroadWest site: Cambria named as investor? <https://www.broadwestpartners.com/> | not fetched: robots unreadable (URLError: <urlopen error Tun; no match | unverified-lead | inferred |
| EN001 | vendor_claim | NPact (Fusion Laboratories LLC) - Fund I → Silicon Valley Community Foundation (EIN 20-5 (technology_provider) | SVCF site: NPact/FIT named (sponsor-side confirmation of the vendor case study)? <https://www.svcf.org/> | fetched 200; no match | unverified-lead | confirmed |
| EN008 | inferred | Blackbaud (Financial Edge NXT) → Greater Washington Community Foundation (EIN  (ledger_provider) | GWCF portal announcement (first-party): Financial Edge NXT named as ledger? <https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived> | fetched 200; no match | unverified-lead | inferred |
| EN011 | reported | Greater Kansas City Community Foundation → INDIAN RIVER COMMUNITY FOUNDATION INC (EIN 20 (administers) | donor-portal.org tenant still live? (tenant use does not show back-office service; IRCF also sends fund access to Foundant) <https://ircf.donor-portal.org/login> | fetched 200; no match | unverified-lead | reported |
| EP003 | inferred | Blackbaud Financial Edge NXT → THE SAN DIEGO FOUNDATION (EIN 95-2942582) (general_ledger) | SDF home page: Blackbaud markers? <https://www.sdfoundation.org/> | fetched 200; no match | unverified-lead | inferred |
| EP004 | inferred | Blackbaud → NEVADA COMMUNITY FOUNDATION INC (EIN 88-02414 (general_ledger) | NCF (Nevada) home page: Blackbaud markers? <https://www.nevadacf.org/> | fetched 200; no match | unverified-lead | inferred |
| EP007 | inferred | Ren → Morgan Stanley Global Impact Funding Trust (M (payment_processor) | MS GIFT 'How it works' PDF (MS side): Ren named for disbursement? <https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gi> | fetched 200; no match | unverified-lead | inferred |
| EP008 | inferred | Renaissance Charitable Foundation → Ren for Charities ACH (payment_channel) | Ren Rapid Disbursement Engine release: RCF named as a user? <https://www.prnewswire.com/news-releases/ren-debuts-rapid-disbursement-engine-expanding-ph> | fetched 200; no match | unverified-lead | inferred |
| EQ008 | crt.sh-sourced | Foundation Source (Vennfi technology) → Charityvest, Inc. (technology_provider) | Charityvest's own guide (sponsor side, no crt.sh): Foundation Source named? <https://guide.charityvest.org/about-our-venture/charityvest-%2B-vennfi> | fetched -> https://guide.charityvest.org/about-our-venture/c 200; matched: “The Foundation Source Relationship \| The Charityvest Guide For the complete documentation ” | confirmed | confirmed |
| EQ015 | reported | Orion Advisor Solutions → GiftingNetwork (partnership) | GiftingNetwork site: Orion partnership named? <https://www.giftingnetwork.com/> | fetched 200; matched: “ponsors, and the wealth management ecosystem, distributed through the Orion and Envestnet ” | confirmed | confirmed |
| ER016 | unknown | Unknown sponsor → Edward Jones private DAF (Generations) (sponsor_of) | EJ DAF product page (independent of the release): sponsor named for the private DAF? <https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-fu> | fetched 200; no match | confirmed | unknown |
| ER018 | inferred | Bonterra → The Goldman Sachs Charitable Gift Fund (EIN 1 (technology_provider) | CAF America site: Bonterra named? (even if so, the GS Gives hop is unstated) <https://www.cafamerica.org/> | fetched -> https://cafamerica.org/ 200; no match | unverified-lead | inferred |
| ES016 | inferred | BNY Mellon Charitable Gift Fund (EIN 30- → DAF Direct widget (sponsor_of) | dafdirect.org: BNY still listed although the 990 records the DAF program's wind-down? <https://www.dafdirect.org/> | fetched 200; matched: “LeaveDAFDirect(this.href,800,600,1,1,1); return false;" href="https://bnycharitable.org/bn” | weakened | inferred |
| ES022 | inferred | GiveClear Foundation (EIN 81-3222963) → Alera Charitable (Alera Group) (sponsor_of) | Alera Group site: GiveClear named as Alera Charitable's sponsor? <https://www.aleragroup.com/> | fetched -> https://aleragroup.com/ 200; no match | unverified-lead | inferred |
| EV005 | inferred | Ren → J.P. Morgan Charitable Giving Fund (donor_export_feature) | jpmgiving.org front page: export feature described? <https://jpmgiving.org/> | fetched 200; no match | unverified-lead | inferred |
| EV006 | vendor_claim | Give Interactive → Give Interactive (vendor_claim) | No independent source can test a vendor's own volume claim; vendor home page re-read <https://www.giveinteractive.com/> | fetched 200; no match | unverified-lead | confirmed |
| EV007 | inferred | Ren (Stellar iPhi) → PNC (pnc.iphiview.com/scbf; program unnamed) (technology_provider) | Live tenant path (host resolves to a Ren load balancer) <https://pnc.iphiview.com/scbf/> | not fetched: robots disallow; no match | unverified-lead | inferred |
| EV008 | inferred | Ren (Stellar iPhi) → Unidentified iPhi tenant 'ocf' (ocf.iphiview. (technology_provider) | Public DNS: does the tenant host still exist? <dns:ocf.iphiview.com> | DNS: gaierror: [Errno -2] Name or service not known; no match | weakened | inferred |
| EX004 | probable | Twilio → Tides Foundation (corporate_daf_at) | Pledge 1% page (sponsor source for Twilio.org): only a Tides referral, not Twilio-specific <https://www.pledge1percent.org/pledging-1-percent-to-charity-made-easy-for-companies/> | fetched 200; matched: “its equity over a ten-year period and created a donor-advised fund at Tides. “We launched ” | unverified-lead | probable |
| EX017 | probable | CrowdStrike → Charities Aid Foundation (CAF America inferre (corporate_daf_at) | CrowdStrike Foundation page: CAF America named? <https://www.crowdstrike.com/en-us/about-us/crowdstrike-foundation/> | fetched 404; no match | unverified-lead | probable |
| EX025 | probable | Pledge 1% → Tides Foundation (referral_partner) | Pledge 1% public page (edge used a 403 community guide) <https://www.pledge1percent.org/pledging-1-percent-to-charity-made-easy-for-companies/> | fetched 200; no match | unverified-lead | probable |
| EY006 | reported | Candid → DAFgiving360 (Schwab Charitable) (donor_research_link) | Direct read (edge used a search snippet) <https://dafgiving360.org/explore-charities> | fetched -> https://www.dafgiving360.org/explore-charities 200; matched: “maximize the impact of their gifts. View charities recommended by CDP Candid Search Candid” | confirmed | confirmed |
| EY007 | reported | Charity Navigator → DAFgiving360 (Schwab Charitable) (donor_research_link) | Direct read (edge used a search snippet) <https://dafgiving360.org/explore-charities> | fetched -> https://www.dafgiving360.org/explore-charities 200; matched: “, revenue range or employer identification number (EIN). Visit Candid Charity Navigator Ch” | confirmed | confirmed |
| EY008 | reported | Candid → Vanguard Charitable (data_feed) | Vanguard Charitable nonprofit page (sponsor side): Candid named? <https://www.vanguardcharitable.org/nonprofit-organizations> | fetched 200; matched: “rn more about our due diligence process. Show More Show Less Why is a Candid profile so im” | confirmed | confirmed |
| EY015 | reported | Charity Navigator → Benevity (charity_verification) | Direct re-read of the Benevity page (the snippet text was not on the 2026-11-15 fetch) <https://benevity.com/solutions/nonprofit-due-diligence> | fetched 200; no match | weakened | reported |
| EY018 | reported | IRS EO BMF / Pub 78 → Daffy (charity_verification) | Daffy help centre front page: IRS status check described? <https://help.daffy.org/en/> | fetched 200; no match | unverified-lead | reported |
| EZ001 | unknown | Unknown sponsor → Edward Jones private DAF (Generations) (sponsor_of) | EJ DAF product page: sponsor named for the private DAF? <https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-fu> | fetched 200; no match | confirmed | unknown |
| EZ002 | unknown | Unknown sponsor → Edward Jones private DAF (Generations) (sponsor_of) | EJ DAF product page: sponsor named for the private DAF? <https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-fu> | fetched 200; no match | confirmed | unknown |
| EZ003 | unknown | Renaissance Charitable Foundation → Edward Jones private DAF (Generations) (sponsor_of) | RCF home page: Edward Jones named? (the standard EJ CGF is RCF's; only a private-DAF reference would contradict) <https://renaissancecharitable.org/> | fetched 200; no match | confirmed | unknown |
| EZ010 | unknown | Pave Finance → Any DAF sponsor or program (technology_provider) | Pave home page: any DAF/charitable offering? <https://www.pavefinance.com/> | fetched 200; no match | confirmed | unknown |
| EZ012 | unknown | National Philanthropic Trust → Wells Fargo DAF program (sponsor_of) | NPT home page: Wells Fargo program named? (absent = slot stays unconfirmed) <https://www.nptrust.org/> | fetched 200; no match | confirmed | unknown |
| EZ022 | unknown | Unknown sponsor → U.S. Bank donor-advised fund offering (sponsor_of) | U.S. Bank charitable-giving page re-read: sponsor named? <https://www.usbank.com/wealth-management/charitable-giving-strategies.html> | fetched 200; no match | confirmed | unknown |

## 7. Changes to report figures (Find/Replace proposals)

These are proposals only; neither document was edited. "Occurrences" is the number of times the Find text appears in the target file as of this run (1 = safe to apply).

- **FR1** — `research/DAF-INDUSTRY-REPORT-2026-11.md` (occurrences: 1)
  - **Find:** "The relationship graph has 131 nodes and 167 edges, every edge sourced and status-labelled"
  - **Replace with:** "The consolidated relationship graph (2026-11-19) has 893 nodes and 1051 edges, merged from the base file and 26 additions files (1110 rows; 51 duplicates merged, 8 alias self-loops set aside), every edge sourced and status-labelled (repo [`relationship-graph-edges-consolidated-2026-11-19.csv`](../data/mission-2026-11-14/relationship-graph-edges-consolidated-2026-11-19.csv))"
- **FR2** — `research/DAF-INDUSTRY-REPORT-2026-11.md` (occurrences: 1)
  - **Find:** "134 confirmed (one more after red-team), 17 historically confirmed, 11 inferred, 5 unknown. A red-team sample of 15 "confirmed" edges found 0 status errors and 2 scope imprecisions"
  - **Replace with:** "958 confirmed, 23 historically confirmed, 47 inferred, 11 unknown, 5 reported, 3 probable, 2 unverified lead, 1 pending, 1 rejected. A wave-2B red-team sample of 15 "confirmed" base edges found 0 status errors and 2 scope imprecisions; a 2026-11-19 red team of all 109 inferred, unknown, reported, probable, pending, vendor-claim and crt.sh-sourced edges (one independent public check each) marked 41 confirmed, 16 weakened, 52 unverified leads and 0 contradicted (repo [`gap19-graph-consolidation.md`](mission-2026-11-14/gap19-graph-consolidation.md))"
- **FR3** — `research/DAF-INDUSTRY-REPORT-2026-11.md` (occurrences: 1)
  - **Find:** "- On public evidence, sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**."
  - **Replace with:** "- On public evidence, sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**. The consolidated graph (2026-11-19) raises this to 32.2% ($105.62bn, 54 sponsors) on any confirmed Ren/Stellar technology, administration or payment edge, and 31.6% (47 sponsors) when the edge's source is dated 2024 or later; NPT (12.8%) still rests on hosting evidence [I] (repo [`gap19-graph-consolidation.md`](mission-2026-11-14/gap19-graph-consolidation.md) §4)."
- **FR4** — `research/mission-2026-11-14/vendor-dependency-concentration.md` (occurrences: 1)
  - **Find:** "relationship-graph-edges.csv) has 167 edges."
  - **Replace with:** "relationship-graph-edges.csv) has 167 edges (base file only; the consolidated graph of 2026-11-19, [`relationship-graph-edges-consolidated-2026-11-19.csv`](../../data/mission-2026-11-14/relationship-graph-edges-consolidated-2026-11-19.csv), has 1051 edges and 893 nodes; see [gap19-graph-consolidation.md](gap19-graph-consolidation.md))."
- **FR5** — `research/mission-2026-11-14/vendor-dependency-concentration.md` (occurrences: 1)
  - **Find:** "Ren appears in 34 edges and Renaissance Charitable Foundation (RCF) in 22"
  - **Replace with:** "In the base file Ren appears in 34 edges and Renaissance Charitable Foundation (RCF) in 22; in the consolidated graph (2026-11-19) Ren (incl. Stellar/iPhi) has degree 131 (112 confirmed) and RCF 29 (24 confirmed). Foundant Technologies has the highest degree (365), almost all from its own client list"
- **FR6** — `research/mission-2026-11-14/vendor-dependency-concentration.md` (occurrences: 1)
  - **Find:** "Ren: **inferred** (support email @reninc.com)"
  - **Replace with:** "Ren: **inferred, weakened** (support email @reninc.com; BofA Program Guidelines v3.2024 say the fund "is currently administered by Bank of America Private Bank" and do not name Ren; E083, gap19 red team)"
- **FR7** — `research/mission-2026-11-14/vendor-dependency-concentration.md` (occurrences: 1)
  - **Find:** "| **Inferred** (CapShift page refers to "your Renaissance Charitable Foundation DAF account")"
  - **Replace with:** "| **Confirmed** (CCF Program Circular, EF001, supersedes inferred E034)"
- **No change proposed:** sponsor-asset CR3/CR5/HHI (§4). The report's wording that Edward Jones's private DAF has no public sponsor stands (E018, ER016, EZ001–EZ003 confirmed as negatives).

## 8. Limits

- One check per edge. Unverified leads are not refutations: many sponsor pages sit behind Cloudflare or refuse robots.txt (cct.org, pittsburghfoundation.org, armanino.com, nhf.org, npact.com, stifelcharitable.org, iphiview.com disallows the tenant paths).
- The alias table is hand-built. Edges between a vendor's product node and the vendor itself become self-loops and are excluded from the statistics.
- Asset shares use DAFRC FY2024 Schedule D values matched by EIN. Programs inside a sponsor (for example the J.P. Morgan funds at NPT) add no assets of their own.
- Re-observations of a tenant (marked in the Check column) are dated evidence, not independent corroboration.

