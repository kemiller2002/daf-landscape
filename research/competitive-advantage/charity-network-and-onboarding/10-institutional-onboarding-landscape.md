# 10 - Institutional Onboarding and Migration Landscape

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Track B1. Scope: how DAF sponsors, DAF technology vendors and community-foundation (CF) software vendors onboard new programs and migrate existing books. Covers public timelines, prices, professional services, customer duties, data migration, integration, training, limitations, failures, complaints, switching barriers and contractual exit-data terms.

Machine-readable data:
- [`data/onboarding-observations.csv`](data/onboarding-observations.csv): 67 coded observations.
- [`data/sources-ONB.csv`](data/sources-ONB.csv): 31 external sources.

Internal repo files are cited by path. This note builds on these files and does not repeat them:
- `research/migration-runbook-2026.md`
- `research/revenue-retention-and-switching-2026-11-11.md`
- `data/switching-cost-control-matrix-2026.csv`
- `research/ren-legal-entities-public-msa-contract-portability-audit-2026-11-12.md`
- `research/mission-2026-11-14/queue-contract-data-rights-agent-controls.md`
- `research/mission-2026-11-14/queue-ren-iphi-attrition.md`
- `data/mission-2026-11-14/cf-vendor-migrations-2022-2026.csv`

## Summary

- **Launching a new program and migrating an existing book are different products, and vendors advertise only the first.**
  - Published new-program timelines:
    - Foundation Source/Charityvest: "a few business days" on a shared sponsor [ONB-023].
    - Ren: 90-120 days and "around $50,000" [ONB-020].
    - NPT private label: 14-16 weeks [ONB-019].
    - akoyaGO: about 13-17 weeks [ONB-024].
  - These are all VENDOR-CLAIM. No DAF vendor publishes a timeline or price for converting an existing book.
- **Primary sources give a consistent picture of real migrations (VERIFIED-FACT, Medium-High).**
  - A single-vendor CF conversion takes 3-6 months from contract to system of record. Berkshire Taconic took 3 months plus a 1-month extension. Hartford took 6 months [ONB-002].
  - A national sponsor took about 8.5 months from vendor selection to go-live. AEF moved to Ren between 2025-07-23 and 2026-04-06 [ONB-015]. Its old portal stayed up about 7 more months.
  - A multi-system rebuild takes 18 months or more. Arizona CF's took that long [ONB-002].
  - At least one large implementation never reached production. FFTC paid Give Interactive $654,500 in CY2023, then went live on GiftingNetwork in July 2026 (`research/mission-2026-11-14/queue-vendor-channel-moves.md`). The abandonment is INFERENCE, Medium.
- **Every cutover we found freezes operations, which is the friction donors and charities actually see (VERIFIED-FACT, High).**
  - Grant-processing holds ran from 4 days (ImpactAssets, planned) to about 2 weeks (Lehigh Valley), 3.5 weeks (AEF submission cut-off to go-live) and about 5.5 weeks (GWCF, after a schedule slip) [ONB-011, ONB-013, ONB-015, ONB-016].
  - All six donor notices reviewed made users re-register or reset credentials (INFERENCE from 6/6, High).
- **How much history moves is a negotiated variable, not a constant.**
  - AEF to Ren: 2 years self-service.
  - GWCF to NPact Foundation Cloud: 7 years [ONB-012].
  - Arizona to Sage Intacct: 26 years, "over concerns expressed by a few consultants" [ONB-002].
  - Balance-forward and truncated history are the cheap default. Full history is a choice that costs more.
- **Public exit terms are narrow and short (VERIFIED-FACT on templates, High; signed contracts unknown).**
  - Ren iPhi: 15 days of "industry-standard format" access after termination.
  - NPact: data deleted 10 business days after hosting ends, and export is a paid service.
  - Ren RAC: returns only customer-provided "Customer Materials".
  - Foundant: CSV "in the same format as such data is stored", within 30 days, with custom export billable [ONB-004; `queue-contract-data-rights-agent-controls.md`].
  - Foundant is the only template found with termination for convenience (30 days) and a pro-rata refund.
