# Track F: institutional distribution and market-entry segments (notes)

**Date:** 2026-11-26. **Companion:** `trackF-segments.csv` (14 rows: F01–F13 plus F14, a channel row).
**Scope:** This pass extends the repository's prior work and does not repeat it. Sponsor-side economics (repo 02 and 07; mission b45n33 and b50-03) are cited, not recomputed. The new material covers banks, credit unions, trust companies, RIA custodians and wealthtech channels, procurement regimes, and sales-cycle evidence.
**Evidence classes:** VERIFIED-FACT, VENDOR-CLAIM, INFERENCE, ASSUMPTION and UNKNOWN. Every URL was accessed on 2026-11-26. Public sources only, with no outreach.

## 1. New primary counts from this pass

| Item | Value | Source | Class |
|---|---|---|---|
| Active FDIC-insured institutions | 4,204 (API index 2026-11-24). The Q2 2026 QBP figure is 4,238 (2026-08-25) | api.fdic.gov/banks/institutions; ABA Banking Journal | VERIFIED-FACT |
| Banks by assets | <$1bn: 3,153; $1–10bn: 890; $10–100bn: 128; ≥$100bn: 33 | FDIC API, computed | VERIFIED-FACT |
| Trust-powers code 10 ("full trust powers granted") | 1,038 in total; 352 in the $1–10bn band; 71 in the $10–100bn band | FDIC API, TRUST field | VERIFIED-FACT. Codes 11 and 12 (exercised or not) do not appear; 2,768 are coded 00 ("not known") |
| Institutions reporting fiduciary and related assets (RC-T, TFRA > 0, YE2025) | 1,006. Of these, 251 hold $1–100bn, together $2.55tn; 28 hold >$100bn, together $43.0tn (custodians) | FDIC API financials, REPDTE 20251231 | VERIFIED-FACT. TFRA includes custody and non-managed assets, so it is **not** a DAF asset figure |
| Federally insured credit unions | 4,214 (2026Q2); 748 complex (>$500m); 146.1m members; $2.50tn assets | NCUA Quarterly Data Summary 2026 Q2 | VERIFIED-FACT |
| SEC-registered RIAs | 16,544 at YE2025; median firm has 8 employees and $446.9m | IAA/COMPLY snapshot 2026, via ThinkAdvisor/InvestmentNews | VERIFIED-FACT (secondary report of a primary dataset) |
| National trust banks | about 60 (OCC) | Federal Register 2026-03-02 | VERIFIED-FACT |
| Single-family offices (North America) | 3,180 in 2024 (Deloitte) | Deloitte press release | VERIFIED-FACT (estimate) |
| DAF sponsors by type, FY2024 | CF 804 ($63.8bn); national 82 ($232.0bn); religious 184 ($18.8bn); university/hospital 128 ($3.4bn); other single-issue 294 ($3.2bn); processors 22 ($2.0bn) | Repo long-tail CSV, recomputed | VERIFIED-FACT (repo) |
| New sponsor formation | 138 entries to the panel FY2021–24 (about 35 a year), of which only 26 are newly ruled organisations (about 6.5 a year) | Repo | VERIFIED-FACT (repo) |

**Units.** The CSV keeps bank fiduciary assets, CU balance-sheet assets, RIA RAUM and DAF Schedule D assets in separate columns, and no ratio is taken across them.

## 2. Who serves banks, CUs and trust companies today (the specific questions)

- **Regional banks.**
  - Regions and First Citizens run on RCF/Ren (repo PW24).
  - KeyBank, Truist/BB&T and BNY CGF appear as iPhi tenants (repo census).
  - Wells Fargo names NPT as its establishment partner.
  - Huntington and First Citizens also refer clients to local community foundations.
  - **TIFIN Give white-label via SEI** (2026-01-29) targets SEI's bank, affiliated-wealth and *independent trust company* clients. It is the newest competitor in exactly this channel. SEI also runs an RCF/Ren stack (repo PW20). [VERIFIED-FACT and VENDOR-CLAIM]
