# Clarity and EDF applied to four post-baseline outcomes, with tags for the 33 direction docs (P-GAP19-12)

**Date:** 2026-11-19 · **Queue item:** P-GAP19-12 (`data/mission-2026-11-14/research-priority-queue.csv`, rank 45, EIV 48.0) · **Method guide:** [clarity-edf-application-guide.md](clarity-edf-application-guide.md)

**Framework versions.** These are the versions pinned in the guide, re-read locally on 2026-11-19 and not modified:
- Clarity `8cd48019b893a4ce42fe4c9dcc81dd81fb12d1ea` (`decision-posture-model.md`, `docs/reconsideration-criteria.md`);
- EDF `41fea6ffc764adc69643d5ee2940916592486f84` (`docs/edf/specification.md` v0.3, `docs/framework-engineering/claim-and-confidence-policy.md`).

**Outputs**
- This note.
- [`data/mission-2026-11-14/clarity-edf-direction-tags-2026-11-19.csv`](../../data/mission-2026-11-14/clarity-edf-direction-tags-2026-11-19.csv): 33 rows, one Clarity/EDF tag per direction doc.
- [`data/mission-2026-11-14/queue-proposals-g12.csv`](../../data/mission-2026-11-14/queue-proposals-g12.csv): two proposals, P-G12-01 and P-G12-02.

**Rules followed**
- **Numbers.** Every number is copied from the governing document named beside it, with that document's validation corrections applied. No validated number was changed. A derived figure would be marked [C]; this note adds none.
- **Scope.** The four outcomes are exactly the ones the queue text names. Two of them each combine two findings, as the queue text does.
- **Files not edited.** The queue item also asks for the results to be appended to `industry-incentives-structural-analysis.md` §6 and `incentive-map.csv`. §7 gives the rows. They were appended to both files in the same commit (`f2d5934`) and were accepted by validation wave 31B.
- **Labels.** [F] means the source states it; [C] is a repository computation; [I] is an inference.

---

## 0. How the frameworks were applied

**EDF claim states for repository findings.** The EDF policy's states are written for claims about EDF's own performance. Here they are applied to this repository's findings by three rules:
- **internal-demonstration.** A fact or count that this research process observed or computed and that a validation wave re-checked. The validators belong to the same process, so under the policy's *Independence* section their re-check is not independent replication. This is the strongest state the policy allows for these findings. It is the state that `incentive-map.csv` calls "documented".
- **suggestive.** An interpretation, attribution or classification where the evidence points one way but a material alternative remains.
- **unsupported.** A plausible mechanism with no evidence that could test it.

Confidence labels are the policy's five qualitative labels. They are not probabilities.

**Clarity posture.**
- Posture is set by two questions: the impact if the decision is wrong, and how correctable the decision is. Correctability covers recovery speed and cost and who bears the consequences.
- Posture is assigned to the **AI-native entrant's response**, not to the outcome itself.
- **Ambiguity in the pinned text.** The pinned `decision-posture-model.md` text puts Guardrail and Strategic in "Type 1 (low correctability)" and Fast and Experimental in Type 2. Its ASCII matrix draws Guardrail on the high-correctability side. This note follows the text:
  - **Fast:** low impact, easily reversible.
  - **Experimental:** reversible but uncertain; the aim is learning with a bounded blast radius.
  - **Guardrail:** high impact, where correctability is limited and the work runs inside regulatory or control boundaries.
  - **Strategic:** high impact and hard to reverse.

**Structural constraint or habit.** The test is the guide's. A behaviour is **structural** when a regulatory, legal-liability or financial origin holds it in place and the actor cannot change that control point alone. It is **habit** when only organizational or informational origins sustain it. It is **mixed** when the two kinds interact, which is the default.

---

## 1. Results in brief

