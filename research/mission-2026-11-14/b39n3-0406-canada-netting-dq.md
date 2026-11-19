# Canada: DAF payout net of transfers, and DAF payout vs the disbursement quota (P-B39N3-04, P-B39N3-06)

**Prepared 2026-11-19 (task b39n3-0406). Desk research only: no outreach, no logins, no forms.** This is research, not legal or tax advice. It builds on [`b39n3-canada-australia.md`](b39n3-canada-australia.md) (including its wave-37B corrections: blank line 5864 counts as zero in medians), the panel [`canada-daf-panel-2026-11-19.csv`](../../data/mission-2026-11-14/canada-daf-panel-2026-11-19.csv) and [`scripts/mission_canada_daf_panel.py`](../../scripts/mission_canada_daf_panel.py), which the new script imports without changing.

**Labels.** **[F]** the source states it; **[C]** computed by `scripts/mission_canada_netting_dq.py`; **[I]** inference.

**Outputs.**
- [`data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv`](../../data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv): 1,710 rows, one per DAF sponsor (line 5860 = Y) and release (2024: 846; 2025: 864), with gifts by donee type, netted payout and the Schedule 8 test.
- [`scripts/mission_canada_netting_dq.py`](../../scripts/mission_canada_netting_dq.py): stdlib, functional; imports `mission_canada_daf_panel` and prints a JSON summary (all numbers below).
- [`data/mission-2026-11-14/queue-proposals-b39n3-0406.csv`](../../data/mission-2026-11-14/queue-proposals-b39n3-0406.csv): 6 follow-ups.

Reproduce: put the panel's CRA files in `DIR` (as in the parent doc) and the four files in §1.2 in `DIR2` (named `{year}_{qd|dq}_<original name>`), then
`python3 scripts/mission_canada_netting_dq.py . --data-dir DIR --extra-dir DIR2 --summary out.json`

---

## Headline findings

1. **Netting changes Canadian DAF payout only slightly under a DAF-to-DAF definition.** On the US-comparable basis (line 5864 ÷ prior-release line 5862, matched sponsors, blank 5864 = 0), the 2025 release gives **13.3% gross, 12.8% net of gifts to DAF-primary sponsors (tier A), 12.0% net of gifts to any 5860 = Y sponsor (tier B), and 8.8% net of gifts to any sponsor or foundation (tier C)**. The base is 586 sponsors and C$15.39bn. The 2024 figures are 16.4%, 15.7%, 14.3% and 10.7% (336 sponsors, C$7.34bn, partial 2023 base) [C].
2. **Sponsor-to-sponsor gifts are smaller in Canada than in the US.** Gifts to other 5860 = Y sponsors equal 9.4% of 2025 line-5864 dollars (tier B; 11.3% in 2024), and gifts to DAF-primary sponsors only 4.1% (3.5%) [C]. Tier B lowers the 2025 aggregate by 1.25 points, against 1.6–3.1 points for US tier A ([queue-net-payout-fidelity-outliers.md](queue-net-payout-fidelity-outliers.md)). The netted Canadian figure (12.0%) stays far below the US 22.8% [C/I].
3. **"DAF-to-foundation" gifts are mostly program grants, not transfers.** Gifts to public and private foundations that never answered 5860 = Y add another C$543m in 2025. The largest are JCF Montreal → Federation CJA (C$32.1m) and Jewish Foundation of Greater Toronto → UJA (C$26.0m), plus hospital and university foundations. Tier C is therefore an upper bound, like US tier C [C/I].
4. **Medians fall further than aggregates.** For matched sponsors in 2025, the median moves from 5.7% gross to 5.4% (A), 4.9% (B) and 4.2% (C). The share of sponsors below 5% rises from 48.2% to 48.9%, 50.9% and 53.8%. Among sponsors with at least C$10m of prior-year DAF assets (68), the median moves from 8.7% to 8.3% (A), 7.4% (B) and 5.0% (C) [C].
5. **The charity-level disbursement quota is not a binding constraint on the largest DAF sponsors.** The DQ is 3.5% of the average value of property not used in charitable activities or administration, up to C$1m, plus 5% above C$1m [F]. 19 of the top-20 sponsors by DAF assets have a Schedule 8 row in each release [C]:
   - **2025:** 13 meet the DQ from DAF disbursements alone, even net of tier-B transfers. One (Brookfield Partners Foundation) meets it from DAF disbursements only gross of transfers (C$23.6m gross, C$20.1m net, DQ C$21.4m). Four meet it only with non-DAF spending: Winnipeg, Calgary, Vancouver and Victoria. One is in shortfall: Hamilton Community Foundation (−C$279k).
   - **2024:** 14 meet the DQ from DAF disbursements net of transfers. Five need non-DAF spending: Winnipeg, Calgary, Vancouver, Edmonton and Hamilton [C].
