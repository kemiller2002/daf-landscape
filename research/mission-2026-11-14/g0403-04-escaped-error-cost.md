# Escaped-error cost m: bank SAR penalties, the DAF excise regime, and the routing variant rerun

*Queue item P-G0403-04. Prepared 2026-11-19.*

- **Parameter:** m, the cost of an error that escapes review, in units of one case's handling time. It enters the routing variant as C_route = h·a_p·L·[(1 − ρ) − 0.5k − k·e − (1 − k)·e·m] − inference ([g0401-g0502-ai-routing-and-per-grant.md](g0401-g0502-ai-routing-and-per-grant.md) §2). Until now it was a sweep {0, 1, 5, 20, 50} with no source.
- **Script:** [`scripts/mission_escaped_error_cost.py`](../../scripts/mission_escaped_error_cost.py). It imports `mission_ai_routing_variant.py` (and through it the calibrated model and v2) unchanged. Stdlib only, functional style, seed 42 plus the routing stream 42 + 104729. Run as `python3 scripts/mission_escaped_error_cost.py .` (10,000 draws, about 4 minutes).
- **Data:** [`data/mission-2026-11-14/escaped-error-cost-2026-11-19.csv`](../../data/mission-2026-11-14/escaped-error-cost-2026-11-19.csv) (1,446 rows).
- **Queue proposals:** [`data/mission-2026-11-14/queue-proposals-g0403-04.csv`](../../data/mission-2026-11-14/queue-proposals-g0403-04.csv).
- **Replication:** the route cells at m = 1, 5 and 20 reproduce `ai-routing-variant-2026-11-19.csv` exactly. The maximum relative difference across 42 cells is 0 (`record_type=meta`).

**Notation.**
- **[F]** quoted from a primary source.
- **[C]** computed from [F] figures and the repo's model inputs.
- **[I]** inference or assumption.
- **[S]** scenario output, conditional on [I].

---

## 1. Bottom line

1. **Conditional on enforcement, a missed SAR at a US bank cost $36k–$471k in FinCEN penalty** (four depository orders that state a count; median $176k) [C]. In the model's units (P14 AML alert handling, 15 min at $55.45/h = $13.86), that is **2,600–34,000 handling units** per missed SAR (median 12,700), before any lookback or remediation cost [C].
   - Bank of America (2026): $1.2bn ÷ "nearly 8,900" missed SARs = **$134,831** per SAR, or **9,726** handling units [C].
   - TD Bank (2024): $1.3bn ÷ "over 6,000" late SARs = **$216,667** [C]. Using all agency amounts stated in the FinCEN order, net of FinCEN's credit, it is $536,750 [C].
   - USAA FSB (2022): $140m ÷ "at least 3,873" late SARs = **$36,148** [C]. Per un-reviewed alert in its ~90,000-alert backlog, it is **$1,556**, or 112 units [C].
   - CommunityBank of Texas (2021): $8m ÷ "at least 17" SARs = **$470,588** [C].
2. **Penalties are not priced per SAR.** They follow the program failure, so allocating the whole penalty to the missed SARs gives an upper bound [I]. The FinCEN penalty was at least 47% of the statutory per-SAR maximum for BofA, 78% for TD and 14% for USAA. These are lower bounds, because each SAR is priced at the order’s cap although the maximum is the transaction amount where that is lower; TD’s order puts its late-reported activity at “over $500 million” across the 6,000 SARs. For Canaccord it was 175%, and for CBOT 199% (17 SARs at its order’s $236,071 cap); both exceed what the SAR violations alone could carry [C]. [V wave 38B]
3. **Lookback labour can rival the penalty.** BofA's order states "800 consultants" for its one-time lookback but no duration. At 0.5–2 years, priced at the P14 rate, that adds **374–1,496 handling units per missed SAR** [C on an assumed duration, I].
4. **The DAF penalty regime is far lighter per error [I].** Under IRC §4966 the sponsor pays 20% of a taxable distribution [F], and under §4967 a fund manager pays 10% of a prohibited benefit, capped at $10,000 [F]. Combined with the repo's grant anchors ($500 median to a $40k mean) and one correction unit, an escaped error in P07 or P08 costs:
   - **1.0–10.6 handling units** if detection and assessment happen 1 time in 10 or less;
   - **2.2–174 units** if every escaped error is detected and taxed [C+I].
