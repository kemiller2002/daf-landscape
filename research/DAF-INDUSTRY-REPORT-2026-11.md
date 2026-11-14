# The U.S. Donor-Advised Fund Industry, November 2026: Structure, Economics, Technology and AI

**Consolidated report.** Version 2026-11-15. Repository `kemiller2002/daf-landscape`.

This report sits on top of the repository's 96 research documents and 89 datasets. It does not repeat them. Each section states the current best understanding, its evidence state, and where the evidence lives.

**Labels used throughout:**
- **Claim states** follow the EDF claim-and-confidence policy: *internal-demonstration, suggestive, unsupported, contradicted*. Confidence runs Low → High.
- **[V]** = independently validated (registers in `data/mission-2026-11-14/validation-register*.csv`).
- **[RT]** = corrected by red-team review.
- **[S]** = scenario number, not an estimate.

**Decision-oriented companion:** [strategic synthesis A–G](mission-2026-11-14/strategic-synthesis.md).
**Method and frameworks:** [Clarity/EDF application guide](mission-2026-11-14/clarity-edf-application-guide.md), pinned to the canonical framework commits.

---

## 1. Market size and shape

| Metric (DAFRC revised, FY2024) | Value | Note |
|---|---|---|
| Charitable assets in DAFs | $327.87bn | FY2020→FY2024 CAGR 18.1% |
| Contributions | $90.57bn | +38.6% YoY after declines in FY2022–23 |
| Grants | $64.60bn | CAGR 16.1% |
| Reported accounts | 3.59m | **79.5% are in 22 donation-processor sponsors holding 0.9% of assets** |
| Traditional invested accounts | ≤ 737k | upper bound; no lower bound from public data |
| Sponsors | ~1,500 (1,512 reported) | about 803 community foundations |

DAFRC totals recompute exactly from its 8,751-row sponsor panel, which is reproduced in the repository with `scripts/mission_daf_metrics.py` [V]. NPT's annual series agrees on dollars within about 2% for FY2020–23. It counts 1.55–1.84× fewer accounts because it excludes most processors.
Sources: [quantitative datasets](mission-2026-11-14/quantitative-datasets-and-data-dictionary.md); [processor share](mission-2026-11-14/regulation-market-structure-portability.md).

**Payout.**
- **Aggregate:** grants over beginning assets were 23.7–28.4% in FY2020–24.
- **Typical sponsor:** the median sponsor with ≥$1m in assets pays out about 11–12.5%, and 19–24% of those sponsors pay out under 5%.
- **By segment:** national sponsors' median is about 20%, community foundations about 11%, and university or hospital sponsors about 5.4% **[RT]**.
- **Transfers between DAF sponsors** are 10–18% of the nationals' listed grant dollars. They inflate apparent payout and double-count in market sums.

Fund-level payout is not public.

**Concentration differs by layer.** Do not conflate these markets:

| Layer | Measure | Finding | State |
|---|---|---|---|
| Sponsor assets | DAFRC FY2024 | CR3 45.5%, CR5 55.8%, HHI ≈ 830 (unconcentrated). National sponsors only: CR3 63.2%, HHI ≈ 1,566 | [V][RT] High |
| Administration | Period-aligned | About 39% of assets at three affiliate-linked nationals (Fidelity/FMR; Schwab; Vanguard as a hybrid). Fully outsourced platform administration: ≥6 sponsors holding 9.1% | Medium |
| Software | Vendor self-reports | Licensed DAF software at 31–94% of sponsors. Community foundations mostly on Foundant CommunitySuite (claims 700+). National and white-label market: Ren (incl. iPhi), Foundation Source, TIFIN Give, Give Interactive | Low-Medium; HHI not computable |
| Custody | Audited notes | ≥26.2% of assets with one custodian family (Fidelity Brokerage Services) | lower bound only |
| Distribution | Channel graph | About 11 wealth-firm programs on RCF + Ren; SEI multi-sources (RCF/Ren and GiveClear/TIFIN) | Medium-High on edges |

Sources: [vendor dependency and concentration](mission-2026-11-14/vendor-dependency-concentration.md); [red team 2B](mission-2026-11-14/red-team-wave2b-graph-data-incentives.md).

---

## 2. Who does what: legal sponsor, administrator, technology, rails, distribution

The industry is a stack whose layers are often owned by different parties. The relationship graph has 131 nodes and 167 edges, every edge sourced and status-labelled: 134 confirmed (one more after red-team), 17 historically confirmed, 11 inferred, 5 unknown. A red-team sample of 15 "confirmed" edges found 0 status errors and 2 scope imprecisions.

