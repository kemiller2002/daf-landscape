# Re-sourcing claims that rested only on crt.sh (P-CMP-CRT-01)

**Date:** 2026-11-19. **Queue item:** P-CMP-CRT-01. **Governing note:** [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md), including its 2026-11-15 correction and wave-23 corrections.

**Outputs:**
- [`data/mission-2026-11-14/crtsh-claims-resourcing.csv`](../../data/mission-2026-11-14/crtsh-claims-resourcing.csv): 70 inventoried claims (CRT19-001 … CRT19-070), each with the route tried, the new evidence and a classification.
- [`data/mission-2026-11-14/queue-proposals-crt19.csv`](../../data/mission-2026-11-14/queue-proposals-crt19.csv): P-CRT19-01 … P-CRT19-06.

**Rules followed.**
- **No crt.sh request of any kind**, not even its robots.txt. No other certificate-transparency service was queried either. I read `sslmate.com/robots.txt` (the certspotter operator) only to judge admissibility (§6); I did not call the certspotter API.
- **Admissible routes only:**
  1. Public DNS through `dns.google` JSON (its robots.txt returns 404, so it sets no rules). I looked up A and CNAME records only, at about 1 request a second, and probed one random label per zone to detect wildcards.
  2. Vendor and sponsor public pages, with robots.txt read first for the `*`, ClaudeBot and anthropic-ai groups.
  3. Filings already harvested in the repo.
  4. The archive.org Wayback availability API (`archive.org/robots.txt` disallows only `/control/` and `/report/`). The snapshot host `web.archive.org` still resets connections, so I read capture metadata only, never captured pages.
- **Hostnames taken from earlier crt.sh output were used only as DNS seeds.** No certificate fields from crt.sh are relied on.
- No logins and no tenant `config.js` probes. One sponsor login host (`login.jcfny.org`) allows robots, but it returned a Cloudflare 403 to a single request, so it was left alone. No credentials were seen.

**Classification:**
- **re-sourced:** an admissible source now supports the substance of the claim. Where a date is replaced, the new date is given.
- **existence-only via DNS:** the hostname resolves today in a zone with no DNS wildcard. Dates, stage (sandbox, staging or production) and certificate counts remain unverified.
- **unverified lead:** no admissible source was found, or DNS cannot separate the claim from a wildcard. The claim must not be used for scoring or headline counts.

---

## 1. Summary

| Classification | Claims |
|---|---|
| re-sourced | 20 |
| existence-only via DNS | 29 |
| unverified lead | 18 |
| no claim (method notes only) | 3 |
| **Total** | **70** |

**Main findings:**
1. **Give Interactive membership mostly survives, but on weaker evidence than reported.** All 9 "known client" sponsors still have live, sponsor-named Give hostnames.
   - Only **$23.90bn** of the **$36.74bn** rests on first-party or filing evidence: Vanguard (vendor release), The Signatry entities (Schedule R and a live portal) and WaterStone (live login).
   - The other **$12.84bn** rests on DNS existence alone: CCT, ImpactAssets, JCF, Minneapolis, Thrivent and Stifel.
   - ImpactAssets belongs in the DNS-only group. Its transition page announces a hub but never names Give. Wave 23 (C4) treated it as announcement-based.
2. **Wave-23 arithmetic error.** The five CT-discovered clients sum to **$9.21bn**, not $9.81bn. The "$32.59bn without all five" figure was already computed on $9.21bn and is correct.
3. **The Give churn count falls.** Only **3 lapsed CF tenants worth $3.56bn** are admissible (EBCF, FFTC, Kalamazoo), not 5 worth $4.79bn.
   - **Omaha:** no admissible trace of a Give tenant exists. Every `omahafoundation` and `ocf-*` name is NXDOMAIN and no Wayback capture came back.
   - **San Diego:** its staging host **still resolves**, so "lapsed" is not shown.
4. **Dates of every Give implementation are leads.** The two exceptions:
   - The Signatry's host was live by **2021-10-27** (Wayback). This replaces the CT date of 2021-06-15.
   - EBCF's production host was captured from **2023-09-24 to 2026-03-13** (Wayback). This replaces the CT span 2023-06-06 to 2026-03-27.
   - The "certified by 2025-09-30" subset of the $40B reconciliation drops from **$31.64bn** to **$6.06bn**: The Signatry, plus CCT through its sandbox capture of 2025-02-23.
5. **DonorSphere and donor-portal.org have DNS wildcards.** DNS therefore cannot confirm any CT-only tenant label there.
   - DonorSphere's 21 CT-only labels (`jfnnj`, `gmw`, `jpmc`, `mssb`, …) count **0** on admissible evidence.
   - The `associated`, `jcf` (MetroWest) and `jfmd` vendor ties stand on 990 payments. Their portal labels stay [I].
6. **No change to the Ren/iPhi or Foundant tenant counts.**
   - **Ren/iPhi:** the census rests on DNS guessing and HTTP reads (61 live hosts, 57 sponsors, 6 exits). Every CT seed was also found by `dns_guess` or in the repo.
   - **Foundant:** no CF vendor-map decision rests on CT, so Foundant stays at 361 CFs (46.5%/33.7% at high/medium). The script's `ct_` field match in the map turned out to be a false positive on "redirect".
7. **Philanthropi:** "certificates still renew" is replaced by Wayback captures. The site was live on 2026-08-11 and the app on 2026-06-11. On 2026-11-19 the whole zone returns SERVFAIL.

---

## 2. DNS results (2026-11-19, dns.google)

