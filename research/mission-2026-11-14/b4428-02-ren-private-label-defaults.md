# P-B4428-02: Ren platform acknowledgement defaults by private label

- **Task:** P-B4428-02, queued in [b44n28-01-donor-info-defaults.md](b44n28-01-donor-info-defaults.md) §3.2, read with its "Validation corrections (wave 34A)" in [validation-wave34a-report.md](validation-wave34a-report.md) (V34A-26, -28, -30).
- **Date:** 2026-11-19. Every page and PDF was read on that date.
- **Data:** [`data/mission-2026-11-14/ren-private-label-defaults-2026-11-19.csv`](../../data/mission-2026-11-14/ren-private-label-defaults-2026-11-19.csv). It has 28 rows, one per program, each with a quote, a URL, a document date and (for PDFs) a SHA-1 prefix.
- **Script:** [`scripts/mission_b4428_02_ren_defaults_build.py`](../../scripts/mission_b4428_02_ren_defaults_build.py). Run it as `python3 -I scripts/mission_b4428_02_ren_defaults_build.py . <out.csv>`. It rebuilds the CSV byte for byte (md5 checked twice) and prints the asset tables in §5.
- **Queue:** [`data/mission-2026-11-14/queue-proposals-b4428-02.csv`](../../data/mission-2026-11-14/queue-proposals-b4428-02.csv) (6 rows).
- **Labels:** [F] first-party text read this pass. [I] inference. [B] blocked by robots or unreachable. [R] repo-carried.

## 0. Answer

