# 05 - Untapped institutional markets

Status: research (2026-11-26). Track C. Agent CD. Public sources only; no outreach, no personal data, no legal opinion. Registers (fragments, merged later by the integrator): [market-segments.csv](data/fragments/CD/market-segments.csv) (P3-SEG-CD001..CD018), [institutional-prospects.csv](data/fragments/CD/institutional-prospects.csv) (P3-PRS-CD001..), [claims.csv](data/fragments/CD/claims.csv), [sources.csv](data/fragments/CD/sources.csv), [assumptions.csv](data/fragments/CD/assumptions.csv), [hypotheses.csv](data/fragments/CD/hypotheses.csv), [evidence-gaps.csv](data/fragments/CD/evidence-gaps.csv). Working data: [bmf-untapped-counts.csv](data/evidence/CD/bmf-untapped-counts.csv), [minimum-viable-program-grid.csv](data/evidence/CD/minimum-viable-program-grid.csv). Phase II baseline: [12 - Market entry segments](../competitive-displacement/12-market-entry-segments.md) (SEG-001..014) and [11 - Institutional distribution](../competitive-displacement/11-institutional-distribution.md).

## Answer in brief

1. **Who can be a sponsor.** Under IRC 4966(d)(1) a sponsoring organization must be described in section 170(c), excluding governmental units (170(c)(1)), and must not be a private foundation (P3-SRC-CD001). The IRS's own page describes sponsors as 501(c)(3) organizations (P3-SRC-CD002). **Banks, trust companies, RIAs, broker-dealers, custodians, for-profit fintechs, insurers, accounting firms and credit unions cannot sponsor DAFs themselves.** They need an affiliated public charity, as Fidelity, Schwab, BofA and Thrivent have, or a partner sponsor, as in Regions with RCF, Wells Fargo with NPT, TIAA with Charityvest and Ohio Wesleyan with The Columbus Foundation (P3-CLM-CD001, P3-CLM-CD003, P3-CLM-CD009). Public universities that are governmental units cannot sponsor either. Their affiliated foundations, which claim foundation code 13, can (P3-CLM-CD002; inference from the statute; counsel to confirm).
2. **Where the greenfield is.** Our IRS BMF join (P3-SRC-CD003) checks each charity against the DAFRC sponsor panel (SRC-013) and the repository's non-DAFRC Schedule D/Part IV harvest (P3-SRC-CD019):
   - **Community foundations are not greenfield.** Of BMF T31 public charities with at least $50M of assets, 375 of 394 (95%) are already in the DAFRC sponsor panel, and 616 of 712 (87%) of those with at least $10M show some DAF signal.
   - **Education and health institutions are greenfield by count.** 3,056 public-charity education and health entities hold at least $100M of total assets, and only 99 (3%) show any DAF signal (P3-CLM-CD005).
   - **No signal is not the same as no offering.** These institutions can offer DAFs through a partner sponsor and leave no trace in their own filings, as Ohio Wesleyan does.
3. **Why they do not offer DAFs.** The binding barriers are not technology. They are, in order:
   - perceived demand and a free alternative: donors can already grant from Fidelity, Schwab or a community foundation, and the institution receives the money anyway;
   - regulatory responsibility (4966/4967 and the pending 4966 regulations, P3-SRC-CD014);
   - for financial institutions: their own sponsor relationships, distribution economics and third-party-risk procurement (SEG-003, CLM-023);
   - minimum scale, but only for a *newly formed* sponsor.