- **Most of the cost shows up as client-side labour and third-party consulting, not vendor list price.**
  - 2022 CF implementation fees: "several thousand dollars to more than $20,000" [ONB-001].
  - 990 Part VII-B implementation-consultant lines run $115k-$724k a year: Maine CF, GNOF, Associated Jewish Charities of Baltimore, JCF San Francisco (`data/mission-2026-11-14/form990-contractors-harvest-full.csv`).
  - JCF paid Ren $417,742 for "PREVIOUS DONOR PORTAL SUPPORT" after it switched. That is a direct tail and dual-run cost (VERIFIED-FACT, High).
- **Vendor-forced events drive many migrations: product sales, hosting moves and decommission dates.**
  - Blackbaud sold FIMS/DonorCentral to NPact in 2022 [ONB-008].
  - NPact moved Host*Net to Azure in May-June 2023 with new usernames [ONB-009].
  - Arizona built its portal in a "90-day crunch" before a vendor shut-off [ONB-002].
  - Switching windows are therefore partly predictable (INFERENCE).
- **Implication for Unbound (RECOMMENDATION).** Barriers rank as follows by evidence:
  1. Operational freeze and credential re-enrolment.
  2. History truncation.
  3. Contractual exit-data limits.
  4. Client project capacity.
  5. Charity payment re-validation.
  6. Fund-accounting conversion (pools, fees, opening balances).

  An entrant that can promise and prove "no visible freeze, full history, credentials and charity enrolments carried over" competes on the friction that is documented, not on price. This bears on a sequencing tension: release 1 is proposed with "no migration", but the ratified entry segment (CNV-ECO-004) consists entirely of sponsors that already have a system. See Implications.

## 1. Onboarding archetypes

| Archetype | Who is onboarded | Published timeline / price | What moves | Evidence |
|---|---|---|---|---|
| A. Greenfield branded program on the vendor's sponsor | RIA, wealth firm, bank or trust | Few business days (FS/Charityvest); 90-120 days and ~$50k (Ren/RCF); 14-16 weeks (NPT) | Nothing. New accounts only | VENDOR-CLAIM [ONB-019, ONB-020, ONB-023] |
| B. Same sponsor, platform replaced | National, faith or single-issue sponsor | AEF: ~8.5 months selection to live; Signatry overlapped Ren managed services and Give in 2021-22 | Accounts, balances, history (depth varies), identities, in-flight grants | VERIFIED-FACT [ONB-015]; `queue-give-interactive-displacement.md` |
| C. CF core-system conversion | Community foundation | 3-6 months single vendor; 18+ months multi-system; 2017 guide says 1-2 years | Full GL, fund ledger, pools, fees, CRM, grants, scholarships, portal | VERIFIED-FACT (self-reported) [ONB-002, ONB-003] |
| D. Vendor-initiated re-platform (same product) | Existing customers | NPact Azure move: ~6 h downtime per system, 5-6 weeks across the base | Hosting and credentials | VERIFIED-FACT [ONB-009] |
| E. Charity-side enrolment | Grantee charities | GWCF: payments delayed until the charity "completes validation"; Chariot OAuth "not self-service" | Bank details, validation status | VERIFIED-FACT [ONB-012]; `queue-contract-data-rights-agent-controls.md` |
| F. Donor-level sponsor transfer | Donor | Cash-only, needs sending-sponsor cooperation, "weeks" (anecdotal) | One fund, as a grant | `research/mission-2026-11-14/daf-user-complaints-deep-research.md` |

The vendor marketing that donors see (Ren: switching is "Not difficult at all" [ONB-020]) describes archetype A, or B from the receiving side only. No public source prices or times archetype B or C from the leaving side. `data/switching-cost-control-matrix-2026.csv` L27 still holds: "No Ren/TIFIN actual customer migration TCO verified".

## 2. Timelines: verified against claimed

