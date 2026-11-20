# Foundant Giving Hub docs (blocked) and NCF donate button (P-B4222-02-01-01, P-B4222-02-02)

- **Task ID:** b4222-02-01-01. **Date:** 2026-11-20.
- **Data:** `data/mission-2026-11-14/foundant-docs-ncf-donate-2026-11-20.csv` (22 rows: 7 robots, 9 document-level, 6 aggregate).
- **Queue proposals:** `data/mission-2026-11-14/queue-proposals-b4222-02-01-01.csv` (5 rows).
- **Script:** none. All fetches were manual one-off `curl` reads of named URLs under the generic user agent `research-script/1.0`. Counts come from shell counts of the downloaded sitemaps (method in §2.3).
- **Evidence labels:** F = fetched from the primary source on 2026-11-20; C = computed from fetched files; R = carried from a repo file; B = blocked or not determined.

## Summary

1. **Task 1 (Foundant documentation) is blocked.** `foundant.com`, `www.foundant.com` and the help-centre host `help.foundant.com` each serve a robots.txt with `User-agent: ClaudeBot` / `Disallow: /` and `User-agent: anthropic-ai` / `Disallow: /`, plus `Claude-Web`. The brief says to stop in that case, so no Foundant page was fetched. The setting, its DAF default and any third-party guidance are **not determined** (CSV R01–R03, A06).
2. **NCF documents a donate button for Giving Funds (DAFs).** The guide reads: "Yes. You can invite others to give to your Giving Fund. Including a donate button can make it easy for others to give directly to your fund online." The fundholder sets it up under Settings after logging in. The guide does not state a default (D01–D03).
3. **The governing "Donate button" section of NCF's Program Agreement was not read.** The guide defers to it ("subject to the requirements for eligible donations outlined in our Program Agreement … under 'Donate button.'"). The agreement is at `secure.ncfgiving.com/agreement`, and that host's robots.txt disallows `/` for all agents (D04, D09, R07).
4. **Donate pages cannot be counted.** NCF's published sitemaps list 659 URLs, all on `www.ncfgiving.com`, and none is a fund donate page (A01–A02). No published link list exposes donate pages either. NCF's public-site terms also bar automated extraction, so no crawl was attempted (A03, D07).
5. **Third-party giving cannot be sized from public data.** NCF's FY2024 Schedule D reports $2,907,564,434 of contributions into 31,943 DAFs. That total covers all givers and has no fundholder/third-party split, so it is only an upper bound (A04–A05).

## 1. Method

1. **Robots first.** Before any page fetch, I read robots.txt for `foundant.com`, `www.foundant.com`, `help.foundant.com`, `support.foundant.com`, `www.ncfgiving.com` and (once the guide linked to it) `secure.ncfgiving.com`. A host counted as off-limits for a path if a group naming `ClaudeBot`, `anthropic-ai`, `Claude-User` or `Claude-SearchBot` had a `Disallow` covering it, or if the `*` group did. `*.fcsuite.com` was not touched (brief; earlier study).
2. **Task 1.** I stopped once the robots check failed on foundant.com and help.foundant.com, as the brief requires. `support.foundant.com` (Zendesk) names no Anthropic token, but I did not use it: reading another Foundant host after the stop condition would be a workaround.
3. **Task 2, documents.** I read the guide at the brief's start URL and the PF-29 row. Then I read the sitemap index, its 8 child sitemaps and 11 more named `www.ncfgiving.com` pages for donate-button text and agreement links: giving-fund, terms-and-disclosures, support, charities, our-financials, forms, one story, and four document pages. Quotes were taken from the HTML text with tags stripped.
4. **Task 2, counting.** I would only look for donate pages through links or NCF's sitemap. No URL was guessed or enumerated.
5. **Stop on terms.** The terms-and-disclosures page (read as one of the 11) bars "automated means, including bots, crawlers, or spiders" without permission. After reading it I fetched no further NCF page and did not crawl the 453 story URLs.
6. **Sizing.** I used the repo's IRS 990 Schedule D harvest. No new 990 fetch.
7. **Privacy.** No donor, fundholder or fund name is recorded. Rows are document-level or aggregate.

## 2. Results

### 2.1 Robots log

