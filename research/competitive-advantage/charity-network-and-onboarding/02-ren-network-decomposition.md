# 02 - Ren charity network decomposition

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: Track A1. This study takes apart Ren's charity network: the Ren for Charities directory and portal, shared vetting, the Rapid Disbursement Engine (RDE) ACH rail, and the Renaissance Charitable Foundation (RCF) and iPhi lines. It builds on prior repo work and does not repeat it: `research/ren-tifin-chariot-deep-dive-2026-11-11.md`, `research/batch-2b-ren-tifin-chariot-charity-vetting-infrastructure-2026-11-12.md`, `research/ren-instant-grant-approval-rcf-policy-clarity-audit-2026-11-12.md`, `research/ren-iphi-platform-contract-architecture-integration-audit-2026-11-12.md`, `research/mission-2026-11-14/queue-batch31-ren-npact-gl.md` (RDE = "Ren for Charities ACH"; Legacy grants), `queue-ren-iphi-attrition.md` §6 (metric conflicts), `b49-04-fraud-diversion-controls.md` §3.3 (claim and bank controls) and `b43n26-01-in-portal-data-provider.md` (Ren's IRS listing versus Candid).

What is new here:
- the full Ren charity help centre (48 articles, read 2026-11-26);
- Ren's current Giving Platform, About and Payments pages;
- RCF's 2023 Grantmaking Due Diligence Policy, read directly;
- the TY2024 Form 990 Schedule I and F counts for RCF, AEF and MS GIFT;
- current IRS baseline counts.

Two scripts reproduce the counts: `scripts/ren_public_baseline_counts.py` and `scripts/ren_schedule_i_recipient_overlap.py`. All metrics are in `data/ren-network-metrics.csv`; sources are REN-001 to REN-040 in `data/sources-REN.csv`.

## Summary