| Case | From → To | Duration | Freeze seen by users | Class |
|---|---|---|---|---|
| Berkshire Taconic CF ($214M) | FIMS → Foundant CSuite | 3-month vendor plan, extended 1 month; 3-week parallel run; portal launched weeks after go-live | Few days without processing | VERIFIED-FACT (self-report) [ONB-002] |
| Hartford Foundation ($1B) | FIMS → Foundant | 6 months contract to system of record (4 months training and clean-up, 1-week freeze, 2 months dual run) | 1 week | VERIFIED-FACT (self-report) [ONB-002] |
| Arizona CF ($1.3B) | FIMS/DonorFirst/gGrants → Salesforce + Intacct + Foundant | Portal 6/2020; GL 4/1/2021; SLM 12/2021 | Not stated | VERIFIED-FACT (self-report) [ONB-002] |
| Lehigh Valley CF | DonorCentral → CSuite | Pause about Sep 27 to Oct 10, 2023; portal Nov 2023 | About 2 weeks with no grant payments | VERIFIED-FACT [ONB-013] |
| Winston-Salem Fdn | Blackbaud/Foundation Cloud portal → Foundant | Old portal closed Aug 21; new portal Sep 30 (2024) | About 6 weeks with no portal | VERIFIED-FACT/INFERENCE (year) (`cf-vendor-migrations-2022-2026.csv`) |
| CF of Acadiana | Ren iPhi → CSuite | Blackout Mar 19-Apr 6; portal live May 14 (2025 inferred) | About 8 weeks to portal | INFERENCE, Medium (same file) |
| AEF (national) | NPact DonorCentral → Ren | Selected 2025-07-23; submission cut-off Mar 13; blackout Mar 23-Apr 6; live Apr 6 2026; old portal off Oct 31 2026 | 3.5 weeks with no new submissions processed on time | VERIFIED-FACT [ONB-015] |
| GWCF | Donor Central + legacy GL → Foundation Cloud + FE NXT | Launch slipped to Sep 21 2026; requests after Aug 14 held | About 5.5 weeks hold; full closure Sep 14-20 | VERIFIED-FACT [ONB-011] |
| ImpactAssets | iPhi → new "DAF Hub" (Give per repo) | Announced Sep 8 2026; homepage login still iPhi on Nov 26 | Read-only for 4 days (planned) | Low: page looks like a draft [ONB-016, ONB-017] |
| FFTC ($2.95bn DAF) | Blackbaud → Give (chosen 2022) → GiftingNetwork portal | Chosen by 2022; Give paid $654.5k in 2023; GiftingNetwork live 2026-07-01 | n/a | INFERENCE, Medium (`queue-vendor-channel-moves.md`) |

**Reading (INFERENCE, Medium).** The vendor build is rarely the critical path. The case studies attribute delay to these causes:
- **Staffing on the vendor side.** Berkshire: "it took a few weeks to get the right staff assigned".
- **Rescheduled client training.** Berkshire extended its plan by a month for this reason.
- **Clean-up and duplicate merging.**
- **Year-end and audit boundaries.** Arizona chose a fiscal-year-start cutover and in hindsight preferred mid-year after the audit.
- **Vendor-imposed deadlines.**

A self-report may hide the bad parts. The case studies are the successful projects foundations volunteered (survivorship bias).

## 3. Price and professional-services evidence

| Item | Figure | Class |
|---|---|---|
| CF implementation fee range | "several thousand dollars to more than $20,000"; most vendors refused to price scenarios | VERIFIED-FACT, 2022 [ONB-001] |
| Foundant CommunitySuite subscription | $4.5-18k small, $23-87k mid, $87-215k large (asset-based) | VERIFIED-FACT (vendor-supplied) [ONB-001] |
| akoyaGO | $5k+/$7.5k+ small; $12.5k+/$20k+ mid; $25k+/$40k+ large (one-time/annual) | Same [ONB-001] |
| Foundant services rate card | $250/h consulting; $2,500 per trainer-day; new-admin training $500-2,500; services fixed-fee per SOW; client-caused delays billable | VERIFIED-FACT [ONB-005]; `competition-and-pricing.md` CP26 |
| Ren program start | "around $50,000" | VENDOR-CLAIM [ONB-020] |
| Ren add-ons | Data Migration, SSO, API Integration as separately ordered one-time services; iPhi BPO staff augmentation | VERIFIED-FACT (catalogue, no prices) [ONB-021, ONB-022] |
| Third-party implementation (990 VII-B) | Maine CF/Foundation Partners $164k + $362k; GNOF/Fusion Labs $118k then Clark Nuber $115k; AJC Baltimore/RSM $217k + $155k; JCF SF Salesforce $724k (one year) | VERIFIED-FACT (`form990-contractors-harvest-full.csv`) |
| Tail / dual run | JCF paid Ren $417,742 for "PREVIOUS DONOR PORTAL SUPPORT" (FYE 6/2023) | VERIFIED-FACT (same file) |
| Abandoned implementation | FFTC paid Give $654,500 (CY2023) | VERIFIED-FACT (payment); INFERENCE (abandonment) |
| Platform pricing shock | Sage Intacct entity pricing for ~1,900 funds would have been "exorbitant"; Sage waived it | VERIFIED-FACT (self-report) [ONB-002] |

