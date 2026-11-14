# DAF user complaints: a coded corpus of complaints from donors, advisers and nonprofits about sponsors, platforms and payment rails

**Research date:** 2026-11-14 | **Evidence window:** 2012 to 2026-11 | **Companion data:** [`data/mission-2026-11-14/daf-user-complaints-corpus.csv`](../../data/mission-2026-11-14/daf-user-complaints-corpus.csv) (244 records) | **Queue proposals:** [`data/mission-2026-11-14/queue-proposals-complaints.csv`](../../data/mission-2026-11-14/queue-proposals-complaints.csv)

**This file builds on:**
- [public-forum-daf-experience-evidence-2026-11-11.md](../public-forum-daf-experience-evidence-2026-11-11.md), whose 12 items (UX-01 to UX-12) are carried into the corpus and flagged as such;
- [public-forum-daf-experience-feedback-plan-2026-11-11.md](../public-forum-daf-experience-feedback-plan-2026-11-11.md);
- [daf-platform-voice-of-customer-reddit-research-todo-2026-11-11.md](../daf-platform-voice-of-customer-reddit-research-todo-2026-11-11.md);
- [daf-end-to-end-experience-comparative-diagnostic-2026-11-11.md](../daf-end-to-end-experience-comparative-diagnostic-2026-11-11.md);
- [regulation-market-structure-portability.md](regulation-market-structure-portability.md);
- [industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md).

**Method:** public sources only. We created no accounts, made no posts and contacted no one.

---

## 1. Summary

1. **The corpus has 244 records: 149 complaints, 16 mixed and 79 praise.** This falls short of a balanced 150+ complaint set from all intended venues, because Reddit was fully blocked and the Bogleheads forum could only be read through search-engine extraction (§9).
   - **Venues:** App Store reviews 104, forums 62, Trustpilot 43, and 28 litigation, regulator, press, advocacy and survey items.
   - **Praise:** most of the 79 praise records come from App Store reviews of challenger apps (Daffy 28, Groundswell 8) and from nonprofit reviews of Benevity on Trustpilot (21).