**Wildcard probes.** One random label (`zz-nx-probe-7q4k.<zone>`) per zone:

| Zone | Result | Usable for existence? |
|---|---|---|
| giveinteractive.com, giveinteractive-clients.com, tifingive.com, vanguardcharitable.org, iphiview.com, stellartechsol.com, fcsuite.com, donorfirst.org, donorfirstx.com, charityvest.org, p.platform.charityvest.org, pinkaloo.com, fftc.org, cct.org, giftingnetwork.com | NXDOMAIN | yes |
| **donorsphere.org** | A 52.138.119.67 (**wildcard**) | **no** |
| **donor-portal.org** | A 165.245.151.118 (**wildcard**) | **no** |
| philanthropi.com | SERVFAIL (zone broken) | no (all names fail) |

**Give Interactive.** The 2026-11-14 watchlist snapshot holds 139 non-wildcard names; all were used as seeds. **89 resolve and 50 are NXDOMAIN.**

| Sponsor slug group | Resolve | NXDOMAIN |
|---|---|---|
| CCT | cct, cct-sandbox, cct-staging, api.cct-sandbox, cct-sftp.int | cct-k8s, cct-sandbox-k8s, cct-staging-k8s |
| ImpactAssets (19 names) | 11: impactassets, -staging, -sandbox, -staging-legacy, -sftp.int, give-ia-sandbox, ia-addepar, ia-dyn-holding-balance, ia-innov, ia-restrictinvestments, ia-reverse-rebook | 8 feature/k8s hosts |
| JCF | jcf-staging, -sandbox, -grant-cart, -innov, -sftp.int | — |
| Minneapolis | minneapolisfoundation-staging, tmf-sftp.int | — |
| Thrivent | thriventcharitable-staging, -sandbox, thrivent-sftp.int, tc-innov | — |
| Stifel | stifelcharitable-staging, stifel-sftp.int, stifel-sftp.ext | — |
| Vanguard | vanguardcharitable (CNAME -primary), vanguard-sandbox, -staging, -sftp.int, vc-innov | vanguard-sandbox-k8s |
| WaterStone | waterstone, -staging, -sandbox, ws-sftp.int | ws-split-interest |
| The Signatry | thesignatry, signatry-sandbox, -staging, -test, -covalience, -sftp.int, ts-fund-statements | signatry-dev, signatry-staging-k8s, thesignatry-k8s |
| nhf / jttw / jmacarthurtrust | all base, staging and SFTP hosts | jmacarthurtrust-k8s, jmctdaf-staging-k8s |
| **San Diego** | **sdfoundation-staging** | — |
| FFTC | — | all 6 (fftc-*, myfftc) |
| EBCF | — | ebcf, ebcf-staging, ebcf-sandbox |
| Omaha | — | omahafoundation, ocf-prod, ocf-sandbox, ocf-sandbox-deb11, ocf-sandbox-tenant, ocf-staging |
| Kalamazoo | — | kzcf, kzcf-staging |

`gms.giveinteractive.com` resolves to a private address (10.128.0.160). It exists, but nothing more can be read from it.

**Other zones:**
- **Vanguard Charitable.** All the §5.2 hosts resolve. `api-give`, `api-salesforce`, `auth0` and the other `api-*` hosts point to distinct API Gateway regional domains. `api-vgi` is a dangling CNAME: it points to `alb-temp-634758386.us-east-1.elb.amazonaws.com`, which is NXDOMAIN.
- **TIFIN.** `assetmarkcharitable`, `-uat`, `-release` and `mc` resolve (CloudFront).
- **iPhi.** `cafa`, `ccfnj`, `eqt`, `rj` and `www` resolve to the iPhi Global Accelerator pair. `maintenance` resolves to 10.166.196.200. `ocf` is NXDOMAIN.
- **DonorFirst.** `bofa`, `oak` and `metabase-dfx` (Azure Front Door) resolve, and `boa-dr` is NXDOMAIN. `api-boa-prod.donorfirstx.com` returns NOERROR with no A record. `aef-stg`, `boa-uat`, `msgift-uat`, `auth` and `help` resolve.
- **Charityvest.** `portal.charityvest.org` (CloudFront) and `guide.oneascent.charityvest.org` (GitBook) resolve. `vennfi.com` returns NOERROR with no A record.
- **Pinkaloo.** `connect` and `setup` are NXDOMAIN; `charities` resolves (AWS).
- **FFTC and CCT portals.** `daf.fftc.org`, `fcjc.fftc.org` and `donorportal.cct.org` resolve.
- **GiftingNetwork.** `www` (GitHub Pages) and `support` (Zendesk) resolve.
- **NPT GivingPoint.** All 13 sites resolve, to the ren-workload-02 ELB pair (3.212.252.244 / 52.23.178.115) or the iPhi Global Accelerator pair.

## 3. Wayback availability results (capture metadata only)

The availability API returns one "closest" capture per query. I asked for the capture closest to 1996-01-01 ("earliest") and the one closest to 2026-11-19 ("latest"). These approximate the first and last captures; they are not a full CDX listing.

From about the 120th host onward the API returned HTTP 429. A second, slower pass re-queried 47 key hosts. Controls returned captures, so most empty results are probably genuine non-captures, but a few hosts stayed rate-limited. **An empty result is still not evidence of absence** (P-CRT19-03).

