# Queue batch 37 C: grant-payment redirection controls (P-PRC-06), DAFpay anonymity (P-B36C-01), Daffy corporate delegates (P-B36B-01), probability samples (P-ANL-04), adviser curricula (P-ANL-06), sponsor funding of adviser education (P-ANL-09)

**Date:** 2026-11-15. Prepared by the batch 37 C agent. These are files only: no commit and no push.

**Method:** Desk research from public sources, 2021 onward. This is research, not legal advice.
- No accounts were created and nothing was logged in to.
- No forms were submitted, no one was contacted, and no API call needing a key was made.
- GitBook's `?ask=` query endpoint on the Chariot help centre was not used. Only static pages were read.
- robots.txt was read on each host before fetching, and its rules were followed:
  - **dafresearchcollaborative.org** and **jdsupra.com** disallow Anthropic agents, so they were not fetched.
  - **psidonline.isr.umich.edu**, **hrs.isr.umich.edu**, **dafgiving360.org**, **schwabcharitable.org** and **candid.org** returned 403 to robots.txt, so they were not fetched.
  - **cd.cfp.net** redirects robots.txt to a login wall, so it was not used. The same PDF was read at www.cfp.net, whose robots.txt allows the path.
  - **scholarworks.indianapolis.iu.edu** disallows `/server/api`, which is where its PDFs sit, so they were not read.
  - www.federalreserve.gov and www.oig.doc.gov returned 404 for robots.txt, which means no rules apply.
- **paypal.com** robots.txt allows the PayPal Giving Fund policy paths, but the server returned 403. Those pages appear here only as search-index text, tagged [R].

**Read first (governing corrections applied):**
- [analyst-and-education-landscape.md](analyst-and-education-landscape.md) §4–§5, including waves 4 and 19. The "61% / 6%" figure is 2018 U.S. Trust/TPI data, not 2026 data.
- [queue-batch36-agent-terms-controls.md](queue-batch36-agent-terms-controls.md) §1, including wave 21. Organizers as well as Financial Advisors may be "any individual, corporation, or trust".
- [queue-batch36-anonymity-feeds-fees.md](queue-batch36-anonymity-feeds-fees.md) §1, including wave 21.
- [ai-governance-failure-modes.md](ai-governance-failure-modes.md) F06 (agent identity), F16 (credential compromise), and wave 2A. Its counts are rubric ratings with no observed incidents.

**Evidence tags:**
- **[F]** fact from a source read this batch.
- **[R]** search-index text; the page itself was not read.
- **[I]** inference.
- **[X]** carried from the repo.

