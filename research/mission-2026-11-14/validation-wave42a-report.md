# Validation wave 42A: GREEN AI overlays and realised tail fees

**Date:** 2026-11-20 · **Validator:** independent-validation-agent-wave42a · **Register:** [`validation-register-wave42a.csv`](../../data/mission-2026-11-14/validation-register-wave42a.csv) (V42A-01 to V42A-34)

**Studies checked**
1. [`b43n25-01-green-overlay-validation.md`](b43n25-01-green-overlay-validation.md) and [`green-overlay-validation-2026-11-20.csv`](../../data/mission-2026-11-14/green-overlay-validation-2026-11-20.csv): second reading of the four provisional GREEN AI overlays, with 25 proposed corrections.
2. [`b4427b-0405-realised-tail-fees-all.md`](b4427b-0405-realised-tail-fees-all.md), [`tail-realised-fees-all-2026-11-20.csv`](../../data/mission-2026-11-14/tail-realised-fees-all-2026-11-20.csv) and `scripts/mission_tail_realised_fees_all.py` (task `run`): realised admin fees for all 641 tail CFs and 29 non-CF census sponsors.

**Method**
- **Study 1.** Re-read methodology §1 and §7 ([evidence-quadrant-methodology.md](evidence-quadrant-methodology.md)), the census, the v1.0 calibration table and the v1.1 §6 adjudication.
  - robots.txt was checked on 2026-11-20 before any fetch:
    - supporthub.smartsimple.com: 200, `*` allows `/hc/en-us/articles/`;
    - www.fluxx.io: 200, ClaudeBot `Allow: /`;
    - webfiles-sc1.blackbaud.com: 404, no rules;
    - givebutter.com: 200, empty `Disallow:`;
    - www.yourcause.com: 200, only PDFs disallowed.
  - 11 first-party pages were re-fetched with UA `research-script/1.0` and every CSV quote from those pages was matched by script.
  - Each Find was counted, alone and applied in order.
- **Study 2.**
  - Task `run` was re-run from the q4405 cache into scratch (`v42a/`).
  - Disclosure shares, medians, bands, Spearman, the pool, the bootstrap and the whole-tail scenarios were recomputed independently from the CSV.
  - 10 CFs' and 2 non-CFs' fee lines were read from the XML.
  - 4 XMLs were re-fetched from the GivingTuesday mirror (robots.txt 404) and are byte-identical to the cache.
- **Not used:** crt.sh, certspotter and sec.gov. There was no outreach and no login. The user agent was never changed.
- **Repo files written:** only this report and the register. Nothing was committed.

## 1. Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| 1. GREEN overlay validation | 17 (V42A-01 to 17) | 14 | 3 | 0 | 0 |
| 2. Realised tail fees, all | 17 (V42A-18 to 34) | 11 | 6 | 0 | 0 |
| **Total** | **34** | **25** | **9** | **0** | **0** |

**GREEN corrections tally (25 items):** 17 accept, 6 modify and 2 reject.

## 2. Findings: study 1 (GREEN overlays)

**The criteria framing is right (V42A-01).**
- §7 has one GREEN sentence: "controls documented, including flag-only and authority separation".
- Treating human review, no automated decision, data handling, model disclosure and opt-in as supplementary (S1–S5) is correct.
- *Challenge.* The study then leads the Givebutter downgrade with default-on and cannot-disable terms, which by its own framing are S2 and S5. Under §7 the binding reasons are two:
  - G2 fails: stretch goals "automatically increase as you raise more", and suggested amounts are "automatically matched".
  - G1 is only partly met: AI fraud review has undocumented limits.

**Quotes and dates re-fetched (V42A-02 to 12, 16).** All 45 quotes from the 11 re-fetched pages match.

| Source | Date found | Confirmed |
|---|---|---|
| SmartSimple Overview | 2026-06-22 | the full set of quotes |
| SmartSimple Configure | 2026-07-07 | the FAQ, including "from within the Foundant application (GLM/SLM, CommunitySuite, GivingData, SmartSimple)" and "© Copyright 2025 Foundant Technologies" |
| SmartSimple release notes | 2026-11-02 | the Azure OpenAI line |
| Fluxx | `datePublished` 2026-07-29, `dateModified` 2026-08-03 | all quotes; no audit statement on the page |
| Blackbaud opt-in | undated | "before January 7, 2026 … will remain enabled"; "external connectors access to your data"; no retraining |
| YourCause post | 2026-07-16 | the FAQ |
| Givebutter AI Addendum | effective 2026-10-01 | §2 providers, §3 "may be used for AI model training", §8.1, §8.2, §8.3 and §8.4 verbatim |
| Givebutter privacy policy | effective 2026-10-01 | §6 fraud review and connector metadata |
| Givebutter recap | byline 2026-10-02 (event 2026-10-01) | the FAQ, including "optional and only used when you choose to use them" |