6. **Yes, one top-20 sponsor meets the DQ only through a carry-forward.** Hamilton Community Foundation's 2025-release return (FPE 2025-03-31) shows spending of C$13.11m against a DQ of C$13.39m [C]. Its 2024-release return shows an excess of C$973k (line 865). ITA s.149.1(20) lets a disbursement excess count for up to five later years [F]. The excess covers the shortfall [C]. The community foundations that need non-DAF spending have DQs equal to 8–21% of their prior-year DAF assets: their DQ base is mainly endowment, not DAFs [C/I].
7. **Panel-wide (2025 release, 864 sponsors).** 375 have a Schedule 8 row [C]:
   - 107 cover the DQ from net DAF disbursements, and 6 only gross of transfers.
   - 212 need non-DAF spending. They hold C$3.22bn of DAF assets.
   - 22 are in shortfall (C$0.30bn of DAF assets). 10 of the 22 are covered by an excess shown in their 2024-release return.
   - 7 sponsors are in shortfall in both releases.
   - The other 489 sponsors (C$2.79bn) have no Schedule 8 row; 22 have no DQ and 6 have blank spending lines.
8. **A 5% floor on DAF assets would bind far more often than the charity DAF.** Apply the DQ formula to each sponsor's prior-year DAF assets alone (a proxy, not law). Then 332 of 586 matched sponsors meet it gross, and 312 meet it net of tier-B transfers. That leaves 274 (47%) below such a floor. Among the top-20 the count is 18 of 20 (net) [C].

---

## 1. Method

### 1.1 Robots.txt and fetch log (UA `research-script/1.0`; checked 2026-11-19 before any fetch)

| Host | Result | Use |
|---|---|---|
| open.canada.ca | 200; `Crawl-delay: 20`; `/data/` not disallowed | 4 CSV downloads, 20 s apart (21:38–21:39 UTC) |
| opencanada.blob.core.windows.net | 404 (no robots = allowed) | download redirect target |
| www.canada.ca | HTTP/2 stream reset (INTERNAL_ERROR), as in the parent pass | **not fetched** |
| laws-lois.justice.gc.ca | 404 (no robots = allowed) | ITA s.149.1 and Income Tax Regulations s.3701 (2 pages) |

The panel inputs (Sections A–C, Identification and Section D/Schedule 6 for 2023–2025, and data dictionary v2.0) are the parent pass's downloads from 2026-11-19 20:58–21:01 UTC. They were reused unchanged.

### 1.2 Data added in this pass

| File | Release | Content | Rows |
|---|---|---|---|
| `qualified_donees_2025_updated.csv` | 2025 (CKAN 4b60228a-…, resource 083ccf7f-…) | T1236 worksheet: donor BN, FPE, donee BN, donee name, Total Gifts | 338,323 |
| `qualified_donees_2024_updated.csv` | 2024 (CKAN 80c00cdb-…, resource 8195b2cb-…) | same | 344,932 |
| `schedule_8_dq_2025_updated.csv` | 2025 (resource 1e079ab4-…) | Schedule 8 lines 805–890 | 14,852 |
| `schedule_8_dq_2024_updated.csv` | 2024 (resource d3c4db23-…) | same | 14,631 |

### 1.3 DQ rules (primary sources)

- **CRA open-data dictionary v2.0, §3.19 "Schedule 8 Disbursement Quota"** [F]:
  - Line 805: "Average value of property not used in charitable activities or administration (line 5900 from your return)".
  - Line 810: accumulated property under a permission to accumulate.
  - Line 815: 805 − 810, floored at 0.
  - If 815 ≤ 1,000,000, line 820 = 815 × 3.5%. Otherwise line 835 = (815 − $1,000,000) × 5% + $35,000.
  - Line 840 is "your charity's disbursement quota requirement for the current fiscal period".
  - Lines 845 / 850 / 855 are pre-filled from Schedule 6 lines 5000 (charitable activities), 5045 (grants to non-qualified donees) and 5050 (gifts to qualified donees).
  - Line 860 = 845 + 850 + 855. Line 865 = 860 − 840, the "disbursement quota excess or shortfall".
  - Lines 870–890 repeat the calculation for the next fiscal period on line 5910.
