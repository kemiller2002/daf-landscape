# P-G050303-01: sponsored projects filed under their own name with the host's EIN

**Date:** 2026-11-20 · **Task:** g050303-01 · **Queue item:** P-G050303-01 (from [queue-proposals-g0503-03.csv](../../data/mission-2026-11-14/queue-proposals-g0503-03.csv)) · **Builds on:** [g0503-03-de-facto-fiscal-sponsors.md](g0503-03-de-facto-fiscal-sponsors.md) §3–§4 (FBO-name rule; recall not measured). The governing base is unchanged: 604,913 Schedule I lines ($90.81bn), proxy denominator $92.72bn.

**Outputs**
- [`data/mission-2026-11-14/sponsored-project-recall-2026-11-20.csv`](../../data/mission-2026-11-14/sponsored-project-recall-2026-11-20.csv): 137 rows. These are the 122 own-name (NP) lines on keyed hosts, plus the 15-line "host plus extra" (HX) diagnostic sample. Hand-check classes are filled in for the 75 sampled rows (§7).
- [`data/mission-2026-11-14/sponsored-project-recall-handcheck-2026-11-20.csv`](../../data/mission-2026-11-14/sponsored-project-recall-handcheck-2026-11-20.csv): the 75 hand judgements. They are the `--hand` input of the script, so the estimates can be reproduced.
- [`scripts/mission_sponsored_project_recall.py`](../../scripts/mission_sponsored_project_recall.py): stdlib only, functional style.
  - It imports `mission_exception_refined.py` and `mission_de_facto_fiscal_sponsors.py` **unchanged**. Neither file was modified.
  - It rebuilds the keyed host index exactly as the de facto script does: 347 EINs, of which 332 are counted and 15 are grantmaker hosts.
  - Check: it reproduces the refined fiscal-sponsor figure of **$1,799,848,564**.
  - Two runs gave byte-identical JSON and CSV.
- [`data/mission-2026-11-14/queue-proposals-g050303-01.csv`](../../data/mission-2026-11-14/queue-proposals-g050303-01.csv): P-G05030301-01..05.

**Labels:** **[F]** filed value; **[C]** computed by the script; **[I]** hand judgement or inference.

**Framing.** As in the parent notes, a flag means a line plausibly falls outside a sponsor's routine path. It does not mean the grant was improper.

---

## 0. Answers in brief

| Question | Answer |
|---|---|
| Lines to the 347 keyed host EINs | **2,790 lines, $1,824.8m**, on 231 EINs that receive top-50 lines [C]. By class:<br>- 2,440 use the host's own name;<br>- **97 are FBO-rule detections ($7.38m, 26 EINs)**;<br>- **122 are flagged by the new own-name rule NP ($23.54m, 28 EINs)**;<br>- 122 are HX ("host plus extra" words, $10.32m, 43 EINs);<br>- 9 NP-type lines ($0.48m) are set aside because the DAF-to-DAF whitelist marks them. |
| Examples from the brief | All three are flagged [C]:<br>- SOL VIDA and HAPPENSTANCE THEATER, both under 11-3451703 (Fractured Atlas);<br>- Future Chefs, under 04-2261109 (TSNE). |
| **Precision of NP** (hand check of 60 of the 122 lines) | **38 / 60 = 63.3%** of lines are sponsored projects (Wilson 95%: 50.7–74.4%) [I]:<br>- 3 are confirmed by a host directory or by the filing text itself;<br>- 34 are likely projects;<br>- 1 is a project whose same-name entity already had its own exemption.<br>The other 22 are 20 host aliases and 2 host programmes.<br>**By dollars, precision is only 40.4%**: one host, Myriad USA, has 26 NP lines ($18.23m), and all of them are filed under its former name, King Baudouin Foundation United States.<br>**Without Myriad: 38 / 45 = 84.4%** of lines (Wilson 71.2–92.3%) and 93.6% of sampled dollars. |
| Estimated true project lines missed by the FBO rule | **≈ 77 lines and ≈ $3.7m** on keyed hosts, post-stratified by host [C from the hand classes]. |
| **Recall of the existing FBO-name rule** (keyed hosts) | **About 56% of project lines** (97 / (97 + 76.6)) [C].<br>- 53% if FBO detections carry their g0503-03 sponsorship precision of 19/21;<br>- 52–61% across the NP precision interval.<br>**About 67% of project dollars.**<br>Counting the HX lines too (3 of 15 sampled are projects): **≈ 49% of lines and ≈ 66% of dollars**. |
| **Added to the fiscal-sponsor dollar figure** | **$0** [C].<br>- All 122 NP lines go to *counted* keyed hosts. The refined EIN-keyed flag already counts every top-50 line to those EINs, whatever the filed name. None goes to the 15 community-foundation or United Way hosts.<br>- Sensitivity outside the keyed set: adding NP lines to the 107 non-keyed intermediary EINs that have at least one FBO detection promotes **no** new host to ≥ 3 projects (5 → 5).<br>**The governing range $35.1m–$114.6m (0.04%–0.12% of proxy dollars) is unchanged.** |
| What changes | Diagnostics only:<br>- keyed hosts with ≥ 3 distinct projects rise from 6 (FBO only) to 15 (FBO + NP);<br>- the FBO-name rule sees only about half of the hosted-project lines at listed hosts. Its silence on a host, e.g. "317 of 337 directory EINs never appear in a project-style line" (g0503-03 §0), is therefore even weaker evidence than the parent note said. |

