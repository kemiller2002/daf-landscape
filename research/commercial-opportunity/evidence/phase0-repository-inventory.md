# Phase 0 research inventory: commercial opportunity for an independent DAF expert firm (Echelon Foundry)

**Date:** 2026-11-20. **Source:** the `daf-landscape` repository only (no web research). The companion fact table is `inventory.csv` in this folder (INV001–INV120). Paths below are relative to the repository root.

**How to read this.** Where a document ends in a "Validation corrections … — governing" or "Red-team corrections" section, the corrected figure is used here. "[V wave N]" means independently validated in that wave. "[I]" is the repo's own inference, "[S]" a scenario figure. The repo is **public-source only**: no interviews, contracts, RFPs, pricing quotes or customer data were obtained (`research/mission-2026-11-14/FINAL-STATUS.md`, "Research coverage and limitations"). So **nothing in the repo is direct evidence of willingness to pay.** What it does provide is evidence of *ability* to pay (budgets, vendor spend), *triggers* (migrations, deals, regulation) and *gaps* that independent expertise could fill.

The repo already has a commercial-opportunity agenda (`research/commercial-opportunity/2026-11-20-research-agenda.md`, "Research hypotheses, not validated demand"). It lists 8 buyer segments, 7 offers to validate and the mandatory questions (pain, budget holder, triggers, alternatives, procurement, WTP, named prospects, disconfirming evidence). None of those questions has been answered yet. This inventory is the baseline for them.

---

## (a) What is already known, by buyer segment

### A1. Sponsors: national (independent, bank- and broker-affiliated)

**Market shape.**
- FY2024 (DAFRC): $327.87bn of assets, $90.57bn contributed, $64.60bn granted, 1,512 sponsors. Repo-corrected assets are $323.27bn [V] (INV001).
- The top 50 sponsors hold 85.5% of assets. CR3 is 45.5% and HHI 830. Fidelity holds 20.5–21.7% every year (INV003).
- So the buyer universe that matters for budget is **under 50 organisations**.

**Captive economics.** About 39% of assets sit at three affiliate-administered nationals (Fidelity, DAFgiving360, Vanguard) [RT 2B] (INV004).
- Fidelity Charitable passes its admin fee to FMR one for one: $139.7m in FY2024, against $0 of IT on its own 990 [V 38B] (INV005).
- 10 of 12 affiliated-commercial sponsors carry no paid executive on their own 990 [V 28] (INV013).
- **Buying authority for technology and operations sits at the parent firm (FMR, Schwab, Vanguard, Morgan Stanley, Goldman), not at the charity.**

**Cost base (ability to pay).**
- DAF-allocated operating cost is $2.14bn (67 bps). Standard nationals spend 32 bps; community foundations spend 127–177 bps [V 5] (INV007).
- Cost per grant: Fidelity $68, DAFgiving360 $55, Vanguard Charitable $134, NPT $419, GS PF $574 [V 5] (INV006).
- Audited fee margins are thin at pass-through sponsors:
  - RCF: +0.8% on a $19.62m fee.
  - Fidelity: other costs come to −15.7% of the fee.
  - NCF: the fee covers about 38% of G&A plus fundraising.
  - JCF is the exception at +32.6% [V 38B] (INV009–INV010).
- Independent nationals' non-DAF reserves cover a median 2.2 months of operating cost, against 29.4 months at bank- or broker-affiliated sponsors [V 29] (INV012).
- Marketing budgets are tiny outside Schwab ($20.3m). Independent nationals spend $3.1m in total [V 28, 40C] (INV014).

**Technology posture.**
- Vanguard Charitable has a $4.24m related-party fee. Its claimed move to Give Interactive is not visible in its FY2026 audit (INV015).
- NPT runs about 13 bank and wealth white-label programs (JPM, UBS, BMO, Glenmede and others) on one Ren GivingPoint build. The Ren fee is undisclosed and probably sits in a $5.87m IT line [V 12; hosting evidence only] (INV016, INV071).
- No sponsor publishes turnaround, exception or reviewer-time metrics. Only 5 of 28 turnaround claims are measured [V 21] (INV018).
- Sponsors post few AI roles: 2 of 15 sponsor postings name AI, and Fidelity Charitable's 11 roles name it 0 times [V 24B/33B] (INV022).
- None of 13 vendors publishes a scoped SOC report [V 5] (INV028).