- **Ren publishes four network numbers, and they measure different layers.** Directory: "1.8M+ charities who can access Ren grants" [REN-002]. Annual recipients: "over 140,000 charities worldwide" each year [REN-003]; the same 140,000 appeared in 2023 [REN-024]. Impact-data scope: "up to 93,000 nonprofits within Ren's network" [REN-023]. ACH enrolment reach: "25+ donor-advised fund programs" [REN-007]. Ren publishes no count of claimed charity profiles, ACH-verified bank accounts or programs that share vetting. VENDOR-CLAIM, Medium.
- **The hypothesis that the directory is built on IRS data is supported, but only for the directory layer.** Ren says it "created this listing to get IRS updates faster than ... through Guidestar" [REN-001] and markets "IRS Business Master File (BMF) checks" [REN-002]. Every claim route is keyed to IRS records: the BMF address, the phone number on the latest e-filed 990 and the officers listed with the IRS [REN-005, REN-006]. Cheque payee names follow the IRS EIN name [REN-011]. The opposing evidence is about vetting, not the listing. RCF's March 2023 policy makes GuideStar Charity Check "the cornerstone" of identity due diligence [REN-027], and iPhi bundles the GuideStar API [REN-025]. INFERENCE, Medium-High.
- **The IRS baseline already matches Ren's directory claim.** The EO BMF (2026-11-09) holds 1,984,891 unique EINs, 1,659,108 of them in subsection 501(c)(3). Pub 78 (2026-11-11) holds 1,437,288 EINs [REN-035, REN-036]. These counts are VERIFIED-FACT, High. The conclusion that Ren's 1.8M+ is not proprietary coverage is INFERENCE, Medium-High: a match in size does not prove provenance (ADVA-10).
- **Filings set a floor on actual recipients.** RCF lists 17,290 recipients of grants over $5k for TY2024 (counts only; the detail is an attachment). AEF lists 13,471 distinct EINs and MS GIFT 16,633. AEF and MS GIFT together reach 26,019 distinct EINs but share only 4,085. About 7% of their recipient EINs are absent from the current BMF and 16% from Pub 78 [REN-032 to REN-034]. The counts are VERIFIED-FACT, High; the filings are sponsor self-reports made under penalty of perjury. The recipient set that matters is tens of thousands per sponsor and mostly sponsor-specific. The 7%/16% gap is an upper bound on the tail outside the IRS files. It matches TY2024 grantees against 2026 files, so it includes organisations revoked after the grant, and it includes subordinates and churches that are legitimately absent from Pub 78. It has not yet been split by cause against a snapshot from the same period (ADVA-11).
- **Ren's main barrier is sponsor-side lock-in and distribution. The verified-payee layer comes second** (revised after ADVA-09 and ADVX-10; see §7). In 2023-2026, only 1 of 26 national, faith or affinity iPhi sponsors left, none to a new entrant, and NPT, J.P. Morgan and ICGF moved deeper into Ren (repo `queue-ren-iphi-attrition.md`). RCF white-label sponsorship carries the adviser channel: Edward Jones, Ameriprise, LPL, Northwestern Mutual and others (repo `ren-distribution-network-institutional-program-comparison-2026-11-12.md`). INFERENCE, Medium-High. The payee layer is the second barrier. It consists of claimed charity accounts (up to 50 admins each [REN-020]), bank accounts verified through Plaid, Early Warning or a manual statement review [REN-008, REN-015, REN-022], and per-grant delivery history. That history includes ACH IDs, USPS scans and third-party "Legacy" grants shown in the same portal [REN-009]. All of this accumulates from Ren's payment volume ("1.7M grants" a year, vendor claim [REN-002]). It mainly adds switching cost for a sponsor that is already leaving. No public evidence shows that it wins sponsors. INFERENCE, Medium.
- **Ren's ACH enrolment is a Ren-internal rail.** Ren pays "directly from your existing accounts, not through pooled third-party accounts" [REN-002]. One enrolment covers only the programs paid on RDE (repo `queue-batch31-ren-npact-gl.md`). AEF's move onto Ren kept charities on cheques until they re-entered and re-verified bank details in the Ren portal [REN-029], and it migrated only 33 months of grant history [REN-030]. INFERENCE, Medium. A sponsor that leaves Ren probably cannot take the ACH enrolments with it. That gap affects how CNV-EXP-002 applies (see Implications).
- **Ren grows the network through its payment flow.** Each grant cheque carries a single-use registration code and QR link [REN-019]. Since November 2026, donors can ask a charity to enrol in ACH, capped at 5 emails a year [REN-016]. Ren Recognize lets charities acknowledge donors [REN-041], and Giving Compass adds impact metrics and "Charity Stories" [REN-013, REN-014]. Every one of these features can be copied. The cheque and grant volume that feeds them cannot. INFERENCE, Medium.
- **International coverage is thin.** The directory and claim routes assume a US EIN and an IRS filing. RCF steers international giving to intermediaries [REN-028]. Under RCF's 2023 policy, a direct grant to a foreign organisation not registered with the IRS has a $50,000 minimum and typically about $4,000 of cost [REN-027]. In TY2024, RCF reported only one foreign recipient under each Schedule F Part II category [REN-032]. VENDOR-CLAIM (first-party policy) plus VERIFIED-FACT (990 counts), High. "Worldwide" in [REN-003] is marketing.
- **Ren's "validated once, trusted across the entire platform" [REN-003] reuses eligibility more than Unbound's rules allow.** CNV-GRT-003 lets cross-sponsor evidence serve only as an input. Unbound can match the friction saving by reusing verification evidence (claims, identity, bank proof) across sponsors while re-running each sponsor's eligibility decision deterministically. RECOMMENDATION.

## 1. What Ren's network is made of