**Reading [I]**
- Filers often write a project's own name with the host's EIN, and the pattern is real: 84% of the non-Myriad flagged lines are hosted projects.
- The pattern is concentrated in two community foundations. Seattle Foundation and The Denver Foundation file 64 of the 122 NP lines, and 31 of the 60 sampled lines are theirs. Morgan Stanley GIFT files 18 more.
- ImpactAssets, which dominates the FBO convention, files almost none (4 lines). The two conventions are complementary: different filers use different ones.
- For the dollar question the finding is negative but robust. The refined flag is keyed by EIN, so the naming convention cannot change the fiscal-sponsor dollars at listed hosts. Outside the list, the NP lines found so far are too few to lift any further host over the ≥ 3-project threshold.
- The open risk is hosts with neither a directory listing nor any FBO line (P-G05030301-01).

---

## 1. Method

### 1.1 Lines and keyed hosts
- **Lines:** `mission_exception_refined.load_screened`, unchanged. That is the top-50 DAFRC sponsors, 94 itemising sponsor-years and FY2023–24, with totals rows dropped and DAF-to-DAF lines marked from the whitelist.
- **Keyed host EINs:** `mission_exception_refined.fs_index` over the Q-B15 rows and the Fiscal Sponsor Directory rows. It is rebuilt with the imported functions exactly as `mission_de_facto_fiscal_sponsors.main` does.
  - The result is **347 distinct EINs**, matching the 2026-11-19 list (433 host rows, 347 EINs).
  - `counted` = 332: the refined flag counts every line to these EINs.
  - `grantmaker` = 15: community-foundation or United Way directory hosts, which the refined flag does not count.
- **Reference names per EIN:** the current EO BMF name, plus the modal plain filed name (`mission_de_facto_fiscal_sponsors.modal_plain`). These are the same references the FBO rule's host-side test uses.

### 1.2 The new rule NP ("own-name project") and the diagnostic class HX
Tokens are `name_key` tokens minus `mission_de_facto_fiscal_sponsors.WEAK`, i.e. the generic words (FOUNDATION, FUND, CENTER, …, INC, THE, OF).

A token counts as present in the references by `tok_hit`, the FBO rule's own test: exact; a prefix of 3 or more characters; an acronym or acronym prefix; or a run-together substring of 5 or more characters.

| Class | Test (line to a keyed EIN) |
|---|---|
| `fbo` | Valid FBO-rule detection (`mission_de_facto_fiscal_sponsors.detect` status `valid`) |
| **`np`** | **At least one non-generic token, and none present in the references.** Not DAF-to-DAF. |
| `np_d2d` | As `np`, but the DAF-to-DAF whitelist marks the line; set aside |
| `hx` | Some tokens present and some not; not counted (diagnostic) |
| `host` | All tokens present |
| `generic` | No non-generic token |

- `fbo` and `np` are disjoint by construction: a valid FBO detection needs a host side that matches.
- Of the 122 NP lines, 121 have no connector at all and 1 is an `unverified` connector line.

### 1.3 Hand check
- **Sample:** the first 60 NP lines, ordered by SHA-1 of `sponsor_ein|fy|line_index|np`. This is deterministic, and `--sample-out` writes it. 60 of 122 is 49% of NP lines.
- **HX diagnostic:** the first 15 HX lines in the same order.
- **Evidence, in order:**
  1. **Filing text.** Schedule I `BusinessNameLine1/2`, city and state, and `PurposeOfGrantTxt` from the e-file XML. Cached copies were used; 8 missing returns were fetched from the GivingTuesday data lake.
  2. **Other filers' text for the same EIN**, e.g. "THE PERFORMANCE ZONE INC AKA THE FIELD" and "FOUNDATION FOR NATIONAL PROGRESS DBA MOTHER JONES".
  3. **Same-name BMF entities**, with their ruling months. The script's `own_name_bmf_eins` column gives these.
  4. **Host project directories, where robots allows (§8).**
- **Classes:**
  - `project_confirmed`: a host directory lists the name, or the filed text names the host.
  - `project_likely`: a distinct organisational name at a fiscal-sponsor EIN, with consistent filing text and no alias evidence.
  - `project_own_ein`: a same-name BMF entity was ruled before the grant year.
  - `host_alias`: a former name, dba, acronym expansion or full legal name.
  - `host_program`: the host's own publication or programme.
- **True positives** are the three project classes.

### 1.4 Estimates
- **Precision:** k / 60, with a Wilson interval. Dollar precision is the true-positive share of sampled dollars.
- **True NP lines and dollars:** post-stratified by host EIN.
  - Each sampled EIN's own sample precision is applied to its NP lines and dollars.
  - The 7 EINs with no sampled line (8 lines, $1.20m) take the pooled precision.
