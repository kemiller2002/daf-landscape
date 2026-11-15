# All-in DAF donor cost at three balances (P-ANL-05); DAFpay access to Vanguard and NCF (P-TRM-01); AEF export (P-TRM-02); TIFIN Louise grant actions (P-CON-03)

**Date:** 2026-11-14 · **Queue items:** P-ANL-05, P-TRM-01, P-TRM-02, P-CON-03 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs:**
- [`scripts/mission_all_in_cost.py`](../../scripts/mission_all_in_cost.py): stdlib, functional. Every input is embedded with its source URL, date and evidence status.
- [`data/mission-2026-11-14/all-in-cost-comparison-2026.csv`](../../data/mission-2026-11-14/all-in-cost-comparison-2026.csv): 51 rows (17 sponsor programs × $25k / $250k / $2.5m).
- [`data/mission-2026-11-14/queue-proposals-cost-access.csv`](../../data/mission-2026-11-14/queue-proposals-cost-access.csv): P-ACC-01 to P-ACC-04.

**Method and rules.**
- I used public pages and PDFs only. I logged in nowhere, submitted no forms, created no accounts and contacted no one.
- One PDF (MS GIFT Donor Circular) uses an image-encoded font, so I read it by OCR (`tesseract`) of the rendered pages.
- Recency: fee inputs are 2024–2026 documents or undated live pages. GS PF's only circular (2008) is not used.
- Labels: **[F]** first-party document; **[R]** search-index capture of a page I could not open (403/404/JS-only); **[3P]** third-party listing; **[I]** my inference; **[A]** modelling assumption.

**Read first and built on:** `queue-sponsor-terms-data-clauses.md` (with wave-9 corrections), `queue-agentic-products-dafpay-fees.md` (with wave-8 corrections), `research/daf-economics-and-distribution-2026-11-11.md` §C, `sponsor-fee-schedules.csv`, `daf-admin-fee-scenarios-2026.csv`, `bank-program-terms-2026.csv`.

---

## 0. Headline answers

| Item | Answer | Confidence |
|---|---|---|
| **P-ANL-05: all-in cost** | **The headline "~0.6%" is the admin fee alone. With the sponsor's typical pool, self-directed all-in cost at $250k runs from 0.26% (Daffy) and 0.62% (Vanguard) to 1.15% (Fidelity), 1.25% (DAFgiving360), 1.45% (NCF) and 2.13% (San Francisco Foundation).**<br>- **Pool choice matters as much as sponsor choice.** At Fidelity, the 60% equity pool costs 0.55% against 0.015% for the total-market index pool. That gap alone is larger than the admin-fee gap between most national sponsors.<br>- **The adviser layer dominates adviser-led programs.** Published caps are 1.00% at MS GIFT, DAFgiving360 and TIFIN Give/GiveClear. Edward Jones documents a 0.70% program fee paid to the adviser. With the adviser layer, all-in cost reaches 1.3–2.0% before fund expenses, so admin-fee comparisons understate the spread by 2–3x.<br>- **Minimum fees bind at $25k** at RCF ($250 → 1.00%), Edward Jones ($200 → 0.80%), MS GIFT ($100 on the 0.27% layer) and NCF ($360 → 1.44%). They do not bind at Fidelity, NPT, Charityvest or Vanguard. Vanguard has a $250 maintenance fee that applies only below $25k.<br>- **Scale economies:** at $2.5m, typical all-in cost falls to 0.27% (Vanguard), 0.85% (Fidelity) and 0.95% (DAFgiving360). SFF stays at 2.13%, because its 1.00% admin tier runs to $3m and its long-term pool costs 1.13%.<br>- **Flat and transaction pricing wins at scale.** Daffy costs 0.18% at $2.5m and Endaoment about 0.29% admin-equivalent. These figures depend on a stated flow assumption. | High on admin fees for 13 programs; medium on pool choice; low for AEF, Edward Jones and GS PF |
| **P-TRM-01: DAFpay access to Vanguard and NCF** | **No public source shows a carve-out, API or partnership for either sponsor. Chariot's own help center says its default "compatible flow" passes donor credentials through to the sponsor, and that this "does not require technical collaboration with DAF providers".**<br>- **Tokenised alternatives are named for others only.** Chariot names DAFgiving360 (emailed code or passkey, 2026-05-31) and Foundant-hosted community foundations (2026-09) as using its credential-free access method. The OAuth and Donor Accounts APIs list no live sponsors; Donor Accounts is in a beta with unnamed "design partners".<br>- **Third parties still list both sponsors.** Platforms (CrowdChange, Donorbox, SCO) list Vanguard and NCF as supported, and CrowdChange tells donors to "connect with their login credentials". Chariot's help article says NCF is "proudly supported by Chariot".<br>- **[I]** The public record is consistent with credential pass-through continuing, against both sponsors' written terms, or with a silent fallback to the "manual flow". Which applies cannot be established without Chariot's authenticated provider list (P-ACC-01). | Medium (absence of evidence; vendor docs are first-party) |
| **P-TRM-02: AEF DonorCentral export** | **The "Export" text is legacy.**<br>- **Where it sits:** the instruction is on AEF's "Technology Upgrade" support site. It describes Blackbaud DonorCentral (aef.donorcentral.com).<br>- **The cut-over:** AEF moved to Ren's DFX platform on **2026-04-06**, and Ren announced that all AEF operations were on its platform on 2026-04-08. AEF's upgrade FAQ says donors will not go back to DonorCentral and that the new platform shows only two years of granting history.<br>- **What the new platform offers:** no AEF or Ren page documents a donor export on it.<br>- **Residual uncertainty:** AEF's homepage still links DonorCentral under "Donors", and the host still serves a login shell, so legacy read-only access may persist (P-ACC-04).<br>- **Repo impact:** row 7 of `donor-data-export-top10-2026.csv` stays "no export on the current platform", with a note. | Medium-high |
| **P-CON-03: what Louise does on "make a grant"** | **Not publicly documented beyond marketing.**<br>- **What the release claims:** the 2025-10-27 release says Louise is "designed to drive actionability and execute real donor requests". Its example is "Set up a monthly recurring $100 grant to the Wounded Warrior Project".<br>- **What no public document describes:** a draft-versus-submit step, a confirmation screen for AI-initiated grants, limits or logging. No help article or video covering Louise was found.<br>- **The manual grant flow:** TIFIN Give's help article (updated 2026-03-05) has a "Review and Confirm Your Grant" step with a guidelines certification. Grants are then "subject to the approval of GiveClear" and reviewed within 48 hours.<br>- **The terms:** they describe an "AI Assistant" whose insights are "for informational and educational purposes only" and undergo "a compliance check". They say nothing about AI-initiated transactions.<br>- **[I]** Any Louise-created grant still passes GiveClear approval. Whether the donor confirms each AI-drafted grant is unknown. | Medium (absence of evidence) |