5. **Proposed m for the routing model (single m, weighted by AI-amenable pool):** **low 1.0, central 2.4, high 106** [I]. Superseded: wave 38B corrects these to 2.20 and 88.5 (P08 at its correction unit). g0403-0104 then bounds detection and lowers the central to 1.77 (bank-SAR transfer kept) or 1.56 (OFAC per-violation analogue), with high 55 or 9.3. Pricing a sanctions miss per missed alert (Amex 2022) instead gives a central of about 128, so the composite still turns on the unsourced P01/P14 terms [C/I] [V wave 39B] The high setting assumes certain detection, a $40k grant, a bank-to-DAF transfer of 0.1 for P01/P14, and operational m = 5.
   - The central value lies below routing's per-draw break-even m in every draw. The break-even (the m at which an AI-closed case saves nothing) has p05 11.3, median 21.7 and p95 199 [C].
   - The high value lies above it in 90% of draws [S].
6. **Rerun (CAL_CENTRAL, large national) [S].**
   - At the central m = 2.4, the routing pool is **$1.26m**, against $1.36m at m = 1 and $445k for assistance. C ranks first with probability 0.009. At the wave-38B central of 2.20 the pool is $1.27m, and at g0403-0104’s 1.77 / 1.56 it is $1.31m / $1.32m [S] [V wave 39B]
   - At a single m = 106, the routing pool is **$0**.
   - **Applying high m only where it belongs** (P01, P07, P08 and P14 high; operational processes at 5) leaves routing at **$535k**, still above assistance. Hybrid routing, which keeps assistance on the remaining cases, reaches $753k.
   - **Under full compliance re-review** (k = 1 for P01, P07, P08 and P14), compliance errors cannot escape, so the process-specific high case equals m = 5 elsewhere, at **$844k**.
7. **The ranking conclusion does not change.** Assistance is still modal nowhere. C's mean rank-first probability is at most 0.032 at a large national under the process-specific central setting (hybrid). It is 0.039 there under process-specific low, and at most 0.043 at any archetype (hybrid, m = 1 or process-specific low, community foundations) [S]. [V wave 38B]
   - Whether routing beats assistance depends on whether high-m errors can escape. Where an escaped error is a real AML miss with bank-style enforcement, E15's at most 0.39% miss rate per auto-closed alert costs about 0.0039 × 12,700 ≈ **49 handling units per AI-closed alert** at the conditional median. That rules out auto-closing [C].
   - DAF sponsors face no SAR regime, so that case applies to them only by analogy [I].

---

## 2. Method

### 2.1 Retrieval and robots.txt

- Every fetch used one helper with the generic user agent `research-script/1.0`. It read the host's robots.txt with `urllib.robotparser`, logged the result, and fetched only when access was allowed.
- Nothing was fetched from sec.gov, crt.sh or certspotter. No login or form was used.
- Discovery used FinCEN's enforcement-action index and one web search, used only to locate the OCC Bank of America release URL. Every number comes from the fetched primary document.

| Host | robots.txt | Fetched |
|---|---|---|
| www.fincen.gov | 200; allowed (only `/core`, `/profiles` assets and admin paths listed) | Enforcement-action index; all 18 FinCEN orders 2021-01 to 2026-03; BofA news release. The TD PDF timed out on the robots check once and was retried successfully |
| www.occ.gov | 200, but the body is an HTML page with no directives, treated as allowed | NR 2024-116 (TD) and NR 2026-89 (BofA). **The order PDF `eaAA-ENF-2026-41.pdf` returned the same HTML page, not the order (not used).** The release index URLs returned 404 |
| www.federalreserve.gov | 404, treated as allowed | TD press release and order PDF (enf20241010a1.pdf) |
| www.law.cornell.edu | 200, allowed | 26 U.S.C. §4966, §4967 |

### 2.2 Inclusion rule

- **Included:** 2021+ FinCEN, OCC or Federal Reserve BSA/AML orders that state **both** a penalty **and** a numeric count of missed or late SARs, of transactions on which a SAR should have been filed, or of missed alerts.
- **Excluded:** orders that give only "hundreds", "dozens" or no count. They are listed in the CSV as `record_type=excluded`.
- Counts are taken with the order's own qualifier ("nearly", "over", "at least"). Per-unit costs from "over" and "at least" counts are therefore upper bounds.

### 2.3 What each agency source states [F]

