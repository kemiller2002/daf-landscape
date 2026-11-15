# Batch 28: NetSuite ledgers (P-LSG-01), DonorCentral operator (P-NPP-04), DAF grant voids (P-PAY-03), community-foundation remittance (P-NPP-01), sponsor app defects (P-CMP-06)

**Date:** 2026-11-15. **Author:** batch-28 queue agent.
**Queue items:** P-LSG-01, P-NPP-04, P-PAY-03, P-NPP-01, P-CMP-06 (`data/mission-2026-11-14/research-priority-queue.csv`).
**Status:** public sources only. I logged in nowhere, submitted no forms, contacted no one and used no credentials. Structured reads were limited to these:
- the public iTunes Search/Lookup API and App Store customer-review RSS;
- public IRS e-file XML on the `gt990datalake-rawdata` S3 bucket (paced at about 1 request per second);
- public PDFs and pages.

Pages that refused scripted reads (pittsburghfoundation.org through curl, ZipRecruiter, Indeed, CareerBuilder, growyourgiving.org through curl) were not worked around. Where WebFetch could read a page, I used it. Where only a search-engine extract was available, the claim is marked [S].
**Recency rule:** every current-state claim rests on 2021+ evidence. Two pre-2021 documents turned up and are named, but not used: a 2018 CCF anonymity fact sheet and a 2019 GKCCF brochure.

**Read first and built on:**
- `queue-ledger-segment-npact-owner.md`, including its **wave-12 corrections**:
  - BroadWest's Texas status is "Right to Transact: NOT ESTABLISHED".
  - NPact privacy policy, "Last updated August 19, 2026".
  - NYCT is lowered to low-medium.
  - CCF's posting date is 2026-06-08, with Financial Edge listed as "preferred" only.
- `queue-nonprofit-side-panel.md`, including its **wave-12 corrections**:
  - Vanguard wording is "is now issuing Grant Payments with PayPal".
  - "No sponsor checked requires EFT today."
  - DAFgiving360's $50 minimum comes from a 2024 policy document.
  - MS GIFT FAQ cite.
  - NPT guide PDF metadata dated 2026-10-15.
- `daf-user-complaints-deep-research.md`, including its **wave-4 correction W4-16** (Fairbairn/Pinkert wording). That correction does not touch the app findings.
- `queue-payment-rails-cluster.md` §2–3 (Fidelity void and EFT text).

**Labels:**
- [F] first-party text read in full, or a filed government record
- [V] vendor statement or case study
- [S] search-engine extract (page not opened)
- [H] HTTP or bundle observation
- [I] inference

**Outputs:**
- `data/mission-2026-11-14/nonprofit-side-panel-2026-cf-supplement.csv`: 54 long-format cells, 10 community foundations × 5–6 fields.
- `data/mission-2026-11-14/daf-grant-voids-disclosures.csv`: 40 rows.
  - 22 rows are itemised void, refund or rescission figures, from 8 sponsors.
  - 16 rows record a "none found" result for a sponsor, or for sponsor-years that have no itemised figure.
  - 2 rows are audited-statement checks.
- `data/mission-2026-11-14/sponsor-app-defects-2021plus.csv`: 55 coded App Store reviews dated 2021 or later.
- `data/mission-2026-11-14/queue-proposals-batch28.csv`: P-B28-01 to P-B28-04.

---

## 0. Headline answers

