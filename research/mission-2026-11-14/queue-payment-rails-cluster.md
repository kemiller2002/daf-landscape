# Payment-rails queue cluster: P-CMP-03, P-CMP-02, P-CON-04, P-CON-02

**Date:** 2026-11-14. **Author:** payment-rails queue agent.
**Builds on:**
- [daf-user-complaints-deep-research.md](daf-user-complaints-deep-research.md) §5.8
- [queue-contract-data-rights-agent-controls.md](queue-contract-data-rights-agent-controls.md) §2
- [industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md) §6.1 and its governing wave-2B red-team section
- [competitive-history-timelines.md](competitive-history-timelines.md)
- [../daf-grant-tracking-payment-rails-comparison-2026-11-11.md](../daf-grant-tracking-payment-rails-comparison-2026-11-11.md)
- [queue-infrastructure-nonprofit-costs-emerging.md](queue-infrastructure-nonprofit-costs-emerging.md), written concurrently. Its fee and cost-per-grant work is reused here, not repeated.

**Outputs:**
- `data/mission-2026-11-14/sponsor-grant-payment-policies.csv`
- `data/mission-2026-11-14/queue-proposals-payment-rails.csv`

**Method and limits.**
- Every factual claim carries an inline URL. "Live" means the page was fetched on 2026-11-14.
- **Fetch failures:**
  - Bogleheads returned HTTP 402/403 to both WebFetch and curl. Forum content comes only from search-engine extracts, already logged as CMP-152 to CMP-155 in `daf-user-complaints-corpus.csv`.
  - dafgiving360.org returned 403 to all fetches.
  - web.archive.org was unreachable from this environment (connection reset; fetch tool blocked), so earlier versions of Fidelity's pages could not be compared.
  - Fidelity's `help/grant-delivery-faq.html`, cited in earlier repo files, now returns 404.
- **Labels:** [F] fetched first-party text; [S] search-engine extract or secondary report, not verified against the page; [I] inference.

---

## 1. Answers at a glance

| ID | Answer | Confidence |
|---|---|---|
| **P-CMP-03** | **No, not as of 2026-11-14 on Fidelity's own pages.** The live nonprofit page says Fidelity "does not currently require EFT enrollment" [F]. The nonprofit FAQ says it is "transitioning grant payments to EFT" under a "digital-first policy", and that never-enrolled nonprofits "receive grants through checks mailed to the addresses listed on your organization's IRS Form 990" [F]. The donor page says approved funds go "via check or EFT" [F]. The July 1, 2026 EFT-only date is documented only in secondary sources: Chariot (Mar and May 2026) and Bogleheads extracts. The extension is documented only in a Bogleheads extract quoting Fidelity's site, with no new date [S]. **Fidelity's own 2026 Giving Report says 67% of grants go by EFT**, which upgrades the Chariot figure from secondary to first-party. No Fidelity page says grants to unenrolled charities are held. The live fallback is a mailed check. | High on current page text. Medium on the history of the announcement and extension. |
| **P-CMP-02** | No sponsor publishes an SLA. Each publishes "generally/typically" ranges for different clocks (§3.1). The only measured distributions are: Chariot's one-nonprofit dataset (ACH 1–2 days, check-paying providers 7–162 days on average); Charityvest's "95% of checks are deposited … within 35 days of when they are sent"; and AssetMark Charitable's median of 2 days from submission to funds. On uncashed checks, Fidelity reports returned grants at 90 days and BlueGive cancels and redeposits at 90 days. Chariot's DAFpay Network voids its checks after 90 days and may regrant the money. **No sponsor publishes a void or reissue rate, and none mentions escheat.** | Medium |
| **P-CON-04** | **No sponsor is publicly documented as live on the provider-side "Create Grant" API.** Chariot's v2026-04-01 OAuth provider spec names no live providers [F]. Donor Accounts (beta, 2026-05-08) is in "a pilot program with a handful of design partners", unnamed [F]. DAFpay's "compatible flow" ("hundreds of DAFs", "+85% of the $326B DAF market") has the donor authenticating to their DAF provider inside or alongside the DAFpay modal, with DAFpay managing "credential verification, multi-factor authentication" [F]. That is a donor-credential path, not a sponsor-exposed API. Named "integrated" providers (Fidelity, Schwab/DAFgiving360, Vanguard, NPT, Charityvest) appear only in third-party integrator pages [S/F]. No volume figure isolates third-party-initiated grants. | Medium-high that no OAuth provider is publicly named. Low on which sponsors are design partners. |
| **P-CON-02** | **No other vendor's public terms copy NPact §2.4's explicit ban on third-party-initiated grants.** The nearest equivalents are generic: iPhi §3.4(c) "for the benefit of a third party"; Foundant MSA §3.2(d) "permit any party, other than the then-currently authorized Users to independently access"; Bonterra §5.6(e) "make available any Services to any third party"; competitive-use bans at Foundant, Bonterra and iPhi; and anti-automation or anti-scraping site and AI terms at TIFIN, Givinga, Foundation Source and Blackbaud AI. No vendor calls any of these terms negotiable. Every contract, though, has an order-of-precedence clause that lets an Order Form, SOW or Work Order override it, in most cases only by express reference (§5). | Medium-high for public templates. Executed contracts unknown (P-CON-01). |

---

## 2. P-CMP-03: Fidelity Charitable and EFT-only grants

### 2.1 What Fidelity's own pages say (live 2026-11-14)

