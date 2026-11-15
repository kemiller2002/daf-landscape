# How large universities, medical centres and DAF sponsors handle DAF grants (P-NEW-HED-01)

- **Queue item:** P-NEW-HED-01, a new direction from the owner. Researched 2026-11-15.
- **Scope:** the 33 largest university and academic-medical-centre (AMC) DAF recipients in [`nonprofit-donate-page-daf-scan-2026.csv`](../../data/mission-2026-11-14/nonprofit-donate-page-daf-scan-2026.csv). The ranks there come from the FY2023–24 top-50-sponsor Schedule I lines built by `scripts/mission_recipient_sectors.py`. The four largest sponsors' pledge and benefit rules are compared with them, with Daffy and IRS Notice 2017-73 added for reference.
- **Read first:**
  - [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md). Its wave-24A corrections cover ImpactAssets and SVCF and do not touch this note.
  - [direction-nonprofit-donate-pages.md](direction-nonprofit-donate-pages.md). Wave 24B found mis-picked donate links and DAFpay forms inside iframes. Both bear on §4.
  - [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md). Its corrections (waves 9 and 21) matter here because NPT's Terms of Use ban robots and scripts, so NPT pages were not fetched.
- **Outputs:**
  - [`gift-office-daf-policies-2026.csv`](../../data/mission-2026-11-14/gift-office-daf-policies-2026.csv): 41 rows (33 recipients, 5 sponsors, 1 regulator, 2 market sources).
  - [`queue-proposals-batch41-n16.csv`](../../data/mission-2026-11-14/queue-proposals-batch41-n16.csv): 3 proposals.
- **Rules followed:**
  - **robots.txt** was read for every host before fetching. A 200 response was parsed for user-agent `*`; a 404 meant no rules; anything else meant the host was not fetched. crt.sh was not used.
  - No logins, forms, outreach or submissions.
  - Pages dated before 2021 are flagged.
  - This is research, not legal or tax advice.
- **Evidence labels:**
  - **[F]** first-party page read in full.
  - **[S]** search-engine text only, not verified against the page.
  - **[U]** nothing found.
  - **[R]** not read because of robots.txt.
  - **[I]** inference.

## 0. Answers in brief

| Question | Finding | Confidence |
|---|---|---|
| **DAF-specific acceptance rules** | Every recipient read accepts grants from external DAFs [F/S]. **12 of the 33 also run their own DAF**, with stated minimums from $100k (Cornell [S], Mayo [S]) to $5m (Yale [F]). Caltech says it does not run one [F]. No recipient published a DAF-specific refusal rule apart from the pledge and benefit limits below. | High that external DAF grants are accepted; medium on the in-house count (several are [S]) |
| **Can a DAF grant fulfil a pledge?** | **Recipients are split.**<br>- **Allowed, if the sponsor does not mention the pledge (Notice 2017-73):** Caltech's gift policies [F] and Stanford Live [F].<br>- **Not allowed:** WashU [F], Chicago Booth [F], Penn [S] and Michigan [S, binding pledges].<br>- **Recorded only as a "non-binding intention":** Duke [F], Northwestern [S]. Caltech also uses a "statement of intent" that is not booked [F]. UW will not set up multi-year pledges for DAF funds [S].<br>- **Not stated:** the rest. | High on the [F] rows. The split itself is the finding. |
| **Sponsors' pledge rules** | **Also split.**<br>- NPT allows pledge payment if it does not reference the pledge [S].<br>- Fidelity allows grants toward **non-binding** pledges, with a "Pledge (non-binding)" use code [F].<br>- Vanguard Charitable lists "Fulfillment of legally binding pledges" as an impermissible purpose [F, Jan 2026].<br>- Daffy bars "pre-existing, legally-binding" pledges [F, repo snapshot].<br>- DAFgiving360's Program Policies could not be read [R]. | High for Fidelity, Vanguard and Daffy; NPT is [S] |
| **Events, benefits, membership, naming** | **No recipient offers bifurcation (DAF pays the deductible part, donor pays the rest)** for DAF gifts.<br>- Duke: no DAF grant if anyone receives value, e.g. Iron Dukes basketball ticket rights [F].<br>- UW: DAF gifts cannot pay for gala, golf or fundraising tickets [F].<br>- Stanford Live: withholds its Bing Fling recognition event from DAF givers at the $7,500+ levels [F].<br>- Ohio State Athletics: DAF gifts do not count toward Priority Points or "overall giving to the University/Athletics" [F]. It attributes the rule to DAFgiving360.<br>- Stanford Athletics: refers DAF gifts that unlock priority seating to tax advisers [F].<br>All five sponsors read bar ticket benefits, and Fidelity, Vanguard and Daffy expressly bar bifurcation [F]. **Naming:** Daffy calls naming rights an incidental benefit [F]; Vanguard says the same on an older page [S]. No recipient addressed naming via DAF. | High |
| **DAF grant forms and portals** | **DAFpay:** Notre Dame (from 2025-11-19), Chicago Booth, Stanford Day of Giving [F]; Penn Fund, St Jude [S].<br>**DAF Direct:** WashU, Columbia CUIMC [F]; Harvard, MIT [S].<br>**A notice form for grants started at the sponsor:** Cornell, Cornell Giving Day, Stanford Day of Giving [F].<br>**Columbia's gift-planning page** has a box where donors type their DAF's name and are sent to the sponsor's login [F]. | High |
| **Recognition and campaign credit** | Only **Caltech** publishes counting rules that name DAFs. DAF grants designated by the donor count in campaign totals, and recognition reports include DAF "soft credit" [F]. Cornell Giving Day counts DAF grants once a form is filed [F]. Princeton's Athletics Giving Day does not count same-day DAF gifts unless arranged in advance [F]. Ohio State Athletics excludes DAF gifts from priority credit [F]. | High on the rows read; most recipients are silent |
| **Published DAF share of gifts** | **No recipient published one** [U]. The only figure is sector-wide: DAFs were **10.6% of 2024 giving to higher education**, from CASE as reported by the Chronicle of Philanthropy [S]. AAMC's 2024 survey reports DAF gifts **growing 44.7%**, not their share [S]. | Low for any institution-level figure |

