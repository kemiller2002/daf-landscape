# Batch 36C: donor anonymity through DAF rails (P-NPP-03), custodian feeds for DAF accounts (P-B32C-02), Candid Charity Check PDF v2 time stamp (P-B30A-03), DAFpay stacking fees (P-AGF-03), DAFpay fee mix (P-AGF-01), DAFgiving360 2026 documents (P-ADV-03, P-ADV-05, P-TRM-06)

**Date:** 2026-11-15. **Queue items:** P-NPP-03, P-B32C-02, P-B30A-03, P-AGF-03, P-AGF-01, P-ADV-03, P-ADV-05, P-TRM-06 (`data/mission-2026-11-14/research-priority-queue.csv`).

**Status: public sources only.**
- I logged in nowhere, submitted no forms and contacted no one. I called no APIs. I read public documentation, including Chariot's and Candid's machine-readable doc indexes (`llms.txt`, `.md` page versions).
- I read robots.txt on each host before scripted reads. Hosts whose robots.txt returned 403 were not fetched: dafgiving360.org, schwabcharitable.org, docs.candid.org and candid.org. Exception: www.schwab.com's robots.txt returned an access-denied page rather than a file. I fetched three public legal pages there once each, as earlier batches did, and nothing else.
- I respected the crawl delays at altruist.com and bridgeft.com (no altruist.com pages fetched) and on the Intercom help centres.
- A practitioner forum post is quoted without the authors' names or contact details.

**Recency rule:** every current-state claim rests on 2021+ evidence. The oldest item used is a 2022-08-25 NPT article on PayPal Grant Payments.