4. **Minimum viable programme size.** Shared technology does lower it, but only where the sponsor-level fixed cost is already paid or shared:
   At the tail-median balance of $133k, base costs and fees of 1.5% down to 0.6%:
   - **Programme hosted on an existing sponsor:** break-even falls to **about 6-19 accounts ($0.8-2.5M of DAF assets)**.
   - **Existing charity adding its own programme:** **about 15-46 accounts ($2.0-6.1M)**.
   - **Newly formed sponsor:** **about 52-164 accounts ($6.9-21.8M)**.

   Across balances of $50k-250k the base-cost ranges widen to 3-189, 8-472 and 26-1,699 accounts respectively. All inputs are ASSUMPTION or INFERENCE ranges from the Phase II event model (P3-CLM-CD011, SRC-063).

   Small programmes are already common: the median tail sponsor runs 24 DAFs (SRC-013). Operating technology is therefore **not** what keeps institutions out (P3-CLM-CD013).

   **Revision 2 (P3-CHL-REV1013, P3-CHL-REV1014, P3-CHL-REV3043).** These break-even counts cover only the programme's running cost. They leave out the institution's own first-year costs, none of which is priced here:
   - onboarding (excluded from F, §3.1);
   - programme legal documents, including the 170(f)(18) acknowledgment;
   - 4966/4967 policies and counsel review;
   - board approval;
   - audit scope;
   - custody or unitization and a custodian feed;
   - CRM or gift-system integration;
   - staff time on sponsor-reserved approvals.

   Counsel and policy work is likely to be the first purchase objection for S1 and S4. Treat the counts as a lower bound on the size at which a programme makes sense to the institution.
5. **The binding constraint for the vendor.** It is the cost of acquiring and onboarding each programme, not the cost of operating it.
   - A programme worth $10-25k a year in licence revenue never repays a $60-250k direct CAC (PAR-023) within five years (P3-CLM-CD012).
   - Small programmes therefore become viable for Echelon only if they are acquired and onboarded in bulk through a host sponsor, a league or another channel, and configured from templates. This is the evidence-limited case for Sequence E ([06](06-customer-acquisition-without-displacement.md), P3-SEQ-CD001).
   - **Revision 2 (P3-CHL-REV2045, P3-CHL-REV2019).** The greenfield count is a market for a **hosted programme service**, delivered by a sponsor or service partner. It is not evidence of demand for licences. The barriers above are demand, free alternatives and regulatory responsibility, and a licence removes none of them. The model's sequences E and G, built on this market, do not pay back for the vendor ([14](14-commercial-sequencing.md)). A licensing addressable market by sponsor size is in agent CE's [sponsor-size-check.csv](data/evidence/CE/sponsor-size-check.csv): only 33 panel sponsors hold 2,646 accounts or more (P3-CLM-CE001). Separating non-captive from captive sponsors in that count is open (P3-VAL-CE001).

## 1. Sponsorship capability by institution type