| Host | Result | Used? |
|---|---|---|
| www.foundant.com | `ClaudeBot`, `anthropic-ai`, `Claude-Web`: `Disallow: /`. `*`: `Allow: /` with `Content-Signal: search=yes,ai-train=no,use=reference`. `Claude-User` and `Claude-SearchBot` not named | No: stop condition met |
| foundant.com | Same block | No |
| help.foundant.com | Same block (help-centre host) | No |
| support.foundant.com | No Anthropic token. `*` disallows `/search`, `/hc/*/search`, account and ticket paths | No (would be a workaround) |
| *.fcsuite.com | Named AI agents disallowed on `/` (carried from the earlier study) | Not fetched |
| www.ncfgiving.com | `User-agent: *` with an empty `Disallow:`, so all paths are allowed. Sitemap declared | Yes (12 pages, 9 sitemap files) |
| secure.ncfgiving.com | `User-agent: *` … `Disallow: /` (only login-parameter URLs allowed) | No |

### 2.2 NCF donate button: documentation (verbatim, https://www.ncfgiving.com/guide-to-giving-at-NCF)

- **Giving Fund (DAF):** "Can I invite others to give to the fund? Yes. You can invite others to give to your Giving Fund. Including a donate button can make it easy for others to give directly to your fund online. For giving collaboratively with family, friends, your community, or others to support the charities and causes you care about, the donate button provides a simple way to give together. You can share your donate button through email, on your website or blog, or anywhere you’d like to invite others to participate. To set up a donate button, log in to your fund opens in a new tab and select Settings. Use of a donate button is subject to the requirements for eligible donations outlined in our Program Agreement opens in a new tab under “Donate button.”" ("opens in a new tab" is link text in the page.)
- **Single-Charity Fund** (held for one charity; not donor-advised): "A Single-Charity Fund can include a donate button that makes it easy for supporters to give directly to your fund online." The flyer page https://www.ncfgiving.com/documents/single-charity-fund-for-charities/ says the same: "Invite supporters to contribute through an NCF donate button".
- **Unidentified gifts:** "Unidentified gifts will be placed in a holding account until NCF can identify the giver and fund. If the gift remains unidentified despite NCF’s good-faith efforts to identify the giver, it will be placed in the general fund for NCF."
- **Status of the guide:** "No part of this document constitutes an agreement between NCF and any giver or any other person or otherwise binds any person." The binding rules are therefore in the unread agreement section.
- **Default state:** the guide says the fundholder sets the button up. Read with "To set up", this suggests it is off until enabled [I]. No default is stated.

### 2.3 Counting donate pages

- **Sitemap:** https://www.ncfgiving.com/sitemap.xml indexes 8 child sitemaps holding 659 URLs: page 34, post 0, story 453, event 2, document 56, video 22, podcast 18, book 74 [C]. All are on `www.ncfgiving.com`. Only one contains "donat", `/documents/donate-business-interests/`, an asset-giving page [C]. **Fund donate pages in the sitemap: 0.**
- **Links:** the 12 pages read link off-site only to `https://secure.ncfgiving.com/` (login) and `https://secure.ncfgiving.com/agreement`. Both are robots-disallowed.
- **Result:** the number of public Giving Fund donate pages is **not determined**. I found no published route to them, and their host is not stated on any page read. NCF's terms bar automated extraction in any case (§2.5). Re-check 2026-11-20 after the owner lifted the site-terms rule (b52-01; sitemaps re-fetched in wave 52A): still 659 sitemap URLs, 0 fund donate pages, and no link to one, so P-B4222-02-02 stays blocked as not determinable. [V wave 52A]
- **How the counts were made:** `grep -o '<loc>[^<]*</loc>'` over each child sitemap, then `wc -l`, then `grep -ci donat`.

### 2.4 Sizing third-party giving into NCF DAFs

- **FY2024 Schedule D Part I** for NCF (EIN 58-1493949; return 202513109349303201; read from the repo harvest) [R]:
  - DAFs held: 31,943
  - contributions to DAFs: $2,907,564,434
  - grants from DAFs: $2,433,041,612
- **Upper bound only.** These contributions include fundholders' own gifts. Schedule D does not split them by giver, so the figure caps third-party giving but does not estimate it.
- **Other sources:** none of the NCF pages read gives a donate-button count, a dollar total, or the share of gifts from non-fundholders.
- **Result:** the third-party share is **not determined** (queue P-B4222-020101-05).

### 2.5 NCF public-site terms

https://www.ncfgiving.com/terms-and-disclosures (undated). Users agree not to "Use automated means, including bots, crawlers, or spiders, to extract data from the Public Website without NCF’s permission (i.e., “scrape” data); or Use any content from the Public Website for the development or training of any software program, model, algorithm, or artificial intelligence tool."

robots.txt allows all paths on `www`, but the terms are stricter. I read them partway through the pass and fetched nothing from NCF afterwards. See the process note in §3.

## 3. Limits and process notes

