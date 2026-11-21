# Professional-education assumptions tested with Clarity and EDF

**Date:** 2026-11-21.

**Framework basis.** Clarity `rules.md` (admissibility: no unbounded "always" or "never" claims; motivation must not stand in for incentives), the posture model and reconsideration criteria. EDF v0.3 claim states (internal-demonstration, suggestive, unsupported, contradicted) and confidence labels. Both are read from the canonical repositories as pinned in [clarity-edf-application-guide.md](../mission-2026-11-14/clarity-edf-application-guide.md). EDF diagnosis is used only where an outcome is observed; otherwise the method is Clarity alone. Each test below records the proposition, the supporting and contradicting evidence, alternative explanations, a structural-versus-habit classification, what evidence would change the verdict, and a verdict with confidence.

## Verdict summary

| # | Assumption taught or implied in education | Verdict | Confidence |
|---|---|---|---|
| H1 | DAF administration necessarily requires extensive manual processing | Contradicted for routine grants; supported for exceptions (about 7–8% of recipient lines) | Medium |
| H2 | Grant eligibility must be re-verified from scratch for each grant | **Contradicted.** Rev. Proc. 2018-32 permits reliance on listed status with a dated record. Recipients repeat (about 12 grants per charity at Fidelity). Checks of purpose and benefit stay per-grant | Medium-High |
| H3 | Complex and noncash gifts are inherently hard to scale | Partly supported. Listed securities and crypto scale already. For illiquid assets the bottleneck is sale and diligence, not intake | Medium |
| H4 | Advisers primarily value investment features | Contradicted on stated reasons (tax ranks first); partly supported by behaviour (asset-based fees, investment choice) | Medium |
| H5 | Donors primarily value tax advantages | Partly supported. Tax drives the choice of vehicle, not the motive to give | Medium-High |
| H6 | Legacy architecture is necessary because of regulation | **Contradicted.** No DAF-specific technology rule exists. Challengers on modern stacks operate under the same law. Lock-in and affiliated procurement explain legacy systems | Medium-High |
| H7 | AI is primarily useful for administrative productivity | Contradicted, weakly: the modelled administrative value is thin, and shipped AI is mostly donor- and nonprofit-facing | Low-Medium |
| H8 | Existing workflows are the optimal division of responsibilities | Contradicted for operations (reconciliation burden on nonprofits, no portability); supported for the legal core (sponsor control) | Medium |

The detailed tests follow. They were written by the education-assumptions research pass of 2026-11-21. The tags below are local to this section:
- [X] marks an external page read in this pass;
- [F] marks a filed fact carried by the repository;
- [R] marks a repository finding;
- [I] marks an inference.

---

**Relation to existing work.** The file `research/commercial-opportunity/clarity-edf-analysis/assumption-tests.md` (2026-11-20; "AT" below) already tests overlapping *commercial* assumptions:
- AT-A1, "administration must remain highly manual";
- AT-A2, "AI is primarily valuable for grant vetting";
- AT-A3, "scale produces better economics";
- AT-A4, "advisers should outsource".

H1 and H7 below reuse those results and cross-reference them rather than redoing the work. The extra effort went to H2, H3, H4, H5, H6 and H8.

**Verdict scale:** supported / partly supported / contradicted / insufficient evidence. **Confidence scale:** High, Medium-High, Medium, Low-Medium, Low. Both are qualitative, not probabilities.

---

## Summary table

| # | Assumption (as commonly stated) | Precise proposition tested | Verdict | Confidence | Main driver |
|---|---|---|---|---|---|
| H1 | DAF administration necessarily requires extensive manual processing | Most per-grant and per-contribution handling must be manual because law or the nature of the work requires it | **Contradicted for the routine path; supported for exceptions** | Medium | Mixed: structural for exceptions, habit for routine work |
| H2 | Grant eligibility must be re-verified from scratch for each grant | Each grant needs a fresh, independent eligibility determination that cannot reuse prior recipient-level verification | **Contradicted as stated.** Recipient status is a reusable, time-stamped attribute. Purpose and benefit are per-grant, and sponsor discretion is case-level | Medium-High | Status: habit/policy. Purpose and benefit: structural |
| H3 | Complex/noncash contributions are inherently hard to scale | Intake, diligence and liquidation of noncash assets cannot be made routine or high-volume | **Partly supported.** Listed securities and crypto already scale. Private interests and real estate are slow because of liquidity events, appraisal and legal diligence, not intake. Specialist intermediaries already provide shared scale | Medium | Liquidity and legal diligence: structural. Intake and documents: habit/informational |
| H4 | Financial advisers primarily value the investment features of DAFs | In advisers' own stated reasons, investment features rank first | **Contradicted on stated reasons.** Tax, convenience and timing rank first; asset growth is 42% and fees 17%. **Partly supported on revealed behaviour:** choosing investments is advisers' most common DAF service, and fee retention shapes channel design | Medium-High (stated); Medium (revealed) | Structural: AUM compensation. Stated motives: informational |
| H5 | Donors primarily value tax advantages | Tax is the primary reason donors use DAFs | **Partly supported.** Tax leads *vehicle choice* (62% to 98%) but not *giving motive* (duty 74%; values 68%; tax 12–21% in HNW samples). Advisers overstate tax relative to clients. A DAF adds no tax advantage over a direct gift for itemizers | Medium-High | Structural (tax code) for vehicle choice; habit/framing in education |
| H6 | Legacy software architecture is necessary because of regulation | Current DAF regulation requires, or effectively forces, legacy system designs | **Contradicted.** No DAF-specific technology rule exists, and modern-stack challengers operate under the same law. Legacy persistence is explained by contracts, migration cost, affiliate procurement and the absence of standards | Medium-High | Habit and financial (switching costs); a thin regulatory overlay (bank third-party risk, recordkeeping) is architecture-neutral |
| H7 | AI is primarily useful for improving administrative productivity | The main value of AI in DAFs is staff productivity in sponsor administration | **Contradicted as a generalisation** (weakly). The measured admin pool is thin and concentrated in document-heavy exceptions. Shipped AI sits mostly on the donor, nonprofit and fundraising side, and governance limits AI to adding evidence. Where the value is largest outside admin is unmeasured | Low-Medium | Structural: liability on whoever signs. Informational: no measured outcomes |
| H8 | Existing workflows are the optimal division of responsibilities | The current split among donor, adviser, sponsor, vendor, payment rail and nonprofit minimises total cost and risk | **Contradicted for the operational split; supported for the legal core.** Sponsor control and donor advisory status are legally fixed. Who carries remittance, reconciliation, eligibility data, complex-asset diligence and data portability is the product of incentives and missing standards | Medium | Legal core: structural. Operational allocation: habit and incentive |