- **NPT private label.**
  - Onboarding takes about 14–16 weeks.
  - No partner count or fees are published, and the page's stat counters were blank placeholders. [VENDOR-CLAIM]
- **Credit unions.**
  - **No member-facing CU DAF was found**, which confirms repo PW24.
  - The CU DAFs that do exist are *institutional* funds that CUs hold at league foundations:
    - the Credit Union Impact Foundation (AL, FL, GA, VA): $10k minimum, $150 setup, 0.75% fee on the balance, $25 per grant;
    - the Carolinas CU Foundation (Allegacy);
    - the Iowa CU Foundation;
    - the Cornerstone Foundation.
  - Member wealth runs through broker-dealer partners (LPL/CFS, Osaic Institutions, Cetera FI). Those programs moved between providers in 2025, but none shows DAF content.
  - Giving features without a DAF:
    - Spiral on Alkami (2025-11-18). Texans CU had "1,000+ members enrolled in 48 hours" [VENDOR-CLAIM].
    - NetGiver (CCUA).
  - **Ren already owns an FI channel asset:** Pinkaloo (acquired in 2021) sold giving tools to financial institutions, including CUs.
  - **Amicus "DAF 2.0"** (white-label DAFs for banks and CUs, 2020–21) was acquired by TIFIN and repositioned toward advisors. That is a disconfirming precedent for a bank/CU-first DAF thesis. [VERIFIED-FACT on the deal; INFERENCE on the reason]
- **RIA custodians.**
  - DAFgiving360 is integrated with Schwab Advisor Center. It has about 4,000 advisors (FY2024) and a $100k minimum for advisor-managed accounts.
  - Altruist launched DAFs sponsored by Endaoment at 50 bps with no minimums; Vanguard is acquiring Altruist in 2026.
  - Foundation Source and Charityvest offer multi-custodial branded DAFs through BridgeFT (2025-09-23).
- **Wealthtech platforms.**
  - GiftingNetwork white-label is in Orion's Premier Partnership Program (2025-08-18) and on Envestnet.
  - Foundation Source is on Envestnet (2025-09).
  - **No Addepar DAF integration was found.**
- **Core and digital-banking marketplaces.** No DAF vendor was found in the Jack Henry FIN/VIP, Q2 Partner Marketplace or Fiserv marketplaces. The only giving product found is Spiral on Alkami. Jack Henry states that FIN inclusion is not an endorsement, so each FI still runs its own due diligence.
- **CF software.**
  - Repo map: Foundant has 361 of 803 CFs (45%), and 315 are unmapped.
  - Foundant claims "700+ CFs" [VENDOR-CLAIM].
  - Recent switches: 5 of 28 iPhi CFs left in 2023–26 (4 to Foundant, 1 to akoyaGO), and WaterStone, a faith sponsor, moved to Give Interactive (repo).
  - Capterra reviewers say most CFs have left or are leaving FIMS.

## 3. Procurement, sales cycle and CAC evidence

- **Banks.**
  - The Interagency Guidance on Third-Party Relationships (OCC 2023-17, FIL-29-2023, SR 23-4; 2023-06-06) covers the whole vendor lifecycle.
  - The 2024 community-bank TPRM guide (OCC 2024-11) adds practical guidance.
  - The bank stays responsible for the outsourced activity. Complexity is scored 5.
- **Credit unions.**
  - NCUA has no vendor-examination authority; a 2026 House bill would grant it.
  - CUs remain fully responsible for due diligence.
  - PYMNTS/Velera (2026): 56% of fintechs cite complex CU procurement (28% in Nov 2023) and 54% cite slow decisions. 58% of hesitant fintechs would partner if a bundled onboarding served several CUs at once (21% before).
  - The average CU sources about 9 products from third parties.
