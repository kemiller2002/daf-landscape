# Direction P-NEW-NPA-01: do the charities that receive the most DAF dollars offer DAF giving on their donate pages?

**Date:** 2026-11-15 · **Queue item:** P-NEW-NPA-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/nonprofit-donate-page-daf-scan-2026.csv`](../../data/mission-2026-11-14/nonprofit-donate-page-daf-scan-2026.csv): 300 rows, one per charity. Detection flags for the donate page and for either page (homepage or donate page), scan outcome, website source, sector and size. No personal data. Tracking and session parameters are stripped from URLs.
- [`data/mission-2026-11-14/queue-proposals-batch39-n6.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n6.csv): P-B39N6-01..03.
- **Script:** [`scripts/mission_donate_page_scan.py`](../../scripts/mission_donate_page_scan.py) (stdlib Python, functional style; pages rendered by headless Chrome through a small embedded Playwright/node helper). Stages: `rank`, `websites`, `scan`, `report`.

**Rules applied**
- **Read first:** [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md) (the recipient universe and DAF-to-DAF rules reused here) and [queue-all-in-cost-dafpay-access.md](queue-all-in-cost-dafpay-access.md) with its governing wave-10 and adviser-fee corrections. Neither correction touches donate pages. That note's DAFpay access findings (credential pass-through by default; tokenised access only for DAFgiving360 and Foundant community foundations) are context for §4 and are not re-tested here. [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md): no crt.sh use.
- **Polite fetching:**
  - robots.txt was read for every host before any page on it, including third-party donation hosts and redirect targets.
  - Status 200 → parsed for user-agent `*`. Status 404/410 → no rules. Anything else (401/403/429/400, timeout, network error) → **robots unreadable, host not fetched**, as in earlier batches.
  - **At most two pages per charity:** the homepage, then one donate/give page chosen from the homepage's links.
  - ≥1.1 s between page loads on the same host. Generic browser User-Agent.
  - Images, media and fonts were not loaded. **Nothing was clicked, typed or submitted.** No logins, no donations, no payment flows, no outreach.
- **Recency:** recipient dollars are FY2023–FY2024 Schedule I lines (tax years 2022–2024); pages were read 2026-11-15.
- **Labels:** **[F]** filed value; **[O]** observed on the live page; **[C]** script computation; **[S]** search-result statement; **[I]** inference.

---

## 0. Answers in brief

| Question | Answer [C/O] |
|---|---|
| **Sample** | **300 charities**, the largest recipients of non-DAF-to-DAF Schedule I dollars from the 90 non-university top-50 sponsor-years. Together they received **$24.08bn, 31.4%** of the $76.70bn net to EIN-identified recipients. Cutoff: $24.7m. |
| **Coverage** | **186 donate pages scanned** (181 separate pages, 5 on the homepage itself), holding $12.67bn (53%) of the sample's DAF dollars.<br>- 53 homepage-only: 28 had no donate/give link, 12 donate pages disallowed by robots.txt, 3 donate hosts with unreadable robots.txt, 10 donate pages unreachable.<br>- 21 homepages not fetched because robots.txt was unreadable (12 × 403, 6 network errors, 2 × 429, 1 × 400). **No homepage was disallowed by robots.txt.**<br>- 23 homepages unreachable (17 × 403, 4 × 405, 2 bot challenges).<br>- 17 had no findable website. |
| **DAFpay / Chariot** | **25 of 186 donate pages (13.4%)**. 20 (10.8%) load the Chariot script (`cdn.givechariot.com`); 5 more show an active DAFpay method, a `secure.dafpay.com` link or visible "DAFpay" text. Dollar-weighted: 10.9%. |
| **DAF Direct** | **3 (1.6%)**: Year Up, OpenSats, Accion Opportunity Fund. |
| **Sponsor-specific** | **8 (4.3%)** name Fidelity Charitable (8), DAFgiving360/Schwab Charitable (7), Vanguard Charitable (2) or NPT (1). Only 2 (1.1%) link to a sponsor site (GiveDirectly, OpenSats). |
| **"Donor-advised" text** | **65 (34.9%)**; 69 (37.1%) including the acronym "DAF". |
| **Own EIN shown** | **67 (36.0%)**. |
| **DAF-adjacent processors** | Every.org 3 (1.6%); Daffy 1; Endaoment 1; PayPal Giving Fund 0; Benevity 0. |
| **Any DAF option** | **75 of 186 (40.3%)** show DAFpay, DAF Direct, a sponsor name or DAF text. **44 (23.7%) mention DAFs without any in-checkout mechanism** (instructions only). |
| **By sector** | Highest: international (9 of 14 any; 5 DAFpay) and health (13 of 21; 7 DAFpay). Lowest: education (14 of 53, 26%; 3 DAFpay), religion (3 of 14; 0 DAFpay), arts (1 of 5). |
| **By size** | DAFpay: 11% at $10–100m revenue, 19% at $100m–1bn, 14% at ≥$1bn. Universities and hospitals that are themselves DAFRC sponsors: 0 of 14 DAFpay. |