| # | Outcome (factual) | Governing docs | Classification | Claim state (fact / classification) | Confidence (fact / classification) | Entrant response and posture |
|---|---|---|---|---|---|---|
| G12-1 | Community-foundation DAF admin fees sit well above the nationals' fees, and CF top-officer pay barely scales with size | direction-cf-consolidation-fees (wave 25A); direction-sponsor-executive-compensation (wave 28) | **Mixed, leaning structural** on the cost level (fixed whole-organisation cost over a small DAF base). **Habit** on fee opacity and on the absence of consolidation. | internal-demonstration / suggestive | High / Low-Medium | Lower-cost back office for one partner CF, on new funds only: **Experimental**. A full system-of-record migration would be **Strategic**. |
| G12-2 | Most surveyed sponsors (DAFRC, n=128, 86% CFs) do not pass full donor contact data to nonprofits by default. At the FY2024 top 20, a full-contact default is documented for 33.2% of assets and a withholding default for 17.2%; 44.6% is undocumented (P-B44N28-01) [V wave 34A] | direction-nonprofit-side-experience (wave 29) | **Mixed, leaning habit** | internal-demonstration / suggestive | Medium / Medium | Disclosure by consent per grant, with a "confidential" option: **Guardrail** |
| G12-3 | No open, multi-sponsor DAF grant-request standard exists | direction-data-standards-interoperability (wave 25B) | **Mixed:** a coordination habit plus a financial origin (vendor-governed rail economics) | internal-demonstration (absence) / suggestive | Medium-High / Low-Medium | Publish and implement a minimal open grant record: **Experimental**. Agent-submitted grants over it: **Guardrail**. |
| G12-4 | Fidelity's asset-allocation pools trail their composites over 5 years by about its first-tier admin fee (0.58–0.76 pp); its Money Market pool trails by 0.65 pp in every window. Over 1 and 3 years the asset-allocation pools are mostly above their composites [V wave 31B] | direction-investment-menus-performance (wave 27) | The shortfall is **structural** (fee arithmetic under an asset-based fee). The non-comparable reporting basis across sponsors is **habit**. | internal-demonstration / suggestive (attribution) | High / Medium-High | Report returns on a declared gross and net basis: **Fast**. Choose an asset-based or flat pricing model: **Strategic**. |

**What this does to existing conclusions.**
- Nothing here changes a validated figure.
- The four classifications are new. They extend report §3 and synthesis C/E as follows:
  - The CF cost gap is a cost-structure finding before it is a technology finding.
  - Donor-data withholding is mostly a default choice, not something the law requires.
  - The missing standard is a coordination gap that no single sponsor has a financial reason to close.
  - Fidelity's tracking gap is a disclosure-basis effect, not evidence of poor management.

---

## 2. G12-1. Community-foundation cost gap and flat CF pay

### EDF v0.3 sequence

1. **System context.**
   - *Primary system:* DAF administration pricing and staffing at community foundations.
   - *Context:* the top 100 CFs by FY2024 DAF assets (fee schedules from 2021 or later) and the top-50 sponsors' TY2021–2025 Form 990s.
   - *Focus:* why CF admin fees and per-dollar staffing cost sit far above the nationals' levels.
2. **Outcome (factual).**
   - **Fees.** The median effective admin fee is **100 / 100 / 67 bps at $100k / $1m / $10m across the 34 published schedules**. On the admin layer alone, the CF median is **about 1.7x the nationals at $100k, 2.2x at $1m and about 3.6–4.7x at $10m (67.2 bps against 18.8 and 14.3 bps)**. **Every published CF schedule is above 45 bps at $1m** [direction-cf-consolidation-fees §0, wave 25A].
   - **Pay.** The TY2024 median top-officer pay at community foundations is **$725,134**. Among the 21 CFs, the log-log slope of top-officer pay on total assets is **0.23 (r² 0.34)**. Top-officer pay per $bn of DAF assets is a **$733,697** median at CFs, against **$14,336** at NPT [direction-sponsor-executive-compensation §0 items 3–4]. Per $bn, community-foundation pay is **about 10–51× that of the four self-staffed nationals (9.6× AEF, 51× NPT)** [same doc, wave 28].
3. **Manifestations.**
   - Minimum fees: a median minimum annual fee of **$250** (n=24; range $50–$2,500) [direction-cf-consolidation-fees §0].
   - Fee opacity: **41** of the top 100 CFs had no fee terms found, and **7** have a fee page with no rates [same].
   - No fee data in the tail: **none of the 1,240 tail sponsors has a published fee in the repository**. Community foundations are **641** of them (51.7% of tail sponsors) [direction-long-tail-sponsors §0, wave 30].
   - Pooled CF Part IX lines 5–10 come to **78.7 bps** of DAF assets. The comparable figures are NPT 6.9, DAFgiving360 8.6 and Vanguard 5.6 bps, and **2.9 bps** for the affiliated-commercial group [direction-sponsor-executive-compensation §0 item 3].
   - CF advertising (line 12) is **18.4 bps** of DAF contributions, against **1.39 bps** for the affiliated-commercial nationals [direction-sponsor-marketing-spend §1].
   - Consolidation is rare: **19 events and no combination of two top-100 CFs** in 2021–2026 [direction-cf-consolidation-fees §0].
4. **Origin network.** No single root cause is claimed.
   - *Financial:*
     - The cost is a whole-organisation cost. CF pay "is whole-organisation pay", which also covers endowment and grantmaking programmes, so the DAF ratios overstate DAF-attributable pay [direction-sponsor-executive-compensation §0 item 3].
     - Pay barely scales with size (slope 0.23). That is consistent with a large fixed cost spread over a small DAF base. [I]
     - DAF fee revenue may cross-subsidise other CF programmes. **Not observed** [I].
   - *Organizational:*
     - The CF mission bundles local grantmaking, donor services and endowment stewardship.
     - CF boards are local, and consolidation needs a combining board's assent. The 19-event count suggests that path is rarely taken. [I]
   - *Informational:*
     - With 41 of 100 publishing no fee terms, donors cannot compare prices, so price pressure is weak. [I]
   - *Technical:*
     - Where a tail CF's vendor is identified, it is Foundant 80% of the time [direction-long-tail-sponsors §0]. The software cost per CF is a fixed input. Its size is **not observed**.
   - *Regulatory:*
     - **No rule found that sets or caps DAF fees.** Regulation is not an origin of the fee level.
   - *Environmental:*
     - Donors who choose a CF for local knowledge are not necessarily choosing on price. **Not measured** [I].