Part VII-B lists only the five highest contractors above $100k, so smaller projects do not appear. Absence of a line proves nothing.

**Cost structure (INFERENCE, Medium).** Visible vendor implementation fees are small: $5k-$25k+ list for CF systems. Total switching cost is driven by:
- client staff time (TAG: at least 0.5 FTE or a consultant for large foundations [ONB-002]);
- third-party consultants ($100k-$700k+ a year at large sponsors);
- dual-run and tail fees;
- lost service during the freeze.

The runbook's switching-cost formula (`research/revenue-retention-and-switching-2026-11-11.md` §6) is the right frame. The public evidence fills in the labour and consulting terms, not the vendor terms.

## 4. Customer responsibilities, data migration, integration and training

**Customer duties (VERIFIED-FACT, High).**
- The Foundant PSA requires:
  - an internal project manager;
  - meeting participation;
  - "complete, accurate and prompt delivery of information, data and feedback".
- Under the same PSA, delays the client causes "may result in additional applicable charges" [ONB-005].
- TAG puts project management, change management, requirements, data mapping and clean-up, integrations and business-specific training on the foundation [ONB-002].
- In Ren's white-label model the firm sets minimums, investment menus and portal workflows. Program assets sit in "an investment account with Customer" [ONB-020, ONB-021]. Custody at the institution makes the institution's custody feed a hard integration dependency for any successor (INFERENCE).

**Data migration patterns (VERIFIED-FACT).**
- **History depth:** 2 years self-service (AEF), 7 years (GWCF), 26 years (Arizona), "all" (ImpactAssets, planned).
- **Draft or in-flight losses:** AEF's 2024 Blackbaud → NPact move removed shopping-cart draft grants older than 90 days (`historical-daf-sponsor-technology-lifecycle-2011-2026.md`, HL09). Flint's legacy page: gifts "may not appear in the donor portal". Tampa Bay: online gifts "temporarily unavailable" months after cutover (`cf-vendor-migrations-2022-2026.csv`).
- **Clean-up strategy:** Berkshire and Arizona both advise doing minimal clean-up before conversion and cleaning in the new system. Berkshire then spent "several days" with the whole team merging duplicates [ONB-002].
- **Conversion mechanics:** dry runs then a final migration, with a freeze to verify (Hartford). Opening balances at month-end close. Foundant's Beginning Balance Implementation Guide says this, read via search index only because the page returned 403.

**Integration (VERIFIED-FACT).**
- Arizona's stack needed Workato (7 production recipes) and a month-end Clearwater-to-Intacct pool-apportionment feed, with daily balances deferred [ONB-002].
- Foundant GLM is fed by export and import, not API.
- No incumbent template found grants an external API right. NPact §2.4 bans access through third-party products (`queue-contract-data-rights-agent-controls.md`).

**Training (VERIFIED-FACT).**
- AEF ran 4 virtual sessions (2 for advisors, 2 for donors) inside the blackout [ONB-015].
- GWCF ran webinars, office hours and in-person sessions [ONB-011].
- Berkshire held weekly 2-hour sessions with sandbox courses [ONB-002].
- Donor-facing training is part of every cutover.

## 5. Configuration limitations, failures and complaints

- **Limitations (VERIFIED-FACT).**
  - FIMS had a limited API for "custom data feeds" (2017) [ONB-003].
  - The NPact Azure move removed the customer's solution-admin role. User changes now need a support ticket [ONB-009].
  - Foundant exit export is "as stored" CSV [ONB-004].
  - Arizona found 4 fund-related gaps in Intacct: fee assessment, pool apportionment, rebalancing and the fund object. It filled them with paid vendor development, consultant work and in-house code [ONB-002].
- **Failures and slips.**
  - GWCF launch slipped and caused a ~5.5-week processing hold (VERIFIED-FACT).
  - FFTC abandoned its Give implementation (INFERENCE, Medium).
  - ImpactAssets' announced Sep 2026 launch is not visible (INFERENCE, Low).
  - akoyaGO itself reports 85% on-time completion of migration tasks, meaning 15% late (VENDOR-CLAIM) [ONB-025].
