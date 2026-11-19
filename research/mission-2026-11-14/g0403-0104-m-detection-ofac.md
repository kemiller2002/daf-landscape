# Escaped-error cost m: IRS detection probability and the OFAC analogue

*Queue items P-G0403-04-01 and P-G0403-04-04 (task g0403-0104). Prepared 2026-11-19.*

- **Builds on:** [g0403-04-escaped-error-cost.md](g0403-04-escaped-error-cost.md), with its wave-38B corrections. The central composite m is about **2.20**, not 2.42. P08 counts only its correction unit, because §4967 puts no tax on the sponsor. P(detected and taxed) was an unsourced sweep from 0.01 to 1.
- **Script:** [`scripts/mission_m_detection_ofac.py`](../../scripts/mission_m_detection_ofac.py). It imports `scripts/mission_escaped_error_cost.py` without modifying it and reuses that module's `m_daf`, `handling_cost`, `weights`, `range_rows`, `eval_draw_pm`, `row` and `write_csv`. Through it, the script also uses the routing variant and the calibrated model (seed 42; routing stream 42 + 104729). It uses only the standard library and is written in a functional style.
  - Run: `python3 scripts/mission_m_detection_ofac.py . --route` (about 25 s).
  - Add `--efile-dir DIR` to recount the IRS e-file index files.
- **Data:** [`data/mission-2026-11-14/m-detection-ofac-2026-11-19.csv`](../../data/mission-2026-11-14/m-detection-ofac-2026-11-19.csv) (385 rows).
- **Queue proposals:** [`data/mission-2026-11-14/queue-proposals-g0403-0104.csv`](../../data/mission-2026-11-14/queue-proposals-g0403-0104.csv) (6 rows).
- **Replication checks:**
  - The wave-38B corrected baseline recomputes to a composite m of **2.196** (central) and **88.48** (high). This matches the corrected 2.20 and 88.5.
  - The route pool at m = 1 is **$1,364,949**, identical to the routing note and the escaped-error CSV.
  - The e-file recount from the IRS index files equals the embedded counts in all 15 cells.

**Notation:** [F] quoted from a primary source; [C] computed; [I] inference or assumption; [S] scenario output.

---

## 1. Bottom line

1. **An escaped DAF compliance error is detected and taxed with probability about 0.1%–1% a year, not 1%–100%.** The bounded settings are P = **0.00115 / 0.00185 / 0.0099** (low / central / high) [C].
   - The IRS examined **666–1,383** Form 990/990-EZ/990-N returns a year in FY2021–FY2025 (Data Book Table 3-5) [F]. That is **0.12%–0.29%** of e-filed 990 and 990-EZ returns, and **0.04%–0.10%** of recognized 501(c)(3) organizations [C].
   - Counting every TE/GE Exempt Organizations filing examined, including related employment and excise returns, coverage is **0.28%–0.56%** [C].
   - At most **15** returns a year report the sponsor's §4966 tax (SOI Form 4720 study, CY2021–CY2024: 7, 15, 10, 6) [F]. Against the 1,512 DAF sponsors in the repo, that is **0.40%–0.99%** of sponsors a year [C].
   - The old sweep's lowest value (0.01) therefore sits at the top of the evidence. The old central value (0.1) is about 50 times the median exam rate.
2. **The §4966 sponsor tax raises only about $0.1m–$1.2m a year in total** ($112,913; $179,819; $1,150,071; $101,894 for CY2021–CY2024) [F].
   - That is **$12k–$115k per reporting return**, implying taxable distributions of about $60k–$575k each at the 20% rate [C].
   - For CY2025 the IRS deleted the cell to avoid disclosure. It is bounded at **≤ $264,759**, a residual shared with three other suppressed rows [C].
   - Individual-level taxes are "not available" from SOI. These are the §4966 manager tax and the §4967 taxes on donors, advisors and managers [F]. **No count of §4967 assessments is published in any source checked.**
3. **With the bounded P, P07's escaped-error m falls from 2.23 to 1.02** (central, $5,100 grant). At the high setting ($40k grant) it falls from 97.2 to **1.95** [C]. The §4966 excise channel is close to negligible in expectation.
4. **Composite m (central), down from 2.20 [C+I]:**
   - **1.77** when P01/P14 keep the wave-38B bank-SAR transfer.
   - **1.56** when P01/P14 use the OFAC analogue.
   - **Composite m (high):** 55.0 with the bank transfer, and **9.3** with the OFAC analogue. The wave-38B high was 88.5.
   - Most of what remains comes from the unsourced operational m = 2 on the 51% of weight outside compliance.