- **Minor attribution.** The study's §3.1 table cites the Overview URL for two FAQ quotes that are on the Configure article (G3 and S3). The CSV notes attribute them correctly.
- **Counterpoint not cited.** Givebutter's privacy policy also says it "does not collect, use, or sell personal data for the purpose of training large language models". The training risk sits with third-party infrastructure, internal-tool and fraud-tool providers.

**The YourCause opt-in nuance is partly right (V42A-07).**
- The grandfathering line is accurate, and so is the external-connector caveat.
- But the GrantsConnect summaries help says the feature "is only available for organizations with Blackbaud AI enabled in GrantsConnect. Contact your Account Manager or CSM to enable it."
- The YourCause FAQ says the features need the opt-in "before they can be enabled".
- So grandfathering keeps the Blackbaud-wide switch on, but it does not by itself switch summaries on. GREEN (provisional) stands. Items 2, 10 and 18 are modified to say this.

**The Givebutter downgrade is confirmed (V42A-13).**
- AMBER is right on the binding grounds: it is not flag-only, fraud-review limits are undocumented, and approval of content still remains.
- RED is not met: "Givebutter Magic does not process payments".

**No first GREEN under §7 (V42A-14).** Confirmed:
- v1.0 gave Fidelity Charitable **GREEN** and gave Ren, Ren RDE, RCF and AEF **GREEN / none**;
- v1.1 §6 says "No provider earns GREEN";
- A1–A5 do not list SmartSimple, Fluxx, YourCause or Givebutter.

**The Foundant entity scope is partly right (V42A-15).**
- The FAQ shows a Foundant-wide service architecture: data is processed "within Foundant cloud infrastructure under Foundant-owned accounts" and reached from the GLM/SLM, CommunitySuite and GivingData backends.
- It does not show the feature live in CommunitySuite or in any CF's DAF workflow. "The evidence does reach Foundant the vendor" is therefore a little strong.
- AMBER for Foundant stands, because Fia's limits are undocumented. Item 3 is modified.

**The 25 corrections (V42A-17).** Every Find occurs exactly once, alone and in order. Two are rejected:
- **Item 23** edits industry report line 865. That line is in §11.25, a wave 28 history paragraph. Its content goes into the new §11.57 instead.
- **Item 17** writes text and a tag into the census CSV's `source_date` and `accessed` columns. The date fix goes into item 13's note and the census source register (S39) instead.

### Accept / modify / reject

| # | File | Find (start) | Decision | Reason |
|---|---|---|---|---|
| 1 | census md | These are the first GREEN-eligible readings… | accept | Supported (V42A-14) |
| 2 | census md | These are complimentary once the customer opts in. | modify | Add GrantsConnect vendor-enabling step; full stop before tag |
| 3 | census md | Under the entity scope rule (§7)… | modify | FAQ shows a Foundant-wide service, not use in CommunitySuite DAF workflows |
| 4 | census md | **Givebutter Magic** (2026-10-01) is the strongest-documented… | modify | Lead with binding §7 reasons; fix run-on into next sentence |
| 5 | census md | \| approval before send or publish; … training limits | accept | Supported |
| 6 | census md | \| GREEN (provisional) \| 4 | accept | 4 → 3 |
| 7 | census md | \| AMBER \| 9 | accept | 9 → 10 |
| 8 | census md | All four GREENs are provisional | accept | Supported |
| 9 | census md | (P-B43N25-01). | accept | Supported |
| 10 | census md | \| Opt-in, off by default \| … | modify | Grandfathering wording, as item 2 |
| 11 | census md | Givebutter (third-party models; …) | accept | Privacy §6 wording verbatim |
| 12 | products CSV | …('starts at $29/month'),GREEN (provisional) | accept | Supported |
| 13 | products CSV | Documented approval-before-send… | modify | Lead with flag-only failure; carries recap date 2026-10-02 |
| 14 | products CSV | connectors need team authorisation… | accept | §8.1, §8.2, §8.4 verbatim |
| 15 | products CSV | some features send data to external providers | accept | §2, §3 and Privacy §6 |
| 16 | products CSV | no: 'Givebutter Magic does not process payments' | accept | Privacy §6 |
| 17 | products CSV | 2026-10-01,2026-11-15 | reject | Puts text and a tag in the date columns; date moved to item 13 and census S39 |
| 18 | products CSV | yes: generative AI off until an org admin opts in… | modify | Add vendor-enabling step; no commas |
| 19 | products CSV | Opt-in default off, no-training… | accept | Supported |
| 20 | products CSV | admin field control; untested; not in a DAF money path | accept | FAQ wording supports "configured from" |
| 21 | products CSV | Beta with controls claimed… | accept | Supported |
| 22 | products CSV | Documented opt-in, field control… | accept | Dates confirmed |
| 23 | industry report | Givebutter Magic is a GREEN/AMBER boundary case. | reject | Line 865 is inside §11.25 (wave 28 history); content moved to §11.57 |
| 24 | strategic-synthesis | Givebutter's stretch goals… | accept | Leads with the binding reason |
| 25 | strategic-synthesis | \| Givebutter AI overlay \| GREEN \| … | accept | Wave-correction table; keeps the wave 28 history in brackets |

