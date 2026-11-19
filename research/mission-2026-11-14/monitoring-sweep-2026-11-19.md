# Monitoring sweep, 2026-11-19

**Scope.** This sweep covers the 49 queue items in `data/mission-2026-11-14/research-priority-queue.csv` with `state=monitoring`. For each, it asks whether the awaited event happened after the 2026-11-14/15 baseline.

**Rules followed.**
- robots.txt was read before any page on a host was fetched (register below).
- Hosts whose robots.txt could not be read were not fetched. crt.sh was not used.
- The client was generic: `daf-landscape-watchlist/1.0 (research; public pages)`.
- There were no logins, forms, keyed APIs or outreach.

The research docs were not edited. Per-item data is in `data/mission-2026-11-14/monitoring-sweep-2026-11-19.csv` and follow-ups are in `data/mission-2026-11-14/queue-proposals-mon19.csv`.

## Headline

- **No awaited headline event happened.**
  - None of the expected CY2025 or FY2026 Form 990s is in the IRS TEOS index for the 12 named sponsors (Fidelity FY6/2026, Vanguard, DAFgiving360, NPT, Givinga, PayPal Giving Fund, Every.org, GS DAPF, Philanthropi, Endaoment, Goodstack US and JCF). Two exceptions are covered in the next section: Goodstack US's CY2025 return, indexed before the baseline, and an amended Fidelity FY6/2025 return.
  - The index was updated on 2026-11-18 (Last-Modified 14:01:58 GMT, up from 2026-10-21). The update added one batch, `2026_TEOS_XML_10A` (43,662 rows).
  - There is no Peterson v. WaterStone ruling in reachable sources, no Vanguard–Altruist close, and no new IRS DAF regulation.
  - No Federal Register IRS document matched "donor advised fund" or "4966" between 2026-11-01 and 2026-11-19, and the IRS had nothing on today's public-inspection list.
- **New filing (not awaited): Fidelity Charitable amended its FY6/2025 Form 990.**
  - The amended 990 is object `202622879349301322` (signed 2026-09-29, e-filed 2026-10-14). The 990-T is object `202642879339300829`.
  - Schedule O: "IS FILING AN AMENDED FORM 990 TO CORRECT AN OVERSTATEMENT OF CAPITAL GAIN NET INCOME ATTRIBUTED TO UNRELATED BUSINESS REVENUE".
  - Gross UBI falls from $88,982,918 to $80,591,303, and Schedule A public support moves from 83.800% to 83.803%.
  - On the 990-T, UBTI falls from $87,754,231 to $79,362,616 and tax from $7,032,458 to $6,361,129.
  - **Schedule D is unchanged** (224,884 DAFs; contributions $26.46bn; grants $15.25bn; EOY $85.48bn). The Schedule I total is also unchanged.
  - No research sentence cites the changed figures (grep), so no finding needs updating.
- **Give Interactive certificate transparency (certspotter): 2 new non-production names.**
  - `thriventcharitable-sandbox2.giveinteractive.com` (first cert 2026-11-17) and `vanguard-dr-sftp.int.giveinteractive.com` (first cert 2026-11-16).
  - There is still no production-named host for Minneapolis, Thrivent, Stifel or JCF.
  - The TMF, Thrivent, Stifel and ImpactAssets homepages still link their iPhi logins.
- **One in-scope iPhi sponsor filed CY2025 (P-REN-02).**
  - Community Foundation of Jackson Hole: object `202632959349300518`, 195 DAFs, $85.8m.
  - It has no Stellar or Ren line in its top-5 Part VII-B list, and its CY2022–24 returns had none either.
- **Ren / RCF portals changed only housekeeping items.**
  - New "Year End Deadlines 2026" brochures, a new maintenance notice (Saturday, November 21) and the Ren LPL page's 2026 Investment Policy Statement (`/wp-content/uploads/2026/11/Investment-Policy-Statement-2026.pdf`).