**Triggers.**
- **Regulation:** the §4966 rules are still proposed. The docket holds 249 submissions, and the 2026–27 Priority Guidance Plan has an item on §§4966/6033 (INV023).
- **Discretion controversy:** the SPLC holds and the 16-AG letter of 2026-05-21 (INV024).
- **Portability:** no outbound-transfer policies are published, and AEF's migration kept only two years of history (INV026).
- **Contract barriers:** six of the top 20 sponsors restrict automated or third-party access (INV025).

### A2. Sponsors: mid-size and community foundations (803 CFs; 1,240 sponsors under $50m)

**Installed base** [V 9] (INV029). The repo's CF vendor map:

| Vendor | CFs | Share of CF DAF assets |
|---|---|---|
| Foundant CommunitySuite | 361 | 32.7% |
| Salesforce | 19 | 23.7% |
| GiftingNetwork | 2 | 11.5% |
| Ren/Stellar iPhi | 22 | 5.9% |
| akoyaGO | 48 | 3.2% |

- About 43% of mapped assets sit behind portal-only front ends, and the ledgers behind them are mostly unknown (INV030).

**Budgets.** These are the most directly commercially relevant numbers in the repo.
- Median CF IT spend by DAF assets: $17k under $10m; $55k at $10–50m; $116k at $50–250m; $468k at $250m–1bn; $1.28m at $1–10bn [V 5] (INV031).
- **Vendor fees actually paid** (Form 990 Part VII-B; only contracts over $100k are disclosed):
  - Ren/Stellar at $118k–$416k a year: Cleveland, Des Moines, Green Bay, Acadiana (INV032).
  - Foundant at $159k–$345k: Columbus, Atlanta, Winston-Salem, Denver (INV033).
  - Give Interactive at FFTC, $654.5k (TY2023), and Kalamazoo, $416.9k (FY2025) (INV034).
  - Source: `data/mission-2026-11-14/form990-contractors-harvest-full.csv`. The per-vendor extraction was done for this inventory; the harvest itself was validated in wave 5.
- **Long tail:**
  - A tail CF's median operating cost is $630k with 5 staff (INV039).
  - The realised tail-CF DAF fee pool is about $49m a year, and the whole tail $49–74m (INV040).
  - Only 2.2% of tail sponsors disclose any DAF-relevant contractor (INV042).
  - An AI project's fixed cost of $150–750k is 1.3–45× the median IT line at CFs under $250m [S] (INV043).

**Pain.**
- Top-100 CF admin fees run 1.7–4.7× the nationals' (INV037).
- CF cost per DAF dollar rose 21% in nominal terms over FY2021–24 (INV044).
- Most CFs pay grants by their own ACH, and no rail dominates (INV046).

**Triggers.** Ren iPhi lost 6 of 57 sponsors in 2023–Nov 2026, 5 of 28 among CFs. All six dated CF portal switches ended on Foundant. NPact's DonorCentral was sunset in October 2026 (INV035, INV036, INV086).

**Disconfirming.**
- CF consolidation is near zero (INV045).
- The tail fee premium is no longer established; the tail-CF median is 137.5 bps on n = 20 (INV038).
- The repo advises against a standalone long-tail business [I] (INV041).

### A3. Sponsors: faith and single-issue

- **NCF** paid Ren $2.50m in TY2024, up from $1.20m in TY2022. Its fee covers well under half of its G&A plus fundraising (INV047).
- **Faith sponsors already buy outside advisory services.**
  - Christian Community Foundation paid PhilanthroCorp $623k and Excellence in Giving $568k (TY2024).
  - AEF paid Excellence in Giving $182k (INV048, unvalidated rows).
