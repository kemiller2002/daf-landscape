# Validation wave 43A: sector shares across all sponsors, and the methodology §7 AI-overlay clarification

**Date:** 2026-11-20 · **Validator:** independent-validation-agent-wave43a · **Register:** [`validation-register-wave43a.csv`](../../data/mission-2026-11-14/validation-register-wave43a.csv) (V43A-01 to V43A-32)

**Studies checked**
1. [`b39n4-01-sector-join-all-sponsors.md`](b39n4-01-sector-join-all-sponsors.md), [`sector-join-all-sponsors-2026-11-20.csv`](../../data/mission-2026-11-14/sector-join-all-sponsors-2026-11-20.csv) and `scripts/mission_sector_join_all.py`. These cover recipient sectors for all 2,705 itemising sponsor-years, with foreign and sub-$5,000 grants, reconciled to sponsors' published splits.
2. [`b4301-05-methodology-s7-clarification.md`](b4301-05-methodology-s7-clarification.md), [`overlay-rule-test-2026-11-20.csv`](../../data/mission-2026-11-14/overlay-rule-test-2026-11-20.csv) and `scripts/mission_b4301_05_overlay_rule_test.py`. These cover the proposed §7a–§7c rules, a 137-row rule test and 10 proposed corrections.

**Method**
- **Study 1.**
  - The script was re-run cache-only into scratch (`v43a/`) from `npcache`, `rcp/lines`, `q120201/lines` and `rcp/bmf`.
  - All headline, treatment, segment and reconciliation figures were recomputed independently from the CSV rows.
  - World Vision and other foreign-heavy weights were read from the coverage-gap CSV.
  - A one-parameter null for the Fidelity test was computed (see finding 4).
- **Study 2.**
  - The script was re-run to scratch.
  - A random sample of 20 of the 137 rows (seed 43) was checked against its source tables, and all 9 changing or annotated rows were read individually.
  - The ten Finds were counted by script.
- **Re-fetched pages.** robots.txt was read first on 2026-11-20, with UA `research-script/1.0`:
  - www.fidelitycharitable.org: 200. Only /retired/, /sample-email/, /nuance/ and /content/dam/fc-public/docs/vessel/ are disallowed. The 2025 and 2026 Giving Report PDFs were fetched.
  - help.givechariot.com: 200, `Allow: /`. The MCP page was fetched as HTML and `.md`.
  - www.ncfgiving.com: 200, empty `Disallow:`. /ai-search and the homepage were fetched.
  - www.dafgiving360.org: robots.txt returned 403, so nothing was fetched.
- **Not used:** crt.sh, certspotter and sec.gov. There was no outreach and no login. The user agent was never changed.
- **Repo files written:** only this report and the register. Nothing was committed or pushed.

## 1. Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| 1. Sector join, all sponsors (V43A-01 to 16) | 16 | 10 | 4 | 1 | 1 |
| 2. Methodology §7 clarification (V43A-17 to 32) | 16 | 7 | 9 | 0 | 0 |
| **Total** | **32** | **17** | **13** | **1** | **1** |

Of the 10 proposed corrections, 3 are accepted (closing tag normalised only), 7 are modified and none is rejected. The validator adds 19 further corrections:
- 2 Benevity annotations in the v1.1 record;
- 4 edits to the b4301-05 study itself;
- 7 edits to the b39n4-01 study itself;
- 3 sector-share propagation edits;
- 3 industry report items: §11.60 and two Benevity list annotations.

That makes 29 items. Each Find occurs exactly once, both alone and when the items are applied in order (validator script, see end).

## 2. Findings: study 1 (sector join, all sponsors)

1. **Reproduces exactly.**
   - The re-run takes 27.5 s and gives md5 `6fcefe1ad983f2b60b35a39dcd30b328`, byte-identical to the committed CSV (15,168 rows).
   - Coverage is 2,705 sponsor-years, 1,379 sponsors, 1,092,809 lines and 264,127 EINs (224,264 in the BMF).
   - The Schedule I and DAF-to-DAF totals equal the coverage-gap CSV with a maximum difference of $0.00 (V43A-01).
2. **Headline and treatment shares confirmed** (V43A-02 to 05).
   - **t_a, DAF-weighted, full layer** ($101,014,250,420): education 22.98%, human services 14.60%, religion 14.06%, public-society benefit 13.17% (NTEE T 5.73), health 9.20%, foreign 3.12%, unclassified 5.91%.
   - **t_b** ($115.52bn): public-society benefit 23.71%, education 20.20%.
   - **t_d:** base $95.23bn.
   - **Bridge:** $93.41bn net, $14.51bn DAF-to-DAF (13.4%).
   - **Filed basis:** foreign 6.93%.
   - **Top 50 against the rest:** education 26.1% against 16.7%, and unclassified 4.5% against 11.4%.
3. **The reconciliation distances are right** (V43A-07).
   - **On Fidelity's FY2024 lines:** t_b 0.1226 / 0.1178 (sched_i) and 0.1301 / 0.1181 (full layer); t_a 0.212–0.240; t_d 0.309–0.344.
   - **Pooled lines:** t_b 0.102–0.147; t_a 0.232–0.270; t_d 0.325–0.360.
   - **Rounding:** t_b's plus_foreign layer against CY2025 is 0.114, so over all three layers t_b is 0.11–0.13.
4. **The Fidelity test measures size, not mechanism** (V43A-08). The study says Fidelity's chart "evidently" counts grants to other sponsors as society benefit. The validator checked this against a one-parameter null.
   - **The null:** add to t_a a pure society-benefit mass equal to Fidelity's DAF-to-DAF lines (10.5% of its net), then renormalise.
   - **Result:** this gives 0.122 against CY2024 and 0.117 against CY2025, the same as t_b. The best-fitting added mass is 16% (0.092) and 13% (0.104).
   - **Reading:** DAF-to-DAF is a sufficient size match, not an identified mechanism. The rejection of t_d stands.
5. **Fidelity's published shares are confirmed verbatim, but the page citation is wrong** (V43A-09, V43A-10).
   - **2025 Giving Report (CY2024).** All 9 dollar shares (society benefit 25%, education 23%, religion 13%, human services 13%, health 8%, arts 6%, international 5%, environment 5%, other 2%) and all 9 volume shares match the script constants.
     - The chart is on **p.12** and the appendix table on p.21, not p.20. direction-recipients §1.4 already cites p.12.
   - **2026 Giving Report (CY2025, p.9).** The shares are 23.4 / 24.8 / 13.1 / 12.2 / 7.5 / 5.5 / 5.2 / 5.9 / 2.5%.
     - The methodology on p.12 removes "$727 million" of outlier granting from the sector chart.
6. **The period mismatch is understated** (V43A-11).
   - **Overlap.** FYE June 2024 overlaps CY2024 by six months and CY2025 not at all.
   - **CY2024 outlier.** Fidelity removed a $430m outlier grant only from its average grant size, so it is inside the CY2024 sector split (2.9% of $14.9bn). Its sector is unknown.
   - **CY2025 outlier.** $727m is 4.0% of $18.3bn.
7. **World Vision confirmed** (V43A-12).
   - **World Vision:** line 3 is $1,136,219,392 (FY2023) and $1,095,205,453 (FY2024), with w2 0.00318 and 0.00451. That leaves $8.5m DAF-weighted.
   - **Other foreign-heavy sponsors:** Rotary 0.026–0.035; JDC 0.0011–0.0072; PEF Israel 0.194–0.248; CAF America 0.854–0.929.
   - **Non-top-50 filed line 3:** $7.14bn.
   - **The point holds.** The filed foreign share is not DAF money.
8. **The pro-rata weight is untestable and cuts both ways** (V43A-13).
   - **World Vision.** Pro rata gives 90% of its DAF grants a foreign destination, which is implausible but immaterial.
   - **PEF Israel, Myriad and CAF America.** The DAF grants plausibly are the foreign grants, so pro rata may understate foreign there.
   - **Community foundations.** Discretionary and scholarship grants go unseparated.
   - **Verdict.** It is correctly tagged [I].