## 3. Findings: study 2 (realised tail fees)

**Reproduction is exact (V42A-18, 19).**
- `run` regenerates the 670-row CSV with identical content (246,047 bytes), and its stdout is identical to `run2.md`.
- The returns are 2,657 = 124 cache + 2,533 mirror, with 0 missing, 0 parse failures and 0 fallbacks.
- The Licking quote check reports "verified".

**Recomputed statistics agree (V42A-20, 22–24, 32).**

| Statistic | Recomputed |
|---|---|
| Any fee shown | 292 (45.6%) |
| Internal fee | 47 (7.3%) |
| Agency / unknown / none | 21 / 224 / 349 |
| Internal-rate median | 101.6 bps (IQR 70.6–136.2; n = 47) |
| Complete-capture band medians | 134.25 / 111.7 / 72.7 |
| Spearman ρ | −0.435 (tie-averaged ranks) |
| Central | $49.40m (80.97 bps) |
| Low / high | $38.5m / $61.5m |
| Independent bootstrap (seed 20261120) | $43.2m–$58.0m |
| Independent bootstrap (seeds 1 and 2) | $41.8m–$58.0m and $42.2m–$57.9m |
| Whole tail (non-CFs nil / full / disclosure ratio 0.2915) | 49.4 / 74.3 / 56.7 |
| Non-CF test | 6/29 vs 22/31; Part V 95 vs 116 bps |

**Minor errors in the study text.**
- **§1.3 table, rule 5 (V42A-21).** It should read 19 agency-worded CFs. The other 2 agency CFs come from rule 1, and as printed the table sums to 643.
- **§4.2 fee lines (V42A-31).** They are in sorted string order, not FY2022–24 order, for all six non-CFs. The XML gives the order:
  - BSA $676,349 / $1,459,026 / $3,010,049;
  - UMF Louisiana $887,808 / $1,098,101 / $1,120,165.
  - The amounts and rates (184.5 and 214.4 bps) are right.
- **Non-CF tail DAF assets (V42A-33).** These are $3,078.8m in the tail CSV, not $3,079.4m. No scenario changes.
- **"About a third" (§3.5).** The flat figures exceed the size-banded central by 27% ($62.9m) and 34% ($66.4m).

**XML spot-checks (V42A-28 to 30)** all match the CSV to the dollar.

| CF | What the XML shows |
|---|---|
| Wabash Valley, FY ending 2024-09-30 | Part XI 2d "ADMINISTRATIVE FEES 1,221,891.", mirrored in Part XII 2d and equal to Part V line 1f; 130.6 bps |
| Coastal Bend, FY2023 | income 1,165,161 against expense 1,058,267 (9.2% apart); 88.3 bps |
| Hutchinson, Montrose, Greene, Central Florida, Lehigh Valley and Door County | all match |

At Montrose only $10,108 of the $216,772 is worded "Donor Advised"; most of it is "MCF Admin Fee".

**Interpretation challenges.**
1. **"Realised" is mostly imputed (V42A-25).**
   - The 41 own complete-capture rates contribute $3.03m of the $49.40m central.
   - $46.37m (94%) is band-median imputation. $23.77m of that falls on the 349 CFs with no fee line, and $2.20m on the agency-classed 21.
   - All-fund rates are a floor-type basis for DAF fees, as b4427b-b4501 said. So the schedule-based $89.9m remains a list-price ceiling and is not refuted; the CF DAF fee pool lies between about $49m and $90m.
