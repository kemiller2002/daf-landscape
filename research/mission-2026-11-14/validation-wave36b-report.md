# Validation wave 36B: unlisted recipients, AI routing and per-grant exceptions

**Date:** 2026-11-19 · **Validator:** independent-validation-agent-wave36b · **Register:** [`data/mission-2026-11-14/validation-register-wave36b.csv`](../../data/mission-2026-11-14/validation-register-wave36b.csv) (V36B-01 to V36B-36)

**Studies checked**
- **Study 1:** [b41n17-g0505-unlisted-recipients.md](b41n17-g0505-unlisted-recipients.md), with `unlisted-recipients-resolution-2026-11-19.csv` and `scripts/mission_unlisted_recipients.py`.
- **Study 2:** [g0401-g0502-ai-routing-and-per-grant.md](g0401-g0502-ai-routing-and-per-grant.md), with `ai-routing-variant-2026-11-19.csv`, `exception-share-per-grant-2026-11-19.csv`, `scripts/mission_ai_routing_variant.py` and `scripts/mission_exception_per_grant.py`.

**Method**
- All three scripts were re-run into scratch (`$SCRATCH/v36b/`) from the existing caches. The repo CSVs were not touched.
- Pools, the misreport range, the per-grant core range and the routing multiples were recomputed from the committed CSVs.
- 40 matched keys **not** in the study's own hand-check sample were drawn (seed 36; 14 tier A, 13 tier B, 13 tier C) and judged on filed name and state against matched name, city and state, using the IRS files already cached (Pub 78, BMF, revocation list).
- Re-fetched first-party sources, with robots.txt checked first:
  - the GivingTuesday mirror of IRS TEOS (robots.txt 404, no rules): the Greater Horizons, SVCF and two Navigation Charitable Fund XMLs in full, and the first 400 kB of eight sponsor returns;
  - navigation.org (robots.txt 200, only a `Sitemap:` line): `/about`;
  - nber.org (`/system/files/` not disallowed): the w31422 PDF;
  - fidelitycharitable.org (`/content/dam/fc-public/docs/insights/` not disallowed): three Giving Report PDFs;
  - nptrust.org (`Disallow:` empty): the annual-report page;
  - vanguardcharitable.org (disallows `/core/` and `/profiles/` only): four annual-report pages.
- User agent `research-script/1.0` throughout. No outreach, logins or forms. crt.sh, certspotter and sec.gov were not used.

## Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| Unlisted recipients (V36B-01 to -18) | 18 | 11 | 6 | 1 | 0 |
| AI routing and per-grant exceptions (V36B-19 to -36) | 18 | 11 | 7 | 0 | 0 |
| **Total** | **36** | **22** | **13** | **1** | **0** |

## Findings

### Study 1: unlisted recipients

**What holds**
- **Reproduction.** The script reproduces the CSV byte for byte in 79 s. Both pools match to the line and the dollar: 12,265 lines / $818,725,018, and 5,013 / $643,991,900 falling to 5,011 / $431,801,212 once the two Greater Horizons totals rows are dropped (V36B-01).
- **Misreport arithmetic.** $33,463,445 × 17/21 + $6,094,566 / 4 = $28.61m, and $33,463,445 + $6,094,566 / 2 = $36.51m (V36B-02).
- **Greater Horizons.** Every stated detail re-reads from the XML (V36B-09):
  - 3,284 `RecipientTable` elements, the last two holding only `CashGrantAmt` 212187406 and 3282;
  - the 3,282 named rows sum to exactly $212,187,406;
  - Schedule I `Total501c3OrgCnt` is 3282, Part IX line 1 is $224,183,118, and scholarships are 224 / $1,413,260;
  - Schedule O has eight explanations, none on Schedule I.
- **SVCF.** The line, the 26.8% share of Part IX line 1, the $4,889,252,836 of Schedule D DAF grants and the seven Schedule O items all match (V36B-10).
- **Navigation Charitable Fund 990s.** Every figure checked re-reads exactly (V36B-11 to -15, -18):
  - **Rename:** the articles were amended 2023-11-01, per Schedule O.
  - **Contributions:** $1,309,000,000, with one Schedule B contributor, RESTRICTED.
  - **Voltage Park:** 100% owned (EIN 923779527), a Delaware C corporation, carried at $883,493,837 both years (Schedule D, method F).
  - **Grants:** $4,125,000 + $37,015,139 = $41,140,139. Vanguard Charitable received $1.75m + $15.375m = $17.125m, with “non-binding recommendations” on the 2024 grant.
  - **Net assets:** $1,289,068,375 at end-2024.