- **Sales cycle data points.**
  - Alkami's FY2025 10-K, read through a mirror (verify on EDGAR): sales cycle of about 3–12 months, then implementation of 6–12 months. Bank implementations fell below 11 months in 2025, from more than 13 months in 2023–24.
  - Alkami's CEO describes about a year to buy and a year to implement. These figures are for digital banking, so they are an upper bound for a DAF module.
  - a16z (2023-10-16): FIs look for a 5–10x ROI multiple, and cores (FIS, Fiserv, Jack Henry) can refer products.
  - Vendor blogs give 6–18 months. These are low quality.
- **CAC.** No published CAC exists for DAF administration or philanthropy technology sold to FIs. **UNKNOWN.** Repo 07's partnership model assumes a revenue share of about 30%.

## 4. Underserved evidence (positive only)

| Segment | Positive evidence | Caveat |
|---|---|---|
| F12 Sponsors re-platforming | Measured iPhi exits: 6 of 57 (10.5%), 5 of them between 2025-05 and 2026-06 | Every exit landed on an existing vendor |
| F02 Community foundations | 5 of 28 iPhi CFs left Ren; FIMS exodus | Foundant absorbs most of them |
| F10 Faith foundations | WaterStone left iPhi for Give Interactive | n = 1 |
| F03 Regional banks / F07 trust companies | Regions costs about 1.10% all-in at $1m on a legacy portal (repo); SEI added a second white-label DAF stack in 2026 aimed at banks and trust companies | The distributor's own claim; a competitor (TIFIN) now holds the SEI channel |
| F04 Credit unions | Fast uptake of giving widgets (Texans CU) | That is not DAF demand. No member DAF exists, and the Amicus pivot points the other way |

**No positive underserved evidence** was found for:
- RIAs (crowded: at least six branded or white-label options, plus free custodian DAFs);
- family offices;
- corporate programs;
- new sponsors (few, and small);
- licensing buyers (the pattern there is acquisition: Pinkaloo, Amicus, Vennfi, Altruist).

## 5. Channels that avoid head-on competition with Ren [INFERENCE]

1. **CF and faith re-platforming (F02, F10, F12).** Here the competition is Foundant, akoyaGO and Give Interactive. Ren is the vendor losing clients, so an entrant competes for its departing clients, not against its sales team.
2. **CU league foundations and CUSO-level aggregators (F14).** They already run institutional DAFs by hand. One contract reaches many CUs, and it fits the bundled-onboarding preference fintechs report.
3. **Digital-banking marketplaces (Alkami, Q2, Jack Henry Banno).** The Spiral/Alkami precedent shows giving widgets get distributed this way. **No DAF vendor is there yet**, but the CU DAF demand evidence is negative, so this is an option to test, not a proven channel.
4. **Multi-custodial data layers (BridgeFT) and wealthtech partner programs (Envestnet, Orion).** These bypass Ren's direct sales, but GiftingNetwork, Foundation Source and TIFIN already hold the slots. Addepar shows no DAF partner.
5. **Bank-tech distributors like SEI.** The model works, but SEI has now taken TIFIN. Comparable distributors are trust-accounting and wealth-platform providers (e.g., FIS, Fiserv wealth units). Whether they have a DAF partner is **UNKNOWN**.

## 6. Gaps and follow-ups

- A FINRA member-firm count (F05).
- A national count of state-chartered trust companies (CSBS or state-by-state).
- Alkami 10-K wording, to be verified on EDGAR.
- 2026 DAFRC report: none found; the 2025 edition (1,485 sponsors per Chariot's summary) is the latest.
- Fee terms and minimums for SEI/TIFIN and GiftingNetwork.
- Whether Pinkaloo is still sold to FIs under Ren.
- Whether Jack Henry FIN, Q2 or Fiserv list any DAF partner: only searched, not browsed.

## 7. Memory-relevant items for the main session

None. The repository memory index was empty, and nothing from memory was used.
