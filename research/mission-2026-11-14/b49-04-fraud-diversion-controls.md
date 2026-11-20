# Fraud and diversion risks around DAF grants and DAF donors, and the controls sponsors publish (2021+)

- **Task:** B49-04. A new, defensive and descriptive direction for the repo: what fraud and diversion risks affect DAF grants and DAF donors, and what controls the FY2024 top-20 sponsors publish.
- **Date:** 2026-11-20. Every page cited was read on that date unless marked [R].
- **Scope rules followed:** public primary sources only; 2021+ evidence; no logins, forms or outreach; robots.txt checked per host, with ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot treated as binding; sec.gov not used; ncfgiving.com not fetched (site terms). Controls and incidents are described **at the level of public reporting only**. This note does not describe how any scheme is carried out beyond the one-line labels the cited sources use, and it names no private victims. No defendant is named here or in the CSV.
- **Builds on:** [b39n1-03-b39n2-02-lobbying-and-breaches.md](b39n1-03-b39n2-02-lobbying-and-breaches.md) (breach registers), [queue-batch37-controls-education.md](queue-batch37-controls-education.md) §1 (payment-redirection controls, P-PRC-06, with its wave-22 corrections), [b4013-02-b4222-02-remittance-and-portal-features.md](b4013-02-b4222-02-remittance-and-portal-features.md) (grant remittance), `payment-redirection-controls-2026.csv` (PR01–PR25), `sponsor-fraud-loss-disclosures.csv`, `daf-security-incidents-2021plus.csv`, `daf-litigation-2021plus.csv` and `sponsor-grant-payment-policies.csv`.
- **Files written:**
  - [`data/mission-2026-11-14/fraud-diversion-controls-2026-11-20.csv`](../../data/mission-2026-11-14/fraud-diversion-controls-2026-11-20.csv): 54 rows, 19 columns (data dictionary in §7).
  - [`data/mission-2026-11-14/queue-proposals-b49-04.csv`](../../data/mission-2026-11-14/queue-proposals-b49-04.csv): 6 rows.
  - [`scripts/mission_b49_04_fraud_controls_build.py`](../../scripts/mission_b49_04_fraud_controls_build.py): writes the CSV and prints every share in this note. Run `python3 -I scripts/mission_b49_04_fraud_controls_build.py . [--doj-hits <jsonl files>]`.
  - [`scripts/mission_b49_04_doj_scan.py`](../../scripts/mission_b49_04_doj_scan.py): the DOJ press-release screen (§3.2).
  - [`scripts/mission_b49_04_get.py`](../../scripts/mission_b49_04_get.py): the robots-checking fetcher used for every page.
- **Labels:** [F] first-party text read this pass; [C] computed by a script; [R] carried from a repo file; [B] blocked or not read; [I] inference.

---

## 0. Answers