| Order | Penalty | Count stated | Kind |
|---|---|---|---|
| FinCEN 2026-03, Bank of America, N.A. (13 Oct 2026; 2018–Jul 2025) | $1.2bn CMP; $750m OCC credited; $450m to Treasury | "failed to identify and file nearly 8,900 SARs, with transaction activity totaling nearly $4 billion"; separately, a one-time review led to "filing over 8,000 SARs totaling approximately $3.96 billion" | missed SAR (lookback) |
| FinCEN 2024-02, TD Bank (10 Oct 2024; 2012–May 2024) | $1.3bn CMP; $543m credited (DOJ, OCC). The order also states ~$1.89bn DOJ, $123.5m FRB and $450m OCC | "willfully failed to timely file over 6,000 SARs"; "thousands of suspicious transactions totaling approximately one and a half billion dollars" unfiled; "over 150 alerts" not generated | late SAR |
| FinCEN 2022-01, USAA FSB (17 Mar 2022; 2016–Apr 2021) | $140m CMP; $60m OCC credited | "at least 3,873 SARs" filed late, averaging 226 days; "around 90,000 un-reviewed alerts and 6,900 un-reviewed cases" | late SAR; un-reviewed alerts |
| FinCEN 2021-03, CommunityBank of Texas (16 Dec 2021; 2015–2019) | $8m CMP; $1m OCC credited | "failed to file at least 17 SARs" | missed SAR |
| FinCEN 2023-03, Shinhan Bank America (29 Sep 2023) | $15m CMP; $5m FDIC credited | "several hundred SARs" late (no number); "468 alerts" that the new system failed to generate in parallel testing | alerts not generated |
| FinCEN 2023-02, Bancrédito (15 Sep 2023) | $15m | "over 300 transactions" found suspicious and belatedly reported | SAR-transactions |
| FinCEN 2026-01, Canaccord Genuity (6 Mar 2026), broker-dealer | $80m ($5m suspended; $40m SEC/FINRA credited) | "at least 160 SARs" (preliminary lookback) | missed SAR |
| FinCEN 2021-02, BitMEX (10 Aug 2021), FCM | $100m | "at least 588 transactions on which BitMEX should have filed a SAR" | SAR-transactions |
| FinCEN 2023-04, Binance (21 Nov 2023), MSB | $3.4bn | "well over a hundred thousand suspicious transactions" | SAR-transactions |
| OCC NR 2024-116 (TD) and NR 2026-89 (BofA) | $450m; $750m | No count: "numerous violations"; "large numbers of late suspicious activity reports" | — |
| Federal Reserve, TD (10 Oct 2024) | $123.5m | No SAR or alert count in the order | — |

**Excluded for lack of a count [F]:**
- Capital One 2021 ($390m). Its counts are 50,000+ CTRs and 75 alerts on one customer group, not SARs.
- Kingdom Trust 2023, Paxful 2025 and UBS 2026 ("hundreds").
- Lake Elsinore 2024 ("dozens").
- Brink's 2025 (filed no SARs; no count).
- Bittrex 2022, A&S World Trading 2022 and Asre 2024.

### 2.4 Conversion to handling units [C]

- m = allocation × P(detected and penalised) × (USD per escaped error) ÷ (USD handling cost of one case).
- Handling cost = minutes × loaded rate ÷ 60, from `ai-process-economics.csv`, the same inputs the calibrated and routing models use:
  - P14 AML alerts: 5 / 15 / 40 min × $55.45/h = **$4.62 / $13.86 / $36.97**.
  - P07 due diligence: 90 min = **$83.18**.
  - P08 prohibited-benefit review: 25 min = **$23.10**.
- The bank anchor uses the DAF model's P14 case as its unit. The units therefore remain the model's own. A bank investigator's real time per alert is not used.

### 2.5 Assumptions [I], all swept