2. **Rule 4 is the pivot (V42A-27).**
   - 7 of the 13 top-band complete-capture CFs come from the matched-expense rule.
   - 9 of the 19 matches are 1.4%–9.2% apart.
   - Beaver County's matched line is "TRUST MANAGEMENT FEES".
   - Excluding the 19 lowers the central to **$32.2m** (top-band median 38.9 bps). Excluding the 11 rule-3 CFs gives $48.1m.
3. **Unflagged partial captures (V42A-26).**
   - Five internal CFs with no Part V figure realise under 30 bps: Aspen 2.8, two "Community Foundation of …" at 8.7 and 21.3, Gulf Coast 16.1 and Central Montana 25.6.
   - Treating them as partial raises the central to **$56.8m**, above the bootstrap interval.
   - The flag itself is mechanical. It sets aside one CF at 154.6 bps, which is above its band median of 134.2, because that CF's Part V rate is 979.5 bps.
4. **The sponsor-level sweep (V42A-21).** Once a CF is classed internal, every non-agency fee line counts as internal. Examples are Door County's "campaign" and "expanded services" fee income, and a "REGISTRATION FEE INCOME" line.
5. **The non-CF scenario at the full CF rate ($74.3m) is an upper scenario,** because none of the six non-CF fee lines can be tied to DAFs.

**Fee-pool propagation (V42A-34).**
- Passages found:
  - b4501-04 §0 and §2.3;
  - direction-long-tail-sponsors (§0 row and §6 bullet);
  - strategic-synthesis line 558 (section "(a) What changed in syntheses A–G");
  - FINAL-STATUS lines 31 and 185;
  - b4427b-b4501 §0 and §3.
- strategic-synthesis §0 has no fee-pool figure.
- The industry report carries the pool only in §11.36 and §11.55. Those are history paragraphs and are left unedited; §11.57 carries the update.
- The corrections below keep the schedule figures as ceilings and add the realised figures as the central.

## Exact corrections

### `research/mission-2026-11-14/direction-ai-product-census.md`