**Reading [I]:**
- Even among the charities DAF donors fund most, in-checkout DAF giving is a minority feature. About one donate page in eight shows DAFpay, and DAF Direct and sponsor links are rare.
- The common pattern is text-only DAF instructions: "ask your sponsor to recommend a grant to EIN …".
- DAFpay concentrates in large health and international fundraising charities on Blackbaud Luminate, Fundraise Up and Engaging Networks forms (§3.3).
- Universities, religious organisations and the many intermediaries at the top of the DAF-dollar list rarely show it, or have no public donate page at all.

---

## 1. Method

### 1.1 Sample (stage `rank`) [F/C]
1. **Lines.** I reused the full Schedule I Part II lines that [`mission_recipient_sectors.py`](../../scripts/mission_recipient_sectors.py) cached for the 94 itemising top-50 sponsor-years (same `pick_returns`; all 94 load with matching line counts). I kept the 90 sponsor-years whose grantor is not a university/hospital, the `all_ex_university_hospital` scope.
2. **DAF-to-DAF removed** exactly as in that script: whitelist decision `include`, self-lines, and blank-EIN lines matching one whitelisted name.
3. **DAF sponsors excluded** as recipients:
   - every DAFRC panel EIN in the national, community-foundation, single-issue or processor segment. Above the cutoff: Rockefeller Philanthropy Advisors, Amalgamated Charitable Foundation, The Nature Conservancy, World Vision, Global Impact, Myriad USA, Williams College, JNF, Global Greengrants, JDC and Sierra Club Foundation;
   - BMF NTEE T31 community foundations outside the panel: Chicago Community Foundation and the National Christian Charitable Foundation EIN 81-1805367.
   - **Kept:** university/hospital panel EINs, which receive grants as ordinary charities (as in the sectors note). They are flagged `dafrc_university_hospital` (23 in the sample).
4. **Recipients without an EIN or not in the IRS EO BMF are excluded** (14 above the cutoff, e.g. the four CZ Biohub/Institute LLCs, UT Austin, Penn State and MD Anderson as government units, and LDS EIN 23-7300405). The LDS Church EIN 87-0234341 is in the BMF and in the sample.
5. **Ranking.** Recipients are ranked by pooled FY2023–24 dollars, and the top 300 are kept.
6. **Sector:** NTEE major group via `classify()` from the sectors script.
7. **Size:** BMF `REVENUE_AMT`; when blank, CY total revenue from the charity's own 990 header (8 cases; `size_source`). Bands: <$10m, $10–100m, $100m–1bn, ≥$1bn, unknown (36).

### 1.2 Website (stage `websites`) [F/S]
- **From the 990 (250 of 300).** The newest e-filed 990/990-EZ per EIN comes from the IRS TEOS index files 2019–2026. I read its `WebsiteAddressTxt` from the GivingTuesday mirror of IRS TEOS (first 256 KB by HTTP Range), falling back to older filings when the mirror lacked the object or the field was empty or "N/A".
- **From manual web search (33).** Used where no usable 990 URL existed, with each search note embedded in the script (`MANUAL_SITES`). Two are weaker: GSD (`gsd.ngo`, from a search summary) and Murmuration (`murmuration.org`, from a directory listing). Yad Eliezer USA's EIN link to yadeliezer.org is unconfirmed.
- **None found (17):** mostly private-style supporting trusts and family vehicles (James Family Charitable Trust, Deitch, Sandberg Goldberg Bernthal, Permanent Archive Fund) and small religious entities.