- **Corroborating detail not in the doc.** Schedule A counts the full $1.309bn as public support, with no excess-contribution reduction. That fits a gift from a publicly supported charity such as SVCF (V36B-12).
- **The fund's About page** carries the quoted McCaleb sentence. All three personal names in the doc appear on that page (V36B-16). §4.2 correctly labels the SVCF-grant = McCaleb-gift link as inference.

**What changes**
1. **The tier-A precision is not 100% (V36B-03).** In the independent sample, tier A was 6 correct, 2 wrong and 6 unsure. The two wrong keys:
   - “The Wildlife Center of Texas” (Houston-prefix EIN) matched “Texas Wildlife Center”, Amarillo, because word order is ignored;
   - “Gateway Center” GA matched a Cordele record, while Pub 78 also lists “Gateway Center 24 7 Inc”, Atlanta.

   Pooled with the study's sample, tier A is 23 correct of 25 judged, or 66% if the 10 unsure keys count as wrong.
2. **Tier B (V36B-04).** Tier B was 5 correct, 5 wrong and 3 unsure, consistent with the study's “a quarter to a half”. Two wrong tier-B keys are YMCA of Stamford (revoked 2022) and Los Angeles Mission Foundation (revoked 2026). Matching runs before the revocation class, so revoked filed EINs can be counted as misreports. YMCA of Stamford is also flagged typo-like.
3. **Tier C is mostly, not wholly, false (V36B-05).** 2 of the 13 tier-C keys are right: The Policy Circle and Social Good Fund, national organisations filed with another state. The study's own “clear misreport”, National Abortion Federation filed in DC ($1.56m), is also a tier-C key, so it sits inside the “genuinely unrecognised” $419.4m.
4. **Re-estimated misreport range.** On the pooled 75 keys:
   - tier A at 23/35 to 23/25;
   - tier B at 6/17 to 10/17;
   - tier C at 2/28.

   This gives **$26.7–36.9m (3.3–4.5%)** against $28.6–36.5m. The “about 4%, not mostly EIN error” conclusion stands.
5. **“Genuinely unrecognised” is an upper bound, not a count (V36B-06).** The $419.4m (51.2%) is arithmetically right, but it is “not found by this matcher by name and state”, and the matcher's recall is unmeasured. It includes:
   - some correct tier-C matches;
   - Rosebud Economic Development Corporation, SD ($8.38m over three keys; it appears to be a tribal enterprise [I]);
   - group-ruling schools such as Regis High School, whose property trust is under Catholic group 0928 (V36B-07).

   §3.4 qualifies the reading well. The §0 header and the “cannot be found ... under any EIN” bullet do not.
6. **Some “clear misreports” are parent or predecessor EINs (V36B-08).**
   - Delbarton School's filed EIN also carries “Order of St Benedict of NJ Delbarton School” (unmatched, $0.83m).
   - Fred Hutchinson's filed EIN is the pre-merger entity's, now on the revocation list.
   - In all, 30 tier-A keys ($6.74m) share a filed EIN with an unmatched name.
7. **The Voltage Park investment is explained on the fund's own page (V36B-17, contradicted).** The doc says “the fund's own text does not explain the investment”. Its About page says: “We've made strategic investments, including in Lightning AI (formerly Voltage Park), with the goal of achieving strong financial returns ... At this time, we do not do impact investing.” The filings remain as described, and neither source describes Voltage Park's business beyond “cloud infrastructure”.
8. **Source of the money (V36B-16).** §0 places the McCaleb quote beside the filed $1.309bn without the [I] tag that §4.2 uses. The correction below adds it.
9. **Minor (V36B-11).** “The Navigation Fund” is the DBA line of the return; the legal-name line reads “Navigation Charitable Fund (fka Further Future Foundation)”. No correction is proposed.

### Study 2: AI routing and per-grant exceptions