| Institution type | Can it be a sponsoring organization itself? | Basis | How it offers DAFs today (public examples) |
|---|---|---|---|
| Community foundation (501(c)(3) public charity) | **Yes** | 4966(d)(1); 804 already report DAFs (SEG-002) | Own programme; also hosts other institutions' programmes (Ohio Wesleyan with The Columbus Foundation, P3-SRC-CD007) |
| Private university or college (501(c)(3), 170(b)(1)(A)(ii)) | **Yes** | 170(c)(2) organization, not a private foundation | Own programmes at Stanford, Harvard, Yale, Columbia, Brown and Cornell, usually with a host-share rule of about 50% (P3-SRC-CD017) |
| Public (state) university | **No, as a governmental unit (170(c)(1) excluded)**. Its affiliated foundation can | 4966(d)(1)(A) text; BMF foundation code 13 = organization operated for a government college or university (2,919 entities) | Through its foundation (UNF Charitable Gift Fund at Nebraska; UC San Diego Foundation; MSU programme run with BNY Mellon CGF, P3-SRC-CD009, P3-SRC-CD017) |
| Hospital, health system or hospital foundation (501(c)(3)) | **Yes** | 170(c)(2) public charity | Rare. Mayo Clinic (60% host rule) and Penn Medicine (50%) are examples (P3-SRC-CD017) |
| Religious foundation or denominational body (501(c)(3)) | **Yes**. A church itself also qualifies under 170(c)(2), but practice is a separate foundation | 184 religious sponsors FY2024 (SEG-010) | NCF, Signatry, Thrivent Charitable, Catholic diocesan foundations (affinity G03-G09) |
| United Way or federated campaign (T70) | **Yes** | 90 of 274 T70 entities at $10M or more show a DAF signal | Some already sponsor |
| Credit union | **No**. Federal credit unions are exempt as federal instrumentalities and state credit unions under 501(c)(14); neither is a 170(c)(2) charity (INFERENCE; counsel to confirm) | 4966(d)(1) | Through league foundations (Credit Union Impact Foundation, Carolinas CU Foundation, Iowa CU Foundation, Cornerstone Foundation; SEG-004, SEG-014) |
| Bank or trust company (national or state) | **No** | Not a 170(c) organization | Affiliated charity (BofA Charitable Gift Fund); partner sponsor private label (Regions on RCF; Wells Fargo with NPT; First Citizens and KeyBank on Ren; SEG-003); distributor (SEI with TIFIN Give, SRC-021) |
| RIA, broker-dealer, wirehouse, custodian | **No** | Not a 170(c) organization | Custodian-affiliated charities (Fidelity Charitable, DAFgiving360, Vanguard Charitable); partner sponsors (Endaoment in Altruist; Charityvest for TIAA and OneAscent) (SEG-005, SEG-006) |
| Fintech or consumer giving app (for-profit) | **No**. It must create a separate 501(c)(3) | Not a 170(c) organization | Daffy (Daffy Charitable Fund), Givinga (Givinga Foundation), Chariot (rails only) (CMP-004, CMP-007, CMP-014) |
| Insurance carrier or fraternal benefit society | **No**. In practice it uses an affiliated public charity | Thrivent Charitable is a separate public charity (P3-SRC-CD013) | Affiliated charity |
| Employer or employee-benefits platform | **No** (for-profit employer) | Not a 170(c) organization | Daffy for Work, Givinga, Morgan Stanley at Work, Blackbaud Giving Fund, AOGF (P3-SRC-CD010, P01-P25 in the [expanded market map](../../data/expanded-daf-market-map-2026.csv)) |
| Accounting or tax network (CPA firm) | **No** | Not a 170(c) organization | No public CPA-network DAF programme found (P3-GAP-CD007) |
| Family office | **No**. Its private foundation is excluded by 4966(d)(1)(B) | 509(a) | Uses national sponsors (SEG-008) |
| Supporting organization (509(a)(3)) | Statutorily **yes**: it is not a private foundation | 4966(d)(1) | Some faith and university vehicles. Type III rules and grant restrictions need counsel (P3-GAP-CD006) |

**Implication for Unbound.** Unbound is technology for sponsors and must never require Echelon Foundry to become one (BRIEF constraint). The organizations that can buy a DAF *programme* without a partner charity are public charities. Every financial-institution route needs a third party with sponsor status: an existing sponsor, a league foundation or a newly formed affiliated charity. That makes the sponsor the critical counterparty in every institutional deal and supports the partner-first direction (DEC-001).

## 2. Why each type does not offer DAFs today (barrier matrix)

Ratings run H (binding), M (material) and L (minor), with "?" where unknown. They are INFERENCE from the evidence cited in the segment registers. No institution was interviewed.