- **Dictionary §1.4.5:** Schedule 8 is new in T3010 v27, following "Budget 2022 – new Disbursement Quota (DQ) amendments … Bill C-32 … Royal Assent". It applies to "fiscal periods beginning on or after January 1, 2023" [F].
- **Income Tax Act s.149.1(1), "disbursement quota"** (laws-lois.justice.gc.ca, "current to 2026-10-29") [F]:
  - The quota is A ÷ 365 × B, where B is:
    - 3.5% of the prescribed amount of property "not used directly in charitable activities or administration", if that amount is at most $1 million but above $100,000 (charitable organizations) or $25,000 (other charities);
    - "$35,000 plus 5% of the amount by which the prescribed amount exceeds $1 million", if above $1 million;
    - nil otherwise.
  - The A ÷ 365 term pro-rates short years. Schedule 8 does not show it, and the script ignores it.
- **ITA s.149.1(20)–(21):** a "disbursement excess" (spending above the DQ) may be counted "for the immediately preceding taxation year … and five or less of its immediately subsequent taxation years" [F]. **s.149.1(1.1)(d)** excludes administration and management from qualifying spending [F].
- **Income Tax Regulations s.3701:** the prescribed amount is the average, over 2–8 equal periods totalling 24 months that end immediately before the year, of the value of such property [F].

### 1.4 Netting (P-B39N3-04)

- **Universe.** Every panel sponsor-year in the 2024 and 2025 releases (line 5860 = Y; latest FPE per BN, as in the panel). T1236 rows are joined on (BN, FPE).
- **Donee resolution.** The 170,944 sponsor gift rows were resolved in this order [C]:
  - exact 15-character BN against the 2023–2025 Identification files: 89.8%;
  - 9-digit BN root, with RR0001 preferred: 4.0%;
  - exact normalised name matching a single legal name: 1.7%;
  - unresolved: 4.4%.
- **Donee classes:**
  - `self`: same BN root as the donor. Dropped.
  - `sponsor_daf_primary`: answered 5860 = Y in any 2023–2025 release, and in its latest such return DAF assets (5862) are at least 50% of total assets (4200).
  - `sponsor_other`: any other 5860 = Y filer.
  - `private_foundation` / `public_foundation` / `charitable_org`: designation B / A / C, never a 5860 = Y filer.
  - `unmatched`: the remainder.
- **Tiers,** nested as in the US method:
  - A = sponsor_daf_primary;
  - B = A + sponsor_other;
  - C = B + private and public foundations.
- **US netted definition** ([queue-net-payout-fidelity-outliers.md §2.2](queue-net-payout-fidelity-outliers.md)): net = 5864 − min(transfers, 5864); net payout = net ÷ prior-release 5862 (same BN, 5860 = Y in the previous release). Blank 5864 counts as 0 (wave 37B).
- **Medians** are taken over matched sponsors with prior 5862 > 0.
- **Itemised-only variant:** drops sponsors with 5864 > 0 and no T1236 rows (their transfers are unknown).

### 1.5 DQ test (P-B39N3-06)

- Schedule 8 rows are joined on (BN, FPE).
- **Requirement:** line 840. If 840 is blank, it is recomputed from 805 − 810 with the formula above (18 rows in 2025, 10 in 2024).
- **Spending:** line 860, else 845 + 850 + 855, else Schedule 6 lines 5000 + 5045 + 5050.
- **Check:** the recomputed DQ equals the filed 840 within C$2 or 0.1% for 325 of 336 comparable 2025 rows (322 of 332 in 2024) [C].
- **Route per sponsor-year** (`route` column):

| Route | Rule |
|---|---|
| DAF_NET_COVERS | 5864 net of tier-B transfers ≥ DQ |
| DAF_GROSS_ONLY | 5864 ≥ DQ > 5864 net of tier B |
| NEEDS_NON_DAF | 5864 < DQ ≤ spending (meets only with non-DAF charitable spending or gifts) |
| SHORTFALL | spending < DQ (needs a carry-forward or carry-back under s.149.1(20)) |
| INCOMPLETE / NO_DQ / NO_SCHEDULE8 | spending lines blank / DQ zero or not computable / no Schedule 8 row |

