# Evidence Quadrant A1: DAF platform and administration (system of record). Primary scorer rationale

**Date:** 2026-11-14. **Scorer:** primary. **Status:** *internal-demonstration*. A blind second scorer has not yet reproduced these positions (methodology §5).
**Scores:** [`data/mission-2026-11-14/quadrant-scores-A1-primary.csv`](../../data/mission-2026-11-14/quadrant-scores-A1-primary.csv): 12 providers × 11 criteria = 132 rows. **Engine output:** [`quadrant-positions.csv`](../../data/mission-2026-11-14/quadrant-positions.csv) and [`quadrants/A1-primary.svg`](quadrants/A1-primary.svg).
**Method:** [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md). This is the repository's own method. It is not a Gartner Magic Quadrant. Positions are bands, not points. Where there was no admissible evidence the score is U, never 0. Vendor self-claims carry `vendor_claim` and the engine caps them at 2.

## 1. Positions

| Provider | X (band) | Y (band) | Coverage X / Y | Quadrant (engine) |
|---|---|---|---|---|
| Ren (incl. iPhi/Stellar, DFX) | 2.67 (2.40–2.80) | 2.30 (2.30) | 0.90 / 1.00 | Proven Leaders |
| Fidelity Charitable (in-house, FMR) | 3.29 (2.80–3.40) | 2.00 (1.50–2.50) | 0.85 / 0.75 | Proven Leaders (boundary) |
| Foundation Source (DAF OS / Vennfi) | 2.12 (1.80–2.40) | 2.18 (1.85–2.45) | 0.85 / 0.85 | Proven Leaders (boundary) |
| Give Interactive | 2.25 (1.35–2.95) | 2.00 (2.00) | 0.60 / 1.00 | Proven Leaders (effectively boundary, see note) |
| TIFIN Give | 2.44 (2.20–2.60) | 1.85 (1.85) | 0.90 / 1.00 | Scale Operators |
| Foundant CommunitySuite | 2.10 (2.10) | 1.80 (1.35–2.35) | 1.00 / 0.75 | Scale Operators (boundary) |
| NPact (FIMS / DonorCentral) | 1.45 (0.80–2.60) | 1.25 (0.75–2.35) | 0.55 / 0.60 | Focused Specialists |
| Blackbaud FE NXT (foundations) | 2.20 | 2.62 | 0.75 / **0.40** | insufficient evidence |
| NPT GivingPoint (sponsor-built; added) | 3.45 | 2.00 | 0.55 / **0.40** | insufficient evidence |
| NCF (sponsor-built, Salesforce) | 2.18 | 1.00 | 0.55 / **0.15** | insufficient evidence |
| SVCF (sponsor-built, Salesforce) | 3.00 | n/a | **0.35** / **0** | insufficient evidence |
| Givinga | 2.00 | 1.73 | **0.35** / 0.55 | insufficient evidence |

**How to read this table:**
- **The field is clustered at the midlines.** Seven of the twelve providers are within about 0.5 of (2, 2). The quadrant labels therefore separate them less than the bands do. The most robust statements are relative ones:
  - Ren and Fidelity Charitable lead on execution.
  - NPact trails on both axes.
  - TIFIN Give's forward score is held back by closed terms and AI without stated controls, not by weak product delivery.
- **Engine note.** Give Interactive's X band (1.35–2.95) crosses the midline. Its point sits exactly 0.25 from 2.0, and the engine flags "boundary" only below 0.25, so the label omits it. Its Y of 2.0 rests on three criteria that are vendor claims capped at 2. Read it as boundary on both axes.
- **Sponsor-built platforms are not like-for-like with vendors.** Fidelity, NPT, NCF and SVCF score their own book only. Y4 (segment breadth) and X4 (channels) structurally favour multi-client vendors.

## 2. Per-provider justification

