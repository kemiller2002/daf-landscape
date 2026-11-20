# Validation wave 51B: recipient concentration and fastest growers (b51-02)

**Validator:** validator wave 51B · **Date:** 2026-11-20 · **Register:** [`data/mission-2026-11-14/validation-register-wave51b.csv`](../../data/mission-2026-11-14/validation-register-wave51b.csv) (V51B-01 to V51B-20)

## Scope

- Study: [b51-02-recipient-concentration-growth.md](b51-02-recipient-concentration-growth.md), `data/mission-2026-11-14/recipient-concentration-growth-2026-11-20.csv` and `scripts/mission_recipient_concentration.py`.
- Not touched: b51-01, b51-03 and b51-04 (wave 51A runs on them in parallel). Earlier waves' §11 paragraphs are left as they are.

## Method

- **Rerun.** I ran the study script with `python3 -B` through a scratch wrapper that redirects its output path to scratch. It used the same caches, ran without `--fetch`, and no repo file was written. The CSV is byte-identical to the repo file (`cmp`).
- **Independent recompute** (scratch `v51b/indep.py`). The only repo functions reused are the universe and return selection (`top_n`, `pick_returns`, `itemized`) and `norm_name`. My own code does the rest:
  - reads the cached Schedule I lines;
  - applies the whitelist (`decision = include`, self-lines, and blank-EIN lines that match a unique panel name);
  - aggregates by recipient;
  - computes the top-N shares, a trapezoid Lorenz-curve Gini (1 − 2 × area) and HHI = 10,000 × Σ share²;
  - builds the balanced panel and the P1/P2 growth lists.
- **Raw XML.** Returns were streamed from the GivingTuesday mirror of IRS TEOS e-file XML and parsed with stdlib ElementTree. Only files under 5 MB were kept, in scratch.
  - 18 grower sponsor-year lines (11 returns) were spot-checked.
  - The Further Future / Navigation identity was checked against the SVCF FY2023 and Navigation FY2023 returns.
  - Marin CF FYE 2022-06 and 2023-06.
  - Dayton Foundation Plus FYE 2022-06 and 2023-06: Part IV, Schedule A, Schedule D, Schedule O and Schedule I.
  - GHCF FY2022: the WoodNext line.
- **BMF.** The cached IRS EO BMF extract (eo1–4, eo_pr, eo_xx, cached 2026-11-14) was read for 92-1117448, 54-2101090 and 88-1330756.
- **Access log.** At 2026-11-20 16:40 UTC, `gt990datalake-rawdata.s3.amazonaws.com/robots.txt` returned HTTP 404, so no rules apply. No Claude or Anthropic agent is named. That was the only host fetched. User agent `research-script/1.0`. No sec.gov, no logins, no forms.

## Counts

| Block | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---:|---:|---:|---:|---:|
| Concentration and reproduction (V51B-01 to 05, 13, 16, 17, 20) | 9 | 9 | 0 | 0 | 0 |
| FY2023 spike and Further Future / Navigation (V51B-06, 07) | 2 | 1 | 1 | 0 | 0 |
| Growth lists and classification (V51B-08 to 12, 18, 19) | 7 | 6 | 1 | 0 | 0 |
| Marin → Dayton Foundation Plus (V51B-14, 15) | 2 | 1 | 0 | 0 | 1 |
| **Total** | **20** | **17** | **2** | **0** | **1** |

## Findings

1. **The FY2023–24 reproduction is exact (V51B-01, 02).** All-itemising net dollars are $36,872,023,110 and $41,415,604,294. Top-10 is 0.153172 and 0.0826519; HHI is 42.5 and 14.4. These equal `daf-grant-recipient-sectors-top50.csv` (Schedule I total minus d2d), and the rerun CSV is byte-identical.

2. **The balanced-panel table, Gini and HHI reproduce cell by cell with independent code (V51B-03, 04).**
   - Net dollars: $31.23bn, $33.43bn, $36.53bn and $40.29bn.
   - Top-1,000 share: 54.30%, 51.95%, 53.72% and 49.06%. That is a fall of **5.24 points** (V51B-05).
   - Gini: 0.891, 0.885, 0.890 and 0.885.
   - HHI: 9.09, 11.11, 43.14 and 14.59.
   - DAF-weighted top-100 shares differ from filed shares by at most 0.28 points (V51B-20).