| Layer | What Ren documents | Evidence | Primary source |
|---|---|---|---|
| L0 Public identity baseline | Listing built from IRS updates; BMF checks; name and address follow IRS records | VENDOR-CLAIM (first-party docs and marketing) | REN-001, REN-002, REN-010, REN-011 |
| L1 Public enrichment | 990 e-file phone and officer list used for claims. Profile page shows a "breakdown of spending among programs, fundraising, and management" (990 Part IX) | VENDOR-CLAIM (first-party docs) | REN-001, REN-005, REN-006 |
| L2 Licensed or partner enrichment | Giving Compass impact metrics and Charity Stories (2026). iPhi: GuideStar API. RCF vetting: GuideStar Charity Check (2023 policy) | VENDOR-CLAIM (first-party doc) | REN-013, REN-014, REN-025, REN-027 |
| L3 Charity-submitted data | Display name, mission, logo, address (display only), NTEE codes (up to 3), impact-report uploads, story approve/decline | VENDOR-CLAIM (first-party doc) | REN-010, REN-012, REN-013, REN-014 |
| L4 Donor-submitted data | Manual "add a charity ... to be vetted" (AEF). Addresses outside the dropdown need verification. Grant purpose, acknowledgement and contact sharing | VENDOR-CLAIM (first-party doc) | REN-030, REN-031 |
| L5 Verified control | Claimed profile; up to 50 admins; MFA; officer ID via Stripe | VENDOR-CLAIM (first-party doc) | REN-005, REN-006, REN-020 |
| L6 Verified payee | ACH approved, pending or rejected after Plaid, manual (Early Warning/Zelle) or bank-statement review | VENDOR-CLAIM (first-party doc) | REN-008, REN-015, REN-022 |
| L7 Operational history | Per-grant status, ACH ID, USPS scans, reissues, 1-to-1 payments since 2025-04-09, Legacy third-party grants | VENDOR-CLAIM (first-party doc) | REN-009, REN-017, REN-040 |
| L8 Cross-sponsor decision reuse | "once a charity is validated, it's trusted across the entire platform" | VENDOR-CLAIM | REN-003 |

**Directory coverage, participation, verified payees and know-how are four separate assets.**

1. **Coverage (L0-L1).** About 1.8-2.0M records, matching the IRS files. Any entrant can rebuild this.
2. **Active participation (L5).** Charities that claimed a profile and have working admin users. Ren publishes no count.
3. **Verified payment destinations (L6).** No count is published. The only signal is "400%+ annual growth rate in grants sent via ACH" [REN-002] and the 2023 RDE figure of more than 100,000 grants in 11 months [REN-024].
4. **Proprietary operational knowledge (L7-L8).** Returns, reissues, cheque-cashing behaviour, multi-campus address mapping [REN-016 release], manual-review outcomes and Legacy grant history. None of it is published.

## 2. Testing the IRS-origin hypothesis

**Hypothesis.** Most of Ren's directory comes from IRS public data (EO BMF and Pub 78). Donor submissions, charity submissions and operational enrichment supplement it.

| Test | Finding | Direction |
|---|---|---|
| Ren's own account of the listing | "Ren created this listing to get IRS updates faster than they were able to through Guidestar" (2022) [REN-001] | Supports IRS origin; also shows Ren moved off GuideStar for the listing |
| Vetting source named in marketing | "IRS Business Master File (BMF) checks and additional layers of vetting" [REN-002]; "vet the charity to verify it is an IRS recognized 501(c)(3)" [REN-038] | Supports BMF as the vetting baseline |
| Scale | Ren's 1.8M+ lies between Pub 78 (1.44M) and the full EO BMF (1.98M). It exceeds the BMF 501(c)(3) count (1.66M) and the deductibility-1 count (1.72M) | Fits a BMF-sized universe. Candid's own counts are the same size, so scale alone cannot tell the two sources apart |
| Record keys | Claims use the "IRS address" (BMF), the phone on the "last 990" e-filed, and officers "listed ... with the IRS". The error text reads "no phone number is on file" / "no charity officers are on file" [REN-005, REN-006, REN-022] | Strong support. The records carry IRS BMF and 990 e-file fields |
| Field authority | Cheque payee "will always match the name associated with your EIN as filed with the IRS". Address edits do not change grant addresses; charities are told to file Form 8822 to update the BMF [REN-010, REN-011] | IRS fields are the authoritative layer; charity edits are display overlays |
| Supplements | Donor manual add for vetting [REN-030]; donor address verification [REN-031]; charity NTEE edits [REN-012]; Giving Compass data [REN-013] | Supports the "supplemented by" part |
| Counter-evidence | RCF's 2023 policy relies on GuideStar Charity Check, which checks BMF, Pub 78, classification and OFAC, as the "cornerstone" of identity due diligence [REN-027]. iPhi includes the GuideStar API [REN-025] | The vetting layer (at least for RCF in 2023) and the iPhi search used Candid. Ren is not one data stack |
| Pub 78 use | Not stated anywhere Ren publishes | Open |

