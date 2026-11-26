# Nonprofit-side panel across DAF sponsors and rails (P-NPT-06); PayPal Grant Payments in 2026 (P-BNK-05); AEF legacy DonorCentral (P-ACC-04)

**Date:** 2026-11-15. **Author:** nonprofit-panel queue agent. **Recency:** 2021+ only. Every cell describes current (2024–2026) terms.

**Read first and built on:**
- `queue-payment-rails-cluster.md`: Fidelity EFT, timing clocks, void/escheat (§2–3)
- `queue-community-foundation-rails-portals.md`, including its wave-7 corrections. GWCF is "REPAY (payments partner, alongside Blackbaud Financial Edge NXT)", not "Blackbaud REPAY". CCT "documents checks only" for DAF grants.
- `queue-agentic-products-dafpay-fees.md`, including its wave-8 corrections. Every.org absorbs the For Good fee for bank-account gifts. The DAFpay rounding worst case applies only where no platform agreement exists.
- `queue-all-in-cost-dafpay-access.md` (wave-10 corrections; §3 AEF export)
- `queue-bank-programs-and-eft-providers.md`, including its wave-6 corrections. Charityvest is "transitioning from Aug 2026, per Chariot; Charityvest's own charity guide still describes PayPal Grant Payments".

**Outputs:**
- `data/mission-2026-11-14/nonprofit-side-panel-2026.csv`: the panel, 33 entities × 8 fields. Each field has a value, a source-URL cell and an origin cell.
- `data/mission-2026-11-14/nonprofit-side-panel-2026-evidence.csv`: 79 long-format cells read fresh on 2026-11-15, or carried from repo prose with their URL.
- `scripts/mission_nonprofit_panel.py`: stdlib, functional; merges seven repo CSVs and the evidence file, and prints coverage.
- `data/mission-2026-11-14/queue-proposals-nonprofit-panel.csv`: P-NPP-01 to P-NPP-04.

**Labels:**
- [F] fetched first-party text
- [S] search-engine extract (the page was not opened)
- [V] vendor statement
- [H] HTTP/DNS observation
- [I] inference

---

## 0. Headline answers

| ID | Answer | Confidence |
|---|---|---|
| **P-NPT-06** | The panel is built: 20 sponsors, intermediaries and rails, plus 13 community foundations. **DAF sponsors and their payout rails charge nonprofits nothing to receive a grant.** The exceptions are three intermediaries and one connector: Benevity/AOGF (2.99% Cause Support Fee capped at $500, plus a manual check fee of the higher of $35 or 8%, capped at $125), Chariot DAFpay at default terms (2.9%), and Every.org via ForGood (1.5%). Minimums run from $50 (Fidelity, DAFgiving360) through $250 (NPT, MS GIFT) to $500 (Vanguard). Intermediaries set disbursement thresholds instead: $10 at Every.org/ForGood and $100 aggregated before a Benevity check. **Every electronic rail falls back to a mailed check.** Remittance data is donor-controlled at every sponsor that publishes a rule. The fund name is offered as a separate disclosure choice at DAFgiving360, NPT, Vanguard (the default), Daffy and Chariot exports. Community-foundation rows are rail-only (§3). | High on fees and rails; medium on remittance; low for community foundations |
| **P-BNK-05** | **Yes for both.** NPT's DAF Guide (PDF created 2026-10-15) still pays grants up to $250,000 by "Grant Payments (electronic funds transfer via PayPal) or check", and says "At this time, NPT does not issue payments via ACH transfer" [F]. Vanguard's live nonprofit page says it "is now issuing grants through PayPal" [F]; its policies (updated 2026-01-09) say "third-party electronic fund transfer provider" or check [F]. **Leaving:** Charityvest, which is moving to Chariot Disbursements from Aug 2026 [F, repo]. **Joining:** none found. PayPal's help and partner pages name no grantmakers [F], and no 2025–26 announcement names a new sponsor [S]. | High for NPT and Vanguard; medium on "no new joiners" (absence of evidence) |
| **P-ACC-04** | **Not determinable from public evidence, and the repo's "live login shell" signal is non-diagnostic.** `aef.donorcentral.com` returns HTTP 200: a 4,971-byte SKY UX shell titled "Donorcentral", last-modified 2026-11-14. **A random nonexistent subdomain (`xyz.donorcentral.com`) and `www.donorcentral.com` return the identical shell from the same IP (172.168.220.232)** [H]. The 200 therefore shows wildcard hosting, not an AEF tenant. AEF's homepage still links "DonorCentral" [F]. AEF's upgrade FAQ answers "No" to returning to DonorCentral and shows two years of history on the new platform [F]. No AEF page grants or denies read-only legacy access. New finding [H/I]: the shell's bundle calls `capp-prod-cores-dc-usc-001.donor.npact.com` and links NPact's "FIMS and DonorCentral" knowledge base. This bears on the repo's statement that "DonorCentral is a Blackbaud product, not NPact" (P-NPP-04). | High on the HTTP facts; access itself unresolved |