- The Signatry's trust owns 99% of Give Interactive, a vendor to other sponsors including Vanguard Charitable. That is a conflict-of-interest diligence topic (INV049).
- Peterson v. WaterStone is pending (INV050).
- **Jewish federations and JCF** pay Ren $156k–$501k a year. JCF has the only material audited fee surplus, +32.6% (INV052).
- **Universities and hospitals** hold only $3.59bn, run a median of 5 DAFs and pay out a median 6.6%. They are weak program buyers and are better treated as recipients (INV053).
- Affinity commercial opportunity tests already drafted (12 hypotheses: church complex gifts, endowment admin, vehicle-neutral decision tools): `data/affinity-daf-commercial-opportunity-tests-2026.csv` (unvalidated, 2026-11-11).

### A4. Wealth managers, RIAs, broker-dealers, banks, trust companies, family offices

**Structure.**
- Most wealth-firm DAFs are white-labels:
  - about 11 firms on RCF sponsorship with Ren technology (INV054);
  - banks on NPT with Ren (INV071);
  - BofA with its private bank as administrator and Ren technology (INV069);
  - Goldman on Ren/Stellar software, with grant administration outsourced to CAF America at $876k (INV070).
- RCF paid Ren $7.51m in 2020 and $19.23m in 2024, about 26.5% CAGR, at 98% of the fee base [V audited] (INV055).
- MS GIFT paid RenPSG $14.93m [V 3] (INV057).
- Stifel's Ren spend rose from $498k to $801k (FY2024 to FY2025) (INV058).

**Economics touching advisers.**
- Only MS GIFT, DAFgiving360 and TIFIN Give cap adviser fees, at 1.00%. Observed RIA brochures charge 0–2% (INV060).
- All-in cost at a $250k DAF runs from 0.26% to 2.13% (INV061).
- External-adviser minimums run from $25k (AEF) to $5m (SVCF, GS IMAP) (INV072).

**Adviser demand signals.** All of these come from sponsor-funded surveys.
- 35% of advisers recommend DAFs most of the time or always (DAFRC 2026, funded by DAFgiving360) (INV062).
- 86% of RIAs with more than $250m AUM offer charitable planning (INV063).
- 73% of advisers have taken philanthropy education (INV063).
- 77% of DAFgiving360 assets are adviser-associated (unvalidated) (INV064).

**Triggers.**
- SEI is running two stacks (INV065).
- Vanguard is acquiring Altruist, which uses Endaoment, not Vanguard Charitable (INV066).
- LPL must rationalise the Commonwealth program after the merger (INV067).
- Edward Jones's private DAF stack is unidentified (INV068).
- TIAA launched Charityvest/Foundation Source (INV065).
- **Common PE ownership has not forced captive choices**, so each platform makes a real vendor decision (INV097).

**Unproven core value proposition.** "DAFs improve adviser retention" is an untested hypothesis. The retention study (Q-B13) is blocked (INV073).

**Pave** is the only fintech already studied as an entrant, and every economic figure in that study is hypothetical (INV074).

### A5. Technology vendors

| Vendor | Key commercial facts (inventory IDs) |
|---|---|
| **Ren** (incl. DonorFirstX, Stellar/iPhi) | Bain/Valeas majority (2023); Great Hill (2025). Revenue not public; named 990 receipts $44.98m from 18 sponsors, 85.8% from three. Confirmed-link floor 32.2% of assets; its >60% claim unsupported. SOC 2 type statements conflict. iPhi attrition 10.5%. Hiring 6 roles, 3 AI (INV055–INV059, INV077, INV078, INV035) |
| **Foundation Source** (Vennfi, Giving Place, PG Calc) | GTCR since 2023; four add-ons; Audax first-lien loan at par; exit or recap 2027–29 [I]. Powers Charityvest, TIAA, OneGive and Temple. Charityvest's president is paid by FS (INV076, INV100) |
| **TIFIN Give / GiveClear** | $4.67m discretionary AUM (ADV, 2025); GiveClear self-reports $372m. Most announcements, least delivery evidence. Seen as the most separable asset for a buyer (INV079, INV080) |
| **Chariot** | $11m Series A; DAFpay at a 2.9% default; Disbursements used by TIFIN, Daffy, Charityvest and 7 CFs. Hiring agentic engineers (INV081, INV082) |
| **Daffy** | $2bn claimed against $334m on its FY2024 990; flat fees; MCP server can move money (INV083) |
| **Give Interactive** | Owned by The Signatry's trust. $23.90bn of first-party-evidenced client assets ($36.74bn on DNS). FFTC and Kalamazoo payments (INV034, INV084) |
| **Foundant** | Count leader in CFs (361; 282 of 351 identified tail CFs). Self-reports 700+ clients and 99% renewal (INV087) |
| **Blackbaud** | BILL named to succeed REPAY; AI governance hiring; universities pay $118k–691k a year (INV085) |
| **NPact** (FIMS/DonorCentral) | About $6.4m acquisition (2022); DonorCentral sunset; owner unconfirmed (INV086) |
| **Givinga** | Account unit undefined, averaging $1.37 per account (INV088) |
| **Benevity/AOGF; Bonterra** | AOGF paid Benevity $54.45m. Bonterra has EBITDA above $100m and is acquisitive (INV089, INV090) |
| **Endaoment** | Sponsor-of-record API; a nonprofit with no equity (INV091) |

