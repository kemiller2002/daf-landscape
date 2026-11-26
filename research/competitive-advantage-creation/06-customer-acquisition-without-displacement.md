# 06 - Customer acquisition without displacing incumbents

Status: research (2026-11-26). Track D. Agent CD. Public sources and repository research only; no outreach. Builds on [05](05-untapped-institutional-markets.md), Phase II [16 - Commercial entry strategy](../competitive-displacement/16-commercial-entry-strategy.md), [07 - Institutional switching incentives](../competitive-displacement/07-institutional-switching-incentives.md) and [11 - Institutional distribution](../competitive-displacement/11-institutional-distribution.md). Registers (fragments): [commercial-sequences.csv](data/fragments/CD/commercial-sequences.csv), [claims.csv](data/fragments/CD/claims.csv), [hypotheses.csv](data/fragments/CD/hypotheses.csv), [decisions.csv](data/fragments/CD/decisions.csv), [evidence-gaps.csv](data/fragments/CD/evidence-gaps.csv).

**Constraints carried from the owner's approvals.** No outreach, spend or contracts. Echelon Foundry never becomes a sponsor. Partner-first (DEC-001), licensing-first (DEC-006) and gated capital (DEC-008). Time to first revenue assumes Unbound at state S4 (production-ready, no customers; see report 02) unless stated otherwise. Strategies that touch live DAF records cannot earn revenue before S4.

## Answer in brief

- **Two strategies have a credible path to full-platform adoption.**
  - **(a) Enabling a new DAF programme at a public charity that has none** (S1).
  - **(b) Hosting several such programmes on one existing sponsor that licenses Unbound for them** (S4, the "host-sponsor programme factory", Sequence E).

  Both are narrow in scope but full in function: the customer runs its fund ledger on Unbound from day one. No incumbent is displaced, because the programme did not exist before. The model, which includes the vendor's whole run, gives about **$1.73M base cash ($350k-$6.45M) and 24 months from S4** to the first referenceable invoice. From today's S2 it gives about $2.60M and 33 months ([16](16-capital-efficient-market-entry.md) §2, corrected, model revision 3). Earlier notes quoted revision 2 ($2.02M and $2.94M) and revision 1 ($953k/21 months and $1.75M/30 months). On present assumptions neither strategy pays back for the vendor (sequences E and G, [14](14-commercial-sequencing.md)), so they are adoption and reference routes, not revenue routes (P3-DEC-CE002).
  - **Revision 2 (P3-CHL-REV1016).** This item previously read: "Time to first revenue is about 6-18 months from S4. Incremental cash is in the tens to low hundreds of thousands of dollars, dominated by SOC 2, insurance and the design-partner implementation." The 6-18 months was the sales and implementation time for the programme alone. The cash band left out the vendor's fixed run until first revenue. The model figures above govern.
- **The narrow component offerings are faster and cheaper to first revenue but have no evidenced path to the platform.** These are charity intelligence, reporting data, migration assessment, reconciliation, file ingestion and compliance evidence: about 3-12 months and under about $25-100k. Phase II found they are commodity-priced or free elsewhere and do not pay back (CLM-021, CLM-028, CLM-041). Analogous software markets show narrow tools in this space being **acquired**, not expanding into platforms (CLM-025). The counter-example, land-and-expand at nCino, began with a core workflow platform (P3-CLM-CD017).
- **The slowest routes are the financial-institution ones.** These are banks, credit unions and trust companies, embedded philanthropy in banking apps, and new sponsor creation: 12-36 months, with third-party-risk procurement, SOC 2 Type 2 history and a partner sponsor all required.
- **New decision proposal:** P3-DEC-CD001 (§5).

## 1. Who buys, uses, pays and benefits

S1-S14 are the Track D strategies.