---

## 1. Method

1. **Scope.**
   - The 20 non-CF entities are the sponsors and rails named in the queue item. Ren-administered programs (RCF and others) form one row. YourCause/Blackbaud Giving Fund is added because the queue text names it.
   - The community-foundation rows are the top 10 by FY2024 DAF assets in `community-foundation-rails-portals-2026-v2.csv`, plus three with distinctive 2026 rails: Seattle (mandatory ACH from 2026-06-30), SPMF (Chariot) and GWCF (REPAY).
2. **Fields.** The eight fields are listed in the data dictionary (§6). The queue's "check-vs-EFT default" becomes `default_rail`. The queue's "remittance data" is split into `remittance_donor_identity` and `remittance_fund_name`.
3. **Merge.** `mission_nonprofit_panel.py` applies ordered rules to each repo CSV. For example, `sponsor-eft-providers-2026.csv:enrollment_requirement` → `enrollment_requirement`, and `bank-program-terms-2026.csv` rows with `item=remittance_fields` → remittance. A row in the evidence file overrides the repo; the origin cell then reads `fresh:… ; supersedes repo:<file>`. The script stops if any entity key matches no input row, or if any evidence row names an unknown entity or field.
4. **Coverage semantics.**
   - *covered*: substantive text.
   - *not_found*: sources were read and were silent. The cell starts "not found".
   - *blank*: not researched for that entity in this pass.
5. **Fetch failures:**
   - dafgiving360.org returned 403. The 2024 Program Policies were read from the third-party-hosted copy already in the repo.
   - Benevity causes-help pages and the PayPal Giving Fund policies pages returned 403.
   - every.org/nonprofits returned 429.
   - Endaoment's "receiving-endaoment-grants" page returned 404.
   - Those cells are [S] or blank. Zendesk help-centre JSON endpoints were not used.
6. **Fee cells for sponsors on a named rail.** Vanguard and NPT use PayPal; Daffy, Charityvest and Endaoment use Chariot. Their fee cells cite the rail's statement, because the sponsors' own pages state no fee. Where neither said anything, the cell reads "not found".

## 2. Coverage (script output, 2026-11-15)

| Field | Sponsors + intermediaries + rails (n=20): covered / not found / blank | Community foundations (n=13): covered |
|---|---|---|
| fee_per_gift | 14 / 3 / 3 | 0 |
| disbursement_cadence | 16 / 0 / 4 | 0 |
| minimum_threshold | 7 / 0 / 13 | 0 |
| default_rail | 20 / 0 / 0 | 13 |
| enrollment_requirement | 20 / 0 / 0 | 1 |
| remittance_donor_identity | 17 / 2 / 1 | 0 |
| remittance_fund_name | 11 / 1 / 8 | 0 |
| void_return_policy | 10 / 2 / 8 | 0 |

The panel has 137 non-blank cells: 79 fresh or curated in the evidence file, and 58 derived from repo CSVs. Every non-blank cell has a source URL. NPT is the only entity with 8/8. Fidelity, Vanguard, Daffy, Benevity and DAFpay have 7/8. YourCause and DAF Direct have 3/8.

## 3. Findings