| Host | Earliest capture | Latest capture | Use |
|---|---|---|---|
| ebcf.giveinteractive.com | 2023-09-24 (200) | 2026-03-13 (200) | EBCF tenancy span |
| ebcf-staging / ebcf-sandbox | 2024-03-22 / 2024-06-19 | 2025-02-03 / 2025-04-07 | EBCF environments |
| kzcf.giveinteractive.com | 2024-09-20 (200) | 2025-02-22 (200) | Kalamazoo tenancy |
| kzcf-staging | 2024-08-25 | 2024-08-25 | — |
| sdfoundation-staging | 2025-04-16 (200) | 2025-04-16 | San Diego staging existed |
| cct-sandbox | 2025-02-23 (200) | 2025-02-23 | CCT environment by 2025-02 |
| thesignatry.giveinteractive.com | 2021-10-27 (200) | 2026-07-17 (200) | Signatry live by 2021-10 |
| signatry-staging | 2024-05-02 | 2024-12-22 | — |
| ts-fund-statements | 2024-08-27 | 2025-02-23 | — |
| philanthropi.com | 2004-10-25 | **2026-08-11 (200)** | site live to 2026-08 |
| app.philanthropi.com | — | **2026-06-11 (200)** | app live to 2026-06 |
| connect.pinkaloo.com | 2022-07-17 | 2022-07-17 | app retired after 2022 |
| charities.pinkaloo.com | 2020-11-27 | 2023-09-26 | — |
| bofa.donorfirst.org | 2020-10-21 | **2026-10-29 (200)** | DFX live 2026 |
| portal.charityvest.org | 2022-07-25 | 2024-08-27 | host predates CT dates |
| guide.oneascent.charityvest.org | 2024-03-27 | 2025-03-16 | — |
| ircf.donor-portal.org | 2022-09-14 | 2026-05-13 | wildcard zone: not probative |
| gkccf.donor-portal.org | 2022-04-19 | 2025-10-17 | — |
| donor-portal.org | 2022-01-13 | 2025-03-31 | — |
| fund-miner.com | 2024-12-12 | 2025-01-15 | — |
| assetmarkcharitable-release / -uat (tifingive) | 2025-02-20 / 2025-04-06 | 2025-02-21 / 2025-04-06 | later than CT dates |
| ocf.iphiview.com (host) | 2018-03-30 | 2018-03-30 | (path `/ocf` 2025-12-20, batch 38) |

No capture was returned for cct, impactassets, vanguardcharitable, waterstone, the omahafoundation, ocf-* and fftc-* Give hosts, the Vanguard Charitable subdomains, daf.fftc.org, fcjc.fftc.org or donorportal.cct.org. Several of these fell in the rate-limited window.

**NPT GivingPoint sites** (second, slower pass; controls `www.vanguardcharitable.org` and `ebcf.giveinteractive.com` returned captures, so the empty results above are probably real non-captures):

| Site | CT first cert (doc) | Earliest Wayback capture returned | Reading |
|---|---|---|---|
| nptgivingpoint.org | 2020-10-29 | 2021-03-05 | live by 2021-03 |
| jpmgiving.org | 2021-06-04 | 2021-12-30 | live by 2021-12 |
| jpmgiftfund.org | 2022-03-16 | 2024-11-10 | live by 2024-11 (upper bound only) |
| donoradvisedfundgiving.org (UBS) | 2021-09-23 | 2022-05-18 | live by 2022-05 |
| **bmodaf.org** | 2026-02-15 (certspotter, current certs only) | **2024-07-31** | **live by 2024-07; the 2026-02-15 date is wrong as a launch date** |
| rathbonesdaf.org | 2024-11-20 | 2025-04-18 | live by 2025-04 |
| icgfdaf.org | 2025-06-02 | 2025-07-14 | live by 2025-07 |
| cazenovecapitaldaf.org | 2021-09-28 | 2025-07-17 | upper bound only |
| nptukgiving.org | 2021-12-16 | (429; a no-timestamp query returned 2026-08-08) | not dated |
| tollesondaf.org, pitcairndaf.org | 2025-02-10, 2025-04-28 | HTTP 429 | not dated |
| npttransatlanticdaf.org | 2025-06-03 | none returned | not dated |

A Wayback first capture is an upper bound on launch, not a launch date.
- **Rathbones (by 2025-04) and ICGF (by 2025-07)** are consistent with the "new GivingPoint sites around FY2025" reading.
- **Tolleson, Pitcairn and Transatlantic stay leads.**
- **BMO:** its site was live by 2024-07-31, well before the certspotter date.

## 4. Recomputed counts (admissible evidence only)

| Count | Before | After | Change and basis |
|---|---|---|---|
| Give "known clients", DAFRC FY2024 | $36.74bn (9 sponsors) | **$36.74bn on DNS existence; $23.90bn on first-party or filing evidence** | Unchanged membership. $12.84bn (CCT 4.65, IA 3.63, JCF 2.87, Minneapolis 0.60, Thrivent 0.59, Stifel 0.49) is DNS-only. First-party/filing tier is 59.7% of $40bn. Basis: DAFRC sponsor-universe FY2024 values, in which ImpactAssets ($3.63bn) and Signatry ($0.40bn) are imputed; on the R1-corrected league table ImpactAssets is $2.90bn, giving a DNS-only tier of $12.11bn [V wave 31B] |
| Same, batch-38 basis (Vanguard FYE 2025-06 $27.01bn) | $41.80bn | **$41.80bn on DNS; $28.96bn first-party/filing** | — |
| CT-discovered five (wave 23) | $9.81bn | **$9.21bn** | Arithmetic: 4,649,987,855 + 2,870,570,567 + 601,822,240 + 594,270,055 + 493,554,856 = 9,210,205,573. "$32.59bn without all five" is correct |
| Certified by 2025-09-30 (claim-time pipeline) | $31.64bn (Vanguard, CCT, IA, Signatry) | **$6.06bn** (Signatry 1.41, CCT 4.65) | Only these two have an admissible date before 2025-09-30. Vanguard's earliest admissible date is the 2025-11-04 release. IA has no admissible date |
| Live for donors | $1.95bn | $1.95bn | Unchanged (first-party login pages) |
| Lapsed Give CF tenants | 5, $4.79bn | **3, $3.56bn** (EBCF 0.53, FFTC 2.95, Kalamazoo 0.08) | Omaha ($0.52bn) is an unverified lead. San Diego ($0.71bn) status is unknown: its staging host resolves. FFTC's $2.95bn is the DAFRC-imputed value; the R1-corrected FY2024 figure is $2.62bn, which makes the three $3.23bn [V wave 31B] |
| Give CF tenants (cf-vendor-map §5 table) | 6 CFs | **6 CFs**, on DNS, Wayback or 990 | CCT, Minneapolis and SDF by DNS; EBCF and KZCF by Wayback; FFTC by 990. All dates are leads except the EBCF and KZCF Wayback spans |
| Give hostnames | 138 CT names (doc); 141 (snapshot) | **89 live hostnames** | 139 non-wildcard seeds: 89 resolve, 50 NXDOMAIN |
| ImpactAssets Give feature hosts | "~15 ia-* in 2026" | **8 resolve** | 19 IA-related names: 11 resolve in total, 8 of them feature hosts |
| Ren/iPhi tenant census | 61 live hosts; 57 sponsors; 6 exits | **unchanged** | DNS and HTTP based; CT seeds were also found by DNS guesses |
| iPhi named CT hosts | 7 | 5 resolve to the tenant pair, plus maintenance (private) | ocf NXDOMAIN |
| Foundant (CF vendor map) | 361 CFs; 46.5% count, 33.7% assets (batch 30) | **unchanged** | No map decision rests on CT |
| Foundant named CT hosts | 11 | not re-checked | Names not kept in the repo. The figure is a CT statistic and feeds no share |
| DonorSphere CT tenant labels | 31 CT names | **0 confirmable by DNS** (wildcard) | Vendor ties for 3 sponsors stand on 990 payments; 5 tenants stand on first-party pages (ghcf, hawaiicf, pgh, fjc; FoundationHub at fumf) |

## 5. Proposed corrections (Find / Replace)

Each Find string occurs exactly once in its file (checked 2026-11-19). Apply them under P-CRT19-01. Historical text is kept: every Replace keeps the original wording and adds the re-sourcing.

### 5.1 `queue-give-interactive-displacement.md`
1. **Find:** "  - [crt.sh `%.giveinteractive.com`](https://crt.sh/?q=%25.giveinteractive.com) returned 1,979 certificates and 138 names."
   **Replace:** "  - [crt.sh `%.giveinteractive.com`](https://crt.sh/?q=%25.giveinteractive.com) returned 1,979 certificates and 138 names. [Compliance, 2026-11-19: unverified lead. Of 139 non-wildcard names, 89 resolve in public DNS on 2026-11-19 and 50 are NXDOMAIN; certificate dates and counts are not re-sourced. See crtsh-resourcing-2026-11-19.md.]"
2. **Find:** "   - **Three are at the staging/SFTP stage:** Minneapolis, Thrivent and Stifel."
   **Replace:** "   - **Three are at the staging/SFTP stage:** Minneapolis, Thrivent and Stifel. (Their Give hostnames resolve in public DNS on 2026-11-19; the stage itself is a CT-only lead.)"
3. **Find:** "Its tenants lapsed in Feb 2024. Tenants for OCF, Omaha, EBCF, KZCF and the San Diego Foundation also expired."
   **Replace:** "Its tenant hostnames are all NXDOMAIN on 2026-11-19; the Feb 2024 lapse month is a CT-only lead. EBCF (Wayback 2023-09-24 to 2026-03-13) and KZCF (Wayback 2024-09-20 to 2025-02-22) tenants are gone from DNS. The Omaha/OCF tenants have no admissible trace, and the San Diego staging host still resolves [crt19]."
4. **Find:** "A `vanguard-sftp` data channel was first certified 2026-11-03."
   **Replace:** "A `vanguard-sftp` data channel exists (it resolves in public DNS on 2026-11-19); its 2026-11-03 first-certificate date is a CT-only lead [crt19]."
5. **Find:** "**Notes on dating.**"
   **Replace:** "**Notes on dating.** [Compliance, 2026-11-19: the Give-host dates in this table are CT-only leads, except thesignatry (live by 2021-10-27, Wayback) and the sponsor-page and 990 facts. Host existence is re-sourced by DNS for every sponsor except FFTC (all hosts NXDOMAIN).]"
6. **Find:** "| `giveinteractive-clients.com` (wildcard since 2024-10-15) |"
   **Replace:** "| `giveinteractive-clients.com` (apex resolves; no DNS wildcard; wildcard-certificate date 2024-10-15 is a CT-only lead) |"

### 5.2 `queue-batch30-cf-coverage-give.md`
1. (The shorter sentence also occurs in the validation block, so the row prefix is included.) **Find:** "| **P-GIV-07** | **Give lost five CF tenants holding $4.79bn of DAF assets."
   **Replace:** "| **P-GIV-07** | **Give lost five CF tenants holding $4.79bn of DAF assets. [crt19: on admissible evidence, three ($3.56bn: EBCF, FFTC, Kalamazoo). Omaha's Give tenancy is a CT-only lead, and San Diego's staging host still resolves.]"