### Ren (incl. iPhi/Stellar, DonorFirstX): Proven Leaders, low margin
**X: 2.67**
- **Footprint.** The broadest evidenced third-party footprint:
  - "DFX powered by Ren" footers on 10+ RCF wirehouse portals, MS GIFT and BofA CGF ([msgift.donorfirstx.com](https://msgift.donorfirstx.com/); [edwardjones.donorfirstx.com](https://edwardjones.donorfirstx.com/)).
  - AEF fully migrated to Ren ([AEF upgrade timeline](https://engage.aefonline.org/upgrade-timeline/)).
  - iPhi live at the Cleveland Foundation and ImpactAssets ([iphiview.com](https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx)).
- **X4 = 4.** Ren has 54 graph edges, the most of any node.
- **X1 = 3, not 4.** Publicly evidenced Ren sponsors hold only about 9% of DAFRC FY2024 assets (V2B-05). Ren's ">60%" claim is disputed (V2B-04) and was not used.
- **X3 = 1.** The SOC 2 claims are Type 2 (2025), then Type 1 (2026), with no report or scope ([AEF 2026 release](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)).
- **X2 = 2.** The delivery record is mixed (AVD01–08).
- **X5 = 3.** Supported by PE ownership and the audited RCF contract ([RCF audited FS 2024](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)).
- **X6 = U.** No Ren-attributed complaint pattern was found.

**Y: 2.30**
- **Y4 = 4.** Broadest segment reach: wealth, bank, independent national, community, impact and university.
- **Y1 = 2.** The public MSAs return only "Customer Materials". The iPhi MSA gives a 15-day export window. API integration is a paid add-on and there are no public docs ([RAC MSA](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf); vendor-data-rights-matrix).
- **Y5 = 2.** The AEF migration was delivered, but the new portal shows only two years of history ([AEF DC sunset](https://engage.aefonline.org/dc-sunset/)).
- **Y3 = 2.** Rules-based "instant" approval sits on RCF's published risk-tiered policy ([RCF due-diligence policy](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf)). No AI is evidenced.

**Overlay:** GREEN/none. No AI claims. Automation is deterministic and sits under sponsor policy. Decision logs are not public.

**Biggest unknowns:**
- What sits behind the ">60%" claim (NPT? community-foundation endowments?).
- SOC report type, scope and entity.
- The full-fidelity export schema.

**What would move it:**
- A reconciled customer list by EIN: X1 to 4.
- A SOC 2 Type 2 report with stated scope: X3 to 3.
- A documented full-history export, or public API docs: Y1/Y5 to 3.

### Fidelity Charitable (sponsor-built, FMR-administered): Proven Leaders (boundary)
**X: 3.29**
- **X1 = 4 and X5 = 4.** Audited $85.9bn, operating since 1991 ([audited FS FY2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)).
- **X2 = 3.** EFT, crypto and DAF Direct were all delivered. The "electronic-only July 2026" item is Chariot's claim, and Fidelity's own FAQ contradicts it ([FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html)).
- **X6 = 2.** The complaint corpus holds 74 records, 35 of them high or critical (app UX, account access), plus 11 praise records. The rate relative to Fidelity's donor base is unknown.
- **X3 = U.** No nonprofit-specific SOC report was found, and affiliate reports are not imputed.

**Y: 2.00**
- **Y2 = 2.** Stripe/ACH EFT, but EFT is not required.
- **Y3 = 2.** The virtual assistant is navigation-only, with disclaimers ([terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html)).
- **Y5 = 2.** Inbound transfers only; no history portability.
- **Y1 = U.** No public API was found. Absence is not scored 0.

**Overlay:** GREEN (conservative, donor-side navigation only).

**Unknowns:**
- Whether any vendor components (for example Ren, per the 60% arithmetic) sit inside FMR's stack.
- Data-export rights.

**What would move it:**
- A published API or export policy: Y1.
- Disclosure of the platform vendor: which provider this row represents.

### Foundation Source (DAF OS / Vennfi): Proven Leaders (boundary)
**X: 2.12**
- **X1 = 2.** Named customers: Charityvest, TIAA, Temple and OneGive ([TIAA release](https://www.tiaa.org/public/about-tiaa/news-press/press-releases/2026/09-28)). FS self-reports 20,000 DAF accounts.
- **X2 = 2.** DAF OS has no named sponsor customer (AVD33).
- **X5 = 3.** GTCR owner and a diversified private-foundation book ([FS 2026-09-30](https://foundationsource.com/newsroom/press-releases/foundation-source-appoints-new-technology-and-product-leaders-to-advance-philtech-platform/)).
- **X3 = U.** No SOC claim was found.

**Y: 2.18**
- **Y1 = 2 (vendor claim).** DAF OS is marketed as "programmable" ([brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/)), with no docs.
- **Y2 = 2.** Charityvest is moving to Chariot electronic disbursements ([Chariot](https://givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner)).
- **Y4 = 3.** Consumer, wealth and university.
- **Y5 = 2.** BridgeFT multi-custody ([FS 2025-09-23](https://foundationsource.com/newsroom/press-releases/foundation-source-elevates-turnkey-daf-platform-with-advisor-branded-multi-custodial-flexibility/)).
- **Y3 = U.** AI is intent only (AVD34).

**Overlay:** none evidenced. A new CTO and Head of Product have an "increased focus on AI". Watch.

**Unknowns:**
- DAF OS customers.
- SOC scope.
- Sponsor contract data rights.

**What would move it:**
- A named DAF OS sponsor customer, or published API docs: X2, Y1.

### Give Interactive: Proven Leaders label, effectively boundary
**X: 2.25, coverage 0.60**
- **X1 = 2.** Vanguard Charitable selected Give Interactive for DAF recordkeeping, but go-live is not evidenced ([PR Newswire](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html)). The Signatry log-in runs on its domain ([log-in](https://thesignatry.giveinteractive.com/log-in)).
- **X3 = 3, secondary.** SOC 2 Type 2 plus a public SOC 3 (Sept 2025), scoped to the DAF platform ([BD Emerson case study](https://www.bdemerson.com/case-studies/give-interactive)). This is the best-scoped assurance in the area.
- **X2 = U and X5 = U.** No delivery evidence and no ownership or funding data.

**Y: 2.00**
- Rests mainly on vendor claims capped at 2: an "open API", §4943 monitoring automation and data migration ([site](https://www.giveinteractive.com/); [fund of funds](https://www.giveinteractive.com/post/fund-of-funds-platform)).
- **Y4 = 3, primary.** National, faith and community-foundation clients.

**Overlay:** AMBER-unverified. "AI tools" and "intelligent" are vague and no controls are documented.

**Biggest unknowns:**
- Vanguard go-live and scope.
- Full client list.
- Ownership.

**What would move it:** a confirmed Vanguard production cutover would push X1 to 3–4 and resolve X2. That single fact could move Give Interactive into a clear Proven Leader position.

### TIFIN Give: Scale Operators
**X: 2.44**
- **X2 = 3.** The best announced-vs-delivered ratio in the area (AVD09–16; for example the [Tax Intelligence help doc](https://intercom.help/bluegive-help-center/en/articles/12326914-using-tax-intelligence)).
- **X4 = 3.** SEI, AssetMark, Confluence and others ([SEI](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)).
- **X1 = 2.** The GiveClear book is small: $372M AUM ([GiveClear](https://www.giveclear.org/reports-and-financials)).
- **X3 = 2.** SOC 2 is vendor-stated, with no type.

**Y: 1.85**
- **Y2 = 3.** The Chariot electronic rail is live ([AssetMark help](https://intercom.help/assetmark-help-center/en/articles/13931732-chariot-program-overview)).
- **Y1 = 1.** The published terms bar automated access and downloading and grant no export right ([terms](https://intercom.help/give-ria/en/articles/10092486-terms-of-use)).
- **Y3 = 1.** Louise "executes real donor requests" with no limits stated ([release](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html)).

**Overlay:** RED-candidate. Louise executes, and the boundary with GiveClear's grant approval is undocumented. It may breach "AI may flag, never clear" if execution bypasses sponsor approval.

**What would move it:**
- Published Louise controls (limits, confirmation, sponsor-approval separation, audit log): Y3 to 2–3, crossing the Y midline.
- A customer-agreement export clause: Y1.

### Foundant CommunitySuite: Scale Operators (boundary)
**X: 2.10, full coverage**
- Several criteria are vendor claims capped at 2: "700+ CFs", $62B and 99% renewal ([product page](https://www.foundant.com/products/communitysuite/)), and SOC 2 Type 2 ([Foundant](https://www.foundant.com/?p=1611)).
- **X5 = 3.** The SmartSimple merger ([BusinessWire](https://businesswire.com/news/home/20240813514222/en/Foundant-Technologies-and-SmartSimple-Software-Announce-Strategic-Merger-to-Revolutionize-Philanthropic-and-Grant-Management-Solutions)).
- **Likely understated.** Foundant is probably the largest community-foundation ledger by count, but the cap holds until independent corroboration exists. The 700+ claim also exceeds a plausible share of DAFRC's 803 community-foundation sponsors.

**Y: 1.80**
- **Y1 = 2.** Self-service exports plus a paid API add-on ([help center](https://support.foundant.com/hc/en-us/articles/35148153853847-Integrations)).
- **Y4 = 1.** Community foundations only.
- **Y2 = U.** No grant-rail evidence.

**Overlay:** AMBER. Fia is in beta, with a policy engine and bias screening claimed but not documented ([Fia release](https://www.financialcontent.com/article/gnwcq-2026-9-2-foundant-introduces-fia-a-new-ai-platform-built-for-social-good-organizations)).

**What would move it:**
- An EIN-level list of community-foundation clients: X1 to 3–4.
- An ACH or electronic grant-payment feature: Y2.

### NPact (FIMS / DonorCentral): Focused Specialists
**X: 1.45**
- **X1 = 2.** "Hundreds" of foundations (2022) ([PR Newswire](https://prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html)).
- **X4 = 1.** NPact lost AEF, its largest evidenced DAF customer, to Ren ([AEF notice](https://www.aefonline.org/donorcentral-transition-notice/)).
- **X5 = 1.** Tech Impact reports users migrating off FIMS ([Tech Impact](https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf)).

**Y: 1.25**
- The standard terms are the clearest positive lock-in evidence in the area ([NPact terms](https://npact.com/software-as-a-service-license-and-services-standard-terms/)):
  - no express export obligation;
  - an August 2025 ban on third-party "passthrough" access and third-party-initiated grants;
  - data deleted 10 business days after hosting ends;
  - a 3-year term.
- **Y1 = 1 and Y5 = 1.**

**Overlay:** none.

**What would move it:** product delivery evidence for Foundation Cloud, and a current customer count.

### Blackbaud Financial Edge NXT (foundations): insufficient evidence (Y coverage 0.40)
- **X5 = 4.** Audited 10-K ([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000006/blkb-20251231.htm)).
- **X3 = 1 and X6 = 1.** Positive deficiency evidence:
  - an FTC order and an SEC penalty following the 2020 ransomware attack ([FTC](https://www.ftc.gov/node/85395));
  - community-foundation donor breach notices ([Paso del Norte](https://pdnfoundation.org/news/notice-of-blackbaud-inc-security-incident)).
- **Y1 = 3.** Public SKY API with General Ledger write access ([connector](https://learn.microsoft.com/en-us/connectors/blackbaudfenxtgenera)).
- **Y3 = U, deliberately.** The Development Agent is a Raiser's Edge NXT product and was not transferred to FE NXT.
- **X1 = U.** FE NXT is a general ledger, not a DAF subledger. No count of DAF sponsors running on it exists.

**Overlay:** none for FE NXT.

**What would move it:** evidence of community foundations running their DAF book on FE NXT. Without it, this provider arguably sits outside A1's scope ("pure CRMs with no DAF ledger" are excluded, and FE NXT is borderline).

### NPT GivingPoint (added; sponsor-built): insufficient evidence
- **Why added.** NPT is the second-largest sponsor ($55.9bn, [990](https://projects.propublica.org/nonprofits/organizations/237825575)) and presents GivingPoint as its own platform. Omitting it would bias the area toward vendors.
- **X4 = 3.** J.P. Morgan and Wells Fargo programs ([JPM](https://www.jpmorgan.com/content/dam/jpm/securities/documents/DAFExecutiveSummary.pdf)).
- **Y2 = 2.** PayPal Grant Payments ([NPT](https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf)).
- **Unknown.** The developer behind GivingPoint, and any Ren link (edge E092 is "unknown").

### NCF and SVCF (sponsor-built on Salesforce Experience Cloud): insufficient evidence
- **Hosting.** Both portals are confirmed on Salesforce hosting by DNS (breadth document S08).
- **NCF.** X1 = 2 ($5.68bn), with an earlier Skuid/Salesforce portal case study ([Skuid](https://www.skuid.com/blog/donor-portal-yields-1-2-billion-grants-skuid-customer)).
- **SVCF.** X1 = 3 ($9.58bn, [990](https://projects.propublica.org/nonprofits/organizations/205205488/202543149349305759/IRS990ScheduleI)).
- **Not counted as platform signals.** The governance and controversy records (CMP-225, CMP-235/236) are about the sponsors, not their platforms, so X6 stays U.
- **Unknown.** The builder, and the fund-accounting ledger behind the portal.

**Overlay:** none.

### Givinga: insufficient evidence (X coverage 0.35)
- **X1 = 2.** Givinga Foundation reports 1.42M accounts but only $12.3M in assets ([990 Sch D](https://projects.propublica.org/nonprofits/organizations/474172718/202503179349301975/IRS990ScheduleD)). This is a workplace ledger, and the paper-filed count is unvalidated.
- **Y.** Everything on the forward axis is a vendor claim: payments, "automated charity vetting", and the December 2025 corporate suite.

**Overlay:** none.

**What would move it:** named white-label partners, SOC evidence, API documentation.

## 3. AI-governance overlay summary

| Provider | Evidenced AI | Respects "AI may add a flag, never clear one"? | Flag |
|---|---|---|---|
| TIFIN Give | Louise executes donor requests (announced; V2A-10) | Undocumented. Execution vs. GiveClear approval boundary not public | RED-candidate |
| Foundant | Fia beta (agents, policy engine, bias screening) | Claimed controls, not documented. Grantmaker-side, not DAF approval | AMBER |
| Give Interactive | "AI tools" / "intelligent" (unverified marketing) | Unknown | AMBER-unverified |
| Fidelity Charitable | Navigation-only virtual assistant with disclaimers | Yes. No decision authority | GREEN |
| Ren | None; deterministic instant approval under RCF policy | n/a (rules, not AI); audit logs not public | GREEN/none |
| Foundation Source | AI intent only (AVD34) | n/a | WATCH |
| Blackbaud | Development Agent (RE NXT, human supervision), not FE NXT | n/a for FE NXT | none |
| Others | None found | n/a | none |

## 4. Key judgment calls

1. **Ren's market-share claim was excluded from X1** (disputed, V2B-04). Its X1 rests on portal footers and DAFRC assets (about 9%).
2. **Ren's X3 is 1, not 0.** The "contradiction" is one AEF boilerplate, and Ren's own announcements consistently say Type 1.
3. **Give Interactive's case-study SOC evidence is treated as `secondary`, not `vendor_claim`.** A third party published it and it states scope. A blind scorer may cap it at 2, which would lower X by about 0.25.
4. **TIFIN's Y3 is 1.** Tax Intelligence is evidenced automation (rubric 2), but Louise is AI that executes with no stated controls (rubric 0). Split the difference.
5. **NPact Y1/Y5 = 1 rests on positive evidence of restrictive terms**, not on absence of evidence. 0 was not used because customer data ownership and paid migration exist.
6. **Blackbaud's RE NXT AI was not transferred to FE NXT.** This drops Blackbaud to insufficient evidence on Y.
7. **NPT GivingPoint was added**, and sponsor-built platforms are scored on their own book. NCF and SVCF are split into separate rows rather than pooled.
8. **Foundant scale is capped at 2** (vendor claim), probably understating it.

## 5. Biggest unknowns across A1

- **Platform identity at the largest sponsors.** FMR's stack, NPT GivingPoint's developer, and Vanguard's Give Interactive go-live. These three facts dominate any market-share reading of A1.
- **Data rights in signed contracts.** Public templates (Ren, NPact) and terms (TIFIN) exist. No signed sponsor contract has been seen.
- **SOC scope for every vendor.** Only Give Interactive states a scope.
- **Customer mapping of the roughly 800 community foundations** across Foundant, NPact, iPhi, akoyaGO and Blackbaud.
- **Complaint signal for the vendors.** The complaint corpus is sponsor-labelled, so vendor-level X6 is mostly U.

Follow-up questions are in [`queue-proposals-quadrant-A1.csv`](../../data/mission-2026-11-14/queue-proposals-quadrant-A1.csv).