- **Carry-forward check:** for 2025 rows only, the sponsor's 2024-release line 865 is compared with the shortfall. Earlier years were not loaded.
- **Own-DQ proxy:** the DQ formula applied to the sponsor's prior-year DAF assets alone. This shows what a DAF-pool floor would require. It is **not** the law.
- **Top-20:** rank by line 5862 within each release (panel `rank_assets_in_year`).

---

## 2. Netting results (P-B39N3-04)

### 2.1 Gifts by donee type (all 5860 = Y sponsors) [C]

| Release | T1236 gifts | Sponsor, DAF-primary | Sponsor, other | Private fdn | Public fdn | Charitable org | Unmatched | Self |
|---|---|---|---|---|---|---|---|---|
| 2024 | C$2,776m | C$67.9m (2.4%) | C$171.6m (6.2%) | C$80.0m (2.9%) | C$402.7m (14.5%) | C$1,874.7m (67.5%) | C$176.9m (6.4%) | C$2.7m |
| 2025 | C$3,205m | C$85.9m (2.7%) | C$122.9m (3.8%) | C$97.4m (3.0%) | C$445.5m (13.9%) | C$2,299.1m (71.7%) | C$150.9m (4.7%) | C$3.6m |

- **Coverage.** In 2024, 510 of 846 sponsors have T1236 rows for their FPE, covering 93.0% of line-5864 dollars. In 2025 it is 488 of 864, covering 94.4% [C].
- **T1236 vs Schedule 6.** T1236 gifts are 91.7% (2024) and 98.2% (2025) of the same sponsors' line 5050 [C].
- **DAF vs non-DAF money.** T1236 covers all gifts, from DAF and non-DAF funds, which is why transfers are capped at 5864.

### 2.2 Payout on prior-year DAF assets, gross and net [C]

| Measure | 2024 release (n = 336; base C$7.34bn) | 2025 release (n = 586; base C$15.39bn) |
|---|---|---|
| Transfers, tier A / B / C (raw) | C$51.9m / C$162.1m / C$432.9m | C$84.2m / C$201.8m / C$738.0m |
| Aggregate payout, gross | 16.41% | 13.30% |
| Net tier A (DAF-primary sponsors) | 15.71% | 12.76% |
| Net tier B (any 5860 = Y sponsor) | 14.28% | 12.05% |
| Net tier C (+ all foundations) | 10.74% | 8.82% |
| Median sponsor, gross → A / B / C | 6.8% → 6.7 / 5.4 / 4.4% | 5.7% → 5.4 / 4.9 / 4.2% |
| Median, prior DAF assets ≥ C$10m (n = 47 / 68) | 11.7% → 10.4 / 9.7 / 7.1% | 8.7% → 8.3 / 7.4 / 5.0% |
| Share of sponsors < 5%, gross → A / B / C | 43.5% → 44.0 / 47.6 / 52.4% | 48.2% → 48.9 / 50.9 / 53.8% |
| Itemised-only (n = 282 / 478): gross → A / B / C | 16.23% → 15.51 / 14.04 / 10.41% | 13.26% → 12.69 / 11.94 / 8.54% |
| Top-20 by DAF assets (n = 10 / 20): gross → A / B / C | 12.82% → 12.39 / 11.33 / 8.07% | 11.34% → 10.83 / 10.15 / 6.78% |

- **Releases.** The 2025 release is the reference. The 2024 matched base covers only sponsors with a v27 return in the partial 2023 release.
- **Medians.** The parent doc's medians are same-filing medians. These are on prior-year assets, with blanks as zero.

### 2.3 Largest transfer edges (gifts ≥ any tier) [C]

| Release | Donor → donee | Class | C$m |
|---|---|---|---|
| 2025 | Private Giving Foundation → CanEd Foundation | public fdn | 36.0 |
| 2025 | JCF Montreal → Federation CJA | public fdn | 32.1 |
| 2025 | JCF Montreal → Johanne Dean & Alain Bedard Foundation | private fdn | 27.9 |
| 2025 | Jewish Fdn of Greater Toronto → UJA of Greater Toronto | public fdn | 26.0 |
| 2025 | Aqueduct Foundation → BenefAction Foundation | sponsor, DAF-primary | 21.8 |
| 2025 | Charitable Gift Funds Canada → Badge of Hope | private fdn | 20.0 |
| 2025 | St Mary's General Hospital Fdn → CanadaHelps | public fdn | 10.2 |
| 2025 | Charitable Gift Funds Canada → Canada Gives | sponsor, DAF-primary | 6.5 |
| 2024 | JCF Montreal → Les Amis Canadiens de l'Université de Tel Aviv | sponsor, other | 19.2 |
| 2024 | Canadian Online Giving Fdn → United Way of Greater Toronto | sponsor, other | 11.1 |
| 2024 | Private Giving Foundation → London Community Foundation | sponsor, other | 10.0 |
| 2024 | Nicola Wealth Private Giving Fdn → CHIMP | sponsor, DAF-primary | 5.5 |

