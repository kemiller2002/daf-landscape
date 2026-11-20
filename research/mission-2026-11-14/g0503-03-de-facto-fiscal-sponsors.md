# P-G0503-03: de facto fiscal sponsors, derived from the filings themselves

**Date:** 2026-11-20 · **Task:** g0503-03 · **Queue item:** P-G0503-03 (from [queue-proposals-g0503-0501.csv](../../data/mission-2026-11-14/queue-proposals-g0503-0501.csv)) · **Builds on:** [g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md), including its wave-39C corrections. The governing base is still 608,610 proxy lines (604,913 Schedule I lines plus Schedule F recipients) and $92.72bn.

**Outputs**
- [`data/mission-2026-11-14/de-facto-fiscal-sponsors-2026-11-20.csv`](../../data/mission-2026-11-14/de-facto-fiscal-sponsors-2026-11-20.csv): 178 rows, one for every recipient EIN with at least one valid project-style line (§7).
- [`scripts/mission_de_facto_fiscal_sponsors.py`](../../scripts/mission_de_facto_fiscal_sponsors.py): stdlib, functional style.
  - It imports `mission_exception_refined.py` unchanged. That file was not modified, and neither was `mission_exception_load.py`.
  - It rebuilds the refined flags with the imported functions. Its "refined_as_published" re-cut matches the published figures exactly: fiscal sponsor 2,682 lines and $1,799.8m; core 7.76% / 11.61%; broad 24.79% / 19.85%.
  - Two runs gave byte-identical summaries.
- [`data/mission-2026-11-14/queue-proposals-g0503-03.csv`](../../data/mission-2026-11-14/queue-proposals-g0503-03.csv): P-G050303-01..05.

**Labels:** **[F]** filed value; **[C]** computed by the script; **[I]** inference or hand judgement.

**Framing.** As in the parent notes, a flag means a line would plausibly fall outside a sponsor's routine path. It does not mean the grant was improper.

---

## 0. Answers in brief

| Question | Answer |
|---|---|
| Project-style lines found | 1,184 lines have a connector [C]:<br>- 346 are valid project-style detections ($41.5m), on 178 recipient EINs;<br>- 43 are unverified;<br>- 795 were rejected by the name rules (§1.3). |
| **De facto hosts (≥ 3 distinct projects)** | **11 EINs** [C]: Tides Center (12 projects), Tides Foundation (8), Social Good Fund (8), Movement Strategy Center (7), Assets Under Movement (filed as Amalgamated Charitable Foundation; 6), GlobalGiving Foundation (6), Possibility Labs (6), Common Counsel Foundation (5), Players Philanthropy Fund (EIN 27-6601178, BMF name Stonier Scholarship Inc; 4), NEO Philanthropy (3), Center for Third World Organizing (3).<br>All 11 fall in the `intermediary_other` host class. No university, hospital or church reaches three projects. |
| **Hosts the directory misses** | **6 of the 11** are not keyed in the Fiscal Sponsor Directory list [C]:<br>- Tides Foundation, which is caught only because it is one of the 19 Q-B15 hosts;<br>- **5 hosts that neither list has**: Assets Under Movement / Amalgamated Charitable Foundation ($58.0m of top-50 lines), GlobalGiving ($33.0m), Possibility Labs ($10.9m), Common Counsel ($10.5m), Center for Third World Organizing ($2.1m).<br>With a threshold of ≥ 2 projects, 19 intermediary hosts are not yet counted. |
| **Directory hosts never seen in project-style lines** | **317 of the 337 keyed directory EINs** never appear in a project-style line [C].<br>- 201 of these receive top-50 lines: $703.2m in all, including Rockefeller Philanthropy Advisors, 50CAN, Global Impact, Myriad USA, Edward Charles Foundation, New Horizons Foundation and Give2Asia.<br>- Only 20 directory EINs have any project-style line, and 5 reach three projects.<br>- Of the 20 Q-B15 EINs, 4 are de facto hosts, 9 have one or two project-style lines and 7 have none. The 7 are North Star Fund, RPA, FJC, Propel Nonprofits, Hopewell Fund, Multiplying Good and Public Health Institute. |
| **Dollars added to the fiscal-sponsor category** | The 5 new hosts, counting every top-50 line to their EINs, as the EIN-keyed method does [C]:<br>- **190 lines, $114.6m: 0.124% of proxy dollars** (0.126% of Schedule I dollars).<br>- DAF-weighted: $103.2m, 0.120% of $86.38bn.<br>- Counting only the project-style lines themselves: $6.5m (0.007%).<br>- At ≥ 2 projects: 19 hosts, 362 lines, $183.6m, 0.198%. |
| Fiscal-sponsor share | **0.44% / 1.94% → 0.47% / 2.06%** of lines / dollars (2,682 → 2,872 lines; $1,799.8m → $1,914.4m) [C].<br>At ≥ 2 projects: 0.50% / 2.14%. |
| **Core union** | **7.76% / 11.61% → 7.79% / 11.73%**: +178 lines and +$108.8m. Twelve of the 190 lines were already in the core through another flag [C].<br>At ≥ 2 projects: 7.82% / 11.80%. |
| **Broad union** | **24.79% / 19.85% → 24.82% / 19.97%** (150,898 → 151,076 lines) [C].<br>At ≥ 2 projects: 24.85% / 20.04%. |
| Precision, hand check of 30 detections | **Parse: 29 / 30 (97%)**. Host and beneficiary were split correctly and are distinct; the one miss names the same food bank on both sides.<br>**Plausible fiscal sponsorship (project hosted by an intermediary): 21 / 30 (70%)** over all classes; **19 / 21 (90%)** among `intermediary_other` hosts.<br>The class rule removes 7 of the 9 non-sponsorship detections: university units, a diocesan appeal, a Salvation Army centre, a community-foundation fund [I]. |
| **Main caveat** | **82% of valid detections (284 of 346) are on one sponsor's Schedule I: ImpactAssets.** 10 of the 11 de facto hosts reach three projects only through ImpactAssets lines. Tides Foundation also has a US Charitable Gift Trust detection, but it repeats an ImpactAssets project (Movement Voter Fund). Only Players Philanthropy Fund reaches three projects without ImpactAssets (three sponsors) [C] [V wave 43B]<br>The method therefore measures one filer's naming convention ("HOST FBO PROJECT") more than the market. The other sponsors almost always file the host name alone. |

