# 10: Executive findings: DAF servicing economics at 20 bps

**Date:** 2026-11-25.

**Status:** theoretical research.
- No time study, buyer conversation, signed contract or operating data exists.
- Every figure comes from labelled assumptions and public filings: average-asset proxies, list prices and 990 contractor lines.
- **This is not evidence of commercial profitability, and it does not authorize launch.**
- All passes, the adversarial review and the integrator are the same model family, so this is not independent validation.

**Model:** [`model/out/results.md`](model/out/results.md). Supporting reports are 00-09.

## The answer in one paragraph

DAF administration is an established business, and 20 bps sits inside its observed price band (about 15-40 bps, or $390-815 per account-year, for full-service administration). But a servicer's cost is driven by accounts and activity, not assets. That makes a flat 20 bps:
- a **market price only around $250-400k average balances**;
- **too high per account** for the high-balance community-foundation and national books that look most profitable;
- **below cost** for books averaging under about $150k.

A lean, AI-native servicer at 20 bps breaks even at about **$1.1-1.5B of average billable assets**. That rises to **$1.8-2.3B** once platform build and sales are carried, and the organization must be about **five to six people once live**, not five at all scales.

The business that works best has these features:
- **administration first**, with **two or three large sponsors** ($0.5-1.5B, $150-700k average balances) on design-partner terms;
- a **cost-reflective tariff**: a per-account fee plus a low asset fee and activity fees, set to equal about 15-25 bps on the target book and payout-neutral;
- **board delegation and continuous charity monitoring** in place from go-live;
- software licensing added later.

It needs **about $3-4.5M** of capital if the build stays small and a design partner signs within a year, and **$5-8M** realistically. It fails if buyers will not pay that tariff, if the redesigned handling minutes are not achieved, or if the platform build approaches Unbound's own $5M estimate without a funded partner.

## Answers to the fifteen questions

### 1. Is 20 bps a credible competitive servicing price?

**Conditionally yes.**
- **Market evidence.** Ren earns 18.5 bps ($737 per account-year) at Morgan Stanley GIFT, and 38-40 bps at USCGT and RCF. TIFIN Give lists 30 bps up to $1M and 10-20 bps above. On assets alone, 20 bps is parity-to-discount (report 01).
- **But buyers compare per account.** At the target sponsors' $0.6-2.5M average balances, 20 bps is $1,200-5,000 per account: 2-7x Ren's realised rate, and a median 11% of a top-25 target's entire non-investment operating cost (ADV-001, 026).
- **And below about $150k it is under cost** (report 05).
- **So:** 20 bps is credible as a headline for books averaging about $250-400k. Elsewhere it should be offered as a per-account-plus-bps tariff that equals about 15-25 bps on the book.

### 2. What is the lowest sustainable servicing price?

**It depends on scale; there is no single floor.** Model B, AI-native, five sponsors, $100-250k balances:

| Average assets | Break-even | 20% margin |
|---|---|---|
| $1B | 24-29 bps | 30-36 bps |
| $2B | 15-17 bps | 18-22 bps |
| $5B | 8-11 bps | 10-14 bps |

- **10 bps** needs $3-5B. **5 bps** is a software-only price for staffed administration at any addressable scale.
- **Carrying build amortisation and sales** adds about 50-60% to the assets needed at 15-25 bps.
- **In per-account terms**, the variable cost of a redesigned operation is about $9-790 per account-year by archetype, or about $55-75 for the market mix including labour (report 04).

### 3. What assets are required to break even?

At 20 bps, average billable assets, AI-native, five sponsors, $150-500k balances:

| Organization | Break-even assets |
|---|---|
| Model B lean (5 core + 1 ops) | $1.14-1.46B |
| Model A founder-led (economic cost) | $1.01-1.28B |
| Model C established | $1.47-1.67B |
| Model B fully loaded (build $1.0M/yr + sales $0.25M/yr) | $1.83-2.29B |
| Model B, AI-enhanced only (redesign not achieved), one sponsor | $1.02-1.95B |

**The prior memo's $725M is superseded.** It used $1.18M fixed cost, $50/h labour, unlimited capacity and no build or sales costs.

### 4. What assets are required for sustainable profitability?

At 20 bps, five sponsors:

| Margin | Operating basis | Fully loaded |
|---|---|---|
| 20% | $1.5-2.1B | $2.4-3.2B |
| 25% | $1.6-2.2B | $2.6-3.6B |
| 30% | $1.7-2.5B | $3.0-3.9B |