**Reading** [I]:
- **Tier A** captures clear DAF-to-DAF moves: Aqueduct → BenefAction, CGF Canada → Canada Gives, and Nicola Wealth → CHIMP.
- **Tier B** adds 5860 = Y charities whose main business is not DAFs: United Way of Greater Toronto, UHN Foundation and the Tel Aviv University friends. Gifts to them are more likely program grants, so tier B is already generous.
- **Tier C** mixes federation and hospital grants with a few DAF-like flows. Examples are CanEd Foundation and CanadaHelps; CanadaHelps answered line 5860 = **N** in both releases [C]. See queue P-B3946-01 and -04.

### 2.4 Coverage gaps [C]

- **No T1236 rows:** 173 sponsors (C$135.2m of 5864) in 2024 and 159 (C$117.6m) in 2025 report DAF disbursements but have no T1236 rows. Examples are Université Laval, the Morris and Rosalind Goodman Family Foundation (2024) and Canada Gives (2025). Their transfers are treated as zero in the all-matched figures.
- **Itemised-only sample:** it moves the 2025 aggregate by about 0.1 point. The median moves more (tier B 4.9% → 3.1%), because the dropped rows are mostly small payers.

---

## 3. Disbursement-quota results (P-B39N3-06)

### 3.1 Top-20 DAF sponsors, 2025 release [C]

DQ = line 840 (Victoria: recomputed from 805). Spending = line 860. "DAF ÷ DQ" = 5864 ÷ DQ; "net B" uses 5864 net of tier-B transfers.

| # | Sponsor | DAF assets | 5864 | DQ | Spending | DAF ÷ DQ | Net B ÷ DQ | DQ ÷ prior DAF assets | Route |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Charitable Gift Funds Canada | C$3,079.6m | 268.3 | 90.7 | 268.3 | 2.96 | 2.63 | 3.7% | DAF_NET_COVERS |
| 2 | Jewish Community Fdn of Montreal | C$2,516.2m | 236.9 | — | — | — | — | — | NO_SCHEDULE8 |
| 3 | Private Giving Foundation | C$1,163.6m | 180.5 | 44.8 | 180.5 | 4.03 | 3.62 | 4.6% | DAF_NET_COVERS |
| 4 | Winnipeg Foundation | C$1,094.0m | 60.5 | 81.4 | 99.8 | 0.74 | 0.70 | 8.1% | NEEDS_NON_DAF |
| 5 | BenefAction Foundation | C$1,059.2m | 92.8 | 27.8 | 93.0 | 3.33 | 3.02 | 3.5% | DAF_NET_COVERS |
| 6 | Aqueduct Foundation | C$910.7m | 99.8 | 52.4 | 137.6 | 1.90 | 1.33 | 6.2% | DAF_NET_COVERS |
| 7 | Jewish Fdn of Greater Toronto | C$887.5m | 62.3 | 38.9 | 63.4 | 1.60 | 1.54 | 5.4% | DAF_NET_COVERS |
| 8 | CHIMP | C$712.8m | 132.6 | 30.4 | 132.6 | 4.36 | 3.97 | 4.5% | DAF_NET_COVERS |
| 9 | Calgary Foundation | C$637.2m | 45.8 | 59.9 | 85.7 | 0.76 | 0.69 | 10.5% | NEEDS_NON_DAF |
| 10 | Strategic Charitable Giving Fdn | C$613.2m | 44.6 | 22.2 | 45.4 | 2.01 | 1.75 | 4.3% | DAF_NET_COVERS |
| 11 | Vancouver Foundation | C$447.8m | 37.7 | 82.8 | 145.8 | 0.46 | 0.28 | 20.3% | NEEDS_NON_DAF |
| 12 | Brookfield Partners Foundation | C$443.2m | 23.6 | 21.4 | 24.5 | 1.10 | 0.94 | 5.2% | DAF_GROSS_ONLY |
| 13 | Canada Gives | C$398.7m | 35.2 | 13.9 | 35.2 | 2.52 | 2.52* | 4.2% | DAF_NET_COVERS |
| 14 | Cidel Foundation | C$299.9m | 22.0 | 3.4 | 22.0 | 6.39 | 6.12 | 4.7% | DAF_NET_COVERS |
| 15 | Université Laval | C$298.7m | 29.3 | 11.4 | 1,168.6 | 2.57 | 2.57* | 3.9% | DAF_NET_COVERS |
| 16 | Abundance Canada | C$270.0m | 55.4 | 11.1 | 58.2 | 5.00 | 4.72 | 4.2% | DAF_NET_COVERS |
| 17 | Toronto Foundation | C$231.4m | 23.9 | 13.9 | 38.2 | 1.72 | 1.56 | 6.8% | DAF_NET_COVERS |
| 18 | Fondation Philantra | C$181.1m | 11.1 | 3.3 | 11.1 | 3.32 | 2.81 | 2.9% | DAF_NET_COVERS |
| 19 | Hamilton Community Foundation | C$157.8m | 6.2 | 13.4 | 13.1 | 0.47 | 0.45 | 8.8% | SHORTFALL (covered by 2024 excess C$0.97m) |
| 20 | Victoria Foundation | C$153.0m | 9.5 | 21.0† | 36.6 | 0.45 | 0.42 | 15.2% | NEEDS_NON_DAF |

