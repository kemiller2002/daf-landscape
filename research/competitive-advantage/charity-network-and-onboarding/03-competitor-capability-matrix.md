# 03 - Competitor capability matrix: charity networks and sponsor onboarding

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Machine-readable matrix: `data/competitor-capability-matrix.csv` (109 rows, long format). Sources: `data/sources-CMP.csv` (CMP-001 to CMP-031). Ren appears only as a summary column; 02 (agent REN) holds the full decomposition.

## Summary

- **Directory size does not protect anyone.** Published "universe" counts run from 1M+ (Every.org) to 1.8-1.9M (Candid, Groundswell), 2M+ "validated" (Benevity), 9M+ (Goodstack) and 10M+ (Bonterra Deed) [CMP-009, CMP-022, CMP-001, CMP-008, CMP-018]. All US counts rest on the same IRS BMF/Pub 78 base, which anyone can download (Pub 78 has about 1.44M lines; repo `data/mission-2026-11-14/charity-data-provider-integrations-2026.csv`). INFERENCE, High.
- **What is scarce is verified payee and control-person data**: bank or deposit accounts tied to a verified individual and reused across many payers. Chariot (Control Person KYC and a Chariot Deposit Account at Column N.A.) [CMP-011], PayPal (confirmed charity status, "more than 200,000" in 2022) [CMP-007], Benevity's Causes Portal (document-based claim plus bank details) [CMP-004], Fidelity's Stripe/ACH enrolment [CMP-005] and Ren for Charities (repo) are the real networks. Of these, only Chariot and PayPal Grant Payments are documented as multi-sponsor rails open to new grantmakers. INFERENCE from VERIFIED-FACT and VENDOR-CLAIM, Medium-High.
- **The incumbents' real moat is operational history**: unique recipients actually paid each year. Fidelity paid about 227,000 charities in 2025 and 213,000 unique nonprofits in CY2024, with 67% of grants by EFT [CMP-005; repo `research/mission-2026-11-14/queue-batch36-metrics-rails.md`]. DAFgiving360 paid about 141,000-170,000 a year (VENDOR-CLAIM, Low) [CMP-028]. Vanguard paid 66,785 (CY2025) [CMP-031]. NPT paid more than 41,000 (FY2024 990) and RCF more than 40,000 (CY2024 990) (repo `data/mission-2026-11-14/grant-count-denominators-2026-11-20.csv`). Sponsor web and annual-report counts are first-party self-reports, so they are classed VENDOR-CLAIM. The High confidence applies only to the fact that the sponsor published the figure. Form 990 statements are classed VERIFIED-FACT.
- **Coverage was acquired in four ways**: (1) IRS bulk data plus in-house rules (Daffy, Chariot, DAFtech, Benevity per country); (2) a Candid licence (PayPal Giving Fund certification uses "Candid's database" [CMP-006]; Groundswell; NPT's GuideStar search; RCF's 2023 policy relied on Charity Check); (3) charity self-enrolment funded by payers (Chariot, PayPal, Benevity, Every.org, Fidelity's own forms); (4) acquisitions (Bonterra rolled up CyberGrants, Network for Good and Deed; Charity Navigator bought Causeway; Foundation Source bought Vennfi). VERIFIED-FACT/VENDOR-CLAIM, Medium.
- **Shared vetting reuse already exists.** CAF America validates once and lets "any CAF America donor" grant to the organization for 1-3 years, with the period set by risk [CMP-014]. Chariot verifies a nonprofit once for all its DAF partners while each sponsor keeps approval [CMP-011; repo `research/batch-2b-ren-tifin-chariot-charity-vetting-infrastructure-2026-11-12.md`]. PayPal reuses confirmed-charity status across grantmakers [CMP-006, CMP-007]. VERIFIED-FACT, High. Reuse as such is table stakes. What could differentiate Unbound is reuse governed by evidence and provenance (CNV-GRT-003/004).
- **Sponsor onboarding benchmarks are thin but usable.** NPT says private-label onboarding takes "approximately 14-16 weeks" [CMP-019]. GivingTech says "Up and running in 8 weeks", priced as a licence (tech-only) or a revenue share (full service) [CMP-024]. TIFIN, Ren, Foundation Source and GiftingNetwork publish no timelines. VENDOR-CLAIM, Medium.
- **Agent and MCP access to charity directories is already shipping**: Benevity with Claude (2025-12-02), Candid with Anthropic, Pledge's MCP server and Daffy's MCP [CMP-001, CMP-023; repo]. VERIFIED-FACT/VENDOR-CLAIM, Medium. An "AI-native" charity search is not a differentiator in itself.
- **No competitor publicly documents** reproducible, versioned eligibility decisions with source snapshots, policy-pack versioning or evidence-bounded cross-sponsor hold propagation. This is "not publicly documented", not evidence that these capabilities are absent. HYPOTHESIS that this is where Unbound can differentiate.

## 1. Scope and method

The study covers 21 providers plus a Ren summary row, across nine capability areas. Rows were built from prior repo research first (cited by path) and then checked against fresh public pages on 2026-11-26. Pages blocked or returning 403 (DAFgiving360, BusinessWire, Envestnet, parts of Candid and Every.org) are recorded as search-index evidence at Low confidence. Matrix status values follow the brief. Where a vendor states a feature, the row is `vendor-claim-only` unless technical or policy documentation backs it (`documented`).

## 2. Coverage numbers, normalized by unit

The figures below are different units and must not be compared as if they were one.

| Unit | Provider: figure (as of) | Class / conf. |
|---|---|---|
| Searchable universe | Bonterra Deed 10M+ (live); Goodstack 9M+ (live); Candid 1.8-1.9M profiles; Groundswell "1.8M+ vetted" (Candid-sourced); Every.org 1M+ 501(c)(3)s | VENDOR-CLAIM, Medium |
| Validated/pre-vetted network | Benevity 2M+ "validated" (2025-12) [CMP-001]; Bonterra 190K+ "pre-vetted" [CMP-016, CMP-017]; CAF America: count not published | VENDOR-CLAIM, Medium |
| Payment-enrolled recipients | PayPal 200,000+ "confirmed charities" (2022) [CMP-007]; Chariot: no claimed-account count; DAFpay on "over 60,000", later "100,000+", nonprofit forms [CMP-012, CMP-013]; Vanguard paid >$1bn electronically to >13,000 charities by Nov 2024 (repo) | VENDOR-CLAIM, Low-Medium |
| Recipients actually paid per year | Fidelity ~227,000 (2025, FAQ); DAFgiving360 >170,000 (FY2026, snippet); Blackbaud Giving Fund >123,000 (2024, release); Vanguard 66,785 (CY2025, annual report [CMP-031]) | VENDOR-CLAIM (first-party), High as published; DAFgiving360 Low |
| Recipients per year, Form 990 | NPT >41,000 (FY2024); RCF >40,000 (CY2024); For Good >22,000 (2024) | VERIFIED-FACT (regulatory filing), High |
| Electronic share | Fidelity 67% of grants (2026 report); Chariot 94.57% of payments (vendor); TIFIN 82% of dollars, first 4 months (vendor) | Mixed, see repo `queue-batch36-metrics-rails.md` |

**INFERENCE (Medium).** A new sponsor in the CNV-ECO-004 entry segment (5,000-50,000 funds) will pay perhaps 5,000-40,000 distinct charities a year. That is a scale NPT and Vanguard reach and Fidelity exceeds five-fold. The coverage problem is therefore enrolment of the recipients those sponsors actually pay, not a 1.8M-row directory.

## 3. Capability matrix (condensed)

Codes: D documented, P partially documented, V vendor claim only, N not publicly documented, A documented absent, blank = not researched or not applicable. The full evidence for each cell is in the CSV.

| Provider | Directory | Vetting/reuse | Charity portal | EFT coverage | Payment partner | Intl | Sponsor onboarding | APIs | White label |
|---|---|---|---|---|---|---|---|---|---|
| Ren (summary) | V | P | D (Ren for Charities) | N | D (RDE, own rails) | | D | | D |
| TIFIN Give / GiveClear | N | P | P (via Chariot) | V | D (Chariot) | N | P | V | D |
| GiftingNetwork | N | | | N | | | P | V | D |
| GivingTech DAFtech | V (5 gov registries) | V | | | V | V (America Gives) | V (8 wks) | V | V |
| Fidelity Charitable | D | P | D | D (67%) | D (Stripe+ACH) | P | | | N |
| DAFgiving360 | V | | | N | | | | | N |
| NPT | D | P | | D | D (PayPal; own EFT) | V | V (14-16 wks) | V (SSO) | D |
| Vanguard Charitable | D | D | D (Candid+PayPal) | D | D (PayPal) | P | | | |
| Foundation Source / Charityvest | N | | | | D (Chariot from Aug 2026) | V | D | P (BridgeFT) | D |
| Daffy | P | | | D | D (Chariot) | | | D (API, MCP) | N |
| Chariot | P | D (verify once; no approval) | D | V | D (CDA, Column) | N | | D | |
| Benevity / AOGF | V (2M+) | V (tiered; daily sanctions) | D | V | D (AOGF, UKOGF) | V | | D (MCP) | |
| Bonterra (CyberGrants, NfG, Deed) | V | V | V | | D (For Good) | V | | | |
| PayPal Giving Fund / Grant Payments | D (Candid) | D | D | V | D | | | | |
| Every.org | D | | V | | V | | | A (no disbursement API) | |
| CAF America | N | D (1-3 yr reuse) | | | | D | | | |
| Candid (supplier) | P | D (Charity Check) | P | | | | | D (licensed; AI limits) | |
| Goodstack | V (9M+) | V | | | | | | D | |
| Pledge | V | | | | | | | D (API, MCP) | |
| Groundswell | V (Candid) | | | | P (Chariot) | | | | |
| Overflow | | | | | P (Chariot) | | | | |
| GoFundMe Giving Funds (new, 2025-06-30) | V | | | | | | | | |
| Blackbaud Giving Fund | D (recipients) | | | | | | | | |

## 4. How each provider built coverage, and what it would cost to copy

| Mechanism | Examples | What a copier gets | Defensibility |
|---|---|---|---|
| IRS bulk plus rules | Daffy, Chariot (six sources), Candid Charity Check (polls IRS every 20 minutes; revocations pushed in under 24h [CMP-020]) | Status for about 1.4-1.9M US entities at near-zero data cost | **None** (INFERENCE, High). The work lies in exceptions: churches, group exemptions and non-BMF recipients. Daffy adds houses of worship manually over "a few days to several weeks" (repo CDP-057). |
| Foreign government registries | Benevity ("built directly from local governmental and regulatory bodies" [CMP-003]); DAFtech (US, UK, CA, IL, FR) [CMP-024] | Country-by-country connectors | Moderate. Each registry has its own schema and terms. |
| Licensed aggregator | PayPal Giving Fund (Candid) [CMP-006]; Groundswell; Vanguard and NPT search | Fast start | Low for the licensee: no AI/ML use without consent and deletion on termination (repo `b43n26-03-charity-data-terms-ai.md`). Supports UNB-CHAR-DEC-001. |
| Self-enrolment with KYC and bank verification | Chariot, PayPal, Benevity Causes Portal, Fidelity Stripe/ACH, Ren for Charities, Every.org claim | Verified payee plus a contact who can act for the charity | **High.** It accrues slowly and is mostly bound to the payer or rail. Fidelity's and Ren's enrolments are not portable (INFERENCE). |
| Validation reuse across donors | CAF America (1-3 yr, risk-tiered) [CMP-014]; Chariot; Benevity across about 1,000 corporate clients | Lower cost per grant | Medium. Reuse is a policy choice, not a data asset. |
| Acquisition | Bonterra (CyberGrants, Network for Good, Deed); Foundation Source (Vennfi, Giving Place) | Installed client bases and their charity records | High while clients stay locked in; inherits legacy UX debt (one Software Advice review calls CyberGrants a burden on nonprofits: search-index, Low). |

## 5. Payment networks: who is open to a new sponsor

Repo `research/DAF-INDUSTRY-REPORT-2026-11.md` identifies four camps. Fidelity runs its own Stripe and ACH. PayPal Grant Payments serves NPT and Vanguard. Ren's RDE pays on each sponsor's bank rails. Chariot Disbursements serves TIFIN/GiveClear, Daffy, Founders Pledge, Groundswell, and Charityvest from August 2026. New evidence:

- **Chariot** documents the full recipient loop: a Control Person verifies identity, funds go to a Column N.A. deposit account, and unclaimed charities get mailed checks at no cost to the nonprofit [CMP-011]. Partners named in one undated post: Daffy, DJCF, Endaoment, EarthShare, Neta and Daffeinated [CMP-012]. VERIFIED-FACT/VENDOR-CLAIM. Chariot remains the most open network for a TPSP-style platform under CNV-PAY-001.
- **PayPal Grant Payments**: charities can accept or decline a grant in a dashboard [CMP-007]. Charity status rests on Candid data [CMP-006]. No current enrolled count was found. A sandbox page claiming 175,000 is undated and was not used [CMP-030].
- **Benevity and Bonterra** run closed corporate-giving rails through their own disbursing foundations (AOGF, UKOGF, For Good). They are not DAF-sponsor rails. Benevity charges nonprofits a 2.99% cause support fee (capped at $500); ForGood charges 1.5% on the Every.org route (repo). These fees are a weakness Unbound should not copy.
- **Every.org** documents that it has no disbursement API [CMP-009]. It pays out through Stripe, PayPal Grants and ForGood (search-index) [CMP-010].

## 6. Sponsor onboarding and white label

| Provider | Model | Timeline | Pricing public? |
|---|---|---|---|
| NPT | Sponsor plus private label (GivingPoint, e.g. jpmgiving.org); SLA-based | ~14-16 weeks [CMP-019] | No |
| GivingTech DAFtech | Tech-only licence or full-service revenue share; optional sponsoring charity | 8 weeks, week-by-week plan [CMP-024] | Model only |
| TIFIN Give / GiveClear | Tech plus independent sponsor plus Chariot; SEI, Confluence and AssetMark launches | Not published | No |
| Foundation Source / Charityvest | Tech plus independent sponsor; TIAA (2026-09-28) and OneAscent | Not published | Donor fee schedule only |
| Ren | RCF-sponsored branded programs or back-office for independent sponsors | Not published (see 02) | Program circulars only |
| GiftingNetwork | Multi-sponsor platform; community foundations; advisor (Orion/Envestnet) channel | Not published | No |

INFERENCE (Medium): a 14-16 week benchmark from an incumbent sponsor and an 8-week claim from a small vendor set the competitive bar for configuration and launch. Neither includes migrating an existing sponsor's history. The CNV-EXP-002 full-history migration is a heavier job than either benchmark describes.

## 7. Table stakes, differentiators, and Unbound overlap

**Table stakes** (most comparable providers document them; INFERENCE, High):
- Search over the whole IRS universe, with Pub 78, BMF, revocation and OFAC checks.
- Electronic payment to enrolled charities with a check fallback.
- Grant status visible to donors.
- White-label portals for wealth channels.
- Sponsor-retained grant approval.
- Some cross-payer reuse of charity verification.

**Differentiators** (few providers have them, or they rest on accumulated assets):
- A large base of claimed recipient accounts with verified payees, reusable across sponsors. Today only Chariot and PayPal offer this to third parties.
- Recipient-level operating history at Fidelity scale.
- Handling of non-BMF recipients (churches, foreign organizations through equivalency determination) at speed.
- A published, short implementation timeline.
- Rights to use charity data in AI and agent channels without a licence (IRS-based registries only).
- Zero fees to nonprofits. Benevity and ForGood charge them.

**Proposed Unbound capabilities that already exist among competitors** (so they cannot be sold as novel):

| Unbound requirement | Existing analogue |
|---|---|
| UNB-CHAR-014 charity evidence and dispute portal | Benevity Causes Portal claim with documents; Chariot Control Person claim; Every.org and Candid profiles; Ren for Charities; PayPal dashboard |
| UNB-CHAR-036/037, CNV-GRT-003 cross-sponsor reuse as input | CAF America 1-3 yr risk-tiered reuse; Chariot verified database used by all partners; PayPal confirmed status |
| UNB-CHAR-015 event-driven monitoring | Candid 20-minute IRS polling and revocations in under 24h; Benevity daily sanctions screening |
| UNB-CHAR-003/016 non-BMF and church handling | Chariot church review against the IRS 14-point criteria; Daffy manual houses of worship; Vanguard extra information for religious organizations |
| CNV-EXP-002 reuse of existing rail enrolment | The core design of Chariot and PayPal Grant Payments |
| CNV-PAY-002 bank-change controls | Chariot KYC; Fidelity requires a resubmitted ACH form or Stripe dashboard change |
| UNB-CHAR-DEC-001 first-party registry built from government sources | Benevity and DAFtech (government registries); Goodstack |
| AI/MCP charity search (UNB-CHAR-034 via agents) | Benevity with Claude, Candid with Anthropic, Pledge MCP, Daffy MCP |

**Not publicly documented by any competitor** (candidate differentiators; HYPOTHESIS):
- Replayable eligibility decisions with source snapshots (UNB-CHAR-025, UNB-CHAR-040).
- Versioned, effective-dated policy packs with shadow replay (CNV-GOV-005).
- Propagation of holds only from public facts, with sponsor-private findings never shared (CNV-GRT-004).
- A neutral, rail-agnostic payee-verification record that the sponsor holds and that survives a rail-partner exit (CNV-PLT-012).
- A published onboarding reconciliation report (CNV-EXP-002).

## Adversarial review response

- **ADVA-18 (upheld, fixed).** The Vanguard figure of 66,785 unique charities in CY2025 is now cited to the primary 2025 Annual Report [CMP-031], fetched 2026-11-26. The report also gives 267,838 grants and $3.96B on a calendar-year basis.
- **ADVA-19 (upheld, fixed).** The classification rule is now applied consistently:
  - A sponsor's or vendor's own web page, annual report or press release count of its grantees is VENDOR-CLAIM. That covers Fidelity's 227,000 and its 67% EFT share, Vanguard's counts and Blackbaud's 123,000.
  - Confidence stays High only for the fact that the figure was published.
  - Statements filed in a Form 990 remain VERIFIED-FACT, because they are regulatory filings made under penalty of perjury. They are still unaudited.
  - Process descriptions on a provider's own policy pages (for example "Stripe and ACH", or Candid as the PayPal Giving Fund vetting source) remain VERIFIED-FACT as authoritative statements of the provider's own process.
- **ADVA-15 (agreed).** The following are **parity**, not differentiators:
  - verify once and reuse across payers (Chariot claim across all its Disbursement partners; Ren's "validated once, trusted across the entire platform"; CAF America);
  - paying a charity's own bank with no portal (Fidelity ACH);
  - revocation updates within 24h (Candid);
  - a charity self-service portal;
  - AI/MCP charity search.

  Partner-neutral routing on its own is also parity in effect, because each rail already reaches its own enrolled base. Only these remain candidate differentiators:
  - versioned decisions bound to their provenance;
  - replay;
  - holds propagated only from public facts;
  - sponsor-held payee evidence that is portable across rails.

## Implications for Unbound

1. RECOMMENDATION: Do not compete on directory size. Build the IRS/OFAC base cheaply (UNB-EXT-001/004). Measure coverage as the share of each sponsor's trailing-12-month recipients and grant dollars that are payment-ready, meaning both eligible and holding verified destination evidence.
2. RECOMMENDATION: Integrate Chariot first and PayPal Grant Payments second as networked rails (consistent with CNV-PAY-001). Treat Fidelity, Ren and Benevity enrolments as non-portable.
3. RECOMMENDATION: Make onboarding speed a measured, public commitment. To beat the incumbent benchmark, aim for configuration in under 8 weeks and full migration in under 14-16 weeks. Back the claim with reconciliation evidence, because no competitor publishes any.
4. RECOMMENDATION: Market governance as the differentiator: evidence-bounded reuse, provenance, replay and sponsor-held payee evidence. Do not market the bare features listed in section 7, because competitors already have them.
5. INFERENCE: The CAF America model, which sets the reuse period by risk tier, is a ready precedent for CNV-GRT-003's 180-day default refresh. Unbound could let sponsors shorten the period by risk tier.

**Potential conflict to flag (not resolved here).** Under CNV-PAY-002, destination evidence is required before the first electronic payment. When Unbound pays through Chariot or PayPal, the rail holds the account-ownership verification, not the sponsor. The clause needs to state whether partner-attested verification satisfies "destination evidence" or whether the sponsor must hold its own copy. If the sponsor must hold its own copy, it conflicts with CNV-EXP-002's "without new Unbound enrolment".

## Open questions / evidence gaps

- Current counts of claimed Chariot accounts and PayPal confirmed charities (only figures from 2022 or with no date were found).
- How many charities have enrolled with Ren for Charities (see 02).
- Benevity's and Bonterra's validation methods, refresh cadence and error rates, which are not published.
- Charity directory and vetting sources for TIFIN, GiftingNetwork and Foundation Source.
- Whether NPT's 14-16 weeks includes migration of fund history.
- Implementation timelines for TIFIN, Ren and Foundation Source.
- Concentration: what share of a mid-size sponsor's grant dollars goes to its top 1,000 recipients. This sets how fast an enrolment drive reaches parity. A test against Schedule I data is proposed.
- DAFgiving360 recipient counts were not fetched directly (robots/403).