**Outputs:**
- [`data/mission-2026-11-14/payment-redirection-controls-2026.csv`](../../data/mission-2026-11-14/payment-redirection-controls-2026.csv): PR01–PR25.
- [`data/mission-2026-11-14/adviser-curricula-daf-content-2026.csv`](../../data/mission-2026-11-14/adviser-curricula-daf-content-2026.csv): EC01–EC11.
- [`data/mission-2026-11-14/queue-proposals-batch37c.csv`](../../data/mission-2026-11-14/queue-proposals-batch37c.csv): P-B37C-01 to P-B37C-03.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-PRC-06** How sponsors control grant-payment redirection | **No sponsor publishes the main control in the federal benchmark: a callback to a known contact before a bank-detail change. Redirection risk is handled by keeping bank details out of the sponsor's hands.** The benchmark is the Commerce OIG July 2026 alert. It asks for a callback to a known contact, dual approval of banking changes, and sender-address checks (PR24).<br>• **Fidelity Charitable** publishes the most detailed own-rail controls (PR01–PR05):<br>&nbsp;&nbsp;– a voided check;<br>&nbsp;&nbsp;– two prior grant IDs or check numbers from the last 3 years;<br>&nbsp;&nbsp;– two named contacts, each with an individual inbox;<br>&nbsp;&nbsp;– a wet signature;<br>&nbsp;&nbsp;– the same form for updates as for enrolments.<br>&nbsp;&nbsp;No callback is stated, and Stripe enrollees change bank details under Stripe's controls. Its donor page is the only sponsor page found that names "business email compromise" (PR07).<br>• **Vanguard Charitable and NPT** pay through **PayPal Grant Payments**, so they hold no charity bank details (PR10, PR13, PR14). Vanguard's charity fraud list has no redirection item (PR11). PayPal's own change controls were not readable (403; PR15).<br>• **Chariot** (and **Daffy**, which pays only into Chariot Deposit Accounts) publishes the strongest charity-side design (PR16–PR21):<br>&nbsp;&nbsp;– non-debitable receiving accounts in the charity's name;<br>&nbsp;&nbsp;– only the Account Owner can change the external bank account;<br>&nbsp;&nbsp;– 2FA is mandatory;<br>&nbsp;&nbsp;– ownership transfer needs identity verification;<br>&nbsp;&nbsp;– payees are verified by officer identity rather than bank statements.<br>&nbsp;&nbsp;No callback or cooling-off period is stated.<br>• **DAFgiving360:** blocked. | High on published text; absence of callbacks is absence from public docs, not proof of practice |
| **P-B36C-01** DAFpay `anonymous=true`: does the nonprofit's Chariot record still show the donor? | **No public document says the record is blanked. Several say the nonprofit sees what the donor typed.**<br>• The **nonprofit's own form** sets `anonymous`, in the same callback that passes `firstName`, `lastName` and `email`. The flag exists "so the donation can be properly anonymized by the DAF provider".<br>• The nonprofit-facing Grant object has donor fields and no anonymity field.<br>• Chariot's DAFpay Security page says the nonprofit "can view the information provided by the donor (Name, Email, Address and Gift Size)". It also says some nonprofits "disallow anonymous gifts through DAFpay".<br>• The 2026 Donor Accounts beta's Grant Request carries a `donor_contact` snapshot and no anonymity field.<br>• The only contrary text is a retired help article, seen in search only [R]. | Medium (absence of an explicit statement) |
| **P-B36B-01** Daffy corporate FA or Organizer: published limits or approval? | **None published. Daffy disclaims checking:** "Daffy is not responsible for reviewing the authority of designees for any corporation or trust."<br>• The API docs issue keys per account at `settings/developers`, and the API returns a single `current_fund`.<br>• How an advisor serving several funds selects a fund, and whether its actions are logged separately, is not documented.<br>• The Agreement says advisor actions "are represented as actions taken by the Organizer directly". | High on text; unknown on mechanics |
| **P-ANL-04** Probability-sample DAF measure? | **None found.**<br>• The 2022 **SCF** has no DAF item. Its only DAF mention excludes DAFs from the trust question, and the public file merges that code into "trusts".<br>• SCF does ask about $500+ charitable gifts (X5822/X5823) and "any sort of charitable trust or foundation" (X7660/X7661).<br>• **PSID's Philanthropy Panel Study** and **HRS** could not be read under the robots rule. No search result shows a DAF item in either.<br>• The PPS's recent funders include the Fidelity Charitable Catalyst Fund. Its 2025 next-gen report was funded by DAFgiving360. | High for SCF 2022; low for PSID/HRS (unread) |
| **P-ANL-06** Curricula audit | **Payout, fee, portability and inactivity content are absent from all 11 public outlines read.**<br>• The CFP Board's 70 topics and learning objectives never name DAFs.<br>• The new **DAFCP** outline covers tax, gift acceptance, Notice 2017-73, succession and technology, but not payout, fees or transfers between sponsors.<br>• The one adviser-facing payout resource found is **sponsor-authored and aggregate-only** (NPT Spotlight). This is the repo's T1 pattern.<br>• Sponsor discretion is taught in one American College CE module (2024). | Medium-high (outlines only; paid content not inspected) |
| **P-ANL-09** Sponsor funding of adviser education | **Of the 11 education items, 5 have documented DAF-sponsor delivery or sponsorship, 1 has a partial tie, 2 have none and 3 are unknown. Dollar amounts are almost entirely undisclosed.**<br>• The four Premier Partners of the American College's **DAF Forum 2027** are **DAFgiving360, Fidelity Charitable, NPT and Vanguard Charitable**. The same institution grants the DAFCP.<br>• Only tier floors are published: Silver from $15,000 and Exhibitor from $5,000.<br>• Adviser-facing research 2024–26 in the repo is sponsor-funded or co-funded throughout: DAFRC 2026, TPI 2026, Fidelity 2024 and Lilly next-gen 2025. | High on the listed ties; amounts unknown |

---

## 1. P-PRC-06: how DAF sponsors control grant-payment redirection

**Why it matters:** Three of the seven Part VI line-5 disclosures in the 1,512-sponsor 990 universe are payment redirection or business email compromise (BEC). They are Prosperity Foundation ($900k wire, $500,845 net), WashU ($565,787) and TNC ($524,983) ([sponsor-fraud-loss-disclosures.csv](../../data/mission-2026-11-14/sponsor-fraud-loss-disclosures.csv)) [X]. The attack is to change the payee's bank details or wire instructions, not to steal a credential at the payer.

### 1.1 Benchmark