- **Recall of the FBO-name rule** on keyed hosts = FBO lines / (FBO lines + estimated true NP lines), and likewise for dollars.
  - FBO detections are taken at precision 1, and at 19/21, the g0503-03 sponsorship precision for intermediary hosts.
  - A variant adds the HX lines at the HX sample's project rate.
  - This measures recall *relative to the two naming forms*. Hosted-project lines filed under the host's own name are invisible to both rules (§4).
- **Dollar effect:**
  - NP lines on counted keyed EINs are already in the refined flag, so they add $0.
  - NP lines on grantmaker hosts would be the only candidates inside the keyed set. There are none.
  - Sensitivity: for non-keyed EINs with at least one valid FBO detection in the intermediary class, the script counts FBO plus NP projects (merged with `merge_projects`) and re-applies the ≥ 3 threshold.

## 2. Results [C]

### 2.1 Lines to keyed hosts

| Class | Lines | $ | EINs |
|---|---|---|---|
| host (name = host) | 2,440 | $1,783.09m | 231 |
| **fbo** | **97** | **$7.38m** | 26 |
| **np** | **122** | **$23.54m** | 28 |
| np_d2d (set aside) | 9 | $0.48m | 4 |
| hx (diagnostic) | 122 | $10.32m | 43 |
| **All** | **2,790** | **$1,824.81m** | 231 |

- **All 122 NP lines go to counted hosts.** None goes to a grantmaker host.
- **Filers of NP lines** (lines / $):

  | Filer | Lines | $ |
  |---|---|---|
  | Seattle Foundation | 34 | $1.09m |
  | The Denver Foundation | 30 | $1.88m |
  | Morgan Stanley GIFT | 18 | $0.66m |
  | ImpactAssets | 4 | $0.19m |
  | NPT | 3 | $3.67m |
  | Chicago Community Trust | 3 | $0.22m |
  | 21 other filers | 1–2 each | — |

  The largest single line is Fidelity Charitable's $9.76m to Myriad USA, filed under "King Baudouin Foundation United States Inc".
- **Top NP hosts** (lines, $, distinct NP projects):

  | Host | Lines | $ | Projects | Note |
  |---|---|---|---|---|
  | Myriad USA | 26 | $18.23m | 2 | both "projects" are spellings of its former name |
  | Trailhead Institute | 12 | $0.92m | 10 | |
  | RVC Seattle | 18 | $0.88m | 7 | |
  | Colorado Nonprofit Development Center | 11 | $0.67m | 7 | |
  | Center for Investigative Reporting | 7 | $0.54m | 1 | Mother Jones |
  | Tides Center | 7 | $0.25m | 5 | |
  | Shunpike | 5 | $0.06m | 4 | |
  | Windward Fund | 1 | $1.00m | — | filed "Winward Fund", a misspelling (alias, unsampled) |

- **NP lines whose name matches another BMF EIN:** 13 lines, $0.39m.

### 2.2 Distinct projects per keyed host
- **NP projects:** 28 EINs. By number of projects: 1 → 16; 2 → 6; 3 → 1; 4 → 1; 5 or more → 4.
- **Keyed hosts reaching ≥ 3 projects:**
  - 6 with FBO lines only;
  - 6 with NP lines only;
  - 15 with FBO + NP.
- All of these hosts are already counted, so the dollar figure does not move.

### 2.3 Precision (60 NP lines; 21 hosts; 15 filers) [I]

| Class | Lines |
|---|---|
| project_confirmed | 3 |
| project_likely | 34 |
| project_own_ein | 1 |
| host_alias | 20 |
| host_program | 2 |

| Measure | Value |
|---|---|
| Precision, lines | **38 / 60 = 63.3%** (Wilson 50.7–74.4%)<br>37 / 60 = 61.7% without the own-EIN case (49.0–72.9%)<br>3 / 60 confirmed |
| Precision, sampled dollars | **40.4%** ($1.81m of $4.47m) |
| Without Myriad USA | 38 / 45 = **84.4%** of lines (71.2–92.3%); 93.6% of dollars |
| HX sample (15) | 3 projects (Philanthropy Together at Global Impact; Sea Potential ×2 at Sustainable Seattle); 12 aliases.<br>20% of lines (Wilson 7.0–45.2%), 0.5% of dollars |

### 2.4 Recall of the FBO-name rule (keyed hosts)

| Basis | Lines | Dollars |
|---|---|---|
| FBO detections | 97 | $7.38m |
| Estimated true NP projects, post-stratified | 76.6 | $3.67m |
| **Recall, FBO at precision 1** | **55.9%** | **66.8%** |
| Recall, FBO at precision 19/21 | 53.4% | 64.5% |
| Recall, at the NP precision Wilson bounds (pooled) | 51.7–61.1% | — |
| Recall including HX at its sample project rate | 49.0% | 66.5% |
| *Pooled (unstratified) estimate, for reference* | *55.7%* | *43.7%* |

