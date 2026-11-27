# Agent CD working notes (Tracks C and D), 2026-11-26

Working files, not durable modelling software (the durable model is F#, agent MOD).

- `bmf-untapped-counts.csv`: produced by `untapped.py`.
  - **Inputs:**
    - IRS EO BMF eo1-eo4.csv (https://www.irs.gov/pub/irs-soi/eo1.csv ... eo4.csv; Last-Modified 2026-11-09; downloaded 2026-11-26; not committed because of size);
    - `data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv` (DAFRC panel EINs);
    - the EIN list from `data/mission-2026-11-14/non-dafrc-daf-filers-990.csv` (all statuses except no_990_object_in_irs_index and xml_http_404; 2,441 EINs).
  - **Filters:** subsection 03; foundation codes 02/03/04 (private foundations) excluded; de-duplicated by EIN; ASSET_AMT thresholds.
  - **Run:** `python3 -I untapped.py <bmf_dir> <panel.csv> <out.csv> <extra_eins.txt>`
- **Education and health union counts:** from `union.py`, same inputs; foundation code 12/13 or NTEE B40-B43, B50, B11, B12, E20-E22, E24, E11, E12. Results by asset threshold [total, with DAF signal]:

  | Threshold | Total | With DAF signal |
  |---|---|---|
  | $10M | 7,233 | 159 |
  | $50M | 4,187 | 121 |
  | $100M | 3,056 | 99 |
  | $1bn | 675 | 48 |
- **Unfiltered BMF category counts:** 501(c)(3) rows including private foundations, from a first pass, for reference:
  - T31: 3,830 public and 294 private foundations;
  - foundation code 13: 2,919;
  - foundation code 12: 5,832;
  - T70: 2,529 public.
- `minimum-viable-program-grid.csv`: produced by `mvp.py`. N* = ceil(F / (B*f - v)); inputs are P3-ASM-CD001..CD006.
- **Web reads:** dates are in `../../fragments/CD/sources.csv`. Several sources were read only through search-result summaries; this is flagged in their limitations.