**Verdict.** INFERENCE, Medium-High. The Ren for Charities directory and claim layer is built on IRS BMF and 990 e-file data, with charity, donor and partner overlays. Whether today's grant vetting on DFX/RCF uses Ren's own IRS pipeline, Candid Charity Check or both is not publicly documented. RCF's policy is dated March 2023 and was re-hosted in 2026-02 without a new revision date.

**Evidence that would settle the question:**
- (a) A current RCF due-diligence policy revision, or Ren's SOC 2 system description naming its data subprocessors.
- (b) A record-level comparison through Ren's public charity search, using a sample built from the IRS files:
  - BMF-only 501(c)(4)s;
  - Pub 78-only EINs (997 exist);
  - organisations newly added in the latest BMF posting, to measure lag;
  - recently auto-revoked organisations;
  - churches absent from both files.
  
  An IRS-built index would show BMF-only entities and track the BMF posting dates. A Candid-built index would show Candid-only records. This study did not call Ren's search API, because its terms of use could not be confirmed.
- (c) Ren job postings or engineering talks that name IRS TEOS ingestion. None were found.

## 3. Workflows, decomposed

**Claiming a charity (control verification)** [REN-005, REN-006, REN-019; repo b49-04]:

| Route | Prerequisite | Speed | What it proves |
|---|---|---|---|
| Postcard | IRS address current; prior postcard attempt expired (3-week lock) | Postal days | Control of the mailbox at the IRS address |
| Telephone | Latest 990 e-filed with a phone number | Immediate | Control of the phone on the 990 (990-N and paper filers cannot use it) |
| Officer identity (Stripe) | Name appears in the IRS officer list | Near-instant | The person's identity matches a listed officer |
| Grant-cheque code | Received a cheque; code is single-use | On receipt | Possession of the cheque |

If all three self-service routes fail, Ren shows "Please contact Ren support" [REN-022]. Additional admins are invited from inside the portal, with no further verification [REN-020].

**ACH enrolment (payee verification)** [REN-008, REN-015, REN-018, REN-021, REN-022]:
- Ren recommends Plaid. The charity must tick the box to share account details.
- The alternative is "Manual (Zelle)", which the front end codes as `EARLY_WARNING`, with micro-deposit amounts or a descriptor code.
- Outcomes are approved (immediate), pending (bank-statement upload, claims-team review) or rejected ("unable to verify that the bank account belongs to your organization").
- If no route works, the charity is paid by cheque.
- Bank-change re-verification, callbacks and cooling-off periods are not publicly documented. This repeats the gap in repo b49-04.
- The donor's payment preference can override ACH. An ACH reissue happens only "if the donor allows payment flexibility" [REN-040].

**Corrections.** Display data is self-serve. Legal name and grant address follow the IRS and each DAF program. Ren tells charities to contact each program and file Form 8822 [REN-010, REN-011]. **Ren does not offer one correction that flows to every program** for grant addresses. VENDOR-CLAIM (first-party documentation), High.

**Vetting reuse and expiry.** Ren claims reuse across the platform [REN-003]. Its validity period, re-check triggers and the scope of a sponsor's override are not publicly documented. The repo audit (`ren-instant-grant-approval-...md`) warns not to read the claim as one sponsor's approval binding another. The status enum in the front end includes `EXPIRED`/`EXPIRING`, but that enum's object is unlabelled, so it is not evidence of a vetting expiry [REN-022].

**History.** The portal shows RDE grants with tracking, plus Legacy grants paid by other systems without tracking [REN-009]. Grant letters exist only for RDE grants [repo queue-batch31]. Aggregated payments ended on 2025-04-09 [REN-017].

## 4. International coverage