Amounts in C$m except DAF assets. \* No T1236 rows, so transfers are unknown. † Line 840 blank; recomputed from line 805 (C$421.1m).

### 3.2 Top-20, 2024 release [C]

- **DAF_NET_COVERS (14):** Charitable Gift Funds Canada, Private Giving Foundation, Aqueduct, BenefAction, Jewish Foundation of Greater Toronto, CHIMP, Strategic Charitable Giving, Brookfield, Goodman Family Foundation\*, Nicola Wealth Private Giving, Canada Gives, Université Laval\*, Abundance Canada and Toronto Foundation (\* no T1236 rows).
- **NEEDS_NON_DAF (5):** Winnipeg (DAF ÷ DQ 0.68), Calgary (0.71), Vancouver (0.51), Edmonton CF (0.18) and Hamilton CF (0.41).
- **NO_SCHEDULE8 (1):** JCF Montreal.
- No top-20 sponsor is in shortfall in 2024.

### 3.3 All sponsors [C]

| Route | 2024: n | 2024: DAF assets | 2025: n | 2025: DAF assets |
|---|---|---|---|---|
| DAF_NET_COVERS | 97 | C$10.77bn | 107 | C$11.74bn |
| DAF_GROSS_ONLY | 5 | C$0.04bn | 6 | C$0.50bn |
| NEEDS_NON_DAF | 215 | C$3.23bn | 212 | C$3.22bn |
| SHORTFALL | 21 | C$0.13bn | 22 | C$0.30bn |
| INCOMPLETE | 3 | <C$0.01bn | 6 | C$0.04bn |
| NO_DQ | 32 | <C$0.01bn | 22 | <C$0.01bn |
| NO_SCHEDULE8 | 473 | C$2.49bn | 489 | C$2.79bn |

- **By designation (2025):**
  - Public foundations: 61 DAF_NET_COVERS, 115 NEEDS_NON_DAF, 16 SHORTFALL, 53 no Schedule 8.
  - Charitable organizations: 427 of 571 have no Schedule 8 row. Most are small holders, below the C$100k threshold or exempt [I].
- **Shortfalls (2025):** 10 of 22 are covered by the excess on the sponsor's 2024-release return. Examples are Hamilton CF, Brant CF, Barrie CF, Creston Valley CF and Legacy Private Trust Foundation. 2024 shortfalls could not be tested, because no 2023 Schedule 8 was loaded.
- **Repeat shortfalls:** 7 sponsors are in shortfall in both releases. They are Brandon University Foundation (−C$0.90m, then −C$0.91m), Fondation du Collège de l'Assomption, Lithuanian Canadian Foundation, Brampton and Caledon CF, Fredericton CF, The Rogan Foundation and Fondation Caritas-Sherbrooke. Whether older excesses cover them is open (P-B3946-02).
- **DAF_GROSS_ONLY (11 sponsor-years):** Burgundy Legacy Foundation, SickKids Charitable Giving Fund and Osprey CF (both years); Alder Foundation and Wood Buffalo CF (2024); Brookfield, North Okanagan CF and Fondation du Cégep de Baie-Comeau (2025).

### 3.4 Answer to the P-B39N3-06 test [C/I]