The [Commerce OIG Fraud Alert (2026-07-27)](https://www.oig.doc.gov/wp-content/OIGPublications/DOC-OIG-Fraud-Alert-July-2026-Approved.pdf) [F] describes criminals who say the grantee "has changed banks or no longer accepts checks". It asks payers to apply three controls:
- **B1 Out-of-band verification:** "Independently verify every request to change banking or payment information by calling/videoconferencing a known contact".
- **B2 Dual approval and separation of duties** for "payment setup, banking changes".
- **B3 Sender inspection** (address, reply-to and domain).

### 1.2 What each sponsor or rail publishes

| Provider | Where charity bank details live | Change path published | B1 callback | B2 dual control | Other controls | Rows |
|---|---|---|---|---|---|---|
| **Fidelity Charitable** (own ACH) | Fidelity | Same ACH form for enrolment and update: "This form is used for both new enrollments and updates to banking, contact, or address information" ([FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html)) | **Not stated** | Not stated. Two named contacts receive the Grant Details Report | • Voided check<br>• Two grant IDs or check numbers from the last 3 years<br>• Individual inboxes only<br>• Wet signature; "E-Signature is not acceptable"<br>• No PO box (CIP)<br>([form, PDF 2025-12-18](https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/charitable-organization-eft-enrollment-form.pdf)) | PR01–PR05 |
| **Fidelity Charitable** (Stripe) | Stripe | Stripe dashboard, under Stripe's controls (not described by Fidelity) | Not stated | Not stated | Two Fidelity pages conflict on whether grant emails are sent ([Stripe FAQ](https://www.fidelitycharitable.org/nonprofits/fidelity-grant.html) vs [FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html)) | PR05, PR06 |
| **Vanguard Charitable** | PayPal | None. Charities enrol at paypal.com/charities ([nonprofits](https://www.vanguardcharitable.org/nonprofit-organizations)) | n/a at Vanguard | n/a | • Security Center lists six schemes against nonprofits, none of them redirection<br>• "call us at 888-383-4483" if correspondence looks doubtful ([Security Center](https://www.vanguardcharitable.org/company-policies/security-center)) | PR10–PR12 |
| **NPT** | PayPal | None ([for nonprofits](https://www.nptrust.org/for-nonprofits/), modified 2026-11-10) | n/a at NPT | n/a | Unaccepted PayPal grant becomes a check after 14 days [X] | PR13 |
| **PayPal Grant Payments / PPGF** | PayPal | Not read (403) | unknown | unknown | PayPal's 2023 study says grant makers need not "collect and retain this information" ([PDF](https://filecache.mediaroom.com/mr5mr_paypal/186631/PP_2023_GrantPayments.pdf)) | PR14, PR15 |
| **Chariot** (receiving account) | A Chariot Deposit Account in the charity's name (Column N.A.); the operating bank is an "External Financial Account" | "Only Account Owners can add or update external financial account details." A bank statement or photo ID may be required if the name does not match ([money movement](https://help.givechariot.com/account-management/money-movement.md)) | **Not stated** | **Partial:** a single role (Owner) for changes; Admins can transfer out but not change the account | • Non-debitable account numbers ([verification](https://help.givechariot.com/onboarding/compliance-verification/verification-and-fraud-prevention.md))<br>• Mandatory 2FA<br>• Owner 2FA reset needs identity verification and Chariot approval<br>• Ownership transfer needs identity verification ([login](https://help.givechariot.com/account-management/login-and-security.md); [ownership](https://help.givechariot.com/account-management/ownership-transfers.md)) | PR16–PR18 |
| **Chariot Disbursements** (pays for sponsors) | As above | Payee verification by "officer identities through IRS master files", not bank statements ([compliance](https://docs.givechariot.com/v2026-04-01/guides/disbursements/compliance.md)) | Partial: "direct contact for larger payments" (check path) | not stated | Positive Pay; delivery tracking; stop-payment API | PR19 |
| **Daffy** | Chariot | Electronic grants only to Chariot; otherwise US mail ([Daffy help](https://help.daffy.org/en/articles/9122843-how-does-daffy-send-donations-to-charity)). Charity profile changes go through a support ticket that asks for EIN and mailing address and has no bank field ([Daffy help](https://help.daffy.org/en/articles/6464786-how-do-i-update-charity-information-on-daffy)) | Inherits Chariot [I] | Inherits Chariot [I] | Check reissue if lost | PR20–PR22 |
| **DAFgiving360** | unknown | Blocked (robots 403) | unknown | unknown | 2024 policies: grants by check [X] | PR23 |

### 1.3 Readings [I]

1. **There are two control strategies, and neither is the federal benchmark.**
   - *Own rail with document checks.* Fidelity relies on a voided check, knowledge of past grant IDs and a wet signature. These defeat a pure email request but not an attacker who holds stolen grant letters. No callback is published.
   - *Keep bank details out of the sponsor's hands.* Vanguard and NPT use PayPal; Daffy uses Chariot. This removes the "please update our bank details" email to the sponsor, because the sponsor has no field to update. It moves the risk to account takeover at the rail, where Chariot publishes Owner-only changes and 2FA, and PayPal's controls could not be read.
2. **Only Fidelity warns about BEC, and only to donors.** Its advice to donors, "Avoid acting on unexpected payment detail changes communicated through a single channel", is the benchmark control. No sponsor page states that it applies the same control to grantees.
3. **The receiving-account model also fits agents.** An agent that can recommend grants (batch 36B) cannot redirect a payment on Chariot or PayPal rails, because the payee account is not a grant field. The redirection vector stays with the charity's Owner credential and with the mailing address used for checks (PR21).
4. **Fidelity's own page warns against third-party tools that collect credentials** (PR08). This sits alongside DAFpay's credential pass-through and the agent wrappers in batches 35–36. Fidelity names no processor.

---

## 2. P-B36C-01: DAFpay with `anonymous=true`

| Evidence | What it says | Tag |
|---|---|---|
| [Integration guide](https://docs.givechariot.com/v2026-04-01/guides/dafpay/integrating-dafpay/integration.md) (v2026-04-01) | The nonprofit's `onDonationRequest` callback returns `firstName`, `lastName`, `email`, `phone`, `address` and `anonymous` together. "Anonymous: Indicate if a donor has chosen to give anonymously on your donation form so the donation can be properly anonymized by the DAF provider." | F |
| [Get Grant](https://docs.givechariot.com/v2026-04-01/api/grants/get.md) | Optional donor fields; no `anonymous` field | F (as batch 36C) |
| [DAFpay Security](https://help.givechariot.com/dafpay/dafpay-security.md) | The nonprofit "can view the information provided by the donor (Name, Email, Address and Gift Size)". The donor can "remove or change those details". "Some nonprofits elect to disallow anonymous gifts through DAFpay on their own website." | F |
| [Grant Request](https://docs.givechariot.com/v2026-04-01/api/grant-requests/get.md) (Donor Accounts beta, [changelog 2026-05-08](https://docs.givechariot.com/v2026-04-01/changelog/2026/5/8.md)) | Sponsor-facing object with "A snapshot of the donor's contact information"; no anonymity field | F |
| [Fundraise Up DAFpay docs](https://fundraiseup.com/docs/dafpay/) (modified 2026-10-30) | By default "the supporter who recommended the grant is recorded as the donor"; anonymity not mentioned | F |
| Daffy help ([visibility](https://intercom.help/daffy/en/articles/6964337-how-do-i-customize-the-information-i-share-with-a-charity), [DAFpay](https://help.daffy.org/en/articles/12084669-what-is-dafpay-and-how-do-i-use-it)) | Daffy-native anonymity sends "no identifying information"; the DAFpay article does not mention anonymity | F |
| Retired Chariot article "What information will my organization get from DAFpay grants" (404) | A search summary says an anonymous donor's name and email "will not be visible" | R |

**Readings [I]:**
- **The flag is an instruction to the sponsor.** The nonprofit's own platform raises it, after the donor has typed or autofilled identity into that platform's form, and it rides in the same payload as the identity fields.
- **No public statement says Chariot blanks those fields** in the nonprofit dashboard or export when the flag is true. The live help page says the opposite in general terms: the nonprofit sees what the donor provided.
- **Effective anonymity therefore depends on the donor clearing the fields.** The nonprofit's form settings may not allow that ("disallow anonymous gifts").
- This strengthens batch 36C's finding. DAFpay's "fewer anonymous gifts" mechanism works before sponsor anonymity policy applies.
- **The only contrary evidence is [R].** P-B37C-01 proposes checking platform-side help pages.

---

## 3. P-ANL-04: does a probability sample measure DAF ownership?

| Survey | DAF item? | Evidence |
|---|---|---|
| **SCF 2022** (public file, October 2023 version) | **No.** The only DAF text excludes them. Under X6830 "Other", code 10 is "Charitable remainder trust: does not include donor-advised funds where R has surrendered all benefit from the asset", and "FOR THE PUBLIC DATA SET, CODE 10 IS COMBINED WITH 'YES' RESPONSES FOR X6828" (trusts). | [codebook](https://www.federalreserve.gov/econres/files/codebk2022.txt) [F] |
| SCF 2022, giving items | X5822: gifts "totaling $500 or more" in 2021. X5823: amount. X7660: "any sort of charitable trust or foundation" (includes charitable remainder trusts). X7661: value. X7660/X7661 are in the public variable list | same [F] |
| **PSID Philanthropy Panel Study** | **Unknown.** psidonline robots.txt returned 403, so it was not read. Search found no DAF item. A 2024 NBER PPS paper on TCJA giving does not mention DAFs. Its acknowledgement lists PPS "recent institutional donors" including the "Fidelity Charitable Catalyst Fund" | [NBER w32737](https://www.nber.org/system/files/working_papers/w32737/w32737.pdf) [F]; PSID [R] |
| **HRS** | Unknown (robots 403; not searched further) | — |
| **Lilly School, *The Next Generation of Philanthropy* (2025)** | Uses PPS. The release reports no DAF rate. "The research was completed with funding from DAFgiving360™" | [Lilly release, 2025-01-29](https://philanthropy.indianapolis.iu.edu/news-events/news/_news/2025/next-generation-donors-charitable-giving-interests-approaches.html) [F] |

**Readings [I]:**
- The SCF does not measure DAF ownership, by design. A DAF is not a household asset, so the codebook tells interviewers to leave it out of trusts.
- A respondent could report a DAF under X7660 ("charitable trust or foundation"). Nothing instructs this, so X7660 cannot serve as a DAF proxy.
- The repo's penetration figures stay sponsor- or bank-sourced (about 7% of affluent households in 2020, BofA/Lilly) and have no probability-sample benchmark.

---

## 4. P-ANL-06: curricula audit against repo findings

All rows are in `adviser-curricula-daf-content-2026.csv`. The scoring uses public outlines and objectives only; paid content was not opened.

| Repo claim (analyst §5.2) | What the 11 items teach, as far as outlines show | Verdict |
|---|---|---|
| **T1** payout ("25% vs 8%") | • DAFCP: no payout item.<br>• CFP: none.<br>• The one adviser-facing payout resource is NPT's Spotlight (2021-08-19, data to 2019). It is aggregate-only, uses four formulas, and says payout is "three to six times higher" than the private-foundation minimum; no median and no account-level figure (EC09) | **Pattern confirmed** in sponsor-authored adviser material; absent from credential outlines |
| **T2** inactivity rules | Absent from every outline | **Gap** |
| **T3** account counts | DAFCP uses assets ($328bn), growth (19%) and contributions ($91bn), not account counts | Not repeated |
| **T4** portability | Absent from all 11 items | **Gap confirmed** (previously DAFCP only) |
| **T5** sponsor discretion | • American College CE (2024): "Explain accurately to clients the possibility that a grant may be denied" (EC06).<br>• DAFCP: "Legal guardrails"; "court cases" | Taught in one CE module |
| **T7** fees | Absent from every outline | **Gap** |
| **T9** tax-first framing | • NAPFA: "maximize tax benefits"; objective 1 is "key features and advantages".<br>• Fidelity: "Tax-Smart" sessions.<br>• CFP E.43 is deductions-only | **Consistent** with the adviser tax-first framing |

**Reading [I]:** The legal and tax mechanics are well covered. What advisers would need to compare sponsors, such as payout distribution, fees, transfer terms and inactivity rules, is not a visible teaching item anywhere. P-ANL-08, a test of a "payout triad", remains unaddressed by any curriculum.

---

## 5. P-ANL-09: sponsor funding of adviser-facing research and education

| Item (2021+) | Sponsor tie | Amount public? | Source |
|---|---|---|---|
| DAF Forum 2027 (American College) | Premier Partners: DAFgiving360, Fidelity Charitable, NPT, Vanguard Charitable | Premier: no. Silver "Starting at $15,000"; Exhibitor "Starting at $5,000" | [sponsors](https://events.theamericancollege.edu/daf-forum/sponsors); [prospectus page](https://partnership.theamericancollege.edu/advancement/annual-experiences/daf-forum) [F] |
| DAFCP (American College, 2026) | No sponsor named. One of 22 listed instructors is an NPT SVP | n/a | [DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp); [NPT advisors](https://www.nptrust.org/advisors-and-institutions/for-advisors/) [F] |
| Fidelity Charitable CE curriculum | Sponsor-delivered, "complimentary CE credits" | no | EC08 [F] |
| NPT DAF Spotlight (payout) | Sponsor-authored | n/a | EC09 [F] |
| NAPFA Partner Solutions webinar (2025–26) | Sponsored; speaker from UI Charitable | no | EC10 [F] |
| CFP Board CE program (2026) | Program sponsor: St. Louis Community Foundation | no | EC11 [F] |
| Lilly *Next Generation of Philanthropy* (2025) | Funded by DAFgiving360 | no | §3 [F] |
| PSID Philanthropy Panel Study | Recent funders include the Fidelity Charitable Catalyst Fund | no | §3 [F] |
| DAFRC adviser report (2026) | Funded by DAFgiving360 | no | analyst file wave 19 [X] |
| TPI adviser study (2026) | Co-sponsored by DAFgiving360 and Foundation Source | no | analyst §4.1 [X] |
| Fidelity Charitable adviser surveys (2024) | Sponsor-commissioned | no | analyst §4.1 [X] |

**Count:** 11 education items:
- 5 have documented DAF-sponsor delivery or sponsorship (EC07–EC11);
- 1 has a partial tie (EC03);
- 2 have none (CFP Board, EC01–EC02);
- 3 are unknown (EC04–EC06).

Every 2024–26 adviser-facing research item in the repo has a DAF-sponsor funder or co-funder.

**Dollars:** only the DAF Forum tier floors are public, so total sponsor spending on adviser education cannot be quantified from public sources [I].

**Framing effect [I]:** in the sponsor-tied items, the content gaps are the same as the gaps in §4: no fee, payout-distribution or portability items. With n=11 this is an association, not proof of influence.

---

## 6. P-B36B-01: Daffy corporate Financial Advisor or Organizer

| Point | Text | Source |
|---|---|---|
| Eligibility | "any individual 18 years or older, corporation, or trust may become a Daffy member" | [Member Agreement](https://www.daffy.org/legal/agreement) (2025-11-11) [F] |
| Authority check | "Daffy is not responsible for reviewing the authority of designees for any corporation or trust." | same [F] |
| Attribution | Advisor actions "are represented as actions taken by the Organizer directly on the Daffy platform". Advisors "may be deemed to be donor-advisors for purposes of Section 4966" | same [F] |
| Advisor permissions | • Can make donations, initiate contributions, change portfolio and access statements.<br>• Cannot change fund information, the legacy plan, members, or payment methods ("Advisors cannot contribute to a fund by using the bank accounts and debit/credit cards linked by other members") | [role permissions](https://help.daffy.org/en/articles/6604373-what-role-permissions-do-members-of-my-fund-have) (modified 2026-09-15) [F] |
| Advisor login | Advisors use "their own secure login credentials" | [advisor help](https://help.daffy.org/en/articles/7257971-what-can-my-advisor-do-once-added-to-my-fund) [F] |
| API keys | Created at `daffy.org/settings/developers`, revocable. Every agent route "acts as you, on your fund". `GET /v1/users/me` returns one `current_fund`, and no fund selector is documented | [agents](https://docs.daffy.org/agents); [auth](https://docs.daffy.org/auth); [users](https://docs.daffy.org/ref/users) [F] |
| Firm arrangements | "If you or your firm would like to cover the membership dues of your clients, get in touch at partner@daffy.org" | [Daffy for advisors](https://www.daffy.org/advisors) [F] |

**Readings [I]:**
- Daffy publishes **no limit, approval step or authority check** for a corporate or trust delegate, and it expressly disclaims reviewing designee authority.
- A corporate advisor login exists. Whether it can create its own API key or MCP grant is **not documented**. If it can, the single `current_fund` design leaves unclear which client fund the key acts on.
- The Agreement says the platform records the advisor's actions as the Organizer's. So even a sanctioned entity delegate, a possible home for an agent operator, would leave no separate identity in Daffy's records. This is the F06 problem.
- Resolving this needs a logged-in test or outreach, and both are barred. It stays open.

---

## 7. Proposed corrections to repo text (not governing until validated)

1. **analyst-and-education-landscape.md §5.2, closing paragraph.**
   - **Find:** "The DAFCP has no named sponsor partner on its page"
   - **Add after the sentence:** "The same college's DAF Forum 2027 lists DAFgiving360, Fidelity Charitable, NPT and Vanguard Charitable as Premier Partners, and one DAFCP instructor is an NPT executive [batch 37C]."
2. **analyst-and-education-landscape.md §5.2, T4 row, verdict.** Append: "Batch 37C found no portability, fee, payout-distribution or inactivity item in 11 public outlines (CFP Board topics and objectives, DAFCP, CAP, two American College CE modules, Fidelity, NPT, NAPFA, CFP CE registry)."
3. **analyst-and-education-landscape.md §4.2 or §7.** Add: "No probability sample measures DAF holding. The 2022 SCF codebook excludes DAFs from its trust question (X6830 code 10, merged into X6828 in the public file) [batch 37C]."
4. **queue-batch36-anonymity-feeds-fees.md §1.1, Reading.** Add: "The `anonymous` flag is set by the nonprofit's own form in the same callback as the donor's name and email. Chariot's DAFpay Security page says the nonprofit sees what the donor provided, and that some nonprofits disallow anonymous DAFpay gifts [batch 37C]."
5. **queue-batch36-agent-terms-controls.md §1.2, reading 3.** Add: "The Agreement also says 'Daffy is not responsible for reviewing the authority of designees for any corporation or trust' [batch 37C]."

---

## 8. Limits

- **Absence findings.** These include no callback published, no anonymity blanking stated, and no DAF item in a curriculum. They rest on public pages read on 2026-11-15. Sponsors may apply controls they do not publish.
- **PayPal and DAFgiving360.** Their controls were not readable (403 responses or robots blocks). PSID and HRS were not read.
- **Curricula.** Only outlines and objectives were read. Paid course content (DAFCP, CAP, Knowledge Hub+) may cover payout, fees or portability.
- **Logo-based sponsor identification.** The DAF Forum Premier Partners were identified from logo image file names under the "Premier Partners" heading.
- **Fidelity form scope.** The ACH form is dated by PDF metadata (2025-12-18). The FAQ describes a newer flow (an emailed secure-form link) whose steps were not seen.

---

## 9. Source register

| ID | Source | Date | Used for |
|---|---|---|---|
| S1 | [Fidelity Charitable ACH Registration Form](https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/charitable-organization-eft-enrollment-form.pdf) | PDF 2025-12-18 | PR01–PR04 |
| S2 | [Fidelity Charitable nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html); [EFT page](https://www.fidelitycharitable.org/nonprofits/eft.html); [Stripe FAQ](https://www.fidelitycharitable.org/nonprofits/fidelity-grant.html) | live 2026-11-15 | PR05, PR06, PR09 |
| S3 | [Fidelity Charitable security tips](https://www.fidelitycharitable.org/articles/security-tips-common-scams.html) | undated | PR07, PR08 |
| S4 | [Vanguard Charitable nonprofits](https://www.vanguardcharitable.org/nonprofit-organizations); [Security Center](https://www.vanguardcharitable.org/company-policies/security-center); [Policies](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) (updated 2026-01-09) | live 2026-11-15 | PR10–PR12 |
| S5 | [NPT for nonprofits](https://www.nptrust.org/for-nonprofits/); [NPT PayPal post](https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/) | 2026-11-10; 2022 | PR13 |
| S6 | [PayPal, *How Philanthropic Dollars Move*](https://filecache.mediaroom.com/mr5mr_paypal/186631/PP_2023_GrantPayments.pdf) | 2023-11 | PR14 |
| S7 | [PPGF Nonprofit Certification Policy](https://www.paypal.com/us/paypal-giving-fund/policies/nonprofit-certification-policy) | 2025-09-10 [R] | PR15 |
| S8 | Chariot help: [verification](https://help.givechariot.com/onboarding/compliance-verification/verification-and-fraud-prevention.md), [money movement](https://help.givechariot.com/account-management/money-movement.md), [login](https://help.givechariot.com/account-management/login-and-security.md), [ownership](https://help.givechariot.com/account-management/ownership-transfers.md), [notifications](https://help.givechariot.com/account-management/notifications.md), [DAFpay Security](https://help.givechariot.com/dafpay/dafpay-security.md) | live 2026-11-15 | PR16–PR18; §2 |
| S9 | Chariot docs v2026-04-01: [disbursement compliance](https://docs.givechariot.com/v2026-04-01/guides/disbursements/compliance.md), [integration](https://docs.givechariot.com/v2026-04-01/guides/dafpay/integrating-dafpay/integration.md), [Get Grant](https://docs.givechariot.com/v2026-04-01/api/grants/get.md), [Grant Request](https://docs.givechariot.com/v2026-04-01/api/grant-requests/get.md), [changelog](https://docs.givechariot.com/v2026-04-01/changelog/llms.txt) | v2026-04-01 | PR19; §2 |
| S10 | Daffy help: [sending](https://help.daffy.org/en/articles/9122843-how-does-daffy-send-donations-to-charity), [charity updates](https://help.daffy.org/en/articles/6464786-how-do-i-update-charity-information-on-daffy), [reissue](https://help.daffy.org/en/articles/9122847-what-if-a-charity-doesn-t-receive-my-donation), [roles](https://help.daffy.org/en/articles/6604373-what-role-permissions-do-members-of-my-fund-have), [advisor](https://help.daffy.org/en/articles/7257971-what-can-my-advisor-do-once-added-to-my-fund) | modified 2026 | PR20–PR22; §6 |
| S11 | [Daffy Member Agreement](https://www.daffy.org/legal/agreement); [agents](https://docs.daffy.org/agents); [MCP](https://docs.daffy.org/agents/mcp); [auth](https://docs.daffy.org/auth); [users](https://docs.daffy.org/ref/users); [advisors](https://www.daffy.org/advisors) | 2025-11-11; live | §6 |
| S12 | [Commerce OIG Fraud Alert](https://www.oig.doc.gov/wp-content/OIGPublications/DOC-OIG-Fraud-Alert-July-2026-Approved.pdf) | 2026-07-27 | PR24 benchmark |
| S13 | [Fundraise Up DAFpay docs](https://fundraiseup.com/docs/dafpay/) | 2026-10-30 | §2 |
| S14 | Daffy help: [visibility](https://intercom.help/daffy/en/articles/6964337-how-do-i-customize-the-information-i-share-with-a-charity), [DAFpay](https://help.daffy.org/en/articles/12084669-what-is-dafpay-and-how-do-i-use-it) | 2026-04-02; 2025-09-05 | §2 |
| S15 | [SCF 2022 codebook](https://www.federalreserve.gov/econres/files/codebk2022.txt) | Oct 2023 public version | §3 |
| S16 | [NBER w32737](https://www.nber.org/system/files/working_papers/w32737/w32737.pdf) | 2024-07 | §3 |
| S17 | [Lilly next-gen release](https://philanthropy.indianapolis.iu.edu/news-events/news/_news/2025/next-generation-donors-charitable-giving-interests-approaches.html) | 2025-01-29 | §3, §5 |
| S18 | CFP Board [2021 Principal Knowledge Topics](https://www.cfp.net/-/media/files/cfp-board/cfp-certification/2021-practice-analysis/2021-principal-knowledge-topics.pdf); [Learning Objectives](https://www.cfp.net/-/media/files/cfp-board/cfp-certification/2021-practice-analysis/2021-cfp-certification-learning-objectives.pdf) | 2021 (LO modified 2026-05-06) | EC01–EC02 |
| S19 | American College [DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp); [press release](https://www.theamericancollege.edu/knowledge-hub/press/new-designation-offers-expertise-in-donor-advised-funds); [CAP](https://www.theamericancollege.edu/learn/professional-designations-certifications/cap) | 2026-07-30; live | EC03–EC04 |
| S20 | Knowledge Hub+ [DAF vehicle](https://knowledgehubplus.theamericancollege.edu/?p=14745); [grant denial](https://knowledgehubplus.theamericancollege.edu/?p=14430) | 2025-03-03; 2024-10-14 | EC05–EC06 |
| S21 | [DAF Forum sponsors](https://events.theamericancollege.edu/daf-forum/sponsors); [speakers](https://events.theamericancollege.edu/daf-forum/speakers-agenda); [sponsorship tiers](https://partnership.theamericancollege.edu/advancement/annual-experiences/daf-forum) | live 2026-11-15 | EC07 |
| S22 | [Fidelity Charitable curriculum](https://fidelitycharitable.org/advisors/practice-management/curriculum.html) | live 2026-11-15 | EC08 |
| S23 | [NPT DAF Spotlight: Payout Rates](https://www.nptrust.org/reports/daf-spotlight-daf-grant-payout-rates/); [NPT for advisors](https://www.nptrust.org/advisors-and-institutions/for-advisors/) | 2021-08-19; live | EC09; EC03 affiliation |
| S24 | [NAPFA webinar listing](https://education.napfa.org/Listing/The-Future-of-Charitable-Giving-Tax-Efficient-Strategies-and-OBBBA-Impacts-12994) | expires 2026-12-31 | EC10 |
| S25 | [CFP Board CE program entry](https://www.cfp.net/for-cfp-pros/continuing-education/continuing-ed/2026/05/04/13/46/42bc4235-5397-422c-aa4d-eab7aca5a6dc) | 2026-05-04 | EC11 |
| S26 | Retired Chariot article (intercom.help/givechariot 8712472) | 404; search index only | §2 [R] |

---

## 10. Data dictionary

### `data/mission-2026-11-14/payment-redirection-controls-2026.csv` (one row per provider × control)

| Column | Meaning |
|---|---|
| row_id | PR01–PR25 |
| queue_item | P-PRC-06 |
| provider | Sponsor, rail or benchmark body |
| provider_role | `sponsor`, `EFT rail`, `disbursement processor`, `benchmark`, etc. |
| rail | Payment rail the control applies to |
| control_area | `enrolment_verification`, `bank_change_process`, `bank_change_authority`, `contact_controls`, `signature_and_identity`, `grant_notification`, `payee_account_custody`, `payee_account_design`, `account_takeover_controls`, `payee_verification`, `donor_facing_BEC_warning`, `charity_facing_fraud_warning`, `credential_sharing_warning`, `charity_profile_change`, `lost_payment_recovery`, `benchmark_controls`, `disclosed_losses`, etc. |
| control_stated | Y, N, P (partial), unknown |
| benchmark_control | Which Commerce OIG control (out-of-band verification, dual approval, sender inspection) the row matches, or what it substitutes |
| key_quote | Verbatim, 40 words or fewer (blank for [R] or [X] rows) |
| source_url, document_date | Primary URL and stated or metadata date |
| read_status | `read in full`, `read (targeted)`, `not read: <reason>`, `carried` |
| evidence_label | F, R, I, X |
| reading | Interpretation, tagged |
| retrieved | Access date |
| notes | Caveats |

### `data/mission-2026-11-14/adviser-curricula-daf-content-2026.csv` (one row per curriculum, CE activity, event or adviser-facing resource)

| Column | Meaning |
|---|---|
| row_id | EC01–EC11 |
| queue_item | P-ANL-06 and/or P-ANL-09 |
| activity, provider, provider_type | What it is, who offers it, and the provider category |
| daf_sponsor_involvement | Y (documented), P (partial), N (none), unknown |
| involvement_type | e.g. sponsor-delivered CE, event Premier Partner, instructor affiliation |
| date, access | Stated date; free, paid or subscription, and what was read |
| source_url, evidence_label | Primary URL; F, R, I, X |
| payout_content, fee_content, portability_content, sponsor_discretion_content | `present`, `partial`, `absent`, `not visible` (in outline) or `n/a` |
| market_or_account_claim | Market figures the item repeats |
| key_quote | Verbatim, 40 words or fewer |
| reading | Interpretation, tagged |
| retrieved | Access date |

### `data/mission-2026-11-14/queue-proposals-batch37c.csv`

Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md):
- `importance`, `gap`, `commercial`, `availability` and `effort` are 1–5.
- `p_change` is 0–1.
- `state` is `open`.
- `proposed_by` is `batch37 C agent`.

---

## 11. Proposals

- **P-B37C-01:** for each fundraising platform that sends the `anonymous` flag, establish from its public help pages whether its own donor record and the Chariot export keep the donor's identity.
- **P-B37C-02:** find a robots-compliant route to the PSID PPS and HRS questionnaires (ICPSR or openICPSR), and to the 2025 SCF codebook when it is released, to settle whether any probability sample has a DAF item.
- **P-B37C-03:** take DAFCP instructor and DAF Forum speaker employers from the College's own bios, and score the sponsor share of the credential's faculty.

## Validation corrections (wave 22, 2026-11-15) — governing
Source: [validation-wave22-report.md](validation-wave22-report.md); register `data/mission-2026-11-14/validation-register-wave22.csv`.

1. **§0, P-PRC-06 row (lead sentence).**
   - **Find:** "**No sponsor publishes the main control in the federal benchmark: a callback to a known contact before a bank-detail change. Redirection risk is handled by keeping bank details out of the sponsor's hands.**"
   - **Replace with:** "**No sponsor publishes the full federal benchmark control: a mandatory callback to a known contact, by a previously established channel, before every bank-detail change. Fidelity Charitable publishes a discretionary version ("we may call your organization's publicly available phone number to verify banking and/or contact information") for enrolments and updates. Elsewhere, redirection risk is handled by keeping bank details out of the sponsor's hands** [V wave 22]."
2. **§0, Fidelity verifier bullet.**
   - **Find:** "&nbsp;&nbsp;– two prior grant IDs or check numbers from the last 3 years;"
   - **Replace with:** "&nbsp;&nbsp;– supporting information from the last 3 years: two prior grant IDs, two check numbers or a Fidelity Charitable reference number (first-time grantees face unspecified \"additional verification\") [V wave 22];"
3. **§0, Fidelity callback sentence.**
   - **Find:** "&nbsp;&nbsp;No callback is stated, and Stripe enrollees change bank details under Stripe's controls."
   - **Replace with:** "&nbsp;&nbsp;The nonprofit FAQ adds that Fidelity \"may call your organization's publicly available phone number\" to verify bank details submitted to enrol or update EFT. This is discretionary, and the number is public, not a previously established contact. Stripe enrollees change bank details under Stripe's controls [V wave 22]."
4. **§1.2 table, Fidelity Charitable (own ACH) row, B1 and B2 cells.**
   - **Find:** "| **Not stated** | Not stated. Two named contacts receive the Grant Details Report |"
   - **Replace with:** "| **Partial:** \"we may call your organization's publicly available phone number to verify banking and/or contact information\", for enrolments and updates ([FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)); discretionary, and to a public number [V wave 22] | Not stated. Two named contacts receive the Grant Details Report |"
5. **§1.2 table, same row, Other controls cell.**
   - **Find:** "• Two grant IDs or check numbers from the last 3 years"
   - **Replace with:** "• Two grant IDs, two check numbers or a reference number from the last 3 years (first-time grantees: unspecified additional verification) [V wave 22]"
6. **§1.3, reading 1.**
   - **Find:** "These defeat a pure email request but not an attacker who holds stolen grant letters. No callback is published."
   - **Replace with:** "These defeat a pure email request but not an attacker who holds stolen grant letters. Fidelity's FAQ adds a discretionary callback to the charity's publicly available number; whether it is applied to every bank change is not stated [V wave 22]."
7. **§7, status line (append after item 5).** "Validation wave 22: proposals 1, 3, 4 and 5 are verified and applied (V22-27 to V22-30). Proposal 2 is applied as batch 37C's reading; the 11 outlines were not re-read item by item."


## Pointer: DAFCP investigation (2026-11-20) — not yet validated

P-ANL-06 and P-ANL-09 (DAFCP rows) are extended in [research/dafcp-investigation-2026-11-20/](../dafcp-investigation-2026-11-20/00-README.md):
- The NPT instructor is confirmed: Lisa Barr, Senior Vice President, Advisor Development.
- The 2025 certificate's sponsors are documented as co-developers of the 2025 certificate. They are not documented as DAFCP sponsors.