---

## H1. "DAF administration necessarily requires extensive manual processing"

**Cross-reference:** AT-A1 ("contradicted for routine work, supported for exceptions"; suggestive, Medium). That result is reused here; only the evidence it lacked is added.

**Precise proposition.** For a DAF sponsor, most per-grant and per-contribution handling must be performed or decided manually, because law or the intrinsic nature of the work requires it, not merely because current systems and habits do.

**Supporting evidence**
- Sponsor job postings still describe manual inbox work, cheque follow-up and reconciliation. Only 2 of 15 sponsor postings name AI [R: AT-A1; `research/mission-2026-11-14/strategic-synthesis.md` §0 B].
- Paper checks remain an active rail. In 2025 about 33% of Fidelity Charitable grants went by check (secondary source, Chariot, Mar 2026). DAFgiving360 states 7–10 business days plus USPS [R: `industry-incentives-structural-analysis.md` §6.1, wave-2B governing corrections].
- Fidelity states that grant recommendations "may take 10 or more business days" [R: same file, §6.2].
- Legal liability attaches to the sponsor and to knowing managers under §§4966, 4967 and 4958 [F: `ai-governance-failure-modes.md` §1]. Some steps therefore need an accountable human.

**Contradicting evidence**
- **Rules-based straight-through processing exists in production at scale.**
  - Ren markets "over half" of grants as approved instantly [R: `research/ren-instant-grant-approval-rcf-policy-clarity-audit-2026-11-12.md`, "Three separate metrics"].
  - RCF's March 2023 policy treats GuideStar Charity Check as adequate risk mitigation for more than 98% of historical grants (same file, "RCF risk policy").
- **Exceptions are a minority.**
  - The core review-need proxy is 7.4–7.8% of top-50 recipient lines and 11.0–11.6% of dollars [R: `gap19-exception-load-proxy.md` §0; `strategic-synthesis.md` §0 A].
  - Like-for-like non-standard grants are about 3.6–4.2% of the four largest nationals' dollars.
  - Grants to revoked EINs are 0.082% of dollars [R: `strategic-synthesis.md` §0 A].
- **Low-cost operators exist.** Cost per grant is $55 at DAFgiving360 and $68 at Fidelity, against $134 at Vanguard Charitable and $419 at NPT [R: AT-A3]. Very different costs under the same law are hard to reconcile with "necessarily".

**Alternative explanations**
- The manual effort may be concentrated in operational holds that are not eligibility decisions: unconfirmed bank details, returned payments, liquidation. It is then a rail and data problem, not a review problem [R: `daf-discretionary-grant-review-policy-explainability-audit-2026-11-12.md`, "Critical distinction", items 4–5].
- Peak-season staffing and year-end intake crunches are timing-structural but handling-habitual [R: `industry-incentives-structural-analysis.md` §3.9].

**Structural vs habit.** **Mixed.**
- Structural: exceptions (foreign grantees, expenditure responsibility, benefit risk, Type III supporting organisations, complex assets).
- Habit: manual handling of routine grants to listed public charities and the default to checks [R: `industry-incentives-structural-analysis.md` §9].

**Evidence quality.** Medium.
- No sponsor publishes its exception rate, reviewer minutes or straight-through share with a defined denominator. Ren's "instant" claim is undefined.
- The exception proxy measures recipients, not observed review.

**What would change the conclusion**
- A measured study at any sponsor showing that routine grants consume most handling time and that the time is legally necessary.
- Exception rates above about 25% of grants.
- A court or the IRS treating per-grant manual review as required to exercise control [R: AT-A1].

**Verdict: contradicted for the routine path; supported for exceptions. Confidence: Medium.**

---

## H2. "Grant eligibility must be repeatedly verified from scratch for each grant"

**Precise proposition.** For every grant, a sponsor must make a new and independent eligibility determination. It cannot rely on a recipient-level verification that is retained, dated and continuously refreshed, plus per-grant checks of the grant-specific elements only.

To test this, eligibility is decomposed into four parts:
- **(a)** recipient legal status: exempt, public charity, not a disqualified supporting organisation, not revoked, not sanctioned;
- **(b)** grant purpose and donor benefit;
- **(c)** sponsor-discretionary concerns: litigation, allegations, reputation;
- **(d)** operational readiness: funds, bank details.