**Reading [I]:**
1. Gift offices and sponsors agree on events and benefits: no tickets, no bifurcation.
2. They do not agree on pledges. Recipients cite the same Code to reach opposite rules. WashU says DAF pledge payment is barred "Under Internal Revenue Code regulations"; Caltech cites Notice 2017-73 to permit it. Sponsors differ again on "binding" versus "non-binding".
3. The workaround that has settled in is the **non-binding intention or statement of intent**: Duke, Northwestern [S], Caltech, and WashU's form [S]. It keeps DAF-funded commitments out of booked pledges.
4. For an entrant, the open product space is matching a donor's stated intention to later DAF grants without the grant referencing it, while still giving the recipient enough to credit the gift. Cornell's and Stanford's notice forms exist for exactly this.

## 1. Recipient universe and coverage

The 33 rows are the university, college and AMC recipients ranked 1–284 in the donate-page scan (FY2023–24 DAF grants from the top-50 sponsors' itemised Schedule I). Together they took **$7.23bn** [C, sum of the scan's `daf_grant_usd_fy2023_2024` for these EINs]. The ranks for Northwestern (74) and Cleveland Clinic (284) come from the same scan.

| Coverage | Recipients |
|---|---|
| **[F] first-party policy or giving page read (15)** | Stanford, Harvard, Cornell, Caltech, Yale, Duke, Dartmouth, Princeton, Columbia, Notre Dame, Chicago (Booth page), University of Washington, Georgetown, Ohio State (Athletics), WashU |
| **[S] search text only (10)** | **Johns Hopkins:** giving.jhu.edu robots.txt returned 403.<br>**MIT:** robots.txt 403.<br>**Penn and Mayo:** recorded as robots-unreadable in the repo scan, so not fetched.<br>**Michigan:** robots allowed, page returned 403.<br>**Not fetched this session:** St Jude, USC, Northwestern, Boston University, Cleveland Clinic. |
| **[U] (1)** | Cedars-Sinai: no public DAF policy surfaced in search |
| **[R] or not researched (7)** | **robots unreadable:** UCSF Foundation, UC Berkeley Foundation, NYU.<br>**robots-disallowed donate host:** Oregon Foundation, Lucile Packard Foundation.<br>**Not researched:** Rockefeller.<br>**Boston College:** its gift policy (Feb 2020) has no DAF clause [S]. |

**Caveat:** the eight unread or snippet-only recipients with robots or fetch problems include the largest one. Johns Hopkins alone took $2.61bn, and its 2026 "DAF Policies and Guidelines" PDF is behind an unreadable robots.txt. The [R]/[S] recipients in P-B41N16-03 account for about $3.7bn [C].

