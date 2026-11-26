# W7: advisor-channel integration

**Outcome:** donors who reach DAFs through financial advisors get accounts, investment management within mandate, and grant recommendations without re-keying. Advisors see client DAF positions in their own systems (BO-44). The sponsor keeps exclusive control (BO-12) and the advisor keeps the relationship (DD-010).

**Evidence:**
- Distribution is channel-led [I]: the RCF–Ren spine spans about 11 wealth-firm programs (industry report §2.2).
- Six of the top 20 sponsors (about $84bn) contractually restrict automated or third-party access (EV-122).
- Public vendor templates allow batch export but not live integration (EV-123).
- Adviser fees are capped at 1.00% only at MS GIFT, DAFgiving360 and TIFIN Give (EV-068).
- The proposed rule would treat a managing personal adviser as a donor-advisor. It is **proposed only** (REG-034, REG-021).

## 1. First-principles decomposition

| Necessary | Why | Inherited, not necessary |
|---|---|---|
| Donor's *consent* to the advisor's role and scope | Privilege grant under the program agreement | Paper letters of authorization |
| Advisor identity and firm affiliation | Fraud control; fee payment | Re-verifying the advisor per sponsor |
| Mandate constraints (pools, models, fee cap) | Fiduciary / IPS | After-the-fact trade review |
| Position and transaction data to the advisor's systems | The advisor's service to the client | Separate portal logins; nightly CSVs |
| Fee calculation and payment to the advisor | Contract; Reg BI and fiduciary disclosure at the advisor (REG-033) | Manual billing reconciliation |

## 2. Inversion findings
- **What if the advisor never logs into a sponsor portal?** Embed everything through APIs and SSO in the advisor's platform (D-W7-4).
- **What if the platform were invisible to donors?** The advisor's brand fronts it (INN-15, contrarian).
- **What if there were no integration per sponsor–advisor pair?** One delegation standard plus one position feed standard across sponsors (D-W7-5).
- **What if mandate review began before the trade?** Pre-trade mandate checks via API (parent design).

## 3. Competing designs

| ID | Type | Mechanism | Who decides / when | Authoritative data | Humans | Controls | Cost drivers | Experience | INN | Maturity |
|---|---|---|---|---|---|---|---|---|---|---|
| D-W7-1 | Conventional | Paper LOA; advisor portal login per sponsor; nightly position files; manual fee reconciliation; wholesalers explain the program | Sponsor staff set up access; post-trade review | Sponsor recordkeeper | Wholesalers, ops staff | LOA signature; periodic review | Wholesaling, re-keying | Advisor juggles portals; donor fills forms | — | Observed [I] |
| D-W7-2 | Automation-first | E-sign LOA; single sign-on; automated daily files to the advisor's portfolio system | Same | Same | Fewer ops | Same plus SSO | Lower | Fewer logins | INN-16 partial | L1 |
| D-W7-3 | AI-native | Scoped, revocable delegation tokens (INN-16) granted by the donor in-app; partner API with pre-trade mandate checks; event webhooks for positions and grants; advisor copilot drafts proposals, never instructions | Donor grants scope; sponsor policy validates every request | Event ledger | Partnerships for firm onboarding; exceptions | Token scopes; mandate checker; fee cap check | Integration per firm platform, once | Advisor works in own tools; donor consents in-app | INN-16, INN-26 | L3 (delegation tested in PoC, INV-A6) |
| D-W7-4 | **Radical: invisible, embedded DAF** | The DAF is a *feature of the advisor or wealth platform*. Account opening, contributions, grants and statements appear inside the platform's UI through embeddable components and APIs. The sponsor operates behind it, with no sponsor-branded donor portal at all | Sponsor decides everything legally; the advisor platform owns the *interaction*. The donor-facing experience is no longer a sponsor function | Sponsor ledger; platform renders | Sponsor ops invisible; platform service teams handle first-line | Contractual: the platform cannot instruct the sponsor directly, only through request APIs; brand disclosure of the sponsor as legal owner | Revenue share to the platform; low CAC | Donor never leaves the advisor relationship | INN-15 | L1 (L2 premise: channel-led growth [I]) |
| D-W7-5 | Ecosystem: neutral delegation and position-feed standard | Industry standard for DAF delegations and position feeds (like FDX/Open Banking for DAFs), adopted by sponsors and wealth platforms | Each sponsor decides; the standard removes pairwise integration | Each sponsor | Standards body | Standard security profile | Standard governance; adoption | Any advisor platform sees any sponsor | INN-16 | L0 (no standard exists, EV / direction-data-standards) |
| D-W7-6 | Contrarian: advisor as "agent of record" for the grant workflow | Advisors (with donor consent) submit grant recommendations in bulk for client books; sponsor policy processes them like any request | Sponsor policy | Ledger | Exceptions | Proposed-rule exposure if the advisor is treated as donor-advisor (REG-034, proposed); §4958 if fees look like grants | Low | Advisor-driven philanthropy planning | INN-16 | L1 |