- The directory, claim and ACH workflows all assume a US EIN, an IRS address and a US bank reachable by Plaid or Early Warning [REN-005, REN-008]. VENDOR-CLAIM (first-party documentation) for the workflows; non-US support is not publicly documented.
- RCF routes most international giving through intermediaries [REN-028]. Under its 2023 policy, more than 98% of recipients were US-registered, and direct grants to foreign organisations not registered with the IRS need ER/ED, a $50k minimum and about $4k of cost [REN-027].
- TY2024 Schedule F Part II recipient counts: RCF 1 and 1; MS GIFT 16 and 1 [REN-032, REN-034].
- The EO BMF holds only 2,453 non-US-address EINs, and Pub 78 lists 848 non-US EINs [REN-035, REN-036].
- INFERENCE, High: Ren has no international charity-network advantage that Unbound would need to match at entry (CNV-GRT-008 defers this area anyway).

## 5. How the network grows

1. **Cheque-borne acquisition.** Every RDE cheque carries a registration code and QR link [REN-019]. Volume drives enrolment.
2. **Sponsor onboarding.** Each sponsor that moves onto RDE adds its recipients. AEF launched its Ren portal in Q2 2026 [REN-029].
3. **Donor pull.** Donor ACH request emails, launched November 2026 with a default cap of 5 a year [REN-016].
4. **Value for charities.** Consolidated grant data and export, acknowledgements (Ren Recognize [REN-041]), impact profiles and Stories [REN-009, REN-013, REN-014].
5. **Lineage.** Ren bought Pinkaloo in March 2021 [REN-039]. The charity front end still carries "Pinkaloo Charities" and "Legacy Pinkaloo" strings [REN-021, REN-022]. The charity layer is roughly five years old, which bounds how much history it can hold. INFERENCE, Medium.

## 6. Classification of each advantage

| Asset | Class | Reasoning |
|---|---|---|
| Sponsor-side platform integration: ledger, fund accounting, custodian feeds, statements, staff workflows across 150+ programs | **Defensible; the primary barrier** (added after ADVA-09) | 1 of 26 national, faith or affinity iPhi sponsors left in 2023-26, and no exit went to a new entrant. Switching means a full platform migration (Track B), not a charity-network rebuild. Not reproducible by building a charity directory |
| Distribution and sponsor entity: RCF white-label programmes for wirehouses and advisers; affiliate investment-fee economics | **Defensible; contract- and incentive-bound** (added after ADVX-10) | A firm that uses RCF as sponsor would have to change sponsor entity as well as technology. Adviser fees ride on the programme. Countering this takes a sponsor partner or a firm-sponsored charity, not technology |
| IRS-derived directory (about 1.8-2.0M records) | **Reproducible** | Public domain, refreshed monthly; this study rebuilt the counts in minutes. UNB-CHAR-010 already requires it |
| 990 e-file enrichment (phones, officers, financials) | **Reproducible** | IRS TEOS XML is public; the parsing work is ordinary |
| Impact data (Giving Compass), Candid search and Charity Check | **Purchasable** | Licensed, with use limits (repo b43n26-03); UNB-CHAR-DEC-001 rules out a runtime dependency on Candid |
| KYC and bank-verification tooling (Stripe Identity, Plaid, Early Warning) | **Purchasable** | Commodity APIs that Ren itself buys |
| Charity-submitted profile data | **Reproducible, slowly** | Same features; the content arrives only through engagement |
| Claimed accounts and admin users | **Accumulated operational history** | Bound to Ren's portal and terms; not portable to a new provider |
| ACH-verified payees | **Accumulated; a secondary barrier and a switching cost rather than a winning asset** | The verification work belongs to Ren. A sponsor leaving Ren keeps its own payee records but probably not Ren's verification state (INFERENCE from AEF [REN-029]). Charities face re-enrolment friction |
| Per-grant delivery and exception history across 150+ programs | **Accumulated; partly portable** | Each sponsor's own grant records are portable to that sponsor (CNV-EXP-002). The cross-sponsor aggregate and the exception know-how are not |
| Cross-sponsor "validated once" reuse | **Defensible network effect, reproducible in design** | The value grows with the number of sponsors on Ren. Chariot and CAF America show the pattern can be built (03 matrix); Unbound's version is constrained by CNV-GRT-003/004 |
| Cheque-borne enrolment loop | **Reproducible mechanism, volume-dependent** | Any payer can print a code. The rate of enrolment depends on cheque volume |