- **Complaints.**
  - Arizona on FIMS: "extreme risk of erroneous payment processing", weak validation, manual workarounds [ONB-002].
  - Donor forum anecdotes on transfer friction (`daf-user-complaints-deep-research.md`, Low).
  - Not reachable: G2/Capterra/Software Advice review pages for CommunitySuite returned 403, and no indexed reviews of iPhi, DFX or DonorCentral were found. User-review evidence is therefore **not publicly documented here**, which is not evidence that complaints are absent.

## 6. Contractual exit-data provisions (public templates)

| Vendor / template | Post-termination data window | Format | Fee for export | Termination for convenience | Renewal / notice | Source |
|---|---|---|---|---|---|---|
| Ren iPhi MSA (2023 draft) | 15 days | "industry-standard format" (unspecified) | Not stated | None ("only as permitted in this Section 10") | 12-month renewal; notice "thirty (60)" days (drafting error) | `queue-contract-data-rights-agent-controls.md` |
| Ren RAC / RCF MSA (June 2023) | Return on request or at termination | Not specified; only customer-provided "Customer Materials" | Not stated | Customer pays fees to end of quarter | 1-year auto-renew; 60-day notice | `ren-legal-entities-...-audit-2026-11-12.md` |
| NPact Standard Terms (2025-08-26) | Deleted 10 business days after hosting ends | No export duty; export is a Professional Service | Yes (PS) | Remaining-term fees on specified terminations | 3-year initial term; 90-day notice | `queue-contract-data-rights-agent-controls.md` |
| Foundant MSA (v01/2024) | Returned or erased within 30 days | CSV "in the same format as such data is stored" via reporting tools | Custom export is billable PS | Yes, 30 days; 100% refund in first 90 days, pro rata after | Auto-renew; 30-day notice | [ONB-004] |
| TIFIN group terms | Access ends at termination; users barred from archiving or downloading | n/a | n/a | Per signed agreement | Auto-renew by default | `queue-contract-data-rights-agent-controls.md` |
| akoyaGO, Give Interactive, GiftingNetwork, NPT, Fidelity Charitable, Schwab DAFgiving360, Goldman Sachs, BofA programs | **Not publicly documented** | | | | | searched 2026-11-26 |

All rows are published templates. Signed order forms and work orders can override them, and none were seen. **No template promises transition assistance at a stated price, an open schema, or export of vendor-generated records** (audit logs, screening snapshots, decision lineage). The Ren RAC gap is analysed in the Ren MSA audit.

## 7. What makes DAF onboarding and migration slow and expensive

INFERENCE from the facts above unless marked.

1. **The product is a regulated sub-ledger, not just a CRM.**
   - The ledger holds unitized pools with daily or monthly NAV, fee schedules, spending policies for endowed funds, restricted and SMA accounts, and grants payable.
   - Opening balances must tie to custody and bank at a period close, so cutovers cluster at month-end and fiscal year-end and are shaped by the audit (Arizona).
   - Arizona's Intacct gaps were all fund-accounting gaps.
2. **Every in-flight item needs an owner.**
   - Approved-unpaid grants, pending stock gifts, drafts, recurring grants and uncashed checks need a home at cutover.
   - Incumbents solve this with a freeze: stop accepting or processing for 4 days to 5.5 weeks. Draft deletion at AEF shows the cheap path.
3. **Identity cannot move, so it is re-issued.**
   - Credentials, MFA and advisor delegations were reset in all six notices. That creates donor support load and a phishing window. NPact even issued @npact.onmicrosoft.com usernames.