## 4. Constraint ledger

| Constraint | D-W7-3 | D-W7-4 radical | D-W7-5 |
|---|---|---|---|
| Legal (exclusive control; advisory privileges; proposed adviser rule) | Survives | Survives if the platform submits *requests only* and sponsor legal ownership is disclosed. Proposed REG-034 would increase scrutiny of adviser-managed setups (still proposed) | Survives |
| Fiduciary (mandate; fee reasonableness) | Survives with fee caps | Revenue share must not become an undisclosed solicitation commission. REG-030: the charitable broker-dealer exemption bars commission-based solicitation. Needs counsel | Survives |
| Accounting | Survives | Survives | Survives |
| Privacy / security | Token scopes | Platform holds donor PII; data-processing agreement; breach exposure doubles | Standard security profile |
| Economic | Integration per platform | Revenue share vs CAC; platform bargaining power | Free-rider problem |
| Operational | Needs partner APIs | Needs a deep platform partnership | Standards take years |
| Human acceptance | Advisors like it | Platforms like it; donors may not know the sponsor | Slow |

**Survivors:**
- D-W7-3 now.
- D-W7-4 as the distribution strategy, gated by counsel review of REG-030 and REG-033.
- D-W7-5 as an industry proposal.

## 5. Cross-industry analogies
- **Banking-as-a-service / embedded finance.** D-W7-4 is the same model. The analogy breaks because DAF assets are irrevocably charitable and the sponsor must keep control. A BaaS bank's equivalent is its regulatory obligations, which are similar in spirit.
- **Open Banking (FDX).** D-W7-5. Breaks where adoption was driven by regulation (UK) or by bank-aggregator economics; no DAF regulator compels it.
- **Insurance managing general agents.** Distribution partners with delegated underwriting. Breaks because a sponsor cannot delegate the grant decision.

## 6. Seven perspectives

| Perspective | Position |
|---|---|
| Inventor | Make the sponsor invisible (D-W7-4) |
| Architect | D-W7-3 is the substrate for D-W7-4. Embedding is a presentation choice on the same APIs |
| Economist | Embedded distribution lowers CAC (the second-largest cost line at 100k accounts: $6.0m of $27.2m in the 09 model) but transfers margin to platforms |
| Regulatory | REG-030 (no commission-based solicitation), REG-033 (Reg BI at the advisor) and REG-034 (proposed) need counsel. Revenue share design is the crux |
| Adversarial | A platform compromise exposes many donors. Platforms may pressure the sponsor to relax grant policy for their clients |
| Customer advocate | Donors prefer one relationship. Nonprofits are indifferent, unless platform branding obscures the donor information they receive |
| Commercial | D-W7-4 is the most defensible distribution: switching costs sit in the platform integration |

**Disagreements:** economist vs commercial on revenue-share levels. Regulatory caution vs inventor on revenue share as a "commission".

**Unresolved:** whether any wealth platform would integrate a non-incumbent sponsor.

## 7. Experiments and recommendation
- **E5 (onboarding):** advisor-initiated onboarding with an upstream attestation (INN-24) vs the form baseline.
- **E11:** CAC sensitivity under the embedded model.

**Recommendation:** adopt D-W7-3; pursue D-W7-4 as the Model C/D distribution thesis; propose D-W7-5.
