# Citation link health, 2026-11-19

**What this is.** A mechanical check of whether the web pages cited in `research/**/*.md` still respond, run on 2026-11-19 by [`scripts/mission_link_health.py`](../../scripts/mission_link_health.py). Per-URL results: [`citation-link-health-2026-11-19.csv`](../../data/mission-2026-11-14/citation-link-health-2026-11-19.csv). Headline-document citations with their sentences: [`citation-link-health-2026-11-19-headline-occurrences.csv`](../../data/mission-2026-11-14/citation-link-health-2026-11-19-headline-occurrences.csv). Queue proposals: [`queue-proposals-links19.csv`](../../data/mission-2026-11-14/queue-proposals-links19.csv).

A live URL does not mean the page still says what the research says it says. This audit tests reachability only, not content.

## Method
- **Extraction.** Every `http(s)://` string in 252 markdown files under `research/` was extracted, cleaned of trailing punctuation and unbalanced brackets, and de-duplicated without the `#fragment`. This gives **3,409 unique URLs** from 12,707 citations. (FINAL-STATUS counted 3,424 with a simpler regex.)
- **Priority.** P1: cited in the industry report, the strategic synthesis or FINAL-STATUS (148 URLs). P2: cited in a `direction-*.md` file and not P1 (819). P3: everything else (2446), randomly sampled with seed 20261119 to fill the request budget.
- **Robots first.** For each host, `robots.txt` was fetched before any other request (one GET per scheme and host). Rules were applied by RFC 9309 longest match for the `*` group (no group names this checker). Crawl-delay was honoured up to 10 s. A `robots.txt` returning 404/410 means no rules (RFC 9309 §2.3.1.3). Any other failure (401/403/429/5xx, timeout, proxy or connection error) means **not checked (robots)**: no further request went to that host.
- **Check.** HEAD first. GET with `Range: bytes=0-0` only when HEAD was refused (400/403/405/406/501), and the body was not read. **Confirmation pass:** every HEAD result of 404/410 was re-checked once with GET (`--confirm-dead`, robots.txt re-read first), because some servers answer HEAD with 404 while GET works. 20 of 38 HEAD 404/410 results answered GET with 2xx and are counted as alive or moved; only URLs that failed both are **dead**. Redirects were followed by hand up to 5 hops, and only after the new host's `robots.txt` allowed the target. A redirect to a different path or host counts as **moved**. A redirect that only changes http→https, `www.` or a trailing slash counts as **alive**.
- **Archive.** For 404/410 results, the archive.org availability API (`/wayback/available`) was queried, after checking archive.org's `robots.txt`.
- **Limits.** At least 1 s between requests to one host; generic User-Agent `Mozilla/5.0 (compatible; link-health-check/1.0)`; 20 s timeout; hard cap of 2,495 HTTP requests including robots.txt and archive calls. **2,257 requests were sent** (main run plus GET confirmation pass), plus 5 in a pre-run smoke test, for 2,262 in total. crt.sh was never requested (compliance note of 2026-11-15). No logins and no forms.

## Summary
Shares below are of URLs **attempted** (robots-blocked counts as attempted: robots.txt was read or failed, and the URL was then withheld). "Not attempted" means not sampled, out of budget, crt.sh, or a placeholder.

| Group | Attempted | alive | moved | dead | 4xx other | 5xx | timeout | connection error | robots-blocked | Not attempted |
|---|---|---|---|---|---|---|---|---|---|---|
| All URLs | 1266 of 3409 | 945 (74.6%) | 122 (9.6%) | 18 (1.4%) | 52 (4.1%) | 3 (0.2%) | 17 (1.3%) | 0 (0.0%) | 109 (8.6%) | 2143 |

| Group | Attempted | alive | moved | dead | 4xx other | 5xx | timeout | connection error | robots-blocked | Not attempted |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 headline docs | 148 of 148 | 115 (77.7%) | 14 (9.5%) | 4 (2.7%) | 1 (0.7%) | 0 (0.0%) | 3 (2.0%) | 0 (0.0%) | 11 (7.4%) | 0 |
| P2 direction-*.md | 817 of 819 | 620 (75.9%) | 91 (11.1%) | 6 (0.7%) | 36 (4.4%) | 3 (0.4%) | 6 (0.7%) | 0 (0.0%) | 55 (6.7%) | 2 |
| P3 other (sampled) | 301 of 2442 | 210 (69.8%) | 17 (5.6%) | 8 (2.7%) | 15 (5.0%) | 0 (0.0%) | 8 (2.7%) | 0 (0.0%) | 43 (14.3%) | 2141 |