| Type (segment) | Technology | Regulatory responsibility | Ops complexity | Minimum scale | Economics | Expertise | Procurement | Custody | Sponsor relationship | Distribution | Perceived demand | Reputational risk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Community foundations (SEG-002; P3-SEG-CD003) | L | L | M | L-M | M | L | M | L | n/a (they are sponsors) | L | **already offer** | L |
| University and college foundations (P3-SEG-CD001) | M | M (4966/4967; host-benefit rules) | M | M | M (host-share caps keep assets at home but fee income is small) | M | M | L (endowment pool) | L | L (alumni base) | **H: national DAFs already deliver grants to them free** | M (perceived self-dealing; [b50-03](../mission-2026-11-14/b50-03-institutional-daf-programs.md)) |
| Hospital and health-system foundations (P3-SEG-CD002) | M | M | M | M | M | H (few have planned-giving DAF expertise) | M-H (health-system IT security reviews) | L | L | L | **H**: only about 10 of 263 large health-support foundations show a DAF signal | M |
| Religious institutions without a foundation (P3-SEG-CD009) | M | M (Phase II affinity guardrail: tithes stay direct) | M | H | M | H | L-M | M | M (NCF and Signatry already serve them) | L | M | M |
| United Ways and federated campaigns (P3-SEG-CD004) | M | L | M | M | M | M | M | L | L | M | M (33% of large T70 already sponsor) | L |
| Community and regional banks (SEG-003; P3-SEG-CD005) | M | **H** (cannot sponsor; fiduciary, UDAAP) | M | M | M (bank keeps the investment fee, e.g. Regions 60 bps) | M | **H** (TPRM 5/5, CLM-023; governing guidance under revision, P3-SRC-CD021) | M | **H** (must contract a sponsor) | **H** (distributors: SEI-TIFIN) | M (SEI sees demand: VENDOR-CLAIM) | M |
| Credit unions (SEG-004; P3-SEG-CD006) | M | **H** (cannot sponsor) | M | **H** (small balances, SEG-004) | **H** | H | H (4/5) | M | M (leagues) | M | **H: no member-facing DAF found** (CLM-024; P3-SRC-CD016) | L |
| Trust companies (SEG-007; P3-SEG-CD007) | L-M | H (cannot sponsor; fiduciary) | M | M | M | L | H | L | H | M | L-M | M |
| RIAs (SEG-006; P3-SEG-CD008) | L | H (cannot sponsor; pending advisor-as-donor-advisor rule, P3-SRC-CD014) | L | H (median firm $447M RAUM) | **H** (custodian DAFs free) | M | L | L | H | M | L (served) | L |
| Family offices (SEG-008) | L | H (private foundation excluded) | L | H | H | L | L | L | n/a | n/a | L | L |
| Corporate giving and employee benefits (SEG-009; P3-SEG-CD010) | L | M | M | L | M | L | H (SOC 2, DPA) | L | M | M | M (crowded: Daffy for Work, Givinga, Benevity) | M |
| Fintechs (P3-SEG-CD011) | L | H (needs own charity) | M | M | M | M | L | M | H | M | M | H (sponsor-of-convenience risk) |
| Custodians (P3-SEG-CD012) | L | H | L | L | M | L | L | L | n/a (have affiliates) | L | served | L |
| Accounting and tax networks (P3-SEG-CD013) | ? | H (independence rules for attest clients: INFERENCE) | M | M | ? | M | M | H (no custody) | H | M | ? | M |
| Insurance and financial planning (P3-SEG-CD014) | L | H | M | M | M | L | M | M | H | L | ? | M |
| CU league and CUSO foundations (SEG-014; P3-SEG-CD015) | **M-H (manual ops; INFERENCE)** | L (are 501(c)(3)) | M | M | M | M | M | L | n/a | M | M | L |
| Professional and alumni associations (P3-SEG-CD016) | M | M (c6 versus c3 split) | M | H | H | H | L | M | H | M | L | M |

**Reading.** Technology is "H" only for the league foundations, and even there it is inferred. Everywhere else the binding barriers are demand, sponsor status or distribution. This repeats Phase II HYP-001 in a greenfield setting: **better DAF technology does not create institutional demand by itself.**

## 3. Can Unbound lower the minimum viable programme size?

### 3.1 Method

A *programme* is a branded set of DAFs held by one sponsoring organization. The programme owner breaks even at N* accounts, where N* = F ÷ (B × f − v):
- **F** is the programme's annual fixed cost;
- **v** is the all-in variable cost per account-year;
- **B** is the average balance;
- **f** is the all-in administration fee rate.

The grid of 243 cases is in [minimum-viable-program-grid.csv](data/evidence/CD/minimum-viable-program-grid.csv); the assumptions are P3-ASM-CD001..CD008.