**Read first and built on**, with their governing corrections:
- `queue-batch33-voids-exports-rails.md` (wave 18);
- `queue-all-in-cost-dafpay-access.md` (wave 10 and the adviser-fee update);
- `queue-batch30-legal-circulars.md` (wave 15);
- `queue-batch32-feeds-owners-codebases.md` (wave 17);
- also `queue-nonprofit-side-panel.md`, `queue-sponsor-terms-data-clauses.md`, `nonprofit-daf-receipt-fees-2026.csv` and `red-team-wave2a-ai-and-entrant.md` (Endaoment's custodian line is marketing copy).

**Evidence labels:**
- **[F]:** first-party (the sponsor's, vendor's or platform's own page, PDF or docs).
- **[P]:** practitioner statement in a public forum.
- **[S]:** secondary source read through a fetch tool.
- **[R]:** search-index summary of a page I could not read first-hand.
- **[I]:** my inference.

**Quote check:** quotes are verbatim and 40 words or fewer. A script checked every CSV quote against the fetched text. The exceptions are three rows carried from the repo (A13–A15, marked "F (repo)") and two pricing-card strings (S11, S12), which are split across HTML elements and were checked by eye in the page's JSON. The Chronicle figures (A16) are paraphrased, not quoted.

**Outputs:**
- [`data/mission-2026-11-14/anonymity-data-flow-2026.csv`](../../data/mission-2026-11-14/anonymity-data-flow-2026.csv): 16 rows covering DAFpay, Chariot Disbursements, Chariot managed sources, PayPal Grant Payments, PPGF and four sponsors' letters.
- [`data/mission-2026-11-14/dafpay-stacking-fees-2026.csv`](../../data/mission-2026-11-14/dafpay-stacking-fees-2026.csv): 14 rows comparing DAFpay and card cost per $1,000 by platform and plan.
- [`data/mission-2026-11-14/queue-proposals-batch36c.csv`](../../data/mission-2026-11-14/queue-proposals-batch36c.csv): P-B36C-01 to P-B36C-03.

---

## 0. Answers

| Item | Answer | Confidence |
|---|---|---|
| **P-NPP-03** | **DAFpay runs two donor-data paths, and the anonymity flag governs only one of them.**<br>- Chariot's v2026-04-01 sponsor spec sends `anonymous` on Create Grant: "`anonymous: true` means the donor's name and contact details are withheld from the nonprofit, per your standard anonymity handling" [F]. That governs the **sponsor's** letter or remittance.<br>- The same spec requires a "Get Current Donor" call. It returns name, email, phone and address, which Chariot "uses … to populate the donor's DAFpay profile" [F].<br>- The sponsor must print the Chariot Grant Request ID on "the grant letter / remittance advice sent to the nonprofit" [F]. No exception for anonymous grants is stated.<br>- The nonprofit-facing Grant object and export have donor-name, email, phone and address fields but **no anonymity field** [F]. No public doc says what the nonprofit sees when `anonymous` is true. The old Chariot article on anonymous DAFpay gifts now 404s.<br>- **Chariot Disbursements:** every donor field in the grantmaker upload is optional, so anonymity means leaving fields out [F/I].<br>- **PayPal Grant Payments:** passes only information "selected by the donor to be shared" [F, 2022].<br>- **PPGF:** shows donor details "except when donors choose to give anonymously" [F, 2025].<br>- **DAFgiving360 (2024):** three letter options, including "Anonymously with an explanatory note" [F]. | High on the documented fields; the outcome for anonymous DAFpay gifts is unknown (P-B36C-01) |
| **P-B32C-02** | **Partly answered: Schwab's custodial feed carries DAF registration codes.**<br>BridgeFT's public reference passes through Schwab registration codes **DASCG "Charity Account (Donor Advised Account)"**, **DASPL "Charity Account (Schwab Private Label)"** and DASPI, plus account type **CHGFT "CHARITABLE GIFT"** [F, page updated 2025-10-06].<br>Its Fidelity (NFS) and Pershing tables have **no DAF code**. Pershing has only generic exempt and nonprofit codes.<br>Which sponsor programs use the Schwab codes is not stated. No public Altruist, Orion, Black Diamond or Addepar document says DAF accounts flow through or how they are classified.<br>Endaoment says "The DAF follows the assets, whether they sit at Altruist, Schwab, Fidelity or BNY" [F, marketing per red-team V2A-18]. | Medium-high on the codes; low on downstream mapping |
| **P-B30A-03** | **Not resolved for 2026 output, but the "v2 sample" is the April 2025 PDF.**<br>Candid's changelog announcing PDF v2 (2025-04-18) embeds the same example file that batch 30 read (generated 2025-04-16). That file prints a date and no time.<br>The changelog calls v2 "a date-stamped document". Candid's guide pages (updated 2026-09-07) promise a "date and timestamped" PDF.<br>The FAQ still cites Rev. Proc. 2011-33 (read 2026-11-15).<br>No 2026-generated Charity Check PDF was found in public files. docs.candid.org blocks robots, so the sample was not re-fetched. | Medium |
| **P-AGF-03** | **Yes, on most platforms read, if the donor does not cover the fee.** Per $1,000 gift:<br>- **Bloomerang:** DAFpay $48.50 vs card $39.80, so DAFpay costs **$8.70 more**; DAFpay is $1.30 cheaper than AMEX.<br>- **Funraise:** DAFpay costs about **$9.70 more** than card, assuming Stripe's standard card rate (DAFpay $39.00).<br>- **BetterWorld** (free plan): **$9.70 more** (DAFpay $39.00).<br>- **Donorbox:** DAFpay $45.00 vs card $38.30–$39.80 with Stripe's nonprofit rate, so **$5.20–$6.70 more**. It is $1.80 cheaper only at Stripe's standard rate.<br>- **Givebutter** (tips on, the default): **$29 more**, because card costs the nonprofit nothing and tips are barred on DAFpay.<br>DAFpay is cheaper only against AMEX, Givebutter with tips off, or a high third-party card rate.<br>**Off switch:** Bloomerang turns DAFpay on by default and allows per-form opt-out [F]. No data on how many nonprofits disable it was found. A 2025 forum thread shows fee hesitancy [P]. | High on published prices; card-side assumptions flagged per row |
| **P-AGF-01** | **One first-party figure found: "80%".** Chariot's help page for DAF sponsors says annual subscriptions, with "no per transaction fees generated by DAFpay use", have "made up 80% of DAFpay usage in the past year" [F, undated].<br>The period and the metric (dollars or gifts) are not stated. It conflicts with the public price "$199/mo + 2.9% fee per donation" for DAFpay Components.<br>No public split of the remaining ~20% between nonprofit-paid, donor-covered and platform-absorbed fees was found.<br>Chariot's Grant object carries `feeDetail.contributions[].feeType` (chariot / daf / fundraising_application), so the split exists in Chariot's data. It is not public [F/I]. | Low-medium (one undated vendor claim) |
| **P-ADV-03 / P-ADV-05** | **Blocked.** dafgiving360.org and the alternative host www.schwabcharitable.org (found as `/node/4831` in search) both return 403 to robots.txt and pages. No third-party copy of the 2026 Program Policies or a Q3 2026 Quarterly Performance Report was found.<br>Search-index summaries [R] show a Q2 2026 report (period ending 2026-06-30) and policy pages dated 2026-02-17, 2026-08-07 and 2026-10-22. The "EFT" wording seen in search concerns contributions, not grants.<br>Chariot still says Schwab gifts arrive "the same way as before" [F]. | Blocked |
| **P-TRM-06** | **Answered: the Schwab Online Services Agreement is public.** `schwab.com/legal/terms` is the SOSA itself ("Schwab Online Services Agreement (the 'SOSA')"), not just site terms.<br>On credentials it says: "Pursuant to the terms of the Schwab Security Guarantee, if you do share this information with anyone we'll consider their activities to have been authorized by you."<br>It caps Schwab's aggregate liability at $100.<br>DAFgiving360's 2024 policies bind Client Center users to "Schwab's Online Services Agreement as currently in effect and as amended from time to time" [F].<br>Whether the Security Guarantee itself covers DAFgiving360 accounts was not checked. | High on the OSA text and its incorporation (2024 policies); unknown on Guarantee scope |

---

## 1. P-NPP-03: what reaches the nonprofit when a donor chooses anonymity or "fund name only"

### 1.1 DAFpay (Chariot), from the v2026-04-01 developer docs [F]

| Step | What the docs say | Source |
|---|---|---|
| Sponsor-side grant | Create Grant body includes `"anonymous": false`. "`anonymous: true` means the donor's name and contact details are withheld from the nonprofit, per your standard anonymity handling." No fund-name-only value | [OAuth API endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md) |
| Donor profile pulled by Chariot | "Get Current Donor" is **required**. It returns first and last name, email, phone and address. Chariot "uses it to populate the donor's DAFpay profile" | same |
| Sponsor remittance | "The Chariot Grant Request ID passed in `note` must appear on the grant letter / remittance advice sent to the nonprofit." | same |
| Nonprofit record | "Donor and gift data are shared with your organization in real time" The Grant object has optional `firstName`, `lastName`, `phone`, `email` and `address` fields, and no anonymity field | [DAFpay Overview](https://help.givechariot.com/dafpay/editor.md); [Get Grant](https://docs.givechariot.com/v2026-04-01/api/grants/get.md) |
| Unintegrated sponsors | "the modal can collect the donation amount and donor information so the nonprofit can be notified in real time". The donor is then asked to put the tracking ID in the sponsor grant note | [DAFpay FAQ](https://docs.givechariot.com/v2026-04-01/guides/dafpay/integrating-dafpay/faq.md) |
| Export | Donor Fund Name, Full/First/Last Name, Email, Phone and Address columns. No anonymity column | [Donation Fields](https://help.givechariot.com/getting-started/donation-fields.md) |
| Chariot's stated data policy | Chariot "stores items that a donor user submits to be shared with the receiving nonprofit" | [help centre: Data Privacy](https://help.givechariot.com/llms-full.txt) |

**Reading [I]:**
- **The flag binds the sponsor.** It tells the sponsor how to handle its own letter. Nothing read says Chariot suppresses the donor profile or modal data in the nonprofit's dashboard when the flag is true.
- **The ID links back to the donor.** The Grant Request ID must appear on the sponsor's remittance, so even an anonymous sponsor payment carries a key back to the DAFpay record. That record holds whatever donor data Chariot shared.
- **Fund-name-only has no DAFpay equivalent.** The spec has a two-state flag. "Fund name only" would depend on the sponsor's own letter options.
- **The anonymous case is undocumented.** It remains the open question (P-B36C-01).
- **Old evidence is gone.** Search summaries of the retired article [R] said anonymity followed the nonprofit's form settings and that every gift needs an email. These could not be read first-hand.

**Other DAFpay-docs points:**
- The FAQ recommends DAFpay as an "Express Checkout" option that can "automatically gather crucial donor information, such as names, email addresses, physical addresses".
- The same FAQ describes "Intelligent Donation Recommendations, taking into account factors like the donor's account balance".
- Chariot's help centre also says it does not store "account balance & donation history". Displaying a balance and not storing it are compatible, but the two statements should be read together (help centre, live 2026-11-15) [F/I].

### 1.2 Chariot Disbursements (sponsor pays through Chariot) [F]

- **Required fields:** the grantmaker upload requires only `grant_id`, `amount` and `ein`. `fund_name`, `first_name`, `last_name`, `email`, `phone`, address, `purpose` and `note` are all optional ([Create a Disbursement](https://help.givechariot.com/disbursements/for-grantmakers/create-a-disbursement.md)).
- **What Chariot passes on:** Chariot says it preserves "the donor, fund, purpose, designation, note, and other remittance details the nonprofit needs" ([For Grantmakers](https://help.givechariot.com/disbursements/for-grantmakers.md)).
- **Checks:** a mailed check carries a grantmaker-branded letter with "Grant details supplied with the disbursement" ([Customize Your Grant Letter](https://help.givechariot.com/disbursements/for-grantmakers/customize-your-grant-letter.md)).
- **Reading [I]:** anonymity and fund-name-only are expressed by **omitting fields**. There is no flag, so a nonprofit cannot tell an anonymous grant from a grant whose sponsor sends sparse data.
- **Managed sources:** for sources Chariot manages (paid plan: Fidelity Charitable, PayPal Grant Payments, Ren and others), the donor data is whatever the sponsor's own feed carries ([Sources](https://help.givechariot.com/getting-started/sources.md)).

### 1.3 PayPal rails and sponsor letters

- **PayPal Grant Payments (NPT, 2022-08-25):** "all personally identifiable information selected by the donor to be shared with the nonprofit is securely transmitted". Staff "can export details for their fundraising records" ([NPT](https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/)) [F]. PayPal's FAQ4654 returned 403.
- **PayPal Giving Fund (policy 2025-01-01):** enrolled charities see donations "including donor details (except when donors choose to give anonymously)" ([policy PDF](https://www.paypalobjects.com/marketing/web25/us/paypal-giving-fund/policy-updates/ppgf-us-delivery-01012025.pdf)) [F].
- **DAFgiving360 (2024 policies):** grants are paid "by issuing checks". The account holder chooses one of:
  - name, special account name and/or address;
  - name or account name only;
  - "Anonymously with an explanatory note".
  
  Name and contact are not released "without the account holder's explicit consent" ([2024 Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf)) [F].
- **Fidelity, Vanguard and NPT:** unchanged from repo; see CSV rows A13–A15.
- **Industry baseline [S]:** a DAF Research Collaborative survey of more than 120 sponsors, reported by the Chronicle of Philanthropy (2024-10-08), found that 60% default to not giving receiving charities donors' contact information, and 35% send only the fund name ([Chronicle](https://www.philanthropy.com/article/why-your-daf-donor-may-not-be-anonymous-after-all)).

**Reading [I]:**
- **Where anonymity sits.** On sponsor-native rails it is a field on the sponsor's letter. On DAFpay the donor's identity is collected before the grant reaches the sponsor.
- **Implication for Quadrant A1–A4.** DAFpay's data advantage for nonprofits ("fewer anonymous gifts", Chariot help centre [F]) is the same mechanism that can bypass sponsor-default anonymity.

---

## 2. P-B32C-02: do custodian feeds carry sponsor-owned DAF accounts?

| Source | Finding | Label |
|---|---|---|
| [BridgeFT: Source Account and Registration Types](https://docs.bridgeft.com/docs/source-account-and-registration-types.md) (updated 2025-10-06) | BridgeFT passes the "original custodial account and registration type information" through. **Schwab:** account type CHGFT "CHARITABLE GIFT"; registration types DASCG "Charity Account (Donor Advised Account)", DASPI "Charity Account with Income", DASPL "Charity Account (Schwab Private Label)", CHNPR "Charity Non-Profit". **Fidelity (NFS):** no charitable or DAF code. **Pershing:** EXMP "Exempt Organizations", NPRO "Non-Profit Organization", IANP; no DAF code | F |
| [Endaoment institutions page](https://endaoment.org/institutions) | "The DAF follows the assets, whether they sit at Altruist, Schwab, Fidelity or BNY." The DAF "becomes a native account type on your platform under your brand, your reporting, your fee line." Partner API tiers: Growth $0–25k setup and $2–5k/month; Strategic $25–100k and $5–15k/month | F (vendor claim; red-team V2A-18: marketing, not proof of custodial agreements) |
| Altruist (InvestmentNews 2026-10-06, repo) | Endaoment is "customer of record". Advisers "see the DAF next to a client's other holdings". Altruist feeds Orion and Black Diamond; DAF flow-through not stated | F (repo) / U |
| Search: Altruist, Orion, Black Diamond, Addepar DAF classification | Nothing found | U |

**Reading [I]:**
- **Schwab's feed has DAF codes.** It identifies at least two charitable/DAF registration types, one of them explicitly "Donor Advised Account". A reporting system receiving Schwab data through BridgeFT therefore gets a machine-readable DAF marker.
- **Fidelity's and Pershing's feeds, as documented by BridgeFT, do not.**
- **What this does and does not support.** It supports giving a pending A3 Y1/Y2 credit for Schwab-custodied DAF accounts (custodial-feed visibility). It does **not** show which programs (DAFgiving360, Endaoment-at-Schwab, Foundation Source) use these codes. "Schwab Private Label" suggests sponsor-branded programs custodied at Schwab, but this is unconfirmed (P-B36C-02).

---

## 3. P-B30A-03: Candid Charity Check PDF v2, time as well as date

- **Changelog** ([04.18.2025 – Charity Check PDF API v2 now available](https://developer.candid.org/changelog/charity-check-pdf-api-v2-now-available.md)):
  - v2 "returns charity verification information in a date-stamped document that can be archived for due diligence records";
  - it adds California AG and FTB status;
  - its "Sample Charity Check PDF v2 report" embeds `docs.candid.org/files/guidestar-charity-check-pdf-api-example-response-13-1837418.pdf`. This is the file batch 30 read (generated 2025-04-16; date only, no time; cites Rev. Proc. 2011-33) [F].
- **Guide pages (updated 2026-09-07):**
  - "Download a date and timestamped charity check PDF document to archive for due diligence" ([verification guide](https://developer.candid.org/docs/verification-using-charity-check.md));
  - "download and save a PDF copy of the charity check report, which includes a timestamp" ([get started](https://developer.candid.org/reference/get-started-with-charity-check.md)) [F].
- **FAQ (read 2026-11-15):** still cites "IRS Revenue Procedure 2011-33" ([FAQ](https://developer.candid.org/reference/faqs-charity-check.md)) [F].
- **v2 endpoint reference** (updated 2026-09-07): describes only the byte-stream output. No change note on time stamps ([charitycheckpdf_v2](https://developer.candid.org/reference/charitycheckpdf_v2.md)).
- **Search:** no 2026-generated Charity Check PDF was found in public grant files, board packets or audit workpapers.

**Reading [I]:**
- **Contradiction.** Candid's only published v2 sample prints a date without a time, while its guides promise a "timestamp". Either the 2026 output has changed and the sample is stale, or "timestamp" means the date.
- **Status of the gap.** The §8.01(1)(c) "date and time" gap from batch 30 stands for the sample. It is **unverified for 2026 output**.
- **Practical advice.** A sponsor archiving only the PDF should also keep the JSON `report_date`, which carries a time in GMT.

---

## 4. P-AGF-03: do platform stacking fees make DAFpay dearer than card?

Per $1,000 gift, nonprofit-paid default (donor does not cover). Full detail is in `dafpay-stacking-fees-2026.csv`.

| Platform / condition | DAFpay | Card | DAFpay − card | Source |
|---|---|---|---|---|
| Bloomerang Fundraising, Visa/MC/Discover | 4.85% = **$48.50** | 3.95% + $0.30 = **$39.80** | **+$8.70** | [Bloomerang pricing help](https://help.bloomerang.com/en/articles/12632855-payment-processing-pricing) [F] |
| Bloomerang, AMEX | $48.50 | 4.95% + $0.30 = $49.80 | −$1.30 | same |
| Bloomerang, third-party processor (Stripe 2.9% + $0.30 assumed) | $48.50 | 1.95% + processor = $48.80 | −$0.30 | same + assumption |
| Donorbox Pro, Stripe nonprofit rate | 4.5% = $45.00 | 1.75% + 2.2% + $0.30 = $39.80 | +$5.20 | [Donorbox DAF page](https://donorbox.org/explore/donor-advised-fund-donations); [pricing](https://donorbox.org/pricing) [F] |
| Donorbox Pro, Stripe standard rate | $45.00 | 1.75% + 2.9% + $0.30 = $46.80 | −$1.80 | same |
| Donorbox Premium, Stripe nonprofit rate | $45.00 | 1.6% + 2.2% + $0.30 = $38.30 | +$6.70 | same |
| Funraise (no donor cover) | 3.9% = $39.00 | processor only (Stripe 2.9% + $0.30 assumed) = $29.30 | +$9.70 | [Funraise DAFpay help](https://help.funraise.io/en/articles/12142901-accept-daf-donations-with-dafpay); [Funraise payments](https://funraise.org/funraise-payments) [F] |
| BetterWorld free plan | 3.9% = $39.00 | 2.9% + $0.30 = $29.30 | +$9.70 | [BetterWorld fees help](https://help.betterworld.org/en/articles/8558015-what-are-the-processing-fees-and-who-covers-them); [pricing](https://betterworld.org/pricing/) [F] |
| Givebutter, tips on (default) | 2.9% = $29.00 | $0 to nonprofit | +$29.00 | [Givebutter DAFpay help](https://help.givebutter.com/en/articles/6764835-how-to-use-givebutter-s-dafpay-donation-method); [pricing](https://givebutter.com/pricing) [F] |
| Givebutter, tips off | $29.00 (if the 3% platform fee does not apply) | 3% + 2.9% + $0.30 = $59.30 | −$30.30 | same |
| Stripe card benchmark | — | $29.30 | — | repo F20 |

**Findings:**
1. **Card is cheaper on most platforms.** With fees not covered by the donor, DAFpay costs more than card on 4 of 5 platforms at their default or most common settings: Bloomerang, Donorbox at Stripe's nonprofit rate, Funraise, BetterWorld and Givebutter with tips. The premium ranges from $5.20 to $29 per $1,000.
2. **Donor-cover rules differ by rail.**
   - **Funraise:** charges no card platform fee unless the donor covers it, but its DAFpay 1% is "always" charged and "DAFpay is not eligible for Donors Cover Fees" (repo F07).
   - **Givebutter:** card costs the nonprofit nothing when tips are on, while DAFpay's 2.9% falls on the nonprofit and "Donors cannot cover processing fees" (repo F03).
   - **Tips:** Chariot's integration FAQ bars them on DAFpay: "you must suppress the option to add a tip" ([Chariot docs FAQ](https://docs.givechariot.com/v2026-04-01/guides/dafpay/integrating-dafpay/faq.md)) [F].
3. **Chariot's own pricing page acknowledges stacking:** "Free to activate + 2.9% fee per donation. Additional fees may apply depending on your fundraising platform. Most platforms allow donors to cover fees" ([pricing](https://www.givechariot.com/chariot-pricing)) [F].
   - Its FAQ calls the 2.9% "a 2.9% grant initiation fee for grants initiated with DAFpay, regardless of whether the donation arrives in your Chariot deposit account or not".
   - The same page now lists "1% On donations from sources you link" (additional sources) and Mailroom at "$50/mo + $1.50 per mail item" [F]. These are new public prices not in `nonprofit-daf-receipt-fees-2026.csv`.
4. **Evidence on switching DAFpay off:**
   - Bloomerang: "on by default for eligible forms, and you can turn it off for any individual form in Donation Settings" ([blog](https://bloomerang.com/blog/dafpay)) [F].
   - Chariot help still says platforms "activate DAFpay automatically for eligible nonprofits" [F].
   - No platform changelog, forum post or support statistic on nonprofits disabling DAFpay after the 2026-10-14 terms was found.
   - The closest practitioner evidence is an AASP FundSvcs thread (2025-10) ([thread](https://aasp.connectedcommunity.org/discussion/dafpay-via-givecampus)) [P]:
     - a university gift-processing lead feared that DAF gifts "we already get without any processing fees" would move to DAFpay;
     - an advancement-services lead noted GiveCampus charges DAFpay "through your existing GiveCampus fee structure. So, for a large DAF grant, that could sting."
   
   This is pre-terms and anecdotal.

**Reading [I]:**
- **Cost per dollar.** On a fee-per-dollar basis, DAFpay is priced as a premium payment method. A DAF gift that would otherwise arrive by sponsor ACH or check costs the nonprofit nothing on those rails. That makes the relevant comparison for an existing DAF donor "DAFpay vs free", not "DAFpay vs card". The forum post is exactly this concern.
- **The case for DAFpay rests on gift size.** Chariot's case rests on larger gifts and data (888% average gift-size increase, Chariot 2025 report, help centre [F, vendor claim]), not on fees.

---

## 5. P-AGF-01: share of DAFpay volume bearing the default 2.9%

- **Chariot's statement** ([OAuth For DAF Sponsors](https://help.givechariot.com/dafpay/oauth-for-daf-sponsors.md), help centre, undated, live 2026-11-15) [F]:
  > "An annual Chariot subscription, which includes holistic use of the Chariot platform beyond just DAFpay and a significant amount of free DAFpay volume. For these organizations, there are no per transaction fees generated by DAFpay use. This is most common for large nonprofits and has made up 80% of DAFpay usage in the past year."
  
  The alternative route is platform access where "nonprofits pay transaction fees in-line with the other payment methods on their forms (typically 2.9%)".
- **Tension with public prices [F]:**
  - The pricing page lists DAFpay Components at "$199/mo + 2.9% fee per donation".
  - Chariot's DAFpay Security page says subscription plans "come with a set limit of included DAFpay volume".
  - Billing help says fees "above your plan's volume limit (such as excess DAFpay volume…)" are billed monthly.
  
  So "subscription" does not always mean fee-free. The 80% presumably refers to higher-tier or enterprise subscriptions, which Fundraise Up describes as having no 2.9% fee (repo F16) [I].
- **What the 80% figure does not say:**
  - the period ("past year" with no date);
  - the metric ("usage", which could mean dollars or gifts);
  - the split of the other ~20% between nonprofit-paid, donor-covered (grossed-up), platform-absorbed (Every.org) and DAFpay Network-netted fees.
- **The split exists in Chariot's data.** The Grant API exposes `feeDetail.total` and `contributions[].feeType` ∈ {chariot, daf, fundraising_application}, and platforms can add `applicationFeeAmount` ([Get Grant](https://docs.givechariot.com/v2026-04-01/api/grants/get.md); [Create Grant](https://docs.givechariot.com/v2026-04-01/api/grants/create.md)) [F]. The data is not public.
- **Searches:** for partner-platform annual reports, Pan-Mass Challenge 990 fee lines and Chariot press statements. They found no further breakdown.

**Reading [I]:**
- **If the claim holds, DAFpay is mainly SaaS revenue.** If the 80% is by dollar volume, DAFpay's revenue model is mainly subscription from large nonprofits. The 2.9% toll then falls mostly on the long tail of small nonprofits reached through platforms, where stacking (§4) also applies.
- **This is a single undated vendor claim.** P-B36C-03 proposes the DAFpay Network's own 990 as a public cross-check.

---

## 6. DAFgiving360 2026 documents (P-ADV-03, P-ADV-05, P-TRM-06)

| Item | Attempted hosts | Result |
|---|---|---|
| Q3 2026 Quarterly Performance Report; pool lineup; admin tiers (P-ADV-03) | dafgiving360.org (robots 403); www.schwabcharitable.org (`/node/4831` per search; robots 403); search for third-party copies | **Blocked.** Search [R] shows a Q2 2026 report (period ending 2026-06-30) and an investment-choices page dated "September 30, 2026" noting that pool funds changed in September 2026. No Q3 report was indexed |
| 2026 Program Policies; ACH/EFT for grants (P-ADV-05) | Same, plus static1.squarespace.com (only the 2024 PDF exists there) and search | **Blocked.** Search [R] shows policy pages dated 2026-02-17, 2026-08-07 and 2026-10-22. The 2026 year-end page's "EFT" wording concerns **contributions**. The 2024 PDF says DAFgiving360 "makes grants by issuing checks". Chariot: Schwab gifts arrive "the same way as before" [F] |
| Schwab OSA (P-TRM-06) | www.schwab.com/legal/terms, /legal/electronic-services-agreement, /legal/third-party-terms (one fetch each) | **Public.** See below |

**P-TRM-06 detail** ([Schwab Online Services Agreement](https://www.schwab.com/legal/terms), © 2026, page code 0225-M8PR) [F]:
- **Title and scope.** The page states: "Use of this site is subject to the terms and conditions contained in the Schwab Online Services Agreement (the 'SOSA') set forth below." The SOSA "applies to Schwab's web sites, other electronic channels as described below, and electronic content, services and tools" and "incorporates by reference the Rules and Guidelines of any Schwab Service for which you register".
- **Credentials.** "we ask you not to share your Registration information (including, but not limited to, passwords, User Names, and screen names) with any other person"; "Pursuant to the terms of the Schwab Security Guarantee, if you do share this information with anyone we'll consider their activities to have been authorized by you."
- **Liability cap.** Aggregate liability of Schwab and its providers is not to "exceed $100 (U.S.)".
- **Conflicts.** "If there is any conflict between (1) the SOSA and (2) your account agreements, then your account agreements will govern." For DAFgiving360, the account agreement is the Program Policies [I].
- **Aggregators.** The Electronic Services Agreement (brokerage) adds that Schwab is not liable for disclosure of access information "to any third party, including, but not limited to, entities that aggregate account information" [F].
- **Incorporation.** The 2024 DAFgiving360 Program Policies bind Client Center users to "Schwab's Online Services Agreement as currently in effect and as amended from time to time" [F]. The 2026 text could not be checked.
- **Reading [I].** The repo's statement that the OSA is "not public" (`queue-sponsor-terms-data-clauses.md` §credential table; `sponsor-terms-clauses-2026.csv` row 31) is superseded: the page already cited there as "site terms" *is* the SOSA. A DAFgiving360 donor who shares credentials with an aggregator or with DAFpay-style credential login is, under the incorporated SOSA, deemed to have authorised that party's acts.

---

## 7. Proposed corrections to repo text (not governing until validated)

1. **`queue-sponsor-terms-data-clauses.md` §credential table, DAFgiving360 row.**
   - **Find:** "Bound by Schwab's Online Services Agreement (not public)."
   - **Replace with:** "Bound by Schwab's Online Services Agreement, which is public at schwab.com/legal/terms (the page titled 'Schwab Online Services Agreement'); it deems credential sharing to authorise the recipient's acts and caps Schwab's liability at $100 (batch 36C)."
2. **`sponsor-terms-clauses-2026.csv` row 31.** Change "schwab.com Terms of Use" to "Schwab Online Services Agreement (schwab.com/legal/terms)". Change the note "Schwab site terms; DAFgiving360 applicability inferred" to "SOSA itself; incorporated by the 2024 DAFgiving360 Program Policies".
3. **`nonprofit-daf-receipt-fees-2026.csv`.** Add Chariot's newly public usage prices: "1% On donations from sources you link" (additional sources, charged on donations received in the Chariot deposit account) and Mailroom "$50/mo + $1.50 per mail item". F14 should note that the pricing page also says "Generally 2.9% fee* on donations facilitated". Source: [pricing](https://www.givechariot.com/chariot-pricing).
4. **`nonprofit-daf-receipt-fees-2026.csv` F06 (Bloomerang).** Add the card comparator from Bloomerang's pricing help: Visa/MC/Discover "3.95% + $0.30", AMEX "4.95% + $0.30"; DAFpay "4.85% Per gift".
5. **`queue-batch32-feeds-owners-codebases.md` §1, custodial route.** Append: "BridgeFT's public registration-type reference shows Schwab passes DAF-specific registration codes (DASCG 'Charity Account (Donor Advised Account)', DASPL 'Charity Account (Schwab Private Label)'); NFS and Pershing tables show none (batch 36C)."

---

## 8. Limits

- No logged-in or API test was run, so no DAFpay record for an anonymous grant was observed.
- The 80% figure is undated and its metric is undefined.
- Card-side rates for Funraise and for Bloomerang's third-party processor route are assumptions (Stripe standard). Donorbox platform fees use the low end of published ranges.
- Stacking comparisons ignore DAFpay's rounding to whole dollars, and the fact that card fees are often donor-covered (BetterWorld: over 95%; Givebutter: 92%).
- BridgeFT codes are custodian labels; their sponsor mapping is unknown.
- DAFgiving360 2026 documents are unreadable from this environment. Search-index captures are [R] only.
- Candid's sample PDF was not re-fetched (docs.candid.org robots 403). Its contents are carried from batch 30.

---

## 9. Source register

| # | Source | Date | Used for | Label |
|---|---|---|---|---|
| 1 | [Chariot docs: OAuth API endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md) | v2026-04-01 | anonymous flag; Get Current Donor; Grant Request ID on letter | F |
| 2 | [Chariot docs: Get Grant](https://docs.givechariot.com/v2026-04-01/api/grants/get.md); [Create Grant](https://docs.givechariot.com/v2026-04-01/api/grants/create.md) | v2026-04-01 | donor fields; feeDetail; applicationFeeAmount | F |
| 3 | [Chariot docs: DAFpay FAQ](https://docs.givechariot.com/v2026-04-01/guides/dafpay/integrating-dafpay/faq.md) | v2026-04-01 | unintegrated grants; donor cover; tips barred; Express Checkout | F |
| 4 | [Chariot help centre (llms-full)](https://help.givechariot.com/llms-full.txt): [Donation Fields](https://help.givechariot.com/getting-started/donation-fields.md), [DAFpay Overview](https://help.givechariot.com/dafpay/editor.md), [For Grantmakers](https://help.givechariot.com/disbursements/for-grantmakers.md), [Create a Disbursement](https://help.givechariot.com/disbursements/for-grantmakers/create-a-disbursement.md), [Customize Your Grant Letter](https://help.givechariot.com/disbursements/for-grantmakers/customize-your-grant-letter.md), [Sources](https://help.givechariot.com/getting-started/sources.md), [DAFpay FAQs](https://help.givechariot.com/dafpay/dafpay-faqs.md), [DAFpay Billing](https://help.givechariot.com/dafpay/dafpay-billing.md), [DAFpay Security](https://help.givechariot.com/dafpay/dafpay-security.md), [OAuth For DAF Sponsors](https://help.givechariot.com/dafpay/oauth-for-daf-sponsors.md) | live 2026-11-15 | data paths; 80% statement; billing | F |
| 5 | [Chariot pricing](https://www.givechariot.com/chariot-pricing) | CMS entries 2025-10 to 2026-09; read 2026-11-15 | 2.9% "grant initiation fee"; Components; 1% sources; Mailroom | F |
| 6 | [NPT: PayPal Grant Payments](https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/) | 2022-08-25 | donor-selected PII; export | F |
| 7 | [PPGF Donation Delivery Policy](https://www.paypalobjects.com/marketing/web25/us/paypal-giving-fund/policy-updates/ppgf-us-delivery-01012025.pdf) | 2025-01-01 | donor details except anonymous | F |
| 8 | [DAFgiving360 2024 Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) | modified 2024-12-12 | letter options; checks; OSA incorporation | F |
| 9 | [Chronicle of Philanthropy](https://www.philanthropy.com/article/why-your-daf-donor-may-not-be-anonymous-after-all) | 2024-10-08 | DAFRC sponsor-default figures | S |
| 10 | [BridgeFT registration types](https://docs.bridgeft.com/docs/source-account-and-registration-types.md) | updated 2025-10-06 | Schwab DAF codes | F |
| 11 | [Endaoment institutions](https://endaoment.org/institutions) | live 2026-11-15 | custodian-agnostic claim; API tiers | F (vendor claim) |
| 12 | [Candid changelog: PDF v2](https://developer.candid.org/changelog/charity-check-pdf-api-v2-now-available.md); [verification guide](https://developer.candid.org/docs/verification-using-charity-check.md); [get started](https://developer.candid.org/reference/get-started-with-charity-check.md); [FAQ](https://developer.candid.org/reference/faqs-charity-check.md); [v2 endpoint](https://developer.candid.org/reference/charitycheckpdf_v2.md) | 2025-04-18; 2026-09-07 | v2 sample identity; "timestamp" wording; 2011-33 citation | F |
| 13 | [Bloomerang pricing help](https://help.bloomerang.com/en/articles/12632855-payment-processing-pricing); [Bloomerang Fundraising pricing](https://help.bloomerang.com/en/articles/13382651-bloomerang-fundraising-pricing); [Bloomerang DAFpay blog](https://bloomerang.com/blog/dafpay) | read 2026-11-15; blog 2026-10-29 | DAFpay 4.85%; card 3.95% + $0.30; default-on | F |
| 14 | [Donorbox DAF page](https://donorbox.org/explore/donor-advised-fund-donations); [Donorbox pricing](https://donorbox.org/pricing) | read 2026-11-15 | DAFpay 4.5%; card platform fees; Stripe rates | F |
| 15 | [Funraise DAFpay help](https://help.funraise.io/en/articles/12142901-accept-daf-donations-with-dafpay); [Funraise payments](https://funraise.org/funraise-payments) | 2026-01-30; live | DAFpay 1% + 2.9%; card platform fee only if donor covers | F |
| 16 | [BetterWorld fees help](https://help.betterworld.org/en/articles/8558015-what-are-the-processing-fees-and-who-covers-them); [BetterWorld pricing](https://betterworld.org/pricing/) | undated; live | DAFpay 3.9%; free plan; card 2.9% + $0.30 | F |
| 17 | [Givebutter DAFpay help](https://help.givebutter.com/en/articles/6764835-how-to-use-givebutter-s-dafpay-donation-method); [Givebutter pricing](https://givebutter.com/pricing) | 2026-10-06; live | DAFpay 2.9%; tips model | F |
| 18 | [AASP FundSvcs thread](https://aasp.connectedcommunity.org/discussion/dafpay-via-givecampus) | 2025-10-06 to 2025-10-12 | practitioner fee concerns; GiveCampus fee route | P |
| 19 | [Schwab Online Services Agreement](https://www.schwab.com/legal/terms); [Electronic Services Agreement](https://www.schwab.com/legal/electronic-services-agreement); [Third-party terms](https://www.schwab.com/legal/third-party-terms) | © 2026; read 2026-11-15 | SOSA text; credential and aggregator clauses | F |
| 20 | Search-index captures of dafgiving360.org pages (program-policies, quarterly-performance-report, investment-choices, giving-deadlines) | 2026 | blocked items | R |
| 21 | [IPS, "New donor-advised fund tech raises old concerns"](https://ips-dc.org/new-donor-advised-fund-tech-raises-old-concerns/) | 2024-08-09 | background only (Chariot fee and privacy statements quoted by editor) | S |

---

## 10. Data dictionary

### `anonymity-data-flow-2026.csv` (one row per rail × layer)

| Column | Meaning |
|---|---|
| `row_id` | A01–A16 |
| `rail` | Payment or data rail (DAFpay, Chariot Disbursements, PayPal Grant Payments, PPGF, sponsor letter) |
| `layer` | Which step of the flow the row describes (sponsor call, Chariot profile, remittance, nonprofit record, export) |
| `donor_control_stated` | What choice the donor or grantmaker is documented as having |
| `if_anonymous_nonprofit_receives` | What reaches the nonprofit for an anonymous gift, as documented; "not documented" where silent |
| `if_fund_name_only_nonprofit_receives` | Same, for a fund-name-only choice |
| `anonymity_flag_in_nonprofit_data` | Whether nonprofit-facing data carries an explicit anonymity marker (yes / no / implied / n/a) |
| `reidentification_path` | Any documented identifier linking an anonymous payment to a richer record; [I] where inferred |
| `key_quote` | Verbatim, ≤40 words, from `source_url`; blank for A16 (paraphrased secondary) |
| `source_url`, `source_date`, `evidence_label`, `retrieved`, `notes` | As named; labels per header (F, F (repo), S) |

### `dafpay-stacking-fees-2026.csv` (one row per platform × plan or condition)

| Column | Meaning |
|---|---|
| `row_id` | S01–S14 |
| `platform`, `plan_or_condition` | Fundraising platform and the plan or processor assumption the row uses |
| `dafpay_chariot_fee_pct`, `dafpay_platform_fee_pct`, `dafpay_total_pct` | Published DAFpay fee components (%) |
| `dafpay_cost_per_1000_usd` | Nonprofit cost on a $1,000 gift if the donor does not cover (before whole-dollar rounding) |
| `dafpay_donor_can_cover` | Whether the platform lets donors cover the DAFpay fee |
| `card_rate_nonprofit_default`, `card_cost_per_1000_usd` | The platform's card cost to the nonprofit on a $1,000 gift (platform + processor), with any assumption stated |
| `card_donor_can_cover` | Whether donors can cover card fees |
| `dafpay_minus_card_per_1000_usd` | Positive = DAFpay costs the nonprofit more |
| `dafpay_vs_card` | DAFpay dearer / cheaper / about equal |
| `dafpay_off_switch` | Documented ability to disable DAFpay |
| `key_quote`, `source_url`, `source_date`, `evidence_label`, `retrieved`, `notes` | As named; "F + assumption" marks rows with an assumed processor rate; P = practitioner forum |

### `queue-proposals-batch36c.csv`

Standard proposal columns per `queue-proposals-README.md`; prefix P-B36C-; `state` = open.

---

## 11. Proposals

- **P-B36C-01:** when a DAFpay grant has `anonymous=true`, what donor data does the nonprofit's Chariot record show? Use public sponsor and partner help pages.
- **P-B36C-02:** which DAF programs sit behind Schwab codes DASCG, DASPL and CHGFT, and do Orion, Black Diamond or Addepar map them to a DAF class?
- **P-B36C-03:** reconcile Chariot's "80% of DAFpay usage" subscription claim with the "$199/mo + 2.9%" Components price. Bound the fee-bearing share with the DAFpay Network's (EIN 93-1372175) Form 990.
