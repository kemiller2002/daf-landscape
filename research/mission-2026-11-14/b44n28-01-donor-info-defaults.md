# P-B44N28-01: what donor information a top-20 sponsor sends by default

- **Task:** P-B44N28-01 (queued in [gap19-clarity-edf-new-findings.md](gap19-clarity-edf-new-findings.md) §3, step 6 "Not observed").
- **Date:** 2026-11-19. All pages were read on that date unless stated.
- **Data:** [`data/mission-2026-11-14/donor-info-defaults-top20-2026-11-19.csv`](../../data/mission-2026-11-14/donor-info-defaults-top20-2026-11-19.csv). It has 20 rows, one per sponsor, and every field carries a quote, a URL and a source date.
- **Queue:** [`data/mission-2026-11-14/queue-proposals-b44n28-01.csv`](../../data/mission-2026-11-14/queue-proposals-b44n28-01.csv) (5 rows).
- **Universe:** the FY2024 top 20 by DAF assets in [`daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv) (`fiscal_year=2024`, `row_type=top50`, R1–R4-corrected `daf_assets_eoy`). Together they hold **$250.63bn**.
  - The ranks differ slightly from those in `sponsor-terms-census-top20-2026.csv`. For example, AEF and MS GIFT swap places at 7 and 8, and Dechomai moves from rank 18 to 20. The set of 20 sponsors is the same in both files.

## 0. Answer

| Question | Finding | Confidence |
|---|---|---|
| **Do the top-20 sponsors withhold donor contact data by default?** | **Neither rule holds. Full contact is the documented default for 33.2% of top-20 assets, and withholding (name or fund name only) for 17.2%. The default is undocumented for 44.6%: no default is stated at NPT, AEF and CJP (20.9%), and the five not-determinable sponsors hold 23.7%. A documented required choice covers only 5.0% (SVCF, JCF).** [V wave 34A]<br>- **Full contact by default:** 5 sponsors with **33.2%** of top-20 assets (Fidelity, RCF, NCF, ImpactAssets, FFTC).<br>- **Contact withheld by default (name only or fund name only):** 5 sponsors with **17.2%** (Vanguard, MS GIFT, BofA CGF, GKCCF; CCT is name only).<br>- **Donor must choose (documented: SVCF, JCF, 5.0%) or no default stated (NPT, AEF, CJP, 20.9%):** 5 sponsors with **25.9%**. An unstated default is not evidence that the donor must choose [V wave 34A]<br>- **Not determinable:** 5 sponsors with **23.7%**. Two are blocked by robots (DAFgiving360, Raymond James Charitable). GS DAF is blocked too, and its only public circular is from 2008, before the 2021 evidence cutoff. Greater Horizons and Dechomai publish no relevant text. | High for the 15 determinable rows (first-party text). The asset shares hinge on DAFgiving360. Its 2024 policy lists options without a default, but says it ‘does not release the account holder's name and contact information to any recipient charity without the account holder's explicit consent’, which leans toward withholding when no choice is made [V wave 34A] [V wave 35B]
| **No sponsor defaults to anonymous** | **0 of 20.** Anonymity is opt-in everywhere it is documented: per grant at all 15 determinable sponsors, and also fund-wide at SVCF, CCT and FFTC. | High |
| **Largest single fact** | **Fidelity Charitable preselects full acknowledgement (name, address, fund name) on every grant.** Its 2025 grants went out **80% with donor name and address, 15% with the fund name only and 5% anonymous** (2026 Giving Report). Fidelity alone holds 26.4% of top-20 assets. | High |
| **The DAFRC survey baseline (CF-weighted)** | DAFRC found 36% of sponsors default to full contact (count basis, n=128, 86% CFs). The top-20 count is **5 of 15 determinable sponsors (33%)**, close to DAFRC. On an asset basis the full-contact share is **43.6% of determinable assets**, because Fidelity dominates. | Medium. The categories are not identical to DAFRC's |
| **Charity gets email or address?** | **Postal address is the norm. Email is rare.**<br>- **Address by default:** Fidelity, RCF, NCF, ImpactAssets, FFTC.<br>- **Address on election:** SVCF (required choice at opening), MS GIFT, NPT, CJP, Vanguard, DAFgiving360 (2024 policy).<br>- **Donor email:** documented as a default only at **RCF**. At CJP and GKCCF it is shared at the donor's choice. | High (first-party), but limited to the text found |
| **API or rail data sharing** | **Four sponsors pass donor-permitted data through a third-party or shared rail:**<br>- Fidelity: DAF Direct, plus Stripe/ACH reports.<br>- DAFgiving360: DAF Direct, plus a Chariot DAFpay access method launched 2026-05-31.<br>- NPT and Vanguard: PayPal Grant Payments.<br>Chariot lists Fidelity and "Ren (Pinkaloo)" as charity-side *managed sources*. **No other top-20 sponsor documents an API or shared rail for donor data.** | High on what is documented; absence is "not found" |

**Verdict on the earlier finding.** The gap19 Clarity note G12-2 framed the outcome as "withheld donor contact data by default", based on the DAFRC sponsor survey. At the top 20 that framing is **too strong as a rule, and so is its opposite, because the default is undocumented for 44.6% of top-20 assets**. Specifically [V wave 34A]:

- the single largest sponsor defaults to full contact;
- the next three (NPT, DAFgiving360, Vanguard) split between "donor chooses", "unknown" and "fund name only".

The G12-2 reconsider-trigger was "P-B44N28-01 shows the top-20 nationals already default to full contact". It is **partly met**. Fidelity, RCF and NCF do default to full contact. Vanguard, MS GIFT and BofA do not, and DAFgiving360 is unobserved. The classification "mixed, leaning habit" stands. The variation is again large under one law, and it also appears on a single vendor platform (Ren; §3.2), where the stated default tracks guide vintage rather than sponsor (b4428-02) [V wave 35B]. An entrant's edge is smaller against Fidelity, RCF and NCF and intact against fund-name-default sponsors (§4).

## 1. Method

1. **Universe.** Took the FY2024 top 20 from the league table (above). Asset shares are computed by script ([`scripts/mission_b44n28_donor_info_build.py`](../../scripts/mission_b44n28_donor_info_build.py), which reproduces the CSV byte for byte) as each sponsor's `daf_assets_eoy` over the top-20 total [V wave 34A].
2. **Repo first.** Searched `research/` and `data/` for the terms "donor contact", "withheld", "anonym" and "donor-information". The prior evidence reused is:
   - [`anonymity-data-flow-2026.csv`](../../data/mission-2026-11-14/anonymity-data-flow-2026.csv), rows A10–A16;
   - [`nonprofit-side-panel-2026-evidence.csv`](../../data/mission-2026-11-14/nonprofit-side-panel-2026-evidence.csv) and [`nonprofit-side-panel-2026-cf-supplement.csv`](../../data/mission-2026-11-14/nonprofit-side-panel-2026-cf-supplement.csv), field `remittance_donor_identity`;
   - [queue-batch36-anonymity-feeds-fees.md](queue-batch36-anonymity-feeds-fees.md) §1;
   - [direction-nonprofit-side-experience.md](direction-nonprofit-side-experience.md) §2.1 (the DAFRC defaults);
   - [gap19-clarity-edf-new-findings.md](gap19-clarity-edf-new-findings.md) §3;
   - [queue-infrastructure-nonprofit-costs-emerging.md](queue-infrastructure-nonprofit-costs-emerging.md) Q-B18 (DAF Direct).
3. **Sources allowed.** Only public sponsor help pages, FAQs, program policies or circulars, grant-recommendation walkthroughs (portal user guides with screenshots) and blank forms. There were no logins, forms or outreach.
4. **Robots.** A stdlib fetcher (`scripts/get.py` in the scratchpad) worked as follows:
   - it read each host's robots.txt and fetched only if both `*` and the generic UA `research-script/1.0` were allowed;
   - a robots.txt that returned 404 was treated as no restriction;
   - any other non-200 response was treated as blocked;
   - every request is logged in §6.
   Search-engine snippets were used only to find URLs. They were never used as evidence, except one item marked [R] in the Raymond James row.
5. **Coding.**
   - **`default_category`** is what reaches the charity if the donor changes nothing on the grant recommendation. It uses one of the task's categories: full contact (name plus postal address or email), name only, fund name only, anonymous, or donor must choose. Where the text gives options but no preselection, the code is "donor chooses; no default stated".
   - **`default_bucket`** collapses this for the asset summary.
   - **Conflicts between documents.** The newest document that describes the donor's screen wins, and the conflict is recorded (BofA).
6. **Evidence labels.** F means first-hand text. "blocked" means robots refusal. "absent" means pages were read but held no relevant text. [R] means a search snippet only.

## 2. Results by sponsor

| # | Sponsor | FY2024 $bn | Default reaching the charity | Must donor choose? | Email / address to charity | Rail or API data sharing |
|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable | 66.20 | **Full contact:** name, address and Giving Account name preselected | No (default; changeable per grant or by phone) | Address yes; email not stated | DAF Direct; Stripe/ACH reports; Chariot managed source |
| 2 | NPT | 42.12 | **Donor chooses** any combination of fund name, advisor names and address; no default stated | Acknowledgment preference is a step | Address if selected | PayPal Grant Payments (donor-selected PII) |
| 3 | DAFgiving360 | 40.94 | **Not determinable.** Live site blocked. The 2024 policy lists 3 options with no default, and under §1.5 that text alone would code ‘no default stated’, as NPT is coded. It adds that DAFgiving360 ‘does not release the account holder's name and contact information ... without the account holder's explicit consent’ [V wave 34A] [V wave 35B] | Unknown | Address if chosen | DAF Direct; DAFpay access method (2026-05-31) |
| 4 | Vanguard Charitable | 21.95 | **Fund name only**: "account name will appear … unless anonymity is requested" | No | Only if donor adds personal info | PayPal Grant Payments |
| 5 | GS DAF | 12.64 | **Blocked** (robots `Disallow: /`) | Unknown | Unknown | None found |
| 6 | SVCF | 9.58 | **Set at opening:** advisor names as specified; address is a required "Choose one" election | Yes, at account opening | Address only if elected | None found |
| 7 | MS GIFT | 9.11 | **Fund name only:** letter identifies the DAF name unless anonymous | No; address opt-in | Address if elected | None found |
| 8 | AEF | 8.38 | **Donor chooses:** "donor or account name (per your instructions)" | Unknown (form not public) | Not stated | None found |
| 9 | RCF | 5.91 | **Full contact including email:** ‘By default … name, email, and address’ (Ren ‘Giving Platform’ guide on RCF's portal, 2026-10-06). The RCF Program Circular (PDF modified 2026-07-23) lists options with no default, RCF's own 2023–24 guide says ‘The default is Fund Name Only’, and private-label programs such as TSA's carry their own defaults, so this is an upper bound for RCF's $5.91bn. Coded by the 2023–24 guide, top-20 full contact would be 30.9% and withholding 19.5% [V wave 34A] | No [V wave 35B] | **Email and address by default** | "Ren (Pinkaloo)" as Chariot managed source (not RCF-specific) |
| 10 | NCF | 5.68 | **Full contact:** fund name "alongside your name and address" | No | Address yes | None found |
| 11 | BofA CGF | 4.73 | **Fund name only** (medium confidence: the governing Program Guidelines, Version 8.2025 of 2025-09-08, still say distributions carry ‘the account name and the name of the Donor or Advisor, unless anonymity is requested’; the portal guide’s screen default is coded, b4428-04) [V wave 48A] "The default is Fund Name Only" | No | Only via custom acknowledgement | None found |
| 12 | Chicago Community Trust | 4.65 | **Name only:** letter names the DAF advisor unless anonymous | No | Not stated | None found |
| 13 | ImpactAssets | 2.90 | **Full contact:** donor and joint advisor name and address | No online; paper form says "select one" | Address yes | None found |
| 14 | Jewish Communal Fund | 2.87 | **Donor must choose:** fund name plus signers' or named names and addresses, or anonymous | Yes (no preselected box) | Address unless anonymous | None found |
| 15 | FFTC | 2.62 | **Full contact:** fund name plus advisor name and address | No | Address yes | None found |
| 16 | GKCCF | 2.57 | **Fund name only:** name and email ‘encouraged’, donor decides. GKCCF also says the check stub ‘will likely include the donor's name and contact information (typically an email address)’. Coded the way CJP is, this would be ‘no default stated’, and the withheld share would fall to 16.1% [V wave 34A] | Unknown [V wave 35B] | Email typically if shared | None found |
| 17 | Greater Horizons | 2.53 | **Not determinable** (no public text) | Unknown | Unknown | None found |
| 18 | CJP | 1.93 | **Donor chooses** (but Policies §4.5 state a fund-name rule ‘unless otherwise requested’; coded by it, as in b4428-02, withholding would be 17.9% and no stated default 20.1%) [V wave 35B] DAF name, name, address and email "each at your direction" | Yes? | Address and email at donor direction | None found |
| 19 | Raymond James Charitable | 1.89 | **Blocked** (robots 403) | Unknown | Unknown | None found |
| 20 | Dechomai Asset Trust | 1.43 | **Not determinable** (no public text) | Unknown | Unknown | None found |

The quotes, URLs and source dates for every cell are in the CSV.

## 3. Summary by assets

Computed by `build.py` from the CSV. The asset field is the FY2024 `daf_assets_eoy` from the league table.

| Default bucket | Sponsors (n) | FY2024 DAF assets ($bn) | Share of top-20 assets | Share of determinable assets | Sponsors |
|---|---|---|---|---|---|
| Full contact | 5 | 83.31 | 33.2% | 43.6% | Fidelity Charitable; Renaissance Charitable Foundation; National Christian Foundation; ImpactAssets; Foundation For The Carolinas |
| Name only | 1 | 4.65 | 1.9% | 2.4% | The Chicago Community Trust |
| Fund name only | 4 | 38.37 | 15.3% | 20.1% | Vanguard Charitable; Morgan Stanley GIFT; Bank of America Charitable Gift Fund; Greater Kansas City Community Foundation |
| Anonymous | 0 | 0.00 | 0.0% | 0.0% | |
| Donor must choose / no default stated | 5 | 64.88 | 25.9% | 33.9% | National Philanthropic Trust; Silicon Valley Community Foundation; American Endowment Foundation; Jewish Communal Fund; Combined Jewish Philanthropies (CJP) |
| Not determinable | 5 | 59.43 | 23.7% | n/a | DAFgiving360; Goldman Sachs Philanthropy Fund (GS DAF); Greater Horizons; Raymond James Charitable; Dechomai Asset Trust |
| **Total** | 20 | 250.63 | 100.0% | determinable = 191.20 (76.3%) | |

- **Count basis:** 5 of 15 determinable sponsors (33%) default to full contact.
- **Asset basis:** full contact is 33.2% of top-20 assets. Contact is withheld by default (name only, fund name only or anonymous) at 17.2% of top-20 assets. On determinable assets the shares are 43.6% full contact and 22.5% withheld.
- **Sensitivity to DAFgiving360 (16.3% of top-20 assets).**
  - If its default is full contact, the full-contact share rises to **49.6%** of top-20 assets: (83.31 + 40.94) / 250.63.
  - If its default is name only or fund name only, the withheld share rises to **33.5%**: (43.02 + 40.94) / 250.63.
  - Either way, **no reading makes contact-withholding the asset-weighted majority** unless the ‘donor chooses’ sponsors effectively send no contact data. That condition is not remote. If DAFgiving360's explicit-consent clause means no contact without an election, and NPT, AEF and CJP likewise send none unless it is chosen, withholding when no choice is made would cover 33.5% + 20.9% = 54.4% of top-20 assets. The asset-weighted answer is therefore open, not settled against withholding [V wave 34A] [V wave 35B]

### 3.1 What changes from the repo

| Repo statement | Where | This pass | Change |
|---|---|---|---|
| "Withheld donor contact data by default" (outcome E, G12-2), from DAFRC 36/24/35/1 | [gap19-clarity-edf-new-findings.md](gap19-clarity-edf-new-findings.md) §3; [industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md) §6 | Top 20: full contact 33% by count (≈DAFRC 36%). **Asset-weighted it is 33–50% depending on DAFgiving360.** Fund-name-or-name-only is 17–34% | **Weakens** the headline for the nationals. Recommended wording: ‘defaults vary. A documented full-contact default covers 33–50% of top-20 assets and a documented withholding default 17–34%; both ranges turn on DAFgiving360. The default is undocumented for the rest, and no top-20 sponsor defaults to anonymous’ [V wave 34A] [V wave 35B] |
| Fidelity: "donor-permitted only" | anonymity-data-flow A13; nonprofit-side-panel `fidelity` | Permission is **preselected**: full acknowledgement is the default on every grant. 80/15/5 in 2025 | **Adds** the default and outcome data |
| RCF: "sub-fund name on the grant letter unless anonymous" [S] | nonprofit-side-panel `rcf_ren` (Salvation Army FAQ) | The Ren ‘Giving Platform’ guide on RCF's portals (2026-10) defaults to **name, email and address**; RCF's 2023–24 guide said Fund Name Only (b4428-02) [V wave 35B] | **Changes** the RCF coding. The TSA FAQ is one private-label program |
| SVCF: "address only if requested" | cf-supplement `cf_svcf` | The address is a **required "Choose one"** election at opening | **Refines** |
| AEF: "not found" | nonprofit-side-panel `aef` | "donor or account name (per your instructions)"; anonymity on the form | **Fills** the gap (default still unstated) |
| NPT, Vanguard, FFTC, CCT, NCF | panel and cf-supplement | Same text re-read | **Confirms**. NCF adds that name and address appear by default |
| DAFRC "35% fund name only" read as a national pattern | direction-nonprofit-side-experience §2.1 | 4 of 15 determinable top-20 sponsors (15.3% of assets) default to fund name only | **Consistent** in count; not dominant by assets |

### 3.2 A vendor platform shows two defaults, by guide vintage [V wave 35B]

Both portals run on Ren's platform (Ren's administration of BofA CGF is inferred, CE0076), and their guides from 2025–26 give different defaults (b4428-02 §3.2) [V wave 35B]:

- BofA's DonorFirst guide says "The default is Fund Name Only" (PDF modified 2026-02-23).
- The Ren ‘Giving Platform Donor User Guide’ on RCF's portal (the same file, SHA-1 93d97b49e84a, on seven RCF portals; its text names Ren, not RCF) says the default [V wave 35B] "includes the grant advisor's name, email, and address" (PDF 2026-10-06).
- MS GIFT, also Ren back-office, states a fund-name default in its 2022 Grantee Guidelines.
- RCF's own earlier guide (template 2309-RCF-FRM-DAF-DONORGUIDE, ©2023; TDA PDF 2024-07-12, UBS PDF 2024-06-14) says ‘The default is Fund Name Only’, as BofA's does [V wave 35B].

These documents do not show a configurable sponsor setting. BofA's 2026-02 guide and RCF's 2023–24 guide state the same fund-name default, and the full-contact text comes from a newer Ren platform guide, so the two defaults differ by guide vintage, not by sponsor. Whether the change is a sponsor setting or a platform release is unresolved. Under EDF the variation still points to organizational or platform origin, not law (P-B4428-02; b4428-02 §3.4) [V wave 35B]. It supports G12-2's "organizational origin, leaning habit". The question is queued as P-B4428-02.

### 3.3 Outcomes, where published

- **Fidelity 2026 Giving Report:**
  - donor name and address: 83% (2020), 80% (2024), 80% (2025);
  - Giving Account name only: 13%, 15%, 15%;
  - anonymous: 4%, 5%, 5%.
  The nonprofit FAQ still says 4% anonymous.
- **Vanguard's nonprofit page** gives both "Only 4%" and "Only 5% of grants are completely anonymous".
- **GKCCF** says anonymity is "rare".
- No sponsor with a fund-name default publishes a disclosure split (P-B4428-03). The sponsor-stats pass confirms it: Vanguard publishes an anonymous share only. Fidelity’s 2022–2024 reports add 82/14/4 (2021), 81/15/4 (2022) and 81/15/4 (2023), so full contact eased from 83% to 80% over 2020–2025 while anonymity stayed at 4–5%. At most 80% of Fidelity’s 2025 grants kept the full-contact default; that is a bound, not a measured retention rate (b4013-b4428) [V wave 39A]

### 3.4 Email and direct contact

- **Email.** Postal address is the field most documents name. Only RCF names donor **email** in its default.
- **Charity able to contact the donor.** Sponsors that send an address say so for the charity's benefit: FFTC shares it "so that the nonprofit may send an acknowledgement", and Fidelity says the charity "may also" acknowledge directly.
- **Restriction.** DAFgiving360's 2024 policy bars donor enclosures with grant checks.
- **Tools for the donor to add contact details:**
  - custom acknowledgements (BofA, RCF, ImpactAssets);
  - an optional "notify an individual not on the fund" (JCF);
  - free-text purpose (AEF);
  - DAFpay's donor-confirmed contact details (DAFgiving360).

## 4. Implications

- **For the Clarity G12-2 entry.**
  - Keep "mixed, leaning habit".
  - Replace the outcome sentence with the asset-weighted range above.
  - Change "Not observed: the defaults at the top-20 national sponsors" to "observed for 15 of 20 (76% of assets); DAFgiving360, GS DAF and Raymond James blocked".
- **For an entrant.** The consent-first design proposed in G12-2 still differs from:
  - fund-name defaults (Vanguard, MS GIFT, BofA), which hold 14.3% of top-20 assets (15.3% with GKCCF; BofA's governing Program Guidelines, Versions 3.2024 and 8.2025 alike, would make it name only, with the withheld share unchanged [V wave 48A]) [V wave 34A];
  - option lists with no default (NPT, AEF, JCF, CJP).
  It does not differ from Fidelity, RCF, NCF, ImpactAssets or FFTC, which already preselect contact sharing.
- **For nonprofits.** At the five full-contact sponsors the remaining gap is email, not identity: only RCF sends email by default.

## 5. Limits

- **Blocked or absent sources.**
  - Three sponsors are blocked: DAFgiving360 (robots 403), GS DAF (robots `Disallow: /`) and Raymond James Charitable (robots 403). Together they are 22.1% of top-20 assets.
  - Two publish nothing relevant: Greater Horizons and Dechomai (1.6%).
  - The CCT nonprofit guide (www.cct.org, robots 403) is carried from the repo, not re-read.
- **"Default" means documented text, not observed screens.** No logged-in walkthrough was possible. Where a guide shows a screenshot (BofA, RCF), it is the sponsor's own published walkthrough. Online forms may preselect differently from paper forms (ImpactAssets, JCF).
- **Dates.**
  - The ImpactAssets FAQ is from 2021 (corroborated by the 2025 form). MS GIFT's Grantee Guidelines are from 2022, JCF's form from 2022 and AEF's process sheet from 2021. All are within the 2021+ rule.
  - DAFgiving360's policy is from 2024.
  - MS GIFT's Aug 2024 Donor Circular could not be read: its PDF text is font-encoded.
- **Category judgement.**
  - SVCF is coded "set at opening", and GKCCF is coded "fund name only" even though it encourages contact.
  - BofA's governing Program Guidelines (Version 8.2025, September 2025) name the account and the donor or advisor; its portal guide (February 2026) defaults the check acknowledgement to the fund name only. The screen default is used at medium confidence; both withhold address and email, so the 17.2% withheld share is unchanged (b4428-04) [V wave 48A]
- **Ranks.** The league table and the terms census order ranks 5–20 slightly differently. Shares use the league table only.
- **Absence of APIs** means no public documentation was found. It does not mean no integration exists.

## 6. Robots and access log (2026-11-19)

The fetcher made 76 requests in all:

- 55 allowed and fetched (HTTP 200);
- 11 on hosts with no robots.txt (404), fetched;
- 3 allowed but the page was 404;
- 6 not fetched because robots.txt returned 403;
- 1 not fetched because robots disallowed it.

| Host | robots.txt | Result |
|---|---|---|
| fidelitycharitable.org, www.fidelitycharitable.org | 200, allowed | fetched |
| www.nptrust.org | 200, allowed | fetched |
| www.dafgiving360.org | **403** | **blocked** (not fetched) |
| static1.squarespace.com (DAFgiving360 2024 PDF) | 404 | fetched |
| www.vanguardcharitable.org | 200, allowed | fetched |
| gspf.goldman.com | 200, **`User-agent: * Disallow: /`** | **blocked** |
| www.svcf.org | 200, allowed | fetched |
| www.morganstanley.com | 200, allowed | fetched |
| msgift.donorfirstx.com, rcf.donorfirstx.com, bofa.donorfirst.org | 404 | fetched |
| www.aefonline.org, aefonline.org, advisorwelcome/donorwelcome.aefonline.org | 200, allowed | fetched |
| www.reninc.com | 200, allowed | fetched (one 2022 RCF application now 404) |
| 8hxvw8tw.media.zestyio.com (TSA FAQ) | 404 | fetched |
| ncfgiving.com, www.ncfgiving.com | 200, allowed | fetched (/faq is 404) |
| www.bankofamerica.com | 200, allowed | fetched |
| www.cct.org | **403** | **blocked** (repo quote carried) |
| donorportal.cct.org | 200, allowed | fetched |
| impactassets.freshdesk.com, impactassets.org | 200, allowed | fetched |
| jcfny.org | 200, allowed | fetched |
| fftc.org | 200, allowed | fetched |
| www.growyourgiving.org, growyourgiving.org | 200, allowed | fetched |
| www.greaterhorizons.org | 200, allowed | fetched (no relevant text) |
| ma.cjp.org, www.cjp.org | 200, allowed | fetched |
| www.raymondjamescharitable.org, raymondjamescharitable.org, www.raymondjames.com | **403** | **blocked** |
| dechomai.org, www.dechomai.org | 200, allowed | fetched (no relevant text) |
| www.dafdirect.org, www.givechariot.com, givechariot.com, help.givechariot.com | 200, allowed | fetched |

## 7. Data dictionary: `donor-info-defaults-top20-2026-11-19.csv`

| Column | Meaning |
|---|---|
| `rank_fy2024`, `sponsor`, `ein` | League-table FY2024 asset rank, display name, EIN |
| `fy2024_daf_assets_usd` | `daf_assets_eoy` from the league table (corrected R1–R4) |
| `share_of_top20_assets` | Computed: assets ÷ $250.63bn top-20 total |
| `default_category` | What reaches the charity if the donor changes nothing, as coded from the text (§1.5) |
| `default_bucket` | Summary bucket: full contact / name only / fund name only / anonymous / donor must choose / no default stated / not determinable |
| `default_detail` | Plain-language description of options and default |
| `default_quote`, `default_url`, `default_source_date` | Verbatim evidence, primary URL, document date (PDF metadata or "live page") |
| `donor_must_choose` + `must_choose_quote/url/source_date` | Y = no preselection, so the donor must pick; N = preselected default; Y? / unknown where the text is ambiguous or absent |
| `charity_gets_email_or_address` + `email_address_*` | Whether the charity receives the donor's postal address and/or email, by default or on election |
| `donor_can_share_directly` + `share_direct_*` | Whether the sponsor documents a way for the donor to put contact details or a message before the charity (custom acknowledgement, address election, DAFpay contact confirmation), or restricts it |
| `api_data_sharing` + `api_*` | Documented sharing of donor data with charities through APIs or shared rails: DAF Direct, Chariot DAFpay or managed sources, PayPal Grant Payments, Stripe/ACH reports |
| `access_robots` | robots.txt status for the hosts used, or the block |
| `evidence_label` | F first-hand; blocked; absent; [R] search snippet |
| `observed_outcome_data` | Published shares of anonymous or partial grants, or conflicts between documents |
| `repo_prior` | Prior repo row or document covering the same point |
| `change_vs_repo` | NEW / confirms / refines / CHANGES / gap |
| `retrieved` | Date read (2026-11-19) |

## 8. Source register (primary URLs)

| # | Source | Date | URL |
|---|---|---|---|
| S1 | Fidelity Charitable, "How is my information shared with recipient charities?" | live (undated) | https://www.fidelitycharitable.org/faqs/all/account-holder-acknowledgements.html |
| S2 | Fidelity Charitable, Giving Account guide: Recommending a grant | live | https://www.fidelitycharitable.org/giving-account-guide/recommending-a-grant.html |
| S3 | Fidelity Charitable, Nonprofit FAQs | live | https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html |
| S4 | Fidelity Charitable, 2026 Giving Report | 2026-04-21 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf |
| S5 | NPT, A Guide to your Donor-Advised Fund | 2026-10-15 | https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf |
| S6 | NPT, PayPal Grant Payments | 2022-08-25 | https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/ |
| S7 | DAFgiving360, 2024 Program Policies | 2024-12-12 | https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf |
| S8 | Chariot, New Access Method for DAFgiving360 in DAFpay | 2026-05-31 | https://givechariot.com/resources/insights/new-access-method-for-dafgiving360-in-dafpay.md |
| S9 | DAF Direct, About | live | https://www.dafdirect.org/about-daf-direct/index.html |
| S10 | Vanguard Charitable, Policies & Guidelines | live (updated 2026-01-09 per repo) | https://www.vanguardcharitable.org/company-policies/policies-and-guidelines |
| S11 | Vanguard Charitable, Nonprofit organizations | live | https://www.vanguardcharitable.org/nonprofit-organizations |
| S12 | SVCF, Donor Advised Fund Agreement | 2025-08-22 | https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf |
| S13 | MS GIFT, Grantee Guidelines | 2022-09-22 | https://msgift.donorfirstx.com/pdf/MSGIFT/Grantee%20Guidelines.pdf |
| S14 | MS GIFT, program page and FAQ | live | https://www.morganstanley.com/gift |
| S15 | AEF, FAQs for individual donors | live | https://www.aefonline.org/thought-leadership/faqs-individual-donors/ |
| S16 | AEF, Grant Recommendation Process for Donors | 2021-12-09 | https://www.aefonline.org/wp-content/uploads/2023/07/Grant-Recommendation-Process-for-Donors.pdf |
| S17 | RCF portal, Ren ‘Giving Platform Donor User Guide’ (same file on seven RCF portals, SHA-1 93d97b49e84a) [V wave 35B] | 2026-10-06 | https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf |
| S18 | RCF, Program Circular | 2026-06-01 | https://rcf.donorfirstx.com/pdf/RCF/RCF%20Program%20Circular.pdf |
| S19 | NCF, Guide to giving | live | https://ncfgiving.com/guide |
| S20 | NCF, Giving Fund | live | https://www.ncfgiving.com/giving-fund |
| S21 | BofA CGF, Guide to Navigating Your Donor Advised Fund | 2025-11-14 / 2026-02-23 | https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf |
| S22 | BofA CGF, Program Guidelines 2024 (Version 3.2024) | 2024-06-05 (PDF modified 2024-09-18) [V wave 34A] | https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf |
| S22a | BofA CGF, Program Guidelines Version 8.2025 (DonorFirst portal copy; grant-distribution text unchanged from Version 3.2024) | PDF 2025-09-08 | https://bofa.donorfirst.org/pdf/bofa/CGF%20Program%20Guidelines.pdf [V wave 48A]
| S23 | CCT, DAF Application | 2024-04-08 | https://donorportal.cct.org/ma/docs/cct/CCT-DAF-Application.pdf |
| S24 | CCT, DAF 101 for Nonprofits (repo-carried; blocked today) | Aug 2024 | https://www.cct.org/wp-content/uploads/2024/08/Donor-Advised-Fund-101-for-Nonprofits_August-2024.pdf |
| S25 | ImpactAssets, support article on anonymity and recognition | 2021-05-27 | https://impactassets.freshdesk.com/support/solutions/articles/62000217339-are-grants-from-my-impactassets-donor-advised-fund-account-anonymous-or-can-i-be-recognized-for-my-g |
| S26 | ImpactAssets, Grant Recommendation Form GE535A | March 2025 | https://impactassets.org/ge535a_ia_daf_grant-recommendation-form |
| S27 | JCF, Grant Recommendation Form | Dec 2022 | https://jcfny.org/wp-content/uploads/2021/02/GRDec22.pdf |
| S28 | FFTC, DAF Agreement | 2026-11-03 | https://fftc.org/sites/default/files/documents/FFTC_DAF_Agreement_Fillable.pdf |
| S29 | GKCCF, Knowledge Hub (nonprofits) | live | https://www.growyourgiving.org/nonprofits/knowledge-hub/ |
| S30 | GKCCF, Fueling nonprofit success | live | https://growyourgiving.org/fueling-nonprofit-success-the-role-of-donor-advised-funds |
| S31 | CJP, DAF Policies and Procedures | 2026-04-29 | https://ma.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf |
| S32 | CJP, DAF Forms | 2024-09-12 | https://ma.cjp.org/hubfs/DAF/DAF%20Forms%20(Adobe%20web%20form%20version)%20-%20Updated%2010-01-24%20MG.pdf |
| S33 | Greater Horizons, Open a DAF (no relevant text) | live | https://www.greaterhorizons.org/open-a-donor-advised-fund/ |
| S34 | Dechomai, FAQs and Policies (no relevant text) | live | https://dechomai.org/faqs/ ; https://dechomai.org/policies-and-procedures/ |
| S35 | Chariot, Sources (managed sources) | live | https://help.givechariot.com/getting-started/sources.md |
| S36 | DAFRC, National Survey of DAF Managers (baseline, repo) | 2025 | https://www.dafresearchcollaborative.org/s/The-National-Survey-of-Donor-Advised-Fund-Managers.pdf |