- The pooled dollar recall is distorted by Myriad: its large alias lines carry the pooled dollar precision.
- The post-stratified estimate keeps Myriad at its sample precision, which is 0.
- The unsampled "Winward Fund" line ($1.0m, a misspelt host name) takes the pooled dollar precision of 40.4%. If it is treated as an alias, true NP dollars fall to about $3.27m and dollar recall rises to about 69% [C, arithmetic on the reported figures].

### 2.5 Effect on the fiscal-sponsor figures

| Item | Lines | $ | Share of proxy $ |
|---|---|---|---|
| Refined fiscal-sponsor flag (reproduced) | — | $1,799.85m | 1.94% |
| NP lines at counted keyed hosts | 122 | $23.54m (true ≈ $3.7m) | already inside the flag |
| NP lines at grantmaker hosts | 0 | $0 | — |
| **Addition to the fiscal-sponsor figure from NP (keyed set)** | **0** | **$0** | **0** |
| Sensitivity: NP lines at 107 non-keyed intermediary EINs with at least one FBO detection | 10 | $0.83m | — |
| … hosts promoted to ≥ 3 projects | 0 | $0 | 0 |
| **Governing ≥ 3 addition (g0503-03 §2.4)** | 190 | **$35.1m–$114.6m** | **0.04%–0.12%, unchanged** |

- The union shares (core 7.79% / 11.73%, broad 24.82% / 19.97% with the de facto addition) are unchanged for the same reason.

## 3. Hand-check sample [I]

Evidence and criteria are in §1.3. Notes per line are in the CSV `hand_note` column. All 75 names are organisational, so they are shown.

**np60**

| # | Filer (FY) | Host EIN · BMF name | Filed name | $ | Class |
|---|---|---|---|---|---|
| 1 | Morgan Stanley Global Impact (2023) | 042261109 · Third Sector New England Inc | Future Chefs | 12,500 | **project (confirmed)** |
| 2 | The Denver Foundation (2023) | 113451703 · Fractured Atlas Inc | SOL VIDA | 7,500 | project (likely) |
| 3 | Seattle Foundation (2023) | 113451703 · Fractured Atlas Inc | HAPPENSTANCE THEATER | 8,000 | project (likely) |
| 4 | Seattle Foundation (2023) | 133191113 · Neo Philanthropy Inc | MORE EQUITABLE DEMOCRACY | 25,000 | project (likely) |
| 5 | The Minneapolis Foundation (2023) | 133357408 · Performance Zone Inc | THE FIELD | 10,000 | alias |
| 6 | The Minneapolis Foundation (2024) | 133357408 · Performance Zone Inc | THE FIELD | 10,000 | alias |
| 7 | Morgan Stanley Global Impact (2024) | 264245043 · Edward Charles Foundation | The Rod Dedeaux Foundation | 50,000 | project (likely) |
| 8 | Seattle Foundation (2023) | 311580932 · Sustainable Seattle | IT TAKES A VILLIAGE | 8,500 | project (likely) |
| 9 | Morgan Stanley Global Impact (2024) | 461323531 · Social Good Fund Inc | Homies Empowerment | 5,000 | project (likely) |
| 10 | Seattle Foundation (2023) | 474257834 · Rvc Seattle | ALL GIRL EVERYTHING ULTIMATE PROGRAM | 2,500 | project (likely) |
| 11 | Seattle Foundation (2023) | 474257834 · Rvc Seattle | ALL GIRL EVERYTHING ULTIMATE PROGRAM | 8,000 | project (likely) |
| 12 | Seattle Foundation (2023) | 474257834 · Rvc Seattle | ALPHABET ALLIANCE OF COLOR | 25,000 | project (likely) |
| 13 | Seattle Foundation (2023) | 474257834 · Rvc Seattle | ALPHABET ALLIANCE OF COLOR | 200,000 | project (likely) |
| 14 | Seattle Foundation (2023) | 474257834 · Rvc Seattle | RAINIER VALLEY CORPS | 30,000 | alias |
| 15 | Seattle Foundation (2023) | 474257834 · Rvc Seattle | RAINIER VALLEY CORPS | 50,000 | alias |
| 16 | Seattle Foundation (2023) | 474257834 · Rvc Seattle | SKYWAY COALITION | 25,000 | project (likely) |
| 17 | Seattle Foundation (2023) | 474257834 · Rvc Seattle | WA-BLOC | 5,000 | project (likely) |
| 18 | Seattle Foundation (2023) | 522094677 · Alliance For Global Justice | TAKING BLACK PRIDE | 40,000 | project (likely) |
| 19 | Boston Foundation Inc (2024) | 582277856 · Myriad Usa Inc | King Baudouin Foundation United States (KBFUS) | 17,500 | alias |
| 20 | Vanguard Charitable Endowmen (2023) | 582277856 · Myriad Usa Inc | KING BAUDOUIN FOUNDATION UNITED STATES INC | 303,300 | alias |
| 21 | Jewish Communal Fund (2023) | 582277856 · Myriad Usa Inc | KING BAUDOUIN FOUNDATION UNITED STATES INC | 349,000 | alias |
| 22 | T Rowe Price Program For Cha (2024) | 582277856 · Myriad Usa Inc | KING BAUDOUIN FOUNDATION UNITED STATES (KBFUS) | 702,011 | alias |
| 23 | The Chicago Community Trust (2023) | 582277856 · Myriad Usa Inc | King Baudouin Foundation United States (KBFUS) | 11,000 | alias |
| 24 | The Chicago Community Trust (2024) | 582277856 · Myriad Usa Inc | King Baudouin Foundation United States (KBFUS) | 202,000 | alias |
| 25 | Morgan Stanley Global Impact (2023) | 582277856 · Myriad Usa Inc | King Baudouin Foundation United States Inc | 429,500 | alias |
| 26 | Morgan Stanley Global Impact (2023) | 582277856 · Myriad Usa Inc | King Baudouin Foundation United States | 30,000 | alias |
| 27 | Morgan Stanley Global Impact (2024) | 582277856 · Myriad Usa Inc | King Baudouin Foundation United States Inc | 15,000 | alias |
| 28 | Community Foundation Of Tamp (2023) | 582277856 · Myriad Usa Inc | KING BAUDOUIN FOUNDATION UNITED STATES (KBFUS) | 15,000 | alias |
| 29 | Community Foundation Of Tamp (2024) | 582277856 · Myriad Usa Inc | KING BAUDOUIN FOUNDATION UNITED STATES (KBFUS) | 20,000 | alias |
| 30 | Raymond James Charitable End (2023) | 582277856 · Myriad Usa Inc | KING BAUDOUIN FOUNDATION UNITED STATES (KBFUS) | 16,105 | alias |
| 31 | Raymond James Charitable End (2024) | 582277856 · Myriad Usa Inc | KING BAUDOUIN FOUNDATION UNITED STATES (KBFUS) | 72,000 | alias |
| 32 | Marin Community Foundation (2023) | 582277856 · Myriad Usa Inc | KING BAUDOUIN FOUNDATION UNITED STATES (KBFUS) | 256,000 | alias |
| 33 | California Community Foundat (2023) | 582277856 · Myriad Usa Inc | KING BAUDOUIN FOUNDATION UNITED STATES INC | 100,000 | alias |
| 34 | The Denver Foundation (2023) | 841267213 · Trailhead Institute | COLORADO BLUEPRINT TO END HUNGER | 322,000 | project (likely) |
| 35 | The Denver Foundation (2023) | 841267213 · Trailhead Institute | LINKAGES | 40,000 | project (likely) |
| 36 | The Denver Foundation (2023) | 841267213 · Trailhead Institute | THE ANCESTRY RESEARCH TRAINING PROJECT - THE ART PROJECT | 7,500 | project (likely) |
| 37 | The Denver Foundation (2024) | 841267213 · Trailhead Institute | APPRENTICE OF PEACE YOUTH ORGANIZATION | 40,000 | project (likely) |
| 38 | The Denver Foundation (2024) | 841267213 · Trailhead Institute | COLORADO BLUEPRINT TO END HUNGER | 270,000 | project (likely) |
| 39 | The Denver Foundation (2024) | 841267213 · Trailhead Institute | ELEVATED DENVER | 10,000 | project (likely) |
| 40 | The Denver Foundation (2024) | 841267213 · Trailhead Institute | JEFFERSON COUNTY FOOD POLICY COUNCIL | 100,000 | project (likely) |
| 41 | The Denver Foundation (2023) | 841493585 · Colorado Nonprofit Development Center | AFRICAN LEADERSHIP GROUP | 391,112 | project (likely) |
| 42 | The Denver Foundation (2023) | 841493585 · Colorado Nonprofit Development Center | BRINGING MUSIC TO LIFE | 21,000 | project (likely) |
| 43 | The Denver Foundation (2024) | 841493585 · Colorado Nonprofit Development Center | BRINGING MUSIC TO LIFE | 13,500 | project (likely) |
| 44 | The Denver Foundation (2024) | 841493585 · Colorado Nonprofit Development Center | GLOBEVILLE ELYRIA SWANSEA COMMUNITY INVESTMENT FUND - GES CIF | 10,000 | project (likely) |
| 45 | The Denver Foundation (2024) | 841493585 · Colorado Nonprofit Development Center | IN LAK'ECH DENVER ARTS | 9,000 | project (likely) |
| 46 | Seattle Foundation (2023) | 911702331 · Northwest Film Forum | ARTE NOIR | 10,000 | project, own EIN exists |
| 47 | Seattle Foundation (2023) | 911702331 · Northwest Film Forum | UPSTART CROW COLLECTIVE | 5,000 | **project (confirmed)** |
| 48 | Seattle Foundation (2023) | 911998597 · Seattle Parks Foundation | DUWAMISH VALLEY SUSTAINABILITY ASSOCIATION | 7,500 | project (likely) |
| 49 | Seattle Foundation (2023) | 912138554 · Shunpike | THE QUEEN'S PROJECT | 8,500 | project (likely) |
| 50 | California Community Foundat (2024) | 912166435 · Multiplier | TRUST FOR CONSERVATION INNOVATION | 12,500 | alias |
| 51 | The Us Charitable Gift Trust (2024) | 942282759 · The Center For Investigative Reporting | Mother Jones | 5,200 | host programme |
| 52 | The Chicago Community Trust (2024) | 942282759 · The Center For Investigative Reporting | Mother Jones | 6,500 | host programme |
| 53 | Morgan Stanley Global Impact (2023) | 942889684 · Earth Island Institute Inc | The Borneo Project | 20,000 | project (likely) |
| 54 | Morgan Stanley Global Impact (2023) | 943213100 · Tides Center | Shalom Bayit | 10,000 | project (likely) |
| 55 | Morgan Stanley Global Impact (2023) | 943213100 · Tides Center | Arab Resource ganizing Center (AROC) - 1073 (TIDES CENTER) | 5,000 | **project (confirmed)** |
| 56 | The Denver Foundation (2023) | 943213100 · Tides Center | VOICES FOR PROGRESS EDUCATION FUND | 25,000 | project (likely) |
| 57 | The Denver Foundation (2024) | 943213100 · Tides Center | DETROIT ACTION EDUCATION FUND | 25,000 | project (likely) |
| 58 | The New York Community Trust (2023) | 954116679 · Social And Environmental Entrepreneurs Inc | SUBSTANCE USE FUNDERS COLLABORATIVE CO AUDACIA CONSULTING LLC | 20,000 | project (likely) |
| 59 | Morgan Stanley Global Impact (2023) | 954116679 · Social And Environmental Entrepreneurs Inc | The Bee Conservancy | 5,000 | project (likely) |
| 60 | Morgan Stanley Global Impact (2024) | 954302067 · Community Partners | Know the Glow | 10,000 | project (likely) |