| Question | Finding | Confidence |
|---|---|---|
| **What do Ren programs default to?** | Of the 28 program rows:<br>- **7 full contact**;<br>- **2 name only**;<br>- **6 fund name only**;<br>- **3 no default stated**;<br>- **0 anonymous**;<br>- **10 not determinable** (6 have no public text: RCF-14 to RCF-17, GCCF-01 and OAK-01; 4 are robots-blocked: RCF-18, GS-01, RJ-01 and the IPHI-00 catch-all row) [V wave 35B].<br>All 7 full-contact rows rest on **one file**: the "Giving Platform Donor User Guide" (PDF 2026-10-06, SHA-1 `93d97b49e84a`). It is linked unchanged from 7 RCF portals: RCF, Ameriprise, RBC, MDRT, RCF Giving Fund, UBS and Northwestern Mutual [F] | High on the text. Several programs carry two first-party texts that disagree (§3.3) |
| **Is email included?** | **Only where that 2026-10 guide applies**: "By default, this includes the grant advisor's name, email, and address".<br>At CJP, email is shared "at your direction". No other program's document mentions donor email.<br>Ren's platform release notes add "Emails that are elected in the grant recommendation screen will now be surfaced" ("2024 August Release" page, dated January 15, 2025). So email is a **platform field**, and on most programs it is elected [F] | High |
| **Sponsor setting or platform default?** | **Not shown either way, but the documents lean toward platform version, not sponsor.**<br>- Every donor guide that states a grant-screen default *and* predates the 2026-10 guide says **fund name**. Letter-policy texts of the same period differ: the MDRT, RCF Giving Fund, Commonwealth and SEI circulars (2024–25) name the fund and the grant advisor, and BofA's 2024 Program Guidelines name the account and the donor or advisor [V wave 35B]. These are RCF's own 2023 template guide (on the TDA and UBS portals, 2024), BofA's guide (2026-02) and MS GIFT's Grantee Guidelines (2022).<br>- The only full-contact default is the 2026 "Giving Platform" guide. It is used identically across RCF's private labels.<br>- One program, **UBS, links both guides with opposite defaults.**<br>- No pair of *different* sponsors is documented on the same version with different defaults.<br>The b44n28-01 §3.2 inference ("configurable sponsor setting, not a platform constraint") compared BofA's 2026-02 guide with RCF's 2026-10 guide. That compares **two guide vintages**, so it does not test the claim [F/I] | Medium. Public guides only. The login shells of all 17 DFX/DonorFirst portals load the same build, but the grant screens behind login were not observed |
| **Asset share, Ren-administered sponsors** (RCF, MS GIFT, BofA CGF, AEF; FY2024 $28.13bn, 8.70% of the $323.27bn corrected market) | - **Fund name only:** 49.2% (MS GIFT, BofA).<br>- **Full contact:** 21.0% (RCF, coded by its 2026-10 guide; an upper bound per V34A-28).<br>- **No default stated:** 29.8% (AEF).<br>If RCF is coded by its own 2023–24 DFX guide, **fund name only rises to 70.2%** and full contact falls to 0% | High arithmetic. The RCF coding swings 21 points |
| **Asset share, all Ren-linked sponsors in the FY2024 top 50** (adds CJP, T. Rowe Price, GS DAF and Raymond James; $45.19bn, 13.98% of market) | - **Full contact:** 13.1%.<br>- **Fund name only:** 34.9% (48.0% with RCF on its 2024 guide).<br>- **No default stated:** 19.9%.<br>- **Not determinable:** 32.1% (GS DAF and Raymond James, both robots-blocked) | High arithmetic; a third of assets unobserved |
| **RCF private labels** | 18 RCF program rows:<br>- 7 full contact (the shared 2026 guide);<br>- 2 name only (Commonwealth and SEI circulars: "acknowledge the fund and the grant advisor's involvement");<br>- 3 fund name only (the TDA portal's 2024 guide; the Franklin circular; the Salvation Army FAQ);<br>- 1 no default stated (LPL circular);<br>- 5 not determinable.<br>**The repo has no RCF program-level asset split**, so all of them weigh only through RCF's $5.91bn (P-B442802-03) | High on the text; no weights |

**Bottom line.** The claim "a sponsor setting, not a platform limit" is **not supported by the public record**. It is not refuted either:
- Ren describes DFX as providing "a secure, configurable interface for donors and program staff" (product descriptions, 2023-06-12).
- Program circulars do word the letter differently from one RCF template to another.

What the documents do show:
- Ren-platform donor guides have stated a **fund name only** default in every dated guide through February 2026. RCF letter-policy circulars of 2024–25 instead name the fund and the grant advisor [V wave 35B].
- The newest guide on RCF's portals moves seven RCF programs to **full contact including email**. That guide is a Ren-generic ‘Giving Platform Donor User Guide’: its text never names RCF or Renaissance, and it says ‘Ren does not send any notification’ [V wave 35B].

Under Clarity/EDF this fits "platform/organizational origin" better than donor choice. The open test is whether MS GIFT, BofA or CJP keep fund-name defaults once they show the 2026 guide (P-B442802-02).

## 1. Method

1. **Universe.**
   - **Ren-linked sponsors** are taken from [`relationship-graph-edges-consolidated-2026-11-19.csv`](../../data/mission-2026-11-14/relationship-graph-edges-consolidated-2026-11-19.csv). A scripted filter on "Ren", "Renaissance", "RenPSG", "Stellar", "iPhi" and "donorfirst" returns 194 edges, 42 of which name a donorfirst host. They cover:
     - RCF private labels: CE0011–CE0069, CE0245/6 and CE0915;
     - MS GIFT: CE0072, CE0168;
     - BofA CGF: CE0076, CE0169;
     - AEF: CE0078/9;
     - CJP: CE0903;
     - T. Rowe Price: CE0212;
     - GS: CE0163, CE0166;
     - Raymond James and other iPhi tenants: CE0755–CE0776;
     - Gulf Coast CF: CE0081.
   - **Host list.** All `*.donorfirstx.com` and `*.donorfirst.org` hosts named anywhere in `research/` and `data/` were collected (`grep -rhoE`). Hostnames in the circulars and channel pages were then probed as well (ubs, northwesternmutual, janney, aef).
   - **Assets** are FY2024 `daf_assets_eoy` from [`daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv) (`row_type=top50`, R1–R4 corrected), joined by EIN. They are attached only to the sponsor-of-record row (`asset_row=Y`), so private labels inside RCF are not double counted.
   - The market total ($323.27bn) is derived from the same file as `daf_assets_eoy ÷ share_daf_assets_eoy`.
2. **Collection.**
   - Each portal's public login page was fetched first, and every PDF it links was listed.
   - Guides, circulars, guidelines, brochures and FAQs were fetched. Forms were left out, except the RCF and RBC account-change forms, which were read and contain no acknowledgement text. So were investment policies, year-end calendars and crypto sheets.
   - RCF/Ren channel PDFs on `www.reninc.com` named in the repo were then fetched, along with sponsors' own sites (AEF, CJP, T. Rowe Price, MS GIFT, BofA, Edward Jones, Gulf Coast CF) and Ren's charity help centre.
   - There were no logins, forms or outreach.
3. **Robots.**
   - A stdlib fetcher (scratchpad `q4428/scripts/get.py`, UA `research-script/1.0`) fetched a URL only if robots.txt allowed both `*` and that UA.
   - A 404 robots.txt was treated as no rules. Any other failure (403, 500, DNS or connection error) was treated as blocked.
   - Every request is logged (§6).
4. **Text extraction and checks.**
   - PDFs were read with `pdftotext`; document dates come from `pdfinfo` (CreationDate/ModDate); HTML dates come from `article:modified_time` or `dateModified`.
   - A checker (scratchpad `q4428/scripts/verify.py`) confirmed that **all 33 quotes in the CSV occur verbatim** in the fetched sources, allowing for whitespace and curly-quote normalisation.
5. **Coding.**
   - `default_category` is what reaches the charity if the donor changes nothing. It uses the task's five categories plus "not determinable".
   - Where a text says the fund or account name always appears, and other details only at the donor's choice, it is coded **fund name only**. This is the stated floor, and it follows how b44n28-01 coded MS GIFT and Vanguard.
   - Where options are listed with no floor and no preselection, it is coded **no default stated**.
   - Where one program has two texts, the newest text describing the grant screen wins. The other is kept in `other_quote`/`other_reading`.
6. **Platform version.**
   - The login shell build was compared across the portals: the `amplifyui/<n>/components.js` path, the `mvc2?v=` bundle hash and the `site-isp.aspx?v=` CSS version.
   - Each guide was tagged by its template and vintage:
     - RCF DFX 10/2021;
     - CFN 5/2022 and SEI 4/2022;
     - `2309-RCF-FRM-DAF-DONORGUIDE` (©2023, PDFs 2024);
     - "Giving Platform Donor User Guide" (2026-10-06);
     - BofA's own guide (2025-11/2026-02).

## 2. Results by program

| ID | Program (portal) | Default | Email | Key document (date) |
|---|---|---|---|---|
| RCF-01 | RCF core (rcf.donorfirstx.com) | **full contact** | Y default | Giving Platform guide (2026-10-06). The circular (2026-07-23) lists options with no default |
| RCF-02 | Ameriprise (ampf) | full contact | Y | same guide; circular 2025-03 options |
| RCF-03 | RBC WM (rbcrcf) | full contact | Y | same guide; circular 2025-07 options |
| RCF-04 | MDRT Global Gift Fund (mdrt) | full contact | Y | same guide; circular 2024-04 "acknowledge the Fund and the Grant Advisor's involvement" |
| RCF-05 | RCF Giving Fund (rcfgivingfund) | full contact | Y | same guide; circular 2025-06 fund + advisor |
| RCF-06 | UBS (ubs) | full contact | Y | **Two guides on one portal:** 2026-10 (full contact) and 2024-06 "The default is 'Fund Name Only'" |
| RCF-07 | Northwestern Mutual | full contact | Y | same guide; circular 2024-07 options |
| RCF-08 | TDA legacy (tda) | **fund name only** | N | 2309 guide (2024-07-12): "The default is 'Fund Name Only'" |
| RCF-09 | Commonwealth (cfndaf; LPL) | **name only** | N | circular 2024-12: fund + grant advisor unless anonymous; 2022 guide lists options |
| RCF-10 | SEI Giving Fund (sei) | name only | N | brochure 2025-03: same wording; 2022 guide lists options |
| RCF-11 | Franklin Charitable Giving Program (ft) | fund name only (floor) | N | circular 2026-09: account name on each grant; rest "reflecting the donor's preference" |
| RCF-12 | Salvation Army DAF | fund name only (floor) | N | FAQ 2025-04: sub-fund name, "the recommender names you choose to include"; address by selection |
| RCF-13 | LPL channel | no default stated | N | circular 2309 (2023-10) options |
| RCF-14–17 | Edward Jones CGF; First Citizens DAF; Janney; Fisher and Pershing channels | not determinable | – | No guide or text on any public page |
| RCF-18 | Azzad (rcf.iphiview.com) | not determinable | – | iPhi robots `Disallow: /` [B] |
| MSG-01 | MS GIFT (msgift) | fund name only | N | Grantee Guidelines 2022-09. The live FAQ says "name of the Account, or Donor as specified" (V34A-26) |
| BOA-01 | BofA CGF (bofa.donorfirst.org) | fund name only | N | portal guide 2026-02-23. The 2024 guidelines say account + donor/advisor name (V34A-30) |
| AEF-01 | AEF (now Ren portal) | no default stated | N | FAQ modified 2026-02-19: "donor or account name (per your instructions)" |
| CJP-01 | CJP (cjp.donorfirstx.com) | fund name only | elected | Policies 2026-04-29 §4.5: identify "by the name of the Donor Advised Fund ... unless otherwise requested"; other details "each at your direction" |
| TRP-01 | T. Rowe Price PCG (pcg.donorfirstx.com) | no default stated | N | FAQ (live) and brochure 2026-11-10: name, account name and address on request, or anonymous |
| GCCF-01, OAK-01 | Gulf Coast CF; Oak (oak.donorfirst.org) | not determinable | – | no text; Oak's PDFs return 404 |
| GS-01, RJ-01, IPHI-00 | GS DAF; Raymond James; other iPhi tenants | not determinable | – | robots `Disallow: /` on gspf.goldman.com and on all 14 iPhi URLs [B] |

**Ren-wide statements** (not program rows):
- Ren's "Giving Season 2025 – commonly asked questions" (modified 2026-06-18) tells charities: "The donor's name appears on page two or three of the grant letter, unless the donor chose to give anonymously". On whether a charity can thank the donor: "if the donor did not provide the information this was intentional".
- Ren Recognize (2026-08-06) exists for grants "through Ren-powered donor-advised funds but did not include enough personal detail".
- Read together, these say that a name, but often no contact detail, reaches charities [F/I].

## 3. Platform-version test

### 3.1 One login build

All 17 reachable DFX/DonorFirst portals serve the same front-end build on 2026-11-19:
- `amplifyui/17570`;
- bundle `mvc2?v=l-gBG9wYhAn3…`;
- CSS `v=260210093200`.

The 17 are rcf, msgift, edwardjones, sei, mdrt, rbcrcf, ampf, cfndaf, ft, firstcitizensdaf, tda, gccf, cjp, rcfgivingfund, pcg, bofa.donorfirst.org and oak.donorfirst.org. Only the title and the linked PDFs differ.

This shows one login application for all tenants, including BofA and MS GIFT. It does **not** show the version of the grant-recommendation screen behind login. The repo records BofA-specific front-end and API hosts (CE0169) [R].

### 3.2 Stated defaults line up with guide vintage, not with sponsor

| Guide template / vintage | Programs whose documents use it | Stated acknowledgement default |
|---|---|---|
| RCF DFX User Guide 10/2021 (reninc.com, 2021-10-21) | RCF | none ("Issue it in the name of the fund, the primary donors, or a special recognition ...") |
| DFX User Guide CFN 5/2022, SEI 4/2022 | Commonwealth, SEI | none |
| MS GIFT Grantee Guidelines (2022-09) | MS GIFT | fund name (address on election) |
| `2309-RCF-FRM-DAF-DONORGUIDE` (©2023; PDFs 2024-06/07) | TDA portal, UBS portal | **"The default is 'Fund Name Only'"** |
| BofA "Guide to Navigating" (2025-11 / 2026-02) | BofA CGF | **"The default is Fund Name Only"** |
| "Giving Platform Donor User Guide" (2026-10-06) | RCF, Ameriprise, RBC, MDRT, RCF Giving Fund, UBS, Northwestern Mutual | **"By default ... name, email, and address"** |

- **Within a sponsor (RCF):** the default changes between vintages, from fund name only to full contact. The UBS portal still links both versions.
- **Across sponsors, same vintage:**
  - every document before 2026-10 that states a default says fund name (RCF, BofA, MS GIFT);
  - the 2026-10 guide is used only by RCF programs, and identically across all seven.
- **So no case was found of two sponsors on the same documented version with different defaults.** The variation the task asked about appears *between versions*, which is what a platform default would produce. A sponsor-level switch that happened to be flipped only by RCF at the 2026 migration would produce the same pattern, so public documents cannot separate the two [I].

**Context for the change.** Ren's charity release notes show a platform-level change to the fields charities see: "Add Email Address to Grants … Emails that are elected in the grant recommendation screen will now be surfaced" (2024 August Release; page dated January 15, 2025). The 2026 guide is the first donor guide that makes email part of the default [F].

### 3.3 Program-level text varies, which shows something is configurable

- **Letter-policy wording differs by RCF template.**
  - The older legal circular says "A letter accompanying the grant will acknowledge the Fund and the Grant Advisor's involvement unless the Grant Advisor wishes to remain anonymous". It is used by MDRT (2024-04), the RCF Giving Fund (2025-06), Commonwealth (2024-12) and SEI (2025-03).
  - The 2023 marketing circular (`2309-RCF-FRM-DAF-CIRC`) lists options with no default. It is used by Ameriprise, RBC, TDA, UBS, NWM, LPL and RCF.
  - Franklin's 2026 circular has its own text.
- **Within-program conflicts.** Five programs carry a UI default and a letter policy that imply different things:
  - BofA: "Fund Name Only" against "account name and the name of the Donor or Advisor";
  - MDRT, RCF Giving Fund, Commonwealth and SEI: the full-contact guide or an options-only guide against "Fund and Grant Advisor".
- **Ren's own description.** Ren sells "a branded technology portal", "branded grant checks with accompanying branded grant letter" and DFX as "a secure, configurable interface for donors and program staff" (Ren Inc. Product Descriptions, 2023-06-12).

So branding, letters and documents are set per program. Whether the acknowledgement *preselection* is also set per program is not documented [F/I].

### 3.4 Verdict on b44n28-01 §3.2

That section reads the BofA (2026-02) and RCF (2026-10) guides as showing "a configurable sponsor setting, not a platform constraint". The comparison is confounded by vintage: RCF's own 2024 guide said "Fund Name Only", like BofA.

Suggested wording for §3.2: "Ren-platform guides state a fund-name default through February 2026 (RCF 2024, BofA 2026-02, MS GIFT 2022). The Ren ‘Giving Platform’ guide of October 2026, linked unchanged from seven RCF portals, states name, email and address [V wave 35B]. Whether this is a sponsor setting or a platform change is unresolved (P-B4428-02)." This is a proposal only; no existing file was edited.

## 4. Email and contact

- **Default email** is documented only in the 2026 Giving Platform guide (7 RCF programs).
- **Elected email:** at CJP ("your email, each at your direction"); Ren's platform surfaces elected emails to charities.
- **Address:** opt-in at MS GIFT, the Salvation Army DAF and T. Rowe Price. It is in the default only under the 2026 guide. BofA, the circular-only programs and AEF do not mention it.
- **Anonymous by default:** none of the 18 determinable rows.

## 5. Asset share by default (computed by the script)

**A. Ren-administered sponsors** (Ren administers per the graph: RCF, MS GIFT, BofA CGF [administration inferred, technology confirmed] and AEF). RCF is coded by its 2026-10 guide.

| Default | Sponsors | FY2024 $bn | Share of set | Share of market |
|---|---|---|---|---|
| full contact | RCF | 5.91 | 21.0% | 1.83% |
| fund name only | MS GIFT; BofA CGF | 13.84 | 49.2% | 4.28% |
| no default stated | AEF | 8.38 | 29.8% | 2.59% |
| name only / anonymous / not determinable | – | 0.00 | 0.0% | 0.00% |
| **Total** | | **28.13** | 100.0% | **8.70%** |

**B. All Ren-linked sponsors in the FY2024 top 50** (A plus the technology tenants CJP, T. Rowe Price, GS DAF and Raymond James).

| Default | Sponsors | FY2024 $bn | Share of set | Share of market |
|---|---|---|---|---|
| full contact | RCF | 5.91 | 13.1% | 1.83% |
| fund name only | MS GIFT; BofA CGF; CJP | 15.77 | 34.9% | 4.88% |
| no default stated | AEF; T. Rowe Price | 8.97 | 19.9% | 2.78% |
| not determinable | GS DAF; Raymond James | 14.53 | 32.1% | 4.49% |
| name only / anonymous | – | 0.00 | 0.0% | 0.00% |
| **Total** | | **45.19** | 100.0% | **13.98%** |

**Sensitivity: RCF coded by its 2023–24 DFX guide ("Fund Name Only").**
- In set A, fund name only becomes **70.2%** ($19.76bn) and full contact **0%**.
- In set B, fund name only becomes **48.0%** ($21.69bn).

The RCF figure is an upper bound in any case. Of RCF's 18 program rows, only 7 sit under the full-contact guide; 5 are coded name only or fund name only from their own texts, 1 has no default stated and 5 are unknown. The repo has no program-level split of RCF's $5.91bn.

**Not in the asset tables:**
- Gulf Coast CF is not in the FY2024 top 50.
- NPT runs on Ren's GivingPoint but administers itself. It is coded "no default stated" in b44n28-01.

## 6. Limits

- **Documents, not screens.** No login was used. A guide's "default" is the sponsor's published description. Live screens may differ, and the UBS portal links two contradictory guides.
- **Blocked.**
  - gspf.goldman.com (`Disallow: /`).
  - Every iPhi/Stellar host tried: 14 URLs, including Raymond James, Azzad, CAFAmerica, Stifel, Thrivent, Johnson CGF and KofC. These serve robots.txt ending `User-agent: * Disallow: /`.
  - www.raymondjamescharitable.org, www.stifelcharitable.org and www.johnsoncharitablegiftfund.org (robots.txt unreachable).
  - semo.donorfirstx.com (robots 500).
  - jcfny.donorfirst.org and jewishfed.donorfirst.org (no longer resolve).
  So the "iPhi / Stellar CF tenants" in the task could not be read at all.
- **Absent.** Edward Jones, First Citizens, Janney, Gulf Coast CF and Oak portals link no guide; Fisher and Pershing channel pages carry no acknowledgement text.
- **The MS GIFT 2024 Donor Circular** is font-encoded (no extractable text), as b44n28-01 found.
- **Floor-as-default coding** (Franklin, Salvation Army, CJP) is a judgement. Coding these "no default stated" would move CJP's $1.93bn (4.3% of set B) from fund name only to no default stated.
- **The CJP recoding** departs from b44n28-01, which coded CJP "donor chooses; no default stated". The same PDF has both texts: §4.5 (formal policy) states the fund-name rule, and the donor-facing notification section lists details ‘each at your direction’. Applied to b44n28-01, the recoding moves CJP's 0.77% of top-20 assets from no stated default (20.9% to 20.1%) to withholding (17.2% to 17.9%); that study has not been recoded [V wave 35B].
- **AEF's FAQ** may predate its 2026 migration to the Ren portal (the charity portal launched in Q2 2026 per AEF's page).
- **Ren roles** are taken from the relationship graph. BofA administration by Ren is "inferred, weakened" there (CE0076).

## 7. Robots and access log (2026-11-19)

There were 177 requests:
- 121 fetched with HTTP 200 (70 on hosts whose robots.txt is 404, 51 explicitly allowed);
- 11 allowed but the page was 404;
- 15 not fetched because robots disallowed them (14 iPhi/Stellar URLs and gspf.goldman.com);
- 1 not fetched because robots returned 500 (semo);
- 29 not fetched because robots.txt was unreachable (DNS or connection failure): 26 DFX/DonorFirst hostnames that do not resolve (22 guessed, 4 listed in the repo) and three sponsor sites.

The full log is in the scratchpad (`q4428/log.jsonl`).

| Host | robots.txt | Result |
|---|---|---|
| rcf, ampf, rbcrcf, mdrt, rcfgivingfund, ubs, northwesternmutual, tda, cfndaf, sei, ft, msgift, cjp, edwardjones, firstcitizensdaf, janney, gccf, pcg, aef `.donorfirstx.com` | 404 | fetched (cjp application PDF 404) |
| bofa.donorfirst.org, oak.donorfirst.org | 404 | fetched (oak PDFs 404) |
| semo.donorfirstx.com | 500 | blocked |
| jcfny.donorfirst.org, jewishfed.donorfirst.org, 25.donorfirstx.com, 25.donorfirst.org | unreachable | not fetched |
| www.reninc.com | 200, allowed | fetched (4 old PDFs now 404) |
| intercom.help (Ren Help Center) | 200, allowed | fetched (3 articles 404) |
| renaissancecharitable.org, www.aefonline.org, ma.cjp.org, www.bankofamerica.com, www.morganstanley.com, www.edwardjones.com, gccf.org, cafamerica.org, www.thriventcharitable.com, www.azzad.com, www.gs.com | 200, allowed | fetched |
| www.trowepricecharitable.org, 8hxvw8tw.media.zestyio.com, www.gulfcoastcf.org | 404 | fetched |
| gspf.goldman.com | 200, `Disallow: /` | blocked |
| rj, rcf (/azzad), sci, cafa, jcgf, ccfnj, infaith, tmf, cfgm, spmf, cfl, dmf `.iphiview.com`; www.iphiview.com; iphi.stellartechsol.com | 200, `User-agent: * Disallow: /` | blocked |
| www.raymondjamescharitable.org, www.stifelcharitable.org, www.johnsoncharitablegiftfund.org | unreachable | not fetched |

## 8. Data dictionary: `ren-private-label-defaults-2026-11-19.csv`

| Column | Meaning |
|---|---|
| `program_id` | Row key. RCF-nn are RCF-sponsored or RCF-serviced programs; other prefixes are sponsors |
| `program`, `sponsor_of_record`, `sponsor_ein` | Program name, legal sponsor and its EIN (blank if not identified) |
| `asset_row` | Y if this row carries the sponsor's FY2024 assets. Only one row per EIN does |
| `ren_role` | Ren's role per the relationship graph or the source: administers, technology provider, iPhi tenant |
| `portal_host` | Donor portal host |
| `platform_version` | Template and vintage of the document used (§1.6) |
| `default_category` | full contact / name only / fund name only / anonymous / no default stated / not determinable (§1.5) |
| `default_detail` | Plain-language summary |
| `email_included` | Y (default) / elected / N / unknown |
| `default_quote`, `default_url`, `default_doc_date`, `default_doc_sha1_12` | Verbatim evidence, primary URL, PDF Creation/ModDate or page date, and the first 12 hex digits of the PDF's SHA-1 |
| `other_quote`, `other_url`, `other_doc_date`, `other_reading` | A second first-party text for the same program and how it would code |
| `access_robots` | robots.txt result for the hosts used |
| `evidence_label` | F, F (medium), absent, blocked |
| `repo_prior` | Prior repo row or edge |
| `change_vs_repo` | NEW / confirms / CHANGES / gap |
| `fy2024_daf_assets_usd` | League-table FY2024 `daf_assets_eoy` (asset rows only) |
| `share_of_ren_linked_assets` | Assets ÷ $45.19bn (set B) |
| `share_of_market_fy2024` | Assets ÷ $323.27bn corrected market total |
| `retrieved` | 2026-11-19 |

## 9. Source register (primary URLs)

| # | Source | Date | URL |
|---|---|---|---|
| S1 | Giving Platform Donor User Guide (identical on 7 RCF portals) | 2026-10-06 | https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf (also /ampf/, /rbcrcf/, /mdrt/, /rcfgivingfund/, /ubs/, /northwesternmutual/ paths in CSV) |
| S2 | RCF Advisor User Guide (same acknowledgement text) | 2026-11-04 | https://rcf.donorfirstx.com/pdf/RCF/Advisor%20User%20Guide.pdf |
| S3 | RCF Program Circular | 2026-06-01 / 2026-07-23 | https://rcf.donorfirstx.com/pdf/RCF/RCF%20Program%20Circular.pdf |
| S4 | RCF Donor User Guide, template 2309 (TDA portal) | 2024-07-12 | https://tda.donorfirstx.com/pdf/tda/RCF%20Donor%20User%20Guide.pdf |
| S5 | UBS Donor User Guide, template 2309 | 2024-06-14 | https://ubs.donorfirstx.com/pdf/UBS/UBS%20Donor%20User%20Guide.pdf |
| S6 | RCF DFX User Guide 10/2021 | 2021-10-21 | https://www.reninc.com/wp-content/uploads/2022/02/Donor-User-Guide-RCF-Rebranded-10-21-Updated-2-3.pdf |
| S7 | Ameriprise, RBC, UBS, NWM, TDA program circulars (2309-RCF-FRM-DAF-CIRC) | 2024-06 to 2025-07 | https://ampf.donorfirstx.com/pdf/AMPF/Program%20Circular.pdf ; https://rbcrcf.donorfirstx.com/pdf/RBC/Program%20Circular.pdf ; https://ubs.donorfirstx.com/pdf/UBS/Program%20Circular.pdf ; https://northwesternmutual.donorfirstx.com/pdf/NWM/Program%20Circular.pdf ; https://tda.donorfirstx.com/pdf/tda/RCF%20Program%20Circular.pdf |
| S8 | LPL circular | 2023-10-11 | https://www.reninc.com/wp-content/uploads/2026/05/2309-RCF-FRM-DAF-LPLCircular.pdf |
| S9 | MDRT Program Circular | 2024-04-12 | https://mdrt.donorfirstx.com/pdf/mdrt/Program%20Circular.pdf |
| S10 | RCF Giving Fund Circular | 2025-06-28 | https://rcfgivingfund.donorfirstx.com/pdf/RCFGF/RCF%20Giving%20Fund%20Circular.pdf |
| S11 | Commonwealth Charitable Fund Program Circular; CFN DFX User Guide | 2024-12-13; 2023-04-10 | https://cfndaf.donorfirstx.com/pdf/CFNDAF/Program%20Circular.pdf ; https://cfndaf.donorfirstx.com/pdf/cfndaf/CFNDAF%20Donor%20User%20Guide.pdf |
| S12 | SEI Giving Fund Brochure; SEI DFX User Guide | 2025-03-18; 2023-03-15 | https://sei.donorfirstx.com/pdf/SEI/SEI%20Giving%20Fund%20Brochure.pdf ; https://sei.donorfirstx.com/pdf/SEI/SEI%20Donor%20User%20Guide.pdf |
| S13 | Franklin Charitable Giving Program Donor Program Circular | 2026-09-04 | https://ft.donorfirstx.com/pdf/ft/Donor%20Program%20Circular.pdf |
| S14 | Salvation Army DAF Grants FAQ (RCF) | 2025-04-14 | https://8hxvw8tw.media.zestyio.com/-2025--TSA_Grants-FAQ.pdf |
| S15 | MS GIFT Grantee Guidelines; MS GIFT program page FAQ | 2022-09-22; live | https://msgift.donorfirstx.com/pdf/MSGIFT/Grantee%20Guidelines.pdf ; https://www.morganstanley.com/gift |
| S16 | BofA CGF Guide to Navigating Your DAF; Program Guidelines 2024 | 2026-02-23; 2024-09-18 | https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf ; https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf |
| S17 | AEF FAQs for individual donors; AEF charities page | 2026-02-19; live | https://www.aefonline.org/thought-leadership/faqs-individual-donors/ ; https://www.aefonline.org/charities/ |
| S18 | CJP DAF Policies and Procedures | 2026-04-29 | https://ma.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf |
| S19 | T. Rowe Price Charitable FAQ; GIVE brochure | live; 2026-11-10 | https://www.trowepricecharitable.org/information/frequently-asked-questions.html ; https://www.trowepricecharitable.org/content/dam/pcg-site/pdfs/GIVE%20Brochure.pdf |
| S20 | Ren Inc. Product Descriptions ("configurable interface", branded letters) | 2023-06-12 | https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf |
| S21 | Ren Help Center, 2024 August Release (email surfaced) | page dated 2025-01-15 | https://intercom.help/rengiving/en/articles/9791601-2024-august-release |
| S22 | Ren Help Center, What is Ren Recognize? | 2026-08-06 | https://intercom.help/rengiving/en/articles/12582141-what-is-ren-recognize |
| S23 | Ren, Giving Season 2025 commonly asked questions | modified 2026-06-18 | https://www.reninc.com/giving-season-2025-commonly-asked-questions/ |
| S24 | Renaissance Charitable FAQ (anonymity) | modified 2026-01-21 | https://renaissancecharitable.org/faqs/ |
| S25 | DFX/DonorFirst login pages (build markers) | live | https://rcf.donorfirstx.com/ and the 16 other portal roots in §3.1 |
| S26 | League table FY2024 (assets) | repo | data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv |
