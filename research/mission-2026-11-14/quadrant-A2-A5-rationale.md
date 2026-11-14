# DAF Evidence Quadrant: A2 and A5 primary scoring rationale

**Date:** 2026-11-14. **Scorer:** primary. **Status:** *internal-demonstration*. A blind second scorer has not yet reproduced these scores, so they are not independent ([methodology §5](evidence-quadrant-methodology.md)).

**Files.**
- Scores: [`quadrant-scores-A2-primary.csv`](../../data/mission-2026-11-14/quadrant-scores-A2-primary.csv) and [`quadrant-scores-A5-primary.csv`](../../data/mission-2026-11-14/quadrant-scores-A5-primary.csv).
- Engine output: [`quadrant-positions.csv`](../../data/mission-2026-11-14/quadrant-positions.csv), plus the charts [`quadrants/A2-primary.svg`](quadrants/A2-primary.svg) and [`quadrants/A5-primary.svg`](quadrants/A5-primary.svg).
- Queue proposals: [`queue-proposals-quadrant-A2A5.csv`](../../data/mission-2026-11-14/queue-proposals-quadrant-A2A5.csv).

**Scope.** This is the repository's own method. It is not a Gartner Magic Quadrant.

**What the positions mean.** Positions are bands, and they hold only within one area on this one date. Never compare a position in A2 with one in A5.