## Implications for Unbound

1. **Do not compete on directory size.** Seed from BMF, Pub 78, auto-revocation and TEOS XML (UNB-CHAR-010). The baseline already matches Ren's headline. Spend the effort on the tail that falls outside it: 7% of AEF/MS GIFT recipient EINs are not in the BMF and 16% are not in Pub 78 (UNB-CHAR-003, UNB-CHAR-016; repo b40n1202-b43n26-03).
2. **Copy Ren's IRS-keyed claim routes, which are cheap and reproducible.** Add the bank-change controls Ren does not document. Proposed `ClaimAttempt` record: `{charity_id, route: Postcard|EfilePhone|OfficerIdv|PaymentCode|StewardManual, source_snapshot_id, initiated_at, expires_at, outcome: Pending|Verified|Failed|Expired, verifier_ref}`. Rules:
   - one open postcard per charity;
   - claims expire after 21 days;
   - the phone route is refused when the latest 990 is not e-filed or has no phone;
   - the officer route requires the person to appear in the latest TEOS officer list;
   - the claim routes give control only; they never verify a payee (UNB-CHAR-026).
3. **Treat migration from Ren as cheque-first unless verified payee evidence can be imported.** CNV-EXP-002's "enrolled with a supported networked partner" clause gives no relief for Ren-paid charities: Ren for Charities ACH is Ren's own rail paid from the sponsor's accounts, not a third-party network. Proposed `ImportedPayeeEvidence` record: `{sponsor_id, charity_id, bank_token, last4, source: IncumbentExport, incumbent_verified_at, imported_at, status: Imported→Reverifying→Verified|Rejected}`.
   - Before the first electronic payment, run an account-ownership check (CNV-PAY-002).
   - If that check fails, fall back to a positive-pay cheque.
   - Do not stop the payment; the hold falls under CNV-LEG-001 limits.
4. **Make the enrolment loop as strong as Ren's.**
   - A single-use code on every cheque and remittance (UNB-CHAR-014).
   - Donor-initiated enrolment requests with a rate cap.
   - Payment-partner enrolments recognised where they exist (CNV-EXP-002).
5. **Ren's message "pay from your existing accounts, not pooled third-party accounts" [REN-002] cuts against CNV-PAY-001's partner-first Release 1.** Expect sponsors to raise funds-in-transit objections. Answer with CNV-PLT-012 exposure limits and the sponsor-originated ACH fallback.
6. **Match "validated once" lawfully.** Share verification evidence (claim, identity, bank proof, source snapshots) across sponsors through the SharedStoreRegister (CNV-TEN-001, UNB-CHAR-036). Re-run each sponsor's eligibility deterministically, which costs little in compute. This keeps CNV-GRT-003/004 intact and still removes the repeated charity-side friction.

## Conflicts with ratified decisions

- **The CNV-PAY-002 round-2 amendment (c10) sharpens the problem (ADVA-03).** It allows destination evidence only as one of exactly two combinations, each with at least 1 business day of cooling-off. A Ren payee record imported into Unbound therefore cannot carry over as evidence. It must be re-proved under combination (a) or (b), which supports the `ImportedPayeeEvidence` path above.
- **No direct contradiction otherwise.** CNV-EXP-002 depends on an assumption: that enrolments held by incumbents sit with networked partners Unbound can use. For Ren-serviced sponsors, which hold about 28-32% of DAF assets by repo estimate, that assumption is probably false. The owner should decide whether imported incumbent payee data may enter the re-verification path above.
- Ren's "more than 60% of all U.S. DAF assets" [REN-003] conflicts with the repo estimate of 28-32% in `DAF-INDUSTRY-REPORT-2026-11.md`. Keep the repo figure. Log the Ren figure as an unreconciled VENDOR-CLAIM.

## 7. Adversarial review response