---

## 1. P-ANL-05: all-in annual donor cost

### 1.1 Definitions and assumptions

**Cost components:**
- **Admin:** the sponsor's published admin or program schedule, applied as the sponsor states it: marginal tiers, first-dollar band (BofA) or flat membership (Daffy). It includes:
  - published minimum annual fees;
  - every mandatory admin layer. MS GIFT has three: the third-party administrator at 0.27% (min $100), the MSSB administrative fee at 0.07%, and the charitable admin fee at its stated **maximum** of 0.03% [F].
- **Investment, "low":** the cheapest published pool or portfolio.
- **Investment, "typical":** the default, most popular or balanced pool. The pool chosen is named in each row **[A]**.
- **Adviser:**
  - **published cap:** MS GIFT, DAFgiving360 and TIFIN Give/GiveClear, all 1.00%;
  - **program fee:** Edward Jones, 0.70% **[R]**;
  - **illustrative 1.00% [A]:** used where an adviser option exists but no cap is published (Fidelity CIAP, NPT, RCF advisor-managed, AEF, NCF SMA, Endaoment AMPs, SFF);
  - **left blank:** sponsors with no adviser-fee program found (Vanguard, RCF donor-directed, BofA, Daffy, Charityvest).
- **"With adviser" totals** exclude fund expenses wherever they are unpublished (`all_in_with_adviser_excl_fund_exp_*`). A second column adds the typical pool where one exists.

**Other assumptions:**
- **Flow assumption [A]:** used only for Daffy and Endaoment. Annual contributions and annual grants each equal 20% of the balance.
- **Constant balance [A]:** fees are computed on a constant balance with no market drift. Excluded: grant-processing exceptions (international, wire), illiquid-gift fees, trading costs (NPT discloses up to 4¢/share) and incentive fees (SFF).

### 1.2 Results (annual cost as % of balance; full dollar values in the CSV)