2. **Find:** "Give certificates stop 2026-03-27."
   **Replace:** "Give certificates stop 2026-03-27 (CT lead); Wayback last captured `ebcf.giveinteractive.com` on 2026-03-13, and the host is NXDOMAIN on 2026-11-19 [crt19]."
3. **Find:** "Certificate spans come from crt.sh (`%.giveinteractive.com`, full export of 2026-11-15, read by the script)."
   **Replace:** "Certificate spans come from crt.sh (`%.giveinteractive.com`, full export of 2026-11-15, read by the script). [Compliance: the spans are unverified leads. `nhf`, `jttw`, `jmacarthurtrust` and `jmctdaf-staging` resolve in public DNS on 2026-11-19.]"
4. **Find:** "- **Known clients:** Vanguard 21.95, CCT 4.65, ImpactAssets 3.63, JCF 2.87, Servant/Signatry 1.41, Minneapolis 0.60, Thrivent 0.59, WaterStone 0.54 and Stifel 0.49, totalling **$36.74bn**."
   **Replace:** "- **Known clients:** Vanguard 21.95, CCT 4.65, ImpactAssets 3.63, JCF 2.87, Servant/Signatry 1.41, Minneapolis 0.60, Thrivent 0.59, WaterStone 0.54 and Stifel 0.49, totalling **$36.74bn**. Of this, $23.90bn (Vanguard, Signatry, WaterStone) rests on first-party or filing evidence. The other $12.84bn rests on DNS existence of sponsor-named Give hosts only [crt19]."
5. **Find:** "- **Live losses.** Only EBCF was a demonstrated live loss, after about 2.5 years (2023-06 to 2026-03)."
   **Replace:** "- **Live losses.** Only EBCF was a demonstrated live loss, after about 2.5 years (2023-06 to 2026-03; Wayback 2023-09-24 to 2026-03-13) [crt19]."

### 5.3 `queue-cf-vendor-map.md`
1. **Find:** "The certificate data show lapsed or staging-only Give tenants at East Bay, Kalamazoo, San Diego, Minneapolis and FFTC (§5)."
   **Replace:** "The certificate data show lapsed or staging-only Give tenants at East Bay, Kalamazoo, San Diego, Minneapolis and FFTC (§5). On admissible evidence (2026-11-19): East Bay and Kalamazoo by Wayback captures, FFTC by its CY2023 990, and San Diego and Minneapolis by live DNS. All certificate dates are leads [crt19]."
2. **Find:** "**Give Interactive certificate tenants at CFs** (crt.sh, certificates from 2021 on):"
   **Replace:** "**Give Interactive certificate tenants at CFs** (crt.sh, certificates from 2021 on; dates are unverified leads under the compliance note, and existence is re-sourced in crtsh-resourcing-2026-11-19.md §2–3):"
3. **Find:** "(only 11 and 7 named `fcsuite` and `iphiview` hosts since 2021)"
   **Replace:** "(only 11 and 7 named `fcsuite` and `iphiview` hosts since 2021, per crt.sh, an unverified-lead statistic used in no share; 5 of the 7 iPhi names resolve on 2026-11-19)"

### 5.4 `queue-watchlist-and-vendor-moves.md`
1. **Find:** "Tenants with a certificate by Sept 2025, when the claim was made, hold $31.6bn."
   **Replace:** "Tenants with a certificate by Sept 2025, when the claim was made, hold $31.6bn (CT-only lead; on admissible dates only The Signatry and CCT, $6.06bn, are evidenced before 2025-09-30 [crt19])."
2. **Find:** "| Certified by 2025-09-30 (Vanguard, CCT, ImpactAssets, Signatry) | | | 31.64 | 31.30 |"
   **Replace:** "| Certified by 2025-09-30 (Vanguard, CCT, ImpactAssets, Signatry; CT-only lead) | | | 31.64 | 31.30 |\n| Admissibly dated by 2025-09-30 (Signatry: Wayback 2021-10-27; CCT: cct-sandbox Wayback 2025-02-23) [crt19] | | | 6.06 | |"
3. **Find:** "1. **The claim is consistent with a pipeline figure.** At claim time, the four tenants with certificates hold $31.6bn of FY2024 DAF assets."
   **Replace:** "1. **The claim is consistent with a pipeline figure.** At claim time, the four tenants with certificates hold $31.6bn of FY2024 DAF assets (certificate dates are CT-only leads; see crtsh-resourcing-2026-11-19.md §4)."
4. **Find:** "The sandbox and staging certificates were renewed on 2026-10-12 and 2026-10-06 ([crt.sh](https://crt.sh/?q=%25.giveinteractive.com))."
   **Replace:** "The sandbox and staging hosts resolve in public DNS on 2026-11-19; their renewal dates (2026-10-12, 2026-10-06, [crt.sh](https://crt.sh/?q=%25.giveinteractive.com)) are unverified leads [crt19]."
5. **Find:** "The TIFIN `assetmarkcharitable*` hosts were first certified 2024-05-01 (UAT) and 2024-05-28 (production) ([crt.sh](https://crt.sh/?q=%25.tifingive.com)),"
   **Replace:** "The TIFIN `assetmarkcharitable*` hosts resolve in public DNS; their first-certificate dates of 2024-05-01 (UAT) and 2024-05-28 (production) ([crt.sh](https://crt.sh/?q=%25.tifingive.com)) are unverified leads, and the earliest Wayback captures are 2025-02/04 [crt19],"
