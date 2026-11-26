# Grant remittance at the top-10 sponsors, and three portal features across vendor tenants (P-B40N13-02, P-B42N22-02)

- **Queue items:** P-B40N13-02 (remittance census, from [direction-data-standards-interoperability.md](direction-data-standards-interoperability.md)) and P-B42N22-02 (portal features, from [direction-donor-feature-census.md](direction-donor-feature-census.md) §4).
- **Date:** 2026-11-19. Every page was read on that date. Public pages only: no enrolment, no logins, no forms, no test payments, no outreach.
- **Builds on:** [g1913-processor-disbursement-rules.md](g1913-processor-disbursement-rules.md) (processor rules), [b40n13-01-grant-purpose-panel.md](b40n13-01-grant-purpose-panel.md) (purpose text in Schedule I), [b4428-02-ren-private-label-defaults.md](b4428-02-ren-private-label-defaults.md) (Ren guides, cached the same day and reused here), `sponsor-grant-payment-policies.csv`, `community-foundation-rails-portals-2026-v2.csv`, `donor-export-evidence-cf-2026.csv` and `daf-data-standards-2026.csv` (DS19–DS23).
- **Files written:**
  - [`data/mission-2026-11-14/grant-remittance-2026-11-19.csv`](../../data/mission-2026-11-14/grant-remittance-2026-11-19.csv): 14 rows (11 for the top-10 sponsors, 3 for the Ren and Chariot rails), 22 columns.
  - [`data/mission-2026-11-14/portal-features-2026-11-19.csv`](../../data/mission-2026-11-14/portal-features-2026-11-19.csv): 32 rows, one per tenant × feature, 16 columns.
  - [`data/mission-2026-11-14/queue-proposals-b4013-02-b4222-02.csv`](../../data/mission-2026-11-14/queue-proposals-b4013-02-b4222-02.csv): 6 rows.
  - [`scripts/mission_b4013_02_b4222_02_build.py`](../../scripts/mission_b4013_02_b4222_02_build.py): builds both CSVs and prints every share in this note. Run `python3 -I scripts/mission_b4013_02_b4222_02_build.py .`
- **Labels:** [F] first-party text read this pass. [R] carried from a repo file. [B] blocked by robots.txt. [C] computed by the script. [I] inference.

---

## 0. Answers

### (A) P-B40N13-02: how the top-10 sponsors' electronic grants carry remittance data