- **13 items are "unclear"** because the source cannot be fetched under the rules. These are SEC (N-PORT and BDC 10-Q), the CourtListener docket page, the iPhi tenant census, the NPT GivingPoint bundle, the Vanguard Tungsten API, the CCT donor portal and trust-center pages, plus two items that are not yet due.

**Watchlist script.** `scripts/mission_watchlist.py` was reviewed before running. Its `ct_crtsh` handler is hard-disabled and returns without any network call. The script does not read robots.txt itself, so it was run with `--only` for the 26 checks whose hosts' robots.txt allow access:

```
python3 scripts/mission_watchlist.py --date 2026-11-19 --irs-dir <scratch> --only ...
```

- **22 checks were skipped:** 10 crt.sh (disabled), 5 iPhi login pages, `http-cct-portal`, `http-fftc-portal`, `http-assetmark-login`, 3 Google News RSS and `sec-altruist`.
- **Results:**
  - 4 changed: `ct-give-certspotter`, `http-cfn-portal`, `http-rcf-portal` and `irs-fidelity`.
  - `http-ren-lpl` also showed a changed link (the Investment Policy Statement noted above).
  - `http-ws-login` failed with 403, as it did on 2026-11-14.
  - The rest were unchanged.
- **Files written:**
  - `data/watchlist-snapshots/2026-11-19/*.json` (26 snapshots)
  - `data/watchlist-snapshots/reports/2026-11-19.md`
  - 26 rows in `data/watchlist-snapshots/manifest.csv`

The IRS index cache was kept in scratch and deleted afterwards.

## Per-item results

Columns: awaited event; event happened (yes / no / unclear); what changed; source; whether a repo finding needs updating.