5. **Propagation.**
   - Financial: a fixed organisational cost is spread over a small DAF base, which gives high bps fees and minimum fees.
   - Informational: unpublished schedules mean weak comparison, which lets the fee persist.
   - Human: donors stay for local relationships, so there is little switching pressure.
6. **Evidence.**
   - *Direct:* fee schedules (34 published), filed pay and Part IX lines.
   - *Inference:* that fixed cost, not margin, drives the gap.
   - *Not observed:*
     - DAF-attributable cost at CFs;
     - DAF fee revenue as a share of CF operating revenue;
     - donor price elasticity.
7. **Control points.** These differ from the origins.
   1. Shared or outsourced DAF back-office administration (a CF consortium, a vendor or a white-label sponsor). It is within CF board control and carries mission and transition cost.
   2. Publishing fee schedules. This costs little and is within CF control.
   3. Lower fee tiers at large balances, which some CFs already have (NYCT's 50 bps flat).
   4. Vendor pricing, which is outside CF control.
8. **Control-point ranking** (heuristic; no scores).
   - By influence on the cost level: 1 > 3 > 2 > 4.
   - By controllability and cost: 2 > 3 > 1 > 4.
9. **Diagnostic sufficiency.**
   - Enough for an Experimental entrant pilot that takes cost out of one partner CF's new funds.
   - Not enough to size the saving or to claim the gap is margin rather than cost.

**Unknowns:** DAF-attributable CF cost (P-G12-01); the cross-subsidy share.
**Next responsible action:** separate DAF administration from other CF cost in top-100 CF audited statements (P-G12-01).

**Classification:** **Mixed, leaning structural** on the cost level, from a financial origin (fixed whole-organisation cost over a small DAF base) that a single CF cannot remove without changing its mission bundle. **Habit** on fee opacity and on the absence of consolidation (organizational and informational origins).
- Claim state: internal-demonstration (facts); suggestive (classification).
- Confidence: High (facts); Low-Medium (classification), because DAF-attributable cost is not observed.

### Clarity

- **Admissibility screen.**
  - *Rejected:* "CFs are inefficient". That substitutes motivation for incentives and is unbounded.
  - *Rejected:* "CF executives are overpaid". The slope shows pay is flat against size, not high against peers, and the national comparison excludes affiliated sponsors whose pay sits in the parent.
  - *Retained:* the bounded mechanism, "a fixed whole-organisation cost spread over a small DAF base".
- **What do I know?** The fee and pay figures above, both validated.
- **What is currently justified?** The cost gap is real at the admin layer. Its cause is most consistent with fixed cost.
- **Entrant response and posture.**
  - Offer one partner CF lower-cost administration for its *new* funds on the entrant's ledger. This is entry option S1 in [ai-native-entrant-simulation.md](ai-native-entrant-simulation.md) §6.
  - Impact if wrong is medium: the partner's donor trust and the entrant's cost of capital.
  - Correctability is high when the pilot is limited to new funds.
  - **Experimental.** Migrating a CF's existing system of record would be **Strategic**: high impact, slow and costly recovery, and the consequences land on the CF's donors.
- **I will reconsider if:**
  - CF audited statements or 990 functional splits show DAF administration costs well below the fee charged (margin or cross-subsidy). That would move the cost level toward habit or financial choice, and the entrant's price advantage would rest on margin rather than automation.
  - A top-100 CF consolidation, or a CF shared-services consortium, publishes a lower fee schedule. That would show the control point works.
  - The pre-2021 schedules at five top-100 CFs (§8) are refreshed and move the n=34 median.
- **Monitoring plan:** the annual CF fee census refresh; Schedule N events; CF 990 Part IX lines 5–10 trends (owner: whoever runs the CF fee census).

---

## 3. G12-2. Donor contact data withheld by default at most surveyed (CF-weighted) sponsors; mixed at the top 20 [V wave 34A]

### EDF v0.3 sequence

1. **System context.**
   - *Primary system:* donor-identity data passed from sponsor to recipient with a DAF grant.
   - *Context:* the DAFRC 2025 manager and donor surveys, FreeWill 2025–26, practitioner threads from 2022–2026, and the sponsor and vendor grant APIs.
   - *Focus:* why nonprofits often do not learn who recommended a grant.
2. **Outcome (factual).** **Only 36% of sponsors default to full contact information, and 35% default to fund name only.** The full set of defaults is full contact 36%, name only 24%, fund name only 35%, other 5% and anonymous 1% (DAFRC manager survey, n=128, 86% community foundations) [direction-nonprofit-side-experience §0 and §2.1, wave 29].
3. **Manifestations.**
   - Identity and data issues are **16** of 48 coded nonprofit-side rows, level with delay and checks (16).
   - FreeWill 2026: **72%** of nonprofits say not knowing which donors have a DAF is their biggest challenge; **20%** name anonymous gifts; **33%** flag DAF donors in their CRM [V].
   - Practitioners report that Fidelity will not tell a charity who sent an unidentified transfer [P].
   - All of the above: [direction-nonprofit-side-experience §0, §2.1].
   - Congregations are told to record the gift as from the sponsor and not to receipt the donor [direction-faith-giving-platforms §0, Subsplash].
4. **Origin network.**
   - *Organizational:* the default is set by the sponsor or its platform vendor, and it varies widely under one federal regime (36/24/35/1). On Ren's platform the stated default tracks guide version, not sponsor (b4428-02) [V wave 35B]. [I] The variation is the strongest sign that law does not dictate the default.
   - *Human (donor preference):*
     - **72%** of donors never or almost never give fully anonymously.
     - Among anonymous givers, **72%** want to avoid public recognition and **71%** want to avoid solicitation [same doc §2.1].
     - Preference is therefore a real origin for a minority, not a reason for a fund-name-only default for everyone. [I]
   - *Informational and technical:*
     - Grant metadata do not travel with the payment in any documented case.
     - ACH CCD allows one 80-character addenda.
     - All per [direction-data-standards-interoperability §0, wave 25B].
     - Donor-disclosure fields exist but are not shared across sponsors: `anonymous` (Chariot) and `shareMyEmail` (Endaoment) [same, §2.3].
     - No industry standard; the DAFRC authors call for one, with full contact as the default.
   - *Regulatory or legal:*
     - The sponsor is the legal donor, so the recipient acknowledges the sponsor, not the donor. That is consistent with the Subsplash guidance [I]. It governs *receipting*, not *contact disclosure*.
     - No rule was found that bars disclosing donor contact data with consent.
     - Privacy-law exposure for bank- or broker-affiliated sponsors is **not examined** in the repository.
   - *Financial:* a sponsor motive to keep the donor relationship (retention) is **unsupported**. No evidence was found, and the admissibility screen rejects it as intent without a signal.
5. **Propagation.**
   - Informational: a thin default means a gift arrives with the fund name only.
   - Organizational: staff de-duplicate and key data by hand [P].
   - Human: the donor is not thanked, and the donor later asks why no receipt arrived [P].
   - Financial: reporting and crediting gaps (CASE soft-credit rules depend on knowing the person) [same doc §2.1].
6. **Evidence.**
   - *Direct:* a survey of 128 managers, 86% of them CFs, so it does not represent the nationals. Donor survey; vendor surveys.
   - *Inference:* the default is a choice.
   - *Observed (P-B44N28-01, 2026-11-19):* first-party text exists for 15 of the top 20 (76.3% of FY2024 top-20 assets).
     - Full contact is the stated default at Fidelity, RCF, NCF, ImpactAssets and FFTC (33.2%).
     - Name or fund name only at Vanguard, MS GIFT, BofA, CCT and GKCCF (17.2%).
     - A required choice at SVCF and JCF (5.0%).
     - No stated default at NPT, AEF and CJP (20.9%).
     - DAFgiving360, GS DAF and Raymond James are blocked by robots, and Greater Horizons and Dechomai publish nothing relevant (23.7%).
     - No top-20 sponsor defaults to anonymous [V wave 34A]
7. **Control points.**
   1. The sponsor default setting. High influence, within sponsor control, low cost.
   2. A per-grant consent prompt with a "confidential" option, which the DAFRC authors suggest instead of "anonymous". High influence, within sponsor control.
   3. A shared donor-disclosure field in a grant record (links to G12-3). Medium influence; needs coordination.
   4. Nonprofit-side matching and CRM inference. Low influence, and it works around the problem rather than fixing it.
8. **Ranking:** 1 ≈ 2 > 3 > 4 by influence and controllability.
9. **Diagnostic sufficiency.**
   - Enough to justify a consent-first default in an entrant's own product.
   - P-B44N28-01 shows that, as a rule, the top 20 do not behave like the CF-heavy survey sample. By count, 5 of 15 determinable sponsors default to full contact, close to DAFRC's 36%. But only 5 of 15 withhold, against DAFRC's 59% for name or fund name only [V wave 34A]

**Unknowns:** national-sponsor defaults; donor opt-in rates when the default changes.
**Next responsible action:** run P-B44N28-01 (already queued).

**Classification:** **Mixed, leaning habit.** The sustaining origins are organizational and informational, and the regulatory origin governs receipting, not disclosure. A preference origin limits the change for a donor minority.
- Claim state: internal-demonstration (survey facts as reported by the repository); suggestive (classification).
- Confidence: Medium (facts, because the sample is CF-weighted); Medium (classification).

### Clarity

- **Admissibility screen.**
  - *Rejected:* "sponsors hide donors to protect their franchise". That is motivation without a signal.
  - *Rejected:* "79% of DAF gifts are partially anonymous". That figure is unverified per the governing doc §2.1 and P-B44N28-02.
- **What is currently justified?** The default is a sponsor choice, and its variation under one law shows it is changeable.
- **Entrant response and posture.**
  - Ask for disclosure consent on each grant (full contact / name only / confidential), with full contact preselected only if the donor opted in at onboarding.
  - Carry the choice in a structured field.
  - Impact if wrong is high for the individual: a disclosure cannot be recalled, and the harm lands on the donor.
  - **Guardrail.** Predefined consent boundaries and an audit log of every disclosure. Choosing the default wording within those boundaries is Experimental.
- **I will reconsider if:**
  - P-B44N28-01 shows the top-20 nationals already default to full contact. The problem would then be CF-specific and the entrant's edge smaller. **Outcome (validated, wave 34A): partly met.**
    - Fidelity, RCF, NCF, ImpactAssets and FFTC default to full contact (33.2% of top-20 assets).
    - Vanguard, MS GIFT, BofA, CCT and GKCCF do not (17.2%).
    - The default is undocumented for 44.6%, including DAFgiving360 (16.3%).
    - The classification stays mixed, leaning habit [V wave 34A]
  - A regulator, AG or court treats donor-data disclosure by a sponsor as a privacy violation, or as a §4967 benefit. That would move the classification toward structural.
  - Published opt-in rates under consent prompts fall below the current full-contact default share. The default would then reflect donor preference, not habit.
- **Monitoring plan:** the DAFRC survey's next edition; FreeWill's annual survey; sponsor help pages (owner: the nonprofit-side workstream).

---

## 4. G12-3. No open DAF grant-request standard

### EDF v0.3 sequence

1. **System context.**
   - *Primary system:* how a grant recommendation starts outside a sponsor's own portal and is reconciled at the recipient.
   - *Context:* US DAF sponsors, rails and vendors, 2026.
   - *Focus:* why no neutral, multi-sponsor grant-request specification exists.
2. **Outcome (factual).**
   - **None was found.** **DAF Direct** is a closed, sponsor-run widget with 3 sponsors and no public API or spec.
   - **Chariot's DAFpay** sponsor guide is the nearest thing to a published grant-request spec, but it is vendor-governed. Chariot certifies each integration, and the guide says it "does not require you to implement an exact API specification".
   - Source: [direction-data-standards-interoperability §0, wave 25B].
3. **Manifestations.**
   - DAF grant metadata do not travel with the payment in any documented case [same §0].
   - The correlation key that makes reconciliation work is Chariot's own ID, which the sponsor has to copy onto its remittance [same §2.2].
   - Donate pages: **25 of 186 (13.4%)** show DAFpay; **DAF Direct 3 (1.6%)**; **44 (23.7%)** mention DAFs without any in-checkout mechanism [direction-nonprofit-donate-pages §0].
   - Agent and API access: AI assistant or agent access exists at **2** sponsors (Daffy's MCP server and TIFIN Give's Louise) and a public API at **3** [direction-donor-feature-census §0, wave 27].
4. **Origin network.**
   - *Organizational:* there is no neutral convening body. The repository found no US private-philanthropy analogue of 360Giving, while the federal Grants Data Standards v3.0 (2026-06-17) exist under the GREAT Act [same doc §0].
   - *Financial:*
     - The only published spec belongs to a rail vendor whose position rests on being the integration point. [I]
     - Each sponsor bears the build cost (typically **2–4 weeks with an existing IdP, or 1–2 months from scratch** for a DAFpay integration [same §2.2]), while the benefit goes to nonprofits and other sponsors. That is a public-good shape. [I]
   - *Technical:* payment rails carry little remittance data (ACH CCD: one 80-character addenda). No DAF-specific addenda or ISO 20022 convention was found [same §0].
   - *Regulatory or legal:*
     - Sponsor legal control means a request stays a recommendation. Existing specs already model that, with `pending/approved/paid/rejected/canceled` [same §2.2], so it shapes the approval step and does not block a standard. [I]
     - FDX and §1033 do not reach DAF accounts, and §1033 is enjoined [same §0], so no regulatory rail compels interoperability.
5. **Propagation.**
   - Organizational: no standard means sponsor-by-sponsor integration.
   - Informational: vendor IDs or emailed reports serve as the correlation key.
   - Human: nonprofits key data by hand (see G12-2).
   - Financial: fee-bearing connectors (DAFpay's default 2.9% per [direction-nonprofit-side-experience §0]).
6. **Evidence.**
   - *Direct:* the published specs and their governance text.
   - *Inference:* the incentives behind the absence.
   - *Not observed:* whether any convening has begun; sponsor build-cost data beyond Chariot's guide.
7. **Control points.**
   1. A neutral body publishes a minimal open DAF grant record (CC BY schema, stewardship committee, SemVer, on the 360Giving and federal GDS model) [same §6].
   2. Large sponsors publish their own grant APIs. High influence, within sponsor control.
   3. Chariot opens governance of its spec. High influence, outside the entrant's control.
   4. A structured-remittance convention on CTX or ISO 20022.
8. **Ranking.**
   - By influence: 2 ≈ 3 > 1 > 4.
   - By controllability for an entrant: 1 > 4 > 2 > 3.
   - The Chariot and Endaoment fields already overlap (same §2.3), so control point 1 costs little to draft.
9. **Diagnostic sufficiency.**
   - Enough to justify drafting and publishing a minimal record (already queued as P-B40N13-03).
   - Not enough to predict adoption.

**Unknowns:** sponsor appetite; Chariot's response.
**Next responsible action:** P-B40N13-03 (field map and draft record).

**Classification:** **Mixed.** It is a coordination habit (organizational and informational origins) combined with a financial origin: vendor-governed rail economics and the public-good cost split. No single sponsor can change these alone. No regulatory or legal origin was found that blocks a standard.
- Claim state: internal-demonstration (an absence in the public record); suggestive (classification).
- Confidence: Medium-High (absence; the governing doc rates private-sector absence medium); Low-Medium (classification).

### Clarity

- **Admissibility screen.**
  - *Rejected:* "incumbents block standards". No signal of blocking was found; the record shows only an absence.
  - *Rejected:* "a standard would unlock DAF giving". The repository already holds H6 (widgets raise DAF grants) as unsupported [industry-incentives-structural-analysis.md §7].
- **What is currently justified?** A minimal open record is feasible and cheap. Its adoption is unknown.
- **Entrant response and posture.**
  - Publish and implement an open grant record. It is reversible and low cost, and it builds learning.
  - **Experimental.** Using it to let AI agents *submit* grants moves money under sponsor legal control. That use is **Guardrail**: high impact, with limited correctability for a misdirected payment, which needs scoped tokens, confirmation and caps. The census found no published cap or confirmation at Daffy's MCP server [direction-ai-product-census §1, wave 28].
- **I will reconsider if:**
  - Any sponsor consortium, Chariot, Candid or DAFRC announces an open DAF grant schema or working group. The absence finding would be superseded and the entrant should adopt, not author.
  - Regulators extend §1033 or FDX scope to charitable accounts. That would add a regulatory origin and a rail.
  - Two or more top-10 sponsors publish public grant APIs. Control point 2 would be working without a standard.
- **Monitoring plan:** Chariot developer changelog; sponsor developer pages; CFPB §1033 docket; 360Giving and GDS releases (owner: the data-standards workstream).

---

## 5. G12-4. Fidelity pool tracking shortfall about equal to the admin fee

### EDF v0.3 sequence

1. **System context.**
   - *Primary system:* published DAF investment-pool returns against benchmarks.
   - *Context:* Fidelity Charitable pools as of 2026-09-30, compared with other top-20 sponsors.
   - *Focus:* why Fidelity's pools trail their benchmarks by more than index menus elsewhere do.
2. **Outcome (factual).**
   - Fidelity's asset-allocation pools **trail their composites by 0.58–0.76 pp a year over 5 years. That is about the size of its 0.60% first-tier admin fee.**
   - **Each asset-allocation pool trails its own underlying Fidelity Advisor Asset Manager fund by 0.59–0.64 pp over 5 years, and the Money Market pool trails its benchmark by exactly 0.65 pp at 1, 3 and 5 years.**
   - The 5-year median is **−0.65 pp on 20 conventional pools**.
   - Source: [direction-investment-menus-performance §0 and §2.3, wave 27].
3. **Manifestations.**
   - Fidelity's return-basis note: "Pool results will include a Fidelity Charitable annual administrative fee"; benchmarks are not fee-adjusted [`sponsor-pool-returns-2021-2025.csv`, rows R001–R003].
   - GKCCF, CJP, FFTC and NPT report returns before admin fees, and Vanguard does not say [direction-investment-menus-performance §2.3].
   - **Bounded-truth caveat from the same CSV.**
     - Over trailing 1 and 3 years the asset-allocation pools are mostly *above* their composites. For example, Asset Allocation 85% is +2.79 pp (1y), +0.15 pp (3y) and −0.76 pp (5y) [rows R001–R003].
     - So "trails by the fee" holds only for the 5-year window on active pools. Only the Money Market pool shows the fee signature in every window.
4. **Origin network.**
   - *Financial:*
     - The admin fee is charged on balances and is deducted inside pool results.
     - The fee revenue goes to the trustee contract with FMR. FY2025 admin fee expense was **$179,875,837** [`incentive-map.csv` row 1, classified there as a structural constraint].
   - *Informational:*
     - Sponsors use no common return basis. Some report net of the admin fee, some gross, and some say nothing.
     - Raw gaps are therefore not like-for-like (P-B42N19-03).
   - *Technical:* active-management deviation and window effects (2022) are the alternative explanation for the asset-allocation pools [same doc §2.3].
   - *Regulatory:* no DAF pool-performance reporting standard was found.
5. **Propagation.**
   - Financial: the fee is deducted in the unit value, so the published return sits below the benchmark.
   - Informational: cross-sponsor tables compare net with gross.
   - Human: donors or analysts read the gap as manager underperformance. [I]
6. **Evidence.**
   - *Direct:* filed and published returns; Fidelity's basis statement.
   - *Inference:* the attribution of the residual to the fee. Three independent-looking signs support it (the composite gap, the underlying-fund gap and the Money Market pool), but they come from one publication.
   - *Not observed:*
     - whether Fidelity applies the first-tier rate or an asset-weighted rate in pool results;
     - the 0.05 pp by which the Money Market gap (0.65) exceeds the first-tier fee (0.60).
7. **Control points.**
   1. A declared return basis (gross and net of admin fee) in sponsor disclosures, within each sponsor's control.
   2. Fee basis: asset-based versus per-account or flat. Sponsor control, but bound to the revenue model.
   3. A cross-sponsor reporting convention, which needs coordination.
8. **Ranking:** by controllability, 1 > 3 > 2. By influence on donors' all-in cost, 2 > 1 ≈ 3.
9. **Diagnostic sufficiency.**
   - Enough to say cross-sponsor pool gaps must not be read as manager quality without basis normalisation.
   - Not enough to compute a like-for-like gross gap for Fidelity (P-B42N19-03 is open).

**Classification:**
- The **shortfall itself is structural.** A financial origin (an asset-based admin fee inside pool results, held in place by the trustee contract) cannot be changed short of changing the fee model.
- The **non-comparable cross-sponsor reporting basis is habit** (an informational origin).
- Claim state: internal-demonstration (gap values); suggestive (fee attribution).
- Confidence: High (values); Medium-High (attribution). The Money Market signature leaves little room for alternatives, but the 0.05 pp residual and the tier used are unexplained.

### Clarity

- **Admissibility screen.**
  - *Rejected:* "Fidelity pools underperform". That ignores the fee basis and is unbounded across windows.
  - *Rejected:* "Fidelity hides fees". The basis is disclosed.
  - *Retained:* the bounded claim, "a 5-year shortfall on asset-allocation pools about equal to the first-tier fee, and an exact 0.65 pp Money Market shortfall in all windows".
- **Entrant response and posture.**
  - Publish pool returns both gross and net of the admin fee, with the tier stated. It is low impact and easily changed: **Fast**.
  - Choosing an asset-based or flat or per-account pricing model sets the revenue model and the incentive alignment. It is costly to reverse once marketed: **Strategic**.
- **I will reconsider if:**
  - Fidelity states that pool results use a fee other than the first-tier 0.60%, or P-B42N19-03 finds other sponsors also report net. Either would re-base the comparison.
  - Calendar-year data (P-B42N19-02) show the 5-year shortfall persisting or widening beyond the fee. That would point to an active-management origin, not only the fee.
  - Fidelity changes its fee basis to per-account or flat. The reconsideration trigger already set in `incentive-map.csv` row 1 would then fire.
- **Monitoring plan:** Fidelity's monthly pool performance summary (owner: the investment-menus workstream).

---

## 6. Clarity/EDF tags for the 33 direction docs

**The gap audit's count.** The audit found that 29 of 33 direction docs never mention Clarity or EDF. A case-insensitive search finds the remaining four mentions are incidental and not applications:
- the word "clarity" in a URL or title (cf-consolidation-fees, data-standards-interoperability, international-comparison);
- the substring "edF" inside the XML tag `DisclosedForCharitablePrpsInd` (data-standards-interoperability);
- a match in a correction text (sponsor-financial-resilience).

So **0 of 33** applied either framework before this note.

**How each row was tagged.** The CSV gives each doc one row, based on the headline finding as its governing validation wave left it. Each row records:
- the finding type;
- whether EDF applies. EDF applies only to an observed outcome; absences, descriptive measures, computed scenarios and polls are tagged with Clarity alone, per the mission rule;
- the claim state and confidence;
- a structural or habit reading where the finding is an incentive finding;
- the Clarity posture of the AI-native entrant's natural response, with a reconsideration trigger.

Postures across the 33 rows:

| Posture | Docs |
|---|---|
| Fast | 9 |
| Experimental | 13 |
| Guardrail | 7 |
| Strategic | 4 |

These counts are a tally of the CSV, not evidence.

Five docs carry `edf_status = diagnosed_G12-n`: G12-1 draws on two of them (cf-consolidation-fees and sponsor-executive-compensation), and G12-2 to G12-4 on one each. Seven more carry `eligible_not_diagnosed` and are candidates for a later EDF pass:
- ai-product-census
- gift-office-daf-handling
- nonprofit-donate-pages
- long-tail-sponsors
- sponsor-marketing-spend
- sponsor-financial-resilience
- faith-giving-platforms

---

## 7. Rows appended to `incentive-map.csv` (applied 2026-11-19; validated, wave 31B)

These use the same columns as `incentive-map.csv`: stakeholder, incentive, mechanism, evidence_url, evidence_date, effect_on_modernization, structural_or_habit, clarity_status, notes.

```
Community foundations (DAF administration),Cover whole-organisation fixed cost from DAF fees,"Median admin fee 100/100/67 bps at $100k/$1m/$10m (n=34); about 1.7x/2.2x/3.6-4.7x nationals; CF top-officer pay slope 0.23 on total assets (21 CFs)",research/mission-2026-11-14/direction-cf-consolidation-fees.md; research/mission-2026-11-14/direction-sponsor-executive-compensation.md,2021+ schedules; TY2024,discourages,mixed,internal-demonstration; High (fact) / suggestive; Low-Medium (cause),"G12-1. Leaning structural on cost level; habit on fee opacity (41 of 100 no terms) and consolidation. Reconsider if DAF-attributable cost is far below fee (P-G12-01)."
Sponsors (donor-data defaults),Default donor disclosure setting,"Defaults: full contact 36%, name only 24%, fund name only 35%, anonymous 1% (DAFRC n=128, 86% CFs)",https://www.dafresearchcollaborative.org/s/The-National-Survey-of-Donor-Advised-Fund-Managers.pdf,2025,discourages,mixed,internal-demonstration; Medium / suggestive; Medium,"G12-2. Leaning habit: variation under one federal regime. Top-20 check (P-B44N28-01; wave 34A): full-contact default 33.2% of FY2024 top-20 assets; withholding default 17.2%; 44.6% undocumented. Reconsider if a privacy/4967 ruling appears. [V wave 34A]"
Rail vendors and sponsors (grant-request spec),Own the integration point; avoid funding a public good,"No open multi-sponsor DAF grant-request standard; DAFpay spec vendor-governed with certification; DAF Direct closed (3 sponsors)",research/mission-2026-11-14/direction-data-standards-interoperability.md,2026,discourages,mixed,internal-demonstration; Medium-High (absence) / suggestive; Low-Medium,"G12-3. Coordination habit plus financial origin; no regulatory blocker found. Reconsider if any open schema or working group is announced."
Fidelity Charitable (pool reporting),Asset-based admin fee deducted inside pool results,"Asset-allocation pools trail composites 0.58-0.76 pp/yr over 5y; Money Market trails by exactly 0.65 pp at 1/3/5y; first-tier fee 0.60%",https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/monthly-pool-performance-summary.pdf,2026-09-30,neutral,structural constraint (shortfall); historical habit (cross-sponsor basis),internal-demonstration; High / suggestive; Medium-High (attribution),"G12-4. 1y/3y AA gaps are positive, so the fee signature is 5y-only for active pools. Reconsider on P-B42N19-02/-03."
```

Text for `industry-incentives-structural-analysis.md` §6: §§2–5 above, as Outcomes D–G.

---

## 8. Observations for document owners

- **Gap audit §4.1, CF fee bullet.**
  - The audit says the five pre-2021 CF schedules (Minneapolis, San Francisco, Greater Cincinnati, San Antonio, Toledo) are "in the top-100 fee median".
  - In `cf-daf-fee-census-2026.csv` they carry status `published_schedule_pre2021` and **no** `admin_bps_*` values. The bps columns are populated only for the 34 `published_schedule` rows and 5 national comparators.
  - The median therefore does not use them. This is consistent with direction-cf-consolidation-fees §0 ("34 publish a full schedule … from a 2021+ source"; "5 more publish only pre-2021 schedules").
  - Proposed as P-G12-02, with a refresh of those five CFs' current schedules.
- **Wave-29 nuance carried forward.** NPT's "79% partially anonymous" stays unverified and is not used here.

## 9. Limits

- All diagnoses are desk analysis on repository documents. No new fetching was done.
- The classifications are suggestive by construction: the same research process that produced the facts also produced these readings, so they are not independent replications.
- Postures describe an entrant's response under the stated assumptions. They are not recommendations to act without the reconsideration checks.
- The posture matrix ambiguity in the pinned Clarity text (§0) is resolved toward the prose. A reader applying the ASCII figure instead (Guardrail on the high-correctability side) would relabel as Strategic the responses marked Guardrail in §§3–4, because those are high impact with low correctability.