5. **Charities and donor platforms: none [F].** No OFAC civil penalty or finding of violation from 2021 to 2026 YTD names a charity, foundation, DAF sponsor or donor platform; 87 release rows were read.
   - Eight releases involve payment processors, money transmitters, prepaid or rewards platforms, or a card issuer. Seven involve crypto exchanges or wallets.
6. **OFAC penalty per apparent violation, conditional on enforcement [C]:**
   - **Processors (n = 8):** $4.19–$2,012, median **$168.50**. In P14 handling units that is **0.3–145, median 12.2**.
   - **Crypto (n = 7):** $43.65–$12,218, median $438.
   - These amounts are 2–3 orders of magnitude below the bank-SAR median of $175,749 (12,678 units). As a sanctions-screening analogue for P01/P14 at a DAF sponsor, they are the nearest regime [I].
7. **One case shows how pricing per missed alert changes the result [C].** In Amex 2022, a single "high confidence" alert was "erroneously closed" by an analyst, and 214 violations followed. The penalty was $430,500 per missed alert, or **31,055 handling units**.
   - An AI that auto-closes a true sanctions match is that case. Per-violation pricing (median 12 units) suits volume-type geolocation misses, but not a missed true match.
8. **Routing rerun (large national, CAL_CENTRAL) [S]:**
   - The route pool is **$1.31m** at the IRS-bounded central m and **$1.32m** with the OFAC analogue. It was $1.27m at m = 2.2.
   - Hybrid routing with process-specific central m reaches **$1.73m–$1.75m**.
   - At process-specific high, route is **$1.11m** (it was $634k with the wave-38B-corrected high).
   - Assistance is unchanged at $445k. Bounding P strengthens routing at compliance processes and does not change the ranking conclusion: C's mean rank-first probability is ≤ 0.035 in every cell.

---

## 2. Method

### 2.1 Retrieval and robots.txt

- One helper fetched every file with user agent `research-script/1.0`. It read robots.txt with `urllib.robotparser`, fetched only allowed URLs and logged every request (70 log lines in the session scratchpad).
- Discovery used two web searches, for the TE/GE program letter and for TIGTA EO reports. No figure is taken from a search snippet.
- Nothing was fetched from sec.gov, crt.sh or certspotter. No login or form was used.