### 2.1 Affiliate-integrated nationals
Fidelity Charitable, DAFgiving360 and Vanguard Charitable combine sponsor brand, affiliated investment funds and affiliated administration:
- Fidelity Charitable pays FMR affiliates amounts equal to donors' administrative fees **[V]**.
- Vanguard Charitable has 35 of 37 pools in Vanguard funds and pays a related-party service fee of $4.24m in FY2026 **[V]**.
- **New:** Vanguard Charitable selected **Give Interactive** for DAF recordkeeping (Nov 2025 release).

### 2.2 The RCF–Ren spine
Renaissance Charitable Foundation sponsors branded programs for Edward Jones, Ameriprise, RBC, LPL/Commonwealth, Northwestern Mutual, UBS (one of four sponsors there), SEI, Fisher and MDRT. Ren supplies the "DFX powered by Ren" portals.

- **The payment flow:** RCF paid Ren $19.23m in FY2024. That equals 98% of RCF's admin-fee revenue from individual-fundholder accounts, the rate in force since FY2023 **[V]**.
- **Ren's role:** RCF describes it as platform, administrative infrastructure and operational support. Ren is not a technology-only vendor **[V]**.
- **Ren beyond RCF:** Ren portals also front Morgan Stanley GIFT (new finding), Bank of America's Charitable Gift Fund and AEF. For Bank of America the only evidence is the portal; the earlier 10-K claim is **contradicted** **[V]**. Ren-owned iPhi still serves the Cleveland Foundation and ImpactAssets.

**Edward Jones Charitable Gift Fund.** Each role has separate evidence:

| Role | Status | Evidence |
|---|---|---|
| RCF as legal sponsor | Confirmed | Edward Jones product page plus RCF's self-description |
| RCF manages and administers the fund | Confirmed | Edward Jones portal |
| Ren technology | Confirmed | Portal displays "DFX powered by Ren" |
| Ren back-office administration for Edward Jones specifically | Inferred only | RCF pays Ren under an audited contract, but nothing names Ren for Edward Jones |

Two Edward Jones figures remain open:
- The 2021 "$2.9bn" figure is unverifiable (source PDF now 404) **[V]**.
- Edward Jones's private DAF has no public sponsor, administrator or vendor.

### 2.3 Foundation Source / Charityvest
Foundation Source (owned by GTCR since 2023) acquired Vennfi (2024) and Giving Place (2025). Charityvest is an independent sponsor powered by Foundation Source, with TIAA, Temple and OneGive programs.
- **Governance conflict:** Charityvest's President and director is paid by Foundation Source ($163,944 via Vennfi, 2024). This is stronger than previously recorded **[V]**.

### 2.4 TIFIN Give / GiveClear
GiveClear is the sponsor and TIFIN Give the platform. Since 2026-10-28 they also power the SEI Charitable Fund. Chariot handles disbursement.

### 2.5 Payment rails
Four camps exist: Fidelity's own EFT/Stripe, PayPal Grant Payments (NPT, Vanguard), Ren's Rapid Disbursement Engine, and Chariot Disbursements (TIFIN/GiveClear, Daffy, Founders Pledge, Groundswell, Charityvest from Aug 2026).
- The only observed switch is Charityvest moving from PayPal to Chariot.
- About 67% of Fidelity grants already go by EFT. No electronic-only mandate is confirmed.

### 2.6 Eligibility data
IRS BMF, Pub 78, revocation and OFAC data sit upstream of every disclosed eligibility check.

### 2.7 Shared single points of failure
- The RCF–Ren contract.
- Ren's DFX portal family.
- Foundation Source behind Charityvest's programs.
- Chariot on Column N.A.
- GiveClear as TIFIN Give's sole sponsor.
- The IRS master file.

Sources: [vendor graph](mission-2026-11-14/vendor-dependency-concentration.md); [breadth](mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md); prior `edward-jones-ren-*`, `ren-*`, `charityvest-*` files.

---

## 3. Economics and incentives