- **Find:** "These are the first GREEN-eligible readings in the repo, marked provisional."
- **Replace with:** "These are the first GREEN-eligible readings of vendor AI products in the repo, marked provisional. None is the first GREEN under §7: none is an A1–A5 provider, and v1.0 calibration had already labelled Fidelity Charitable GREEN and Ren/RCF/AEF “GREEN / none” before v1.1 withdrew both [V wave 42A]"
- **Find:** "These are complimentary once the customer opts in."
- **Replace with:** "These are complimentary once the customer opts in. The Blackbaud-wide default is not universal: organisations that “used generative AI before January 7, 2026” stay enabled, and enabling generative AI also enables “external connectors access to your data” unless an admin clears that box. GrantsConnect summaries still have to be switched on by Blackbaud (“Contact your Account Manager or CSM to enable it”). [V wave 42A]"
- **Find:** "Under the entity scope rule (§7), they do not change any sponsor's overlay, or the Foundant overlay (AMBER, Fia beta), even though SmartSimple is in the Foundant family."
- **Replace with:** "Under the entity scope rule (§7), they do not change any sponsor's overlay. SmartSimple's own FAQ says the Application Analysis service takes data “from within the Foundant application (GLM/SLM, CommunitySuite, GivingData, SmartSimple)”, so it is a Foundant-wide service, but no source shows it in use in a community foundation's DAF workflow. The Foundant overlay stays AMBER because Fia's agents and policy engine have undocumented limits, and §7 has no rule for rating a provider from one GREEN component [V wave 42A]"
- **Find:** "**Givebutter Magic** (2026-10-01) is the strongest-documented fundraising row."
- **Replace with:** "**Givebutter Magic** (2026-10-01) is AMBER, not GREEN. Its stretch goals “automatically increase as you raise more” and its suggested amounts are “automatically matched”, so the AI is not flag-only, and its privacy policy says AI tools “review transactions, detect fraud, and assess risk” with undocumented limits. Its AI Addendum (effective 2026-10-01) also says “AI Features are enabled by default”, that AI-assisted fraud detection and Receipt Matching “cannot be disabled”, and that data captured by third-party AI infrastructure services “may be used for AI model training”. [V wave 42A]"
- **Find:** "| approval before send or publish; read-only connectors; training limits | free; Plus $29/month | **GREEN (provisional)**"
- **Replace with:** "| approval before send or publish; read-only connectors; AI on by default; fraud and receipt AI cannot be disabled | free; Plus $29/month | **AMBER** [V wave 42A]"
- **Find:** "| GREEN (provisional) | 4"
- **Replace with:** "| GREEN (provisional) | 3 [V wave 42A]"
- **Find:** "| AMBER | 9"
- **Replace with:** "| AMBER | 10 [V wave 42A]"
- **Find:** "All four GREENs are provisional"
- **Replace with:** "Three GREENs remain, all provisional; Givebutter Magic moved to AMBER [V wave 42A]"
- **Find:** "(P-B43N25-01)."
- **Replace with:** "(P-B43N25-01). Validated 2026-11-20: SmartSimple, Fluxx Finn and YourCause hold as GREEN (provisional), and none is the first GREEN under §7 [V wave 42A]"
- **Find:** "| Opt-in, off by default | Blackbaud (global generative-AI switch); Fluxx Finn; SmartSimple (vendor must enable) | Bloomerang; Salesforce"
- **Replace with:** "| Opt-in, off by default | Blackbaud (global generative-AI switch; organisations that used generative AI before 2026-01-07 stay enabled; GrantsConnect summaries enabled by Blackbaud); Fluxx Finn; SmartSimple (vendor must enable) | Bloomerang; Salesforce; Givebutter (AI on by default; fraud and receipt AI cannot be disabled) [V wave 42A]"
- **Find:** "Givebutter (third-party models; own models de-identified only)"
- **Replace with:** "Givebutter (third-party models; own models de-identified only; observability and fraud-tool data “may be used for AI model training”) [V wave 42A]"
- **Find:** "| opt-in, off by default; no retraining; humans decide"
- **Replace with:** "| opt-in, off by default (organisations using generative AI before 2026-01-07 stay enabled; summaries enabled by Blackbaud on request); no retraining; humans decide [V wave 42A]"
- **Find:** "| S39 | Givebutter Spread 2026 recap | vendor blog | 2026-10-01"
- **Replace with:** "| S39 | Givebutter Spread 2026 recap | vendor blog | 2026-10-02 (event 2026-10-01) [V wave 42A]"

### `data/mission-2026-11-14/philanthropy-ai-products-2026.csv`