- **Meets the DQ only through non-DAF spending.** Among the top-20, Winnipeg, Calgary, Vancouver and Victoria (2025) and Edmonton and Hamilton (2024) do.
  - All are community foundations with large endowments, so their DQ base is mostly non-DAF property.
  - Their DQ is 8–21% of prior-year DAF assets, so no realistic DAF payout would cover it alone.
  - This is not a compliance concern; it shows that the DQ is set at charity level.
- **Meets the DQ only through a carry-forward.** Among the top-20, Hamilton Community Foundation does, in 2025.
- **Meets it only gross of DAF-to-DAF transfers.** Among the top-20, Brookfield Partners Foundation does, in 2025.
- **National, bank and online sponsors** (Charitable Gift Funds Canada, Private Giving Foundation, BenefAction, CHIMP, Strategic, Canada Gives, Abundance, Cidel and Philantra) pay out 2.0 to 6.4 times their DQ from DAFs. Their DQ is 2.9–4.7% of prior DAF assets [C].
- **The DQ does not reach accounts.** It is set at charity level, so a sponsor can be far above it while individual accounts pay nothing. The T3010 has no account-level line, so dormant accounts cannot be seen [I].

---

## 4. Limits

- **T1236 covers all gifts.** Gifts from non-DAF funds (endowment, unrestricted) to other sponsors or foundations are netted as if DAF money, as in the US method. This overstates netting for community foundations. The cap at 5864 limits it [I].
- **Sponsor list.** It is the panel's 5860 = Y filers in any 2023–2025 release. Organisations that answer N but run DAF-like products (e.g. CanadaHelps) fall in tier C, or out of netting [C/I].
- **The DAF-primary cut (≥ 50% of total assets) is a rule of thumb.** London Community Foundation and United Way of Greater Toronto, for example, fall in tier B, not A.
- **Donee resolution.** 4.4% of gift rows are unresolved; they include municipalities, foreign universities and malformed BNs. Root matching may assign a gift to the wrong program account of the same organisation. No effect on class is expected [I].
- **Missing T1236 rows.** 159–173 sponsors per release report 5864 but no T1236 rows. Their transfers are unknown, not zero.
- **Schedule 8 gaps:**
  - 489 of 864 sponsors in 2025 (C$2.79bn of DAF assets) have no Schedule 8 row, including JCF Montreal (C$2.52bn).
  - Some rows leave 815–840 or 860 blank. These were recomputed or filled from Schedule 6, with the method flagged in `dq_check` and `dq_spending_source`.
  - 11 rows in 2025 and 10 in 2024 have a filed 840 that differs from the formula (e.g. Brookfield 2024). Possible reasons are the A ÷ 365 short-year term or Minister-authorised changes [I].
- **Carry-forwards.** Only one prior year (the 2024 release) was checked. Carry-backs from the next year were not checked. The script also ignores the C$25k/C$100k de minimis and short-year pro-rating.
- **Prior-year DAF assets** cover sponsors that were 5860 = Y in the previous release only. The 2024 base is partial (2023 = v27 forms only).
- **CRA guidance.** www.canada.ca was unreachable, so CRA guidance (e.g. on DQ calculation or DAFs) was not read. The rules come from the CRA dictionary and from the Act and Regulations [F].
- **Recency.** All sources are 2021 or later. ITA and Regulations consolidations are current to 2026-10-29.

---

## 5. Data dictionary: `canada-daf-netting-dq-2026-11-19.csv`

One row per BN × release (2024, 2025) with line 5860 = Y. Amounts are in C$ as filed. Booleans are yes/no; blank means not available.