3. **The FY2023 spike: the values are right, but the sum and one description are off (V51B-06).**
   - The values: Johns Hopkins $1,558,446,223; Navigation $1,309,000,000; the four CZ LLCs $1,656,553,619.
   - They sum to **$4.52bn, not $4.53bn**.
   - Johns Hopkins is not a "single-sponsor line". Its FY2023 total comes from 27 panel sponsors: Fidelity Charitable $831.9m, Schwab Charitable $481.8m, JCF $140.9m, NPT $68.8m and others. Only the Navigation and CZ recipients are single-sponsor (SVCF).

4. **Further Future Foundation and Navigation Charitable Fund are one entity (V51B-07).**
   - SVCF's CY2023 Schedule I line reads "Further Future Foundation", EIN 921117448, $1,309,000,000, purpose "Sciences".
   - The recipient's own FY2023 990 (same EIN) gives its name as "NAVIGATION CHARITABLE FUND (FKA FURTHER FUTURE FOUNDATION)", doing business as The Navigation Fund. The name-change box is checked; it was formed in 2022 in Delaware.
   - The BMF has NAVIGATION CHARITABLE FUND, foundation code 15, ruling 2023-03, NTEE U05.
   - So no study is wrong. Docs that use only the old name should carry the current one, and corrections are proposed below. b51-01 also uses only the old name; it is left to wave 51A.

5. **The growth lists and their classification are confirmed (V51B-08 to 10, 12).**
   - Panel totals: P1 $64.66bn, P2 $76.82bn, +$12.17bn (+18.8%). 2,167 recipients clear the floor.
   - Top 50 by absolute growth: +$8.71bn, which is 71.6% of growth; the top 10 add $5.82bn. Johns Hopkins grows by $2,129,712,820.
   - My own list of the top 50 by absolute growth has the same EINs as the CSV.
   - Classification of the 50: new organisations 10, fiscal sponsors 3, intermediaries 16, universities 11, CZ LLCs 4. The full type list in §0 also matches.
   - Percentage list: median P1 $25,000; 44 have P1 under $100k; for 15 The Chicago Community Trust is the top grantor (its share 0.63–1.00); 20 have a single grantor.
   - Entrants: 206, with $5.59bn (46.0% of growth). 77 are new organisations, and Navigation plus the CZ LLCs account for $2.97bn.
   - In `pct_p1_1m`, three percentages are truncated rather than rounded: they should read 3,948%, 2,890% and 2,567% (V51B-11).

6. **All 18 spot-checked grower lines match the raw XML to the dollar (V51B-18).** They cover 11 returns and 10 sponsors: SVCF, SPMF, Servant, UCLA Foundation, CCT, JCF, CJP, Dechomai, GS DAPF and Schwab.

7. **Marin CF → Dayton Foundation Plus: the line is confirmed, but it is not DAF-to-DAF under the repo's definition (V51B-14, 15).**
   - **Marin's side.**
     - The FYE 2022-06-30 Schedule I line is $385,691,381 in cash, purpose "TRANSFER OF ASSETS". A second $5,455,497 "TRANSFER OF ASSETS" line follows in FYE 2023.
     - Marin's Schedule D DAF grants jump from $101.5m to $514.3m that year, then return to $114.5m, so the money very likely left Marin's DAF column [I].
   - **Dayton Foundation Plus.**
     - It is a 509(a)(3) **Type II** supporting organisation of The Dayton Foundation (EIN 31-6027287), which is its sole member and is on the whitelist (W3).
     - It answers Yes to Part IV line 6. In Schedule D, column (a) (DAFs) is blank in every year FY2020–24, and everything is in column (b), "funds and other accounts": 78 funds, $389.7m of contributions and $399.7m at year end in FYE 2022.
     - It is not in the DAFRC panel. BMF: foundation code 17, NTEE T11.
   - **Whitelist assessment.** The whitelist exists to stop DAF grants being counted twice in DAFRC market totals. Dayton Plus reports no DAFs and sits outside the panel, so there is nothing to double count. I recommend **not extending the whitelist** on this case. Treat the line as a sponsor-family fund transfer: name it in the study and keep it in the existing non-DAFRC sensitivity. A repo-wide rule for transfers to supporting organisations of panel sponsors can stay under P-B5102-01.
   - **Open reconciliation.** Dayton Plus books $361.9m of its FY2022 contributions as non-cash, while Marin reports cash. The returns cannot reconcile this.