**Cross-vendor facts.**
- None of 30 AI products passes the repo's RED test (INV092).
- Executed contracts are unseen (INV093).
- **No analyst firm covers DAF platforms** (INV094).
- **Sponsors' vendor-selection criteria are unknown**: queue item P-ANL-07 is blocked (INV095).

### A6. Investors, PE, VC and acquirers

- 89 firms have been scored. Revealed interest is concentrated in Bain, Valeas and Great Hill (Ren), GTCR (Foundation Source), and wealth platforms (INV096).
- Portfolio adjacencies are mapped across about 60 companies (INV097).
- **No DAF revenue multiple is computable.** The only priced DAF-rail deal is The Giving Block, and it was impaired (INV098).
- PE enters at the buyout of profitable administrators, not early stage [I] (INV099).
- Exit windows open in 2026–29 for Benevity, Bonterra, Foundation Source, Orion and Ren [I] (INV100).
- Failure and cohort data are ready-made diligence content (INV101, INV102).
- The repo's own entrant economics: a $120k-a-year operating layer needs 76k–369k grants a year per customer [RT] (INV103).

### A7. Banks and new entrants

- Covered in A4 and A5.
- The new-entrant evidence is the 2021–26 cohort: 18 entrants, none documented as shut down (INV102). Altruist, SEI, TIAA and GoFundMe became programs or sponsors in 2025–26 (INV065, INV066).

### A8. Nonprofits and universities

- Sponsors charge nonprofits $0 to receive a grant. Intermediaries charge 1.5–2.99%, about $32 per $1,000 through DAFpay (INV104).
- DAFs are about 13% of giving at 54 large nonprofits (a vendor-run study) and 22% or more of major-gift revenue. The repo's own floor is 8.4% of recipients' contributions (INV105).
- Only 41.2% of top recipients show any DAF option on their donate page (INV106).
- Donor contact data is withheld by default at most surveyed sponsors (INV107).
- Pain is real, but nonprofits are not the payer and budgets are unknown.

### A9. Education providers

- AFP's DAF education is funded by Fidelity Charitable. AFP issued a DAF Curriculum Design RFP in November 2024, the one documented procurement of DAF expertise in the repo (INV108).
- **DAFCP** costs $1,495 and has no adoption data. Its lineage, faculty and forum are sponsor-aligned. It omits fees, payout, portability and technology. The issuer has run deficits [pending validation] (INV109–INV111).
- 11 adviser curricula omit fees, payout distribution, portability and inactivity [V 22] (INV112).

### A10. Adjacent

- **Third-party administration:** Total Administrative Services ($15.4m), Charitable Solutions ($4.43m), FrontStream, CAF America and Excellence in Giving (INV075, INV048).
- **Complex-asset intake:** Dechomai, and Fidelity's $2.6bn of non-public assets (INV113).
- **California platform law** reaches DAF technology vendors (INV114).
- **DAF news attention is rising** (INV115).

---

## (b) Existing strategic conclusions about opportunities for entrants and consultants