| Column | Meaning |
|---|---|
| dataset_year, bn, fpe, legal_name, designation, rank_assets_in_year | As in the panel CSV (A public foundation, B private foundation, C charitable organization) |
| top20 | yes if rank_assets_in_year ≤ 20 in that release |
| daf_assets_5862, prior_daf_assets_5862, daf_disbursements_5864, total_assets_4200 | Panel values (prior = same BN, previous release, 5860 = Y) |
| qd_rows, qd_total_gifts | T1236 rows for this BN/FPE and the sum of Total Gifts |
| line_5050 | Schedule 6 line 5050, gifts to qualified donees |
| netting_coverage | itemised (T1236 rows present or 5864 = 0) / no_t1236 (transfers unknown) |
| gifts_self … gifts_unmatched | T1236 gifts by donee class (§1.4) |
| n_donees_sponsor, n_donees_foundation | Distinct donees in tier B classes / in private + public foundation classes |
| transfers_tier_a/b/c | Raw gifts in each nested tier |
| net_5864_tier_a/b/c | 5864 − min(transfers, 5864) (blank 5864 = 0) |
| payout_prior_gross | 5864 ÷ prior_daf_assets_5862 |
| payout_prior_net_tier_a/b/c | net_5864 ÷ prior_daf_assets_5862 |
| has_schedule8 | Schedule 8 row exists for BN/FPE |
| dq_805 … dq_870 | Schedule 8 lines as filed (805 property base; 810 accumulation; 815 base; 840 DQ; 845 / 850 / 855 spending components; 860 total; 865 excess or shortfall; 870 next-period base) |
| dq_recomputed | DQ formula applied to 815 (or 805 − 810 when 815 is blank) |
| dq_check | ok / differs / 840_blank_recomputed_from_805 |
| dq_requirement_used | 840, or dq_recomputed if 840 is blank |
| dq_rate_on_base | DQ ÷ 815 |
| dq_over_prior_daf_assets | DQ ÷ prior-year DAF assets |
| daf_5864_over_dq, net_b_over_dq | 5864 (gross; net of tier B) ÷ DQ |
| dq_on_prior_daf_assets | DQ formula applied to prior-year DAF assets (proxy floor, not law) |
| daf_meets_own_dq_proxy_gross / _net_b | 5864 (gross / net of tier B) ≥ that proxy |
| dq_spending_used, dq_spending_source | Spending used (860; else 845 + 850 + 855; else Schedule 6 lines 5000 + 5045 + 5050) and its source |
| dq_excess_used | Spending − DQ |
| prior_release_dq_865 | Line 865 on the sponsor's previous-release Schedule 8 (2025 rows only) |
| shortfall_covered_by_prior_release_excess | For shortfalls: prior_release_dq_865 ≥ shortfall |
| route | §1.5 |

## 6. Source register

| ID | Source | URL | Grade | Read |
|---|---|---|---|---|
| S01 | CRA, 2025 List of charities: qualified donees; Schedule 8 DQ (open data) | https://open.canada.ca/data/en/dataset/4b60228a-2b78-45d3-8e05-f7150b8fe8d8 (resources 083ccf7f-88b8-4852-a35c-ba91a1ae7bda, 1e079ab4-59b2-4cd0-8af6-3531b36f0fbd) | P | 2026-11-19 |
| S02 | CRA, 2024 List of charities: qualified donees; Schedule 8 DQ (open data) | https://open.canada.ca/data/en/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8 (resources 8195b2cb-ce2d-4cd2-b829-6d07f4959f49, d3c4db23-284f-49d7-9c86-6d8532f417bd) | P | 2026-11-19 |
| S03 | CRA, List of charities data dictionary v2.0 (§1.4.5, §3.4, §3.19, Schedule 6 lines 5050/5900/5910) | https://open.canada.ca/data/dataset/4b60228a-2b78-45d3-8e05-f7150b8fe8d8/resource/5c37b152-9381-4a8c-a475-fc8a60c6512b/download/open-data-data-dictionary-v2.0_eng.pdf | P | 2026-11-19 (parent pass download) |
| S04 | CRA, 2023–2025 List of charities: Sections A–C, Identification, Section D/Schedule 6 (panel inputs) | https://open.canada.ca/data/en/dataset/05b3abd0-e70f-4b3b-a9c5-acc436bd15b6 ; …/80c00cdb-1358-415c-bb8b-0de7f12675b8 ; …/4b60228a-2b78-45d3-8e05-f7150b8fe8d8 | P | 2026-11-19 |
| S05 | Income Tax Act, s.149.1 (definitions "disbursement quota", "qualifying disbursement"; (1.1), (2)–(4), (20), (21)), current to 2026-10-29 | https://laws-lois.justice.gc.ca/eng/acts/I-3.3/section-149.1.html | P | 2026-11-19 |
| S06 | Income Tax Regulations, s.3701 (prescribed amount) | https://laws-lois.justice.gc.ca/eng/regulations/C.R.C.,_c._945/section-3701.html | P | 2026-11-19 |
| S07 | Repo: US net payout tiers and definition | [queue-net-payout-fidelity-outliers.md](queue-net-payout-fidelity-outliers.md) | R | 2026-11-19 |
| S08 | Repo: Canadian panel and wave-37B corrections | [b39n3-canada-australia.md](b39n3-canada-australia.md) | R | 2026-11-19 |
