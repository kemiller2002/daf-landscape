# Gap-19 refresh: stale fee and terms evidence, and announced-vs-delivered

**Date:** 2026-11-19 · **Queue items:** P-GAP19-09 (fee and terms recency), P-GAP19-10 (announced vs delivered)

**Outputs**
- [`data/mission-2026-11-14/cf-daf-fee-census-refresh-2026-11-19.csv`](../../data/mission-2026-11-14/cf-daf-fee-census-refresh-2026-11-19.csv): 12 rows (FR01–FR12). These are every fee, terms or rail row in the repo whose evidence is dated before 2021.
- [`data/mission-2026-11-14/announced-vs-delivered-refresh-2026-11-19.csv`](../../data/mission-2026-11-14/announced-vs-delivered-refresh-2026-11-19.csv): 42 rows.
  - 22 are re-checks of every `no_public_evidence_yet` and `partial` row, plus AVD13 and AVD35 where the evidence changed.
  - 18 are new rows (AVD40–AVD57) for 2025–26 announcements named in the repo's newer docs.
- [`data/mission-2026-11-14/queue-proposals-g09.csv`](../../data/mission-2026-11-14/queue-proposals-g09.csv): P-G09-01 to P-G09-03.
- The source files are not modified: `cf-daf-fee-census-2026.csv`, `announced-vs-delivered.csv` and the report all stay as they were. Corrections are proposed in §4.

**Rules followed**
- **Access:** no logins, no forms, no sign-ups and no outreach.
- **robots.txt:** read before any page on a host was fetched, and obeyed (register in §5).
  - Hosts whose robots.txt could not be read were not fetched (docs.daffy.org).
  - Hosts that disallow generic clients were not fetched (gspf.goldman.com).
  - Hosts whose robots.txt disallows ClaudeBot or anthropic-ai were not fetched (www.foundant.com, per the repo).
  - NPT was not fetched because its Terms of Use bar robots (repo).
  - crt.sh was not used.
- **Recency:** 2021 and later. 2025–26 versions were preferred.
- **Labels:** [F] first-party page or PDF, fetched and read · [R] search-engine result only · [C] my computation · repo = carried from a repo file without a new fetch.

---

## 0. Headline

| Question | Answer |
|---|---|
| **Pre-2021 CF fee documents** | **Three of the five now have 2025–26 sources; two have none.**<br>- **Updated:** Minneapolis (2025-03 schedule), San Francisco (summary modified 2026-08) and Greater Cincinnati (fee sheet titled 2026, created 2025-12).<br>- **No newer source:** San Antonio's 2020 handbook and Toledo's "Rev. 12-2016" page are still the live documents [F]. |
| **What changed** | **Minneapolis** now publishes tiers above $1m (0.6% to $5m, 0.5% to $10m, negotiable above).<br>**San Francisco** keeps the same tiers but states no $500 minimum, and its top tier is now open-ended.<br>**Cincinnati** cut its headline rate from 1.1% to 0.95%, publishes tiers to $5m and raised its minimum from $400 to $600 [F]. |
| **Effect on the CF/national ratio** | **None.** With the three refreshed schedules added (n = 37), the medians stay at **100 / 100 / 67.2 bps** at $100k / $1m / $10m, so the 1.7x / 2.2x / 3.6–4.7x ratios stand.<br>- **Coverage:** the published-schedule count rises from 34 to 37, and their share of top-100 CF DAF assets from 43.0% to 46.1% [C].<br>- **Interquartile ranges:** 100–125, 100–121.9 and 48.0–84.4 bps.<br>- **Asset-weighted means:** 99.4 / 91.2 / 60.1 bps. |
| **Other pre-2021 terms rows** | None could be updated.<br>- **GS DAF 2008 circular:** robots.txt disallows the host.<br>- **AEF 2012 survey rate:** AEF publishes no schedule, and its "Welcome Hub" fee page is now 404.<br>- **RCF terms (©2014):** re-read; the scraping clause is unchanged.<br>- **Harvard gift guide (May 2020):** still the posted version.<br>- **NPT 2019 due-diligence PDF:** not fetched. A 2024-09 NPT guide shows in search results only [R].<br>- **IRS Notice 2017-73:** still the reliance guidance (repo). |
| **Announced vs delivered (22 re-checks)** | **5 of 22 rows changed status.**<br>- **To delivered:** AVD09 (TIFIN Give campaigns) and AVD29 (Charityvest commission-free stock gifts).<br>- **To partial:** AVD02 (Ren × Giving Compass, live on the charity side), AVD17 (GiveClear Direct: the page is live but still labelled "Coming Soon") and AVD31 (Charityvest on Chariot for direct accounts; turnkey partners unverified).<br>- **Unchanged:** 17 rows. AVD35 (Fidelity e-only) is still contradicted.<br>- **New totals on the 39-row register:** 17 delivered / 11 partial / 9 no evidence / 2 contradicted (was 15 / 10 / 12 / 2). |
| **New rows (18)** | 8 delivered, 3 partial, 7 no public evidence yet.<br>- **Overdue:** the ImpactAssets DAF Hub (promised for 2026-09-08). Its log-in is still on iPhi.<br>- **Not yet observed:** the Vanguard Charitable go-live on Give Interactive and the Vanguard–Altruist close.<br>- **Delivered:** Altruist's Endaoment-sponsored DAF, Janus Henderson/Givinga accounts and Bloomerang DAFpay are live. |