- **Nonprofit landing page.** "Fidelity Charitable does not currently require EFT enrollment but encourages en[rollment]…". It calls EFT "a safer, faster alternative to paper checks" ([fidelitycharitable.org/nonprofits.html](https://www.fidelitycharitable.org/nonprofits.html); same text at [nonprofits/overview.shtml](https://www.fidelitycharitable.org/nonprofits/overview.shtml)) [F].
- **Nonprofit FAQ** ([nonprofits/faqs.html](https://www.fidelitycharitable.org/nonprofits/faqs.html)) [F]:
  - "As Fidelity Charitable moves towards a digital-first policy we are transitioning grant payments to EFT to ensure faster, safer, and more reliable delivery of funds."
  - "While we do not currently require EFT enrollment for nonprofit organizations, we encourage you to enroll."
  - It asks nonprofits to "work with your board to update your policy" where board policy restricts EFT.
  - "Nonprofits that have never enrolled in our EFT program receive grants through checks mailed to the addresses listed on your organization's IRS Form 990."
  - Stripe and ACH both deliver funds in "1-2 days". "The ACH enrollment queue may take several weeks." Both are free.
  - "We can void a grant check and notify the recommending donor" at the charity's request. "Fidelity Charitable cannot reissue a grant check unless requested by the recommending donor."
- **EFT page.** Stripe enrollment takes "1-3 business days". The ACH queue "may take up to 4 weeks" and "may face seasonal delays". The page sets no deadline ([nonprofits/eft.html](https://www.fidelitycharitable.org/nonprofits/eft.html)) [F].
- **Donor-facing page.** "Fidelity Charitable will send approved funds via check or EFT" ([supported-charities](https://www.fidelitycharitable.org/giving-account/supported-charities.html)) [F]. The address FAQ tells donors to point unenrolled charities to the nonprofit page ([different-charity-addresses](https://www.fidelitycharitable.org/faqs/all/different-charity-addresses.html)) [F].
- **Program Guidelines** (PDF created 2026-09-11). No EFT-only grant rule was found. "EFT" appears only for contributions ([program guidelines PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf)) [F].
- **2026 Giving Report** (PDF created 2026-04-21): "Today, 67% of our grants are distributed via EFT, meaning that more than 2 million grants have reached nonprofits faster and more securely than with traditional check processing." Also: "In 2025, 98% of grant recommendations were initiated digitally" ([2026 Giving Report PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf)) [F]. The report does not mention an EFT-only date.

### 2.2 What secondary sources say

| Source | Claim | Status |
|---|---|---|
| Chariot, "Top 8 Takeaways…", dated "Mar 24" (© 2026) | "Fidelity Charitable is moving to electronic-only disbursement in July 2026"; 67% EFT and 33% check in 2025 ([Chariot](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report)) | [S]. The 67% now matches Fidelity's report. The July date has no source link. |
| Chariot, "Your 'Not Enrolled for E-Pay' Status…", dated "May 7" (© 2026) | "Electronic-only disbursement in July 2026"; unenrolled organizations "will not be able to receive grants from Fidelity Charitable at all"; "before the June 30 Fidelity enrollment deadline"; 3 million grants in 2025, about 1 million by check ([Chariot](https://www.givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors)) | [S]. Chariot sells the competing receiving rail. |
| Bogleheads t=464478 (Dec 2025–Oct 2026) | Quotes a notice: "beginning July 1, 2026, all … grants will be delivered exclusively through EFT". Later posts quote Fidelity's site: "Fidelity Charitable has extended our EFT requirement date to allow organizations sufficient time to enroll" (no new date). One post fears grants "will be held until they do". A mid-Oct 2026 post reports a grant to a check-only charity "went through" ([thread](https://www.bogleheads.org/forum/viewtopic.php?t=464478); [page 5](https://www.bogleheads.org/forum/viewtopic.php?p=8701653)) | [S] only. The forum blocks fetches. Search-engine extracts are logged as CMP-152 and CMP-155 in `daf-user-complaints-corpus.csv`. |

### 2.3 Answer

1. **Was the EFT-only rule implemented?** Not on the public record as of 2026-11-14.
   - Fidelity's nonprofit, FAQ and donor pages all describe checks as a live fallback and say EFT is "not currently" required [F].
   - The Program Guidelines dated September 2026 contain no EFT-only rule [F].
   - The only evidence of implementation runs the other way: an October 2026 forum report of a check grant [S].
2. **Was it extended?** Only a Bogleheads extract shows this [S]. It is consistent with Fidelity's current "not currently require" wording, which reads as a deferral rather than a cancellation [I]. **No new effective date was found anywhere.**
3. **What happens to grants for unenrolled charities?**
   - Fidelity's current text: a mailed check to the Form 990 address [F].
   - The "held until enrolled" scenario appears only as a forum worry [S]. No Fidelity text supports it.
   - Chariot's claim that such charities "will not be able to receive grants … at all" [S] is not reflected on any Fidelity page.
4. **What share goes by EFT?**
   - 67% of grants by count (Fidelity, first-party) [F]. The dollar share is not published.
   - "More than 2 million" EFT grants at 67% implies at least about 3 million grants a year [I], which matches Chariot's figure.
   - **The share of recipient charities still unenrolled is not published.**
5. **Correction for the repo.** [queue-infrastructure-nonprofit-costs-emerging.md](queue-infrastructure-nonprofit-costs-emerging.md) calls the 67% "secondary and unconfirmed by Fidelity". It is confirmed in Fidelity's 2026 Giving Report [F]. The wave-2B red-team insert for §6.1 in [industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md) can now cite Fidelity directly.

### 2.4 Other sponsors' EFT and check policies

| Sponsor | Rails | EFT required? | Unenrolled fallback | Evidence |
|---|---|---|---|---|
| **DAFgiving360** | Only checks are documented | No EFT option documented | n/a | 2024 Program Policies: "on average, checks are generally mailed within seven to 10 business days … USPS delivery typically takes three to five business days" ([2024 Program Policies PDF, third-party-hosted copy](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf)) [F]. A forum extract says "only paper checks" ([Bogleheads](https://www.bogleheads.org/forum/viewtopic.php?t=464478&start=100)) [S]. The site blocked fetches, so a 2026 EFT programme cannot be ruled out. This stays open as P-INF-06. |
| **Vanguard Charitable** | PayPal Grant Payments; checks (implied) | No | Check (implied, not stated) | "Receive your funds in a matter of minutes"; "Grants are generally processed within a few days" ([Vanguard nonprofits](https://www.vanguardcharitable.org/nonprofit-organizations)) [F]. 2023: funds "arrive within one day of the receiving charity accepting the grant"; "more than $130 million to more than 400 eligible charities" May–Sep 2023 ([PR Newswire, 2023-09-20](https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html)) [F]. |
| **NPT** | PayPal Grant Payments, check, wire | No | "If the charity has not yet registered for Grant Payments, NPT will process and mail a check as before" ([NPT Grant Payments flyer, 2022](https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf)) [F] | PayPal grants: "the grantee has 14 days to accept the payment before it expires and is then reissued to the grantee as a check" ([NPT DAF Guide, PDF dated 2026-10-15](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf)) [F]. |
| **Daffy** | Chariot Disbursements; US Mail | No | "Organizations that have not claimed a Chariot profile will continue to receive Daffy donations by US Mail" ([Daffy help, 2026-08-06](https://help.daffy.org/en/articles/15604949-what-is-chariot-disbursements)) [F] | Over $250M sent electronically through Chariot ([Chariot, Jul 2026](https://givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner)) [S]. |
| **Charityvest** | Chariot from Aug 2026 (replacing PayPal); check | No | "They will be sent a check in the mail" ([Chariot, 2026-07-29](https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner)) [F] | Charityvest's own guide still says "PayPal digital grant (daily) or paper check (weekly)" ([Charityvest guide](https://guide.charityvest.org/for-donors/getting-started/grants-to-charity.md)) [F]. The guide lags the switch. |

**Pattern** [I]:
- No sponsor examined requires EFT today.
- Every one that offers electronic delivery falls back to a mailed check.
- The newer sponsors (Daffy, Charityvest, AssetMark/TIFIN, BlueGive) put the fallback trigger in Chariot's five-business-day claim window. Fidelity and NPT key it to enrollment status at the time of payment.

---

## 3. P-CMP-02: Grant timing, SLAs, and void, reissue and escheat policies

### 3.1 Published timing by clock

The clocks follow the T2–T6 model in [../daf-grant-tracking-payment-rails-comparison-2026-11-11.md](../daf-grant-tracking-payment-rails-comparison-2026-11-11.md). **None of these figures is a contractual SLA.** All are worded "may", "generally", "typically" or "on average".

| Sponsor / rail | T2→T3 review | T3→T5 issue | T5→T6 settle | Source |
|---|---|---|---|---|
| Fidelity, any rail | "may take 10 or more business days"; longer in peak periods | — | Stripe/ACH "1-2 days"; EFT "up to 9x faster" than checks | [grant-processing-timeline](https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html); [nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html) [F] |
| DAFgiving360, check | "seven to 10 business days" until the check is mailed, on average | (included) | USPS "three to five business days" | [2024 Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) [F] |
| Vanguard, PayPal | "generally processed within a few days" | — | "matter of minutes"; "within one day of … accepting" | [Vanguard nonprofits](https://www.vanguardcharitable.org/nonprofit-organizations); [PR 2023](https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html) [F] |
| NPT, any rail | Domestic "5 business days or less" (the timeline page says 3–5); international up to 8 weeks | — | PayPal acceptance window of 14 days, then a check | [NPT DAF Guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) [F] |
| Daffy, Chariot / mail | Review "can take up to one week" | Chariot: "disbursed immediately" | Mail depends on "location and local USPS office" | [Daffy help](https://help.daffy.org/en/articles/9122843-how-does-daffy-send-donations-to-charity) [F] |
| Charityvest, PayPal or check (guide predates Chariot) | — | PayPal daily, checks weekly | Check "approximately 10 business days" in the mail; **"95% of checks are deposited by recipient charities within 35 days of when they are sent"** | [Charityvest grant status](https://guide.charityvest.org/for-donors/getting-started/check-grant-status.md) [F] |
| AssetMark Charitable (TIFIN Give-administered), Chariot | Verification "typically takes 1–3 business days" | — | **Median 2 days from grant submission to funds received; 0 days for electronic** | [AssetMark help](https://intercom.help/assetmark-help-center/en/articles/13931838-how-grant-payments-are-delivered-electronic-check) [F] |
| BlueGive, ACH / check | — | — | ACH "within 3 business days" of approval; check "within 1-2 weeks" | [BlueGive FAQ](https://intercom.help/bluegive-help-center/en/articles/10597826-granting-faqs) [F] |
| Chariot Disbursements, unclaimed account | — | Five-business-day claim window with three reminder emails, then a mailed check | Check delays of "~2-3 week[s]" | [Chariot tracking](https://help.givechariot.com/disbursements/for-grantmakers/tracking-and-delivery.md); [Chariot FAQ](https://help.givechariot.com/getting-started/disbursements-faqs.md) [F] |

**Measured (not published-target) data:**
1. **Chariot "All Checks, No Balance"** (Jan 2026). One nonprofit; "over 2,000 DAFpay gifts from 34 different DAF Providers over a 6 month period in 2025"; measured "from the point of grant initiation until actual payment delivery".
   - The fastest providers (Pledger, The Donors Fund, Fidelity) paid by ACH "within 1-2 days of grant approval".
   - The 18 check-paying providers averaged "7 to 162 days".
   - "Even the largest national DAFs have struggled to get their ACH rates much higher than 50%."
   - Source: [Chariot](https://givechariot.com/resources/insights/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits) [F]. This is a vendor study with n=1 recipient.
2. **Charityvest:** 95% of checks deposited within 35 days of sending (above) [F]. The sample and period are not stated.
3. **AssetMark:** median of 2 days (above) [F]. The sample and period are not stated.
4. **PayPal survey of 300 PayPal Confirmed Charities** (2023): "Charities receive over 55% of contributions from institutional grant makers via check and 22% via ACH" ([PayPal, How Philanthropic Dollars Move](https://filecache.mediaroom.com/mr5mr_paypal/186631/PP_2023_GrantPayments.pdf)) [F]. This is a vendor survey, and the denominator includes foundations.

### 3.2 Uncashed checks: void, reissue and escheat

| Party | Void trigger and window | What happens to the money | Reissue rule | Source |
|---|---|---|---|---|
| Fidelity Charitable | "Likely due to the charity not depositing the check after 90 days or the grant being returned by the postal service" | Returned to the donor's Giving Account. Search-indexed text of the now-404 grant-delivery FAQ says the grant is cancelled and the donor notified, with a possible EFT reissue if the charity enrolls during the check timeline | "Cannot reissue a grant check unless requested by the recommending donor." For a lost check, the donor calls to cancel and makes a new recommendation | [returned-grant FAQ](https://fidelitycharitable.org/faqs/all/returned-grant.html) [F]; [nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html) [F]; [lost-grant-check](https://fidelitycharitable.org/faqs/all/lost-grant-check.html) [F]; [grant-delivery FAQ (404 on 2026-11-14)](https://www.fidelitycharitable.org/help/grant-delivery-faq.html) [S] |
| BlueGive | "If the grantee doesn't cash your grant check within 90 days, the check will be cancelled and redeposited" | Back to the donor's account | — | [BlueGive FAQ](https://intercom.help/bluegive-help-center/en/articles/10597826-granting-faqs) [F] |
| Chariot DAFpay Network (intermediary) | "Issued checks are valid for 90 days. After this period, unclaimed funds will be voided" | "DPN retains exclusive legal control"; it may contact the donor or "grant the funds to a charity in the DPN Directory that operates in a similar cause area" | — | [DAFpay Network](https://help.givechariot.com/dafpay/dafpay-network.md) [F] |
| Daffy | Not stated | Not stated | "Daffy can cancel the original check and reissue a new one" via a help ticket | [Daffy help](https://help.daffy.org/en/articles/9122847-what-if-a-charity-doesn-t-receive-my-donation) [F] |
| Ren (sponsor administrator), dated 2025-12-10 | Not stated | Not stated | A reissue request needs the grant ID, check number and tracking. "ACH reissuance is only possible if the donor allows payment flexibility" | [Ren help](https://intercom.help/rengiving/en/articles/13123383-what-should-i-do-if-i-have-issues-with-receiving-a-grant-check-or-need-to-request-a-reissue) [F] |
| NPact (software) | — | — | Vendor docs cover a grantee cashing both the original and the reissued check, and a reissue changing the grant date shown to donors | [NPact doc](https://npact.document360.io/fims-and-donorcentral/docs/how-do-i-handle-a-situation-where-the-grantee-cashed-the-original-check-and-the-reissue); [NPact doc](https://npact.document360.io/fims-and-donorcentral/docs/re-issuing-a-grant-check-changes-the-grant-date-shown-in-donorcentral) [S] |
| DAFgiving360, Vanguard, NPT, Charityvest | **No public void window found** | — | — | Searches of their program documents found no uncashed-check clause (the DAFgiving360 2024 Program Policies and NPT DAF Guide PDFs were text-searched) |

**Escheat.** No DAF sponsor page, program policy or vendor document examined mentions escheat or state unclaimed-property reporting for grant checks. Where a public policy exists, the money reverts to the donor's fund (Fidelity, BlueGive) or is regranted under the sponsor's legal control (DPN). [I] Sponsors appear to treat a void as a cancelled grant, not as abandoned property owed to the payee. Whether state unclaimed-property law reaches voided charitable grant checks was not tested, and no source on it was found.

**Rates.** **No void, reissue or returned-mail rate is published** by any sponsor or vendor. Fidelity says "1 in 5 organizations report[ed] mail fraud" ([nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)) [F], but gives no rate per check.

---

## 4. P-CON-04: Live DAFpay providers and third-party grant initiation

### 4.1 Chariot's three integration modes

| Mode | Who creates the grant | Evidence of live providers |
|---|---|---|
| **OAuth Integration** (provider exposes Get Donor, List Funds, Create Grant with idempotency, Get Grant Status) | "Chariot creates grants via your API"; grants "flow through your existing review and disbursement pipeline" ([OAuth overview](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/overview.md); [API endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md)) [F] | **None named.** The docs give build estimates ("~2–4 weeks" to "~1–2 months", plus 1–2 weeks of Chariot certification) but no customer list [F]. |
| **Donor Accounts (beta)** (DAF verifies the donor and decides on Grant Requests through Chariot's APIs) | The DAF submits or rejects each Grant Request ([changelog 2026-05-08](https://docs.givechariot.com/changelog/2026/5/8)) [F] | "Available as part of a pilot program with a handful of design partners", unnamed [F]. |
| **Compatible flow** (legacy and main path) | The donor authenticates to their DAF provider by signing in "within the DAFpay modal", being "redirected to their DAF provider's site", or using "a secure SMS link or QR code". The gift is "submitted in real time" ([Compatible Providers](https://help.givechariot.com/dafpay/editor/supported-providers)) [F]. "DAFpay manages the entire grant submission process, including credential verification, multi-factor authentication, error management" ([DAFpay overview](https://docs.givechariot.com/v2026-04-01/guides/dafpay/overview.md)) [F]. The `/v1/dafs` API exposes `supported` and `institutionDown` flags per DAF ([List DAFs](https://docs.givechariot.com/v2026-04-01/api/donor-advised-funds/list.md)) [F] | "Hundreds of DAFs … representing +85% of the $326B DAF market" [F]. **There is no public per-DAF list.** The API needs a key. |

[I] An `institutionDown` flag and DAFpay-managed MFA fit a design where Chariot acts in the donor's own sponsor session, on the donor's credentials or a redirect. In that design the sponsor exposes nothing to Chariot. This is an inference from documentation, not a confirmed architecture. It matches the credential-sharing critique already in the repo ([Inequality.org](https://inequality.org/article/new-donor-advised-fund-tech-raises-old-concerns/)).

### 4.2 Named "integrated" providers come from integrators, not sponsors

- The Giving Block: "DAFpay currently has integrations with over 65% of the market, including … Fidelity Charitable, Schwab Charitable, and Charityvest" (undated) ([Giving Block](https://thegivingblock.com/integrations/chariot/)) [F].
- Givebutter and PMC pages list Fidelity, Vanguard, Schwab and NPT as fully compatible. Overflow adds Bank of America's Charitable Gift Fund, J.P. Morgan and BNY Mellon ([Givebutter help](https://help.givebutter.com/en/articles/6764835-how-to-use-givebutter-s-dafpay-donation-method); [PMC](https://www.pmc.org/ways-to-give/donor-advised-funds); [Overflow](https://overflowapp.zendesk.com/hc/en-us/articles/36109985992077-DAF-Giving-FAQs)) [S].
- **No sponsor page found endorses DAFpay or names Chariot as an authorized grant initiator.** Fidelity, DAFgiving360 and BNY instead run their own initiation widget, DAF Direct (see [queue-infrastructure-nonprofit-costs-emerging.md](queue-infrastructure-nonprofit-costs-emerging.md) §Q-B18, not repeated here).

### 4.3 Chariot Disbursements partners are a different relationship

These partners send payouts to nonprofits over Chariot. That does not make them DAFpay providers.

- **Live partner list:** Groundswell, Daffy, Founders Pledge, DAFShare, Dallas Jewish Community Foundation, Community Foundation of Northwest Mississippi, Neta Foundation, Community Foundation of South Puget Sound, Endaoment, GoodToday, phil, EarthShare, TIFIN, Jewish Federation of Northern New Jersey, Community Foundation of East Mississippi, Brooklyn Org, Modern Philanthropy Foundation, and Saint Paul & Minnesota Foundation ([Chariot, For Nonprofits](https://help.givechariot.com/disbursements/for-nonprofits.md)) [F].
- Charityvest is missing from that list despite its August 2026 switch ([Chariot](https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner)). [I] The list is probably lagging.
- AssetMark Charitable also pays through Chariot ([AssetMark help](https://intercom.help/assetmark-help-center/en/articles/13931838-how-grant-payments-are-delivered-electronic-check)) [F].

### 4.4 Volume figures

| Figure | Scope | Source |
|---|---|---|
| "DAFpay volume grew 46% in 2025 to over $5 million" | **Ambiguous.** It sits beside a single nonprofit CFO's testimonial and may describe one organization, not the network | [givechariot.com/dafpay](https://www.givechariot.com/dafpay) [F] |
| DAFpay average gift ~$1,000, median $250 | Network | same [F] |
| DAFpay on "over 100,000 nonprofits'" forms (Jan 2026) | Reach, not volume | [Business Wire, 2026-01-28](https://www.businesswire.com/news/home/20260128542200/en) [S]; [FinTech Futures copy](https://www.fintechfutures.com/press-releases/chariot-launches-first-gift-processing-platform-for-nonprofits) [S] |
| Daffy: "over a quarter billion dollars electronically" | Chariot Disbursements payouts, **not** DAFpay initiation | [Chariot, Jul 2026](https://givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner) [S] |
| Charityvest 2025: 48,744 grants, $119.2M | Volume moving to Chariot Disbursements | [Chariot, 2026-07-29](https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner) [F] |

**No public figure measures donor-delegated, third-party-initiated grant volume across sponsors.** The repo's description of DAFpay as "the only documented cross-vendor write channel" ([queue-contract-data-rights-agent-controls.md](queue-contract-data-rights-agent-controls.md) §2.9) should be qualified. The *sponsor-sanctioned* write channel (OAuth or Donor Accounts) is documented, but no named sponsor is live on it. The channel that carries volume is the donor-credential compatible flow.

---

## 5. P-CON-02: Have other vendors copied NPact §2.4?

### 5.1 NPact, the reference clause (re-checked 2026-11-14)

- **Still present.** The Standard Terms say "Last updated: August 26, 2025".
- **§2.4 "Rejection of External Passthrough".** NPact does not authorize customers, donors, vendors or agents "to access the Services or Software through third-party products or applications or initiate and/or authorize any actions including … donations, grants, transfers … or payments of any kind through third-party products or applications". Access is allowed "only by … direct login through the NPact Software".
- **Negotiability.** The Standard Terms "shall prevail unless and to the extent a provision … is expressly amended in the applicable SOW by reference to the applicable Section", and that amendment is valid "only for that particular SOW" (§19).
- Source: [NPact Standard Terms](https://npact.com/software-as-a-service-license-and-services-standard-terms/) [F].

### 5.2 Other vendors' public terms

| Vendor | Document (date) | Third-party / agent / automation clause | Same as §2.4? | Override mechanism |
|---|---|---|---|---|
| **Ren iPhi** | iPhi Platform MSA, Final Draft 2023-06-20 v2 (still served 2026-11-14) | §3.4: Customer shall not "permit or enable any third parties to … (c) use the Services for purposes of a third party or otherwise for the benefit of a third party; or (d) … creating a product or service commercially competitive" | **Partly.** It restricts third-party benefit but does not single out grant initiation or third-party apps | "In the event of a conflict … the terms of the Order Form and/or SOW shall prevail" ([iPhi MSA .docx](https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20v2.docx)) [F] |
| **Ren RAC / RCF** | Online RAC MSA v1 | No third-party-access clause found beyond confidentiality | No | "This Agreement will control unless the Work Order states that a specific provision … will be superseded" ([RAC MSA](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf)) [F] |
| **Stellar** | Runs on iPhi, per Ren product description | Inherits iPhi | — | ([Ren iPhi Product Descriptions](https://www.reninc.com/wp-content/uploads/2023/09/Ren-iPhi-Product-Descriptions-v1.pdf)) [S] |
| **Foundant** | MSA v012024 (orders on or after 2024-01-12) | §3.2(c) no "service bureau" use or processing of "any party other than Client"; **(d) "permit any party, other than the then-currently authorized Users to independently access the Platform"**; (g) no building of competitive products. "Users" include "donors, grant or scholarship applicants" authorized by Client | **Partly.** An agent with its own credentials would need to be an "authorized User". Grant initiation is not named. API is a paid add-on (repo) | Order of precedence: DPA, then SLA, then **Client Order Form**, then MSA. The Order Form outranks the MSA ([Foundant MSA PDF](https://info.foundant.com/rs/356-VHW-319/images/FT%20MSA%20-%20Final%20-%20v012024.pdf); [Foundant legal](https://www.foundant.com/legal/)) [F] |
| **Blackbaud** | Blackbaud Solutions Agreement (footer March 2026); AUP; AI Terms (June 2026) | BSA §3(a): access only "for Your internal business purposes". "Users" are employees, affiliates' employees and listed contractors. §17(f) disclaims third-party apps. AI Terms: "You may not use web scraping, web harvesting, or web data extraction methods to extract data from the AI" | **No.** No passthrough or grant-initiation ban. SKY API is the sanctioned route (repo) | The Agreement prevails over the Order Form "except where the Order Form explicitly amends a provision" ([BSA PDF](https://www.blackbaud.com/wp-content/uploads/2025/01/blackbaud-solutions-agreement.pdf); [AUP](https://www.blackbaud.com/wp-content/uploads/2025/02/acceptable-use-policy.pdf); [AI Terms 2026](https://www.blackbaud.com/wp-content/uploads/2026/06/blackbaud-ai-terms-2026.pdf); [terms index](https://www.blackbaud.com/terms-and-conditions)) [F] |
| **Bonterra** | Subscription and Services Agreement (online, 2026-07-13) | §5.6(d) no competitive use or benchmarking; **(e) no making "available any Services to any third party"** except as expressly permitted. "Third-Party Application" means products the "Customer elects to use with the Subscription Services". Bonterra "may cease making any such integration available in its discretion". "User" includes "agents who are authorized" | **No.** Customer-elected third-party apps are expected. No ban on initiation | The Agreement controls "except to the extent the Order Form specifically states that a provision … is superseded" ([Bonterra SSA PDF](https://www.bonterratech.com/wp-content/uploads/2026/07/bonterra-subscription-and-services-agreement-online_071326.pdf)) [F] |
| **Foundation Source** | Site Terms of Use (last updated 2026-01-12). The client services agreement is not public | Bans "scraping", making Services "available to third parties without our permission", and "any robot, spider, or other programmatic or similar automatic device". User must not be a competitor | **Site-level only** | The services contract applies alongside ([Foundation Source Terms of Use](https://foundationsource.com/terms-of-use)) [F] |
| **TIFIN Give** | TIFIN Terms (2025-02-19) | §5.3 bans robots and automated access; §7(e) bans benchmarks | No (generic) | Customer Software & Services Agreement governs (§16.9), per the repo ([TIFIN Terms](https://intercom.help/give-ria/en/articles/10092486-terms-of-use); [queue-contract-data-rights-agent-controls.md](queue-contract-data-rights-agent-controls.md) §2.4). TIFIN itself pays through Chariot Disbursements ([Chariot list](https://help.givechariot.com/disbursements/for-nonprofits.md)) [F] |
| **Givinga** | Site terms (undated) | Bans "any robot, spider, scraper or other automated means or any manual process" without written permission, and competitive monitoring | Site-level only | No platform contract is public ([Givinga terms](https://www.givinga.com/terms-and-conditions)) [F] |
| **Give Interactive** | **No public terms found** | — | Unknown | Searches returned only press coverage ([Pulse 2](https://pulse2.com/give-interactive-launches-fund-of-funds-platform-for-daf-sponsors-and-private-foundations/)) [S] |

### 5.3 Answer

1. **Adoption.** No vendor besides NPact has a public clause that specifically bans third-party products from initiating grants or payments, or that requires direct-login-only access. The others restrict third parties through:
   - authorized-user definitions (Foundant, Blackbaud, Bonterra);
   - third-party-benefit or service-bureau bans (iPhi, Foundant);
   - competitive-use bans (iPhi, Foundant, Bonterra, Foundation Source);
   - anti-automation clauses at site or AI level (TIFIN, Givinga, Foundation Source, Blackbaud AI).

   [I] A sponsor-designated agent with its own named user seat is arguably allowed under Foundant, Blackbaud and Bonterra. It is arguably barred under iPhi §3.4(c) and NPact §2.4.
2. **Negotiability.** No vendor describes these clauses as negotiable. Structurally, all of them can be amended:
   - NPact, Blackbaud, Bonterra and Ren RAC need an express, section-referenced override in the SOW or Order Form.
   - At Foundant and iPhi, the Order Form or SOW generally prevails.

   Whether any executed contract has used that route remains P-CON-01.
3. **Trend watch.** NPact (2025-08), Bonterra (2026-07) and Blackbaud AI Terms (2026-06) are all recent revisions. Only NPact moved toward an explicit grant-initiation ban. Proposal P-PAY-07 sets up dated monitoring.

---

## 6. Implications for repo conclusions

- **Paper checks persist from habit on both sides** ([industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md) §6.1). This is supported more strongly, with one change. The largest sponsor publicly backed off a hard cutoff: it now says "not currently require", and the deadline was reportedly extended. That points to nonprofit enrollment, including board policy and the ACH queue, as a binding constraint, not a soft one. This is consistent with the "Reconsider if … EFT enrollment is blocked by an external constraint" trigger, though that trigger is not yet met.
- **The interoperability map should separate three channels:**
  1. sponsor-sanctioned API initiation (OAuth or Donor Accounts): documented, no named live sponsor;
  2. donor-credential initiation (DAFpay compatible flow): where the volume is;
  3. sponsor-run initiation widgets (DAF Direct).

  NPact §2.4 is aimed squarely at channel 2.
- **Cycle-time measurement remains thin.** The only distributions are vendor-published (Chariot, Charityvest, AssetMark). P-INF-04, a time-and-motion study, still applies. P-PAY-03 adds a route to void and refund counts in audited financials.

---

## 7. Source register

| # | Source | Type | Date (as shown) | Retrieved | URL |
|---|---|---|---|---|---|
| 1 | Fidelity Charitable nonprofit landing page | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/nonprofits.html |
| 2 | Fidelity Charitable nonprofit overview | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/nonprofits/overview.shtml |
| 3 | Fidelity Charitable nonprofit FAQ | sponsor | live (©1998-2026) | 2026-11-14 | https://www.fidelitycharitable.org/nonprofits/faqs.html |
| 4 | Fidelity Charitable EFT page | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/nonprofits/eft.html |
| 5 | Fidelity Charitable supported charities (donor) | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/giving-account/supported-charities.html |
| 6 | Fidelity Charitable charity-address FAQ | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/faqs/all/different-charity-addresses.html |
| 7 | Fidelity Charitable returned-grant FAQ | sponsor | live | 2026-11-14 | https://fidelitycharitable.org/faqs/all/returned-grant.html |
| 8 | Fidelity Charitable lost-grant-check FAQ | sponsor | live | 2026-11-14 | https://fidelitycharitable.org/faqs/all/lost-grant-check.html |
| 9 | Fidelity Charitable grant processing timeline | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html |
| 10 | Fidelity Charitable grant-delivery FAQ | sponsor | 404 on retrieval; search-index text only | 2026-11-14 | https://www.fidelitycharitable.org/help/grant-delivery-faq.html |
| 11 | Fidelity Charitable Program Guidelines | sponsor | PDF created 2026-09-11 | 2026-11-14 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf |
| 12 | Fidelity Charitable 2026 Giving Report | sponsor | PDF created 2026-04-21 | 2026-11-14 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf |
| 13 | Chariot, Top 8 Takeaways (Fidelity 2026 report) | vendor blog | "Mar 24" (© 2026) | 2026-11-14 | https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report |
| 14 | Chariot, "Not Enrolled for E-Pay" | vendor blog | "May 7" (© 2026) | 2026-11-14 | https://www.givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors |
| 15 | Bogleheads t=464478 | forum | 2025-12 to 2026-10 | blocked (402/403); search extracts | https://www.bogleheads.org/forum/viewtopic.php?t=464478 |
| 16 | Bogleheads p=8701653 (page 5) | forum | 2026 | blocked; search extract | https://www.bogleheads.org/forum/viewtopic.php?p=8701653 |
| 17 | DAFgiving360 2024 Program Policies (third-party-hosted copy) | sponsor | PDF modified 2024-12-12 | 2026-11-14 | https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf |
| 18 | Vanguard Charitable nonprofit page | sponsor | live | 2026-11-14 | https://www.vanguardcharitable.org/nonprofit-organizations |
| 19 | Vanguard Charitable PayPal launch release | press release | 2023-09-20 | 2026-11-14 | https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html |
| 20 | NPT Grant Payments flyer | sponsor | 2022-08 | 2026-11-14 | https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf |
| 21 | NPT Guide to your DAF | sponsor | PDF dated 2026-10-15 | 2026-11-14 | https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf |
| 22 | Daffy, What is Chariot Disbursements | sponsor | 2026-08-06 | 2026-11-14 | https://help.daffy.org/en/articles/15604949-what-is-chariot-disbursements |
| 23 | Daffy, How does Daffy send donations | sponsor | live | 2026-11-14 | https://help.daffy.org/en/articles/9122843-how-does-daffy-send-donations-to-charity |
| 24 | Daffy, charity didn't receive donation | sponsor | live | 2026-11-14 | https://help.daffy.org/en/articles/9122847-what-if-a-charity-doesn-t-receive-my-donation |
| 25 | Chariot, Getting to know Daffy | vendor blog | "Jul 21" (© 2026) | 2026-11-14 | https://givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner |
| 26 | Chariot, Getting to know Charityvest | vendor blog | 2026-07-29 | 2026-11-14 | https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner |
| 27 | Charityvest Guide, Grant to Charity | sponsor | live | 2026-11-14 | https://guide.charityvest.org/for-donors/getting-started/grants-to-charity.md |
| 28 | Charityvest Guide, Check Grant Status | sponsor | live | 2026-11-14 | https://guide.charityvest.org/for-donors/getting-started/check-grant-status.md |
| 29 | AssetMark help, how grant payments are delivered | sponsor | "updated this week" | 2026-11-14 | https://intercom.help/assetmark-help-center/en/articles/13931838-how-grant-payments-are-delivered-electronic-check |
| 30 | BlueGive granting FAQs | sponsor | "updated this week" | 2026-11-14 | https://intercom.help/bluegive-help-center/en/articles/10597826-granting-faqs |
| 31 | Ren help, grant check reissue | administrator | 2025-12-10 | 2026-11-14 | https://intercom.help/rengiving/en/articles/13123383-what-should-i-do-if-i-have-issues-with-receiving-a-grant-check-or-need-to-request-a-reissue |
| 32 | NPact docs, double-cashed reissue | vendor docs | n/a | search index | https://npact.document360.io/fims-and-donorcentral/docs/how-do-i-handle-a-situation-where-the-grantee-cashed-the-original-check-and-the-reissue |
| 33 | NPact docs, reissue changes grant date | vendor docs | n/a | search index | https://npact.document360.io/fims-and-donorcentral/docs/re-issuing-a-grant-check-changes-the-grant-date-shown-in-donorcentral |
| 34 | Chariot, All Checks No Balance | vendor study | "Jan 20" (© 2026) | 2026-11-14 | https://givechariot.com/resources/insights/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits |
| 35 | PayPal, How Philanthropic Dollars Move | vendor survey | 2023 | 2026-11-14 | https://filecache.mediaroom.com/mr5mr_paypal/186631/PP_2023_GrantPayments.pdf |
| 36 | Chariot help, DAFpay Network | vendor | live | 2026-11-14 | https://help.givechariot.com/dafpay/dafpay-network.md |
| 37 | Chariot help, Disbursements tracking and delivery | vendor | live | 2026-11-14 | https://help.givechariot.com/disbursements/for-grantmakers/tracking-and-delivery.md |
| 38 | Chariot help, Disbursements FAQs | vendor | live | 2026-11-14 | https://help.givechariot.com/getting-started/disbursements-faqs.md |
| 39 | Chariot help, Disbursements for Nonprofits (partner list) | vendor | live | 2026-11-14 | https://help.givechariot.com/disbursements/for-nonprofits.md |
| 40 | Chariot help, DAFpay Compatible Providers | vendor | "last updated 1 month ago" | 2026-11-14 | https://help.givechariot.com/dafpay/editor/supported-providers |
| 41 | Chariot docs, DAFpay OAuth overview | vendor docs | v2026-04-01 | 2026-11-14 | https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/overview.md |
| 42 | Chariot docs, DAFpay OAuth API endpoints | vendor docs | v2026-04-01 | 2026-11-14 | https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md |
| 43 | Chariot docs, DAFpay overview | vendor docs | v2026-04-01 | 2026-11-14 | https://docs.givechariot.com/v2026-04-01/guides/dafpay/overview.md |
| 44 | Chariot docs, List DAFs API | vendor docs | v2026-04-01 | 2026-11-14 | https://docs.givechariot.com/v2026-04-01/api/donor-advised-funds/list.md |
| 45 | Chariot changelog, Donor Accounts beta | vendor docs | 2026-05-08 | 2026-11-14 | https://docs.givechariot.com/changelog/2026/5/8 |
| 46 | Chariot DAFpay product page | vendor | live | 2026-11-14 | https://www.givechariot.com/dafpay |
| 47 | Business Wire, Chariot gift processing launch | press release | 2026-01-28 | 403; search extract | https://www.businesswire.com/news/home/20260128542200/en |
| 48 | FinTech Futures copy of launch release | press release copy | 2026-01 | search extract | https://www.fintechfutures.com/press-releases/chariot-launches-first-gift-processing-platform-for-nonprofits |
| 49 | The Giving Block, Chariot integration | integrator | undated | 2026-11-14 | https://thegivingblock.com/integrations/chariot/ |
| 50 | Givebutter help, DAFpay | integrator | undated | search extract | https://help.givebutter.com/en/articles/6764835-how-to-use-givebutter-s-dafpay-donation-method |
| 51 | PMC, Donor Advised Funds | nonprofit | undated | search extract | https://www.pmc.org/ways-to-give/donor-advised-funds |
| 52 | Overflow, DAF Giving FAQs | integrator | undated | search extract | https://overflowapp.zendesk.com/hc/en-us/articles/36109985992077-DAF-Giving-FAQs |
| 53 | Inequality.org DAFpay critique | commentary | c.2024 | repo | https://inequality.org/article/new-donor-advised-fund-tech-raises-old-concerns/ |
| 54 | NPact SaaS Standard Terms | vendor contract | last updated 2025-08-26 | 2026-11-14 | https://npact.com/software-as-a-service-license-and-services-standard-terms/ |
| 55 | Ren iPhi Platform MSA | vendor contract | final draft 2023-06-20 v2 | 2026-11-14 | https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20v2.docx |
| 56 | Ren RAC MSA | vendor contract | v1 | 2026-11-14 | https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf |
| 57 | Ren iPhi Product Descriptions | vendor | 2023-09 | search extract | https://www.reninc.com/wp-content/uploads/2023/09/Ren-iPhi-Product-Descriptions-v1.pdf |
| 58 | Foundant MSA | vendor contract | v012024 | 2026-11-14 | https://info.foundant.com/rs/356-VHW-319/images/FT%20MSA%20-%20Final%20-%20v012024.pdf |
| 59 | Foundant legal page | vendor | live | 2026-11-14 | https://www.foundant.com/legal/ |
| 60 | Blackbaud Solutions Agreement | vendor contract | footer March 2026 | 2026-11-14 | https://www.blackbaud.com/wp-content/uploads/2025/01/blackbaud-solutions-agreement.pdf |
| 61 | Blackbaud Acceptable Use Policy | vendor | 2025-02 upload | 2026-11-14 | https://www.blackbaud.com/wp-content/uploads/2025/02/acceptable-use-policy.pdf |
| 62 | Blackbaud AI Terms 2026 | vendor | June 2026 | 2026-11-14 | https://www.blackbaud.com/wp-content/uploads/2026/06/blackbaud-ai-terms-2026.pdf |
| 63 | Blackbaud terms index | vendor | live | 2026-11-14 | https://www.blackbaud.com/terms-and-conditions |
| 64 | Bonterra Subscription and Services Agreement | vendor contract | 2026-07-13 | 2026-11-14 | https://www.bonterratech.com/wp-content/uploads/2026/07/bonterra-subscription-and-services-agreement-online_071326.pdf |
| 65 | Foundation Source Terms of Use | vendor site terms | last updated 2026-01-12 | 2026-11-14 | https://foundationsource.com/terms-of-use |
| 66 | TIFIN Terms | vendor terms | 2025-02-19 | repo | https://intercom.help/give-ria/en/articles/10092486-terms-of-use |
| 67 | Givinga terms | vendor site terms | undated | 2026-11-14 | https://www.givinga.com/terms-and-conditions |
| 68 | Pulse 2 on Give Interactive | press | 2026-07 | search extract | https://pulse2.com/give-interactive-launches-fund-of-funds-platform-for-daf-sponsors-and-private-foundations/ |