- **Alive:** 945 of 1266 attempted (74.6%); **moved** (redirected to a new location that answers 2xx): 122 (9.6%). Of the moved URLs, 2 redirect a deep link to a site homepage, a likely soft 404.
- **Dead (404/410):** 18 (1.4%). Archive lookups for dead URLs: no capture: 11, capture: 7.
- **Other 4xx:** 52 (403: 52). Hosts: doi.org (13), www.nysenate.gov (5), www.bogleheads.org (4), causeshelp.benevity.org (2), philanthropy.org (2), www.fintechfutures.com (2), www.gartner.com (2), achdevguide.nacha.org (1). A 403 usually means a bot or access wall, not a missing page, so these are not counted as dead.
- **5xx:** 3; **timeouts:** 17; **connection or proxy errors:** 0.
- **Robots-blocked:** 109 (8.6%). By reason: not checked (robots: robots unreadable (403)): 46; not checked (robots: disallowed): 28; not checked (robots: robots unreadable (503)): 16; redirect target not checked (robots: disallowed): 5; not checked (robots: robots unreadable (error: RemoteDisconnected: Remote end closed connection without response)): 3; not checked (robots: robots unreadable (401)): 2; not checked (robots: robots unreadable (520)): 2; not checked (robots: robots unreadable (301)): 1.
- **Not attempted:** 2143 (not checked (not sampled): 2116; not checked (crt.sh policy): 22; not checked (placeholder): 5).
- Hosts with the most dead URLs: www.reninc.com (3), advisors.ubs.com (1), developer.candid.org (1), engage.aefonline.org (1), intercom.help (1), kalfound.org (1), ohiocpa.com (1), thecr.com (1), theveritasfoundation.com (1), vinkius.com (1).

## Dead links in the headline documents
4 unique dead URLs are cited 19 times in the industry report, the strategic synthesis and FINAL-STATUS. The "Sentence" column is the sentence or table cell that carries the citation (`<url>` marks where the link stood). The "Other sources" column says whether the same sentence also cites a live URL or a repository file.