- **Find:** "most features free; AI custom reports need Givebutter Plus ('starts at $29/month'),GREEN (provisional)"
- **Replace with:** "most features free; AI custom reports need Givebutter Plus ('starts at $29/month'),AMBER [V wave 42A]"
- **Find:** "Documented approval-before-send, no payment processing, read-only connectors, training limits; untested"
- **Replace with:** "Not flag-only: stretch goals auto-increase and suggested amounts are matched automatically; AI transaction review (fraud and risk) has undocumented limits. Approval before send or publish, no payment processing and read-only connectors are documented. Supplementary: AI features are on by default and fraud-detection and Receipt Matching AI cannot be disabled. Recap post dated 2026-10-02 (event 2026-10-01) [V wave 42A]"
- **Find:** "connectors need team authorisation; contact summaries can be turned off"
- **Replace with:** "AI Features “enabled by default” (AI Addendum 8.1); fraud-detection and Receipt Matching AI “cannot be disabled” (8.2); connectors need affirmative opt-in (8.4); contact summaries can be turned off [V wave 42A]"
- **Find:** "some features send data to external providers"
- **Replace with:** "some features send data to external providers (Anthropic; Google; OpenAI); observability-log and fraud-tool data “may be used for AI model training” (AI Addendum s3; Privacy s6) [V wave 42A]"
- **Find:** "no: 'Givebutter Magic does not process payments'"
- **Replace with:** "no: 'Givebutter Magic does not process payments'; platform AI fraud tools review transactions (Privacy s6) [V wave 42A]"
- **Find:** "yes: generative AI off until an org admin opts in; opt-out 'takes effect immediately'"
- **Replace with:** "yes for organisations new to it: generative AI off until an org admin opts in; organisations that used generative AI before 2026-01-07 “remain enabled”; GrantsConnect summaries are also enabled through the account manager or CSM; opt-in also enables external-connector access unless cleared; opt-out 'takes effect immediately' [V wave 42A]"
- **Find:** "Opt-in default off, no-training, human-decision statements documented first-party; summaries only"
- **Replace with:** "Opt-in default off, no-training, human-decision statements documented first-party; summaries only; re-confirmed GREEN (provisional) by a second reader 2026-11-20 with an opt-in grandfathering caveat [V wave 42A]"
- **Find:** "admin field control; untested; not in a DAF money path"
- **Replace with:** "admin field control; untested; not in a DAF money path; re-confirmed 2026-11-20; the same service is configured from Foundant GLM/SLM, CommunitySuite and GivingData (Configure article FAQ, 2026-07-07) but the Foundant overlay stays AMBER [V wave 42A]"
- **Find:** "Beta with controls claimed but not documented (v11 consensus); foundant.com barred to this agent by robots"
- **Replace with:** "Beta with controls claimed but not documented (v11 consensus); foundant.com barred to this agent by robots; Foundant's GREEN-eligible Application Analysis (AIP12) is a separate feature and does not document Fia's limits so AMBER stands [V wave 42A]"
- **Find:** "Documented opt-in, field control, no-training and human-decision statements; flags only; untested"
- **Replace with:** "Documented opt-in, field control, no-training and human-decision statements; flags only; untested; re-confirmed 2026-11-20 on the product page FAQ (published 2026-07-29); the Fluxx MCP bundled with Finn stays AMBER (AIP14) [V wave 42A]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "Givebutter's stretch goals and suggested amounts change without per-action approval, so it is a GREEN/AMBER boundary case."
- **Replace with:** "Givebutter is AMBER: its stretch goals and suggested amounts change without per-action approval, its AI features are on by default, and its fraud-detection and Receipt Matching AI cannot be disabled [V wave 42A]"
- **Find:** "| Givebutter AI overlay | GREEN | **GREEN/AMBER boundary**"
- **Replace with:** "| Givebutter AI overlay | GREEN | **AMBER** (was GREEN/AMBER boundary in wave 28) [V wave 42A]"
- **Find:** "The CF pool is therefore about $63m–$90m, and the whole-tail $138m still depends on untested non-CF charging (b4427b-b4501 §3) [V wave 41B]"
- **Replace with:** "The CF pool is therefore about $63m–$90m, and the whole-tail $138m still depends on untested non-CF charging (b4427b-b4501 §3) [V wave 41B]. Superseded on realised fees: across all 641 tail CFs, size-banded realised all-fund rates give a CF pool of about $49m ($38.5m–$61.5m), 94% of it imputed from band medians, so the flat $63m overstated it by about a quarter. Only 6 of 29 sampled non-CFs show a fee line and none is worded as an internal fund fee, so the whole tail realises about $49m–$74m (range $38.5m–$92.5m). The $90m and $138m schedule figures are list-price ceilings, not estimates of fees collected (b4427b-0405) [V wave 42A]"

### `research/mission-2026-11-14/b43n25-01-green-overlay-validation.md`

- **Find:** "and opting in also opens external-connector access."
- **Replace with:** "and opting in also opens external-connector access. GrantsConnect summaries still need Blackbaud to enable them (“Contact your Account Manager or CSM to enable it”), so grandfathering does not by itself switch them on [V wave 42A]"
- **Find:** "AI transaction review has undocumented limits."
- **Replace with:** "AI transaction review has undocumented limits. Only the flag-only failure and the undocumented review limits are binding under §7; the default-on and cannot-disable terms are supplementary (S2, S5) [V wave 42A]"

### `research/mission-2026-11-14/b4427b-0405-realised-tail-fees-all.md`