**Margins of 40-60% appear only at $5-10B.** No addressable book of that size exists outside captives and competitors.

### 5. What assets are required to survive adverse market conditions?

Starting assets needed to stay at break-even after the stress (in brackets: to keep a 10% margin). Model B, five sponsors, $150k balance:

| Stress | Model B | Model A |
|---|---|---|
| Market -30% | $2.45B ($2.83B) | $2.19B |
| Market -50% | $4.48B | |
| Combined: -30%, minutes x1.5, wages +10%, vendors +25% | $4.27B | |
| Severe | $6.65B | |
| Market -30%, fully loaded | About $3.3-3.8B [D, approximate] | |

**Per-account pricing halves the damage of a 30% fall** (report 05 §4). **Contractual minimums protect only small sponsors.** Asset-linked minimums do not fix the core exposure, and floors above about 1% of balance harm small funds.

### 6. What is the smallest credible organization?

**Before launch: about three people.** Founder, CTO and engineer or controller, plus contracted assurance, legal, vCISO and engineering.

**Once live: about five to six people.** Dual control and absence cover need two operations staff and a controller. The prior budget's single operations person cannot sustain separation of duties (report 03).

| Model | Fixed cost |
|---|---|
| Model A (cash) | $1.12M + about $0.2M for two operations staff |
| Model B (economic) | $1.74M including the second operations person |

**Step hires:**
- an operations manager after 4 added operations staff;
- an integration engineer and an implementation analyst per 8 live sponsors;
- a fund accountant per 15,000 accounts;
- a compliance officer above 10,000 accounts.

**December needs about 3x average daily capacity.**

### 7. How much startup capital is required?

| Case | Trough | With 25% buffer | Conditions |
|---|---|---|---|
| Minimum credible | $2.7-3.6M | $3.3-4.5M | Founder-led to Model B; a $1.5B design partner signs at about month 12; build under $1M |
| Conservative | $5-8M | | Slower sales, several smaller sponsors, or a $1.8M build |
| Unbound-scale build ($5M) | $8.5-11.4M | | |

**Timing.** Earliest go-live is about month 18. Each 6-month sales delay adds about $0.8-0.9M (report 06).

### 8. Which existing sponsors could independently sustain the business?

**By arithmetic, at 20 bps, 19 addressable sponsors** each contribute more than Model B's $1.74M fixed cost. That falls to **10 fully loaded** and **5 if buyers hold the price to Ren's $737 per account**. After removing competitors (NPT), the recently migrated (AEF), processors (Dechomai) and double counts (GKCCF and Greater Horizons are one group), about **2-4 realistic decision units** remain:
- Jewish Communal Fund;
- the Greater Kansas City Community Foundation / Greater Horizons group;
- possibly ImpactAssets;
- the Chicago Community Trust or the Foundation for the Carolinas.

The community foundations need non-DAF fund support. **These are hypotheses, not leads.** Nothing shows any of them will switch or outsource. No business should be built on one of them alone, because losing the anchor takes the margin from 48% to 3% (report 05 §5).

### 9. Which customer segments are most profitable?

**Sponsors with $250M-1.5B of DAF assets and $150-700k average balances.** At 20 bps, every addressable sponsor at $100M or more is contribution-positive: 156 sponsors and $135B of assets. The median contribution is $0.16M at $100-250M, $0.56M at $250-500M and $1.1M at $500M-1B.

**Best fit:**
- **Independent nationals and faith/single-issue federations** with digital grantmaking (high balances, few check grants);
- **Mid-size community foundations** only where DAFs can be served separately from other fund types.

The SPN top-25 hypotheses (22 community foundations) should be read through that integration caveat.

### 10. Which customer segments should we avoid?

| Segment | Why |
|---|---|
| Sponsors under about $50-75M | 1,179 sponsors with $9B of assets; all negative at 20 bps |
| Small-balance programs (under $10k per account) | 61% of accounts, 0.1% of assets |
| Workplace and processor programs, university and hospital programs | Mostly negative |
| Captives (Fidelity, Schwab, Vanguard: 43% of assets) and wealth-affiliate programs already outsourced to Ren | Not buyable |
| Competitors offering private label (NPT) and sponsors that migrated recently | Not buyable soon |
| Complex-asset-heavy donors | Serve only with activity fees; about $700 per account-year even redesigned |

### 11. Should we prioritize software licensing or outsourced administration?