**hx15**

| # | Filer (FY) | Host EIN · BMF name | Filed name | $ | Class |
|---|---|---|---|---|---|
| 1 | Community Foundation Of New  (2023) | 133357408 · Performance Zone Inc | THE PERFORMANCE ZONE INC AKA THE FIELD | 22,500 | alias |
| 2 | Donor Advised Charitable Giv (2024) | 204286082 · United Charitable | UNITED CHARITABLE PROGRAMS | 40,500 | alias |
| 3 | Morgan Stanley Global Impact (2023) | 208655418 · Omprakash Inc | OMPRAKASH O | 125,000 | alias |
| 4 | Vanguard Charitable Endowmen (2023) | 237357906 ·  | MARCUS A FOSTER EDUCATIONAL INSTITUTE | 150,000 | alias |
| 5 | Seattle Foundation (2023) | 311580932 · Sustainable Seattle | SEA POTENTIAL | 500 | project (likely) |
| 6 | Seattle Foundation (2023) | 311580932 · Sustainable Seattle | SEA POTENTIAL | 500 | project (likely) |
| 7 | The Minneapolis Foundation (2024) | 521273585 · Global Impact | GLOBAL IMPACT - PHILANTHROPY TOGETHER | 10,000 | project (likely) |
| 8 | National Philanthropic Trust (2023) | 582277856 · Myriad Usa Inc | MYRIAD USA AKA KING BAUDOUIN FOUNDATION UNITED STATES | 1,671,200 | alias |
| 9 | Fidelity Investments Charita (2024) | 680101012 · Center For Volunteer And Nonprofit Leadership Of Marin | CENTER FOR VOLUNTEER AND NONPROFIT LEADERSHIP OF M | 5,700 | alias |
| 10 | National Philanthropic Trust (2023) | 770273721 · Los Altos Community Foundation | LOS ALTOS MOUNTAIN VIEW COMMUNITY FOUNDATION | 5,500 | alias |
| 11 | Donor Advised Charitable Giv (2023) | 912138554 · Shunpike | SHUNPIKE ARTS COLLECTIVE | 14,700 | alias |
| 12 | Donor Advised Charitable Giv (2024) | 930386984 · Ywca Of Greater Portland | YOUNG WOMEN'S CHRISTIAN ASSOCIATION OF GREATER PORTLAND | 8,450 | alias |
| 13 | National Philanthropic Trust (2024) | 942282759 · The Center For Investigative Reporting | FOUNDATION FOR NATIONAL PROGRESS DBA MOTHER JONES | 155,400 | alias |
| 14 | The San Francisco Foundation (2023) | 942655955 · Somarts | SOMARTS CULTURAL CENTER | 85,000 | alias |
| 15 | Jewish Community Foundation  (2023) | 952557063 · Public Health Foundation Inc | Heluna Health | 63,000 | alias |

## 4. Limits

