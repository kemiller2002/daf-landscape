# DAF Evidence Quadrant: calibration and consensus (2026-11-14)

**Role:** calibration adjudicator under the two-scorer rule ([evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §5).
**Inputs:**
- Primary and blind score files: `data/mission-2026-11-14/quadrant-scores-A{1..5}-{primary,blind}.csv`.
- The calibration diff from `scripts/mission_quadrant_calibration.py`: `quadrant-calibration-providers.csv` and `quadrant-calibration-criteria.csv`.
- All six scorer rationales.
- Newer evidence:
  - [queue-vendor-scope-ren-denominator.md](queue-vendor-scope-ren-denominator.md)
  - [queue-contract-data-rights-agent-controls.md](queue-contract-data-rights-agent-controls.md)
  - [queue-infrastructure-nonprofit-costs-emerging.md](queue-infrastructure-nonprofit-costs-emerging.md)
  - [daf-user-complaints-deep-research.md](daf-user-complaints-deep-research.md)
  - `validation-register-wave3.csv` does not exist yet, so it was not used.

**Outputs:**
- `data/mission-2026-11-14/quadrant-scores-A{1..5}-consensus.csv`: 473 rows, one per provider × criterion, with `scorer = consensus`.
- `scorer = consensus` rows in `quadrant-positions.csv`.
- Charts: `quadrants/A{1..5}-consensus.svg`.
- Queue proposals: `queue-proposals-quadrant-calibration.csv` (P-QCAL-01 to 07).

**Status.** These are *internal-demonstration* claims (Clarity/EDF). Positions marked **reproduced** below meet the methodology's reproduction test. All other positions remain single-adjudicator judgements. **This is the repository's own method. It is not a Gartner Magic Quadrant**, it is not affiliated with Gartner, and it does not use Gartner's criteria or labels.

## 1. Method

1. **Agreeing cells** are cells that the calibration script did not flag. Both scorers scored the cell within 1 point of each other, or both left it U. The consensus score is the mean of the two effective scores, with the vendor-claim cap of 2 applied first, rounded to the nearest 0.5. The evidence class, summary and URL come from the better-classed of the two rows. `notes = agree`.
2. **Flagged cells** are the 71 `one_scorer_unknown` cells and the 1 `gap_gt_1` cell. I read both scorers' evidence, and opened source URLs where the outcome turned on them. I then applied the methodology:
   - **Absence = U.** A score that rests only on "no audit / no API / no SOC found" becomes U. This rule removed several blind-scorer 1s built on "Form 990 only".
   - **Vendor claims are capped at 2.**
   - **The better-evidenced score wins.**
   - **Admissible evidence that one scorer missed is used**, unless it fails admissibility or relevance. Relevance fails when the evidence concerns another entity or product, for example a vendor's marketing scored for a sponsor, or Raiser's Edge NXT AI scored for Financial Edge NXT.
3. **Unflagged cells at disputed or insufficient-evidence providers.** I examined every 1-point gap at these providers. I overrode the mean in 11 cells where one side was clearly better evidenced.
4. **Consistency across areas.** The same evidence gets the same score wherever it recurs. Examples:
   - Every.org payout cadence: Y2 = 2 in both A2 and A4.
   - TIFIN Terms: Y1 = 1 for TIFIN Give (A1) and GiveClear (A3).
   - Entity-level audits without a rail-scoped control report: X3 = 2 for both Fidelity EFT and PayPal Grant Payments.
5. **Status labels.**
   - **Reproduced:** both scorers' quadrants have the same base quadrant, ignoring "(boundary)", and the consensus agrees.
   - **Adjudicated:** the consensus is plottable, but the scorers differed in base quadrant, or one of them could not plot the provider.
   - **Insufficient evidence:** consensus coverage is below 0.5 on either axis.
6. **Engine.** `python3 scripts/mission_quadrants.py .` was rerun unchanged. Bands set unknowns to 0 for the low bound and 4 for the high bound. "Boundary" means the point estimate is within 0.25 of a midline.

## 2. Agreement statistics

### 2.1 Provider status from the calibration CSV (primary vs blind, before adjudication)

| Area | Providers | Reproduced | Disputed | Insufficient evidence |
|---|---|---|---|---|
| A1 | 12 | 3 | 4 | 5 |
| A2 | 7 | 4 | 2 | 1 |
| A3 | 12 | 5 | 2 | 5 |
| A4 | 7 | 3 | 2 | 2 |
| A5 | 5 | 3 | 1 | 1 |
| **All** | **43** | **18 (42%)** | **11 (26%)** | **14 (33%)** |

### 2.2 Criterion-level agreement

| Area | Cells | Both scored | Exact agreement (of both scored) | Within 1 point | Both U | One scorer U | Gap > 1 | Exact or both-U (of all cells) |
|---|---|---|---|---|---|---|---|---|
| A1 | 132 | 80 | 53 (66%) | 80 (100%) | 33 | 19 | 0 | 65% |
| A2 | 77 | 60 | 43 (72%) | 60 (100%) | 11 | 6 | 0 | 70% |
| A3 | 132 | 79 | 48 (61%) | 79 (100%) | 35 | 18 | 0 | 63% |
| A4 | 77 | 47 | 32 (68%) | 46 (98%) | 12 | 18 | 1 | 57% |
| A5 | 55 | 39 | 28 (72%) | 39 (100%) | 6 | 10 | 0 | 62% |
| **All** | **473** | **305** | **204 (67%)** | **304 (99.7%)** | **97** | **71** | **1** | **64%** |

**Reading:**
- **When both scorers found evidence, they almost never disagreed by more than a point.** There was one gap above 1 point in 305 scored pairs: Daffy Y4 (primary 3, blind 1).
- **Disagreement is mostly about evidence discovery, not judgement.** 71 of the 72 flagged cells (99%) are cells where one scorer found admissible evidence and the other did not. The blind scorers were barred from some repository files (the complaint corpus, the edge graph and the AVD file in A2/A5), so blind X6 is often U.
- **About two-thirds of all cells are identical** (exact numeric match or both U).

### 2.3 Adjudication outcomes (473 consensus cells)

| Outcome | Cells |
|---|---|
| Agree, identical scores (incl. 97 both-U) | 301 |
| Agree, 1-point gap: mean rounded to 0.5 | 89 |
| Adjudicated (72 flagged + 11 unflagged gaps at disputed/insufficient providers) | 83 |
| of which the blind score adopted | 43 |
| of which the primary score adopted | 32 |
| of which a third value was set from evidence opened by the adjudicator | 8 |
| of which set to U (absence or wrong entity) | 13 (counted within the three rows above) |

## 3. Adjudications

The four adjudications that most changed the record, all from evidence opened on 2026-11-14:

1. **Charityvest X3 → 3 (A3 and A4).** Both scorers missed the final audited statements. The primary scorer could not open the attachment, and the blind scorer saw only the 2019 draft. Smith & Howard's FY2024/FY2023 audit is posted on the [financial-reporting page](https://guide.charityvest.org/governance-and-legal/financial-reporting). It carries an unmodified opinion and a related-party note on the Vennfi / Foundation Source services agreement ($653,138 in 2024). This lifts Charityvest's X just above the midline in both areas (2.10 in A3, 2.15 in A4).
2. **NPT X3 → 2 (A3), not the blind scorer's 3.** The "consolidated statements 2024" link on NPT's annual-report page is a [2-page statement of financial position](https://www.nptrust.org/consolidated-statements-2024-npt/). It has no auditor's report and no notes.
3. **NCF X3 → 3 and X5 → 4 (A3).** The [2025 consolidated FS](https://site.ncfgiving.com//wp-content/uploads/2026/07/NCF-25-Consolidated-FS-Final.pdf) carry an independent auditor's report. NCF still cannot be plotted, because its Y coverage is 0.15.
4. **Daffy Y4 → 3 (A4), the only gap above 1.** The [Daffy for Work page](https://www.daffy.org/resources/daffy-for-work-stock-matching) shows a live workplace program: launched in 2023, extended in 2024, with stock matching added in April 2026. The blind scorer missed it.

Other notable calls:
- **Benevity Y2 → 3.** I verified Benevity's [nonprofit-eligibility page](https://benevity.com/nonprofit-eligibility) for daily sanctions screening and appeals that pause disbursements. This flips Benevity from Scale Operators to Proven Leaders (boundary) in A5.
- **Endaoment Y2, Y3 and Y5 → 3 (A4).** First-party docs back them: required idempotency keys, Endaoment review of every API grant, and a cancel window. Its audit is confirmed.
- **Fidelity Charitable (A1).** The 1-point gaps resolve against the primary scorer's Proven Leaders (boundary) label. Y1 = 1 rests on DAF Direct and the nonprofit reports.
- **Every.org X1 = 2 (A2).** Its 990-PF outranks the primary scorer's vendor claim. This makes Every.org plottable in both A2 and A4.

### 3.1 Full adjudication register

P = primary score. B = blind score. **C** = consensus score. URLs are the evidence used.

| Area | Provider | Criterion | P | B | C | Flag | Reason | Evidence |
|---|---|---|---|---|---|---|---|---|
| A1 | Blackbaud Financial Edge NXT (foundations) | X1 | U | 1 | **1** | one_scorer_unknown | only blind found admissible evidence (one named CF using FE NXT for fund accounting; no DAF-sponsor count); accepted | [source](https://www.casestudies.com/company/blackbaud/case-study/the-san-diego-foundation-customer-case-study) |
| A1 | Blackbaud Financial Edge NXT (foundations) | X2 | 3 | U | **3** | one_scorer_unknown | only primary found admissible evidence (SKY API / General Ledger API delivered with docs, V2A-28); accepted; RE NXT agent item not relied on | [source](https://learn.microsoft.com/en-us/connectors/blackbaudfenxtgenera) |
| A1 | Blackbaud Financial Edge NXT (foundations) | X6 | 1 | U | **1** | one_scorer_unknown | only primary found admissible evidence: CF donor breach notices naming Blackbaud (CMP-237) are positive complaint evidence; blind U reflected corpus coding only | [source](https://pdnfoundation.org/news/notice-of-blackbaud-inc-security-incident) |
| A1 | Blackbaud Financial Edge NXT (foundations) | Y2 | U | 1 | **1** | one_scorer_unknown | only blind found admissible evidence: connector docs show a G/L with no grant-recommendation or nonprofit-shared state; positive characterisation, accepted | [source](https://learn.microsoft.com/en-us/connectors/blackbaudfenxtgenera) |
| A1 | Blackbaud Financial Edge NXT (foundations) | Y3 | U | 2 | **U** | one_scorer_unknown | blind's Development Agent evidence is for Raiser's Edge NXT, not FE NXT; evidence about another product fails scope, so U (kept in overlay) | [source](https://www.nasdaq.com/press-release/blackbaud-launches-new-category-ai-agent-general-availability-its-first-agent-goodtm) |
| A1 | Blackbaud Financial Edge NXT (foundations) | Y5 | U | 2 | **2** | one_scorer_unknown | only blind found admissible evidence: SKY API / Power Automate connector gives API-based extraction (partial interoperability); no transition terms | [source](https://learn.microsoft.com/en-us/connectors/blackbaudfenxtgenera) |
| A1 | Fidelity Charitable (in-house, FMR-administered) | Y1 | U | 1 | **1** | one_scorer_unknown | blind found documented partial data mechanisms (DAF Direct widget; nonprofit Stripe/ACH reports) and no API; primary left U; accepted at 1 (no export or API right for donors) | [source](https://fidelitycharitable.org/about-us/news/daf-direct-brings-new-giving-option-to-nonprofits.html) |
| A1 | Foundant CommunitySuite | X6 | 2 | U | **2** | one_scorer_unknown | primary's 99% renewal claim is an admissible vendor_claim (capped at 2); blind left U because review sites were not coded; accepted | [source](https://www.foundant.com/products/communitysuite/) |
| A1 | Foundant CommunitySuite | Y5 | 2 | U | **2** | one_scorer_unknown | primary's evidence (Foundant markets FIMS-to-CommunitySuite migrations) is admissible vendor_claim of migration support, capped at 2; no exit terms | [source](https://communityfoundations.foundant.com) |
| A1 | Foundation Source (DAF OS / Vennfi) | X6 | 2 | U | **U** | one_scorer_unknown | primary's Charityvest forum records (CMP-180/181) are coded to the sponsor Charityvest, which is scored separately in A3/A4; four low-severity records do not establish a platform-level signal; U | [source](https://www.bogleheads.org/forum/viewtopic.php?t=417491) |
| A1 | Give Interactive | X2 | U | 2 | **2** | one_scorer_unknown | only blind scored: Vanguard partnership announced 2025-11; newer evidence shows a Vanguard production tenant from Aug 2026 (CT logs, inferred) and live WaterStone/Signatry portals, while go-live is undisclosed; mixed record = 2 | [source](https://www.giveinteractive.com/post/fund-of-funds-platform) |
| A1 | Givinga | X4 | U | 2 | **2** | one_scorer_unknown | only blind scored; channel partners (PlanSource, EarthShare, WeSpire, Double the Donation) re-confirmed in queue-infrastructure-nonprofit-costs-emerging.md; accepted | [source](https://www.businesswire.com/news/home/20210812005102/en) |
| A1 | NCF (sponsor-built, Salesforce) | X4 | U | 3 | **3** | one_scorer_unknown | only blind scored; first-party NCF page (30+ local offices, adviser and church channels) is admissible; consistent with the sponsor-channel reading both scorers used for Fidelity/NPT | [source](https://www.ncfgiving.com/about/) |
| A1 | NPT GivingPoint (sponsor-built) | X2 | U | 3 | **3** | one_scorer_unknown | only blind scored; NPT first-party account of the two-year GivingPoint build delivered in 2021 plus PayPal Grant Payments adoption; accepted. Note: newer evidence shows GivingPoint is Ren-hosted iPhi with a Ren-built front end (research/mission-2026-11-14/queue-vendor-scope-ren-denominator.md), so the 'sponsor-built' label is wrong | [source](https://www.nptrust.org/philanthropic-resources/philanthropist/five-things-to-know-about-npt-givingpoint-a-conversation-with-chris-adams-svp-of-it-solutions-and-cybersecurity/) |
| A1 | NPT GivingPoint (sponsor-built) | Y1 | U | 1 | **1** | one_scorer_unknown | only blind scored: NPT's own 'modern APIs' claim (vendor_claim) with no public API or export terms; accepted at 1. iPhi MSA template (15-day export window) is consistent | [source](https://www.nptrust.org/nptgivingpoint/) |
| A1 | NPact (FIMS / DonorCentral) | X2 | U | 2 | **2** | one_scorer_unknown | only blind scored: 2022 product acquisition delivered and AEF DonorCentral move executed, then AEF churned to Ren; mixed = 2 | [source](https://www.aefonline.org/donorcentral-transition-notice/) |
| A1 | SVCF (sponsor-built, Salesforce) | X4 | U | 2 | **2** | one_scorer_unknown | only blind scored; first-party svcf.org (direct donors, corporate DAF services, advisers); accepted | [source](https://www.svcf.org/) |
| A1 | SVCF (sponsor-built, Salesforce) | X6 | U | 2 | **U** | one_scorer_unknown | blind's two coded records are governance/culture items about the sponsor, which blind itself notes are not platform failures; fails relevance to a platform X6; U | [source](https://marcgunther.com/blog/2018/04/23/emmett-carsons-credibility-problem) |
| A1 | SVCF (sponsor-built, Salesforce) | Y4 | U | 2 | **2** | one_scorer_unknown | only blind scored; first-party svcf.org shows community donors plus corporate DAF services; accepted | [source](https://www.svcf.org/) |
| A2 | Chariot DAFpay | X6 | 2 | U | **2** | one_scorer_unknown | only primary scored; App Store reviews (5 praise, 1 high, 1 medium) and IPS critique are admissible complaint evidence; mixed = 2 | [source](https://apps.apple.com/us/app/dafpay/id6633440388) |
| A2 | DAF Direct | X1 | 1 | 2 | **1** | disputed-provider gap | blind's 2 rests on sponsor backing, which is channel reach (X4), not scale; the only adoption figure is 1,251 charities (2015) and 2026 site lists 5 example users; primary better evidenced | [source](https://www.philanthropy.com/news/effort-to-spur-giving-from-donor-advised-funds-online-appears-to-stall/) |
| A2 | DAF Direct | Y1 | U | 1 | **1** | one_scorer_unknown | only blind scored: DAF Direct's own terms/about/privacy pages describe a recommendation widget with data shared only with the three sponsors and no API; positive product evidence, not absence; accepted | [source](https://www.dafdirect.org/) |
| A2 | Every.org | X1 | 1 | 2 | **2** | disputed-provider gap | blind's CY2024 990-PF ($47.3M disbursements; IRS XML shows $44.9M granted) is primary evidence and outranks primary's vendor_claim; better-evidenced score wins | [source](https://projects.propublica.org/nonprofits/organizations/611913297) |
| A2 | Every.org | X2 | U | 3 | **2** | one_scorer_unknown | only blind scored; live API/webhook docs and payout help page show delivery, but no tracked announcements and the API excludes disbursements; scored 2 (mixed) not 3 | [source](https://docs.every.org/docs/intro) |
| A2 | Every.org | X5 | U | 2 | **2** | one_scorer_unknown | only blind scored; Every.org funding page (Gates, Fidelity Charitable Catalyst Fund) and $9.7M assets; accepted | [source](https://support.every.org/hc/en-us/articles/360058165794-How-is-Every-org-funded) |
| A2 | Every.org | Y1 | 2 | 3 | **2** | disputed-provider gap | same evidence for both; the docs state 'no programmatic donations or disbursements via API', so for an A2 rail the API is partial; primary's reading fits the rubric | [source](https://docs.every.org/docs/intro) |
| A2 | Fidelity Charitable EFT (Stripe/ACH) | X3 | 2 | U | **2** | one_scorer_unknown | primary cites Fidelity Charitable's own audited FS (entity-level, not an affiliate report); scored 2 as entity-level assurance without a rail-scoped control report, matching the PayPal Grant Payments consensus | [source](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf) |
| A2 | PayPal Grant Payments | X3 | U | 2 | **2** | one_scorer_unknown | only blind scored: parent's audited 10-K with ICFR attestation, no product-scoped SOC; entity-level assurance = 2 | [source](https://investor.pypl.com/financials/sec-filings/default.aspx) |
| A3 | AEF | Y1 | U | 1 | **1** | one_scorer_unknown | only blind scored: AEF DC-sunset notice documents that only two years of history moved to the Ren portal (export limitation); accepted | [source](https://engage.aefonline.org/dc-sunset/) |
| A3 | BofA Charitable Gift Fund | X3 | U | 1 | **U** | one_scorer_unknown | blind's 1 rests on 'Form 990 only; no audit/SOC published', which is absence of assurance evidence; methodology: absence = U | [source](https://projects.propublica.org/nonprofits/organizations/46010342/202503219349318170/full) |
| A3 | Charityvest (adviser programs) | X3 | 2 | 1 | **3** | disputed-provider gap | adjudicator retrieved the audited FY2024/2023 statements both scorers missed (primary could not open; blind saw only the 2019 draft); published audit with administrator note = 3 | [source](https://guide.charityvest.org/governance-and-legal/financial-reporting) |
| A3 | Charityvest (adviser programs) | X6 | 2 | U | **2** | one_scorer_unknown | only primary scored; 4 forum records, none high/critical; held at 2 because the sample is too small for the 'low rate' anchor | [source](https://www.bogleheads.org/forum/viewtopic.php?t=417491) |
| A3 | Charityvest (adviser programs) | Y1 | U | 1 | **U** | one_scorer_unknown | blind's evidence is Foundation Source's DAF OS marketing, not Charityvest's donor/adviser data rights, and its 1 rests on 'no public API' (absence); U | [source](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/) |
| A3 | DAFgiving360 | X2 | U | 3 | **3** | one_scorer_unknown | only blind scored; CY2025 results validated (V2A-08) and Chariot DAFpay integration live (E109); accepted | [source](https://www.dafgiving360.org/press-release/2025-results) |
| A3 | DAFgiving360 | X3 | U | 2 | **U** | one_scorer_unknown | blind's 2 rests on a financials page whose statements could not be read (403 again on 2026-11-14); an unread page is not assurance evidence; U | [source](https://www.dafgiving360.org/about-dafgiving360/financials) |
| A3 | DAFgiving360 | Y1 | U | 2 | **2** | one_scorer_unknown | only blind scored; DAFgiving360 exposes donor/fund/grant endpoints to Chariot DAFpay (partner API, confirmed edge E109); partial API = 2 | [source](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md) |
| A3 | Fidelity Charitable | Y3 | 1 | U | **1** | one_scorer_unknown | only primary scored; virtual-assistant terms are admissible evidence of a navigation-only AI feature with no governed automation; blind's U treated absence of controls as absence of evidence | [source](https://www.fidelitycharitable.org/legal/virtual-assistant.html) |
| A3 | GiveClear | Y1 | U | 0 | **1** | one_scorer_unknown | blind's TIFIN Terms §5.3 restriction is admissible positive evidence, but §8 leaves content ownership with client/user (queue-contract-data-rights-agent-controls.md), so not a full 0; aligned with the agreed A1 TIFIN Give Y1 = 1 | [source](https://intercom.help/give-ria/en/articles/10092486-terms-of-use) |
| A3 | GiveClear | Y3 | 1 | U | **1** | one_scorer_unknown | only primary scored: Louise announced as executing donor requests with no published controls; newer evidence shows GiveClear's grant review still precedes payment (granting FAQ); 1 retained | [source](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html) |
| A3 | Goldman Sachs Philanthropy Fund | X3 | U | 1 | **U** | one_scorer_unknown | blind's 1 rests on 'Form 990 filed; no published audit or SOC' (absence); U | [source](https://projects.propublica.org/nonprofits/organizations/311774905/202503109349303645/full) |
| A3 | Morgan Stanley GIFT | X3 | U | 1 | **U** | one_scorer_unknown | blind's 1 rests on absence of audit/SOC; Ren's contradictory SOC claims are not imputed to the sponsor; U | [source](https://projects.propublica.org/nonprofits/organizations/527082731/202503239349300435/full) |
| A3 | NCF | X3 | U | 3 | **3** | one_scorer_unknown | only blind scored; adjudicator opened the 2025 consolidated FS (Capin Crouse): independent auditor's report present; accepted | [source](https://site.ncfgiving.com//wp-content/uploads/2026/07/NCF-25-Consolidated-FS-Final.pdf) |
| A3 | NCF | X5 | 3 | 4 | **4** | disputed-provider gap | audited statements confirmed plus operation since 1982: meets the 4 anchor; blind better evidenced | [source](https://site.ncfgiving.com//wp-content/uploads/2026/07/NCF-25-Consolidated-FS-Final.pdf) |
| A3 | NPT | X2 | U | 2 | **2** | one_scorer_unknown | only blind scored; grant volume confirmed (V1-14) but FY2025 grant figure inconsistent across NPT's own documents (V2B-06); mixed = 2 | [source](https://www.nptrust.org/annual-reports/npt-annual-report/) |
| A3 | NPT | X3 | U | 3 | **2** | one_scorer_unknown | blind scored 3 without inspection; adjudicator opened the linked 'consolidated statements 2024' PDF: a 2-page statement of financial position with no auditor's report or notes, so 2 not 3 | [source](https://www.nptrust.org/consolidated-statements-2024-npt/) |
| A3 | Renaissance Charitable Foundation | Y1 | U | 2 | **2** | one_scorer_unknown | only blind scored; Ren RCF MSA template returns customer materials on request, API a paid add-on (sponsor-level contractual export); consistent with Ren A1 Y1 = 2 | [source](https://www.reninc.com/wp-content/uploads/2025/08/Online-RCF-MSA_v1.pdf) |
| A3 | Vanguard Charitable | X3 | 3 | 4 | **3** | disputed-provider gap | both cite the audited FY2025/26 statements; related-party fee notes are audited disclosure but not control disclosures, so 3 not 4 | [source](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf) |
| A3 | Vanguard Charitable | Y1 | U | 1 | **U** | one_scorer_unknown | blind's evidence is Give Interactive's 'open API' marketing (another entity, go-live undisclosed) with no Vanguard export/API documented; U | [source](https://www.giveinteractive.com/) |
| A3 | Vanguard Charitable | Y4 | U | 2 | **2** | one_scorer_unknown | only blind scored; Vanguard Charitable's published policies address individual investors and advisers; two segments = 2 | [source](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) |
| A4 | Charityvest (direct) | X3 | 2 | 1 | **3** | disputed-provider gap | adjudicator retrieved the audited FY2024/2023 statements both scorers missed; published audit with administrator related-party note = 3 | [source](https://guide.charityvest.org/governance-and-legal/financial-reporting) |
| A4 | Charityvest (direct) | X6 | 2 | 3 | **2** | disputed-provider gap | blind's 3 ('low severe rate') rests on 4 low-severity records and 0 Trustpilot reviews; the complaints study says no comparable rates exist; primary's 2 better fits the evidence | [source](https://www.bogleheads.org/forum/viewtopic.php?t=417491) |
| A4 | Charityvest (direct) | Y1 | U | 1 | **U** | one_scorer_unknown | blind's evidence is the administrator's DAF OS marketing, not Charityvest's donor data rights; 1 rests on absence; U | [source](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/) |
| A4 | DAFgiving360 (direct) | X2 | U | 3 | **3** | one_scorer_unknown | only blind scored; CY2025 results validated (V2A-08); accepted | [source](https://www.dafgiving360.org/press-release/2025-results) |
| A4 | DAFgiving360 (direct) | X3 | U | 2 | **U** | one_scorer_unknown | financials page unreadable (403); not assurance evidence; U | [source](https://www.dafgiving360.org/about-dafgiving360/financials) |
| A4 | DAFgiving360 (direct) | Y1 | U | 2 | **2** | one_scorer_unknown | only blind scored; DAFpay provider endpoints (partner API); accepted | [source](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md) |
| A4 | Daffy | X3 | U | 1 | **U** | one_scorer_unknown | blind's 1 rests on 'Form 990 only; no audit or SOC found' (absence); U | [source](https://projects.propublica.org/nonprofits/organizations/863177440/202513209349301201/full) |
| A4 | Daffy | Y4 | 3 | 1 | **3** | gap_gt_1 | gap > 1. Adjudicator opened the Daffy for Work page: workplace programme live since 2023, extended 2024, stock matching Apr 2026; plus individual/family members and fintech/developer partners; blind missed the workplace segment | [source](https://www.daffy.org/resources/daffy-for-work-stock-matching) |
| A4 | Endaoment | X2 | U | 3 | **3** | one_scorer_unknown | only blind scored; committed audits published and public API docs live (docs.endaoment.org); accepted | [source](https://blog.endaoment.org/blog/2022-2023-fiscal-audits-complete) |
| A4 | Endaoment | X3 | U | 3 | **3** | one_scorer_unknown | only blind scored; adjudicator opened the FY22-23 audit PDF (independent auditor's report, unmodified opinion); accepted, noting it is the latest published year | [source](https://storage.googleapis.com/endaoment-static/docs-assets/audit-fy22-23.pdf) |
| A4 | Endaoment | Y2 | 2 | 3 | **3** | disputed-provider gap | blind cites live docs (async grant API, entity transfers, on-chain records) that primary did not; better-evidenced score wins | [source](https://docs.endaoment.org/advisors/about/platform-recordkeeping.md) |
| A4 | Endaoment | Y3 | U | 2 | **3** | one_scorer_unknown | only blind scored (2); newer evidence (queue-contract-data-rights-agent-controls.md) documents required idempotency keys, a cancel window while PendingLiquidation, Endaoment review of every API grant and Recommendation objects: deployed automation with documented authority separation = 3, consistent with Chariot Disbursements | [source](https://docs.endaoment.org/llms.txt) |
| A4 | Endaoment | Y5 | 2 | 3 | **3** | disputed-provider gap | blind cites first-party docs for API entity transfers and on-chain history; primary relied on a capped marketing claim; better-evidenced score wins | [source](https://docs.endaoment.org/llms.txt) |
| A4 | Every.org | X1 | U | 1 | **1** | one_scorer_unknown | only blind scored; 990-PF has no Schedule D DAF data; revenue $51.4M, net assets $9.0M; verifiable but small = 1 | [source](https://projects.propublica.org/nonprofits/organizations/611913297) |
| A4 | Every.org | X3 | U | 1 | **U** | one_scorer_unknown | blind's 1 rests on '990 only; no audit/SOC found' (absence); U | [source](https://projects.propublica.org/nonprofits/organizations/611913297) |
| A4 | Every.org | X4 | U | 2 | **2** | one_scorer_unknown | only blind scored; nonprofit donate network and multi-rail payout partners are admissible distribution evidence (secondary); accepted | [source](https://support.every.org/hc/en-us/articles/360059998673-How-long-does-it-take-for-my-donation-to-reach-the-nonprofit) |
| A4 | Every.org | X5 | U | 2 | **2** | one_scorer_unknown | only blind scored; private nonprofit funded by philanthropy, thin net assets; accepted | [source](https://projects.propublica.org/nonprofits/organizations/611913297) |
| A4 | Every.org | Y2 | U | 3 | **2** | one_scorer_unknown | only blind scored (3); the same payout evidence was scored 2 by both scorers in A2 (batched, PayPal Grants every 4-5 weeks); aligned to 2 | [source](https://support.every.org/hc/en-us/articles/360059998673-How-long-does-it-take-for-my-donation-to-reach-the-nonprofit) |
| A4 | Every.org | Y4 | U | 2 | **2** | one_scorer_unknown | only blind scored; vendor_claim (capped 2) of consumer donors and nonprofits; accepted | [source](https://support.every.org/hc/en-us/articles/360061886773-Does-Every-org-charge-fees) |
| A4 | Every.org | Y5 | U | 2 | **2** | one_scorer_unknown | only blind scored; vendor_claim (accepts DAF grants from other sponsors; multi-rail payout); accepted | [source](https://www.every.org/daf-donations) |
| A4 | Fidelity Charitable (direct) | Y3 | 1 | U | **1** | one_scorer_unknown | only primary scored; virtual-assistant terms (navigation only, no authority); accepted | [source](https://www.fidelitycharitable.org/legal/virtual-assistant.html) |
| A4 | Givinga consumer accounts | X4 | 2 | U | **2** | one_scorer_unknown | only primary scored; vendor_claim (employer, adviser and white-label channels on givinga.com / givingafoundation.org), capped at 2; no consumer-specific edge | [source](https://www.givinga.com/) |
| A4 | Givinga consumer accounts | Y2 | 2 | U | **2** | one_scorer_unknown | only primary scored; vendor_claim of payment processing and automated charity vetting, capped at 2 | [source](https://www.givinga.com/) |
| A5 | Benevity validation | X6 | 2 | U | **2** | one_scorer_unknown | only primary scored; Trustpilot/corpus records (17 nonprofit praise vs ~9 high-severity delay complaints; $35-or-8% check fee) are admissible; mixed = 2 | [source](https://www.trustpilot.com/review/benevity.com) |
| A5 | Benevity validation | Y2 | 2 | 3 | **3** | disputed-provider gap | blind cites Benevity's nonprofit-eligibility page (adjudicator verified: daily sanctions/watchlist screening, deactivation, appeals with paused disbursements); outranks primary's capped 'continuously validated' claim | [source](https://benevity.com/nonprofit-eligibility) |
| A5 | Benevity validation | Y5 | 2 | U | **2** | one_scorer_unknown | only primary scored; Alaya-to-Benevity migration path is documented migration support; accepted | [source](https://causeshelp.benevity.org/hc/en-us/articles/44498461447572-The-Alaya-product-is-moving-to-Benevity) |
| A5 | Chariot verification | Y5 | U | 2 | **2** | one_scorer_unknown | only blind scored; verification feeds multiple DAF providers via DAFpay but two of six sources are undisclosed; partial = 2 | [source](https://help.givechariot.com/onboarding/trust-and-safety/compliance) |
| A5 | Goodstack | X1 | U | 3 | **3** | one_scorer_unknown | only blind scored; Google for Nonprofits help page names Goodstack as its verifier (independent customer confirmation) and corroborates the vendor's 7.5M verifications; accepted | [source](https://support.google.com/nonprofits/answer/12016036?hl=en) |
| A5 | Goodstack | X2 | U | 3 | **3** | one_scorer_unknown | only blind scored; live verification at Google plus documented API and hosted flows; accepted | [source](https://support.google.com/nonprofits/answer/12016036?hl=en) |
| A5 | Goodstack | X4 | U | 3 | **2** | one_scorer_unknown | only blind scored (3); only the Google edge is independently confirmed; Canva, Atlassian, LinkedIn, ElevenLabs are vendor-listed logos (vendor_claim cap); scored 2 | [source](https://support.google.com/nonprofits/answer/12016036?hl=en) |
| A5 | Goodstack | X5 | U | 2 | **2** | one_scorer_unknown | only blind scored; $28M Series A (General Catalyst, Nov 2024) re-confirmed in emerging-entrants file; accepted | [source](https://tech.eu/2024/11/18/goodstack-secures-28m-from-general-catalyst/) |
| A5 | Goodstack | X6 | U | 2 | **2** | one_scorer_unknown | only blind scored; 741 Trustpilot reviews mixed; Google cites 3-5 business-day reviews; accepted | [source](https://uk.trustpilot.com/review/goodstack.org) |
| A5 | Goodstack | Y3 | U | 2 | **2** | one_scorer_unknown | only blind scored; automated verification with document fallback and the partner sets eligibility (Goodstack does not decide); accepted | [source](https://support.google.com/nonprofits/answer/12016036?hl=en) |
| A5 | IRS BMF / Pub 78 / TEOS (public baseline) | X3 | 3 | U | **3** | one_scorer_unknown | only primary scored; Rev. Proc. 2018-32 reliance standard (secondary source) is admissible statutory assurance; accepted | [source](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/) |

## 4. Consensus positions

Bands are given in parentheses. "Calibration status" is defined in §1.5. Within each area, rows are sorted by consensus X.

### A1: DAF platform and administration

| Provider | X point (band) | Y point (band) | Coverage X / Y | Consensus quadrant | Primary / blind quadrant | Calibration status |
|---|---|---|---|---|---|---|
| NPT GivingPoint (sponsor-built) | 3.1 (2.33–3.33) | 1.73 (1.12–2.52) | 0.75 / 0.65 | Scale Operators | insufficient evidence / Scale Operators (boundary) | **adjudicated** |
| Fidelity Charitable (in-house, FMR-administered) | 3.06 (2.6–3.2) | 1.57 (1.57–1.57) | 0.85 / 1.0 | Scale Operators | Proven Leaders (boundary) / Scale Operators | **adjudicated** |
| Ren (incl. iPhi/Stellar, DonorFirstX) | 2.81 (2.52–2.93) | 2.33 (2.33–2.33) | 0.9 / 1.0 | Proven Leaders | Proven Leaders / Proven Leaders | **reproduced** |
| SVCF (sponsor-built, Salesforce) | 2.64 (1.45–3.25) | 2.0 (0.3–3.7) | 0.55 / 0.15 | insufficient evidence | insufficient evidence / insufficient evidence | **insufficient evidence** |
| NCF (sponsor-built, Salesforce) | 2.63 (1.98–2.98) | 1.0 (0.15–3.55) | 0.75 / 0.15 | insufficient evidence | insufficient evidence / insufficient evidence | **insufficient evidence** |
| Give Interactive | 2.47 (1.98–2.77) | 2.08 (2.08–2.08) | 0.8 / 1.0 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders (boundary) | **reproduced** |
| TIFIN Give | 2.44 (2.2–2.6) | 1.93 (1.93–1.93) | 0.9 / 1.0 | Scale Operators (boundary) | Scale Operators (boundary) / Proven Leaders (boundary) | **adjudicated** |
| Foundation Source (DAF OS / Vennfi) | 2.27 (1.7–2.7) | 2.03 (1.73–2.33) | 0.75 / 0.85 | Proven Leaders (boundary) | Proven Leaders (boundary) / Scale Operators (boundary) | **adjudicated** |
| Foundant CommunitySuite | 2.1 (2.1–2.1) | 1.9 (1.43–2.42) | 1.0 / 0.75 | Scale Operators (boundary) | Scale Operators (boundary) / Proven Leaders (boundary) | **adjudicated** |
| Blackbaud Financial Edge NXT (foundations) | 1.88 (1.88–1.88) | 2.09 (1.77–2.38) | 1.0 / 0.85 | Forward Builders (boundary) | insufficient evidence / Forward Builders (boundary) | **adjudicated** |
| Givinga | 1.77 (0.98–2.77) | 1.73 (0.95–2.75) | 0.55 / 0.55 | Focused Specialists (boundary) | insufficient evidence / Focused Specialists | **adjudicated** |
| NPact (FIMS / DonorCentral) | 1.5 (1.12–2.12) | 1.04 (0.62–2.23) | 0.75 / 0.6 | Focused Specialists | Focused Specialists / Focused Specialists | **reproduced** |

### A2: Grant disbursement and nonprofit-side rails

| Provider | X point (band) | Y point (band) | Coverage X / Y | Consensus quadrant | Primary / blind quadrant | Calibration status |
|---|---|---|---|---|---|---|
| Fidelity Charitable EFT (Stripe/ACH) | 2.9 (2.9–2.9) | 1.82 (1.55–2.15) | 1.0 / 0.85 | Scale Operators (boundary) | Proven Leaders (boundary) / Scale Operators | **adjudicated** |
| PayPal Grant Payments | 2.72 (2.45–2.85) | 2.41 (2.05–2.65) | 0.9 / 0.85 | Proven Leaders | Proven Leaders / Proven Leaders | **reproduced** |
| Chariot Disbursements | 2.44 (2.2–2.6) | 3.17 (3.17–3.17) | 0.9 / 1.0 | Proven Leaders | Proven Leaders / Proven Leaders | **reproduced** |
| Chariot DAFpay | 2.2 (2.2–2.2) | 2.88 (2.88–2.88) | 1.0 / 1.0 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders | **reproduced** |
| Ren Rapid Disbursement Engine | 2.17 (1.95–2.35) | 2.15 (2.15–2.15) | 0.9 / 1.0 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders (boundary) | **reproduced** |
| Every.org | 2.0 (1.5–2.5) | 2.24 (1.9–2.5) | 0.75 / 0.85 | Proven Leaders (boundary) | insufficient evidence / Proven Leaders | **adjudicated** |
| DAF Direct | 1.53 (1.15–2.15) | 1.47 (1.25–1.85) | 0.75 / 0.85 | Focused Specialists | Forward Builders (boundary) / Focused Specialists | **adjudicated** |

### A3: Sponsors for the adviser / wealth channel

| Provider | X point (band) | Y point (band) | Coverage X / Y | Consensus quadrant | Primary / blind quadrant | Calibration status |
|---|---|---|---|---|---|---|
| DAFgiving360 | 3.18 (2.7–3.3) | 2.0 (1.7–2.3) | 0.85 / 0.85 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders (boundary) | **reproduced** |
| Fidelity Charitable | 3.12 (3.12–3.12) | 1.65 (1.65–1.65) | 1.0 / 1.0 | Scale Operators | Scale Operators (boundary) / Scale Operators | **reproduced** |
| NPT | 3.11 (2.8–3.2) | 1.92 (1.15–2.75) | 0.9 / 0.6 | Scale Operators (boundary) | Scale Operators (boundary) / Scale Operators (boundary) | **reproduced** |
| Renaissance Charitable Foundation | 3.06 (2.75–3.15) | 2.15 (2.15–2.15) | 0.9 / 1.0 | Proven Leaders (boundary) | Proven Leaders / Proven Leaders (boundary) | **reproduced** |
| NCF | 2.95 (1.48–3.48) | 1.5 (0.22–3.62) | 0.5 / 0.15 | insufficient evidence | insufficient evidence / insufficient evidence | **insufficient evidence** |
| Vanguard Charitable | 2.93 (2.93–2.93) | 1.83 (1.1–2.7) | 1.0 / 0.6 | Scale Operators (boundary) | insufficient evidence / Scale Operators | **adjudicated** |
| Morgan Stanley GIFT | 2.73 (1.5–3.3) | 1.5 (0.22–3.62) | 0.55 / 0.15 | insufficient evidence | insufficient evidence / insufficient evidence | **insufficient evidence** |
| Goldman Sachs Philanthropy Fund | 2.55 (1.4–3.2) | 1.0 (0.15–3.55) | 0.55 / 0.15 | insufficient evidence | insufficient evidence / insufficient evidence | **insufficient evidence** |
| BofA Charitable Gift Fund | 2.5 (1.38–3.18) | 1.0 (0.15–3.55) | 0.55 / 0.15 | insufficient evidence | insufficient evidence / insufficient evidence | **insufficient evidence** |
| AEF | 2.47 (2.23–2.62) | 1.29 (1.1–1.7) | 0.9 / 0.85 | Scale Operators | Scale Operators / Scale Operators | **reproduced** |
| Charityvest (adviser programs) | 2.1 (2.1–2.1) | 2.21 (1.33–2.92) | 1.0 / 0.6 | Proven Leaders (boundary) | Forward Builders (boundary) / Focused Specialists (boundary) | **adjudicated** |
| GiveClear | 2.06 (1.85–2.25) | 1.7 (1.7–1.7) | 0.9 / 1.0 | Scale Operators (boundary) | Proven Leaders (boundary) / Focused Specialists (boundary) | **adjudicated** |

### A4: Consumer and digital-first sponsors

| Provider | X point (band) | Y point (band) | Coverage X / Y | Consensus quadrant | Primary / blind quadrant | Calibration status |
|---|---|---|---|---|---|---|
| Fidelity Charitable (direct) | 3.23 (3.23–3.23) | 1.65 (1.65–1.65) | 1.0 / 1.0 | Scale Operators | Scale Operators (boundary) / Scale Operators | **reproduced** |
| DAFgiving360 (direct) | 3.18 (2.7–3.3) | 2.0 (1.7–2.3) | 0.85 / 0.85 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders (boundary) | **reproduced** |
| Daffy | 2.76 (2.35–2.95) | 2.65 (2.65–2.65) | 0.85 / 1.0 | Proven Leaders | Proven Leaders / Proven Leaders | **reproduced** |
| Endaoment | 2.17 (1.95–2.35) | 3.0 (3.0–3.0) | 0.9 / 1.0 | Proven Leaders (boundary) | Forward Builders / Proven Leaders (boundary) | **adjudicated** |
| Charityvest (direct) | 2.15 (2.15–2.15) | 2.21 (1.33–2.92) | 1.0 / 0.6 | Proven Leaders (boundary) | Proven Leaders (boundary) / Focused Specialists (boundary) | **adjudicated** |
| Every.org | 1.55 (0.85–2.65) | 2.0 (1.7–2.3) | 0.55 / 0.85 | Forward Builders (boundary) | insufficient evidence / Forward Builders | **adjudicated** |
| Givinga consumer accounts | 1.45 (0.8–2.6) | 2.0 (0.8–3.2) | 0.55 / 0.4 | insufficient evidence | insufficient evidence / insufficient evidence | **insufficient evidence** |

### A5: Charity eligibility and verification data

| Provider | X point (band) | Y point (band) | Coverage X / Y | Consensus quadrant | Primary / blind quadrant | Calibration status |
|---|---|---|---|---|---|---|
| IRS BMF / Pub 78 / TEOS (public baseline) | 3.45 (3.45–3.45) | 3.18 (2.7–3.3) | 1.0 / 0.85 | Proven Leaders | Proven Leaders / Proven Leaders | **reproduced** |
| Candid (GuideStar APIs / Charity Check) | 3.03 (2.28–3.28) | 2.62 (2.62–2.62) | 0.75 / 1.0 | Proven Leaders | Proven Leaders / Proven Leaders | **reproduced** |
| Benevity validation | 2.53 (2.15–2.75) | 2.17 (2.17–2.17) | 0.85 / 1.0 | Proven Leaders (boundary) | Scale Operators (boundary) / Proven Leaders | **adjudicated** |
| Goodstack | 2.45 (2.45–2.45) | 2.47 (1.98–2.77) | 1.0 / 0.8 | Proven Leaders | insufficient evidence / Proven Leaders | **adjudicated** |
| Chariot verification | 2.22 (2.0–2.4) | 2.55 (2.55–2.55) | 0.9 / 1.0 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders (boundary) | **reproduced** |

### 4.1 Status summary

| Area | Reproduced | Adjudicated | Insufficient evidence |
|---|---|---|---|
| A1 | 3 (Ren, Give Interactive, NPact) | 7 | 2 (NCF, SVCF) |
| A2 | 4 (Chariot Disbursements, Chariot DAFpay, PayPal Grant Payments, Ren RDE) | 3 (Fidelity EFT, DAF Direct, Every.org) | 0 |
| A3 | 5 (Fidelity, DAFgiving360, NPT, RCF, AEF) | 3 (Vanguard, Charityvest, GiveClear) | 4 (GS PF, MS GIFT, BofA CGF, NCF) |
| A4 | 3 (Fidelity direct, DAFgiving360 direct, Daffy) | 3 (Endaoment, Charityvest direct, Every.org) | 1 (Givinga consumer) |
| A5 | 3 (IRS baseline, Candid, Chariot verification) | 2 (Benevity, Goodstack) | 0 |
| **All** | **18** | **18** | **7** |

**What the consensus changes:**
- **Seven providers become plottable that a scorer could not plot.** Insufficient-evidence status falls from 14 providers (pre-adjudication status) to 7:
  - Blackbaud, Givinga and NPT GivingPoint in A1
  - Every.org in A2
  - Vanguard in A3
  - Every.org in A4
  - Goodstack in A5
- **Every disputed provider gets a single label.** Nine of the 11 land on a boundary.
- **Robust positions.** These keep the same base quadrant across all three score sets and are not boundary in the consensus:
  - Proven Leaders: Ren (A1), Chariot Disbursements and PayPal Grant Payments (A2), Daffy (A4), Candid and the IRS baseline (A5).
  - Scale Operators: AEF (A3), Fidelity Charitable (A3, A4).
  - Focused Specialists: NPact (A1).

**Scope notes that qualify individual rows:**
- **NPT GivingPoint (A1) is not sponsor-built.** Newer evidence shows the GivingPoint front end is built by Ren and hosted on Ren's `ren-workload-02` iPhi infrastructure ([vendor-scope file §0, §3](queue-vendor-scope-ren-denominator.md)). The row now describes NPT's book on Ren technology. Methodology v1.1 should fold it into Ren. Doing so would lift Ren's X1 from 3.5 toward 4: publicly evidenced Ren technology covers about 26–28% of DAFRC FY2024 assets.
- **Blackbaud FE NXT (A1) is borderline in scope.** It is a general ledger, not a DAF subledger. Its plot rests on X1 = 1 from a single community-foundation case study.
- **Every.org's A2 position (X = 2.00) sits exactly on the midline**, and its in-scope DAF rail function is thin.

## 5. AI-governance overlay (flag, not axis)

The rule tested is "AI may add a flag, never clear one" ([ai-governance-failure-modes.md](ai-governance-failure-modes.md)).

| Area | Provider | Evidenced AI / automation | Consensus flag |
|---|---|---|---|
| A1 / A3 | TIFIN Give / GiveClear | Louise is announced as able to "execute real donor requests", and no Louise controls are published. Newer evidence ([contract file §3.2](queue-contract-data-rights-agent-controls.md)) shows GiveClear still reviews and approves every grant before payment. | **AMBER (high).** Downgraded from the primary scorer's RED-candidate because sponsor approval survives. Limits, confirmation and logs are still undocumented. |
| A4 | Daffy | Deployed MCP server and CLI that move money. Confirmation happens only on the client side. No spend limits or scopes. Daffy accepts or rejects after submission. | **AMBER**: real money movement, with approval delegated to the AI client |
| A5 | Benevity | Match Assurance AI verifies eligibility and auto-submits (vendor claim). AI grant scoring is announced with "admin final control". | **AMBER / at risk**: AI may effectively clear eligibility, and human override is undocumented |
| A1 | Foundant | Fia beta (agents, policy engine, bias screening), with controls claimed but not documented | **AMBER** |
| A1 | Give Interactive | "AI tools" marketing, and AI grantmaking modules described as "stay tuned" | **AMBER-unverified** |
| A1 | Foundation Source | New CTO and Head of Product with an "increased focus on AI"; intent only | **WATCH** |
| A5 | Goodstack | "AI-powered automation/reviews" claims (class U). The partner sets eligibility. | **Unverified; consistent in design** |
| A1 / A3 / A4 | Fidelity Charitable | Navigation-only virtual assistant with disclaimers. No decision authority. | **GREEN** |
| A1 / A2 / A3 | Ren, Ren RDE, RCF, AEF | Rule-based "instant" approval under RCF's published, risk-tiered policy. No AI. | **GREEN / none.** The decision logs are not public. |
| A2 / A5 | Chariot (Disbursements, DAFpay, verification) | No AI in the payment or eligibility decision. Records `approved_by`. LLM gift coding is a separate product (class D). | **Consistent**: the sponsor keeps final authority by contract |
| A4 | Endaoment | No AI. API grants are held for Endaoment review, with idempotency and a cancel window. | **Consistent**: a reference design |
| A5 | Candid | AI assistant and a read-only MCP connector | **Consistent (read-only)** |
| A1 | Blackbaud | Development Agent with human supervision (Raiser's Edge NXT, not FE NXT) | **None for FE NXT** |
| All others | NPact, Givinga, NPT, NCF, SVCF, Vanguard, DAFgiving360, GS PF, MS GIFT, BofA CGF, PayPal Grant Payments, Fidelity EFT, DAF Direct, Every.org, IRS | None evidenced (Every.org's API moves no money) | **None.** Absence of evidence does not mean no AI is in use. |

## 6. Evidence gaps that would move positions

These are ranked by how many positions the gap could change. Proposed questions are in `queue-proposals-quadrant-calibration.csv`.

1. **Y-axis evidence for wealth-captive and faith sponsors (GS PF, MS GIFT, BofA CGF, NCF).** Their Y coverage is 0.15, so 4 of the 7 remaining insufficient-evidence rows are in A3. The missing items are program circulars covering grant rails, data export and transfer-out terms. MS GIFT and GS PWM now run on Ren DFX/iPhi, so Ren's templates bound what is possible. (P-QCAL-04)
2. **DAFgiving360 sits at Y = 2.00 exactly in A3 and A4.** Three things would settle it: its payment rail (EFT share against "only paper checks" reports), its audited statements (the page returned 403 twice), and its outbound transfer terms. Any one of them decides Proven Leaders or Scale Operators. (P-QCAL-02)
3. **Fidelity's electronic-only grant status and donor data export.** These move Fidelity EFT (A2, Y = 1.82) and Fidelity Charitable (A1, A3, A4) toward the Y midline. Public statements still conflict. (P-QCAL-03)
4. **TIFIN Louise's action path.** If Louise-initiated grants are documented to pass GiveClear approval, with limits and logs, Y3 rises from 1 to 2–3. That would move TIFIN Give (Y = 1.93) and GiveClear (Y = 1.70) across or onto the midline. (P-QCAL-06)
5. **The scope of the NPT–Ren relationship.** The question is whether Ren supplies only the front end or also the ledger. The answer decides whether the NPT GivingPoint row is merged into Ren, and whether Ren's X1 reaches 4. (P-QCAL-01)
6. **Charityvest and Vanguard Y1/Y3, where Y coverage is 0.6.** Neither documents donor data export. Vanguard's Give Interactive go-live is undisclosed. Charityvest sits on the boundary on both axes in A3 and A4. (P-QCAL-05)
7. **Rubric harmonisation between scorers.** Two places need it:
   - **A3 X1 thresholds.** The primary scorer used 2 = $1–7bn and 4 = ≥$40bn. The blind scorer used 2 = $0.5–5bn and 4 = ≥$20bn. The blind bands match the methodology's anchor (2 = "<$5bn").
   - **Sponsor X3.** "Form 990 only" was scored 1 by one scorer and U by the other. The consensus applies "absence = U".

   Both should become area notes in methodology v1.1. Otherwise the next re-score will reproduce the same 1-point drift. (P-QCAL-07)
8. **Other unknowns.**
   - SOC report scope for every A1/A2 vendor. Ren's Type I/II conflict holds X3 = 1 for Ren, RDE and AEF.
   - Scale-normalised complaint rates (X6 is U for most vendors).
   - Every.org's DAF-specific scale.
   - Givinga's consumer channel, plus its $316k "external bank fraud loss" line, which is not scored.

   These are already queued (P-QA1-04, P-QA3-04, P-QA3-07, P-INF-01).

## 7. Limits

- **The adjudicator is a single scorer.** Adjudicated positions are not independent reproductions. Under EDF they remain *internal-demonstration* until a third pass or new primary evidence confirms them.
- **Means hide judgement.** Rounding 1-point gaps to the 0.5 mean narrows apparent disagreement. Positions are bands, not ranks.
- **Inspection was partial.** Opened sources included the Charityvest, NCF, NPT and Endaoment financial documents, the Benevity eligibility page and the Daffy for Work page. The Google for Nonprofits help page returned 429, and the DAFgiving360 financials page returned 403. Cells resting on those pages use the scorers' recorded summaries.
- **Never compare positions across areas.** Fidelity Charitable, DAFgiving360, Charityvest and Every.org appear in more than one area and are scored separately in each.