| Conclusion | Where | Validation status |
|---|---|---|
| Do not build a sponsor, custody, rails, charity master data or a full system of record. Partner with Endaoment/Daffy APIs, Chariot and IRS data | `DAF-INDUSTRY-REPORT-2026-11.md` §8; `strategic-synthesis.md` §0 D | Red-team corrected (wave 2A) |
| The cheapest probe is an AI operating layer with deterministic rules. It is a **conditional probe, not a recommendation**: about 42 customers for $5m ARR, and most CFs lack the grant volume | report §8 | RT 2A; scenario |
| Redesign or conventional automation beats AI-on-workflow. AI fits noncash intake and non-standard due diligence. The AI value pool is thin ($445k at a large national) | `ai-economics-v2-observed-costs.md`; `gap19-ai-calibration.md` | Validated 31A; assumption-driven |
| Avoid a standalone long-tail business and credential-based integrations. Do not wait for an open rail. Never hold donor funds | `strategic-synthesis.md` §0 D | Validated facts; [I] conclusion |
| Value shifts to distribution access, nonprofit identity and remittance data, measured latency, dated eligibility evidence and local knowledge | synthesis §0 E | [I] on validated facts |
| Incumbents are vulnerable through shared single points of failure (RCF–Ren), the CF cost gap, legacy attrition, unproven challenger claims and the assurance gap | synthesis §0 C | Validated facts |
| Common PE ownership has not produced captive distribution. Wealth platforms partner rather than buy. The likely next deals are an FS recap, more PE layering at Ren, platforms buying white-label stacks, and nonprofit-software consolidators buying DAF payments | `firms-interested-in-daf-organizations.md` §1.6, §8.2 | Facts validated (wave 4); deals [I, M–L] |
| Grant vetting is **not** proven as the best first product. Investigate engagement and end-to-end exceptions first (Clarity posture: Experimental) | `decision-intelligence-pilot-2026-11-11.md` | Unvalidated analyst pilot |
| DAFCP: enrol one person as a research instrument. Publish complementary operations and technology education and an evidence-based platform comparison. Do not build a competing certification | `dafcp-investigation-2026-11-20/01-…md`; `10-strategic-scenarios…md` | **Pending validation** |
| Pave: a partnership-led RIA entry. Do not launch a sponsor | `pave-finance-daf-market-entry-study-2026-11-11.md` | Unvalidated (2026-11-11) |
| Affinity B2B opportunity tests OP01–OP12 (church complex gifts, endowment administration, vehicle-neutral decision interface, consent-aware grant acceptance) | `data/affinity-daf-commercial-opportunity-tests-2026.csv` | Unvalidated hypotheses |
| No analyst coverage, so the repo's own Evidence Quadrants (43 providers, two blind scorers) are the only independent vendor positioning | report §10; `analyst-and-education-landscape.md` | Internal-demonstration (EDF) |
| Who resists redesign: holders of asset-based fees. Who benefits: nonprofits, small donors and non-AUM challengers | `industry-incentives-structural-analysis.md` §5 | Inference; RT corrected |

**Implication.** The repo already argues, directionally, for **independent evidence, benchmarking, assurance and redesign advice** over a new platform. But it has **never tested whether anyone will pay for that.**

---

## (c) Contradictions, unresolved hypotheses and outdated claims

**Superseded or contradicted (do not reuse):**
- Early 11-11/11-12 files say there is no Ren evidence at Goldman Sachs (`goldman-sachs-two-daf-programs-2026-11-11.md`) and none at NPT (`national-philanthropic-trust-financial-technology-audit-2026-11-11.md`). Both are **superseded**:
  - Goldman uses Ren/Stellar [V wave 3].
  - NPT GivingPoint runs on a Ren build, on hosting evidence only [V wave 12].