### 1.3 Scan (stage `scan`) [O]
1. robots.txt for the homepage host is checked first (rules above).
2. If allowed, the homepage is rendered in headless Chrome. Wait: DOM ready + network idle ≤10 s + 2.5 s.
3. If the page redirected to another host, that host's robots.txt is checked; if it disallows, the content is discarded.
4. **Choosing the donate link.** The best donate/give anchor is picked by score: "donate" text, path or `donate.` host 4; "give now / make a gift / ways to give" text 3; `/give`, `/giving`, `give.`/`giving.` host 2; "support" 1. Links to social media and to DAF sponsors are excluded.
5. **Query-string links.** A link that differs from the homepage only by query string (e.g. Fundraise Up `?form=donate`) is loaded as the donate page, because the query opens the form.
6. robots.txt for the donate host is checked, then the page is rendered once, with the same redirect check.

### 1.4 Detection (stage `report`) [C]
Searched in: raw HTML, rendered DOM, every child frame's DOM, all request URLs, and the visible text (scripts and styles removed).

| Flag | Rule |
|---|---|
| `dafpay_chariot` | Any of:<br>- `givechariot.com`, `chariot-connect` or `<chariot-` elements;<br>- a `dafpay.com` link;<br>- an active `"DAFPay"` payment method in page config;<br>- "DAFpay" in visible text.<br>`dafpay_widget` = Chariot script, element or request only. |
| `dafpay_generic_string_only` | Only platform-generic strings were found: Classy's `paymentMethods.dafpay.label` i18n bundle, Fundraise Up's `.ui-payment-button-dafpay` CSS, an Angular `#dafpay-button` style. These appear whether or not the charity enabled DAFpay, so they are **not counted** (5 pages). |
| `daf_direct`, `daf_direct_widget` | `dafdirect.org` or "DAF Direct"; the widget variant requires the DAF Direct script or link path |
| `fidelity_charitable`, `dafgiving360_schwab`, `vanguard_charitable`, `npt` (+ `_link`) | Name or domain anywhere; `_link` = the domain in an href/src or request |
| `text_donor_advised`, `text_daf_acronym`, `daf_text_any` | "donor-advised" (any dash or space) in visible text; case-sensitive "DAF"/"DAFs" |
| `ein_own_displayed`, `ein_label_present` | The charity's own EIN (`XX-XXXXXXX` or 9 digits) in visible text; an EIN/Tax ID label |
| `every_org`, `paypal_giving_fund`, `daffy`, `endaoment`, `benevity`, `daf_adjacent_processor_any` | Domain or name patterns |
| `any_daf_option` | DAFpay, DAF Direct, sponsor-specific, or DAF text |
| `platforms` | Donation platform fingerprints (Classy/GoFundMe Pro, Fundraise Up, Blackbaud, EveryAction, Donorbox, Engaging Networks, Stripe and others). Context only; never counted as a DAF option. |

**Spot checks [O].** Every DAFpay, DAF Direct, sponsor and Every.org hit was checked against its matched snippet:
- The 20 DAFpay widget hits load `cdn.givechariot.com/chariot-connect.umd.js` or per-charity Chariot "cargo" scripts. Examples: `cargo/luminate-online/mskcc-main-pci.js` and `cargo/every-action/crr-main.js`.
- Typical DAFpay visible text: "Click the DAFpay button below to initiate a gift from Fidelity Charitable, Schwab Charitable, and 1,100 other DAF providers" (Breakthrough T1D).
- Typical sponsor wording without a link: "Clients of BNY Mellon, Fidelity Charitable and Schwab Charitable can make a designation through the DAF Direct tool" (Year Up).

---

## 2. Coverage [C]