- **Task 1 has no findings.** Nothing here should be read as Foundant's default being either on or off.
- **The NCF agreement's donate-button rules are unknown.** These include eligible donors, minimums, receipting, giver visibility and whether anonymous gifts are allowed.
- **Pages read before the terms.** The NCF pages were fetched with `curl` (11 pages plus the guide, and 9 sitemap files) before the terms page was read. The terms page itself was one of the 11. These were small, targeted reads of named URLs, not a crawl. Still, under NCF's terms the stricter reading would have called for reading the terms first. Queue P-B4222-020101-04 proposes manual-only practice for this host. On 2026-11-20 the owner lifted the site-terms rule for such hosts (polite, named-page fetches only); b52-01 re-read the same pages under that decision, so these results no longer rest only on the earlier reads. [V wave 52A]
- **Repo compliance flag.** The repo already carries clauses of NCF's Program Agreement (effective 2025-09-17), read on 2026-11-14 from `secure.ncfgiving.com`. That host's robots.txt disallows `/` for all agents. The carried census row does not record this. The earliest repo record of the disallow is the batch 35 B robots log (queue-batch35-access-owners-faith.md, prepared 2026-11-15). [V wave 46A] I did not use those clauses for any finding here. Queue P-B4222-020101-03 asks the owner to review them.
- **Provenance note (validation).** secure.ncfgiving.com/robots.txt was re-read on 2026-11-20 at 04:08 UTC. It is the Salesforce platform template (‘robots.txt for sfdc appservers’): `googlebot` is allowed, and `*` is disallowed on `/` except login-parameter URLs. The 2026-11-14 study that read the agreement logged no robots check, so whether the disallow applied that day cannot be known. The Wayback Machine was unreachable from the validation session. 74 lines in 37 files under research/ and data/ cite the host, for Program Agreement clauses and for login-page fingerprints. The options are left to the owner (validation-wave46a-report.md). [V wave 46A]
- **Recency.** All evidence is from 2024 onward: live pages read 2026-11-20 and the FY2024 990.

## 4. Data dictionary: `foundant-docs-ncf-donate-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_id | R = robots result; D = document-level quote or status; A = aggregate count or status |
| task | T1 = Foundant documentation; T2 = NCF donate button (P-B4222-02-02) |
| row_type | robots, document or aggregate |
| entity_or_host | Host (robots rows), document, or entity |
| item | What the row records |
| value | Finding: Y, a count, a dollar figure (for A04, semicolon-separated in the order of `item`), or "not determined" / "not read" |
| quote | Verbatim text from source_url (robots quotes use " / " for line breaks); blank if none |
| source_url | Primary URL; blank where nothing could be read |
| evidence_label | F fetched, C computed, R carried from repo, B blocked or not determined |
| access_status | Whether the host or page was read, and why not |
| notes | Context, caveats, cross-references |
| retrieved | Date of read (2026-11-20) |

## 5. Source register

| Source | URL | Read |
|---|---|---|
| Foundant robots.txt | https://www.foundant.com/robots.txt ; https://foundant.com/robots.txt | 2026-11-20 (robots only) |
| Foundant help-centre robots.txt | https://help.foundant.com/robots.txt | 2026-11-20 (robots only) |
| Foundant support robots.txt | https://support.foundant.com/robots.txt | 2026-11-20 (robots only) |
| fcsuite robots.txt (carried) | https://cfga.fcsuite.com/robots.txt | not re-read |
| NCF robots.txt | https://www.ncfgiving.com/robots.txt | 2026-11-20 |
| NCF secure-site robots.txt | https://secure.ncfgiving.com/robots.txt | 2026-11-20 |
| NCF guide to giving | https://www.ncfgiving.com/guide-to-giving-at-NCF | 2026-11-20 |
| NCF sitemap index and children | https://www.ncfgiving.com/sitemap.xml (sitemap-page, -post, -story, -event, -document, -video, -podcast, -book .xml) | 2026-11-20 |
| NCF Single-Charity Fund page | https://www.ncfgiving.com/documents/single-charity-fund-for-charities/ | 2026-11-20 |
| NCF public-site terms | https://www.ncfgiving.com/terms-and-disclosures | 2026-11-20 |
| NCF Program Agreement | https://secure.ncfgiving.com/agreement | not read (robots) |
| NCF FY2024 Form 990 | https://projects.propublica.org/nonprofits/organizations/581493949/202513109349303201/full (via repo harvest) | carried |
| Repo inputs | data/mission-2026-11-14/portal-features-2026-11-19.csv (PF-29); data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv; research/mission-2026-11-14/b4222-02-01-foundant-giving-hub.md | 2026-11-20 |