---

## 1. Fee and terms refresh (P-GAP19-09)

### 1.1 The five pre-2021 CF schedules

All five rows come from `cf-daf-fee-census-2026.csv` with status `published_schedule_pre2021`. The bps figures use the census engine's conventions (marginal tiers, minimum applied as a floor, blank above a stated cap) [C].

| ID | CF (rank) | Old source (date) | Current source (date) | Current DAF admin terms | bps @ $100k / $1m / $10m | Change vs old |
|---|---|---|---|---|---|---|
| FR01 | Minneapolis (19) | DAF policies PDF (2020-09) | [Administrative Fee Schedule 2025](https://www.minneapolisfoundation.org/wp-content/uploads/2025/03/administrative-fee-schedule-2025.pdf); [DAF policies 2025](https://www.minneapolisfoundation.org/wp-content/uploads/2025/03/DAF-policies-2025.pdf) (2025-03-24) | First $1M 1%; next $4M 0.6%; next $5M 0.5%; >$10M negotiable. Minimum $750 ($10,000 for Signature Funds). Fee on a 36-month average balance. $10,000 to open; $250 minimum grant; grants paid by check in 5–10 business days | 100 / 100 / 59 | Tiers above $1m now published. Rate to $1m and minimum unchanged [F] |
| FR02 | San Francisco (20) | 2019 one-pager | [DAF Summary of Fees](https://sff.org/wp-content/uploads/2026/10/DAF-Summary-of-Fees.pdf) (modified 2026-08-25; uploads/2026/10) | $0–3m 1.00%; $3–10m 0.75%; $10–25m 0.50%; $25m+ 0.25%. $10,000 to open; no minimum fee stated. Investment fees ~0.13–1.10% plus 0.07% administration and 0.04% custodian/consultant. Outside manager from $1m | 100 / 100 / 82.5 | Same tiers; top tier open-ended; no $500 minimum stated; outside-manager threshold down from $2.5m (2024-06 version) to $1m [F] |
| FR03 | Greater Cincinnati (27) | DAF FAQs (2020-07) | [Community Investment Fees 2026](https://www.gcfdn.org/wp-content/uploads/2025/12/GCF-Community-Investment-Fees-2026.pdf) (2025-12-03); [DAF FAQ 2026](https://www.gcfdn.org/wp-content/uploads/2026/02/GCF-Donor-Advised-Funds-FAQ-2026-2.pdf) (2026-02-24) | 0.95% on the first $1M; 0.85% $1–2.5M; 0.55% $2.5–5M; personalised over $5M. Minimum fee $600. Any initial contribution | 95 / 95 / – (cap) | Rate 1.1% → 0.95%; minimum $400 → $600; tiers published to $5m [F] |
| FR04 | San Antonio (65) | Donor handbook (2020-10) | Same handbook, still the only fee document (sitemap scan) | Minimum fee $750; no percentage schedule | – | None found [F] |
| FR05 | Greater Toledo (79) | investments-fees page (Rev. 12-2016) | Same page; [fund-comparison](https://toledocf.org/fund-comparison) (undated) | Growth Fund 1.45% total, minimum $100, $25,000 to open; plus a .12% bank and recordkeeping fee (fees page) or a ".25%" bank/investment fee (fund-comparison page) | – | None. The two live pages disagree on the bank fee [F] |

**Recomputed census statistics** [C], for when FR01–FR03 are merged:

| Metric | Census (2026-11-15) | With FR01–FR03 |
|---|---|---|
| Published 2021+ schedules (top 100) | 34 (43.0% of DAF assets) | 37 (46.1%) |
| Pre-2021 only | 5 | 2 |
| Median admin bps @ $100k / $1m / $10m | 100 / 100 / 67.2 (n = 34 / 34 / 33) | 100 / 100 / 67.2 (n = 37 / 37 / 35) |
| Interquartile range | 100–131 / 100–125 / 46.5–85 | 100–125 / 100–121.9 / 48.0–84.4 |
| Asset-weighted mean | 99.5 / 90.6 / 59.5 | 99.4 / 91.2 / 60.1 |
| Median minimum annual fee (published only) | $250 (n = 24) | $250 (n = 26) |
| CF median ÷ nationals (60 / 45 / 14.3–18.8 bps) | 1.7x / 2.2x / 3.6–4.7x | unchanged |
| Above 45 bps at $1m; above 60 bps at $100k | all 34; 32 of 34 | all 37; 35 of 37 |

The San Francisco admin layer (100 bps at $250k) is the one `all-in-cost-comparison-2026.csv` already takes from SFF's 2026 Advisor Guide. **The 2.13% all-in figure cited in the report and the synthesis is unaffected.**

### 1.2 Other pre-2021 fee, terms and rail rows

| ID | Row(s) | Old evidence | Result 2026-11-19 | Status |
|---|---|---|---|---|
| FR06 | GS DAF Program Circular: 7 rows in `bank-program-terms-2026.csv`, 3 in `all-in-cost-comparison-2026.csv`, row 52 in `sponsor-fee-schedules.csv` | 2008-08 circular | gspf.goldman.com robots.txt is `User-agent: * Disallow: /` (only named search bots allowed), so the host was not fetched. Search found no 2021+ public circular | not_fetched_robots |
| FR07 | AEF starting rate, row 53 in `sponsor-fee-schedules.csv` | 2012 Chronicle survey (0.70%) | No public schedule. The engage "Welcome Hub" fee page is 404, and the engage sitemap lists only pilot and upgrade hubs | no_newer_public_source |
| FR08 | RCF Terms & Conditions (top-20 terms census) | undated (©2014) | Re-read. The ©2014 and ©2017 lines remain, and the "deep-link, scrape, frame or mirror ... without the advance written authorization" clause is unchanged | unchanged (code G stands) |
| FR09 | NPT due-diligence PDF (GO-S4) | 2019-09 | Not fetched (NPT Terms of Use). Search lists a 2024-09 "A Guide to your Donor Advised Fund" PDF as a candidate [R] | not_fetched_terms |
| FR10 | Harvard Gift Policy Guide (GO-03) | 2020-05 | Still posted. The PDF was created 2020-05-14 and its cover reads "MAY 2020" | unchanged, still pre-2021 |
| FR11 | IRS Notice 2017-73 (GO-R1) | 2017-12 | The repo finds no final DAF regulation (wave 24A; 2026-11-19 sweep), so the reliance language stands | unchanged (regulatory) |
| FR12 | Matching-gift policies MG05/06/10/12/13 | 2011–2015 | Not refreshed. These are employer policies, not sponsor fee, terms or rail rows, and the file already flags them | out of scope |

**Not covered here:** the post-2021 but over-12-month items named in P-GAP19-09 (UBS Feb 2023, RCF due diligence Mar 2023, Northwestern Mutual Nov 2024, the 2023–24 ADV rows and the rail-share observations). They are carried to P-G09-01. A scan of the date columns in `grant-rail-shares-panel-2026.csv`, `adviser-fee-evidence-2026.csv`, `adviser-fees-observed-2026.csv` and six other fee and terms files found no pre-2021 evidence dates.

---

## 2. Announced vs delivered (P-GAP19-10)

### 2.1 Re-checks of the 22 open rows (plus AVD13, AVD35)

| ID | Company: capability | 2026-11-14 | 2026-11-19 | Key evidence |
|---|---|---|---|---|
| AVD02 | Ren: Giving Compass impact data | no evidence | **partial** | Ren for Charities release notes: validation launched 2026-03-05; uploads 04-17; "donor visibility" wording 06-22; Impact Stories 07-01. The how-to still says "Stay tuned" for the donor side [F] |
| AVD03 | Ren: use of Bain proceeds | partial | partial | Adds 2026 ACH-upload (08-26) and donor ACH request (Nov) releases [F] |
| AVD04 | Ren: Great Hill roadmap | partial | partial | Same; no roadmap published [F] |
| AVD07 | Ren: invested-crypto DAF | no evidence | no evidence | The May 2026 noncash sheet lists crypto as accepted gifts only [F] |
| AVD08 | Ren: daily unitization | no evidence | no evidence | Only vendor sub-accounting PDFs (2025-05) [R] |
| AVD09 | TIFIN Give: community campaigns | partial | **delivered** | Knowledge-centre "Community Giving Campaigns" how-to with four entry points [F] |
| AVD12 | TIFIN Give: Louise | partial | partial | None of the 29 knowledge-centre articles mentions Louise [F, absence] |
| AVD13 | TIFIN Give: Chariot | delivered | delivered (stronger) | Chariot case study: 82% of volume electronic, $34.1M and 5,175 grants in the first 4 months; KB says Chariot is the default rail [F] |
| AVD15 | TIFIN Give: Confluence 2026 | no evidence | no evidence | Confluence's site names no TIFIN or branded DAF [F, absence] |
| AVD17 | GiveClear Direct | no evidence | **partial** | The "For Individuals" page is live ("Open a Giving Fund", "no advisor required"), but the menu still says "(Coming Soon)" [F] |
| AVD18 | GiveClear 2026 targets | no evidence | no evidence | Not yet due [F] |
| AVD20 | Chariot: "ubiquitous layer" | partial | partial | More partners, but Fidelity still uses Stripe/ACH [F] |
| AVD21 | Chariot: Gift Processing | partial | partial | No GA entry after the 2026-01-14 beta [F] |
| AVD22 | Chariot: DAFpay Donor Accounts | partial | partial | Still beta with design partners [F] |
| AVD23 | Chariot: FDX v6 | no evidence | no evidence | Docs updated 05-22, OAuth added 09-08; no aggregator named [F] |
| AVD29 | Charityvest: zero-fee stock gifts | partial | **delivered** | "Stock and ETF donations trade commission-free". Invested accounts are still 0.60% on the first $500k [F] |
| AVD31 | Charityvest: Chariot from Aug 2026 | no evidence | **partial** | The donor guide says grants go "electronically through Chariot or by weekly check" and no longer mentions PayPal. Turnkey partners are unverified [F] |
| AVD32 | Foundation Source: multi-custodial | partial | partial | No named customer [R] |
| AVD33 | Foundation Source: DAF OS/FundOS | no evidence | no evidence | No named sponsor customer [R] |
| AVD34 | Foundation Source: AI | no evidence | no evidence | The 2026-11-18 Outlook discusses "responsible AI" but announces no product [F] |
| AVD35 | Fidelity: e-only from July 2026 | contradicted | contradicted | The FAQ still says "we do not currently require EFT enrollment" [F] |
| AVD36 | Fidelity: DAF Direct | partial | partial | Site live [F] |
| AVD38 | Groundswell: 24-hour grants | no evidence | no evidence | Vendor claim restated; no measurement [F] |
| AVD39 | Benevity: Alaya by 2026-12-15 | no evidence | no evidence | Not yet due. The help page returned 403 [none] |

**Register totals (39 rows):** 17 delivered, 11 partial, 9 no public evidence yet and 2 contradicted, against 15 / 10 / 12 / 2.

### 2.2 New rows (2025–26 announcements from the repo's newer docs)

| ID | Company: capability (announced) | Status | Evidence |
|---|---|---|---|
| AVD40 | Give Interactive: Vanguard Charitable recordkeeping (2025-11-04) | no evidence | No go-live seen (repo sweep 2026-11-19); no date was promised |
| AVD41 | ImpactAssets: DAF Hub on 2026-09-08 | no evidence (overdue) | The transition page is unchanged ("AUG. X", Lorem ipsum FAQ), and the homepage log-in still points to iphi.stellartechsol.com [F] |
| AVD42 | Daffy: Quick Donate (2025-04) | delivered | Help how-to; "never submits a donation without your confirmation" [F] |
| AVD43 | Daffy: AI charity-data flagging (2025-04) | no evidence | The "How is Daffy using AI" article is now 404 [F, absence] |
| AVD44 | Altruist/Endaoment DAFs (2026-10) | delivered | Live page: 50 bps starting fee, $0 minimums, sponsored by Endaoment [F] |
| AVD45 | Vanguard acquiring Altruist (2026-08-26) | no evidence | The release still says "expected to close later this year" [F] |
| AVD46 | Janus Henderson/Givinga accounts (2025-09) | delivered | Live site: open an account, 30 bps, Givinga named [F] |
| AVD47 | Bloomerang DAFpay for all customers (Oct 2026) | delivered | "now available for all Bloomerang Fundraising customers" [F] |
| AVD48 | Blackbaud Development Agent, US (2026-03) | delivered | Product page: US RE NXT customers; vendor metrics [F] |
| AVD49 | Blackbaud agent, international and Enterprise ("later in 2026") | no evidence | The FAQ still says US RE NXT only [F] |
| AVD50 | Blackbaud further agents (2026-08) | no evidence | "actively working toward additional agents" [F] |
| AVD51 | Benevity Match Assurance (2026-03) | delivered | "adopted by more than 500 clients" (vendor) [F] |
| AVD52 | Benevity Impact Workspace ("later this year") | no evidence | No launch release in the sitemap [F, absence] |
| AVD53 | Fundraise Up Agentic Giving (2026) | partial | "rolling out in stages"; early access [F] |
| AVD54 | Bonterra Que (2025-10-01) | partial | Launch post plus vendor-only claims (repo AP11/AP12) [F/repo] |
| AVD55 | Foundant Fia (2026-09-02) | partial | Beta; controls claimed, not documented; foundant.com release read 2026-11-20: "currently in beta with its initial group of early-adopter organizations" [F] |
| AVD56 | Ren Recognize (2026-08-06) | delivered | Help article [F] |
| AVD57 | Ren donor ACH request emails (Nov 2026) | delivered | Help article [F] |

**Totals if merged (57 rows):** 25 delivered, 14 partial, 16 no public evidence yet and 2 contradicted.

**Not added: Blackbaud Giving Fund, NPT export and the Give Interactive CCT tenant.** I found no dated 2025–26 announcement for any of them. CCT rests on certificate names only. SEI Charitable Fund is already AVD14 (delivered).

---

## 3. What this changes in the findings

- **CF fee gap: no change to any cited ratio or median.** Coverage of the census improves (37 schedules, 46% of assets). The refreshed sources show lower rates at scale than the old ones disclosed: Minneapolis now publishes 59 bps at $10m, and Cincinnati cut its rate to 95 bps up to $1m. Both are still above the nationals' 45 bps at $1m.
- **Delivery record: slightly better than reported.** Three rows moved from "no evidence" to "partial" and two from "partial" to "delivered". No row moved down. The by-company bullets in report §5 still hold:
  - TIFIN Give's Louise still has only vendor evidence.
  - Ren and Foundation Source still lack evidence for unitization and DAF OS.
  - Daffy's sponsor-side AI flagging (synthesis §2, "announced only") is still unevidenced (AVD43).
- **The rail-switch statement now has first-party confirmation.** Charityvest's own guide confirms Chariot for direct accounts.

---

## 4. Proposed Find/Replace corrections (not applied)

The §5 corrections are safe on the refresh alone. The fee corrections apply once FR01–FR03 are merged into the census (P-G09-01).

1. **`research/DAF-INDUSTRY-REPORT-2026-11.md` §5 table**
   - **Find:** `| Evidence of delivery | 15 |` · **Replace:** `| Evidence of delivery | 17 |`
   - **Find:** `| Partial | 10 |` · **Replace:** `| Partial | 11 |`
   - **Find:** `| No public evidence yet | 12 |` · **Replace:** `| No public evidence yet | 9 |`
   - Add after the table: "Re-checked 2026-11-19: 5 status changes, all upward (repo [`announced-vs-delivered-refresh-2026-11-19.csv`](../data/mission-2026-11-14/announced-vs-delivered-refresh-2026-11-19.csv))."
2. **Same file, §5 Daffy bullet** (only if AVD42–43 are merged)
   - **Find:** `- **Daffy:** 5 of 5 delivered.`
   - **Replace:** `- **Daffy:** 5 of 5 original items delivered; of two 2025 AI items added on 2026-11-19, Quick Donate is documented and the charity-data flagging is not.`
3. **Same file, line 797 (CF fee summary)**
   - **Find:** `34 top-100 CFs (43% of top-100 CF DAF assets) publish a full fee schedule`
   - **Replace:** `37 top-100 CFs (46% of top-100 CF DAF assets) publish a full fee schedule (refreshed 2026-11-19)`
   - The medians and ratios in the same sentence are unchanged.
4. **`research/mission-2026-11-14/direction-cf-consolidation-fees.md` §0**
   - **Find:** `**34 publish a full schedule for a standard DAF from a 2021+ source. They hold 43.0% of top-100 CF DAF assets.**<br>- 5 more publish only pre-2021 schedules.`
   - **Replace:** `**37 publish a full schedule for a standard DAF from a 2021+ source. They hold 46.1% of top-100 CF DAF assets.**<br>- 2 more publish only pre-2021 schedules (San Antonio, Toledo); Minneapolis, San Francisco and Greater Cincinnati moved to 2025–26 sources on 2026-11-19.`
   - **Find:** `**Median 100 / 100 / 67 bps across the 34 published schedules** (interquartile ranges 100–131, 100–125 and 47–85). The DAF-asset-weighted means are 99.5 / 90.6 / 59.5 bps.`
   - **Replace:** `**Median 100 / 100 / 67 bps across the 37 published schedules** (interquartile ranges 100–125, 100–122 and 48–84). The DAF-asset-weighted means are 99.4 / 91.2 / 60.1 bps.`
   - **Find:** `32 of 34 CFs charge more` · **Replace:** `35 of 37 CFs charge more`
   - **Find:** `All 34 CFs charge more` · **Replace:** `All 37 CFs charge more`
5. **`research/mission-2026-11-14/competitive-history-timelines.md` §rails**
   - **Find:** `The only observed switch between rails is Charityvest moving from PayPal to Chariot in August 2026`
   - **Replace:** `The only observed switch between rails is Charityvest moving from PayPal to Chariot in August 2026, confirmed for direct accounts in Charityvest's donor guide on 2026-11-19 ([Charityvest guide](https://guide.charityvest.org/for-donors/getting-started/grants-to-charity))`

`gap19-clarity-edf-new-findings.md` line 72 also says "across the 34 published schedules". Update it the same way when the census is merged.

---

## 5. Source and robots register

| Host | robots.txt (2026-11-19) | Fetched? |
|---|---|---|
| www.minneapolisfoundation.org | `*`: Disallow /wp-admin/ | yes |
| sff.org | `*`: Disallow /wp-admin/; Crawl-delay 10 (honoured) | yes |
| www.gcfdn.org | `*`: Disallow (empty) | yes |
| saafdn.org | `*`: Disallow (empty); Crawl-delay 10 (honoured) | yes |
| toledocf.org | Served with HTTP 404 but readable; `*` disallows /cpresources/, /vendor/, /.env, /cache/ (GPTBot, Google-Extended, PerplexityBot: Disallow /) | yes |
| gspf.goldman.com | `*`: Disallow / | **no** |
| www.aefonline.org, engage.aefonline.org | `*`: Disallow empty or /wp-admin/; Crawl-delay 10 | yes (engage) |
| renaissancecharitable.org | `*`: Disallow empty; Crawl-delay 10 | yes |
| alumni.harvard.edu | `*`: Disallow /core/, /admin/ and others; path allowed | yes |
| www.nptrust.org | `*` allowed, but Terms of Use bar robots (repo) | **no** |
| intercom.help | `*` disallows /not-authorized, /not-found, /[helpCenterIdentifier]/ | yes (Ren, TIFIN Give KB) |
| help.daffy.org | Same Intercom rules | yes |
| docs.daffy.org | robots.txt returns HTML (unreadable) | **no** |
| www.reninc.com | `*`: Disallow /wp-admin/ (Anthropic-AI group: Allow /faqs/, no Disallow) | one PDF |
| docs.givechariot.com | `*`: Allow / (disallows /api/fern-docs/) | yes |
| www.givechariot.com | `*`: Disallow /admin/* | yes |
| www.giveclear.org | `*` with no Disallow | yes |
| guide.charityvest.org | `*`: Allow / | yes |
| www.fidelitycharitable.org | `*` disallows /retired/ and three others | yes |
| www.dafdirect.org | `*`: Disallow /cgi-bin | yes |
| www.groundswell.io | `*`: Disallow (empty) | yes |
| causeshelp.benevity.org | `*` allows /hc/…/articles | attempted; **HTTP 403** |
| benevity.com | Allow / (incl. ClaudeBot) | yes |
| www.confluencefp.com | Disallow (empty) | yes |
| www.prnewswire.com | `*` disallows template and multivu paths | yes |
| impactassets.org | `*`: Disallow /wp-admin/ | yes |
| altruist.com | `*` disallows /wp-json/, /?rest_route= | yes |
| corporate.vanguard.com | `*`: Disallow /404 | yes |
| bloomerang.com | Allow / (search params disallowed) | yes |
| www.blackbaud.com | `*`: Disallow /wp-content/uploads/*.pdf | yes |
| fundraiseup.com | Allow / | yes |
| www.bonterratech.com | Allow / (incl. ClaudeBot) | yes |
| www.janushenderson.com → www.janushendersoncharitable.org | Both allow `*` except `;` and /prod/documents/docId/ | yes. The second host's robots.txt was read after the redirect, so that one page preceded its robots check |
| www.foundant.com | Disallows ClaudeBot and anthropic-ai (repo) | **no** |

Search-only sources ([R]) are listed in the CSVs' URL columns (BridgeFT, Foundation Source newsroom, NPT 2024 guide, Ren sub-accounting PDF).

## 6. Limits

- **Pages not read:**
  - The Greater Cincinnati FAQ PDF's text layer is partly garbled, so its minimum grant was not read.
  - I did not open any account, so GiveClear Direct and Altruist account opening were not tested.
  - The Benevity help page (403) and the docs.daffy.org pages were not read.
- **Absence findings:** AVD12, AVD15, AVD43 and AVD52 rest on the pages and sitemaps listed. Missing evidence is not treated as non-delivery.
- **Vendor metrics:** figures for Blackbaud, Benevity, Chariot/TIFIN and Bloomerang are self-reported and unaudited.