| Finding | Response | Change made |
|---|---|---|
| ADVA-09: Ren's lock-in is sponsor-side, across the whole platform, not the payee layer | **Accepted.** The repo attrition census supports it: 1 of 26 national, faith and affinity sponsors left, and community foundations (outside CNV-ECO-004's entry segment) account for 5 of the 6 exits. 02 had scoped itself to the charity network and then ranked moats inside that scope only. Ren publishes no count of claimed profiles or verified payees, so no charity-side network effect is evidenced | Summary re-ranked; two primary rows added in §6; payee layer reclassed as secondary |
| ADVX-10: the binding barrier is distribution and incentives | **Largely accepted.** RCF white-label sponsorship and adviser economics bind firms and advisers, and technology alone cannot displace them. Partly refuted: for sponsors that run their own entity (AEF, MS GIFT, mid-size nationals), the barrier is platform migration cost. The payee layer then adds re-enrolment friction after switching, which the 33-month AEF history import and its cheque-until-reverified handling illustrate | §6 distribution row added |
| ADVA-10: "not proprietary" is labelled VERIFIED-FACT | Accepted | Split: counts are VERIFIED-FACT; the conclusion is INFERENCE, Medium-High |
| ADVA-11: the non-BMF tail suffers time skew | Accepted | Labelled as an upper bound; cause split listed as an open question |
| ADVA-19: self-reported counts are labelled VERIFIED-FACT | Accepted | Ren help centre, AEF and RCF policy statements reclassed to VENDOR-CLAIM (first-party; High that the statement exists) in the text, `data/ren-network-metrics.csv` and `data/sources-REN.csv`. The 990 counts stay VERIFIED-FACT as regulatory filings, noted as self-reported. IRS file counts and direct observations of `app.js` stay VERIFIED-FACT |
| ADVA-03: c10 allows exactly two destination-evidence combinations | Accepted | Added to Conflicts |

**Implication of the revision (RECOMMENDATION).** In CNV-ECO-004's entry segment, beating Ren takes three things in order:
1. a cheaper, lower-risk sponsor migration (Track B);
2. a sponsor-entity or partner answer for adviser-distributed programmes;
3. only then, the charity re-enrolment work in §Implications 2-4.

A better charity network alone would not move sponsors.

## Candidate requirements (proposed)

- Refine **UNB-CHAR-014**: claim routes keyed to IRS records (BMF address postcard, e-filed 990 phone, officer list with IDV, single-use payment code), with expiry and a one-open-attempt rule.
- Refine **UNB-CHAR-032 / CNV-PAY-002**: callback to a known contact plus a cooling-off period on every payee-bank change. Ren documents neither.
- Refine **UNB-CHAR-041**: import incumbent payee and enrolment data as `ImportedPayeeEvidence`, which must be re-verified before the first electronic payment.
- Refine **UNB-CHAR-036/037**: reuse verification evidence across sponsors; never share sponsor eligibility outcomes.
- New: donor-initiated charity enrolment requests, rate-capped and opt-out per charity.
- New: measure and report directory coverage of each sponsor's actual recipient set, split into BMF, Pub 78 and neither.

## Open questions / evidence gaps

1. Counts of claimed profiles, ACH-verified payees and active admins: not publicly documented. These are the numbers that measure the moat.
2. Which programs are among the "25+" RDE ACH programs (only AEF is confirmed), and whether the 150+ programs all share vetting.
3. The current vetting data source for RCF and DFX: Ren's own IRS pipeline or Candid Charity Check. Settle it with test (b) in §2 or with a SOC 2 system description.
4. How long ACH approval and vetting status stay valid, what triggers re-verification, and what control applies to bank changes.
5. Whether Ren can export a sponsor's payee verification state when the sponsor leaves; whether AEF's pre-Ren charity ACH records were carried over.
6. The definition and base date of the 140,000 annual recipients (unchanged since 2023) and of the 93,000 in the Giving Compass scope.
7. The cause split of the non-BMF recipient tail (subordinate, church, revoked after grant, government or foreign, unknown) against a contemporaneous BMF snapshot (ADVA-11).
8. RCF's recipients below $5k and their EINs: the Schedule I detail is an attachment, and recipients below the $5k threshold are not itemised.

Limitations:
- The IRS bulk files were read from a session-shared scratch download. Their IRS Last-Modified headers were checked.
- The help centre was fetched with a 0.5-second delay, slightly below its stated crawl-delay of 1. Only 48 pages were requested.
- No logins were used and no Ren APIs were called.