6. **Find:** "| confirmed (CT) |"
   **Replace:** "| hosts exist (public DNS, 2026-11-19); dates CT-only lead [crt19] |"
7. **Find:** "**`api-give.vanguardcharitable.org`** (first certified 2026-02-25), issued together with `api-salesforce`, `api-vgi` and `auth0` ([crt.sh](https://crt.sh/?q=%25.vanguardcharitable.org))."
   **Replace:** "**`api-give.vanguardcharitable.org`** (resolves to an API Gateway regional domain; first-certified date 2026-02-25 and co-issuance with `api-salesforce`, `api-vgi` and `auth0` are CT-only leads, [crt.sh](https://crt.sh/?q=%25.vanguardcharitable.org)) [crt19]."

### 5.5 `queue-fidelity-chariot-goodstack-vanguard.md`
1. **Find:** "### 5.2 Hosts first certified in 2025 or later (from the watchlist snapshot `data/watchlist-snapshots/2026-11-14/ct-vanguardcharitable.json`, crt.sh; root probe 2026-11-14)"
   **Replace:** "### 5.2 Hosts first certified in 2025 or later (from the watchlist snapshot `data/watchlist-snapshots/2026-11-14/ct-vanguardcharitable.json`, crt.sh; root probe 2026-11-14). First-cert dates are unverified leads; every host except `api-vgi` resolves in public DNS on 2026-11-19 [crt19]"
2. **Find:** "| api-vgi | 2026-02-25 | n/a | No DNS answer seen from here; the proxy returned 502 |"
   **Replace:** "| api-vgi | 2026-02-25 | n/a | No DNS answer seen from here; the proxy returned 502. 2026-11-19: dangling CNAME to `alb-temp-634758386.us-east-1.elb.amazonaws.com` (NXDOMAIN) [crt19] |"

### 5.6 `queue-batch32-feeds-owners-codebases.md`
1. **Find:** "Certificates issued 2026-08-06 to 2026-09-04 cover `app-dev-migrate`, `app-stage-migrate`, `api-stage`, `stg-v3`, `sales` and `marketingproject` [F]."
   **Replace:** "Certificates issued 2026-08-06 to 2026-09-04 cover `app-dev-migrate`, `app-stage-migrate`, `api-stage`, `stg-v3`, `sales` and `marketingproject` [CT lead]. Admissible substitute: Wayback captured `philanthropi.com` (HTTP 200) on 2026-08-11 and `app.philanthropi.com` on 2026-06-11. On 2026-11-19 every name in the zone returns SERVFAIL [crt19]."
2. **Find:** "App hosts (`connect`, `charities`, `setup`) have no named certificate after 2022 ([crt.sh](https://crt.sh/?q=%25.pinkaloo.com)) [F]."
   **Replace:** "App hosts (`connect`, `charities`, `setup`) have no named certificate after 2022 ([crt.sh](https://crt.sh/?q=%25.pinkaloo.com)) [CT lead]. `connect` and `setup` are NXDOMAIN on 2026-11-19, and Wayback last captured `connect` on 2022-07-17 and `charities` on 2023-09-26 [crt19]."
3. **Find:** "2026 certificates for `bofa`, `oak`, `boa-dr` and `metabase-dfx` under donorfirst.org, plus `*.donorfirstx.com` and `api-boa-prod` [F]."
   **Replace:** "2026 certificates for `bofa`, `oak`, `boa-dr` and `metabase-dfx` under donorfirst.org, plus `*.donorfirstx.com` and `api-boa-prod` [CT lead]. `bofa`, `oak` and `metabase-dfx` resolve and `boa-dr` is NXDOMAIN on 2026-11-19; Wayback captured `bofa.donorfirst.org` (HTTP 200) on 2026-10-29 [crt19]."
4. **Find:** "Certificates 2026-08 to 2026-10 for `portal.`, `*.p.platform.` and `guide.oneascent.` under charityvest.org ([crt.sh](https://crt.sh/?q=%25.charityvest.org)) [F]."
   **Replace:** "Certificates 2026-08 to 2026-10 for `portal.`, `*.p.platform.` and `guide.oneascent.` under charityvest.org ([crt.sh](https://crt.sh/?q=%25.charityvest.org)) [CT lead]. `portal` and `guide.oneascent` resolve on 2026-11-19; Wayback captures date them from 2022-07-25 and 2024-03-27 [crt19]."
5. **Find:** "`vennfi.com` has no A record and no certificates [F]"
   **Replace:** "`vennfi.com` has no A record (NOERROR, no answer, 2026-11-19) [F]; \"no certificates\" is a CT lead [crt19]"

### 5.7 `queue-bdc-coverage-migrations-goodstack.md`
1. **Find:** "`ircf.donor-portal.org` had named certificates 2021-02-08 to 2022-01-04 ([crt.sh](https://crt.sh/?q=ircf.donor-portal.org))."
   **Replace:** "`ircf.donor-portal.org` had named certificates 2021-02-08 to 2022-01-04 ([crt.sh](https://crt.sh/?q=ircf.donor-portal.org); unverified lead). `donor-portal.org` has a DNS wildcard, so DNS cannot confirm the tenant [crt19]."

### 5.8 `queue-community-foundation-rails-portals.md`
1. **Find:** "Its brand fallback is `donor-portal.org`, whose wildcard certificate dates from 2026-08-22 ([crt.sh](https://crt.sh/?q=%25.donor-portal.org))."
   **Replace:** "Its brand fallback is `donor-portal.org`, whose wildcard certificate dates from 2026-08-22 ([crt.sh](https://crt.sh/?q=%25.donor-portal.org); unverified lead). The zone also has a DNS wildcard (2026-11-19) [crt19]."