| Question | Finding | Confidence |
|---|---|---|
| **ACH SEC code (CCD, CCD+ or CTX)** | **Not stated on any public page read.** 0 of 14 rows name an SEC code [C]. This covers the eight readable top-10 sponsors only: DAFgiving360 and GS DAPF (24.1%) could not be read, SVCF rests on a repo row, and no page describes the code of PayPal’s own transfer to the charity’s bank [V wave 39A]<br>- Six sponsors pay by ACH or "electronic transfer" but do not say which code: Fidelity, SVCF, MS GIFT, AEF, RCF and NCF. Together they hold $104.86bn, 47.1% of top-10 FY2024 DAF assets [C]. SVCF pays by check by default and only reserves ACH (repo row), and AEF’s ACH began in 2026, with checks until a charity is verified [V wave 39A]<br>- Two sponsors send no ACH at all. NPT's 2026 guide says "At this time, NPT does not issue payments via ACH transfer"; its electronic route is PayPal Grant Payments, plus wires for grants of $250,000 or more. Vanguard documents only PayPal Grant Payments and says nothing about ACH either way, so only NPT states that it sends no ACH; PayPal itself moves accepted funds to the charity’s bank. Together: $64.07bn, 28.8% [C][F] [V wave 39A]<br>- Two sponsors could not be read: DAFgiving360 (robots.txt 403) and GS DAPF (robots.txt `Disallow`). Together: $53.58bn, 24.1% [C][B]. | High that nothing is published; the codes themselves are unknown |
| **Grant ID or fund name in the addenda** | **Not documented for any top-10 sponsor** (0 of 10) [C].<br>- The only first-party statement that an identifier travels in a payment memo is Chariot's DAFpay guide: the Tracking ID appears "usually as 'Tracking ID {id} - Gift through DAFpay'. Wording varies by provider." It names no provider, and it adds that "Some DAF providers do not pass the Tracking ID through on their remittances" [F].<br>- Fidelity's ACH entries show "Fidelity Charitable" as the source on the bank statement, and Stripe payouts show "Fidelity grant". These are payer names, not grant data [F]. | High on the pages read |
| **What arrives out-of-band** | **Every documented route sends the grant detail separately from the money.** By top-10 assets [C]:<br>- **Email report plus dashboard or emailed letter, 48.7%.** NPT is in this group only because wires get an emailed letter; its grants up to $250,000 go by the PayPal dashboard, and grouping NPT by that route gives 29.8% email and 39.3% portal or dashboard [V wave 39A] Fidelity ACH sends an encrypted, consolidated Grant Details Report by email every day, to up to five contacts. Fidelity Stripe uses the Stripe dashboard and export. NPT uses the PayPal dashboard, and emails the letter separately for wires.<br>- **Portal or dashboard only, 20.4%.** Vanguard uses the PayPal dashboard. MS GIFT, AEF and RCF use Ren's charity portal (a grants report with a CSV export, Grant ID and ACH ID).<br>- **Letter only, 2.6%.** NCF: "a letter identifying your Giving Fund and any grant purpose".<br>- **Not stated, 4.3%:** SVCF.<br>- **Not determinable, 24.1%:** DAFgiving360 and GS. | High |
| **Batching** | Two sponsors and Chariot say one payment can carry several grants:<br>- Fidelity: "Each EFT is comprised of one or more donor-recommended grants" (enrolment form, 2025-12).<br>- Fidelity's Stripe route pays out in Stripe "Payouts".<br>- Chariot: "One deposit → many donations"; "Some providers batch several gifts into one payment" [F].<br>So a bank line cannot be matched to a grant without the out-of-band file. | High for Fidelity; others not stated |
| **Chariot's sponsor list** | Chariot's "Sources Managed By Chariot" (paid plan) lists **Fidelity Charitable, PayPal Grant Payments and Ren (Pinkaloo)** among 11 sources. Through them, 7 of the top 10 can be connected: Fidelity; NPT and Vanguard via PayPal; MS GIFT, AEF and RCF via Ren [F/I].<br>- None of the top 10 is a Chariot Disbursement Partner.<br>- Chariot works out the source by giving each payer **its own receiving account number**, so teams need not "rely on inconsistent descriptions to figure out where funds came from". For any other ACH payer, a nonprofit must upload "donation files, grant letters, or other documentation" itself, because "Custom Payment Sources only automate the movement of funds" [F]. | High on Chariot's text |

**Bottom line (A).** The repo's earlier finding (DS21–DS22: "no sponsor documents a grant ID in ACH addenda") **holds across the whole top 10**, and it is now sharper on three points:
- Two of the top four sponsors document no ACH of their own: NPT states it outright, and Vanguard documents only PayPal Grant Payments [V wave 39A]
- The Ren programs move remittance into a charity portal keyed by Grant ID and ACH ID.
- Chariot, the main reconciliation intermediary, identifies payers by **routing each payer to a different account number**, not by reading addenda. That design only makes sense if addenda and descriptors cannot be relied on [I].

Sizing for a remittance standard: about $105bn (47%) of top-10 assets pays by ACH with undisclosed addenda, and every observed route keeps grant data in a separate email, dashboard, portal or letter [C].

### (B) P-B42N22-02: impact reports, self-serve export and public giving pages