**Supporting evidence**
- **Sponsor policies state per-grant review.**
  - Vanguard Charitable: "Each recurring grant, regardless of issue date, is subject to the same review and approval process as a single grant", and a previously approved grant can be denied if status changes [X: [Vanguard Charitable policies](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines), read 2026-11-21].
  - Fidelity Charitable "conducts a robust and thorough review of each grant recommendation", drawing on IRS databases, litigation records and news [X: [Fidelity granting due diligence](https://www.fidelitycharitable.org/legal/granting-due-diligence.html), read 2026-11-21].
- **Status is time-varying.** Revocations happen, and sponsors exercise discretion beyond the statutory floor. In 2026 three nationals restricted grants to a listed public charity, the SPLC, after an indictment [R: `industry-incentives-structural-analysis.md` §3.4; AG letter dated 2026-05-21 per the wave-4 governing correction].
- **Components (b) and (c) are genuinely grant-specific.**
  - §4967 prohibited benefits and pledge rules depend on the purpose of each grant [F: 26 USC 4967].
  - RCF requires an officer to review grants over $500k (2023 policy) [R: Ren audit, "RCF risk policy"].
- **Rev. Proc. 2018-32 reliance has conditions.** It fails if the grantor knew of the revocation, knew it was imminent, or was partly responsible for it.
  - Third-party reports relied on under §8.01 must carry the name, EIN, foundation status and deductibility, a "most current update" statement, and the date and time.
  - The grantor must retain a copy [X: [IRB 2018-23, Rev. Proc. 2018-32 §§4.04, 5.02, 8.01](https://www.irs.gov/irb/2018-23_IRB), read 2026-11-21].
  - So *something* must be checked and retained at, or close to, the time of each grant.

**Contradicting evidence**
- **The law makes reliance recipient-level and announcement-driven.**
  - Under Rev. Proc. 2018-32, grantors may rely on TEOS or EO BMF data until the IRS publicly announces a change (§4.01, §5.01).
  - §5.01 states that "sponsoring organizations of donor-advised funds may rely on an organization's public charity status" for §4966 purposes [X: IRB 2018-23].
  - The requirement is a *current, dated snapshot*, not re-derivation from scratch. A continuously refreshed recipient record with a per-grant snapshot ID meets it.
- **Recipients repeat heavily, so per-grant re-derivation duplicates work.** Published grant and recipient counts [R: `g0401-g0502-ai-routing-and-per-grant.md` §B2]:

  | Sponsor and period | Grants | Distinct recipients | Grants per recipient |
  |---|---|---|---|
  | Fidelity, FY2024 basis | about 2.50m | about 206k | ≈12 |
  | Vanguard | about 225k | about 60k | ≈3.8 |
  | NPT | about 130k | about 41k | ≈3.2 |
  | T. Rowe Price | about 32k | about 13k | ≈2.4 |

  [I] At Fidelity, more than 90% of grant-level status checks are repeat checks on a recipient already verified.
- **Industry practice already reuses verification.**
  - Ren publicly claims charity vetting is "reused across its platform" [R: Ren audit, "Executive conclusion"].
  - RCF's 2023 policy uses a recipient-level third-party report (Charity Check) for more than 98% of historical grants (same file).
  - Fidelity "immediately stops making grants" when status is lost, which is a recipient-level trigger [X: Fidelity due-diligence page].
- **The underlying data change monthly at most.** Pub 78, the BMF and the auto-revocation list are monthly files [R: `direction-data-standards-interoperability.md` §6 item 3]. Re-verifying daily from scratch adds no information beyond a monthly diff plus OFAC updates.
- **The repository's governance analysis treats routine eligibility as deterministic.** It recommends an EIN-keyed lookup with a snapshot ID stored on each decision and "continuous status subscription" (design D) [R: `ai-governance-failure-modes.md` §4.1]. In the AI-economics model, redesign D ranks first for routine eligibility (P06) with P = 0.94 [R: `ai-economics-v2-observed-costs.md` §1].
- **Education lag signal.** Vanguard's public policy still cites Rev. Proc. 2011-33, which 2018-32 superseded [X: Vanguard policies page]. Candid's Charity Check PDF also still cites 2011-33 [R: `DAF-INDUSTRY-REPORT-2026-11.md`, batch 30 paragraph]. [I] Policy texts and teaching materials can lag the reliance rule they implement.

**Alternative explanations**
- "Each grant is reviewed" in sponsor policy may mean each grant passes an *automated* recipient gate plus grant-specific checks, not a manual re-derivation. Policy wording does not reveal the implementation [I].
- Per-grant review language may serve reputational and discretionary protection (component (c)), which the SPLC episode shows is real. It may not be tax-compliance necessity [R: `industry-incentives-structural-analysis.md` §3.4].
- The purpose-review component (b) is unavoidable per grant. Its *cost* depends on intake design: structured donor attestation can prevent avoidable review [R: `daf-discretionary-grant-review-policy-explainability-audit-2026-11-12.md`, Sponsor comparison (DAFgiving360, AEF rows)].

**Structural vs habit**
- **(a) Status:** a per-grant *dated snapshot* is structural (Rev. Proc. 2018-32 §8.01). Re-deriving it from scratch is **habit/policy**.
- **(b) Purpose and benefit:** **structural** (§4967) and grant-specific.
- **(c) Discretionary hold:** **sponsor policy**, neither law nor habit. It is a choice.
- **(d) Operational readiness:** habit and data.

**Evidence quality.** Medium-High on the legal rule (primary IRB text read) and on the grant/recipient ratios (published counts). Low on what sponsors actually implement: policy text only, and no logs.

**What would change the conclusion**
- IRS guidance or enforcement denying reliance where a sponsor used a cached but current dated snapshot.
- Final §4966/6033 guidance imposing per-grant diligence duties beyond status. The 2026–27 Priority Guidance Plan item is open [R: `regulation-market-structure-portability.md` Q-B09].
- Sponsor data showing that most per-grant time goes to status rather than purpose or discretion. That would make the habit share larger, not smaller.

**Verdict: contradicted as stated. Confidence: Medium-High.** Eligibility does need a *per-grant dated record*, and purpose, benefit and discretion are evaluated per grant. Recipient status does not have to be verified *from scratch* for each grant.

---

## H3. "Complex/noncash asset contributions are inherently difficult to scale"

**Precise proposition.** Accepting, diligencing and converting noncash assets cannot be made routine or high-throughput, because the difficulty is intrinsic to the assets rather than to how intake is organised.

The proposition is tested separately for three classes:
- **(i)** listed securities and crypto;
- **(ii)** restricted or control stock and private business, LP or fund interests;
- **(iii)** real estate, art and other illiquids.

**Supporting evidence**
- **Volumes at the largest sponsor stay low.** Fidelity takes about 500 complex contributions a year, averaging 65 days from acceptance to liquidity. That is against about 3m grant recommendations and more than 395k donors [R: `direction-noncash-gift-infrastructure.md` §3 table; `industry-incentives-structural-analysis.md` §3.9].
- **Gatekeeping signals per-case cost** [R: `direction-noncash-gift-infrastructure.md` §3].
  - NPT minimums: $2m for real estate, $1m for alternatives, $500k for private business, $250k for art.
  - NPT's real-estate diligence takes 3–6 months, needs a $25k good-faith contribution and 6 months of carrying costs, and requires debt-free, vacant property.
  - NPT's "gift processing fee" is sized to the diligence.
- **Intrinsic per-asset work.** Each gift involves operating agreements, transfer restrictions, §4943 holdings tests, UBIT and Form 8283 qualified appraisals. AI extraction errors on transfer restrictions "could be material" [R: `ai-governance-failure-modes.md` §4.7].
- **Liquidity is exogenous.** Intermediaries move proceeds only "after a liquidity event" [X: [TIFIN Give complex gifting](https://intercom.help/give-ria/en/articles/9981851-complex-gifting); [AssetMark complex gifting](https://intercom.help/assetmark-help-center/en/articles/10644732-complex-gifting), both read 2026-11-21]. No intake process can make an illiquid LP interest sell faster.
- **Outsourcing of the hardest assets.** AEF does not accept illiquids directly; it uses Dechomai and Realty Gift Fund. The evidence suggests DAFgiving360 routes some to a charitable intermediary [R: `direction-noncash-gift-infrastructure.md` §3].

**Contradicting evidence**
- **Class (i) already scales.**
  - The Giving Block reports more than $100m of 2025 crypto across 22,343 donations [C, company claim].
  - DonateStock Charitable filed $25.1m in 2,630 securities gifts in FY2025 [F].
  - FreeWill Impact Fund filed 986 noncash gifts in TY2024 [F] [R: `b40n14-03-b38c-03-noncash-vendors-dpn.md` §0(A)].
  - In-kind listed stock to DAFs is routine at nationals [R].
  - [I] "Noncash" as a category therefore overstates the difficulty. Volume is a problem only for class (ii)/(iii).
- **Class (ii)/(iii) also scale, through a specialist intermediary rather than in-house.**
  - Dechomai Asset Trust took in $986m (CY2021), $525m (CY2022), $961m (CY2023) and $649.8m of Schedule M gifts in 2024 [F/R: `direction-noncash-gift-infrastructure.md` §1 item 4; `b40n14-03…` §0].
  - It serves several sponsors and RIA DAF programmes (AEF, AssetMark Charitable, TIFIN Give) and receives grants from DAFgiving360 and Fidelity [R; X: the two help-centre pages above].
  - [I] Pooling scarce legal and valuation expertise across sponsors is the classic way to scale a low-frequency, high-skill task.
- **Diligence elapsed time can be short.** AssetMark and TIFIN Give say Charitable Solutions' due-diligence review "typically takes between 1–3 business days" [X: both pages; vendor claim, undefined start and end points]. [I] Fidelity's 65 days is therefore mostly time to liquidity, not intake.
- **Pricing shows divergent economics, not impossibility.**
  - Fidelity charges "no additional charge" for non-public assets, and Ren does diligence "at no extra cost".
  - Dechomai charges 1–3% with a $10k minimum on its last published, undated sheet [R: `direction-noncash-gift-infrastructure.md` §1 item 5, wave-25B correction 2].
  - [I] A sponsor that absorbs the cost signals the work is economic at its scale.
- **Fidelity's dollar volume is material.** Noncash contributions were $2.6bn in 2025, 8% of contribution dollars; lifetime $18.1bn [R: same file, §3]. Low count but large dollars is "low volume, high value", not "unscalable".

**Alternative explanations**
- **Selection.** Minimums and fees screen out small complex gifts. Observed low counts may reflect sponsor rationing, not intrinsic limits [I].
- **Demand side.** Advisers rate "donating non-cash assets" as very or extremely important for 55% (DAFRC 2026, Fig. 5.1). The report itself suggests appreciated securities could be the default mode of giving [X: DAFRC adviser report PDF, pp. 33–34, read 2026-11-21]. Under-use may be an advice and education gap more than a capacity limit.
- **Document-heavy intake is where AI has a modelled case.** P03 is one of only three processes where AI-on-workflow wins first-rank draws at all, at 14–16% [R: `ai-economics-v2-observed-costs.md` §1]. That points to tooling, not inherent limits, as the open variable.

**Structural vs habit**
- **Structural:** time to liquidity for private and illiquid assets; appraisal, UBIT, §4943 and transfer-restriction law; valuation risk.
- **Habit/informational:** the in-house versus intermediary choice, intake document handling, the lack of a standard data packet, and the advice gap on appreciated securities.

**Evidence quality.** Medium.
- Fidelity's figures are first-party.
- Intermediary turnaround is a vendor claim with undefined endpoints.
- No sponsor publishes complex-gift cycle-time distributions.
- Dechomai fees are undated.

**What would change the conclusion**
- Published p50/p90 intake-to-acceptance times by asset class showing that intake, not liquidity, dominates elapsed time even at specialists. That would strengthen "hard to scale".
- Evidence that the intermediary model carries hidden failure costs: valuation disputes, IRS challenges, concentration risk in one administrator. Note the potential conflict: six of 22 named DAFCP experts are at Charitable Solutions, an unvalidated pointer [R: `analyst-and-education-landscape.md`, DAFCP pointer].
- Documented failure of a high-volume complex-asset programme.

**Verdict: partly supported. Confidence: Medium.** The claim is true for illiquid classes, and the cause is liquidity and legal diligence, not intake. It is false for listed securities and crypto. Even for illiquids, specialisation already provides cross-sponsor scale. "Inherently" is too strong.

---

## H4. "Financial advisers primarily value the investment features of DAFs"

**Cross-reference:** AT-A4 (advisers keep the relationship and the assets).

**Precise proposition.** When advisers decide whether to recommend and how to use a DAF, investment features (asset growth, investment menu, ability to manage and charge on DAF assets) matter more than tax, convenience, timing or client-goal features.

**Supporting evidence (revealed behaviour and incentives)**
- **Choosing investments is advisers' most common DAF service.** 56% "always or often" choose investments and 44% adjust them. Only 11% advise clients on where to grant [X: DAFRC, *Financial Planning in the Age of DAFs* (2026), Fig. 5.3, n=669, read 2026-11-21].
- Advisers directly manage DAF investments for about 45% of their DAF clients (same report, Data and Methods).
- **Channel design follows AUM.** Fidelity's adviser-managed programme holds $37.1bn, 46.9% of its investments [R: AT-A4]. Programmes let advisers charge up to 1% on DAF assets (DAFgiving360 PMA, MS GIFT, TIFIN) [R: `strategic-synthesis.md` §0 A].
- The repository household model shows an RIA losing 25% of fee revenue on a $500k gift without a sponsor mandate, and fee-neutral with a 0.75% mandate [R: `industry-incentives-structural-analysis.md` §3.3; Medium-High that the incentive exists].
- DAFgiving360 reports 77% of DAF assets associated with an adviser [R: `analyst-and-education-landscape.md` §4.1, sponsor self-report].

**Contradicting evidence (stated reasons)**
- **Reasons to recommend a DAF, very or extremely important** [X: DAFRC 2026, Fig. 5.1, read 2026-11-21]:

  | Reason | Share |
  |---|---|
  | Tax benefits | 83% |
  | Client convenience | 69% |
  | Flexible timing | 69% |
  | Estate planning objectives | 63% |
  | Simplified record keeping | 60% |
  | Donating noncash assets | 55% |
  | Adviser convenience | 49% |
  | Family philanthropy | 45% |
  | **Asset growth** | **42%** (9th of 10) |
  | Privacy | 28% |

- **Advisers' own motives** [X: same report, Fig. 5.2]:

  | Motive | Share |
  |---|---|
  | Accomplish a client goal | 87% |
  | Support client values | 75% |
  | Strengthen the relationship | 71% |
  | Makes me feel good | 41% |
  | **Adviser or management fees** | **17%** (58% say not or slightly important) |

- Fees and costs are a moderate or major client concern for only 32% of advisers (Fig. 6.1). The study is not cost-led either.
- The repository's education review records the same ordering from the secondary source [R: `analyst-and-education-landscape.md` §4.1, wave-19 governing correction 3].

**Alternative explanations**
- **Social desirability and sample.** The sample is a convenience sample of 669, unweighted and funded by DAFgiving360 [R: wave-19 correction 2]. Self-reports understate self-interested motives. "Strengthen the relationship" (71%) may be a respectable proxy for retention.
- **Stated versus revealed.** Advisers may *recommend* for tax reasons and *engage* through investments, because investment management is what they are paid for and licensed to do. The two findings are compatible [I].
- **Heterogeneity.** Advisers serving $10m+ clients differ from those serving clients under $1m (DAFRC §2–3). Wirehouse and RIA channels have different compensation [R: `industry-incentives-structural-analysis.md` §3.3, open question on Edward Jones and MS adviser pay].

**Structural vs habit**
- **Structural (financial):** AUM-based compensation makes investment control of DAF assets matter commercially. Channel products are built around it.
- **Informational/habit:** education and marketing that frame DAFs around tax and convenience. The DAFCP curriculum's sponsor ties are noted, pending validation [R: `analyst-and-education-landscape.md` §5.1, DAFCP pointer].

**Evidence quality.** Medium.
- One primary survey (sponsor-funded, convenience sample).
- Incentive evidence from fee schedules and ADVs is strong.
- There is no observational data linking adviser fee eligibility to DAF recommendation rates.

**What would change the conclusion**
- A study comparing recommendation rates where advisers can and cannot charge on DAF assets. If recommendations drop sharply without fee eligibility, the revealed-preference reading dominates.
- Wirehouse compensation disclosures for DAF assets.
- A final §4966 rule treating personal investment advisers as donor-advisors (2023 NPRM) and a resulting change in adviser behaviour [R: `industry-incentives-structural-analysis.md` §3.4].

**Verdict: contradicted on advisers' stated reasons (Confidence: Medium-High); partly supported on revealed behaviour and channel economics (Confidence: Medium).** "Primarily investment" is wrong as a description of why advisers recommend DAFs. It is a fair description of where advisers spend their DAF effort and how channels are monetised.

---

## H5. "Donors primarily value tax advantages"

**Precise proposition.** For donors who use DAFs, tax advantage is the main reason for using the vehicle and for giving through it.

The test distinguishes three levels:
- **(a)** why give at all;
- **(b)** why choose a DAF as the vehicle;
- **(c)** what the DAF adds over a direct gift.

**Supporting evidence (level b: vehicle choice)**
- **BofA Private Bank/Escalent 2026** (n=1,431, ≥$3m). Reasons among DAF users: tax-free growth 98%, maximise tax benefits 96%, simplicity 94%, privacy 80% [R: `direction-public-opinion-dafs.md` §3 DS07; wave-29 note: page 403 on re-fetch, not re-verified].
- **DAFRC National Survey of DAF Donors 2025** (>2,100, sponsor-recruited). Reasons for *setting up* a DAF, "a lot/great deal" [X: [Chariot summary](https://givechariot.com/resources/insights/breaking-down-the-new-national-daf-donor-survey), read 2026-11-21]:

  | Reason | Share |
  |---|---|
  | Tax advantages | **62%** (highest) |
  | Ease of noncash contributions | 35% |
  | Investment growth | 32% |
  | Convenience | 32% |
  | Professional recommendation | 29% |

  Contribution reasons: capital gains avoidance 51%, bunching 41%.
- **Fidelity Charitable (2022, about 1,000 own donors):** "nearly 9 in 10" see the DAF as a tool to maximise impact *and* their tax benefit [X: [Fidelity](https://www.fidelitycharitable.org/insights/why-donors-use-a-donor-advised-fund.html), read 2026-11-21]. The item is double-barrelled.
- **Contribution timing is tax-driven.** Year-end cutoffs and peaks [R: `industry-incentives-structural-analysis.md` §3.9].

**Contradicting evidence (levels a and c)**
- **Motivations for giving *from* a DAF** (DAFRC 2025): duty to give back 74%, personal connection 71%, satisfaction 67%, sustainable change 63%, local impact 59% [X: Chariot summary]. Tax is not the primary *giving* motive even among DAF holders.
- **Affluent donors generally** (2025 BofA/Lilly, 2024 data): personal values 68%, interest in the issue 57%, firsthand experience 50% are the top motivations. Tax does not appear among those listed [X: [BofA 2025 study page](https://www.privatebank.bankofamerica.com/articles/2023-bank-of-america-study-of-philanthropy.html), read 2026-11-21].
- **HNW and UHNW samples:**
  - Goldman Sachs 2026: 12% cite tax deductions as a reason to give, and 6% say taxes affect gift size.
  - TPI 2026: tax is a motive for 21% of clients, while 40% of advisers rank it.
  [R: `analyst-and-education-landscape.md` §4.2, §5.2 T9]
  The repository labels this an **adviser–client perception gap** documented by sponsor-funded research itself.
- **Historical:** in the 2008 BofA study, about 52% of wealthy donors said their giving would stay the same without income-tax deductions [X: search summary of [Chronicle](https://www.philanthropy.com/news/half-of-affluent-americans-say-tax-policy-doesnt-affect-their-giving/); secondary, older than the 2021+ window, context only].
- **Level (c): the DAF adds no tax advantage over a direct gift** in the same year for itemizers, and loses for non-itemizers from 2026 (§170(p) excludes DAF gifts). Capital-gains avoidance on listed stock is identical for direct gifts [R: `direction-donor-tax-scenarios-2026.md` §1; `strategic-synthesis.md` §0 A "contradicted; Medium-High"]. [I] What donors value as a "tax advantage" is often the *timing* (bunching, deduction now and grant later) and *administrative* convenience of realising the tax benefit, not a larger benefit.
- **Awareness of tax changes is low.** 58% of Fidelity donors were unaware that 2025 tax changes could affect their giving [R: `direction-public-opinion-dafs.md` §3 DS08]. That is hard to square with tax being the overriding consideration.

**Alternative explanations**
- **Question framing.** Surveys of *vehicle* reasons elicit tax; surveys of *giving* motives elicit values. Both can be true at once: tax is a reason for the wrapper, and values are the reason for the gift [I].
- **Sample construction.** All DAF donor samples are sponsor-recruited or customer-based [R: `direction-public-opinion-dafs.md` §0]. Wealthier, older donors (DAFRC: average age 67, 96% with net worth above $1m) have more tax exposure.
- **Adviser mediation.** Advisers rank tax first (83%). The donor-side tax emphasis may partly reflect how the product was sold [I; R: T9].

**Structural vs habit**
- Vehicle-level tax relevance is **structural** (tax code: deduction timing, appreciated assets, AGI limits).
- The belief that DAFs are *tax-superior* is **habit/framing** in education and marketing. The repository advises entrants against "selling the DAF as tax-superior" [R: `strategic-synthesis.md` §0 D].

**Evidence quality.** Medium. Several independent survey families point the same way on the vehicle-versus-motive split, but all are self-reported and none is a probability sample of DAF holders. No probability sample measures DAF holding at all [R: `analyst-and-education-landscape.md` wave-22 correction 3].

**What would change the conclusion**
- A probability-sample study, or a natural experiment (for example around OBBBA 2026: the 0.5% floor, the 35% cap and exclusion from the non-itemizer deduction), showing DAF contributions fall sharply when the tax value falls. That would support "primarily tax" in revealed behaviour.
- Conversely, stable DAF inflows after the 2026 changes would weaken it.
- The first FY2026 filings are the observable test [I].

**Verdict: partly supported. Confidence: Medium-High.** Tax is the leading reason to choose and fund the DAF vehicle. It is not the primary reason DAF donors give. The tax advantage is mostly about timing and administration, not size, relative to direct giving.

---

## H6. "Legacy software architecture is necessary because of regulation"

**Precise proposition.** The regulatory regime for DAFs (tax law, IRS reporting, securities and banking rules, state charity law) requires, or so constrains choices that it effectively forces, the legacy system designs incumbents use: batch processing, monolithic recordkeeping, paper rails, closed data.

**Supporting evidence (regulatory constraints that bear on systems)**
- **Recordkeeping and reporting duties are real:**
  - contemporaneous acknowledgements;
  - Form 8283 for noncash gifts;
  - Form 990 Schedule D Part I and Schedule I;
  - dated eligibility snapshots under Rev. Proc. 2018-32 §8.01 [X: IRB 2018-23; R: `direction-data-standards-interoperability.md` §1.3].
- **Sanctions screening** (OFAC) and, for bank- and broker-affiliated sponsors, the parent's vendor-risk and data-security regimes. Reg BI applies to broker-dealer recommendations [R: `industry-incentives-structural-analysis.md` §3.3]. Federal banking agencies' 2023 interagency third-party risk-management guidance (88 FR 37920; not re-read this pass) raises the cost of onboarding a new vendor for bank-affiliated programmes [I].
- **State platform law reaches DAF technology vendors.** California's charitable-platform rules create Type A and Type E duties, though light ones for vendors that do not hold funds [R: `DAF-INDUSTRY-REPORT-2026-11.md`, batch 30].
- **Regulatory uncertainty as a brake.** The 2023 §4966 NPRM is unfinished and has been reframed in the 2026–27 Priority Guidance Plan [R: `regulation-market-structure-portability.md` Q-B09]. A sponsor may defer re-platforming until the rules settle [R: `industry-incentives-structural-analysis.md` §7, H2 "unsupported, Low-Medium"].

**Contradicting evidence**
- **No DAF-specific technology rule exists.**
  - No SEC or FINRA rule, guidance or enforcement specific to DAFs [R: `regulation-market-structure-portability.md` §5; `analyst-and-education-landscape.md` §5.1].
  - No state DAF law in a 51-jurisdiction search, Connecticut excepted [R: `strategic-synthesis.md` §0 A].
  - The reporting duties above specify *data*, not architecture.
- **Modern stacks operate under identical law.**
  - Endaoment publishes an OpenAPI grant API (idempotency keys, async status).
  - Chariot publishes the DAFpay sponsor spec.
  - Daffy runs an MCP server that moves money.
  [R: `direction-data-standards-interoperability.md` §2.3; `direction-ai-product-census.md` §1 item 2]
  None reports a regulatory obstacle to its architecture. Eighteen 2021–2026 entrants show no documented shutdown [R: `strategic-synthesis.md` §0 A; small n].
- **The payment rails modernised; DAF usage did not.**
  - Fedwire moved to ISO 20022 on 2025-07-14 with structured remittance, and the CHAR purpose code exists.
  - ACH CTX supports up to 9,999 addenda.
  - No DAF sponsor documents using any of them. Remittance stays in email, dashboards or letters [R: `direction-data-standards-interoperability.md` §2.4].
  - Paper checks persist with **no statutory check requirement found** [R: `industry-incentives-structural-analysis.md` §6.1].
- **Legacy persistence has non-regulatory explanations with direct evidence.**
  - Vendor-retained IP, no guaranteed export, termination charges and auto-renewal [R: `industry-incentives-structural-analysis.md` §3.8].
  - Migrations freeze grants for about 3–5 weeks. AEF's move kept two years of history [R: AT-A6; `historical-daf-sponsor-technology-lifecycle-2011-2026.md`, AEF section].
  - Affiliated procurement: Fidelity with FMR, Vanguard Charitable with Vanguard, RCF with Ren [R: `industry-incentives-structural-analysis.md` §3.7].
  - Ren's acquisitions show "no observed merging of all acquired ledgers into one architecture". The Blackbaud→Ren lineage dates from 2011 [R: `historical-daf-sponsor-technology-lifecycle-2011-2026.md`, ownership table].
- **Assurance is thin in a way inconsistent with regulation-driven design.** None of 13 vendors publishes a scoped SOC report, and Ren's own boilerplate drifts between "Type 2" and "Type 1" [R: `DAF-INDUSTRY-REPORT-2026-11.md` line ~197; `strategic-synthesis.md` §0 C]. If regulation were driving architecture, one would expect documented control frameworks [I].
- **There is no independent comparative evidence in the market.** No analyst covers DAF platforms [R: `analyst-and-education-landscape.md` §1]. Buyers cannot specify alternatives, which is an informational origin [R: AT §2 C1].

**Alternative explanations**
- "Regulation" may be used loosely to mean *liability aversion* and *parent-company risk policy*. These are real constraints on change velocity, but they are organisational choices, not legal requirements [I].
- **Path dependence.** The core DAF ledgers descend from the 2000s (Kintera/Giving Capital → Blackbaud → Ren). Rewrite cost and migration risk explain persistence without regulation [R: lifecycle file].

**Structural vs habit**
- **Mostly habit and financial** (switching costs, contracts, affiliated procurement, missing standards).
- A **thin structural overlay** (data-retention and reporting duties, bank third-party-risk processes) raises the *cost of change* but does not dictate architecture.

**Evidence quality.** Medium-High on the absence of an architectural mandate: several searches, primary rule texts, and modern operators as existence proofs. Medium on the causes of persistence: contract terms are seen, but executed contracts are not (Q-N04).

**What would change the conclusion**
- A regulator or examiner finding that a modern-stack sponsor's design violated a recordkeeping or control requirement.
- Final §4966/6033 guidance imposing technology-specific record formats.
- Evidence that bank-affiliated sponsors' vendor-risk regimes *prohibit*, rather than slow, cloud or API-based DAF platforms.

**Verdict: contradicted. Confidence: Medium-High.** Regulation shapes what data must exist and who signs. It does not require legacy architecture. Legacy persistence is explained by switching costs, contracts, procurement structure and the absence of standards.

---

## H7. "AI is primarily useful for improving administrative productivity"

**Cross-reference:** AT-A2 ("AI is primarily valuable for grant vetting": contradicted; AI value sits in document-heavy, low-volume, high-value work). That result is reused here. H7 is broader, since it asks whether *admin productivity* is the primary locus at all.

**Precise proposition.** The main value of AI in the DAF system is reducing staff time in sponsor and vendor administration (intake, review, reconciliation, service), as opposed to value in decision quality, risk detection, donor and adviser experience, discovery, or nonprofit-side operations.

**Supporting evidence**
- **Where AI has a modelled case, it is administrative.** The candidates are complex-asset intake (P03), non-standard due diligence (P07), reconciliation (P16) and service agent-assist (P11) [R: `ai-economics-v2-observed-costs.md` §1 item 3].
- Inference cost is immaterial: about $0.45 per heavy review against about $83 of reviewer time [R: `strategic-synthesis.md` §0 B].
- **Vendors' hiring signals:** AI appears in 29.1% of vendor postings against 13.3% of sponsor postings [R: same, §0 B].
- **Deployed nonprofit-side AI is productivity-oriented.** Chariot uses gift-processing and reconciliation AI to compensate for missing remittance standards [R: `direction-data-standards-interoperability.md` §2.4]. Grantmaking-software AI produces application summaries for reviewers [R: `direction-ai-product-census.md` §1 item 4].

**Contradicting evidence**
- **The admin productivity pool is small and narrow.**
  - The large-national value pool is about $445k a year ($202k–$793k), up to $1.06–1.36m with routing.
  - At community foundations under $250m, "do nothing" wins in 87–100% of draws.
  - AI on the existing workflow ranks first in at most 17% of draws in any process.
  - Redesign, not AI, ranks first for routine processes.
  [R: `ai-economics-v2-observed-costs.md` §1; `strategic-synthesis.md` §0 B, G10 "the operations-AI value pool is thin"]
- **Most shipped AI is not sponsor administration.**
  - Donor-side agents: TIFIN Louise, Daffy MCP.
  - Discovery and recommendation: Charity Navigator Horizon, Candid assistant.
  - Fundraising outreach: Blackbaud Development Agent, Bloomerang Penny, Salesforce Agentforce.
  - The large DAF platforms and sponsors ship no generative or agentic AI. Fidelity's assistant is navigation-only.
  [R: `direction-ai-product-census.md` §1 items 2–3, 5–6]
- **Governance points to decision quality, not throughput.** The "flag-only" rule (AI may add a flag, never clear one) makes AI net risk-*reducing* only as an additional detector. Clearing cases to save time *creates* the highest-severity failure (F04) [R: `ai-governance-failure-modes.md` §1 item 2, §4.3]. Under that rule, AI's defensible value is partly *more* review of the right cases, which raises cost.
- **Advice and engagement gaps are larger than admin gaps.** Only 11% of advisers advise on where to grant, and the report itself flags clients' unmet need for guidance on charity evaluation [X: DAFRC 2026 Fig. 5.3 and takeaways]. That is a non-administrative opportunity, though no measured AI outcome exists.
- **Trust risk sits at the donor interface.** 93% of donors rate transparency about AI use as important [R: `ai-governance-failure-modes.md` §1 item 5]. Value there is contingent and unmeasured.

**Alternative explanations**
- **Early-market artefact.** Productivity framing dominates because it is easy to justify in procurement. Value elsewhere is speculative [I].
- **Value may accrue to parties other than sponsors.** Nonprofits (reconciliation), donors (agents) and advisers (prospecting). "Primarily admin" may be true *for sponsors* and false *for the system* [I].

**Structural vs habit**
- **Structural:** liability attaches to the accountable signer (§§4966, 4967 and 4958 knowing-manager taxes), which caps AI to assistive and evidential roles in approval.
- **Habit/informational:** the productivity framing and the absence of outcome measurement.

**Evidence quality.** Low-Medium.
- Pools are scenario figures [S] calibrated to 21 external studies.
- The product census is first-party pages, not usage.
- No measured DAF AI outcome exists anywhere.

**What would change the conclusion**
- A sponsor-published AI pilot with measured handling-time reduction *and* error rates at scale. That would strengthen "admin productivity".
- Measured donor or adviser outcomes from engagement or discovery AI (grant-out rate, payout, satisfaction). That would further weaken it.
- A measured exception and handling-time study (Q-N03).

**Verdict: contradicted as a generalisation (weakly). Confidence: Low-Medium.** Admin productivity is *a* use. In modelled economics it is thin outside document-heavy exceptions, and shipped AI is concentrated elsewhere. Which non-admin use is most valuable remains **insufficient evidence**.

---

## H8. "Existing workflows represent the optimal division of responsibilities"

The parties are the donor, adviser, sponsor, vendor, payment rail and nonprofit.

**Precise proposition.** The current allocation of tasks, costs, data and risk among these six parties minimises total system cost and risk for the legal outcomes required. Moving a task to another party would not improve outcomes.

**Supporting evidence (the legal core is fixed for good reasons)**
- **Sponsor legal control is definitional.** It underpins the donor's completed-gift deduction. Penalties are allocated to the sponsor, managers and donor-advisors [F: §§4966, 4967; IRS DAF page; R: `industry-incentives-structural-analysis.md` §3.4]. Madoff: "if you don't give up dominion and control, you don't get the tax benefits" [R: same file, §8].
- **Specialisation where it pays.** Complex assets go to intermediaries (Dechomai, Realty Gift Fund), and charity data goes to Candid [R: H3 above; `direction-noncash-gift-infrastructure.md` §3].
- **Some reallocations were tried and stalled.**
  - DAF Direct (a sponsor-run widget) stalled per 2015 reporting.
  - Widget UX effects are "unsupported" [R: `industry-incentives-structural-analysis.md` §3.10, §7 H6].
  - [I] Absence of adoption may mean absence of net value.

**Contradicting evidence (the operational allocation is incentive- and habit-shaped)**
- **Nonprofits carry reconciliation cost they cannot control.**
  - Remittance metadata does not travel with payment at any documented sponsor.
  - Only 36% of sponsors in the CF-weighted DAFRC survey default to sharing full donor contact.
  - Nonprofits are price-takers with "structural" weak leverage, Medium-High.
  [R: `direction-data-standards-interoperability.md` §0; `strategic-synthesis.md` §0 E, G4; `industry-incentives-structural-analysis.md` §3.10]
  [I] The party with the least ability to fix the data problem bears it, which is the opposite of an efficient allocation.
- **Processors reallocate charitable intent.**
  - Benevity's $100 check threshold.
  - YourCause redirects to employer-chosen charities after 180 days; PPGF and Benevity redirect to processor-chosen charities.
  - Void windows run from 90 to 180 days.
  - Rules change without notice and contradict themselves.
  [R: `g1913-processor-disbursement-rules.md` §1 items 1, 5, 7]
- **Advisers hold the assets, not the grantmaking.** 56% choose investments, but 11% advise on grants [X: DAFRC Fig. 5.3]. The party paid on balances is not the party engaged in grant-out. That is an incentive tilt toward accumulation, though its effect is unproven [R: `industry-incentives-structural-analysis.md` §1 item 1, wave-2B §9 correction].
- **Sponsors outsource the platform but keep liability.** RCF pays Ren 98% of a specified fundholder-fee base ($19.2m, FY2024). Named Ren receipts are 85.8% from three customers, a concentration and single point of failure [R: `strategic-synthesis.md` §0 C].
- **Donors cannot carry their history or easily move.**
  - None of 12 sponsors publishes an outbound transfer policy.
  - No sponsor commits to carrying grant history.
  - Six of the top 20 sponsors contractually limit automated or third-party access.
  [R: `regulation-market-structure-portability.md` Q-B17; `strategic-synthesis.md` §0 D, G1]
- **Payment rails are under-used.** The rails can carry structured remittance (CTX, ISO 20022, CHAR), but the sponsors read do not use them. Paper checks persist without a legal requirement [R: H6 above].
- **Eligibility verification is duplicated across sponsors.** Each sponsor re-verifies the same recipients. A shared, dated eligibility record is legally usable (Rev. Proc. 2018-32 §8.01 third-party reports) [X; R: H2 above].

**Alternative explanations**
- **Local optimality.** Each party's allocation may be locally rational given its contracts and liability (Clarity "incentives over intent"), yet globally sub-optimal. Nothing in the evidence suggests deliberate misallocation [R: `industry-incentives-structural-analysis.md` §1 item 5].
- **Privacy is a genuine reason** for donor-data defaults: 80% of wealthy DAF users value privacy (BofA 2026). Anonymity choices are a donor right [R: `direction-public-opinion-dafs.md` §3]. Some "information hoarding" is donor-chosen.
- **Untested reallocations may carry hidden costs.** Shifting eligibility to a shared utility concentrates error. Mandatory EFT raises payment-fraud exposure, though cost per rail is unknown [R: `industry-incentives-structural-analysis.md` §6.1 unknowns].

**Structural vs habit**
- **Legal core** (sponsor control, donor advisory status, liability allocation): **structural**.
- **Operational split** (who carries remittance data, reconciliation, eligibility data, transfer service, check versus EFT defaults, data portability): **mixed, leaning habit and incentive**, sustained by fee structures, contracts and missing standards [R: `industry-incentives-structural-analysis.md` §9].

**Evidence quality.** Medium.
- Many direct observations of the allocation and its frictions.
- No end-to-end cost accounting across all six parties, so "optimal" cannot be tested quantitatively. Only dominated allocations can be identified.

**What would change the conclusion**
- An end-to-end cost study showing that nonprofit-side reconciliation and processor holds are small relative to the costs of alternatives such as standards governance and fraud.
- Evidence that sponsor-default EFT or shared eligibility records raise fraud or error materially.
- Conversely, a sponsor that moves remittance into structured payment fields and publishes nonprofit-side savings would confirm the reallocation case.

**Verdict: contradicted for the operational division; supported for the legal core. Confidence: Medium.**

---

## Cross-cutting observations

1. **Education teaches the legal mechanics well and the operating assumptions less well.**
   - The repository's comparison of 11 teaching claims finds the errors in quantitative framing (payout, accounts, fees, who drives adoption), not in law [R: `analyst-and-education-landscape.md` §5.2].
   - H2, H5 and H6 fit the same pattern: correct law, with operational inferences that do not follow.
   - Examples: per-grant review becomes "from scratch"; vehicle-level tax relevance becomes "donors give for tax"; "regulated" becomes "legacy is required".
2. **Who funds the evidence.** The adviser and donor surveys used here are sponsor-funded or sponsor-recruited, and sponsor-affiliated experts are prominent in DAFCP [R: same file, §5.1 and pointers]. This does not invalidate the data. Notably, the sponsor-funded DAFRC adviser study itself contradicts H4 on stated reasons.
3. **The most decision-relevant missing datum is the same for H1, H2 and H7:** measured per-grant handling time split by component (status, purpose and benefit, discretion, operations) at any sponsor (Q-N03).

## Sources read first-hand in this pass (2026-11-21)

- Rev. Proc. 2018-32, IRB 2018-23, §§4.01, 4.04, 5.01, 5.02, 8.01: https://www.irs.gov/irb/2018-23_IRB
- DAFRC, *Financial Planning in the Age of Donor Advised Funds* (2026), Figs. 5.1–5.3 and 6.1–6.2, n=669: https://www.dafresearchcollaborative.org/s/DAF_FinancialAdvisorReport_Final_Web.pdf (served from static1.squarespace.com)
- Chariot summary of the DAFRC National Survey of DAF Donors (2025): https://givechariot.com/resources/insights/breaking-down-the-new-national-daf-donor-survey
- Fidelity Charitable, why donors use a DAF (2022 survey): https://www.fidelitycharitable.org/insights/why-donors-use-a-donor-advised-fund.html
- Fidelity Charitable, granting due diligence: https://www.fidelitycharitable.org/legal/granting-due-diligence.html
- Vanguard Charitable, policies and guidelines: https://www.vanguardcharitable.org/company-policies/policies-and-guidelines
- 2025 BofA Study of Philanthropy page (motivations, 2024 data): https://www.privatebank.bankofamerica.com/articles/2023-bank-of-america-study-of-philanthropy.html
- TIFIN Give complex gifting (Charitable Solutions/Dechomai; 1–3 business days of diligence): https://intercom.help/give-ria/en/articles/9981851-complex-gifting
- AssetMark Charitable complex gifting (same partner and claim): https://intercom.help/assetmark-help-center/en/articles/10644732-complex-gifting

**Not retrieved:**
- The DAFRC donor-survey executive summary. It redirected; the Chariot secondary summary was used instead.
- The BofA 2021 and 2023 full PDFs (404 or not resolved). The historical tax-motive figure therefore rests on a Chronicle search summary only.
- DAFgiving360 pages (robots 403, per the repository).