| item | awaited event | happened | what changed / evidence | source | repo update |
|---|---|---|---|---|---|
| P-GIV-02 | Production Give host or login-link change for Minneapolis/Thrivent/Stifel/JCF; new Ren-client slugs | no | No production-named host for TMF, Thrivent, Stifel or JCF. Certspotter shows 2 new non-production names: thriventcharitable-sandbox2.giveinteractive.com (first cert 2026-11-17) and vanguard-dr-sftp.int.giveinteractive.com (first cert 2026-11-16); 86 names in all. The TMF, Thrivent and Stifel homepages still link iPhi logins (watchlist: unchanged). crt.sh was not used. iPhi login pages were not fetched because robots.txt disallows them | https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names ; data/watchlist-snapshots/reports/2026-11-19.md | yes (data only): data/mission-2026-11-14/give-interactive-client-timeline.csv: add ct_first_certificate rows for thriventcharitable-sandbox2 (2026-11-17) and vanguard-dr-sftp.int (2026-11-16). No research sentence changes: 'Minneapolis, Thrivent, Stifel and JCF have only staging/sandbox/SFTP hosts' still holds |
| P-REN-01 | Next iPhi tenant exits (NXDOMAIN/redirect) for Minneapolis, Thrivent, Stifel, ImpactAssets, Gulf Coast CF | unclear | Census not re-run. robots.txt on *.iphiview.com and iphi.stellartechsol.com is 'User-agent: * Disallow: /', so the tenant path probe cannot run under these rules. Indirect check: the TMF, Thrivent, Stifel and ImpactAssets homepages still link their iPhi logins on 2026-11-19, so no exit is visible | data/watchlist-snapshots/reports/2026-11-19.md | no |
| P-ASR-01 | Every.org first Form 990 (CY2025) in IRS index | no | Not in the 2026 TEOS index (Last-Modified 2026-11-18; the new batch 2026_TEOS_XML_10A has 43,662 rows). The latest Every.org row is still the CY2024 990-PF (2025_TEOS_XML_10A) | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-AGF-05 | Launch of write-capable agent paths into DAF grants (Daffy, TIFIN Louise, Chariot, Endaoment, Fundraise Up) | no | Web search found no launch announcement dated after 2026-11-15. Daffy's MCP, the Chariot MCP and Fundraise Up Agentic Giving are already in agentic-philanthropy-products-2026.csv (AP03/AP05/AP07) | web search (no page fetch) | no |
| P-WAT-04 | Vanguard-Altruist close; Altruist ADV/BD or DAF-page change | no | The Altruist DAF page and the Vanguard press release are unchanged since 2026-11-14 (watchlist). Search found no report that the deal has closed; the announcement said 'later in 2026'. IAPD/BrokerCheck were not checked. SEC EFTS was not queried (robots.txt 403) | https://altruist.com/donor-advised-funds/ ; https://corporate.vanguard.com/content/corporatesite/us/en/corp/who-we-are/pressroom/press-release-vanguard-announcement-082626.html | no |
| P-LND-01 | Quarterly BDC 10-Q marks/refinancing of Bonterra unitranche | unclear | Not checked: www.sec.gov and efts.sec.gov return 403 for robots.txt to a generic User-Agent, so under the sweep rules no SEC page was fetched | https://www.sec.gov/robots.txt (403) | no |
| P-WAT-01 | GiveClear CY2025 990 (AssetMark transfer) | no | Not in the 2026 TEOS index (Last-Modified 2026-11-18; the new batch 2026_TEOS_XML_10A has 43,662 rows). GiveClear's latest return is CY2024 (2025_TEOS_XML_11B) | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-WAT-05 | ImpactAssets DAF Hub new launch date published | no | The transition page is unchanged. It still says 'transitioning to a new DAF hub on September 8, 2026' and keeps the 'Lorem ipsum' FAQ placeholder. The homepage CLIENT LOGIN still points to iphi.stellartechsol.com/calvert. The CT names impactassets.giveinteractive.com, -staging and -sandbox were already present on 2026-11-14 | https://impactassets.org/daf-platform-transition/ ; data/watchlist-snapshots/reports/2026-11-19.md | no |
| P-B30B-03 | Every.org and Givinga CY2025 returns | no | Not in the 2026 TEOS index (Last-Modified 2026-11-18; the new batch 2026_TEOS_XML_10A has 43,662 rows). Givinga's latest return is CY2024 (2025 index, batches 09A and 11A) | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-REN-02 | TY2025 990s of 56 in-scope iPhi sponsors + NCF, Catholic CF, GS Gives | yes (1 sponsor) | In batch 10A, 1 in-scope iPhi sponsor has a CY2025 990: Community Foundation of Jackson Hole (EIN 83-0308856, object 202632959349300518, 195 DAFs, $85.8m). Its top-5 Part VII-B list has no Stellar or Ren line; its CY2022-24 lists had none either. NCF, Catholic Community Foundation (LA) and GS Gives CY2025 are not indexed. Thrivent's and Stifel's CY2025 returns came in batch 09A, before the baseline, and are already in the repo | https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_10A.zip | no |
| P-VEN-02 | Vanguard Charitable Give Interactive go-live | no | No go-live seen. New CT name vanguard-dr-sftp.int.giveinteractive.com (first cert 2026-11-16), a disaster-recovery SFTP environment that is not donor-facing. client.vanguardcharitable.org still goes through the Salesforce SAML chain to mygiving (unchanged). The FY6/2026 990 is not indexed | https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names ; data/watchlist-snapshots/reports/2026-11-19.md | yes (data only): give-interactive-client-timeline.csv: add the vanguard-dr-sftp.int ct_first_certificate row (see P-GIV-02) |
| P-VCM-01 | CCT FYE 9/2026 990; vendor layer evidence | no | CCT's FY9/2026 990 is not indexed; its latest is FY9/2025 (2026_TEOS_XML_08A). cct.giveinteractive.com/config.js still carries client name cct-prod-okta. donorportal.cct.org was not fetched because robots.txt allows only /index.html | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv ; https://cct.giveinteractive.com/config.js | no |
| P-990-07 | 2027 990s of Vanguard, JCF, Thrivent, Stifel, FFTC (Give vs Ren lines) | no | Not yet due. Vanguard FY6/2026, JCF FY6/2026 and FFTC CY2025 are not indexed. Thrivent's and Stifel's CY2025 returns predate the baseline and are already harvested (Thrivent shows a Renaissance Acquisition Co line of $479,172) | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-ASR-04 | Quarterly terms-monitor run (next 2027-02) | unclear | Not run: not due until 2027-02 | - | no |
| P-AGA-06 | Quarterly trust-center re-scan | unclear | Not run: quarterly and not due. robots.txt cannot be read on trust.givechariot.com and trust.giveinteractive.com (both return HTML) or on trust.benevity.com (307), so those hosts would be skipped. trust.blackbaud.com and trust.foundant.com allow crawling | - | no |
| P-GPT-02 | New GivingPoint client codes / <brand>daf.org domains | unclear | Not checked. www.nptgivingpoint.org/robots.txt returns the app's HTML shell rather than a robots file, so it cannot be read and the bundle was not fetched. crt.sh was not used | - | no |
| P-B37A-03 | N-PORT-P marks/DDTL draws on Bonterra 2032 facility | unclear | Not checked: www.sec.gov and efts.sec.gov return 403 for robots.txt to a generic User-Agent, so under the sweep rules no SEC page was fetched | https://www.sec.gov/robots.txt (403) | no |
| P-B37A-01 | TY2025 Ren receipts (RCF, MS GIFT, USCGT, NCF, Stifel, Thrivent, AEF) | no | RCF, Morgan Stanley GIFT, US Charitable Gift Trust, NCF and AEF CY2025 are not indexed. Their CY2024 returns came in 2025 batches 11A-11D. Stifel's and Thrivent's CY2025 returns predate the baseline (09A) | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-99F-07 | 144 unmirrored FY2025 returns available / DAFRC FY2025 release | unclear | Batch 10A adds 99 returns (990/990-EZ/990-PF) from EINs in dafrc-sponsor-schedule-d-fy2019-2024.csv: 74 for CY2025, 13 for FY6/2026 and 12 others. These are not yet on the gt990datalake mirror (a sampled object returned 404). Whether they overlap the 144 was not tested. The DAFRC FY2025 release was not checked. The script was not re-run (report-only sweep) | https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_10A.zip | no |
| P-NPT-02 | GiveClear CY2025 990 Schedule D | no | Not in the 2026 TEOS index (Last-Modified 2026-11-18; the new batch 2026_TEOS_XML_10A has 43,662 rows) | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-BUY-02 | PE-owner DAF/wealth-platform links (Bain Ren+Envestnet; GTCR FS+AssetMark) | no | Foundation Source's 2026-11-18 release names only Charityvest as partner. It does not mention GTCR, AssetMark, Envestnet or CAPTRUST. No Ren/Envestnet item was found | https://www.prnewswire.com/news-releases/foundation-source-client-giving-tops-1-5-billion-as-ceo-outlines-three-trends-shaping-philanthropy-in-2027--302942977.html | no |
| P-FCG-04 | Tungsten Swagger / new vcapps.org or API Gateway hosts | unclear | Not checked. api-tungsten.vanguardcharitable.org/robots.txt returns 403. crt.sh, the source for vanguardcharitable.org CT, is disallowed | - | no |
| P-LND-05 | Foundation Source Audax unitranche marks | unclear | Not checked: www.sec.gov and efts.sec.gov return 403 for robots.txt to a generic User-Agent, so under the sweep rules no SEC page was fetched | https://www.sec.gov/robots.txt (403) | no |
| P-B37A-02 | GS DAPF CY2025 990 (post-Ayco) | no | GS DAPF (EIN 31-1774905) CY2025 is not indexed. Its latest is CY2024 (2025_TEOS_XML_11A) | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-B35A-02 | Public-support watchlist: next returns / 990-PF / foundation code | no | No new return in 10A for CF South Lake County (latest FY9/2025), Community Foundations Inc (latest CY2024), National Charitable Fund (latest CY2024) or Los Altos CF (no name match in the 2026 index). No 990-PF from any of them. The BMF was not re-checked | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-GIV-05 | Vanguard Give ledger go-live; Salesforce front end stays? | no | Same as P-VEN-02: no go-live seen, the Salesforce donor chain is unchanged and the FY6/2026 990 is not indexed | https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names | no |
| P-PRC-03 | Flipcause Ch.7: claims, avoidance actions, Stripe settlement order | unclear | Web search found no report dated after 2026-11-15 and no Stripe settlement approval order. The Epiq docket was not fetched | web search (no page fetch) | no |
| P-QA3-07 | Every.org sponsor entity / Givinga account nature | no | No new Every.org or Givinga filings indexed | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-PE-03 | Hg exit path for Benevity | no | Search found no sale or continuation-fund report. One search snippet attributes to The Logic a >US$90m employee/stakeholder stock-option sale dated 2026-10-30. That is before the baseline and was not verified; the repo already records 'US$90.1m equity issued to Dec 2025' | web search (no page fetch) | no |
| P-CMP-04 | SPLC hold reversal; DAF-to-DAF outflow shift | no | Search found no reversal reported after 2026-11-15. The outflow test needs the FY6/2026 returns of Fidelity, Vanguard and DAFgiving360, none of which is indexed | web search ; https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-VCM-03 | Recipients of Fidelity's CY2025 $727m outlier | no | Fidelity's FYE6/2026 990 is not indexed. New in 10A: an AMENDED FY6/2025 990 (object 202622879349301322, signed 2026-09-29). Its Schedule I total and Schedule D are identical to the original | https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_10A.zip (member 202622879349301322_public.xml) | no |
| P-B29C-03 | Re-run void scan (TY2024 unmirrored + TY2025; Fidelity FY2026) | no | Trigger not met: Fidelity FY2026 is not indexed and the target is 2027-Q1. 10A returns are not yet mirrored | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-PE-01 | GTCR sale/recap of Foundation Source; AssetMark/CAPTRUST cross-sell | no | The 2026-11-18 release (CEO Joseph Mrak III, 2027 outlook) has no ownership, financing or cross-sell news. It reports 20,000 DAF accounts at 2025-12-31 and, through partner Charityvest, >41,000 DAF grants totalling >$212m in 2026 to September | https://www.prnewswire.com/news-releases/foundation-source-client-giving-tops-1-5-billion-as-ceo-outlines-three-trends-shaping-philanthropy-in-2027--302942977.html | no |
| P-MOR-04 | FY2024-25 Schedule D fully processed (mortality re-run) | no | Trigger not met. 10A adds some FY2025 returns but processing is not complete | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-PE-04 | TA/Genstar sale of Orion | no | Search found no sale report | web search (no page fetch) | no |
| P-WAT-02 | ImpactAssets CY2025 990 ($160.8m NPT grant recurrence) | no | ImpactAssets CY2025 is not indexed (watchlist irs-impactassets unchanged) | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-B32C-01 | Philanthropi TY2025 990; DNS/CT changes | no (990) / unclear (web) | Philanthropi (EIN 45-5634144) CY2025 is not indexed; its latest is CY2024 (2025_TEOS_XML_11C). philanthropi.com robots.txt could not be read (proxy 502), so no fetch. crt.sh is disallowed | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-B35A-03 | GS DAPF CY2025 presentation of Ayco (rule R2) | no | GS DAPF CY2025 is not indexed | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-B35C-02 | Every.org first 990 recipient analysis | no | Every.org CY2025 is not indexed | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-CFR-05 | CCT change of layer (Give donor link; GiftingNetwork footer; check rail) | unclear | cct.giveinteractive.com/config.js is unchanged in substance (cct-prod-okta, give-cct-prod Cognito). donorportal.cct.org was not fetched: robots.txt allows only /index.html. www.cct.org was not fetched: robots.txt sits behind a Cloudflare challenge | https://cct.giveinteractive.com/config.js | no |
| P-CMP-07 | Peterson v. WaterStone status/outcome; other disputes | unclear | No ruling found. HEAD probes of RECAP storage for Docs 56-85 found only Doc 58 (already known). The CourtListener docket page was not fetched because www.courtlistener.com robots.txt has 'User-agent: * Disallow: /'. Search found no new coverage or other disputes | https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.58.0.pdf | no |
| P-B29B-02 | Ruling on MTD FAC (Doc 34) in D. Colo. 1:26-cv-00179 | unclear | No new RECAP document beyond Doc 58 (Docs 56-57 and 59-85 return 404). An unbought or sealed order cannot be ruled out. The docket page is disallowed by robots.txt | https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.58.0.pdf | no |
| P-PRC-02 | Givinga $316k bank-fraud loss: CY2025 recovery line | no | Givinga CY2025 is not indexed | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-NPO-01 | Fidelity FYE6/2026 990 (expected ~May 2027) | no | Not indexed. New: an AMENDED FY6/2025 990 (10A) that corrects an overstated capital gain attributed to unrelated business revenue. Gross UBI falls from $88,982,918 to $80,591,303; Schedule A public support moves from 83.800% to 83.803%. The amended 990-T (202642879339300829) lowers UBTI from $87,754,231 to $79,362,616 and tax from $7,032,458 to $6,361,129. Schedule D (224,884 DAFs; $85.48bn EOY) and the Schedule I total are unchanged | https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_10A.zip (member 202622879349301322_public.xml) | no: No research sentence cites the changed UBI/public-support figures (grep). Optional: rows citing original object 202601389349301700 (e.g. form990-returns-schedule-d-harvest-full.csv) could note the superseding amendment; values unchanged |
| P-B35B-01 | JCF FY6/2026 990; production JCF Give tenant | no | JCF FY6/2026 is not indexed. CT shows only jcf-grant-cart, jcf-innov, jcf-sandbox, jcf-sftp.int and jcf-staging; there is no production JCF name | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv ; https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names | no |
| P-NPO-02 | Post-SPLC DAF-to-DAF outflows (FYE6/2026-27 returns) | no | The returns are not yet filed or indexed | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-99F-01 | Resolve DAFRC imputed sponsor-years via 990 check | no | No trigger event; this item needs PDF images or audits, not new index rows. Not worked in this sweep | - | no |
| P-B36A-03 | Measured DAF balances for carry-forward cases | no | No new return in 10A for Truman Heartland, CF Snohomish County, JCF Greater Phoenix (470874376) or CF Middle Tennessee (no name match). Annual reports were not checked | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |
| P-B32B-03 | Givinga CY2025 recovery/insurance line | no | Givinga CY2025 is not indexed | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | no |