4. **History is priced, and depth is traded away.**
   - Balance-forward or 2-year history cuts mapping effort.
   - Full history (Arizona's 26 years) is a deliberate client choice made against advice.
5. **Exports are "as stored", not semantic.**
   - Foundant CSV-as-stored and Ren "industry-standard format" mean the receiver must reverse-engineer the source schema.
   - Generated records (decision lineage, screening evidence) are not promised.
6. **Client capacity is the constraint.**
   - Vendors write client duties and delay charges into contracts (Foundant PSA).
   - Large sponsors buy $100k-$700k+ a year of outside help.
   - Small CFs have 1-5 staff.
7. **Charities and custodians are counterparties too.**
   - Charity payment validation must be redone (GWCF), and custody feeds must be re-pointed.
   - Ren's model keeps custody at the distributing institution, so changing the administrator does not move the assets but does re-point every feed.
8. **The calendar is often set by vendors.**
   - Product sales (FIMS 2022), hosting moves (2023) and decommission dates (Arizona 2020) force migrations on the vendor's timetable, and projects then compress (the "90-day crunch").

### Switching barriers ranked by evidence strength

| Rank | Barrier | Evidence | Strength |
|---|---|---|---|
| 1 | Operational freeze (grant processing hold) | 6 primary sponsor notices; 4 days to 5.5 weeks | High (VERIFIED-FACT) |
| 2 | Credential and delegation re-enrolment | 6/6 notices; NPact hosting doc | High |
| 3 | Short or undefined exit-data rights; paid export; no generated-record export | 4 public templates | High on templates; Unknown on signed contracts |
| 4 | History truncation in the successor | AEF 2y, GWCF 7y | High |
| 5 | Client project capacity and consultant spend | TAG case studies; 990 VII-B lines | Medium-High |
| 6 | Renewal, notice and termination-fee mechanics (60-90 day notice; 3-year NPact term; fees to quarter end or remaining term) | Templates | High on templates; Unknown on signed contracts |
| 7 | Fund-accounting conversion complexity (pools, fees, opening balances, FY/audit timing) | Arizona; Hartford; Foundant guide (search-level) | Medium |
| 8 | Charity payment re-validation after cutover | GWCF | Medium (single case) |
| 9 | Dual-run and tail fees | JCF $417,742; Signatry overlap | Medium (two cases) |
| 10 | Custody and investment-advisor coupling | Ren product description (custody at customer) | Medium (structural INFERENCE) |
| 11 | Implementation failure risk | FFTC/Give; akoyaGO 85% on-time | Low-Medium (INFERENCE) |
| 12 | Staff skill lock-in (staff trained on one vendor) | ACT for Alexandria RFP | Low |

Counter-evidence that barriers are surmountable: Ren iPhi lost 6 of 57 tracked clients in 2023-2026, and all dated CF portal switches ended on Foundant (`queue-ren-iphi-attrition.md`, `queue-bdc-coverage-migrations-goodstack.md`). Migration happens at roughly 2-4% a year in that sample (INFERENCE, Medium). The barriers slow switching and raise its cost. They do not prevent it.

## Implications for Unbound

**Where to compete (RECOMMENDATION).** The documented pain is in the freeze, identity reset, history loss and exit opacity. Unbound's append-only event ledger, deterministic controls and DB-backed durable queues fit a design that removes those frictions without moving money (CNV-LEG-001). Price alone does not attack the main cost, which is client labour and the freeze.

**Proposed design: migration as a governed run.** This refines CNV-EXP-002, UNB-TEN-011, UNB-GAP-025 and RR-REQ-X-061-r1. It reuses `research/ai-native-daf-enterprise/workflow-innovation/03-alternative-designs/W8-system-of-record-migration.md` D-W8-3.

**States.** `Scoped > SourceSnapshotted(n) > Mapped > DryRunReconciled(n) > ShadowRunning > CutoverScheduled > Frozen(<=T) > FinalLoaded > Reconciled > Live > LegacyReadOnly > Archived`. Terminal `Abandoned` is reachable from any state before `Live` with no effect on the source system. This closes the gap noted in `requirements/reconciliation/2026-11-23/workflows/REPORT-ENT.md` item 12.

**Data.**
- `MigrationRun`: id, sponsor, source system and version, policy-pack version.
- `SourceSnapshot`: hash manifest, as-of, record counts by entity.
- `MappingSpec`: versioned field crosswalk with AI-proposed and human-approved flags (CNV-AIO-001).
- `IdCrosswalk`: legacy id to Unbound id per account, fund, grant, recipient and contribution.
- `InFlightRegister`: one row per approved-unpaid grant, pending contribution, draft, recurring schedule and uncashed check, each with an owner (legacy or Unbound) and a disposition.
- `ReconciliationReport`: counts, amounts, balances by fund, NAV and unit holdings, Schedule D aggregates, with zero unexplained differences.
- `CutoverDecision`: signed by a sponsor controller.

**Rules.**
- Full history by default, matching CNV-EXP-002's "full fund history". Balance-forward only with written sponsor waiver per data class.
- At least 2 dry runs with automated diffs before cutover.
- A shadow run replays new legacy transactions daily and diffs them, replacing manual dual entry (Berkshire 3 weeks, Hartford 2 months).
- Grant recommendations are **accepted** during the freeze and queued durably, never rejected or deleted (contrast AEF drafts). The design target is a freeze of 2 business days or less for processing and no freeze for submission. This is a HYPOTHESIS to test.
- Cutover is at a month-end close, and the sponsor chooses the audit boundary.

**Failure behaviour.**
- A reconciliation difference blocks `FinalLoaded > Reconciled`.
- If the freeze exceeds T, the sponsor may roll back to legacy, and the queued recommendations are exported back.
- An unknown in-flight item blocks cutover and needs a named owner.

**Identity continuity.**
- Pre-provision donor and advisor identities from sponsor-attested contact data.
- Users activate by invitation with risk-based proofing (CNV-PLT-003), not mass re-registration.
- Advisor delegations and successors migrate through the IdCrosswalk.
- Open point: contact data imported in bulk should not trigger CNV-PLT-011 72-hour change holds, since it is not a change, but it must not become a bypass. See open questions.

**Charity continuity.**
- CNV-EXP-002 already pays enrolled charities through their networked rail.
- For non-networked charities, a predecessor's verified bank evidence could count as CNV-PAY-002 destination evidence only with provenance (verifier, date, method). Otherwise first payment waits for verification. GWCF shows the delay is real, so pre-cutover outreach should be a migration task.

**Exit symmetry (sales asset).** Publish Unbound's own exit terms:
- Self-service export at any time of all records, including generated records such as decision lineage, screening snapshots, audit events and statements, in a documented open schema (the `research/migration-runbook-2026.md` interchange schema).
- At least 90 days of read access after termination.
- No export fee.
- Every incumbent template found is weaker. Fund moves at exit remain grant-based (CNV-ENT-002, UNB-XIN-SAS-007).

**Source adapters, prioritised by entry segment (CNV-ECO-004).** Mid-size national and single-issue sponsors with 5k-50k funds are most likely on Ren DFX or iPhi, NPact, Give or in-house systems. Community foundations, who run Foundant and akoyaGO, are not the entry segment. Most public migration evidence comes from CFs, so its transfer to national sponsors is INFERENCE.

**Flagged tension (not a contradiction of a ratified clause).**
- The proposed release-1 scope says "no migration in R1": one reference sponsor (`requirements/discovery/2026-11-23-cross-industry/17-RELEASE-1-SCOPE.md`, UNB-XIN-OTH-002 deferred).
- The ratified entry segment (CNV-ECO-004) consists of sponsors that already have a system and history.
- CNV-EXP-002 requires full-history import.
- Unless the first commercial sponsor is greenfield, migration sits on the critical path to the first paying sponsor. The product owner should decide whether migration capability is a release-1.x gate.

## Open questions / evidence gaps

1. Signed exit terms. No executed Ren, NPact, Foundant, Give, TIFIN or NPT order form or work order was seen. Template terms may be overridden.
2. No public cost or time for migrating **out** of Ren DFX or iPhi, or out of NPT GivingPoint, Fidelity, DAFgiving360, Goldman Sachs or BofA programs. Their onboarding and offboarding is **not publicly documented**.
3. Is FIMS (now NPact) under an end-of-support date? None was found. Two 2022 case studies cite "sunset" expectations [ONB-002].
4. Did ImpactAssets' Sep 2026 launch slip, or is the page a draft? Re-check its homepage login.
5. The FFTC Give abandonment: is there a cause or any recovery? 990s for CY2025-26 are not yet indexed.
6. User reviews on G2, Capterra and Software Advice were blocked (403). Re-try by an allowed route. Treat review evidence as missing.
7. Can predecessor bank-verification evidence count under CNV-PAY-002, and does bulk contact import interact with CNV-PLT-011? Both need decisions by the sponsor's counsel and the product owner.
8. Test hypothesis: an automated shadow run plus queued submissions cuts the user-visible freeze to 2 business days or less on a synthetic five-year fixture (runbook M01-M13).