| Input | Low / base / high | Basis |
|---|---|---|
| v, variable cost per account (sponsor labour + failure cost + platform licence) | $120 / $247 / $370 | Phase II MD-6 system variable $197 per account (sponsor-borne labour at ×1.4 efficiency, SRC-063, PAR-021) less vendor variable $31, plus licence $40-120 (PAR-012). Low reflects tail activity: median payout 11.7%, against about 9 grants per account-year in the model |
| F, programme hosted on an existing sponsor (white-label configuration) | $5k / $10k / $15k | E23 configuration upkeep (3,600 min/yr AI-native at $80/h ÷ 0.75 utilisation ≈ $6.4k) plus programme reporting; ASSUMPTION |
| F, existing public charity adding its own DAF programme | $13k / $25k / $40k | 30-60% of the Phase II AI-native sponsor-level cost of $43.7k (E21 reporting, E22 audit, E23 upkeep), plus a platform minimum up to $12.5k (Givinga base fee, CLM-038); ASSUMPTION |
| F, newly formed sponsor charity (e.g. a bank or fintech affiliate) | $60k / $90k / $140k | Full $43.7k sponsor-level cost, plus external audit, legal, insurance and state registration (UNKNOWN; ASSUMPTION $15-60k), plus a platform minimum |
| B, average balance | $50k / $133k / $250k | Tail median average account $133k (IQR $61k-263k, SRC-013); NPT median $79.7k (market-demand M30) |
| f, fee rate | 0.6% / 1.0% / 1.5% | Charityvest 0.6% (P06); Credit Union Impact Foundation 0.75% (SEG-004); tail CF published median 150 bps at $100k (P3-SRC-CD018) |

One-time onboarding is not in F. The Phase II AI-native figure is $48k per sponsor (onetime_per_sponsor, SRC-063). Templated programme configuration on an existing tenant is assumed at 10-25% of that (P3-ASM-CD007).

**Revision 2 (P3-CHL-REV3043).** The 10-25% applies to **configuration** only: fund types, fee schedule, branding and reports. Governance and legal work is not templatable configuration and is **unknown, not priced**. It covers the programme agreement, the host-share terms, a policy overlay, 170(f)(18) acknowledgment documents and board approval. It is borne by the host, the institution or both.

### 3.2 Results: programme-owner break-even (base v, base F)

| Hosting model | B = $50k | B = $133k | B = $250k |
|---|---|---|---|
| Hosted on an existing sponsor | 20-189 accounts ($1.0-9.5M) | 6-19 ($0.8-2.5M) | 3-8 ($0.75-2.0M) |
| Existing charity, own programme | 50-472 ($2.5-23.6M) | 15-46 ($2.0-6.1M) | 8-20 ($2.0-5.0M) |
| Newly formed sponsor | 179-1,699 ($9-85M) | 52-164 ($6.9-21.8M) | 26-72 ($6.5-18M) |

Each cell spans fees of 1.5% (the low figure) to 0.6% (the high figure).

**Reading (P3-CLM-CD011).**
- **Shared technology matters most where the institution would otherwise need its own sponsor-level apparatus.** Hosting on an existing sponsor removes 80-95% of F. A university, hospital, credit-union or bank programme of a few dozen accounts covers its own operating cost at fees of 1% or more, provided balances are $130k or above.
- **A newly formed sponsor stays uneconomic below roughly $7-20M of DAF assets.** This supports Phase II's finding that new sponsor creation (SEG-011) is "too small", and it argues against offering "sponsor-in-a-box" formation as a product.
- **Balance dominates.** At $50k average balances and 0.6% fees, even hosted programmes need about 190 accounts. Phase II already showed that sub-$10k accounts lose money at any flat bps (SEG-004).

### 3.3 Does this make small programmes viable *for Echelon*?

Not on its own (P3-CLM-CD012). Vendor-side economics per programme:

| Item | Range | Basis |
|---|---|---|
| Licence revenue per small programme | $2k-25k a year | 24-60 accounts × $40-120, or a minimum fee up to $12.5k-25k (CLM-038 benchmark); ASSUMPTION |
| Direct CAC per sponsor | $60k-250k | PAR-023 (untested, CLM-026) |
| Onboarding, templated on a shared tenant | $5k-12k | 10-25% of the Phase II $48k; ASSUMPTION (P3-ASM-CD007) |
| Programmes needed to cover vendor fixed cost | ≈ 20-30 at $0.3M fixed; ≈ 60-110 at $0.9M; ≈ 120-225 at $1.8M | Vendor fixed ÷ per-programme contribution of $8k-15k. $1.8M is the Phase II MD-6 vendor fixed cost (PAR-022 ×0.8-1.5); lower fixed costs are Track A states (report 02) |

The comparison: about 6.5 sponsors are newly formed each year and about 35 enter the panel (SEG-011). 165-174 institutional sponsors exist in total (P3-SRC-CD017). A portfolio of 60-225 *new* small programmes is therefore an aggressive target, achievable only if:
- each programme is acquired for less than about one year of its licence revenue (P3-HYP-CD005), and
- the vendor's fixed cost falls towards the Track A shared-infrastructure states.

**Small programmes are viable as a portfolio carried by a channel, not as individually sold customers.**

## 4. Qualified prospect universe (public organizational data)

Counts below are organizations or entities, not buyers. "DAF signal" means the EIN appears in the DAFRC FY2021-24 sponsor panel (SRC-013) or in the repository's non-DAFRC 990 harvest of Schedule D DAF values and Part IV line 6 "yes" flags (P3-SRC-CD019). BMF assets are total assets on the latest return (P3-SRC-CD003; file dated 2026-11-09).

### 4.1 Charitable institutions (can sponsor)

| Category (BMF public charities) | ≥ $10M assets | of which DAF signal | ≥ $100M assets | of which DAF signal | Source / date |
|---|---|---|---|---|---|
| Community foundations (NTEE T31) | 712 | 616 (87%) | 267 | 262 (98%) | BMF 2026-11-09; CoF "more than 900 CFs" (undated) and DAFRC 804 CFs reporting DAFs FY2024 |
| Public foundations (T30) | 413 | 84 | 77 | 32 | BMF |
| Federated giving, including United Ways (T70) | 274 | 90 | 68 | 40 | BMF |
| Higher-education institutions (B40-B43, B50) | 1,394 | 71 | 738 | 50 | BMF |
| Education support and fundraising, including university foundations (B11, B12) | 1,253 | 38 | 380 | 26 | BMF |
| Foundations for government colleges and universities (foundation code 13; overlaps B-codes) | 511 | 24 | 167 | 11 | BMF |
| Hospitals (E20-E22, E24) | 2,613 | 18 | 1,459 | 11 | BMF |
| Health support and fundraising, including hospital foundations (E11, E12) | 847 | 22 | 263 | 10 | BMF |
| Religion support and fundraising (X11, X12) | 148 | 34 | 27 | 16 | BMF |
| **Education and health union (de-duplicated by EIN; foundation codes 12/13 or the NTEE codes above)** | **7,233** | **159** | **3,056** | **99** | BMF |

**Qualified core (INFERENCE).** The most plausible new-programme adopters are education and health *foundations* (B11/B12, foundation code 13, E11/E12) with at least $100M of assets and no DAF signal. They number roughly **600-800** after overlap and after excluding operating hospitals, whose assets are operating plant rather than gift funds. **This is a count of organizations, not of demand** (Revision 2, P3-CHL-REV1011). The observed rate of new institutional programme launches in FY2021-24 has not been measured (P3-GAP-CD010), and it is the figure that matters.
- These organizations already run gift-acceptance, planned-giving and endowment operations, which supply the expertise and custody the matrix lists.
- Existing institutional programmes show the use case: host-share rules (12 of 18 pages, P3-SRC-CD017) and complex-asset intake (GW, P3-SRC-CD008).
- **No public evidence shows that these institutions want a DAF programme.** Their institutional segment's DAF assets grew 11% over FY2021-24 against 38% for the market, and its share is falling (1.38% to 1.11%; P3-CLM-CD004).