**Repo updates suggested (not made):**
1. `data/mission-2026-11-14/give-interactive-client-timeline.csv`: add two `ct_first_certificate` rows.
   - Thrivent: `thriventcharitable-sandbox2.giveinteractive.com`, 2026-11-17.
   - Vanguard Charitable: `vanguard-dr-sftp.int.giveinteractive.com`, 2026-11-16.
   - No research sentence changes. The sentences "Minneapolis, Thrivent, Stifel and JCF have only staging/sandbox/SFTP hosts" (P-GIV-02 rationale) and Vanguard "not yet live" still hold.
2. Optional: rows that cite Fidelity's original FY6/2025 object `202601389349301700` could note the superseding amendment `202622879349301322`. The Schedule D and Schedule I values cited are unchanged (P-MON19-04).

## Batch 10A coverage of tracked sponsors

The checks matched sponsor EINs and names in `index_2026.csv` against batch `2026_TEOS_XML_10A`.

**Rows in 10A for tracked EINs:** Fidelity Charitable only. Its rows are the amended FY6/2025 990 and 990-T.

**Latest 2026-index rows for the others (all from before the baseline):**
- Vanguard FY6/2025 (05A)
- DAFgiving360 FY6/2025 (05A)
- NPT FY6/2025 (05A)
- Endaoment FY6/2025 (05A)
- Goldman Sachs Charitable Gift Fund FY6/2025 (05A)
- Ayco FY6/2025 (05A)
- JCF FY6/2025 (03A)
- Goodstack US (Percent Impact Foundation) CY2025 (09A, object `202602459349300235`; already in the repo's validation registers)
- Thrivent CY2025 (09A)
- Stifel CY2025 (09A)
- CCT FY9/2025 (08A)
- CF South Lake County FY9/2025 (06A)
- WaterStone FY3/2025 (02A)
- National Charitable Fund CY2024 (02A)

**No 2026-index row at all.** Their latest returns are CY2024 in the 2025 index:
- Every.org (CY2024 990-PF, 10A)
- Givinga (09A/11A)
- PayPal Giving Fund (11C)
- Philanthropi (11C)
- GiveClear (11B)
- ImpactAssets (11B)
- GS DAPF 31-1774905 (11A)
- Morgan Stanley GIFT (11A)
- US Charitable Gift Trust (11B)
- NCF (11D)
- AEF (11D)
- Community Foundations Inc (11D)
- Truman Heartland (11A)
- CF Snohomish (11D)
- RCF CY2024 (990-T only in the 2026 index)

Last year's CY2024 returns of these sponsors came in batches 11A–11D, so the next index update(s) are the likely window (P-MON19-03).

**Sponsor-wide:** 10A holds 99 returns (990/990-EZ/990-PF) from EINs in `dafrc-sponsor-schedule-d-fy2019-2024.csv`: 74 for CY2025, 13 for FY6/2026 and 12 others. They are not yet on the gt990datalake mirror (a sampled 10A object returned 404).

## Source register

**robots.txt checks.** All were read on 2026-11-19 before any other request to the host.

| host | robots.txt result | decision |
|---|---|---|
| apps.irs.gov | 404 (no file) | fetched: index_2025.csv, index_2026.csv, HEAD on 2026_TEOS_XML_09A/10A.zip, download of 10A.zip |
| www.irs.gov | 200; disallows /search/ etc. | not needed |
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no file) | fetched 2 original XMLs (Fidelity 990 and 990-T); 1 object 404 (not mirrored) |
| api.certspotter.com | 404 (no file) | fetched (unauthenticated issuances API, via watchlist) |
| www.courtlistener.com | 200; `User-agent: * Disallow: /` | **not fetched** (docket page) |
| storage.courtlistener.com | 404 (no file) | HEAD probes on RECAP Docs 56–85 (1 s apart) |
| www.sec.gov, efts.sec.gov | 403 | **not fetched** (N-PORT, 10-Q, EFTS) |
| news.google.com | 200; `/rss/search` disallowed for * | **not fetched** (3 RSS checks) |
| impactassets.org, www.vanguardcharitable.org, client.vanguardcharitable.org, waterstone.org, www.minneapolisfoundation.org, www.thriventcharitable.com, thriventcharitable.thrivent.com, www.stifel.com, intercom.help, altruist.com, corporate.vanguard.com, www.reninc.com | 200; target paths allowed | fetched via watchlist (waterstone.org/login returned 403) |
| cfndaf.donorfirstx.com, rcf.donorfirstx.com | 404 (no file) | fetched via watchlist |
| impactassets.iphiview.com, tmf.iphiview.com, infaith.iphiview.com, sci.iphiview.com, iphi.stellartechsol.com | 200; `User-agent: * Disallow: /` | **not fetched** |
| donorportal.cct.org, daf.fftc.org | 200; `Allow: /index.html`, `Disallow: /` | **not fetched** |
| assetmarkcharitablemc.tifingive.com | 200 but HTML (not a robots file) | **not fetched** (unreadable) |
| cct.giveinteractive.com | 200; `User-agent: *` with no rules | fetched /config.js |
| www.cct.org | Cloudflare challenge | **not fetched** |
| www.federalregister.gov | 200; search pages disallowed, /api/ not | fetched the documents and public-inspection API (no key) |
| www.prnewswire.com | 200; release paths allowed | fetched 1 release (Foundation Source, 2026-11-18) |
| www.nptgivingpoint.org, trust.givechariot.com, trust.giveinteractive.com | 200 but HTML (unreadable) | **not fetched** |
| trust.benevity.com | 307 | **not fetched** |
| api-tungsten.vanguardcharitable.org | 403 | **not fetched** |
| philanthropi.com | proxy 502 | **not fetched** |
| trust.blackbaud.com, trust.foundant.com, www.foundant.com, www.daffy.org, www.givechariot.com, tifin.com | readable; allowed | not fetched (item not due, or covered by search) |