8. **A second sponsor-family transfer sits in the FY2022 top 10 (V51B-17).**
   - GHCF's FY2022 line of $170,000,000 (purpose "PUBLIC BENEFIT") goes to WoodNext Philanthropies (EIN 88-1330756). The BMF lists that EIN under the name GREATER HOUSTON COMMUNITY FOUNDATION as a Type I supporting organisation (foundation code 21).
   - The self-line rule does not catch it.
   - Dropping both the Dayton Plus and WoodNext lines moves FY2022 top-10 from 7.67% to 7.11% and top-1,000 from 51.95% to 51.16%. FY2021 and FY2024 are unchanged, so the trend conclusions stand.

9. **The classification is neutral (V51B-19).**
   - `type_of` uses only BMF NTEE and foundation codes, repo lists and university, college or hospital name tests.
   - A keyword search of the study finds no viewpoint or partisan characterisation.
   - "Policy or advocacy" is code-defined. It is applied to The 85 Fund (I01) by code alone.
   - Minor: EIN 83-3403946 (filed "Eames Institute") carries the BMF name San Antonio Valley Ranch LLC. Its type comes from NTEE A54 and is unaffected.

## Accept / modify / reject

| Claim | Register | Decision | Note |
|---|---|---|---|
| FY2023–24 reproduction; script reproducibility | V51B-01, 02 | Accept | Exact |
| Balanced-panel table; Gini/HHI; top-1,000 −5.2 pts | V51B-03 to 05 | Accept | Independent code matches |
| FY2023 spike breakdown | V51B-06 | Modify | $4.52bn; JHU is multi-sponsor (27) |
| Navigation = Further Future (same EIN) | V51B-07 | Accept | Add the filed name in b51-02 and the current name in older docs |
| Top-50 growth $8.71bn / 72%; JHU +$2.13bn | V51B-08 | Accept | |
| Classification of the 50 | V51B-09 | Accept | |
| Percentage list (CCT) | V51B-10 | Accept | |
| pct_p1_1m percentages | V51B-11 | Modify | Rounding: 3,948 / 2,890 / 2,567% |
| Entrants 206 / $5.59bn | V51B-12 | Accept | |
| CZ merged 16.6% | V51B-13 | Accept | |
| Marin → Dayton Plus $385.7m line | V51B-14 | Accept | Purpose “TRANSFER OF ASSETS” |
| Dayton Plus as a DAF holder / DAF-to-DAF | V51B-15 | Modify | Not a DAF sponsor on its filings; whitelist not to be extended |
| Non-DAFRC sensitivity | V51B-16 | Accept | |
| FY2022 top-10 list | V51B-17 | Modify (interpretation) | Add the WoodNext intra-family transfer |
| Spot-check of 18 grower lines | V51B-18 | Accept | 18/18 exact |
| Neutral classification | V51B-19 | Accept | |
| DAF-weighted ≤ 0.3 pt | V51B-20 | Accept | |

## Exact corrections

### `research/mission-2026-11-14/b51-02-recipient-concentration-growth.md`

**Find:** "The FY2023 spike comes from a few very large single-sponsor lines:"
**Replace with:** "The FY2023 spike comes from three very large recipients, two of them paid by SVCF alone: [V wave 51B]"

**Find:** "  - Johns Hopkins University, $1.56bn;"
**Replace with:** "  - Johns Hopkins University, $1.56bn from 27 sponsors (largest lines: Fidelity Charitable $831.9m, Schwab Charitable $481.8m); [V wave 51B]"

**Find:** "  - the Navigation Charitable Fund, $1.31bn (one SVCF line);"
**Replace with:** "  - the Navigation Charitable Fund, $1.31bn (one SVCF line, filed as “Further Future Foundation”: the same EIN, 92-1117448, renamed 2023-11-01); [V wave 51B]"

**Find:** "These are $4.53bn of the $5.64bn top-10 total in FY2023 [F]."
**Replace with:** "These are $4.52bn of the $5.64bn top-10 total in FY2023 [F]. [V wave 51B]"

**Find:** "Murmuration Research Institute (W99; +3,947%), Jackson Hole Classical School (+2,889%), BeyGood Foundation (T30; +2,566%)"
**Replace with:** "Murmuration Research Institute (W99; +3,948%), Jackson Hole Classical School (+2,890%), BeyGood Foundation (T30; +2,567%) [V wave 51B]"