- **Find:** "Hard floor (only the 47 internal disclosers, at their own rate): $3.2m."
- **Replace with:** "Hard floor (only the 47 internal disclosers, at their own rate): $3.2m. Own observed rates supply $3.0m of the central; $46.4m (94%) is band-median imputation, $23.8m of it on the 349 CFs that show no fee line [V wave 42A]"
- **Find:** "and its non-CF half has no realised evidence of CF-type charging [C; I]."
- **Replace with:** "and its non-CF half has no realised evidence of CF-type charging [C; I]. The realised figures use all-fund rates, a floor-type basis for DAF fees, so the schedule CF figure ($89.9m) stays a list-price ceiling rather than being refuted [V wave 42A]"
- **Find:** "- **Non-CF scenarios** on $3,079.4m"
- **Replace with:** "- **Non-CF scenarios** on $3,078.8m (the tail CSV total for 599 non-CF sponsors) [V wave 42A]"
- **Find:** "property, rental | agency | 21"
- **Replace with:** "property, rental | agency | 19 (21 with the 2 agency readings under rule 1) [V wave 42A]"
- **Find:** "The pool's central case sets their own rates aside and gives them their band median instead."
- **Replace with:** "The pool's central case sets their own rates aside and gives them their band median instead. The flag is mechanical: the “Community Foundation of the …” rate (154.6 bps) is above its band median (134.2) and is set aside only because its Part V rate (979.5 bps) is implausible, as is Door County's (429.0) [V wave 42A]"
- **Find:** "both overstate the size-banded central by about a third."
- **Replace with:** "overstate the size-banded central by 27% and 34% respectively [V wave 42A]"
- **Find:** "(non-CF tail DAF assets $3,079.4m)"
- **Replace with:** "(non-CF tail DAF assets $3,078.8m) [V wave 42A]"
- **Find:** "$1,459,026 / $3,010,049 / $676,349"
- **Replace with:** "$676,349 / $1,459,026 / $3,010,049 (FY2022 / FY2023 / FY2024) [V wave 42A]"
- **Find:** "$1,098,101 / $1,120,165 / $887,808"
- **Replace with:** "$887,808 / $1,098,101 / $1,120,165 [V wave 42A]"
- **Find:** "$117,062 / $211,824 / $99,325"
- **Replace with:** "$99,325 / $117,062 / $211,824 [V wave 42A]"
- **Find:** "$120,145 / $121,681 / $129,852"
- **Replace with:** "$121,681 / $129,852 / $120,145 [V wave 42A]"
- **Find:** "$172,666 / $37,412 / $550"
- **Replace with:** "$172,666 / $550 / $37,412 [V wave 42A]"
- **Find:** "$2,797 / $6,549 / $6,843"
- **Replace with:** "$6,843 / $6,549 / $2,797 [V wave 42A]"
- **Find:** "only EITC/tax-credit wording is screened."
- **Replace with:** "only EITC/tax-credit wording is screened. Nine of the 19 matches are approximate (the expense is 1.4%–9.2% off the fee), and Beaver County's matched line is “TRUST MANAGEMENT FEES”, which may be a trustee pass-through. Excluding all 19 lowers the central to $32.2m (top-band median 38.9 bps), so rule 4 is the pivot of the central [V wave 42A]"
- **Find:** "Captures that are partial but unflagged remain in the band rates, which biases them down."
- **Replace with:** "Captures that are partial but unflagged remain in the band rates, which biases them down. Five unflagged internal CFs with no Part V figure realise under 30 bps (Aspen 2.8; Gulf Coast 16.1; Central Montana 25.6; two others at 8.7 and 21.3); treating them as partial raises the central to $56.8m [V wave 42A]"

### `research/mission-2026-11-14/b4427b-b4501-npt-screen-and-realised-fees.md`

- **Find:** "the CF pool would be **$62.9m** ($10.7m–$79.0m across the observed internal-fee rates) [C on that assumption]."
- **Replace with:** "the CF pool would be **$62.9m** ($10.7m–$79.0m across the observed internal-fee rates) [C on that assumption]. Superseded by b4427b-0405: with size bands across all 641 tail CFs the realised all-fund central is $49.4m ($38.5m–$61.5m) [V wave 42A]"
- **Find:** "Together, the two bracket the CF pool at roughly **$63m–$90m**."
- **Replace with:** "Together, the two bracket the CF pool at roughly **$63m–$90m**. Superseded: with size bands across all 641 tail CFs the realised all-fund central is $49.4m ($38.5m–$61.5m), so the flat $62.9m overstated it by about a quarter; the CF pool now spans about $49m (realised, floor-type) to $90m (schedule, ceiling-type) (b4427b-0405) [V wave 42A]"
- **Find:** "is not tested here and remains the unevidenced part** (P-B4427B4501-05)."
- **Replace with:** "is not tested here and remains the unevidenced part** (P-B4427B4501-05). Tested in b4427b-0405: 6 of 29 sampled non-CFs show any fee line and none is worded as an internal fund fee, so the whole tail realises about $49m–$74m central, not $138m [V wave 42A]"

### `research/mission-2026-11-14/b4501-04-tail-fee-pool-revision.md`