**What holds**
- **Reproduction.** Both scripts reproduce their CSVs byte for byte: the routing CSV (17,412 rows, 10,000 draws) and the per-grant CSV (10,156 rows). The line shares match the proxy to within 4.8×10⁻⁷ (V36B-19, -20).
- **Formula.** The code implements the stated formula exactly (V36B-21):
  - QA at the model's 0.5 convention;
  - sampled errors reworked at 1 handling-time, escaped errors at m;
  - inference on every amenable case;
  - k = 1 on P01, P07, P08 and P14 under the compliance stress.
- **E19 quotes.** The three E19 quotes appear verbatim in w31422 §6.3, p. 39, in the August 2026 revision (V36B-22). Both ends of the h range are the high false-negative-cost ends of a single-pathology frontier, and the mapping to DAF cases is correctly tagged [I].
- **m is a sweep only.** It appears in the spec rows and §A2 as an unsourced sweep (V36B-24).
- **Headline values.** All headline-table values, sweeps and compliance-stress figures match the CSV (V36B-28, -29).
- **No modal change.** The most likely winner changes in none of the 144 main cells, none of the 24 calibrated cells, and no sweep except h ≥ 0.70 (V36B-27). At h = 0.90, CF_1BN also flips P08, which the text omits.
- **Grant counts.** The re-fetched counts match:
  - Fidelity's grant counts and its counts of grants ≥ $1m (V36B-30);
  - NPT's chart data: 87,490 / 102,745 / 106,235 / 129,575 / 159,543 grants and 274 / 286 / 335 / 406 / 528 international (V36B-31);
  - Vanguard: 196K, 209K, 240,064 and 267,838 grants; 52,800, 56,744, 62,586 and 66,785 organisations (V36B-32);
  - the 990 Part III texts of Goldman Sachs, Ayco, T. Rowe Price and NPT, word for word (V36B-33).
- **Per-grant core union.** Recomputed: 6.99–8.46% excluding `none`; 2.80–7.91% with `none`; broad 16.98–31.24% (V36B-34).

**What changes**
1. **“Roughly triples” holds only at m ≤ 1 (V36B-25).**
   - Under CAL_CENTRAL the route/assist pool multiple is 2.70–3.35× at m = 1 but **2.14–2.59× at m = 5**, across archetypes.
   - Across framings, at a large national with m = 1, it is 1.72× (task) to 6.75× (field).
   - The result also depends on ρ = 0: at ρ = 0.25 the pool is $938k; at ρ = 0.5 it is $522k (V36B-21).
2. **“The gain does not depend on s” is wrong as worded (V36B-26).** The routing *pool* is identical across framings ($1,364,949 at m = 1). The *gain* over assistance ranges from +$0.57m to +$1.16m.
3. **m is tagged [I], but the headline multiple is not (V36B-24).** §0 and §A4 state the multiple without the m condition.
4. **Fidelity CY2022 recipients (V36B-30).** The 2023 Giving Report's chart gives **188,777** charities, and its text says “189,000” three times; “nearly 200,000” appears once. The study used 200,000. Re-running with 188,777 leaves the pooled core range unchanged (6.99–8.46%) and moves broad shares by ≤ 0.02 pp.
5. **NPT foreign shares mix two bases (V36B-35).**
   - The 0.31% is on NPT's report basis (US DAF program only).
   - The 2.6% of lines and 7.5% of dollars are on its whole-entity Form 990.
   - The report's own international dollar share is 5.9% (FY2023: $269.08m of $4.54bn) and 6.4% (FY2024: $352.23m of $5.49bn).
   - Schedule F's 413 and 488 rows exceeding 335 and 406 grants reflects both the scope difference and rows-versus-grants counting. The doc's conclusion that Schedule F cannot be read as grant counts stands.
6. **Pool rule (V36B-36).** T. Rowe Price states no dollar figure, so only the unitemised-mean test applies to it, contrary to the §B3 wording.

## Exact corrections

### `research/mission-2026-11-14/b41n17-g0505-unlisted-recipients.md`

- **Find:** "Genuinely unrecognised on 2026-11 lists"
- **Replace with:** "Not found by name and state on 2026-11 lists (an upper bound on unrecognised: matcher recall unmeasured) [V wave 36B]"

- **Find:** "plus tier-C matches judged false, $35.2m)"
- **Replace with:** "plus tier-C matches, mostly false (2 of 28 right in the pooled 75-key hand check), $35.2m) [V wave 36B]"

