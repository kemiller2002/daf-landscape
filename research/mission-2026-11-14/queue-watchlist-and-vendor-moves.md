# Watchlist baseline and vendor moves (P-GIV-02, P-GIV-01, P-BUY-01, P-ASR-01, P-VEN-02, P-VEN-08, P-VEN-10)

**Date:** 2026-11-14. **Status:** public sources only. No log-in was attempted and no authenticated page was read. Tenant config files were not probed. No one was contacted.

**Evidence labels** (same as [queue-give-interactive-displacement.md](queue-give-interactive-displacement.md)):
- **confirmed:** a first-party page, a live HTTP response or an IRS filing states the fact.
- **inferred:** convergent indirect evidence, such as CT logs, host names or the timing of a grant.
- **unknown:** no evidence either way.

A certificate name shows that an environment has been configured. **It is not a contract and not a go-live.** A press headline is a lead to check, not a fact.

**Files written:**
- [`scripts/mission_watchlist.py`](../../scripts/mission_watchlist.py): the watchlist runner. Stdlib only, functional style. It reuses the extraction and normalisation code in `mission_terms_monitor.py` and follows the IRS-index pattern in `mission_990_contractors.py`.
- [`data/mission-2026-11-14/watchlist.csv`](../../data/mission-2026-11-14/watchlist.csv): 37 checks.
- [`data/watchlist-snapshots/2026-11-14/`](../../data/watchlist-snapshots/2026-11-14/): one JSON baseline per check.
- [`data/watchlist-snapshots/reports/2026-11-14.md`](../../data/watchlist-snapshots/reports/2026-11-14.md): the baseline report.
- [`data/watchlist-snapshots/manifest.csv`](../../data/watchlist-snapshots/manifest.csv): run log.
- [`relationship-graph-edges-additions-4.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-4.csv): edges ED001–ED008.
- [`queue-proposals-watchlist.csv`](../../data/mission-2026-11-14/queue-proposals-watchlist.csv): proposals P-WAT-01 to P-WAT-05.

---

## 0. Answers

| Item | Answer as of 2026-11-14 | Label |
|---|---|---|
| **P-GIV-01** ImpactAssets DAF Hub | **Not live.** The [homepage](https://impactassets.org/) "CLIENT LOGIN" still points to [`iphi.stellartechsol.com/calvert`](https://iphi.stellartechsol.com/calvert/LogIn/tabid/444/Default.aspx), page title "Account Login - The ImpactAssets Donor Advised Fund". The [transition page](https://impactassets.org/daf-platform-transition/) still announces "a new DAF hub on September 8, 2026", with the key-date "AUG. X" and lorem-ipsum FAQs. A search snippet mentioned a "June 1, 2026" date, but that text is not on the page today. Give Interactive work continues: `ia-innov` was first certified 2026-10-27 and `impactassets-sftp.int` 2026-11-03 ([certspotter](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names)). The sandbox and staging certificates were renewed on 2026-10-12 and 2026-10-06 ([crt.sh](https://crt.sh/?q=%25.giveinteractive.com)). | confirmed (login on iPhi; launch date passed); inferred (Give is the hub vendor) |
| **P-VEN-08** AssetMark program | **Yes, it is on TIFIN Give, and GiveClear Foundation is the sponsor.** AssetMark's [program guidelines](https://intercom.help/assetmark-help-center/en/articles/10924891-assetmark-charitable-program-guidelines) (page date 2025-03-25) say: "AssetMark has contracted with GiveClear Foundation … to be the 501(c)(3) Donor Advised Fund Sponsor, and TIFIN WealthTech, LLC ('TIFIN Give'), to provide a digital DAF platform." The page links to `assetmarkcharitable-release.tifingive.com`. The old iPhi host [`impactassets.iphiview.com`](https://impactassets.iphiview.com/) still redirects 301 → `/assetmark` → 301 → `assetmarkcharitablemc.tifingive.com/login` (title "AssetMark"). The TIFIN `assetmarkcharitable*` hosts were first certified 2024-05-01 (UAT) and 2024-05-28 (production) ([crt.sh](https://crt.sh/?q=%25.tifingive.com)), shortly before the June 2024 announcement ([InvestmentNews](https://www.investmentnews.com/fintech/news/assetmark-and-tifin-give-forge-daf-partnership-254585)). **Migration from ImpactAssets/iPhi:** ImpactAssets' CY2024 Schedule I shows a **$86,038,909 grant to GiveClear Foundation** ("general support"). No such grant appears in CY2023 ([990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543169349307999_public.xml)). **Size:** not disclosed per program. GiveClear as a whole reported **228 DAFs and $215.3m** at end-2024, up from $24.8m. CY2024 contributions were $210.0m, and GiveClear paid Tifin Give LLC $185,921 ([GiveClear 990 CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533199349302978_public.xml)). | confirmed (sponsor, platform, redirect, grant); inferred (the $86m grant is the AssetMark book moving off ImpactAssets/iPhi) |
| **P-VEN-10** "$40B+" | **Plausible only as a pipeline figure dominated by Vanguard; at most about 5% is live.** Identified tenants hold $35.7–36.7bn of DAFRC FY2024 DAF assets (§3). Tenants with a certificate by Sept 2025, when the claim was made, hold $31.6bn. Vanguard alone is $21.95bn, or 55% of $40bn. Its net assets were $27.21bn at 6/30/2025, which would be 68%. Tenants live for donors (The Signatry, WaterStone) hold about $1.95bn. | inferred |
| **P-BUY-01** Vanguard–Altruist | **Not closed.** Vanguard's own [release](https://corporate.vanguard.com/content/corporatesite/us/en/corp/who-we-are/pressroom/press-release-vanguard-announcement-082626.html) still reads "expected to close later this year, subject to customary closing conditions, including receipt of required regulatory approvals". Vanguard raised about $4bn of private-placement debt to finance the deal, reported 2026-11-10 ([WealthManagement](https://www.wealthmanagement.com/financial-technology/vanguard-inks-4-billion-of-private-debt-for-altruist-deal)). No closing announcement appears in the 50-item Google News feed or in EDGAR full-text search since 2026-08-01. The only EDGAR hit is a Lazard 8-K (2026-10-22) that mentions both names. **DAF sponsor:** Altruist's own [DAF page](https://altruist.com/donor-advised-funds/) says "DAFs on Altruist are sponsored by Endaoment" and does not mention Vanguard Charitable. | confirmed (pending; Endaoment); "not closed" means not observed in public sources |
| P-GIV-02 | Baseline set. There is **no production host** for `minneapolisfoundation`, `thriventcharitable`, `stifelcharitable` or `jcf`. New since the earlier timeline: `signatry-sandbox` (2026-11-11), `gms` (2026-11-06), `give-sftp.int` (2026-11-04) and `give-services-api` (2026-10-27). None of these is a new Ren-client slug. | confirmed (CT) |
| P-ASR-01 | **No** Every.org CY2025 return appears in the IRS index. The newest Every.org row is the CY2024 990-PF. The 2026 index was last modified 2026-10-21. | confirmed absence |
| P-VEN-02 | The live donor log-in is unchanged: [`client.vanguardcharitable.org`](https://client.vanguardcharitable.org/) → Salesforce `saml/authn-request.jsp`. **New:** Vanguard Charitable's own CT history shows **`api-give.vanguardcharitable.org`** (first certified 2026-02-25), issued together with `api-salesforce`, `api-vgi` and `auth0` ([crt.sh](https://crt.sh/?q=%25.vanguardcharitable.org)). The FYE 6/2026 990 is not in the index. | confirmed (host); inferred (Give integration endpoint) |

---

## 1. The watchlist

### 1.1 What it checks

| Type | Checks | Signal flagged in the report |
|---|---|---|
| `ct_crtsh` | `%.giveinteractive.com` (all names, plus per-tenant views for Minneapolis, Thrivent, Stifel, JCF, ImpactAssets, Vanguard); `%.giveinteractive-clients.com`; `%.tifingive.com`; `%.vanguardcharitable.org` | New names; a `watch_regex` name appears for the first time, for example `^minneapolisfoundation\.giveinteractive\.com$`, the production host |
| `ct_certspotter` | `giveinteractive.com`, currently valid issuances | Same as above. Certspotter indexes new hosts before crt.sh |
| `http` | Log-in links and redirect chains for ImpactAssets (home, transition page, iPhi `calvert` log-in, `impactassets.iphiview.com`), Vanguard Charitable (home, `client.`), WaterStone, Minneapolis (site and iPhi), Thrivent (site and iPhi), Stifel (DAF page and iPhi), AssetMark (guidelines and TIFIN log-in), Altruist DAF page, and Vanguard's Altruist release | Change in final host or status, matching links, "Powered by"/copyright footers, `watch_regex` URL hits or sentences |
| `rss` | Google News: "Vanguard Altruist"; "Altruist donor-advised" | New headlines that match close/complete, or Endaoment/Vanguard Charitable |
| `sec_efts` | EDGAR full-text "Altruist" + "Vanguard" since 2026-08-01 (8-K, 425, SC 13D, ADV, BD, D) | New filings |
| `irs_index` | Every.org, Vanguard Charitable, Givinga, ImpactAssets, GiveClear, Endaoment | A return with `tax_period` ≥ the watched period appears; any new index rows |

### 1.2 How to run

```
python3 scripts/mission_watchlist.py                    # all checks, today's date
python3 scripts/mission_watchlist.py --type irs_index   # one type (repeatable)
python3 scripts/mission_watchlist.py --only http-ia-home
python3 scripts/mission_watchlist.py --report-only      # rebuild today's report
```

- **Cadence.** Run weekly. P-GIV-01 asks for weekly log-in checks.
- **Partial runs.** A run with `--only` or `--type` merges into that date's report.
- **IRS index cache.** The index files (60–100 MB each) are kept outside the repo, in `--irs-dir` or `$WATCHLIST_IRS_DIR` (default `~/.cache/daf-landscape/irs-index`). They are downloaded again only when the IRS `Last-Modified` changes. The default years are the run year −1, the run year and the run year +1, and `index_2027.csv` will be picked up automatically when it appears.
- **Next run.** The next run compares itself with the latest earlier successful snapshot of each check.
- **User-agent.** The runner sends an honest generic user-agent. Override it with `WATCHLIST_UA` if a site (for example SEC) asks for a declared contact.

### 1.3 Baseline result

- 36 of 37 checks were observed.
- **WaterStone returned HTTP 403** (Cloudflare) to the script. It is logged as failed. The cut-over is already confirmed in [queue-give-interactive-displacement.md](queue-give-interactive-displacement.md) §2, and `waterstone.giveinteractive.com` is tracked through CT.
- crt.sh accepts only a **leading** `%` wildcard. The per-tenant checks therefore share one cached domain query and narrow it with `name_filter`.

---

## 2. Login-link and host baseline (2026-11-14)

| Sponsor | Log-in link / final host | Give hosts (first cert) | Reading |
|---|---|---|---|
| ImpactAssets | `iphi.stellartechsol.com/calvert` (Stellar) ([home](https://impactassets.org/)) | production `impactassets` 2026-01-28; 9 `ia-*` feature hosts (2026-02-24 to 2026-09-01); `ia-innov` 2026-10-27; SFTP 2026-11-03 | Launch date 2026-09-08 has passed, and the log-in is still on iPhi |
| Minneapolis Foundation | "Donor Login" → `tmf.iphiview.com/tmf/` ([site](https://www.minneapolisfoundation.org/)) | `minneapolisfoundation-staging` 2026-02-12; `tmf-sftp.int` 2026-10-05 | No production host |
| Thrivent Charitable | `www.thriventcharitable.com` → 301 `thriventcharitable.thrivent.com`. "Log In" → `infaith.iphiview.com` ([site](https://www.thriventcharitable.com/)). The iPhi page footer reads "© 2025 Thrivent Charitable" | `thriventcharitable-staging` 2026-08-14; `thrivent-sftp.int` 2026-10-05; `tc-innov` 2026-11-09 (slug match inferred) | No production host |
| Stifel Charitable | "DonorView Portal" → `sci.iphiview.com` ([DAF page](https://www.stifel.com/individual/donor-advised-funds)) | `stifelcharitable-staging` 2026-06-25; `stifel-sftp.int`/`.ext` 2026-09-04 | No production host |
| JCF (inferred slug) | not checked (jcfny.org returned 403 earlier) | `jcf-staging` 2026-01-21 … `jcf-sandbox` renewed 2026-10-15 | No production host |
| Vanguard Charitable | `#login` (Auth0) on [home](https://www.vanguardcharitable.org/); `client.` → Salesforce SAML | `vanguardcharitable` 2026-01-28; `vc-innov` 2026-10-09; `vanguard-sftp.int` 2026-11-03 | Ledger implementation; the donor UX is Salesforce |
| AssetMark Charitable | `impactassets.iphiview.com` → `assetmarkcharitablemc.tifingive.com/login` | n/a (TIFIN: `assetmarkcharitable*` 2024-05-01/28; `auth-give-amk` 2024-05-28) | On TIFIN Give since mid-2024 |
| Altruist DAF | [`altruist.com/donor-advised-funds/`](https://altruist.com/donor-advised-funds/) links to [endaoment.org](https://endaoment.org/); log-in `app.altruist.com` | n/a | Endaoment-sponsored |

---

## 3. P-VEN-10: reconciling "$40B+ live or in implementation"

The claim reads "2025 $40B+ live or in implementation" ([company page](https://www.giveinteractive.com/company)). BD Emerson repeats it as of Sept 2025 ([case study](https://www.bdemerson.com/case-studies/give-interactive)).

Sources for the table:
- **DAF assets:** DAFRC FY2024 ([dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)). Where DAFRC imputed a value, the filed 990 value is also shown ([dafrc-corrections-itemized.csv](../../data/mission-2026-11-14/dafrc-corrections-itemized.csv)).
- **First cert:** from [give-interactive-client-timeline.csv](../../data/mission-2026-11-14/give-interactive-client-timeline.csv) and this baseline.

| Tenant | Status 2026-11-14 | First Give cert | DAFRC FY2024 DAF $bn | Filed/corrected $bn |
|---|---|---|---|---|
| Vanguard Charitable | implementation (ledger) | 2025-08-06 | 21.95 | 21.95 |
| Chicago Community Trust | implementation (production host; portal GiftingNetwork) | 2024-08-12 | 4.65 | 4.65 |
| ImpactAssets | implementation, dual tenancy | 2025-04-29 | 3.63 (imputed) | 2.90 |
| Jewish Communal Fund (inferred) | implementation | 2026-01-21 | 2.87 | 2.87 |
| Servant Foundation (The Signatry) | live | 2021-06-15 | 1.01 | 1.01 |
| Signatry Charitable Trust | live | 2021-06-15 | 0.40 (imputed) | 0.80 |
| Minneapolis Foundation | implementation (staging) | 2026-02-12 | 0.60 | 0.60 |
| Thrivent Charitable | implementation (staging) | 2026-08-14 | 0.59 | 0.59 |
| WaterStone | live (2026-11-01) | 2025-10-28 | 0.54 | 0.54 |
| Stifel Charitable | implementation (staging) | 2026-06-25 | 0.49 | 0.49 |
| **All identified** | | | **36.74** | **36.40** |
| Certified by 2025-09-30 (Vanguard, CCT, ImpactAssets, Signatry) | | | 31.64 | 31.30 |
| Live for donors today (Signatry entities, WaterStone) | | | 1.95 | 2.34 |

`nhf`, `jttw` and `jmacarthurtrust` are unresolved and add nothing. Foundation for the Carolinas ($2.95bn) is excluded because it lapsed by Feb 2024.

**Reading (inference).**
1. **The claim is consistent with a pipeline figure.** At claim time, the four tenants with certificates hold $31.6bn of FY2024 DAF assets. Using Vanguard's 6/30/2025 net assets of $27.21bn instead of DAF assets ([FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)) lifts the total to about $37bn. Contracts usually precede certificates, so clients signed but not yet certified (JCF, Minneapolis) could close the rest of the gap. The basis Give uses (DAF assets, total assets, or current market values) is **unknown**.
2. **Vanguard is 55–68% of the claim.** The figure therefore says little about Give's breadth.
3. **Almost all of it is implementation, not live.** Donor-live tenants are about $1.95bn, or 5% of $40bn.
4. **Double-count caveat.** Servant Foundation moved its DAF book into the Signatry Charitable Trust in 2023–25. Counting both at different dates may overstate that row by up to about $1bn. Excluding Servant gives $35.7bn, which matches the earlier estimate in [queue-vendor-scope-ren-denominator.md](queue-vendor-scope-ren-denominator.md) §1.3.

---

## 4. P-VEN-08 detail: AssetMark's move off ImpactAssets/iPhi

| Evidence | Fact | Label |
|---|---|---|
| Redirect | `impactassets.iphiview.com` → `impactassets.iphiview.com/assetmark` → `assetmarkcharitablemc.tifingive.com:443/login` (baseline `http-ia-iphi`) | confirmed |
| Sponsor and platform | GiveClear Foundation (sponsor); TIFIN WealthTech LLC (platform). Fees 0.60% to $1m, 0.20% above ([guidelines](https://intercom.help/assetmark-help-center/en/articles/10924891-assetmark-charitable-program-guidelines)). The [overview](https://intercom.help/assetmark-help-center/en/articles/10646047-assetmark-charitable-program-overview) says "AssetMark Charitable has partnered with the GiveClear Foundation" | confirmed |
| Timing | TIFIN hosts first certified 2024-05 ([crt.sh](https://crt.sh/?q=%25.tifingive.com)). Partnership announced June 2024 ([InvestmentNews](https://www.investmentnews.com/fintech/news/assetmark-and-tifin-give-forge-daf-partnership-254585)). TIFIN's case study says AssetMark decided "in mid-2024" to "evolve its donor-advised fund program" (search snippet; the [page](https://tifin.com/resources/dafs-are-no-longer-a-nice-to-have-test/19597/) returned 404 to fetch) | confirmed (certificates, announcement); snippet only (case study) |
| Money moved | ImpactAssets CY2024 Schedule I: GiveClear Foundation $86,038,909 "GENERAL SUPPORT". GiveClear CY2024: DAF contributions $210,026,838; DAFs 228; EOY $215,283,755 (CY2023 $24,788,267). Tifin GIve LLC paid $185,921 for "Technical and Charitable Support Services" | confirmed |
| Prior sponsor | The redirect lives on ImpactAssets' iPhi subdomain, which suggests the old AssetMark-branded DAF was an ImpactAssets program on Stellar's iPhi. No first-party page says so | inferred |
| Program size | No per-program figure. Upper bound: all of GiveClear ($215m at end-2024), which also serves Zions, SEI (from 2026-10) and other partners (edges E140–E143, E048) | unknown (bounded) |

Related signal: ImpactAssets also granted **$160,826,426 to National Philanthropic Trust** in CY2024, its largest grant that year. The purpose is unknown (proposal P-WAT-02).

---

## 5. Limits

- **Single date.** Every finding is a single-date observation. "Not closed" and "not live" mean not observed in public sources on 2026-11-14.
- **SEC.** EDGAR full-text search does not index Form ADV or BD. Vanguard Group is private, so its acquisition may produce no 8-K. SEC asks automated clients to declare a contact. The runner sends a generic name and EFTS answered 200; `www.sec.gov/cgi-bin` browse pages refused it.
- **Google News.** Coverage varies over time, and the headlines are secondary.
- **WaterStone.** The site blocks scripted fetches (403).
- **IRS index.** The 2026 index was last updated 2026-10-21, so returns filed after that date are invisible until the next update.
- **Not probed.** Give and TIFIN tenant config files and the content of `api-give.vanguardcharitable.org` were not probed. Host names only.

---

## 6. Data dictionary

### `data/mission-2026-11-14/watchlist.csv`

| Column | Meaning |
|---|---|
| `check_id` | Unique slug. It is also the snapshot file name |
| `check_type` | `ct_crtsh`, `ct_certspotter`, `http`, `rss`, `sec_efts` or `irs_index` |
| `entity` | Sponsor, vendor or deal watched |
| `queue_items` | Queue IDs served (`;`-separated) |
| `target` | crt.sh query (leading `%` only), certspotter domain, URL, EDGAR query or EIN (9 digits) |
| `link_regex` | `http` only: regex selecting anchors and script/iframe sources (by href or text) to record |
| `watch_regex` | What counts as a signal: CT names, URL/footer substrings and sentences (`http`), headlines (`rss`) |
| `params` | `k=v;k=v`. `name_filter` (crt.sh), `max_pages` (certspotter), `startdt`, `forms` (EDGAR, `\|`-separated), `min_tax_period` (YYYYMM), `types`, `years` (IRS) |
| `notes` | Baseline context and caveats |

### `data/watchlist-snapshots/<date>/<check_id>.json`

| Field | Meaning |
|---|---|
| `check_id`, `check_type`, `entity`, `queue_items`, `target`, `watch_regex` | Copied from config |
| `date`, `observed_at_utc` | Run date and UTC timestamp |
| `ok`, `status`, `error` | Fetch outcome (HTTP code, `bad_json`, exception class) |
| `source_url` | Human-readable source to cite |
| `summary` | Stable fields compared between runs. CT: `names`, `watch_hits`, `name_count`. http: `final_host`, `final_status`, `chain_hosts`, `title`, `links`, `footers`, `watch_hits_urls`, `watch_sentences`. rss: `items`, `watch_hits`. sec: `filings`. irs: `returns`, `target_return_present`, `target_returns`, `min_tax_period` |
| `detail` | Supporting data that is not compared. CT: per-name `first_not_before`/`last_not_before`/`certs`. http: full redirect `chain`, form actions, meta, text/raw sha256. irs: rows, index Last-Modified, XML and ProPublica URLs |

### `data/watchlist-snapshots/reports/<date>.md`

- **Summary table.** One row per check: status, state (`baseline`, `unchanged`, `changed` or `failed`), previous date and signals.
- **Per-check sections.** Current observations and the changes against the previous snapshot.

### `data/watchlist-snapshots/manifest.csv`

Columns: `date, check_id, check_type, entity, queue_items, status, state, previous_date, signals, error`. There is one row per check per date, and a re-run on the same date replaces that date's rows.

### `relationship-graph-edges-additions-4.csv`

The columns are the same as the other edge files. ED001–ED008 add one new relationship type, `grant_to`: a Schedule I grant from one DAF sponsor to another, with the amount in `evidence_summary`. ED007 uses status `pending`, for a signed deal that has not closed.

### `queue-proposals-watchlist.csv`

Format per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md), prefix `P-WAT-`.

## Validation corrections (wave 5, 2026-11-14) — governing
Source: [validation-wave5-report.md](validation-wave5-report.md). Where these conflict with the text above, these govern.

9. **`research/mission-2026-11-14/queue-watchlist-and-vendor-moves.md`, line 28 (P-VEN-08).** After "GiveClear as a whole reported **228 DAFs and $215.3m**", add: "The count of 228 is identical to CY2023's despite 8.7× asset growth, so treat it as unreliable."