**Reading [I]**
- Read from the filings, the de facto fiscal-sponsor set is small and mostly already listed: 6 of the 11 hosts are on the refined list.
- Adding the other five moves the fiscal-sponsor dollar share by about a tenth of a point, and the core and broad unions by 0.03 pp of lines and 0.12 pp of dollars. The headline proxy (core ≈ 7.8% / 11.7%, broad ≈ 25% / 20%) is unchanged in substance.
- The bigger message runs the other way. The directory-keyed list cannot be confirmed from filer naming for 94% of its EINs (317 of 337), even for most of the 221 that receive top-50 grants. This is not evidence against them. The filer convention appears at one sponsor only, so absence of "FBO" lines says almost nothing.

---

## 1. Method

### 1.1 Lines and weights

- **Lines:** `mission_exception_refined.load_screened`, i.e. the `mission_exception_load.py` pipeline:
  - top-50 DAFRC sponsors and 94 itemising sponsor-years;
  - Schedule I lines from the line cache (`[ein, name, where, irc, cash, noncash]`);
  - **totals rows dropped** by `mission_exception_load.drop_totals_rows`;
  - DAF-to-DAF lines marked from the whitelist.
- That gives 604,913 lines and $90.81bn of Schedule I dollars.
- **Shares** use the proxy denominator (Schedule I + Schedule F = 608,610 lines, $92.72bn), so they are comparable with the published unions.
- **DAF weighting.** `mission_exception_load.py` does *not* apply DAF weighting. It drops totals rows and reports DAF-to-DAF lines (`*_ex_d2d`).
  - The DAF weighting used in the repo is the one in `mission_recipient_sectors.py`: each sponsor-year's lines × its `daf_share_of_grants` from `sponsor-cost-structure.csv`, capped at 1. That weighting is applied here as a second basis (94 of 94 sponsor-years have a weight; $86.38bn weighted).
  - The union re-cut stays on the filed-dollar basis of the published proxy.
  - The added dollars are also reported without DAF-to-DAF lines: none of the 190 added lines is DAF-to-DAF.