### 4.2 Financial and commercial institutions (cannot sponsor; need a partner sponsor)

| Category | Count | Band detail | Source and date | Limitation |
|---|---|---|---|---|
| FDIC-insured institutions | 4,204 active (QBP Q2 2026: 4,238) | 3,153 under $1bn; 890 at $1-10bn; 128 at $10-100bn; 33 at $100bn or more. 1,006 report fiduciary assets; 251 hold $1-100bn of fiduciary assets; 1,038 hold full trust powers | FDIC BankFind API, REPDTE 2025-12-31, queried 2026-11-26 (SRC-048; SEG-003) | Fiduciary assets are not DAF assets. Banks with a DAF programme are not identifiable from call data (P3-GAP-CD002) |
| Federally insured credit unions | 4,214 | 748 above $500M | NCUA Q2 2026 summary (SRC-049) | No finer bands retrieved this pass (P3-GAP-CD003) |
| SEC-registered investment advisers | 16,544 (YE2025) | About 67% (≈11,100) under $1bn AUM; median $446.9M | IAA/COMPLY snapshot 2026 (P3-SRC-CD005; SRC-050) | Bracket table not retrieved; 21,669 including exempt reporting advisers (2024) |
| National trust banks | ~60 | n/a | OCC rule, Federal Register 2026-03-02 (SRC-052) | |
| State-chartered trust companies | UNKNOWN nationally | CO 8 (YE2024); MA 14 + 2 limited purpose (2026); CA 7 (YE2024) | State regulators (P3-SRC-CD006) | No national count found (P3-GAP-CD004) |
| Family offices | 3,180 single-family offices in North America (2024) | n/a | Deloitte via SEG-008 | Cannot sponsor; not a programme buyer |
| Corporate foundations | 3,601-3,859 | n/a | SEG-009 | Directory figures |
| CU league and CUSO foundations offering institutional DAFs | 4 or more found | n/a | SEG-014; SRC-057 | Search-based |

### 4.3 Named institutions with a relevant public fact

Named institutions appear only where a public document shows a DAF-relevant fact; see [institutional-prospects.csv](data/fragments/CD/institutional-prospects.csv). The facts fall into four groups:
- **Banks with partner sponsors:** Regions (RCF), Wells Fargo (NPT), First Citizens and KeyBank (Ren and RCF tenants), BofA (own affiliate).
- **Distributors:** SEI (TIFIN Give for banks and trust companies).
- **University programmes on partner sponsors:**
  - Ohio Wesleyan with The Columbus Foundation;
  - George Washington and Michigan State with BNY Mellon CGF. That sponsor voted to end its DAF programme in December 2024 per repository records, and the programmes' current status was not checked (P3-GAP-CD005).
- **League-foundation credit-union DAFs:** Allegacy FCU with the Carolinas CU Foundation; WeStreet CU with the Cornerstone Foundation.

**The BNY Mellon CGF case cuts both ways.** It is the only public instance found of hosted institution programmes losing their host. That is a buying trigger for a replacement host, and a warning that programme owners depend on the sponsor's strategy.

## 5. Which institution types would most likely adopt a new DAF offering without switching providers?

These are ranked on public evidence; all are hypotheses for V-1/V-6 validation.

1. **Education and health foundations without a programme (P3-SEG-CD001/CD002).**
   - **For:** a greenfield adoption, not a switch, with the largest count of qualified organizations (about 600-800). They are 501(c)(3) organizations that can sponsor or be hosted. Procurement is moderate (3), and existing gift operations supply custody and expertise. Peer programmes publish host-share rules that Unbound's configuration could express.
   - **Against:** the institutional segment is shrinking relative to the market, and a free alternative exists (accepting grants from national DAFs).
2. **Institutions hosted on an existing community or national sponsor (P3-SEG-CD017, "host sponsors").**
   - **For:** the host adds programmes as a new line rather than replacing its core system. Ohio Wesleyan with The Columbus Foundation shows the arrangement exists. The BNY CGF exit shows hosted programmes can need a new home.
   - **Against:** the host must accept a second system or migrate; no public evidence that hosts want a separate platform for hosted programmes (P3-HYP-CD002).