| Location | Dead URL | Status | Sentence | Other sources | Archive |
|---|---|---|---|---|---|
| DAF-INDUSTRY-REPORT-2026-11.md:71 | https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf | HEAD 404; GET 404 | Renaissance Charitable Foundation sponsors branded programs for Edward Jones, Ameriprise, RBC, LPL/Commonwealth (Commonwealth sponsorship by RCF inferred), Northwestern Mutual, UBS (one of four sponsors there), SEI, Fisher and MDRT ([Edward Jones Charitable Gift Fund portal]; [Ameriprise RCF portal]; [RBC RCF portal]; … | another cited source alive | no capture |
| DAF-INDUSTRY-REPORT-2026-11.md:87 | https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf | HEAD 404; GET 404 | - The 2021 "$2.9bn" figure is unverifiable (source PDF now 404) **[V]** ([Ren/RCF Edward Jones adviser guide (HTTP 404)]; repo [`validation-register.csv`](../data/mission-2026-11-14/validation-register.csv)). | only external source dead; repo pointer present | capture 20250109124657 http://web.archive.org/web/20250109124657/https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf |
| DAF-INDUSTRY-REPORT-2026-11.md:105 | https://developer.candid.org/docs/faqs-charity-check | HEAD 404 after 301; GET 404 after 301 | IRS BMF, Pub 78, revocation and OFAC data sit upstream of every disclosed eligibility check ([IRS EO BMF extract]; [IRS TEOS bulk data downloads]; [IRS Auto-Revocation List]; [Chariot compliance help page]; [Candid Charity Check FAQ]; [RCF grantmaking due-diligence policy]). | another cited source alive | capture 20250425115007 http://web.archive.org/web/20250425115007/https://developer.candid.org/docs/faqs-charity-check |
| DAF-INDUSTRY-REPORT-2026-11.md:135 | https://engage.aefonline.org/dc-sunset/ | HEAD 404; GET 404 | History loss in platform migrations \| Habit ([AEF DonorCentral sunset notice]) | only external source dead; NO repo pointer | capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/ |
| DAF-INDUSTRY-REPORT-2026-11.md:169 | https://engage.aefonline.org/dc-sunset/ | HEAD 404; GET 404 | AEF's own migration kept two years ([AEF DonorCentral sunset notice]). | only external source dead; NO repo pointer | capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/ |
| DAF-INDUSTRY-REPORT-2026-11.md:957 | https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf | HEAD 404; GET 404 | - UBS DAF fact sheet (Feb 2023): <url> | source-list entry (not a claim) | no capture |
| DAF-INDUSTRY-REPORT-2026-11.md:970 | https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf | HEAD 404; GET 404 | - Ren/RCF Edward Jones adviser guide (HTTP 404) (c. 2021-22; 404 on 2026-11-14): <url> | source-list entry (not a claim) | capture 20250109124657 http://web.archive.org/web/20250109124657/https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf |
| DAF-INDUSTRY-REPORT-2026-11.md:995 | https://developer.candid.org/docs/faqs-charity-check | HEAD 404 after 301; GET 404 after 301 | - Candid Charity Check FAQ (accessed 2026-11-14): <url> | source-list entry (not a claim) | capture 20250425115007 http://web.archive.org/web/20250425115007/https://developer.candid.org/docs/faqs-charity-check |
| DAF-INDUSTRY-REPORT-2026-11.md:1008 | https://engage.aefonline.org/dc-sunset/ | HEAD 404; GET 404 | - AEF DonorCentral sunset notice (2026-10-31): <url> | source-list entry (not a claim) | capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/ |
| FINAL-STATUS.md:157 | https://engage.aefonline.org/dc-sunset/ | HEAD 404; GET 404 | ([GTCF DAF transfer instructions]; [Daffy help: closing an account]; [AEF DonorCentral sunset notice]; repo [`sponsor-transfer-portability-terms.csv`](../../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv)) | another cited source alive | capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/ |
| FINAL-STATUS.md:238 | https://engage.aefonline.org/dc-sunset/ | HEAD 404; GET 404 | - AEF DonorCentral sunset notice (2026-10-31): <url> | source-list entry (not a claim) | capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/ |
| strategic-synthesis.md:26 | https://engage.aefonline.org/dc-sunset/ | HEAD 404; GET 404 | A8 \| None of 12 sponsors reviewed publishes an outbound transfer policy. (repo [`sponsor-transfer-portability-terms.csv`](../../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv)) Transfers are usually liquidated to cash, take 10 business days to 4 weeks, and carry **no grant-history portability** (AEF's o… | another cited source alive | capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/ |
| strategic-synthesis.md:73 | https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf | HEAD 404; GET 404 | **Architectural: shared single points of failure** \| Several wealth-firm programs use RCF as sponsor and Ren as technology (Edward Jones, Ameriprise, RBC, LPL/Commonwealth (Commonwealth sponsorship by RCF inferred), Northwestern Mutual, UBS (one of four sponsors), SEI, Fisher, MDRT). ([Edward Jones Charitable Gift Fund… | another cited source alive | no capture |
| strategic-synthesis.md:77 | https://engage.aefonline.org/dc-sunset/ | HEAD 404; GET 404 | **Customer experience: history and portability** \| No outbound transfer policies; no history portability; (repo [`sponsor-transfer-portability-terms.csv`](../../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv)) separate logins (Edward Jones portal is distinct from the brokerage login); ([Edward Jones Cha… | another cited source alive | capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/ |
| strategic-synthesis.md:96 | https://developer.candid.org/docs/faqs-charity-check | HEAD 404 after 301; GET 404 after 301 | Charity master data \| IRS BMF/Pub 78/revocations/OFAC are free and authoritative; every disclosed eligibility check sources from them ([IRS TEOS bulk data downloads]; [IRS Auto-Revocation List]; [OFAC Framework for Compliance Commitments]; [Chariot compliance help page]; [Candid Charity Check FAQ]) | another cited source alive | capture 20250425115007 http://web.archive.org/web/20250425115007/https://developer.candid.org/docs/faqs-charity-check |
| strategic-synthesis.md:158 | https://engage.aefonline.org/dc-sunset/ | HEAD 404; GET 404 | - Outbound transfers have no published policy at 12 sponsors, run as cash after liquidation in 10 business days to 4 weeks, and carry no history; about $7.5bn moved in 2024 anyway ([GTCF DAF transfer instructions]; [AEF DonorCentral sunset notice]; [Inequality.org on DAF-to-DAF giving]; repo [`sponsor-transfer-portabil… | another cited source alive | capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/ |
| strategic-synthesis.md:273 | https://engage.aefonline.org/dc-sunset/ | HEAD 404; GET 404 | - AEF DonorCentral sunset notice (2026-10-31): <url> | source-list entry (not a claim) | capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/ |
| strategic-synthesis.md:309 | https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf | HEAD 404; GET 404 | - UBS DAF fact sheet (Feb 2023): <url> | source-list entry (not a claim) | no capture |
| strategic-synthesis.md:337 | https://developer.candid.org/docs/faqs-charity-check | HEAD 404 after 301; GET 404 after 301 | - Candid Charity Check FAQ (accessed 2026-11-14): <url> | source-list entry (not a claim) | capture 20250425115007 http://web.archive.org/web/20250425115007/https://developer.candid.org/docs/faqs-charity-check |

Of the 19 citations, 8 are entries in a document's source list (a line of the form "- Name (date): <url>"), not claims. The claims those entries support cite the same URL inline, and the inline citations are classified in the table.

### Headline claims whose only external source is now dead and that carry no repository pointer
A claim is flagged when every external URL in its sentence or table cell is dead and the sentence names no repository file.

- **DAF-INDUSTRY-REPORT-2026-11.md:135** — History loss in platform migrations \| Habit ([AEF DonorCentral sunset notice]) — dead source: https://engage.aefonline.org/dc-sunset/ (only external source dead; NO repo pointer; archive: capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/)
- **DAF-INDUSTRY-REPORT-2026-11.md:169** — AEF's own migration kept two years ([AEF DonorCentral sunset notice]). — dead source: https://engage.aefonline.org/dc-sunset/ (only external source dead; NO repo pointer; archive: capture 20261003000017 http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/)

### Headline claims whose external sources are all dead but that still point to a repository file
- **DAF-INDUSTRY-REPORT-2026-11.md:87** — - The 2021 "$2.9bn" figure is unverifiable (source PDF now 404) **[V]** ([Ren/RCF Edward Jones adviser guide (HTTP 404)]; repo [`validation-register.csv`](../data/mission-2026-11-14/validation-register.csv)). — dead: https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf

### Headline-document URLs that could not be confirmed (robots, access wall, server error, timeout)
These are not evidence that a link is dead. They are listed so a person can check them in a browser.

| URL | Category | Detail |
|---|---|---|
| https://doi.org/10.1177/08997640251331853 | 4xx other | 403 |
| https://efts.sec.gov/LATEST/search-index?q=%22Charitable%20Gift%20Fund%22&ciks=0000070858 | robots-blocked | not checked (robots: robots unreadable (403)) |
| https://github.com/kemiller2002/daf-landscape/pull/20 | robots-blocked | not checked (robots: robots unreadable (403)) |
| https://inequality.org/article/daf-to-daf-giving-2024/ | robots-blocked | not checked (robots: robots unreadable (403)) |
| https://legiscan.com/CA/bill/AB1712/2019 | robots-blocked | not checked (robots: robots unreadable (403)) |
| https://www.businesswire.com/news/home/20220208005152/en | timeout | timeout |
| https://www.businesswire.com/news/home/20230725652545/en/Ren-Secures-Strategic-Growth-Investment-Led-by-Bain-Capital-Tech-Opportunities | timeout | timeout |
| https://www.businesswire.com/news/home/20251001579571/en/Bonterra-Launches-Que-The-First-Agentic-AI-Platform-for-Funders-Nonprofits-and-Supporters | timeout | timeout |
| https://www.federalregister.gov/documents/2023/11/14/2023-24982/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966 | robots-blocked | redirect target not checked (robots: disallowed) |
| https://www.federalregister.gov/documents/2024/01/09/2024-00260/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966 | robots-blocked | redirect target not checked (robots: disallowed) |
| https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx | robots-blocked | not checked (robots: disallowed) |
| https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf | robots-blocked | not checked (robots: robots unreadable (403)) |
| https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads | robots-blocked | not checked (robots: disallowed) |
| https://www.reedsmith.com/articles/private-equity-behind-the-scenes/sec-sets-the-tone-for-2026-regulatory-focus-on-investment-managers/ | robots-blocked | not checked (robots: robots unreadable (timeout)) |
| https://www.thinkadvisor.com/2020/09/30/fidelity-charitable-ends-daf-account-minimums/ | robots-blocked | not checked (robots: robots unreadable (403)) |

### Headline-document URLs that redirect to a new location
| Cited URL | Final URL | Hops |
|---|---|---|
| https://endaoment.org/institutions | https://endaoment.org/api | 308 -> 200 |
| https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/ | https://ffnews.com/news/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving | 301 -> 200 |
| https://guide.charityvest.org/about-our-venture/charityvest-%2B-vennfi | https://guide.charityvest.org/about-our-venture/charityvest-+-vennfi | 302 -> 200 |
| https://help.daffy.org/en/articles/11730892-how-do-i-change-my-membership | https://help.daffy.org/en/articles/11730892-why-did-my-membership-tier-change | 301 -> 200 |
| https://thenonprofittimes.com/?p=215695 | https://thenonprofittimes.com/npt_articles/national-philanthropic-trust-grants-grew-20-to-6-6b/ | 301 -> 200 |
| https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-DAF-Research-Collaborative.pdf | https://static1.squarespace.com/static/6011def87418a462fcb03978/t/6941a4cc17e484296f44b45d/1765909728393/Annual+DAF+Report+2025+-+DAF+Research+Collaborative.pdf | 302 -> 200 |
| https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | https://static1.squarespace.com/static/6011def87418a462fcb03978/t/69e7dcabc2072a18999be588/1776802987461/Annual+DAF+Report+2025+Updated+Analysis+Dataset.xlsx | 302 -> 200 |
| https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf | https://static1.squarespace.com/static/6011def87418a462fcb03978/t/69e91dfad34ffd5d1cb6aea5/1776885242265/Annual+DAF+Report+2025+Updated+Analysis.pdf | 302 -> 200 |
| https://www.foundant.com/products/communitysuite/ | https://www.foundant.com/products/foundation-management-software/ | 301 -> 200 |
| https://www.givechariot.com/post/founders-pledge-selects-chariot-to-power-grant-payments | https://www.givechariot.com/resources/insights/founders-pledge-selects-chariot-to-power-grant-payments | 308 -> 200 |
| https://www.irs.gov/autorevocationlist | https://www.irs.gov/charities-non-profits/automatic-revocation-of-exemption | 301 -> 200 |
| https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/ | https://www.nptrust.org/wp-content/uploads/2024/11/2024-DAF-Report-NPT.pdf | 301 -> 200 |
| https://www.privsource.com/acquisitions/deal/n8S0zL | https://www.privsource.com/acquisitions/deal/foundation-source-acquires-pacific-foundation-services-ane_n8S0zL | 301 -> 200 |
| https://www.young.senate.gov/?p=13549 | https://www.young.senate.gov/newsroom/press-releases/young-bennet-introduce-legislation-to-support-more-charitable-giving-opportunities/ | 301 -> 200 |

## Limitations
- **Reachability, not content.** A 2xx response does not confirm that the page still supports the claim. Redirects to homepages and "page not found" pages served with a 200 status (soft 404s) are flagged only when the redirect itself lands on `/`.
- **HEAD-first bias.** Some servers answer HEAD differently from GET. Every HEAD 404/410 was re-checked with GET, but a HEAD 2xx was not, so a page that answers HEAD 200 and GET 404 would be counted alive. One URL (pr-inside.com) is kept as dead on HEAD because its robots.txt disallowed it at confirmation time.
- **Access walls are not dead links.** 401/403/429 responses and robots.txt files that could not be read are reported separately. They need a browser check, not a re-source.
- **Sampling.** P3 URLs were sampled at random to fit the 2,495-request cap. P3 shares are estimates for the unsampled remainder. P1 and P2 were attempted in full, except where the budget ran out (see "Not attempted").
- **Robots strictness.** Hosts whose `robots.txt` could not be read were not checked at all, so results for those hosts are unknown. Robots rules apply to the `*` group, because no group names this checker.
- **Single run.** Transient outages and rate limits on 2026-11-19 may show as timeouts or 5xx. One re-run would separate them from persistent failures.
- **Proxy.** Requests went through the session's egress proxy. A proxy refusal (CONNECT 403/502) is recorded as a connection or proxy error, not as a site response.
- **Sentence attribution.** Sentences are split mechanically on punctuation, or by table cell. A claim may also be supported by text on neighbouring lines that this audit does not see.