9. **The §3.2 layer label is wrong** (V43A-06, contradicted).
   - $77.91bn is the plus_foreign_sub5k base; plus_foreign is $75.99bn.
   - The two layers differ by up to 0.4 pt, not 0.1.
10. **The recommendation is sound as a convention but should be labelled [I]** (V43A-14).
    - **Use t_b for sponsor-published comparisons, and t_a with T shown (t_c) for where DAF money ends up.**
    - **The case for t_b is thin.** It rests on one sponsor's dollar split, a size-only fit, a zero-overlap CY2025 comparison and undisclosed outliers.
    - **The t_b base double counts.** It exceeds t_a by the DAF-to-DAF dollars, so 23.7% must never be read as a market share.
11. **Propagation** (V43A-15). Only FINAL-STATUS and direction-recipients §0 and §1.4 carry recipient-sector shares; all of them are top-50 figures. strategic-synthesis §0 and the industry report body carry none, apart from the §11.27 foreign 7.8%, which is unchanged. The top-50 figures stay correct, and the all-sponsor figures are added beside them. DAFgiving360's robots.txt is still 403 (V43A-16).

## 3. Findings: study 2 (methodology §7 clarification)

1. **Reproduces exactly** (V43A-17).
   - **Counts.** 137 rows (34 / 2 / 4 / 42 / 5 / 30 / 20); 0 first-GREEN eligible; 12 GREEN-labelled; 7 changes against the governing label plus 2 annotations; 24 superseded labels reproduced; no RED; no census change; 87 area rows.
   - **Sample** (V43A-28). 20 of 20 sampled rows match their source labels, and their proposed outcomes equal the governing labels.
2. **The Chariot quote is verbatim** (V43A-18).
   - The FAQ "Which Chariot products does this connector support?" answers: "This connector is built for Chariot's Gift Processing platform. It also surfaces DAFpay components for organizations using Chariot's DAFpay product."
   - Disbursements appears only in the site navigation. The page was last updated 2026-07-22.
   - **But the page's intro** also offers lookups of "DAF eligibility, IRS status" from "Chariot's database of verified nonprofits", although no such tool is listed.
3. **Chariot Disbursements should be a pending note, not a rating change** (V43A-19, V43A-23).
   - **Why it conflicts with the study's own rule.** The study's §7a(4) says evidence that would lower a flag must meet T1. The downgrade instead rests on a product list for another product.
   - **Why it needs adjudication.** Both v1.1 scorers agreed on AMBER.
   - **Decision.** Keep AMBER, with a pending-adjudication note (P-B430105-01) giving the proposed None (watch) reading. The validator adds rule §7a(7), "a two-scorer flag is not removed on a confinement reading alone".
