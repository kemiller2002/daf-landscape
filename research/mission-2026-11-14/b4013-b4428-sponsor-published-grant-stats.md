# Sponsor-published grant statistics: restricted share (P-B4013-01) and disclosure outcomes (P-B4428-03)

- **Tasks:** P-B4013-01 (queued in [b40n13-01-grant-purpose-panel.md](b40n13-01-grant-purpose-panel.md), read with its wave-35A corrections in [validation-wave35a-report.md](validation-wave35a-report.md)) and P-B4428-03 (queued in [b44n28-01-donor-info-defaults.md](b44n28-01-donor-info-defaults.md) §3.3, read with its wave-34A and wave-35B corrections, and [b4428-02-ren-private-label-defaults.md](b4428-02-ren-private-label-defaults.md)).
- **Date:** 2026-11-19. Every page and PDF cited as [F] was fetched on that date.
- **Data:** [`data/mission-2026-11-14/sponsor-published-grant-stats-2026-11-19.csv`](../../data/mission-2026-11-14/sponsor-published-grant-stats-2026-11-19.csv). It has 66 rows: 55 figures (one per sponsor, period and category) and 11 rows for top-15 nationals with nothing published.
- **Script:** [`scripts/mission_b4013_b4428_sponsor_stats_build.py`](../../scripts/mission_b4013_b4428_sponsor_stats_build.py). Run it as `python3 -I scripts/mission_b4013_b4428_sponsor_stats_build.py . <out.csv>`. It rebuilds the CSV byte for byte (md5 `190c2c59…`, checked twice), joins FY2024 ranks and assets, and prints the computed values used below.
- **Queue:** [`data/mission-2026-11-14/queue-proposals-b4013-b4428.csv`](../../data/mission-2026-11-14/queue-proposals-b4013-b4428.csv) (5 rows).
- **Labels:** [F] first-party text read this pass. [C] computed by the script. [S] secondary source relaying a sponsor figure. [R] repo-carried or search-snippet only, not re-read. [B] blocked by robots or unreachable. [I] inference.

## 0. Answer

| Question | Finding | Confidence |
|---|---|---|
| **(A) Who publishes a restricted / unrestricted split?** | **4 of the top-15 nationals, holding 76.7% of top-15 national FY2024 DAF assets ($223.07bn) [C]:** Fidelity Charitable, NPT, DAFgiving360 and Vanguard Charitable. The other 11 publish nothing found; GS DAPF and Raymond James are robots-blocked. | High on what was found; absence is "not found" |
| **(A) The figures** | - **Fidelity:** 63–64% of grant recommendations "where needed most" every year 2020–2025 (60% in 2019), so **36% carry a donor designation** in 2025, which includes honor dedications as well as uses [F/C] [V wave 39A]<br>- **DAFgiving360:** 72% of grants with no purpose specified (FY2022), 71% (CY2023), 72% (FY2024) [F, via the Schwab pressroom]; FY2025 "70%+" [R] or 72% and CY2025 74% [S].<br>- **NPT:** unrestricted 63% (FY20), **47%** of 130,875 grants (FY24), **66%** (105,909 of 159,543, FY25) by count [F]; FY23 "more than half" [F].<br>- **Vanguard (dollars):** 42% of grant dollars (2020), "more than half" (2021–2023), **48.3%** (FY2024), **51.7%** (FY2025), "half … $2 billion" of $3.9bn in 2025 (51.3% computed from the rounded numbers; the release headline says grants were “exceeding $3.9 Billion”, so this is an upper bound) [V wave 39A] [F/C]. | High on the text. Bases differ (count vs dollars) |
| **(A) Definitions differ, and two are not "restrictions" at all** | - Fidelity: special purposes "are conveyed to grant recipients as recommendations, not restrictions" (footnote, 2021–2025 reports).<br>- DAFgiving360: "did not specify a purpose".<br>- NPT: unrestricted is what NPT awards when the advisor recommends no specific purpose (Schedule I narrative, b40n13-01).<br>- Vanguard: unrestricted is "a grant given to a nonprofit that can be used for any purpose as directed by the nonprofit".<br>So the complement is "a purpose was entered", not "a legally binding restriction" | High |
| **(B) Who publishes disclosure outcomes?** | **Only Fidelity publishes a full split (full contact / fund name only / anonymous). Vanguard publishes an anonymous share only. Together they hold 39.5% of top-15 national assets [C].** NPT's FY20 (96% non-anonymous) and FY21 (97% of donors identified) figures exist only as search snippets of pages that now return 404 [R]. AEF and GKCCF give qualitative statements only. | High |
| **(B) Fidelity, default = full contact** | 83/13/4 (2020), 82/14/4 (2021), 81/15/4 (2022 and 2023), 80/15/5 (2024 and 2025) [F]. Full contact fell 3 points in five years [C]. | High |
| **(B) Vanguard, default = fund name only** | "Only 4% of grants are completely anonymous" and, on the same page, "Only 5% …" [F]. No full-contact share is published. | High on the text; internally inconsistent |
| **(B) How often do donors leave the default unchanged? [I]** | - **Fidelity: at most 80% of 2025 grants kept the full-contact default; at least 20% departed from it** (15% fund name only + 5% anonymous) [C/I].<br>- **Vanguard: at most 95–96% kept the fund-name default; at least 4–5% departed to anonymity.** Departures toward adding contact details are not published, so the true keep rate is lower by an unknown amount [I].<br>- **Anonymity is about 4–5% under a full-contact default (Fidelity), a fund-name default (Vanguard) and a no-stated-default regime (NPT, snippet only).** That pattern is consistent with a stable preference, but it does not test default sensitivity: anonymity is the same opt-out under both observed defaults, no sponsor defaults to anonymous, and the NPT figure is an unverified snippet [I] [V wave 39A] | Medium. Bounds are arithmetic; the attribution is inference |

