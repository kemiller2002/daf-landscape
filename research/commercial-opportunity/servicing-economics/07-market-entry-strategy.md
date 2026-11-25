# 07: Market-entry strategy

**Date:** 2026-11-25.

**Inputs:** reports 01-06, the adversarial review (report 08) and the strategy cash plans (report 06).

**Status:** strategy hypotheses. **There is no signed business, pipeline or buyer evidence.** Market opportunity is not the same as attainable revenue.

## 1. Strategy comparison

| | A Software first | B Administration first | C Anchor customer | D Multiple smaller customers | E Partnership distribution | F Combined |
|---|---|---|---|---|---|---|
| **Capital (trough, base)** | $5.95M (+ build risk to $7.6M) | $5.42M | $2.7-3.6M (founder-led to Model B) | $5.36M | $8.54M | ≥ A + B overlap, about $6-8M |
| **Time to revenue** | First licence about month 16; cash about month 17 | First go-live month 18 | Month 18 (anchor live) | Month 18, then one go-live every 4 months | Month 18 | As A, then as B |
| **Sales complexity** | Low per deal, many deals; competes with iPhi/Stellar, Foundant and Blackbaud on features | High: outsourcing decision plus migration | Very high: one decision unit worth $3M a year; board, RFP and auditor sign-off | High per deal, repeated 5-6 times | Medium: one partner, but partner economics dominate | Highest: two motions |
| **Required staffing** | 4 core (no operations) | Model B + 1 ops | Model A/B + operations steps at 5,000 accounts | Model B + per-sponsor steps | Model B | Both organizations |
| **Competitive differentiation** | Weak: price inside the incumbent band, no installed base (Unbound EV-01) | Moderate: staffed offer prices below Ren where Ren earns 38-40 bps | Moderate, with the anchor's own terms | Moderate | Weak: the partner owns the relationship | Moderate |
| **Customer acquisition cost** | High per dollar of revenue | High | Concentrated: one long cycle | Highest in total | Lower CAC, but about 30% revenue share | High |
| **Operational risk** | Low (sponsor operates) | High | High plus concentration | High, spread across sponsors | High | Highest |
| **Profitability (run-rate at m60)** | -$0.09M | $0.70M | $2.4-2.8M | $0.67M ($1.93M with a floored tariff) | -$0.60M | Depends on mix |
| **Scalability** | Needs 50-100k platform funds; only about 20 US sponsors have 5,000+ accounts | Step hiring per report 05 §6 | Fast to $2-3B, then the same as D | Linear in sponsors | Bounded by partner | Two cost bases |
| **Strategic flexibility** | High (no operations liabilities) | Medium | Low until diversified | Medium-high | Low (partner dependence) | High in theory |
| **Survives losing the largest customer?** | Yes | Partly | **No**: margin 47.9% → 2.8% without the anchor, and negative after a market fall | Yes (-$0.04M) | No | Partly |

**Normalized to $1.5B at a $250k balance (report 06):**

| Plan | Capital | Run-rate profit |
|---|---:|---:|
| Anchor | $4.21M | $0.83M |
| Three $500M sponsors | $4.69M | $0.81M |
| Five $300M sponsors | $5.61M | $0.38M |
| Partnership at 14 bps net | $6.86M | -$0.09M |

The anchor's advantage is mostly timing and fewer onboardings, not structural economics (ADV-013).

## 2. Recommended route (conditional)

**Administration first, on a design-partner basis, with two or three large sponsors rather than one anchor.** The tariff is cost-reflective, and software licensing comes later as an extension.

1. **Target profile.** Sponsors with $250M-$1.5B of DAF assets, average balances of $150k-$700k and digital grantmaking, that are not captive, not recently migrated and not running integrated community-foundation software for many fund types. There are 156 addressable sponsors at $100M or more and 80 at $250M or more (report 02 and `sponsor-model-economics.csv`). The strongest segments are independent nationals and faith/single-issue federations, plus mid-size community foundations only where DAFs can be separated from other funds.
2. **Design-partner terms.**
   - Prepaid implementation, or a minimum annual fee from signing.
   - Board delegation adopted at go-live (RC-SE-004).
   - Permission to measure a 90-day event log (RC-SE-006).
   - Payment rails passed through at cost.
   - Exit and portability terms written in from the start.
3. **Tariff to test with buyers.** A per-account fee of about $100-200 plus 5-10 bps, with activity fees for complex gifts, international grants and wires.
   - It is set to equal about 15-25 bps on the target book.
   - It is payout-neutral: approved-unpaid grants are excluded from billable assets.
   - Floors are capped at 1% of balance, and none apply to dormant funds subject to a sweep policy.

   A flat 20 bps stays as the comparison price for the 20 bps question.