**Revenue model.**
- Sponsors charge tiered basis points on balances. Fidelity, DAFgiving360 and Charityvest start at 0.60% on the first $500k. RCF/Ren charges 0.65% with a $250 minimum. Bank of America charges 0.90% flat. Daffy charges flat memberships of $0–40/month.
- Investment expense ratios flow to affiliated managers at the nationals.
- Adviser fees on DAF assets (for example OneGive's waivable 55 bps **[V]**) bind distribution.

**Incentive structure.** Analysis: [industry incentives](mission-2026-11-14/industry-incentives-structural-analysis.md), with [RT] corrections.

| Practice | Classification | Confidence |
|---|---|---|
| Asset-based fee alignment favouring retention | **Mixed**: incentive documented, effect on payout unsupported **[RT]** | Low on effect |
| No payout requirement | Structural (statute) | High |
| Edge-case grant review (§4966/4967) | Structural | Medium-High |
| Manual review of listed public charities | **Mixed** | Medium |
| Paper checks | Mixed, leaning habit | Medium |
| History loss in platform migrations | Habit | Medium |
| Weak nonprofit leverage | Structural | Medium-High |

**Who resists redesign (by incentive, not intent):** affiliated managers, fee-share administrators, advisers paid on DAF AUM, and discretion-valuing sponsors.
**Who benefits:** working nonprofits, small donors, and challengers not paid on assets.

**Challengers.**
- Daffy reports $2bn in assets (Sept 2026, company-reported). Its FY2024 990 shows $334.19m net assets **[V]**.
- Charityvest's 2025 figures are company-reported and not comparable to its 990 series **[V]**.
- Both raised effective prices as they moved upmarket. Incumbents removed minimums (2020).

**Vendor economics.** Ren's corporate revenue, margins and customer concentration are not public. The audited RCF payment is a named service fee, not Ren's ARR. Ren's claims of ">60%", "about half" or "$200bn" of DAF assets are **unsupported** on public evidence:
- Publicly evidenced Ren-linked sponsors hold about 8.7% of assets.
- The "$200bn" figure includes non-DAF assets.
- The arithmetic ceiling outside the four largest sponsors is about 48% **[RT]**.

---

## 4. Operations: grant workflow, exceptions and portability

**Legal frame.**
- §4966 taxes taxable distributions: 20% on the sponsor, 5% (capped at $10k) on knowing managers.
- §4967 taxes prohibited benefits: 125% on the donor or adviser, 10% on knowing managers.
- §4958(c)(2) makes grants, loans and compensation to donors or advisers automatic excess benefits.
- Grants to listed §170(b)(1)(A) public charities are excepted from §4966, and grantors may rely on IRS status listings.

**Exception share.** Observable non-standard grants (foreign, fiscal-sponsor, non-501(c)(3)) are about 2.5–3% of dollars at the large nationals and far less by count. Foreign grants alone are 1.46% of dollars across the four largest nationals (NPT 4.84%). This is a floor: new-charity reviews and declines are invisible in filings.

**Discretion beyond tax exposure.** In 2026, after the April 21 SPLC indictment, the California AG's release named Fidelity Charitable, Vanguard Charitable and DAFgiving360 as having restricted grants **[RT confirmed]**. Persistence of those holds is unknown.

**Operating metrics.** No sponsor publishes grant turnaround P50/P90, exception rates or reviewer minutes. NPT processed 159,543 grants in FY2025. Its U.S. DAF program granted $6.44bn **[V][RT]**; the $6.61bn release figure likely includes U.K. and Transatlantic programs.

**Portability.**
- None of 12 sponsors reviewed publishes an outbound transfer policy. Transfers are cash after liquidation and take 10 business days to 4 weeks.
- No sponsor commits to moving grant history. AEF's own migration kept two years.
- About $7.5bn moved sponsor-to-sponsor in 2024.

Sources: prior batch 2A/2B/2C files; [regulation and portability](mission-2026-11-14/regulation-market-structure-portability.md); [breadth §6](mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md).

---

## 5. Technology history: announced vs delivered

The timeline has 195 dated events across 16 company groups and 163 source URLs. Of 39 announced capabilities:

| Delivery status | Count |
|---|---|
| Evidence of delivery | 15 |
| Partial | 10 |
| No public evidence yet | 12 |
| Contradicted | 2 |

By company:
- **Daffy:** 5 of 5 delivered.
- **Chariot Disbursements:** the clearest beta-to-production trail.
- **TIFIN Give:** announces most often, and its Louise AI has only vendor evidence.
- **Ren and Foundation Source:** broad claims (daily unitization, DAF OS) with little public delivery evidence.

**Private-equity ownership changes are followed fast by leadership change and roll-ups.** GTCR named a new CEO at Foundation Source six days after closing, followed by four acquisitions in about 17 months. Customer effects are unobserved.

**Ren's dates, scale claims and SOC 2 type drift over time.** SOC 2 is stated as "Type 2" in July 2025 and "Type 1" in April 2026, both in Ren's own boilerplate; no report has been seen **[V]**.

Missing evidence is not treated as non-delivery. Source: [competitive histories](mission-2026-11-14/competitive-history-timelines.md).

---

## 6. Regulation

- **Proposed regulations:** the 2023 proposed §4966 regulations (REG-142338-07) are **neither final nor withdrawn** (Federal Register query, 2026-11-14). The comment period was extended to Feb 15, 2024.
- **Guidance plan:** the 2026–27 Priority Guidance Plan (2026-09-29) reframes the project as "guidance under sections 4966 and 6033 regarding certain DAF arrangements".
- **The pending adviser question:** the proposal would treat a donor's personal investment adviser who manages DAF assets as a donor-advisor. This would affect the adviser-managed channel.
- **OBBBA (2025):** excludes DAF gifts from the new nonitemizer deduction and adds a 0.5%-AGI floor and a 35% cap from 2026.
- **Not enacted:** the ACE Act; IRA-to-DAF QCD bills (introduced only); California AB 1712 (failed 2020).
- **No DAF-specific SEC or FINRA rule found.** The SEC withdrew its predictive-analytics conflicts proposal (2025-06-12).

Tracker: `data/mission-2026-11-14/regulatory-status-tracker.csv`.

---

## 7. AI in DAF operations

**Adoption.**
- 30 use cases were inventoried, with 2 more (Bonterra) identified by red team.
- 10 are DAF-direct: 6 announced, 1 demonstrated, 2 deployed with evidence, 1 unverified.
- **There is no public evidence of AI in sponsor-side approval or eligibility determination.** The one sponsor-side exception is Daffy's announced charity-data flagging **[RT]**.
- The agentic frontier is donor-side: TIFIN Give's Louise executes donor requests, and Daffy's MCP server exposes `make_donation` with no documented limits **[V]**.

**Economics** ([AI economics](mission-2026-11-14/ai-economics-replacement-analysis.md), with red-team corrections):
- Inference cost is immaterial: about $0.45 per heavy document review against about $83 of reviewer time **[V]**.
- The model's result that "AI on the existing workflow ranks last in 16/16 processes" is **determined by its assumptions**, not by evidence about AI **[RT]**.
- What is reasoned rather than modelled: redesign removes exception classes, while AI only shortens handling. AI economics clear plausible governance costs at vendor or network scale, not per process per sponsor.
- The single most important missing evidence is a measured exception, handling-time and QA study at any sponsor.

**Governance** ([AI failure modes](mission-2026-11-14/ai-governance-failure-modes.md)):
- **Accountability:** liability attaches to the sponsor and to knowing fund managers, so approval authority must stay human or deterministic.
- **The control rule:** **AI may add a flag, never clear one.** This converts the gravest failure, a missed sanctions or prohibited-benefit case, from risk created to risk reduced.
- **Rubric rating** (not observed incidents): unconstrained AI creates risk in 13 of 16 failure modes and redistributes it in 3.

---

## 8. Entry strategy for an AI-native provider

From [entrant simulation](mission-2026-11-14/ai-native-entrant-simulation.md), red-teamed:
- **What not to build:** a sponsoring charity, custody, payment rails, charity master data or a full system-of-record. Each can be partnered: sponsor-of-record APIs (Endaoment; Daffy for Developers), Chariot, custodians, and IRS bulk data.
- **The cheapest probe:** Strategy 3, an AI-native operating layer over existing sponsors with exception-only routing under **deterministic sponsor rules** plus continuous eligibility monitoring.
  - **[RT]** It is a **conditional probe, not a recommendation.** At $120k/yr it needs about 76k–369k grants/yr per customer to break even, which most independent and community-foundation sponsors lack.
  - Its capital advantage is a headcount assumption: it needs about 42 customers for $5m ARR against 5 for a full platform.
- **Gating question:** do sponsor–vendor contracts grant API and data-export rights?

---

## 9. Evidence quality, validation and limits

**Independent validation and red-team review** checked **80 consequential claims**. These were done by agents that did not author the work and were not given the original conclusions.

| Result | Count |
|---|---|
| Confirmed | 45 |
| Partially confirmed | 25 |
| Contradicted | 7 |
| Unable to verify | 3 |

Model arithmetic, the DAFRC recomputation and 6 hand-checked derived metrics reproduced exactly. Corrections were appended to source documents as dated, governing sections; no original text was deleted.

**Limits.**
- All evidence is public-source. No vendor tests, sponsor interviews or contracts were obtained.
- The shared web-search budget ran out during the mission. Some items rest on direct fetches or search summaries and are flagged.
- The Wayback Machine could not be read.
- The coverage matrix measures depth on a purposive set of 33 entities, not the about-1,500-sponsor universe.

**Evidence that would most change this report:**
1. A sponsor time-and-motion study.
2. Ren's denominator for its share claims.
3. Give Interactive's scope at Vanguard Charitable.
4. Sponsor–vendor API and data-export clauses.
5. Fund-level payout by fee model.
6. Final §4966/6033 guidance.

See [synthesis §F](mission-2026-11-14/strategic-synthesis.md) and the [research queue](../data/mission-2026-11-14/research-priority-queue.csv).