4. **Chariot verification is not settled by an annotation** (V43A-20). On the Candid precedent (an MCP exposing the vendor's data counts at T2 and gives AMBER (low)), the intro's verified-nonprofit and DAF-eligibility wording could tie the MCP to verification. This is recorded as an open question.
5. **NCF** (V43A-21, V43A-22).
   - **The page.** The quote is present, but only in the page metadata. The record date is 2026-08-12, and the record status field reads "private". The server-rendered homepage shows no link.
   - **The study's reasoning is inconsistent.** It justifies NCF by parity with Fidelity's Virtual Assistant. But Fidelity's rows are None (inform-only), and the study's own §5 says that assistant is not described as AI.
   - **Decision.** AMBER (low) is supportable on Candid's read-only precedent, marked provisional.
6. **Tie precedence is ambiguous** (V43A-24). Benevity's Match Assurance is "adjacent to the validation product" yet counts on T3, while Chariot's confined components do not count. Rule 5 should say "unless it also meets T1, T3 or T4".
7. **The entity scope rule is consistent** (V43A-25). T4 restates it, all 20 gap19 rows are unchanged, and Agentforce stays off NCF.
8. **The stale Benevity RED claim is partially confirmed** (V43A-27).
   - **Still RED.** The v11 §5 row, the v11 §6 text and industry report lines 314 and 331 still read RED.
   - **Recorded, not applied.** In quadrant-v11-rescore.md the wave 21 change sits only in the governing appendix; its body still reads RED.
   - **Fix.** Annotate rather than rewrite the consensus record.
9. **The mechanics of the ten corrections** (V43A-26).
   - **Find check.** Every Find occurs once, and no value has straight quotes.
   - **Two defects.** Items 1 and 3 drop the full stop before following text.
   - **Section placement.** §7a–§7c are inserted under a 2026-11-14 "v1.1 area notes" heading with no date or status. The validator labels them "proposed 2026-11-20 … binding from the next re-score" (V43A-31).
10. **The first-GREEN wording is consistent with §7c** (V43A-29, V43A-32). FINAL-STATUS and the census say "none is the first GREEN under §7". §11.57 says the same thing in other words. No change is needed.

### Accept / modify / reject (the 10 proposed corrections)

| # | File | Find (start) | Verdict | Reason |
|---|---|---|---|---|
| 1 | evidence-quadrant-methodology.md | "An **AI-governance overlay** is reported…" | **modify** | Add the missing full stop before the following sentence; tag |
| 2 | evidence-quadrant-methodology.md | "- **RED:** AI can complete…" | **modify** | Date and status the rules; add "unless it also meets T1, T3 or T4" to §7a(5); add §7a(7), so a two-scorer flag is not removed on confinement alone |
| 3 | direction-ai-product-census.md | "The overlay vocabulary was written…" | **modify** | Add the missing full stop; tag |
| 4 | direction-ai-product-census.md | "and §7 has no rule…" | **modify** | Keep the wave 42A statement as history ("had no rule … [V wave 42A]") and append the §7b reading |
| 5 | quadrant-calibration.md | "No decision authority. \| **GREEN**" | accept | Tag normalised |
| 6 | quadrant-calibration.md | "**GREEN / none.** …" | accept | Tag normalised |
| 7 | quadrant-v11-blind-and-calibration.md | Chariot Disbursements row | **modify** | AMBER stands; the proposed None (watch) reading becomes a pending-adjudication note (P-B430105-01) |
| 8 | quadrant-v11-blind-and-calibration.md | Chariot verification row | **modify** | Keep the annotation; add the open Candid-parity question from the MCP intro |
| 9 | quadrant-v12-targeted-rescore.md | "\| NCF (A3 and A1) \| none evidenced" | **modify** | Mark provisional; record the "private" status; cite Candid's read-only AMBER (low) |
| 10 | b43n25-01-green-overlay-validation.md | "proposed for clarification as P-B4301-05." | accept | Tag normalised |

**Adjudication note (Chariot).** A rating that two scorers agreed cannot be changed by a study or a validator alone. It is therefore applied as a pending note, and the rating stays AMBER until the next re-score adjudicates P-B430105-01.

## Exact corrections

### `research/mission-2026-11-14/evidence-quadrant-methodology.md`

- **Find:** "An **AI-governance overlay** is reported for every area as a flag, not an axis."
- **Replace with:** "An **AI-governance overlay** is reported for every area as a flag, not an axis. It is a flag on provider rows scored in A1–A5 only; vendor products outside those areas get product-level readings (see §7, “AI overlay scope”) (b4301-05). [V wave 43A]"
- **Find:** "- **RED:** AI can complete a money-moving or status-clearing action without documented sponsor or human approval."
- **Replace with:** "- **RED:** AI can complete a money-moving or status-clearing action without documented sponsor or human approval.\n- **None:** no AI capability is evidenced. This is not evidence of absence (as used in the v1.1 consensus, quadrant-v11-blind-and-calibration.md §6).\n\n**AI overlay scope (§7a; proposed 2026-11-20 in b4301-05, binding from the next re-score, like the other §7 notes).**\n1. The overlay is a flag on provider rows scored in an area A1–A5. Only those rows carry an area overlay, and only they count in area totals.\n2. A vendor product outside A1–A5 may be read with the same GREEN, AMBER and RED tests. The result is a product-level reading, written against the product (for example in the AI product census). It is not an area overlay.\n3. A product-level reading enters a provider row only as a component under §7b, and only on a documented tie: T1, the capability is documented in the scored offering; T2, it runs on a vendor-wide AI platform or agent channel that its source does not confine to another product, or that a source says reaches the scored offering; T3, it performs the scored offering’s own function (moves its grants or sets its eligibility status); T4, a source ties a vendor capability to the sponsor’s program (entity scope rule).\n4. Ties are asymmetric, so the overlay can add a flag but never clear one. An AMBER or RED component counts on any of T1–T4. A GREEN component counts only on T1: it must be live in the scored offering, with its controls documented there. Evidence that would lower a flag must meet the same T1 test.\n5. A capability that its source confines to another product is not counted unless it also meets T1, T3 or T4. If it is AMBER or RED, the provider row shows it as “adjacent product AMBER/RED: <product>”, so the flag stays visible.\n6. The entity scope rule applies unchanged: a vendor’s, parent’s or owner’s capability is not a sponsor’s capability, and the reverse also holds, unless T4 is met.\n7. A flag that both scorers agreed is not removed on a confinement reading alone: it stands, with a pending note, until adjudicated (§5).\n\n**AI overlay components (§7b).**\n1. Count each live AI component tied under §7a. Live means GA, beta, or a preview open to customers. Announced or roadmap items are WATCH and do not count. Automation or navigation that its source does not describe as AI is not an AI component.\n2. The provider’s flag is its most severe counted component: RED, then AMBER, then GREEN. A component whose controls could not be read counts as AMBER (unverified).\n3. A provider is GREEN only if every counted component is GREEN. A GREEN component never offsets, lowers or clears another component’s AMBER or RED.\n4. When counted components differ, write the flag and then the split: “AMBER (mixed: GREEN <component>; AMBER <component>)”. Product rows keep their own readings.\n5. With no counted component, the flag is None, with its existing qualifier.\n\n**“First GREEN” (§7c).** “First GREEN”, “only GREEN” and “no provider earns GREEN” refer to area overlays only. A first GREEN needs all four of the following:\n1. A provider row scored in A1–A5 under v1.1 or later. v1.0 had no written GREEN test. Its labels (GREEN for Fidelity Charitable; “GREEN / none” for Ren, Ren RDE, RCF and AEF) were withdrawn by the v1.1 consensus and are history, not precedent.\n2. At least one counted AI component. “None” can never be GREEN, and neither can rule-based or navigation-only automation.\n3. Every counted component GREEN under §7b, on admissible first-party evidence (§3, §8) for the scored offering.\n4. The two-scorer rule (§5): the GREEN must be reproduced by the blind scorer or upheld in an adjudication. A single-scorer or provisional label is written “GREEN (provisional)” and is not a first GREEN.\nThe claim names the version and date (“first GREEN area overlay under §7, v1.x, <date>”). A product-level reading outside A1–A5 is a “GREEN-eligible product reading”, never a first GREEN. If a first GREEN is withdrawn, later claims must say so (b4301-05) [V wave 43A]"

### `research/mission-2026-11-14/direction-ai-product-census.md`

- **Find:** "The overlay vocabulary was written for DAF providers."
- **Replace with:** "The overlay vocabulary was written for DAF providers. Under methodology §7a every row here is a product-level reading: it is not an area overlay, it can never be a first GREEN (§7c), and it enters an A1–A5 provider’s flag only as a tied component under §7b (b4301-05). [V wave 43A]"
- **Find:** "and §7 has no rule for rating a provider from one GREEN component [V wave 42A]"
- **Replace with:** "and §7 had no rule for rating a provider from one GREEN component [V wave 42A]. Under methodology §7b (b4301-05) a GREEN component cannot offset Fia’s AMBER; Application Analysis is not shown live in CommunitySuite, so it is not yet a counted component of the Foundant row [V wave 43A]"

### `research/mission-2026-11-14/quadrant-calibration.md`

- **Find:** "No decision authority. | **GREEN**"
- **Replace with:** "No decision authority. | **GREEN** (v1.0 label; withdrawn by the v1.1 consensus to None (inform-only); not a first GREEN or precedent under methodology §7c; b4301-05) [V wave 43A]"
- **Find:** "**GREEN / none.** The decision logs are not public."
- **Replace with:** "**GREEN / none.** The decision logs are not public. (v1.0 label; withdrawn by the v1.1 consensus to None; “none” cannot be GREEN under methodology §7c; b4301-05) [V wave 43A]"

### `research/mission-2026-11-14/quadrant-v11-blind-and-calibration.md`

- **Find:** "| 2.80 (2.80–2.80) | 3.52 (3.52–3.52) | 1.0/1.0 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | AMBER"
- **Replace with:** "| 2.80 (2.80–2.80) | 3.52 (3.52–3.52) | 1.0/1.0 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | AMBER; pending adjudication (queue P-B430105-01): under proposed methodology §7a and §7b this row would read None (watch: agent-capable API) [adjacent product AMBER: Chariot Gift Processing AI; Chariot MCP], because Chariot’s MCP help page names only Gift Processing and DAFpay as supported products (“built for Chariot's Gift Processing platform. It also surfaces DAFpay components”). Both v1.1 scorers agreed on AMBER, so AMBER stands until adjudicated (b4301-05) [V wave 43A]"
- **Find:** "| 2.58 (2.58–2.58) | 2.65 (2.65–2.65) | 1.0/1.0 | Proven Leaders | Proven Leaders / insufficient evidence | adjudicated | None"
- **Replace with:** "| 2.58 (2.58–2.58) | 2.65 (2.65–2.65) | 1.0/1.0 | Proven Leaders | Proven Leaders / insufficient evidence | adjudicated | None [adjacent product AMBER: Chariot Gift Processing AI; Chariot MCP] (annotation under proposed methodology §7a; open question for P-B430105-01: the MCP page also offers lookups of “DAF eligibility, IRS status” from “Chariot's database of verified nonprofits”, which on the Candid precedent could tie it to verification) (b4301-05) [V wave 43A]"
- **Find:** "| adjudicated | RED (provisional)"
- **Replace with:** "| adjudicated | RED (provisional); superseded by AMBER (provisional) in wave 21 (quadrant-v11-rescore.md, Validation corrections (wave 21)) [V wave 43A]"
- **Find:** "It is adjacent to the validation product, so the flag is provisional."
- **Replace with:** "It is adjacent to the validation product, so the flag is provisional. (Superseded: wave 21 moved Benevity to AMBER (provisional), because first-party pages keep human approval by default; see quadrant-v11-rescore.md, Validation corrections (wave 21).) [V wave 43A]"

### `research/mission-2026-11-14/quadrant-v12-targeted-rescore.md`

- **Find:** "| NCF (A3 and A1) | none evidenced"
- **Replace with:** "| NCF (A3 and A1) | none evidenced at v1.2; at the next re-score AMBER (low), provisional, under methodology §7a and §7b: NCF’s own “AI-powered search experience” (ncfgiving.com/ai-search, record dated 2026-08-12, record status field “private”; gap19-ai-coverage S18–S20), re-read 2026-11-20; a read-only search with undocumented controls, as Candid’s AMBER (low) (b4301-05) [V wave 43A]"

### `research/mission-2026-11-14/b43n25-01-green-overlay-validation.md`

- **Find:** "proposed for clarification as P-B4301-05."
- **Replace with:** "proposed for clarification as P-B4301-05. The proposed rules (b4301-05-methodology-s7-clarification.md, §7a–§7c) confirm both inferences: a GREEN component cannot lift a provider that also has an AMBER component, and no vendor product outside A1–A5 can be a first GREEN (b4301-05) [V wave 43A]"

### `research/mission-2026-11-14/b4301-05-methodology-s7-clarification.md`

- **Find:** "Rule (a) only confirms that a sponsor's own feature belongs on its row, as Fidelity's Virtual Assistant does on Fidelity's."
- **Replace with:** "Rule (a) only confirms that a sponsor's own AI feature belongs on its row. The precedent is Candid’s read-only AMBER (low), not Fidelity’s Virtual Assistant, which §5 treats as not described as AI. The page’s record status field reads “private”, so the move is provisional [V wave 43A]"
- **Find:** "at the next re-score. Chariot verification (A5) gains an adjacent-product note only."
- **Replace with:** "pending adjudication (P-B430105-01); AMBER stands until then. Chariot verification (A5) gains an adjacent-product note, with an open question on the MCP page’s “DAF eligibility, IRS status” lookups [V wave 43A]"
- **Find:** "and the flag stays shown as adjacent."
- **Replace with:** "and the flag stays shown as adjacent. However, §7a(4) also says evidence that would lower a flag must meet T1, and a product list for another product is not T1 evidence about Disbursements, so the downgrade is held as a pending adjudication note, not a rating change [V wave 43A]"
- **Find:** "was applied only in quadrant-v11-rescore.md (queue P-B430105-05)."
- **Replace with:** "is recorded only in the governing wave 21 corrections appendix of quadrant-v11-rescore.md, whose body still reads RED (queue P-B430105-05) [V wave 43A]"

### `research/mission-2026-11-14/b39n4-01-sector-join-all-sponsors.md`

- **Find:** "with NTEE T left inside society benefit [P vs F]."
- **Replace with:** "with NTEE T left inside society benefit [P vs F]. This is a one-parameter fit: adding a pure society-benefit mass equal to Fidelity’s FY2024 DAF-to-DAF lines (10.5% of its net) to t_a fits as well (0.122 against CY2024, 0.117 against CY2025), so the test measures the size of the society-benefit gap, not Fidelity’s mechanism. Across all three layers t_b is 0.11–0.13 [V wave 43A]"
- **Find:** "$77.91bn (plus_foreign)"
- **Replace with:** "$77.91bn (plus_foreign_sub5k; plus_foreign $75.99bn) [V wave 43A]"
- **Find:** "For the top 50, the full layer and plus_foreign are within 0.1 pt of each other: top-50 sub-$5,000 dollars are $1.92bn DAF-weighted, against a $77.9bn base."
- **Replace with:** "For the top 50, the full layer and plus_foreign differ by at most 0.4 pt (education 25.1 against 25.4, religion 13.9 against 13.5): top-50 sub-$5,000 dollars are $1.92bn DAF-weighted, against a $77.9bn base. [V wave 43A]"
- **Find:** "The 2025 Giving Report (CY2024; p.20 and the appendix)"
- **Replace with:** "The 2025 Giving Report (CY2024; chart on p.12, appendix table on p.21) [V wave 43A]"
- **Find:** "so Fidelity does not treat T as pass-through."
- **Replace with:** "so Fidelity does not treat T as pass-through. “Evidently” is too strong: a pure society-benefit mass of the same size (10.5% of Fidelity’s net) fits as well as t_b (0.122 / 0.117), and the best-fitting mass is 13–16%, so DAF-to-DAF is a sufficient size match, not an identified mechanism [V wave 43A]"
- **Find:** "periods are offset by six months (FYE June against calendar year)"
- **Replace with:** "periods differ: Fidelity’s FY2024 return (July 2023–June 2024) overlaps CY2024 by six months and CY2025 not at all, and the CY2024 split includes a $430m outlier grant that Fidelity removed only from its average grant size [V wave 43A]"
- **Find:** "and the appendix; the methodology is on p.19."
- **Replace with:** "and the appendix; the methodology is on p.19. The chart is on p.12 and the appendix table on p.21, not p.20; the 2025 methodology removes a $430m outlier grant from average grant size only, so the CY2024 sector split includes it [V wave 43A]"

### `research/mission-2026-11-14/direction-recipients-impact-matching.md`

- **Find:** "**On the strict BMF-only basis**, which drops the name-rule fills, the shares are 27.9 / 15.8 / 15.9 / 12.6 / 8.8 / 6.0 / 6.2 / 6.3% [C]."
- **Replace with:** "**On the strict BMF-only basis**, which drops the name-rule fills, the shares are 27.9 / 15.8 / 15.9 / 12.6 / 8.8 / 6.0 / 6.2 / 6.3% [C].<br><br>**All itemising sponsors** ([b39n4-01](b39n4-01-sector-join-all-sponsors.md); 1,379 sponsors, DAF-weighted, with foreign and sub-$5,000 grants, $101.01bn): education 23.0%, human services 14.6%, religion 14.1%, public-society benefit 13.2% (NTEE T 5.7 pts), health 9.2%, foreign grants (Schedule F) 3.1%, unclassified 5.9%. Keeping DAF-to-DAF grants, the basis comparable with sponsor-published splits, gives public-society benefit 23.7% and education 20.2% [V wave 43A]"
- **Find:** "evidently includes sponsor-to-sponsor grants [C/I]."
- **Replace with:** "is consistent with including sponsor-to-sponsor grants [C/I]. b39n4-01 §4 formalises the test: keeping DAF-to-DAF lines cuts the sum of absolute differences from 0.21–0.24 to 0.12–0.13 against the CY2024 and CY2025 splits, but a pure society-benefit mass of the same size fits as well, so the test shows the size of the gap, not the mechanism [V wave 43A]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "- **Where DAF money goes:** $77.34bn to ~174k recipients net of DAF-to-DAF; education 25.8%, human services 14.3% ([direction-recipients-impact-matching.md](direction-recipients-impact-matching.md))."
- **Replace with:** "- **Where DAF money goes:** $77.34bn to ~174k recipients net of DAF-to-DAF; education 25.8%, human services 14.3% at the top 50 ([direction-recipients-impact-matching.md](direction-recipients-impact-matching.md)). Across all 1,379 itemising sponsors, DAF-weighted with foreign and sub-$5,000 grants ($101.01bn, FY2023–24): education 23.0%, human services 14.6%, religion 14.1%, public-society benefit 13.2%, foreign grants 3.1%; on the basis comparable with sponsor-published splits (DAF-to-DAF kept), public-society benefit is 23.7% ([b39n4-01](b39n4-01-sector-join-all-sponsors.md)) [V wave 43A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.60 Sector shares across all sponsors; AI overlay rules clarified (validated, wave 43A)\n\n**Sector shares across all sponsors; AI overlay rules clarified** (validated, wave 43A). Extending the recipient-sector join to all 1,379 itemising DAFRC sponsors (FY2023–24) re-runs byte for byte. DAF-weighted, with foreign and sub-$5,000 grants ($101.01bn), education takes 23.0%, human services 14.6%, religion 14.1%, public-society benefit 13.2% and foreign grants 3.1%. Outside the top 50, education falls to 16.7% and unclassified rises to 11.4%. Filed foreign dollars (6.9%) are dominated by operating charities with tiny DAF books, such as World Vision (DAF weight 0.003–0.005). Keeping DAF-to-DAF grants matches Fidelity’s published split best (sum of differences 0.12–0.13, against 0.21–0.24), and the validator confirmed every Fidelity share. But a pure society-benefit mass of the same size fits as well, and the CY2025 comparison shares no months with the filing, so that basis is for sponsor comparisons only. Proposed methodology §7a–§7c confine the AI overlay to A1–A5 provider rows, never let a GREEN component offset an AMBER, and define “first GREEN”; none of 137 ratings qualifies. Chariot Disbursements stays AMBER pending adjudication, NCF moves to AMBER (low) provisionally, and Benevity’s stale RED labels are annotated (repo [`validation-wave43a-report.md`](mission-2026-11-14/validation-wave43a-report.md)) [V wave 43A]\n\n---\n\n## Source register"
- **Find:** "- **RED (provisional):** Benevity Match Assurance."
- **Replace with:** "- **RED (provisional):** Benevity Match Assurance. Superseded: wave 21 moved it to AMBER (provisional), so no provider is RED (repo [`quadrant-v11-rescore.md`](mission-2026-11-14/quadrant-v11-rescore.md), Validation corrections (wave 21)) [V wave 43A]"
- **Find:** "- **RED (provisional):** Benevity. Its AI auto-submits match requests with no documented approval step."
- **Replace with:** "- **RED (provisional):** Benevity. Its AI auto-submits match requests with no documented approval step. Superseded: wave 21 moved it to AMBER (provisional), because first-party pages keep human approval by default [V wave 43A]"

Every Find above was checked by script (`v43a/tools/parse_corr.py`): each occurs exactly once in its file, alone and when all 29 items are applied in order. No value contains a straight double quote, and every Replace except the §11.60 insertion ends “[V wave 43A]”.