- **Find:** "- About half of the pool goes to organisations that **cannot be found on either IRS list under any EIN** by name and state."
- **Replace with:** "- About half of the pool goes to organisations that **this matcher did not find on either IRS list under any EIN** by name and state. That is an upper bound on unlisted recipients, not a count: the matcher's recall is unmeasured (brand names such as “Fidelity Charitable” are missed), a few tier-C keys counted here are right (The Policy Circle; Social Good Fund; National Abortion Federation filed in DC), and the class includes plausibly legitimate absences such as group-ruling schools and an apparently tribal enterprise (Rosebud Economic Development Corporation, SD, $8.4m) [H/I] [V wave 36B]"

- **Find:** "    - **tier A** (identical name, same state): **17 of 17 judged** (Wilson 82–100%; 17/21 = 81% if unsure counts as wrong);"
- **Replace with:** "    - **tier A** (identical name, same state): **17 of 17 judged** (Wilson 82–100%; 17/21 = 81% if unsure counts as wrong). A validator sample of 14 other tier-A keys found 6 correct, 2 wrong (a word-order collision and a same-name collision) and 6 unsure, so pooled tier A is 23 of 25 judged, or 66% if unsure counts as wrong [H] [V wave 36B]"

- **Find:** "    - **tier C** (identical name, other state): **0 of 15**."
- **Replace with:** "    - **tier C** (identical name, other state): **0 of 15**. The validator's 13 further tier-C keys had 2 correct (national organisations filed with another state), so pooled 2 of 28 [H] [V wave 36B]"

- **Find:** "  - The misreport estimate therefore rests on tier A, plus a quarter to a half of tier B [H]."
- **Replace with:** "  - The misreport estimate therefore rests on tier A, plus a quarter to a half of tier B [H]. On the pooled 75-key check (tier A 23/35 to 23/25, tier B 6/17 to 10/17, tier C 2/28) it is $26.7–36.9m (3.3–4.5%) [C/H] [V wave 36B]"

- **Find:** "SVCF's Schedule I does not say whether the grant came from a DAF, and SVCF's Schedule R does not list the recipient [F/I]."
- **Replace with:** "SVCF's Schedule I does not say whether the grant came from a DAF, and SVCF's Schedule R does not list the recipient [F/I]. That this grant is the McCaleb gift is an inference, not a filed fact: no filing names the donor, though the fund's Schedule A counts the full $1,309,000,000 as public support, consistent with a single gift from a publicly supported charity such as SVCF [F/I] [V wave 36B]"

- **Find:** "  - National Abortion Federation ($1.85m MD, plus $1.56m filed with a DC address);"
- **Replace with:** "  - National Abortion Federation ($1.85m MD, tier A; the further $1.56m filed with a DC address is a tier-C key, so it is counted in the not-found total although the match looks right) [V wave 36B]"

- **Find:** "  - Delbarton School ($1.94m);"
- **Replace with:** "  - Delbarton School ($1.94m; the same filed EIN also carries “Order of St Benedict of NJ Delbarton School”, $0.83m, unmatched, so the filed EIN may be the operating order's rather than a keying error) [I] [V wave 36B]"

- **Find:** "By pool: unlisted-EIN 5 correct / 11 wrong / 4 unsure; blank-EIN 13 / 6 / 1."
- **Replace with:** "By pool: unlisted-EIN 5 correct / 11 wrong / 4 unsure; blank-EIN 13 / 6 / 1.\n\n**Validator re-check (wave 36B).** An independent seeded sample of 40 other matched keys (14 tier A, 13 tier B, 13 tier C) gave:\n- **tier A:** 6 correct, 2 wrong, 6 unsure. The wrong keys are “The Wildlife Center of Texas” TX matched to “Texas Wildlife Center”, Amarillo (word order is ignored), and “Gateway Center” GA matched to a Cordele record.\n- **tier B:** 5 correct, 5 wrong, 3 unsure. Two of the wrong keys, YMCA of Stamford and Los Angeles Mission Foundation, have filed EINs on the revocation list but were matched to other organisations; matching runs before the revocation class.\n- **tier C:** 2 correct, 11 wrong. The correct ones are The Policy Circle and Social Good Fund, national organisations filed with a donor-side state.\n\nPooled over 75 keys: tier A 23 of 25 judged (66% if unsure counts as wrong), tier B 6 of 13, tier C 2 of 28 [H] [V wave 36B]"