## 2. Comparison table

Full text, URLs and dates are in the CSV. **Rule** = the gift office's stated rule. "—" = not stated on the pages read.

| Entity (rank, FY23–24 DAF $m) | Pledge via DAF | Events / benefits | Membership / priority / naming | Form or portal | Recognition / campaign | Own DAF | Label |
|---|---|---|---|---|---|---|---|
| Johns Hopkins (1, 2,610) | — | — | — | Pledge-payment option on online form; DC campus asks to be notified of DAF grants | — | Yes ($250k, older brochure) | S/R |
| Stanford (3, 626) | Allowed if sponsor does not mention it (Stanford Live) | Recognition event withheld; separate ticket purchase allowed | Athletics: priority-seating gifts referred to tax adviser | DAFpay + notice form (Day of Giving) | Day of Giving counts DAF grants with form | Yes ($1m) [S] | F |
| Harvard (5, 441) | — | No "material return benefit" (general) | Faculty may not give via DAF to their own work | DAF Direct [S] | Receipt to DAF as legal donor [S] | Yes [S] | F/S |
| Cornell (9, 309) | — | — | — | External DAF submission form | Giving Day counts DAF grants via form | Yes ($100k) [S] | F |
| UCSF Foundation (12, 243) | not read | | | | | | R |
| Caltech (13, 216) | **Allowed** if transmittal does not mention pledge, no benefit, no deduction; statement of intent | No quid pro quo | — | Statement-of-intent agreement | **DAF grants counted in campaign; soft credit in recognition** | **No** | F |
| UC Berkeley Fdn (14, 206) | not read | | | | | | R |
| MIT (18, 188) | — | — | — | DAF Direct [S] | — | Yes ($1m) [S] | S |
| Yale (20, 170) | — | — | — | Tell Yale; legal name and EIN | Multi-year pledge credit rule (general) | Yes ($5m) | F |
| Penn (22, 163) | **Not allowed** [S] | — | — | DAFpay on Penn Fund [S] | Penn DAF credited on distribution, not on funding [S] | Yes ($250k) [S] | S |
| Duke (24, 160) | **Non-binding intention only** | **No DAF grant if anyone receives value** | Iron Dukes ticket rights excluded | Note on commitment form | May qualify for matching funds | No | F |
| Dartmouth (25, 159) | — | No expected benefit (general) | Board approves naming | EIN only | CASE recording standards | Yes ($250k) [S] | F |
| Princeton (34, 131) | — | — | Athletics lifetime membership has priority ticket access (DAF not addressed) | EIN only | Athletics Giving Day excludes same-day DAF gifts unless pre-arranged | — | F |
| Columbia (35, 130) | Columbia DAF cannot meet binding pledges [S] | — | — | DAF-name lookup; DAF Direct + email notice (CUIMC) | — | Yes ($1m; ≥50% to Columbia) | F/S |
| Notre Dame (38, 121) | — | — | Football lottery via giving; DAF not addressed [S] | **DAFpay (2025-11-19)** | — | Yes ($500k) [S] | F |
| Chicago, Booth page (39, 121) | **Not allowed** | — | — | DAFpay | — | — | F |
| St Jude (50, 98) | — | Gala sponsorships include tickets [S] | — | On-site DAF tool, DAF email [S] | Grant shows fund name only unless requested [S] | — | S |
| USC (57, 95) | — | — | Athletics Victory Points on cash, not pledges [S] | DAFs listed for athletics [S] | — | — | S |
| Michigan (60, 93) | **Not allowed** (binding) [S] | No tickets or auctions [S] | Athletics Priority Points on lifetime giving [S] | — | — | Yes [S] | S |
| UW Foundation (64, 89) | No multi-year pledge for DAF [S] | **No gala, golf or fundraising tickets** | Tyee Club points (DAF not addressed) [S] | Legal name and EIN | Receipt to DAF [S] | — | F/S |
| Mayo (66, 87) | — | — | Cumulative recognition tiers [S] | — | Publicly credited a named Vanguard Charitable fund's $10m grant to the advising couple [S] | Yes ($100k) [S] | S |
| Northwestern (74, 78) | Non-binding intention form [S] | — | — | Multiyear Intention Form [S] | — | — | S |
| Georgetown (93, 64) | — | — | — | Designation in sponsor's instructions field; gift-accounting email | — | — | F |
| Ohio State (115, 54) | — | **DAF gifts excluded from priority credit** | Priority Points and levels exclude DAF and IRA gifts | — | Excluded from "overall giving to the University/Athletics" for priority | — | F |
| WashU (116, 53) | **Not allowed** ("Under Internal Revenue Code regulations") | — | Eliot Society (DAF not addressed) | **DAF Direct** | — | — | F |
| BU (118, 53) | — | — | — | DAF provider selector [S] | — | — | S |
| Cedars-Sinai (162, 40) | — | Gala tickets sold [S] | — | — | — | — | U |
| Cleveland Clinic (284, 25) | — | — | Members-only events [S] | Pledge-payment link [S] | — | — | S |
| NYU, Oregon Fdn, Lucile Packard, Rockefeller, Boston College | not read | | | | | | R |
| **Fidelity Charitable** | **Non-binding pledges only** | No part of attendance cost; no split gifts | Memberships only if fully deductible [S] | DAF Direct; grant "Use" codes | — | — | F |
| **DAFgiving360** | not read | Ohio State attributes a priority-points exclusion to it | | DAF Direct participant | | | R/S |
| **Vanguard Charitable** | **No legally binding pledges** | No bifurcated grants; no more-than-incidental benefits | Naming rights incidental (older page) [S] | Not a DAF Direct participant (repo) | Advisor chooses named or anonymous | — | F |
| **NPT** | **Allowed if NPT does not reference it** [S] | not read | | | | | S |
| **Daffy** | No pre-existing binding pledges | No gala tickets, auctions, or memberships over $75; no bifurcation | **Naming rights are incidental** | Advisor affirms compliance on each recommendation | | | F |
| **IRS Notice 2017-73** | Reliance rule: no more-than-incidental benefit if the sponsor does not mention the pledge, no other benefit, no deduction | Proposed: DAF paying any part of an advisor's ticket (even the deductible part) is more than incidental; same for memberships | | | | | F |