### 1.2 Detection rules (published in the script docstring)

Names are normalised with `mission_exception_load.upname`: upper case, `&` → AND, every other non-alphanumeric character → space.
- IRS e-file business names cannot contain "/". Filers therefore type "c/o" as `CO`, `C O` or `C-O`, and "f/b/o" as `FBO`.
- In the 2026-11 BMF, by contrast, names do keep "/": SAMOSET FIRE CO OF BRISTOL C/O … is an example.

| Rule | Regex (on normalised name) | Default host side |
|---|---|---|
| R1 fbo | `\bF ?B ?O\b` \| `\bFOR (THE )?BENEFIT OF\b` | left ("X FBO Y") |
| R2 care_of | `\bIN CARE OF\b` \| `\bC O\b` \| `\bCO\b` | right ("Y c/o X") |
| R3 on_behalf_of | `\bON BEHALF OF\b` \| `\bO B O\b` \| `\bOBO\b` | left |
| R4 project_of | `\bA PROJECT OF\b` \| `\bFISCALLY SPONSORED BY\b` \| `\bFISCAL SPONSOR (FOR\|OF)\b` | right |

- The leftmost connector splits the name into a left and a right side; ties go by rule order.
- Bare "CARE OF" and "PROJECT OF" without "A" were tested and dropped. They were legal-name phrases in every valid hit, for example HOSPICE AND PALLIATIVE CARE OF IREDELL COUNTY and INNOCENCE PROJECT OF TEXAS.

### 1.3 Name rules (all must hold)

| Rule | Test | Lines rejected |
|---|---|---|
| N1 | Recipient EIN present (not blank or placeholder) | 6 |
| N2 | **Legal-name guard**: the connector rule does not also match the EIN's current BMF name. Examples: BARRINGTON STAGE CO INC, JEWISH COMMUNITY PROJECT OF LOWER MANHATTAN, LIBRARY FOUNDATION FOR THE BENEFIT OF …, AMERICAN TRUST … FBO (a trust account) | 554 ($37.9m) |
| N3 | **Host side.** A side matches when at least half of its non-generic tokens are in the EIN's reference names: the current BMF name plus the modal plain filed name for that EIN.<br>A token counts as present when it is exact, a prefix of 3 or more characters, an acronym or acronym prefix (TSNE, MCV), or a run-together substring of 5 or more characters (SOCIALGOOD).<br>If exactly one side matches, it is the host; if both match, the default side; if neither, `unverified`, which is not counted | 43 unverified ($1.4m) |
| N4 | **Project side** must:<br>- contain a token of at least 2 letters (160 rejected, mostly "… CO" county or company endings);<br>- not consist only of host tokens (20);<br>- for bare `CO`: not follow OF / AND / THE / IN / FOR, appear in a raw name without "(", and contain a non-generic token (14);<br>- for R2 with the host on the left ("X c/o Z"): Z must carry an organisation word (FUND, PROJECT, COALITION, TRUST, …) and no addressee marker (LLP, LLC, ESQ, TREASURER, MANAGEMENT, OFFICE, …). This rejects mailing addressees such as "THE BUDDY FUND CO TIM MURCH" and "THE LENNY ZAKIM FUND CO DLA PIPER LLP" (41) | 235 |
| N5 | **Distinct projects** per EIN: keys (`mission_exception_refined.name_key`) are merged when they have the same token set, or when one is a prefix of 5 or more characters of a longer key. This handles truncation, as in MOVEMENT VOTER FU / MOVEMENT VOTER FUND | — |

- **De facto host:** at least **3** distinct projects from valid detections. ≥ 2 is reported as a sensitivity.
- **Host class**, in order:
  1. `university_college`: NTEE B4/B5 or UNIVERSITY / COLLEGE;
  2. `hospital_health`;
  3. `school_k12`;
  4. `religious_body`;
  5. `community_foundation_united_way`: T31/T70 or the name says so;
  6. then BMF FOUNDATION 10 / 11 / 12;
  7. group-exempt national bodies;
  8. else `intermediary_other`.