| Host | robots.txt | Result |
|---|---|---|
| www.irs.gov | 200; disallows `/core/`, `/profiles/`, search paths, admin and some language node paths | Allowed: Data Book pages and xlsx (Tables 1-2, 2-6, 3-5, FY2021–FY2025), SOI Form 4720 tables (CY2021–2025), Pub 6038, TE/GE letters (Pub 5313, 5329), compliance-strategy pages, Form 990 downloads page. `p5329.pdf` returned 404 at both `system/files/irs-pdf/` and `pub/irs-pdf/`; the FY2024 letter came from `pub/irs-access/p5329_accessible.pdf` |
| apps.irs.gov | robots.txt request returned 302 (no file) | E-file index CSVs (2021–2025). Local copies fetched 2026-11-14 by an earlier task were recounted, not re-downloaded |
| www.tigta.gov | 200; disallows only `/search/`, `/pagefind/`, `/index.json` | TIGTA 2026-1S0-042, 2024-100-040, 2026-3S0-045, 2025-308-030 |
| www.gao.gov | **403 on robots.txt (Akamai "Access Denied")** | **Not fetched.** No GAO report was used (P-G0403-0104-02) |
| www.oversight.gov | 406 on robots.txt | Not fetched (TIGTA's own host was used instead) |
| ofac.treasury.gov | 200; disallows admin, search, `/core/`, `/profiles/`, oembed | Enforcement index (2026 YTD), 2021–2025 year pages, 15 enforcement-release PDFs (`/media/<id>/download?inline`) |
| home.treasury.gov | 200; `Allow: /` | Checked; not needed (OFAC releases are on ofac.treasury.gov) |

### 2.2 Detection probability (A)

- **Definition.** P is the probability that an escaped compliance error, here a §4966 taxable distribution, is detected by the IRS and taxed. A sponsor that finds its own error and self-reports it has not let the error escape; that case belongs to the correction unit, not to P.
- **Channel.** For an escaped error the main route to a tax is an IRS examination of the sponsor's return. P = c × q:
  - c is the yearly exam coverage of the filer population;
  - q is the probability that an exam finds and taxes the specific error.
  - **q is set to 1**, so every P here is an upper bound on this channel [I]. Press, whistleblower and state AG detection are not quantified.
- **Coverage measures [C]:**
  - *Narrow:* Data Book "Forms 990, 990-EZ and 990-N" returns examined ÷ e-filed 990 + 990-EZ (IRS e-file index, same processing year). The numerator includes 990-N exams and the denominator does not, which slightly overstates the rate.
  - *Per 501(c)(3):* the same numerator ÷ recognized 501(c)(3) organizations (Data Book Table 2-6). This understates the rate, because the denominator includes 990-N filers and churches.
  - *Broad:* TE/GE Exempt Organizations "filings" examined (Accomplishments Letters FY2021–24; FY2025 = FY2021 × 0.85 from TIGTA's "15 percent fewer") ÷ e-filed 990 + 990-EZ + 990-PF. This overstates the rate, because related employment and excise returns are counted as filings.
- **Incidence cross-check [C on I].** The maximum yearly count of returns reporting the sponsor §4966 tax is divided by the 1,512 DAF sponsors. If every sponsor had at least one escaped taxable distribution a year, P could not exceed this ratio.
- **Settings:**
  - **low:** minimum narrow rate (FY2024).
  - **central:** median narrow rate (FY2023).
  - **high:** the larger of the maximum broad rate and the incidence ratio (0.0099).

### 2.3 OFAC analogue (B)

- **Scope.** Every row on OFAC's 2021–2026 civil-penalty pages was read: 19, 16, 16, 12, 14 and 10 rows, 87 in all. Two groups were included:
  - **processor:** payment processor, money transmitter, prepaid or rewards platform, payments subsidiary, card issuer;
  - **crypto:** virtual-currency exchange or wallet. DAF sponsors take crypto gifts through such platforms.
- **Excluded:** banks acting as banks (TD 2021, Wells Fargo 2023 and others), and non-financial exporters.
- For each included release, the following were quoted from the release PDF: penalty, apparent-violation count, violating value, statutory maximum, base penalty, voluntary self-disclosure and egregiousness.
- **Counts.** Where the release states a total, that total is used. For Airbnb (3,464 + 3,076 extrapolated, plus 44 confirmed) and ShapeShift (39 + 16,839 + 33 + 272 = the release's "17,183 instances"), the stated parts are summed.
- **Conversion.** USD per violation = penalty ÷ count. Handling units = that ÷ the P14 base handling cost (15 min × $55.45/h = $13.86), the same unit as the escaped-error note.
- **m for P01/P14 under the OFAC analogue:** P_OFAC × USD per violation ÷ $13.86 + 1 correction unit. The settings are low (processor minimum, P_OFAC 0.01), central (processor median, 0.1) and high (processor maximum, 1.0). **P_OFAC has no source** [I].

### 2.4 Recomputed m (C)

- The settings come from the escaped-error note (grant $500 / $5,100 / $40,000; operational m 1 / 2 / 5; bank transfer 0 / 0.01 / 0.1; allocation 0.25 / 0.5 / 1).
- P07 uses the bounded P. P08 is held at its correction unit (wave 38B). There are three variants:
  - **w38b_baseline:** the wave-38B corrected composite, as a replication check.
  - **irs_bounded:** P07 uses the IRS-bounded P; P01/P14 keep the wave-38B bank-SAR transfer term.
  - **irs_bounded_ofac:** as irs_bounded, but P01/P14 use the OFAC analogue.
- Weights are the AI-amenable pool shares from `ee.weights`, with P07 at 35.1%.
- The rerun covers the large-national CAL_CENTRAL archetype only.

---

## 3. Results: detection probability (A)

### 3.1 IRS examinations of exempt-organization returns [F] and coverage [C]

| FY | 990/EZ/N examined | 990-PF etc. examined | Form 4720 examined | EO filings examined (TE/GE) | e-filed 990 + 990-EZ | 501(c)(3) orgs | Narrow rate | Per 501(c)(3) | Broad rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2021 | 1,383 | 203 | 301 | 3,249 | 469,208 | 1,431,266 | 0.295% | 0.097% | 0.562% |
| 2022 | 1,343 | 170 | 292 | 3,425 | 515,245 | 1,480,565 | 0.261% | 0.091% | 0.542% |
| 2023 | 1,029 | 81 | 231 | 2,464 | 557,294 | 1,514,558 | 0.185% | 0.068% | 0.361% |
| 2024 | 666 | 72 | 210 | 1,955 | 578,455 | 1,548,798 | 0.115% | 0.043% | 0.277% |
| 2025 | 889 | 77 | 188 | 2,762 [C] | 594,022 | 1,596,231 | 0.150% | 0.056% | 0.381% |

- **Exam outcomes.** TE/GE change rates on closed EO exams were 82.3% / 77.5% / 75.7% / 74.5% (FY2021–24) [F]. An exam usually changes something, but whether it touches a specific grant is not reported.
- **Form 4720 exams.** These fell from 301 to 188 a year. They cover all charities, private foundations and related persons, so they cap exam-generated §4966/§4967 assessments at a few hundred returns a year across all chapter-42 taxes [C].
- **No DAF-specific compliance strategy.** None of TE/GE's in-process compliance strategies (read 2026-11-19) targets DAFs or sponsoring organizations. The exempt-organization strategies cover loans to disqualified persons, NIL, government grant abuse, hospitals, corporate jets, **"Addressing Illicit Financing Activities by Exempt Organizations"** and employment-tax items [F]. Nor does the FY2027 program letter (Pub 5313) mention DAFs. Its only "donor" mention concerns the new scholarship tax credit [F].
- **Direction of travel.** TIGTA (2026-1S0-042) reports that EO "completed fewer examinations in FY 2025 compared to FY 2021, by 15 … percent". It also reports 723 TE/GE employees taking deferred resignation in FY2025, whose loss "will likely affect future goals" [F]. Coverage is therefore not rising.

### 3.2 §4966 sponsor tax reported on Form 4720 (SOI) [F] and derived figures [C]

| CY | Returns with sponsor §4966 tax | Tax (USD) | Per return | Implied distribution per return (÷ 0.20) | Share of 1,512 sponsors |
|---|---:|---:|---:|---:|---:|
| 2021 | 7 | 112,913 | 16,130 | 80,652 | 0.46% |
| 2022 | 15 | 179,819 | 11,988 | 59,940 | 0.99% |
| 2023 | 10 | 1,150,071 | 115,007 | 575,036 | 0.66% |
| 2024 | 6 | 101,894 | 16,982 | 84,912 | 0.40% |
| 2025 | d (suppressed) | ≤ 264,759 (residual) | — | — | — |

- **Scale against all Form 4720 tax.** Total organizational tax on Form 4720 was $291m–$995m a year. The §4966 sponsor tax is **0.01%–0.12%** of it [C].
- **Reading the counts.** SOI counts returns filed, which mixes self-reported and exam-assessed tax. Individual taxes, including §4967 and the §4966(a)(2) manager tax, are "not available" [F].
- **Tax events per grant.** Fifteen taxed sponsor returns in the peak year, set against Fidelity Charitable's "nearly 2.7 million" grants in 2024 alone, is **5.6 × 10⁻⁶ taxed events per grant**. That is an industry-wide upper bound, because other sponsors' grants would only enlarge the denominator [C].

### 3.3 Bounded P and its effect on DAF process m [C]

| Setting | P(detected and taxed) | Source of bound | m_P07 ($500) | m_P07 ($5,100) | m_P07 ($40,000) |
|---|---:|---|---:|---:|---:|
| low | 0.00115 | min narrow rate (FY2024) | 1.001 | 1.014 | 1.11 |
| central | 0.00185 | median narrow rate (FY2023) | 1.002 | **1.023** | 1.18 |
| high | 0.0099 | 15 / 1,512 sponsors ≈ max broad rate | 1.012 | 1.12 | **1.95** |
| old sweep | 0.01 / 0.1 / 1 | none | — | 1.12 / 2.23 / 13.3 | 1.96 / 10.6 / 97.2 |

The P07 values here were computed with `ee.m_daf` (P07 handling 90 min × $55.45/h = $83.18). In the composite, each setting uses its own grant: $500, $5,100 or $40,000 [C].

---

## 4. Results: OFAC analogue (B)

### 4.1 Releases 2021–2026: processors and crypto platforms [F] with per-violation cost [C]

| Release | Group | Penalty (USD) | Violations | USD per violation | P14 units | Penalty ÷ violating value | Penalty ÷ base | VSD / egregious |
|---|---|---:|---:|---:|---:|---:|---:|---|
| BitPay, 2021-02-18 | processor | 507,375 | 2,102 | 241.38 | 17.4 | 3.93 | 0.23 | no / no |
| MoneyGram, 2021-04-29 | processor | 34,328.78 | 359 | 95.62 | 6.9 | — | 0.65 | yes / no |
| Payoneer, 2021-07-23 | processor | 1,385,901.40 | 2,220 | 624.28 | 45.0 | 1.75 | 0.36 | 19 of 2,220 / no |
| Airbnb Payments, 2022-01-03 | processor | 91,172.29 | 6,584 (sum) | 13.85 | 1.0 | — | 0.25 | yes / no |
| American Express National Bank, 2022-07-15 | processor (card issuer) | 430,500 | 214 | 2,011.68 | 145.1 | 2.77 | 0.75 | no / no |
| Tango Card, 2022-09-30 | processor (rewards) | 116,048.60 | 27,720 | 4.19 | 0.3 | 0.30 | 0.60 | yes / no |
| daVinci Payments, 2023-11-06 | processor (prepaid; non-profit clients) | 206,213 | 12,391 | 16.64 | 1.2 | 0.38 | 0.75 | yes / no |
| Uphold HQ, 2023-03-31 | processor (MSB) | 72,230.32 | 152 | 475.20 | 34.3 | 0.40 | 0.80 | yes / no |
| Kraken, 2022-11-28 | crypto | 362,158.70 | 826 | 438.45 | 31.6 | 0.22 | 0.43 | yes / no |
| Bittrex, 2022-10-11 | crypto | 24,280,829.20 | 116,421 | 208.56 | 15.0 | 0.09 | 0.05 | no / no |
| Poloniex, 2023-05-01 | crypto | 7,591,630 | 65,942 | 115.13 | 8.3 | 0.50 | 0.08 | no / no |
| CoinList, 2023-12-13 | crypto | 1,207,830 | 989 | 1,221.26 | 88.1 | 0.96 | 0.39 | no / no |
| Binance, 2023-11-21 | crypto | 968,618,825 | 1,667,153 | 581.00 | 41.9 | 1.37 | — | no / yes |
| ShapeShift, 2025-09-22 | crypto | 750,000 | 17,183 (sum) | 43.65 | 3.1 | 0.06 | 0.02 | no / no (defunct) |
| Exodus, 2025-12-16 | crypto | 3,103,360 | 254 | 12,217.95 | 881.4 | — | 0.65 | no / 12 of 254 |

| Group | Min | Median | Max | Median in P14 units |
|---|---:|---:|---:|---:|
| Processors (8) | $4.19 | **$168.50** | $2,011.68 | **12.2** |
| Crypto (7) | $43.65 | $438.45 | $12,217.95 | 31.6 |
| All (15) | $4.19 | $241.38 | $12,217.95 | 17.4 |

### 4.2 Reading the analogue [I]

- **Same legal exposure.** A DAF sponsor is a US person and is under the same strict-liability OFAC regime as these firms. The releases are therefore a closer analogue for P01/P14 than bank SAR orders, which rest on BSA duties the sponsor does not have.
- **Penalty scale.** Penalties scale with transaction value and count under the Enforcement Guidelines: half the transaction value per violation for non-egregious self-disclosed cases, or the schedule amount otherwise. Most processor penalties are **0.3–4 times the violating value**, so a sanctions miss on a $5,100 grant implies a few thousand dollars at most, conditional on enforcement.
- **Two kinds of miss.**
  - *Volume misses* (geolocation, many small transactions: Tango, daVinci, Airbnb) price at **$4–$17** per violation. They resemble a P14 rule that is mis-tuned.
  - *A missed true match* (Amex: one alert closed, $430,500) prices at **31,055 units per missed alert** [C], which is within the bank-SAR range.
  - A DAF sponsor's sanctions error is usually a single grant to a listed party, which is the second kind. For it the per-violation median understates the cost, unless the sponsor discloses voluntarily and the grant is small.
- **Enforcement odds.** OFAC issues 10–20 penalty releases a year across the whole economy, none of them against a charity in 2021–2026. P(enforcement | violation) for a DAF sponsor is therefore small, but no denominator is published (P-G0403-0104-03).

---

## 5. Recomputed m and routing rerun

### 5.1 Composite and process m [C+I]

| Variant | Setting | P07 | P08 | P01 / P14 | **Composite m** |
|---|---|---:|---:|---:|---:|
| w38b_baseline (replication) | low / central / high | 1.012 / 2.226 / 97.18 | 1 | 1.00 / 7.34 / 1,268.8 | 1.004 / **2.196** / 88.48 |
| irs_bounded | low / central / high | 1.001 / 1.023 / 1.954 | 1 | 1.00 / 7.34 / 1,268.8 | 1.000 / **1.773** / 55.03 |
| irs_bounded_ofac | low / central / high | 1.001 / 1.023 / 1.954 | 1 | 1.00 / 2.22 / 146.1 | 1.001 / **1.564** / **9.28** |

- **Proposed m for the routing model:** low 1.0, central **1.6–1.8**, high **9.3** with the OFAC analogue, or 55 if bank-SAR transfer is kept [I].
- **What remains of the central m:**
  - about 1.0 from the unsourced operational m = 2 on the 51% of weight outside compliance;
  - about 0.49 from correction units;
  - **0.008** from §4966 (P07);
  - 0.05 (OFAC) or 0.26 (bank transfer) from P01/P14 [C].
- The excise channel no longer matters. The only P01/P14 cost that could matter is the per-missed-alert OFAC case (§4.2), and that applies only where an AI may close a true sanctions match.

### 5.2 Routing rerun, large national, CAL_CENTRAL [S]

| Cell | Pool p50 | P(C first) |
|---|---:|---:|
| Assist (calibrated) | $444,899 | 0.0021 |
| Route m = 1 (replicates) | $1,364,949 | 0.0123 |
| Route m = 2.2 (wave-38B central) | $1,273,475 | 0.0095 |
| Route composite irs_bounded central (1.77) | $1,305,560 | 0.0103 |
| Route composite irs_bounded_ofac central (1.56) | $1,321,027 | 0.0109 |
| Route composite irs_bounded high (55.0) | $0 | 0.0005 |
| Route composite irs_bounded_ofac high (9.28) | $687,995 | 0.0027 |
| Route / hybrid, process-specific w38b central | $1,267,324 / $1,694,109 | 0.0096 / 0.0320 |
| Route / hybrid, process-specific irs_bounded central | $1,297,172 / $1,729,866 | 0.0107 / 0.0339 |
| Route / hybrid, process-specific irs_bounded_ofac central | $1,319,149 / $1,751,682 | 0.0108 / 0.0353 |
| Route / hybrid, process-specific w38b high | $634,379 / $902,092 | 0.0030 / 0.0129 |
| Route / hybrid, process-specific irs_bounded high | $1,113,294 / $1,515,209 | 0.0069 / 0.0249 |
| Route / hybrid, process-specific irs_bounded_ofac high | $1,115,307 / $1,517,886 | 0.0069 / 0.0250 |

**Which earlier claims change:**

| Earlier claim (g0403-04, wave 38B) | Status |
|---|---|
| "P(detected and taxed) swept 0.01–1, no source" | **Replaced.** Bounded at 0.0012–0.0099 (central 0.0018) from IRS exam coverage and SOI §4966 incidence; the old low is now the upper bound |
| Central composite m ≈ 2.20 | **Lowered to 1.56–1.77**; route pool at large nationals $1.31m–$1.32m (from $1.27m) |
| High composite m 88.5 | **Lowered to 55** (bank transfer kept) **or 9.3** (OFAC analogue); single-m routing at 9.3 keeps $688k (above assist) |
| "Sanctions violations carry strict-liability OFAC penalties that apply to charities" (P-G0403-04-04 proposed) | **Quantified, with a caveat.** No 2021+ OFAC action against a charity or donor platform; processor analogue median $168.50 per violation (12 units), but $430,500 per missed true-match alert (Amex) |
| Assistance modal nowhere; ranking unchanged | **Unchanged.** Max mean P(C first) in the rerun is 0.035 |

---

## 6. Limits

1. **q = 1.** The probability that an exam of a sponsor finds and taxes a particular escaped grant is unknown. Setting it to 1 makes every P an upper bound on the exam channel.
2. **No size breakdown.** Large sponsors may be examined well above the all-filer rate; the Data Book gives no size breakdown (P-G0403-0104-01). The high setting (0.0099) is 5.4 times the median narrow rate, and the maximum broad rate is about 3 times it.
3. **Fiscal and processing years are mixed.** Data Book fiscal years are matched to e-file processing years, and e-file rows can include amended or duplicate returns. That moves the rates by a few percent, not by orders of magnitude.
4. **The FY2025 TE/GE exam count is derived** from TIGTA's rounded "15 percent", not quoted.
5. **SOI §4966 counts mix channels.** They include self-reported tax and are suppressed for CY2025. §4967 and manager taxes are not published, so no count of §4967 assessments exists in the sources checked.
6. **GAO not checked.** gao.gov denied the robots.txt request (403), so GAO reports were not used.
7. **OFAC.** Fifteen releases; no charity cases; P(enforcement) has no source; penalties depend on self-disclosure and on ability to pay (ShapeShift). Per-violation figures assume penalties are linear in count, which the Enforcement Guidelines support only for the base penalty.
8. **Out of scope.** The operational m (1 / 2 / 5) is still unsourced and now dominates the composite. Reputational and state-AG costs are not quantified.
9. **Rerun scope.** Only the large-national CAL_CENTRAL cells were run (P-G0403-0104-05).

---

## 7. Data dictionary: `m-detection-ofac-2026-11-19.csv`

Columns are as in `escaped-error-cost-2026-11-19.csv`: record_type, id, entity, metric, value, unit, basis, assumption, source, note.

| record_type | id | Metrics |
|---|---|---|
| meta | `run`; `efile_recount_PY<yr>` | draws (0 without `--route`); e-file recount by RETURN_TYPE (only with `--efile-dir`) |
| irs_exam | `FY<yr>` | returns_examined_990_990EZ_990N, returns_examined_990PF_1041A_1120POL_5227, returns_examined_form_4720, returns_examined_tege_total (Data Book Table 3-5) |
| irs_filed | `FY<yr>` | tax_exempt_org_returns_filed (Table 1-2), recognized_501c3_orgs (Table 2-6) |
| efile | `PY<yr>` | efile_index_rows_{990, 990EZ, 990PF} |
| tege_exam | `FY<yr>` | eo_filings_examined_closed (FY2025 computed from TIGTA %) |
| coverage | `FY<yr>` | exam_rate_990_990EZ, exam_rate_990series_per_501c3_org, exam_rate_eo_filings_broad, form4720_exams_per_eo_return_filed |
| soi_4966 | `CY<yr>` | returns_reporting_4966_sponsor_tax, 4966_sponsor_tax_usd (or _upper_bound for CY2025), 4966_tax_per_return, implied_taxable_distribution_per_return, share_of_daf_sponsors_reporting_4966, form4720_total_org_tax_{returns, usd} |
| p_detect | `low`, `central`, `high`, `sponsor_incidence_max`, `fidelity_grant_check` | p_detected_and_taxed; taxed_4966_returns_per_fidelity_grant |
| ofac_scope | year | release_rows_read |
| ofac | release id | penalty_usd, apparent_violations, usd_per_violation, m_conditional_P14_units, violating_value_usd, statutory_max_usd, base_penalty_usd, penalty_per_usd_violating_value, penalty_share_of_base, usd_per_missed_alert and its units (Amex only) |
| ofac_range | `{processor, crypto, all}_{min, median, max}` | usd_per_violation, m_conditional_P14_units |
| m_process | `<variant>_<setting>` | m_P01, m_P07, m_P08, m_P14 |
| m_composite | `<variant>_<setting>` | m_weighted_P01_P15 |
| route | `CAL_CENTRAL\|NAT_LARGE\|<variant>\|<cell>` | sponsor_ai_gross_value_p50 (p25/p75 in note), mean_p_C_rank_first_gross_P01_P15, P07_p_C_net_positive |

- **basis** values: F (quoted), C (computed), C+I (computed on assumptions), S (scenario).
- **Units:** usd, returns, organizations, share, prob, ratio, handling units (one P14 or P07 case's handling cost).

---

## 8. Source register

| Ref | Source | URL |
|---|---|---|
| S01 | IRS Data Book Table 3-5 (Table 21 before FY2025), FY2021–FY2025 | https://www.irs.gov/statistics/soi-tax-stats-returns-of-tax-exempt-organizations-employee-retirement-plans-government-entities-and-tax-exempt-bonds-irs-data-book-table-3-5 ; files https://www.irs.gov/pub/irs-soi/21dbs03t21eo.xlsx … 24dbs03t21eo.xlsx, https://www.irs.gov/pub/irs-soi/25db-3-05-eo.xlsx |
| S02 | IRS Data Book Table 1-2 (Table 2), FY2021–FY2025 | https://www.irs.gov/statistics/soi-tax-stats-numbers-of-returns-filed-by-type-of-return-irs-data-book-table-1-2 ; https://www.irs.gov/pub/irs-soi/25db-1-02-nr.xlsx (and 21–24dbs01t02nr.xlsx) |
| S03 | IRS Data Book Table 2-6 (Table 14), FY2021–FY2025 | https://www.irs.gov/statistics/soi-tax-stats-tax-exempt-organizations-and-nonexempt-charitable-trusts-irs-data-book-table-2-6 ; https://www.irs.gov/pub/irs-soi/25db-2-06-eo.xlsx (and 21–24dbs02t14eo.xlsx) |
| S04 | IRS Data Book index of tables | https://www.irs.gov/statistics/soi-tax-stats-irs-data-book-index-of-tables |
| S05 | SOI Exempt Organizations Excise Tax (Form 4720) Table 1, CY2021–CY2025 | https://www.irs.gov/statistics/soi-tax-stats-excise-tax-statistics ; https://www.irs.gov/pub/irs-soi/21pf00et.xlsx … https://www.irs.gov/pub/irs-soi/25pf00et.xlsx |
| S06 | IRS Pub 6038 (Rev. 1-2026), Form 4720 excise taxes CY2024 | https://www.irs.gov/pub/irs-pdf/p6038.pdf |
| S07 | TE/GE Accomplishments Letters FY2021, FY2022, FY2023 (Pub 5329) | https://www.irs.gov/pub/irs-prior/p5329--2021.pdf ; https://www.irs.gov/pub/irs-prior/p5329--2022.pdf ; https://www.irs.gov/pub/irs-prior/p5329--2023.pdf |
| S08 | TE/GE FY2024 Accomplishments Letter (accessible version) | https://www.irs.gov/pub/irs-access/p5329_accessible.pdf |
| S09 | TE/GE Program Letters (FY2027 current; FY2026, FY2025) | https://www.irs.gov/pub/irs-pdf/p5313.pdf ; https://www.irs.gov/pub/irs-prior/p5313--022026.pdf ; https://www.irs.gov/pub/irs-prior/p5313--2025.pdf ; index https://www.irs.gov/government-entities/tax-exempt-and-government-entities-annual-priority-and-program-letters |
| S10 | TE/GE in-process and completed compliance strategies | https://www.irs.gov/government-entities/tax-exempt-government-entities-tege-in-process-compliance-strategies ; https://www.irs.gov/government-entities/tax-exempt-government-entities-tege-completed-compliance-strategies |
| S11 | TIGTA 2026-1S0-042, Statistical Trends of the TE/GE Division Through FY2025 (19 Aug 2026) | https://www.tigta.gov/sites/default/files/reports/2026-08/20261S0042fr.pdf |
| S12 | TIGTA 2024-100-040, Tax-Exempt Compliance Unit (16 Aug 2024) | https://www.tigta.gov/sites/default/files/reports/2024-08/2024100040fr.pdf |
| S13 | IRS Form 990 series downloads and e-file index CSVs (2021–2025) | https://www.irs.gov/charities-non-profits/form-990-series-downloads ; https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv (and 2021–2024) |
| S14 | DAFRC 2025 dataset, 1,512 FY2024 sponsors (via repo [full-universe-990-harvest-and-corrected-totals.md](full-universe-990-harvest-and-corrected-totals.md)) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx |
| S15 | Fidelity Charitable 2024 grant count (via repo `grant-rail-shares-panel-2026.csv`) | repo |
| S16 | OFAC civil penalties and enforcement information (2026 YTD; 2021–2025 pages) | https://ofac.treasury.gov/civil-penalties-and-enforcement-information ; …/2021-enforcement-information … …/2025-enforcement-information |
| S17 | OFAC releases: BitPay | https://ofac.treasury.gov/media/54341/download?inline |
| S18 | MoneyGram | https://ofac.treasury.gov/media/97356/download?inline |
| S19 | Payoneer | https://ofac.treasury.gov/media/911571/download?inline |
| S20 | Airbnb Payments | https://ofac.treasury.gov/media/917236/download?inline |
| S21 | American Express National Bank | https://ofac.treasury.gov/media/924406/download?inline |
| S22 | Tango Card | https://ofac.treasury.gov/media/928326/download?inline |
| S23 | daVinci Payments | https://ofac.treasury.gov/media/932276/download?inline |
| S24 | Uphold HQ | https://ofac.treasury.gov/media/931556/download?inline |
| S25 | Kraken | https://ofac.treasury.gov/media/929541/download?inline |
| S26 | Bittrex | https://ofac.treasury.gov/media/928746/download?inline |
| S27 | Poloniex | https://ofac.treasury.gov/media/931701/download?inline |
| S28 | CoinList | https://ofac.treasury.gov/media/932406/download?inline |
| S29 | Binance | https://ofac.treasury.gov/media/932351/download?inline |
| S30 | ShapeShift | https://ofac.treasury.gov/media/934641/download?inline |
| S31 | Exodus | https://ofac.treasury.gov/media/934831/download?inline |
| S32 | 26 U.S.C. §4966, §4967 (rates, via the escaped-error note) | https://www.law.cornell.edu/uscode/text/26/4966 ; https://www.law.cornell.edu/uscode/text/26/4967 |
| — | Model inputs and prior m: [g0403-04-escaped-error-cost.md](g0403-04-escaped-error-cost.md), [validation-wave38b-report.md](validation-wave38b-report.md), `scripts/mission_escaped_error_cost.py`, `scripts/mission_ai_routing_variant.py` | repo |