**Outsourced administration first.**
- Licence prices sit inside the incumbent band (0.5-9 bps).
- Unbound's vendor break-even needs 50-100k platform funds; only about 20 US sponsors hold 5,000+ accounts.
- Software-first is unprofitable within 60 months in the model, needing $6-7.6M of capital. Partnership-first nets 14 bps and never reaches profit.
- Administration earns the scarce, higher-priced layer.

**Add licensing after two or three administration clients are live.**

### 12. What operational activities must be eliminated or automated?

**Must happen, or the 20 bps economics fail** (about 50 minutes per account-year instead of about 260 conventionally):
- board-delegated straight-through approval of routine grants;
- reuse of eligibility determinations;
- continuous charity monitoring with exception-only human review in place of scheduled 180-day human re-verification (about $1 vs $69 per account-year);
- EFT-by-default grants (checks on request);
- structured intake;
- automated reconciliation and statements;
- event-driven rather than calendar-driven confirmations;
- a December deferral policy (no December 31 legal deadline for DAF grants).

**Kept unchanged:** legally required checks at approval and at release, sanctions screening, and sponsor reserved decisions.

### 13. What requirements should be changed?

See report 09. Unbound is not modified; the transfer candidates are:

| Candidate | Change |
|---|---|
| RC-ACT-001 | Lazy, evidence-change-driven 180-day review |
| RC-ACT-002 / RC-SE-005 | Exclusivity only for A3+ deciders; pooled preparation staff allowed |
| RC-ACT-007 / RC-SE-004 | Delegation as an onboarding exit criterion |
| RC-ACT-008 | EFT-by-default |
| RC-SE-001 | Per-account fee component |
| RC-SE-002 | Payout-neutral fee base |
| RC-SE-003 | Payment rails passed through at cost |
| RC-SE-006 | Time study before any price commitment |
| RC-SE-007 | Complex gifts as an activity fee |
| RC-SE-008 | Commercial licence terms as a gate |

### 14. What advantages are difficult for incumbents to replicate?

**Few.**
- **Temporary:** the redesign levers are policy changes incumbents can adopt (Unbound EV-02). Reusable configuration is also temporary, and a shared charity-verification network is weak, because eligibility data is a commodity and cross-sponsor sharing needs consent.
- **More durable:** a per-account, payout-neutral, portable offer with published control and outcome metrics. Incumbents whose revenue depends on bps, renewal friction and change orders cannot match it without cutting their own revenue.
- **Durable if earned:** clean SOC 1 and SOC 2 history with evidence-by-default controls. The entrant starts with none.
- **Not an advantage:** price.

### 15. What evidence would invalidate the entire business strategy?

| # | Evidence | Why it is decisive |
|---|---|---|
| 1 | Sponsor CFOs price administration per account near Ren's $737 and will not pay 15-25 bps-equivalent on high-balance books | Cheapest test: owner-led conversations quoting both bps and $/fund |
| 2 | A 90-day event log shows redesigned handling well above about 50 minutes per account-year, or board delegation unavailable at go-live | At AI-enhanced handling, break-even rises to about $1.5-2B per sponsor and smaller portfolios never profit |
| 3 | The platform build cannot be scoped under about $1-2M and no commercial licence to Unbound or Echelon components is available (PolyForm Noncommercial today) | Capital rises to $8.5-11M |
| 4 | Counsel concludes the servicer is a money transmitter for sponsor-originated payments | Licensing and bonding costs, and a different payments design |
| 5 | No sponsor of $0.5B or more is in a renewal window or willing to migrate within 12-18 months | Every capital figure assumes a signing at about month 12 |
| 6 | Incumbents re-tier and match per-account terms in renewals | Removes the only durable positioning |

## What has changed from the prior memos (corrections, originals preserved)

| Topic | Prior | Now |
|---|---|---|
| Fixed cost | $1,177,750 for 5 FTE | $1.66M base for the same roles; $1.74M with dual control |
| Labour | $50/h | $65.45/h |
| Incremental cost | $75 per account | About $55-90 per account under AI-native handling, by mix; $9-790 by archetype |
| Break-even | $725M | $1.1-1.5B operating, $1.8-2.3B fully loaded |
| Outsourced administration benchmark | "33-37 bps" | 18.5 bps (MS GIFT) to 38-40 bps on average assets |

## Readiness

- **Development:** research and model are complete for this stage. The model is reproducible: 28 tests pass and output is deterministic.
- **Commercial launch:** **not authorized by this research.** Launch needs:
  - buyer evidence on the tariff;
  - a time study;
  - a build plan and licence terms;
  - counsel's payments opinion;
  - a signed design partner.