| # | Strategy | Buyer | User | Budget owner | Economic beneficiary |
|---|---|---|---|---|---|
| S1 | New DAF programme at an existing public charity (university, hospital, faith or league foundation) | Foundation CEO or VP advancement | Gift-operations staff; donors | Foundation operations or advancement budget | Institution (assets retained under host-share rules, P3-SRC-CD017); donors |
| S2 | New sponsor creation (bank, fintech or insurer forms an affiliated charity) | Parent firm's wealth or product head | New charity's staff; clients | Parent firm | Parent firm (investment fees, client retention) |
| S3 | Existing sponsor's new channel (e.g. a community foundation opening an advisor or affinity sub-brand) | Sponsor CEO or COO | Sponsor staff; advisors | Sponsor | Sponsor (fee growth) |
| S4 | New white-label programmes hosted by an existing sponsor (programme as configuration) | Host sponsor CEO or COO, with the institution as co-buyer | Host operations; institution's gift office; donors | Host (licence); institution (programme fee) | Host (hosting fees); institution (branded retention) |
| S5 | Specialized DAFs (faith or zakat, scholarship, complex-asset, giving-circle) | Affinity sponsor or host | Programme staff; donors | Sponsor | Sponsor; affinity community |
| S6 | Institutional pilot (Unbound runs a bounded slice, e.g. a new programme or fund class, beside the incumbent) | Sponsor COO or CFO | Ops team | Sponsor innovation or ops budget | Sponsor (option value); Echelon (reference) |
| S7 | Charity intelligence or eligibility evidence | Compliance lead at a sponsor, CSR platform or payment network | Grant reviewers | Compliance budget | Sponsor (lower vetting cost) |
| S8 | Migration assessment | Sponsor COO at a contract-end window | Ops and IT | Ops | Sponsor (negotiating leverage, CHL-096) |
| S9 | Reconciliation | Sponsor CFO or controller | Accounting | Finance | Sponsor; auditor |
| S10 | File ingestion (contribution and custodian files) | Ops head | Ops | Ops | Sponsor |
| S11 | Compliance evidence (audit-ready controls evidence) | CFO; audit committee | Controller; auditors | Finance or audit | Sponsor (audit fee and time) |
| S12 | Reporting (Schedule D and Part IV data, donor statements, board reports) | CFO at a small or tail sponsor | Finance | Finance | Sponsor (filing quality, P3-SRC-CD018 §5) |
| S13 | Advisor integrations | Wealth platform, RIA or custodian partnerships team | Advisors | Platform | Platform; advisors |
| S14 | Embedded philanthropy (giving or DAF inside a banking, credit-union or benefits app) | Digital-banking or benefits product head | Members or employees | FI digital budget; employer benefits budget | FI or employer (engagement); sponsor |

## 2. Market conditions