3. **CU league and CUSO foundations (SEG-014; P3-SEG-CD015).**
   - **For:** already 501(c)(3) sponsors running institutional DAFs with apparently manual operations (INFERENCE). One contract reaches many credit unions.
   - **Against:** no member DAF demand (CLM-024).
4. **Faith foundations and denominational networks (SEG-010; affinity G02, G07, G09).** They are mobile (WaterStone), and federated structures can replicate a programme. Most large ones already sponsor, so for those it is a switch, not greenfield.
5. **Community banks and trust companies through a host sponsor.** They cannot sponsor, and TPRM 5/5 makes the route slow. It is realistic only behind a sponsor or distributor (SEG-003, SEG-007). The governing guidance is in flux. On 2026-09-15 the OCC, Federal Reserve, FDIC and NCUA proposed new interagency third-party risk management guidance (91 FR 58536; comments closed 2026-11-16). It would rescind and replace the June 2023 interagency guidance (88 FR 37920) and emphasizes tailoring to the bank's size and the risk of each relationship (P3-SRC-CD021). Whether the final text eases or tightens vendor review for a small DAF-technology supplier is open (P3-GAP-CD012).

**Not recommended as targets:**
- RIAs and custodians: price-compressed and already served (CLM-039).
- Employers and employee-benefit platforms: crowded (P3-CLM-CD014).
- Fintechs: they need their own charity, and the reputational risk is high.
- Family offices: cannot sponsor.
- Accounting networks: no evidence either way (P3-GAP-CD007).
- New sponsor formation: uneconomic below about $7-20M (§3).

## 6. Regulatory context relevant to new programmes

- **4966 regulations are still proposed.** The rules at 88 FR 77922 remain proposed as of the latest sources found (Council on Foundations 2026-05-08; Treasury and IRS 2026-27 priority guidance plan still lists 4966 guidance, P3-SRC-CD014). Two open points affect new programmes:
  - the treatment of personal investment advisers as donor-advisors, which affects bank, RIA and trust programmes where the institution manages DAF assets;
  - fund-definition boundaries, which affect "organization-advised" and scholarship-type funds at universities.
- **OBBBA changes from 2026 (P3-SRC-CD015; secondary sources).** The new non-itemizer deduction excludes gifts to DAFs, and a 0.5% of AGI floor applies to itemizers. Direction of effect on demand is unmeasured. Bunching may favour DAFs among itemizers, while mass-market DAF appeal may weaken.
- **Hosted programme roles.** Where an institution's programme sits on a partner sponsor, the sponsor carries the 4966/4967 responsibility, and the institution's role is marketing and possibly investment management. Unbound's sponsor-segregation and sponsor-reserved approval controls (V-9) map onto that split; this is INFERENCE and needs counsel review.
- **Charitable-solicitation registration (Revision 2, P3-CHL-REV3025).** Hosted, white-label or channel programmes that pay a partner, institution or Echelon a share linked to contributions may trigger state registration as a professional fundraiser, fundraising counsel or commercial co-venturer. This has not been analysed. Until counsel answers it per channel model, exclude contribution-linked shares from proposed terms and price on accounts or flat fees (P3-GAP-CD013).

## 7. Limitations

- **BMF asset sizes are approximations.** Total assets on the latest return; hospital and university figures are operating assets.
- **NTEE coding is imperfect.**
- **"No DAF signal" is not proof that no DAF programme exists.** Programmes hosted elsewhere leave no trace in the host institution's own filings.
- **All cost inputs are ranges, not measurements.** The minimum-viable-programme grid has no time study (PAR-018/019) and should be ported to the Phase III F# model (agent MOD).
- **Light sourcing for some figures.** The Council on Foundations, the IAA snapshot and several programme pages were read through search summaries only.
- **No institution was contacted.**