| Feature | Finding | Confidence |
|---|---|---|
| **(a) Donor-level impact report beyond grant status** | **None found.**<br>- The nearest is a **category dashboard** on two Ren DFX tenants: RCF's "Giving Platform" guide (2026-10), whose homepage "Showcases your impact of giving by breaking grants into philanthropic categories", and BofA's guide (2026-02), which charts "Charitable impact on different categories of Charities" and shows the top 3 charities. Both are coded P [F].<br>- Ren's Giving Compass partnership (2026-03) brings **charity-level** impact metrics to donors and advisors. It reports on charities, not on the donor's own grants, so it is coded N [F].<br>- GivingPoint (NPT 2026 guide), GiftingNetwork (CCT FAQ 2025-12), Foundant tenants and NCF describe no impact report (ND) [F]. | Medium. Absence rests on guides, not on screens |
| **(b) Self-serve CSV or Excel export of grant history** | **Shipped, and documented by 7 tenants or vendors (Y)**, plus 3 partial (P):<br>- **Top-20 sponsors:** CCT on GiftingNetwork ("export CSV and chart-format gift history and grant history reports anytime", 2025-12). BofA on Ren DFX, partial: Excel export in the text for contributions; the grant-listing button appears in a screenshot [R]. GKCCF, partial: "download your granting history", format not stated.<br>- **Foundant CommunitySuite:** the vendor recorded "Added donation and grant history export for fund managers" (2024-08-27). Columbus (2025-04), Omaha and Sarasota (2025-06) document it; Tampa Bay documents contributions only (P).<br>- **NPact Foundation Cloud:** Greater Washington CF, CSV (2026-09).<br>- **Not documented:** RCF's 2026 Giving Platform guide and NPT's 2026 GivingPoint guide (ND). GivingPoint code holds Excel handlers (batch 33B), but they are not shown to donors.<br>- **Not readable:** DonorCentral (U/B) and iPhi (B). | High on the documents |
| **(c) Giving page or campaign that people without an account can give to** | **One top-20 sponsor documents it: NCF (Y).** "You can invite others to give to your Giving Fund. Including a donate button can make it easy for others to give directly to your fund online" [F].<br>- **Vendor capability:** Foundant's Giving Hub is "where anyone can donate to any fund you make publicly available" (Y). Two Foundant tenants point fundholders to *public* funds (Atlanta 2025-03, Sarasota 2025-06, both P). One Foundant tenant refuses: Triangle (2024-10) "is unable to support active fundraising or solicitation for contributions to any of the funds it holds" (N).<br>- **NPT:** third parties may contribute only by signing a Contribution Agreement (P).<br>- **Fidelity:** Gift4Giving runs the other way; the account holder lets someone else pick a charity. The page does not say that others cannot give to a Giving Account, so the code is ND, not N [V wave 39A] | High for NCF and Foundant; whether CFs list DAFs on their hubs is open |

**Bottom line (B).** The census white space needs narrowing:
- **(b) is not white space.** Grant-history export is shipped by GiftingNetwork, Foundant CommunitySuite and NPact Foundation Cloud on 2025–2026 documents. iPhi DonorView rests only on Minneapolis’s 2022 FAQ (repo row), and the iPhi sponsor hosts are robots-blocked [V wave 39A] What is missing is documentation at the national sponsors: Fidelity, Vanguard, RCF and NPT.
- **(c) is shipped by one top-10 sponsor (NCF) and by Foundant as a capability.** One community foundation (Triangle, 2024 guide) declines to support fundraising for any of its funds, while its Donate tab still sends fundholders to the Giving Hub to give to listed funds. No page read shows whether CFs list DAFs on their hubs [V wave 39A] The capability exists, so this is a choice, not a missing product.
- **(a) remains white space.** No tenant read offers a donor-level report beyond category totals.

---

## 1. Method

