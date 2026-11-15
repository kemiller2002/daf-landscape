# Ren (Stellar) iPhi client attrition 2023–2026, with the PNC/Truist/UBS hosts, Foundation Cloud ledgers and Ren ACH coverage

Queue items: **P-BMG-03** (main), **P-VEN-05**, **P-BMG-02**, **P-QA2-03**. Prepared 2026-11-15. All network reads were public pages, DNS and certificate logs. There were no logins, forms or outreach. Evidence tags follow the repo convention: [F] first-party or filing, [I] inference, [V] vendor claim, [R] third-party database.

Script: [`scripts/mission_ren_iphi_attrition.py`](../../scripts/mission_ren_iphi_attrition.py). Outputs:
- [`ren-iphi-tenant-census.csv`](../../data/mission-2026-11-14/ren-iphi-tenant-census.csv) (76 rows).
- [`ren-iphi-attrition-summary.json`](../../data/mission-2026-11-14/ren-iphi-attrition-summary.json).
- [`spectrumportal-tenant-audit.csv`](../../data/mission-2026-11-14/spectrumportal-tenant-audit.csv) (16 rows).
- [`ren-charity-ach-program-evidence.csv`](../../data/mission-2026-11-14/ren-charity-ach-program-evidence.csv) (58 rows).
- [`relationship-graph-edges-additions-11.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-11.csv) (EK001–EK034).
- [`queue-proposals-ren-attrition.csv`](../../data/mission-2026-11-14/queue-proposals-ren-attrition.csv) (P-REN-01 to P-REN-05).

## 1. Findings

1. **Attrition, 2023-01 to 2026-11: 6 of 57 iPhi sponsors left (10.5%).** The 95% Wilson interval is 4.9–21.1%.
   - **Bounds.** Counting only dated exits gives a lower bound of 8.8% (5/57). Adding the 2 sponsors whose status is unknown gives 14.0% (8/57). Also treating the 3 sponsors evidenced only by TY2024 990 lines as exits gives a worst case of 19.3% (11/57).
   - **Annual rate.** Spread over the whole window, that is about 2.8% a year (3.8% at the 14.0% bound). The exits are bunched, though: 5 of the 6 happened between May 2025 and June 2026. That is a recent run-rate of roughly 8% a year [I].
   - **Exits by assets.** The six exits held $1.23bn of FY2024 DAF assets. That is 1.5% of the in-scope book ($79.7bn). NPT alone is $42.1bn of that book; excluding NPT and the two Goldman programs, the exits are 4.9%.
2. **Community foundations are where Ren loses clients: 5 of 28 left (17.9%; Wilson 7.9–35.6%).** Those five held $0.69bn, 15.0% of the $4.60bn CF DAF book on iPhi.
   - **Destinations.** Four went to Foundant CommunitySuite: Acadiana (2025-05-14 [I]), Flint (about 2026-01 [I]), Arkansas (2026-06-01 [F]) and Gulf Coast CF of Venice (in progress in 2026 [F banner]). One went to akoyaGO (Yakima, undated).
   - **Faith/affinity and national sponsors.** One exit out of 26: WaterStone moved to Give Interactive. Its legacy iPhi page says so in its own words [F].
   - **No exit lands on Foundation Cloud, DonorFirstX or Salesforce.**
3. **The census is larger than the CF vendor map showed.** It covers 61 live `*.iphiview.com` hosts plus path tenants on `www.iphiview.com` and `iphi.stellartechsol.com`. 28 tenant hosts are new to the repo.
   - **Faith and affinity foundations:** Barnabas, Christian Financial Resources, Georgia Baptist, Tennessee Baptist, Mennonite Brethren, Methodist Foundation of Mississippi, Missouri UMF, Dallas Seminary, Faithful Journey, FaithWise/Fuller, Knights of Columbus.
   - **National sponsors:** Raymond James Charitable Endowment Fund ($1.89bn), CAF America, Johnson Charitable Gift Fund, RSF.
   - **Bank and trust programs:** KeyBank, Regions, Truist/BB&T, BNY Mellon CGF, Equity Trustees (Australia).
   - **NPT white-label programs:** J.P. Morgan and ICGF.
4. **Some iPhi exits stay inside Ren.** NPT's `npt`, J.P. Morgan's `jpmc` and ICGF's `icgf` iPhi hosts now 301-redirect to Ren-hosted "GivingPoint" sites (`nptgivingpoint.org`, `jpmgiving.org`, `icgfdaf.org`). Each bundle says "offered in conjunction with National Philanthropic Trust" and links to `renpsg.atlassian.net` [F]. These are counted as **active**.
5. **P-VEN-05: none of the three bank hosts is a Ren-administered DAF.**
   - **Truist** is "F&E ClientView", a Foundations & Endowments client-reporting log-in (the BB&T alias shows the same page). It is out of scope.
   - **UBS** redirects to `donoradvisedfund.ubs.com`. UBS's DAF is NPT-sponsored [R/F]. The host sits on the legacy 67.216.67.0/24 range that also holds dead iPhi hosts, and it resets connections. It adds nothing to the Ren numerator beyond NPT.
   - **PNC**'s `/scbf` path returns 404. The program is unnamed. PNC's white-label "PNC Gifting Portal" (2021) is a candidate only.
6. **P-BMG-02:** of the 16 spectrumportal tenants, 2 are outgoing portals over Blackbaud (Tampa Bay, Winston-Salem) and 1 is grants-side (New Mexico). Two more have Blackbaud evidence (Greater Washington: 990 lines; Kalamazoo: NXT donation forms). Only Santa Barbara has an NPact (Fusion Labs) payee. 10 are unresolved. **`ledger_implied = yes` cannot stand for spectrumportal as a class.**
7. **P-QA2-03:** only **AEF** is tied to Ren's charity ACH portal on a public first-party page ("Powered by Ren … provide ACH information") [F]. RCF says only "Ren-powered technology" and "electronically or by check". No program page names the Rapid Disbursement Engine. Ren's own scale figures do not reconcile (§6).

## 2. Method

| Step | What was done | Source / rule |
|---|---|---|
| Seeds: repo | Every `*.iphiview.com` host or path and `iphi.stellartechsol.com/<path>` cited in `research/` and `data/` (35 hosts; this script's outputs excluded) | `repo_iphi_mentions` |
| Seeds: CT | crt.sh bare-domain queries for `iphiview.com`, `stellartechsol.com`, `donorfirstx.com`, `reninc.com`, `spectrumportal.net`. iPhi uses wildcard certificates (`*.iphiview.com`, DigiCert, yearly since 2011), so only 7 named iPhi hosts appear: one ZeroSSL batch on 2025-04-20 (`cafa`, `ccfnj`, `eqt`, `rj`, `ocf`, `www`, `maintenance`) | [crt.sh](https://crt.sh/?q=iphiview.com) |
| Seeds: guesses | Homepage domain stem plus two initial-letter acronyms for each of the 803 CFs in the CF map and the 1,512 sponsors in the 990 universe, plus ~200 bank, broker and Ren labels (1,888 labels) | `guess_labels` |
| DNS | `<label>.iphiview.com` A/CNAME over DoH (dns.google and cloudflare-dns.com, alternating, ≤1 request/s per resolver). There is no wildcard record: a random label gives NXDOMAIN. Of 1,891 names, 61 resolve | [dns.google](https://dns.google/resolve?name=zz-nonexistent-probe-7q.iphiview.com&type=A) |
| Path probe | `/<label>/` on the two multi-tenant hosts `www.iphiview.com` and `iphi.stellartechsol.com` for 830 labels (acronyms of non-CF sponsors plus the fixed list), ≤1 request/s per host | `path_labels` |
| HTTP | Public log-in page of each tenant. Redirects that stay on Ren/iPhi hosts are followed; external ones are recorded and the destination's DNS and bundle are read. The script extracts DotNetNuke `MetaAuthor`/`MetaCopyright`, the footer (c) year, the "Welcome to …" line and transition banners | `follow_tenant`, `dest_facts` |
| Join | CF map (current fund-login vendor), 990 Part VII-B harvest (Stellar / Ren / Renaissance payees, TY2021+), dated migration file, plus a small manual table that cites a URL for every non-CF identity | `MANUAL`, `AUTHOR_EIN`, `MANUAL_STATUS` |
| Classify | Precedence: out_of_scope → dated migration → manual status → CF map shows another vendor → banner names a new vendor → external redirect (Ren-hosted = active; legacy range or HTTP ≠ 200 = unknown; other = migrated) → NXDOMAIN or 404 = lapsed → live page with identity = active (with a banner = migrating) | `classify` |
| Rate | Unit = sponsor (EIN; tenant identity where there is no EIN). A sponsor takes the best status across its tenants. Population = US DAF/CF sponsors with an iPhi tenant or Stellar payee, with no evidence of exit before 2023. Bank reporting portals, non-US trustees, products not identified and hosts with no identity are excluded | `in_scope`, `sponsors`, `attrition_summary` |

**Hosting signal [F].**
- 60 tenant rows resolve to one AWS Global Accelerator pair (35.71.183.32 / 13.248.164.2).
- `pnc` and the GivingPoint sites sit on the `ren-workload-02` ELB.
- `af`, `lcf` and `mccf` still resolve into 67.216.67.0/24. PTR records there read `user-67-216-67-*.dbsintl.net`. None of the three answers HTTPS, and none has an identity [I: pre-AWS legacy range].

## 3. Tenant census
### 3.1 Exits (in-scope sponsors)

| Sponsor (EIN) | Type | FY2024 DAF $m | iPhi tenant | Last Ren/Stellar 990 line | Destination | Exit date | Basis |
|---|---|---|---|---|---|---|---|
| WaterStone (Christian Community Foundation Inc) (751750059) | faith_affinity_sponsor | 537 | [iphi.stellartechsol.com/ws](https://iphi.stellartechsol.com/ws/) | TY2024 STELLAR TECHNOLOGY 'COMPUTER & SOFTWARE EXPENSES' $366,469 | Give Interactive | 2025-2026 [I] | WaterStone: legacy iPhi page (iphi.stellartechsol.com/ws) says 'Your Giving Fund now lives in our new WaterStone Donor Portal at waterstone.giveinteractive.com'; Stellar  |
| Arkansas Community Foundation (521055743) | community_foundation | 350 | [arcf.iphiview.com/arcf](https://arcf.iphiview.com/arcf/) | TY2022 STELLAR TECHNOLOGY SOLUTIONS 'DATABASE PROVIDER FEES' $100,555 | Foundant CommunitySuite | 2026-06-01 | cf-vendor-migrations-2022-2026.csv: iPhi -> Foundant (complete; legacy arcf.iphiview.com login page still answers) |
| Gulf Coast Community Foundation (Venice, FL) (591052433) | community_foundation | 148 | [gccf.iphiview.com/gccf](https://gccf.iphiview.com/gccf/) | none listed | Foundant CommunitySuite | 2026 [I] (in progress) | Gulf Coast CF (Venice): CF map 2026-11-14 fund login is gulfcoastcf.fcsuite.com; legacy iPhi page: 'We're moving to a new Donor Portal experience launching soon' |
| Community Foundation of Acadiana (721493023) | community_foundation | 145 | [cfacadiana.iphiview.com/cfacadiana](https://cfacadiana.iphiview.com/cfacadiana/) | TY2024 Stellar Technology Solutions 'Software Support/Technology' $118,458 | Foundant CommunitySuite (CSuite) | 2025-05-14 | cf-vendor-migrations-2022-2026.csv: iPhi -> Foundant (complete; cfacadiana.iphiview.com no longer resolves) |
| The Community Foundation of Greater Flint (382190667) | community_foundation | 29 | [cfgf.iphiview.com/cfgf](https://cfgf.iphiview.com/cfgf/) | TY2022 STELLAR TECHNOLOGY SOLUTIONS 'TECHOLOGY SERVICES' $114,605 | Foundant CommunitySuite | 2026-01-20 | cf-vendor-migrations-2022-2026.csv: iPhi -> Foundant (in progress or just finished; cfgf.iphiview.com still live with a 'moving to a new system' banner) |
| YAKIMA VALLEY COMMUNITY FOUNDATION (200697012) | community_foundation | 18 | [yvcf.iphiview.com/yvcf](https://yvcf.iphiview.com/yvcf/) | none listed | akoyaGO (GOfund / GOdonate) | undated | cf-vendor-migrations-2022-2026.csv: iPhi -> akoyaGO (complete; the homepage still links a yvcf.iphiview.com give page, which no longer resolves) |

### 3.2 Active and unknown (in-scope sponsors)

| Sponsor (EIN) | Type | FY2024 DAF $m | Tenant | Footer (c) | Latest Ren/Stellar 990 line | Status | Note |
|---|---|---|---|---|---|---|---|
| ICGF Donor-Advised Fund (Independent Charitable Gift Fund; N (237825575) | bank_program | 42,119 | [icgf.iphiview.com/icgf](https://icgf.iphiview.com/icgf/) |  |  | active | redirects to Ren-hosted front end https://icgfdaf.org (AWS Global Accelerator pair (35.71.183.32 / 13.248.164.2); GivingPoint;renp |
| J.P. Morgan Charitable Giving Fund (NPT program) (237825575) | bank_program | 42,119 | [jpmc.iphiview.com/jpmc](https://jpmc.iphiview.com/jpmc/) |  |  | active | redirects to Ren-hosted front end https://jpmgiving.org (ren-workload-02 ELB (AWS); GivingPoint;renpsg_jira;NPT; HTTP 200) |
| National Philanthropic Trust (237825575) | national_sponsor | 42,119 | [npt.iphiview.com/npt](https://npt.iphiview.com/npt/) |  |  | active | redirects to Ren-hosted front end https://nptgivingpoint.org (ren-workload-02 ELB (AWS); GivingPoint;renpsg_jira;NPT; HTTP 200) |
| GS DONOR ADVISED PHILANTHROPY FUND (311774905) | national_sponsor | 11,843 | 990 only |  | TY2022 STELLAR TECHNOLOGY SOLUTIONS 'SOFTWARE PROVIDER' $390,398 | active | GS PWM DAF log-in gspf.goldman.com is iPhi (Stellar footer, iPhiSession cookie) on the ren-workload-02 ELB (queue-vendor-scope, va |
| Renaissance Charitable Foundation (Azzad program) (352129262) | national_sponsor | 5,634 | [rcf.iphiview.com/azzad](https://rcf.iphiview.com/azzad/) | 2013 | TY2024 Renaissance Administration L 'Administration' $19,225,546 | active |  |
| NATL CHRISTIAN CHARITABLE FDN INC (581493949) | faith_affinity_sponsor | 5,460 | 990 only |  | TY2024 STELLAR TECHNOLOGY SOLUTIONS 'SOFTWARE/CONSULTING' $2,495,829 | active | 990 payee in TY2024 (latest harvested year); no iPhi host found by DNS guess or path probe |
| ImpactAssets (262048480) | national_sponsor | 3,628 | [iphi.stellartechsol.com/calvert](https://iphi.stellartechsol.com/calvert/) | 2022 | TY2024 STELLAR TECHNOLOGY SOLUTIONS 'TECHNOLOGY SERVICES' $232,315 | active |  |
| Raymond James Charitable Endowment Fund (593652538) | national_sponsor | 1,886 | [rj.iphiview.com/rj](https://rj.iphiview.com/rj/) | 2022 |  | active |  |
| Community Foundation of Greater Memphis (581723645) | community_foundation | 694 | [cfgm.iphiview.com/cfgm](https://cfgm.iphiview.com/cfgm/) | 2026 | TY2024 STELLAR TECHNOLOGY SOLUTIONS 'SOFTWARE' $203,119 | active | homepage links tenant (CF map) |
| The Minneapolis Foundation (416029402) | community_foundation | 602 | [tmf.iphiview.com/tmf](https://tmf.iphiview.com/tmf/) | 2013 |  | active | homepage links tenant (CF map) |
| Thrivent Charitable Impact & Investing (411802412) | faith_affinity_sponsor | 594 | [infaith.iphiview.com/infaith](https://infaith.iphiview.com/infaith/) | 2025 | TY2025 RENAISSANCE ACQUISITION COMP 'TECHNOLOGY SERVICES' $479,172 | active |  |
| Saint Paul & Minnesota Foundation (416031510) | community_foundation | 581 | [spmf.iphiview.com/spmf](https://spmf.iphiview.com/spmf/) | 2013 |  | active | homepage links tenant (CF map) |
| THE GOLDMAN SACHS CHARITABLE GIFT FUND (113813663) | national_sponsor | 517 | 990 only |  | TY2024 STELLAR TECHNOLOGY SOLUTIONS 'INFORMATION TECHNOLOGY' $172,604 | active | 990 payee in TY2024 (latest harvested year); no iPhi host found by DNS guess or path probe |
| Stifel Charitable (842049692) | national_sponsor | 494 | [sci.iphiview.com/sci](https://sci.iphiview.com/sci/) | 2026 | TY2025 RENAISSANCE 'OPS SYSTEM & SERVICE' $801,302 | active |  |
| The Cleveland Foundation (340714588) | community_foundation | 489 | [www.iphiview.com/tcf](https://www.iphiview.com/tcf/) | 2014 | TY2024 STELLAR TECHNOLOGY SOLUTIONS 'HOSTING & CUSTOMIZATIONS - S' $416,391 | active | homepage links tenant (CF map) |
| Community Foundation of Louisville (310997017) | community_foundation | 469 | [cfl.iphiview.com/cfl](https://cfl.iphiview.com/cfl/) | 2013 |  | active | homepage links tenant (CF map) |
| CAFAmerica (431634280) | national_sponsor | 441 | [cafa.iphiview.com/cafa](https://cafa.iphiview.com/cafa/) | 2020 |  | active |  |
| Community Foundation of Greater Des Moines (426139033) | community_foundation | 375 | [dmf.iphiview.com/dmf](https://dmf.iphiview.com/dmf/) | 2013 | TY2024 REN TECHNOLOGY SERVICES 'SOFTWARE SERVICES' $203,595 | active | homepage links tenant (CF map) |
| Johnson Charitable Gift Fund (300233491) | national_sponsor | 327 | [jcgf.iphiview.com/jcgf](https://jcgf.iphiview.com/jcgf/) | 2020 |  | active |  |
| Sioux Falls Area Community Foundation (311748533) | community_foundation | 202 | [sfacf.iphiview.com/sfacf](https://sfacf.iphiview.com/sfacf/) | 2013 |  | active | homepage links tenant (CF map) |
| Knights of Columbus Charitable Fund Inc (815466677) | faith_affinity_sponsor | 131 | [ccfnj.iphiview.com/kofc](https://ccfnj.iphiview.com/kofc/) | 2013 |  | active |  |
| Baton Rouge Area Foundation (726030391) | community_foundation | 99 | [www.iphiview.com/braf](https://www.iphiview.com/braf/) |  | TY2022 STELLAR TECHNOLOGY SOLUTIONS 'IT SOFTWARE PROVIDER' $125,927 | active | homepage links tenant (CF map) |
| Innovia Foundation (910941053) | community_foundation | 78 | [innovia.iphiview.com/innovia](https://innovia.iphiview.com/innovia/) | 2020 |  | active | homepage links tenant (CF map) |
| The Greater Green Bay Community Foundation (391699966) | community_foundation | 63 | [ggbcf.iphiview.com/ggbcf](https://ggbcf.iphiview.com/ggbcf/) | 2022 | TY2024 STELLAR TECHNOLOGY SOLUT 'ERP SYSTEM PROVIDER' $185,735 | active | homepage links tenant (CF map) |
| Central Valley Community Foundation (770478025) | community_foundation | 56 | [cvcf.iphiview.com/cvcf](https://cvcf.iphiview.com/cvcf/) | 2013 |  | active | homepage links tenant (CF map) |
| Community Foundation of Jackson Hole (830308856) | community_foundation | 48 | [cfjh.iphiview.com/cfjh](https://cfjh.iphiview.com/cfjh/) | 2013 |  | active | homepage links tenant (CF map) |
| CATHOLIC COMMUNITY FOUNDATION (383941057) | faith_affinity_sponsor | 41 | 990 only |  | TY2024 STELLAR TECHNOLOGY SOLUTIONS 'PAYMENT PROCESSING' $311,878 | active | 990 payee in TY2024 (latest harvested year); no iPhi host found by DNS guess or path probe |
| Stanislaus Community Foundation (680483054) | community_foundation | 34 | [scf.iphiview.com/scf](https://scf.iphiview.com/scf/) | 2022 |  | active | homepage links tenant (CF map) |
| RSF Social Finance (136082763) | national_sponsor | 33 | [rsf.iphiview.com/rsf](https://rsf.iphiview.com/rsf/) | 2024 | TY2023 STELLAR TECHNOLOGY SOLUTIONS 'IT SERVICES' $107,760 | active |  |
| Southwest Florida Community Foundation (596580974) | community_foundation | 27 | [swfla.iphiview.com/swfla](https://swfla.iphiview.com/swfla/) | 2024 | TY2021 STELLAR TECHNOLOGY SOLUTIONS 'TECHNOLOGY SVCS' $110,707 | active | homepage links tenant (CF map) |
| Colorado Gives Foundation (510157964) | community_foundation | 23 | [cgf.iphiview.com/cgf](https://cgf.iphiview.com/cgf/) | 2024 |  | active | homepage links tenant (CF map) |
| Dallas Seminary Foundation (752188543) | faith_affinity_sponsor | 19 | [dsf.iphiview.com/dsf](https://dsf.iphiview.com/dsf/) | 2015 |  | active |  |
| Warren County Community Foundation (251380549) | community_foundation | 16 | [wccf.iphiview.com/wccf](https://wccf.iphiview.com/wccf/) | 2026 |  | active |  |
| Marion Community Foundation (314446189) | community_foundation | 15 | [mcf.iphiview.com/mcf](https://mcf.iphiview.com/mcf/) | 2012 |  | active | homepage links tenant (CF map) |
| Community Foundation of Washington County MD, Inc. (522001455) | community_foundation | 13 | [cfwc.iphiview.com/cfwc](https://cfwc.iphiview.com/cfwc/) | 2016 |  | active | homepage links tenant (CF map) |
| Northshore Community Foundation (611517784) | community_foundation | 12 | [braf.iphiview.com/nscf](https://braf.iphiview.com/nscf/) |  |  | active | homepage links tenant (CF map) |
| Faithful Journey Foundation (863667928) | faith_affinity_sponsor | 11 | [fjf.iphiview.com/fjf](https://fjf.iphiview.com/fjf/) | 2025 |  | active |  |
| FaithWise Advisors (tff -> fuller tenant) [EIN The Fuller Fo (954124436) | faith_affinity_sponsor | 9 | [fuller.iphiview.com/fuller](https://fuller.iphiview.com/fuller/) | 2026 |  | active |  |
| The Community Foundation for San Benito County (770312582) | community_foundation | 6 | [cfsbc.iphiview.com/cfsbc](https://cfsbc.iphiview.com/cfsbc/) | 2022 |  | active | homepage links tenant (CF map) |
| THE COMMUNITY FOUNDATION FOR ... (DAFRC truncated name, EIN  (275098203) | community_foundation | 4 | [rb.iphiview.com/rb](https://rb.iphiview.com/rb/) | 2013 |  | active | homepage links tenant (CF map) |
| Palm Health Foundation (592391119) | single_issue_charity | 2 | [phf.iphiview.com/phf](https://phf.iphiview.com/phf/) | 2013 |  | active |  |
| Fort Atkinson Community Foundation (396220899) | community_foundation | 2 | [facf.iphiview.com/facf](https://facf.iphiview.com/facf/) | 2023 |  | active | homepage links tenant (CF map) |
| The Methodist Foundation of Mississippi (640507167) | faith_affinity_sponsor | 2 | [mfm.iphiview.com/mfm](https://mfm.iphiview.com/mfm/) | 2013 |  | active |  |
| The Catholic Foundation of Central Florida [EIN by truncated (260879378) | faith_affinity_sponsor | 1 | [cfcf.iphiview.com/cfcf](https://cfcf.iphiview.com/cfcf/) | 2019 |  | active |  |
| Missouri United Methodist Foundation (430899770) | faith_affinity_sponsor | 0 | [mumf.iphiview.com/mumf](https://mumf.iphiview.com/mumf/) | 2013 |  | active |  |
| Barnabas Foundation (no EIN) | faith_affinity_sponsor |  | [bf.iphiview.com/bf](https://bf.iphiview.com/bf/) | 2011 |  | active |  |
| Christian Financial Resources (no EIN) | faith_affinity_sponsor |  | [cfr.iphiview.com/cfr](https://cfr.iphiview.com/cfr/) | 2020 |  | active |  |
| Georgia Baptist Foundation (no EIN) | faith_affinity_sponsor |  | [gbf.iphiview.com/gbf](https://gbf.iphiview.com/gbf/) | 2021 |  | active |  |
| Mennonite Brethren Foundation (no EIN) | faith_affinity_sponsor |  | [mbf.iphiview.com/mbf](https://mbf.iphiview.com/mbf/) | 2020 |  | active |  |
| Tennessee Baptist Foundation (no EIN) | faith_affinity_sponsor |  | [tbf.iphiview.com/tbf](https://tbf.iphiview.com/tbf/) | 2013 |  | active |  |
| Community Foundation of Teton Valley (no EIN) | community_foundation |  | [tvcf.iphiview.com/tvcf](https://tvcf.iphiview.com/tvcf/) | 2013 |  | active |  |
| UBS Donor Advised Fund (NPT-sponsored) [I] (237825575) | bank_program | 42,119 | [iphi.stellartechsol.com/ubs](https://iphi.stellartechsol.com/ubs/) |  |  | unknown | redirects to https://donoradvisedfund.ubs.com/ubs on the legacy 67.216.67.0/24 (dbsintl.net) range; no HTTPS answer on 2026-11-15 |
| UBS Donor Advised Fund (NPT-sponsored) [I] (237825575) | bank_program | 42,119 | [ubs.iphiview.com/ubs](https://ubs.iphiview.com/ubs/) |  |  | unknown | redirects to https://donoradvisedfund.ubs.com/ubs/ on the legacy 67.216.67.0/24 (dbsintl.net) range; no HTTPS answer on 2026-11-15 |
| THE AYCO CHARITABLE FOUNDATION (141782466) | national_sponsor | 1,383 | 990 only |  | TY2023 STELLAR TECHNOLOGY SOLUTIONS 'SOFTWARE PROVIDER' $336,481 | unknown | last Ren/Stellar 990 line TY2023; later absence is weak (top-5 > $100k listing rule) |
| BNY Mellon Charitable Gift Fund (300748315) | bank_program | 5 | [bnym.iphiview.com/bnym](https://bnym.iphiview.com/bnym/) |  |  | unknown | redirects to https://BNYMellonCharitableGiftFund.org/bnym/, which resolves to Ren/iPhi hosting (AWS Global Accelerator pair (35.71 |

### 3.3 Program-level moves, out-of-scope and unidentified hosts

| Host | Identity | Status | Reason |
|---|---|---|---|
| [impactassets.iphiview.com/impactassets](https://impactassets.iphiview.com/impactassets/) | ImpactAssets | lapsed | iPhi tenant path returns HTTP 404 on 2026-11-15 |
| [impactassets.iphiview.com/assetmark](https://impactassets.iphiview.com/assetmark/) | ImpactAssets (AssetMark program) | migrated | iPhi path now 301-redirects to https://assetmarkcharitablemc.tifingive.com:443/login (other: d14zkyumas3s29.cloudfront.net) |
| 990-only:311709466 | T ROWE PRICE PROGRAM FOR CHARITABLE | active | 990 payee in TY2024 (latest harvested year); no iPhi host found by DNS guess or path probe |
| 990-only:910575950 | JEWISH FEDERATION OF GREATER SEATTLE | active | 990 payee in TY2024 (latest harvested year); no iPhi host found by DNS guess or path probe |
| [keybank.iphiview.com/keybank](https://keybank.iphiview.com/keybank/) | KeyBank (client log-in; product not stated) | active | live iPhi login page with sponsor identity; no homepage link recorded in CF map |
| [ocf.iphiview.com/ocf](https://ocf.iphiview.com/ocf/) | (none) | lapsed | iPhi host NXDOMAIN 2026-11-15 and no destination evidenced |
| [pnc.iphiview.com/scbf](https://pnc.iphiview.com/scbf/) | PNC (path /scbf; program unnamed) | lapsed | iPhi tenant path returns HTTP 404 on 2026-11-15 |
| 990-only:237174183 | JEWISH COMMUNAL FUND | migrated | JCF 990 TY2022 pays Renaissance Acquisition Co for 'PREVIOUS DONOR PORTAL SUPPORT' $417,742, i.e. the Ren/iPhi portal was already the previous system; |
| [bbt.iphiview.com/bbt](https://bbt.iphiview.com/bbt/) | Truist Financial Corporation (BB&T legacy alias; F&E ClientView) | out_of_scope | Not a US DAF/CF donor portal (trust/foundation client reporting or non-US trustee) |
| [eqt.iphiview.com/eqt](https://eqt.iphiview.com/eqt/) | Equity Trustees (Australia) | out_of_scope | Not a US DAF/CF donor portal (trust/foundation client reporting or non-US trustee) |
| [truist.iphiview.com/truist](https://truist.iphiview.com/truist/) | Truist Financial Corporation (F&E ClientView) | out_of_scope | Not a US DAF/CF donor portal (trust/foundation client reporting or non-US trustee) |
| 990-only:362167761 | Jewish Federation of Metropolitan | unknown | last Ren/Stellar 990 line TY2021; later absence is weak (top-5 > $100k listing rule) |
| [af.iphiview.com/af](https://af.iphiview.com/af/) | (none) | unknown | host resolves to legacy 67.216.67.0/24 (dbsintl.net) range and gives no HTTPS answer; no identity |
| [lcf.iphiview.com/lcf](https://lcf.iphiview.com/lcf/) | (none) | unknown | host resolves to legacy 67.216.67.0/24 (dbsintl.net) range and gives no HTTPS answer; no identity |
| [mccf.iphiview.com/mccf](https://mccf.iphiview.com/mccf/) | (none) | unknown | host resolves to legacy 67.216.67.0/24 (dbsintl.net) range and gives no HTTPS answer; no identity |

### 3.4 Rate table

| Measure | Value |
|---|---|
| Population (sponsors) | 57 (CF 28, faith/affinity 16, national 10, bank program 2, single-issue 1) |
| Exits (migrated + lapsed) | 6 → **10.5%** (Wilson 95%: 4.9–21.1%) |
| Lower bound (dated exits, 2023–2026) | 5 → 8.8% |
| Upper bound (+ unknown: BNY Mellon CGF, Ayco) | 8 → 14.0% |
| Worst case (+ sponsors evidenced only by TY2024 990 lines: NCF, Catholic Community Foundation, GS Gives) | 11 → 19.3% |
| Annualised over 3.9 years | 2.8% (point) – 3.8% (14.0% bound) |
| CF only | 5/28 = 17.9% (Wilson 7.9–35.6%); $0.69bn of $4.60bn CF DAF assets (15.0%) |
| Exit DAF assets | $1.23bn: 1.5% of $79.7bn; 4.9% excluding NPT, GS PWM and GS Gives |
| Destinations | Foundant 4, Give Interactive 1, akoyaGO 1 |
| Program-level moves inside active sponsors | ImpactAssets' AssetMark program: iPhi path → TIFIN Give. ImpactAssets' main log-in moved paths (now `iphi.stellartechsol.com/calvert`) and is still on iPhi. NPT, JPM and ICGF: iPhi → Ren GivingPoint (not attrition) |
| Exit before the window (excluded) | Jewish Communal Fund: TY2022 990 pays Renaissance Acquisition for "PREVIOUS DONOR PORTAL SUPPORT" ($417,742) |

**Reading [I].**
- **Ren's iPhi book is losing its community-foundation tail faster than its affinity and bank core.** That core includes several large non-CF tenants that are visibly preparing to leave: Give Interactive staging tenants exist for Minneapolis, Thrivent, Stifel and ImpactAssets (queue-vendor-scope report).
- **Within-Ren moves mask CT/DNS signals.** NPT-family programs leave iPhi hosts for Ren's GivingPoint, so a host that redirects away is not by itself an exit.
- **Stale legacy pages persist after a switch.** Arkansas, Flint, Gulf Coast and WaterStone still answer on iPhi. A live iPhi page is therefore weak evidence of a current client unless the sponsor's homepage links it. The CF map records that link for 21 of the 23 active CFs.
- **The 990 trail is thin.** Only 20 of the 57 sponsors show a Ren or Stellar payee line, because of the "top 5 above $100k" rule. Fees for most small tenants are under that threshold.

## 4. P-VEN-05: PNC, Truist, UBS (and other bank hosts)

| Host | What answers on 2026-11-15 | Sponsor / operator | Verdict |
|---|---|---|---|
| [truist.iphiview.com/truist](https://truist.iphiview.com/truist/) and [bbt.iphiview.com/bbt](https://bbt.iphiview.com/bbt/) | "Welcome to F&E ClientView"; MetaAuthor "Truist Financial Corporation"; (c)2021; trust and brokerage affiliate disclosures | Truist Foundations & Endowments client reporting, on iPhi [F] | **Not a DAF.** Out of scope; upgrades EA027 to confirmed (EK021) |
| [ubs.iphiview.com](https://ubs.iphiview.com/) and [iphi.stellartechsol.com/ubs](https://iphi.stellartechsol.com/ubs/) | 301 → `donoradvisedfund.ubs.com/ubs`, which resolves to 67.216.67.101 (dbsintl.net legacy range) and resets the connection | UBS Donor-Advised Fund. Sponsor: NPT (2008 launch with NPT, [wealthmanagement.com](https://www.wealthmanagement.com/financial-planning/ubs-wealth-management-and-the-national-philanthropic-trust-launch-the-first-ubs-donor-advised-fund) [R]; NPT funding instructions route securities through UBS Financial Services, [nptrust.org](https://www.nptrust.org/funding-and-transfer-instructions-npt/)). NPT's own `/ubsdaf/` page now returns 404 | **Inside NPT** (EIN 23-7825575). Adds no separate Ren numerator; live status unknown |
| [pnc.iphiview.com](https://pnc.iphiview.com/) | 301 → `/scbf` → IIS 404; host on the `ren-workload-02` ELB | Unnamed. Candidate [I]: a nonprofit client of the PNC Gifting Portal, a white-label DAF platform PNC Institutional Asset Management launched on 2021-03-08 for nonprofits sponsoring DAFs ([PNC release](https://pnc.mediaroom.com/2021-03-08-PNC-Institutional-Asset-Management-Launches-PNC-Gifting-Portal)). No acronym "SCBF" matches any of the 1,512 sponsors | **Unresolved; tenant path dead** (P-REN-04) |
| [jpmc.iphiview.com/jpmc](https://jpmc.iphiview.com/jpmc/) | 301 → [jpmgiving.org](https://jpmgiving.org/) (ren-workload-02) | J.P. Morgan Charitable Giving Fund, "offered in conjunction with National Philanthropic Trust" | Active; NPT program on Ren GivingPoint (EK023–EK024) |
| [icgf.iphiview.com/icgf](https://icgf.iphiview.com/icgf/) | 301 → [icgfdaf.org](https://icgfdaf.org/) (iPhi IPs) | ICGF (Independent Charitable Gift Fund) DAF, NPT program | Active; NPT program (EK025–EK026) |
| [bnym.iphiview.com/bnym](https://bnym.iphiview.com/bnym/) | 301 → BNYMellonCharitableGiftFund.org (iPhi IPs) → HTTP 502 | BNY Mellon Charitable Gift Fund, EIN 30-0748315 ($4.7m) | Unknown (EK022 inferred) |
| [keybank.iphiview.com/keybank](https://keybank.iphiview.com/keybank/) | Generic "Client Log In"; (c)2021 KeyCorp | KeyBank; product not stated | Out of scope (inferred, EK018) |
| [rb.iphiview.com/rb](https://rb.iphiview.com/rb/) | "Welcome to Regions … Go to my Fund → Donor Dashboard" | Regions Bank tenant, linked as the fund log-in of a small CF (EIN 27-5098203) | Active (counted under that CF) |

**990 evidence.** The 990 harvest shows PNC, Truist and UBS only as investment managers or custodians (for example Akron CF, Kalamazoo CF, Pittsburgh Foundation, Permian Basin). One harvested filer, American Online Giving Foundation, paid "PNC BANK – ADMINISTRATIVE SVCS" ($196k TY2021, $149k TY2022). That shows PNC acting as an administrator for a DAF sponsor, but nothing ties it to iPhi.

## 5. P-BMG-02: spectrumportal.net (Foundation Cloud) tenants

Every tenant serves the same Angular sign-in shell, titled "Foundation Cloud Community Portal". It loads Blackbaud's `bbCheckout` payment script and calls `api.spectrumportal.net/SpectrumWeb2API`. Because the shell is identical, an HTTP 200 does not prove a tenant is in use: Winston-Salem's outgoing portal still returns 200. Tenant-level ledger evidence must come from the CF's own site or 990s.

| CF (EIN) | FY2024 DAF $m | spectrumportal host | Sign-in page | Homepage markers | 990 ledger-vendor lines (TY2021+) | Portal role | Ledger reading | ledger_implied (revised) |
|---|---|---|---|---|---|---|---|---|
| THE SAN DIEGO FOUNDATION (952942582) | 708 | [sdfoundation.spectrumportal.net](https://sdfoundation.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| TULSA COMMUNITY FOUNDATION (731554474) | 694 | [tcf.spectrumportal.net](https://tcf.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| COMMUNITY FOUNDATION OF TAMPA BAY INC (593001853) | 590 | [cftampabay.spectrumportal.net](https://cftampabay.spectrumportal.net/accounts/signin) | 404 Not Found | bbox.blackbaudhosting.com;fcsuite | none > $100k | outgoing portal (migrated) | Blackbaud (before migration) -> Foundant | no (portal over Blackbaud) |
| Greater Washington Community Foundation (237343119) | 403 | [thecommunityfoundation.spectrumportal.net](https://thecommunityfoundation.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | TY2024 BLACKBAUD $151,433 | TY2022 Blackbaud $177,444 | fund portal (sign-in SPA served) | Blackbaud (payee) [I] | no (portal over Blackbaud) |
| The Winston-Salem Foundation (566037615) | 357 | [wsfoundation.spectrumportal.net](https://wsfoundation.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | Foundant TY2024 $187,344 | outgoing portal (migrated) | Blackbaud (before migration) -> Foundant | no (portal over Blackbaud) |
| SANTA BARBARA FOUNDATION (951866094) | 152 | [donorportal-sbfoundation.spectrumportal.net](https://donorportal-sbfoundation.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | TY2024 FUSION LABS INC 'HOSTED INFRASTRUCTURE' $130,000 | fund portal (sign-in SPA served) | NPact (Fusion Labs payee) [I] | yes [I] |
| NEVADA COMMUNITY FOUNDATION INC (880241420) | 140 | [nevadacf.spectrumportal.net](https://nevadacf.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| KALAMAZOO COMMUNITY FOUNDATION (383333202) | 78 | [kalfound.spectrumportal.net](https://kalfound.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | host.nxt.blackbaud.com | none > $100k | fund portal (sign-in SPA served) | Blackbaud RE NXT (homepage uses Blackbaud NXT/BBOX donation forms) [I] | no (portal over Blackbaud) |
| AMARILLO AREA FOUNDATION INC (750978220) | 48 | [aaf.spectrumportal.net](https://aaf.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| MONTANA COMMUNITY FOUNDATION INC (810450150) | 47 | [mtcf.spectrumportal.net](https://mtcf.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| COMMUNITY FOUNDATION OF THE EASTERN SHOR (521326014) | 29 | [cfes.spectrumportal.net](https://cfes.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| THE COMMUNITY FOUNDATION OF FREDERICK (521488711) | 21 | [frederickcountygives.spectrumportal.net](https://frederickcountygives.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| DOOR COUNTY COMMUNITY FOUNDATION INC (391980685) | 17 | [doorcountycommunityfoundation.spectrumportal.net](https://doorcountycommunityfoundation.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| NORTHWEST MINNESOTA FOUNDATION (411556013) | 9 | [nwmf.spectrumportal.net](https://nwmf.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| INITIATIVE FOUNDATION (363451562) | 6 | [ifound.spectrumportal.net](https://ifound.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | - | none > $100k | fund portal (sign-in SPA served) | unknown (no 990 ledger payee > $100k) | unknown |
| NEW MEXICO COMMUNITY FOUNDATION (850311210) | 5 | [nmcf.spectrumportal.net](https://nmcf.spectrumportal.net/accounts/signin) | 200 Foundation Cloud Community Portal | fcsuite | none > $100k | partner/grantee portal | not a fund ledger front end | no |

**Reading [I].**
- **Blackbaud evidence (4 of 15 fund-side tenants).** Tampa Bay and Winston-Salem (outgoing portals), Greater Washington (Blackbaud 990 payee) and Kalamazoo (homepage donate button posts to `host.nxt.blackbaud.com`) all point to a Blackbaud CRM or ledger behind the portal.
- **NPact evidence (1 tenant).** Only Santa Barbara has a Fusion Labs "hosted infrastructure" payee, i.e. NPact.
- **Platform-level signal.** Every tenant loads `bbCheckout`. Together with the four cases above, this supports a reading that Foundation Cloud is often a portal over Blackbaud Raiser's Edge or Financial Edge, not a ledger of its own.
- **Recommendation.** Set `ledger_implied` for spectrumportal rows to `unknown` by default and to `no` where Blackbaud is evidenced. Count the Foundation Cloud ledger share only where NPact is evidenced: Santa Barbara alone, about $0.15bn.
- **Owner.** Who owns Foundation Cloud itself is still [R] only, as the wave-7 correction requires. No tenant page names NPact.
- **Not used.** `Main/settings.js` on the tenant sites exposes an Azure App Configuration connection string. It was not used and is not reproduced here.

## 6. P-QA2-03: which Ren-administered programs pay through Ren ACH / the RDE

| Program | Public charity-facing evidence | Verdict |
|---|---|---|
| American Endowment Foundation | "Our Charity Portal is now live. Powered by Ren, charities can claim their organization, provide ACH information, and prepare to manage upcoming Grant Letters." Grant checks carry a QR code "after the launch in Q2 2026" ([AEF charities](https://www.aefonline.org/charities/), modified 2026-04-20) [F] | **Yes: Ren for Charities ACH.** Checks are still issued, with a portal hook |
| Renaissance Charitable Foundation | Grant timing depends on "whether funds are delivered electronically or by check"; "the grant experience is supported by Ren-powered technology" ([RCF FAQ](https://renaissancecharitable.org/faqs/), modified 2026-01-21) [F] | **Probable** [I]. Electronic delivery on Ren technology; RDE and Ren for Charities are not named |
| MS GIFT | Brochure claims "Rapid disbursement technology with ACH granting capabilities" ([brochure](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf)) [V]; administration paid to RenPSG ($14.93m CY2024) | **Probable** [I]; not named on a charity page |
| BofA CGF | The current guides describe check fields only (queue-community-foundation-rails §5) | **No evidence** |
| Edward Jones Charitable Gift Fund | Candidate page returned 404 on 2026-11-15 | **Not established** |
| iPhi community foundations | SPMF uses Chariot; Louisville pays by check (repo) | **No** (iPhi web is not the RDE) |

**Ren's own figures.** Ren's help centre and payments page name no programs. The [overview](https://intercom.help/rengiving/en/articles/6229556-ren-for-charities-overview) (2026-07-08) says charities can "enroll in ACH grants from 25+ donor-advised fund programs at once". Release notes refer to an "ACH ID for RDE ACH" ([2024-10](https://intercom.help/rengiving/en/articles/10073077-2024-october-release)), 1-to-1 grants by "checks or ACH" ([2025-04](https://intercom.help/rengiving/en/articles/11080449-2025-april-release)), and donor "ACH request" emails ([2026-11](https://intercom.help/rengiving/en/articles/17828016-2026-november-release)).

**The metrics do not reconcile.**

| Source | Figures |
|---|---|
| [Ren payments page](https://www.reninc.com/payments/) (2026-11-04) | "1.7M Grants Processed Annually"; "1.8M+ Charities who can access Ren grants"; "$48K Granted to charities per second"; "400%+ Annual growth rate in grants sent via ACH" [V] |
| [RDE launch release](https://www.prnewswire.com/news-releases/ren-debuts-rapid-disbursement-engine-expanding-philanthropic-services-to-meet-rapid-daf-growth-301999647.html) (2023-11-28) | "more than 100,000" grants in the first eleven months of 2023 [V] |

- **$48K per second** is about $1.5tn a year on a calendar basis, or about $0.35tn counting only business hours. Both exceed all US DAF grantmaking (about $55bn). It cannot be an annual run-rate [I].
- **1.7M grants a year** fits only as all grants across all Ren-administered programs (RCF, AEF, MS GIFT and others), not RDE-ACH grants.
- **Reconciling the two.** The 2023 RDE figure (>100k) and the 400% ACH growth claim fit together only if RDE carries a minority of Ren's grants [I].

## 7. Limitations

- **Guess coverage.** DNS and path discovery find only labels that were guessed. Tenants with labels unrelated to the sponsor's name or domain are missed. The CF map, which found tenants by homepage links, adds no iPhi tenant the sweep missed, but non-CF tenants could still be missing.
- **"Active" means the log-in still answers, not that it is used.** Legacy pages persist. For non-CF sponsors with no homepage check, "active" is an upper reading.
- **Exit dates.** Two are inferred from rules (Acadiana, Flint), one is "in progress" (Gulf Coast), one is "2025–2026" (WaterStone) and one is undated (Yakima).
- **990 listing threshold.** Part VII-B lists only the top five contractors above $100k. TY2025 returns are not yet harvested (P-REN-02).
- **EIN matches.** Matches for Catholic Foundation of Central Florida, FaithWise/Fuller, Palm Health and Warren County are inferred and flagged in `ein_basis`. Six faith foundations and Teton Valley are not in the 990 universe and have no EIN or asset figure.
- **Assets.** Assets are DAFRC FY2024. NPT ($42.1bn) is counted once, and its full book is not all on iPhi.
- **Point in time and reproducibility.** Everything was read on 2026-11-15. The spectrum task uses the system resolver and is not cached; everything else replays from cache.

## 8. Data dictionary: `ren-iphi-tenant-census.csv`

| Column | Meaning |
|---|---|
| `tenant_key` | `host/path` of the iPhi portal instance, or `990-only:<EIN>` for a Ren/Stellar payee with no tenant found |
| `sponsor_key` | Unit used for the rate: EIN, else `org:<identity>` |
| `host`, `path`, `label` | Tenant host, DNN portal path and subdomain label |
| `product` | `Ren (Stellar) iPhi`, `iPhi F&E ClientView (trust reporting)`, `Ren GivingPoint front end (NPT white label)`, or a `[990 payee]` variant |
| `org` | Sponsor name (manual table, MetaAuthor or DAFRC name) |
| `org_identity_meta_author` | DotNetNuke `MetaAuthor` of the log-in page |
| `org_type` | `community_foundation`, `faith_affinity_sponsor`, `national_sponsor`, `single_issue_charity`, `bank_program`, `bank_platform`, `bank_trust_reporting`, `non_us_trustee` |
| `ein`, `eins_all`, `ein_basis` | Primary EIN, all EINs tied to the tenant (for example a CF using another CF's tenant), and how the EIN was matched |
| `fy2024_daf_assets_usd` | DAFRC FY2024 end-of-year DAF assets |
| `discovery` | `repo`, `ct`, `dns_guess`, `path_probe`, `cf_map_link`, `990_harvest` |
| `dns_status`, `dns_cname`, `dns_a`, `hosting`, `dns_evidence_url` | DoH result on 2026-11-15 and hosting class |
| `root_status`, `root_location` | HTTP status and Location of `https://<host>/` |
| `tenant_url`, `tenant_status`, `tenant_final_url` | Tenant log-in URL; status after following redirects that stay on Ren/iPhi hosts; final URL if different |
| `external_redirect`, `redirect_dest_*` | Off-iPhi redirect target and its hosting, HTTP status, bundle markers (GivingPoint, renpsg Jira, NPT), program name and whether it is on Ren IPs |
| `copyright_meta`, `footer_year`, `welcome_text`, `banner`, `iphi_markers` | Page facts: meta copyright, latest (c) year, "Welcome to …" line, transition banner, iPhi technical markers |
| `ct_named_first`, `ct_named_last`, `ct_named_count` | Named-host certificate dates on crt.sh (blank = wildcard only) |
| `map_portal_vendor`, `map_portal_url`, `map_links_tenant`, `map_conflicting_signals` | CF vendor map join (2026-11-14) |
| `ren_990_lines`, `ren_990_last_ty` | Stellar / Ren / Renaissance Part VII-B lines, TY2021+ |
| `migration_event` | Event date from `cf-vendor-migrations-2022-2026.csv`, if any |
| `status` | `active`, `migrating`, `migrated`, `lapsed`, `unknown`, `out_of_scope` |
| `destination_vendor`, `exit_date`, `status_basis` | Where the sponsor went, when, and the rule or evidence |
| `in_attrition_scope` | `yes` if the row counts toward the sponsor population (§2) |
| `manual_note`, `manual_src` | Manual-table note and its URL |
| `retrieved` | 2026-11-15 |

**Companion files.**
- `ren-iphi-attrition-summary.json` holds the rates, bounds, lists, CT ranges and hosting counts.
- `spectrumportal-tenant-audit.csv` has one row per Foundation Cloud host. Its columns cover DNS, sign-in status, homepage markers, Blackbaud / NPact / Foundant 990 lines, migration event, `portal_role`, `ledger_reading` and `ledger_implied_revised`.
- `ren-charity-ach-program-evidence.csv` has one row per (page, keyword, program) match. Its columns are page owner, URL, HTTP status, page update date, program, keyword and snippet.

**To reproduce:** `python3 scripts/mission_ren_iphi_attrition.py --cache-dir <dir> --fetch --task all` makes network calls. A full first run takes about 50 minutes at ≤1 request/s per host. Without `--fetch`, the script replays from the cache.

## 9. Graph edges and queue proposals

- **Edges.** EK001–EK034 are in [`relationship-graph-edges-additions-11.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-11.csv).
  - **New iPhi tenant edges:** EK001–EK020.
  - **Truist F&E ClientView (upgrades EA027):** EK021.
  - **BNY Mellon CGF (inferred):** EK022.
  - **NPT GivingPoint programs:** EK023–EK026.
  - **WaterStone:** EK027–EK028.
  - **Gulf Coast:** EK029.
  - **AssetMark → TIFIN Give:** EK030, upgrading EA032.
  - **ImpactAssets still on iPhi:** EK031.
  - **Blackbaud at Kalamazoo:** EK032.
  - **RCF and AEF payment rails:** EK033–EK034.
- **Proposals.** P-REN-01 to P-REN-05 are in [`queue-proposals-ren-attrition.csv`](../../data/mission-2026-11-14/queue-proposals-ren-attrition.csv):
  - P-REN-01: quarterly re-sweep.
  - P-REN-02: TY2025 990s.
  - P-REN-03: NPT GivingPoint book.
  - P-REN-04: PNC `/scbf` and `ocf`.
  - P-REN-05: a named RDE program and Ren's metrics.

## Validation corrections (wave 11, 2026-11-15) — governing
Source: [validation-wave11-report.md](validation-wave11-report.md). Where these conflict with the text above, these govern.

**Line 283, reproducibility.** Append: "No cache directory is committed with the repo, so an independent rerun must use `--fetch`. Wave 11's live rerun on 2026-11-15 reproduced the census exactly (76 rows, 0 status differences)."

**§1 item 1, bounds.** Add: "Four of the six exits are classified from `cf-vendor-migrations-2022-2026.csv`. All four destinations were re-verified live in wave 11. Gulf Coast's new portal is still 'launching soon', so the strict dated-exit figure (5/57 = 8.8%) is the conservative headline."

**§6, $48K-per-second bullet (line 235).** Add: "Ren's own about page states '$35B Granted to charities annually' (about $1.1K per second, or about $66.6K per minute). The '$48K per second' is therefore most likely a per-minute figure mislabelled [I]."

**Line 65, Yakima row.** No change is needed. Add a caution to the method notes: "`yvcf.org` is the Yampa Valley CF, not Yakima. Yakima is at `yakimavalleycf.org`."