- **Recall is relative to the two naming forms.** Hosted-project grants filed under the host's own name are invisible to every name rule. So are project names that happen to share a token with the host (e.g. "SEA POTENTIAL" against "SUSTAINABLE SEATTLE", caught only as HX). True recall of the FBO rule against *all* hosted-project grants is lower than 56%, by an amount that cannot be measured from filings.
- **Directory evidence is thin.** Most host directories show current projects only, render client-side, or were blocked (§8). Only 3 of 60 lines are directory- or text-confirmed:
  - Future Chefs (TSNE directory);
  - Upstart Crow Collective (Northwest Film Forum page);
  - AROC (the filed name says "(TIDES CENTER)").
  <br>The CNDC and Trailhead pages list 2026 partners, which do not include the 2023–24 projects. The 34 `project_likely` calls rest on name, purpose text and the host being a fiscal sponsor. "Confirmed only" precision is 5%. The 63% figure is an upper-leaning judgement [I].
- **Concentration.** 31 of the 60 sampled lines come from two filers (Seattle Foundation and The Denver Foundation), and the 60 lines sit on 21 hosts. 15 sampled lines are one alias (KBFUS) at one host.
- **Aliases are the main error.** They are former names (KBFUS → Myriad USA; Trust for Conservation Innovation → Multiplier), dbas (The Field; Mother Jones), acronym expansions (RVC → Rainier Valley Corps), current names (Heluna Health) and misspellings (Winward). An archived-name reference list would remove most of them (P-G05030301-02).
- **Parenthetical host names are stripped** by `name_key` before matching, so "… (TIDES CENTER)" and "… (COMMUNITY INITIATIVES)" land in NP rather than FBO (P-G05030301-04).
- **Same-name BMF entities.** Arte Noir's own exemption (ruling 2022-12) predates the grant, so this may be a graduated project or a filer EIN error. Skyway Coalition (2025-04) and Rod Dedeaux Foundation (2024-10) were ruled at or after the grant year. SOL VIDA's same-name BMF entity is in CA, while the filed line is in Denver, CO, so it is unrelated.
- **DAF-to-DAF.** Nine NP-type lines (FJC under its full name; New Horizons Foundation; Tides Foundation; SouthCoast Community Foundation) are whitelist-marked and set aside, consistent with the parent's treatment.
- **Sensitivity scope.** The non-keyed sensitivity covers only EINs that already have an FBO detection. Hosts with neither a listing nor an FBO line are not examined (P-G05030301-01).
- All limits of the parent notes apply: recipient-level Schedule I, attachment-only sponsors, truncated names, and directory self-listing.

## 5. Reproduction

```
python3 scripts/mission_sponsored_project_recall.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
    --pub78 data-download-pub78.txt --fsd-html all-fiscal-sponsors-alpha-ordered.html \
    --hand data/mission-2026-11-14/sponsored-project-recall-handcheck-2026-11-20.csv [--out CSV] [--sample-out CSV]
```

- The inputs are those of `mission_de_facto_fiscal_sponsors.py`. The archive, revocation and e-file inputs are not needed, because no union re-cut is required.
- Run time is about 3 minutes.
- The JSON summary on stdout holds every figure quoted here:
  - `keyed_*`, `np_*`;
  - `sample`, `hx_sample`;
  - `np_true_est_post_stratified`, `fbo_recall_post_stratified`, `fbo_recall` (pooled);
  - `keyed_hosts_ge3`, `sensitivity_nonkeyed`, `refined_fs_usd_check`.
- Without `--hand`, the script still writes the sample and the counts, and leaves the estimates empty.

## 6. Source register

