# Queue batch 38 C: close-out checks on adviser-education faculty (P-B37C-03), DAFpay anonymity on platforms (P-B37C-01), probability samples (P-B37C-02), Chariot's "80%" (P-B36C-03), shared AI platform pricing (P-AIV2-04), complaint venues (P-CMP-10, P-CMP-08, P-B28-04, P-B29C-01) and nine quick checks

**Date:** 2026-11-15. Prepared by the batch 38 C agent. Files only: no commit, no push.

**Method:** Desk research from public sources, 2021 onward. This is research, not legal advice.
- No accounts, logins, form submissions, outreach, or API calls that need a key.
- GitBook's `?ask=` endpoint on Chariot's help centre was not used. Only static `.md` pages were read.
- robots.txt was read on every host before fetching, and its rules were followed:
  - **openicpsr.org**, **give.org** and **glassdoor.com** disallow Anthropic agents, so they were not fetched.
  - **psidonline**, **hrs**, **hrsdata** and **simba.isr.umich.edu** returned 403 to robots.txt. **psidtest.isr.umich.edu** (PSID's mirror) allows all, so the PSID questionnaires were read there.
  - **play.google.com** allows `/store/apps/details` but disallows `/_` (the review-paging endpoint) and `/store/search`. Only the server-rendered details page was read. Package IDs were tested directly on that page.
  - **bbb.org** disallows every URL containing `?`, which includes its search, so BBB profiles cannot be discovered by an approved method.
  - **api.brokercheck.finra.org** returned 403 to robots.txt, so BrokerCheck was not used. **finra.org** disallows `fda_documents` but allows the monthly disciplinary-action PDFs under `/sites/default/files/YYYY-MM/`.
  - **projects.propublica.org** disallows `download-xml` and `display_990`. Organization pages were read there, and return XML came from the public `gt990datalake-rawdata` S3 mirror the repo already uses, which has no robots.txt.
  - **web.archive.org**: the connection was reset through the proxy, so robots.txt could not be read and Wayback was not used.
  - **support.givecampus.com** returned 403 to the article fetch, so GiveCampus appears only as search-index text [R].
- **Tags:**
  - [F] first-party document read.
  - [S] computed from repo data.
  - [R] search-index or secondary summary, not read first-hand.
  - [I] inference by this agent.
  - [U] unknown or not public.

**Read first (governing corrections applied):**
- [daf-user-complaints-deep-research.md](daf-user-complaints-deep-research.md), with waves 4 and 14.
- [queue-batch37-controls-education.md](queue-batch37-controls-education.md), with wave 22. The `anonymous` flag rides in the same callback as name and email, and the DAFpay Security page says nonprofits see what the donor provided.
- [queue-batch36-anonymity-feeds-fees.md](queue-batch36-anonymity-feeds-fees.md), with waves 21 and 22.
- [ai-economics-replacement-analysis.md](ai-economics-replacement-analysis.md) and [ai-economics-v2-observed-costs.md](ai-economics-v2-observed-costs.md) §3.2 and §4.5, plus the labour-rate check.
- [failed-daf-startups-deep-research.md](failed-daf-startups-deep-research.md), with wave 4 (W4-10, W4-11 on Flipcause).
- [queue-batch28-ledgers-voids-cf-apps.md](queue-batch28-ledgers-voids-cf-apps.md) §5, with wave 13. Defect counts are "20 (18 excluding 2 feature regressions)".

---

## 0. Status of every item

| Item | Status | One-line reason |
|---|---|---|
| **P-B37C-03** DAFCP and DAF Forum faculty employers | **Partially answered** | The College publishes employers for only 7 of the 22 DAFCP instructors (via the Caspersen bio and the DAF Forum 2027 speaker page). None of the 7 works for a DAF sponsor, and 1 runs a DAF administrator. 1 of the 7 Forum speakers works for a sponsor (Thrivent Charitable). 15 instructors have no College-published employer |
| **P-B37C-01** platform-side anonymity for DAFpay | **Partially answered** | No platform documents an anonymous DAFpay path that hides identity from the nonprofit. Funraise disables "Anonymous" for DAFpay. Givebutter, Bloomerang and Donorbox say donor details sync to the nonprofit's records. Chariot's own DAFpay page says "DAF donor name and email provided in real-time". The Chariot export field for the anonymous case is still undocumented |
| **P-B37C-02** probability samples with a DAF item | **Answered for SCF 2025 and PSID 2023/2025. HRS is unreadable** | **SCF 2025** (October 2026 codebook): no DAF item. The only DAF text again excludes DAFs from the trust question. **PSID Section M 2023 and 2025:** no DAF item. The 2021 PSID questionnaire mirror is truncated before Section M. HRS hosts return 403 to robots.txt |
| **P-B36C-03** Chariot "80%" vs "$199/mo + 2.9%" | **Partially answered** | The current pricing page has no fee-free published tier. Fee-free volume can only sit in "Enterprise … custom volume-based pricing" [I]. The period is still undated. DPN's 990 cannot bound the fee share: it books $0 program-service revenue. Wayback was unreachable, so change over time could not be traced |
| **P-AIV2-04** price a shared DAF AI platform | **Partially answered** | Observed per-sponsor **core-platform** payments run $118k–$416k a year (median $204k, 17 sponsors, TY2024 990s). TIFIN Give takes 74% of GiveClear's non-investment operating cost. No vendor discloses an AI platform cost, so the $1.5–6m stays an assumption. Scenario table in §5 |
| **P-CMP-10** connector privacy, credential and fee complaints | **Partially answered** | The corpus holds 1 advocacy privacy critique, 1 credential/login complaint and 1 fee/middleman complaint about DAFpay. No complaint rate can be computed: denominators are absent and the venues differ |
| **P-CMP-08** venue access | **Partially answered** | **Google Play:** a server-rendered subset can be collected (31 reviews, 2021+, coded). **BBB:** search is robots-disallowed. **Give.org and Glassdoor:** disallow Anthropic agents. **CFPB:** narratives cannot be searched (batch 29) |
| **P-B28-04** Android defects | **Answered on a Google-selected subset** | On Fidelity Charitable Android, 5 of 12 reviews are launch crashes on v5.11–5.18 (2025-10 to 2026-08), so post-v5.0 defects persist on Android. One crash blocks sign-in. There are no explicit login-auth complaints. **Daffy has no Play listing:** `com.daffy.app` belongs to an unrelated developer |
| **P-B29C-01** adviser-channel complaint frame | **Partially answered (frame and pilot)** | Frame designed (§9). Pilot: 17 FINRA monthly disciplinary reports (2025-01 to 2026-11) contain no "donor-advised" text. BrokerCheck API and state AG logs are not robots-readable or public |
| **P-ANL-10** tax-motive gap and 2026 bunching | **Not public (yet)** | No 2026 contribution data split by adviser channel has been published. Fidelity's CY2025 report names no law-driven pre-funding |
| **P-ANL-12** adviser-associated vs adviser-initiated | **Partially answered** | Known: Fidelity 46.9% of investments adviser-managed (2025); DAFgiving360 77–78% of assets adviser-associated. Payout and transfer-out by adviser status are not public anywhere. No Vanguard figure was found |
| **P-VCM-05** Commonwealth departures and RCF outbound grants | **Not public (yet)** | ProPublica's latest RCF return is CY2024, and Commonwealth departures date from 2025 onward |
| **Q-B16** Daffy unit economics | **Partially answered** | Daffy Charitable Fund CY2024: operating cost $360k, 0 employees, "Fee Income" inside $141.6k of other revenue. Membership revenue is not in the fund's 990 and is presumably with the operating company [I]. Company P&L not public |
| **Q-B14** failed or exited DAF tech providers | **Answered** | Closed by [failed-daf-startups-deep-research.md](failed-daf-startups-deep-research.md) §1 (as corrected by W4-10 and W4-11) |
| **P-AGA-05** SOC reliance at NCF and Charityvest | **Not public** | No SOC or service-organization reference in the NCF or Charityvest audits (repo `sponsor-audit-notes.csv`). Foundation Source publishes no attestation (`vendor-assurance-scope-2026.csv`). A targeted search found none |
| **P-AGF-02** DAF dollars to DAFpay fees in 2025 | **Not public** | No platform-wide DAFpay dollar total. The "grew 46% in 2025 to over $5 million" line on Chariot's DAFpay page sits next to a customer quote and is ambiguous [I]. DPN, the only slice with a public 990, books no fee revenue. Its 990 is not audited: `FSAuditedInd` is false or 0 in TY2024 and TY2025. Its TY2025 return books $88,736 of “fees for services – other” (3.02% of $2,941,073 contributions), an unnamed expense consistent with the 2.9% fee [V wave 37B] |
| **P-CON-08** renewal calendar | **Partially answered** | Public terms exist only for Ren (1-year renewals, 60-day notice), Ren iPhi (12-month auto-renew; notice drafted "thirty (60) days") and NPact (3-year initial term, 1-year renewals, 90-day notice). Sponsor-specific start dates are not public. 8 dated migration events give only go-live anchors |

---

## 1. P-B37C-03: who teaches the DAFCP, from the College's own pages

**Sources [F]:**
- [DAFCP page](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp): 22 faculty names. Only Paul M. Caspersen has a title and employer. The others show credentials only and link to LinkedIn, which was not used under this item's rule.
- [Caspersen bio](https://www.theamericancollege.edu/about-the-college/our-people/faculty/paul-m-caspersen). College bio URLs built the same way returned 404 for the other 21 names.
- [DAF Forum 2027 speakers](https://events.theamericancollege.edu/daf-forum/speakers-agenda): 7 speakers, each with a title and employer.
- [DAF Forum sponsors](https://events.theamericancollege.edu/daf-forum/sponsors): Premier Partners unchanged (DAFgiving360, Fidelity Charitable, NPT, Vanguard Charitable). No other tier is named.

| Person | On DAFCP faculty? | Employer as the College prints it | Class |
|---|---|---|---|
| Paul M. Caspersen | yes | Managing Director, The American College Center for Philanthropy and Social Impact; CAP Program Director | academic (the credential body) |
| Bryan Clontz | yes | Founder and President, Charitable Solutions, LLC | **processor or recordkeeper**. Dechomai Foundation, a national DAF sponsor, paid Charitable Solutions LLC $4,425,428 for "administrative services" in TY2024 ([990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543159349304249_public.xml); repo `form990-contractors-harvest-full.csv`) [S] |
| Ted Hart | yes | Global Donor-Advised Fund Expert and Author | independent consultant |
| Tiffany House | yes | Tax, Estate, & Charitable Strategist, Gift Planning Institute | independent consultant |
| Dan Heist | yes | Assistant Professor, Romney Institute, Brigham Young University | academic |
| Dana Holt | yes | CEO & Philanthropic Strategist, HOLT Consulting, LLC | independent consultant |
| Russ Willis | yes ("Russell A. Willis III") | Planned Gift Design Services | independent consultant |
| Nikki Johnson | no (Forum only) | Gift Planner, Charitable Giving Services, Thrivent Charitable | **DAF sponsor** |
| 15 other DAFCP instructors | yes | not published by the College | unknown |

**Scores [S]:**
- **DAFCP faculty, College-published employers only:** 7 of 22 known.
  - DAF sponsor: 0 of 7. Processor or recordkeeper: 1. Independent consultant: 4. Academic: 2.
  - Batch 37C identified one of the 15 unknown instructors as an NPT SVP, from NPT's page rather than the College's. Counting that outside source, the sponsor tie is 1 of 8 known.
- **DAF Forum 2027 speakers:** 1 of 7 at a sponsor (Thrivent Charitable), 1 at a DAF administrator, 4 consultants, 1 academic.
- **Premier sponsorship:** 4 of 4 Premier Partners are the largest national sponsors (unchanged from batch 37C).

**Reading [I]:**
- The sponsor exposure of the credential runs through **event money** (the Premier tier) more than through **faculty employment**, as far as the College discloses.
- The faculty is mostly consultants and planned-giving practitioners.
- With 15 of 22 employers undisclosed by the College, the faculty share cannot be stated with confidence. Bounds: 0–68% sponsor-tied (0 known; 15 unknown out of 22).

## 2. P-B37C-01: what each platform says the nonprofit sees

| Platform | (a) How anonymity is set on the form | (b) Platform donor record for a DAFpay gift | (c) Chariot export | Source | Tag |
|---|---|---|---|---|---|
| **Funraise** | "Anonymous" is listed among Giving Form features "not available with DAFpay" | The supporter is the DAF institution; the human donor gets a **soft credit** | Fee detail is in Chariot; "Any status update in Chariot will be synced" | [help, 2026-01-30](https://help.funraise.io/en/articles/12142901-accept-daf-donations-with-dafpay) | F |
| **Fundraise Up** | not addressed | "By default, the supporter who recommended the grant is recorded as the donor". Four CRM integrations can switch this to fund-as-donor with the supporter as soft credit | Export carries the DAF Tracking ID and External ID linking to the Chariot grant | [docs, modified 2026-10-30](https://fundraiseup.com/docs/dafpay/) | F |
| **Givebutter** | not addressed | "The donor will be prompted to enter their contact information". The Transactions page shows "all your DAF donations, including donor information" | not addressed (Tracking ID only) | [help, 2026-10-06](https://help.givebutter.com/en/articles/6764835-how-to-use-givebutter-s-dafpay-donation-method) | F |
| **Bloomerang** | not addressed for DAFpay. The generic help uses a "Recognition Name" of "Anonymous" or an "Anonymous Donors" constituent for gifts with no donor record | "supporters share their details on your donation form up front. Bloomerang CRM then syncs the donor and gift only after the gift is confirmed as received" | not addressed | [DAFpay post, published 2026-10-23](https://bloomerang.com/blog/dafpay); [anonymous-gift help, 2026-10-12](https://help.bloomerang.com/en/articles/12632501-how-do-i-make-a-donation-anonymous) | F |
| **Donorbox** | not addressed | "View all gift and donor details in your Donorbox dashboard, as these are synced automatically" | not addressed. Fees stated as "4.5% … a 1.6% Donorbox platform fee and a 2.9% Chariot fee" | [DAF page, undated](https://donorbox.org/explore/donor-advised-fund-donations) | F |
| **BetterWorld** | not addressed (DAFpay is one-time only) | not addressed | not addressed | [donor help, 2026-03-31](https://help.betterworld.org/en/articles/13764053-how-to-make-a-donation-using-dafpay) | F |
| **GiveCampus** | not addressed | Search summary: schools receive "the same biographical information on DAFpay donors as any other gift" | not addressed | [support article](https://support.givecampus.com/hc/en-us/articles/30078146512919-Accepting-DAF-Gifts-on-GiveCampus) returned 403 | R |
| **Chariot (vendor)** | Retired article (404): "Every DAFpay gift requires an email address … if your donation form allows for gifts to be submitted anonymously, then the donation will also be anonymous via DAFpay" | Live DAFpay page: "DAF donor name and email provided in real-time" | — | [retired article](https://intercom.help/givechariot/en/articles/8706359-does-dafpay-support-anonymous-donations) [R]; [DAFpay page](https://givechariot.com/dafpay.md) [F] | F/R |

**Reading [I]:**
- At the four platforms that address the point, the nonprofit-side record keeps the donor's identity for a DAFpay gift (Fundraise Up, Givebutter, Bloomerang, Donorbox). Funraise is the exception: it records the DAF as the supporter but still soft-credits the human donor.
- Funraise **removes the anonymous option** for DAFpay altogether.
- No platform states that an anonymous DAFpay gift arrives without name and email.
- The only statement that anonymity carries through is a retired Chariot article [R]. It conditions anonymity on the *form* allowing anonymous submissions, and in the same breath it requires an email address.
- Combined with batch 37C, **effective anonymity from the nonprofit is not documented anywhere in the nonprofit-side stack**. At most, recognition-level anonymity is handled inside the nonprofit's CRM (Bloomerang's "Recognition Name").
- (c), the Chariot export field values for the anonymous case, remains undocumented [U].

## 3. P-B37C-02: probability samples

| Survey | Wave read | DAF item? | Evidence |
|---|---|---|---|
| **SCF 2025** | Codebook, "final public version (October 2026 version)" | **No.** The wording is unchanged from 2022: X6830 code 10, "Charitable remainder trust: does not include donor-advised funds where R has surrendered all benefit from the asset", and "FOR THE PUBLIC DATA SET, CODE 10 IS COMBINED WITH 'YES' RESPONSES FOR X6828". The giving items are X5822/X5823 (gifts of $500 or more "During 2024", amount) and X7660/X7661 ("any sort of charitable trust or foundation", value; includes CRTs). There is no DAF instruction | [codebk2025.txt](https://www.federalreserve.gov/econres/files/codebk2025.txt), lines about 19425–19455 and 31486–31535 [F] |
| **PSID Section M 2023** | Full questionnaire | **No.** M2–M12 ask donation amounts by purpose (religious, combined-purpose including "your local community foundation", basic needs, health, education, and so on). The intro defines donations as "money, assets, property or goods, whether made directly to the organization, through payroll deduction, or on the internet, such as crowdfunding". There is no item on giving vehicles | [q2023.pdf](https://psidtest.isr.umich.edu/documents/psid/questionnaires/q2023.pdf) [F] |
| **PSID Section M 2025** | Full questionnaire | **No.** Same structure, M2–M12G, then "End SECTION_M". No "donor-advised", "DAF" or "giving fund" anywhere in the 557 pages | [q2025.pdf](https://psidtest.isr.umich.edu/documents/psid/questionnaires/q2025.pdf) [F] |
| PSID 2021 | Mirror PDF has 161 pages; its TOC puts Section M at p. 465 | unverified (truncated copy) | [q2021.pdf](https://psidtest.isr.umich.edu/documents/psid/questionnaires/q2021.pdf) [F] |
| HRS 2022/2024 | — | unverified (hrs and hrsdata robots 403; openICPSR disallows Anthropic agents) | [U] |
| BofA Study of Philanthropy 2025 | press summaries only | Bundles DAFs with other "giving vehicles" (24% of affluent households). n = 1,514, described as nationally representative. A bank-commissioned study | [ml.com summary](https://www.ml.com/articles/bank-of-america-study-of-philanthropy.html) [R] |

**Reading [I]:**
- Two flagship U.S. probability samples (SCF 2025 and PSID 2023/2025) do not measure DAF holding or DAF-routed giving.
- In PSID, a DAF grant reaches the data only as a gift to its end purpose, if the respondent counts it at all. Grant timing differs from contribution timing, so PSID giving cannot separate DAF contributions from DAF grants.
- The repo's penetration figures therefore still have no probability-sample benchmark.

## 4. P-B36C-03: Chariot's "80%" against its prices

**What is public now [F]:**

1. **Chariot help, [OAuth For DAF Sponsors](https://help.givechariot.com/dafpay/oauth-for-daf-sponsors.md)** (re-read 2026-11-15; text unchanged from batch 36C):
   - "An annual Chariot subscription, which includes … a significant amount of free DAFpay volume. For these organizations, there are no per transaction fees generated by DAFpay use. This is most common for large nonprofits and has made up 80% of DAFpay usage in the past year."
   - No date, no metric.
2. **[DAFpay Security](https://help.givechariot.com/dafpay/dafpay-security.md):**
   - "Nonprofits also have the option to pay zero processing fees as part of a Chariot subscription plan, which come with a set limit of included DAFpay volume."
3. **[Pricing page](https://www.givechariot.com/chariot-pricing)**, read 2026-11-15:
   - Components "$199/mo + 2.9% fee per donation, Billed annually".
   - Free platform access "Generally 2.9% fee* on donations facilitated".
   - "Need Enterprise? Built for scale. Get custom volume-based pricing". No published tier is fee-free.
4. **[DAFpay Network help](https://help.givechariot.com/dafpay/dafpay-network.md):**
   - Names DPN with "EIN: 93-1372175".
   - "Standard DAFpay fees of 2.9% apply to these donations".
   - Gifts via The Chesed Fund, CauseMatch, ChabadOne, Charidy or Rayze.It "will continue to be disbursed via the DAFpay Network, even after you've claimed your Chariot Deposit Account".

**DAFpay Network Inc (EIN 93-1372175), Form 990 [F]:**

| | TY2023 | TY2024 | TY2025 |
|---|---|---|---|
| Filing | 990-N (< $50k receipts) | 990, filed 2025-03-13 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202510729349301206_public.xml)) | 990, ReturnTs 2026-05-18T19:51:48-06:00 (XML public in IRS TEOS `2026_TEOS_XML_05B`; not in the S3 mirror at 2026-11-19) [V wave 37B] |
| Contributions | — | $1,199,247 | $2,941,073 |
| Program-service revenue | — | **$0** | $0 |
| Grants paid | — | $831,404 (largest: Chai Lifeline $372,832; Effective Ventures Foundation $155,818) | $2,178,671 (TY2025 XML, Part IX line 1; 104 Schedule I lines totalling $1,324,158) [b38c-03] [V wave 41A] |
| Fees for services (other) | — | $18,345 | $88,736 (TY2025 XML, IRS TEOS `2026_TEOS_XML_05B`) [V wave 37B] |
| Self-description | — | "THE CHARITY OPERATES AS A SPONSOR TO DONOR ADVISED FUNDS…" | — |
| Location / officers | — | Boone, IA. Unpaid directors: Salomon Serfati (principal officer), Yitzhak Moshe Bengualid Goldstein, Laivi Forta | same |

Source: [ProPublica organization page](https://projects.propublica.org/nonprofits/organizations/931372175).

**Reconciliation [I]:**
- **The pricing pages and the 80% fit together only if the fee-free volume sits in Enterprise or custom contracts.** The only *published* subscription (Components, $199/mo) still carries 2.9%. "Subscription" in the 80% sentence must therefore mean negotiated plans with an included-volume allowance.
- **The metric is probably dollars, not gifts.** The sentence ties fee-free use to "large nonprofits". Pan-Mass Challenge alone passed $5m of DAFpay in a calendar year (Chariot year-in-review, [R]), so a few large subscribers can dominate dollar volume. This is not confirmed.
- **DPN's 990 cannot bound the fee-bearing share:**
  - In TY2024 it books no program-service revenue and only $18k of other fees (1.53% of contributions). The TY2025 return revises this. Its XML is public in IRS TEOS `2026_TEOS_XML_05B` and was read in wave 37B. DPN records contributions gross ($2,941,073) and books $88,736 of “fees for services – other” (3.02%). The 2.9% on DPN-routed gifts therefore appears as an unnamed DPN expense, not netted before receipt. TY2024's 1.53% remains unexplained [V wave 37B]
  - DPN carries only unclaimed-nonprofit and five named Jewish-giving-platform flows, about $1.2m in TY2024 and $2.9m in TY2025. On DPN’s own description these are DAF grants that it receives and regrants. It answers Part IV line 6 “No” and files no Schedule D, so its flows belong in neither sponsor nor processor totals; adding them would double-count sponsor grants (b40n14-03-b38c-03 §3) [b38c-03] [V wave 41A]
  - Upper bound on fees on that slice, if all of it bore 2.9% grossed on receipt: about $36k (TY2024) and $88k (TY2025) [I].
- **Change over time:** not traceable. Wayback could not be reached, and GitBook page history is not public. The text is unchanged between batch 36C (2026-11-14/15) and this read.

## 5. P-AIV2-04: pricing a shared DAF AI platform from disclosures

### 5.1 Observed prices sponsors pay platform vendors (TY2024 Form 990 Part VII-B; top-5 contractors over $100k only, so censored below $100k) [S]

Source: repo [`form990-contractors-harvest-full.csv`](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv), each row linked to its XML.

| Vendor → sponsor (TY2024) | Amount | Service as filed |
|---|---|---|
| Stellar (Ren) → Cleveland Foundation | $416,391 | Hosting & customizations, software |
| Stellar → Christian Community Foundation | $366,469 | Computer & software |
| Foundant → Columbus Foundation | $344,614 | Operating platform services |
| Stellar → Catholic Community Foundation | $311,878 | Payment processing |
| Stellar → Thrivent Charitable | $270,307 | Technology services |
| Ren PSG → T. Rowe Price Program | $259,797 | Technology |
| NPact → American Endowment Foundation | $249,500 | Software development |
| Stellar → ImpactAssets | $232,315 | Technology services |
| Ren → CF Greater Des Moines | $203,595 | Software services |
| Stellar → Community Foundation (EIN 58-1723645) | $203,119 | Software |
| Foundant → Winston-Salem Foundation | $187,344 | Computer support & consulting |
| TIFIN Give → GiveClear Foundation | $185,921 | Technical and charitable support |
| Stellar → Greater Green Bay CF | $185,735 | ERP system provider |
| Stellar → Goldman Sachs Charitable Gift Fund | $172,604 | Information technology |
| Foundant → Denver Foundation | $158,850 | Financial activities software |
| Ren → JF Greater Seattle | $155,909 | Endowment platform service |
| Stellar → CF Acadiana | $118,458 | Software support |
| **17 core-platform relationships** | **median $203,595; IQR $179k–$291k; range $118k–$416k** | |

**Outliers, excluded from the median:**
- Stellar → NCF: $2,495,829. NCF also paid Salesforce $1,356,801.
- Full-administration contracts: Renaissance Administration → RCF $19.23m; RenPSG → MS GIFT $14.93m; Benevity → AOGF $54.45m; CyberGrants → CAF America $8.29m.

**First-party price list [F]:** GiveClear's DAF administrative fee for TIFIN Give accounts is 0.60% on the first $1m, 0.20% on the next $1.5m, and 0.10% above $2.5m ([TIFIN Give help, 2025-09-24](https://intercom.help/give-ria/en/articles/9820884-tifin-give-fee-structure)).

**Vendor capture, one observed case [S]:**
- GiveClear's TY2024 operating cost excluding investment management was $250,440 (repo `sponsor-cost-structure.csv`).
- Its payment to TIFIN Give LLC was $185,921, which is **74% of that cost**.
- That is a vendor share of the sponsor's own operating budget, not the τ (fee share of AI savings) in v2 [I].

**Not public [U]:**
- AI-specific prices from Ren, TIFIN, Foundation Source/Vennfi, Blackbaud or Benevity. Searches of pricing pages and press found none.
- Platform build or run costs. No public RFP with an awarded DAF-platform value was found in this pass.

### 5.2 Scenarios (transparent; inputs from v2 §3.2 and §4.5, nothing new invented) [I]

- **Formula:** break-even sponsors N = P / (τ·V − c).
  - V = v2 p50 sponsor AI value.
  - τ ∈ {0.2, 0.5}.
  - c = per-sponsor vendor cost, $10k or $50k (inside the v2 range).
  - P = platform cost, $1.5m or $6m.

| Archetype (V) | τ | AI fee τ·V | Fee as % of observed median core-platform payment ($204k) | N at P=$1.5m, c=$10k | N at P=$6m, c=$10k | N at P=$1.5m, c=$50k | N at P=$6m, c=$50k |
|---|---|---|---|---|---|---|---|
| NAT_LARGE ($1.18m) | 0.2 | $236k | 116% | 7 | 27 | 8 | 32 |
| NAT_LARGE | 0.5 | $590k | 290% | 3 | 10 | 3 | 11 |
| NAT_MID ($131k) | 0.2 | $26k | 13% | 93 | 370 | never | never |
| NAT_MID | 0.5 | $66k | 32% | 27 | 108 | 97 | 387 |
| CF_1BN ($164k) | 0.2 | $33k | 16% | 66 | 263 | never | never |
| CF_1BN | 0.5 | $82k | 40% | 21 | 83 | 47 | 188 |
| CF_250M ($42k) | 0.5 | $21k | 10% | 136 | 545 | never | never |

**Reading [I]:**
- At mid-size sponsors the AI fee the model supports ($26–82k) would be a 13–40% uplift on the median observed core-platform contract. That is plausible as an add-on sold by an incumbent platform vendor. It is far too small to pay for a standalone AI platform unless the vendor already carries the platform cost.
- This favours the **incumbent-vendor add-on** route (Ren/Stellar, Foundant, NPact, TIFIN) over a separate shared AI utility. The incumbent's P is partly sunk and its c is near zero.
- The scenario cannot test this, because P is not disclosed.
- **Recommended change to the v2 assumptions (not applied):** keep P at $1.5–6m labelled as an assumption. Add the observed **$118k–$416k core-platform price band** as the ceiling context for the per-sponsor fee. Note that c above about $33k makes CF_1BN break-even impossible at τ = 0.2.

## 6. P-CMP-10: connector complaints

From [`daf-user-complaints-corpus.csv`](../../data/mission-2026-11-14/daf-user-complaints-corpus.csv), Chariot/DAFpay records:
- 5 praise reviews (App Store).
- **CMP-094** (2026-07-07): login bugs and Fidelity integration failures. This is credential/login.
- **CMP-147** (2026-11-02, Trustpilot): "unnecessary middleman", forced account opening, cannot self-close. This is fee or pass-through.
- **CMP-242** (advocacy, c.2024): the [IPS / Inequality.org](https://inequality.org/article/new-donor-advised-fund-tech-raises-old-concerns/) critique of anonymity and credential sharing. This is privacy.

No donor-filed privacy complaint about DAFpay was found. No new connector complaint appears in the Google Play sample (§7).

The design evidence is documentary rather than complaint-based:
- Chariot's page promises "DAF donor name and email provided in real-time" [F].
- The §2 platform pages show identity reaching the nonprofit.

**Why no rate [I]:** DAFpay users per sponsor are not public, connector reviews sit on different venues from sponsor reviews, and the counts are single digits. Any rate comparison would be noise.

## 7. P-CMP-08 and P-B28-04: Google Play, BBB, Give.org, Glassdoor

**Google Play collection method:**
- The public details page (`/store/apps/details?id=…&hl=en_US&gl=US`, a robots-allowed path) embeds a Google-selected review subset in its `AF_initDataCallback` data.
- Paging reviews needs `/_/…batchexecute`, which robots.txt disallows, so the subset is all that can be collected.
- Package IDs were tested on the details path. `/store/search` is disallowed, so search could not be used to find them.

| App | Package | Developer | Rating / ratings | Downloads | Updated | Reviews rendered (2021+) |
|---|---|---|---|---|---|---|
| Fidelity Charitable | com.fidelity.charitable | Fidelity Investments | 3.8 / 29 | 5K+ | 2026-11-09 | 12 |
| Benevity | org.benevity.app | Benevity Inc | 3.2 / 94 | 50K+ | 2026-08-27 | 19 (plus 1 from 2020, excluded) |
| Pledger Charitable | com.pledger.donor | Pledger Charitable | 4.1 / 9 | 500+ | 2026-03-06 | 0 rendered |
| B Charitable | org.bcharitable.mobile | B Charitable, Inc. | none | 100+ | 2026-10-20 | 0 |
| Daffy | — | `com.daffy.app` is "Daffy S&D", Innovative Network (Pvt) Ltd, unrelated | — | — | — | excluded |

None of these IDs returned a listing: Vanguard Charitable, DAFgiving360/Schwab, Charityvest, Every.org, Groundswell, Endaoment, NCF, The Donors Fund, Givinga or Chariot. Absence of a listing is not proven by this, since only plausible package IDs were tested.

**Fidelity Charitable Android coding (taxonomy from batch 28; extension codes `data_integrity`, `network_error`) [S]:**

| Defect type | n | Versions | Dates |
|---|---|---|---|
| crash_on_launch | 5 | 5.11, 5.13, 5.17, 5.17, 5.18 | 2025-10-31 to 2026-08-14 |
| feature_regression | 1 | 5.16 | 2026-05-28 ("can no longer create recurring grants") |
| data_integrity | 1 | 5.12 | 2026-01-06 (bank details deleted, transactions reversed) |
| not a defect | 5 | 5.0, 5.2, 5.2, —, 5.17 | 3 praise, 2 feature gaps |

**Reading [I]:**
- On iOS, batch 28 found no login complaint after v5.0 and a one-day hotfix for 5.21.
- On Android, the Play subset shows **post-v5.0 launch crashes over about 10 months**. One review says the problem lasted "months", and one says the crash blocks sign-in. Several name 2026 devices (Galaxy S26, Pixel 10).
- So "login failures stop after v5.0" holds for explicit login-auth complaints on both platforms. **Fidelity's mobile defects did not stop after v5.0 on Android, however. They shifted to launch crashes.**
- The Android 5.16 recurring-grant regression also postdates the iOS 5.16 restore date in batch 28.
- Google selects which reviews render, so these are not frequencies.
- **Benevity** (19 reviews, 2021+):
  - 4 network errors, 3 login/access (one is SSO structural: a retiree asked for work credentials), 2 security_ux (root-detection, one framed as privacy), 1 hang, 1 launch crash.
  - 4 service complaints, including "$100 minimum before disbursing … to charities that accept donations through checks" and 2-month disbursement.
  - 1 feature gap and 3 praise.

**Other venues:**
- **BBB:** profile pages are allowed, but discovery needs `/search?…`, which is disallowed for all agents. A web search found no BBB profile for any national sponsor [R].
- **Give.org:** robots.txt disallows ClaudeBot and anthropic-ai, so it was not fetched.
- **Glassdoor:** robots.txt `Disallow: /` for ClaudeBot, so it was not fetched.
- **CFPB:** unchanged from batch 29 §2.4. Narrative search is not available through the public API.

## 8. Quick checks (detail for §0)

- **P-ANL-10:**
  - Fidelity's [2026 Giving Report](https://www.fidelitycharitable.org/insights/2026-giving-report.html) gives $18.3bn of grants in 2025 (+23%) and says only that "Donors took advantage of tax-smart donation strategies". It does not mention OBBBA or the 0.5% floor.
  - Adviser commentary urged 2025 pre-funding ([Kiplinger](https://www.kiplinger.com/personal-finance/charity/charitable-giving-changes-in-obbb-one-big-beautiful-bill)) [R].
  - Testing the tax-motive gap needs 2026 flows split by adviser channel. No sponsor publishes that, and CY2026 reports arrive in 2027.
- **P-ANL-12:**
  - Fidelity CIAP (adviser-managed) investments were 46.9% of the total in 2025. DAFgiving360's adviser-associated share is 77–78% of assets ([queue-batch37-filing-questions.md](queue-batch37-filing-questions.md) §0) [F/S].
  - No sponsor publishes payout or transfer-out rates by adviser status. The "initiated" share remains the 2018 survey figure (wave-corrected in the analyst file).
- **P-VCM-05:** The latest RCF return on ProPublica is CY2024 ([RCF](https://projects.propublica.org/nonprofits/organizations/352129262)). CY2025 is not posted, and CY2026 will not be filed before late 2027.
- **Q-B16:**
  - Daffy Charitable Fund CY2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513209349301201_public.xml)) [F]:
    - Contributions $194.0m; program-service revenue $0; other revenue $141,564, including "Fee Income".
    - Operating cost $360,305; IT $153,483; 0 employees.
    - 8,905 accounts and $334.5m in DAF assets (repo).
  - **Arithmetic bound only [I]:** 8,905 accounts × $3–$20 a month comes to $0.32–2.14m a year at the tiers in [competitive-history-timelines.md](competitive-history-timelines.md). Who receives membership fees, and the company's costs, are not public.
- **Q-B14:** answered by [failed-daf-startups-deep-research.md](failed-daf-startups-deep-research.md). The modal exit is acquisition by Ren, Foundation Source or TIFIN. Losses arose in the payments or custody layer (Ammado, Flipcause per W4-10/11, SDG Impact Fund).
- **P-AGA-05:** No SOC or service-organization statement appears in NCF's 2025 or Charityvest's FY2024 audits (repo `sponsor-audit-notes.csv`). Foundation Source has no trust or security page (`vendor-assurance-scope-2026.csv`). A search for "Foundation Source" with "SOC 1", "SOC 2" or "SSAE 18" found nothing [R].
- **P-AGF-02:**
  - No platform-wide 2025 DAFpay dollar total is public.
  - Chariot's [DAFpay page](https://givechariot.com/dafpay.md) carries "DAFpay volume grew 46% in 2025 to over $5 million" next to a customer CFO quote. Read as one customer's figure [I], since one nonprofit (PMC) passed $5m on its own [R].
  - No sponsor policy on donor-covered fees was found (unchanged).
  - DPN is the only slice with a public 990 (§4). That 990 is not audited: `FSAuditedInd` is false or 0 in TY2024 and TY2025 (wave 37B) [b38c-03] [V wave 41A]
- **P-CON-08:**
  - Public term structures are in [`vendor-data-rights-matrix.csv`](../../data/mission-2026-11-14/vendor-data-rights-matrix.csv). Ren and RCF: 1-year renewals, 60-day notice. Ren iPhi: 12-month auto-renew, notice drafted "thirty (60) days". NPact: 3-year initial term, 1-year renewals, 90-day notice (§8.1). TIFIN, Foundation Source, Foundant, Blackbaud, Chariot, Givinga: not public.
  - Sponsor go-live dates exist for 8 migration events in [`cf-vendor-migrations-2022-2026.csv`](../../data/mission-2026-11-14/cf-vendor-migrations-2022-2026.csv) (Foundant 2023–2026; akoyaGO undated).
  - **[I]** An NPact customer that went live in year t reaches its first exit window about 90 days before t+3. This calendar can be built only for named go-lives.

## 9. P-B29C-01: sampling frame for adviser-channel sponsor complaints

| Layer | Unit | Public, robots-compliant access | Pilot result (2026-11-15) |
|---|---|---|---|
| FINRA monthly "Disciplinary and Other FINRA Actions" PDFs | Each action, with a keyword screen for "donor-advised", "donor advised", sponsor names, "charitable gift fund" or "charitable" | Yes: `finra.org/sites/default/files/YYYY-MM/disciplinary-actions-<month>-<year>.pdf`. The 2025–2026 naming resolved 17 of 23 months. The pre-2025 naming differs and was not resolved | **0 DAF mentions** in about 160k words. 1 "charitable" hit: an Aug-2026 case of an undisclosed outside business activity referring customers to "a leveraged charitable giving program" (not a DAF) |
| FINRA BrokerCheck / Disciplinary Actions Online | Rep or firm disclosures for affiliated broker-dealers (Morgan Stanley for MS GIFT; Merrill for BofA; LPL/Commonwealth for RCF programs) | **No.** api.brokercheck robots 403; `fda_documents` disallowed | not run |
| SEC IAPD (adviserinfo.sec.gov) | Adviser disclosures | Partly. Firm pages are allowed, but brochures are disallowed and there is no keyword search | not run |
| State AG / charity-regulator complaint logs | Complaints naming a sponsor | Generally not published. Only enforcement releases are public (already in the corpus, e.g. the 2026 SPLC holds and the Georgia SDG order) | not run |
| FINRA arbitration awards | Awards naming a DAF | A search engine surfaced one DAF defence verdict from a 2012 contribution (pre-2021, [Marshall Dennehey](https://marshalldennehey.com/major-victories/defense-verdict-secured-finra-arbitration-matter)) [R] | out of window |

**Reading [I]:** Regulator venues yield almost nothing on adviser-channel DAFs, which is consistent with batch 29. X6 for A3 sponsors should stay U, or rest on litigation and enforcement only. No venue examined supplies complaints at the volume consumer venues do.

---

## 10. Limits

- **The Google Play sample is Google-selected** (the "most relevant" subset on the details page). Counts describe that subset, not app-wide frequencies.
- **Faculty employers** come only from College pages. LinkedIn and employer sites were excluded by the item's rule, apart from batch 37C's NPT note.
- **DPN TY2025** was first read from ProPublica’s summary. Its XML is public in IRS TEOS `2026_TEOS_XML_05B` and was read in wave 37B and in b40n14-03-b38c-03; it was still not on the GivingTuesday mirror on 2026-11-20 [b38c-03] [V wave 41A]
- **Wayback** was unreachable, so no time series of Chariot pages was possible.
- **AI scenario** values use v2 p50 values. They are illustrations, not new estimates.

## 11. Source register

| # | Source | Date / version | Used in | Tag |
|---|---|---|---|---|
| S1 | [DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp); [Caspersen bio](https://www.theamericancollege.edu/about-the-college/our-people/faculty/paul-m-caspersen) | live 2026-11-15 | §1 | F |
| S2 | [DAF Forum speakers](https://events.theamericancollege.edu/daf-forum/speakers-agenda); [sponsors](https://events.theamericancollege.edu/daf-forum/sponsors) | live 2026-11-15 | §1 | F |
| S3 | Dechomai Foundation TY2024 990 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543159349304249_public.xml)) via repo harvest | filed 2025 | §1 | F/S |
| S4 | [Funraise DAFpay help](https://help.funraise.io/en/articles/12142901-accept-daf-donations-with-dafpay) | 2026-01-30 | §2 | F |
| S5 | [Fundraise Up DAFpay docs](https://fundraiseup.com/docs/dafpay/) | modified 2026-10-30 | §2 | F |
| S6 | [Givebutter DAFpay help](https://help.givebutter.com/en/articles/6764835-how-to-use-givebutter-s-dafpay-donation-method) | 2026-10-06 | §2 | F |
| S7 | [Bloomerang DAFpay post](https://bloomerang.com/blog/dafpay); [Bloomerang anonymous-gift help](https://help.bloomerang.com/en/articles/12632501-how-do-i-make-a-donation-anonymous) | 2026-10-23/29; 2026-10-12 | §2 | F |
| S8 | [Donorbox DAF page](https://donorbox.org/explore/donor-advised-fund-donations) | undated, live | §2 | F |
| S9 | [BetterWorld donor help](https://help.betterworld.org/en/articles/13764053-how-to-make-a-donation-using-dafpay) | 2026-03-31 | §2 | F |
| S10 | [GiveCampus support article](https://support.givecampus.com/hc/en-us/articles/30078146512919-Accepting-DAF-Gifts-on-GiveCampus) | 403; search summary | §2 | R |
| S11 | [Chariot DAFpay page](https://givechariot.com/dafpay.md); retired [anonymity article](https://intercom.help/givechariot/en/articles/8706359-does-dafpay-support-anonymous-donations) (404) | live; retired | §2, §8 | F; R |
| S12 | [SCF 2025 codebook](https://www.federalreserve.gov/econres/files/codebk2025.txt) | October 2026 public version | §3 | F |
| S13 | PSID questionnaires [2021](https://psidtest.isr.umich.edu/documents/psid/questionnaires/q2021.pdf), [2023](https://psidtest.isr.umich.edu/documents/psid/questionnaires/q2023.pdf), [2025](https://psidtest.isr.umich.edu/documents/psid/questionnaires/q2025.pdf) | PSID mirror | §3 | F |
| S14 | [BofA Study of Philanthropy summary](https://www.ml.com/articles/bank-of-america-study-of-philanthropy.html) | 2025 | §3 | R |
| S15 | Chariot help: [OAuth For DAF Sponsors](https://help.givechariot.com/dafpay/oauth-for-daf-sponsors.md), [DAFpay Security](https://help.givechariot.com/dafpay/dafpay-security.md), [DAFpay Network](https://help.givechariot.com/dafpay/dafpay-network.md); [pricing](https://www.givechariot.com/chariot-pricing) | read 2026-11-15 | §4 | F |
| S16 | DAFpay Network Inc: [ProPublica](https://projects.propublica.org/nonprofits/organizations/931372175); [TY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202510729349301206_public.xml) | filed 2025-03-13; 2026-05-19 | §4 | F |
| S17 | Repo `form990-contractors-harvest-full.csv`, `sponsor-cost-structure.csv` (per-row XML links) | TY2024 | §5 | S |
| S18 | [TIFIN Give fee structure](https://intercom.help/give-ria/en/articles/9820884-tifin-give-fee-structure) | 2025-09-24 | §5 | F |
| S19 | Google Play details pages: [Fidelity Charitable](https://play.google.com/store/apps/details?id=com.fidelity.charitable&hl=en_US&gl=US), [Benevity](https://play.google.com/store/apps/details?id=org.benevity.app&hl=en_US&gl=US), [Pledger](https://play.google.com/store/apps/details?id=com.pledger.donor&hl=en_US&gl=US), [B Charitable](https://play.google.com/store/apps/details?id=org.bcharitable.mobile&hl=en_US&gl=US), [com.daffy.app (unrelated)](https://play.google.com/store/apps/details?id=com.daffy.app&hl=en_US&gl=US) | retrieved 2026-11-15 | §7 | F |
| S20 | robots.txt of bbb.org, give.org, glassdoor.com, openicpsr.org, play.google.com, api.brokercheck.finra.org, finra.org | read 2026-11-15 | method, §7, §9 | F |
| S21 | FINRA monthly disciplinary actions, e.g. [Oct 2025](https://www.finra.org/sites/default/files/2025-10/disciplinary-actions-october-2025.pdf), [Aug 2026](https://www.finra.org/sites/default/files/2026-08/disciplinary-actions-august-2026.pdf) (17 months, 2025-01 to 2026-11) | 2025–2026 | §9 | F |
| S22 | [Fidelity Charitable 2026 Giving Report](https://www.fidelitycharitable.org/insights/2026-giving-report.html) | 2026 | §8 | F |
| S23 | [RCF on ProPublica](https://projects.propublica.org/nonprofits/organizations/352129262) | latest CY2024 | §8 | F |
| S24 | Daffy Charitable Fund CY2024 990 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513209349301201_public.xml)) | filed 2025 | §8 | F |
| S25 | Repo files: `sponsor-audit-notes.csv`, `vendor-assurance-scope-2026.csv`, `vendor-data-rights-matrix.csv`, `cf-vendor-migrations-2022-2026.csv`, `daf-user-complaints-corpus.csv`, `queue-batch37-filing-questions.md` | 2026-11-14/15 | §6, §8 | S |

## 12. Data dictionary

### `data/mission-2026-11-14/play-store-reviews-2021plus.csv` (one row per review, 31 rows)

| Column | Type | Meaning |
|---|---|---|
| record_id | text | GP-001… |
| platform | text | "Google Play (US, en_US)" |
| sponsor_or_platform | text | Entity the app serves |
| app_name, package_id, developer | text | From the details page (developer from `/store/apps/developer?id=`) |
| app_rating_at_retrieval, app_rating_count_at_retrieval, downloads_band, app_updated_on | text | Header values on the details page at retrieval |
| review_id | text | Play review UUID |
| review_date | date | UTC date of the review timestamp |
| rating | int | 1–5 |
| app_version | text | Version the reviewer used (blank if not given) |
| defect_type | enum | Batch 28 enum (`login_auth`, `crash_on_launch`, `crash_in_flow`, `crash_post_auth`, `data_parse_error`, `hang_ui`, `update_distribution`, `feature_regression`, `security_ux`, `not_defect_praise`, `not_defect_fees`, `not_defect_service`, `not_defect_feature_request`, `not_defect_feature_gap`), plus the extensions `data_integrity` (data altered or lost) and `network_error` (app reports no or failed connection) |
| defect_summary | text | Neutral paraphrase |
| fix_class | enum | Batch 28 enum (`fixable_auth`, `fixable_release_qa`, `fixable_product`, `service_ops`, `structural_pricing`, `n/a`) |
| in_defect_count | yes/no | Counted as an app defect |
| developer_reply | yes/no | Developer reply present |
| sample_frame | text | Google-selected server-rendered subset; not complete, not random |
| notes | text | Context (post-v5.0 build, iOS comparison, extension code) |
| source_url, retrieved | text, date | Details page; 2026-11-15 |

### `data/mission-2026-11-14/queue-proposals-batch38c.csv`

Format per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md); 2 rows.

## 13. Proposals

- **P-B38C-01:** where DAFpay fees on DAFpay Network-routed gifts are booked (DPN TY2025 990 once its XML is public), and whether DPN acts as a sponsor or a pass-through.
- **P-B38C-02:** re-read the Fidelity Charitable Play page in 2027-Q1 to test whether the Android launch-crash cluster ended after 5.19–5.22.

## 14. Proposed corrections to repo text (not governing until validated)

1. **queue-batch28-ledgers-voids-cf-apps.md §5.4, point 2.**
   - **Append:** "On Android, the Google Play details-page subset (Google-selected) shows five post-v5.0 launch-crash reviews (v5.11–5.18, 2025-10 to 2026-08), one saying the crash blocks sign-in, so defect persistence after v5.0 is platform-specific [batch 38C]."
2. **queue-batch37-controls-education.md §3 table.**
   - **Add rows:**
     - "SCF 2025 (October 2026 codebook): no DAF item; X6830 code-10 exclusion unchanged."
     - "PSID Section M 2023 and 2025 (psidtest mirror): no DAF or giving-vehicle item [batch 38C]."
3. **daf-user-complaints-deep-research.md §3, BBB row.**
   - **Append:** "bbb.org robots.txt disallows URLs with '?', including search, so sponsor-profile discovery is not robots-compliant. give.org and glassdoor.com disallow Anthropic agents [batch 38C]."

## Validation corrections (wave 23, 2026-11-15) — governing
Source: [validation-wave23-report.md](validation-wave23-report.md); register `data/mission-2026-11-14/validation-register-wave23.csv`.

1. **§0, P-AIV2-04 row.**
   - **Find:** "Observed per-sponsor **core-platform** payments run $118k–$416k a year (median $204k, 17 sponsors, TY2024 990s). TIFIN Give takes 74% of GiveClear's non-investment operating cost."
   - **Replace with:** "Observed per-sponsor **core-platform** payments run $118k–$498k a year (median $218k, 18 sponsors, TY2024 990s, including Stifel Charitable → Ren $498,305 'OPS SYSTEM & SERVICE'). TIFIN Give's $185,921 equals 74% of GiveClear's non-investment operating cost, but the 990 does not show which Part IX lines carry it [V wave 23]."
2. **§5.1 table, summary row.**
   - **Find:** "| **17 core-platform relationships** | **median $203,595; IQR $179k–$291k; range $118k–$416k** | |"
   - **Replace with:** "| **17 core-platform relationships** | **median $203,595; IQR $179k–$291k; range $118k–$416k** (adding Stifel Charitable → Ren $498,305, omitted here: 18 relationships, median $217,955, range $118k–$498k [V wave 23]) | |"
3. **§5.1, vendor capture.**
   - **Find:** "Its payment to TIFIN Give LLC was $185,921, which is **74% of that cost**."
   - **Replace with:** "Its payment to TIFIN Give LLC was $185,921, which is **74% of that cost**. No Part IX line outside investment management (11f, $1.56m) is that large, so the payment is spread across lines or partly inside 11f; the ratio is an upper bound on the vendor's share of that budget [V wave 23]."