| # | Existing alternatives | Purchasing trigger | Procurement complexity (1-5) | Regulatory exposure | Likely competitive response |
|---|---|---|---|---|---|
| S1 | Refer donors to national DAFs (free to the institution); host on a community foundation or national sponsor (Columbus Foundation; formerly BNY CGF); Foundant, DAFtech (8-week launch), Givinga ($12.5k base, CLM-038), NPT private label (14-16 weeks) | Campaign launch; complex-gift opportunity; host exit (BNY CGF voted to end its programme, Dec 2024, per repository records; the status of its hosted programmes is unverified, P3-GAP-CD005); new planned-giving leadership (unmeasured) | 3 (security review, board) | High for the sponsor (4966/4967, pending regulations); Unbound is a vendor | NPT, RCF and DAFtech price-match turnkey launches; community foundations offer hosting |
| S2 | Partner-sponsor private label (RCF, NPT, Charityvest, Endaoment) at near-zero fixed cost to the firm | Desire to own the sponsor and its economics; captive-sponsor strategy | 4-5 (formation, board, TPRM) | Highest: new charity, 1023 determination, state registration, 4966 | Partner sponsors undercut formation economics (§3 of [05](05-untapped-institutional-markets.md): break-even $7-20M) |
| S3 | The sponsor's incumbent adds the channel (Ren claims 150+ partners, CLM-036) | Growth target; advisor demand | 3 | Medium (advisor rule pending, P3-SRC-CD014) | Incumbent configures the channel within its contract |
| S4 | The host's existing system (Foundant 45% of community foundations); referral to national sponsors | Host wants a programme-hosting line; institution wants a brand without a sponsor apparatus | 3 (host) + 2-3 (each institution) | Sponsor-level; per-programme segregation (V-9) | Foundant or NPT add hosted-programme features; national sponsors expand private label |
| S5 | NCF, Signatry, Thrivent, AMCF already serve affinities (affinity G03-G09) | Mission-aligned product gap (zakat timing, church-loan funds) | 2-3 | Medium; religious-purpose grant rules | Affinity sponsors add features on Ren or Give Interactive |
| S6 | Do nothing; incumbent roadmap | Board pressure on cost or ops; incident | 3 | Low-medium | Incumbent retention discount (CHL-098) |
| S7 | Candid Charity Check from $2,750; free IRS data; Treasury Do Not Pay (CLM-041) | Audit finding; vetting backlog | 2 | Low (data licensing, DEC-004) | Commodity price pressure |
| S8 | Receiving vendor scopes the migration free; consultants (CHL-068) | Contract-end window | 2 | Low | Free assessments; incumbent renewal discounts |
| S9 | Spreadsheets; fund-accounting modules; BlackLine-type tools (generic) | Audit finding; close delays | 3 | Low-medium (SOC 1 reliance) | Incumbent module bundling |
| S10 | Incumbent import tools; manual entry | Volume growth; error incidents | 3 | Low | Bundling |
| S11 | Auditor PBC lists; GRC tools | Audit fee increase | 3 | Low | Bundling |
| S12 | Accountant prepares 990; Foundant or other reporting | Filing errors (228 tail sponsors carry imputed values; 59 blank Schedule D Part I, P3-SRC-CD018) | 1-2 | Low | Little (low value) |
| S13 | DAFgiving360, Fidelity, Altruist-Endaoment, TIFIN, Foundation Source, GiftingNetwork (CLM-039) | Platform roadmap | 4 | Medium | Slots already held; free custodian DAFs |
| S14 | Spiral giving widgets on Alkami; Daffy for Work; Givinga; Morgan Stanley at Work; Benevity (P3-SRC-CD010) | Engagement or benefits refresh | 4-5 (TPRM; enterprise) | Medium-high (sponsor needed; GLBA; employment) | Crowded; marketplaces add incumbents |

## 3. Delivery economics

TTFR is the time to first revenue, in months from S4. Cash bands for incremental cash before first revenue, excluding Unbound completion: **A** under $25k; **B** $25-100k; **C** $100-300k; **D** over $300k. Bands are INFERENCE from Phase II segment cycles (SEG register), vendor launch claims (CLM-038; NPT 14-16 weeks) and the assurance expectations in CLM-040. Exact capital belongs to Track A/B (reports 02-03).

