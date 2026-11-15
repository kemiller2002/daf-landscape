# Direction P-NEW-NPC-01: what nonprofits experience when they receive DAF grants, 2021–2026

**Date:** 2026-11-15 · **Queue item:** P-NEW-NPC-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/nonprofit-side-daf-issues-2021-2026.csv`](../../data/mission-2026-11-14/nonprofit-side-daf-issues-2021-2026.csv): 60 coded rows (NPS-001 to NPS-060).
  - 32 rows are fresh (read 2026-11-15).
  - 5 are sponsor or intermediary policy rows carried from repo notes.
  - 23 are the 2021+ nonprofit complaint and mixed records carried from the complaints corpus, each linked by `corpus_link`.
  - Data dictionary in §8.
- [`data/mission-2026-11-14/queue-proposals-batch44-n28.csv`](../../data/mission-2026-11-14/queue-proposals-batch44-n28.csv): P-B44N28-01 to P-B44N28-03.

**Read first and built on**, with their governing corrections:
- [daf-user-complaints-deep-research.md](daf-user-complaints-deep-research.md), with waves 4 and 14. Neither changes the nonprofit records.
- [queue-batch33-voids-exports-rails.md](queue-batch33-voids-exports-rails.md), with wave 18. The PPGF uncashed-check rule is a standing rule since at least 2022-03-15, not a 2025 change.
- [direction-nonprofit-donate-pages.md](direction-nonprofit-donate-pages.md), with waves 24B and 26. Any DAF option is 75/182 (41.2%) as a lower bound; DAFpay is 13.4–13.7%.
- [direction-gift-office-daf-handling.md](direction-gift-office-daf-handling.md), with wave 26. The Ohio State exclusion applies to DAFgiving360 only. Bifurcation is expressly barred by the three sponsors read first-hand (Fidelity, Vanguard, Daffy).
- Also used:
  - [queue-nonprofit-side-panel.md](queue-nonprofit-side-panel.md);
  - [queue-batch36-anonymity-feeds-fees.md](queue-batch36-anonymity-feeds-fees.md), with waves 21 and 22;
  - [direction-nonprofit-daf-benchmarks.md](direction-nonprofit-daf-benchmarks.md).

**Rules followed**
- **robots.txt:** read for every host before any fetch. A 200 response was parsed for `*` and `ClaudeBot`. A 404 meant no rules. Anything else (403, timeout, a bot challenge) meant the host was **not fetched**.
- **Hosts not fetched:**
  - philanthropy.com and insidephilanthropy.com: disallowed.
  - The ScholarWorks PDF path: disallowed.
  - councilofnonprofits.org: disallowed.
  - inequality.org and ips-dc.org: 403.
  - learninghub.feedingamerica.org and paypal-community.com: robots unreadable.
  - reddit.com (blocked in earlier waves). crt.sh was not used.
- **No contact or accounts:** no logins, forms, posts or outreach.
- **Personal data:** none collected. Forum posts are paraphrased, with no poster names or institutions. Quotes are taken only from organisations or published authors and are ≤40 words.
  - A script checked every CSV quote verbatim against the fetched page or PDF text (`quote_check` column; 0 mismatches).
- **Recency:** only evidence from 2021–2026. Pre-2021 items (the CEP 2020, Lilly 2020 and Chronicle 2018 surveys and articles, the 2017 PPGF lawsuit, a 2020 Community-Centric Fundraising essay) are excluded from the table and named only as context.

**Evidence labels**
- [F] first-party page or PDF read.
- [V] vendor statement about its own market (an interested party).
- [P] practitioner post on a public, view-only association forum (paraphrased).
- [S] secondary report of a primary source not read.
- [R] search-index text only.
- [U] nothing found.
- [I] inference.
- "[F, repo]" means carried from a repo note with its URL.

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **What do nonprofits complain about most?** | **Not knowing who gave, and money arriving late by check.**<br>Of 48 coded complaint, mixed and finding rows: identity and data 16 (anonymity/acknowledgement 7, missing donor data 5, crediting/reporting 4), delay and checks 16, restrictions and discretion 8, fees 4, service and verification 4.<br>Excluding the 14 Benevity Trustpilot rows (an intermediary, not a DAF sponsor), **identity and data leads at 15 of 34**, then restrictions and discretion 8 and delay and checks 7 [C]. | Medium. Venue-driven counts, not prevalence |
| **Published nonprofit-side surveys (2021–2026)** | There are four public sources, and none is a neutral nonprofit census:<br>- The DAF Research Collaborative's interviews with 46 fundraisers (2025, via [NonProfit Times](https://thenonprofittimes.com/?p=214617)).<br>- Its sponsor survey (n=128) and donor survey (n>2,100) (2025, [F]).<br>- FreeWill's 2025 and 2026 vendor surveys. FreeWill 2026: **72% say the biggest challenge is not knowing which donors have a DAF**; 20% name anonymous gifts; 33% flag DAF donors in their CRM ([FreeWill](https://www.nonprofits.freewill.com/resources/blog/donor-advised-fund-statistics)) [V].<br>- FreeWill 2025: 27% of fundraisers get "too many" anonymous DAF gifts ([Foundation Group](https://www.501c3.org/?p=28265)) [S].<br>We found no 2021–2026 AFP, Bloomerang, NonProfit PRO, Nonprofit Tech for Good, NAIS or CASE survey with a DAF pain-point item. | High that coverage is thin |
| **Is "anonymous" the real problem?** | **Mostly not chosen anonymity. Thin defaults are the problem.**<br>- Only **36% of sponsors default to full contact information**; **35% default to fund name only** and 1% to anonymous (DAFRC manager survey, n=128, 86% community foundations) [F].<br>- Donors: 72% never or almost never give fully anonymously, and 79% of partial-anonymity donors think the fund name identifies them [F].<br>- Fidelity reports 4% anonymous grants ([FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)) [F].<br>- Only **49% of donors say charities always thank them** [F]. | High on the survey figures; medium on the reading |
| **Checks, voids, lost checks** | **The worst nonprofit-side outcomes sit at the check layer, and the nonprofit cannot fix a check by itself.**<br>- **Chariot:** one nonprofit's 2,000+ gifts from 34 providers. Check-paying providers averaged **7–162 days**; ACH providers paid in 1–2 days ([Chariot](https://givechariot.com/resources/insights/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits)) [V].<br>- **Lost checks:** an AASP thread (2025) reports DAF and IRA checks repeatedly lost in the mail [P].<br>- **Fidelity** reissues only at the donor's request [F]. YourCause/Blackbaud may forfeit voided funds [F]. PPGF may reassign uncashed funds [F, repo]. | Medium-high |
| **Restrictions (benefits, pledges)** | **Real friction, and inconsistent on the nonprofit side.**<br>- Advancement offices describe sponsor letters that bar pledge payment, refused sponsorship splits, and a 2024 Schwab Charitable audit that clawed back a scholarship grant [P].<br>- One nonprofit's 2025 gala FAQ tells staff a sponsorship *may* be split between a DAF and personal funds ([Keshet FAQ](https://www.keshetonline.org/wp-content/uploads/2025/04/FAQ_-Using-Donor-Advised-Funds-DAFs-for-Keshets-Gala-Sponsorships.pdf)) [F]. The sponsors read first-hand bar that [I]. | Medium |
| **Fees** | **Sponsors charge nonprofits nothing. Fees come from intermediaries and connectors:** Benevity's $35-or-8% check fee and DAFpay's default 2.9% [F, repo].<br>The new evidence is practitioner worry that **DAFpay converts fee-free direct DAF grants into fee-bearing ones** (AASP threads 2025-10 and 2026-05) [P]. | Medium |
| **Sector associations** | **AFP's DAF education is funded by Fidelity Charitable** (a three-year Catalyst Fund investment from Jan 2024). AFP frames the issue as a fundraiser knowledge gap ([AFP RFP](https://afpglobal.org/sites/default/files/attachments/resource/DAF_Curriculum_Design_RFP_11_7_24.pdf)) [F].<br>CASE gives counting rules only ([VSE guidance 2026-07-29](https://www.case.org/system/files/media/inline/VSE%20Survey%20Guidance%20Document%20Updated%20July%2029%202026.pdf)) [F]. NAIS: no DAF guidance found [U].<br>**The richest first-hand nonprofit voice is AASP's public FundSvcs forum** (9 threads, §2). | High on what was found |

---

## 1. Method and access log

1. **Search.** Web searches covered the themes in the queue item: surveys; practitioner blogs; AFP, NAIS and CASE; anonymity; checks and voids; pledges and benefits; DAFpay and PPGF fees. Each candidate host's robots.txt was checked with a script before any fetch.
2. **Reading.**
   - Pages were read with a fetch tool. PDFs were downloaded once and converted to text (`pdftotext`): the DAFRC manager and donor surveys, CASE VSE, the AFP RFP and the Keshet FAQ.
   - Seven Chariot, FreeWill, Bloomerang, NPT, Foundation Group, Fidelity, DonorDock and Blackbaud pages were saved for the quote check.
3. **Coding.**
   - One row per dated source statement.
   - The `issue_category` taxonomy is nonprofit-specific (§8). Each category maps to an `issue_family` that lines up with the donor-corpus categories (§3).
   - Severity uses the corpus scale: low = inconvenience; medium = repeated friction or money at risk of delay; high = money withheld for weeks or more, lost or clawed back; critical = loss or diversion alleged. For policy rows, severity is the impact if the rule is triggered.
4. **Carried rows.** These are the complaints-corpus nonprofit records dated 2021+ (23). Their categories are re-mapped (e.g. `nonprofit_receipt_attribution` → `donor_data_gap`). Paraphrases and grades are unchanged, and the four Reddit rows keep "not re-verified".

| Host | robots.txt | Used |
|---|---|---|
| thenonprofittimes.com, givechariot.com, bloomerang.com, 501c3.org, nonprofits.freewill.com, dafresearchcollaborative.org, aasp.connectedcommunity.org, afpglobal.org, case.org, fidelitycharitable.org, donordock.com, keshetonline.org, charitycompliancesolutions.com | 200, allowed | Yes |
| static1.squarespace.com (DAFRC PDFs), webfiles-sc1.blackbaud.com | 404 (no rules) | Yes |
| scholarworks.indianapolis.iu.edu | 200; `/server/` PDF path disallowed; item page bot-challenged | Abstract not read; PDF not fetched (P-B44N28-02) |
| nonprofitpro.com | allowed, but the page returned 307 (Sucuri) to the fetch tool | Not read; [R] only |
| philanthropy.com, insidephilanthropy.com, councilofnonprofits.org | disallowed | Not fetched |
| inequality.org, ips-dc.org | 403 | Not fetched |
| learninghub.feedingamerica.org, paypal-community.com | unreadable | Not fetched |
| case.org session page | allowed; page 403 | Not read |
| community.blackbaud.com | allowed; body did not render | Not used |

## 2. What nonprofits report, by issue

### 2.1 Identity, acknowledgement and donor data (16 rows)

- **Fundraisers (DAFRC interviews, 2025).** They list six challenges: verifying the organisation, investigating DAF donations, entering grants, thanking the donor, understanding DAF rules, and getting gift information from donors.
  - NPT's summary: "This lack of transparency makes acknowledging the funder (as opposed to the DAF advisor) cumbersome." ([NPT](https://thenonprofittimes.com/?p=214617)) [S].
  - NPT headlines "79% of DAF gifts are partially anonymous". The DAFRC donor report uses 79% for a different measure: the share of occasional partial-anonymity donors who feel identifiable. **[I] Treat the 79% as unverified** (P-B44N28-02).
- **Sponsor defaults (DAFRC manager survey, 2025).** Defaults are full contact 36%, name only 24%, fund name only 35%, other 5% and anonymous 1%. The authors say the variety "has created considerable confusion among professional fundraisers" and call for an industry standard with full contact as the default ([PDF](https://www.dafresearchcollaborative.org/s/The-National-Survey-of-Donor-Advised-Fund-Managers.pdf)) [F].
- **Donors (DAFRC donor survey, 2025).**
  - 49% say they are always or almost always thanked; 8% never or almost never.
  - 72% of anonymous givers want to avoid public recognition and 71% want to avoid solicitation.
  - The authors suggest sponsors offer a "confidential" option instead of "anonymous" ([PDF](https://www.dafresearchcollaborative.org/s/The-National-Survey-of-Donor-Advised-Fund-Donors.pdf)) [F].
- **FreeWill 2026.** 72% of nonprofits say not knowing which donors have a DAF is their biggest challenge; 20% name anonymous gifts as a top challenge; 33% flag DAF donors in their CRM [V]. FreeWill 2025: 27% get "too many" anonymous DAF gifts [S].
- **Practitioners (AASP, 2022–2026)** [P]:
  - Fidelity will not tell a charity who sent an unidentified transfer. Donors later ask why they got no receipt.
  - Wires rarely identify the advising donor.
  - DAFpay gifts often arrive with little donor detail, and data from major sponsors is downloaded, de-duplicated and keyed by hand.
- **Advice columns and vendors.** These describe the same confusion over whether to thank the sponsor or the donor ([Bloomerang 2023](https://bloomerang.com/blog/ask-an-expert-how-to-enter-and-credit-donor-advised-fund-gifts-in-your-database); [Chariot](https://givechariot.com/resources/insights/stop-sending-thank-you-notes-to-fidelity)) [V].
- **CASE (2026).** Institutions must hard-credit DAF gifts to a DAF column and count top DAF donors by soft-credited account. Sector reporting therefore also depends on knowing the person [F].

### 2.2 Delay, check handling, lost and voided checks (16 rows)

- **Delay.** Chariot's single-nonprofit sample: check-paying providers averaged 7–162 days. "Even the largest national DAFs have struggled to get their ACH rates much higher than 50% of their payments." Delays of 60–90 days lead to void and reissue [V].
  - The post shows "Jan 20" with no year. Its CMS timestamps and 2025 data imply January 2026 [I]. This supersedes the corpus date "c.2024" for CMP-241 (§9).
- **Lost in the mail.** An AASP office reports DAF and IRA checks repeatedly lost in the mail, with donors re-requesting them [P].
- **Reissue is out of the nonprofit's hands:**
  - Fidelity: "Fidelity Charitable cannot reissue a grant check unless requested by the recommending donor." [F].
  - YourCause/Blackbaud: reissue is possible only for checks older than 45 days, is not guaranteed after 120 days, and can take up to 90 days; "Once a payment is Voided, the funds are at risk of being forfeited and checks cannot be reissued." ([Blackbaud](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-giving-check-reissues.html)) [F].
- **Intermediaries.** Benevity's 11 Trustpilot delay complaints (2025–26) remain the densest cluster (carried).
- **Batching.** A Chariot customer reports payouts at most twice a month, triggered by hand, which delays gift entry and thank-yous [P].

### 2.3 Sponsor restrictions and discretion (8 rows)

- **Pledges.** Many sponsor grant letters say funds cannot pay a pledge, so offices write pledges down by hand or treat them as non-binding (AASP 2024) [P]. This matches the recipient split in the gift-office note.
- **Benefits.**
  - Offices report pressure to let sponsors split DAF and personal payments, and an unexpected DAF sponsorship payment with logo recognition accepted (AASP 2024–25) [P].
  - One nonprofit's own staff FAQ allows the split: "Yes, as long as they personally pay for the part that covers goods and services." ([Keshet](https://www.keshetonline.org/wp-content/uploads/2025/04/FAQ_-Using-Donor-Advised-Funds-DAFs-for-Keshets-Gala-Sponsorships.pdf)) [F]. Fidelity, Vanguard and Daffy bar bifurcation (gift-office note, wave 26). **Nonprofit-side guidance therefore diverges from sponsor rules** [I].
- **Clawback.** A university received a Schwab Charitable audit notice over a scholarship grant paid on to a student and was asked to refund it (AASP 2024) [P].
- **Holds.** The SPLC holds of 2026 and the statements against them are carried from the corpus (CMP-205, 219, 220).

### 2.4 Fees (4 complaint rows; 3 policy rows)

- **Policy rows.** Sponsors charge nothing. Benevity charges the higher of $35 or 8% per check, capped at $125 [F, repo]. DAFpay's default is 2.9% [F, repo].
- **Practitioner worry, new here.** DAFpay could move donors who now grant directly at no cost onto a fee-bearing path; through GiveCampus, fees follow the platform schedule, which "could sting" on large grants (AASP 2025–26) [P, paraphrased].
- **PPGF via Meta (2023).** PPGF can decline to pass a gift on, and fees now come out of each gift ([DonorDock](https://www.donordock.com/articles/why-you-should-reconsider-using-meta-charitable-giving-tools-paypal-giving-fund)) [V].

### 2.5 Service, verification and knowledge (4 + 3 rows)

- **Verification.** New nonprofits are told to seek sponsor "pre-certification" (NPT) [S]. Benevity verification complaints are carried.
- **AFP.** AFP's curriculum premise: "Many professional fundraisers are unclear about how they work and how they could benefit their nonprofit organizations." [F]. The programme is Fidelity-funded, and no AFP material voicing nonprofit complaints about sponsors was found [U].

## 3. Comparison with the donor-side complaint corpus

Donor rows are the complaints-corpus records whose complainant is a donor (incl. employee donors), with valence complaint or mixed, dated 2021+ (n=85; 53 excluding the App Store). Nonprofit rows are this table's complaint, mixed and finding rows (n=48; 34 excluding Benevity).

| Issue family | Nonprofit (n=48) | Nonprofit excl. Benevity (n=34) | Donor 2021+ (n=85) | Donor excl. App Store (n=53) |
|---|---|---|---|---|
| Identity and data (anonymity, acknowledgement, donor data, crediting) | **16** | **15** | 5 | 4 |
| Delay and checks | **16** | 7 | 9 | 8 |
| Restrictions and discretion (pledge/benefit rules, holds) | 8 | 8 | 10 | 10 |
| Nonprofit-side or rail fees | 4 | 3 | 4 | 4 |
| Service and verification | 4 | 1 | 3 | 2 |
| Donor-only (app/login, donor fees, investments, liquidation, portability, succession) | — | — | **54** | 25 |

**Readings [C/I]:**
1. **The two stakeholders complain about different things.**
   - Donor complaints are dominated by app, login and fee issues that nonprofits never see.
   - Nonprofit complaints are dominated by identity and data issues, which donors almost never raise. **No donor record in the corpus mentions anonymity, acknowledgement or thanks**, yet the DAFRC donor survey shows only 49% are always thanked.
   - The acknowledgement gap is real on both sides. It is just invisible in donor complaint venues.
2. **Delay and checks is the shared ground.** Donors report voided checks and charities that never deposited (CMP-165, 191, 153). Nonprofits report lost checks, slow check-paying providers and forfeiture rules. Both sides lose. Only the donor can trigger a reissue at Fidelity.
3. **Restrictions look different from each side.**
   - Donors complain about declines and holds (SPLC, UNRWA, 990 non-filers).
   - Nonprofits complain about pledge and benefit rules and clawbacks, which donors raise rarely (CMP-170).
4. **Intermediaries skew the nonprofit side.** Removing Benevity halves the delay count. This confirms the corpus finding that the worst nonprofit delay sits with workplace and payment intermediaries, not national sponsors.

## 4. Comparison with the repo's void-window and anonymity findings

| Repo finding | Nonprofit-side evidence | Effect |
|---|---|---|
| Fidelity is the only national sponsor with a published void window (90 days); GiveClear also 90; PPGF reassigns funds; no escheat language anywhere (batch 33, wave 18) | Chariot: 60–90-day delays lead to void and reissue [V]. AASP: lost checks re-requested by donors [P]. YourCause: voided funds "at risk of being forfeited" [F] | **Adds one forfeiture rule (YourCause) to the repo's void table.** Confirms that the nonprofit cannot restart a voided grant itself at Fidelity, Ren or YourCause. No nonprofit source quotes a void window, which suggests nonprofits rarely know it [I] |
| Remittance is donor-controlled; Fidelity has 4% anonymous; the DAFpay export has no anonymity field (panel; batch 36, wave 22) | DAFRC: 35% of sponsors default to fund-name-only and 1% to anonymous. FreeWill: 20% of nonprofits name anonymity a top challenge, but 72% name "not knowing who has a DAF". AASP: DAFpay data still needs manual de-duplication | **Shifts the problem from "anonymity" to "default and partial data".** The repo's 4% figure is consistent; the nonprofit pain comes from the partial-information middle (fund name only, wires, connector exports) |
| DAFpay 2.9% default; stacked fees exceed card cost (batch 36, wave 21) | Practitioners fear cannibalising fee-free direct DAF grants [P] | Adds a demand-side objection the fee analysis did not capture |
| Pledge and benefit rules split across sponsors and recipients (gift-office note, wave 26) | AASP workarounds; one nonprofit FAQ permits a split that the sponsors bar | Confirms the split and shows that nonprofit guidance can be wrong in the permissive direction |

## 5. Implications [I]

- **Data, not money transfer.** For a nonprofit-facing product, the largest unmet need is identity and data: a confidential-not-anonymous default, a stable donor and fund identifier on every rail, and machine-readable remittance. Faster money matters most where checks remain.
- **Fees are an adoption risk for connectors.** The fee objection is specific: nonprofits resist paying for DAF gifts that already arrive free.
- **The nonprofit voice is under-sampled.** It sits in association forums and vendor surveys. Sector associations are either sponsor-funded (AFP) or silent (NAIS). Any claim about "what nonprofits want" should cite the AASP-type venue or commission a neutral survey.

## 6. Limitations

- **Small sample.** There are 32 fresh rows. Nine are AASP threads, which over-represent university and hospital advancement-services offices.
- **Vendor sources.** Vendor rows (Chariot, FreeWill, Bloomerang, DonorDock) come from interested parties. Three Chariot posts carry no year (NPS-026, NPS-027 are "year unknown").
- **Unread sources.** The DAFRC "Reinventing the Cycle" report, the FreeWill full reports, the Chariot/K2D reports and NonProfit PRO were not read (robots, forms or bot protection).
- **Reddit rows.** The four r/nonprofit rows are carried from earlier repo coding and not re-verified.
- **Counts.** Counts reflect venue accessibility, not prevalence.

## 7. Source register

| # | Source | Date | URL | Use |
|---|---|---|---|---|
| S01 | The NonProfit Times, "Guessing Game: 79% Of DAF Gifts Are Partially Anonymous" | 2025-05-15 | https://thenonprofittimes.com/?p=214617 | NPS-001–004 [S] |
| S02 | DAFRC, National Survey of DAF Managers | 2025 (PDF 2025-12-16) | https://www.dafresearchcollaborative.org/s/The-National-Survey-of-Donor-Advised-Fund-Managers.pdf | NPS-005 [F] |
| S03 | DAFRC, National Survey of DAF Donors | 2025 | https://www.dafresearchcollaborative.org/s/The-National-Survey-of-Donor-Advised-Fund-Donors.pdf | NPS-006–007 [F] |
| S04 | FreeWill, "Decoding DAFs for nonprofits" (2026 report summary) | 2026-08-21 | https://www.nonprofits.freewill.com/resources/blog/donor-advised-fund-statistics | NPS-008 [V] |
| S05 | Foundation Group (FreeWill guest post) | 2025-08-11 | https://www.501c3.org/?p=28265 | NPS-009 [S] |
| S06 | Bloomerang Ask an Expert, entering and crediting DAF gifts | 2023-06-30 | https://bloomerang.com/blog/ask-an-expert-how-to-enter-and-credit-donor-advised-fund-gifts-in-your-database | NPS-010 |
| S07 | Bloomerang Ask an Expert, recognising DAF gifts | 2021-05-22 | https://bloomerang.com/blog/ask-an-expert-how-should-donor-advised-fund-gifts-be-recognized | NPS-011 |
| S08–S17 | AASP FundSvcs threads (view-only) | 2022–2026 | https://aasp.connectedcommunity.org/discussion/ : need-to-reissue-dafira-checks; dafpay; dafpay-via-givecampus; daf-day-chariot; unidentified-electronic-transfer-from-fidelity-not-daf-is-there-any-way-to-identify-donor-or-confirm-it-was-anonymous; donor-advised-funds-and-pledges; donor-advised-funds-qcds-and-sponsorships; daf-refund; dafs-that-come-as-grants; donor-advised-fund-daf-gift-acknowledgements | NPS-012–021 [P] |
| S18 | Keshet, FAQ on DAFs for gala sponsorships | 2025-04 | https://www.keshetonline.org/wp-content/uploads/2025/04/FAQ_-Using-Donor-Advised-Funds-DAFs-for-Keshets-Gala-Sponsorships.pdf | NPS-022 [F] |
| S19 | Chariot, "All Checks, No Balance" | Jan 20 [2026, I] | https://givechariot.com/resources/insights/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits | NPS-023–024 [V] |
| S20 | Chariot, "The Grants That Go Nowhere Good" | Apr 1 [2026, I] | https://givechariot.com/resources/insights/the-grants-that-go-nowhere-good | NPS-025 [V] |
| S21 | Chariot, "Stop Sending Thank You Notes to Fidelity" | Apr 15, year unknown | https://givechariot.com/resources/insights/stop-sending-thank-you-notes-to-fidelity | NPS-026 [V] |
| S22 | Chariot, "DAF Gifts: Why Eventually Isn't Good Enough" | Apr 21, year unknown | https://www.givechariot.com/post/daf-gifts-why-eventually-isn-t-good-enough | NPS-027 [V] |
| S23 | Chariot, "Top 6 Takeaways from New DAF Research Collaborative Report" | Apr 10 [2025, I] | https://givechariot.com/resources/insights/top-6-takeaways-from-new-daf-research-collaborative-report | Cross-check for S02 |
| S24 | Blackbaud NPOconnect, Check Reissues | live 2026-11-15 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-giving-check-reissues.html | NPS-028 [F] |
| S25 | Fidelity Charitable nonprofit FAQ | live 2026-11-15 | https://www.fidelitycharitable.org/nonprofits/faqs.html | NPS-029 [F] |
| S26 | DonorDock, Meta tools and PayPal Giving Fund | 2023, updated 2026-07-07 | https://www.donordock.com/articles/why-you-should-reconsider-using-meta-charitable-giving-tools-paypal-giving-fund | NPS-030 [V] |
| S27 | AFP, DAF Curriculum Design RFP | 2024-11-07 | https://afpglobal.org/sites/default/files/attachments/resource/DAF_Curriculum_Design_RFP_11_7_24.pdf | NPS-031 [F] |
| S28 | CASE, VSE Survey Guidance | updated 2026-07-29 | https://www.case.org/system/files/media/inline/VSE%20Survey%20Guidance%20Document%20Updated%20July%2029%202026.pdf | NPS-032 [F] |
| S29 | Repo carried policy rows (Benevity fees, PPGF delivery, DAFpay 2.9%, Chariot anonymity field, Vanguard returns) | 2025–2026 | URLs in CSV | NPS-033–037 [F, repo] |
| S30 | Complaints corpus nonprofit records 2021+ | 2025–2026 | `daf-user-complaints-corpus.csv` | NPS-038–060 |
| X1 | Excluded: Charity Compliance Solutions on PPGF (recounts the 2017 suit) | undated | https://charitycompliancesolutions.com/paypal-giving-fund-misleads-donors-and-charities | Pre-2021 event |
| X2 | Excluded: FreeWill "Mystery Money" deck (2026-04-08) | 2026 | https://lp.freewill.com/hubfs/7139016/Donor%20Stewardship%20Summit%202026/FreeWill%20%7C%20Mystery%20Money.pdf | No DAF content |
| X3 | Excluded: CCF essay (2020), IU Lilly blog (2020), CEP/Lilly/Chronicle surveys (2018–2020) | pre-2021 | see corpus S23–S24 | Context only |
| X4 | Not read: IU ScholarWorks "Reinventing the Cycle"; NonProfit PRO "DAF Day 2025"; Chronicle 2025 DAF articles; Feeding America DAF guide; IPS/Inequality.org | — | robots or bot protection (§1) | [R] at most |

## 8. Data dictionary (`nonprofit-side-daf-issues-2021-2026.csv`)

| Field | Type | Values / meaning |
|---|---|---|
| issue_id | text | NPS-001…NPS-060 |
| date | text | Event or publication date; "inferred" or "year unknown" where the page lacks a year |
| date_precision | enum | day, month, year, inferred, year unknown, live |
| issue_category | enum | grant_delay_check_handling, lost_voided_checks, anonymity_acknowledgement, donor_data_gap, crediting_reporting, sponsor_restrictions, grant_holds_discretion, fees, verification_enrollment, customer_service, knowledge_gap |
| secondary_category | enum | Same list, or blank |
| issue_family | enum | delay_checks, identity_data, restrictions_discretion, fees, service_verification, knowledge (used in §3) |
| severity | enum | low, medium, high, critical (corpus scale; for policy rows, impact if triggered) |
| voice | text | Who speaks: e.g. nonprofit_practitioner_forum, nonprofit_review, sponsor_survey, donor_survey, nonprofit_aggregate_survey, vendor_analysis, sector_association, sponsor_policy, intermediary_policy, nonprofit_guidance, advocacy |
| source_type | enum | trade_press, research_report, vendor_content, sector_association_forum, sector_association_guidance, nonprofit_guidance, sponsor_policy, review_site, public_forum, advocacy |
| valence | enum | complaint, mixed, finding, guidance, policy (§3 counts complaint + mixed + finding) |
| sponsor_vendor_named | text | Sponsor, vendor or intermediary named by the source; "none"/"generic" where unnamed |
| org_type | text | research, vendor, practitioner, association, nonprofit, national_sponsor, intermediary, or the corpus org_type for carried rows |
| paraphrase | text | Summary; forum posts are paraphrased only, with no names |
| short_quote | text | Verbatim, ≤40 words, from an organisation or published source; blank for forum rows and carried rows |
| quote_check | text | "verbatim match in fetched text" or "no quote" |
| metric | text | Figures and sample sizes as published |
| evidence_label | text | [F], [V], [P], [S], [F, repo], or the corpus E-grade for carried rows |
| source_url | url | Primary URL |
| robots_status | text | robots.txt result for the host, or "carried; not re-fetched" |
| access_date | date | 2026-11-15 |
| origin | text | fresh 2026-11-15; repo: file §; carried from complaints corpus |
| corpus_link | text | Related complaints-corpus record_id |
| notes | text | Caveats, date inference, interested-party flags |

## 9. Proposed corrections to repo text (not governing until validated)

1. **`daf-user-complaints-corpus.csv` CMP-241.** Change date "c.2024" to "2026-01-20 [I] (post 'Jan 20'; analysis of 2025 DAFpay gifts; CMS timestamps 2026-01)". Add to the paraphrase: "18 check-paying providers averaged 7–162 days; ACH providers 1–2 days (one nonprofit, 2,000+ gifts, 34 providers)".
2. **`uncashed-grant-rules-2026.csv`.** Add a YourCause/Blackbaud NPOconnect row: reissue only for outstanding checks more than 45 days old; reissue not guaranteed after 120 days; up to 90 days to reissue; "Once a payment is Voided, the funds are at risk of being forfeited" (S24).
3. **NPT's "79% of DAF gifts are partially anonymous".** No other repo note cites it (grep, 2026-11-15). Any future citation should carry "[S]; possibly conflates the DAFRC donor-survey 79% (identifiable via fund name); unverified" until P-B44N28-02 is done.