**Sources used.**
- IRS TEOS index 2026 (Last-Modified 2026-11-18): https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv
- IRS TEOS batch 10A (Last-Modified 2026-11-18, 258,857,026 bytes): https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_10A.zip
  - Members read: `202622879349301322_public.xml` (Fidelity amended 990), `202642879339300829_public.xml` (Fidelity amended 990-T) and `202632959349300518_public.xml` (CF Jackson Hole CY2025).
- IRS TEOS index 2025 (Last-Modified 2026-01-21): https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv
- Fidelity FY6/2025 original 990: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml
- Fidelity FY6/2025 original 990-T: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611359339301216_public.xml
- Certspotter, giveinteractive.com: https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names
- RECAP Peterson v. WaterStone, Doc 58 (highest found): https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.58.0.pdf
- Federal Register API, IRS, "donor advised fund", from 2026-11-01 (0 results): https://www.federalregister.gov/api/v1/documents.json?conditions[term]=donor%20advised%20fund&conditions[publication_date][gte]=2026-11-01&conditions[agencies][]=internal-revenue-service
- Foundation Source release, 2026-11-18: https://www.prnewswire.com/news-releases/foundation-source-client-giving-tops-1-5-billion-as-ceo-outlines-three-trends-shaping-philanthropy-in-2027--302942977.html
- Give Interactive tenant config: https://cct.giveinteractive.com/config.js
- Watchlist report: `data/watchlist-snapshots/reports/2026-11-19.md`

**Web search.** Queries covered Peterson v. WaterStone, IRS DAF regulations, vendor announcements (Daffy, Chariot, TIFIN Give, Foundant, Blackbaud, Ren, Benevity, Bonterra, Foundation Source), the Vanguard–Altruist close, Flipcause, the SPLC holds, the ImpactAssets DAF Hub and Give Interactive/Vanguard. They found nothing dated after 2026-11-15 bearing on a monitored event, except the Foundation Source release above and a 2026-11-05 Blackbaud bbcon London headline. That headline was seen only as a title and is not relevant to any item. Search results are leads, not facts; nothing was taken from a snippet without the date caveat noted in the table.

## Limits

- "No" means the event is absent from sources this sweep could reach. RECAP holds only purchased documents.
- The TEOS index has no submission date finer than the year, so "new since baseline" rests on batch 10A being new. Its Last-Modified date is 2026-11-18; the previous index update was 2026-10-21.
- SEC-based items cannot be monitored under a generic client (P-MON19-02).