| Question | Finding | Confidence |
|---|---|---|
| **Do the top-20 sponsors publish fraud or security notices?** | **Three do on their own sites: Fidelity Charitable, NPT and Vanguard Charitable, 52.0% of FY2024 top-20 DAF assets** [C]. Two more are covered only by their parents' general pages (Morgan Stanley for MS GIFT, Bank of America Private Bank for BofA CGF), which lifts coverage to **5 sponsors, 57.5%** [C].<br>- **Seven sponsors (10.9% of assets) were searched and publish nothing** relevant: SVCF, RCF, ImpactAssets, JCF, FFTC, CJP and Dechomai [C].<br>- **Four (24.4%) could not be read:** DAFgiving360, GS DAF and Raymond James Charitable (robots), and NCF (site terms) [C/B]. | High on what is published; "nothing found" means not on pages read |
| **Which risks do the notices name?** | Five families appear in first-party text:<br>1. **Charity impersonation and look-alike charities** (Fidelity, NPT, Vanguard).<br>2. **Payment-detail change requests / business email compromise (BEC)** (Fidelity's donor page; the Morgan Stanley and BofA parent pages). **No top-20 sponsor page warns charities about bank-change fraud** [F].<br>3. **Grant-offer and "deposit and forward" scams using the sponsor's name** (Vanguard's lists, for donors and for grantees) [F].<br>4. **Credential sharing with third-party giving tools** (Fidelity; BofA Private Bank names DAF-credential widgets on charity sites; Vanguard says not to link accounts to donor-tracking apps) [F].<br>5. **Mail and check fraud** (Fidelity's EFT pitch: "1 in 5 organizations reporting mail fraud", unsourced) [F]. | High |
| **Donor two-factor authentication** | **Published as required or prompted at 4 sponsors (53.8% of assets): Fidelity, NPT, Vanguard and CCT** [C].<br>- **Fidelity** goes furthest: MFA at login and on new devices, a **step-up code for new bank instructions and contact changes**, voice biometrics on the phone, and new advisor-portal MFA (2026) [F].<br>- **Vanguard**: "MFA is now required for all web-registered Vanguard Charitable users" [F].<br>- **NPT**: a verification code at online registration; per-login use is not stated [F].<br>- **GKCCF and Greater Horizons** (2.0%) offer MFA as an **option** only [F]. | High |
| **Charity bank-change verification** | **Unchanged from batch 37C, now checked across the top 20.** No sponsor publishes a mandatory callback to a known contact before a bank change, which is the Commerce OIG benchmark (FDC-45).<br>- Sponsor-published charity-side checks cover **2 sponsors, 29.8%**: Fidelity (documents plus a *discretionary* callback to a public number) and AEF (ACH "submitted and verified" in a Ren portal before electronic payment) [C/F].<br>- Counting sponsors whose payments run on **Ren for Charities** (MS GIFT, AEF, RCF per `grant-remittance-2026-11-19.csv`), the share is **4 sponsors, 35.8%** [I/C]. Ren publishes claim checks (postcard to the IRS address, call to the 990 phone number, or officer ID check) and rejects bank links it cannot tie to the organisation [F].<br>- **25.6%** (NPT, Vanguard) pay through PayPal Grant Payments and hold no charity bank details [R/C]; PayPal's own change controls were again unreadable (HTTP 403). | High on text; absence of a callback is absence from public pages |
| **Enforcement and court records** | **See §3.2.** DOJ screen result: DOJ_RESULT_SUMMARY. SEC (excluded by rule), CourtListener (robots 403), the FTC (HTTP 404 to every path) and the Florida AG (robots 403) were not read. State AG warnings found (Hawaii 2025, Nebraska 2024) concern counterfeit-check refund scams against nonprofits, not DAFs. | Medium (federal releases only) |
| **FBI IC3 and FTC** | **IC3 started reporting "Charity" as a crime type only in its 2025 report: 662 complaints and $7,907,609 losses in 2025**; 2023 and 2024 are marked "not captured" [F]. Complainants aged 60+ filed 126 of them, with $3,474,668 of losses [F]. A January 2025 IC3 PSA counts **more than 4,500 complaints and about $96m** of 2024 losses to "fraudulent charities, crowdfunding accounts, and disaster relief campaigns", a broader definition [F]. **Neither mentions DAFs.** FTC pages could not be read. | High for IC3 figures |
| **Link to the breach work** | The breach registers (b39n1-03) found **no register entry naming a charitable or DAF entity**; every notice is filed by a parent or a vendor [R]. The controls found here are the donor-side answer to that exposure: credential theft at a parent leads to account takeover at the DAF only if login and step-up checks fail, and those checks are published at sponsors holding 53.8% of top-20 assets [I/C]. | Inference |

**Bottom line.** Public evidence of DAF-specific fraud is thin, and what exists is **sponsor and vendor warnings, not case records**. The published controls split three ways:
1. **Donor-side account protection** (MFA, step-up codes, "we never ask for codes") is documented by the three largest readable sponsors.
2. **Charity-side bank-change protection** is either a document check at the sponsor (Fidelity), a third-party portal with its own verification (Ren, Chariot), or removed from the sponsor altogether by PayPal custody (NPT, Vanguard).
3. **Charity-facing fraud warnings** are the gap: only Vanguard publishes one, and it does not cover bank-change requests.

---

## 1. Method

1. **Universe.** The FY2024 top 20 and their DAF assets come from `donor-info-defaults-top20-2026-11-19.csv` (the league-table cut used by b44n28-01). Shares are each sponsor's assets over the top-20 total of $250.63bn, computed by the build script [C].
2. **Repo first.** Earlier rows were reused rather than re-collected: PR01–PR25 (payment redirection), the breach registers, the Form 990 fraud-loss lines, the remittance census and the litigation file. New rows say what they add.
3. **Discovery.** For each top-20 sponsor: (a) homepage links matching security, fraud, scam, phishing or two-factor terms; (b) **every URL in the sponsor's XML sitemaps**, screened for the same terms (counts per sponsor are in the CSV `control_or_finding` field); (c) a site-restricted web search. Search results were used only to find URLs; nothing in this note rests on a search snippet.
4. **Robots and access.** `scripts/mission_b49_04_get.py` fetched robots.txt per host and fetched a page only if `*`, `research-script/1.0`, ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot were **all** allowed. A 404 robots.txt counted as no restriction; any other non-200 robots response counted as blocked. The user agent was never changed. Bot interstitials and blanket 404/403 responses were logged and **not** worked around (§2).
5. **Enforcement.** DOJ HTML pages answer a generic client with a bot interstitial, so the DOJ **public JSON API** (`/api/v1/press_releases.json`, allowed by robots.txt) was used to screen every press release dated 2021-01-01 to 2026-11-20 for DAF and sponsor terms (§3.2). The screen keeps only matching releases and their snippets; the judgement of relevance was made by reading each hit.
6. **Federal reports.** IC3's 2021–2025 annual reports and the 2025 charity PSA were read in full text (pdftotext). FTC pages could not be read.
7. **Coding.** Each CSV row is one notice, control, report statistic or blocked source. `stated` is Y, partial, optional, parent only, N, absent (searched, nothing found), blocked, not read or repo. Coverage shares count a sponsor once if any of its rows meets the test.

## 2. Robots and access log

Requests: 138 page and robots requests, plus the DOJ API screen (§3.2). One line per host.

| Host | robots.txt | Result | Use |
|---|---|---|---|
| www.fidelitycharitable.org, fidelitycharitable.org | 200, all agents allowed | 200 (two old FAQ URLs 404) | FDC-01 to FDC-09 |
| www.nptrust.org | 200, allowed | 200 | FDC-10 to FDC-13 |
| www.dafgiving360.org | **HTTP 403** | blocked | FDC-14 |
| www.vanguardcharitable.org | 200, allowed | 200 | FDC-15, FDC-16 |
| gspf.goldman.com | 200, **Disallow for `*` and all five AI agents** | blocked | FDC-17 |
| www.svcf.org | 200, allowed | 200 | FDC-18 |
| www.morganstanley.com | 200, allowed | 200 | FDC-19 |
| advisor.morganstanley.com | unreachable (connection failed) | blocked | not used |
| www.aefonline.org | 200, allowed | 200 | FDC-20 |
| renaissancecharitable.org | 200, allowed | 200 | FDC-21 |
| www.ncfgiving.com | not requested | site terms ban automated extraction | FDC-22 |
| www.privatebank.bankofamerica.com, www.ml.com, www.bankofamerica.com | 200, allowed | 200 | FDC-23 |
| www.cct.org | 200, allowed | **HTTP 403** to the page | not used |
| donorportal.cct.org | 200, allowed | 200 | FDC-24 |
| impactassets.org, jcfny.org, fftc.org / www.fftc.org, www.cjp.org / ma.cjp.org, dechomai.org | 200, allowed | 200 (some sitemap paths 404) | FDC-25 to FDC-27, FDC-30, FDC-32 |
| www.growyourgiving.org, www.greaterhorizons.org | 200, allowed | 200 | FDC-28, FDC-29 |
| www.raymondjamescharitable.org | unreachable (connection failed) | blocked | FDC-31 |
| www.givechariot.com | 200, allowed | 200 | FDC-33 |
| intercom.help (rengiving) | 200, allowed | 200 | FDC-34 to FDC-36 |
| www.reninc.com | 200, allowed | 404 (ACH guide PDF) | not used |
| www.paypal.com | 200, allowed | **HTTP 403** | not used |
| ghcf.org | 200, allowed | 200 | FDC-37 |
| www.ic3.gov | 200, allowed | 200 | FDC-38 to FDC-41 |
| www.fincen.gov, fincen.gov | 200, allowed | release page 200; alert and FTA PDFs 404 | FDC-42 |
| ag.hawaii.gov, ago.nebraska.gov | 200, allowed | 200 | FDC-43, FDC-44 |
| www.oig.doc.gov | 404 (no restriction) | 200 | FDC-45 |
| www.justice.gov | 200, allowed | HTML: bot interstitial / 403 (not bypassed); **API: 200** | FDC-46 |
| www.ftc.gov, consumer.ftc.gov | **404 for robots.txt and every page** | unreadable; treated as blocked | FDC-50 |
| www.courtlistener.com | **HTTP 403** | blocked | FDC-49 |
| www.myfloridalegal.com | **HTTP 403** | blocked | FDC-51 |
| oig.lsc.gov | unreachable | blocked | not used |
| www.sec.gov | not requested | excluded by shared rule | FDC-48 |

## 3. Results

### 3.1 Sponsor security notices and controls, top 20

| # | Sponsor | FY2024 share | Own fraud/scam notice | Login MFA | Charity bank-change control published | Rows |
|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable | 26.4% | **Y**: BEC and payment-change warning; credential-sharing warning; look-alike charities; "Fraud is on the rise across the charitable sector" | **Y**: login MFA; step-up code for new bank instructions and contact changes; voice biometrics; advisor-portal MFA (2026) | **Partial**: documents plus a discretionary callback to a public number; the FAQ now accepts "a voided check **or bank letter** dated within the last 12 months" (the form in PR01 says voided check) | FDC-01–09 |
| 2 | NPT | 16.8% | **Y** (donor articles 2022-09-23, 2024-05-01) | **Y** at registration (code by text or voice) | n/a: PayPal holds bank details (PR13); charity page has no redirection item | FDC-10–13 |
| 3 | DAFgiving360 | 16.3% | blocked | blocked | blocked | FDC-14 |
| 4 | Vanguard Charitable | 8.8% | **Y**: scams aimed at donors and at grantees | **Y**: "required for all web-registered … users"; never asks for MFA codes | n/a: PayPal (PR10) | FDC-15–16 |
| 5 | GS DAF | 5.0% | blocked | blocked | blocked | FDC-17 |
| 6 | SVCF | 3.8% | none found | none found | none found | FDC-18 |
| 7 | MS GIFT | 3.6% | parent page only (BEC, call-back verification) | not found | Ren rail [I] | FDC-19 |
| 8 | AEF | 3.3% | none found | not found | **Y**: ACH "submitted and verified" in Ren portal before EFT | FDC-20 |
| 9 | RCF | 2.4% | none found | not found | Ren rail [I] | FDC-21 |
| 10 | NCF | 2.3% | not read (site terms) | not read | not read | FDC-22 |
| 11 | BofA CGF | 1.9% | parent page only (DAF-credential widgets; "changed account" messages) | not found | not found | FDC-23 |
| 12 | CCT | 1.9% | none read (www.cct.org 403) | **Y**: MFA set up at first login, email or SMS (guide 2024-02) | not found | FDC-24 |
| 13 | ImpactAssets | 1.2% | none found | not found | not found | FDC-25 |
| 14 | JCF | 1.1% | none found | not found | not found (wire grants followed by an email to the charity contact) | FDC-26 |
| 15 | FFTC | 1.0% | none found | not found | not found | FDC-27 |
| 16 | GKCCF | 1.0% | none found | **optional** | not found | FDC-28 |
| 17 | Greater Horizons | 1.0% | none found | **optional** | not found | FDC-29 |
| 18 | CJP | 0.8% | none found (security pages are about physical safety) | not found | not found | FDC-30 |
| 19 | Raymond James Charitable | 0.8% | blocked | blocked | blocked | FDC-31 |
| 20 | Dechomai | 0.6% | none found | not found | not found | FDC-32 |

**Computed coverage** (build script output) [C]:

| Test (sponsor counted once if any row meets it) | Sponsors | Share of FY2024 top-20 DAF assets |
|---|---|---|
| Own donor-facing fraud or scam notice | 3 | 52.0% |
| Any donor-facing notice, including parent-only pages | 5 | 57.5% |
| Login MFA or one-time code published as required or prompted | 4 | 53.8% |
| MFA published as optional only | 2 | 2.0% |
| Notice names payment-detail changes or BEC (own or parent) | 3 | 31.9% |
| Charity-side bank-change verification published by the sponsor | 2 | 29.8% |
| … plus sponsors paying through Ren for Charities [I] | 4 | 35.8% |
| Charity bank details held by PayPal, not the sponsor | 2 | 25.6% |
| Blocked or not read | 4 | 24.4% |
| Searched, nothing found | 7 | 10.9% |

**What the notices say** [F] (quotes in the CSV):
- **Fidelity Charitable** has the fullest set. Its security page says "Fraud is on the rise across the charitable sector" and warns that "these evolving risks may require additional verification and processing time for certain transactions". Its 2026 advisor note adds "expanded due diligence for processing qualifying grants and contributions … additional review may extend processing timelines". This is the only top-20 statement that fraud controls lengthen grant processing, which bears on the repo's grant-latency work (`grant-latency-statements-2026.csv`) [I].
- **Vanguard Charitable** is the only sponsor that lists scams aimed at **grantees** under its own name: grants to individuals, requests to deposit a check and send part of it elsewhere, fees for releasing grants, lotteries, gift-card or crypto requests. None is a bank-change request. The deposit-and-forward item matches the counterfeit-check refund scheme that the Hawaii (2025) and Nebraska (2024) attorneys general describe (FDC-43, FDC-44) [F/I].
- **The BofA and Merrill article** (same text on both sites) is the only top-20-family page that warns about **charity-site widgets asking for DAF login credentials**. Fidelity's page makes the same point without naming widgets, and Vanguard says "Do not connect your philanthropic accounts to donor-tracking apps" [F]. These sit against the DAFpay credential-pass-through and agent-wrapper work in batches 35–36 [R].
- **No sponsor page addressed to charities** warns about requests to change bank details, the risk behind three of the seven Form 990 fraud disclosures in the repo (§5). Vanguard's grantee list and NPT's charity page are the only charity-facing texts, and neither covers it [F].

### 3.2 Enforcement and court records

DOJ_SECTION

**Other venues.**
- **State attorneys general.** Hawaii (News Release 2025-81, 2025-08-19) and Nebraska (2024-06-25) warn nonprofits about counterfeit donation checks followed by partial-refund requests. Neither mentions DAFs (FDC-43, FDC-44). Names used by the scammers in the Hawaii release are not stored. Florida's release on a charity scam was robots-blocked (FDC-51).
- **Repo record.** The Georgia action against SDG Impact Fund (LIT-04, a DAF-style sponsor accused of misusing donor funds) remains the repo's only 2021+ enforcement record of misuse **by a sponsor** (FDC-47) [R].
- **Not read:** SEC litigation releases (rule), CourtListener (robots 403), the FTC (HTTP 404).

### 3.3 Charity-payment change controls: rails

The rails now carry most of the published charity-side checks [F]:
- **Ren for Charities** (RCF, AEF, MS GIFT and other Ren programs; FDC-34 to FDC-36). A charity is claimed through one of three checks: a postcard to its IRS-filed address, an automated call to the phone number on its latest e-filed Form 990, or an officer identity check through Stripe. Bank links go through Plaid or manual review, and Ren says it rejects a link "if we are unable to verify that the bank account belongs to your organization". Check grants show USPS scan events in the portal. **No callback or cooling-off period is stated for later bank changes.**
- **Chariot** (FDC-33; PR16–PR19 in the repo). Its article names three DAF-specific diversion patterns, at the level of a one-line description each: impersonating a charity to a DAF provider to change contact or address details; enrolling a charity in a digital payment system with falsified bank documents; and mail theft with check alteration. It gives no counts and names no sponsor. Chariot sells the receiving-account product it recommends, so the article is a vendor notice, not a case record.
- **PayPal Grant Payments** (NPT, Vanguard): unreadable again (403).
- **Benchmark.** The Commerce OIG alert (July 2026) asks grant makers to verify every bank-change request with a known contact, to require dual approval, and to inspect sender addresses (FDC-45). Morgan Stanley's parent page states the call-back control for clients ("calling a trusted phone number (i.e., a call-back verification)") (FDC-19). **No DAF sponsor or rail states that it applies that control to every charity bank change.**
- **A peer example outside the top 20.** Greater Houston Community Foundation tells donors to verify transfer and grant instructions through a known phone number, to turn on MFA, and never to share portal credentials with external tools (FDC-37). Nothing in the top 20 is as explicit for donors except Fidelity.

## 4. FBI IC3, FinCEN and FTC

| Source | Figure | DAF mention | Row |
|---|---|---|---|
| IC3 PSA I-011625-PSA (2025-01-16) | 2024: "more than 4,500 complaints" and "approximately $96 million" lost to fraudulent charities, crowdfunding accounts and disaster relief campaigns | none | FDC-38 |
| IC3 2025 Internet Crime Report | **Charity** crime type: **662 complaints, $7,907,609** (2025). 2024 and 2023: "* Crime Type or Descriptor was not captured in these years." | none | FDC-39 |
| IC3 2025, complainants 60+ | Charity: 126 complaints, $3,474,668 | none | FDC-40 |
| IC3 2021–2024 reports | No "Charity" crime type in the text of any of the four reports (pdftotext search) [C] | none | FDC-39 notes |
| IC3 2025, BEC (all sectors) | 24,768 / 21,442 / 21,489 complaints and $3.05bn / $2.77bn / $2.95bn losses in 2025 / 2024 / 2023 | none | FDC-41 |
| FinCEN Financial Trend Analysis (release 2024-09-09) | 15,417 BSA reports from 841 institutions, more than $688m, in the six months after the Feb-2023 mail-theft check-fraud alert; 44% of stolen checks altered and deposited, 26% used as counterfeit templates, 20% fraudulently signed | none | FDC-42 |
| FTC Consumer Sentinel | not read: ftc.gov returned 404 to every path | — | FDC-50 |

**Reading [I].** The federal series measure **donors defrauded by fake charities**, not DAF grants diverted from real ones. The two figures differ by an order of magnitude because the PSA counts crowdfunding and disaster-relief schemes with charity fraud, while the annual-report category is narrower. Neither can be scaled to DAFs. The check-fraud and BEC series are the relevant context for grant diversion, because DAF grants still move by mailed check and by bank transfer to charity-held accounts (`sponsor-grant-payment-policies.csv`, `grant-remittance-2026-11-19.csv`) [R].

## 5. Link to earlier repo work

1. **Breach notices (b39n1-03).** No 2021–26 Massachusetts or Vermont register entry names a charitable or DAF entity, and every DAF-adjacent notice is filed by a parent (Fidelity Investments, Schwab/TD Ameritrade, Vanguard Group, Ameriprise, Morgan Stanley) or a vendor (Infosys McCamish) [R]. Two consequences [I]:
   - The **donor-side** controls found here (MFA, step-up codes, voice biometrics, "we never ask for codes") are what stands between a parent-level credential or data exposure and a DAF account takeover. They are published at sponsors with 53.8% of top-20 assets. They are not published at the sponsors whose parents filed the 2023–2026 notices other than Fidelity and Vanguard: DAFgiving360 is blocked and MS GIFT shows only a parent page.
   - No public record found links any of those breaches to a DAF grant being redirected. The registers cannot show it, and DOJ releases do not (§3.2).
2. **Payment redirection (batch 37C, PR01–PR25).** This pass confirms PR07, PR08, PR11 and PR12 live, extends the check to all top-20 sponsors, and adds one discrepancy: Fidelity's FAQ now accepts a bank letter as well as a voided check (FDC-07 vs PR01). The batch-37C conclusion stands: no sponsor publishes a mandatory callback to a known contact for every bank change.
3. **Remittance (b4013-02).** Every documented electronic route sends grant detail out-of-band, by emailed report, portal or letter, and no top-10 sponsor documents a grant ID in ACH addenda [R]. Those emails and letters are the "grant letters" whose controls this task asked about [I]. The controls published for them are thin:
   - Fidelity's Grant Details Report is encrypted and goes only to named individual inboxes (PR03) [R].
   - Ren and Chariot move grant letters into authenticated portals (FDC-36) [F].
   - Fidelity reissues a check only at the donor's request, and voids one at the charity's request (FDC-08) [F].
   - No top-20 sponsor publishes how a charity can verify that a grant letter or notice is genuine.
4. **Form 990 losses (`sponsor-fraud-loss-disclosures.csv`).** Three of seven Part VI line-5 disclosures in the 1,512-sponsor universe are payment redirection or BEC, and one DAF processor (Givinga) booked a $316,184 "external bank fraud loss" in CY2024 [R]. These are the only dollar figures in the repo for losses at or near DAF sponsors. None is a DAF grant diverted from a top-20 sponsor.

## 6. Limits

1. **Absence is not proof.** "None found" means no relevant text on the homepage, in the sponsor's sitemaps or in site-restricted search. Logged-in help centres and PDFs not in a sitemap were not read.
2. **Blocked share.** DAFgiving360, GS DAF, Raymond James Charitable and NCF hold 24.4% of top-20 assets and are unread. Every coverage share would rise if they publish controls.
3. **Published is not practised.** The CSV records what sponsors say. It cannot show whether a callback, step-up code or review is applied every time.
4. **DOJ screen scope.** The DOJ API carries DOJ and USAO press releases only. Releases are written for the public and may describe a DAF as "a charitable account" or name no sponsor; the term screen would miss such wording. Court dockets (PACER, CourtListener) and SEC releases were not available.
5. **FTC unread.** ftc.gov answered 404 to every request, robots.txt included, so FTC figures are absent. The FTC loss figure quoted inside NPT's 2022 article was not used.
6. **Parent pages.** MS GIFT and BofA CGF rows rest on parent-company pages that do not mention the DAF program. They are labelled "parent only" and excluded from the "own notice" share.
7. **Vendor sources.** Chariot's article is commercial. It is used only for the list of patterns it names, not for prevalence.
8. **Dates.** Most sponsor pages are undated live pages; the CSV records any date shown. All were live on 2026-11-20.

## 7. Data dictionary

### `data/mission-2026-11-14/fraud-diversion-controls-2026-11-20.csv` (54 rows; one row per notice, control, statistic, blocked source or repo link)

| Field | Meaning |
|---|---|
| `row_id` | FDC-01 … FDC-54 |
| `record_type` | sponsor_notice, sponsor_control, rail_control, vendor_notice, peer_benchmark, federal_report, enforcement_or_regulator, repo_link |
| `entity` | Sponsor, rail, regulator or source named in the row. No individual is named |
| `top20_rank` | FY2024 rank in the top 20 (blank if not a top-20 sponsor) |
| `entity_role` | sponsor, sponsor_parent (page published by the parent company), payment_rail_vendor, regulator, state_regulator, federal_regulator, federal_prosecutor, court_records, repo |
| `risk_category` | payment_redirection_BEC, account_takeover, credential_sharing_third_party, charity_impersonation, grant_offer_scam, check_theft_alteration, overpayment_refund, charity_fraud, internal_misappropriation, phishing_impersonation, all. Semicolon-separated when a row covers two |
| `audience` | Who the notice or control addresses: donor, charity, advisor, both, public, financial_institutions, grant_makers, sponsor, all |
| `control_or_finding` | Plain description of the control, notice or finding, at the level of the source |
| `stated` | Y; partial; optional; parent only; N (page read, item missing); absent (searched, nothing relevant found); blocked; not read; repo; see note |
| `key_quote` | Verbatim first-party text (or the computed DOJ hit list for FDC-46) |
| `figure_value` | Numbers stated by the source or computed, semicolon-separated |
| `figure_unit` | Units for `figure_value`, in the same order |
| `source_url` | Primary URL(s); repo path for repo rows |
| `source_date` | Date shown on the source, PDF metadata, or "live page" |
| `access_status` | Robots and HTTP outcome for the source |
| `evidence_label` | F first-party read; C computed; R repo; B blocked or not read; absent |
| `repo_link` | Earlier repo rows this row confirms, extends or depends on |
| `notes` | Caveats, discrepancies and scope notes |
| `retrieved` | 2026-11-20 |

### `data/mission-2026-11-14/queue-proposals-b49-04.csv`

Same header and format as `queue-proposals-gap19-13.csv`; 6 rows (P-B4904-01 to -06).

## 8. Source register

| # | Source | Date | URL |
|---|---|---|---|
| S1 | Fidelity Charitable, "Confident giving: Smart security tips for navigating common scams" | live page | https://www.fidelitycharitable.org/articles/security-tips-common-scams.html |
| S2 | Fidelity Charitable, "Your security matters to us" | live page | https://www.fidelitycharitable.org/security.html |
| S3 | Fidelity Charitable, one-time security codes; MFA FAQs | live pages | https://www.fidelitycharitable.org/help/security-codes.html ; https://www.fidelitycharitable.org/faqs/all/when-asked-to-complete-mfa.html ; https://www.fidelitycharitable.org/faqs/all/extra-login-security-mfa.html |
| S4 | Fidelity Charitable, "Improvements to the advisor experience" (PDF) | 2026-10-06 | https://www.fidelitycharitable.org/content/dam/fc-public/vessel/enhancements-to-the-advisor-experience.pdf |
| S5 | Fidelity Charitable, nonprofit FAQ and EFT page | live pages | https://www.fidelitycharitable.org/nonprofits/faqs.html ; https://www.fidelitycharitable.org/nonprofits/eft.html |
| S6 | NPT, "How NPT Conducts Grantmaking Due Diligence—and How Donors Can Avoid Charity Scams" | 2022-09-23 | https://www.nptrust.org/philanthropic-resources/philanthropist/how-npt-conducts-grantmaking-due-diligence-and-how-donors-can-avoid-charity-scams/ |
| S7 | NPT, "Awareness for Donors: Due Diligence When Choosing Nonprofit Organizations for Grant Recommendations" | 2024-05-01 | https://www.nptrust.org/?p=9117 |
| S8 | NPT, "How to Open a DAF Account Online" (PDF) | 2025-04-29 | https://www.nptrust.org/wp-content/uploads/2021/01/How-to-Open-a-DAF-Account-Online-NPT.pdf |
| S9 | NPT, For Nonprofits | live page | https://www.nptrust.org/for-nonprofits/ |
| S10 | Vanguard Charitable, Security Center; registration FAQ | live pages | https://www.vanguardcharitable.org/company-policies/security-center ; https://www.vanguardcharitable.org/faq/how-do-i-register-my-vanguard-charitable-account-online |
| S11 | Morgan Stanley, Cybersecurity and Fraud Awareness | live page | https://www.morganstanley.com/about-us/cybersecurity-and-fraud-awareness |
| S12 | AEF, Charities page (Ren-powered portal) | live page | https://www.aefonline.org/charities/ |
| S13 | Bank of America Private Bank / Merrill, "Donors, beware these digital giving scams" | live page (cites 2025-02-27) | https://www.privatebank.bankofamerica.com/articles/online-charity-scams.html ; https://www.ml.com/articles/online-charity-scams.html |
| S14 | The Chicago Community Trust, Donor Portal User Guide (PDF) | 2024-02-06 | https://donorportal.cct.org/ma/docs/cct/DonorPortalUserGuide.pdf |
| S15 | JCF, FAQs | live page | https://jcfny.org/faqs/ |
| S16 | GKCCF, Access Your Fund Online; Privacy Policy | live pages | https://www.growyourgiving.org/access-fund-online/ ; https://www.growyourgiving.org/privacy-policy/ |
| S17 | Greater Horizons, Access Your Fund Online | live page | https://www.greaterhorizons.org/access-fund-online/ |
| S18 | Sitemaps screened (SVCF, AEF, RCF, ImpactAssets, JCF, FFTC, CJP, GKCCF, Greater Horizons, Vanguard Charitable, NPT, Dechomai) | read 2026-11-20 | e.g. https://www.svcf.org/sitemap.xml ; https://impactassets.org/sitemap_index.xml ; https://dechomai.org/sitemap.xml (full list in the CSV `source_url` fields) |
| S19 | Chariot, "Behind-the-Scenes Risks: How DAF Giving is Being Exploited" | live page | https://www.givechariot.com/post/behind-the-scenes-risks-how-daf-giving-is-being-exploited-and-what-you-can-do-about-it |
| S20 | Ren for Charities help: claiming your charity; ACH setup; where is our grant | live pages | https://intercom.help/rengiving/en/articles/14285109-claiming-your-charity-step-by-step ; https://intercom.help/rengiving/en/articles/6232119-charity-ach-setup-step-by-step ; https://intercom.help/rengiving/en/articles/9970231-where-is-our-grant |
| S21 | Greater Houston Community Foundation, donor security tips | live page | https://ghcf.org/articles/how-to-avoid-impersonation-fraud-donor-security-tips/ |
| S22 | FBI IC3 PSA I-011625-PSA | 2025-01-16 | https://www.ic3.gov/PSA/2025/PSA250116 |
| S23 | FBI IC3 Internet Crime Reports 2021–2025 | annual | https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf (and 2024, 2023, 2022, 2021 at the same path) |
| S24 | FinCEN, "FinCEN Issues In-Depth Analysis of Check Fraud Related to Mail Theft" | 2024-09-09 | https://www.fincen.gov/news/news-releases/fincen-issues-depth-analysis-check-fraud-related-mail-theft |
| S25 | Hawaii Department of the Attorney General, News Release 2025-81 | 2025-08-19 | https://ag.hawaii.gov/wp-content/uploads/2025/08/News-Release-2025-81.pdf |
| S26 | Nebraska Attorney General, "Scammers Targeting Nebraska Nonprofits with Fraudulent Refunds" | 2024-06-25 | https://ago.nebraska.gov/node/2215 |
| S27 | U.S. Department of Commerce OIG Fraud Alert (PDF) | 2026-07-27 | https://www.oig.doc.gov/wp-content/OIGPublications/DOC-OIG-Fraud-Alert-July-2026-Approved.pdf |
| S28 | U.S. DOJ press releases API | read 2026-11-20 | https://www.justice.gov/api/v1/press_releases.json |
| S29 | Blocked or unread: DAFgiving360, GS DAF, Raymond James Charitable, NCF (terms), CourtListener, FTC, Florida AG, PayPal, SEC (rule) | 2026-11-20 | see §2 |
