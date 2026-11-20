# P-B39N6-03: pass-through recipients — large DAF grantees with no public donate page

**Date:** 2026-11-20 · **Task:** b39n6-03 · **Queue item:** P-B39N6-03

**Outputs**
- [`data/mission-2026-11-14/pass-through-recipients-2026-11-20.csv`](../../data/mission-2026-11-14/pass-through-recipients-2026-11-20.csv): 28 rows × 68 columns, one per EIN in the population (§7).
- [`scripts/mission_pass_through_recipients.py`](../../scripts/mission_pass_through_recipients.py): stdlib, functional style. It has two stages: `fetch` (990 XML and public web pages) and `report` (pure; writes the CSV and a JSON summary). It imports `mission_recipient_sectors.py`, `mission_daf_to_daf.py`, `mission_net_payout.py` and `mission_990_contractors.py` unchanged. Two `report` runs gave byte-identical CSV and JSON.
- [`data/mission-2026-11-14/queue-proposals-b39n6-03.csv`](../../data/mission-2026-11-14/queue-proposals-b39n6-03.csv): P-B39N603-01..06.

**Labels:** **[F]** filed value; **[C]** computed by the script; **[I]** inference or hand judgement; **[W]** read from a public web page (URL given).

---

## 0. Answers in brief

| Question | Answer |
|---|---|
| Population | 28 EINs have `scan_status = home_only_no_donate_link` in the donate-page scan [C]. They took **$3.24bn of top-50 FY2023–24 Schedule I dollars net of DAF-to-DAF: 4.14% of $78.29bn**. DAF-weighted, the figures are $3.19bn and **4.29% of $74.28bn** [C].<br>The 28 are mixed. My judgement [I] sorts them into:<br>- 3 fiscal sponsors;<br>- 5 pooled funds;<br>- 2 grantmaking public charities;<br>- 3 single-recipient conduits;<br>- 2 affiliated support foundations;<br>- 1 giving platform;<br>- 3 private foundations;<br>- 8 operating charities;<br>- 1 church (LDS, which files no 990). |
| **Share taken by the pass-through intermediaries** | **Core intermediaries** (the 10 fiscal sponsors, pooled funds and grantmaking public charities): **$1.77bn, 2.26% filed / 2.33% DAF-weighted** [C].<br>The **7 named in the queue item** (NVF, Blue Meridian, US Energy Foundation, ClimateWorks, Hopewell, Windward, Energy Foundation China) take **$1.42bn, 1.81% / 1.88%** [C].<br>The rule-based pass-through set covers 18 EINs: fiscal sponsor, or grants ≥ 50% of expenses. It takes $2.25bn, 2.87% / 2.97% [C]. |
| Individually (DAF-weighted share of top-50 dollars) [C] | - NVF 0.57%;<br>- Blue Meridian 0.49%;<br>- Climate Imperative 0.31%;<br>- US Energy Foundation 0.25%;<br>- ClimateWorks 0.23%;<br>- Hopewell 0.19%;<br>- Windward 0.11%;<br>- Charter School Growth Fund 0.10%;<br>- Energy Foundation China 0.04%;<br>- Stand Together Trust 0.04%. |
| **How they receive DAF grants** | - **None of the 28 shows DAF instructions, a DAF widget, sponsor links, wire/ACH details or a "give through your DAF" page** on the public pages read [C, W].<br>- **For the 10 core intermediaries there is no giving page of any kind.** What the pages offer is a relationship path:<br>  - partner-interest forms (Blue Meridian; Windward's "Partner with Windward" option);<br>  - partner commitments (Blue Meridian General and Impact Partners commit **$50m and $15m**);<br>  - "Projects raise their own funding" (Hopewell);<br>  - general info@ e-mails [W].<br>- So the DAF grant is a sponsor-initiated payment that follows a donor recommendation. The recipient publishes no rail; the sponsor's grant portal and its payment method are the only path that can be seen [I]. |
| **Does the money pass onward?** | **Yes, mostly within the same two years.** Own 990s, tax years 2023+2024, Part IX lines 1–3 ÷ Part VIII 1h [C]:<br>- **core 10: 0.86** (net of grants to other population members: 0.83);<br>- **named 7: 0.83** (0.81);<br>- fiscal sponsors 0.75;<br>- pooled funds 0.89;<br>- operating charities 0.16. |
| Per organisation (onward ratio) [C] | - **Blue Meridian 1.69**: it granted $792.5m against $470.2m contributed and drew down net assets by $344.1m;<br>- Climate Imperative 1.04;<br>- NVF 0.84;<br>- ClimateWorks 0.69;<br>- Windward 0.66;<br>- US EF 0.60;<br>- EF China 0.60;<br>- Hopewell 0.57.<br>For the fiscal sponsors, the remainder is mostly spent directly by sponsored projects (staff and programme costs), not kept: NVF's net assets fell $360.7m over the two years. |
| Chains inside the set | $183.1m of the population's own Schedule I grants go to other population EINs [C]. Examples:<br>- Climate Imperative → Energy Foundation China $56.8m and US EF $34.7m;<br>- ClimateWorks → the two Energy Foundations $40.5m;<br>- Hopewell → NVF $17.6m.<br>Some DAF dollars therefore pass through two intermediaries before reaching an operating charity. |

---

## 1. Method

### 1.1 Population
- Source: `nonprofit-donate-page-daf-scan-2026.csv` (P-NEW-NPA-01; [scan note](direction-nonprofit-donate-pages.md)), rows where `scan_status = home_only_no_donate_link`. That is **28 of 300**.
- In those rows the homepage was robots-allowed and read, but no donate/give link was found on it.
- The population is defined by the scan, not by organisation type. It therefore includes non-intermediaries: a church, a university foundation, research institutes, CDFIs and private foundations. These are typed in §1.4 and reported separately.

### 1.2 Dollars [C]
- **Lines.** Every Schedule I Part II line of the 94 itemising top-50 sponsor-years (FY2023–FY2024). These come from the line cache of `mission_recipient_sectors.py`, with returns chosen by `mission_daf_to_daf.pick_returns`.
- **DAF-to-DAF removed** with `mission_recipient_sectors.annotate`: whitelist `include`, self-lines, and blank-EIN name matches.
- **Denominators** reproduce the repo's sector file exactly: **$78,287,627,404 filed** and **$74,281,457,270 DAF-weighted** (`daf-grant-recipient-sectors-top50.csv`, `all_top50_itemising, 2023-2024, ALL`).
- **DAF weighting** is the repo's rule. Each sponsor-year's lines are multiplied by `daf_share_of_grants` from `sponsor-cost-structure.csv`, capped at 1. 94/94 sponsor-years have a weight.
- **Check.** The scan's frame excludes university/hospital grantors (scope `ex_uh`). On that scope my per-EIN dollars reproduce the scan's `daf_grant_usd_fy2023_2024` for **28/28** EINs (within $1). The headline uses the `all` scope; it differs by at most $0.2m per EIN.

### 1.3 Onward flow from the recipient's own returns [C]
- **Returns.** Each EIN's e-filed return for tax years 2023 and 2024:
  - IRS TEOS `index_2023..2026`, RETURN_TYPE 990, 990-EZ or 990-PF;
  - latest OBJECT_ID per TAX_PERIOD;
  - read from the GivingTuesday mirror (`gt990datalake-rawdata.s3.amazonaws.com`, robots.txt 404, so no rules apply).
- **Coverage.** 27 of 28 EINs have two years, giving 54 returns. LDS files only 990-T.
- **Inflow:** Part VIII line 1h (990-PF: Part I line 1; 990-EZ: line 1).
- **Outflow:** Part IX lines 1 + 2 + 3: grants to domestic organisations, to individuals, and foreign grants (990-PF: Part I line 25; 990-EZ: line 10). The Schedule I Part II recipient table is also read, for its count and $ and for flows to other population EINs.
- **Onward ratio** = Σ outflow ÷ Σ inflow over the two tax years. The net version subtracts Schedule I $ paid to other population EINs. Grants-share-of-expenses = outflow ÷ total functional expenses.
- **Retention.** Net assets at the start of the first year, set against the end of the second.
- **Timing flag.** Set where top-50 DAF $ exceed the recipient's contributions over the two years. That is impossible within the same years, so it signals a timing or revenue-line mismatch: 6 EINs.

### 1.4 Classification
- **Rule** (`pass_through_class`) [C], first match wins:
  1. `fiscal_sponsor`: the 990 describes the filer as a fiscal sponsor (FISCAL(LY) SPONSOR in text outside the grant tables), or the homepage says so;
  2. `regranting_intermediary`: Part IX lines 1–3 are at least 50% of total expenses;
  3. otherwise `operating`; `no_990` where there is no return.
- **Hand subtype** (`hand_subtype`) [I] comes from the 990 text, the Schedule I pattern and the site. The basis is recorded per row.
- **The core intermediaries** are those hand-typed `fiscal_sponsor`, `pooled_fund` or `grantmaking_public_charity` (10 EINs).
- The rule's 18 also include:
  - single-recipient conduits (Our American Future Foundation, LOFT/Leadership Network, Breakthrough Energy Catalyst);
  - the UCLA Foundation and Primary School, which pass money to an affiliate;
  - Bright Funds, a giving platform;
  - a scholarship private foundation;
  - Connecticut Project.

### 1.5 Receiving channel (web) [C, W]
- **robots.txt first**, for every host actually requested. www and bare hosts are checked separately, and each check is logged (§6.2). A 403 or other unreadable result means nothing is fetched from that host.
- **Pages read, where allowed:**
  - the homepage;
  - up to 10 same-site links whose URL or anchor suggests giving, partnering or fiscal sponsorship (news, blog and report paths skipped);
  - up to 6 sitemap URLs;
  - six fixed paths: `/donate`, `/give`, `/support`, `/ways-to-give`, `/faq`, `/contact`.
- **How pages were read:**
  - raw HTML with urllib, UA `research-script/1.0`, at least 1.5 s between requests to a host;
  - no JS rendering, no forms submitted, no logins;
  - off-host redirects were not followed into content.
- **Detectors:** donor-advised / DAF text; DAFpay/Chariot or DAF Direct; Fidelity, Schwab and Vanguard links; wire/ACH; check by mail; stock gifts; grant agreement; fiscal-sponsor language; pooled-fund commitment terms; own EIN shown; giving e-mails.
- **Channel class**, first match:
  1. `daf_instructions`;
  2. `giving_page_no_daf` (a giving path with its own content, not the homepage served again);
  3. `giving_contact_only`;
  4. `no_giving_info_found`;
  5. otherwise `robots_unreadable` / `redirects_offsite`.
- **Hand reading.** I read the FAQ, partner, contact and fiscal-sponsorship pages of the core intermediaries; notes are in `channel_note_hand`. Of those hand-read pages, only robots-allowed ones were read (helper with the same robots check).

## 2. Overlap with other studies (read, not edited)

| Study | Overlap | What this note adds |
|---|---|---|
| [g0503-03 de facto fiscal sponsors](g0503-03-de-facto-fiscal-sponsors.md) | - NVF, Windward and Hopewell are Q-B15 hosts, already counted by the refined fiscal-sponsor flag.<br>- NVF and Windward are "two-project hosts".<br>- Hopewell is one of 7 Q-B15 hosts with no project-style line.<br>- Their top-50 $ figures agree: NVF 48 lines $432.0m; Windward 31 lines $80.5m; Hopewell 57 lines $149.7m, matching `fiscal-sponsor-ein-list-2026-11-19.csv`.<br>- None of the 5 hosts g0503-03 adds is in this population. | Outflow side (990 Part IX / Schedule I) and receiving channel. No change to the fiscal-sponsor flag or the unions is proposed. |
| [g050303-02 AUM and NPT foreign](g050303-02-aum-and-npt-foreign.md) | - Assets Under Movement is not in this population.<br>- The overlap is method only: the 990 read, and the DAF-share apportionment and Schedule D cautions.<br>- 5 of the 10 core intermediaries make large Part IX line 3 foreign grants (ClimateWorks $223.0m, Climate Imperative $151.5m, NVF $113.2m, EF China $109.1m, Windward $80.0m). That is a second-hop foreign flow that the sponsor-level foreign figures in that note do not capture. | Look-through proposal P-B39N603-01. |
| [b40n12 DAF share of recipient revenue](b40n12-daf-share-of-recipient-revenue.md) | - `top50_daf_share_of_contrib` here reproduces that file's `share_sched_i` for the 7 overlapping EINs (e.g. NVF 0.3453, Blue Meridian 0.7719, Hopewell 0.4234).<br>- It uses the same numerator, denominator and object IDs. | The comparison of outflows with inflows, and the channel. |
| [nonprofit donate-page scan](direction-nonprofit-donate-pages.md) | Source of the population. | - 3 of the 28 rows are scan artefacts:<br>  - UCLA Foundation redirects to mygiving.ucla.edu;<br>  - Bright Funds redirects to hello.brightfunds.org;<br>  - Homewise has an unlinked `/donate/` page.<br>- See P-B39N603-05. |

## 3. Results

### 3.1 How they receive DAF grants

Channel classes, all 28 [C]:
- `no_giving_info_found` 22;
- `giving_page_no_daf` 1 (Homewise `/donate/`: "Donate to Homewise … Contact us to have a conversation", with no payment form);
- `giving_contact_only` 1 (Vital Strategies, partnerships@ e-mail);
- `redirects_offsite` 2 (UCLA Foundation, Bright Funds);
- `robots_unreadable` 2 (Worthington Scholarship Foundation; Charter School Growth Fund, whose robots.txt answered 200 in a first pass and 403 in the final pass).

No page matched any DAF, sponsor-link, wire/ACH, check or stock detector. No intermediary displays its EIN. The Primary School is the one organisation that shows its EIN on its homepage.

Core intermediaries, by hand reading [W] (pages read 2026-11-20):

| Organisation | What the public site offers a funder | Pages |
|---|---|---|
| New Venture Fund | No donate page (`/donate` etc. 404). The FAQ explains fiscal sponsorship. Contact gives info@ and a separate "New Project Inquiries" e-mail. | [FAQ](https://newventurefund.org/who-we-are/faq/), [contact](https://newventurefund.org/contact/) |
| Hopewell Fund | No donate page. "Projects raise their own funding, and we ensure those funds are managed responsibly". Contact: info@ for "exploring fiscal sponsorship". | [fiscal sponsorship](https://www.hopewellfund.org/fiscal-sponsorship), [contact](https://www.hopewellfund.org/contact) |
| Windward Fund | No donate page. Homepage: "connect donors … with projects". The contact form's reason list includes "Partner with Windward" (not submitted). | [home](https://www.windwardfund.org/), [contact](https://www.windwardfund.org/contact/) |
| Blue Meridian Partners | No donate page. Partner interest form (General / Impact Partner). FAQ: "General and Impact Partners make initial commitments of $50 million and $15 million … contributed over time". It has raised "over $4 billion". | [engage](https://bluemeridian.org/engage-with-us/), [FAQ](https://bluemeridian.org/frequently-asked-questions/) |
| ClimateWorks | No donate page. `/support` redirects off-site to a magazine article. "working with over 80 funders". | [about](https://www.climateworks.org/about-us/) |
| US Energy Foundation | No donate page. FAQ: "We partner with individuals and organizations in the U.S. to align on strategy and raise vital resources". Contact: web form and media e-mail. | [FAQ](https://www.ef.org/about-us/faq/) |
| Energy Foundation China | No donate page. A "Key Funders" page lists foundations, including ClimateWorks and Hewlett. | [funders](https://www.efchina.org/About-Us-en/Funders-en) |
| Climate Imperative | Minimal site (about 700 characters of text); contact page only. | [home](https://climateimperative.org/) |
| Charter School Growth Fund | robots.txt unreadable in the final pass; nothing cited. | — |
| Stand Together Trust | About and contact pages; no giving content found. Several article URLs returned 403. | [about](https://standtogethertrust.org/about-us/) |

**Reading [I].**
- The DAF money reaches these organisations through the sponsor's own grant flow: the donor recommends, the sponsor's due diligence clears the EIN, and the sponsor pays.
- The recipient's public pages give the donor nothing to use: no DAF form, no wire details, not even the EIN.
- The giving relationship is negotiated off-page, through partner commitments, a project's own fundraising or info@ e-mails. Concentration fits this. Blue Meridian's top-50 dollars come from 3 sponsors, and GS DAPF alone is 54.5%. Energy Foundation China takes 99.1% from Fidelity Charitable. These are a few large donor recommendations, not retail giving.
- **Not observable:** grant agreements and wire instructions, if they exist, are not public. The sponsors' charity-search tools are forms and were not used. P-B39N603-06 proposes reading the sponsors' public help-centre rules instead.

### 3.2 Share of top-50 DAF dollars [C]

Denominators: $78.29bn filed; $74.28bn DAF-weighted. Shares are DAF-weighted unless stated.

| Group | n | Top-50 $ (filed) | Share filed | Top-50 $ (DAF-weighted) | Share DAF-weighted |
|---|---|---|---|---|---|
| Population (scan rows) | 28 | $3,238.0m | 4.14% | $3,189.1m | 4.29% |
| Rule pass-through set | 18 | $2,248.4m | 2.87% | $2,205.3m | 2.97% |
| **Core intermediaries (hand)** | **10** | **$1,766.3m** | **2.26%** | **$1,734.0m** | **2.33%** |
| … fiscal sponsors | 3 | $662.2m | 0.85% | $648.5m | 0.87% |
| … pooled funds | 5 | $830.0m | 1.06% | $826.8m | 1.11% |
| … grantmaking public charities | 2 | $274.1m | 0.35% | $258.7m | 0.35% |
| **Named in the queue item** | **7** | **$1,415.4m** | **1.81%** | **$1,399.0m** | **1.88%** |

Individually, core 10 and the other large rows:

| Scan rank | Organisation | Subtype [I] | Top-50 $ filed | DAF-wtd share | Sponsors | Largest sponsor (share of its top-50 $) |
|---|---|---|---|---|---|---|
| 4 | Church of Jesus Christ of LDS | church_no_990 | $465.6m | 0.62% | 20 | Fidelity Charitable (58%) |
| 6 | New Venture Fund | fiscal_sponsor | $432.0m | 0.57% | 26 | Fidelity Charitable (47%) |
| 7 | Blue Meridian Partners | pooled_fund | $363.0m | 0.49% | 3 | GS DAPF (55%) |
| 11 | Climate Imperative Foundation | grantmaking_public_charity | $247.1m | 0.31% | 4 | NPT (42%) |
| 17 | US Energy Foundation | pooled_fund | $190.4m | 0.25% | 8 | Fidelity Charitable (46%) |
| 21 | ClimateWorks Foundation | pooled_fund | $169.5m | 0.23% | 9 | Fidelity Charitable (59%) |
| 26 | Hopewell Fund | fiscal_sponsor | $149.7m | 0.19% | 29 | Fidelity Charitable (67%) |
| 72 | Windward Fund | fiscal_sponsor | $80.5m | 0.11% | 16 | GS DAPF (47%) |
| 75 | Charter School Growth Fund | pooled_fund | $76.8m | 0.10% | 6 | NPT (33%) |
| 226 | Energy Foundation China | pooled_fund | $30.3m | 0.04% | 3 | Fidelity Charitable (99%) |
| 267 | Stand Together Trust | grantmaking_public_charity | $27.0m | 0.04% | 13 | NCF (48%) |

The other 17 rows are in the CSV.

### 3.3 Does the money pass onward? [C]

Own 990s, tax years 2023 + 2024 pooled:

| Group / organisation | Contributions (1h) | Grants out (IX 1–3) | Onward ratio | Net of intra-set | Grants / expenses | Net-asset change | Top-50 DAF $ / contributions |
|---|---|---|---|---|---|---|---|
| Core 10 | $4,907.0m | $4,244.2m | **0.86** | 0.83 | 0.73 | −$672.5m | 0.36 |
| Named 7 | $3,887.3m | $3,220.8m | **0.83** | 0.81 | 0.71 | −$474.0m | 0.36 |
| Fiscal sponsors (3) | $2,101.2m | $1,582.9m | 0.75 | 0.74 | 0.65 | −$300.0m | 0.32 |
| Pooled funds (5) | $2,123.4m | $1,896.4m | 0.89 | 0.87 | 0.78 | −$127.1m | 0.39 |
| Operating (8, for contrast) | $847.3m | $131.4m | 0.16 | 0.16 | 0.18 | +$193.3m | 0.39 |
| New Venture Fund | $1,251.0m | $1,052.9m | 0.84 | 0.84 | 0.65 | −$360.7m | 0.35 |
| Blue Meridian | $470.2m | $792.5m | 1.69 | 1.67 | 0.89 | −$344.1m | 0.77 |
| Climate Imperative | $472.1m | $490.0m | 1.04 | 0.83 | 0.78 | −$148.5m | 0.52 |
| US Energy Foundation | $534.8m | $322.5m | 0.60 | 0.60 | 0.70 | +$91.8m | 0.36 |
| ClimateWorks | $590.9m | $408.6m | 0.69 | 0.62 | 0.70 | +$39.1m | 0.29 |
| Hopewell | $353.5m | $201.2m | 0.57 | 0.51 | 0.57 | +$12.8m | 0.42 |
| Windward | $496.7m | $328.8m | 0.66 | 0.65 | 0.71 | +$47.9m | 0.16 |
| Energy Foundation China | $190.2m | $114.4m | 0.60 | 0.60 | 0.71 | +$39.2m | 0.16 |
| Charter School Growth Fund | $337.3m | $258.5m | 0.77 | 0.76 | 0.77 | +$46.9m | 0.23 |
| Stand Together Trust | $210.3m | $274.9m | 1.31 | 1.31 | 0.87 | −$96.9m | 0.13 |

**Reading [I].**
- The core intermediaries are pass-throughs on their own numbers: 86 cents of grants out per dollar contributed in the same two years, and net assets down $672.5m.
- Pooled funds and grantmaking charities regrant close to all of it. Blue Meridian and Stand Together Trust grant more than they raise, drawing on net assets.
- For the fiscal sponsors the onward ratio understates the pass-through. NVF, Hopewell and Windward fund their projects' own staff and programmes inside the same EIN, which shows as functional expenses, not grants. NVF's expenses were $1.62bn against $1.25bn contributed.
- **Second hop.** $183.1m of the population's Schedule I grants go to other population EINs. $182.9m of that comes from the core 10, and Climate Imperative alone accounts for $97.7m.
- **Foreign second hop.** $529.5m (16.4%) of the named seven's grants are foreign (Part IX line 3).
- Both observations argue for a look-through view of DAF dollars (P-B39N603-01).

## 4. Limits

- **Population is scan-defined.** It holds 28 rows, not all fiscal sponsors. Tides, RPA, NEO and others have donate links or other scan statuses and are not here. The core-10 share is a lower bound for "intermediaries" among top-50 recipients.
- **Hand subtypes and channel notes are judgement** [I]. Each carries its basis in the CSV.
- **Timing.** Sponsor fiscal years and recipient tax years differ, so ratios are pooled over two years.
- **Six EINs are timing-flagged**, with DAF $ greater than contributions: Breakthrough Energy Catalyst, Connecticut Project, Homewise, Primary School, Worthington, XQ. Their ratios are not interpreted (P-B39N603-04).
- **Onward ratios are not DAF-specific.** The 990 does not separate DAF-sourced contributions. The ratio says the organisation as a whole passes money on.
- **Raw HTML only.** JS-injected widgets would be missed. The original scan rendered with headless Chrome and also found no donate link for these homepages.
- **Pages not read:**
  - off-host redirects were not followed into content (UCLA, Bright Funds, the LDS donations sign-in);
  - several hosts answered some paths with 403 or 503 (Charter School Growth Fund, Bright Funds `/faq`, Stand Together Trust articles, churchofjesuschrist.org fixed paths);
  - these were not retried, and the UA was not changed.
- **Not observable from public pages:** grant agreements, wire instructions, minimum grant sizes (except Blue Meridian's partner tiers), and sponsor-side due-diligence notes.
- **Unread data:**
  - Stand Together Trust files its Schedule I as one "SEE ATTACHED" line ($272.2m), so its recipients and intra-set flows are unknown;
  - Bright Funds files Part IX grants with no Schedule I Part II lines.
- **2021+ only:** all filings are tax years 2023–2024; all pages were read 2026-11-20.

## 5. Reproduction

```
S=<scratchpad>
python3 scripts/mission_pass_through_recipients.py fetch  . --index-dir $S/irs --work W
python3 scripts/mission_pass_through_recipients.py report . --np-cache $S/npcache --lines-cache $S/rcp/lines --work W
```

- **`fetch`** caches the XML to `W/xml/` and writes `W/filings.json` and `W/web.json` (it takes about 2.5 min, most of it for the polite web pass). `--no-web` skips the pages.
- **`report`** is pure. It writes the CSV and prints the JSON summary, which holds every figure in §0–§3: totals, the `population`, `pass_through`, `named`, `hand_core` and `by_hand_subtype` aggregates, and `robots_log`.

## 6. Source register

### 6.1 Sources

| ID | Source | Version / access |
|---|---|---|
| S1 | IRS Form 990 Schedule I Part II, top-50 sponsors FY2023–24: e-file XML, GivingTuesday mirror of IRS TEOS ([IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)) | Line cache of `mission_recipient_sectors.py` (unchanged); 94/94 sponsor-years |
| S2 | Recipient Form 990 / 990-EZ / 990-PF, tax years 2023–24: `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`; object IDs in the CSV column `f990_object_ids` | Fetched 2026-11-20; robots.txt 404 |
| S3 | [IRS TEOS e-file index](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv) (index_2023..2026) | Local cache of earlier tasks |
| S4 | `daf-to-daf-recipient-whitelist.csv`, `sponsor-cost-structure.csv`, `dafrc-sponsor-schedule-d-fy2019-2024.csv` | Repo files |
| S5 | `nonprofit-donate-page-daf-scan-2026.csv` | Repo file (population) |
| S6 | Public web pages of the 28 organisations (URLs in §3.1 and in the CSV columns `website`, `web_evidence_url`) | Read 2026-11-20, UA `research-script/1.0` |

### 6.2 robots.txt log (2026-11-20, final pass)

| Host | Code | Result |
|---|---|---|
| www.churchofjesuschrist.org | 200 | parsed |
| www.newventurefund.org / newventurefund.org | 200 / 200 | parsed |
| www.bluemeridian.org / bluemeridian.org | 200 / 200 | parsed |
| www.climateimperative.org / climateimperative.org | 200 / 200 | parsed |
| www.ef.org | 200 | parsed |
| www.climateworks.org | 200 | parsed |
| www.hopewellfund.org | 200 | parsed |
| xqsuperschool.org | 200 | parsed |
| ouramericanfuturefoundation.org | 200 | parsed |
| www.vitalstrategies.org | 200 | parsed |
| www.uclafoundation.org | 200 | parsed |
| gsd.ngo / www.gsd.ngo | 200 / 200 | parsed |
| www.windwardfund.org | 200 | parsed |
| chartergrowthfund.org | 403 | unreadable; nothing fetched (200 in a first pass) |
| www.brightfunds.org | 200 | parsed |
| www.breakthroughenergy.org | 200 | parsed |
| worthingtonscholars.org | 403 | unreadable; nothing fetched |
| murmuration.org | 200 | parsed |
| arcinstitute.org | 200 | parsed |
| www.hope-ec.org / hope-ec.org | 200 / 200 | parsed |
| convergentresearch.org / www.convergentresearch.org | 200 / 200 | parsed |
| www.theprimaryschool.org | 200 | parsed |
| www.efchina.org | 200 | parsed |
| www.ctproject.org / ctproject.org | 200 / 200 | parsed |
| www.aiefdn.org | 200 | parsed |
| loftleaders.org / www.loftleaders.org | 200 / 200 | parsed |
| standtogethertrust.org | 200 | parsed |
| www.homewise.org / homewise.org | 200 / 200 | parsed |
| gt990datalake-rawdata.s3.amazonaws.com | 404 | no rules |

No robots rule disallowed any requested URL (`web_pages_robots_disallowed` = 0 for every row). sec.gov was not used.

## 7. Data dictionary: `pass-through-recipients-2026-11-20.csv` (28 rows)

All $ are USD. "Top-50" means the FY2023–24 Schedule I lines of the 94 itemising top-50 sponsor-years, net of DAF-to-DAF.

| Column | Meaning |
|---|---|
| daf_rank, ein, name, ntee_cd, website | From the donate-page scan (rank among its 300) |
| named_in_queue_item | 1 for the 7 EINs named in P-B39N6-03 (both Energy Foundation EINs) |
| pass_through_class | Rule class (§1.4): fiscal_sponsor / regranting_intermediary / operating / no_990 [C] |
| hand_subtype, hand_subtype_basis | Hand subtype and its evidence [I] |
| top50_usd_ex_uh_filed | Top-50 $ from non-university/hospital grantors (the scan frame) |
| scan_daf_grant_usd | The scan's value, for the reproduction check |
| top50_usd_all_filed, top50_usd_all_daf_weighted | Top-50 $ from all 94 sponsor-years: filed, and DAF-weighted |
| top50_usd_fy2023, top50_usd_fy2024 | Filed top-50 $ by sponsor fiscal year |
| share_all_filed, share_all_daf_weighted | Shares of $78,287,627,404 and $74,281,457,270 |
| top50_lines, top50_grantors | Lines and distinct sponsors |
| top_grantors, top_grantor_share | Three largest sponsors with $, and the largest sponsor's share |
| f990_tax_periods, f990_object_ids, f990_years | Recipient returns used |
| contrib_1h_usd, gov_grants_1e_usd, total_revenue_usd, total_expenses_usd | Summed over the returns (990-PF and 990-EZ equivalents in §1.3) [F summed] |
| grants_out_ix1_3_usd, grants_foreign_ix3_usd | Part IX lines 1–3, and line 3 alone |
| sched_i_lines, sched_i_usd | Recipient's own Schedule I Part II (990-PF: grants-paid table) |
| onward_ratio_grants_to_contrib | grants_out ÷ contributions |
| onward_ratio_net_of_population | (grants_out − sched_i_to_population_usd) ÷ contributions |
| grants_share_of_expenses | grants_out ÷ total_expenses |
| top50_daf_share_of_contrib | top50_usd_all_filed ÷ contributions |
| timing_flag | 1 if top-50 $ exceed contributions (ratios not interpreted) |
| net_assets_boy_first, net_assets_eoy_last, net_assets_change | Net assets at the start of the first return, at the end of the last, and the change |
| sched_i_to_population_usd, sched_i_to_population_detail | Recipient's Schedule I $ to other population EINs (EIN:$) |
| top_sched_i_recipients | Three largest own-Schedule I recipients (EIN or name, $m) |
| daf_ind_part_iv_6 | Part IV line 6 per return (1/0; blank for 990-PF) |
| fiscal_sponsor_text_hits, fiscal_sponsor_text_example | Self-descriptive fiscal-sponsorship text nodes outside grant tables |
| robots_state, robots_code | robots.txt result for the site's host |
| channel_class | §1.5 class |
| web_daf_text … web_tax_id_label | 1 if any page read matched the detector: daf_text, daf_widget, sponsor_link, wire_ach, check_mail, stock, grant_agreement, fiscal_sponsor, pooled_fund_terms, own_ein_shown, tax_id_label |
| web_home_fiscal_sponsor, web_home_fs_snippet | Homepage fiscal-sponsorship language, and a snippet |
| web_giving_emails | Giving/partner/development e-mail addresses found |
| web_evidence_url | Page behind the channel class (or the off-host redirect target) |
| web_daf_snippet | Context of the first DAF mention (none found) |
| web_pages_read, web_pages_robots_disallowed | Pages read with HTTP 200; candidate URLs disallowed by robots |
| channel_note_hand | Hand-read note on the receiving path [I/W] |