| ID | Answer | Confidence |
|---|---|---|
| **P-LSG-01** | **Two of three confirmed; NCF not confirmed.** **SVCF: NetSuite is the finance system.** An NPact case study, published 2025-04-29 and quoting SVCF's SVP Finance, describes "a custom accounting application that would layer on top of NetSuite". SVCF instead co-developed NPact's **Fund Investment Tool (FIT)**, which now runs its fund allocations, fees and rebalancing on top of NetSuite [V]. **Pittsburgh: NetSuite + Salesforce is the current core ERP**, now under "remediation". The first-party CIO posting (deadline 2026-03-20) says "core ERP system encapsulated by NetSuite, Salesforce" [F]. **NCF: still low.** Salesforce is a 990 payee [F], and NetSuite appears only in aggregator snippets [S]. NCF also pays Ren/Stellar (iPhi) $2.50m (TY2024) [F], so its DAF ledger may be iPhi. The confirmed NetSuite + Salesforce assets are **$10.10bn** (SVCF $9.58bn + Pittsburgh $0.53bn). NCF's $5.46bn stays unresolved | High (Pittsburgh), medium-high (SVCF NetSuite; Salesforce at SVCF medium), low (NCF) |
| **P-NPP-04** | **NPact, which trades as Fusion Laboratories LLC, operates DonorCentral in 2026.** The evidence: NPact's product page "DonorCentral®: The Secure, Self-Service Donor Advised Fund Portal", "integrated with NPact's FIMS system", "Built on NPact's cloud platform" [F]; the 2022-09-12 release announcing the acquisition from Blackbaud [F]; NPact's SaaS terms (rev. 2025-08-26), which name "Manufacturer is Fusion Laboratories LLC / dba NPact" [F]; and the live bundle, which calls `*.donor.npact.com` and `auth0.donorcentral.com`, offers "NPact" alongside "BBID" as a user type, and embeds an NPact merchant agreement [H]. The Blackbaud SKY UX styling is a front-end legacy and does not show who operates the product. A sponsor tenant still linked in 2026: Calgary Foundation (`calgaryfoundation.donorcentral.com`) [F]. GWCF is replacing its "Donor Central Portal" with NPact's Foundation Cloud Community Portal; launch was moved to 2026-09-21 [F] | High |
| **P-PAY-03** | **Voided or refunded DAF grants show up only as Schedule O reconciling items, and only for 8 of 21 sponsors scanned (TY2021–24).** No sponsor gives counts, causes, or a split between checks and EFT. The largest series is Fidelity's "ADJUSTMENT FOR PRIOR YEAR VOIDED GRANTS": **$16.04m (FY2023), $16.59m (FY2024), $11.15m (FY2025)**, equal to **0.155%, 0.131% and 0.073%** of grants paid [F]. Other national sponsors: GS DAPF "GRANT REFUNDS" $9.18m (0.30%, TY2024); AEF "REFUNDED GRANTS" $4.06m and $2.61m (0.33%, 0.20%); Ayco $75k (0.02%). Community foundations run higher because their figures are entity-wide: CCF "RESCINDED GRANTS" 1.9–4.6% (TY2021–23), OCF "Grant and scholarship refunds" 0.8–2.3%, Columbus 0.02–0.24%. SVCF's "Grant Cancellations not offset" was $6.86m in TY2022, and the IRS XML masks the TY2023–24 figures. **NPT, DAFgiving360, Vanguard, MS GIFT, BofA, Ren, NCF, CCT, FFTC, GKCCF, NYCT, TBF and CFGA itemise nothing.** Fidelity's and NCF's audited statements carry no void note. **A void rate per check cannot be computed from public data** (§3.4) | High on the filed figures; low on any rate per check |
| **P-NPP-01** | All 10 community-foundation rows now carry evidence. **Minimum grant (7 of 10 published):** $100 at Columbus and CFGA, $200 at SVCF, $250 at CCT, NYCT and TBF, $500 at OCF. GKCCF says only that its "Board ... may designate" a minimum. FFTC and CCF publish none. **Cadence (5 of 10 published, plus Columbus's daily review):** SVCF 5–7 business days; CCT approves twice weekly and mails within 5–7 days; NYCT 3–5 business days; TBF weekly (Friday to Friday); OCF weekly [I]. **Fund name on the remittance:** a default at SVCF, FFTC, GKCCF (on the check), Columbus and NYCT; a four-way choice at TBF; not stated at CCT, OCF, CFGA or CCF. **Donor identity:** 9 of 10 publish a rule. FFTC and CFGA share the advisor's **mailing address** by default, SVCF only on request. **Void or uncashed-check rule: 0 of 10 publish one** | High on the cells filled; the void gap is itself a finding |
| **P-CMP-06** | **Defects in the 2021+ reviews concentrate in one app and one era.** Fidelity Charitable has 27 written reviews dated 2021 or later, 20 of them describing defects: **10 login/auth** (2021-09 to 2023-11, v3.0–4.2, half naming Face ID or loss of saved credentials after an update), **5 crashes**, 2 feature regressions, 1 parse error, 1 hang and 1 broken update prompt. **No login complaint follows the v5.0 rebuild of 2024-06-20.** In 2026 the defects were a launch crash on 5.21 on iOS 27 (2026-10-08), fixed by 5.21.1 the next day, and lost features (tax lots, recurring-grant edits). Daffy: 28 reviews, 1 defect (2FA by hardware key only, no TOTP). DAFgiving360 and Vanguard Charitable have **no standalone iOS app** (iTunes search, 2026-11-15). Causes [I]: auth and biometric breakage at iOS major releases (iOS 15 in 2021; Face ID in Dec 2022; iOS 27 in 2026), and thin release QA on a low-use app. The app has 24 ratings, against Daffy's 560. Its publisher is FMR ("Fidelity Investments"), which runs the Gift Fund's administration by contract (FS note 7). Fidelity shipped 25 versions in about 29 months; Daffy shipped 25 in about 5 | Medium (small n; RSS shows only the latest ~50 reviews) |

---

## 1. P-LSG-01: NetSuite + Salesforce at SVCF, NCF and Pittsburgh

### 1.1 Silicon Valley Community Foundation ($9.58bn): NetSuite confirmed [V]; Salesforce medium

NPact's customer story, "Fund Investment Tool (FIT): Silicon Valley Community Foundation", was published 2025-04-29 and modified 2026-10-20 ([npact.com](https://npact.com/customer-stories/silicon-valley-community-foundation/)) [V]. It says:
- "SVCF engaged a vendor to lead them through a digital transformation … This multi-year project included a new CRM, donor portal, gift management system, and finance system, as well as developing a custom accounting application that would layer on top of NetSuite for completing its complex investment administrative fee, income allocation, spending policy, and investment rebalancing calculations."
- "The project hit a major snag when the team's implementation partner cautioned SVCF against building a custom finance application on top of NetSuite."
- "SVCF partnered with NPact to co-develop FIT". FIT is "designed specifically to integrate with leading fund accounting solutions like NetSuite".
- It quotes Sarah Valencia, SVP Finance: "We have over 1,500 funds and allocating support fees, which is our main source of operating revenue." The story adds that grants "once processed on a weekly cadence can now be delivered daily".
- NPact's FIT page says it "Integrates with Oracle NetSuite or Blackbaud Financial Edge NXT®" and lists SVCF as a FIT customer story ([FIT page](https://npact.com/software/fund-investment-tool-fit/), modified 2026-11-12) [V].

**Reading [I].**
- NetSuite is SVCF's general ledger and finance system.
- DAF fund-level allocations, fees and rebalancing run in NPact FIT, which sits on NetSuite.
- The story names a new CRM and donor portal but not their vendor.
- Salesforce rests on the repo's portal signal (`donor.siliconvalleycf.org/s/` is an Experience Cloud path) and on [R] postings that name "NetSuite, Salesforce, Asana". Salesforce therefore stays medium.
- The "previous partners" are not named. Slalom is a 990 payee: $0.80m, $1.53m and $0.63m in TY2022–24 ([TY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349305759_public.xml)) [F]. That is consistent with Slalom being the implementer, but not proof.

**Taxonomy consequence.** SVCF fits "NetSuite + NPact FIT (+ Salesforce portal)" better than the bare SF_NETSUITE label. NPact's footprint by DAF assets is therefore larger than the repo's NPact/FIMS figures of $2.7bn (P-B28-01).

### 1.2 The Pittsburgh Foundation ($0.53bn): NetSuite + Salesforce confirmed [F]

The CIO posting ([pittsburghfoundation.org/cio](https://pittsburghfoundation.org/cio); no posting date shown; application deadline "March 20, 2026"; read through WebFetch, since direct curl returns 403) [F] says:
- The CIO ensures "smooth operation of the core ERP system encapsulated by NetSuite, Salesforce … and a cloud-based data warehouse".
- "Recently, the Foundation has undertaken a process with an external consultant to assist in remediation of the implementation of a technology plan".

**Reading.**
- NetSuite + Salesforce is in place as the core ERP, no longer only "implementing" as the repo's Systems Solutions Architect [R] cite has it.
- The implementation is being remediated [F].
- The repo's portal signal, Blackbaud NetCommunity, is therefore a legacy or transitional front end [I].
- Upgrade the confidence from low to **high**.

### 1.3 National Christian Foundation ($5.46bn): not confirmed

- **[F]** Salesforce Inc is a 990 Part VII-B payee: $1.17m, $1.13m and $1.36m in TY2022–24. Stellar Technology Solutions (iPhi, now Ren) was paid $1.20m, $1.45m and $2.50m. Avaap USA was paid $0.70m and Accenture $0.80m in TY2022. Intellinet received $4.63m in TY2024. Source: `form990-contractors-harvest-full.csv`, from the [TY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513109349303201_public.xml).
- **[S]** A search extract lists an NCF "NetSuite Administrator" posting on Indeed. A ZipRecruiter "Manager, Treasury Accounting Operations" posting lists "NetSuite experience is a plus" ([ZipRecruiter](https://www.ziprecruiter.com/c/National-Christian-Foundation/Job/Manager,-Treasury-Accounting-Operations/-in-Alpharetta,GA?jid=cdb3e19103cb0134)). Both pages returned 403. The repo's recruiter.com posting (S18) now returns 404.
- **[F]** The 2025 audited consolidated statements show capitalised "Software development costs" of $2,004,000 (2025) and $3,130,000 (2024). They name no system ([NCF 25 FS](https://site.ncfgiving.com//wp-content/uploads/2026/07/NCF-25-Consolidated-FS-Final.pdf)).
- **Reading [I].**
  - NetSuite is plausibly NCF's corporate GL.
  - The DAF sub-ledger may be Ren iPhi, given the rising Stellar payments.
  - Keep NCF at **low**. Re-label it "Salesforce + Ren iPhi; NetSuite GL [S]", not SF_NETSUITE.

### 1.4 Effect on ledger shares

| Family | Before (repo) | After batch 28 |
|---|---|---|
| NetSuite (+ Salesforce or NPact FIT), confirmed | $0 confirmed; $15.56bn low | **$10.10bn**: SVCF (medium-high) + Pittsburgh (high) |
| NCF | in SF_NETSUITE, low | UNRESOLVED (Salesforce / iPhi / NetSuite [S]); $5.46bn |

The Minneapolis Foundation was not re-checked in this batch.

---

## 2. P-NPP-04: who operates DonorCentral in 2026

| Evidence | What it shows | Label |
|---|---|---|
| NPact product page `npact.com/software/donorcentral/` (live 2026-11-15) | "Get to Know DonorCentral® The Secure, Self-Service Donor Advised Fund Portal for Community Foundations … integrated with NPact's FIMS system … Built on NPact's trusted infrastructure … Built on NPact's cloud platform … Ongoing customer support from NPact" ([page](https://npact.com/software/donorcentral/)) | [F] |
| PR Newswire, 2022-09-12 | "NPact Acquires FIMS and DonorCentral® NXT Products from Blackbaud". NPact "is committed to supporting and enhancing them for the foreseeable future" ([release](https://www.prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html)) | [F] |
| NPact SaaS License and Services Standard Terms, "Last updated: August 26, 2025" | "Manufacturer is Fusion Laboratories LLC / dba NPact". It disclaims "Blackbaud products" as third-party products ([terms](https://npact.com/software-as-a-service-license-and-services-standard-terms/)) | [F] |
| NPact Terms of Use, "Last updated: July 15th, 2025" | "Fusion Laboratories dba NPact, a Delaware corporation". The SaaS terms say "LLC", so the two documents conflict on entity form, as the wave-10 note records ([terms of use](https://npact.com/terms-of-use/)) | [F] |
| Live bundle `aef.donorcentral.com/main.18637f992cb04132.js` (5.9 MB) | API hosts `capp-prod-cores-dc-usc-001.donor.npact.com` and `…donorcentral.com/v1`; identity `auth0.donorcentral.com`; claims namespace `melabs.io/claims/dc/*`; user types "BBID", "NPact", "Social", "SSO", "None"; embedded text "entered into by and between NPact (the "Platform"), and … ("Merchant")"; links to NPact's FIMS/DonorCentral knowledge base | [H] |
| NPact KB "How to log into DonorCentral for donors and advisors" | Published and updated 2024-07-30. New users must contact their community foundation ([KB](https://npact.document360.io/fims-and-donorcentral/docs/how-to-log-into-donorcentral-for-donors-and-advisors)) | [F] |
| Calgary Foundation "Donor Central" page | Links `https://calgaryfoundation.donorcentral.com/#/sign-in` ([page](https://calgaryfoundation.org/giving/donor-central/)) | [F] |
| GWCF technology update | Foundation Cloud Community Portal "will replace our existing Donor Central Portal"; "The launch date … has been pushed back to September 21, 2026" ([news](https://www.thecommunityfoundation.org/news/an-update-on-our-technology-transformation-what-fundholders-need-to-know)) | [F] |
| Search extract (Vermont CF portal) | "provider upgraded servers on July 31, 2024"; users had to reset passwords | [S] |

**Answer.**
- NPact (Fusion Laboratories) owns, hosts and supports DonorCentral.
- The Blackbaud SKY UX CSS and the "BBID" login option are front-end legacies of the 2022 carve-out.
- The 2024-07-30 KB date and the Vermont 2024-07-31 server note suggest NPact moved logins and hosting to its own infrastructure around July 2024 [I].
- **Correction:** the repo statement "DonorCentral is a Blackbaud product, not NPact" (`queue-all-in-cost-dafpay-access.md` §3) is wrong for 2022-09 onward. The wildcard-hosting caveat from `queue-nonprofit-side-panel.md` still holds: an HTTP 200 on `<x>.donorcentral.com` does not prove a tenant.
- Tenants: Calgary is confirmed through a sponsor-side link. AEF still links DonorCentral from its homepage (repo, [F] 2026-11-15; AEF returned 403 to curl in this batch).

---

## 3. P-PAY-03: voided, returned and cancelled DAF grants

### 3.1 Method

- I downloaded the latest-filed 990 XML for the top 30 sponsors by FY2024 DAF assets.
- I also downloaded TY2021–2024 returns for 21 of them: the top 12 nationals and banks, and the top-10 community foundations (64 files). URLs came from `form990-returns-schedule-d-harvest-full.csv`.
- Every Schedule O/D explanation field was scanned for void, refund, returned grant, rescind, cancel, uncashed, escheat, unclaimed and stale-dated.
- I read Fidelity's FY2025 audited statements and NCF's 2025 audited statements in full text.
- Scripts are in the scratchpad (not committed). Rows are in `daf-grant-voids-disclosures.csv`.

### 3.2 What is disclosed

| Sponsor | Label (verbatim) | TY2021 | TY2022 | TY2023 | TY2024 | % of Part I grants (latest) |
|---|---|---|---|---|---|---|
| Fidelity Charitable (FYE Jun) | "ADJUSTMENT FOR PRIOR YEAR VOIDED GRANTS" (Part XI l.9; Sch D XII 4b) | n/s | $16,044,329 | $16,590,356 | $11,153,865 | 0.073% |
| GS DAPF | "GRANT REFUNDS" | – | – | – | $9,183,637 | 0.298% |
| AEF | "REFUNDED GRANTS" | – | – | $4,061,784 | $2,608,512 | 0.200% |
| Ayco | "GRANT REFUNDS" | – | – | – | $75,000 | 0.025% |
| SVCF | "Grant Cancellations not offset" | – | $6,855,601 | masked | masked | 0.164% (TY2022) |
| CCF (FYE Jun) | "ADD BACK RETURNED GRANTS MADE IN PRIOR YEAR" / "RESCINDED GRANTS" | $7,933,668 | $7,732,022 | $12,950,897 | −$2,971,713 | 0.88% |
| OCF | "Grant and scholarship refunds" | – | $3,375,256 | $1,657,524 | $2,192,128 | 1.19% |
| Columbus | "REFUNDS OF PRIOR YEARS' GRANTS" + "PRIOR YEAR GRANTS RESCINDED" | – | $95,536 + $586,536 | $552,567 + $210,804 | $38,003 | 0.015% |

"–" means the return was scanned and no item was found. "n/s" means the return was not in the harvest. "Masked" means the IRS public XML shows `XXX-XX-XXXX`, the redaction pattern applied to nine-digit strings. Sources: XML links in the CSV, for example Fidelity's [TY2024 return](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml).

### 3.3 What is not disclosed

- **No itemised figure in any return scanned:** NPT, DAFgiving360 (Schwab), Vanguard (TY2021–23), MS GIFT, BofA CGF, Ren, NCF, CCT, GKCCF, FFTC, NYCT, TBF, CFGA.
- That absence means their book and 990 treatment of voids match, so no reconciling item arises. **It does not mean zero voids.**
- **Audited statements:** Fidelity FY2025 shows grants as one line ($15,296,337,770), and its contributions note says accepted gifts "are not refundable". NCF 2025 has nothing. Neither has a void, refund or uncashed-check note ([Fidelity FS](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)).
- **Nowhere disclosed:**
  - number of grants voided;
  - cause (uncashed check, charity returned funds, sponsor rescission after due diligence, charity status lapsed);
  - check vs EFT;
  - DAF vs other fund types (community foundations);
  - escheat amounts.
- Labels differ ("voided", "refunded", "rescinded", "cancellations") and are not comparable across sponsors. Community-foundation figures include scholarships and competitive grants.

### 3.4 Can a void rate per check be estimated?

**Only illustratively, for Fidelity, and with low confidence [I].**
- **Inputs:**
  - FY2025 voided-grant adjustment: $11.15m.
  - FY2025 grants: $15.3bn.
  - Fidelity's 2026 Giving Report: "more than 2 million" EFT grants at 67%, which implies about 3m grants a year (repo §2.1, [F]).
- **Calculation:**
  - average grant ≈ $5,100;
  - $11.15m ÷ $5,100 ≈ 2,200 grant-equivalents, about 0.07% of grants.
  - If every void were a check (about 1m checks a year), that is about 0.2% of checks.
- **Caveats:** the numerator is a prior-year adjustment, and voided grants need not be average-sized. Treat the figure as an order-of-magnitude marker, not a rate.

---

## 4. P-NPP-01: top-10 community foundations, nonprofit side

Full cells and verbatim quotes are in `nonprofit-side-panel-2026-cf-supplement.csv`.

| CF | Min grant | Cadence | Fund name on remittance | Donor identity default | Void rule | Key source |
|---|---|---|---|---|---|---|
| SVCF | $200 (US); $10,000 intl/ER | 5–7 business days; check by default | Yes ("SVCF letter specifying the name of the fund") | Advisor name(s); address on request; anonymity fund-wide or per grant | not found | [DAF agreement, mod. 2025-08-22](https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf) |
| CCT | $250 | Approves twice weekly; check mailed in 5–7 days | Not stated | Advisor named unless anonymous | not found | [Donor FAQ 2025-12](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf); [DAF application](https://donorportal.cct.org/ma/docs/cct/CCT-DAF-Application.pdf); [DAF 101 for nonprofits, Sept 2025](https://www.cct.org/wp-content/uploads/2024/08/Donor-Advised-Fund-101-for-Nonprofits_August-2024.pdf) |
| FFTC | not found | 10-day lead time only | Yes (default) | Advisor name **and address**; anonymity option | not found | [DAF agreement, mod. 2026-11-03](https://fftc.org/sites/default/files/documents/FFTC_DAF_Agreement_Fillable.pdf) |
| GKCCF | none set ("Board ... may designate") | not found | Yes, on the check | Donor contact on check stub (encouraged); anonymity "rare" | not found | [Knowledge hub](https://www.growyourgiving.org/nonprofits/knowledge-hub/); [procedures 2023](http://growyourgiving.org/documents/procedures-and-bylaws.pdf) |
| Columbus | $100 (2025); $250 preferred (2022) | Suggestions reviewed daily | Yes unless anonymous | Advisor named; checkbox anonymity (fund, advisor or both) | not found | [Portal guide 2025](https://columbusfoundation.org/media/p1za1dz4/csuite-fund-portal-donor-resources-2025.pdf); [DAF guide 2022](https://columbusfoundation.org/media/4ive4cst/donor-advised-funds-procedures-and-guidelines-062022.pdf) |
| NYCT | $250 | 3–5 business days | Yes ("The New York Community Trust / Fund Name / at the suggestion of …") | Advisor named; advisor and/or fund withheld on request | not found | [DAF Policies 2025 ed.](https://thenytrust.org/wp-content/uploads/2026/03/DAF-Policies-and-Guidelines-2025-edited.pdf) |
| OCF | $500 ($1,000+ preferred) | Weekly [I]; ACH pilot, lump-sum deposits | not stated | Award letter shows preferred recognition; no contact info means anonymous | not found | [DAF page](https://oregoncf.org/ways-to-give/choose-your-fund/donor-advised-fund); [grantee guidance](https://oregoncf.org/grants-and-scholarships/advised-fund-grantees/advised-fund-grantee-guidance); [ACH](https://oregoncf.org/ach-grant-payments) |
| TBF | $250 | Weekly (in by Friday, paid by the next Friday); check or EFT | Four-way per-grant choice | Personal info not shared without permission | not found | [Donor handbook, mod. 2025-12-17](https://www.tbf.org/-/media/tbf/files/development/donor-handbook.pdf) |
| CCF | not found (2021+) | not found | not found (2021+) | not found (2021+) | not found | [DonorConnect Dos/Don'ts 2025](https://www.calfund.org/wp-content/uploads/CCF-DonorConnect-Dos-Donts-v2.0.pdf) |
| CFGA | $100 | not found | Not stated in 2025 guide ([S] says it can be withheld) | Advisor name **and mailing address**; "anonymous" box | not found | [Fund Advisor Portal Guide, 2025-03](https://cfgreateratlanta.org/wp-content/uploads/2025/03/Fund-Advisor-Portal-Guide.pdf) |

**Comparison with national sponsors [I].**
- Community-foundation minimums ($100–$500) sit at or above Fidelity and DAFgiving360 ($50).
- Three foundations set the remittance to name the fund by default (SVCF, NYCT, FFTC). DAFgiving360, NPT and Vanguard offer the fund name as a separate choice.
- Two foundations (FFTC, CFGA) share the advisor's **mailing address** by default. No national sponsor's published rule does this.
- None of the 10 publishes a void, uncashed-check or escheat rule. Fidelity, BlueGive and Chariot DPN each publish a 90-day rule.

---

## 5. P-CMP-06: sponsor mobile app defects (2021+)

### 5.1 Apps in scope (iTunes Search/Lookup API, 2026-11-15)

| App | Seller of record | Ratings | Avg | Current version / date | Min iOS |
|---|---|---|---|---|---|
| Fidelity Charitable (id552407907) | Fidelity Investments | 24 | 3.58 | 5.22 / 2026-11-11 | 17.0 |
| Daffy: Save, Invest, Give (id1578035540) | Daffy Charitable Fund | 560 | 4.91 | 1.54.4 / 2026-11-10 | 17.6 |
| DAFgiving360 / Schwab Charitable | no standalone app returned for "dafgiving360" or "schwab charitable" | – | – | – | – |
| Vanguard Charitable | no standalone app returned | – | – | – | – |

Sources: [Fidelity Charitable](https://apps.apple.com/us/app/fidelity-charitable/id552407907); [Daffy](https://apps.apple.com/us/app/daffy-save-invest-give/id1578035540). Reviews come from the US customer-review RSS (`itunes.apple.com/us/rss/customerreviews/page=N/id=…/sortby=mostrecent/json`, pages 1–10). The feed returned 53 Fidelity and 28 Daffy written reviews in all.

### 5.2 Defect classification (Fidelity Charitable, 27 written reviews 2021+)

| Defect type | n | Versions | Dates | Notes |
|---|---|---|---|---|
| login_auth | 10 | 3.0, 3.1, 3.2, 4.2 | 2021-09 to 2023-11 | 4 name Face ID; 1 says a saved password was lost after an update; 2 say the problem lasted more than 2 months |
| crash_on_launch | 2 | 5.21 | 2026-10-08 | iOS 27; forced-update path; **5.21.1 shipped 2026-10-09** |
| crash_in_flow | 2 | 4.1 | 2023-04, 2023-09 | crash on new or scheduled grant |
| crash_post_auth | 1 | 3.0 | 2021-10 | "throws an error retrieving the accounts and quits" on iOS 15.0.1 |
| feature_regression | 2 | 5.10, 5.21.1 | 2025-09, 2026-10 | recurring-grant editing (restored in 5.16, 2026-05-13); tax-lot selection |
| data_parse_error / hang_ui / update_distribution | 1 each | 3.0 / 4.1 / 5.3.1 | 2021–2025 | |
| not a defect | 7 | | | 3 praise; fees; service delay; 2 feature requests |

Daffy (28 reviews): 27 praise, 1 security_ux (hardware-key-only 2FA, no TOTP; 2026-08-15).

### 5.3 Release-note and stack signals

- **Fidelity cadence.** 25 versions, from 5.0 (2024-06-20, "elevated design experience") to 5.22 (2026-11-11), about one every 5 weeks. The notes are feature-led: account opening, EFT contributions, statements, successor nomination.
  - **5.19 and 5.21 (Sept–Oct 2026)** add a "Security Center" covering "biometric login, … third-party app authentication settings … trusted devices". The two launch-crash reviews on 5.21 came the day it shipped. Changes to the auth stack and crashes coincide [I].
  - 5.22 adds an OS age-signal request.
- **Daffy cadence.** 25 versions in 5 months (2026-06-12 to 2026-11-10). Its notes openly list fixes:
  - "Fixes an issue where some members saw a sign-in error on the Welcome screen" (1.44.15, 2026-07-26);
  - "Fixed an issue that could cause the app to briefly freeze right after signing in" (1.44.17);
  - "iOS 27 support • Fixes a crash when scrolling through portfolio options" (1.52.1, 2026-09-18, before iOS 27 crashes appeared at Fidelity).
- **Who builds the Fidelity app.** The seller of record is "Fidelity Investments". The Gift Fund's audited statements (note 7) say the Trustees "have contracted with FMR LLC … to provide various administrative and investment management services", including National Charitable Services LLC for "administrative and recordkeeping services".
  - Fidelity Investments' public mobile postings ask for native Swift, SwiftUI and UIKit ([example](https://jobs.fidelity.com/en/jobs/2137710/principal-mobile-developer/)) [S].
  - No posting specific to Fidelity Charitable was found. The app is therefore most likely built in-house at FMR, not by an outside vendor [I].
  - No framework signal was found for Daffy.

### 5.4 Why the defects recur [I]

1. **Breakage at iOS major releases.** Complaint clusters follow iOS 15 (Sept 2021), the Dec 2022 Face ID failures that a reviewer ties to iOS updates, and iOS 27 (Oct 2026). Daffy shipped iOS 27 support before release.
2. **Auth and credential handling.** Lost saved passwords after updates, Face ID fallbacks that fail, and a credentials step that hangs point to keychain, biometric and session handling. The v5.0 rebuild appears to have fixed this: no login complaint follows it in the 2021+ sample.
3. **Low usage, thin feedback loop.** The app has 24 ratings, against 560 for Daffy. Fidelity reports that 98% of grant recommendations start digitally (repo §2.1) but does not split web from app. Defects can persist for months (two reviews say more than 2 months).
4. **Regression on feature parity.** Features dropped and later restored (recurring edits, tax lots) suggest the mobile and web feature sets are managed separately.

**Correction for `daf-user-complaints-deep-research.md` line 327.** That line says Fidelity login failures "appear in every update cycle". On 2021+ evidence, login failures stop after v5.0 (2024-06). The 2026 defects are a launch crash fixed within a day, plus feature regressions.

---

## 6. Corrections to existing repo text (proposed)

1. **`cf-ledger-families-2026.csv`, SVCF row.**
   - Change the product to "NetSuite GL + NPact Fund Investment Tool (FIT) layer; Salesforce Experience Cloud portal".
   - Change the confidence to medium-high.
   - Change the evidence to the NPact story, 2025-04-29 [V].
2. **`cf-ledger-families-2026.csv`, Pittsburgh row.**
   - Change the evidence to the CIO posting [F] ("core ERP system encapsulated by NetSuite, Salesforce"; "remediation of the implementation").
   - Change the confidence to high.
   - Change the status to "implemented; under remediation 2026".
3. **`cf-ledger-families-2026.csv`, NCF row.** Move to UNRESOLVED: "Salesforce (990) + Ren iPhi (990 Stellar $2.50m TY2024); NetSuite GL [S]".
4. **`queue-ledger-segment-npact-owner.md` lines 30, 56 and 75.** Replace "$15.6bn in a low-confidence NetSuite + Salesforce bucket" with "$10.10bn confirmed (SVCF, Pittsburgh); NCF $5.46bn unresolved".
5. **`queue-all-in-cost-dafpay-access.md` §3.** Replace "(DonorCentral is a Blackbaud product, not NPact)" with "(DonorCentral has been owned and operated by NPact / Fusion Laboratories since 2022-09; its front end keeps Blackbaud SKY UX styling)".
6. **`nonprofit-side-panel-2026.csv`, community-foundation rows.** Merge the supplement. The community-foundation void_return_policy changes from blank to "not found (10 of 10 checked)".
7. **`daf-user-complaints-deep-research.md` lines 177 and 327.** Add "No login complaints after v5.0 (2024-06-20) in 2021+ reviews".

---

## 7. Source register

| # | Source | Type | Date | URL |
|---|---|---|---|---|
| S1 | NPact SVCF customer story | [V] | pub. 2025-04-29 | https://npact.com/customer-stories/silicon-valley-community-foundation/ |
| S2 | NPact FIT product page | [V] | mod. 2026-11-12 | https://npact.com/software/fund-investment-tool-fit/ |
| S3 | NPact FFTC customer story (RE NXT, FE NXT, Foundation Cloud) | [V] | pub. 2025-03-07 | https://npact.com/customer-stories/foundation-for-the-carolinas/ |
| S4 | Pittsburgh Foundation CIO posting | [F] | deadline 2026-03-20 | https://pittsburghfoundation.org/cio |
| S5 | NCF 2025 consolidated FS | [F] | 2026-07 | https://site.ncfgiving.com//wp-content/uploads/2026/07/NCF-25-Consolidated-FS-Final.pdf |
| S6 | NCF ZipRecruiter posting (403) | [S] | undated | https://www.ziprecruiter.com/c/National-Christian-Foundation/Job/Manager,-Treasury-Accounting-Operations/-in-Alpharetta,GA?jid=cdb3e19103cb0134 |
| S7 | NPact DonorCentral page | [F] | live 2026-11-15 | https://npact.com/software/donorcentral/ |
| S8 | NPact FIMS/DonorCentral acquisition release | [F] | 2022-09-12 | https://www.prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html |
| S9 | NPact SaaS terms; Terms of Use | [F] | 2025-08-26; 2025-07-15 | https://npact.com/software-as-a-service-license-and-services-standard-terms/ ; https://npact.com/terms-of-use/ |
| S10 | DonorCentral bundle | [H] | 2026-11-15 | https://aef.donorcentral.com/main.18637f992cb04132.js |
| S11 | NPact KB login article | [F] | 2024-07-30 | https://npact.document360.io/fims-and-donorcentral/docs/how-to-log-into-donorcentral-for-donors-and-advisors |
| S12 | Calgary Foundation Donor Central | [F] | live | https://calgaryfoundation.org/giving/donor-central/ |
| S13 | GWCF technology update | [F] | 2026 | https://www.thecommunityfoundation.org/news/an-update-on-our-technology-transformation-what-fundholders-need-to-know |
| S14 | IRS 990 XML, 30 latest + 64 TY2021–24 returns | [F] | TY2021–24 | links per row in daf-grant-voids-disclosures.csv |
| S15 | Fidelity Charitable FY2025 audited FS | [F] | report 2025-10-29 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf |
| S16 | SVCF DAF agreement; DAF guide | [F] | 2025-08-22; 2025-05-08 | https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf ; https://www.svcf.org/assets/files/publications/svcf-daf_10_screen.pdf |
| S17 | CCT donor portal FAQ; DAF application; DAF 101 for nonprofits | [F] | 2025-12-02; 2024-04-08; Sept 2025 | https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf ; https://donorportal.cct.org/ma/docs/cct/CCT-DAF-Application.pdf ; https://www.cct.org/wp-content/uploads/2024/08/Donor-Advised-Fund-101-for-Nonprofits_August-2024.pdf |
| S18 | FFTC DAF agreement | [F] | 2026-11-03 | https://fftc.org/sites/default/files/documents/FFTC_DAF_Agreement_Fillable.pdf |
| S19 | GKCCF knowledge hub; procedures and bylaws | [F] | live; 2023-11-10 | https://www.growyourgiving.org/nonprofits/knowledge-hub/ ; http://growyourgiving.org/documents/procedures-and-bylaws.pdf |
| S20 | Columbus portal guide 2025; DAF guide 2022 | [F] | 2025-04-22; 2022-06-24 | https://columbusfoundation.org/media/p1za1dz4/csuite-fund-portal-donor-resources-2025.pdf ; https://columbusfoundation.org/media/4ive4cst/donor-advised-funds-procedures-and-guidelines-062022.pdf |
| S21 | NYCT DAF Policies and Guidelines 2025 | [F] | 2026-03-31 | https://thenytrust.org/wp-content/uploads/2026/03/DAF-Policies-and-Guidelines-2025-edited.pdf |
| S22 | OCF DAF page; grantee guidance; ACH page | [F] | live | https://oregoncf.org/ways-to-give/choose-your-fund/donor-advised-fund ; https://oregoncf.org/grants-and-scholarships/advised-fund-grantees/advised-fund-grantee-guidance ; https://oregoncf.org/ach-grant-payments |
| S23 | TBF donor handbook; DAF agreement | [F] | 2025-12-17; 2025-05-28 | https://www.tbf.org/-/media/tbf/files/development/donor-handbook.pdf ; https://www.tbf.org/-/media/tbf/files/development/donor-advised-fund-agreement.pdf |
| S24 | CCF DonorConnect Dos/Don'ts | [F] | 2025-01-07 | https://www.calfund.org/wp-content/uploads/CCF-DonorConnect-Dos-Donts-v2.0.pdf |
| S25 | CFGA Fund Advisor Portal Guide | [F] | 2025-03-26 | https://cfgreateratlanta.org/wp-content/uploads/2025/03/Fund-Advisor-Portal-Guide.pdf |
| S26 | App Store pages, version history, review RSS, iTunes API | [F] | 2026-11-15 | https://apps.apple.com/us/app/fidelity-charitable/id552407907 ; https://apps.apple.com/us/app/daffy-save-invest-give/id1578035540 |
| S27 | Fidelity Investments mobile developer posting | [S] | 2026 | https://jobs.fidelity.com/en/jobs/2137710/principal-mobile-developer/ |

---

## 8. Data dictionary

### `nonprofit-side-panel-2026-cf-supplement.csv` (long format; one row per CF × field)

| Column | Type | Meaning |
|---|---|---|
| entity_id | text | Same key as `nonprofit-side-panel-2026.csv` (e.g. `cf_svcf`) |
| entity | text | Community foundation name |
| field | enum | `minimum_grant`, `issue_cadence`, `default_rail`, `remittance_fund_name`, `remittance_donor_identity`, `void_return_policy` |
| value | text | Normalised answer, or `not found` (sources checked and silent) |
| verbatim_quote | text | Exact text from the source; for `not found`, the list of documents checked |
| source_url | text | One or more URLs separated by ` ; ` |
| source_date | text | PDF modification or creation date, or page date |
| origin | text | `fresh:2026-11-15` plus a label ([F], [S], [I]); "(absence)" marks a negative finding |
| notes | text | Caveats, recency exclusions, links to panel cells |

### `daf-grant-voids-disclosures.csv`

| Column | Type | Meaning |
|---|---|---|
| row_id | text | V01… |
| sponsor, ein, sponsor_type | text | Filer name as on the 990; EIN without hyphen; national / bank sponsor / community foundation |
| tax_year, fiscal_year_end | text | IRS tax year; period end date (comma list for "none found" rows) |
| source_type | text | Form 990 Schedule O reconciliation, XML full-text scan, or audited FS |
| line_reference | text | FormAndLineReferenceDesc as filed |
| disclosed_label_verbatim | text | Label as filed (e.g. "ADJUSTMENT FOR PRIOR YEAR VOIDED GRANTS"), or `none found` |
| amount_usd_as_filed | number/text | Amount and sign as filed; `REDACTED` where the IRS XML shows XXX-XX-XXXX |
| grants_paid_part_i_line13_usd | number | CYGrantsAndSimilarPaidAmt (denominator) |
| sched_d_daf_grants_usd | number | Schedule D Part I DAF grants (context) |
| amount_pct_of_part_i_grants | number | abs(amount) ÷ Part I grants × 100; approximate, because numerators often relate to prior-year grants |
| scope | text | Entity-wide vs DAF-dominant |
| counts_disclosed | yes/no | Whether a number of grants is given (always no) |
| what_is_not_disclosed | text | Missing dimensions |
| confidence | text | Filed figure vs interpretation |
| source_url | text | XML or PDF link(s) |
| retrieved | date | 2026-11-15 |
| notes | text | Cross-references, redaction, comparability |

### `sponsor-app-defects-2021plus.csv`

| Column | Type | Meaning |
|---|---|---|
| record_id | text | APP-001… |
| sponsor, app_name, app_store_id, seller_of_record | text | App identity from iTunes Lookup |
| review_id | text | App Store review id (RSS `id.label`) |
| review_date | date | RSS `updated` (UTC date) |
| rating | int | 1–5 |
| app_version | text | Version the reviewer used |
| title | text | Review title |
| defect_type | enum | `login_auth`, `crash_on_launch`, `crash_in_flow`, `crash_post_auth`, `data_parse_error`, `hang_ui`, `update_distribution`, `feature_regression`, `security_ux`, `not_defect_praise`, `not_defect_fees`, `not_defect_service`, `not_defect_feature_request`, `not_defect_feature_gap` |
| defect_summary | text | One-line paraphrase of the review |
| fix_class | enum | `fixable_auth`, `fixable_release_qa`, `fixable_product`, `service_ops`, `structural_pricing`, `n/a` |
| in_defect_count | yes/no | Counted as a defect |
| notes | text | Platform or release context (e.g. hotfix date from version history) |
| source_url, retrieved | text, date | App Store page; 2026-11-15 |

### `queue-proposals-batch28.csv`

Columns follow `queue-proposals-README.md`.

---

## 9. Limitations

- **SVCF NetSuite rests on a vendor case study.** NPact has a commercial interest, though the story quotes a named SVCF officer. SVCF's own pages and its audit were not found.
- **Void figures appear only where the book and 990 treatments differ.** Sponsors without itemised figures are not void-free. SVCF's TY2023–24 amounts are masked in the public XML.
- **The App Store RSS returns only the latest written reviews,** about 50 per app. Ratings without text and Android were not analysed (P-B28-04). Defect classification is mine, made from short texts.
- **Community-foundation cadence is often a service target,** e.g. "typically", "generally", not a guarantee.