- Only `intermediary_other` hosts that are not already counted by the refined flag enter the headline "added" set. Already counted means a Q-B15 or directory host, excluding the community-foundation and United Way hosts that the refined flag leaves out.
- Added hosts are flagged on every top-50 line to their EIN, the same rule the refined EIN-keyed list uses.

### 1.4 Re-cut of the unions

Lines to added EINs gain `fiscal_sponsor_name`, `any_si` and `any_core_si`, on top of their refined flags. The pooled tallies and shares are then recomputed with `mission_exception_load.tally / add / shares`, with Schedule F unchanged.

## 2. Results [C]

### 2.1 Detections

| | Lines | $ |
|---|---|---|
| Connector present | 1,184 | — |
| Valid | 346 | $41.5m |
| … R1 fbo | 328 | $41.2m |
| … R2 care_of | 15 | $0.29m |
| … R3 on behalf of | 1 | $0.01m |
| … R4 a project of | 2 | $0.01m |
| Unverified | 43 | $1.4m |
| Rejected (N1, N2, N4) | 795 | $51.6m |

- **EINs with valid detections:** 178. By distinct projects: 1 → 142; 2 → 25; 3 → 2; 4 → 1; 5 or more → 8.
- **Host classes of the 178:** intermediary_other 132, religious_body 20, university_college 18, community_foundation_united_way 4, school_k12 3, hospital_health 1.
- **By filer**, valid lines (distinct hosts):

  | Filer | Valid lines (hosts) |
  |---|---|
  | ImpactAssets | **284 (136)** |
  | Raymond James Charitable | 27 (22) |
  | Morgan Stanley GIFT | 23 (16) |
  | US Charitable Gift Trust | 5 (4) |
  | NPT | 3 (3) |
  | California Community Foundation | 3 (3) |
  | DAFgiving360 | 1 (1) |

  The other 41 of the 48 itemising sponsors contribute none.

### 2.2 De facto hosts (≥ 3 projects)

| EIN | Host (BMF; filed name) | Projects | Filers | Top-50 lines | Top-50 $ | Directory | Q-B15 | Already counted |
|---|---|---|---|---|---|---|---|---|
| 943213100 | Tides Center | 12 | 1 | 75 | $68.1m | yes | yes | yes |
| 510198509 | Tides Foundation | 8 | 2 | 85 | $112.2m | no | yes | yes |
| 461323531 | Social Good Fund | 8 | 1 | 57 | $19.9m | yes | yes | yes |
| 201037643 | Movement Strategy Center | 7 | 1 | 30 | $4.6m | yes | no | yes |
| 821517696 | Assets Under Movement (filed: Amalgamated Charitable Foundation) | 6 | 1 | 58 | $58.0m | no | no | **added** |
| 300108263 | GlobalGiving Foundation | 6 | 1 | 54 | $33.0m | no | no | **added** |
| 853989363 | Possibility Labs | 6 | 1 | 26 | $10.9m | no | no | **added** |
| 943214166 | Common Counsel Foundation | 5; 4 after merging “Fund for the Movement 4 Black Lives” and “M4BL” [V wave 43B] | 1 | 34 | $10.5m | no | no | **added** |
| 276601178 | Stonier Scholarship Inc (filed: Players Philanthropy Fund) | 4 | 3 | 45 | $17.3m | yes | yes | yes |
| 133191113 | NEO Philanthropy | 3 | 1 | 44 | $47.5m | yes | no | yes |
| 521211059 | Center for Third World Organizing | 3 | 1 | 18 | $2.1m | no | no | **added** |

- **Next tier: 2 projects, intermediary class, not yet counted** (14 hosts; top-50 $):
  - Digital Harbor Foundation $27.1m;
  - Sustainable Markets Foundation $12.3m;
  - Sustainable Economies Law Center $4.6m;
  - Resist $4.4m;
  - Project South $4.2m;
  - Center for Economic Democracy $3.5m;
  - Runway Root $2.8m;
  - MICA Group $2.8m;
  - Common Future $2.8m;
  - Allied Media Projects $1.9m;
  - WESPAC Foundation $1.6m;
  - EIN 842045603 (not in the BMF) $0.6m;
  - Movement Alliance Project $0.6m;
  - Centro por la Justicia $0.06m.