| Outcome (`scan_status`) | Charities | Note |
|---|---|---|
| `donate_scanned` | 181 | Separate donate page rendered |
| `donate_on_homepage` | 5 | Donate form on the homepage itself |
| `home_only_no_donate_link` | 28 | Mostly intermediaries and fiscal sponsors: New Venture Fund, Blue Meridian, Climate Imperative, US Energy Foundation, ClimateWorks, Hopewell, Windward, Energy Foundation, Stand Together Trust. Also XQ, the UCLA Foundation and the LDS Church homepage |
| `home_only_donate_robots_blocked` | 12 | Giving host disallows the gift path. 9 universities: UChicago, Oregon, Illinois, Tufts, Colorado, K-State, CMU, Utah, Hillsdale. Plus Lucile Packard, American Friends of Tel Aviv University and Groton Hill |
| `home_only_donate_robots_unreadable` | 3 | Johns Hopkins, Chicago CRED, Resolve to Save Lives |
| `home_only_donate_unreachable` | 10 | 403/405/challenge on the giving host. Examples: Cornell, USC, Northwestern, Partners In Health, Human Rights Watch |
| `robots_unreadable_home` | 21 | Examples: UCSF Foundation, UC Berkeley Foundation, Penn, Young Life, ACLU, Broad, Mayo Clinic (two EINs), NYU, AHA, Met Museum |
| `home_unreachable` | 23 | 403/405 or bot challenge to a headless browser. Examples: MSF USA, Princeton, Michigan, NRDC, Boys & Girls Clubs, Smithsonian, Met Opera |
| `no_website_found` | 17 | §1.2 |
| **Total** | **300** | **robots-blocked:** 0 homepages and 12 donate pages (11 by the linked host's robots.txt, 1 after a redirect)<br>**robots-unreadable:** 21 homepages and 3 donate hosts<br>**unreachable:** 23 homepages and 10 donate pages |

---

## 3. Results

### 3.1 Overall [C/O]
Rates are shares of the scanned pages (n).

| Measure | Donate page (n = 186) | Either page, same 186 | Either page, all with a page scanned (n = 239) | Donate page, DAF-dollar-weighted |
|---|---|---|---|---|
| DAFpay / Chariot (confirmed) | 25 (13.4%) | 25 (13.4%) | 25 (10.5%) | 10.9% |
| … Chariot script loaded | 20 (10.8%) | 21 (11.3%) | 21 (8.8%) | 9.5% |
| DAFpay platform strings only (not counted) | 5 (2.7%) | 6 | 7 | 2.0% |
| DAF Direct | 3 (1.6%) | 3 | 3 (1.3%) | 0.9% |
| Sponsor-specific mention | 8 (4.3%) | 8 | 8 (3.3%) | 2.9% |
| Sponsor-site link | 2 (1.1%) | 2 | 2 (0.8%) | 1.0% |
| "Donor-advised" text | 65 (34.9%) | 69 (37.1%) | 71 (29.7%) | 43.1% |
| "Donor-advised" or "DAF" text | 69 (37.1%) | 73 (39.2%) | 75 (31.4%) | 44.2% |
| Own EIN displayed | 67 (36.0%) | 72 (38.7%) | 78 (32.6%) | 40.8% |
| Every.org | 3 (1.6%) | 3 | 4 (1.7%) | 2.1% |
| PayPal Giving Fund | 0 | 0 | 0 | 0 |
| Any DAF-adjacent processor | 3 (1.6%) | 3 | 4 (1.7%) | 2.1% |
| **Any DAF option** | **75 (40.3%)** | 77 (41.4%) | 79 (33.1%) | 46.5% |

- Of the 25 DAFpay pages, 8 show no "donor-advised" text: the widget is the only DAF signal.
- Of the 75 pages with any DAF option, 44 rely on text alone (no DAFpay, DAF Direct or sponsor name).

### 3.2 By NTEE sector and by size (donate page) [C]

| Group | n | DAFpay | Chariot script | DAF Direct | Sponsor | "Donor-advised" | DAF text any | Own EIN | DAF-adjacent | Any DAF option |
|---|---|---|---|---|---|---|---|---|---|---|
| Education | 53 | 3 (6%) | 2 (4%) | 1 (2%) | 2 (4%) | 12 (23%) | 13 (24%) | 12 (23%) | 0 | 14 (26%) |
| Public-society benefit | 36 | 3 (8%) | 2 (6%) | 2 (6%) | 2 (6%) | 12 (33%) | 12 (33%) | 11 (31%) | 0 | 14 (39%) |
| Human services | 26 | 4 (15%) | 3 (12%) | 0 | 2 (8%) | 11 (42%) | 11 (42%) | 11 (42%) | 1 (4%) | 12 (46%) |
| Health | 21 | 7 (33%) | 6 (29%) | 0 | 1 (5%) | 12 (57%) | 12 (57%) | 7 (33%) | 0 | 13 (62%) |
| International | 14 | 5 (36%) | 5 (36%) | 0 | 1 (7%) | 7 (50%) | 8 (57%) | 6 (43%) | 2 (14%) | 9 (64%) |
| Religion | 14 | 0 | 0 | 0 | 0 | 3 (21%) | 3 (21%) | 5 (36%) | 0 | 3 (21%) |
| Environment/animals | 11 | 1 (9%) | 1 (9%) | 0 | 0 | 4 (36%) | 4 (36%) | 6 (55%) | 0 | 4 (36%) |
| Arts/culture | 5 | 0 | 0 | 0 | 0 | 1 (20%) | 1 (20%) | 4 (80%) | 0 | 1 (20%) |
| Unclassified / Z | 6 | 2 | 1 | 0 | 0 | 3 | 5 | 5 | 0 | 5 |
| **Size: <$10m** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **$10–100m** | 66 | 7 (11%) | 6 (9%) | 2 (3%) | 5 (8%) | 17 (26%) | 20 (30%) | 28 (42%) | 1 (2%) | 23 (35%) |
| **$100m–1bn** | 72 | 14 (19%) | 10 (14%) | 1 (1%) | 3 (4%) | 33 (46%) | 34 (47%) | 28 (39%) | 1 (1%) | 37 (51%) |
| **≥$1bn** | 28 | 4 (14%) | 4 (14%) | 0 | 0 | 10 (36%) | 10 (36%) | 6 (21%) | 1 (4%) | 10 (36%) |
| **Size unknown** | 19 | 0 | 0 | 0 | 0 | 5 (26%) | 5 (26%) | 5 (26%) | 0 | 5 (26%) |
| **DAF rank 1–100** | 55 | 8 (14%) | 8 (14%) | 0 | 2 (4%) | 22 (40%) | 22 (40%) | 16 (29%) | 2 (4%) | 25 (46%) |
| **DAF rank 101–200** | 62 | 6 (10%) | 4 (6%) | 1 (2%) | 1 (2%) | 21 (34%) | 22 (36%) | 22 (36%) | 0 | 22 (36%) |
| **DAF rank 201–300** | 69 | 11 (16%) | 8 (12%) | 2 (3%) | 5 (7%) | 22 (32%) | 25 (36%) | 29 (42%) | 1 (1%) | 28 (41%) |
| **DAFRC univ./hospital EINs** | 14 | 0 | 0 | 0 | 0 | 3 (21%) | 3 (21%) | 3 (21%) | 0 | 3 (21%) |

Cells with n < 15 are indicative only.

### 3.3 Platforms and DAFpay [O/C]
- **Donation platforms detected on the 186 donate pages:** Stripe 67, Classy/GoFundMe Pro 30, Fundraise Up 20, Blackbaud 17, EveryAction 9, Donorbox 7, Network for Good/Bonterra 3, Funraise 2, Engaging Networks 2, iDonate 1, Givebutter 1, GiveSmart 1. A page can show several.
- **Confirmed DAFpay by platform** (a page counts once per platform present; Classy examples: City Year shows "click DAF pay below", Robin Hood links `secure.dafpay.com`):
  - Blackbaud: 8 of 17, mainly Luminate Online "Donation2" forms with Chariot cargo scripts (MSK, Dana-Farber, Breakthrough T1D, CARE, Central Park Conservancy, Fred Hutch, Start Early);
  - Fundraise Up: 7 of 20 (IRC, UNICEF USA, Alzheimer's Association, Helen Keller Intl, HRF, Everytown, IPPF);
  - Classy/GoFundMe Pro: 4 of 30;
  - Engaging Networks 1, EveryAction 1, Funraise 1.
- **[I]** Chariot's reach among top DAF recipients runs largely through Luminate and Fundraise Up integrations. Classy pages carry DAFpay strings in the platform bundle, but few show it enabled in the static or rendered page (P-B39N6-01).
- **DAFpay pages (25, rank order):**
  - MSK, IRC, Jackson Hole Classical School, Dana-Farber, UNICEF USA, Helen Keller Intl, Edesia, Breakthrough T1D, Alzheimer's Association, Michael J. Fox Foundation;
  - Central Park Conservancy, Per Scholas, Fred Hutch, WWF, CARE, City Year, Human Rights Foundation, Villanova, Everytown Support Fund;
  - Brennan Center, Robin Hood, IPPF (via fosfeminista.org), Start Early, American Cancer Society, Center for Reproductive Rights.

### 3.4 Sponsor-specific and DAF Direct [O]
- **Sponsor names (8 pages):** GiveDirectly, Breakthrough T1D, Year Up, OpenSats, Evidence Action, Accion Opportunity Fund, Everytown, New Teacher Center.
- **Links to sponsor sites:** only GiveDirectly (a block linking Fidelity Charitable, DAFgiving360, Vanguard Charitable and NPT) and OpenSats.
- **Text without a link:** the rest name sponsors in text, as DAFpay copy ("give from Fidelity Charitable, DAFGiving360, or 1,000+ other DAF providers") or as DAF Direct copy.
- **DAF Direct (3):**
  - Year Up describes "a designation through the DAF Direct tool" for clients of BNY Mellon, Fidelity Charitable and Schwab Charitable;
  - OpenSats links a `dafdirect.org/DAFDirect/daflink` URL;
  - Accion OF embeds a DAF Direct sponsor selector (Fidelity Charitable / DAFgiving360 / BNY Mellon).
  - New Teacher Center uses the same sponsor list ("If you have an account with Fidelity Charitable, Schwab Charitable, or BNY Mellon, you can make a designation and gift here") behind a shortened link, without naming DAF Direct. It is counted as sponsor-specific, not as DAF Direct [O; the BNY Mellon/Fidelity/Schwab trio matches DAF Direct's participating sponsors, I].

---

## 4. Implications [I]
- **Checkout reach.** For a DAF entrant, the charity-side checkout is not yet a solved channel even among the most DAF-funded charities: ≈13% DAFpay and ≈2% DAF Direct on donate pages. The dominant pattern is still "give through your sponsor's site with our EIN".
- **Recognition is the visible need.** Recognition data (EIN, legal name) is shown on about 36% of donate pages.
- **Where checkout matters little.** A large share of top DAF dollars goes to intermediaries with no donate page (28 of 300, several in the top 30) or to universities whose giving forms are robots-restricted or bot-protected. For those, sponsor-initiated grants, not charity checkouts, carry the money (P-B39N6-03).
- **Concentration.** DAFpay adoption is concentrated in large health and international fundraisers on enterprise forms. That fits the queue-all-in-cost note's finding that DAFpay's default access passes donor credentials through. The two observations together say nothing about which sponsors' donors can complete a DAFpay gift (not tested; no flows were opened).

## 5. Limitations
- **Static view only.**
  - Options shown only after interaction (choosing "Donor-advised fund" inside a multi-step form, opening a modal) are missed unless the platform loads them on page load. Rates are therefore lower bounds for the mechanisms.
  - Platform-generic strings were deliberately excluded.
- **One donate page.** University "give" landing pages often link onward to the actual gift form, which was not fetched, so education is likely under-measured.
- **Coverage bias.** 114 of 300 charities have no scanned donate page, and they are disproportionately universities, hospitals and bot-protected large brands. Bot protection here means a 403 to a headless browser, which the scan did not try to circumvent.
- **Robots policy.** An unreadable robots.txt (403/429/5xx/network error) was treated as "do not fetch", consistent with earlier batches. That choice is conservative and costs 24 hosts.
- **Websites.** 33 come from manual search, two of them weak (§1.2). 990 website fields can be stale. Redirects were followed and re-checked against robots.
- **Text rules are blunt.** "DAF" can appear in unrelated contexts. "Donor-advised" can appear in FAQs or footers rather than the gift form; the flag records presence on the page, not a working option.
- **Sample definition.** The sample follows filed Schedule I dollars (>$5,000 lines, domestic recipients) from the top-50 sponsors only. Government units and LLCs not in the BMF are excluded.
- **One-day snapshot** (2026-11-15). Year-end campaigns can change forms.

## 6. Data dictionary: `nonprofit-donate-page-daf-scan-2026.csv`

| Column | Meaning |
|---|---|
| daf_rank | Rank by FY2023–24 non-DAF-to-DAF Schedule I dollars from the 90 non-university top-50 sponsor-years (1 = largest) |
| ein, name, schedule_i_name, state | Recipient EIN, BMF name, most common Schedule I name, BMF state |
| ntee_cd, ntee_major_group, sector_method | BMF NTEE code, major group and method (`ntee`, `bmf_foundation_*`, `name_rule:*`) per `mission_recipient_sectors.classify` |
| dafrc_university_hospital | 1 = EIN is a DAFRC university/hospital panel member (holds DAFs; kept as a charity) |
| daf_grant_usd_fy2023_2024, grantor_sponsors | Dollars received and number of distinct top-50 grantor sponsors |
| size_band, size_source, revenue_usd | Revenue band: `a_lt_10m`, `b_10m_100m`, `c_100m_1bn`, `d_ge_1bn` or `unknown`; source (`bmf_revenue_amt` or `990_total_revenue`); revenue used |
| website, website_source | Homepage scanned; `990 WebsiteAddressTxt (…object id)`, `manual web search: …` or `none` |
| home_robots, home_robots_code | `allowed` / `disallowed` / `unreadable` and the robots.txt HTTP code or error |
| home_state | Homepage render outcome (`ok`, `http_403`, `bot_challenge`, `robots_*_after_redirect`, …) |
| donate_url, donate_anchor | Chosen donate/give link (tracking parameters removed) and its anchor text |
| donate_state | `to_fetch`, `donate_on_homepage`, `no_donate_link_found`, `robots_disallowed`, `robots_unreadable` |
| donate_robots, donate_page_state | robots verdict for the donate host; donate page render outcome |
| page_scanned | `donate`, `homepage` (homepage only) or `none` |
| scan_status | Summary outcome (§2) |
| donate_* | Detection flags on the donate page (1/0; blank when no donate page was scanned): see §1.4. Each of the 28 flags in `FLAG_COLS` (adds `dafpay_text`: "DAFpay" in visible text) |
| donate_platforms | Platform fingerprints on the donate page (`;`-separated) |
| either_* , either_platforms | Same flags, 1 if found on the homepage or the donate page (blank if no page scanned) |
| accessed | 2026-11-15 when a page was scanned |
| source | Provenance |

**Reproduction**
```
python3 scripts/mission_donate_page_scan.py rank --np-cache NPCACHE --bmf-dir BMF --lines-cache LINES --work W
python3 scripts/mission_donate_page_scan.py websites --index-dir IRS_INDEX --work W
python3 scripts/mission_donate_page_scan.py scan --work W        # node + Playwright + Chrome; robots-first
python3 scripts/mission_donate_page_scan.py report --work W      # writes the CSV and W/summary.json
```
- `LINES` is the `mission_recipient_sectors.py` lines cache.
- `IRS_INDEX` holds the IRS TEOS `index_YYYY.csv` files.
- Every number in §0–3 comes from `W/summary.json` or the CSV.

## Validation corrections (wave 24B, 2026-11-15) — governing
Source: [validation-wave24b-report.md](validation-wave24b-report.md); register `data/mission-2026-11-14/validation-register-wave24b.csv`.

1. **§5 Limitations, new bullet after the snapshot bullet.**
   - **Find:** "- **One-day snapshot** (2026-11-15). Year-end campaigns can change forms."
   - **Replace with:** "- **One-day snapshot** (2026-11-15). Year-end campaigns can change forms.\n- **Link choice.** At least four scanned \"donate pages\" are not donate pages: rank 77 (a UA Foundation news item), 84 (a Rockefeller Foundation news item), 165 (a USCCB news article) and 244 (Boston Children's \"donate-blood\" page). None shows a DAF option. Without them, any DAF option is 75/182 (41.2%) and DAFpay 25/182 (13.7%). Two `donate_url` values still carry tracking parameters (e.g. `_ga`) [V wave 24B].\n- **Wave 24B re-read.** A stratified sample of 30 charities was re-read (10 of 25 DAFpay positives, 20 others; 29 fetched).\n  - The \"donor-advised\" and own-EIN flags matched on 29 of 29 pages, and \"any DAF option\" on 28 of 29.\n  - 7 of 10 DAFpay positives reproduced from the page and rendered DOM. The other 3 (IPPF, Per Scholas, Edesia) carry the form in an iframe, which only a frame-level read sees.\n  - No negative showed DAFpay [V wave 24B]."
