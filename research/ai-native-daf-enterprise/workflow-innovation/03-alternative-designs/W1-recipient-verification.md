# W1: Recipient verification and eligibility

**Outcomes:**
- BO-21: the intended recipient is identified as a legal entity.
- BO-22: its eligibility class is known at grant time.
- BO-23: sanctions exposure is cleared.
- BO-28: routine grants are approved quickly.

**Evidence of inefficiency** ([top-workflows](../01-existing-outcomes/top-workflows.csv)):
- Opex per grant spans $61–$2,487 (EV-136).
- Fidelity makes about 12.5 grants per recipient per year (FINAL-STATUS PR #73).
- The top 1,000 recipients receive about 49–54% of top-50 dollars (recipient-concentration data).
- Revoked-EIN grants are 0.082% of top-50 dollars (strategic synthesis §0).
- Cross-sponsor repetition is under measurement in E7.

## 1. First principles: what is strictly necessary

| Element | Necessary content |
|---|---|
| **Information** | The legal entity meant by the donor (EIN or foreign identifier); its IRS status class at grant time (Pub 78 / EO BMF foundation code, revocation); OFAC status against current lists; a verified payment endpoint (needed later for W3, not for eligibility) |
| **Authority** | The sponsor decides. For listed §170(b)(1)(A) organizations the sponsor may rely on IRS data (Rev. Proc. 2018-32). A potential sanctions true match needs a named person (regulatory map §12) |
| **Resources** | IRS bulk files (free); OFAC lists (free); an entity-resolution capability for name-only input |
| **Actions** | Resolve the entity; read status as of the grant date; screen; record the evidence with source versions |

**What is not necessary:** a person looking up each grant, a fresh lookup per grant when nothing changed, or waiting for the recommendation before verifying.

## 2. Inversion findings

| Prompt | Finding |
|---|---|
| Eliminate? | Per-grant verification *can* be eliminated. Its function, eligibility evidence at grant time, is replaced by a continuously refreshed recipient record plus a pinned snapshot reference on each grant |
| Begin before the request? | Yes: the universe of likely recipients (Pub 78 plus past payees) can be pre-verified |
| No employee touch? | Yes for listed public charities with fresh data and no flags; no for potential sanctions matches |
| External partner? | Verification evidence could be supplied by a shared network; the sponsor still decides |

## 3. Designs

| # | Design | Mechanism | Who decides | When work happens | Authoritative data | Human roles | Controls | Cost drivers | Donor / advisor / nonprofit experience | Maturity | INN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | **Conventional baseline** | Staff look up each recommendation in IRS tools and screen OFAC; queue; batch approval | Staff reviewer per grant | At request, in a queue | IRS website at lookup time; usually no stored snapshot | Reviewer per grant | Two-person review at some sponsors (inferred) | Reviewer minutes × grants | Days of wait; no status visibility; nonprofit sees nothing until paid | Observed industry practice (approval latency unpublished, EV-076) | — |
| D2 | **Automation-first** | Same sequence; API lookups and screening per grant; reviewer confirms the result | Reviewer clicks approve | At request | API response at lookup time | Reviewer confirms each grant | Same as D1 plus logs | Reviewer minutes reduced, still per grant | Faster, still queued | L1 | — |
| D3 | **AI-native (parent design)** | Policy-as-code decides routine grants; AI flags only; exceptions to a single queue | Rule (routine); person (exceptions) | At request, in seconds for routine | Pinned eligibility snapshot (bitemporal) | Specialists for exceptions only | Freshness SLO; block-never-release; flag-only AI | Exception volume × minutes | Routine grants approved in minutes; status shared | L3 (parent PoC, 59 tests) | INN-05 |
| D4 | **Radical: verification passport, before the request** | Verification moves from the *transaction* to the *recipient*, and from *request time* to *source-change time*. Every Pub 78 entity and every past payee carries a continuously refreshed evidence record. A grant only *references* the record version valid at the grant date. Sanctions screening runs on the universe whenever a list changes | Rule, on refresh; the grant decision is a lookup; person for true matches | Continuously, independent of requests | Recipient evidence record (versioned) | Specialists handle ambiguous resolution and status changes | Refresh-diff limits (CTL-050); list pinning; change → hold in-flight grants | Refresh compute (small); resolution of long-tail names | Instant routine decision; donor sees "verified" at search time | L2 (premises supported: recurrence and bulk data) | INN-01, INN-03, INN-34 |
| D5 | **Externalized / ecosystem: cross-sponsor verification network** | A neutral network holds recipient evidence records contributed and consumed by many sponsors, with provenance. Each sponsor applies its own policy and decides | Each sponsor (rule or person) | Continuously; one refresh serves all members | Network record plus each sponsor's own decision record | Network operator's data team; each sponsor's compliance officer | Provenance; member dispute and correction process (bureau model); poisoning defenses | Operator fixed cost shared; member marginal cost low | Same as D4; recipients correct their own record once | L1 (L2 if E7 shows overlap) | INN-02 |
| D6 | **Recipient-attested identity (extra)** | Recipients claim and maintain their own record (authorized officer verification, bank account, contacts); the sponsor verifies the officer once, and IRS and OFAC data are still read from source | Sponsor rule on IRS/OFAC; recipient owns profile facts | At recipient enrollment | IRS/OFAC for status; recipient for profile | Payments ops for disputes | Officer verification; cooling-off on changes | Enrollment support | Nonprofit controls its own data; one profile for all sponsors if shared | L1 | INN-07, INN-38 |

**Why D4 differs from D3 in mechanism, not degree:**
- In D3 work happens *per request*; in D4 it happens *per source change*.
- The authoritative datum moves from a per-grant lookup to a per-recipient versioned record.

## 4. Constraint removal and reintroduction ledger

All designs were generated with constraints removed (for example "approve every grant instantly, verify never"), then constraints were reintroduced one at a time.

| Constraint reintroduced | Ideas that die | Ideas modified | Survivors |
|---|---|---|---|
| **Legal** (§4966; OFAC strict liability; Rev. Proc. 2018-32 reliance as of grant date) | "Verify never"; "pay first, verify later" (INN-35) | D4 must pin the snapshot *as of the grant date* (bitemporal); OFAC requires current lists, so universe rescreen on every list change | D2–D6 |
| **Fiduciary** | — | D5: the sponsor cannot outsource its *decision*, only evidence | D2–D6 |
| **Accounting** | — | Evidence references must be stored with the decision record | All |
| **Privacy / security** | D5 cannot share donor identities or grant amounts | D5 shares recipient evidence only; donor data excluded | D5 modified |
| **Economic** | D1 at scale (cost linear in grants) | D5 needs enough members to fund the operator | D3, D4, D5 |
| **Operational** | — | D4: name-only requests still need resolution at request time; churches without 990 data (8.3% of top-50 dollars to church-status recipients, strategic synthesis §0 G4) need a manual path | D3, D4 (+ long-tail path) |
| **Human acceptance** | — | D5: competitors must trust a shared record, an unproven premise | D4 strong; D5 uncertain |

## 5. Cross-industry analogies

- T1: payee directories.
- T15: marketplace verification.
- T16: credit-bureau shared files.
- T13: versioned data with pinned reads.

([cross-industry transfers](../02-creative-hypotheses/cross-industry-transfers.md))

## 6. Creative competition (seven perspectives)

| Perspective | Position |
|---|---|
| **Inventor** | Go further than D4: publish the verified record to donors at *search* time, so ineligible recipients are never recommended. Validation then happens before the request exists |
| **Enterprise architect** | D4 fits the event model: `CharityEligibilityChanged` already exists. The record must be bitemporal or audits fail. D5 adds a multi-party trust boundary that the parent architecture does not have |
| **Economist** | D4's cost is almost fixed; D3's scales with exceptions. D5 has utility economics: value grows with overlap, but only if members join. Without E7 data, D5's value is unknown |
| **Regulatory specialist** | Reliance on IRS lists is explicitly permitted; reliance on *another sponsor's* diligence is not addressed by any guidance found (API-12 issue). OFAC: a stale universe screen is a violation risk, so the list-change trigger is mandatory |
| **Adversarial reviewer** | D4 moves work to the long tail (name-only, churches, new organizations), so the exception queue may grow, not shrink. A poisoned refresh propagates to every grant at once. D5 creates a high-value attack target and a concentration point |
| **Customer advocate** | Donors gain "verified" badges and instant routine grants. Nonprofits benefit most from D6 (one profile). Congregations risk being treated as second-class because their data is thin |
| **Commercial strategist** | D4 is table stakes, easily copied. D5 is the only design with a possible moat (network), but it competes with Candid and Chariot and needs neutral governance |

**Recorded disagreements:**
1. *Economist vs Inventor:* does search-time verification change donor behavior or just add UI? Unresolved; no data.
2. *Adversarial vs Architect:* whether D4 really reduces human work or shifts it to the long tail. The Architect expects a net reduction because the long tail is a small share of dollars; the Adversarial reviewer notes that grant *count*, not dollars, drives work. Unresolved until E1 and E7.
3. *Regulatory vs Commercial:* whether D5 is legally usable at all. Unresolved; counsel needed.

**Unresolved questions:**
- the cross-sponsor overlap (E7);
- the long-tail share of grant *lines* (not dollars);
- the legal status of reliance on shared diligence;
- the governance model for a neutral network.

## 7. Forwarded to experiments

| Candidate | Experiment | Metric |
|---|---|---|
| D3 vs D4 vs D2 | **E1** verification architectures on a synthetic grant stream calibrated to recipient concentration | Verification events per grant; recommendation-time latency; stale-status escapes when statuses change; human resolutions |
| D5 | **E7** cross-sponsor recipient overlap from Schedule I | Share of each sponsor's recipient lines and dollars already verified by other members; reuse curve by join order |
| D4 under adversarial loads | **E1** adversarial cases: poisoned refresh, status change between refresh and grant, name collisions | Escapes; blast radius |
| Cost | **E11** | Cost per grant across D1–D5 |