| # | TTFR (months) | Required integration | Required investment (cash band; drivers) | Expansion potential | Path to full platform? |
|---|---|---|---|---|---|
| S1 | 6-18 (sales 3-9 + implementation 2-4) | Custodian or investment feed (the endowment pool's custodian); payment rails; gift-system export | B-C: SOC 2 Type 1 to 2; cyber and E&O insurance; design-partner implementation; counsel review of programme documents | Medium: peer institutions; federations (university systems) | **Yes, by construction.** The programme runs on Unbound's ledger |
| S2 | 12-30 (IRS determination time UNKNOWN, P3-GAP-CD008) | As S1, plus parent CRM and SSO | C-D: plus the parent's TPRM | Low-medium | Yes, but rare and uneconomic below about $7-20M |
| S3 | 9-24 | Advisor desktops, custodians | C | Medium | Only if the channel runs on a separate ledger; otherwise it is the incumbent's |
| S4 | 9-24 for the first host; 1-4 per additional programme | As S1 at host level; programme configuration only thereafter | B-C (first host); A per additional programme if templated (P3-ASM-CD007) | High in count (about 600-800 qualified institutions, [05](05-untapped-institutional-markets.md) §4); **demand unobserved**: existing institutional sponsors average ~24 accounts and the segment's share is falling (P3-CLM-CD004). Revision 2 (P3-CHL-REV1011): previously "**High in count**" without the demand qualifier | **Yes.** The host's hosted book runs on Unbound. The host's main book may follow later (unproven, P3-HYP-CD002) |
| S5 | 9-24 (as an S1 or S4 variant) | Affinity-specific rules (e.g. zakat classification) | B | Medium within federated faith structures | Yes, if delivered as a programme |
| S6 | 6-18; pilots are often unpaid (revenue may lag) | Parallel run with the incumbent; data feeds | B-C | Medium | Plausible but unproven. Running a second ledger beside the incumbent adds cost to the sponsor |
| S7 | 3-9 (possible at S2/S3; public data only) | Grant-review workflow API | A | Low (CLM-041) | **No evidence.** Commodity; component only (Phase II 16 §5) |
| S8 | 3-9 if priced; Phase II says unpriceable (CHL-068) | Read-only exports | A | Low | Only as pre-sales for S1/S4 or migration (CLM-021) |
| S9 | 6-15 | Bank, custodian and ledger feeds | B (SOC 2 expected) | Medium | Weak to moderate. Sits next to the ledger, not on it |
| S10 | 6-15 | Inbound file formats | B | Medium | Weak to moderate |
| S11 | 6-15 | Control evidence from the sponsor's systems | B | Low (budget unclear, Phase II 16 §5) | Weak |
| S12 | 3-9 | Ledger exports | A | Low (tail fee pool about $49-74M a year for the whole tail, P3-SRC-CD018) | Weak; possibly a door-opener to S1/S4 at tail sponsors |
| S13 | 12-24 | Custodian and platform APIs | C | Low (slots held) | No (Phase II 16 §5) |
| S14 | 12-30 | Digital-banking marketplaces (Alkami, Q2, Jack Henry); HRIS | C-D | High in count, low in value | Unproven; needs a sponsor partner |

## 4. Does a narrow offering lead to full platform adoption? (evidence, not assumption)

| Evidence | Market | What it shows | Direction |
|---|---|---|---|
| nCino FY2026: ACV $602.4M, ACV net retention 112%. Top-40 and top-50 US banks added mortgage, consumer lending and spreading to existing commercial-lending deployments (P3-SRC-CD011) | Bank lending software | Land-and-expand works **after landing with a core workflow platform** used by the same buyer | Positive, but the "narrow" land was a workflow system of record, not a data or tooling add-on |
| Foundant: first online grant application 2007 (Grant Lifecycle Manager); CommunitySuite later reached 500 and then "700+" community foundations (P3-SRC-CD012) | Community-foundation software (same buyers as DAFs) | A grants product preceded a full community-foundation suite at the same vendor | Positive but weak. Whether CommunitySuite was built or acquired, and whether GLM customers converted, is unverified (P3-GAP-CD009) |
| Pinkaloo (Ren, 2021), Amicus (TIFIN), Vennfi (Foundation Source) were acquired (CLM-025; SRC-053, SRC-054) | DAF technology | Narrow DAF-tech firms were absorbed by platform owners rather than expanding into platforms | **Negative** for independent narrow-to-platform |
| Candid Charity Check from $2,750; free IRS files (CLM-001, CLM-041) | Charity data | Charity data remains a commodity data product | Negative for S7 as a wedge |
| Free migration in nonprofit CRM; vendors scope migrations free (CLM-021, CHL-068) | Migration services | Assessments are a cost of sale | Negative for S8 as revenue |
| Spiral giving widgets inside Alkami; no DAF vendor in Jack Henry, Q2 or Fiserv marketplaces (SRC-055, CLM-023) | Digital banking | Point features in marketplaces stay features | Neutral to negative for S14 |
| Phase II model: non-custodial services never pay back within 120 months at base (CLM-028) | This package | Narrow services do not finance a platform | Negative |

**Conclusion (P3-CLM-CD018, inferred, Medium).** A narrow offering credibly leads to platform adoption only when three conditions hold:
1. it is bought by the **same budget owner** who would buy the platform;
2. it sits on the **system-of-record data path** (fund ledger, contributions, grants), not beside it;
3. the vendor **survives long enough** to expand.

Only S1, S4 and S5 meet the first two by construction, because a new programme's ledger is the platform. S9 and S10 partly meet them. S7, S8, S11-S14 do not, on present evidence. "Narrow" should therefore mean **narrow in who it serves (one new programme), not in what it does**.

## 5. Ranking by time to first revenue and cash need

| Rank | Strategy | TTFR | Cash band | Platform path | Comment |
|---|---|---|---|---|---|
| 1 (fastest, weakest) | S12 reporting / S7 charity intelligence | 3-9 | A | No evidence | Revenue small and commodity; use only as a door-opener or credibility asset |
| 2 | S8 migration assessment | 3-9 | A | Pre-sales only | Treat as CAC (Phase II DEC-001 context) |
| 3 (**recommended core**) | **S1 new programme at an existing public charity** | 6-18 | B-C | Yes | Greenfield, no displacement, procurement 3; demand unproven |
| 4 (**adoption and reference route**; Revision 2: previously "recommended scale route") | **S4 host-sponsor programme factory** (Sequence E) | 9-24 first host; 1-4 per added programme | B-C, then A per programme | Yes | Only route where small programmes are viable for the *programme* (§3.3 of [05](05-untapped-institutional-markets.md)). It does not carry the vendor: E never pays back in the model ([14](14-commercial-sequencing.md)) |
| 5 | S6 institutional pilot | 6-18 (revenue may lag) | B-C | Plausible | Doubles the sponsor's systems; design-partner economics |
| 6 | S9 reconciliation / S10 file ingestion | 6-15 | B | Weak-moderate | Needs SOC 2 and feeds; better delivered inside S1/S4 |
| 7 | S5 specialized DAFs | 9-24 | B | Yes (as programme) | Variant of S1/S4 for affinity foundations |
| 8 | S3 existing sponsor's new channel | 9-24 | C | Only if separate ledger | Incumbent can configure it |
| 9 | S13 advisor integrations / S14 embedded philanthropy | 12-30 | C-D | No / unproven | Crowded; TPRM |
| 10 (slowest, costliest) | S2 new sponsor creation | 12-30 | C-D | Yes but rare | Uneconomic below about $7-20M of DAF assets |

## 5a. New decision proposal

**P3-DEC-CD001 (proposed - owner decision required; Revision 2, 2026-11-26).** Treat **new-programme enablement through a host sponsor** (S1 and S4, Sequence E variant P3-SEQ-CD001) as an **adoption and reference route**, not the primary revenue route, consistent with P3-DEC-CE002. The primary revenue customer is decided by the revenue-per-customer gate in P3-DEC-CE002. Run the route only within an explicit loss budget set by the owner under DEC-008. Treat narrow component offerings (S7, S8, S11, S12) as acquisition cost or credibility assets, not revenue lines. Exclude new sponsor formation and direct bank, credit-union and trust-company sales from initial go-to-market.

This refines DEC-001; it does not replace it. It is reversible, since no build commitment beyond configuration templates is involved. Conditions and evidence needed:
- at least one host sponsor willing to license for hosted programmes (V-6), and willing to run a second system beside its main book (P3-HYP-CD002);
- programme-level willingness to pay among education and health foundations (V-2);
- counsel confirmation of hosted-programme role allocation, including who carries 4966 responsibility for the host's donors and any charitable-solicitation registration (P3-GAP-CD013);
- the minimum fee per programme, or number of programmes per host, at which the route would carry the licensor. On present model inputs no such point has been shown within 120 months;
- customer continuity before any pilot: escrow, a tested full-history export and a funded wind-down period (P3-CHL-REV1015). The model now carries a wind-down cost of $25k-100k when the kill rule pauses a stream with a signed customer (P3-ASM-MOD038). Escrow and a tested export remain unpriced.

**Revision 2 history.** The original proposal (2026-11-26) read: "Adopt new-programme enablement through a host sponsor (S1 and S4, Sequence E variant P3-SEQ-CD001) as the evidence-preferred non-displacing acquisition route under DEC-001." It conflicted with the model, where E and G never pay back ([14](14-commercial-sequencing.md); [16](16-capital-efficient-market-entry.md) §6 step 5), and with agent CE's finding (P3-CLM-CE003). It was revised after round-1 review: P3-CHL-REV1008, REV1012, REV1033 and REV2039.

**Positioning note (P3-CHL-REV1041, P3-CHL-REV2039).** On model revision 3 the break-even single sponsor depends on who performs the deep review (P3-DEC-MOD005; `gate-break-even.md`):
- Echelon performing M1: not reached;
- M1 risk-tiered (subject to counsel and V-9): 5,202 accounts;
- the sponsor performing it: 3,079 accounts ($175k net);
- M5, conditional on OD-CDD-02: 3,169 accounts.

Plausible sponsors (non-captive, not donation processors) are few: 17 at 2,646 accounts or more, and 10 at 5,291 or more (`platform-classes.md`). **Partner-book result:** the one route that pays back is a partner licensing Unbound for its whole book of small sponsors (SEQ-PB, P3-SEQ-MOD012). With the sponsor performing the deep review it reaches +$4.18M at month 120, pays back at month 76 and peaks at $2.43M; under M5 it pays back at month 80 (`bases.md`). Under the kill rule with the cost center opened at month 0, it still pauses at month 24, like every configuration. Revision 3 note: revision 2 gave 10,963 accounts ($622k) under M1 and 3,949 ($224k) under M5. Nearly all of them already run a contracted platform (P3-CLM-CE001). An earlier Revision 2 note said "roughly 2,000 accounts". Selling to them is displacement, not a non-displacing route. Do not describe sponsor routes above about 2,500 accounts as non-displacing. The owner's positioning choice is: niche licensing to mid and large sponsors through a partner that already serves them; or greenfield enablement priced to carry a licensor. That choice is the P3-DEC-CE002 gate.

**Sponsor-facing value (P3-CHL-REV1032).** Under licensing (DEC-006) the sponsor keeps the residual staffed work, about 53 minutes per account-year at ×1.4 sponsor efficiency (~74 minutes). It also bears its own conversion labour. Every sponsor-facing value statement should quote both ([10](10-structural-cost-elimination.md) §3).

## 6. Commercial sequences supported by this evidence

See [commercial-sequences.csv](data/fragments/CD/commercial-sequences.csv).

- **P3-SEQ-CD001 (Sequence E, host-sponsor programme factory):**
  1. A design-partner sponsor (community foundation, faith foundation or league foundation) licenses Unbound for its *hosted* programmes.
  2. Templated programme configuration is offered to institutions in its network.
  3. A second host is added.
  4. The host's main book follows (optional, unproven).

  First revenue in 9-24 months from S4. Failure band: high (very high as a revenue route: E does not pay back in the model). Main dependencies are host willingness (P3-HYP-CD002) and institution demand (P3-HYP-CD001).
- **P3-SEQ-CD002 (direct new programme at an education or health foundation):** one foundation programme, then peer institutions. First revenue in 6-18 months. Failure band: high. Each sale is individual; vendor economics need a programme minimum fee and a lower vendor fixed cost.
- **Not registered (insufficient evidence):**
  - league-foundation channel (P3-HYP-CD003; untested back-office need);
  - Sequence B (charity intelligence as a wedge), which the analogues contradict (§4).

## 7. What would change these conclusions

- **Institutional demand appears:** structured review or V-1 interviews show education and health foundations launching DAF programmes at a rate of several per year, or naming the lack of a sponsor apparatus as the barrier. That would strengthen S1. The opposite finding would remove S1 and most of S4.
- **A host sponsor refuses a second system:** hosts insist on one system for all funds, which would make S4 a displacement sale after all (P3-HYP-CD002 falsified).
- **Final 4966 regulations** treat institution-managed investment as donor-advisor activity, raising compliance cost for hosted programmes (P3-SRC-CD014).
- **Present state, not a future condition (Revision 2, P3-CHL-REV1008).** Turnkey and private-label programme products already exist: NPT private label in 14-16 weeks, DAFtech in 8 weeks, Givinga at a $12.5k base fee, and community foundations offering hosting (§2, CLM-038). S1 and S4 therefore compete with these offers today, and their pricing is already compressed. This bullet previously read: "Incumbents publish turnkey hosted-programme products at near-zero minimums (NPT, DAFtech, Charityvest already partly do), compressing S1 and S4 pricing." It is kept here as a condition only in its stronger form: such products reaching near-zero minimums with SOC 2 Type II and references would remove the remaining price room.