- The BofA 10-K evidence of Ren is **contradicted**. Only the portal shows Ren.
- "Fidelity electronic-only by July 2026" is **not confirmed**. 67% of grants go by EFT, and checks continue.
- CR3 of 58% (`vendor-dependency-concentration.md` §1.5) is a period mismatch, replaced by 45.5%. The "about 34% left for others" figure becomes about 48% [RT 2B].
- The 990 balance-sheet proxy as an operating margin is **retired** [V 40C] (INV011).
- The tail-CF fee median of 150 bps (n = 6) is superseded by 137.5 bps (n = 20). The tail price premium is no longer established [V 44B].
- The AI-economics v1 result "AI ranks last in all 16 processes" does not survive v2. The large-national AI pool fell from $1.18m to $445k after calibration.
- Startup failure patterns from the purposive-50 (acquisition as the modal exit) do not hold for the 2021–26 cohort.
- "61% of clients start the philanthropy conversation" is 2018 TPI data, not 2026 evidence [V 19].
- Give Interactive "lost five CF tenants" is corrected to three, and its crt.sh-only claims are downgraded to leads.

**Open contradictions to resolve:**
- Kalamazoo CF paid Give Interactive $416,932 in its FY2025 return, yet the certificate evidence lists Kalamazoo as a lost tenant (INV034). Not yet re-read.
- Ren's SOC 2 statements alternate between Type 1 and Type 2.
- Ren's share claims (>60%, about half, "$200bn") against the 32.2% confirmed floor. The $200bn includes non-DAF assets.
- Vanguard Charitable's "Give Interactive recordkeeping" claim is absent from its FY2026 audit.
- Daffy's $2bn claim (2026) against $334m (FY2024 990), and Charityvest's 2025 self-reported figures against its 990 series.
- RCF's donor-information default: 2.4% under Ren's October 2026 guide, against "Fund Name Only" in RCF's 2023–24 guide.

**Unresolved hypotheses with commercial weight:**
- DAFs improve adviser retention (Q-B13, blocked).
- Executed contracts grant API, export or transition rights (Q-N04 / P-CON-01 / P-QA1-06, blocked).
- Measured exception rates and handling time (Q-N03, blocked).
- Edward Jones private DAF stack; Give Interactive's role at CCT; NPact's owner; NPT's payment to Ren; whether the SPLC holds persisted.
- LPL's choice for the Commonwealth program; Vanguard's DAF policy after Altruist (P-BUY-01, P-BUY-03).

**Stale or dated evidence to flag:**
- The Morningstar Vanguard fee table (2023).
- The Chronicle CF fee survey (2009).
- The Kitces DAF tactics piece (2015).
- Datos Insights (2021), the last analyst report.
- The BofA/Lilly penetration figure (2020 data).
- The TIFIN Give ADV (March 2025).
- Goldman circulars (2008–2017).
- DAFgiving360 2024 Program Policies (check-only).
- The 2018 TPI conversation data.
- The pre-mission 2026-11-11/12 top-level files are **first-pass and unvalidated**. Mission-era validated files supersede them where they overlap.

---

## (d) Clarity and EDF applications already done

Frameworks are pinned to Clarity `8cd4801` and EDF v0.3 `41fea6f` (`research/mission-2026-11-14/clarity-edf-application-guide.md`).

1. **Decision Intelligence architecture and pilot** (2026-11-11). Three result cards:
   - grant vetting as first product: posture Experimental;
   - 3.59m accounts as software TAM: rejected;
   - Ren against Foundation Source profitability: "not justified".

   Files: `decision-intelligence-architecture-2026.md`, `decision-intelligence-pilot-2026-11-11.md`, `data/decision-intelligence-*.csv/json`. Includes 20 unexecuted adversarial regression cases.
2. **Clarity report-assumption audit**: 32 reviews of external and internal claims, plus 10 conclusion cards (`clarity-report-assumption-audit-2026-11-11.md`, `data/clarity-*.csv`).
3. **Industry incentives**: EDF outcomes A–G, with the structural-against-habit test (`industry-incentives-structural-analysis.md`, `data/mission-2026-11-14/incentive-map.csv`).
4. **gap19 Clarity/EDF new findings** [V 31B] (`gap19-clarity-edf-new-findings.md`):
   - G12-1: CF cost gap, mixed and leaning structural;
   - G12-2: donor-data withholding, leaning habit;
   - G12-3: no open grant standard, a coordination gap;
   - G12-4: Fidelity's tracking gap matches its fee.