**Bottom line.** Schedule I cannot measure restrictions (b40n13-01), and sponsor publications only partly fill the gap. Four sponsors with 77% of top-15 national assets publish an unrestricted share. On a grant-count basis it mostly sits at **63–74%** (Fidelity 64%, NPT 66% in FY25, DAFgiving360 71–74%, Vanguard 70% in CY2022; NPT’s FY24 47% is the exception), and **about half on a dollar basis** at the one sponsor that reports dollars (Vanguard 48–52%) [F] [V wave 39A] That gap fits restricted grants being larger on average [I]. Vanguard publishes both bases for one year: its 2023-04-26 release says unrestricted gifts were “more than 50% of total dollars granted and 70% of individual grants” in 2022, so within Vanguard restricted grants are larger on average unless the 2022 unrestricted dollar share was 70% or more, which its 42%, 48.3% and 51.7% dollar figures make unlikely [V wave 39A] On disclosure, only Fidelity publishes a full split. Its 80% full-contact share is an upper bound on default retention, not a measure of it.

## 1. Method

1. **Universe.** The FY2024 top-15 nationals by `daf_assets_eoy` in [`daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv) (`fiscal_year=2024`, `row_type=top50`, `type=National`). The script ranks them. Defaults for (B) are joined from [`donor-info-defaults-top20-2026-11-19.csv`](../../data/mission-2026-11-14/donor-info-defaults-top20-2026-11-19.csv) by EIN.
2. **Sources.** Only the sponsors' own annual or giving reports, press releases and web pages, all 2021 or later. Pre-2021 *periods* appear only where a 2021+ document reports them (Fidelity 2019 in the 2021 report; NPT FY15 and FY20 in the 2025 report; Vanguard 2020 in a 2022 release). They are flagged and are not used in any conclusion. The 2020 Vanguard release ("Three-quarters of the grants … were unrestricted", 2020-02-18) and NPT's 2019 annual report (3% anonymous) are pre-2021 sources and are excluded.
3. **Discovery.** Web-search results were used only to find URLs. Search-snippet figures that could not be read at source are kept in the CSV as [R] with "UNVERIFIED" in `notes`, and are not used in any computed figure.
4. **Robots.** A stdlib fetcher (scratchpad `q1328/scripts/get.py`, UA `research-script/1.0`) fetched a URL only if robots.txt allowed both `*` and that UA. A 404 robots.txt counts as no rules; any other failure counts as blocked. Every request is logged (§8).
5. **Extraction and checks.** PDFs were read with `pdftotext` (layout and raw modes) and dated with `pdfinfo`. HTML dates come from the release dateline or `article:modified_time`. A checker (scratchpad `q1328/scripts/verify.py`) confirmed that **all 50 [F]/[S] quotes in the CSV occur verbatim** in the fetched files, after whitespace and curly-quote normalisation.
6. **Coding.** One row per figure. `basis` records what the sponsor counts (grant recommendations, grants or dollars). Where the unit is not stated it reads "count implied" or "unit not stated". `value_qualifier` keeps "more than", "at least" and "about" claims apart from exact values.

## 2. Results (A): restricted vs unrestricted

### 2.1 Fidelity Charitable (rank 1, $66.20bn): "where needed most" share of grant recommendations

| Year (calendar) | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| Designated "where needed most" | 60% | 63% | 64% | 63% | 63% | 64% | 64% |
| Report | 2021 | 2021 (and 2026) | 2022 | 2023 | 2024 | 2025 (and 2026) | 2026 |

- **Definition.** "While donors have the option to designate a specific fund, campaign, or other use …, the majority opt to make unrestricted grants." Footnote: "special purposes are conveyed to grant recipients as recommendations, not restrictions." The Giving Account guide says an account holder "may recommend that a grant be used … for a 'special purpose,' such as a building fund, research project, or in honor of a person". So a special purpose is opt-in, and "where needed most" is the outcome when nothing is entered [I: preselection is not shown].
- **Denominator.** "Grant recommendations". Count vs dollars is not stated; the table sits beside count-based items (grants by type), so count is implied. No dollar share is published.
- **Internal inconsistency.** The 2024 report prints 63% and, two lines later, "over two-thirds opted to make unrestricted grants".
- **Processing link.** The FAQ still says selecting "Where It Is Needed Most" "can also help expedite the processing of the grant recommendation" (re-read 2026-11-19).

### 2.2 NPT (rank 2, $42.12bn): unrestricted share of grant volume (fiscal year July–June)

| FY | FY15 | FY20 | FY21 | FY23 | FY24 | FY25 |
|---|---|---|---|---|---|---|
| Unrestricted | 13% | 63% | 70% [R] | >50% | **47%** | **66%** |
| Grants (denominator) | | | 88,289 [R] | | 130,875 | 159,543 |

- FY15, FY20 and FY25 come from the 2025 report's chart "UNRESTRICTED GRANTS | SHARE OF VOLUME" (`data-data="13,63,66"`) and its text: "In FY25, 105,909 grants, or 66% of the total, were unrestricted". 105,909 / 159,543 = **66.4%** [C].
- FY24: "47% of grants were unrestricted" and "Nearly half of all grants were unrestricted" (2024 report). That implies about 61,511 grants on the 2024 report’s count, or about 60,900 on the 2025 report’s restated FY24 count of 129,575 [C] [V wave 39A]
- FY23: "more than half of all grant recommendations were unrestricted"; the same page says "the majority of grants were unrestricted or designated toward general operating support". So FY23 may fold general-operating designations into the majority claim.
- **Unexplained break.** FY24 is 19 points below FY25 [C] and 16 below FY20, and the snippet FY21 is 70%. The 2025 report also restates every earlier grant count without a note (FY21 87,490, FY22 102,745, FY23 106,235, FY24 129,575, against 88,289, 103,816, 107,385 and 130,875 in the 2024 report), and its “+23%” fits the restated base, so NPT’s counting method changed between reports [V wave 39A] NPT gives no method note. A definition change (for example, whether "general operating support" designations count as unrestricted) is plausible but untested [I] (P-B4013B4428-01).
- **Definition.** NPT's FY2024 Schedule I narrative (b40n13-01, as corrected in wave 35A): "IF THE DONOR ADVISOR DOES NOT RECOMMEND A SPECIFIC CHARITABLE PURPOSE, NPT AWARDS THE GRANT AS "UNRESTRICTED" EXCEPT FOR EXPENDITURE RESPONSIBILITY GRANTS WHERE A SPECIFIC CHARITABLE PURPOSE IS REQUIRED." So unrestricted is the no-action outcome, and the complement includes ER grants as well as donor-recommended purposes.

### 2.3 DAFgiving360 (rank 3, $40.94bn): grants that "did not specify a purpose"

| Period | Value | Wording and basis | Source | Label |
|---|---|---|---|---|
| FY2022 | 72% | "These unrestricted grants have reached 72% of the total" (grants "not designated for a specific purpose") | Release 2022-07-19, Schwab pressroom | F |
| CY2023 | 71% | "71% of donors' grant recommendations did not specify a purpose" | Release 2024-01-23, Schwab pressroom | F |
| FY2024 | 72% | "Seventy-two percent of grants in the fiscal year did not specify a purpose" | Release 2024-07-23, Schwab pressroom | F |
| FY2025 | 70%+ | Repo-carried from the FY2025 release (dafgiving360.org, robots 403) | ai-economics-replacement-analysis.md P05 | R |
| FY2025 | 72% | "unrestricted grants, which now account for 72% of the overall giving" (basis ambiguous) | Chariot, 2025-08-04 | S |
| CY2025 | 74% | "74% of grants were unrestricted" (about 1.5m grants) | Chariot, 2026-02-12 | S |

- The Schwab pressroom (`pressroom.aboutschwab.com`, robots allow with crawl-delay 10, respected) republishes DAFgiving360's own releases. dafgiving360.org was not fetched (robots.txt 403). BusinessWire did not connect.
- The repo's FY2025 "70%+" is consistent with Chariot's 72% for the same year. It stays [R] because the release could not be re-read.

### 2.4 Vanguard Charitable (rank 4, $21.95bn): unrestricted share, mostly of dollars

| Period | Value | Basis | Release |
|---|---|---|---|
| CY2020 | 42% | grant dollars | 2022-01-25 |
| CY2021 | >50% ("of all giving") | dollars (implied by comparison) | 2022-01-25 |
| Dec 2022 | >50% ("of the grants recommended") | grants recommended | 2022-12-08 |
| CY2022 | >50% ("of dollars granted") | dollars | 2023-01-25 |
| Apr 2023 | >50% ("of the dollars granted annually"); +150% in five years | dollars | 2023-04-26 |
| FY2023 | >50% ("of all grants recommended") | grants recommended | 2023-08-10 |
| CY2023 | >50% ("of the total dollars granted") | dollars | 2024-01-30 |
| FY2024 | **48.3%** | grant dollars | 2025-08-25 |
| FY2025 | **51.7%** | grant dollars | 2025-08-25 |
| CY2025 | "half of all grants … accounting for $2 billion"; $2.0bn / $3.9bn = **51.3%** [C] | label "grants", figure in dollars | 2026-03-02 |

- **Definition** (2023-04-26 release): "unrestricted granting—defined as a grant given to a nonprofit that can be used for any purpose as directed by the nonprofit".
- Vanguard switches between count and dollar wording. The 2023-04-26 release also gives a 2022 count share, “70% of individual grants issued as unrestricted”, beside “more than 50% of total dollars granted” [V wave 39A] The two exact figures (48.3%, 51.7%) are dollars. The FY2024 releases (2024-08-27, 2025-02-04) give no share.

### 2.5 The other eleven top-15 nationals

| Rank | Sponsor | FY2024 $bn | Status |
|---|---|---|---|
| 5 | GS DAPF | 12.64 | **Blocked** (gspf.goldman.com `Disallow: /`) |
| 6 | MS GIFT | 9.11 | None found: morganstanley.com/gift and the "MS GIFT grantmaking" PDF (modified 2024-10-01) read; annual-report URLs for 2021–2025 return 404 |
| 7 | AEF | 8.38 | None found for (A); a qualitative anonymity line only (§3) |
| 8 | RCF | 5.91 | None found |
| 9 | BofA CGF | 4.73 | None found |
| 10 | ImpactAssets | 2.90 | None found (impact reports give grant counts, e.g. 13,500 in 2024, but no purpose split) |
| 11 | Greater Horizons | 2.53 | None found |
| 12 | Raymond James Charitable | 1.89 | **Blocked** (robots 403) |
| 13 | Dechomai | 1.43 | None found |
| 14 | US Charitable Gift Trust | 1.19 | None found |
| 15 | Ayco Charitable Foundation | 1.16 | None found |

"None found" rests on web searches plus the pages listed. It means "not found", not "not published".

### 2.6 What (A) adds to b40n13-01 [I]

- **The repo claim C1 (DAFgiving360 "70%+ unrestricted") is now corroborated for adjacent periods by first-party text**: 72% (FY2022), 71% (CY2023) and 72% (FY2024). FY2025 itself is still unread at source.
- **At three of the four publishers, "unrestricted" is the outcome when the donor enters no purpose.** This is explicit at NPT and DAFgiving360, and implied by Fidelity's opt-in "special purpose". So the published restricted share is an *active-designation rate*: 36% (Fidelity 2025), 28–29% (DAFgiving360 FY2022–FY2024) and 34% (NPT FY25; 53% in FY24) of grants by count [C]. It is not a measure of legally binding restrictions, and Fidelity says outright that its designations are not restrictions. At Fidelity it is not even a pure use rate: a special purpose can be “in honor of a person”, and the FAQ speaks of “Selecting” Where It Is Needed Most as the grant use, so a no-entry default is not shown. Only DAFgiving360 and NPT state the no-purpose rule, and NPT’s FY23 report folds “general operating support” designations into its majority claim [V wave 39A]
- **Count vs dollars.** Count-basis shares for 2023–2025 run 63–74%, except NPT's FY24 47%. Vanguard's only dollar-basis exact figures run 48–52%. If Vanguard's donors behave like the others, restricted grants are larger than unrestricted ones on average [I]. Vanguard’s 2023-04-26 release gives both bases for 2022 (“more than 50% of total dollars granted” and “70% of individual grants”), so the pattern is observed at one sponsor for one year; the CSV has no row for the 70% count figure [V wave 39A]

## 3. Results (B): observed disclosure outcomes against defaults

### 3.1 Published splits

| Sponsor | Default (b44n28-01, wave 34A/35B) | Period | Full contact | Fund name only | Anonymous | Basis |
|---|---|---|---|---|---|---|
| Fidelity | full contact (preselected per grant; account default changeable by phone) | 2020 | 83% | 13% | 4% | grants |
| | | 2021 | 82% | 14% | 4% | grants |
| | | 2022 | 81% | 15% | 4% | grants |
| | | 2023 | 81% | 15% | 4% | grants |
| | | 2024 | 80% | 15% | 5% | grants |
| | | 2025 | 80% | 15% | 5% | grants |
| | | FAQ (live) | | | 4% | grants |
| Vanguard | fund name only | live page | n/p | n/p | 4% **and** 5% | grants |
| NPT | donor chooses; no default stated | FY20 | 96% non-anonymous [R] | | (≈4%) | not stated |
| | | FY21 | 97% of *donors* included identifying information [R] | | | donors |
| AEF | donor chooses; no default stated | 2025 | "most DAF donors opt against remaining anonymous" (qualitative) | | | donors |
| GKCCF (CF) | fund name only | live | "It's rare for donors to choose to grant anonymously" [R, repo] | | | |

n/p = not published. Fidelity's rows sum to 100 in every year [C]. The 2023-data report also says "96% of grants included the account name or the recommending donors' names and addresses".

### 3.2 Comparison with the defaults

- **Fidelity (full-contact default).** The outcome is close to the default, but one grant in five departs from it, and the departure share has grown from 17% (2020) to 20% (2024–2025) [C].
- **Vanguard (fund-name default).** Only the anonymous tail is published, and the page gives two values (4%, 5%). The share of grants where donors *add* name or address, the departure that matters for a withholding default, is not published.
- **NPT, AEF, CJP (no stated default).** NPT's only numbers are unverified snippets. They put anonymity near 3–4%, as at the other two.
- **No sponsor with a withholding default publishes the full-contact share** (as b44n28-01 §3.3 found). This pass confirms it for Vanguard and found nothing for MS GIFT or BofA (the other fund-name defaults in the top 15).

### 3.3 Anonymity looks default-insensitive [I]

| Regime | Sponsor | Anonymous share |
|---|---|---|
| Full-contact default | Fidelity | 4–5% (2020–2025) |
| Fund-name default | Vanguard | 4% / 5% |
| No stated default | NPT | ≈4% (FY20, snippet) |

Three different defaults give the same anonymous share, but none of them is an anonymous default: under full contact and fund name only, anonymity is the same opt-out, and the NPT leg is a snippet that §1.3 excludes from conclusions. The comparison therefore cannot show that defaults do not move anonymity [V wave 39A] That is what one would expect if full anonymity is a deliberate choice by a stable 4–5% minority, and not something a default produces. All figures are counts. Dollar shares may differ: a second-hand "National Study on DAFs" claim puts anonymous DAF grants at about 9% of dollars against under 4% of grants (unverified; P-B4013B4428-03).

### 3.4 How often do donors leave the default unchanged? [I]

- **Fidelity, 2025:** the default is full contact, and 80% of grants carry full contact. So **at most 80% of grants left the default unchanged**. Some full-contact grants may come from donors who would have chosen it anyway, and some from donors who changed it and changed it back. **At least 20% departed.** Part of the 15% fund-name share may reflect an account-level default changed by phone, not a per-grant edit; that is still a donor action (P-B4013B4428-05).
- **Vanguard:** the default is fund name only. **At most 95–96% kept it; at least 4–5% departed (to anonymity).** Grants where the advisor "may add personal information" are also departures but are unpublished, so the true keep rate is lower by an unknown amount.
- **Reading across the two.** Under Fidelity's full-contact default, 15% of grants actively *withhold* contact (fund name only). If willingness to change the setting were symmetric, a similar minority would actively *add* contact under a fund-name default. Then roughly 80% of Vanguard grants would reach charities with fund name only, against 15% at Fidelity. That is a **plausible scale for the default effect, not a measurement**: it rests on Fidelity's donors standing in for Vanguard's.
- **Implication for G12-2 ("mixed, leaning habit").** The data are consistent with the habit reading. At the one sponsor with a full split, about four-fifths of grants carry whatever the default supplies, and the only margin that looks preference-driven (anonymity) is flat across regimes. The decisive test, a full split from a withholding-default sponsor, is not public (P-B4013B4428-04).

## 4. Corrections and notes for other repo documents (proposed, not applied)

- `b40n13-01-grant-purpose-panel.md` §6 C1: add that DAFgiving360's FY2022 (72%), CY2023 (71%) and FY2024 (72%) "no purpose specified" shares are first-party and verbatim (Schwab pressroom), and that FY2025 remains [R].
- `b44n28-01-donor-info-defaults.md` §3.3: add Fidelity's 2021–2023 splits (82/14/4, 81/15/4, 81/15/4), and the observation that Vanguard's two anonymity figures sit on one live page.
- Any repo sentence that reads Fidelity's 64% as "unrestricted grants" should carry Fidelity's own caveat: special purposes are "recommendations, not restrictions".

## 5. Limits

- **Bases differ.** Fidelity, NPT and DAFgiving360 report counts (Fidelity's unit is implied, not stated). Vanguard's exact figures are dollars. Shares cannot be pooled or asset-weighted across sponsors.
- **Periods differ.** Fidelity and Vanguard's main series are calendar years; NPT and DAFgiving360 mostly fiscal years (July–June). Vanguard and DAFgiving360 also publish calendar-year figures.
- **Definitions differ** (§0): "where needed most", "did not specify a purpose", "unrestricted", "any purpose as directed by the nonprofit". None is a legal restriction measure.
- **NPT series break** (FY24 47% vs FY25 66%) is unexplained.
- **Blocked or unreachable:** dafgiving360.org (robots 403), gspf.goldman.com, raymondjamescharitable.org, BusinessWire and web.archive.org (connection failures). DAFgiving360 FY2025 and later figures rest on repo-carried text or Chariot.
- **Snippets.** NPT FY21 (70% unrestricted; 97% of donors identified) and FY20 (96% non-anonymous) are search-snippet text from pages that now return 404. They are kept as [R] and not used.
- **Process lapse.** One query to the archive.org availability API (`archive.org/wayback/available`, listing captures only, no content) was sent by `curl` without a prior robots check; nothing from it is used beyond noting that captures exist (P-B4013B4428-01).
- **Transient robots failure.** Fidelity's robots.txt returned 403 once (5 PDF requests refused) and 200 before and after; the PDFs were fetched on retry after a 200.
- **Default-stickiness numbers are bounds and an analogy**, not estimates from a controlled comparison.
- **Fidelity's 2023 Giving Report PDF** carries a 2024-04-15 creation date, later than the 2024 report's 2024-03-06; its methodology says it covers calendar 2022.

## 6. Data dictionary (`sponsor-published-grant-stats-2026-11-19.csv`)

| Field | Meaning |
|---|---|
| `row_id` | `A-…` restricted-share figure; `B-…` disclosure figure; `X-nn` top-15 national with nothing published (nn = national rank) |
| `task` | A (P-B4013-01), B (P-B4428-03) or A+B |
| `sponsor`, `ein` | Sponsor of record and EIN |
| `national_rank_fy2024` | Rank among FY2024 `type=National` top-50 rows by `daf_assets_eoy` (blank if not a top-15 national) |
| `fy2024_daf_assets_usd` | FY2024 `daf_assets_eoy` from the league table |
| `metric` | `share_where_needed_most`, `share_unrestricted`, `share_no_purpose_specified`, `share_full_contact`, `share_fund_name_only`, `share_anonymous`, `share_non_anonymous`, `share_donors_identified`, `qualitative`, `none published` |
| `period`, `period_basis` | Year or fiscal year the figure describes; calendar / fiscal Jul-Jun / snapshot |
| `value_pct` | Percentage as published (blank for qualitative) |
| `value_qualifier` | exact / more than / at least / about / qualitative / not found / blocked |
| `basis` | What is counted, as the sponsor words it: grant recommendations, grants, grant dollars, donors; "implied" or "unit not stated" where unclear |
| `numerator`, `denominator` | Published counts or dollars where given |
| `definition` | Sponsor's definition of the category |
| `quote` | Verbatim text (whitespace-normalised) from `source_url` |
| `source_url`, `source_date` | Primary URL; publication or PDF creation date |
| `source_type` | sponsor annual report / sponsor release / sponsor web page / affiliate pressroom / secondary / repo-carried |
| `evidence_label` | F, S, R, B or absent (see labels above) |
| `robots` | robots.txt result for the host |
| `sponsor_default` | (B rows) `default_category` from donor-info-defaults-top20 |
| `notes` | Caveats, conflicts, UNVERIFIED flags, reasons for not-found |

## 7. Source register

| # | Source | Date | URL |
|---|---|---|---|
| S1 | Fidelity Charitable 2021 Giving Report (2019–2020 data) | 2021-02-16 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2021-giving-report.pdf |
| S2 | Fidelity Charitable 2022 Giving Report (2021 data) | 2022-02-14 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2022-giving-report.pdf |
| S3 | Fidelity Charitable 2023 Giving Report (2022 data) | PDF 2024-04-15 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf |
| S4 | Fidelity Charitable 2024 Giving Report (2023 data) | 2024-03-06 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf |
| S5 | Fidelity Charitable 2025 Giving Report (2024 data) | 2025-02-19 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf |
| S6 | Fidelity Charitable 2026 Giving Report (2025 data) | 2026-04-21 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf |
| S7 | Fidelity Charitable nonprofit FAQ ("Only 4%") | live | https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html |
| S8 | Fidelity Charitable FAQ, acknowledgement default | live | https://www.fidelitycharitable.org/faqs/all/account-holder-acknowledgements.html |
| S9 | Fidelity Charitable FAQ, grant processing ("Where It Is Needed Most") | live | https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html |
| S10 | Fidelity Charitable Giving Account guide, recommending a grant ("special purpose") | live | https://www.fidelitycharitable.org/giving-account-guide/recommending-a-grant.html |
| S11 | NPT 2025 Annual Report (FY25; FY15/FY20 chart) | modified 2026-09-10 | https://www.nptrust.org/annual-reports/npt-annual-report/ |
| S12 | NPT 2024 Annual Report (FY24) | modified 2026-09-10 | https://www.nptrust.org/annual-reports/the-2024-annual-report/ |
| S13 | NPT 2023 Annual Report (FY23) | 2024-03-12 | https://www.nptrust.org/annual-reports/the-2023-annual-report/ |
| S14 | NPT, For Nonprofits | live | https://www.nptrust.org/for-charities/ |
| S15 | Schwab Charitable FY2022 results (DAFgiving360 release, Schwab pressroom) | 2022-07-19 | https://pressroom.aboutschwab.com/press-releases/press-release/2022/Schwab-Charitable-Donors-Granted-4.7-Billion-to-Charity-in-Fiscal-Year-2022/default.aspx |
| S16 | Schwab Charitable CY2023 results | 2024-01-23 | https://pressroom.aboutschwab.com/press-releases/press-release/2024/Schwab-Charitable-Donors-Grant-Over-6-Billion-to-Charity-in-2023/default.aspx |
| S17 | DAFgiving360 FY2024 results | 2024-07-23 | https://pressroom.aboutschwab.com/press-releases/press-release/2024/DAFgiving360-Donors-Give-More-Than-6.6B-to-Charities-in-Fiscal-Year-2024/default.aspx |
| S18 | DAFgiving360 FY2025 results (repo-carried; robots-blocked) | 2025-07-29 | https://www.dafgiving360.org/press-release/fiscal-year-2025-results |
| S19 | Chariot, "Breaking down the DAFgiving360 FY25 Annual Report" [S] | 2025-08-04 | https://www.givechariot.com/resources/insights/breaking-down-the-dafgiving360-fy25-annual-report |
| S20 | Chariot, "DAFgiving360's 2025 Results" [S] | 2026-02-12 | https://www.givechariot.com/resources/insights/dafgiving360s-2025-results-4-of-our-biggest-takeaways-for-nonprofit-fundraisers |
| S21 | Vanguard Charitable, CY2021 results | 2022-01-25 | https://www.vanguardcharitable.org/news/vanguard-charitable-donors-build-record-charitable-giving-year-granting-total-over-178-billion |
| S22 | Vanguard Charitable, 25 years and $15bn | 2022-12-08 | https://www.vanguardcharitable.org/news/vanguard-charitable-celebrates-25-years-and-15-billion-granted |
| S23 | Vanguard Charitable, CY2022 results | 2023-01-25 | https://www.vanguardcharitable.org/news/vanguard-charitable-donors-set-new-granting-record-despite-economic-challenges |
| S24 | Vanguard Charitable, unrestricted giving report release | 2023-04-26 | https://www.vanguardcharitable.org/news/unrestricted-giving-increased-over-past-5-years |
| S25 | Vanguard Charitable, FY2023 results | 2023-08-10 | https://www.vanguardcharitable.org/news/vanguard-charitable-FY23-granting-record |
| S26 | Vanguard Charitable, CY2023 results | 2024-01-30 | https://www.vanguardcharitable.org/news/vanguard-charitable-donors-granted-2-billion-2023 |
| S27 | Vanguard Charitable, FY2025 results (FY2024 48.3%) | 2025-08-25 | https://www.vanguardcharitable.org/news/vanguard-charitable-donors-deepen-their-impact-driving-another-year-record-granting |
| S28 | Vanguard Charitable, CY2025 results | 2026-03-02 | https://www.vanguardcharitable.org/news/vanguard-charitable-2025-record-granting |
| S29 | Vanguard Charitable, Nonprofit organizations ("Only 4%", "Only 5%") | live | https://www.vanguardcharitable.org/nonprofit-organizations |
| S30 | AEF Difference Fact Sheet 2025 | 2025-03-03 | https://advisorwelcome.aefonline.org/wp-content/uploads/2025/03/AEF_Difference_Fact-Sheet_2025.pdf |
| S31 | MS GIFT grantmaking PDF; MS GIFT page (no figures) | 2024-10-01; live | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf ; https://www.morganstanley.com/gift |
| S32 | NPT FY2024 Schedule I narrative (via b40n13-01) | FY2024 return | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml |

## 8. Robots log

Per-request JSON lines are in scratchpad `q1328/log.jsonl` (128 requests, 117 allowed).

| First request (UTC) | Host | robots.txt | Decision | Requests |
|---|---|---|---|---|
| 2026-11-19T22:43:24 | www.fidelitycharitable.org | 200 | allowed | 10 |
| 2026-11-19T22:43:41 | www.fidelitycharitable.org | 403 (transient) | refused; retried after 200 | 5 |
| 2026-11-19T22:43:25 | www.vanguardcharitable.org | 200 (`/news/` allowed) | allowed | 74 |
| 2026-11-19T22:43:26 | www.nptrust.org / nptrust.org | 200 (`Disallow:` empty for `*`) | allowed | 20 |
| 2026-11-19T22:43:26 | www.dafgiving360.org | 403 | **blocked, nothing fetched** | 1 |
| 2026-11-19T22:46:52 | www.givechariot.com | 200 | allowed | 3 |
| 2026-11-19T22:47:23 | pressroom.aboutschwab.com | 200 (crawl-delay 10) | allowed; ≥10 s between requests | 3 |
| 2026-11-19T22:47:55 | www.businesswire.com | connection failure | blocked | 3 |
| 2026-11-19T22:48:52 | advisorwelcome.aefonline.org | 200 | allowed | 1 |
| 2026-11-19T22:49:08 | www.morganstanley.com | 200 | allowed | 7 |
| 2026-11-19T22:50:36 | web.archive.org | connection failure | blocked | 2 |

The Vanguard sitemap (`/sitemap.xml`, allowed) and the robots.txt files themselves were also read with `curl` using the same UA.