- **Find:** "- Sponsor EIN misreporting that can be shown from public names and states is **$29–37m**, 3.5–4.5% of the $818.7m."
- **Replace with:** "- Sponsor EIN misreporting that can be shown from public names and states is **$27–37m**, 3.3–4.5% of the $818.7m, on the pooled 75-key hand check ($28.6–36.5m on the original 40 keys). Part of it is filing under a parent, religious-order or predecessor EIN rather than keying error (e.g. Delbarton School; Fred Hutchinson's pre-merger EIN) [C/H/I] [V wave 36B]"

- **Find:** "- About **half the pool ($419m) goes to organisations with no IRS listing under that name in that state.**"
- **Replace with:** "- About **half the pool ($419m) goes to organisations that the matcher did not find under that name in that state.** This is an upper bound on unlisted recipients, not a count of them: recall is unmeasured, and the class includes some correct tier-C matches [V wave 36B]"

- **Find:** "The fund's own text does not explain the investment."
- **Replace with:** "The fund's filings do not explain the investment, but its About page does: “The Navigation Fund’s founding endowment was provided by Jed McCaleb … We've made strategic investments, including in Lightning AI (formerly Voltage Park), with the goal of achieving strong financial returns that enable us to do more through our grantmaking. At this time, we do not do impact investing” (navigation.org/about, read 2026-11-19) [P] [V wave 36B]"

- **Find:** "the filings do not reconcile them."
- **Replace with:** "the filings do not reconcile them. The fund's About page names the holding “Lightning AI (formerly Voltage Park)” and calls it a strategic investment made “with the goal of achieving strong financial returns” [P]; neither the page nor the filings describe its business further [V wave 36B]"

### `research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md`

- **Find:** "   - At the evidence-bounded share of high-confidence cases (h = 0.21–0.49, from E19), routing roughly triples the pool, provided an escaped error costs no more than about five handling-times."
- **Replace with:** "   - At the evidence-bounded share of high-confidence cases (h = 0.21–0.49, from E19), routing multiplies the pool by 2.7–3.4× when an escaped error costs one handling-time and by 2.1–2.6× at five (CAL_CENTRAL, across archetypes). Both m and ρ = 0 (no residual human time on AI-closed cases) are unsourced [I]; at ρ = 0.25 the large-national pool falls from $1.36m to $938k [S] [V wave 36B]"

- **Find:** "   - The gain does not depend on s. The routing formula never uses the disputed time-saving parameter, so the field and task framings give the same routing result."
- **Replace with:** "   - The routing pool does not depend on s: the routing formula never uses the disputed time-saving parameter, so the field and task framings give the same routing pool. The gain over assistance does depend on s: at a large national (m = 1) the routing pool is 6.8× the assist pool under the field framing, 3.1× under the central one and 1.7× under the task framing [C] [V wave 36B]"

- **Find:** "then P03 and P07 flip to C, and at h = 0.90 so do P13 and P14."
- **Replace with:** "then P03 and P07 flip to C, and at h = 0.90 so do P13 and P14 (and P08 at CF_1BN) [V wave 36B]"

- **Find:** "  - Hence the threefold pool and the large-national platform break-even rising from 13% to 29–38% of draws (m = 1–5)."
- **Replace with:** "  - Hence a large-national pool 2.4–3.1× the assist pool and a platform break-even rising from 13% to 29–38% of draws (m = 5 to 1). Both depend on the unsourced m and on ρ = 0 [V wave 36B]"

- **Find:** "against 2.6% of its recipient lines and 7.5% of its dollars [F/C]."
- **Replace with:** "against 2.6% of its recipient lines and 7.5% of its dollars on its whole-entity Form 990. The annual report covers the US DAF program only; on its own figures international grants are 5.9% (FY2023) and 6.4% (FY2024) of grant dollars [F/C] [V wave 36B]"

- **Find:** "  - On NPT's own figures, foreign grants are **0.31% of grants, 2.6% of recipient lines and 7.5% of dollars** (FY2023–24)."
- **Replace with:** "  - Foreign grants are **0.31% of grants** on NPT's annual-report basis (US DAF program only), and **2.6% of recipient lines and 7.5% of dollars** on its whole-entity Form 990 (FY2023–24). The report's own international dollar share is 5.9% and 6.4% ($269.08m of $4.54bn; $352.23m of $5.49bn), so the two bases should not be compared directly [F/C] [V wave 36B]"