**Find:** "Whether such lines are DAF-to-DAF is queued (P-B5102-01)."
**Replace with:** "Marin’s purpose text is “TRANSFER OF ASSETS”, and its Schedule D DAF grants jump from $101.5m (FY2021) to $514.3m (FY2022) before returning to $114.5m, so the money very likely left Marin’s DAF column [I]. The recipient is a 509(a)(3) Type II supporting organisation of The Dayton Foundation (its sole member). It answers Yes to Part IV line 6 but reports its 78 funds ($399.7m) only in Schedule D column (b), “funds and other accounts”, never as DAFs (FY2020–24), and it is outside the DAFRC panel. So the line is a sponsor-family fund transfer, not DAF-to-DAF under the repo’s whitelist, which should not be extended for it. FY2022 also holds GHCF’s $170.0m line (purpose “PUBLIC BENEFIT”) to WoodNext Philanthropies (EIN 88-1330756), which the BMF lists under the name Greater Houston Community Foundation as a Type I supporting organisation; the self-line rule does not catch it. Dropping both lines moves FY2022 top-10 from 7.67% to 7.11% and top-1,000 from 51.95% to 51.16%; FY2021 and FY2024 are unchanged. A repo-wide rule stays queued (P-B5102-01). [V wave 51B]"

**Find:** "Lines to other DAF holders (e.g. Dayton Foundation Plus) stay in;"
**Replace with:** "Lines to other donor-advised or sponsor-family holders (e.g. Dayton Foundation Plus, which reports its donor funds only as “funds and other accounts”, and GHCF’s supporting organisation WoodNext Philanthropies) stay in; [V wave 51B]"

### `research/mission-2026-11-14/b39n603-02-g191302-03-bright-funds-svcf.md`

**Find:** "- Further Future Foundation's status was not checked (P-B39N60302-05)."
**Replace with:** "- Further Future Foundation's status was not checked here (P-B39N60302-05). Later waves resolved it: the same EIN (92-1117448) renamed itself Navigation Charitable Fund on 2023-11-01; its FY2023 990 is filed as “Navigation Charitable Fund (fka Further Future Foundation)”; BMF ruling 2023-03, NTEE U05, foundation code 15. [V wave 51B]"

### `research/mission-2026-11-14/direction-recipients-impact-matching.md`

**Find:** "SVCF's single lines to Further Future Foundation ($1.31bn)"
**Replace with:** "SVCF's single lines to Further Future Foundation ($1.31bn; now Navigation Charitable Fund, same EIN 92-1117448) [V wave 51B]"

### `research/mission-2026-11-14/gap19-exception-load-proxy.md`

**Find:** "Further Future Foundation (BMF ruling 2023-03)"
**Replace with:** "Further Future Foundation (BMF ruling 2023-03; now Navigation Charitable Fund, same EIN 92-1117448) [V wave 51B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.78 Recipient concentration and fastest growers (validated, wave 51B)\n\n**Recipient concentration and fastest growers** (validated, wave 51B). A scratch rerun of b51-02 reproduced its CSV byte for byte, and independent code (its own netting pass, a Lorenz-curve Gini and HHI) matched every concentration row. On the 44-sponsor balanced panel, net Schedule I dollars rose from $31.23bn (FY2021) to $40.29bn (FY2024). The top-1,000 share fell 5.2 points, from 54.3% to 49.1%, while Gini stayed between 0.885 and 0.891. The FY2023 top-10 spike (15.4%) is $4.52bn of $5.64bn. It comes from Johns Hopkins ($1.56bn from 27 sponsors), four CZ Biohub LLCs ($1.66bn) and SVCF’s $1.309bn line to Further Future Foundation, which is the renamed Navigation Charitable Fund under the same EIN (92-1117448). The 50 largest growers added $8.71bn, 72% of panel growth; 18 of their lines re-read in raw XML matched exactly. Marin CF’s FY2022 $385.7m “transfer of assets” very likely left Marin’s DAF column. It went to a Dayton Foundation supporting organisation that reports no DAFs, so it is a sponsor-family transfer, not DAF-to-DAF, and the whitelist need not be extended for it (repo [`validation-wave51b-report.md`](mission-2026-11-14/validation-wave51b-report.md)). [V wave 51B]\n\n---\n\n## Source register"