| Sponsor / program | Admin $25k | Admin $250k | Admin $2.5m | Typical all-in $25k | $250k | $2.5m | Typical pool used | Adviser layer | With adviser (excl. funds) $250k |
|---|---|---|---|---|---|---|---|---|---|
| Fidelity Charitable | 0.60 | 0.60 | 0.30 | 1.15 | 1.15 | 0.85 | AA 60% Equity 0.55% ([F](https://www.fidelitycharitable.org/giving-account/what-it-costs.html)) | CIAP "customary advisor fee", no cap ([F](https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/giving-account-guide-financial-advisors.pdf)) → 1.00% [A] | 1.60 |
| Vanguard Charitable (Premier) | 0.60 | 0.60 | 0.25 | 0.62 | 0.62 | 0.27 | Moderate Growth 0.02% ([F](https://www.vanguardcharitable.org/investments)) | none found | — |
| DAFgiving360 core | 0.60 | 0.60 | 0.30 | 1.25 | 1.25 | 0.95 | Balanced Pool ~0.65% [R] | cap 1% ([R](https://www.dafgiving360.org/investment-options-advisor)); $100k min | 1.60 |
| NPT | 0.85 | 0.85 | 0.55 | 1.46 | 1.46 | 1.16 | Active Moderate 0.51% + 0.10% advisory ([F](https://www.nptrust.org/investment-descriptions-and-performance-npt/)) | unpublished → 1.00% [A] | 1.85 |
| RCF advisor-managed | **1.00** (min) | 0.65 | 0.35 | n/p | n/p | n/p | not published | unpublished → 1.00% [A] | 1.65 |
| RCF donor-directed | **1.00** (min) | 0.60 | 0.30 | n/p | n/p | n/p | not published | — | — |
| Edward Jones CGF (Ren) | **0.80** (min) | 0.60 | 0.30 | n/p | n/p | n/p | not published | 0.70% program fee [R] | 1.30 |
| AEF [3P] | 0.70 | 0.70 | 0.36 | n/p | n/p | n/p | adviser portfolio | unpublished → 1.00% [A] | 1.70 |
| BofA CGF | 0.90 | 0.75 | 0.35 | 1.11 | 0.96 | 0.56 | Passive, high end 0.21% incl. 0.12% mgmt (repo) | none separate | — |
| MS GIFT | **0.50** (min) | 0.37 | 0.36 | n/p | n/p | n/p | not published | max 1.00% ([F](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf)) | 1.37 |
| GS PF | n/p | n/p | n/p | n/p | n/p | n/p | — | — | — |
| NCF | **1.44** (min) | 0.90 | 0.62 | 1.99 | 1.45 | 1.17 | Balanced Growth 0.55% ([F](https://site.ncfgiving.com//wp-content/uploads/2026/08/Grow-your-giving-for-greater-impact.pdf)) | SMA from $300k → 1.00% [A] | (not eligible) |
| Daffy [A flow] | 0.14 | 0.10 | 0.02 | 0.30 | 0.26 | 0.18 | ETF portfolios 0.16% [R] | none | — |
| Charityvest | 0.60 | 0.60 | 0.30 | 0.71 | 0.71 | 0.41 | built-in fees 0.11% ([F](https://pcadafguide.foundationsource.com/how-client-fees-work)) | none found | — |
| Endaoment [A flow] | 0.30 | 0.30 | 0.29 | 0.90 | 0.90 | 0.89 | traditional portfolio 0.60% [R] | AMP fee "separately disclosed" → 1.00% [A] | 1.30 |
| TIFIN Give / GiveClear | 0.60 | 0.60 | 0.36 | n/p | n/p | n/p | not published | cap 1% ([F](https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines)) | 1.60 |
| San Francisco Foundation | 1.00 | 1.00 | 1.00 | 2.13 | 2.13 | 2.13 | Long-Term Pool 1.02% + 0.11% admin ([F](https://sff.org/wp-content/uploads/2026/05/2026-Advisor-Guide-1.pdf)) | SFM from $1m → 1.00% [A] | (not eligible) |

n/p = not published. **Bold** = a minimum fee binds.

**Low-cost-pool all-in at $250k:**

| Sponsor | All-in |
|---|---|
| Daffy | 0.23% |
| Vanguard | 0.61% |
| Fidelity | 0.615% |
| DAFgiving360 | 0.63% |
| Charityvest | 0.65% |
| Endaoment | 0.83% |
| BofA | 0.92% |
| NPT | 1.02% |
| SFF | 1.24% |
| NCF | 1.40% |

### 1.3 Findings

1. **The admin-fee convention misleads at both ends [I].**
   - At $250k, admin fees cluster tightly (0.60–0.90%, plus SFF at 1.00%).
   - Typical all-in cost spans 0.26–2.13%, about an 8x range.
   - Teaching that cites "~0.6%" (T7) is accurate only for Vanguard, or for index-pool users elsewhere.
2. **Pool default is a hidden price lever.**
   - Fidelity's and DAFgiving360's balanced pools add 0.55–0.65%. Both sponsors also offer index pools at 0.015–0.03%.
   - Vanguard's Portfolio Solutions cost 0.01–0.02%. This is the main reason it is cheapest among the incumbents at every balance.
   - The CSV records both "low" and "typical" so the choice is explicit.
3. **Minimum fees create a small-account penalty.**
   - **Where they bind** (breakeven balance below which the minimum applies): NCF $40,000, RCF $38,462, MS GIFT $37,037 (0.27% layer), Edward Jones $33,333 **[R]**, NPT $24,000, Fidelity and Charityvest $16,667.
   - **Vanguard** has no minimum fee, but a $250 maintenance fee "may" apply below $25,000. At $20k that would be 1.25%.
4. **The adviser layer is the largest single item for adviser-led sponsors.**
   - The three published caps are all 1.00%, and MS GIFT says part of the advisory fee "is shared with the applicable Financial Advisor" [F].
   - [I] The repo's TIFIN warning (do not add entity-level 30+10 bps to sponsor fees) still holds. The donor-facing cap is the relevant number.
5. **Bank and wealth-captive programs are cheaper on admin and dearer all-in.**
   - MS GIFT's admin stack (0.37% at $250k) is the lowest among the advisor-led programs.
   - With the 1.00% advisory cap, it reaches 1.37% before fund expenses.
   - BofA's first-dollar banding means a $100,001 account pays 0.75% on every dollar.
6. **Community foundation premium.**
   - SFF's 1.00% admin plus a 1.13% long-term pool is the most expensive program measured.
   - [I] SFF's pool holds private equity, venture capital and hedge funds, so its costs pay for a different asset mix. It is not a like-for-like price.
7. **Transaction pricing (Endaoment) and flat pricing (Daffy) favour large balances.**
   - Endaoment's 0.29–0.30% admin-equivalent rests on the 20%/20% flow assumption. A fund that grants 50% of its balance a year would pay about 0.60%.
   - Daffy's cap of $480/yr makes it the cheapest at $2.5m, but Daffy offers no adviser channel.

### 1.4 Input caveats (all also in the CSV `assumptions` / `notes` columns)

- **DAFgiving360:**
  - All dafgiving360.org pages return 403.
  - The tiers come from a 2024 DAFgiving360 deck: 0.60/0.30/0.20/0.15 with breakpoints at $500k, $1m, $2.5m and $5m. This settles the repo's "breakpoints not verified" flag (sponsor-fee-schedules.csv row "0.15%").
  - The deck also says "$0+ – no annual fee or minimum".
  - Underlying pool funds changed in September 2026, so the pool expense figures (SWTSX 0.03%; JBALX ~0.65% [R]) need re-checking (P-ACC-02).
- **NPT:** new to the repo.
  - The CAF schedule is 0.85/0.70/0.60/0.45/0.25/0.15/0.10%, with a $17 monthly minimum. Source: the NPT guide PDF created 2026-10-15 [F].
  - This replaces the repo's "schedule NOT published" entry.
- **MS GIFT:** new to the repo. Schedule C of the August 2024 Donor Circular publishes the full fee stack. This corrects the repo's "admin fee schedule not found publicly".
- **NCF:** new to the repo. The full ministry-support schedule is 0.90/0.70/0.50/0.35/0.30/0.25/0.20/0.15/0.10/0.05% [F], replacing the "detailed schedule not retrieved" entry.
- **AEF:**
  - AEF publishes no schedule; the tiers are a third-party listing (©2024).
  - The 2012 Chronicle figure (0.70% start) agrees on the first tier.
- **Edward Jones:**
  - The documented fee is 60 bps "and tiers down", with a $200 minimum and a 0.70% program fee. All three come from a Ren help page that now returns 404 [R].
  - Breakpoints are **assumed** equal to RCF donor-directed.
- **Charityvest:** the source page gives both "starting at 45bps" and a 60 bps tier table. The table is used.
- **TIFIN Give / GiveClear:**
  - TIFIN Give guidelines (2025-08-12): 0.60% to $1m, 0.20% above.
  - GiveClear's white-label "Customer DAF" guidelines (V08.25.2025): 0.60% / 0.20% / 0.10% above $2.5m.
  - AssetMark Charitable (repo): 0.60% / 0.20%.
- **BofA:** not re-read. Uses the repo row (CGF fee PDF, estimates as of 2024-02-16).
- **GS PF:** no 2021+ schedule; row left blank.

---

## 2. P-TRM-01: how DAFpay reaches Vanguard Charitable and NCF donors

### 2.1 What the sponsors' terms say (repo, verified 2026-11-14)

- **Vanguard User Agreement (May 2025):** "You are prohibited from allowing another person or entity, including charities or grant recommendation processing services, to use your user name(s) and password(s)". It also bars any "electronic agent, bot, or other automated means" ([F](https://www.vanguardcharitable.org/company-policies/user-agreement)).
- **NCF Program Agreement (effective 2025-09-17):** bars using "any third-party service or application that requires you to provide your NCF credentials". It also says "NCF does not authorize any third-party service to access the Secure Site" ([F](https://secure.ncfgiving.com/agreement)).

### 2.2 What Chariot documents about access methods

| Method | What Chariot says | Named sponsors | Source |
|---|---|---|---|
| **Compatible flow** (default) | "Hundreds of DAFs are fully compatible with DAFpay, representing +85% of the $326B DAF market." Authentication "may vary by provider": "Sign in directly within the DAFpay modal", "Be briefly redirected to their DAF provider's site", or "Login … using a secure SMS link or QR code" | none | [Chariot help, Compatible Providers](https://help.givechariot.com/llms-full.txt) [F] |
| **Credential pass-through** | "When a donor enters their account credentials in the modal, that information is fully encrypted and is not stored". "A donor's login credentials are passed through to each DAF provider". "Chariot offers a service to DAF account holders that does not require technical collaboration with DAF providers" | none; framed as the general service, with "formal agreements with many DAF providers" for deeper integration (unnamed) | [Chariot help, DAFpay Security](https://help.givechariot.com/llms-full.txt) [F]; [DAFpay Donor Terms, eff. 2025-09-24](https://www.dafpay.com/donor-terms-of-use) ("permission to use the DAF Provider credentials"; "triggering the transmission of any two factor authentication codes") [F] |
| **New tokenised access** | "a new access method … that alleviates the need for donors to remember their password and enter their account credentials via DAFpay" | **DAFgiving360** (emailed code, optional passkey, call from DAFgiving360 on first use; 2026-05-31); **Foundant CommunitySuite** community foundations ("secure direct API integration"; 2026-09-18) | [Chariot help FAQ](https://help.givechariot.com/llms-full.txt); [DAFgiving360 note](https://givechariot.com/resources/insights/new-access-method-for-dafgiving360-in-dafpay.md); [Foundant note](https://www.givechariot.com/resources/insights/-dafpay-foundant-how-community-foundations-using-communitysuite-can-enable-dafpay-) [V] |
| **OAuth integration** (sponsor's own login page, scoped tokens) | "You never share donor credentials with Chariot — only scoped, revocable tokens." "Only one integration is supported per DAF." | none | [docs v2026-04-01 OAuth overview](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/overview.md); [checklist](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/integration-checklist.md) [F] |
| **Donor Accounts** (one-time code; sponsor decisions Grant Requests by API) | "in beta … a pilot program with a handful of design partners" | none named | [changelog 2026-05-08](https://docs.givechariot.com/changelog/2026/5/8) [F] |
| **Manual / unintegrated flow** | The donor enters intent, "is directed to their DAF provider's site to complete the gift"; Chariot "cannot confirm whether it was completed" | none | [Compatible Providers](https://help.givechariot.com/llms-full.txt); [Unintegrated Grants API](https://docs.givechariot.com/v2026-04-01/api/unintegrated-grants/list.md) [F] |

### 2.3 Vanguard and NCF specifically

- **Chariot:**
  - No Chariot page names Vanguard as a supported or integrated provider.
  - Chariot's help center mentions Vanguard only as a grantmaker whose gifts "will still be delivered the same way as before" (that is, not via Chariot Disbursements).
  - A Chariot help article (now 404; [R] snippet) says JCF and NCF "are both proudly supported by Chariot".
- **Third-party platforms:**
  - CrowdChange: "Major DAF providers are supported, including Fidelity, DAFGiving360, Vanguard, National Christian Foundation". The donor must "connect with their login credentials" ([CrowdChange](https://chadmin.crowdchange.help/ct/donor-advised-funds-dafpay-by-chariot-integration), image dated 2024).
  - Donorbox and SCO make similar claims ([R]).
- **No announcement found:** I found no Vanguard–Chariot or NCF–Chariot partnership announcement in 2021–2026 Chariot news. The partnerships Chariot did announce are Thrivent Charitable (2025-10), TIFIN (2025-12-02) and the six Disbursements partners (2025-04-30).
- **The provider list is not public:** Chariot's `GET /v1/donor_advised_funds?supportedOnly=true` would answer the question, but it requires an OAuth bearer token ([docs](https://docs.givechariot.com/v2026-04-01/api/donor-advised-funds/list.md)).

**Conclusion [I]:** three readings are possible.
1. DAFpay still passes Vanguard and NCF donor credentials through its modal. That would breach both sponsors' written terms, with the donor bearing the loss: Vanguard treats credentialed instructions as authorised by the donor, and NCF holds the donor responsible "whether or not authorized".
2. DAFpay has moved those providers to the manual flow.
3. A private agreement exists.

No public evidence distinguishes these. The DAFgiving360 switch shows that Chariot moves a sponsor to tokenised access when the sponsor cooperates, and announces it. No such announcement exists for Vanguard or NCF. P-ACC-01 proposes the check.

---

## 3. P-TRM-02: AEF DonorCentral export

| Evidence | What it shows | Source |
|---|---|---|
| Platform-resources page (live) | Six-step "Generate a list of grants paid within a specific date range" in DonorCentral, ending "Click on the Export button". Links to `aef.donorcentral.com` | [F](https://engage.aefonline.org/platform-resources/) |
| Same site's header | "AEF TECHNOLOGY UPGRADE" (wave-9 correction 5) | [F](https://engage.aefonline.org/platform-resources/) |
| Upgrade timeline | Blackout 2026-03-23 to 04-06; "April 6 – New Platforms Go Live" | [F](https://engage.aefonline.org/?p=13612) |
| Upgrade FAQ | "Will I Go Back to Using the Previous Platform (DonorCentral) after this transition?" "No." "Only granting history from the past two (2) years will be reviewable on this platform." | [F](https://engage.aefonline.org/?p=12588) |
| Ren release, 2026-04-08 | Ren "now fully power[s] all of American Endowment Foundation's customers"; no mention of reporting or exports | [F](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/) |
| New portal | `portal.aefonline.org`: "DFX powered by Ren"; no export or history text | [F](https://portal.aefonline.org/) |
| Legacy host | `aef.donorcentral.com` returns HTTP 200 with a Blackbaud SKY UX single-page app titled "Donorcentral"; AEF's homepage still lists it under "Donors" | server response 2026-11-14; [AEF home](https://www.aefonline.org/) |

**Answer:**
- The export instruction describes the legacy Blackbaud DonorCentral, not the current Ren platform. (DonorCentral is a Blackbaud product, not NPact.)
- No donor-side export is documented for the platform AEF donors have used since 2026-04-06.
- **[I]** The DonorCentral login may still give read-only access to pre-migration history, which would explain why the help text is still up. This is unverified without a login (P-ACC-04).

**Correction for `queue-sponsor-terms-data-clauses.md` §4:** "If the export is still live, AEF becomes the only top-10 sponsor with a documented donor-side export" should read:

> "The export belongs to legacy DonorCentral; AEF's current Ren DFX platform (live 2026-04-06) documents no export. Row 7 is unchanged."

---

## 4. P-CON-03: what TIFIN Give's Louise does when asked to make a grant

| Source | What it says | Date |
|---|---|---|
| [PR Newswire launch](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html) | Louise is "designed to drive actionability and execute real donor requests within the charitable experience". Example requests: "Set up a monthly recurring $100 grant to the Wounded Warrior Project", "Contribute 100 shares of NVDA stock to my DAF", "Add one of my children to my DAF". "Louise is now available to donors using TIFIN Give." Nothing on drafting, confirmation, approval, limits or logging | 2025-10-27 [V] |
| [TIFIN Give Terms of Use §19](https://intercom.help/give-ria/en/articles/10092486-terms-of-use) | "The Services may include an AI assistant". Its insights are "for informational and educational purposes only". "Before any insights are displayed to you, they undergo a compliance check". Silent on AI-initiated grants | 2025-02-19 [F] |
| [Make a grant (help)](https://intercom.help/give-ria/en/articles/9450799-make-a-grant-to-a-charity) | Manual flow: amount and reason, then "Complete", then a "Review and Confirm Your Grant" tab with a guidelines-compliance checkbox and an anonymity choice. No mention of Louise | updated 2026-03-05 [F] |
| [Program guidelines](https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines) | Grants "are reviewed for approval within 48 hours"; GiveClear is the sponsor. No AI clause | updated 2025-08-12 [F] |
| [New interface article](https://intercom.help/give-ria/en/articles/11724183-new-user-interface-details) | No mention of Louise | 2025-07-21 [F] |
| tifin.com product, news and Giving Tuesday pages; give.tifin.com/demo | HTTP 404 on 2026-11-14; no video found | — |

**Name collision.** "Louise by TIFIN" was also the brand of the DAF platform built from TIFIN's 2022 Amicus.io acquisition. The "$38bn in assets" figure in search results belongs to that 2022 platform, not to the 2025 AI assistant.

**Answer:**
- **Claimed:** execution of grant requests.
- **Not documented anywhere public:**
  - whether Louise creates a submitted grant, a draft, or pre-fills the manual "Review and Confirm" screen;
  - per-action limits;
  - logging or audit trail;
  - confirmation for recurring grants.
- **[I]** Every grant still requires GiveClear approval, so Louise cannot move money without the sponsor's decision. The donor-side control point is undocumented. The repo's AP02 classification (announced) and its F06/F16 risk ratings stand.

---

## 5. Implications for repo conclusions

1. **`sponsor-fee-schedules.csv`:**
   - Add NPT's CAF schedule and $17 monthly minimum, from the NPT guide PDF created 2026-10-15.
   - Add MS GIFT's Schedule C stack and 1.00% advisory maximum.
   - Add NCF's full schedule.
   - Add TIFIN Give/GiveClear tiers and the 1% sub-advisory cap.
   - Add the SFF schedule.
   - Fix DAFgiving360's tier-4 breakpoints ($2.5m–$5m).
   - Mark the AEF row as third-party (©2024), not just "2012 historical".
2. **Analyst-education gap (T7):** replace "~0.6%" with:

   > "admin 0.6% is typical; all-in self-directed 0.3–1.5% depending on pool; adviser-led 1.3–2.0% before fund expenses."

3. **Agentic-control gap matrix:** keep "sponsor terms prohibit third-party credential use" set to yes for Vanguard and NCF. Add a column "documented DAFpay access method": DAFgiving360 = token or passkey; Foundant CFs = API; Vanguard and NCF = not public (credential pass-through by default per Chariot's docs).
4. **`donor-data-export-top10-2026.csv` row 7 (AEF):** add a note that the Export instruction is legacy DonorCentral. No change in score.

## 6. Limitations

- **Blocked pages:**
  - DAFgiving360 (403): DAFgiving360 pool figures are search-index captures or 2024 documents.
  - Daffy portfolio pages (JS-only): Daffy pool figures are search-index captures.
  - Endaoment portfolio expense: search-index capture.
- **Unpublished fund expenses:** pool or fund expenses are not published for MS GIFT, AEF, RCF, Edward Jones or TIFIN Give. Their "with adviser" totals exclude fund costs.
- **Illustrative adviser fee:** the 1.00% figure is a modelling choice, not an observed fee.
- **Flow assumption:** drives the Daffy and Endaoment results; change `CONTRIB_SHARE` and `GRANT_SHARE` in the script to test others.
- **Fee exclusions:** costs are annual run-rate on a constant balance. Grant-processing exceptions, illiquid-asset fees, trading costs and incentive fees are excluded.
- **Not found ≠ absent:** "not found" means searched and not found.

## 7. Source register

| ID | Source | URL | Date | Label |
|---|---|---|---|---|
| C01 | Fidelity Charitable: What it costs | https://www.fidelitycharitable.org/giving-account/what-it-costs.html | live; ©1998-2026 | F |
| C02 | Fidelity advisor guide (CIAP) | https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/giving-account-guide-financial-advisors.pdf | undated | F |
| C03 | Fidelity CIAP investment guidelines | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-investment-guidelines.pdf | file 2025-07-29 | F |
| C04 | Vanguard Charitable fees | https://www.vanguardcharitable.org/fees-and-expenses | live | F |
| C05 | Vanguard Charitable investments | https://www.vanguardcharitable.org/investments | ERs as of 2026-09-30 | F |
| C06 | DAFgiving360 deck (FPA of MI) | https://www.financialplanningassociation.org/sites/default/files/2024-09/FPA%20of%20MI_DAFGiving360_deck_092724_ver3.pdf | 2024-09 | F |
| C07 | DAFgiving360 fees; advisor options | https://www.dafgiving360.org/features/fees-and-minimums ; https://www.dafgiving360.org/investment-options-advisor | 403 | R |
| C08 | Schwab SWTSX | https://www.schwabassetmanagement.com/products/swtsx | 0.030% | R |
| C09 | NPT donor guide | https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf | created 2026-10-15 | F |
| C10 | NPT investment descriptions | https://www.nptrust.org/investment-descriptions-and-performance-npt/ | IDAP 0926; perf. to 2026-06-30 | F |
| C11 | NPT FAQ | https://www.nptrust.org/?p=206 | ©2026 | F |
| C12 | RCF advisor-managed; donor-directed | https://renaissancecharitable.org/advisor-managed-dafs/ ; https://renaissancecharitable.org/donor-directed-dafs/ | live | F |
| C13 | Edward Jones DAF opening instructions (Ren help) | https://intercom.help/rengiving/en/articles/11004460-ej-daf-opening-instructions | now 404 | R |
| C14 | AEF third-party fee listing | https://donoradvisedfunds.com/dafs/american-endowment-foundation-aef/ | ©2024 | 3P |
| C15 | AEF Maintain the Fund | https://advisorwelcome.aefonline.org/maintain-the-fund | live | F |
| C16 | BofA CGF fee schedule (repo) | https://www.bankofamerica.com/content/documents/philanthropic/cgf_fee_schedule.pdf | est. 2024-02-16 | F (repo) |
| C17 | MS GIFT Donor Circular, Schedule C | https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf | Aug 2024 | F (OCR) |
| C18 | NCF Giving Fund fees | https://www.ncfgiving.com/givingfund | ©2026 | F |
| C19 | NCF pools brochure | https://site.ncfgiving.com//wp-content/uploads/2026/08/Grow-your-giving-for-greater-impact.pdf | est. 2026-07-31 | F |
| C20 | NCF investments page | https://www.ncfgiving.com/investments | rates as of 2026-11-01 | F |
| C21 | Daffy membership fees | https://help.daffy.org/en/articles/6323771-what-are-daffy-s-membership-fees | 2026-08-06 | F |
| C22 | Daffy ETF expense range; investment fees | https://www.daffy.org/answers/what-is-the-range-of-the-expense-ratio-for-the-etfs-in-these-portfolios ; https://help.daffy.org/en/articles/12068158-does-daffy-charge-investment-fees | 2025 | R / F |
| C23 | Charityvest fees (Foundation Source guide) | https://pcadafguide.foundationsource.com/how-client-fees-work | live | F |
| C24 | Endaoment fee schedules (donor; advisor) | https://docs.endaoment.org/donors/resources/fee-schedule.md ; https://docs.endaoment.org/advisors/resources/fee-schedule.md | live | F |
| C25 | Endaoment VOO portfolio page | https://app.shadow.endaoment.org/portfolios/7b59269e-05d0-4a74-837c-44f1249da4da | capture | R |
| C26 | TIFIN Give program guidelines | https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines | 2025-08-12 | F |
| C27 | GiveClear Customer DAF guidelines | https://irp.cdn-website.com/5c4108df/files/uploaded/DAF+Program+Guidelines-d1858d87.pdf | V08.25.2025 | F |
| C28 | San Francisco Foundation 2026 Advisor Guide | https://sff.org/wp-content/uploads/2026/05/2026-Advisor-Guide-1.pdf | 2026-05 | F |
| C29 | GS PF Program Circular (not used) | https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111 | 2008-08 | F (pre-2021) |
| D01 | Chariot help center full text (Compatible Providers; DAFpay Security; FAQ) | https://help.givechariot.com/llms-full.txt | read 2026-11-14 | F |
| D02 | Chariot docs index v2026-04-01 | https://docs.givechariot.com/v2026-04-01/llms.txt | v2026-04-01 | F |
| D03 | Chariot OAuth overview; checklist | https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/overview.md ; https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/integration-checklist.md | v2026-04-01 | F |
| D04 | Chariot changelog (Donor Accounts) | https://docs.givechariot.com/changelog/2026/5/8 | 2026-05-08 | F |
| D05 | Chariot List DAFs; Unintegrated Grants API | https://docs.givechariot.com/v2026-04-01/api/donor-advised-funds/list.md ; https://docs.givechariot.com/v2026-04-01/api/unintegrated-grants/list.md | v2026-04-01 | F |
| D06 | Chariot DAFgiving360 access note | https://givechariot.com/resources/insights/new-access-method-for-dafgiving360-in-dafpay.md | 2026-05-31 | V |
| D07 | Chariot Foundant note | https://www.givechariot.com/resources/insights/-dafpay-foundant-how-community-foundations-using-communitysuite-can-enable-dafpay- | 2026-09-18 | V |
| D08 | DAFpay Donor Terms | https://www.dafpay.com/donor-terms-of-use | eff. 2025-09-24 | F |
| D09 | CrowdChange DAFpay page | https://chadmin.crowdchange.help/ct/donor-advised-funds-dafpay-by-chariot-integration | c.2024 | 3P |
| D10 | Chariot help: types of DAF providers (NCF/JCF) | https://intercom.help/givechariot/en/articles/8742318-what-are-the-different-types-of-daf-providers | 404; snippet | R |
| D11 | Vanguard User Agreement; NCF Program Agreement (repo clauses) | https://www.vanguardcharitable.org/company-policies/user-agreement ; https://secure.ncfgiving.com/agreement | May 2025; 2025-09-17 | F |
| E01 | AEF platform resources | https://engage.aefonline.org/platform-resources/ | live | F |
| E02 | AEF upgrade FAQ; timeline | https://engage.aefonline.org/?p=12588 ; https://engage.aefonline.org/?p=13612 | 2026 | F |
| E03 | Ren release: AEF fully on Ren | https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/ | 2026-04-08 | F |
| E04 | AEF portal; AEF homepage; DonorCentral host | https://portal.aefonline.org/ ; https://www.aefonline.org/ ; https://aef.donorcentral.com/ | live 2026-11-14 | F |
| L01 | TIFIN Louise release | https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html | 2025-10-27 | V |
| L02 | TIFIN Give Terms of Use | https://intercom.help/give-ria/en/articles/10092486-terms-of-use | 2025-02-19 | F |
| L03 | TIFIN Give: make a grant; new UI | https://intercom.help/give-ria/en/articles/9450799-make-a-grant-to-a-charity ; https://intercom.help/give-ria/en/articles/11724183-new-user-interface-details | 2026-03-05; 2025-07-21 | F |
| L04 | TIFIN Amicus.io acquisition (name history) | https://www.investmentnews.com/fintech/tifin-group-acquires-fintech-targeting-donor-advised-funds/218849 | 2022-03 | 3P |

## 8. Data dictionary: `all-in-cost-comparison-2026.csv` (one row per sponsor program × balance)

| Column | Meaning |
|---|---|
| sponsor, program | Sponsor and the program or account type modelled |
| balance_usd | Constant balance: 25,000 / 250,000 / 2,500,000 |
| admin_fee_usd, admin_fee_bps | Annual admin/program fee, including minimums, mandatory admin layers and (Daffy, Endaoment) flow-implied fees |
| min_annual_fee_usd | Published minimum annual fee (NPT $17×12; NCF $30×12; Daffy lowest paid tier) |
| min_fee_binding_at_balance | yes/no: whether the minimum exceeds the tiered fee at this balance |
| min_fee_breakeven_balance_usd | Balance below which the minimum binds (minimum ÷ first-tier rate; MS GIFT uses the 0.27% layer) |
| inv_low_bps / _option / _usd | Cheapest published pool or portfolio expense |
| inv_typical_bps / _option / _usd | Default, popular or balanced pool expense (choice named; an assumption) |
| all_in_low_usd/_bps; all_in_typical_usd/_bps | Admin + investment (blank if investment not published) |
| adviser_fee_bps | Adviser fee used |
| adviser_fee_basis | published_cap / program_fee / illustrative_assumption / not_offered_or_not_found / not_published |
| adviser_layer_standard | yes if the program is adviser-led by design |
| adviser_option_eligible_at_balance | yes/no/unknown versus the published adviser-option minimum |
| adviser_fee_usd | Adviser fee in dollars |
| all_in_with_adviser_excl_fund_exp_usd/_bps | Admin + adviser fee (fund expenses excluded) |
| all_in_with_adviser_typical_usd/_bps | Admin + adviser + typical pool (blank if pool not published) |
| flow_assumption_used | States the contributions/grants share where used |
| admin_/inv_/adviser_source_url, _date, _status | Source for each input: URL, stated date, and evidence status (primary, primary_pdf_ocr, search_index_capture, third_party, repo_prior) |
| retrieved | 2026-11-14 |
| confidence | high / medium / low for the row |
| assumptions, notes | Modelling assumptions and source caveats |

### `queue-proposals-cost-access.csv`

Format per `queue-proposals-README.md`; prefix P-ACC-.

## Validation corrections (wave 10, 2026-11-15) — governing
Source: [validation-wave10-report.md](validation-wave10-report.md). Where these conflict with the text above, these govern.

- **Line 24, adviser-layer bullet.** After "Published caps are 1.00% at MS GIFT, DAFgiving360 and TIFIN Give/GiveClear.", add: "MS GIFT's cap excludes Legacy Pools (0.60–1.24%) and, under Select UMA, third-party SMA manager fees, which are charged on top."
- **Line 65, MS GIFT row, adviser cell.** Replace "max 1.00% ([F](…))" with "max 1.00% from 2021-07-21, excl. Legacy Pools and SMA fees ([F](…))".
- **Line 133–135, Edward Jones.** Replace "Breakpoints are **assumed** equal to RCF donor-directed." with "Breakpoints are **assumed** equal to RCF donor-directed (0.60/0.30/0.20/0.15). A search-index capture of Ren's EJ client resource guide (article 10810347, now 404) shows administrator tiers of 0.60% / 0.35% / 0.25% (first $500k / next $500k / next $1m) and totals of 1.30% / 1.05% / 0.95%. If those apply, EJ admin at $2.5m is about 34 bps, not 30. Rows at $25k and $250k are unchanged."
- **Line 62, Edward Jones row.** Change the $2.5m admin cell from "0.30" to "0.30 (0.34 if captured tiers apply)".

## Adviser-fee update (2026-11-15) — governing over the adviser-layer rows
Source: [queue-adviser-fees-pools-npact.md](queue-adviser-fees-pools-npact.md); `data/mission-2026-11-14/adviser-fees-observed-2026.csv`.
- **Fidelity CIAP rows (all-in-cost-comparison-2026.csv rows 2–4):** CIAP requires $100k, so the adviser-managed scenario is not available at $25k.
- **NPT rows (11–13):** adviser-managed accounts start at $500k, so the scenario is not available at $25k or $250k.
- **AEF rows (23–25):** use the observed 0.46% implied adviser fee (TY2024 990) instead of the illustrative 1.00%. AEF all-in with adviser at $250k ≈ 1.16%, not 1.70%.
- **Caps:** no adviser-fee cap exists at Fidelity CIAP, NPT, AEF or RCF. Observed RIA brochures show 0–2.00%. Vanguard Charitable offers no adviser-managed option.