- Two-project hosts already counted: New Venture Fund, Windward Fund, TSNE, Fractured Atlas, Open Collective Foundation, SEE and Inquiring Systems.
- Two-project hosts outside the intermediary class: UCSF Foundation, USC, American Endowment Foundation and Greater Cincinnati Foundation.

### 2.3 Comparison with the directory list and the Q-B15 hosts

| Set | EINs | … de facto (≥ 3) | … any project-style line | … none, but receives top-50 lines |
|---|---|---|---|---|
| Directory, keyed (fiscal-sponsor-ein-list, source = directory) | 337 | 5 | 20 | **201 ($703.2m)** |
| Q-B15 hosts (EIN-keyed) | 20 | 4 | 13 | 7 |
| De facto set | 11 | — | 11 | — |

- **Missed by the directory:** Tides Foundation (Q-B15 only), plus the 5 added hosts above.
- **Largest directory hosts with top-50 lines but no project-style line:**
  - Rockefeller Philanthropy Advisors $245.9m (a Q-B15 host);
  - 50CAN $94.2m;
  - Global Impact $51.5m;
  - Myriad USA $46.5m;
  - Edward Charles Foundation $23.5m;
  - New Horizons Foundation $20.2m;
  - Give2Asia $12.0m;
  - Good Nation Foundation $9.7m;
  - Redford Center $9.3m;
  - Southern Vision Alliance $8.9m.
- These include the four hosts the parent note treats as upper-bound cases (50CAN, Global Impact, NEO, Myriad). Of those four, only NEO Philanthropy shows project-style lines.

### 2.4 Effect on the fiscal-sponsor category and the unions (count / dollar share)

| Scope | Fiscal sponsor: refined → +de facto (≥ 3) → +≥ 2 | Core: refined → ≥ 3 → ≥ 2 | Broad: refined → ≥ 3 → ≥ 2 |
|---|---|---|---|
| All top-50 itemising (94) | 0.44 / 1.94 → **0.47 / 2.06** → 0.50 / 2.14 | 7.76 / 11.61 → **7.79 / 11.73** → 7.82 / 11.80 | 24.79 / 19.85 → **24.82 / 19.97** → 24.85 / 20.04 |
| Big-4 nationals | 0.24 / 2.05 → 0.26 / 2.15 → 0.27 / 2.25 | 7.55 / 10.62 → 7.56 / 10.71 → 7.58 / 10.81 | 27.79 / 18.00 → 27.80 / 18.10 → 27.82 / 18.19 |
| National | 0.32 / 2.09 → 0.35 / 2.24 → 0.38 / 2.33 | 7.29 / 10.49 → 7.31 / 10.64 → 7.34 / 10.73 | 26.10 / 17.70 → 26.12 / 17.85 → 26.15 / 17.94 |
| Community foundation | 1.19 / 1.67 → 1.26 / 1.77 → 1.31 / 1.83 | 9.39 / 16.84 → 9.46 / 16.94 → 9.51 / 16.99 | 17.86 / 29.27 → 17.93 / 29.37 → 17.99 / 29.42 |
| Faith | 0.32 / 2.02 → 0.33 / 2.02 → 0.34 / 2.03 | 8.38 / 10.21 → 8.39 / 10.21 → 8.40 / 10.22 | 23.97 / 18.82 → 23.98 / 18.82 → 23.99 / 18.83 |

- The added dollars are concentrated: Assets Under Movement is $58.0m of the $114.6m.
- Assets Under Movement / Amalgamated Charitable Foundation (NTEE T30) also runs donor-advised and pooled funds, so part of its $58.0m may be DAF-to-DAF or pooled-fund flow rather than fiscal sponsorship. It is not on the DAF-to-DAF whitelist (P-G050303-02) [I].
- Without it, the ≥ 3 addition is $56.6m (0.061%) [C, from the per-EIN figures]. None of its 58 lines carries another flag, so without it the fiscal-sponsor share is 0.46% / 2.00%, the core 7.78% / 11.67% and the broad union 24.81% / 19.90%. Assets Under Movement, Possibility Labs and Common Counsel are all DAFRC-vetted DAF sponsors (DAF share of grants 0.73, 0.65 and 0.62 in sponsor-cost-structure.csv; the DAF-to-DAF whitelist excludes them under rules W2 and W4), so part of their $79.4m may be DAF-to-DAF flow. Only $1.06m of Assets Under Movement’s $58.0m arrives on project-style lines. Its site offers DAFs and collaborative or pooled funds and supports “sponsored projects”, so it is a hybrid, not a pure fiscal sponsor. The ≥ 3 addition is best stated as $35.1m–$114.6m (0.04%–0.12% of proxy dollars); the lower end drops the three DAF-sponsor hybrids [V wave 43B]