**Evidence base.**
- The repository files named in the method.
- `vendor-data-rights-matrix.csv` and `daf-user-complaints-corpus.csv`, which arrived during this pass.
- Three live pages fetched this pass, because the repository had almost no evidence on these two providers:
  - Goodstack: [cause verification docs](https://docs.goodstack.io/docs/guides/Cause%20verification/)
  - Every.org: [API docs](https://docs.every.org/docs/intro)
  - Every.org: [payout help page](https://support.every.org/hc/en-us/articles/360059998673-How-long-does-it-take-for-my-donation-to-reach-the-nonprofit)

**Late arrivals.** Three concurrent files arrived after the scores were set: `nonprofit-receipt-cost-by-rail.csv`, `daf-user-complaints-deep-research.md` and `queue-contract-data-rights-agent-controls.md`. They were read, and no score changed. See §7. `queue-infrastructure-nonprofit-costs-emerging.md` was still absent.

## 1. Positions

### A2: Grant disbursement and nonprofit-side DAF rails

| Provider | X (band) | Y (band) | Coverage X/Y | Quadrant |
|---|---|---|---|---|
| Fidelity Charitable EFT (Stripe/ACH) | 2.90 (2.90–2.90) | 2.06 (1.75–2.35) | 1.00/0.85 | Proven Leaders (boundary) |
| PayPal Grant Payments | 2.73 (2.05–3.05) | 2.29 (1.95–2.55) | 0.75/0.85 | Proven Leaders. The Y band dips below the midline. |
| Chariot Disbursements | 2.44 (2.20–2.60) | 2.95 (2.95) | 0.90/1.00 | Proven Leaders |
| Ren Rapid Disbursement Engine | 2.17 (1.95–2.35) | 2.15 (2.15) | 0.90/1.00 | Proven Leaders (boundary) |
| Chariot DAFpay | 2.00 (2.00) | 2.75 (2.75) | 1.00/1.00 | Proven Leaders. X sits exactly on the midline, so treat it as Forward Builder/Leader boundary. |
| DAF Direct | 1.67 (1.25–2.25) | 2.00 (1.20–2.80) | 0.75/0.60 | Forward Builders (boundary) |
| Every.org | 1.44 (0.65–2.85) | 2.24 (1.90–2.50) | 0.45/0.85 | Insufficient evidence (hollow marker) |

**Reading.** No A2 rail is clearly a leader on both axes:
- **Fidelity EFT** and **PayPal Grant Payments** lead on execution, because they carry the most volume through the largest sponsors.
- **Chariot Disbursements** has the strongest forward profile: a public API, multi-sponsor reach and a documented boundary on approval authority. Its execution is mid-tier.
- **Ren RDE** sits at the centre. Its scale is vendor-claimed, its SOC claims conflict, and it uses each sponsor's own bank rails.

### A5: Charity eligibility and verification data

| Provider | X (band) | Y (band) | Coverage X/Y | Quadrant |
|---|---|---|---|---|
| IRS BMF / Pub 78 / TEOS (reference point) | 3.45 | 2.94 (2.50–3.10) | 1.00/0.85 | Proven Leaders (baseline) |
| Candid (GuideStar APIs / Charity Check) | 3.20 (2.40–3.40) | 2.65 | 0.75/1.00 | Proven Leaders |
| Chariot verification | 2.22 (2.00–2.40) | 2.69 (2.15–2.95) | 0.90/0.80 | Proven Leaders. Its X lower bound touches the midline. |
| Benevity validation | 2.41 (2.05–2.65) | 1.85 | 0.85/1.00 | Scale Operators |
| Goodstack | 2.00 (0.30–3.70) | 2.38 (1.55–2.95) | 0.15/0.65 | Insufficient evidence (hollow marker) |

**Reading.** The free public baseline outscores every commercial provider on both axes:
- **Candid** earns its execution score from documented reliance on it. RCF's policy says Charity Check is adequate risk mitigation for more than 98% of its grants.
- **Commercial forward value** lies in faster refresh (weekly IRB updates), OFAC bundling, handling of churches and unlisted organizations, and API delivery. It does not lie in a different source of truth.

## 2. Key judgment calls

1. **Chariot is split into two A2 entries.**
   - **Disbursements** is a payout rail for grantmakers.
   - **DAFpay** is donor checkout on the nonprofit side. It has different customers, a different delivery record and its own complaint signal.
   - Graph edges E109 and E151 (DAFgiving360, Thrivent) count only toward DAFpay. Red-team finding RT-2B confirmed that these edges are checkout access, not disbursement.
   - **Chariot verification** is a third entry, scored in A5.
2. **PayPal Giving Fund complaints are not applied to PayPal Grant Payments.** The repository records that these are distinct services ([reconciliation evidence §8](../daf-cross-institution-reconciliation-evidence-2026-11-11.md)). Grant Payments X6 is therefore U.
3. **Fidelity EFT X1 = 4 is classed `secondary`.** The 67% EFT share and roughly 1m checks come from Chariot's summary of Fidelity's report ([Chariot, Mar 2026](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report)). Validation V2B-13 found this only partially confirmed.
4. **Fidelity EFT Y5 = 1 rests on positive evidence of fragmentation, not on missing evidence.** Two documented facts support it ([Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)):
   - Nonprofits must enrol with each sponsor separately.
   - Reissuing a lost check requires action from the recommending donor.
5. **The electronic-only claim for July 2026 does not reduce Fidelity's X2.** The claim was made by Chariot, not by Fidelity (AVD35). Fidelity's own live FAQ says EFT is "not currently required".
6. **Ren RDE X3 = 1.** The two SOC claims, both hosted by AEF, conflict: Type II in July 2025 and Type I in April 2026. Under the rubric, contradictory assurance falls below "vendor-stated SOC 2".
7. **Ren RDE X4 = 3 is an inference.** It assumes Ren's administration channels also carry RDE payments. No program is confirmed to use RDE (queue question P-QA2-03).
8. **IRS Y3 is U, meaning not applicable.** It is not 0, because a data source has no automation to govern. IRS X3 = 3 rests on reliance under Rev. Proc. 2018-32, which was read only in secondary form, so its class is `secondary`.
9. **Candid X1 is classed `validated`.** Validation V2A-23 confirmed the RCF policy text.

## 3. Per-provider justification

### A2

**Chariot Disbursements**

| Criterion | Score | Evidence |
|---|---|---|
| X1 | 2 | Named customers include Daffy, which reports more than $380M sent electronically ([Daffy](https://www.daffy.org/resources/electronic-donations-chariot)). Others: TIFIN Give/GiveClear ([TIFIN](https://tifin.com/news/tifin-and-chariot-partner-to-transform-grant-payments/19418/)), Founders Pledge, Groundswell, GoodToday, Brooklyn Org, SPMF, and Charityvest from Aug 2026. None of the top three sponsors uses it. |
| X2 | 3 | Moved from beta ([changelog](https://docs.givechariot.com/changelog/2025/3/17)) to general availability to customer use. |
| X3 | 2 (vendor claim) | Vendor-stated SOC 2 Type II ([security](https://help.givechariot.com/onboarding/trust-and-safety/security)). |
| X4 | 3 | Eight confirmed edges in the graph. |
| X5 | 2 | $11M Series A ([Chariot](https://www.givechariot.com/resources/insights/chariot-announces-11-million-series-a-investment-round-led-by-maveron)). Depends on a bank partner, Column N.A. |
| X6 | U | No evidence. |
| Y1 | 3 | Versioned API with write scopes and statements in BAI2/CSV ([OAuth docs](https://docs.givechariot.com/v2026-04-01/guides/oauth.md)). |
| Y2 | 3 | Electronic deposit, claim flow, check fallback and webhook status ([docs](https://docs.givechariot.com/guides/disbursements)). |
| Y3 | 3 | The sponsor keeps approval authority ([addendum](https://www.givechariot.com/dafpay-provider-addendum)). Grant creation is idempotent, and webhooks deliver at least once with retries ([webhooks](https://docs.givechariot.com/api/webhooks)). |
| Y4 | 4 | Customers span the consumer, wealth, community-foundation, corporate and effective-altruism segments. |
| Y5 | 2 | Charityvest moved in from PayPal ([Chariot](https://givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner)). Terms for leaving are not published. |

**Chariot DAFpay**
- X1 2, X4 2: access methods for DAFgiving360 and Thrivent ([llms.txt](https://www.givechariot.com/llms.txt)) and a GoFundMe Pro beta ([GoFundMe](https://prosupport.gofundme.com/hc/en-us/articles/49765186392731-Accept-donor-advised-fund-gifts-with-DAFpay)).
- X2 2: Donor Accounts and FDX remain in beta with no named production user (AVD22, AVD23).
- X6 2: mixed reviews ([App Store](https://apps.apple.com/us/app/dafpay/id6633440388)). Five are praise. One high-severity review reports a Fidelity integration failure. One reviewer could not close their account. The IPS raised a privacy critique.
- Y1 3: DAF providers must expose donor, fund, grant and status endpoints ([endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md)).
- Y2 2: settlement still depends on each sponsor's own rail, and GoFundMe Pro records a DAFpay gift as an "offline transaction".
- Y3 3: approving a donor account is explicitly not approving a grant.
- Y5 3: works across many sponsors, against a lock-in signal: a default 2.9% fee and loss of access on termination ([terms](https://www.givechariot.com/legal-nonprofit)).

**PayPal Grant Payments**
- X1 3: Vanguard paid $130M in its first four months ([PR Newswire](https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html)) and more than $1B to over 13,000 charities by Nov 2024 ([NonProfit PRO](https://nonprofitpro.com/article/vanguard-charitable-donors-gave-more-than-3b-in-fiscal-year-2024)). NPT also uses it ([NPT](https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf)).
- X2 3: announced in 2022 ([PayPal](https://newsroom.paypal-corp.com/2022-08-25-PayPal-Launches-Grant-Payments,-Enabling-Charities-to-Quickly-Receive-Funds-from-Grantmakers)) and delivered with published metrics.
- X4 2: Vanguard, NPT and Every.org payouts. It lost Charityvest.
- X5 3: parent company files audited statements ([PayPal SEC filings](https://investor.pypl.com/financials/sec-filings/default.aspx)).
- Y1 2: charity-side transaction ID, grant details and download ([help](https://www.paypal.com/us/cshelp/article/what-are-grant-payments-help883)). No public API was found.
- Y2 3: accept/decline, grant status, expiry and retry.
- Y5 2: shared across sponsors. Donor-data use is restricted ([charity terms](https://www.paypal.com/us/legalhub/paypal/pp-confirmed-charity-tnc?locale.x=en_US)).
- X3, X6, Y3: U.

**Ren Rapid Disbursement Engine**
- X1 2 (vendor claim): the launch release claims more than 100k grants and $500M ([PR Newswire](https://prnewswire.com/news-releases/ren-debuts-rapid-disbursement-engine-expanding-philanthropic-services-to-meet-rapid-daf-growth-301999647.html)).
- X2 2 (vendor claim): all delivery evidence is vendor language ([payments page](https://www.reninc.com/payments/); [AEF 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)).
- X3 1: the SOC claims conflict.
- X4 3: inherits Ren's channel edges (inference).
- X5 3: private-equity backing ([Great Hill](https://www.businesswire.com/news/home/20251028702541/en/Great-Hill-Partners-Announces-Strategic-Growth-Investment-in-Philanthropy-Tech-Platform-Ren)) and audited RCF fee disclosures ([RCF audit](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)).
- Y1 2: data return is contractual ([MSA](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf)). There is no public API.
- Y2 2: ACH, check and positive pay run on each sponsor's own rails.
- Y3 2: vetting, staff approval and divestment are separate steps ([product descriptions](https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf)).
- Y4 3: wealth, AEF and bank sponsors.
- Y5 2: the iPhi MSA promises export within 15 days.
- X6: U.

**Fidelity Charitable EFT**
- X1 4 (secondary): scale, as discussed in judgment call 3.
- X2 3: EFT has been live since 2014 ([Fidelity](https://www.fidelitycharitable.org/about-us/news/10-23-2014.shtml)).
- X3 2: the audit covers financial statements, not EFT controls ([audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)).
- X4 2: a rail for a single sponsor.
- X5 4: long operating history and audited statements.
- X6 2: the check-path failures reported are the kind EFT removes ([Bogleheads](https://www.bogleheads.org/forum/viewtopic.php?t=457510)), and the ACH enrolment queue can take weeks.
- Y1 2: Stripe export and an emailed ACH report.
- Y2 3: a stated digital-first transition ([FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html)), but about 33% of grants still go by check.
- Y4 2: serves one sponsor's donors.
- Y5 1: fragmentation, as discussed in judgment call 4.
- Y3: U.

**DAF Direct**
- X1 1: 1,251 charities by 2015, described as a "slow road" ([Chronicle](https://www.philanthropy.com/news/effort-to-spur-giving-from-donor-advised-funds-online-appears-to-stall/)).
- X2 2: the widget was delivered ([Fidelity 2013](https://fidelitycharitable.org/about-us/news/daf-direct-brings-new-giving-option-to-nonprofits.html)), but adoption stalled.
- X4 2, X5 2, Y2 2, Y4 2, Y5 2: three sponsors. The `fmr.com` contact suggests Fidelity operates it (inferred; [dafdirect.org](https://www.dafdirect.org/)). It offers only grant initiation from the nonprofit's site.
- X3, X6, Y1, Y3: U.

**Every.org** (insufficient evidence)
- X1 1 (vendor claim): three API partners.
- X4 2, Y2 2, Y5 3: pays out through Stripe weekly or on demand, PayPal Grants every 4–5 weeks, ForGood with a 1.5% fee, or Network for Good in monthly lump sums with a $10 minimum ([help](https://support.every.org/hc/en-us/articles/360059998673-How-long-does-it-take-for-my-donation-to-reach-the-nonprofit)).
- Y1 2: free APIs, but "no programmatic donations or disbursements via API" ([docs](https://docs.every.org/docs/intro)).
- X2, X3, X5, X6, Y3: U.

### A5

**IRS BMF / Pub 78 / TEOS** (reference point)
- X1 4, X4 4: the IRS files sit upstream of every checker that discloses its sources (edges E153 and E154).
- X2 3: monthly updates. Pub 78 was last updated 2026-09-10 ([IRS bulk data](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads)).
- X3 3: Rev. Proc. 2018-32 lets grantors rely on the listings ([Tax Adviser](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/)).
- X5 4: statutory federal source.
- X6 2: donors report lag for new charities and slow church verification ([Bogleheads](https://www.bogleheads.org/forum/viewtopic.php?t=294702)).
- Y1 3: bulk files only, with no real-time API.
- Y2 2: monthly snapshots, gaps for churches, and a revocation list that must be checked for reinstatement ([auto-revocation](https://www.irs.gov/autorevocationlist)).
- Y4 3: covers all exempt-organization types, with structural gaps.
- Y5 4: public domain and keyed by EIN.

**Candid**
- X1 4 (validated): RCF policy, more than 98% of grants ([RCF](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf)).
- X2 3: Claude connector delivered ([Anthropic](https://www.anthropic.com/news/claude-for-nonprofits)).
- X4 3: [Charity Check FAQ](https://developer.candid.org/docs/faqs-charity-check), Groundswell, Ren iPhi.
- X5 2: the Chronicle reports staff cuts ([Chronicle](https://www.philanthropy.com/news/candid-cuts-staff-bets-its-future-on-ai/)); the cut size is unverified.
- Y1 3: [developer portal](https://developer.candid.org/).
- Y2 3: weekly IRB updates plus OFAC.
- Y3 2: AI assistant and a read-only MCP connector ([Candid](https://candid.org/press/candid-partners-with-anthropic-to-bring-trusted-data-to-claude-for-nonprofits/)).
- Y4 3, Y5 2: outputs are keyed by EIN and include PDFs.
- X3, X6: U.

**Chariot verification**
- Y2 3: six sources, of which only four are named (IRS BMF, Form 990, Pub 78, OFAC), plus a church path using the IRS 14-point criteria ([compliance](https://help.givechariot.com/onboarding/trust-and-safety/compliance); [unlisted organizations](https://help.givechariot.com/onboarding/unlisted-organizations)).
- Y3 3: verification is input evidence, and the sponsor decides ([addendum](https://www.givechariot.com/dafpay-provider-addendum)).
- Y1 2: the database is proprietary.
- X3 2 (vendor claim): vendor-stated SOC 2.
- Y5, X6: U.

**Benevity validation**
- X1 3: the AOGF Form 990 reports $1.56B in contributions ([ProPublica](https://projects.propublica.org/nonprofits/organizations/810739440/202642259349301349/IRS990ScheduleF)). The claim of "2.5M continuously validated" nonprofits is vendor-stated ([Benevity](https://benevity.com/)).
- X2 2 (vendor claim): Match Assurance reports 500+ clients ([Benevity Live](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026)).
- X5 3: Hg ownership ([BetaKit](https://betakit.com/british-private-equity-investor-hg-to-acquire-controlling-stake-in-benevity/)).
- X6 2: nonprofits report payment delays and a check fee of $35 or 8% ([Trustpilot](https://www.trustpilot.com/review/benevity.com)).
- Y3 1 (vendor claim): AI reads receipts, verifies eligibility and auto-submits. Oversight is not described.
- Y5 2: the Alaya migration path ([help](https://causeshelp.benevity.org/hc/en-us/articles/44498461447572-The-Alaya-product-is-moving-to-Benevity)).

**Goodstack** (insufficient evidence)
- Y1 3: OpenAPI docs and webhooks.
- Y2 2: configurable eligibility checks.
- Y4 2: discount and credit programs.
- X3 2 (vendor claim): SOC 2 and ISO 27001 badges ([docs](https://docs.goodstack.io/docs/guides/Cause%20verification/)).
- X1, X2, X4, X5, X6, Y3, Y5: U. There are no named customers, data sources or coverage figures.

**Not scored**, because evidence is too thin or the provider is out of scope:
- The Giving Block "Accept DAF Grants"
- GivingIQ EasyDAF
- Charity Navigator API ([API](https://www.charitynavigator.org/products-and-services/api/)). It is rating-oriented, not a source of record for eligibility.

## 4. AI-governance overlay (flag, not axis)

The rule tested is "AI may add a flag, never clear one" ([ai-governance-failure-modes.md](ai-governance-failure-modes.md)).

| Provider | Evidenced AI | Flag |
|---|---|---|
| Chariot (Disbursements, DAFpay, verification) | No AI in the grant, payment or eligibility decision path. A separate Gift Processing product uses LLMs to code gifts for CRMs (U09; no error rates). | **Consistent.** The sponsor keeps final authority by contract. |
| PayPal Grant Payments, Fidelity EFT, Ren RDE, DAF Direct, Every.org | None evidenced on the rail. Ren's "over half instantly approved" claim is rule automation, not evidenced AI. | **No AI evidenced.** For Ren, the controls behind instant approval are undisclosed. |
| Candid | AI assistant and a read-only MCP connector | **Consistent (read-only).** |
| IRS | n/a | n/a |
| Benevity | Match Assurance AI verifies eligibility and auto-submits (deployed, per vendor) | **At risk.** AI may effectively clear eligibility, and human override and audit trail are undocumented (P-QA2-06). |
| Goodstack | None evidenced | No AI evidenced |

## 5. Unknowns that matter most

- **Recipient experience on most rails.** A2 X6 is U for Chariot Disbursements, PayPal Grant Payments, Ren RDE and Every.org. The complaint corpus is mostly from donors.
- **Assurance.** No A2 or A5 provider has a SOC report whose scope has been inspected.
- **Ren RDE.** Which programs use it, and the true grant volume.
- **Every.org and Goodstack.** Basic scale and durability.
- **Exit terms.** Interoperability terms for leaving any rail: history export, and nonprofit re-enrolment.
- **Candid.** Licence and export terms, and current refresh cadence.
- **Recipient staff-time and float estimates.** The values in `nonprofit-receipt-cost-by-rail.csv` are partly assumed, so they were not used to score X6.

## 6. What would move providers

| Provider | Upward | Downward |
|---|---|---|
| Chariot Disbursements | A scoped SOC 2 report (X3→3–4). Charityvest turnkey or a top-3 sponsor adopting it (X1/X4). Published exit and history-export terms (Y5). | Evidence of failures concentrated at Column N.A. Long betas stalling. |
| PayPal Grant Payments | A public API or a schema for sponsor-side status (Y1). Recipient settlement metrics (X6). | Further sponsor losses after Charityvest. Recipient complaints. |
| Ren RDE | Confirmed RDE use by named programs, with independent volume data (X1/X2 above the cap). Resolving the SOC claims (X3). | A confirmed SOC Type I-only status. A nonprofit complaint pattern. |
| Fidelity EFT | A confirmed EFT-only policy, plus a portable or shared nonprofit enrolment (Y2/Y5). | Holds on non-enrolled charities causing harm (X6). |
| DAF Direct | A current adoption figure. | Evidence that it has been retired. |
| Every.org | A Form 990 and payout volumes (lifts coverage above 0.5). | — |
| Candid | A SOC report. Published licence and export terms. | A confirmed headcount shrinkage that affects data quality. |
| Benevity | Documented human-in-the-loop for Match Assurance (Y3→3). | False approvals caused by the AI. |
| Goodstack | Named customers and data sources. | — |
| IRS | A real-time API, or shorter refresh lag. | Coverage regressions. |

**Re-scoring triggers** follow methodology §5. The blind second scorer should re-score from these same files and the URLs listed above.

## 7. Cross-check against late-arriving files (no score changes)

- **[`nonprofit-receipt-cost-by-rail.csv`](../../data/mission-2026-11-14/nonprofit-receipt-cost-by-rail.csv).** These figures support the existing notes. They do not change any score.
  - $0 to the nonprofit on four rails: Fidelity ACH/Stripe (R04, R05), PayPal Grant Payments (R06; high case only with optional instant transfer), Chariot Disbursements (R10) and DAF Direct (R11).
  - $29 per $1,000 on DAFpay default terms (R07). This supports the lock-in signal behind DAFpay's Y5 score.
  - 1.5% on Every.org's ForGood route (R13).
- **[`daf-user-complaints-deep-research.md`](daf-user-complaints-deep-research.md).** Two findings, neither of which changes a score:
  - Bogleheads quotes a Fidelity notice of EFT-only delivery from 2026-07-01, which was later extended. This supports Fidelity's Y2 = 3 (digital-first transition under way). It does not affect X2, because the live FAQ still says EFT is not required.
  - Chariot/DAFpay's mixed record matches X6 = 2.
- **[`queue-contract-data-rights-agent-controls.md`](queue-contract-data-rights-agent-controls.md).** Two findings, both consistent with existing scores:
  - Chariot's disbursement approvals record who approved them (`approved_by`). This supports Chariot Disbursements Y3 = 3.
  - Ren returns only materials the customer *provided*, not records the platform generated. This is consistent with Ren RDE Y1 = 2 and Y5 = 2, and is a candidate for a downward move on re-score.