2. **Complaint volume follows venue, not underlying defect rates.** By count, the top complaint/mixed categories are UX/app defects (30), account access/login (24), grant delay (21), nonprofit receipt/attribution (17) and grant rejection/sponsor discretion (17).
   - The two largest categories come almost entirely from one source: the Fidelity Charitable iOS app, which has 53 written reviews over 13 years, 38 of them 1–2 stars ([App Store](https://apps.apple.com/us/app/fidelity-charitable/id552407907)).
   - **Medium confidence** that the app has chronic login and crash problems. **Low confidence** that this matters commercially: the app shows only 24 current ratings, which suggests few donors use it.
3. **The highest-severity complaints are structural. They come from the sponsor's legal control, not from software.** Examples:
   - Fairbairn (liquidating ~$100M of donated stock) ([ThinkAdvisor](https://www.thinkadvisor.com/2021/03/01/fidelity-charitable-wins-lawsuit-over-stock-donation/));
   - the 2026 SPLC grant holds at Fidelity Charitable, Vanguard Charitable and DAFgiving360, which drew a 16-attorney-general letter ([CA AG](https://oag.ca.gov/node/623769));
   - removal of UNRWA USA from Fidelity Charitable's charity search ([Rolling Stone](https://www.rollingstone.com/politics/politics-features/fidelity-charitable-donations-gaza-relief-unrwa-1235007400/));
   - a successor adviser locked out of a $21M fund ([InvestmentNews](https://www.investmentnews.com/practice-management/multimillion-dollar-donor-advised-fund-lawsuit-puts-spotlight-on-control-risks/265478));
   - donors "ghosted" by a crypto DAF claiming ~$10B ([Chronicle](https://www.philanthropy.com/news/donors-say-they-were-ghosted-by-a-10-billion-daf/)).
   - **Every donor lawsuit we found against a major sponsor failed or is pending** (Fairbairn lost at trial; Pinkert dismissed for standing ([9th Cir.](https://caselaw.findlaw.com/court/us-9th-circuit/1912100.html))). Complaining donors' realistic options are to exit, to push through AGs or the press, or to move their money.
4. **Nonprofits complain about different things than donors.**
   - Nonprofits: grant delay (10 of 28 coded nonprofit complaint/mixed records), receipt and attribution problems (9), and rail fees (3). The aggregate surveys agree: in CEP's survey, 44% of nonprofits said DAFs hamper donor relationships ([Chronicle](https://www.philanthropy.com/news/some-nonprofits-say-donor-advised-funds-hurt-relationships-with-supporters/)).
   - Donors: app and login (53 of 115 donor complaint/mixed records), fees and minimums (11), delay (10) and discretion (9).
   - The most concentrated nonprofit pain in this corpus comes from **workplace-giving and payment intermediaries** (Benevity, PayPal Giving Fund via GoFundMe), not from the national DAF sponsors ([Trustpilot Benevity](https://www.trustpilot.com/review/benevity.com); [Minnesota Council of Nonprofits](https://minnesotanonprofits.org/?p=4641)).
5. **Paper checks are a cross-cutting root cause.** Records include:
   - voided uncashed checks ([Bogleheads t=457510](https://www.bogleheads.org/forum/viewtopic.php?t=457510));
   - address-change failures ([Bogleheads t=246729](https://www.bogleheads.org/forum/viewtopic.php?t=246729));
   - a Benevity fee of "$35 or 8%" per check ([Trustpilot](https://www.trustpilot.com/review/benevity.com));
   - DAFgiving360 described as "only paper checks" ([Bogleheads t=464478](https://www.bogleheads.org/forum/viewtopic.php?t=464478&start=100)).
   - Fidelity Charitable's reported move to EFT-only grants from July 1, 2026, later extended, is the most important 2026 change. Public statements conflict on its status ([Bogleheads t=464478](https://www.bogleheads.org/forum/viewtopic.php?t=464478); [Fidelity nonprofit page](https://www.fidelitycharitable.org/nonprofits/overview.shtml)).
6. **Classification:** 117 complaint/mixed records are coded **fixable** (UX, login, service, notices, rails) and 47 **structural** (§4966 sponsor control, discretionary declines, liquidation, portability frictions, succession).
   - Structural records are fewer but far more severe: all 5 "critical" records are structural.

---

## 2. Scope, definitions and coding

**What we counted.** Each record is one dated, sourced statement of dissatisfaction (or praise) about:
- a DAF sponsor (national, community, faith or challenger);
- a DAF technology vendor or app;
- a payment rail (Chariot/DAFpay, check vs EFT);
- an adjacent intermediary that legally operates as a donor-advised or pass-through charity and that nonprofits experience as part of the same flow (PayPal Giving Fund, Benevity's disbursement charity, GoFundMe's PayPal Giving Fund routing).

Adjacent intermediaries are tagged `org_type` = `workplace_giving_intermediary` or `payment_platform_daf`, so they can be filtered out.

**Complainant types:** donor, donor (employee), successor adviser, financial adviser, nonprofit, state AG, advocacy group, employee. Roles are self-described or inferred from text; `attribution_confidence` records how sure we are.

**Categories** follow the task taxonomy:
- grant_delay
- grant_rejection_discretion
- fees
- investment_options
- liquidation_stock_handling
- account_access
- customer_service
- transfer_portability
- succession_inheritance
- tax_receipt_documentation
- ux_app
- nonprofit_receipt_attribution
- payment_rail_fees
- data_privacy
- other

**Coding rules:**
- Each record gets one primary category and an optional secondary category.
- **Severity:** low (inconvenience), medium (repeated friction or money at risk of delay), high (money withheld for weeks or more, or the product unusable), critical (loss or diversion of charitable assets alleged, or a governance breach).
- **structural_or_fixable:** "structural" means the complaint follows from sponsor legal control (§4966 sponsoring-organization ownership), statutory eligibility rules, liquidation and portability practices, or succession policy. "Fixable" means it could be solved by product, service or rail changes without changing the legal model.

**Evidence grades** reuse the repo scale from [daf-end-to-end-experience-comparative-diagnostic-2026-11-11.md](../daf-end-to-end-experience-comparative-diagnostic-2026-11-11.md):

| Grade | Meaning | Example in this corpus |
|---|---|---|
| E1 | Primary record | Court opinion, AG release, survey |
| E2 | Credible secondary | Press, law-firm analysis |
| E3 | Dated first-person report | Review, forum post |
| E4 | Secondhand or search-extracted | Bogleheads content read via search-engine extraction |

**Quotes** are limited to 25 words. Most records store a short title or excerpt.

---

## 3. Venue access log and record counts

| Venue | Access result (2026-11-14) | Records | Complaint / mixed / praise |
|---|---|---|---|
| Apple App Store (US customer-review RSS) | Accessible. Fidelity Charitable (53 written reviews), Daffy (28), Groundswell (8), DAFpay (6), The Donors Fund (2), Benevity (7 giving-related; 2 volunteer-only reviews excluded) | 104 | 46 / 7 / 51 |
| Trustpilot | Accessible. Benevity (88 reviews; 41 giving-relevant coded, ~21 webinar-feedback reviews excluded), Daffy (1), Chariot (1). Fidelity Charitable, Vanguard Charitable, Schwab Charitable, Every.org, Endaoment and PayPal Giving Fund pages return 404 (no profile). Charityvest has a page but 0 reviews | 43 | 20 / 3 / 20 |
| Bogleheads.org forum | Direct fetch returned HTTP 402. Content read via search-engine extraction (E3/E4) | 46 (incl. 3 carried) | 37 / 4 / 5 |
| Reddit (all subreddits) | **Blocked**: WebFetch refuses reddit.com and old.reddit.com, search tool refuses the domain, JSON endpoint 403 | 13 carried from repo 2026-11-11 files (not re-verified) | 9 / 0 / 4 (plus 3 Bogleheads carried) |
| BBB (bbb.org) | Search works. **No business profiles** for Fidelity Charitable, Schwab Charitable, Vanguard Charitable or Daffy ([BBB search](https://www.bbb.org/search?find_country=USA&find_text=Fidelity%20Charitable)). The only Fidelity complaints are against Fidelity Investments (brokerage), out of scope | 0 | — |
| CFPB complaint database API | Reachable. "donor advised", sponsor names, "charitable" all returned 0 hits; the term search appears not to cover narratives reliably, so this is **inconclusive**, not proof of absence ([API](https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/)) | 0 | — |
| Google Play | Page fetched without reviews rendered ([example](https://play.google.com/store/apps/details?id=com.fidelity.charitable&hl=en_US)); Daffy has no Android app per its Trustpilot reviewer | 0 | — |
| PayPal Community forum | Direct fetch HTTP 503. Content read via search extraction | 3 | 3 / 0 / 0 |
| Courts, AGs, press, advocacy, surveys, vendors | Accessible via search and fetch | 28 | 27 / 1 / 0 |
| Glassdoor | Not searched separately. The SVCF 2018 employee complaints are covered via the Chronicle | — | — |
| **Total** | | **244** | **149 / 16 / 79** |

---

## 4. Frequency analysis

### 4.1 By category (complaint + mixed, n = 165)

| Category | n | Main sources | Typical severity | Structural / fixable |
|---|---|---|---|---|
| ux_app | 30 | Fidelity Charitable app (24), Daffy (3), Benevity (3) | medium–high | fixable |
| account_access (login, 2FA, SSO) | 24 | Fidelity Charitable app (18), Benevity SSO (3), Daffy hardware-key-only 2FA, DAFpay | high | fixable |
| grant_delay | 21 | Benevity (11), Fidelity Charitable (5), DAFgiving360 (3), PayPal Giving Fund, Charityvest | high | mostly fixable; verification delays structural |
| grant_rejection_discretion | 17 | SPLC holds (big three, AGs, coalitions), UNRWA (Fidelity), 990/private-foundation/pledge declines | high | structural |
| nonprofit_receipt_attribution | 17 | PayPal Giving Fund/GoFundMe, voided checks, CRM attribution, anonymity | medium–high | mixed |
| other | 14 | Governance scandals, activity policies, sponsor viability, values objections | varies; includes 3 critical | mostly structural |
| fees (incl. minimums) | 11 | Vanguard minimums/maintenance fee, Daffy tiers, Pinkert, Fidelity "steals" review | medium | fixable (pricing) / structural (affiliated fees) |
| customer_service | 9 | Benevity, SDG Impact Fund, Vanguard brokerage transfer | medium–high | fixable |
| payment_rail_fees | 7 | Paper checks, Benevity check fee, Chariot account closure, Fidelity EFT mandate | medium | fixable |
| transfer_portability | 4 | No in-kind DAF-to-DAF path; Morgan Stanley migration; shutdown risk | medium | structural |
| liquidation_stock_handling | 3 | Fairbairn (×2), Vanguard refusal of in-kind VTSAX | critical/medium | structural |
| tax_receipt_documentation | 3 | Benevity missing confirmation, Fidelity app lacks documents, nonprofit DAF/QCD classification | medium | fixable |
| investment_options | 2 | Daffy cash allocation, adviser-management minimums | low–medium | mixed |
| data_privacy | 2 | Blackbaud 2020 breach at a community foundation; DAFpay anonymity critique | medium | fixable |
| succession_inheritance | 1 | Peterson v. WaterStone | critical | structural |

**Interpretation.** Login, crash and UX complaints dominate because app stores are the most accessible venue and the Fidelity Charitable app has the longest public review history (2012–2026). If the App Store is excluded (n = 112 complaint/mixed), the order changes. Grant delay (20), nonprofit receipt/attribution (17) and grant rejection/discretion (17) lead, and app defects fall to the bottom (UX 4, login 1). **Venue choice decides the headline. Neither ranking is a prevalence estimate.**

### 4.2 By organization

| Organization | Complaint | Mixed | Praise | Dominant complaint | Scale caveat |
|---|---|---|---|---|---|
| Fidelity Charitable (incl. multi-sponsor SPLC items) | 62 | 12 | 11 | App login/crash; discretion (SPLC, UNRWA) | Largest sponsor by accounts and grants, with the longest-lived public app, so the most exposure in any venue |
| Benevity (workplace-giving intermediary) | 25 | 2 | 21 | Disbursement delay to nonprofits; support access | Only sponsor-like entity with an active Trustpilot profile. Nonprofit reviewers are invited to review after webinars, which inflates praise |
| Daffy | 9 | 1 | 28 | Small UX gaps, fee tiers, 2FA | App rating 4.91 from 560 ratings (iTunes lookup, 2026-11-14). The written-review sample skews toward enthusiasts |
| DAFgiving360 (Schwab Charitable) | 9 | 0 | 3 | Slow grants, paper checks, fees | No app reviews; forum only |
| PayPal Giving Fund / GoFundMe | 7 | 0 | 0 | Redirected or unclaimed gifts, unauthorized pages | AG and press items, not individual reviews |
| Vanguard Charitable | 6 | 1 | 0 | $500 grant minimum, $25K threshold, SPLC hold | Forum only. Prior repo item UX-01 (check visibility) |
| Chariot / DAFpay | 3 | 0 | 5 | Login/integration failure; can't close account; privacy critique | DAFpay app has 11 ratings |
| Charityvest | 3 | 0 | 1 | Check batching, viability concern | Forum only |
| SDG Impact Fund; WaterStone; FJP Buffalo; New Britain CF; SVCF | 2 each or fewer | — | — | Governance, access, misuse | Litigation and regulator items |
| Groundswell; The Donors Fund | 0 | 0 | 10 | — | Small written-review samples |

**Normalization caveat.** Raw counts cannot be divided by customer base in any meaningful way:
- The repo puts the standard nationals at roughly $233B of assets ([regulation-market-structure-portability.md](regulation-market-structure-portability.md)), but venue participation is not proportional to accounts.
- The Fidelity Charitable app's 24 current ratings, against hundreds of thousands of donors, imply that well under 1% of donors review. The share is unknown and differs by brand.
- Challenger apps actively solicit reviews.
- The fair statement is that **no sponsor in this corpus shows a complaint rate that can be compared with another sponsor's.** We report only the mix of complaint types within each organization.

### 4.3 Who complains about what

| Complainant | Records (complaint/mixed) | Top categories |
|---|---|---|
| Donors (incl. employee donors) | 115 | UX/app 30, login 23, fees 11, grant delay 10, discretion 9 |
| Nonprofits (individual + aggregate) | 28 | grant delay 10, receipt/attribution 9, rail fees 3, discretion 3 |
| State AGs | 7 | discretion (SPLC), unconsented solicitation (GoFundMe/PPGF), asset misuse (SDG, FJP, New Britain) |
| Advocates and coalitions | 7 | discretion, values objections, privacy |
| Successor advisers | 2 | access revoked, succession |
| Financial advisers | 2 | adviser-management minimums; advisory-only rights after SPLC |

Advisers are under-represented, as expected. Advisers rarely post sponsor complaints publicly. Their documented grievance, sponsors that bar adviser management or set $250K+ minimums, comes from trade press written by a competing sponsor (AEF) ([WealthManagement](https://www.wealthmanagement.com/philanthropy/importance-professional-asset-management-daf-accounts)).

### 4.4 Trends over time

Records by year (complaint+mixed / praise): 2021 17/7, 2024 15/15, 2025 32/24, 2026 40/11. 2026 is the highest year for complaints, for three reasons:
1. The SPLC hold cluster (April–October 2026) added ten discretion records across press, AG and forum venues.
2. Fidelity Charitable's October 2026 app update crashed on iOS 27, prompting three reviews in two weeks ([App Store](https://apps.apple.com/us/app/fidelity-charitable/id552407907)).
3. Benevity's nonprofit complaints rose.

The Fidelity Charitable app shows the same login defect returning across versions 1.0 (2012–13), 2.x (2016–18), 3.x (2020–22) and 4.x (2023), each time after an iOS or app update. This suggests a regression-testing gap rather than a one-off bug (inference, medium confidence). App complaints in 2025–26 move from login toward feature regressions: lost tax-lot selection and lost editing of recurring grants.

---

## 5. Notable cases

### 5.1 Fairbairn v. Fidelity Investments Charitable Gift Fund (filed 2018; decided 2021)

**Facts:**
- Malcolm and Emily Fairbairn gave about 1.93M Energous shares (roughly $100M) to their Fidelity Charitable account in late December 2017.
- They alleged that Fidelity sold the whole block in the last ~2.5 hours of the year's last trading day, against promises including a 10%-of-daily-volume cap, and that the sale drove the price down ([ThinkAdvisor](https://www.thinkadvisor.com/2021/03/01/fidelity-charitable-wins-lawsuit-over-stock-donation/); [Bloomberg Tax](https://news.bloombergtax.com/daily-tax-report/fidelity-wins-battle-over-donated-stock-alleged-tax-losses)).

**Rulings:**
- An earlier ruling held that the sponsor's legal control did **not** bar a donor's claim of false promises ([Bloomberg Law](https://news.bloomberglaw.com/daily-tax-report/insight-organization-control-over-donor-advised-fund-requirement-doesnt-trump-donors-claim-of-false-promises)).
- After a bench trial, the court found for Fidelity in February 2021. The employee testified that Fidelity "typically" traded under 10%, and the court found no binding promise and no negligent trading ([ThinkAdvisor](https://www.thinkadvisor.com/2021/03/01/fidelity-charitable-wins-lawsuit-over-stock-donation/)).

**Classification:** structural (liquidation at sponsor discretion), critical severity.

**What it shows:** the most financially consequential DAF complaint on record concerns contribution-side liquidation, not grants. Sponsors' liquidation policies match the portability analysis: Vanguard liquidates "at its sole discretion", and DAF-to-DAF transfers are generally made in cash ([regulation-market-structure-portability.md](regulation-market-structure-portability.md)).

### 5.2 Pinkert v. Schwab Charitable Fund (2020–2022)

**Claim:** a donor alleged that Schwab Charitable overpaid affiliated custody and brokerage fees to Charles Schwab & Co.

**Outcome:** dismissed for lack of standing, and the Ninth Circuit affirmed in September 2022. The donor had agreed to fees that were disclosed ([Justia](https://cases.justia.com/federal/district-courts/california/candce/3:2020cv07657/368135/74/0.pdf); [FindLaw](https://caselaw.findlaw.com/court/us-9th-circuit/1912100.html)).

**Classification:** structural fee complaint. It links directly to the affiliated-fee incentive described in [industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md).

**What it shows:** fee grievances about affiliated providers are nearly impossible to bring in court. That leaves pricing competition (Daffy, Charityvest) and disclosure as the only remedies.

### 5.3 The 2026 SPLC grant holds

**What happened:**
- After the April 2026 indictment of the Southern Poverty Law Center, Fidelity Charitable, Vanguard Charitable and DAFgiving360 halted grants ([Fox Business](https://www.foxbusiness.com/markets/fidelity-vanguard-reportedly-pause-splc-grants-federal-fraud-charges)).
- SPLC's October 2026 list adds Mightycause Charitable Foundation and a Goldman Sachs DAF program ([SPLC](https://www.splcenter.org/resources/hopewatch/president-ceo-donor-advised-funds/)).

**Complaints came from every stakeholder group:**
- 16 state AGs ([CA AG](https://oag.ca.gov/node/623769)), with Illinois warning that automatic cutoffs create "problems for donors" ([IL AG](https://illinoisattorneygeneral.gov/news/story/attorney-general-raoul-urges-funds-to-reevaluate-decision-to-cut-off-donations-to-southern-poverty-law-center));
- a major-donor coalition ([Democracy Alliance](https://democracyalliance.org/articles/major-donors-donor-networks-and-foundations-call-on-fidelity-vanguard-and-charles-schwab-to-reverse-harmful-capitulation-to-administrations-politicized-attack-on-southern-poverty-law-cent/));
- competing community foundations inviting transfers ([SFF](https://sff.org/big-daf-platforms-drop-southern-poverty-law-center-underscoring-need-for-impact-investors-to-choose-partners-wisely/));
- the nonprofit movement ([Community-Centric Fundraising](https://communitycentricfundraising.org/2026/05/13/a-statement-regarding-the-three-largest-daf-sponors-halt-on-grant-making-to-the-southern-poverty-law-center/));
- ordinary donors on Bogleheads ([t=470890](https://www.bogleheads.org/forum/viewtopic.php?t=470890); [t=470976](https://www.bogleheads.org/forum/viewtopic.php?t=470976)).

Bogleheads posters quoted Fidelity's guideline that an organization under government investigation is not treated as operating exclusively for charitable purposes ([t=470976](https://www.bogleheads.org/forum/viewtopic.php?t=470976)).

**Classification:** structural (sponsor control and liability aversion).

**What it shows:** this is the first recorded case where a discretion complaint produced organized calls to switch sponsors. We found **no outflow data** (queue item P-CMP-04).

### 5.4 Other discretion cases

- **UNRWA USA (2024).** Removed from Fidelity Charitable's eligible-charity search without announcement, despite IRS good standing. A Change.org petition followed ([Rolling Stone](https://www.rollingstone.com/politics/politics-features/fidelity-charitable-donations-gaza-relief-unrwa-1235007400/); [Change.org](https://www.change.org/p/urge-fidelity-charitable-to-reinstate-unrwa-on-their-giving-platform)). We found no confirmation of reinstatement.
- **The reverse complaint.** Activists object to sponsors *processing* grants they consider harmful: the Unmasking Fidelity coalition ([The Scope](https://thescopeboston.org/7120/news/fidelity-charitable-exposed-for-funding-hate-groups-activists-demand-disclosure/)) and critics of NCF's $56M to groups labeled hate groups ([Advocate](https://www.advocate.com/religion/2019/3/19/christian-foundation-huge-funder-anti-lgbtq-hate-groups)).
- **Sponsors are squeezed from both sides.** Any discretion policy draws complaints from someone. That is a structural property of §4966 control, not a product defect.

### 5.5 Successor adviser locked out: Peterson v. WaterStone (2026)

**Claim:** the successor adviser to a $21M family DAF says WaterStone (Christian Community Foundation) revoked his online access, stopped communicating and refused his grant recommendations, including about $1M. He sued in January 2026 ([InvestmentNews](https://www.investmentnews.com/practice-management/multimillion-dollar-donor-advised-fund-lawsuit-puts-spotlight-on-control-risks/265478); [MinistryWatch](https://ministrywatch.com/client-sues-waterstone-claims-he-was-blocked-from-family-account/)).

**Sponsor's position:** WaterStone cites its ultimate control and the original donor's instructions.

**Status: sources conflict.** Foley (May 2026) describes the motion to dismiss as pending ([Foley](https://www.foley.com/insights/publications/2026/05/new-lawsuit-tests-the-limits-of-donor-advised-fund-advisory-privileges/)). A Greenleaf Trust note suggests dismissal for standing ([Greenleaf](https://greenleaftrust.com/missives/donor-advised-funds-back-in-court/)).

**Classification:** structural (succession and advisory privilege), critical severity.

### 5.6 Sponsor failure and fraud

- **SDG Impact Fund.** About six donors told the Chronicle that the fund, which claimed ~$10B mostly in crypto, stopped returning calls, refused grants and asset returns, and solicited loans ([Chronicle](https://www.philanthropy.com/news/donors-say-they-were-ghosted-by-a-10-billion-daf/)). Georgia's AG sued, alleging donor money paid for tuition, vacations and tickets, and asked for a receiver ([WSB-TV](https://www.wsbtv.com/news/local/atlanta/where-did-money-go-ag-sues-charity-spotlighted-by-channel-2/76726H6FXFCW5JQXC2N2VOTEQQ/)).
- **Foundation for Jewish Philanthropies (Buffalo).** New York's AG found the former CEO misused about $3.1M of donor-advised and other funds ([Nonprofit Issues](https://www.nonprofitissues.com/node/2964)).
- **Community Foundation of Greater New Britain.** Connecticut opened an investigation in June 2026 into a former mayor's DAF at the foundation ([CT AG via pubt.io](https://pubt.io/view/E30BE1AA1335C93B56D6EAE7F82F85169F3EB9E1)).

These are the only "critical" governance complaints. They concentrate in small or unconventional sponsors, which supports the repo view that sponsor viability and governance are real donor risks outside the nationals.

### 5.7 Payment-platform DAFs and nonprofits

- **PayPal Giving Fund, 2017.** A class action alleged that gifts to unenrolled charities were redirected ([NPR](https://www.npr.org/sections/thetwo-way/2017/02/28/517790137/lawsuit-alleges-that-paypal-diverted-donations-to-different-charities)).
- **PayPal Community forum.** Charities report unpaid gifts after six weeks, and donors report gifts sent to similarly named charities ([PayPal Community](https://www.paypal-community.com/t5/About-Payments/PayPal-Giving-Fund-problem/td-p/954817)).
- **GoFundMe, October 2025.** GoFundMe created about 1.4M nonprofit pages without consent, routed funds via PayPal Giving Fund, and required acceptance of its terms before a page could be removed ([Minnesota Council of Nonprofits](https://minnesotanonprofits.org/?p=4641)). This drew a multistate AG letter ([NY AG](https://ag.ny.gov/sites/default/files/letters/multistate-letter-on-gofundme-letters-2026.pdf)) and reportedly an Alaska AG lawsuit in March 2026 ([Oakland Voices](https://oaklandvoices.us/2026/04/13/california-attorney-general-gofundme-pages/)).
- **Benevity.** Trustpilot holds 88 reviews with 47% at 1 star ([Trustpilot](https://www.trustpilot.com/review/benevity.com)). Nonprofits describe moving release dates, months-long delays and a check fee of "the higher of $35 … or 8%". Many other nonprofits praise it.

**Implication:** nonprofits experience intermediated giving as one category. Their worst experiences sit at the payment and intermediary layer, where gifts are pooled, held until a charity enrolls, or batched.

### 5.8 Grant delay and paper checks at national sponsors

- **DAFgiving360.** Donors reported grants taking 2–3 months and switched to Fidelity ([t=360946](https://www.bogleheads.org/forum/viewtopic.php?t=360946)). Others reported on-time grants.
- **Fidelity Charitable.**
  - A 2025 App Store review says grants "can be held up for months" with no communication ([App Store](https://apps.apple.com/us/app/fidelity-charitable/id552407907)).
  - A 2022 Ukraine-relief grant sat a week under sanctions review and cleared after a phone call ([t=372045](https://www.bogleheads.org/forum/viewtopic.php?t=372045)).
  - Voided checks after ~90 days are a recurring forum topic ([t=457510](https://www.bogleheads.org/forum/viewtopic.php?t=457510)). Fidelity's own FAQ confirms that uncashed checks are voided and that it cannot give nonprofits the donor's contact details ([Fidelity grant-delivery FAQ](https://www.fidelitycharitable.org/help/grant-delivery-faq.html)).
- **Vanguard Charitable.** The prior repo item UX-01 records a donor's repeated reissues and lack of check visibility ([r/fatFIRE](https://www.reddit.com/r/fatFIRE/comments/1938ysc)).
- **EFT-only transition.** Bogleheads quotes Fidelity's notice that "beginning July 1, 2026, all … grants will be delivered exclusively through EFT", followed by an extension ([t=464478](https://www.bogleheads.org/forum/viewtopic.php?t=464478)). Fidelity's live nonprofit page still says EFT is "not currently" required ([Fidelity](https://www.fidelitycharitable.org/nonprofits/overview.shtml)).

### 5.9 Challenger platforms

Daffy draws mostly praise (28 of 38 records): low fixed fees, easy stock and crypto funding. Its complaints are narrow:
- hardware-key-only 2FA with no TOTP ([App Store](https://apps.apple.com/us/app/daffy-save-invest-give/id1578035540));
- no Android app ([Trustpilot](https://www.trustpilot.com/review/daffy.org));
- ETF recognition, irreversible tier upgrades, cash drag and check-by-default grants ([t=438382](https://www.bogleheads.org/forum/viewtopic.php?t=438382));
- viability questions ([r/fatFIRE](https://www.reddit.com/r/fatFIRE/comments/1jzb8hb/daffy_donor_advised_fund_company_stable/)).

Charityvest draws praise for easy transfers, plus complaints about twice-monthly check batches and early transparency ([t=417491](https://www.bogleheads.org/forum/viewtopic.php?t=417491); [t=317726](https://www.bogleheads.org/forum/viewtopic.php?t=317726)).

Chariot/DAFpay has the most mixed record:
- praise: "game changer";
- complaints: a 1-star "never worked" with Fidelity login integration ([App Store](https://apps.apple.com/us/app/dafpay/id6633440388)), a Trustpilot complaint about being unable to close an account ([Trustpilot](https://www.trustpilot.com/review/givechariot.com)), and an IPS critique of anonymity and credential sharing ([Inequality.org](https://inequality.org/article/new-donor-advised-fund-tech-raises-old-concerns/)).
- DAFpay's standard 2.9% fee is paid by the nonprofit ([search summary of Chariot help center](https://help.givechariot.com/dafpay/dafpay-faqs)). No nonprofit complaint about it surfaced in accessible venues.

---

## 6. Structural vs fixable

| Class | Records (complaint/mixed) | Categories | Who can fix | Examples |
|---|---|---|---|---|
| **Fixable: product/UX** | ~54 | ux_app, account_access | Sponsor or vendor engineering | Fidelity app login regressions; Daffy 2FA; Benevity SSO |
| **Fixable: service/communication** | ~20 | customer_service, grant status notices, tax confirmations | Sponsor operations | "No communication" on held grants; Benevity unreachable support |
| **Fixable: rails** | ~20 | payment_rail_fees, check-related receipt failures | Sponsor + nonprofit + rail vendor | Paper-check voids, address changes, $35/8% check fee, EFT enrollment queue |
| **Fixable: pricing** | ~9 | fees (minimums, tiers) | Sponsor pricing | Vanguard $500 minimum; Daffy tiers |
| **Structural: legal control/discretion** | ~20 | grant_rejection_discretion, succession | Only law, or a sponsor's choice of policy | SPLC, UNRWA, WaterStone, 990/pledge rules |
| **Structural: asset handling/portability** | ~7 | liquidation, transfer_portability | Industry standards / regulation | Fairbairn; no in-kind DAF-to-DAF; history loss |
| **Structural: governance/fraud** | ~6 | other (critical) | Regulators, AGs | SDG Impact Fund, FJP Buffalo, New Britain CF |
| **Structural: nonprofit data model** | ~8 | nonprofit_receipt_attribution (sponsor-as-legal-donor) | Partly fixable with data standards | CRM soft credit, anonymity, Form 990 donor identity |

Counts are approximate where categories split. The exact coding is in the CSV column `structural_or_fixable` (117 fixable, 47 structural).

**Key point:** fixable complaints are more numerous, but structural complaints drive litigation, AG involvement and organized switching. Entrants can win on the fixable layer: Daffy's praise ratio shows this. Every entrant still inherits the structural layer.

---

## 7. Links to repo hypotheses

| Repo hypothesis | What the complaint corpus adds | Direction | Confidence |
|---|---|---|---|
| **Portability lock-in is practical, not legal** ([regulation-market-structure-portability.md](regulation-market-structure-portability.md)) | Donors confirm the transfer is cash-only, needs the sending sponsor's cooperation and leaves money out of the market for weeks ([t=462044](https://www.bogleheads.org/forum/viewtopic.php?t=462044)). Vanguard refused in-kind VTSAX ([t=284384](https://www.bogleheads.org/forum/viewtopic.php?t=284384)). Some switching does happen: Schwab→Fidelity ([t=360946](https://www.bogleheads.org/forum/viewtopic.php?t=360946)), Morgan Stanley→Fidelity/Schwab ([r/fatFIRE](https://www.reddit.com/r/fatFIRE/comments/1w4unkb/do_you_have_a_donor_advised_fund/)). SPLC created organized switching calls | Supports | Medium |
| **Paper checks persist from habit on both sides** ([industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md)) | Checks are the root of voids, address failures, lost-check hunts and intermediary check fees. Fidelity's move to EFT-only shows the largest sponsor treating checks as a cost. Rollout conflicts and the ACH queue show that nonprofit enrollment is the bottleneck | Supports; adds nonprofit-enrollment constraint | Medium-high |
| **Sponsor discretion is a growing risk (2026 SPLC)** | Discretion complaints are the fastest-growing high-severity category in 2026 and the only one drawing multistate AG letters. Complaints come from both political directions (UNRWA vs NCF/"Unmasking Fidelity") | Supports | High |
| **Asset-based fees create retention incentives** | Fee complaints exist (Pinkert; "steals in fees" review; Vanguard minimums and maintenance fee), but they are fewer than delay or discretion complaints. Pinkert shows that courts will not police affiliated fees. No complaint links fees to slower grants | Neutral; effect remains unsupported | Low |
| **AI-agent risk** ([ai-governance-failure-modes.md](ai-governance-failure-modes.md)) | Benevity users already complain of being "passed through AI bots" with no human ([Trustpilot](https://www.trustpilot.com/review/benevity.com)). Grant holds with "no communication" are the scenario an agent would worsen if it cannot explain a decline. Connectors (DAFpay) already draw credential and anonymity critiques | Supports caution on agentic support and connectors | Medium |
| **Nonprofit burden is a separate UX problem** ([daf-end-to-end-experience-comparative-diagnostic-2026-11-11.md](../daf-end-to-end-experience-comparative-diagnostic-2026-11-11.md)) | 28 nonprofit records are dominated by delay and attribution. CEP and Lilly surveys quantify concern (44% relationship harm; 55% concerned about soliciting DAF gifts) ([Chronicle](https://www.philanthropy.com/news/nonprofits-concerned-about-seeking-and-processing-donor-advised-fund-gifts/)) | Supports | Medium-high |

---

## 8. Implications

**For entrants:**
1. The fixable layer is open to compete on: reliable login, modern 2FA (TOTP and passkeys), proactive grant-status notices, EFT by default, Android parity and tax-document access. Daffy's 28:9 praise-to-complaint ratio in reviews shows that donors reward this, though the ratio is inflated by solicited reviews.
2. Do not promise control the law does not grant. The largest losses (Fairbairn, WaterStone) came from donors' expectations about liquidation and succession. Publish liquidation methods (e.g., volume caps) and succession terms in plain language, and make decline reasons explainable.
3. Viability is a trust tax for small sponsors (Daffy and Charityvest viability threads; the SDG Impact Fund collapse). Publish 990s and audited statements, plus a wind-down and transfer plan that includes grant-history export.
4. Do not cut human support when automating. "AI bots" is already a complaint.

**For incumbents:**
1. App regression testing. The Fidelity Charitable app's repeated login failures, 2012–2026, are cheap to fix and appear in every update cycle.
2. Communicate holds and declines. "No communication" turns a compliance review into a reputational complaint. A reason code and expected date would turn many grant-delay complaints into neutral events.
3. Discretion policy is now an AG-level issue. The SPLC holds show that broad "under investigation" clauses produce coordinated complaints, and competitors use them to recruit.
4. Nonprofit-side tooling (EFT enrollment, donor-identity passthrough, grant letters with stable IDs) addresses the second-largest stakeholder's complaints.

**For the industry report:** present complaint findings by stage (contribution, investment, recommendation, approval, payment, receipt, succession) and by class (structural vs fixable), not as sponsor league tables.

---

## 9. Limitations and selection bias

- **Venue blocking.** Reddit, the largest donor venue, was inaccessible (fetch and search both refused). Bogleheads content came from search-engine extraction, not from reading posts. Attribution of specific claims to specific threads is approximate in some records (`attribution_confidence` = low or medium). Thread dates are estimated from thread IDs or content.
- **App-store dominance.** 104 of 244 records are App Store reviews, and 53 are about one app. Excluding them changes the category ranking (§4.1).
- **Negative and positive selection.**
  - Complainers are unrepresentative. People post after failures.
  - Praise is also selected: challenger apps prompt for reviews, and Benevity's praise comes partly from webinar-feedback solicitations (we excluded about 21 webinar-only reviews but kept platform praise).
- **No denominators.** We cannot compute complaint rates per account or per grant.
- **Adjacent entities.** Benevity, PayPal Giving Fund and GoFundMe are not classic DAF sponsors. They are included because nonprofits experience them as the same flow. Filter on `org_type` to exclude them.
- **Interested sources.** Chariot, AEF, SFF, SPLC and advocacy groups are interested parties and are graded accordingly.
- **Allegations are not findings.** Lawsuit and press claims (WaterStone, SDG, Benevity reviews) are recorded as complaints, not facts.
- **CFPB result is inconclusive.** The API returned 0 for every DAF term and also for generic words, which points to a query-method limit.
- **Time variance.** Many records describe older software or policies. 2012–2023 app reviews do not describe the current app.

---

## 10. Source register (principal sources)

| ID | Source | Date | URL |
|---|---|---|---|
| S01 | Fidelity Charitable iOS app reviews (RSS) | 2012–2026 | https://apps.apple.com/us/app/fidelity-charitable/id552407907 |
| S02 | Daffy iOS app reviews | 2021–2026 | https://apps.apple.com/us/app/daffy-save-invest-give/id1578035540 |
| S03 | DAFpay iOS app reviews | 2024–2026 | https://apps.apple.com/us/app/dafpay/id6633440388 |
| S04 | Groundswell iOS app reviews | 2022–2024 | https://apps.apple.com/us/app/groundswell-giving-charity/id1597818417 |
| S05 | Benevity iOS app reviews | 2019–2026 | https://apps.apple.com/us/app/benevity/id1437459628 |
| S06 | Trustpilot Benevity (pp. 1–3) | 2025–2026 | https://www.trustpilot.com/review/benevity.com |
| S07 | Trustpilot Daffy | 2025-05-28 | https://www.trustpilot.com/review/daffy.org |
| S08 | Trustpilot Chariot | 2026-11-02 | https://www.trustpilot.com/review/givechariot.com |
| S09 | Bogleheads: Fidelity DAF eliminating checks | 2025-12 to 2026-10 | https://www.bogleheads.org/forum/viewtopic.php?t=464478 |
| S10 | Bogleheads: Vanguard or Schwab DAF | c.2021 | https://www.bogleheads.org/forum/viewtopic.php?t=360946 |
| S11 | Bogleheads: Donations barred / SPLC | 2026-04/05 | https://www.bogleheads.org/forum/viewtopic.php?t=470976 ; https://www.bogleheads.org/forum/viewtopic.php?t=470890 |
| S12 | Bogleheads: Fidelity not releasing grant | 2022 | https://www.bogleheads.org/forum/viewtopic.php?t=372045 |
| S13 | Bogleheads: Daffy | c.2024 | https://www.bogleheads.org/forum/viewtopic.php?t=438382 |
| S14 | Bogleheads: DAF-to-DAF transfer | c.2025 | https://www.bogleheads.org/forum/viewtopic.php?t=462044 |
| S15 | Fairbairn ruling coverage | 2021-03-01 | https://www.thinkadvisor.com/2021/03/01/fidelity-charitable-wins-lawsuit-over-stock-donation/ |
| S16 | Pinkert, 9th Cir. | 2022-09 | https://caselaw.findlaw.com/court/us-9th-circuit/1912100.html |
| S17 | Peterson v. WaterStone | 2026 | https://www.investmentnews.com/practice-management/multimillion-dollar-donor-advised-fund-lawsuit-puts-spotlight-on-control-risks/265478 ; https://www.foley.com/insights/publications/2026/05/new-lawsuit-tests-the-limits-of-donor-advised-fund-advisory-privileges/ |
| S18 | 16-AG SPLC letter | 2026-05-22 | https://oag.ca.gov/node/623769 |
| S19 | SDG Impact Fund (Chronicle; GA AG) | 2025–2026 | https://www.philanthropy.com/news/donors-say-they-were-ghosted-by-a-10-billion-daf/ |
| S20 | Fidelity/UNRWA (Rolling Stone) | 2024 | https://www.rollingstone.com/politics/politics-features/fidelity-charitable-donations-gaza-relief-unrwa-1235007400/ |
| S21 | PayPal Giving Fund class action (NPR) | 2017-02-28 | https://www.npr.org/sections/thetwo-way/2017/02/28/517790137/lawsuit-alleges-that-paypal-diverted-donations-to-different-charities |
| S22 | GoFundMe unauthorized pages | 2025–2026 | https://minnesotanonprofits.org/?p=4641 ; https://ag.ny.gov/sites/default/files/letters/multistate-letter-on-gofundme-letters-2026.pdf |
| S23 | CEP nonprofit survey | 2020-01 | https://www.philanthropy.com/news/some-nonprofits-say-donor-advised-funds-hurt-relationships-with-supporters/ |
| S24 | Lilly/Schwab nonprofit study | 2020-10 | https://www.philanthropy.com/news/nonprofits-concerned-about-seeking-and-processing-donor-advised-fund-gifts/ |
| S25 | IPS DAFpay critique | c.2024 | https://inequality.org/article/new-donor-advised-fund-tech-raises-old-concerns/ |
| S26 | Fidelity Charitable nonprofit EFT page | accessed 2026-11-14 | https://www.fidelitycharitable.org/nonprofits/overview.shtml |
| S27 | BBB search (no sponsor profiles) | 2026-11-14 | https://www.bbb.org/search?find_country=USA&find_text=Fidelity%20Charitable |
| S28 | CFPB complaint API | 2026-11-14 | https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/ |

Every record's own URL is in the CSV.

---

## 11. Data dictionary: `daf-user-complaints-corpus.csv`

| Column | Type | Definition |
|---|---|---|
| record_id | text | `CMP-NNN`, sequential |
| source_url | URL | Page holding the complaint (thread, review page, ruling, release) |
| date | text | Publication or review date. ISO day where known; `c.YYYY` or a range for forum threads |
| date_precision | enum | `day`, `month`, `month/year`, `approx (thread id / content)` |
| venue | text | Named venue, e.g. "Apple App Store (US) customer review RSS", "Bogleheads.org forum", "Trustpilot" |
| venue_type | enum | app_store, forum, review_site, litigation, regulator, press, advocacy, survey, vendor, other |
| organization | text | Entity complained about. Multi-sponsor items list each sponsor separated by ";" |
| org_type | enum | national_sponsor, national_sponsor_challenger, community_foundation, faith_sponsor, community_or_faith_sponsor, other_sponsor, payment_rail, payment_platform_daf, workplace_giving_intermediary, workplace_daf_platform, industry, mixed |
| complainant_type | text | donor, donor (employee), nonprofit, adviser, successor advisor, state AG, advocacy, employee, unclear (self-described or inferred) |
| valence | enum | complaint, mixed, praise |
| category | enum | Primary category (taxonomy in §2), or `praise` |
| secondary_category | enum | Optional second category |
| severity | enum | low, medium, high, critical; `n/a` for praise |
| structural_or_fixable | enum | structural, fixable; `n/a` for praise |
| paraphrase | text | Neutral summary; app and Trustpilot rows append star rating and version |
| short_quote | text | ≤25 words (often the review title) |
| resolution | text | Resolution if stated, else "not stated" |
| evidence_grade | text | E1–E4 (see §2) |
| attribution_confidence | text | high, medium, low, with reason |
| access_date | date | 2026-11-14 |
| notes | text | Provenance (App Store review id; "carried from repo"; extraction caveats) |

**Reproduction:** App Store rows come from `https://itunes.apple.com/us/rss/customerreviews/page=N/id=<appId>/sortby=mostrecent/json` (pages 1–10). The coding map is applied by review id, and review ids are kept in `notes`.
