# Methodology §7 clarification: AI overlay scope, mixed components and “first GREEN” (P-B4301-05)

**Date:** 2026-11-20. Task ID b4301-05. This task proposes edits; it does not make them. Nothing was committed or pushed, and no existing file was changed. The proposed edits are in [Exact corrections](#exact-corrections).

**Files written**
- This document.
- [`overlay-rule-test-2026-11-20.csv`](../../data/mission-2026-11-14/overlay-rule-test-2026-11-20.csv): 137 rows, one per existing overlay rating, with the outcome under the proposed rules.
- [`queue-proposals-b4301-05.csv`](../../data/mission-2026-11-14/queue-proposals-b4301-05.csv): 5 rows.
- `scripts/mission_b4301_05_overlay_rule_test.py`: builds the CSV and prints the counts (`python3 scripts/mission_b4301_05_overlay_rule_test.py .`).

**The gap.** Methodology [§7](evidence-quadrant-methodology.md) defines GREEN, AMBER and RED in three sentences. It does not say:
- whether the overlay applies to vendor products outside areas A1–A5;
- how to combine components rated differently;
- what a “first GREEN” is.

The GREEN validation ([b43n25-01](b43n25-01-green-overlay-validation.md) §4, §5, §6) had to infer an answer to each, marked [I]. Wave 42A ([report](validation-wave42a-report.md), V42A-14, V42A-15) confirmed those inferences but noted that “§7 has no rule for rating a provider from one GREEN component”.

## 1. Results in brief

| Point | Proposed rule (short form) | Ratings that change |
|---|---|---|
| (a) Vendor products outside A1–A5 | The overlay is a flag on A1–A5 provider rows only. Other products get **product-level readings**. A reading enters a provider row only as a component with a documented tie. An AMBER or RED component counts on any of four ties. A GREEN component counts only when it is live in the scored offering. A component that the source confines to another product is shown as “adjacent”, not counted. | **Chariot Disbursements (A2): AMBER → None (watch: agent-capable API) [adjacent product AMBER]**, pending adjudication (P-B430105-01); AMBER stands until then. Chariot verification (A5) gains an adjacent-product note, with an open question on the MCP page’s “DAF eligibility, IRS status” lookups [V wave 43A] |
| (b) One GREEN component, one AMBER | The provider takes its most severe counted component. It is GREEN only if every counted component is GREEN. A GREEN component never offsets an AMBER. Write the split: “AMBER (mixed: GREEN …; AMBER …)”. | None. No A1–A5 provider has a counted GREEN component, so no row is “mixed” today. Foundant would become “AMBER (mixed)” if Application Analysis were shown live in CommunitySuite. |
| (c) “First GREEN” | The label is for area overlays only. It needs: v1.1 or later; at least one counted AI component; every counted component GREEN; and the two-scorer rule satisfied. v1.0 labels and “GREEN / none” are history, not precedent. | None. 0 of 137 rows qualify. All 12 GREEN-labelled rows fail at least one condition. |

**Other changes.** NCF's A1 and A3 rows move from None to **AMBER (low)** at the next re-score. This comes from new evidence, not from the rules: an NCF “AI-powered search experience” page, record dated 2026-08-12 (gap19 S18). Rule (a) only confirms that a sponsor's own AI feature belongs on its row. The precedent is Candid’s read-only AMBER (low), not Fidelity’s Virtual Assistant, which §5 treats as not described as AI. The page’s record status field reads “private”, so the move is provisional [V wave 43A]

**Counts** (script output):
- 137 ratings tested.
- 7 rows differ from the label that governs today, covering two providers: Chariot Disbursements (2 rows) and NCF A1/A3 (5 rows across the v1.0, v1.1 and v1.2 sets).
- 2 rows gain an annotation only (Chariot verification).
- 24 superseded labels are reproduced by the rules as later adjudications already changed them, including all four v1.1 blind-versus-v11 adjudications.
- No census product row changes level.
- No row is RED under the rules.

## 2. Method

1. **Locating the method.** Searched `research/mission-2026-11-14/quadrant*.md`, `evidence-quadrant-methodology.md` and `direction-ai-product-census.md` for “§7”, “AI overlay” and “GREEN”. The methodology is [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md):
   - §1 states the overlay and its principle, “AI may add a flag, never clear one”;
   - §7 holds the entity scope rule and the overlay vocabulary.
2. **Read before drafting:**
   - [b43n25-01](b43n25-01-green-overlay-validation.md) in full, with the wave 42A corrections ([validation-wave42a-report.md](validation-wave42a-report.md); applied in the census and the b43n25-01 file);
   - [quadrant-calibration.md](quadrant-calibration.md) §5, the v1.0 overlay;
   - [quadrant-v11-blind-and-calibration.md](quadrant-v11-blind-and-calibration.md) §5 (per-row overlays) and §6 (vocabulary, adjudications);
   - [quadrant-v11-rescore.md](quadrant-v11-rescore.md) §3 with its wave 21 corrections;
   - [quadrant-v12-targeted-rescore.md](quadrant-v12-targeted-rescore.md) §4;
   - the v1.0 A1 and A2–A5 rationales (overlay tables);
   - the census doc and CSV;
   - [gap19-ai-coverage-20-entities.md](gap19-ai-coverage-20-entities.md) and its CSV.
3. **Inventory.** Every overlay rating in the quadrant and census data became one row (137 in all). Where a source table groups providers (“All others”; “Ren, Ren RDE, RCF, AEF”; “Chariot (Disbursements, DAFpay, verification)”), the group was split into one row per provider.

   | Rating set | Rows |
   |---|---|
   | v1.0 consensus | 34 |
   | v1.0 primary scorer, A1 GREEN labels | 2 |
   | v1.1 blind labels that were adjudicated | 4 |
   | v1.1 consensus | 42 |
   | v1.2 targeted | 5 |
   | Census products | 30 |
   | gap19 entities | 20 |

4. **Test.** For each area row the script lists the AI components the repo evidences, each with a tie code. It then applies the rules as pure functions:
   - §7a decides which components count;
   - §7b combines them;
   - §7c tests first-GREEN eligibility.

   Tie codes are judgments, recorded in the CSV (`components_considered`) so a reviewer can contest each one. Census and gap19 labels are read directly from their CSVs. Product and entity rows keep their own readings (§7b(4)).
5. **Two first-party pages re-read** (2026-11-20, user agent `research-script/1.0`), because they decide outcomes:
   - the Chariot MCP help page, which decides whether Chariot's AI reaches DAFpay or Disbursements;
   - the NCF AI search page.

   Both quotes used below were found in the fetched text by script.

### robots.txt log (checked 2026-11-20 before any fetch)

| Host | Status | Result |
|---|---|---|
| help.givechariot.com | 200 | `User-agent: *` `Allow: /` |
| www.ncfgiving.com | 200 | `User-agent: *` `Disallow:` (empty; all allowed) |

crt.sh, certspotter and sec.gov were not used. There was no outreach and no login.

## 3. Point (a): does the overlay apply to vendor products outside A1–A5?

### Proposed rule (§7a)

1. The overlay is a flag on provider rows scored in an area A1–A5. Only those rows carry an area overlay, and only they count in area totals.
2. A vendor product outside A1–A5 may be read with the same GREEN, AMBER and RED tests. The result is a **product-level reading**, written against the product (for example in the AI product census). It is not an area overlay.
3. A product-level reading enters a provider row only as a component under §7b, and only on a documented tie:
   - **T1:** the capability is documented in the scored offering;
   - **T2:** it runs on a vendor-wide AI platform or agent channel that its source does not confine to another product, or that a source says reaches the scored offering;
   - **T3:** it performs the scored offering's own function (moves its grants or sets its eligibility status);
   - **T4:** a source ties a vendor capability to the sponsor's program (entity scope rule).
4. **Ties are asymmetric, so the overlay can add a flag but never clear one.**
   - An AMBER or RED component counts on any of T1–T4.
   - A GREEN component counts only on T1: it must be live in the scored offering, with its controls documented there.
   - Evidence that would lower a flag must meet the same T1 test.
5. A capability that its source confines to another product is not counted. If it is AMBER or RED, the provider row shows it as “adjacent product AMBER/RED: <product>”, so the flag stays visible.
6. The entity scope rule applies unchanged. A vendor's, parent's or owner's capability is not a sponsor's capability, and the reverse also holds, unless T4 is met.

### Reasoning

- **Scope.** §1 reports the overlay “for every area”, and the area table names who is in scope. The census applies the vocabulary to 30 products from 22 vendors, most of them outside A1–A5, and says “the overlay vocabulary was written for DAF providers”. Without a rule, a census GREEN can be read as an area GREEN, which is the error b43n25-01 §4 corrected.
- **Asymmetric ties.** The overlay principle is about not letting automation remove a safeguard. The equivalent rule for the rater is that weak evidence may add a flag, but only strong, offering-specific evidence may award GREEN or lower a flag. A shared platform or agent channel is a real path for risk, so it is enough to add a flag. Controls documented for one product say nothing about another, so they are not enough for GREEN.
- **Adjacent products.** Visibility keeps the principle intact even when a flag does not count.
- **Entity scope.** T4 restates the existing entity scope rule at component level. It is not a new path.

### Test against existing ratings

**Area rows.** Of 87 area rows, every AMBER or RED flag held on a T1–T4 tie except one provider:

| Provider (area) | Components and ties | Outcome |
|---|---|---|
| TIFIN Give (A1); GiveClear (A3) | Louise: T1 for TIFIN; T4 for GiveClear (Louise runs on GiveClear programs, 48-hour review) | AMBER (RED-boundary), unchanged |
| Daffy (A4) | MCP and Quick Donate, T1 | AMBER, unchanged |
| Foundant CommunitySuite (A1) | Fia beta, T2 (vendor platform, not confined) | AMBER, unchanged. The weakest held tie: foundant.com is robots-barred, and the release does not name CommunitySuite |
| Blackbaud FE NXT (A1) | Blackbaud Copilot technical preview in FE NXT (2024-10-07, wave 28), T1. The RE NXT Development Agent and Chat are confined to RE NXT, so they are adjacent | AMBER, unchanged. The basis should cite the FE NXT preview, not “AI agents in an adjacent CRM” (queue P-B430105-02) |
| Chariot DAFpay (A2) | Chariot MCP, T2. The help page says the connector “is built for Chariot's Gift Processing platform. It also surfaces DAFpay components” (tool `get_dafpay_components`) | AMBER, unchanged |
| **Chariot Disbursements (A2)** | The Gift Processing AI and the MCP are both confined to Gift Processing (and DAFpay); Disbursements is not named. The remaining basis, an agent-capable API, is not AI under the v1.1 Endaoment precedent | **AMBER → None (watch: agent-capable API) [adjacent product AMBER]** |
| Chariot verification (A5) | Same confinement | None, plus an adjacent-product note |
| Candid (A5) | MCP connector and assistant, T2 (they expose Candid's data) | AMBER (low), unchanged |
| Benevity validation (A5) | Match Assurance, T3 (it performs an eligibility check) | AMBER (provisional), unchanged from wave 21 |
| Goodstack (A5) | “AI-powered automation” in verification, T1 | AMBER, unchanged |
| MS GIFT (A3) | “Automated” vetting of undisclosed nature, T1 | AMBER (provisional), unchanged |

**None rows.** Vendor evidence that might have been imported stays out:
- Salesforce Agentforce does not reach the NCF and SVCF rows.
- Foundation Source's roadmap does not reach Charityvest, and it is WATCH in any case.
- Fidelity's Virtual Assistant does not reach Fidelity EFT or DAF Direct.

**Census rows (30).** All are product-level readings, and none changes level. Seven feed an area row as counted components:
- AIP01 (TIFIN Give, GiveClear);
- AIP02 and AIP03 (Daffy);
- AIP07 (Chariot DAFpay);
- AIP11 (Foundant);
- AIP22 and AIP23 (Candid).

AIP06 and AIP07 are adjacent to Chariot Disbursements and Chariot verification, and AIP17 and AIP18 are adjacent to Blackbaud FE NXT. The GREEN rows AIP12, AIP13 and AIP16 feed no area row:
- AIP12 is configured from CommunitySuite but not shown live there (wave 42A V42A-15), so it fails T1.
- AIP16 is GrantsConnect, not FE NXT.
- AIP13 belongs to Fluxx, which has no area row.

**gap19 entity rows (20).** None changes. Every case where a parent or owner capability was kept out by entity scope holds:
- SEI and TIFIN;
- Morgan Stanley and Debrief;
- BofA and Erica;
- Edward Jones;
- Charityvest and Foundation Source;
- TIAA and OneAscent with Charityvest;
- iPhi and RCF with Ren.

### Ratings that change

- **Chariot Disbursements (A2): AMBER → None (watch: agent-capable API) [adjacent product AMBER: Chariot Gift Processing AI; Chariot MCP].** Apply at the next re-score, after adjudication: both v1.1 scorers had agreed on AMBER. Keeping AMBER would require treating an agent-capable API as an AI component. That would also move Endaoment from None (watch) to AMBER (queue P-B430105-01).
- **Chariot verification (A5):** None, with an adjacent-product note added. Annotation only.

## 4. Point (b): a provider with one GREEN component and one AMBER

### Proposed rule (§7b)

1. Count each live AI component tied under §7a.
   - Live means GA, beta, or a preview open to customers.
   - Announced or roadmap items are WATCH and do not count.
   - Automation or navigation that its source does not describe as AI is not an AI component.
2. The provider's flag is its most severe counted component: RED, then AMBER, then GREEN. A component whose controls could not be read counts as AMBER (unverified).
3. A provider is GREEN only if every counted component is GREEN. A GREEN component never offsets, lowers or clears another component's AMBER or RED.
4. When counted components differ, write the flag and then the split: “AMBER (mixed: GREEN <component>; AMBER <component>)”. Product rows keep their own readings.
5. With no counted component, the flag is None, with its existing qualifier.

### Reasoning

- **Most-severe aggregation.** The overlay principle forbids AI clearing a flag. Letting a well-governed component clear a flag raised by a poorly governed one would be the rating-level version of the same failure. A donor or nonprofit exposed to the AMBER component gains nothing from the GREEN one.
- **The “mixed” notation** keeps the documented GREEN visible, which is the useful finding for due diligence. b43n25-01 §5 inferred this rule for Foundant (“a provider is GREEN only if every evidenced live AI capability meets the GREEN wording (rule inferred)”), and wave 42A (V42A-15) accepted the result.
- **Unreadable controls count as AMBER (unverified).** A component whose controls cannot be read cannot support GREEN, and treating it as absent would clear a flag by default.

### Test against existing ratings

- **No A1–A5 provider has a counted GREEN component.** No area row is mixed, and no area level changes under §7b.
- **Foundant (A1):** Fia is AMBER. Application Analysis (GREEN) is not shown live in CommunitySuite, so it is not counted. The row stays AMBER. If it is shown live, the label becomes “AMBER (mixed: GREEN AIP12 SmartSimple Application Analysis; AMBER AIP11 Foundant Fia)”, never GREEN.
- **Blackbaud FE NXT (A1):** the GREEN YourCause summaries (AIP16) are not an FE NXT component. Stays AMBER.
- **Vendor-level aggregates outside A1–A5** are informational only, because no area row exists for them:
  - Fluxx: Finn GREEN plus the bundled MCP AMBER gives AMBER (mixed);
  - Blackbaud: AIP16 GREEN plus AIP17 and AIP18 AMBER gives AMBER (mixed);
  - Foundant: AIP11 AMBER plus AIP12 GREEN gives AMBER (mixed).

  The census keeps one reading per product, so its rows do not change.
- **Daffy (A4):** two AMBER components; the most severe is AMBER. Unchanged.

### Ratings that change

None.

## 5. Point (c): what counts as a “first GREEN”

### Proposed rule (§7c)

“First GREEN”, “only GREEN” and “no provider earns GREEN” refer to area overlays only. A first GREEN needs all four of the following:
1. **A provider row scored in A1–A5 under v1.1 or later.** v1.0 had no written GREEN test. Its labels (GREEN for Fidelity Charitable; “GREEN / none” for Ren, Ren RDE, RCF and AEF) were withdrawn by the v1.1 consensus and are history, not precedent.
2. **At least one counted AI component.** “None” can never be GREEN, and neither can rule-based or navigation-only automation.
3. **Every counted component GREEN under §7b,** on admissible first-party evidence (§3, §8) for the scored offering.
4. **The two-scorer rule (§5).** The GREEN must be reproduced by the blind scorer or upheld in an adjudication. A single-scorer or provisional label is written “GREEN (provisional)” and is not a first GREEN.

The claim names the version and date: “first GREEN area overlay under §7, v1.x, <date>”. A product-level reading outside A1–A5 is a “GREEN-eligible product reading”, never a first GREEN. If a first GREEN is withdrawn, later claims must say so.

### Reasoning

- **Why v1.0 labels do not count.** v1.0 §1 asks only whether capabilities “respect” the principle. The GREEN/AMBER/RED definitions arrived with the v1.1 area notes.
  - The v1.0 GREEN for Fidelity Charitable rested on a navigation-only assistant with disclaimers. v1.1 §6 held that this “is not a documented flag-only or authority-separation control”.
  - “GREEN / none” for Ren, Ren RDE, RCF and AEF described rule-based instant approval with “no AI”.
  - Condition 2 makes both readings impossible under the new rule rather than leaving them as precedents.
- **Why the two-scorer rule.** The v1.1 blind scorer also gave GREEN to Fidelity and Candid, and the consensus overturned both (§6). Condition 4 excludes such labels, so “first” cannot attach to a single reading.
- **Why the census GREENs are excluded.** Condition 1 restates b43n25-01 §4 and V42A-14 as a rule. The census GREENs are the first GREEN-eligible vendor product readings, not a first GREEN.

### Test against existing ratings

12 rows carry a GREEN label. **0 of 137 rows meet §7c.**

| GREEN-labelled rows | First condition failed |
|---|---|
| v1.0 consensus: Fidelity Charitable; Ren; Ren RDE; RCF; AEF (5 rows) | 1 (v1.0 label). Ren, Ren RDE, RCF and AEF also fail 2 (no AI component) |
| v1.0 primary scorer, A1: Fidelity; Ren (2 rows) | 1 |
| v1.1 blind scorer: Fidelity; Candid (2 rows) | 2 for Fidelity (no counted AI component: the Virtual Assistant is not described as AI). 3 for Candid (its counted components are AMBER (low)). Both also fail 4 (not upheld) |
| Census: AIP12 SmartSimple; AIP13 Fluxx Finn; AIP16 YourCause (3 rows) | 1 (not an A1–A5 area row). All are also provisional |

The current wording in the census, the industry report §11.57 and FINAL-STATUS (“none is the first GREEN under §7”) is consistent with §7c, and no text change is needed there.

### Ratings that change

None. The v1.0 table gains a note on two rows so that the withdrawn labels cannot be read as precedent (corrections below).

## 6. Consistency checks

- **“AI may add a flag, never clear one.”**
  - §7a lets weak evidence add a flag and requires offering-specific evidence to award GREEN or lower a flag.
  - §7b never lets GREEN offset AMBER or RED.
  - Confined flags stay visible as “adjacent”.
  - The one downgrade (Chariot Disbursements) does not come from GREEN evidence. It comes from a flag whose components were never tied to the product, and the flag stays shown as adjacent. However, §7a(4) also says evidence that would lower a flag must meet T1, and a product list for another product is not T1 evidence about Disbursements, so the downgrade is held as a pending adjudication note, not a rating change [V wave 43A]
- **Entity scope rule.** T4 is that rule at component level. The test kept out every parent, owner or vendor capability that the gap19 and v1.1 work had kept out. TIFIN to GiveClear is the one tie a source documents, and it holds.
- **Agreement with past adjudications.** The rules reproduce all four v1.1 blind-versus-v11 adjudications (Fidelity, Candid, Endaoment, Foundant) and the wave 21 Benevity change. This is partly circular, because the tie codes were assigned from the same evidence the adjudicators used.

## 7. Other findings from the test (not caused by the rules)

1. **Stale Benevity RED.** The v1.1 consensus record (quadrant-v11-blind-and-calibration.md §5 A5 row and §6 text) and the industry report's v1.1 overlay lists still say RED (provisional). The wave 21 change to AMBER (provisional) is recorded only in the governing wave 21 corrections appendix of quadrant-v11-rescore.md, whose body still reads RED (queue P-B430105-05) [V wave 43A]
2. **NCF overlay is out of date.** v1.1 and v1.2 have None. The gap19 entity reading (2026-11-19) is AMBER (low) for NCF's own AI search. The page was re-read on 2026-11-20: “Explore trusted NCF resources through an AI-powered search experience”, record dated 2026-08-12. Proposed: AMBER (low) at the next re-score (queue P-B430105-03).
3. **Non-AI automation is rated two ways.** Morgan Stanley GIFT's “Automated” vetting is AMBER (provisional), but Givinga's “Automate compliance, charity vetting” is None evidenced. §7b and §7c settle only that such automation can never be GREEN (queue P-B430105-04).
4. **MS GIFT, gap19 versus v1.2.** gap19 records “None evidenced (program)” for AI, and v1.2 records AMBER (provisional) for non-AI automation. Both stand, but the report should cite v1.2 for the overlay.

## 8. Limits

- **Tie codes are judgments.** They are recorded per component in the CSV. Three held flags rest on the weakest ties:
  - Foundant (T2: Fia's reach into CommunitySuite is not documented, and foundant.com is robots-barred);
  - Blackbaud FE NXT (a 2024 technical preview of unknown current status);
  - Benevity (T3: Match Assurance is “adjacent to” the validation product).
- **The rules are proposals.** The rating changes apply at the next re-score, as the v1.1 notes did, and the Chariot change needs adjudication.
- **Rows not included.** v1.0 primary and blind rationale overlays and the v11 primary table were not given separate rows, except the GREEN labels and the four adjudicated blind labels. Their other labels match the consensus rows or were adjudicated in calibration.md §5 and v11 §6.
- **No re-reading beyond two pages.** Apart from the two pages in §2, no vendor page was re-read. Census readings were taken as validated (waves 28 and 42A).
- **“AMBER (low)” is a census-local sub-label** (wave 28). The v1.1 consensus also uses it for Candid, and the NCF proposal follows that use.

## Exact corrections

### `research/mission-2026-11-14/evidence-quadrant-methodology.md`

- **Find:** "An **AI-governance overlay** is reported for every area as a flag, not an axis."
- **Replace with:** "An **AI-governance overlay** is reported for every area as a flag, not an axis. It is a flag on provider rows scored in A1–A5 only; vendor products outside those areas get product-level readings (see §7, “AI overlay scope”) [b4301-05]"
- **Find:** "- **RED:** AI can complete a money-moving or status-clearing action without documented sponsor or human approval."
- **Replace with:** "- **RED:** AI can complete a money-moving or status-clearing action without documented sponsor or human approval.\n- **None:** no AI capability is evidenced. This is not evidence of absence (as used in the v1.1 consensus, quadrant-v11-blind-and-calibration.md §6).\n\n**AI overlay scope (§7a).**\n1. The overlay is a flag on provider rows scored in an area A1–A5. Only those rows carry an area overlay, and only they count in area totals.\n2. A vendor product outside A1–A5 may be read with the same GREEN, AMBER and RED tests. The result is a product-level reading, written against the product (for example in the AI product census). It is not an area overlay.\n3. A product-level reading enters a provider row only as a component under §7b, and only on a documented tie: T1, the capability is documented in the scored offering; T2, it runs on a vendor-wide AI platform or agent channel that its source does not confine to another product, or that a source says reaches the scored offering; T3, it performs the scored offering’s own function (moves its grants or sets its eligibility status); T4, a source ties a vendor capability to the sponsor’s program (entity scope rule).\n4. Ties are asymmetric, so the overlay can add a flag but never clear one. An AMBER or RED component counts on any of T1–T4. A GREEN component counts only on T1: it must be live in the scored offering, with its controls documented there. Evidence that would lower a flag must meet the same T1 test.\n5. A capability that its source confines to another product is not counted. If it is AMBER or RED, the provider row shows it as “adjacent product AMBER/RED: <product>”, so the flag stays visible.\n6. The entity scope rule applies unchanged: a vendor’s, parent’s or owner’s capability is not a sponsor’s capability, and the reverse also holds, unless T4 is met.\n\n**AI overlay components (§7b).**\n1. Count each live AI component tied under §7a. Live means GA, beta, or a preview open to customers. Announced or roadmap items are WATCH and do not count. Automation or navigation that its source does not describe as AI is not an AI component.\n2. The provider’s flag is its most severe counted component: RED, then AMBER, then GREEN. A component whose controls could not be read counts as AMBER (unverified).\n3. A provider is GREEN only if every counted component is GREEN. A GREEN component never offsets, lowers or clears another component’s AMBER or RED.\n4. When counted components differ, write the flag and then the split: “AMBER (mixed: GREEN <component>; AMBER <component>)”. Product rows keep their own readings.\n5. With no counted component, the flag is None, with its existing qualifier.\n\n**“First GREEN” (§7c).** “First GREEN”, “only GREEN” and “no provider earns GREEN” refer to area overlays only. A first GREEN needs all four of the following:\n1. A provider row scored in A1–A5 under v1.1 or later. v1.0 had no written GREEN test. Its labels (GREEN for Fidelity Charitable; “GREEN / none” for Ren, Ren RDE, RCF and AEF) were withdrawn by the v1.1 consensus and are history, not precedent.\n2. At least one counted AI component. “None” can never be GREEN, and neither can rule-based or navigation-only automation.\n3. Every counted component GREEN under §7b, on admissible first-party evidence (§3, §8) for the scored offering.\n4. The two-scorer rule (§5): the GREEN must be reproduced by the blind scorer or upheld in an adjudication. A single-scorer or provisional label is written “GREEN (provisional)” and is not a first GREEN.\nThe claim names the version and date (“first GREEN area overlay under §7, v1.x, <date>”). A product-level reading outside A1–A5 is a “GREEN-eligible product reading”, never a first GREEN. If a first GREEN is withdrawn, later claims must say so [b4301-05]"

### `research/mission-2026-11-14/direction-ai-product-census.md`

- **Find:** "The overlay vocabulary was written for DAF providers."
- **Replace with:** "The overlay vocabulary was written for DAF providers. Under methodology §7a every row here is a product-level reading: it is not an area overlay, it can never be a first GREEN (§7c), and it enters an A1–A5 provider’s flag only as a tied component under §7b [b4301-05]"
- **Find:** "and §7 has no rule for rating a provider from one GREEN component [V wave 42A]"
- **Replace with:** "and under methodology §7b a GREEN component cannot offset Fia’s AMBER; Application Analysis is not shown live in CommunitySuite, so it is not yet a counted component of the Foundant row [b4301-05]"

### `research/mission-2026-11-14/quadrant-calibration.md`

- **Find:** "No decision authority. | **GREEN**"
- **Replace with:** "No decision authority. | **GREEN** (v1.0 label; withdrawn by the v1.1 consensus to None (inform-only); not a first GREEN or precedent under methodology §7c) [b4301-05]"
- **Find:** "**GREEN / none.** The decision logs are not public."
- **Replace with:** "**GREEN / none.** The decision logs are not public. (v1.0 label; withdrawn by the v1.1 consensus to None; “none” cannot be GREEN under methodology §7c) [b4301-05]"

### `research/mission-2026-11-14/quadrant-v11-blind-and-calibration.md`

- **Find:** "| 2.80 (2.80–2.80) | 3.52 (3.52–3.52) | 1.0/1.0 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | AMBER"
- **Replace with:** "| 2.80 (2.80–2.80) | 3.52 (3.52–3.52) | 1.0/1.0 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | AMBER; at the next re-score under methodology §7a and §7b: None (watch: agent-capable API) [adjacent product AMBER: Chariot Gift Processing AI; Chariot MCP], because the MCP is “built for Chariot’s Gift Processing platform” and surfaces DAFpay, not Disbursements (adjudicate; queue P-B430105-01) [b4301-05]"
- **Find:** "| 2.58 (2.58–2.58) | 2.65 (2.65–2.65) | 1.0/1.0 | Proven Leaders | Proven Leaders / insufficient evidence | adjudicated | None"
- **Replace with:** "| 2.58 (2.58–2.58) | 2.65 (2.65–2.65) | 1.0/1.0 | Proven Leaders | Proven Leaders / insufficient evidence | adjudicated | None [adjacent product AMBER: Chariot Gift Processing AI; Chariot MCP] (annotation under methodology §7a) [b4301-05]"

### `research/mission-2026-11-14/quadrant-v12-targeted-rescore.md`

- **Find:** "| NCF (A3 and A1) | none evidenced"
- **Replace with:** "| NCF (A3 and A1) | none evidenced at v1.2; at the next re-score AMBER (low) under methodology §7a: NCF’s own “AI-powered search experience” (ncfgiving.com/ai-search, record dated 2026-08-12; gap19-ai-coverage S18), re-read 2026-11-20 [b4301-05]"

### `research/mission-2026-11-14/b43n25-01-green-overlay-validation.md`

- **Find:** "proposed for clarification as P-B4301-05."
- **Replace with:** "proposed for clarification as P-B4301-05. The proposed rules (b4301-05-methodology-s7-clarification.md, §7a–§7c) confirm both inferences: a GREEN component cannot lift a provider that also has an AMBER component, and no vendor product outside A1–A5 can be a first GREEN [b4301-05]"

Every Find above was checked by script: each occurs exactly once in its file. No value contains a straight double quote. These corrections touch different lines and can be applied in any order.

## Data dictionary

### `data/mission-2026-11-14/overlay-rule-test-2026-11-20.csv` (137 rows, one per existing overlay rating)

| Column | Meaning |
|---|---|
| row_id | OT001–OT137 |
| rating_set | v1.0 consensus (superseded); v1.0 primary scorer A1 (superseded); v1.1 blind scorer (adjudicated); v1.1 consensus; v1.2 targeted; census (product readings); gap19 AI coverage (entity readings) |
| source_pointer | Repo file and section, or CSV and product ID, where the rating is recorded |
| area | A1–A5 for area rows; “outside” or “product of A1-A5 provider” for census rows; “entity” for gap19 rows |
| subject | Provider, product or entity |
| recorded_label | Label as written in the source |
| governing_label_now | Label that governs today after later consensus or validation corrections (for example, Benevity AMBER (provisional) from wave 21; MS GIFT AMBER (provisional) from v1.2) |
| scope_class | area_row, product_reading or entity_reading (§7a) |
| components_considered | Area rows: each AI component with its level and tie code (T1–T4, confined, none, not AI, not live, or configured but not shown live). Product and entity rows: n/a |
| counted_components | Components that count under §7a |
| rule_a_scope | How §7a classifies the row and, for products, which area row it feeds or is adjacent to |
| rule_b_components | Combined level under §7b, with mixed, adjacent and watch notes |
| rule_c_first_green | “eligible”, or “no:” and the first §7c condition failed |
| proposed_outcome | Label under the proposed rules. Bracketed text is a §7b mixed or adjacent annotation |
| change_vs_recorded | no; annotation only; or yes: old -> new, against recorded_label |
| change_vs_governing | The same, against governing_label_now (the rows that would actually change) |
| change_driver | none; rule; or new evidence admitted by §7a |
| note | Caveats and evidence for the call |

### `data/mission-2026-11-14/queue-proposals-b4301-05.csv`

This file uses the header and format of `queue-proposals-gap19-13.csv`. It holds five proposals, P-B430105-01 to -05:
1. Chariot Disbursements adjudication;
2. Blackbaud FE NXT AI status;
3. NCF AI search controls;
4. Non-AI automation harmonisation;
5. Stale Benevity RED labels.

## Source register

| ID | Source | Type | Date | Accessed | URL or path |
|---|---|---|---|---|---|
| R1 | Methodology §1, §3, §5, §7, §8 | repo | 2026-11-14 | 2026-11-20 | research/mission-2026-11-14/evidence-quadrant-methodology.md |
| R2 | GREEN overlay validation (P-B43N25-01) | repo | 2026-11-20 | 2026-11-20 | research/mission-2026-11-14/b43n25-01-green-overlay-validation.md |
| R3 | Validation wave 42A (V42A-01 to V42A-17) | repo | 2026-11-20 | 2026-11-20 | research/mission-2026-11-14/validation-wave42a-report.md |
| R4 | v1.0 calibration overlay (§5) | repo | 2026-11-14 | 2026-11-20 | research/mission-2026-11-14/quadrant-calibration.md |
| R5 | v1.1 consensus overlays (§5) and adjudications (§6) | repo | 2026-11-14 | 2026-11-20 | research/mission-2026-11-14/quadrant-v11-blind-and-calibration.md |
| R6 | v1.1 rescore §3 and wave 21 corrections (Benevity) | repo | 2026-11-15 | 2026-11-20 | research/mission-2026-11-14/quadrant-v11-rescore.md |
| R7 | v1.2 targeted overlay (§4) | repo | 2026-11 | 2026-11-20 | research/mission-2026-11-14/quadrant-v12-targeted-rescore.md |
| R8 | v1.0 A1 and A2–A5 rationale overlays | repo | 2026-11-14 | 2026-11-20 | research/mission-2026-11-14/quadrant-A1-rationale.md; quadrant-A2-A5-rationale.md |
| R9 | AI product census and CSV (30 rows) | repo | 2026-11-15 (wave 42A applied) | 2026-11-20 | research/mission-2026-11-14/direction-ai-product-census.md; data/mission-2026-11-14/philanthropy-ai-products-2026.csv |
| R10 | gap19 AI coverage, 20 entities | repo | 2026-11-19 | 2026-11-20 | research/mission-2026-11-14/gap19-ai-coverage-20-entities.md; data/mission-2026-11-14/ai-coverage-20-entities-2026-11-19.csv |
| R11 | Validation wave 28 (Blackbaud Copilot FE NXT preview, V28-31) | repo | 2026-11-15 | 2026-11-20 | research/mission-2026-11-14/validation-wave28-report.md |
| R12 | v1.1 consensus Y3 cells | repo | 2026-11-14 | 2026-11-20 | data/mission-2026-11-14/quadrant-scores-A1..A5-v11consensus.csv |
| P1 | Chariot MCP server help page (“built for Chariot's Gift Processing platform. It also surfaces DAFpay components”; `get_dafpay_components`) | vendor help | page says “Last updated 4 months ago” | 2026-11-20 | https://help.givechariot.com/account-management/chariot-mcp-server |
| P2 | NCF AI search page (“Explore trusted NCF resources through an AI-powered search experience”) | sponsor page | record 2026-08-12 | 2026-11-20 | https://www.ncfgiving.com/ai-search |
| P3 | Foundant Fia release (context only; cited via R2) | vendor PR mirror | 2026-09-02 | not re-read | https://www.financialcontent.com/article/gnwcq-2026-9-2-foundant-introduces-fia-a-new-ai-platform-built-for-social-good-organizations |
| P4 | SmartSimple Configure AI Application Analysis (CommunitySuite named; cited via R2, R3) | vendor help | 2026-07-07 | not re-read | https://supporthub.smartsimple.com/hc/en-us/articles/40249784423831-Configure-AI-Application-Analysis |
| P5 | Fidelity Charitable Virtual Assistant terms (cited via R9) | sponsor terms | undated | not re-read | https://www.fidelitycharitable.org/legal/virtual-assistant.html |