## 3. Hand check (30 detections) [I]

- **Sample:** the first 30 valid detections ordered by SHA-1 of `sponsor_ein|fiscal_year|line_index`. This is deterministic, and the script's `--sample-out` writes it.
- 26 of the 30 are ImpactAssets lines, 2 Morgan Stanley GIFT and 2 Raymond James. That mirrors the 82% concentration.
- **Criteria:**
  - **(P) parse**: the host and beneficiary are split correctly and are different entities;
  - **(S) sponsorship**: the beneficiary is plausibly a project hosted by an intermediary, not a unit, campaign or component fund of the host. This is judged from the filed name and the BMF name only; no host web pages were consulted.

| # | Filed name (abridged) | Class | P | S |
|---|---|---|---|---|
| 1 | Partnership for the Advancement of New Americans FBO Detention Resistance | intermediary | ✓ | ✓ |
| 2 | TSNE MissionWorks CO MA Voter Table | intermediary | ✓ | ✓ |
| 3 | The Seeds Project FBO Earth Songs | religious_body | ✓ | ✓ |
| 4 | Sonoma State University FBO Green Music Center | university | ✓ | ✗ unit |
| 5 | Archdiocese of Denver FBO Archbishop's Catholic Appeal | religious_body | ✓ | ✗ own appeal |
| 6 | Movement Strategy Center FBO Resonance Network | intermediary | ✓ | ✓ |
| 7 | Open Collective Foundation FBO Collective Diaspora | intermediary | ✓ | ✓ |
| 8 | First In Foundation co Players Philanthropy Fund | intermediary | ✓ | ✓ |
| 9 | WESPAC Foundation FBO Palestinian Youth Movement | intermediary | ✓ | ✓ |
| 10 | Sustainable Prosperity FBO Day One Disaster Relief | intermediary | ✓ | ✓ |
| 11 | The Salvation Army FBO Pasadena Hope Center | religious_body | ✓ | ✗ own unit |
| 12 | Greater Cincinnati Foundation FBO Cincinnati Women … | cf / UW | ✓ | ✗ component fund |
| 13 | Dynamic Community Solutions FBO Puuhonua o Waianae | intermediary | ✓ | ✓ |
| 14 | MCV Foundation FBO School of Medicine | university | ✓ | ✗ unit |
| 15 | Movement Strategy Center FBO HEAL Food Alliance | intermediary | ✓ | ✓ |
| 16 | Second Harvest FBO Second Harvest Food Bank of Santa Clara and San Mateo Co | intermediary | ✗ same org | ✗ |
| 17 | Environmental Health Coalition FBO CEJA | intermediary | ✓ | ✓ |
| 18 | Movement Strategy Center FBO Just Homes | intermediary | ✓ | ✓ |
| 19 | Windward Fund FBO Heartland Fund | intermediary | ✓ | ✓ |
| 20 | Tides Center Inc FBO Arab Resource and Organizing Center | intermediary | ✓ | ✓ |
| 21 | The Giving Back Fund FBO Nexus | cf / UW (NTEE T70) | ✓ | ✓ |
| 22 | MICA Group FBO Mindfulness for All | intermediary | ✓ | ✓ |
| 23 | The Common Counsel Foundation FBO Native Voices Rising | intermediary | ✓ | ✓ |
| 24 | Amalgamated Charitable Foundations FBO New Sheriff in Town Fund | intermediary | ✓ | ✓ |
| 25 | New Mexico Community Capital FBO Native Women Lead | intermediary | ✓ | ✓ |
| 26 | Tides Center Inc FBO AROC (FY2024) | intermediary | ✓ | ✓ |
| 27 | Southern Conservation Partners FBO Earthseed Land Collective | intermediary | ✓ | ✓ |
| 28 | UCSF Foundation FBO UCSF Maternal Depression … Fund | university | ✓ | ✗ unit fund |
| 29 | Woodstock Community Trust FBO Woodstock Area Relief Fund | intermediary | ✓ | ✗ component fund |
| 30 | University of Southern California FBO Emerge Lab | university | ✓ | ✗ unit |