- **Find:** "| **Tail admin-fee pool** | **Central about $138m a year; range about $76m–$184m** [C on the assumptions in §1.3]."
- **Replace with:** "| **Tail admin-fee pool** | **Central about $138m a year; range about $76m–$184m** [C on the assumptions in §1.3]. *Superseded 2026-11-20 as a fee estimate:* on realised all-fund rates the tail CF pool is $49.4m ($38.5m–$61.5m) and the whole tail $49.4m–$74.3m central ($38.5m–$92.5m) depending on non-CF charging; the published-schedule figures here remain list-price ceilings ([b4427b-0405-realised-tail-fees-all.md](b4427b-0405-realised-tail-fees-all.md)) [V wave 42A]"
- **Find:** "**Headline: central about $138m; range about $76m–$184m** (bold cells)."
- **Replace with:** "**Headline: central about $138m; range about $76m–$184m** (bold cells). These are list-price figures; realised all-fund rates give $49.4m for CFs and $49.4m–$74.3m for the whole tail (b4427b-0405) [V wave 42A]"

### `research/mission-2026-11-14/direction-long-tail-sponsors.md`

- **Find:** "Its admin-fee pool is small: about $138m a year if every tail sponsor charged like the median of the published tail-CF schedules, or about $90m if only CFs charge, within about $76m–$184m."
- **Replace with:** "Its admin-fee pool is small. On realised all-fund fee rates tail CFs collect about $49m a year ($38.5m–$61.5m), and the whole tail about $49m–$74m depending on whether non-CF sponsors charge (range $38.5m–$92.5m). Published tail-CF schedules give list-price ceilings of about $90m (CFs only) and $138m (whole tail). [V wave 42A]"
- **Find:** "Non-CF charging stays unevidenced (b4427b-b4501 §3) [V wave 41B]"
- **Replace with:** "Non-CF charging stays unevidenced (b4427b-b4501 §3) [V wave 41B]. Extended to all 641 tail CFs with size bands, realised all-fund rates give a CF pool of $49.4m (81 bps; $38.5m–$61.5m; bootstrap 90% $42.9m–$58.0m), 94% of it imputed from band medians. Only 6 of 29 sampled non-CFs show any fee line and none is worded as an internal fund fee, so the whole tail realises $49.4m–$74.3m central (range $38.5m–$92.5m) against the schedule-based $138m (b4427b-0405) [V wave 42A]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "The community-foundation pool is about $63–90m. The non-CF step is untested."
- **Replace with:** "The community-foundation pool is about $49m on realised all-fund rates across all 641 tail CFs ($38.5m–$61.5m), with $90m as a published-schedule ceiling. Non-CFs rarely show fees (6 of 29 sampled; none worded as an internal fund fee), so the whole tail realises about $49m–$74m, not $138m [V wave 42A]"
- **Find:** "giving a floor-type CF pool of about $63m; non-CF charging is untested [V wave 41B]"
- **Replace with:** "giving a floor-type CF pool of about $63m; non-CF charging is untested [V wave 41B]. Superseded: size-banded realised all-fund rates across all 641 tail CFs give $49.4m ($38.5m–$61.5m; 94% imputed from band medians), and the whole tail $49.4m–$74.3m central ($38.5m–$92.5m) because only 6 of 29 sampled non-CFs show any fee line (b4427b-0405) [V wave 42A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.57 AI GREEN overlays rechecked; realised tail fees (validated, wave 42A)\n\n**AI GREEN overlays rechecked; realised tail fees** (validated, wave 42A). A second reading of the four provisional GREEN vendor AI products, with pages re-fetched by the validator, holds SmartSimple AI Application Analysis, Fluxx Finn and YourCause AI Application Summaries at GREEN (provisional). Givebutter Magic moves to AMBER: its stretch goals and suggested amounts change automatically, so it is not flag-only, and its AI fraud review has undocumented limits. Its AI Addendum also turns AI features on by default. None of the three GREENs is an A1–A5 provider, so the v1.1 overlay still has no GREEN provider. Blackbaud organisations that used generative AI before 7 January 2026 stay enabled. Form 990 admin fees across all 641 tail community foundations re-run exactly. Size-banded realised all-fund rates give a CF pool of $49.4m a year ($38.5m–$61.5m), 94% of it imputed from band medians. Only 6 of 29 sampled non-CF sponsors show any fee line, and none is worded as an internal fund fee. The whole tail therefore realises about $49m–$74m, against the schedule-based $138m, which remains a list-price ceiling. [V wave 42A]\n\n---\n\n## Source register"
