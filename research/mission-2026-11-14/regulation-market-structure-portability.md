# Regulation, market structure and portability: four open questions (Q-B09, Q-B02, Q-B01, Q-B17)

**Prepared 2026-11-14. Desk research only. No vendor, sponsor or regulator was contacted.** Every factual claim carries a source ID from the [source register](#source-register), and each register entry gives a URL and a date. Labels: **[F]** means the source states it directly. **[C]** is our own arithmetic on sourced figures. **[I]** is an inference or judgment. Bounded estimates show their inputs.

Companion data:
- [`data/mission-2026-11-14/regulatory-status-tracker.csv`](../../data/mission-2026-11-14/regulatory-status-tracker.csv): 15 regulatory and legislative items.
- [`data/mission-2026-11-14/sponsor-transfer-portability-terms.csv`](../../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv): 12 sponsors plus one row on DAF-to-DAF flow volume.
- The sponsor-level account figures come from the DAFRC FY2024 dataset, which a parallel workstream already extracted to [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) [S23b].

**What this note does not repeat.** The 2026 donor tax mechanics (0.5% floor, 35% cap, the nonitemizer deduction) are covered in `research/donor-tax-personas-2026.md`. The first-pass mention of the 2026–27 Priority Guidance Plan is in `research/daf-market-demand-and-evidence-gaps-2026-11-11.md` §8. Migration test design is in `research/migration-runbook-2026.md`. This note adds status verification, sponsor-level market structure, a vendor-penetration bound and outbound transfer terms.

---

## Executive answers

| Q | Answer | Confidence |
|---|---|---|
| **Q-B09 Regulation** | The Nov 14, 2023 proposed §4966 DAF regulations (REG-142338-07) are **neither final nor withdrawn**. A Federal Register query on 2026-11-14 shows only the 2023 proposal, a Jan 2024 correction and the 2024 hearing notices [S01–S04]. The **2026–27 Priority Guidance Plan** (Sept 29, 2026) replaced the "final regulations under §4966" item with "guidance under sections 4966 and 6033 regarding certain DAF arrangements" and dropped it from the deregulation list [S06,S07]. The **OBBBA (signed July 4, 2025)** does not name DAFs directly. It does exclude DAF gifts from the new permanent nonitemizer deduction and adds the 0.5%-AGI floor and the 35% cap from 2026 [S10,S11]. The **ACE Act** has not been enacted or found reintroduced. The **QCD-to-DAF** bills (House Apr 2025; Senate Mar 3, 2026) are introduced only [S13,S14]. **No state DAF law was found**: California AB 1712 failed in Feb 2020 [S16]. **No SEC or FINRA item specific to DAFs was found.** | High on federal regulatory status; medium on the absence of state, SEC and FINRA items, because search coverage was limited |
| **Q-B02 Processor share** | In DAFRC's revised FY2024 data, the 22 donation-processor sponsors hold **2,852,908 of 3,590,067 accounts (79.5%)** but **$2.93B of $327.87B in assets (0.9%)** [S23,S23b]. Three sponsors account for 99.4% of processor accounts. Givinga Foundation alone reports **1,421,011 accounts (39.6% of all US DAF accounts) holding $1.95M**. Bounded share of accounts that are pass-through: **50%–79.5%**, depending on whether we trust two data points that were filed on paper or imputed. Accounts at non-processor sponsors, the ceiling for "traditional invested" accounts: **at most 737,159 (20.5%)**. | High on the DAFRC figures; medium on the bounds |
| **Q-B01 External platform share** | The answer depends on the definition. (A) **Licensing third-party DAF fund-accounting or portal software:** bounded at **31%–94% of 1,512 sponsors**. Community foundations are most likely a majority: Foundant alone claims 700+ community-foundation clients against DAFRC's 803 [S25,S23]. (B) **Outsourcing DAF administration to a platform-administrator** (Ren, Foundation Source, TIFIN-type): we can name **≥6 legal sponsors (0.4%)**. These six hold **9.1% of DAF assets**. If every reported Ren customer were a distinct sponsor, the ceiling would be about **13%** of sponsors. | Low to medium. The vendor counts are self-reported and have no common denominator |
| **Q-B17 Portability** | **None of the 12 sponsors reviewed publishes an outbound transfer policy.** Every published page is about *inbound* transfers ("recommend a closing grant from your old sponsor"). Outbound moves rely on general rules that allow grants to 501(c)(3) public charities, subject to sponsor discretion and grant minimums [S34–S49]. Stated timelines run from "within 10 business days" after approval (Fidelity) to "2–4 weeks" end to end (GTCF) [S35,S48]. Transfers are generally done **in cash after liquidation** [S48]. **No sponsor commits to carrying grant history**: Daffy records become inaccessible after closure, and AEF's own platform migration kept only two years of history [S42,S51]. DAF-to-DAF flows reached **about $7.5B in 2024 (about 12% of DAF grants)** [S50]. | Medium to high |

---

## Q-B09. Regulation status as of November 2026

### 1. Proposed §4966 regulations (REG-142338-07)

**Status: still proposed. Not finalized and not withdrawn.** [F]

- Published Nov 14, 2023 as FR Doc. 2023-24982. A correction followed Jan 9, 2024 (2024-00260). Hearing notices followed Feb 29 and Apr 19, 2024 (2024-04262, 2024-08419) [S01–S03].
- On 2026-11-14 we queried the Federal Register API for IRS documents mentioning "donor advised fund". It returned no final rule and no withdrawal notice after the April 2024 hearing notice [S04]. The only newer match was the Sept 30, 2026 "Trump Accounts" temporary rule, whose DAF relevance we did not verify (text fetch blocked) [S04].
- Under the proposal, the rules would apply to taxable years ending after final regulations are published. Commentators describe sponsors as able to rely on the proposal but not bound by it [S08] [F, secondary].

**Content most relevant to business models** [F, S08,S09]:
- A **"personal investment advisor"** would be treated as a donor-advisor regardless of formal appointment. This is an adviser who manages both a donor's personal assets and that donor's DAF assets. The adviser's compensation paid from the DAF could then be an automatic excess benefit under §4958(c)(2), with a 25% tax on the adviser [S08].
- Community foundations and the Council on Foundations objected that the provision was overly broad. The May 6–7, 2024 hearings drew more than 30 in-person speakers [S08,S09].
- Fidelity Charitable told donors that its Charitable Investment Advisor Program (CIAP) does not change, because the rules were only proposed [S53].

### 2. Priority Guidance Plan trajectory

| Plan | DAF items | Source |
|---|---|---|
| 2024–25 | Four DAF items: §4966 final, §4958 proposed, §4967 proposed, public-support computation | [S05] (described retrospectively) |
| 2025–26 (fall 2025) | Only "Final regulations under section 4966" remained, listed as a deregulation/burden-reduction item. §4958, §4967 and public-support items were dropped | [S05,S06] |
| **2026–27 (released Sept 29, 2026)** | **"Guidance under sections 4966 and 6033 regarding certain donor-advised fund arrangements."** No longer listed for deregulation. §4958/§4967 DAF regulations absent | [S06,S07] |

**[I] Interpretation.** In 2025–26 the item was framed as burden reduction. In 2026–27 it is framed as "certain arrangements" plus Form 990 reporting (§6033). That reads as a narrower, targeted project rather than finalization of the full 2023 package. Plausible targets include arrangements resembling the 2023 personal-investment-advisor or "deemed DAF" concepts, or new Schedule D reporting, but the plan text does not say which. **No compliance date exists.** Neither the repo nor any product should treat the 2023 proposal as current law (consistent with `decision-intelligence-architecture-2026.md` rule 7).

### 3. Federal legislation, 2025–2026

- **OBBBA, Pub. L. 119-21, signed July 4, 2025.** Vanguard Charitable states that "Donor-advised funds are not directly named or impacted in the legislation" (page updated Oct 2026) [S10]. Indirect effects, all effective for tax years beginning after Dec 31, 2025 [S10,S11,S12]:
  - Permanent **nonitemizer deduction**: $1,000 for single filers, $2,000 for joint filers, cash gifts only, **DAF contributions excluded**.
  - **0.5%-of-AGI floor** for itemizers.
  - Deduction value capped at **35%** for the 37% bracket.
  - **1% floor for corporate gifts.**
- **ACE Act (Accelerating Charitable Efforts Act).** Introduced in the Senate in 2021 and the House in 2022. It would have set DAF distribution timelines. It was never enacted, and we found no 2025–26 reintroduction in searches run 2026-11-14 [S52]. Confidence is medium: "not found" is not proof that no bill exists.
- **IRA Charitable Rollover Facilitation and Enhancement Act.** It would allow QCDs to DAFs.
  - House: introduced Apr 10, 2025 by Reps. Smith and Panetta [S13]. Policy trackers list it as H.R. 2891, a number we did not verify on congress.gov.
  - Senate: introduced Mar 3, 2026 by Sens. Young, Bennet, Lankford, Cortez Masto and Cantwell [S14]. Trackers list it as S. 3975, also unverified.
  - Status: introduced only. Neither press release describes conditions on DAFs [F].
- **H.R. 9721, Fiscal Sponsorship Transparency Act of 2026.** Approved by Ways and Means on July 22, 2026. New Form 990 reporting would carve out DAFs. It would apply to tax years beginning after Dec 31, 2027. It is not law [S15].

### 4. State actions

- **California AB 1712 (2019–20).** It would have had the AG require DAF reporting, including inactive-fund policies capped at 36 months. Status: "Failed 2020-02-03, filed with the Chief Clerk pursuant to Joint Rule 56" [S16,S17]. **We found no DAF reporting law effective in 2025.** The prompt's premise of a "California DAF reporting law effective 2025" is **not supported**.
- **California AB 488 (2021), charitable fundraising platforms.** Core provisions took effect Jan 1, 2023, and AG regulations were finalized in 2024 [S18]. DAF sponsors are **conditionally excluded**. Per secondary summaries, the exclusion requires that a sponsor not list or name charities for solicitation by people who lack advisory privileges. **[I]** This conditional exclusion matters more for donation processors and app-based sponsors with public charity search than for traditional sponsors.
- **California AG DAF audit, "Donor Advised Funds: An Overview" (PDF, 2022).** It covered 57 sponsors and **excluded the two donation processors surveyed** because they "do not operate in the manner of other DAFs" [S19]. It is evidence of oversight interest, not a rule.
- We found no 2025–26 state DAF payout or reporting statute (searches 2026-11-14). Confidence is medium.

### 5. SEC and FINRA

No SEC or FINRA rule, guidance or enforcement action **specific to DAFs** was identified [searches 2026-11-14]. Adjacent items:
- SEC 2026 exam priorities emphasize fee-related conflicts of interest [S20].
- FINRA amended its gifts rule (Rule 3220), effective Mar 30, 2026. It covers gifts between firms and employees, not charitable accounts [S21].

**[I]** For adviser-managed DAF programs, the operative regulatory exposure is the **§4958 risk in the 2023 proposal**, not securities regulation. Two disclosures in the repo already show where SEC fiduciary rules touch DAFs: the OneAscent ADV conflict disclosure (`sponsor-governance-and-fee-transparency-2026-11-11.md`) and TIFIN's ADV, which names the sponsor as its advisory client.

---

## Q-B02. Pass-through processor accounts versus traditional invested accounts

### Definitions differ by source

| Source | Definition or treatment | Effect |
|---|---|---|
| DAFRC 2025 report and Apr 2026 memo | Classifies at the **sponsor level**. "National Sponsor (Donation Processor): …primarily focused on streamlining mass-scale or complex contributions and that also administers DAFs" [S22] | Every account at a processor sponsor counts as a processor account. Invested accounts at a processor, and cash-only accounts at a "standard" sponsor, are not separated |
| CA AG audit (2022) | **Excluded** the two donation processors from all results [S19] | Its account counts are not comparable with DAFRC totals |
| IRS Schedule D, Part I | "Number of DAFs at end of year" as reported by the sponsor | Sponsors can define an "account" differently. PayPal Giving Fund calls each donor's "Donor Account" a DAF [S24]. Network for Good reports **1** account [S23b] |
| NPT DAF Report (through 2024) | DAFRC became the producer for the 2025 edition; the original report says DAFRC separates processors so that trends "can be more easily interpreted" [S22] | Older NPT series mixed processor growth into headline account counts. The 2022 jump included about 1.29M accounts created at processors [S22] |

### FY2024 figures (revised Apr 2026 data) [F, S23,S23b]

| Segment | Sponsors | Accounts | Share of accounts | DAF assets | Share of assets | Mean assets/account [C] |
|---|---:|---:|---:|---:|---:|---:|
| Donation processors | 22 | 2,852,908 | 79.5% | $2.93B | 0.9% | ~$1,027 |
| Standard nationals | 81 | 515,376 | 14.4% | $233.17B | 71.1% | ~$452,000 |
| Community foundations | 803 | 104,425 | 2.9% | $66.14B | 20.2% | ~$633,000 |
| Single-issue (all) | 606 | 117,358 | 3.3% | $25.64B | 7.8% | ~$218,000 |
| **Total** | **1,512** | **3,590,067** | 100% | **$327.87B** | 100% | $91,300 (DAFRC) |

Single-issue subtypes [S23b]: religious 184 / 76,796 / $18.77B; other 294 / 37,142 / $3.40B; universities and healthcare 128 / 3,420 / $3.47B. These subtype sponsor counts differ slightly from the memo's percentage chart. We used the dataset. Processor payout in FY2024 was **190.3%**, against **23.0%** for standard nationals [S23].

### Processor accounts are concentrated in three entities [F, S23b]

| Processor sponsor (EIN) | FY2024 accounts | DAF assets | Data source flag |
|---|---:|---:|---|
| Givinga Foundation (47-4172718) | 1,421,011 | $1.95M | paper submission |
| American Online Giving Foundation (81-0739440) | 720,545 | $265.6M | IRS 990 (FYE Mar 2024) |
| PayPal Charitable Giving Fund (45-0931286) | 694,979 | $151.2M | **Imputed** (last FYE Dec 2023) |
| 19 others (Give Back Fdn 7,686; Philanthropi 5,923; FrontStream 1,952; Blackbaud Giving Fund 460; Dechomai 181 with $2.22B; Network for Good 1 …) | 16,373 | ~$2.51B | mixed |

**[C]** The top three hold 2,836,535 accounts. That is 99.4% of processor accounts and 79.0% of all US DAF accounts. Givinga alone is 39.6% of all US DAF accounts, at about **$1.37 per account**. Dechomai, a noncash-asset processor, holds 75% of processor *assets* with only 181 accounts. **[I]** "Processor" therefore covers at least three different businesses: workplace giving ledgers, consumer checkout giving, and noncash conversion.

PayPal's policy describes a 5% minimum annual distribution, a 36-month inactivity rule and funds held "in a secure, dedicated bank account" with no investment [S24]. That is the archetype of a non-invested pass-through account. We did not verify that American Online Giving Foundation is the Benevity-affiliated entity; it is commonly reported as such.

### Bounded share [C]

- **Upper bound on the processor share (as reported):** 2,852,908 / 3,590,067 = **79.5%**.
- **Sensitivity 1: drop Givinga's paper-filed count.** Excluding it from both numerator and denominator gives (2,852,908 − 1,421,011) / (3,590,067 − 1,421,011) = **66.0%**.
- **Sensitivity 2: also drop PayPal's imputed count.** That gives (1,431,897 − 694,979) / (2,169,056 − 694,979) = **50.0%**.
- **Bounded estimate:** 50%–79.5% of reported US DAF accounts are pass-through processor accounts. Processors hold under 1% of DAF assets on every variant.
- **"Traditional invested" accounts:** at most **737,159** (20.5% of reported accounts). Even that ceiling includes cash-like app accounts at "standard" sponsors. For example, Charityvest has 18,427 accounts averaging about $5,350, and Daffy has 4,869 averaging about $37,335 [S23b]. **Public data cannot establish a lower bound**, because Schedule D does not report invested versus cash balances.
- DAFRC's original Dec 2025 report gave 710,634 non-processor accounts out of 3,562,623 (80.1% processor) [S22]. The revision moved the share by under one point.
- The underlying data have gaps. DAFRC had filed data for **51.7% of sponsors, covering 74.3% of accounts**. The rest are imputed [S23].

**Decision implication [I].** Any per-account market size should start from **≤737k accounts**. Any asset-based size should start from **≈$325B of non-processor assets** ($327.87B − $2.93B). This confirms and quantifies the caution recorded in backlog row Q01.

---

## Q-B01. Share of sponsors paying an external technology or administration platform

### Two definitions, because they answer different commercial questions

- **Definition A, licensed software.** The sponsor pays a third party for fund accounting, CRM or a donor portal that runs its DAF ledger: Foundant CommunitySuite, NPact/FIMS, akoyaGO, iPhi, Give Interactive or Blackbaud. Staff remain in-house.
- **Definition B, outsourced administration.** A platform-administrator runs the DAF program's operations and technology, often bundled with a branded program: Ren, Foundation Source DAF OS, TIFIN Give, Givinga.

### Inputs

| Input | Value | Date | Source | Caveat |
|---|---|---|---|---|
| Sponsor universe | 1,512: 803 community foundations, 606 single-issue, 103 nationals (81 standard + 22 processors) | FY2024; Apr 2026 data | S23, S23b | Legal sponsors, not programs |
| Foundant CommunitySuite | "700+ community foundations"; 99% renewal | retrieved 2026-11-14 | S25 | Self-reported. May include Canadian or non-DAF foundations |
| Foundant (earlier) | >500 CommunitySuite community foundations; GLM >400 | July 2022 | S26 | Self-reported to Tech Impact |
| akoyaGO | "nearly 200 foundation customers" | July 2022 | S26 | Not all community foundations |
| NPact (FIMS, DonorCentral NXT acquired from Blackbaud) | "hundreds" of foundations; no FIMS count | Sept 2022 | S27 | Users are migrating off FIMS to Foundant [S26] |
| Give Interactive | 3 community-foundation clients | July 2022 | S26 | |
| iPhi (Stellar, acquired by Ren 2023) | ~175 clients | undated lead | S33 | Unverified investigative lead |
| Ren | "over 150 DAF programs"; >$175B | Nov 5, 2025 | S28 | Programs ≠ legal sponsors. Many programs sit under RCF |
| Ren (earlier) | ~200 customers | 2023, secondary | S32 | Dated, secondary |
| Foundation Source | 20,000 DAF accounts; 1,700 nonprofits; >5,600 private foundations | Dec 31, 2025 | S30 | Its turnkey DAFs are **sponsored by Charityvest**, so nonprofit "clients" are not separate legal sponsors |
| Named outsourced legal sponsors | RCF, Morgan Stanley GIFT, BofA Charitable Gift Fund and AEF (Ren); Charityvest (Foundation Source); GiveClear (TIFIN) | 2025–26 | repo; S29 | Six entities with sponsor-level FY2024 data |

### Arithmetic [C]

**Definition A, licensed software**
- Community foundations only: if all 700 Foundant clients were US community foundations that sponsor DAFs, that is 700 / 803 = **87.2%**.
- **Illustrative haircut** (assumption, not data): if one-third were non-US or non-DAF, that is 467 / 803 = **58.2%**.
- The other community-foundation vendors (akoyaGO ~200, NPact "hundreds", iPhi ~175) mean combined vendor claims exceed 803. **[I]** Community foundations very rarely build their own DAF ledger. That is consistent with Tech Impact surveying 11 vendors "actively marketing" to them [S26].
- **Lower bound, all sponsors:** (467 community foundations + 6 named outsourced sponsors) / 1,512 = **31.3%**. Using 700 instead of 467 gives (700 + 6) / 1,512 = 46.7%.
- **Upper bound:** assume every community foundation, every single-issue sponsor and about 10 nationals use paid third-party DAF software, and that the large nationals and processors use affiliate or in-house systems. That gives (803 + 606 + 10) / 1,512 = **93.8%**.
- **Bounded estimate A: 31%–94% of sponsors.** Community foundations are likely a majority of the vendor base. We have no public evidence on single-issue charities: university and religious sponsors may run DAFs in general nonprofit ERP or fundraising systems.

**Definition B, outsourced administration**
- Lower bound: 6 / 1,512 = **0.4% of sponsors**. These six hold $29.79B, or **9.1% of DAF assets**. They hold 91,803 accounts, which is 12.5% of non-processor accounts [S23b].
- Ceiling scenario: if Ren's ~200 reported customers were all distinct US legal sponsors, 200 / 1,512 = **13.2%**. Adding iPhi's ~175, if distinct, gives 375 / 1,512 = 24.8%. The 175 is unverified and overlaps with Definition A.
- **Bounded estimate B: 0.4%–13% of sponsors, but at least 9% of assets.**
- **[I]** Ren's "~half of all DAF assets" (about $175B) far exceeds the $29.8B we can attribute. Its claim must therefore count sponsors that use Ren or iPhi *software* without outsourcing administration, possibly including NPT ($42.12B) and others. That is unverified, and it is an example of mixing Definitions A and B.

### Serviceable market implication [I]

- The legal-sponsor market for **full outsourced DAF administration is small**: tens of sponsors. It is reached mainly through wealth-firm *programs* that are consolidated under a few sponsors (RCF, Charityvest, GiveClear).
- The **community-foundation software market is the broad, contestable market**: about 800 sponsors, already served by incumbents with near-total penetration (Foundant claims 99% renewal [S25]). Displacing an incumbent requires a migration, not a greenfield sale.
- New vendor revenue therefore comes mainly from three sources:
  1. Winning program-level wealth-firm mandates.
  2. Displacing legacy software, for example the FIMS base after its 2022 sale [S27].
  3. Bundling payments or compliance modules into existing stacks.

---

## Q-B17. DAF-to-DAF portability

### What sponsors publish

Rows, URLs and retrieval dates are in the CSV. In summary [F]:

- **Inbound pages are common.** Fidelity [S34], DAFgiving360 [S37], Charityvest [S43], Daffy [S41], RCF/Ren [S46], AEF [S44,S45], TIFIN Give/GiveClear [S47] and GTCF [S48] all explain how to receive a **grant** from a donor's current sponsor, with the donor's new account named in the memo.
- **Explicit outbound policies: none found.**
  - Outbound transfers rest on general grant eligibility. Fidelity allows grants to "qualified charitable organizations under section 501(c)(3)" [S35]. Vanguard allows grants to 501(c)(3) public charities [S38]. TIFIN Give allows "public charities and private operating foundations" [S47].
  - Each sponsor keeps discretion over whether to approve.
  - AEF states that "nearly all other donor-advised fund sponsors allow these transfers" [S45]. **[I]** "Nearly all" implies some do not.
- **Minimum grants act as the practical transfer floor:**

  | Sponsor | Minimum grant |
  |---|---|
  | Fidelity | $50 [S36] |
  | GiveClear | $100 [S47] |
  | NPT | $250 [S40] |
  | Charityvest | $15 [S43] |
  | Vanguard | $500, with an exception that allows one final grant below $500 for closing accounts with a balance under $500 [S38] |

- **Fees.** No sponsor publishes a transfer-out or closing fee. NPT says it does not charge grant fees [S40]. Fidelity's ongoing fee is 0.60% or $100 minimum on the first $500k, tiered down [S36]. Some sponsors charge balance maintenance fees, for example Vanguard's $250 below $25k [S39]. These can make partial residual balances costly.
- **Cash or in-kind.** "DAF-to-DAF transfers are generally completed as cash grants… your sponsor will typically liquidate them" [S48, GTCF May 18, 2026]. Vanguard liquidates contributed assets at its sole discretion [S38]. **[I]** A donor cannot carry a specific portfolio across sponsors. Advisers lose the position, though not necessarily the relationship.
- **Timelines.**

  | Sponsor | Stated timeline |
  |---|---|
  | Fidelity | Approved grants typically paid within 10 business days [S35] |
  | NPT | Grants processed weekly [S40] |
  | GiveClear | Review within 48 hours; electronic payment 2–7 business days [S47] |
  | GTCF | Grant recommendations 5–10 business days; 2–4 weeks end to end; credit 3–5 days after receipt [S48] |
  | Daffy | "Up to several weeks… Daffy has no control over this" [S41] |
  | RCF | Funding posts 2–5 days after proof of funding (general funding step) [S46] |

- **Tax treatment.** Inbound transfers are not new deductible contributions [S38,S43,S48].
- **History portability.** No sponsor commits to transferring grant or contribution history.
  - GTCF tells donors to download their full history before closing [S48].
  - Daffy says tax summaries and receipts "will no longer be accessible after the account is closed" [S42].
  - When AEF itself changed platforms (keeping the same sponsor), donors' portal history kept only the prior two years [S51].
- **Adviser relationships.** These depend on the *receiving* sponsor.
  - AEF accepts only donors "whose financial advisor manages the assets" [S44].
  - RCF requires an investment account opened with RCF as owner [S46; repo E13].
  - [I] An adviser-managed DAF can move between adviser-friendly sponsors with the adviser intact. A move to a sponsor that does not allow outside advisers (for example, a pooled-only sponsor) ends the adviser's role.
- **Tooling.** Daffy initiates inbound transfers through Chariot's DAFpay [S41]. [I] This lowers the donor's effort, but the outbound sponsor's approval is unchanged.

### Scale of movement [F, S50]

- Inequality.org/IPS (June 22, 2026) estimates **about $7.5B of 2024 grants went from DAF sponsors to other DAF sponsors**: about 11.6% of $64.6B in DAF grants [C]. About $5.6B moved between national sponsors.
- DAFgiving360 gave more than $0.5B to NPT, RCF and Fidelity Charitable combined.
- Caveats: the method classifies grantors and grantees with an 80%-DAF-grant threshold, and it mixes donor-initiated transfers with sponsor-to-sponsor program flows. The article's own labels contain unit and year inconsistencies. Treat it as an order-of-magnitude figure.

**Lock-in implication [I].** Legal lock-in is **weak**. Transfer is a routine grant, and inbound sponsors actively market it (Charityvest has run fee promotions [S43]). Practical lock-in comes from five frictions:
1. Liquidation and loss of positions.
2. No history portability.
3. Adviser eligibility at the receiving sponsor.
4. Minimum balances, residual balances and maintenance fees.
5. Approval latency of 1–4 weeks, which matters at year-end.

Those frictions favor incumbents with adviser channels (an adviser can block or enable a move) more than incumbents with retail donors. The $7.5B flow shows they are surmountable at scale.

---

## Synthesis: regulatory risk and market implications by business model

| Model | Regulatory risk (Nov 2026) | Market-structure implication | Portability implication |
|---|---|---|---|
| **Asset-based-fee sponsors** (Fidelity, Vanguard, NPT, DAFgiving360) | **Low near-term.** No payout mandate; ACE Act dormant. Medium-term: the §4966/§6033 "certain arrangements" project could add reporting. OBBBA's DAF exclusion from the nonitemizer deduction slightly favors direct giving for small donors [S10,S11] [I] | Revenue rides on the ~$233B at standard nationals, not on the 2.85M processor accounts | Biggest *source* of outbound DAF-to-DAF flow (DAFgiving360 >$0.5B [S50]); liquidation and history frictions protect balances |
| **Adviser-managed programs** (RCF/Ren, AEF, Morgan Stanley GIFT, BofA, GiveClear, CIAP-type) | **Highest specific exposure.** If finalized as proposed, the personal-investment-advisor rule would turn DAF-paid adviser compensation into a §4958 excess benefit [S08]. The project is reframed, not abandoned [S06,S07]. Watch whether the new "certain arrangements" guidance revives it | The six named outsourced sponsors hold 9.1% of DAF assets [C] | Advisers can pull assets *in* (AEF ~$200M inbound over several years [S44]). Rule changes could reverse that |
| **White-label and administration vendors** (Ren, Foundation Source, TIFIN, Givinga) | Indirect. Their sponsor clients bear §4966/§4958 risk. A §6033 reporting change would be **a feature opportunity** (reporting modules) [I] | Definition B market is tens of legal sponsors. The broad market is ~800 community foundations already on licensed software (Definition A). Growth comes from program mandates and migrations | Platform switches keep the same sponsor; history loss is a vendor-level risk (AEF: 2 years) [S51] |
| **AI-native entrants** | Low direct risk if they stay a software layer. If they sponsor DAFs or touch processor-style flows, California AB 488 platform rules may apply unless the DAF-sponsor exclusion conditions hold [S18] [I] | Per-account economics: ≥80% of "accounts" are processor ledgers averaging ~$1,027 or less. The invested, adviser-relevant pool is ≤737k accounts [C] | Their best opening is the inbound-transfer path plus full-history import, the gap that no incumbent publishes [I] |

---

## Open questions

1. What will the 2026–27 "certain DAF arrangements" guidance cover, and will it come as proposed regulations or a notice? Monitor the Federal Register and IRS.
2. Confirm the bill numbers (H.R. 2891, S. 3975) and committee actions on congress.gov, which was not fetched.
3. Sponsor-level validation of Givinga's 1.42M paper-filed count and PayPal's imputed FY2024 count. Check the FY2024 990 Schedule D filings directly.
4. Vendor-sponsor mapping by EIN: which of the 803 community foundations use Foundant, NPact, akoyaGO or iPhi. Candidates: community-foundation 990 Schedule O and contractor disclosures, plus vendor case studies.
5. Explicit outbound transfer policies. We need program guidelines from DAFgiving360 (page returned HTTP 403), NCF (no transfer page found), NPT and Vanguard (silent), and Fidelity's full Program Guidelines.
6. Does Ren's "$175B / half of DAF assets" include software-only iPhi sponsors such as NPT?

---

## Data dictionary

### `regulatory-status-tracker.csv`
| Column | Meaning |
|---|---|
| item | Name of regulation, plan item, bill or state action |
| jurisdiction | `US-federal`, `US-CA`, `US-states` |
| instrument | proposed_regulation, guidance_plan, statute, bill, state_bill, state_statute, state_report, agency_rule, none_found |
| status | Status as verified on status_date (e.g., `proposed_not_final`, `enacted`, `introduced`, `failed`, `committee_approved`, `not_found`) |
| status_date | ISO date of the latest verified status event, or of the retrieval check |
| effect_on_daf_operations | Operational effect on sponsors (fact or labeled inference) |
| effect_on_business_models | Labeled inference on the asset-fee, adviser-managed, white-label and AI-native models |
| source_url | Primary or best available URL |
| notes | Confidence, caveats, retrieval date |

### `sponsor-transfer-portability-terms.csv`
| Column | Meaning |
|---|---|
| sponsor | Legal sponsor (program or brand in parentheses) |
| transfer_out_allowed | `not_published_general_501c3_eligibility` (no explicit outbound policy; general grant rules imply permitted), `implied_yes`, or `unknown` |
| mechanism | Published transfer mechanism (usually inbound closing grant) |
| in_kind_or_cash | Stated asset form; `not_stated` if absent |
| minimums | Grant or account minimums relevant to a transfer |
| fees | Published fees relevant to transfer or residual balances |
| stated_timeline | Sponsor's own processing-time language |
| history_portability | Whether grant/contribution history moves; `not_stated` if absent |
| source_url | Page(s) used |
| retrieved_date | Date fetched (2026-11-14 unless marked) |
| notes | Caveats, adviser-relationship terms, confidence |

---

## Source register

All URLs were retrieved on 2026-11-14 unless another date is given. "Search" means the page was surfaced through web search and its content was taken from the search summary, not a full fetch.

| ID | Source | Date of source | URL |
|---|---|---|---|
| S01 | Federal Register 2023-24982, proposed §4966 regs | 2023-11-14 | https://www.federalregister.gov/documents/2023/11/14/2023-24982/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966 |
| S02 | FR 2024-00260 correction | 2024-01-09 | https://www.federalregister.gov/documents/2024/01/09/2024-00260/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966 |
| S03 | FR 2024-08419 hearing notice (also 2024-04262, 2024-02-29) | 2024-04-19 | https://www.federalregister.gov/documents/2024/04/19/2024-08419/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966-hearing |
| S04 | Federal Register API query, IRS + "donor advised fund", newest first | queried 2026-11-14 | https://www.federalregister.gov/api/v1/documents.json?conditions[term]=%22donor%20advised%20fund%22&conditions[agencies][]=internal-revenue-service&order=newest |
| S05 | EY Tax News, 2025–26 PGP exempt-org projects | 2025-10-03 | https://taxnews.ey.com/news/2025-2004-irs-and-treasury-2025-2026-priority-guidance-plan-includes-various-projects-applicable-to-tax-exempt-organizations |
| S06 | ArentFox Schiff, 2026–27 PGP alert | 2026-10-07 | https://www.afslaw.com/perspectives/alerts/irs-and-treasury-release-2026-2027-priority-guidance-plan-what-tax-exempt |
| S07 | RSM, FY2027 exempt-org guidance priorities | 2026-10-01 | https://www.rsmus.com/insights/tax-alerts/2026/treasury-irs-exempt-organization-guidance-priorities-fy-2027 |
| S08 | Baker McKenzie via Global Compliance News, proposed regs and hearings (search) | 2024-05-17 | https://www.globalcompliancenews.com/2024/06/01/https-insightplus-bakermckenzie-com-bm-tax-united-states-donor-fund-proposed-regulations_05172024/ |
| S09 | Council on Foundations hearing testimony (search) | 2024-05-06 | https://cof.org/sites/default/files/2024-05/2024-05-06-Council-Public-Testimony-DAF-Regulations.pdf |
| S10 | Vanguard Charitable, "How the OBBBA changed charitable giving rules for 2026" | 2025-07-09, updated Oct 2026 | https://www.vanguardcharitable.org/news/could-2025-budget-reconciliation-bill-impact-your-giving |
| S11 | IRS newsroom, nonitemizer deduction excludes DAF contributions (cited in repo) | 2026-11-10 | https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize |
| S12 | IRS Publication 505 (2026), 0.5% floor (cited in repo) | 2026 | https://www.irs.gov/publications/p505 |
| S13 | Rep. Adrian Smith press release, IRA Charitable Rollover bill | 2025-04-10 | https://adriansmith.house.gov/media/press-releases/smith-panetta-introduce-bipartisan-bill-support-charitable-giving |
| S14 | Sen. Todd Young press release, Senate companion | 2026-03-04 | https://www.young.senate.gov/?p=13549 |
| S15 | CBIZ, four pending House bills (H.R. 9721 etc.) | 2026-08-19 | https://www.cbiz.com/insights/article/four-pending-house-bills-could-affect-not-for-profit-reporting-political-activity-and-religious-organizations |
| S16 | LegiScan, CA AB 1712 (2019–20) status (search) | 2020-02-03 status | https://legiscan.com/CA/bill/AB1712/2019 |
| S17 | Bloomberg Tax on AB 1712 | 2020-01-14 | https://news.bloombergtax.com/daily-tax-report-state/california-looks-into-billions-held-in-funds-intended-for-charities |
| S18 | Davis Wright Tremaine, AB 488 rules in effect (search) | 2024-06 | https://www.dwt.com/insights/2024/06/california-ab-488-charitable-funds-rules-in-effect |
| S19 | California AG, "Donor Advised Funds: An Overview" (audit PDF) | PDF created 2022-05-18 | https://oag.ca.gov/system/files/media/donor-advised-funds-overview.pdf |
| S20 | Reed Smith, SEC 2026 regulatory focus (search) | 2026 | https://www.reedsmith.com/articles/private-equity-behind-the-scenes/sec-sets-the-tone-for-2026-regulatory-focus-on-investment-managers/ |
| S21 | Norton Rose Fulbright, new FINRA gifts rule (search) | 2026 | https://www.nortonrosefulbright.com/en/knowledge/publications/52e43690/the-new-finra-gifts-rule |
| S22 | DAFRC, The Annual DAF Report 2025 (PDF) | Dec 2025 | https://static1.squarespace.com/static/6011def87418a462fcb03978/t/6941a4cc17e484296f44b45d/1765909728393/Annual+DAF+Report+2025+-+DAF+Research+Collaborative.pdf |
| S23 | DAFRC, Annual DAF Report 2025: Updated Analysis Memo | Apr 2026 | https://static1.squarespace.com/static/6011def87418a462fcb03978/t/69e91dfad34ffd5d1cb6aea5/1776885242265/Annual+DAF+Report+2025+Updated+Analysis.pdf |
| S23b | DAFRC Updated Analysis Dataset (as extracted in repo `dafrc-sponsor-schedule-d-fy2019-2024.csv`) | Apr 2026 | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx |
| S24 | PayPal Giving Fund Donor Account Policy | updated 2024-08-13 | https://www.paypal.com/us/webapps/mpp/givingfund/policies/donor-account-policy |
| S25 | Foundant CommunitySuite product page | retrieved 2026-11-14 | https://www.foundant.com/products/communitysuite/ |
| S26 | Tech Impact, Landscape of Integrated Software for Community Foundations | July 2022 | https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf |
| S27 | PR Newswire, NPact acquires FIMS and DonorCentral NXT from Blackbaud (search) | 2022-09-12 | https://prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html |
| S28 | Pulse 2.0, Great Hill Partners investment in Ren | 2025-11-05 | https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/amp/ |
| S29 | AEF/Ren, AEF fully on Ren platform (repo R05) | 2026-04-08 | https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/ |
| S30 | Foundation Source, "The modern operating system for DAFs" | metrics as of 2025-12-31 | https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/ |
| S32 | IBJ, Ren Bain Capital investment, ~200 customers (repo N13) | 2023 | https://www.ibj.com/articles/indianapolis-based-ren-inc-snags-big-investment-from-bain-capital-fund |
| S33 | Repo lead: `research/iphi-175-client-lead-and-dns-execution-2026-11-11.md` | 2026-11-11 | (internal) |
| S34 | Fidelity Charitable FAQ, transfer to Giving Account | retrieved 2026-11-14 | https://www.fidelitycharitable.org/faqs/all/transfer-to-giving-account.html |
| S35 | Fidelity Charitable, Recommending a grant | retrieved 2026-11-14 | https://www.fidelitycharitable.org/giving-account-guide/recommending-a-grant.html |
| S36 | Fidelity Charitable, What it costs | retrieved 2026-11-14 | https://www.fidelitycharitable.org/giving-account/what-it-costs.html |
| S37 | DAFgiving360, Transfer a DAF (HTTP 403 on fetch; search summary) | retrieved 2026-11-14 | https://www.dafgiving360.org/transfer-donor-advised-fund |
| S38 | Vanguard Charitable Policies & Guidelines | updated 2026-01-09 | https://www.vanguardcharitable.org/company-policies/policies-and-guidelines |
| S39 | Vanguard Charitable, Transferring assets | retrieved 2026-11-14 | https://www.vanguardcharitable.org/transferring-assets |
| S40 | NPT DAF FAQ | retrieved 2026-11-14 | https://www.nptrust.org/donor-advised-funds/faq/ |
| S41 | Daffy Help, How do I transfer a DAF? | 2025-09-18 | http://help.daffy.org/en/articles/5594104-how-do-i-transfer-a-donor-advised-fund |
| S42 | Daffy Help, How do I close my Daffy account? | 2026-04-02 | http://help.daffy.org/en/articles/6520234-how-do-i-close-my-daffy-account |
| S43 | Charityvest, Transfer a DAF page and guide | retrieved 2026-11-14 | https://www.charityvest.org/transfer-a-daf ; https://guide.charityvest.org/for-donors/promos/transfer-a-daf |
| S44 | AEF, Recent increase in DAF transfers to AEF | undated; retrieved 2026-11-14 | https://www.aefonline.org/thought-leadership/recent-increase-daf-transfers-aef/ |
| S45 | AEF, Transferring DAFs to AEF | undated; retrieved 2026-11-14 | https://www.aefonline.org/thought-leadership/transferring-donor-advised-funds-to-aef/ |
| S46 | Ren, How to open an RCF DAF (account closing grant) | retrieved 2026-11-14 | https://www.reninc.com/rcf-daf/ |
| S47 | TIFIN Give DAF Program Guidelines (GiveClear) | 2025-08-12 | https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines |
| S48 | Greater Tacoma Community Foundation, DAF Transfer Instructions | 2026-05-18 | https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf |
| S49 | National Christian Foundation, Giving Fund page | retrieved 2026-11-14 | https://www.ncfgiving.com/giving-fund/ |
| S50 | Inequality.org (IPS), DAF-to-DAF giving reached $7B in 2024 | 2026-06-22 | https://inequality.org/article/daf-to-daf-giving-2024/ |
| S51 | AEF DonorCentral sunset; two years of history (repo R06) | 2026-10-31 | https://engage.aefonline.org/dc-sunset/ |
| S52 | Steptoe, King/Grassley ACE Act introduction (search) | 2021 | https://www.steptoe.com/en/news-publications/senators-king-and-grassley-introduce-daf-and-private-foundation-reform-legislation.html |
| S53 | Fidelity Charitable, Proposed DAF regulations (search) | 2023–24 | https://www.fidelitycharitable.org/articles/proposed-donor-advised-fund-regulations.html |

**Method limits.**
- Shared web-search budget ran out during the Q-B17 work. Remaining sponsor pages were fetched directly where URLs were known.
- Pages that could not be fetched were dropped or marked: DAFgiving360 and congress.gov returned 403, ProPublica returned a security check, and the Trump Accounts rule text was not retrievable.
- Rows sourced from search summaries are marked "(search)" above. Treat them as secondary.