- **Parse precision: 29 / 30 = 96.7%.**
- **Sponsorship precision: 21 / 30 = 70%** over all classes; **19 / 21 = 90.5%** in `intermediary_other`. The 2 misses are #16 and #29. A validator re-read reproduces parse 29 / 30. From names alone, sponsorship is 19–21 / 30, because #10 and #17 cannot be judged without host pages. #26 repeats #20’s project in another year, so the sample holds 29 distinct projects, and 21 / 30 has a Wilson 95% interval of about 52–83% [V wave 43B]
- The class rule removes 9 sampled detections: 7 non-sponsorship cases and 2 plausible ones (#3, and #21, The Giving Back Fund, a known fiscal sponsor caught by the T70 rule, as the parent note also found).
- **De facto host check** (all 11; names and filings only): 10 are recognisable fiscal sponsors or pass-through intermediaries [I]. GlobalGiving is a donation platform passing funds to (often foreign) projects, so it counts as an intermediary but not a fiscal sponsor in the narrow sense.
- **Recall is not measured.** Lines filed under the project's own name with the host's EIN (e.g. "SOL VIDA" or "HAPPENSTANCE THEATER" under Fractured Atlas's EIN; "Future Chefs" under TSNE) are not project-style names and are not detected (P-G050303-01).

## 4. Limits

- **Filer concentration.** ImpactAssets writes "HOST FBO PROJECT" routinely; most sponsors do not. The ≥ 3 rule therefore selects ImpactAssets' sponsored-project grantees. A "≥ 3 projects from ≥ 2 filers" rule, read as at least three projects outside ImpactAssets, leaves only Players Philanthropy Fund; Tides Foundation has two filers, but all eight of its projects come from ImpactAssets [V wave 43B] The set is a lower bound on de facto hosts, not a census.
- **Truncation.** Filed names are cut at about 35–75 characters, so some connectors and projects are lost (e.g. "Tides Foundation For benefit of Movement Voter Fu"). The prefix merge (N5) handles partial project names; names cut before the connector cannot be recovered.
- **Bare "CO".** It is ambiguous (company, county, Colorado, c/o). The N2 and N4 guards remove the cases seen. Some c/o lines with the host on the left that name real projects are rejected by the addressee rule, e.g. "TIDES CENTER CO VC INCLUDE" and "FUND FOR THE CITY OF NEW YORK CO POWER OF TWO". The same Tides project is still caught through an FBO line.
- **Host classes are name- and code-based.** NTEE T70 puts The Giving Back Fund in the community-foundation class, as in the parent note. Only `intermediary_other` hosts are added; including all classes changes nothing at ≥ 3, because no other class reaches 3.
- **Assets Under Movement.** The EIN carries the filed name "Amalgamated Charitable Foundation" on 1 sponsor's lines and the BMF name "ASSETS UNDER MOVEMENT". The script treats them as the same entity through the modal filed name. The name change was not checked against an IRS determination [I].
- **Hand check.** Judgements use filing text and BMF names only. No host pages were read, and the 30-line sample is dominated by one filer.
- All limits of the parent notes apply: recipient-level Schedule I, attachment-only sponsors (BofA, Renaissance), and directory self-listing.

## 5. Reproduction

```
python3 scripts/mission_de_facto_fiscal_sponsors.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
    --pub78 data-download-pub78.txt --revocation data-download-revocation.txt --efile-index-dir IRS \
    --bmf-archive-dir ARCH --fsd-html all-fiscal-sponsors-alpha-ordered.html [--out CSV] [--sample-out CSV]
```

- The inputs are exactly those of `mission_exception_refined.py` (parent §6).
- The archive, revocation and e-file inputs are needed only to rebuild the refined flags for the union re-cut.
- Run time is about 2–3 minutes.
- The JSON summary on stdout holds every figure quoted here:
  - `status`, `valid_by_rule`, `valid_by_sponsor`;
  - `eins_by_projects`, `de_facto_*`, `directory_*`, `q19_not_de_facto`;
  - `added`, `unions` (four variants × five scopes).
- No web requests were made in this task. The directory page is the 2026-11-19 cache used by the parent note.

## 6. Source register

| ID | Source | Version / access | robots.txt |
|---|---|---|---|
| S1 | IRS Form 990 Schedule I Part II lines, top-50 sponsors FY2023–24: e-file XML via the GivingTuesday mirror of IRS TEOS ([IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)) | line cache of P-NEW-REC-01; unchanged | per parent S1 |
| S2 | IRS EO BMF ([eo1–eo4, eo_pr, eo_xx](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf)): NAME, NTEE_CD, FOUNDATION, GROUP | Last-Modified 2026-11-09 (cached) | per parent |
| S3 | [IRS Pub 78 data](https://apps.irs.gov/pub/epostcard/data-download-pub78.zip) | cached 2026-11-11 | per parent |
| S4 | [Fiscal Sponsor Directory: All Fiscal Sponsors (alpha ordered)](https://fiscalsponsordirectory.org/all-fiscal-sponsors-alpha-ordered/), keyed list [`fiscal-sponsor-ein-list-2026-11-19.csv`](../../data/mission-2026-11-14/fiscal-sponsor-ein-list-2026-11-19.csv) | cached page, fetched 2026-11-19 (not re-fetched) | `User-Agent: * / Disallow:` (logged 2026-11-19, parent §8 S2) |
| S5 | Archived monthly EO BMF ([NCCS raw/bmf](https://nccsdata.s3.us-east-1.amazonaws.com/raw/bmf/2024-06-BMF.csv)), [IRS revocation list](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip), IRS e-file index 2021–2026 | as parent §8 S5–S8; used only to rebuild the refined recent-ruling flags | per parent |
| S6 | `sponsor-cost-structure.csv` (`daf_share_of_grants`) | repo file; used for the DAF-weighted basis | — |
| S7 | Schedule F figures, `daf-foreign-grants-schedule-f-2023-2024.csv` | repo file; denominator only | — |

## 7. Data dictionary: `de-facto-fiscal-sponsors-2026-11-20.csv` (178 rows)

One row per recipient EIN with at least one valid project-style line. Rows are sorted by distinct projects (descending), then by top-50 dollars.

| Column | Meaning |
|---|---|
| ein | Recipient EIN as filed |
| bmf_name, bmf_state, bmf_ntee, bmf_foundation | 2026-11 EO BMF name, state, NTEE code and FOUNDATION code (blank if not in the BMF) |
| modal_filed_name | Most frequent filed name for this EIN on lines with no connector; part of the N3 reference names |
| host_class | §1.3 class: university_college, hospital_health, school_k12, religious_body, community_foundation_united_way, federated_national, intermediary_other |
| distinct_projects | Distinct beneficiary keys after the N5 merge |
| project_style_lines, project_style_usd | Valid detections for this EIN, and their Schedule I $ |
| unverified_lines | Connector lines to this EIN where neither side matched the host (N3), not counted |
| rules_hit | Rules among valid detections (fbo; care_of; on_behalf_of; project_of) |
| sponsors | Distinct filing sponsors among valid detections |
| example_projects | Up to 6 canonical project keys, alphabetical |
| top50_lines, top50_usd | All top-50 FY2023–24 Schedule I lines and $ to this EIN (totals rows dropped) |
| top50_usd_daf_weighted | The same, with each sponsor-year's lines × its DAF share of grants (capped at 1) |
| in_directory, in_q19 | EIN keyed from the Fiscal Sponsor Directory; EIN is one of the 20 Q-B15 host EINs |
| in_refined_fs_flag | Already counted by the refined fiscal-sponsor flag (Q-B15 or directory, not an excluded community-foundation / United Way host) |
| grantmaker_host | Directory host excluded from the refined flag as a community foundation / United Way |
| de_facto_ge3 | distinct_projects ≥ 3 |
| de_facto_intermediary | de_facto_ge3 and host_class = intermediary_other |
| added_headline | de_facto_intermediary and not in_refined_fs_flag; these EINs are added in the headline re-cut (§2.4) |