### 3.1 Fee per gift
- **$0 at sponsors and payout rails:**
  - Fidelity: "Both Stripe and ACH are free services offered by Fidelity Charitable" ([FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)) [F].
  - PayPal Grant Payments: "There are currently no fees associated with receiving grants via PayPal" ([PayPal](https://www.paypal.com/us/cshelp/article/what-are-grant-payments-help883)) [F].
  - Chariot Disbursements: "at no cost" ([Chariot](https://www.givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors)) [V].
  - DAF Direct: "no administration or transaction fees" ([DAF Direct](https://www.dafdirect.org/about-daf-direct/index.html)) [F].
  - PayPal Giving Fund: "Without charging … charities" ([PPGF](https://www.paypal.com/us/webapps/mpp/givingfund/about)) [F].
  - DAFgiving360, AEF and YourCause state no nonprofit fee ("not found").
  - NCF passes on the bank's wire fee, "usually about $25", for wires on request ([NCF](https://www.ncfgiving.com/support)) [F].
- **Benevity/AOGF** ([fee schedule, updated 2026-10-01](https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf)) [F]:
  - The Cause Support Fee is 2.99%, capped at $500. The cap does not apply to matches or securities.
  - Card gifts carry 2.95%.
  - The **manual check fee is the higher of $35 or 8% per check, capped at $125**. It applies after a Cause has received two checks.
  - Client master agreements may set different rates.
  - [I] On a $300 check the check fee is $35, or 11.7%, on top of the Cause Support Fee. This is the steepest nonprofit-side cost in the panel.
- **Chariot DAFpay default** is 2.9% (repo F01, [Chariot ToS](https://www.givechariot.com/legal-nonprofit)). **Every.org via ForGood** is 1.5%; it is 0% via a connected bank or PayPal Grants, and per the wave-8 correction, Every.org currently absorbs the ForGood fee for bank-account gifts.

### 3.2 Default rail and enrollment
- **No sponsor requires EFT.** This repeats `queue-payment-rails-cluster.md` §2.4. The exception among community foundations is Seattle Foundation, which requires ACH from 2026-06-30 (CF census).
- **Every electronic rail falls back to a check.** What triggers the fallback differs:
  - enrollment status at the time of payment: Fidelity, NPT, AEF, Benevity, YourCause;
  - a five-business-day claim window: Chariot (Daffy, Charityvest, Endaoment, DPN);
  - a 14-day PayPal acceptance expiry: NPT;
  - up to 90 days of enrollment outreach: PPGF.
- **Check-only programs:** BofA CGF and DAFgiving360, as documented in 2024. NPT says it "does not issue payments via ACH"; its electronic rail is PayPal only ([NPT guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf)) [F].
- **Endaoment:** grants are "paid out as USD through Chariot", and "You do not need to claim an Endaoment profile" ([docs](https://docs.endaoment.org/organizations/resources/organization-faq.md)) [F]. Older Endaoment pages still describe a claim-and-ACH path [S].
- **Ren for Charities:** one ACH sign-up covers "25+ donor-advised fund programs", which are not named ([Ren help](https://intercom.help/rengiving/en/articles/6229556-ren-for-charities-overview)) [F]. That count is the only figure Ren publishes for the network the CF census queried.

### 3.3 Cadence and thresholds
- **Sponsors** publish per-grant processing ranges: 3–10 business days, or Fidelity's "10 or more".
- **Intermediaries batch:**
  - PPGF pays enrolled charities monthly, "15-45 days after donation at the end of the month" ([PayPal](https://www.paypal.com/us/cshelp/article/how-does-paypal-giving-fund-grant-donations-to-charities-help969)) [F].
  - Every.org pays connected banks weekly; otherwise it pays monthly via PPGF, or via ForGood on the 15th of the following month. The ForGood minimum is $10 ([Every.org](https://support.every.org/hc/en-us/articles/360059998673-How-long-does-it-take-for-my-donation-to-reach-the-nonprofit)) [F].
  - YourCause schedules are "set by the client", mostly monthly or quarterly ([Blackbaud](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-faq-how-to-receive-donations.html)) [F].
  - Benevity holds checks until $100 has accumulated across the platform. It sweeps balances of $20 or more annually. Below $20, the donor advice "may be rejected" [F]. Faster cycles began rolling out from 2026-04-07 [S].
- **Minimum grant:**
  - Fidelity: $50 (repo).
  - DAFgiving360: $50 ([2024 Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf)) [F].
  - NPT: $250 [F]. MS GIFT: $250 (repo).
  - Vanguard: $500 ([policies](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines)) [F].

### 3.4 Remittance data
- **Donor identity is donor-controlled wherever a rule is published:**
  - Fidelity: "Any information the donor has permitted us to share"; about 4% of grants are anonymous.
  - DAFgiving360: three options, including "Anonymously with an explanatory note". Nothing is released "without the account holder's explicit consent".
  - NPT: "will not release your name or contact information for grants that are sent anonymously".
  - Vanguard: anonymous distributions "omit account and advisor information but state the grant purpose".
  - Daffy: only "If the donor chooses to share it".
  - Charityvest: "completely anonymous" is possible.
  - Endaoment: name and email "should they choose".
  - PPGF: shared with enrolled charities unless the donor gives anonymously [S].
  - BofA, MS GIFT and NCF: the account or donor name appears unless anonymous (repo).
- **Fund name** is a separate choice at DAFgiving360 (special account name), NPT, Daffy and Vanguard. Vanguard shows it by default: "The account name will appear in letters and communications".
- **Chariot's donation export** has "Donor Fund Name", "Donor Full Name", email, phone and address columns, plus "DAF Organization". It has **no anonymity column** ([Chariot](https://help.givechariot.com/getting-started/donation-fields.md)) [F]. How sponsor anonymity choices map into these columns is not documented (P-NPP-03).
- **Format:**
  - Fidelity: daily secure-email ACH report, or weekly Stripe notice.
  - NCF: Excel letter.
  - Benevity: Detailed Report CSV [S].
  - PayPal: dashboard with "donor details, grant letter, and terms & conditions".
  - Chariot: dashboard.

### 3.5 Void and return
- **Published rules:**
  - Fidelity: 90 days; the donor must request a reissue.
  - BlueGive: 90 days (repo).
  - Chariot DPN: 90 days, then possible regrant.
  - NPT: 14-day PayPal expiry, then a check.
  - PayPal Grant Payments: the expiry is "set by the grantmaker".
  - Ren: reissue needs the grant ID; ACH reissue only if the donor allows.
  - Benevity: the sub-$20 sweep can reject the donor's advice.
- **Vanguard** says only "Approval for the return of grant funds for any reason is at the discretion of Vanguard Charitable" [F].
- **DAFgiving360's 2024 policies** cover declining a grant when the charity is unreachable for 30 days, not uncashed checks [F].
- **No escheat language was found** in any source. This matches §3.2 of the payment-rails note.

### 3.6 Community foundations
- Only the rail is populated, from the CF census. Two cells, OCF enrollment and Seattle's ACH mandate, also carry enrollment detail.
- The other seven fields were not researched in this pass. They are blank, not "not found" (P-NPP-01).
- [I] With 0/13 coverage, nothing should be inferred about community-foundation remittance or void practice.

## 4. P-BNK-05 detail
- **NPT.** In the guide created 2026-10-15:
  - "Grant Payments (electronic funds transfer via PayPal) or check";
  - "If a grant is sent by EFT via PayPal, the grantee has 14 days to accept";
  - wires only for grants of $250,000 or more and for international grants;
  - "At this time, NPT does not issue payments via ACH transfer" ([guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf)) [F].
  - The older NPT for-charities URL returns 404.
- **Vanguard:**
  - The live nonprofit page tells charities to sign up at paypal.com/charities ([Vanguard](https://www.vanguardcharitable.org/nonprofit-organizations)) [F].
  - The policies page (updated 2026-01-09) keeps the generic "third-party electronic fund transfer provider" wording ([policies](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines)) [F].
- **Charityvest** is leaving PayPal: Chariot from Aug 2026 ([Chariot](https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner)) [F]. Its own guide still says "daily via PayPal and weekly via check" ([guide](https://guide.charityvest.org/for-donors/getting-started/grants-to-charity.md)) [F].
- **New users:** none found.
  - PayPal's help page refers only to "grantmakers, such as significant donor-advised funds and community foundations" [F].
  - Searches for 2025–26 announcements returned only the 2022–23 launch coverage [S].
  - The CF census found no community foundation using PayPal Grant Payments.
  - Not done: the 990 Schedule O / Part VII-B check named in the queue. PayPal would not appear as a contractor for a free service [I].

## 5. P-ACC-04 detail (public HTTP/DNS only; no login, no API calls)

| Observation | Result | Label |
|---|---|---|
| `GET https://aef.donorcentral.com/` | 200, `content-length: 4971`, `last-modified: Sat, 14 Nov 2026 08:38:22 GMT`, nginx, `<title>Donorcentral</title>`, Angular `<app-root>` with SKY UX styles | [H] |
| `GET https://xyz.donorcentral.com/` (nonexistent) and `https://www.donorcentral.com/` | 200, same 4,971 bytes, same last-modified | [H] |
| DNS | `aef.`, `xyz.` and `www.donorcentral.com` all resolve to 172.168.220.232 (wildcard) | [H] |
| Public JS bundle `main.18637f992cb04132.js` | API base `https://capp-prod-cores-dc-usc-001.donor.npact.com`; links to `npact.document360.io/fims-and-donorcentral/…`; tenant resolved at runtime from claims (`http://melabs.io/claims/dc/tenant`) | [H] |
| AEF homepage | Nav link "DonorCentral" → `https://aef.donorcentral.com/#/sign-in?redirectUrl=…` | [F] ([AEF](https://www.aefonline.org/)) |
| AEF upgrade FAQ | "No. You will continue to use this new platform."; "Only granting history from the past two (2) years will be reviewable on this platform." Nothing on read-only legacy access | [F] ([FAQ](https://engage.aefonline.org/?p=12588)) |

**Answer.**
- Public evidence cannot show whether AEF donors can still sign in to DonorCentral.
- The host-level 200 is a wildcard and carries no information about AEF.
- AEF's only statements point away from DonorCentral, yet it still links the login.
- The tenant answer sits behind runtime calls to the NPact-hosted API, which were deliberately not made.

**Correction candidate for `queue-all-in-cost-dafpay-access.md` §3 [I].** "the host serves a live login shell" and "(DonorCentral is a Blackbaud product, not NPact)" should be read with two caveats:
1. the shell is served for any subdomain;
2. the current DonorCentral front end calls NPact infrastructure.

Who owns the product should be confirmed from a primary announcement (P-NPP-04) before any wording changes.

## 6. Data dictionary: `nonprofit-side-panel-2026.csv` (one row per entity)

| Column | Meaning |
|---|---|
| `entity_id` | Stable key (e.g. `fidelity`, `chariot_dafpay`, `cf_svcf`) |
| `entity` | Display name |
| `entity_type` | One of: `national_sponsor`, `bank_sponsor`, `challenger_sponsor`, `intermediary` (PPGF, Every.org, Benevity, YourCause), `rail` (Chariot, PayPal Grant Payments, DAF Direct), `community_foundation` |
| `fee_per_gift` | Amount deducted from, or billed to, the receiving nonprofit per gift at default terms |
| `disbursement_cadence` | How often, and how fast, funds leave after approval, as published (none is an SLA) |
| `minimum_threshold` | Minimum grant (sponsors), or minimum disbursement or check threshold (intermediaries) |
| `default_rail` | Rail used for an enrolled nonprofit, and the fallback for an unenrolled one |
| `enrollment_requirement` | What the nonprofit must do to receive electronically |
| `remittance_donor_identity` | Donor name and contact disclosure rules, anonymity option, and delivery format |
| `remittance_fund_name` | Whether the DAF or fund name reaches the nonprofit |
| `void_return_policy` | Uncashed-check window, expiry, reissue and regrant rules |
| `<field>_src` | Source URL(s), separated by " ; " |
| `<field>_origin` | `fresh:<retrieved> [class]`, optionally followed by `; supersedes repo:<file>`, or `repo:<file>` |
| `fields_covered` | Count of covered fields (not blank, not "not found") out of 8 |

**`nonprofit-side-panel-2026-evidence.csv`** (long format) has these columns:
- `entity_id`, `field`, `value`, `source_url`
- `evidence_class` (F/S/V/I/H)
- `source_date`, `retrieved`, `note`

**`queue-proposals-nonprofit-panel.csv`** contains P-NPP-01 (community-foundation remittance and void), P-NPP-02 (void and escheat at seven sponsors), P-NPP-03 (anonymity through Chariot) and P-NPP-04 (DonorCentral operator).

## 7. Limitations
- Some remittance cells rest on search extracts [S]: PPGF, Benevity, Every.org and RCF. RCF's evidence is one RCF-sponsored program's FAQ.
- DAFgiving360 terms are from 2024; the site blocks fetches.
- Benevity rates can be overridden by client master agreements. YourCause terms vary by corporate client.
- Fee cells give list terms, not realised fees (see `queue-agentic-products-dafpay-fees.md` §3.5).
- Community-foundation rows are deliberately thin.

## Validation corrections (wave 12, 2026-11-15) — governing
Source: [validation-wave12-report.md](validation-wave12-report.md). Where these conflict with the text above, these govern.

- Line 32 (P-BNK-05): replace the quote "is now issuing grants through PayPal" with the live text "is now issuing Grant Payments with PayPal" ([Vanguard](https://www.vanguardcharitable.org/nonprofit-organizations), fetched 2026-11-15).
- Line 91: replace "**No sponsor requires EFT.**" with "**No sponsor checked requires EFT today.** Fidelity says it does 'not currently require EFT' but is 'transitioning grant payments to EFT' under a digital-first policy."
- Line 110: add "(2024 policy document; no 2025/26 version checked)" after the DAFgiving360 $50 cite.
- Line 111: replace "MS GIFT: $250 (repo)" with "MS GIFT: $250 ([MS GIFT FAQ](https://www.morganstanley.com/gift), search capture 2026)".
- Lines 97 and 157 (NPT guide cite): add "URL path is /2024/09/ but PDF metadata is 2026-10-15".