4. **Organization.** Founder-led (Model A) to signing. Then two operations staff and a controller before go-live, which in practice is Model B's headcount. Model C structure comes after about $3B or 10+ sponsors.
5. **Capital.** About $3-4.5M if a design partner of $1B or more signs by about month 12 and the build stays under $1M. Plan for $5-8M, and for $8.5-11M if the build approaches Unbound's estimate.
6. **Software licensing later.** Offer the platform to sponsors that want to keep operations in-house once two or three administration clients are live. That spreads the build over more funds without making licensing the funding engine.

**Why not anchor-only:** concentration. Without the anchor, the remaining $1B book barely breaks even (+$0.06M a year), and any market fall then makes it lose money. Two or three large sponsors give almost the same economics with survivable concentration.

**Why not software-first:** licence price sits inside the incumbent band (report 01), break-even needs a platform scale that the US market barely contains (Unbound EV-01), and it does not reach profit within 60 months in the model.

**Why not partnership-first:** the partner's 30% share leaves 14 bps, below break-even at any realistic scale; channel owners also subsidise administration from advisory fees (report 01 §g).

## 3. Competitive response

Assume incumbents respond. In order of their cost:
1. Do nothing where they already earn about 18 bps (MS GIFT).
2. Re-tier small-account minimums and reprice at renewal.
3. Offer early multi-year renewals with discounts and waived change orders to at-risk clients.
4. Bundle managed services onto Stellar/iPhi at marginal cost.
5. Channel owners absorb administration cost to protect advisory assets.
6. Copy the redesign policies.

| Claimed advantage | Durable? | Note |
|---|---|---|
| Shared charity-verification evidence network | Temporary to weak | Eligibility data is a commodity; cross-sponsor sharing needs consent; incumbents at scale have more recipient overlap |
| Integrated accounting controls with SOC 1 evidence by default | Moderately durable if delivered | Auditor trust accrues over years; the entrant starts with none |
| Reusable sponsor configuration | Temporary | Lowers onboarding cost, but templates can be copied |
| Lower operational complexity (delegation, EFT default, continuous monitoring, December deferral) | Temporary | These are policy changes incumbents can adopt (Unbound EV-02) |
| Portability: no termination fee, full export | Durable as positioning | Easy to match technically, but matching hurts incumbents whose revenue depends on exit friction |
| Price | Not an advantage | Above market per account at high balances; below cost at low balances |

**Durable position, if any.** A per-account-priced, payout-neutral, portable offer with published control and outcome metrics, plus a measured, lower unit cost. This is hard for incumbents to match while their revenue model depends on bps, renewal friction and change orders. The cost advantage itself is temporary.

## 4. Charitable outcomes and incentives (summary of report 08 §ADV-14)

**Incentive risks under asset-only fees.**
- **Delaying grants or retaining assets:** the servicer earns less when payout rises, even though work rises.
- **Rejecting legitimate complex gifts:** these cost about $700 per account-year even with redesign.
- **Floors:** they push small funds toward closure.

**Safeguards adopted in the recommended tariff.**
- A payout-neutral fee base.
- Complex gifts as disclosed activity fees, so the servicer has no reason to refuse them. The sponsor decides acceptance.
- Floors capped at 1% of balance, with none on dormant funds subject to a sweep policy.
- A grant-latency SLA (standard grants within 5 business days; within 10 in December), with published metrics.
- No fee sharing on investment products.
- Published effective bps and dollars per account by band.

**Perspectives.**
- **Servicer:** prefers per-account and activity pricing, which is also the fairest.
- **Sponsor:** accepts only below its avoided cost.
- **Donor:** neutral, unless floors or deferral harm them.
- **Recipient charity:** benefits only with the latency SLA and parity for charities without EFT.

## 5. What must be true for the business to work

| # | Condition | How to test it |
|---|---|---|
| 1 | Two or three sponsors of $0.5-1.5B accept a cost-reflective tariff equal to 15-25 bps on their book | Owner-led CFO conversations quoting bps and $/fund |
| 2 | Redesigned handling reaches about 50 minutes per account-year (market mix) within 12 months of go-live | 90-day event log at a design partner |
| 3 | Board delegation is adopted at go-live | Design-partner commitment |
| 4 | The build fits under about $1-2M for a servicing-only scope, or a licence to Unbound is available on commercial terms | Build plan and licence terms (ECH: PolyForm Noncommercial today) |
| 5 | The servicer is not a money transmitter for sponsor-originated payments | Counsel opinion, CST-C08 |
| 6 | SOC 1 and SOC 2 Type 2 reports are achievable within the first 12-18 months | Readiness assessment |

If (1) or (4) fails, the business does not work at 20 bps on a lean organization.