5. **Evidence Quadrants**: five areas, 43 providers, two blind scorers plus adjudication; internal-demonstration status (report §10; `quadrant-*.md`).
6. **Strategic synthesis A–G**: every claim carries an EDF claim state and a Clarity posture (`strategic-synthesis.md` §0).
7. **Topic-level Clarity checks**:
   - affinity: 18 checks;
   - historical lifecycle: 18;
   - technology audit: 16 falsification checks;
   - Pave and fund-manager hypothesis maps;
   - wealth-continuity counterhypotheses.
8. **DAFCP Clarity and EDF assessments** (`dafcp-investigation-2026-11-20/08-clarity-assessment.md`, `09-edf-assessment.md`). Pending validation.
9. **Gap**: no Clarity or EDF result yet addresses **Echelon's own commercial questions** (which segment pays, for what, at what price).

---

## (e) Explicit gaps for the commercial questions

**Willingness to pay and pricing**
1. No interview, survey, RFP response, quote or signed engagement exists for any segment. The repo's own guardrail is that "public research is not proof of willingness to pay".
2. There is no price evidence for consulting, research subscriptions or technology assessments in DAF. The one procurement signal is AFP's 2024 curriculum RFP, and its value is unknown.
3. Competing consultants and advisory firms are not mapped:
   - Excellence in Giving, PhilanthroCorp, Daylight Advisors and Tech Impact appear only incidentally;
   - no list of philanthropy-tech consultancies, Big-4 practices or CF consultants exists;
   - no pricing for any of them.

**Budgets and ability to pay**

4. Vendor spend below $100k is invisible in Part VII-B, which hides most CF and tail spend. Only 2.2% of tail sponsors list any DAF contractor.
5. Affiliated nationals' technology budgets sit at FMR, Schwab and Vanguard and are not public. Process-level cost at nationals is blocked (P-COST-01; P-AIV2-05).
6. Bank and broker program budgets (Edward Jones, LPL, UBS, Ameriprise, RBC) are unknown. Only the RCF-level payment is known.
7. PE deal-team diligence budgets and how they buy (commercial due-diligence vendors used) are unknown.
8. Nonprofit and university advancement budgets for DAF tools or training are unknown. So are wealth-management budgets for philanthropy tooling.

**Procurement and buyer roles**

9. Sponsor vendor-selection criteria and RFP processes are unknown (P-ANL-07, blocked). No named budget holder exists: CTO, COO, CFO, board investment or technology committee, or parent-firm IT.
10. There is no map of decision-makers at the top 50 sponsors or at the roughly 11 RCF wealth programs and 13 NPT white-labels, nor of who owns DAF program strategy at wealth firms (philanthropic-services heads, product managers).
11. Contract terms (term length, renewal, termination, export rights) are unseen. These would shape migration-advisory timing (Q-N04, P-CON-01, P-QA1-06, all blocked).
12. Procurement constraints are not documented: conflict-of-interest policies for independent advisers, vendor-neutrality requirements, board approvals, and SOC or security reviews applied to consultants.

**Demand and triggers**

13. There is no dated pipeline of trigger events tied to named organisations. The repo has the raw material:
    - iPhi exits and DonorCentral sunset clients;
    - the Vanguard Charitable/Give Interactive go-live;
    - LPL–Commonwealth;
    - Altruist after the close;
    - the Foundation Source and Benevity exit windows;
    - the final §4966 rule.
14. The size of the consulting or market-intelligence market is unknown. There are no comparables for DAF research subscriptions and no buyers of DAFRC, NPT or Chariot reports identified.
15. Whether vendors (Ren, Foundant, Chariot, TIFIN) buy independent evaluation or market intelligence, or resist it, is unknown.
16. Credential value (DAFCP or CAP) for winning work is unknown. The repo found no postings and no adoption data.

**Evidence quality**

17. 517 queue items are open and 78 blocked. Many of the highest commercial-value items (commercial score 5) are blocked because they need human access, interviews or owner downloads (`data/mission-2026-11-14/owner-fetch-targets-2026-11-20.csv` lists 519 blocked sources).
18. Validation is same-model-family cross-agent checking, not independent human review.
19. The DAFCP package and the 2026-11-11/12 first-pass files are unvalidated.