| ID | Source | Version / access | robots.txt |
|---|---|---|---|
| S1 | IRS Form 990 Schedule I Part II lines, top-50 sponsors FY2023–24 (e-file XML via the GivingTuesday mirror of IRS TEOS; [IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)) | Line cache of P-NEW-REC-01, unchanged. Purpose text from cached XML. 8 returns fetched 2026-11-20 from `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml` | robots.txt 404 (no rules), logged 2026-11-20T04:48:45Z |
| S2 | [IRS EO BMF extract](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf): NAME, STATE, NTEE_CD, RULING | Last-Modified 2026-11-09 (cached) | per parent |
| S3 | [IRS Pub 78 data](https://apps.irs.gov/pub/epostcard/data-download-pub78.zip) | cached 2026-11-11 | per parent |
| S4 | [Fiscal Sponsor Directory, all sponsors (alpha)](https://fiscalsponsordirectory.org/all-fiscal-sponsors-alpha-ordered/) | 2026-11-19 cache (not re-fetched) | `Disallow:` empty (parent log) |
| S5 | [TSNE: Our fiscally sponsored projects](https://tsne.org/our-fiscally-sponsored-projects-and-organizations/) | fetched 2026-11-20; lists Future Chefs | `User-agent: * / Disallow:` (empty) |
| S6 | [Northwest Film Forum: fiscal sponsorship](https://nwfilmforum.org/education/artist-services/nonprofit-fiscal-sponsorship-filmmakers/) | fetched 2026-11-20; lists Upstart Crow Collective | `*` disallows /wp/wp-admin/ only |
| S7 | [FJC about page](https://fjc.org/about/) | fetched 2026-11-20; "FJC - A Foundation of Philanthropic Funds" (alias for the np_d2d lines) | `*` disallows /wp-admin/ only |
| S8 | [kbfus.org](https://www.kbfus.org/) | fetched 2026-11-20; redirects to myriadusa.org (page then 403); alias evidence | www.kbfus.org and www.myriadusa.org: `User-agent: *`, no Disallow |
| S9 | [CNDC partner projects](https://cndc.org/projects/), [Trailhead projects](https://trailhead.institute/projects-at-trailhead-institute/), [Multiplier projects](https://multiplier.org/projects/), [Sustainable Seattle fiscal sponsorship](https://sustainableseattle.org/programs/fiscal-sponsorship/), [Community Partners fiscal sponsorship](https://communitypartners.org/fiscal-sponsorship/), [NEO fiscal sponsorship](https://neophilanthropy.org/services/fiscal-sponsorship/), [Fractured Atlas](https://www.fracturedatlas.org/) | fetched 2026-11-20. **No sampled name found**: pages list current (2026) projects or render client-side | all allow (empty Disallow, or admin paths only) |
| S10 | `sponsor-cost-structure.csv`, `daf-foreign-grants-schedule-f-2023-2024.csv` | repo files (denominator only) | — |

## 7. Data dictionary: `sponsored-project-recall-2026-11-20.csv` (137 rows)

There is one row per NP line on a keyed host EIN (122). The 15 HX diagnostic-sample rows follow, with `rule_class` = `hx`. Rows are sorted by recipient EIN, sponsor, year and line index.

| Column | Meaning |
|---|---|
| sponsor_ein, sponsor_name | Filing DAF sponsor (DAFRC panel name) |
| fiscal_year, line_index | Sponsor fiscal year; 0-based index of the line in that return's screened Schedule I lines |
| recipient_ein | Recipient EIN as filed: a keyed host EIN |
| host_bmf_name, host_modal_filed_name | The reference names: the 2026-11 EO BMF name, and the most frequent connector-free filed name for that EIN |
| host_in_q19, host_in_directory | EIN is a Q-B15 host / keyed from the Fiscal Sponsor Directory |
| host_counted_in_refined_flag | EIN counted by the refined fiscal-sponsor flag, i.e. not a community-foundation / United Way host |
| filed_name | Recipient name as filed. Written only when it contains an organisation word or was hand-checked as organisational; otherwise "[withheld: no organisation word]", so that no individual's name is recorded |
| rule_class | `np` (own-name project rule) or `hx` (host plus extra; diagnostic sample only) |
| connector_status | FBO-rule status if the name has a connector (`unverified` etc.); blank if none |
| amount_usd | Schedule I cash + non-cash, filed $ |
| d2d | DAF-to-DAF whitelist flag (always False for `np`) |
| in_sample | `np60` (precision sample), `hx15` (HX diagnostic), or blank |
| own_name_bmf_eins | Other EINs whose current BMF name has the same name key, as `EIN:STATE` |
| hand_class | project_confirmed / project_likely / project_own_ein / host_alias / host_program (sampled rows only) |
| hand_note | Evidence for the hand class |

**Hand-check file** (`sponsored-project-recall-handcheck-2026-11-20.csv`): sample, sponsor_ein, fiscal_year, line_index (the join keys), hand_class, hand_org (yes = organisational name; may be shown), hand_note.

## 8. Robots and fetch log (2026-11-20, UA `research-script/1.0`)

| Host | robots.txt | Action |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | 8 XML returns fetched |
| tsne.org | `*` Disallow empty; Crawl-delay 10 | 2 pages |
| nwfilmforum.org | admin only | 2 pages |
| cndc.org, trailhead.institute, multiplier.org, sustainableseattle.org, communitypartners.org, neophilanthropy.org, fjc.org, www.fracturedatlas.org, www.newhorizonsfoundation.org, www.seechange.org | allow | homepages and directory pages; seechange.org/projects returned a 114-byte shell |
| www.seattleparksfoundation.org | admin and feed paths; no Claude or anthropic group | the guessed URL returned 404 |
| www.earthisland.org | **ClaudeBot / anthropic-ai disallowed for /journal** | /journal was not fetched. Project URL guesses returned 404; the homepage connection was reset |
| www.kbfus.org, www.myriadusa.org | allow | redirect recorded; page 403 (bot protection), not retried |
| thefield.org | **`User-agent: *` Disallow: /** | **blocked**: not fetched |
| shunpike.org, socialgoodfund.org, afgj.org, www.rvcseattle.org | robots.txt returned 403 | **treated as blocked**: not fetched |
| rvcseattle.org | allow | homepage 403; not retried |
| www.edwardcharlesfoundation.org, www.allianceforglobaljustice.org | no response | not fetched |
| www.tides.org | allow (no public project directory) | not needed |

- No host's terms forbidding extraction were met on the pages fetched.
- No logins or forms were used.
- No individuals' names are recorded. Host pages and BMF records contain contact names; none were copied.