1. **Universe.**
   - **(A):** the FY2024 top 10 by corrected DAF assets from [`daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv): Fidelity, NPT, DAFgiving360, Vanguard, GS DAPF, SVCF, MS GIFT, AEF, RCF and NCF. Together they hold $222.51bn, 68.8% of the $323.27bn corrected market [C].
   - **(B):** the five portal families named in the queue item, plus top-20 sponsors and top-40 community foundations already mapped to a vendor in `community-foundation-rails-portals-2026-v2.csv`.
2. **Sources.**
   - Nonprofit-facing EFT pages and FAQs, the Fidelity EFT enrolment form (read, not submitted), sponsor guides and program circulars, Ren's charity help centre, Chariot's help centre (`llms-full.txt`) and developer docs, and community-foundation portal guides.
   - Search-engine results were used only to find URLs. Every quote in both CSVs was then read from our own fetch.
3. **Fetching.**
   - A stdlib fetcher (scratchpad `q1322/scripts/get.py`, UA `research-script/1.0`) fetched a URL only if robots.txt allowed both `*` and that UA.
   - A 404 robots.txt counted as no rules. Any other non-200 answer (403, 302, 500) counted as blocked.
   - Ren DFX guides, the BofA guide and the RCF circular were reused from the same-day P-B4428-02 cache (`q4428/log.jsonl`).
4. **Quote check.** A verifier (scratchpad `q1322/scripts/verify.py`) normalised whitespace and quote marks and confirmed that **all 30 quotes in the two CSVs (11 + 19) occur verbatim** in the cached sources: 0 misses, and 16 rows carry no quote by design [C]. Quotes inside `notes` were spot-checked by hand.
5. **Coding.**
   - **(A)**
     - `ach_sec_code` and `grant_id_in_addenda` are coded `not stated` unless a page names them.
     - `out_of_band_channel` records the channel the page describes.
     - The asset shares group each sponsor by its first (primary) route row.
   - **(B)**
     - `Y` = documented.
     - `P` = partial or conditional (category-only impact view; contributions-only export; public funds only; agreement-only third-party gifts).
     - `N` = documented as absent or refused.
     - `ND` = not found on the pages read.
     - `U` = no readable page.
     - `B` = blocked by robots.txt.
   - `recency_2025_26` flags whether the document is dated 2025–2026, as the queue item asks. All documents used are 2021 or later; three rows rest on 2022–2024 documents and are flagged `no`.

## 2. Robots and access log (2026-11-19)

There were 91 requests in this pass:
- 75 fetched with HTTP 200;
- 8 not fetched because robots.txt disallowed them or could not be read;
- 5 allowed but answered 403;
- 3 allowed but answered 404 [C].

| Host | robots.txt | Result |
|---|---|---|
| www.fidelitycharitable.org | 200, allowed | 7 × 200 (EFT page, FAQ, Stripe page, enrolment form, details page); 2 × 404 (an old grant-delivery FAQ URL and how-it-works) |
| www.nptrust.org, www.vanguardcharitable.org, www.aefonline.org, www.ncfgiving.com, ncfgiving.com, www.morganstanley.com, www.svcf.org, www.reninc.com | 200, allowed | 200 |
| intercom.help (Ren Help Center) | 200, allowed | 11 × 200 |
| help.givechariot.com, docs.givechariot.com, givechariot.com | 200, allowed | 18 × 200 |
| newsroom.paypal-corp.com; filecache.mediaroom.com | 200; 404 | 200 |
| **www.paypal.com** | 200, allowed | **403** (Grant Payments help article) |
| **www.dafgiving360.org, www.schwabcharitable.org** | **403** | **not fetched** |
| **gspf.goldman.com, rj.iphiview.com** | 200, `Disallow: /` | **not fetched** |
| www.goldmansachs.com | 200, allowed | 404 (guessed URL) |
| **npact.document360.io** (DonorCentral knowledge base) | **302 redirect** | **not fetched** (treated as blocked) |
| **npact.com** | **403** | **not fetched** |
| cfgnh, pacf, cfsjc, northerncincinnati `.donorcentral.com` | 200, allowed | 200, but script shells with no text |
| **support.foundant.com** | 200, allowed | **403** on 3 articles |
| www.foundant.com, dev.foundant.com, idealab.foundant.com | 200, allowed | 200 |
| donorportal.cct.org | 200, allowed | 200 (FAQ PDF) |
| **www.cct.org** | 200, allowed | **403** |
| columbusfoundation.org | 404 | 200 |
| cfgreateratlanta.org, omahafoundation.org, www.cftampabay.org, www.cfsarasota.org, trianglecf.org, www.thecommunityfoundation.org, www.growyourgiving.org, www.fftc.org, www.cfscc.org | 200, allowed | 200 |

crt.sh, certspotter and sec.gov were not used.

## 3. Results (A): remittance by sponsor

Full rows are in the CSV. The fragments quoted below are verbatim.

| # | Sponsor (FY2024 $bn) | Electronic route | SEC code / addenda | Out-of-band remittance | Source |
|---|---|---|---|---|---|
| 1 | Fidelity (66.20) | **ACH**; **Stripe** payout | Not stated. Bank statement: "Fidelity Charitable" (ACH) or "Fidelity grant" (Stripe) | ACH: encrypted Grant Details Report emailed daily to up to 5 contacts, containing "grant amount, grant acknowledgement information, and the donor-recommended grant purpose". The primary inbox must belong to one person ("A group shared inbox will not be accepted"). Stripe: dashboard plus export, whose full columns include donor contact details "not available in the dashboard" | Enrolment form (PDF 2025-12-18); nonprofit FAQ; EFT page; Stripe page [F] |
| 2 | NPT (42.12) | PayPal Grant Payments; wire for grants of $250,000+ and all international grants; **no ACH** | n/a | PayPal dashboard ("all relevant donor and grant details"). Wire: "the grant letter will be separately emailed to them" | NPT DAF Guide (PDF 2026-10-15) [F] |
| 3 | DAFgiving360 (40.94) | not documented | not determinable | not determinable | robots 403 [B]; repo: checks only (2024 policies) [R] |
| 4 | Vanguard (21.95) | PayPal Grant Payments | n/a | PayPal dashboard: "all the information a donor has elected to share" | Nonprofit page [F] |
| 5 | GS DAPF (12.64) | not documented | not determinable | not determinable | robots `Disallow` [B] |
| 6 | SVCF (9.58) | check by default; ACH or wire reserved | not stated | not stated | repo row [R] |
| 7 | MS GIFT (9.11) | ACH through Ren | not stated | Letter "with the date, description, and purpose of the grant"; Ren charity portal | MS GIFT FAQ [F]; Ren payments page (modified 2026-11-04) [F] |
| 8 | AEF (8.38) | ACH through the Ren charity portal (launched 2026) | not stated | Portal: "View current and historical grant letters". Payment is by check until ACH is verified | AEF charities page [F] |
| 9 | RCF (5.91) | ACH through Ren | not stated | Ren for Charities grants report: searchable by "Grant ID, Amount, Acknowledgement"; CSV export; ACH ID shown once the grant is "DELIVERED". **Conflict:** the 2026 Giving Platform guide says "if the grant is sent to the organization electronically, no grant letter will be generated", while the 2026 RCF Program Circular says "check or ACH accompanied by a grant letter" | Ren help (modified 2026-05-04); RCF guide (2026-10-06); circular (2026-07-23) [F] |
| 10 | NCF (5.68) | "ACH or electronic transfer when available"; wire on request (fee "usually about $25") | not stated | Letter "identifying your Giving Fund and any grant purpose"; questions to egrants@ncfgiving.com. No public enrolment form | NCF support page; NCF guide [F] |

**Rails behind the sponsors.**
- **Ren for Charities** says a charity can enrol in ACH "from 25+ donor-advised fund programs at once". Its grants report exists to "Match payments (Check/ACH) to specific grants" [F]. Within the top 10, this rail serves MS GIFT, AEF and RCF ($23.40bn, 10.5% of top-10 assets) [C].
- **PayPal Grant Payments** carries NPT and Vanguard ($64.07bn). PayPal's own 2023 research note presents the design as the answer to the remittance gap: it "consolidates payment and donor information into one secure portal, rather than separating the payment from the donor information as happens with an ACH payment" [F].
- **Chariot**, the receiving side:
  - Each source gets "its own unique account number", so payer identity comes from routing, not from descriptors.
  - Chariot's webinar page says ACH "typically lands with a bank reference ID that has nothing to do with the grant ID" [F].
  - For DAFpay gifts paid outside Chariot, the DAFpay Tracking ID may appear in the memo, but "Some DAF providers do not pass the Tracking ID through"; the fallback is "the donor's fund name, amount, date, and designation" [F].

**Comparison with the processor rules (g1913).** That note found processors pay in pooled monthly batches. Here, among sponsors, the only documented batching is Fidelity's ("one or more donor-recommended grants" per EFT). It is daily, not monthly, and it comes with a per-grant report. Sponsors differ from processors on cadence, but not on where the remittance lives: outside the payment in both cases [I].

**Link to Schedule I purpose text (b40n13-01).** Fidelity's Schedule I purpose is one boilerplate string on all 80,308 lines, yet its out-of-band GDR carries the "donor-recommended grant purpose". The grant purpose a charity needs is therefore present in the email report, but neither in the payment nor in the public filing [I].

## 4. Results (B): features by portal family

| Family (tenants read) | (a) impact | (b) export | (c) public giving | Key evidence |
|---|---|---|---|---|
| **Ren DFX / DonorFirst**: RCF + 6 private labels (2026-10 guide); BofA (2026-02 guide) | P (category dashboard) on both | RCF ND; BofA P (Excel: contributions in text, grants in a screenshot [R]) | ND | "Showcases your impact of giving by breaking grants into philanthropic categories" (RCF); "You can export to Excel to sort and do analysis" (BofA) [F] |
| **Ren platform-wide** | N (charity-level Giving Compass metrics) | – | – | "Ren has partnered with Giving Compass" (Q1 2026 release notes) [F] |
| **Ren/Stellar iPhi**: GS DAPF, Raymond James; Minneapolis CF (DonorView) | B | B for GS and RJ; Minneapolis Y (2022 FAQ, outside the 2025–26 window) [R] | B | robots `Disallow` [B] |
| **GivingPoint**: NPT (2026-10 guide) | ND | ND (Excel handlers in code, batch 33B [R]) | P (third-party contributions need a signed Contribution Agreement) | NPT DAF Guide [F] |
| **DonorCentral (NPact)** | U | U | U | Knowledge base and npact.com blocked; tenant portals are script shells. AEF (2026) and Vermont CF (May 2025) have left [B/R] |
| **NPact Foundation Cloud**: Greater Washington CF | ND | Y (CSV) | ND | "export your grant history ... as a CSV" (2026-09-21) [F] |
| **GiftingNetwork**: CCT (2025-12 FAQ); FFTC | ND | CCT Y (CSV); FFTC U | ND | "export CSV and chart-format gift history and grant history reports anytime" [F] |
| **Foundant CommunitySuite**: vendor; Columbus, Atlanta, Tampa Bay, Omaha, Sarasota, Triangle | ND | Vendor Y (2024-08); Columbus, Omaha and Sarasota Y; Tampa Bay P; Atlanta ND | Vendor Y (Giving Hub); Atlanta P; Sarasota P; Triangle N | "The Giving Hub is where anyone can donate to any fund you make publicly available" (blog, modified 2026-04-22) [F] |
| **Own portal**: NCF | ND | ND [R] | **Y** (donate button) | "Including a donate button can make it easy for others to give directly to your fund online" [F] |
| **Own portal**: Fidelity | ND [R] | ND [R] | N (Gift4Giving runs the other way) | Giving Account details page [F] |
| **Unidentified white-label portal**: GKCCF | – | P (download; format not stated) | – | 2022 article, modified 2026-07-14 [F] |

**Counts over the 32 feature rows** [C]:
- (a) impact: 2 P, 1 N, 3 ND.
- (b) export: 7 Y, 3 P, 3 ND, 2 U, 1 B.
- (c) public giving: 2 Y, 3 P, 2 N, 3 ND as coded; with Fidelity’s Gift4Giving row recoded from N to ND it is 2 Y, 3 P, 1 N, 4 ND [V wave 39A]
- 26 of the 32 rows rest on 2025–2026 documents.

## 5. Limits

- **Documents, not files or screens.** SEC codes and addenda are bank-file facts. No public page states them, and an enrolment or test payment would have been needed to observe them; both are out of scope. "Not stated" therefore does not mean "absent". The repo's Nacha description (DS22) comes from a guide whose robots.txt later returned 403 (wave 25B); it is used here only as context.
- **Blocked hosts.** DAFgiving360, GS DAPF, the iPhi hosts and the DonorCentral knowledge base account for 24.1% of top-10 assets in (A) and all DonorCentral and iPhi cells in (B). PayPal's Grant Payments help pages returned 403, so PayPal rows rest on NPT's and Vanguard's text and on PayPal's 2023 newsroom note.
- **Conflicting first-party text.**
  - Fidelity: Stripe notices are "emailed each Monday" (FAQ) versus "does not currently send an email" (Stripe page).
  - RCF: an electronic grant comes with no grant letter (guide) versus a grant letter with every check or ACH (circular).
  - Both conflicts are recorded in the CSV, not resolved.
- **Undated pages.** Chariot's help centre (GitBook), NCF, Vanguard and the MS GIFT pages state no date; they are recorded as `live`. The sample Fidelity Grant Details Report linked from the FAQ is a 2020 PDF, so it is not used. The column list above comes from the 2025 enrolment form instead.
- **Old evidence flagged.** Three (B) rows rest on 2022–2024 documents (Minneapolis 2022, the Foundant idea-lab reply 2024-08, Triangle 2024-10). They are within the 2021+ rule but flagged `recency_2025_26=no`.
- **Feature coding is a judgement.** A category chart is coded P for impact, not Y. Giving to public funds is coded P for (c), because the question asks about a page others can use to give *to a DAF*. Foundant’s vendor row is coded Y on the same kind of public-fund text, so it records a capability, not a documented DAF giving page [V wave 39A]
- **Chariot's list is not a census.** The managed-source list names platforms, not sponsors. The mapping of NPT and Vanguard to PayPal, and MS GIFT, AEF and RCF to Ren, comes from the sponsors' own pages [I].

## 6. Data dictionaries

### `grant-remittance-2026-11-19.csv`

| Column | Meaning |
|---|---|
| `row_id` | RA-01 … RA-14 |
| `fy2024_rank`, `fy2024_daf_assets_usd` | FY2024 corrected rank and `daf_assets_eoy`, joined by EIN from the league table by the script (blank for rail rows) |
| `sponsor`, `ein` | Sponsor or rail name; EIN (blank for rail rows) |
| `electronic_route`, `route_operator` | The electronic payment route the page describes, and who operates it |
| `ach_sec_code` | SEC code if a page states one; otherwise `not stated`, `n/a: …` (no ACH) or `not determinable` (blocked) |
| `grant_id_in_addenda`, `fund_name_in_addenda` | Whether a page says the grant ID or fund name travels in the ACH addenda or memo |
| `bank_statement_descriptor` | What the page says the bank statement shows |
| `batching` | Whether one payment can carry several grants |
| `out_of_band_channel`, `out_of_band_fields` | The channel that carries grant detail outside the payment, and the fields it is said to contain |
| `chariot_list_status` | Whether the sponsor or its rail appears on Chariot's managed-source or disbursement-partner lists |
| `key_quote` | Verbatim fragment from `source_url` (checked by script; blank for blocked or repo rows) |
| `source_url`, `source_date` | Primary URL (or repo pointer) and the date the document states, or `live` |
| `access_status` | `read`, `blocked: …`, or a repo-row note |
| `evidence_label` | F / R / B |
| `notes` | Second sources, conflicts, caveats |
| `retrieved` | 2026-11-19 |

### `portal-features-2026-11-19.csv`

| Column | Meaning |
|---|---|
| `row_id` | PF-01 … PF-32 |
| `vendor_platform` | Portal family: Ren DFX, iPhi, GivingPoint, DonorCentral, NPact Foundation Cloud, GiftingNetwork, Foundant CommunitySuite, own portal |
| `tenant` | Sponsor, community foundation or `vendor` |
| `segment` | `top20 sponsor`, `top20 sponsor (CF)`, `community foundation`, `vendor` |
| `rank_fy2024` | Top-50 rank and/or community-foundation rank (`CF n`) from repo CSVs |
| `feature` | `donor_impact_report` (a), `self_serve_grant_export` (b), `public_giving_page` (c) |
| `value` | Y / P / N / ND / U / B, as defined in §1.5 |
| `detail` | Plain-language summary |
| `quote` | Verbatim fragment (checked by script; blank where the value is ND, U or B) |
| `source_url`, `doc_date` | Primary URL and document date (PDF CreationDate/ModDate, page modified time, or `live`) |
| `recency_2025_26` | `yes` if the document is dated 2025–2026 or live; `no` otherwise; `n/a` if blocked |
| `evidence_label` | F / R / B |
| `access_status` | Fetch outcome |
| `notes` | Repo pointers and caveats |
| `retrieved` | 2026-11-19 |

The queue-proposals file follows the header and scales of `queue-proposals-gap19-13.csv`.

## 7. Source register

| # | Source | Date | URL |
|---|---|---|---|
| S1 | Fidelity Charitable, Charitable Organization EFT Enrollment Form | PDF 2025-12-02 / 2025-12-18 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/charitable-organization-eft-enrollment-form.pdf |
| S2 | Fidelity Charitable, Nonprofits FAQ | live | https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html |
| S3 | Fidelity Charitable, EFT for Nonprofits | live | https://www.fidelitycharitable.org/nonprofits/eft.html |
| S4 | Fidelity Charitable, Fidelity grants through Stripe | live | https://www.fidelitycharitable.org/nonprofits/fidelity-grant.html |
| S5 | Fidelity Charitable, Giving Account details (Gift4Giving) | live | https://www.fidelitycharitable.org/giving-account/giving-account-details.html |
| S6 | NPT, A Guide to your Donor-Advised Fund | PDF 2026-10-15 | https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf |
| S7 | NPT, Grant Payments with PayPal article | 2022-08-25, modified 2026-05-19 | https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/ |
| S8 | Vanguard Charitable, Nonprofit organizations | live | https://www.vanguardcharitable.org/nonprofit-organizations |
| S9 | PayPal newsroom, Grant Payments research note | 2023-12 | https://newsroom.paypal-corp.com/2023-12-PayPal-Grant-Payments |
| S10 | MS GIFT program page FAQ | live | https://www.morganstanley.com/gift |
| S11 | AEF, Charities page (Ren charity portal) | live | https://www.aefonline.org/charities/ |
| S12 | Ren, Payments page | modified 2026-11-04 | https://www.reninc.com/payments/ |
| S13 | Ren Help Center, Charity Grants (reports, CSV, ACH ID) | modified 2026-05-04 | https://intercom.help/rengiving/en/articles/6232128-charity-grants |
| S14 | Ren Help Center, Ren for Charities overview | modified 2026-07-08 | https://intercom.help/rengiving/en/articles/6229556-ren-for-charities-overview |
| S15 | Ren Help Center, 2026 Q1 release notes (Giving Compass) | modified 2026-03-05 | https://intercom.help/rengiving/en/articles/13792235-2026-q1-release-notes |
| S16 | RCF/Ren, Giving Platform Donor User Guide | PDF 2026-10-06 | https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf |
| S17 | RCF Program Circular | PDF 2026-06-01 / 2026-07-23 | https://rcf.donorfirstx.com/pdf/RCF/RCF%20Program%20Circular.pdf |
| S18 | BofA CGF, Guide to Navigating Your DAF | PDF 2025-11-14 / 2026-02-23 | https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf |
| S19 | NCF, Support page (electronic grants) | live | https://ncfgiving.com/support |
| S20 | NCF, Guide to giving at NCF (letter; donate button) | live | https://www.ncfgiving.com/guide-to-giving-at-NCF |
| S21 | Chariot Help Center, full text (Sources, Account Numbers, Custom Sources, Key Concepts) | live (GitBook) | https://help.givechariot.com/llms-full.txt |
| S22 | Chariot docs, DAFpay Managing Gifts (memo Tracking ID) | API version 2026-04-01 | https://docs.givechariot.com/v2026-04-01/guides/dafpay/integrate-dafpay/managing-gifts.md |
| S23 | Chariot webinar page, Powering modern DAF grants | live | https://givechariot.com/resources/webinars/-powering-modern-daf-grants |
| S24 | Chariot insight, "Not Enrolled for E-Pay" | live | https://givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors |
| S25 | CCT, Donor Portal FAQ (GiftingNetwork) | PDF 2025-12-02 | https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf |
| S26 | Greater Washington CF, new donor portal (NPact) | 2026-09-21 | https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived |
| S27 | Foundant, The Portal and the Giving Hub | 2024-08-30, modified 2026-04-22 | https://www.foundant.com/blog/the-portal-and-the-giving-hub-what-s-new/ |
| S28 | Foundant Idea Lab, Export grants or grant history | reply 2024-08-27 | https://idealab.foundant.com/forums/597718-communitysuite-idea-lab/suggestions/48688049-export-grants-or-grant-history-new-portal |
| S29 | Columbus Foundation, CSuite fund portal donor resources | PDF 2025-02-24 / 2025-04-22 | https://columbusfoundation.org/media/p1za1dz4/csuite-fund-portal-donor-resources-2025.pdf |
| S30 | CF for Greater Atlanta, Fund Advisor Portal Guide | PDF 2025-03-25 | https://cfgreateratlanta.org/wp-content/uploads/2025/03/Fund-Advisor-Portal-Guide.pdf |
| S31 | CF Tampa Bay, Portal guide | live | https://www.cftampabay.org/portal-guide |
| S32 | Omaha CF, My Account | modified 2025-03-04 (repo) | https://omahafoundation.org/myaccount/ |
| S33 | CF of Sarasota County, Giving Portal Manual | PDF 2025-06-10 | https://www.cfsarasota.org/files/galleries/CFSarasota_Giving_Portal_Manual.pdf |
| S34 | Triangle CF, New Donor Portal Guide | PDF 2024-10-07 | https://trianglecf.org/wp-content/uploads/2024/10/New-Donor-Portal-Guide-October-2024-.pdf |
| S35 | GKCCF, 7 tips for your online giving experience | 2022-03-28, modified 2026-07-14 | https://www.growyourgiving.org/news/7-tips-for-maximizing-your-online-giving-experience |
| S36 | Minneapolis Foundation, DonorView FAQs (carried) | PDF 2022-07-07 | https://www.minneapolisfoundation.org/wp-content/uploads/2023/11/DonorView-FAQs-Final.pdf |
| S37 | Blocked hosts (not read) | – | https://www.dafgiving360.org/ ; https://gspf.goldman.com/ ; https://rj.iphiview.com/ ; https://npact.document360.io/fims-and-donorcentral/docs ; https://npact.com/software/donorcentral/ ; https://www.paypal.com/us/cshelp/article/what-are-grant-payments-help883 |
| S38 | Repo carried | 2026-11-14/15 | data/mission-2026-11-14/sponsor-grant-payment-policies.csv; community-foundation-rails-portals-2026-v2.csv; donor-export-evidence-cf-2026.csv; daf-sponsor-league-table-fy2021-2025.csv; research/mission-2026-11-14/queue-batch33-voids-exports-rails.md |
