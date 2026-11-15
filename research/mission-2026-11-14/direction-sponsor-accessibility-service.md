# Direction P-NEW-UXS-01: automated accessibility and published service levels, top-20 DAF sponsors

**Date:** 2026-11-15 · **Queue item:** P-NEW-UXS-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/sponsor-a11y-axe-2026.csv`](../../data/mission-2026-11-14/sponsor-a11y-axe-2026.csv): 60 rows, one per sponsor × page role (home / open_account / help), with axe-core violation counts by impact and the top rule IDs.
- [`data/mission-2026-11-14/sponsor-service-levels-2026.csv`](../../data/mission-2026-11-14/sponsor-service-levels-2026.csv): 20 rows, one per sponsor. Phone numbers and hours, response-time statements, live-chat signals, help-page counts, accessibility overlay and statement, WCAG claim.
- [`data/mission-2026-11-14/queue-proposals-batch40-n10.csv`](../../data/mission-2026-11-14/queue-proposals-batch40-n10.csv): P-B40N10-01..03.
- **Script:** [`scripts/mission_sponsor_a11y_service.py`](../../scripts/mission_sponsor_a11y_service.py). Functional-style Python. Pages are rendered by headless Chromium through Playwright for Python 1.63, using the preinstalled browser. Raw page JSON and homepage screenshots stay in the scratch cache, **not in the repo**.

**Rules applied**
- **Read first:**
  - [daf-user-complaints-deep-research.md](daf-user-complaints-deep-research.md), with its governing wave-4 and wave-14 corrections.
  - [queue-batch29-complaints-voids.md](queue-batch29-complaints-voids.md), with its governing wave-14 corrections.
  - Neither correction touches accessibility or service levels. The batch-29 rule still governs: complaint rates "must not be used to rank sponsors' service quality". This note follows the same spirit, and its counts are **not a service-quality ranking** (§4).
- **Universe:** the 20 largest DAFRC FY2024 sponsors by end-of-year DAF assets, with the R1 "filed replaces imputed" corrections from `dafrc-corrections-itemized.csv` applied. The script reuses `corrected_fy2024()` / `top_n()` from `mission_void_scan.py`. The 20 hold $250.6bn of corrected FY2024 DAF assets. They are the same 20 sponsors as `sponsor-terms-census-top20-2026.csv`.
- **Polite fetching:**
  - robots.txt was read for every host before any page on it, including cdnjs (404, so no rules).
  - Status 200 is parsed for `*`. 404/410 means no rules. Anything else (401/403/429/5xx, network error) means **robots unreadable, host not fetched**, the rule used in earlier batches.
  - Page loads were sequential and ≥2.5 s apart. The browser sent its normal headless-Chrome User-Agent, which was not changed or disguised.
  - **Nothing was clicked, typed or submitted.** No cookie banners were dismissed. There were no logins, chat sessions, phone calls or outreach.
  - Public pages only. Pages behind login links were excluded at selection, and a page that is a login screen (password field plus a login URL or title) would not have been scanned.
- **Page budget:** ≤5 distinct pages per sponsor: homepage, open-account page, help/FAQ page, contact page (if different), accessibility statement (if linked).
  - Total loads per sponsor (`page_loads_total`) are 0–6.
  - Fidelity (6 loads, 3 distinct pages) was also used for a pilot run. AEF (6 loads, 4 distinct pages) needed a second selection pass after a link-rule fix (§3.3). Both are slightly over "~5".
- **Labels:** **[O]** observed on the live page (2026-11-15); **[C]** script computation; **[I]** inference.

---

## 0. Answers in brief

> **Automated checks find only part of WCAG issues.** axe-core tests a subset of WCAG success criteria that can be machine-checked. Typical estimates are about a third to a half of issues. It cannot judge alt-text quality, keyboard-only use, logical focus order, meaningful link text in context, cognitive load, captions, or anything behind a login. **"0 violations" means "no automated failures on this page as first rendered", not "accessible".**

| Question | Answer |
|---|---|
| **Coverage** | **13 of 20 sponsors** readable, holding **$173.8bn (69.3%)** of top-20 assets [C]. **37 pages** scanned with axe [C].<br>Not readable:<br>- **robots.txt unreadable, not fetched:** DAFgiving360 (robots 403), Morgan Stanley GIFT (robots timeout), Raymond James Charitable (robots unreadable).<br>- **Homepage 403 to headless Chrome:** GS DAF and BofA CGF ("Access Denied"); Chicago Community Trust and JCF (Cloudflare "Just a moment…") [O]. |
| **Violations by impact** (WCAG 2.0/2.1/2.2 A+AA rules, axe 4.9.1) | **Critical:** 7 of 37 pages (31 elements), at 4 sponsors (NPT, Vanguard, SVCF, NCF).<br>**Serious:** 22 pages (155 elements).<br>**Moderate / minor:** 0, because the WCAG-tag run excludes axe's "best-practice" rules, where most moderate/minor rules live [C]. |
| **Clean pages** | **14 of 37 pages** had no automated WCAG failure [C].<br>All 3 pages: Renaissance, Greater Kansas City CF, Greater Horizons.<br>Some pages: Fidelity (home and open-account; FAQ had 1), ImpactAssets (home, FAQ), CJP (contact). |
| **Top rule IDs** (pages / sponsors / elements) | **color-contrast** 16 / 8 / 124 · **target-size** 6 / 2 / 6 · **link-name** 5 / 3 / 13 · **label** (critical) 4 / 2 / 13 · **aria-hidden-focus** 3 / 1 / 9 · **image-alt** (critical) 2 / 2 / 16 · **aria-allowed-attr** (critical) 2 / 1 / 2 · **link-in-text-block** 1 / 1 / 3 [C] |
| **Phone hours** | Stated on scanned pages by **3 of 13** [O]:<br>- Renaissance ("Office Hours Monday-Friday \| 8AM – 5PM Eastern")<br>- GKCCF and Greater Horizons (Donor Services "Monday-Friday, 8 a.m.-5:30 p.m. CT")<br>FFTC says only "during business hours". 12 of 13 show at least one phone number. Vanguard shows none, only a contact form. |
| **Response-time promises** | **None quantified** on any scanned page [O].<br>Unquantified only: Vanguard ("we'll be in touch soon"), Dechomai ("we will respond right away"), FFTC ("we'll have the right team member get in touch"; the regex missed this one and it was read in the cached text). |
| **Live chat** | **No chat widget script or global detected** on any public page scanned [C].<br>Only signal: Fidelity's "Virtual Assistant" link in the header and footer [O]. Chat may exist after login; that was not tested. |
| **Help-centre article counts** | No sponsor's scanned help page was a searchable help centre. FAQ question counts on the FAQ pages [C]:<br>- NPT: 56 question items (accordion headings)<br>- Dechomai: 18<br>- Vanguard: 10 visible question lines<br>- ImpactAssets: 9–10<br>- Fidelity: 7 lines on /faqs.html (Fidelity's separate "Help Center" was not loaded; see §3.3)<br>- 7 sponsors: the help role fell back to a contact page.<br>ImpactAssets runs a Freshdesk knowledge base (impactassets.freshdesk.com) [O]. Its article total was not counted. |
| **Accessibility statements** | **1 of 13 links one (AEF)**, and its body is **placeholder text** ("See our Accessibility Tips for what to do for this page on your website.") with **no WCAG claim** [O].<br>**0 of 13 claim a WCAG version or level** on scanned pages.<br>FFTC loads the **accessiBe overlay** (acsbapp.com) [O]. SVCF's footer "ACCESSIBILITY" is a javascript widget control, not a statement [O]. |

**Reading [I]:**
- The large nationals that could be read (Fidelity, NPT, Vanguard) are not clearly better than community foundations on automated checks. Fidelity is near-clean. NPT carries critical form-label and image-alt failures on all three pages; label is the same 4 unlabelled form fields site-wide. Vanguard repeats one aria-hidden-focus pattern site-wide.
- **Colour contrast is the dominant failure**, as on the web generally.
- **Published service levels are thin.** No top-20 sponsor readable here publishes a response-time promise or a public chat channel. Only 3 publish phone hours on the pages checked, and none publishes a WCAG conformance claim. This is consistent with the complaints corpus, which records "no communication" on held grants (fixable service/communication theme, ~20 records), but it does not measure actual responsiveness.

---

## 1. Method

1. **Seeds.** One public homepage per sponsor (table in the script, `SEEDS`).
   - Corporate-hosted programmes have no stand-alone DAF site. The seed is the programme page: GS `pwm.gs.com/.../philanthropic-strategy`, MS `morganstanley.com/what-we-do/wealth-management/gift`, BofA `bankofamerica.com/philanthropic/donoradvised.go`.
   - These programme URLs were found by web search on 2026-11-15.
2. **Page selection** from the homepage's links. The rules are fixed, ordered regexes (`OPEN_RULES`, `HELP_RULES`, `CONTACT_RULES`, `A11Y_RULES`), applied to link text/aria-label, then to the href.
   - Links must stay on the sponsor's domain, or a hosted help-centre tenant named after it (e.g. `impactassets.freshdesk.com`).
   - Login/sign-in hrefs, PDFs, `mailto:`, `tel:` and `javascript:` links are excluded.
   - Text such as "get help", "how we help", "for nonprofits" or "support us" is excluded from the help role.
   - FAQ links win over help-centre links. If neither exists, the contact page is the help page (flagged `fallback: contact`).
   - An accessibility link is looked for on every loaded page.
3. **Rendering.** `domcontentloaded`, then network-idle (≤12 s), then 2.5 s. Viewport 1366×900, CSP bypassed, so that axe could be injected.
4. **axe-core 4.9.1** from cdnjs, injected into the page. `runOnly` tags: `wcag2a wcag2aa wcag21a wcag21aa wcag22aa`.
   - Counted: violated **rules** and affected **elements (nodes)**, by impact.
   - Recorded: axe's "incomplete" (needs-review) rule count. These are not violations.
5. **Service-level extraction** from visible page text (pure regex functions in the script):
   - US phone numbers;
   - day-and-time hour ranges with an optional time zone;
   - "within N hours/days" statements, split by context into support-response and other (e.g. processing);
   - unquantified "we'll be in touch/respond" phrases;
   - chat vendor scripts and globals (Intercom, Zendesk, Drift, LivePerson, Salesforce Embedded Service, Genesys, Nuance, HubSpot and others) and chat text;
   - accessibility-overlay scripts (accessiBe, UserWay, AudioEye and others);
   - WCAG version and level text on the statement page.
   - Every non-empty field was checked against the cached page text. Reviewer notes are in the script's `REVIEW_NOTES` and the CSV `notes` column.

**Reproduce**

```
python3 scripts/mission_sponsor_a11y_service.py --cache-dir <scratch> --fetch              # first pass
python3 scripts/mission_sponsor_a11y_service.py --cache-dir <scratch> --fetch --reselect   # re-run selection, reusing loaded pages
python3 scripts/mission_sponsor_a11y_service.py --cache-dir <scratch>                      # rebuild CSVs from cache
```

## 2. Results by sponsor

| # | Sponsor | Assets $bn | Home C/S rules (elements) | Open-account C/S (elements) | Help C/S (elements) | Phone hours | Chat | A11y statement |
|---|---|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable | 66.2 | 0/0 (0) | 0/0 (0) | 0/1 (1) FAQ | not on pages | "Virtual Assistant" link | none linked |
| 2 | NPT | 42.1 | 2/2 (17) | 1/1 (5) | 1/1 (5) FAQ | not on pages | none | none linked |
| 3 | DAFgiving360 | 40.9 | — robots.txt 403 | — | — | n/a | n/a | n/a |
| 4 | Vanguard Charitable | 22.0 | 0/1 (3) | 0/1 (3) | 1/1 (4) FAQ | no phone shown | none | none linked |
| 5 | GS DAF | 12.6 | — 403 Access Denied | — | — | n/a | n/a | n/a |
| 6 | SVCF | 9.6 | 0/1 (6) | 1/0 (7) | 0/2 (7) contact | not on pages | none | widget control only |
| 7 | MS GIFT | 9.1 | — robots.txt timeout | — | — | n/a | n/a | n/a |
| 8 | AEF | 8.4 | 0/3 (22) | 0/3 (5) advisor "Start the DAF Process" | 0/3 (5) contact | not on pages | none | **linked; placeholder text** |
| 9 | Renaissance | 5.9 | 0/0 | 0/0 "Open Account/Log In" → program finder | 0/0 contact | **M–F 8–5 ET** | none | none linked |
| 10 | NCF | 5.7 | 1/1 (19) | 0/1 (7) | 1/1 (6) contact | not on pages | none | none linked |
| 11 | BofA CGF | 4.7 | — 403 Access Denied | — | — | n/a | n/a | n/a |
| 12 | Chicago Community Trust | 4.7 | — 403 bot challenge | — | — | n/a | n/a | n/a |
| 13 | ImpactAssets | 2.9 | 0/0 | 0/1 (21) Freshdesk "how do I open" article | 0/0 FAQ | not on pages | none | none linked |
| 14 | JCF | 2.9 | — 403 bot challenge | — | — | n/a | n/a | n/a |
| 15 | FFTC | 2.6 | 0/1 (4) | 0/1 (15) | 0/1 (3) contact | "business hours" only | none | **accessiBe overlay**, no statement |
| 16 | GKCCF | 2.6 | 0/0 | 0/0 | 0/0 contact | **M–F 8–5:30 CT** | none | none linked |
| 17 | Greater Horizons | 2.5 | 0/0 | 0/0 | 0/0 /support | **M–F 8–5:30 CT** | none | none linked |
| 18 | CJP | 1.9 | 0/1 (16) | no link found | 0/0 contact | not on pages | none | none linked |
| 19 | Raymond James Charitable | 1.9 | — robots.txt unreadable | — | — | n/a | n/a | n/a |
| 20 | Dechomai | 1.4 | 0/1 (1) | no link found | 0/2 (4) FAQ | not on pages | none | none linked |

C/S = critical/serious violated rules; elements = affected nodes, all impacts. Full rule lists are in the CSV `top_rule_ids`.

**Notes**
- **Shared site templates.** GKCCF and Greater Horizons share a template and results. NPT's critical `label` hits are the same unlabelled form fields on every page, and Vanguard's `aria-hidden-focus` is one component repeated.
- **Weak open-account pages.** Several "open account" pages are marketing or explainer pages, not application forms: ImpactAssets' is a help article, AEF's is an advisor gateway page and Renaissance's is a program finder. The account application itself sits behind a login or adviser for most sponsors.

## 3. Limitations

1. **Automated checks find only part of WCAG issues.**
   - Each page was scanned once, at desktop width, in its first rendered state, with cookie banners and accordions left as they were.
   - Cross-origin iframes (chat, video, embedded forms) are not tested.
   - Excluding best-practice rules is why moderate/minor counts are 0.
   - **Counts are not comparable across sites of different size and complexity, and must not be used as an accessibility ranking.**
2. **Coverage bias.**
   - The 7 unreadable sponsors are mostly adviser-channel or bank programmes (DAFgiving360, GS, MS, BofA, Raymond James), plus two large CF/federation sites behind Cloudflare.
   - The readable sample therefore over-represents community foundations and direct-to-donor nationals.
   - 403 responses to headless Chrome were recorded and not worked around. The User-Agent was never spoofed.
3. **Page-selection limits.**
   - FAQ links beat help-centre links, so Fidelity's richer `help-center.html` and ImpactAssets' Freshdesk knowledge base were not counted.
   - For 7 of 13 sponsors the help role is a contact page, because no FAQ/help link was on the homepage.
   - A first pass picked wrong "help" pages ("How you can help", "How we help", "Get Help"). These were fixed by tightening the rule and re-selecting with cache reuse, and the wrong pages were dropped.
4. **Service levels are "published on the scanned public pages", not "offered".**
   - Phone hours, chat or statements may exist on other pages, in PDFs, or after login.
   - Absence means "not found on ≤5 public pages".
   - Phone-number lists can include fax numbers (e.g. Renaissance's (877) 222-1829 is labelled Fax).
5. **Moving target.** Websites change. The figures are as of 2026-11-15.

## 4. How this fits the repo
- **Complaints research.** Supports the "fixable service/communication" theme in daf-user-complaints-deep-research.md §6. That theme concerns slow or absent responses on held grants. No sponsor here publishes a response-time standard that donors could hold it to [I].
- **Agentic-support risk.** Relevant to the AI-agent risk row in §7: the only conversational channel seen is Fidelity's Virtual Assistant [O].
- **No quality ranking.** Following batch 29 §2.5, these counts are **not** a sponsor service-quality or accessibility ranking.

## 5. Data dictionary

### `sponsor-a11y-axe-2026.csv` (one row per sponsor × page role)

| Column | Meaning |
|---|---|
| fy2024_rank, sponsor, ein, fy2024_daf_assets_corrected | Rank and corrected FY2024 DAF assets (DAFRC + R1 corrections) |
| page_role | home, open_account or help |
| selection_rule, link_text | Which ordered rule chose the link, and the link's text (`fallback: contact` = no FAQ/help link) |
| url_requested, url_final, http_status | Requested URL, URL after redirects, main-document HTTP status |
| robots | robots.txt outcome for the host |
| scan_status | ok, `skipped: robots`, `http 403`, `no matching public link found on homepage`, or error |
| page_title | Document title (first 120 characters) |
| axe_version, axe_rule_tags | axe-core version (4.9.1) and the WCAG tags run |
| rules_violated | Distinct axe rules violated |
| critical/serious/moderate/minor_rules | Violated rules by axe impact |
| nodes_total, critical/serious/moderate/minor_nodes | Affected elements, total and by impact |
| top_rule_ids | Up to 5 rules as `id(impact):elements`, most elements first |
| incomplete_rules | axe "needs review" rule count (not violations) |
| retrieved | 2026-11-15 |

### `sponsor-service-levels-2026.csv` (one row per sponsor)

| Column | Meaning |
|---|---|
| seed_url, pages_loaded, page_loads_total, page_urls | Seed, distinct pages loaded OK, total navigations incl. pilot/re-selection, role=URL list |
| phone_numbers_found | Distinct US numbers in page text (may include fax) |
| phone_hours_stated / _text / _source_role | Whether a day-plus-time range (or a 24/7 support phrase) was found, up to 2 snippets, and on which page |
| support_response_promise | `Y (time stated)`, `unquantified only`, `N (none found…)`, or `not assessed` |
| support_response_text / _unquantified | "within N …" statements in a contact or response context; soft phrases ("we'll be in touch soon") |
| other_within_statements | "within N …" statements in other contexts (e.g. processing) |
| live_chat_signal, live_chat_evidence | Chat vendor script or global and/or chat text on scanned pages, with evidence strings |
| help_page_url | Page used for the help role |
| help_article_links | Distinct links to /articles, /article or /kb on the help page |
| help_faq_question_items | Distinct headings/buttons/summary/dt ending in "?" (DOM) |
| help_question_lines | Distinct visible text lines ending in "?" |
| help_count_method | Description of the three counts |
| a11y_overlay_detected | Hosts of accessibility-overlay scripts or links (e.g. acsbapp.com) |
| a11y_statement_present / _url / _status | Accessibility link found and loaded (`Y`), absent on scanned pages, or not assessed |
| wcag_version_claimed, wcag_level_claimed, a11y_wcag_text | WCAG version/level text found on the statement page (blank = none) |
| notes | Reviewer notes and non-OK page statuses |
| retrieved | 2026-11-15 |