| Assumption | Values | Why |
|---|---|---|
| Penalty allocation to the missed SARs | 0.25 / 0.5 / 1.0 | The orders also penalise program, CDD, correspondent and CTR failures. Penalty above the per-SAR statutory maximum (Canaccord 175%) shows that part of the penalty cannot be SAR-driven |
| P(escaped error detected and penalised) | 0.01 / 0.1 / 1.0 | **No source.** Every per-SAR figure is conditional on an enforcement action having happened. Most missed SARs at most banks never lead to one |
| BofA lookback duration | 0.5 / 1 / 2 years × 2,080 h × 800 consultants | The order states 800 consultants and no duration. Hours are priced at the P14 rate, which is a lower bound for consultants |
| Ongoing remediation | Excluded from m | BofA's "incremental 750" staff for "16,000 U.S. investigations each month" is the cost of reviewing at a correct threshold. In the routing model it is the review cost that routing avoids, not a cost of an escaped error |
| Bank-to-DAF transfer, P01/P14 | 0 / 0.01 / 0.1 | DAF sponsors are not BSA SAR filers (§5) |
| Operational-error m, other processes | 1 / 2 / 5 | At least one handling unit of rework (the model's convention for sampled errors), up to five with donor or charity contact. **No source** |
| Correction after a compliance error is found | +1 unit | Model convention |

**DAF compliance m (P07, P08)** = P(detected and taxed) × tax ÷ handling cost + 1.
- P07: tax = 20% × grant (§4966(a)(1), paid by the sponsor).
- P08: tax = min(10% × benefit, $10,000) (§4967(a)(2), paid by the fund manager). The benefit is bounded by the grant.
- The 125% tax on the donor or advisor (§4967(a)(1)) and the 5% manager tax under §4966 are not sponsor costs, so they are excluded. By the same rule the §4967(a)(2) tax used for P08 is not a sponsor cost either: §4967 taxes only the advisor or related person and a fund manager who agreed “knowing” the benefit, and nothing falls on the sponsoring organization. P08 is kept only as a proxy for exposure through the sponsor’s managers. With P08 at its correction unit alone, the composite m is 2.20 (central) and 88.5 (high), not 2.42 and 106 [C]. [V wave 38B]
- **Grant anchors already in the repo:**
  - DAFgiving360 median $500; JCF NY median $750 (both [F] in the repo).
  - Fidelity ≈ $5.1k, Vanguard $11.4k and NPT $40k means (v2 anchors).

**Composite single m** = Σ_p w_p·m_p over P01–P15.
- w_p is the AI-amenable pool share: v1 base pool × ai_amenability.
- The compliance set P01, P07, P08 and P14 carries **49.3%** of the weight. P07 alone carries 35.1%.

| Setting | P(detect) | Grant | Operational m | Transfer | Allocation |
|---|---|---|---|---|---|
| low | 0.01 | $500 | 1 | 0 | 0.25 |
| central | 0.1 | $5,100 | 2 | 0.01 | 0.5 |
| high | 1.0 | $40,000 | 5 | 0.1 | 1.0 |

**Rerun.**
- Run under CAL_CENTRAL for all six archetypes and CAL_COMPLIANCE_FULL for the large national.
- Route at m ∈ {0, 1, 2, 5, 10, 20, 30, 50, 100}; hybrid at m ∈ {1, 5, 20}; route at each composite m.
- A **process-specific** variant uses each process's own m_p. It reuses `rv.c_value` and `rv.per_case_yield` unchanged.

---

## 3. Results: bank side

### 3.1 Dollars and handling units per escaped error [C]

| Order | USD per unit (FinCEN CMP) | Share of per-SAR statutory max | m, conditional, allocation 1 (P14 low / base / high handling) |
|---|---:|---:|---|
| BofA 2026, missed SARs | 134,831 | 0.47 | 29,179 / **9,726** / 3,647 |
| BofA 2026, SARs filed in review | 150,000 | 0.52 | 32,462 / 10,821 / 4,058 |
| TD 2024, late SARs | 216,667 (all agencies 536,750) | 0.78 | 46,889 / **15,630** / 5,861 |
| USAA 2022, late SARs | 36,148 | 0.14 | 7,823 / **2,608** / 978 |
| USAA 2022, un-reviewed alerts | 1,556 | — | 337 / **112** / 42 |
| CBOT 2021, missed SARs | 470,588 | — | 101,841 / **33,947** / 12,730 |
| Shinhan 2023, alerts not generated | 32,051 | — | 6,936 / 2,312 / 867 |
| Bancrédito 2023, SAR-transactions | 50,000 | — | 3,607 (base) |
| Canaccord 2026, missed SARs | 500,000 | **1.75** | 36,069 (base) |
| BitMEX 2021, SAR-transactions | 170,068 | — | 12,268 (base) |
| Binance 2023, SAR-transactions | 34,000 | — | 2,453 (base) |

Range summaries:
- **Core depository (BofA, TD, USAA, CBOT):** $36,148–$470,588, median $175,749; 2,608–33,947 units, median 12,678.
- **All SAR-type counts:** $34,000–$500,000, median $152,450.
- **Per alert:** $1,556–$32,051.

- The CBOT figure shows the small-count problem: 17 SARs against an $8m penalty for a five-year program failure. At the $236,071 per-SAR cap stated in the CBOT order, the penalty is 1.99× the SAR-only statutory maximum, so like Canaccord it cannot be carried by the SAR violations alone [C]. [V wave 38B]
- The TD all-agency total ($3.22bn) is computed as FinCEN $1.3bn + DOJ $1.89bn + FRB $123.5m + OCC $450m − $543m credit. It may still double count where the DOJ amount includes forfeiture or credited items, so it is shown only as an alternative.

### 3.2 Expected bank m, core median [C on I]

| P(detected and penalised) \ allocation | 0.25 | 0.5 | 1.0 |
|---|---:|---:|---:|
| 0.01 | 32 | 63 | 127 |
| 0.1 | 317 | 634 | 1,268 |
| 1.0 | 3,170 | 6,339 | 12,678 |

Even the most lenient corner, 32, lies above routing's median break-even m (21.7).

### 3.3 Lookback labour, BofA [C on I]

800 consultants × duration × 2,080 h ÷ 8,900 SARs, in 15-minute P14 units:

| Duration | Units per missed SAR |
|---|---:|
| 0.5 yr | 374 |
| 1 yr | 748 |
| 2 yr | 1,496 |

At allocation 1 and P = 1 this adds 4–15% to the penalty-based 9,726. Its weight relative to the penalty grows as allocation falls, because a lookback is triggered once enforcement starts, whatever the penalty allocation.

---

## 4. Results: DAF side and proposed m

### 4.1 Process m from the excise regime [C on I]

P07 (20% sponsor tax on a taxable distribution, 90-minute case) and P08 (10% manager tax on a prohibited benefit, 25-minute case), each with one correction unit:

| Grant | P07, P = 0.1 | P07, P = 1 | P08, P = 0.1 | P08, P = 1 |
|---|---:|---:|---:|---:|
| $500 (DAFgiving360 median) | 1.12 | 2.20 | 1.22 | 3.16 |
| $750 (JCF median) | 1.18 | 2.80 | 1.32 | 4.25 |
| $5,100 (Fidelity mean) | 2.23 | 13.3 | 3.21 | 23.1 |
| $11,400 (Vanguard mean) | 3.74 | 28.4 | 5.93 | 50.3 |
| $40,000 (NPT mean) | 10.6 | 97.2 | 18.3 | 174 |

At P = 0.01 every cell is ≤ 1.97 (full grid in the CSV, `record_type=daf_m`).

### 4.2 Composite and process-specific m [I]

| Setting | P01 / P14 | P07 | P08 | Other processes | **Composite m** |
|---|---:|---:|---:|---:|---:|
| low | 1.00 | 1.01 | 1.02 | 1 | **1.01** |
| central | 7.34 | 2.23 | 3.21 | 2 | **2.42** |
| high | 1,269 | 97.2 | 174 | 5 | **106** |

**Proposed range for the routing model's m:**
- **1–106, central 2.4** [I], resting on IRC §4966/§4967 rates [F], grant anchors [F in repo] and the model's handling costs [C]. Of the central 2.42, only about 0.65 comes from the excise rates (0.43 from §4966 on P07, 0.22 from the manager-only §4967 tax on P08). The rest is 1.01 from the unsourced operational m = 2 on the 51% of weight outside compliance, 0.49 from correction units and 0.26 from the unsourced bank transfer. With operational m = 1 the composite is 1.91 [C]. [V wave 38B]
- Its width comes almost entirely from the detection probability and the bank-to-DAF transfer factor, neither of which has a source (P-G0403-04-01, -04).
- **Recommendation: report the process-specific variant, not a single m.** A single m spreads the compliance tail over the 51% of AI-amenable labour (P11 service inquiries, P03 complex assets and the rest) where an escaped error is ordinary rework.

### 4.3 Routing rerun [S]

Large national, CAL_CENTRAL (median sponsor AI gross value; mean P(C first, gross) over P01–P15):

| Cell | Pool p50 | P(C first) | P07 P(net > 0) | P(vendor break-even ≤ 5) |
|---|---:|---:|---:|---:|
| Assist (calibrated) | $444,899 | 0.0021 | 0.307 | 0.132 |
| Route m = 1 (replicates routing note) | $1,364,949 | 0.0123 | 0.635 | 0.378 |
| Route m = 2.42 (composite central) | $1,259,839 | 0.0089 | 0.608 | 0.351 |
| Route m = 5 | $1,062,284 | 0.0049 | 0.547 | 0.291 |
| Route m = 10 | $622,830 | 0.0026 | 0.380 | 0.173 |
| Route m = 20 (replicates) | $43,725 | 0.0014 | 0.190 | 0.086 |
| Route m = 30 / 50 / 100 | $0 | ≤ 0.0009 | ≤ 0.128 | ≤ 0.059 |
| Route m = 106 (composite high) | $0 | 0.0002 | 0.035 | 0.017 |
| Route, process-specific central | $1,249,027 | 0.0095 | 0.611 | 0.348 |
| Hybrid, process-specific central | $1,674,826 | 0.0318 | 0.710 | 0.452 |
| Route, process-specific high | $534,970 | 0.0030 | 0.037 | 0.102 |
| Hybrid, process-specific high | $753,432 | 0.0124 | 0.061 | 0.183 |

Other archetypes (CAL_CENTRAL, route; pool p50 for assist / m = 1 / composite central / process-specific high):

| Archetype | Assist | m = 1 | Composite central | Process-specific high |
|---|---:|---:|---:|---:|
| Mid national | $49k | $165k | $152k | $62k |
| $1bn community foundation | $69k | $191k | $177k | $73k |
| $250m community foundation | $18k | $48k | $44k | $18k |
| Community foundation, $10–100m | $2.4k | $7.1k | $6.5k | $2.7k |

- **CAL_COMPLIANCE_FULL, large national:** assist $386k; route m = 1 $985k; composite central $938k; process-specific high $844k (equal to m = 5, because compliance errors cannot escape when k = 1); single m = 106 $334k.
- At mid nationals and community foundations, the share of draws in which C clears its fixed cost in P07 is at most 6.8% (hybrid, m = 1 or process-specific low, $1bn community foundation). At the process-specific central setting it is 6.1%. In P14 it is 0 in every cell [S]. The `REF_V1_1M` reference archetype is in the CSV but not reported here.

**Which earlier conclusions change.**

| Earlier claim | Status |
|---|---|
| Routing note: "m remains unsourced"; routing pool falls below assist at m = 20 and is $0 at m = 50 | **Bounded.** The central m (2.4, mostly assumption-driven: §4.2) sits in the range where routing holds about 92% of its m = 1 pool at a large national. [V wave 38B] Any single m above ~20 still erases it. Bank-style enforcement (m in the thousands) erases it in any process where such errors can escape |
| BD recut: "the BofA order suggests escaped-error costs in compliance can be very large" | **Confirmed and quantified.** Conditional on enforcement: 2,600–34,000 units per missed SAR at the core banks, plus 374–1,496 for lookback labour |
| Assistance modal nowhere; routing's advantage hinges on m | **Unchanged / refined.** The advantage survives every setting under which high-m errors are confined to compliance processes, or caught by full re-review |

---

## 5. Transfer from bank SAR penalties to DAF grant compliance [I]

- **Different legal regime.**
  - A bank's escaped AML error is a willful BSA reporting violation. FinCEN may impose up to the greater of the transaction amount (capped at $286,184) or $71,545 per SAR violation [F, BofA order]. The bank's regulator can add cease-and-desist orders and asset caps (OCC, TD).
  - A DAF sponsor is a charity, not a BSA "financial institution" with a SAR duty. Its escaped grant-compliance error is an excise-tax event:
    - 20% of a taxable distribution, on the sponsor (§4966);
    - 125% of a prohibited benefit, on the advisor, and 10% (capped at $10k) on the manager (§4967).
  - These taxes scale with the grant (hundreds to tens of thousands of dollars), not with the program. Per error they are therefore two to four orders of magnitude below bank SAR penalties.
- **Detection differs.** Bank SAR failures are found by prudential examiners who sit in the bank, then priced at the program level. DAF taxable distributions surface through IRS examination of Forms 990 and 4720, or through press and donor complaints. The repo has no 2021+ figure for the IRS assessment rate (P-G0403-04-01). That gap is why P is swept from 0.01 to 1. [g0403-0104-m-detection-ofac.md](g0403-0104-m-detection-ofac.md) fills it: IRS exams reach 0.12%–0.30% of e-filed 990/990-EZ returns a year (FY2021–25), and at most 15 returns a year report the sponsor §4966 tax (CY2021–24). That puts P at about 0.0012–0.0099, which is average-filer exam coverage rather than a strict ceiling [C/I] [V wave 39B]
- **Grant clawback.** Recovering a grant made in error costs staff time and recipient goodwill, not a penalty multiple. It is represented here only as one correction unit plus the operational m (1–5). The repo has no source on clawback frequency or effort (P-G0403-04-05).
- **Sponsor reputation.** This is the channel through which a DAF error could approach bank-scale cost: loss of donor accounts, a state attorney-general action, or press coverage of a grant to a hate group or a sanctioned party. No 2021+ source quantifies it per error, so it sits only in the "high" transfer setting.
- **Where the bank analogy is closest:**
  - P14 (fraud, AML and sanctions screening) and P01 (KYC on donors and assets). Sanctions violations carry strict-liability OFAC penalties that apply to charities; P-G0403-04-04 proposes collecting OFAC 2021+ releases.
  - Large nationals that operate as, or alongside, a broker-dealer or bank affiliate. The affiliate's AML program then covers the donor relationship.
- **Net.** Bank SAR penalties are an **upper envelope** for DAF P01/P14, not an estimate. For P07/P08 the excise regime gives a direct, if detection-dependent, figure.

---

## 6. Limits

1. **Small n.** Four depository orders state SAR counts. Their per-SAR penalty spans 13× (USAA to CBOT), and the small-count order (CBOT, 17 SARs) sets the top.
2. **Counts are lower bounds** ("over", "at least", "preliminary"). TD's late-SAR count excludes the "thousands" of unfiled transactions, so per-unit figures overstate the cost per error.
3. **Allocation and detection probability are unsourced** and drive expected m one-for-one.
4. **Lookback duration and consultant cost** are not stated in the BofA order. The OCC order PDF could not be retrieved (HTML returned).
5. **Penalty is not the only bank cost.** TD's OCC asset cap and the reputational and market costs are not monetised here.
6. **The handling unit is the DAF model's.** Using a bank investigator's time per alert would change the bank m by the ratio of handling costs. The three P14 handling levels give a 2.7–8× band.
7. **Single-m structure.** The routing model applies one m to all processes. The process-specific variant addresses this, but it sits outside the imported module's own main loop. It uses only that module's pure functions.
8. **Grant anchors are means or medians.** Taxable distributions may be larger or smaller than typical grants. Foreign and non-501(c)(3) grants in P07 are probably larger than the median.

---

## 7. Data dictionary: `escaped-error-cost-2026-11-19.csv`

| Column | Meaning |
|---|---|
| record_type | `meta`; `order` (one included order); `excluded` (2021+ order or agency source without a usable count); `range` (summary across orders); `bank_m_grid` (expected bank m by allocation × P); `lookback` (BofA lookback units by duration); `daf_m` (P07/P08 m by grant × P); `weights` (AI-amenable pool share by process); `composite` (process m and weighted m for low/central/high); `breakeven_m` (per-draw m at which an AI-closed case saves nothing, and share of draws above it); `route` (routing rerun summaries) |
| id | Order id (e.g. `BOFA_2026`), setting name, grid cell, or `scenario\|archetype\|variant\|cell` for `route` rows. Route cells: `m=<x>` (single m), `composite_<setting>_m=<x>`, `process_specific_<setting>` (m_p by process), `calibrated` (assist) |
| entity | Institution, grant anchor or blank |
| metric | e.g. `fincen_cmp_usd`, `count`, `usd_per_unit_fincen`, `usd_per_unit_all_agency`, `fincen_cmp_share_of_per_sar_statutory_max`, `m_conditional_full_alloc_hc_{low,base,high}`, `m_expected`, `m_<Pxx>`, `m_weighted_P01_P15`, `sponsor_ai_gross_value_p50`, `mean_p_C_rank_first_gross_P01_P15`, `P07_p_C_net_positive`, `p_vendor_breakeven_le_available` |
| value | Number (USD, count, ratio, handling units or probability per `unit`) |
| unit | Unit; for `count` rows, the count kind (`missed_sar`, `late_sar`, `sar_transactions`, `unreviewed_alerts`, `alerts_not_generated`) |
| basis | F / C / I / C+I / S (notation above) |
| assumption | The assumption values behind the row |
| source | Primary URL(s); for repo-derived anchors, the repo file |
| note | Order quote and qualifier, period, credits, caveats, or p25/p75 for pools |

---

## 8. Source register

| Ref | Source | URL |
|---|---|---|
| S01 | FinCEN Consent Order 2026-03, Bank of America, N.A. (13 Oct 2026) | https://www.fincen.gov/system/files/2026-10/BoA-Consent-Order-Execution-Final.pdf |
| S02 | FinCEN news release, "FinCEN Assesses $1.2 Billion Penalty against Bank of America" | https://www.fincen.gov/news/news-releases/fincen-assesses-12-billion-penalty-against-bank-america |
| S03 | OCC NR 2026-89, $750m CMP against Bank of America | https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-89.html |
| S04 | FinCEN Consent Order 2024-02, TD Bank (10 Oct 2024) | https://www.fincen.gov/system/files/enforcement_action/2024-10-10/FinCEN-TD-Bank-Consent-Order-508FINAL.pdf |
| S05 | OCC NR 2024-116, TD Bank $450m CMP | https://www.occ.gov/news-issuances/news-releases/2024/nr-occ-2024-116.html |
| S06 | Federal Reserve Board, TD $123.5m (release; order PDF) | https://www.federalreserve.gov/newsevents/pressreleases/enforcement20241010a.htm ; https://www.federalreserve.gov/newsevents/pressreleases/files/enf20241010a1.pdf |
| S07 | FinCEN Consent Order 2022-01, USAA FSB | https://www.fincen.gov/system/files/enforcement_action/2023-04-05/USAA_Consent_Order_Final_508_2.pdf |
| S08 | FinCEN 2021-03, CommunityBank of Texas | https://www.fincen.gov/system/files/enforcement_action/2023-04-05/CBOT_Enf_Action_121621_508_FINAL.pdf |
| S09 | FinCEN 2023-03, Shinhan Bank America | https://www.fincen.gov/system/files/enforcement_action/2023-09-29/SHBA_9-28_FINAL_508.pdf |
| S10 | FinCEN 2023-02, Bancrédito | https://www.fincen.gov/system/files/enforcement_action/2023-09-15/Bancredito_Consent_FINAL_091523_508C.pdf |
| S11 | FinCEN 2026-01, Canaccord Genuity | https://www.fincen.gov/system/files/2026-03/Canaccord-Consent-Order-No-2026-01.pdf |
| S12 | FinCEN 2021-02, BitMEX | https://www.fincen.gov/system/files/enforcement_action/2021-08-10/Assessment_BITMEX_508_FINAL_0.pdf |
| S13 | FinCEN 2023-04, Binance | https://www.fincen.gov/system/files/enforcement_action/2023-11-21/FinCEN_Consent_Order_2023-04_FINAL508.pdf |
| S14 | FinCEN 2021-01, Capital One (excluded) | https://www.fincen.gov/system/files/enforcement_action/2023-04-05/Assessment_CONA_508_0.pdf |
| S15 | FinCEN 2023-01 Kingdom Trust; 2025-02 Paxful; 2026-02 UBS; 2024-03 Lake Elsinore; 2025-01 Brink's; 2022-03 Bittrex (excluded) | URLs in CSV `record_type=excluded` |
| S16 | FinCEN enforcement-action index | https://www.fincen.gov/news/enforcement-actions/ |
| S17 | 26 U.S.C. §4966 | https://www.law.cornell.edu/uscode/text/26/4966 |
| S18 | 26 U.S.C. §4967 | https://www.law.cornell.edu/uscode/text/26/4967 |
| S19 | DAFgiving360 FY2026 results (median grant $500), via repo | https://www.dafgiving360.org/press-release/fiscal-year-2026-results |
| S20 | JCF NY 2023 Giving Report (median grant $750), via repo | https://jcfny.org/app/uploads/2024/04/2023-JCF-Giving-Report.pdf |
| — | Model inputs: handling minutes and rates (`ai-process-economics.csv`); v2 grant anchors ([ai-economics-v2-observed-costs.md](ai-economics-v2-observed-costs.md)); calibration ([gap19-ai-calibration.md](gap19-ai-calibration.md)); routing ([g0401-g0502-ai-routing-and-per-grant.md](g0401-g0502-ai-routing-and-per-grant.md)); BofA citation and wave-37C corrections ([g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md), [validation-wave37c-report.md](validation-wave37c-report.md)) | Repo |