2. **Find:** "The live donor-portal certificate was reissued 2026-09-27 ([crt.sh](https://crt.sh/?q=donorportal.cct.org))."
   **Replace:** "The live donor-portal certificate was reissued 2026-09-27 ([crt.sh](https://crt.sh/?q=donorportal.cct.org); unverified lead) [crt19]."
3. **Find:** "The GiftingNetwork documents were refreshed in December 2025 and the GiftingNetwork certificate in September 2026."
   **Replace:** "The GiftingNetwork documents were refreshed in December 2025 (the certificate refresh in September 2026 is a CT-only lead) [crt19]."

### 5.9 `queue-donor-export-cf-payments-donorsphere.md`
1. **Find:** "- **Domain history.** The DonorSphere CT history begins in 2011 ([crt.sh](https://crt.sh/?q=%25.donorsphere.org)) [F]."
   **Replace:** "- **Domain history.** The DonorSphere CT history begins in 2011 ([crt.sh](https://crt.sh/?q=%25.donorsphere.org)) [CT lead; not re-sourced, crt19]."
2. **Find:** "| `jfnnj`, `gmw` | JF Northern NJ (by name); `gmw` unidentified | config / CT names only | inferred / unknown |"
   **Replace:** "| `jfnnj`, `gmw` | JF Northern NJ (by name); `gmw` unidentified | config / CT names only. `donorsphere.org` has a DNS wildcard, so DNS cannot confirm any label [crt19] | inferred / unknown (CT names: unverified lead) |"

### 5.10 `queue-ledgers-behind-portals.md`
1. **Find:** "Give `cct` production certificate 2025-06 to 2026-08 ([crt.sh](https://crt.sh/?q=%25.giveinteractive.com))"
   **Replace:** "Give `cct` host resolves in public DNS (2026-11-19); the production certificate span 2025-06 to 2026-08 ([crt.sh](https://crt.sh/?q=%25.giveinteractive.com)) is an unverified lead"
2. **Find:** "- **Certificates:** Let's Encrypt certificates from 2020-08-29, and wildcard `*.donor-portal.org` from 2021-10-14 ([crt.sh](https://crt.sh/?q=donor-portal.org)). No tenant names are exposed."
   **Replace:** "- **Certificates:** Let's Encrypt certificates from 2020-08-29, and wildcard `*.donor-portal.org` from 2021-10-14 ([crt.sh](https://crt.sh/?q=donor-portal.org); dates are unverified leads). No tenant names are exposed. The zone also has a DNS wildcard (2026-11-19), so DNS cannot enumerate tenants either [crt19]."
3. **Find:** "- **Certificates:** one certificate name only, `fund-miner.com`, issued 2023-04-20 to 2026-06-07."
   **Replace:** "- **Certificates:** one certificate name only, `fund-miner.com`, issued 2023-04-20 to 2026-06-07 (crt.sh; unverified lead) [crt19]."
4. **Find:** "- **No 2021+ client announcement** was found for the CT-only labels `jpmc` and `mssb`."
   **Replace:** "- **No 2021+ client announcement** was found for the CT-only labels `jpmc` and `mssb`. They are unverified leads: `donorsphere.org` has a DNS wildcard [crt19]."

### 5.11 `queue-npt-givingpoint-fidelity-stack.md`
1. **Find:** "CT dates come from crt.sh unless marked; crt.sh covers full history."
   **Replace:** "CT dates come from crt.sh unless marked; crt.sh covers full history. [Compliance, 2026-11-19: the \"First CT cert\" column is an unverified lead. All 13 sites resolve in public DNS; see crtsh-resourcing-2026-11-19.md §3 for Wayback dating.]"
2. **Find:** "CT first dates: Rathbones 2024-11, Tolleson 2025-02, Pitcairn 2025-04, ICGF and Transatlantic 2025-06."
   **Replace:** "CT first dates (leads): Rathbones 2024-11, Tolleson 2025-02, Pitcairn 2025-04, ICGF and Transatlantic 2025-06. Admissible: Wayback captures Rathbones by 2025-04-18 and ICGF by 2025-07-14; Tolleson, Pitcairn and Transatlantic are undated. BMO was live by 2024-07-31 (Wayback), not 2026-02 [crt19]."

### 5.12 `queue-ren-iphi-attrition.md`
1. **Find:** "so only 7 named iPhi hosts appear: one ZeroSSL batch on 2025-04-20 (`cafa`, `ccfnj`, `eqt`, `rj`, `ocf`, `www`, `maintenance`)"
   **Replace:** "so only 7 named iPhi hosts appear: one ZeroSSL batch on 2025-04-20 (`cafa`, `ccfnj`, `eqt`, `rj`, `ocf`, `www`, `maintenance`; the batch date is an unverified lead, and every CT seed was also found by DNS guessing or the repo, so the census counts do not change [crt19])"

### 5.13 `queue-vendor-channel-moves.md`
1. **Find:** "First certified 2026-04-13 ([crt.sh](https://crt.sh/?q=daf.fftc.org))"
   **Replace:** "Resolves in public DNS (2026-11-19); first-certified date 2026-04-13 ([crt.sh](https://crt.sh/?q=daf.fftc.org)) is an unverified lead"
2. **Find:** "First certified 2026-04-13, the same day as daf.fftc.org ([crt.sh](https://crt.sh/?q=fcjc.fftc.org))"
   **Replace:** "Resolves in public DNS (2026-11-19); first-certified 2026-04-13, the same day as daf.fftc.org ([crt.sh](https://crt.sh/?q=fcjc.fftc.org)), is an unverified lead"