## 3. Primary-source extracts (quotes ≤40 words)

### 3.1 Regulator

- **[IRS Notice 2017-73](https://www.irs.gov/pub/irs-drop/n-17-73.pdf)**, December 2017 (before the recency window, but in force under its own reliance clause) [F].
  - **Pledges, §4:** a DAF distribution to a charity the advisor pledged to is not a more-than-incidental benefit if (1) "the sponsoring organization makes no reference to the existence of a charitable pledge", (2) no other more-than-incidental benefit, and (3) no deduction is claimed.
  - **Reliance, §7:** "Taxpayers may rely on the rules described in section 4 until additional guidance is issued."
  - **Tickets (proposal only):** "the relief of the Donor/Advisor's obligation to pay the full price of a ticket to a charity-sponsored event can be considered a direct benefit to the Donor/Advisor that is more than incidental."
  - **Memberships:** treated the same way.
  - Whether later guidance superseded §4 was **not checked** (P-B41N16-01).

### 3.2 Recipients

- **[Caltech Gift Policies, 2024-10-01](https://giving.caltech.edu/documents/6199/Caltech_Gift_Policies_2024-10-01.pdf)** [F].
  - **Pledges:** DAF gifts "may be used to make pledge payments on behalf of a donor as long as the pledge is not mentioned in the letter of transmittal, the donor/advisor accrues no benefits (i.e., no quid pro quo)". The policy cites Notice 2017-73.
  - **Campaign counting** includes "grants from donor-advised fund(s) designated by the donor(s)".
  - **Recognition reports** include soft credit for "donor-advised funds".
  - **Statement of intent:** used when a donor plans to pay through a DAF. It "is not considered legally binding, nor is the pledge balance counted in the Institute's financial statements."
- **[Stanford Live DAF and private-foundation guidelines](https://res.cloudinary.com/dopulypdj/image/upload/v1711662327/Guidelines_for_Gifts_from_Donor_Advised_Funds_and_Private_Foundations_FINAL.pdf)**, uploaded 2024-03-28 per the CDN version stamp [F].
  - **Pledges:** "donor advised funds can be used to pay an existing pledge as long as the donor advised fund sponsoring organization makes no reference to the existing pledge."
  - **Recognition event:** "we are unable to extend Bing Fling invitations to donors giving through a donor advised fund."
  - **Tickets:** non-deductible ticket purchases are available separately.
  - **Receipts:** none issued for DAF gifts.
  - This is a unit-level document, not university-wide policy.
- **[Stanford Athletics giving](https://gostanford.com/giving)** [F]: DAF gifts are generally accepted, but donors should consult a tax adviser on gifts that "qualify the donor to purchase priority seating for any Stanford Athletics event."
- **[Stanford Day of Giving FAQ](https://dayofgiving.stanford.edu/pages/faq-2307)** [F]: DAFpay at checkout, or a form for DAF grants started at the sponsor "so we can count your gift."
- **[Duke Gift Planning DAF page](https://giving.duke.edu/gift-planning/gift-plans-in-detail/donor-advised-funds/)** [F].
  - **Pledges:** "Such a commitment would be considered a 'non-binding intention' rather than a legal 'pledge.'"
  - **Benefits:** "DAF grants cannot be used if the donor or anyone else receives something of value in return–such as the ability to purchase basketball tickets in Cameron Indoor Stadium through support of the Iron Dukes."
  - **[Duke Finance DAF records page](https://finance.duke.edu/adrecords/donor-advised-funds/)** [F]: "nor can a donor use a DAF to pay for tickets or ticket rights."
- **[WashU DAF page](https://giving.washu.edu/how-to-give/donor-advised-funds/)** [F].
  - **Pledges:** "Under Internal Revenue Code regulations, a donor-advised fund cannot be used to satisfy a personal pledge made to the University."
  - **DAF Direct:** lists Fidelity Charitable, DAFgiving360 and BNY Mellon Charitable Gift Fund. The repo records that BNY voted on 2024-12-24 to stop its DAF programme, so the list may be stale [I].
- **[Chicago Booth, how to give](https://www.chicagobooth.edu/alumni/giving/how-to-give)** [F]: "A gift from a donor-advised fund may not be used to satisfy a personal obligation such as a pledge." DAFpay is offered on the online form.
- **[University of Washington DAF page](https://www.washington.edu/giving/donor-advised-funds/)** [F]: "DAF gifts cannot be used to pay for tickets to a fundraising event, gala dinner, or golf tournament."
- **[Ohio State Athletics, Priority Points](https://ohiostatebuckeyes.com/sports/2026/4/27/priority)**, 2026-04-27 [F]: "Per Charles Schwab DAF giving 360, gifts from this Donor Advised Fund cannot count towards Priority Points, Annual Priority Levels, Lifetime Priority Levels, or overall giving to the University/Athletics."
- **[Cornell external DAF submission form](https://giving.cornell.edu/how-to-give/daf/)** [F]: notifies Cornell "to make sure your grant is properly credited and designated." [Cornell Giving Day](https://givingday.cornell.edu/info/about) [F]: "Complete this form to have a grant from your DAF included in our totals."
- **[Notre Dame, 2025-11-19](https://giving.nd.edu/giving-to-notre-dame-via-donor-advised-funds-just-got-easier/)** [F]: DAFpay on the giving site; "External DAF gifts now require fewer details."
- **[Columbia Gift Planning DAF page](https://giftplanning.columbia.edu/what-you-can-give/donor-advised-fund)** [F]: a "Give From Your Donor-Advised Fund" box sends donors to their sponsor's login; the Columbia-run DAF needs $1m+. [CUIMC](https://www.giving.cuimc.columbia.edu/ways-give/planned-giving/donor-advised-funds) [F]: DAFDIRECT for Fidelity, Schwab and BNY, plus an email notice to a named officer.
- **[Harvard Gift Policy Guide Overview](https://alumni.harvard.edu/sites/default/files/page/files/Gift_Policy_Guide_Overview.pdf)**, May 2020 (pre-2021, still posted) [F]: faculty may not make a gift "either individually or through a foundation or donor-advised fund" restricted to their own work.
- **[Dartmouth Gift Acceptance Policy](https://policies.dartmouth.edu/policy/gift-acceptance-policy)**, revised 2026-10-17 [F]: gifts "should not be granted with any degree of expected benefit or influence over Dartmouth activities."
- **[Yale DAF page](https://forhumanity.yale.edu/planning-your-gift/donor-advised-funds)** and **[Yale gift policies](https://forhumanity.yale.edu/gift-policies)** [F]: Yale DAF minimum $5m; multi-year annual pledges get full reunion credit in the year documented. Neither is DAF-specific on pledges.
- **[Princeton, how to make a gift](https://alumni.princeton.edu/give/how-make-gift)** and **[Tiger Athletics Giving Day FAQ](https://tagd.princeton.edu/TagdCampaign/Faqs)** [F]: gifts made on the day by DAF are not counted in the competitions unless pre-arranged.
- **[Georgetown gift instructions](https://giving.georgetown.edu/how-to-give/gift-instructions/)** [F]: DAF giving "works the same way as giving through check".

### 3.3 Sponsors

- **Fidelity Charitable** [F]. robots.txt allows these paths. The PDF was fetched directly; the FAQs were read with WebFetch.
  - [Program Guidelines (©2026)](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf): a grant must not "confer a more than incidental benefit on an Account Holder, Authorized Person, or other third party". There is no pledge clause.
  - [Pledge FAQ](https://www.fidelitycharitable.org/faqs/all/grant-pledge.html): "Grant recommendations can be made in support of non-legally binding pledges."
  - [Incidental-benefit FAQ](https://www.fidelitycharitable.org/faqs/all/more-than-incidental-benefit.html): covers "tickets to attend an event, raffle tickets, auction items".
  - [Gala FAQ](https://www.fidelitycharitable.org/faqs/all/grant-gala-event.html): no split payments; the minimum attendance cost must be paid outside the DAF.
- **[Vanguard Charitable Policies & Guidelines, January 2026](https://www.vanguardcharitable.org/sites/default/files/2026-01/policies_and_guidelines_january_2026_011326_final_0.pdf)** [F]. robots.txt allows the path; read with WebFetch.
  - **Impermissible purposes:** "Bifurcated grants" and "Fulfillment of legally binding pledges or other obligations".
  - **Benefits:** "More than incidental benefits, such as receipt of anything of value in return for the grants, such as free dinner or goods or services."
  - **Anonymity:** anonymous grants still state their purpose.
- **[Daffy Member Agreement](https://www.daffy.org/legal/agreement)**, repo snapshot `data/terms-snapshots/daffy-member-agreement/2026-11-14.txt` [F].
  - **Bifurcation:** for a $200 ticket with $100 deductible, "neither portion of the donation can be paid for from the member's Daffy account."
  - **Naming:** "naming rights are an incidental benefit".
- **NPT** [S]. Not fetched because its Terms ban robots and scripts. Search text of its [grantmaking-rules page](https://www.nptrust.org/what-is-a-donor-advised-fund/grantmaking-rules/) says a grant may fulfil a personal pledge if NPT does not reference it in the grant purpose, check memo or cover letter.
- **DAFgiving360** [R]. [Program Policies](https://www.dafgiving360.org/resource/dafgiving360-program-policies) not read (robots.txt 403). A 2017 Schwab Charitable fact sheet seen in search is outside the recency window and was not used.

## 4. Side finding: donate-page scan undercounts university DAF tools

The 2026-11-15 donate-page scan coded `either_any_daf_option = 0` for six recipients whose giving pages offer a DAF tool:
- Stanford: DAFpay and notice form on Day of Giving.
- Columbia: DAF lookup and DAF Direct.
- Notre Dame: DAFpay at checkout.
- WashU: DAF Direct.
- Cornell: DAF submission form. Its donate page was unreachable in the scan, so this 0 is not a scan miss.
- Chicago: DAFpay on Booth's form.

The likely causes [I]:
- the tools sit on DAF or gift-planning pages, not the scanned donate URL;
- DAFpay renders inside the checkout after the gift amount is entered, or in an iframe (wave 24B).

For the other five, the scan's 0 conflicts with the giving pages. So the scan's DAF-option shares are probably a lower bound for large universities (P-B41N16-02).

## 5. Limitations

- **Selection:** universities and AMCs only. Rank order is by top-50-sponsor itemised grants (FY2023–24), not total DAF receipts.
- **Robots and fetching:** eight recipients are [S] or [R] because of robots.txt or fetch problems, including the largest (Johns Hopkins). Several fetch attempts in this session were refused by the session's permission layer; those pages are labelled [S] and were not retried.
- **Unit-level pages:** Stanford Live, Chicago Booth and Ohio State Athletics are unit-level and may not state university-wide policy.
- **Absence ≠ policy:** "—" means the pages read were silent, not that no rule exists.
- **Dates:** the Harvard Gift Policy Guide (May 2020), NPT due-diligence PDF (2019) and IRS Notice (2017) are before 2021. They are flagged and used only where still the live posted version or the governing authority.
- **Not legal or tax advice.** Recipients' readings of the Code differ, and this note does not resolve them.

## 6. Source register

| ID | Source | Date | Accessed | robots | Label |
|---|---|---|---|---|---|
| G1 | [IRS Notice 2017-73](https://www.irs.gov/pub/irs-drop/n-17-73.pdf) | 2017-12 | 2026-11-15 | allowed | F |
| G2 | [Caltech Gift Policies](https://giving.caltech.edu/documents/6199/Caltech_Gift_Policies_2024-10-01.pdf) | 2024-10-01 | 2026-11-15 | allowed | F |
| G3 | [Stanford Live DAF/PF guidelines](https://res.cloudinary.com/dopulypdj/image/upload/v1711662327/Guidelines_for_Gifts_from_Donor_Advised_Funds_and_Private_Foundations_FINAL.pdf) | 2024-03 (upload) | 2026-11-15 | allowed | F |
| G4 | [Stanford Day of Giving FAQ](https://dayofgiving.stanford.edu/pages/faq-2307); [Stanford Athletics giving](https://gostanford.com/giving); [Stanford Admin Guide, gifts](https://adminguide.stanford.edu/chapters/giving-stanford/gifts-university/gifts-university) (updated 2025-02-18) | current | 2026-11-15 | 404 no rules / allowed / allowed | F |
| G5 | [Harvard Gift Policy Guide Overview](https://alumni.harvard.edu/sites/default/files/page/files/Gift_Policy_Guide_Overview.pdf) | 2020-05 | 2026-11-15 | allowed | F |
| G6 | [Cornell DAF form](https://giving.cornell.edu/how-to-give/daf/); [Cornell Giving Day](https://givingday.cornell.edu/info/about) | current | 2026-11-15 | allowed | F |
| G7 | [Yale DAF](https://forhumanity.yale.edu/planning-your-gift/donor-advised-funds); [Yale gift policies](https://forhumanity.yale.edu/gift-policies) (redirect to giving.yale.edu) | current | 2026-11-15 | 404 no rules | F |
| G8 | [Duke Gift Planning DAF](https://giving.duke.edu/gift-planning/gift-plans-in-detail/donor-advised-funds/); [Duke blueprint](https://giving.duke.edu/blueprints/4-common-questions-about-donor-advised-funds/); [Duke Finance](https://finance.duke.edu/adrecords/donor-advised-funds/) | 2021+ | 2026-11-15 | allowed | F |
| G9 | [Columbia Gift Planning DAF](https://giftplanning.columbia.edu/what-you-can-give/donor-advised-fund); [CUIMC DAF](https://www.giving.cuimc.columbia.edu/ways-give/planned-giving/donor-advised-funds) | current | 2026-11-15 | allowed | F |
| G10 | [Princeton how to give](https://alumni.princeton.edu/give/how-make-gift); [TAGD FAQ](https://tagd.princeton.edu/TagdCampaign/Faqs) | current | 2026-11-15 | allowed / 404 | F |
| G11 | [Dartmouth Gift Acceptance Policy](https://policies.dartmouth.edu/policy/gift-acceptance-policy); [Dartmouth how to give](https://alumni.dartmouth.edu/how-give) | rev. 2026-10-17 | 2026-11-15 | allowed | F |
| G12 | [Notre Dame DAFpay post](https://giving.nd.edu/giving-to-notre-dame-via-donor-advised-funds-just-got-easier/) | 2025-11-19 | 2026-11-15 | allowed | F |
| G13 | [Chicago Booth how to give](https://www.chicagobooth.edu/alumni/giving/how-to-give) | current | 2026-11-15 | allowed | F |
| G14 | [UW DAF](https://www.washington.edu/giving/donor-advised-funds/) | current | 2026-11-15 | allowed | F |
| G15 | [Ohio State Priority Points](https://ohiostatebuckeyes.com/sports/2026/4/27/priority) | 2026-04-27 | 2026-11-15 | allowed | F |
| G16 | [WashU DAF](https://giving.washu.edu/how-to-give/donor-advised-funds/) | current | 2026-11-15 | allowed | F |
| G17 | [Georgetown gift instructions](https://giving.georgetown.edu/how-to-give/gift-instructions/) | current | 2026-11-15 | allowed | F |
| G18 | Fidelity Charitable: [Program Guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf), [pledge FAQ](https://www.fidelitycharitable.org/faqs/all/grant-pledge.html), [incidental FAQ](https://www.fidelitycharitable.org/faqs/all/more-than-incidental-benefit.html), [gala FAQ](https://www.fidelitycharitable.org/faqs/all/grant-gala-event.html) | ©2026 | 2026-11-15 | allowed | F |
| G19 | [Vanguard Charitable P&G Jan 2026](https://www.vanguardcharitable.org/sites/default/files/2026-01/policies_and_guidelines_january_2026_011326_final_0.pdf) | 2026-01 | 2026-11-15 | allowed | F |
| G20 | [Daffy Member Agreement](https://www.daffy.org/legal/agreement) (repo snapshot) | 2026-11-14 | 2026-11-14 | repo | F |
| G21 | **Search text only.**<br>- **Recipients:** JHU [FAQ](https://giving.jhu.edu/faqs) and [2026 DAF PDF](https://giving.jhu.edu/wp-content/uploads/2026/07/gp-daf-policies-guidelines-2026.pdf); [MIT](https://giving.mit.edu/donor-advised-funds); [Penn policy 2217](https://www.finance.upenn.edu/?p=1101); [Michigan](https://giving.umich.edu/um/donor-advised-fund); [Mayo](https://plannedgiving.mayoclinic.org/donor-advised-funds); [St Jude](https://www.stjude.org/give/planned-giving/impact-major-gift/donor-advised-funds.html); [Northwestern intention form](https://kellogg.northwestern.edu/-/media/files/multiyear-intention-form.ashx?la=en); [UW A&S FAQ](https://artsci.washington.edu/giving/faq); [USC Victory Points](https://usctrojans.com/sports/2025/3/19/usc-trojans-athletics-victory-points-trojan-athletic-fund); [BU](https://www.bu.edu/alumni/giving/ways-to-give/); [Cleveland Clinic](https://my.clevelandclinic.org/giving/ways-to-give/gift-planning).<br>- **Sponsors:** [NPT rules](https://www.nptrust.org/what-is-a-donor-advised-fund/grantmaking-rules/); [DAFgiving360 policies](https://www.dafgiving360.org/resource/dafgiving360-program-policies).<br>- **Market:** [Chronicle/CASE](https://www.philanthropy.com/news/heartening-rebound-lifts-college-and-university-gifts-to-61-5-billion/); [AAMC 2024](https://www.aamc.org/media/85521/download). | various | 2026-11-15 | **Unreadable or 403:** JHU, MIT, DAFgiving360.<br>**Repo-unreadable:** Penn, Mayo.<br>**Terms ban scripts:** NPT.<br>**Bot challenge:** AAMC.<br>**Not fetched:** the rest. | S |

## 7. Data dictionary: `gift-office-daf-policies-2026.csv`

| Column | Meaning |
|---|---|
| row_id | `GO-NN` recipient, `GO-S#` sponsor, `GO-R#` regulator, `GO-M#` market source |
| side | recipient / sponsor / regulator / market |
| entity, ein | Name; EIN (recipients from the donate scan; sponsors from repo source registers) |
| daf_rank_2023_24, daf_grant_usd_m_fy2023_24 | Rank and $m from `nonprofit-donate-page-daf-scan-2026.csv` (FY2023–24 top-50-sponsor itemised Schedule I) |
| entity_type | university, AMC, foundation, sponsor, etc. |
| pledge_rule | `allowed_if_no_reference`, `not_allowed`, `non_binding_intention_only`, `not_stated`, `not_read`, or a short phrase |
| pledge_evidence | Verbatim quote ≤40 words; [S] marks search text |
| events_benefits_rule, events_benefits_evidence | Events, tickets and bifurcation rule; quote ≤40 words |
| membership_priority_naming | Membership, athletics priority points and naming treatment |
| daf_form_or_portal | DAFpay, DAF Direct, notice form, or none |
| recognition_and_campaign_credit | How DAF grants count for recognition, giving days or campaigns |
| inhouse_daf_program | Whether the recipient runs its own DAF, and its minimum |
| published_daf_share | Any published DAF share of gifts |
| donate_scan_any_daf_option | `either_any_daf_option` from the donate-page scan (blank = not scanned) |
| source_urls, page_date, accessed, robots_status | Provenance |
| evidence_label | F / S / U / R as defined above |
| notes | Caveats and inferences |

**Reproduction:** robots-first fetch (user-agent `*`; 404 means no rules; anything else means not fetched). PDFs were converted with `pdftotext -layout`; HTML went through BeautifulSoup text. Two sponsor sources were read with WebFetch after a manual robots.txt check. Every value was entered by hand from the cited text.