- **Find:** "They include only sponsor-years whose source dollars are within 20% of Part IX and whose unitemised mean is ≤ $5,000."
- **Replace with:** "They include only sponsor-years whose source dollars are within 20% of Part IX and whose unitemised mean is ≤ $5,000. T. Rowe Price states no dollar figure, so only the unitemised test applies to it [V wave 36B]"

- **Find:** "2. **Period mismatch.** Fidelity and Vanguard publish calendar years, while their 990 years end in June."
- **Replace with:** "2. **Period mismatch.** Fidelity and Vanguard publish calendar years, while their 990 years end in June. Fidelity's 2023 Giving Report charts 188,777 charities for CY2022 (its text says “189,000” three times and “nearly 200,000” once); the 200,000 used here overstates FY2023 R by about 5,600. With 188,777, the pooled core range is unchanged and broad shares move by at most 0.02 pp [C] [V wave 36B]"

### `research/mission-2026-11-14/gap19-exception-load-proxy.md`

- **Find:** "  - SVCF FY2023 → Further Future Foundation (92-1117448), **$1,309.0m**, BMF ruling 2023-03 (recent ruling);"
- **Replace with:** "  - SVCF FY2023 → Further Future Foundation (92-1117448), **$1,309.0m**, BMF ruling 2023-03 (recent ruling). The recipient renamed itself Navigation Charitable Fund on 2023-11-01. By end-2024 it had granted $41.1m and held $883.5m in its wholly owned for-profit, Voltage Park, Inc. ([b41n17-g0505-unlisted-recipients.md](b41n17-g0505-unlisted-recipients.md) §4.2) [V wave 36B]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "Shared-platform break-even falls to 16% of draws, and no process changes its most likely winner [S] ([gap19-ai-calibration.md](gap19-ai-calibration.md); wave 31A)."
- **Replace with:** "Shared-platform break-even falls to 16% of draws, and no process changes its most likely winner [S] ([gap19-ai-calibration.md](gap19-ai-calibration.md); wave 31A). Routing high-confidence cases to AI alone, instead of assisting every case, raises the large-national pool to $1.06–1.36m if an escaped error costs 1–5 handling-times (an unsourced sweep [I]; $44k at 20). It still changes no process's most likely winner at h ≤ 0.49 [S] ([g0401-g0502-ai-routing-and-per-grant.md](g0401-g0502-ai-routing-and-per-grant.md); wave 36B) [V wave 36B]"

- **Find:** "That proxy measures recipients, not review ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md); wave 32A)."
- **Replace with:** "That proxy measures recipients, not review ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md); wave 32A). Counted per grant at Fidelity, NPT and Vanguard, the core proxy is about 7–8.5% of grants (2.8–7.9% if no unitemised recipient is flagged). The broad share, 17–31%, depends on an unidentified grants-per-recipient assumption [C/I] ([g0401-g0502-ai-routing-and-per-grant.md](g0401-g0502-ai-routing-and-per-grant.md); wave 36B) [V wave 36B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.40 Unlisted recipients, AI routing and per-grant exceptions (validated, wave 36B)\n\n**Unlisted recipients, AI routing and per-grant exceptions** (validated, wave 36B). Top-50 FY2023–24 Schedule I lines to EINs on neither IRS list total $818.7m. A name-and-state match finds a listed charity under another EIN for only about 4% of that ($27–37m on a 75-key hand check), so sponsor EIN error is not the main explanation. About half ($419m) was not found by name and state; that is an upper bound on unlisted recipients, because the matcher's recall is unmeasured. SVCF's single $1.309bn FY2023 line went to Further Future Foundation, renamed Navigation Charitable Fund in November 2023. By end-2024 the fund had granted $41.1m, $17.1m of it to Vanguard Charitable with non-binding recommendations, and held $883.5m in its wholly owned for-profit, Voltage Park, which its website now calls Lightning AI. Greater Horizons' $212.2m blank line is a totals row. Routing confident cases to AI alone raises the large-national AI value pool from $445k to $1.06–1.36m if an escaped error costs 1–5 handling-times, an unsourced assumption, but it changes no process's likely winner. Counted per grant, the core review-need proxy is about 7–8.5% of grants at Fidelity, NPT and Vanguard [V wave 36B]\n\n---\n\n## Source register"