3. **Find:** "Host certified since **2023-10-06** ([crt.sh](https://crt.sh/?q=donorportal.cct.org))."
   **Replace:** "Host certified since **2023-10-06** ([crt.sh](https://crt.sh/?q=donorportal.cct.org); unverified lead). Admissible bound: the earlier CCT guide `DonorPortalUserGuide.pdf` was created 2024-02-06 (wave 6) [crt19]."
4. **Find:** "Tenant `cct`: sandbox 2024-08-12, production 2025-06-11, SFTP 2026-11-03 (repo CT work, [give-interactive-displacement §2](queue-give-interactive-displacement.md))"
   **Replace:** "Tenant `cct`: sandbox 2024-08-12, production 2025-06-11, SFTP 2026-11-03 (repo CT work, [give-interactive-displacement §2](queue-give-interactive-displacement.md); dates and stage are CT-only leads; the hosts resolve in DNS and `cct-sandbox` was captured by Wayback on 2025-02-23)"
5. **Find:** "- **CT logs.** `giftingnetwork.com` certifies only `www` and `support` ([crt.sh](https://crt.sh/?q=%25.giftingnetwork.com))."
   **Replace:** "- **CT logs.** `giftingnetwork.com` certifies only `www` and `support` ([crt.sh](https://crt.sh/?q=%25.giftingnetwork.com); unverified lead). Both resolve, the zone has no DNS wildcard, and the known portals sit on client domains (`daf.fftc.org`, `donorportal.cct.org`) [crt19]."

### 5.14 `queue-batch38-vendors-ledgers-portals.md` and `validation-wave23-report.md`
1. **`queue-batch38-vendors-ledgers-portals.md`.**
   **Find:** "($9.81bn at FY2024)"
   **Replace:** "($9.21bn at FY2024; corrected from $9.81bn [crt19])"
2. **`validation-wave23-report.md`.**
   **Find:** "($9.81bn at FY2024)"
   **Replace:** "($9.21bn at FY2024; corrected from $9.81bn [crt19])"
3. **`validation-wave23-report.md`.**
   **Find:** "$9.81bn of it (CCT $4.65bn, JCF $2.87bn, Minneapolis $0.60bn, Thrivent $0.59bn, Stifel $0.49bn)"
   **Replace:** "$9.21bn of it (CCT $4.65bn, JCF $2.87bn, Minneapolis $0.60bn, Thrivent $0.59bn, Stifel $0.49bn; corrected from $9.81bn [crt19]). ImpactAssets ($3.63bn) is also attributed to Give only through hostnames, because its transition page names no vendor"

### 5.15 `compliance-note-crtsh-robots.md`
1. **Append a section** "## Re-sourcing (P-CMP-CRT-01, 2026-11-19)" pointing to this document. Its text:

   "70 claims inventoried: 20 re-sourced, 29 existence-only via DNS, 18 unverified leads. Give admissible lapsed CF tenants: 3 ($3.56bn), not 5 ($4.79bn). Give known clients $36.74bn stand on DNS, of which $23.90bn on first-party or filing evidence. Ren/iPhi and Foundant counts are unchanged. donorsphere.org and donor-portal.org have DNS wildcards, so their CT-only labels cannot be re-sourced by DNS. Certspotter is treated like crt.sh from 2026-11-19, because its operator's robots.txt (sslmate.com) disallows /api; its results are unverified leads (P-CRT19-02 closed by the compliance note) [V wave 31B]."

No claim-bearing correction is needed for `direction-patents-security.md` (crt.sh was excluded), `research/iphi-175-client-lead-and-dns-execution-2026-11-11.md` (a method note; the script now refuses `--ct`) or `data/watchlist-snapshots/reports/2026-11-14.md` (historical diff report; do not cite its CT observations).

## 6. Limits and open points

- **Certspotter is not crt.sh, but it raises the same question.** `api.certspotter.com/robots.txt` returns 404, while `sslmate.com/robots.txt` (the same operator) disallows `/api` and `/crt` for all agents.
  - Several repo dates come from certspotter only: `tc-innov`, `vc-innov`, `ia-innov`, the `*-sftp.int` first dates, BMO 2026-02-15, the Fidelity CT set and the CCT 2026-09-01 renewals.
  - I did not query certspotter. I have classed these claims by their DNS status only. The admissibility decision (P-CRT19-02) was taken the same day in compliance-note-crtsh-robots.md: certspotter is no longer used, and its results are unverified leads unless confirmed by DNS, first-party pages or filings [V wave 31B].
- **Wayback coverage is partial** because of HTTP 429 rate-limiting (P-CRT19-03). The availability API's "closest" capture is only an approximation of the first and last capture.
- **DNS shows existence today, not history and not stage.** A resolving `*-staging` name says nothing about whether production exists. Absence claims ("no production host") cannot be re-sourced by DNS without guessing names.
- **The CT names used as DNS seeds came from earlier crt.sh output.** Re-sourcing by DNS confirms each name independently, but the list of names was found through crt.sh. Names that were never seen in CT were not probed.
- **First-party searches found nothing new.**
  - giveinteractive.com (empty robots.txt): the homepage, company page, solutions pages and the fund-of-funds post name no client except Vanguard (via a link to `/post/vanguard`).
  - jcfny.org, minneapolisfoundation.org and thriventcharitable.thrivent.com (robots allowed) link no Give host.
  - cct.org returned 403 and was not fetched.
