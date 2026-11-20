# Validation wave 50A: DAF litigation and sponsors' state charity registration

**Validator:** validator wave 50A · **Date:** 2026-11-20 · **Register:** [`data/mission-2026-11-14/validation-register-wave50a.csv`](../../data/mission-2026-11-14/validation-register-wave50a.csv) (38 rows, V50A-01 to V50A-38)

**Studies validated**
- b50-01, DAF litigation: [`b50-01-daf-litigation.md`](b50-01-daf-litigation.md) and `data/mission-2026-11-14/daf-litigation-2026-11-20.csv`.
- b50-02, state registration: [`b50-02-state-registration.md`](b50-02-state-registration.md), `data/mission-2026-11-14/state-registration-2026-11-20.csv` and `scripts/mission_state_registration.py`.

Wave 50B (b50-03, b50-04, §11.76) was not touched.

## 1. Method

- **Opinions.** Six primary documents were downloaded again with the generic user agent `research-script/1.0` and converted with `pdftotext -layout`. Quotes were matched page by page, with whitespace normalised.
  - *Pinkert*, 9th Cir. slip opinion, from cdn.ca9.uscourts.gov. The govinfo copy and its MODS record (dateIssued 2022-09-14) were also fetched.
  - *Pinkert*, N.D. Cal. ECF 74 (govinfo).
  - *Fairbairn*, ECF 257 (govinfo).
  - *Keefer*, N.D. Tex. Doc. 79 and Doc. 86 (govinfo).
  - The Georgia AG release of 2026-09-25 (law.georgia.gov).
- **Registries.** Colorado (data.colorado.gov `37wu-kn3g`) and Connecticut (data.ct.gov `ngch-56tr`) were pulled fresh through the Socrata `/resource/` endpoints into a validator cache.
  - The pull used the study's own pure functions, loaded from the script file. Output went to scratch, so the repo CSV was not overwritten.
  - All 200 CO and CT rows were compared with the repo CSV on 8 key fields.
  - A separate pass read the raw CO filings of the 14 NOTICE 1 sponsors, including FY2024 renewal payment and approval dates.
  - Colorado's notice schedule was re-read on coloradosos.gov.
- **Access claims.** Robots.txt was checked for each host before any other fetch from it. No CAPTCHA was triggered, no API behind a CAPTCHA was called, and nothing on www.charities.pa.gov beyond robots.txt was fetched.
  - NY: the page and its JS bundle were read.
  - WA: the data.wa.gov view metadata and the Socrata catalog were read, plus the CCFS home page HTML.
  - CA: one GET of the legacy Search.aspx.
- **Constraints.** No sec.gov, crt.sh, certspotter, CourtListener, FindLaw, Justia, PACER or off-limits hosts. No logins, forms or outreach. Scripts were run with `python3 -B`, and their output went to scratch.

### robots.txt log (2026-11-20)

| Host | robots.txt | Fetched |
|---|---|---|
| www.govinfo.gov | 200; `*` group, disallows `/search/`, `/core/` etc.; no Claude group | `/content/pkg/` PDFs, `/metadata/pkg/` MODS |
| cdn.ca9.uscourts.gov | 200; `Allow: /`, disallows newsletters only | 21-16299 slip opinion |
| law.georgia.gov | 200; standard Drupal disallows | Press release |
| data.colorado.gov, data.ct.gov | 200; disallow browse, `/api/odata/`, collocate; no Claude group; robotparser allows `/resource/` for `*`, ClaudeBot, anthropic-ai, Claude-User, Claude-Web, Claude-SearchBot | SODA `/resource/` only |
| www.coloradosos.gov | 200; disallows `/ccsa/pages/search/` and others; no Claude group | `/pubs/charities/FAQ/notices.html` |
| charities-search.ag.ny.gov | 200; `User-agent: *` / `Disallow:` (empty) | `/RegistrySearch` page and `/assets/index-C5m9GbLo.js` |
| www.charities.pa.gov | 200; `User-agent: *` / `Disallow: /` | robots.txt only |
| data.wa.gov | 200; Socrata template | `/api/views/f9jk-mm39.json` |
| api.us.socrata.com | (as in study) | Catalog query, data.wa.gov `q=charities` |
| ccfs.sos.wa.gov | 404 (no rules) | Home page HTML only |
| rct.doj.ca.gov | 404 (no rules) | One GET of `Search.aspx?facility=Y` |
| charitiesnys.com | 500 (treated as disallowed) | Nothing |

## 2. Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| b50-01 DAF litigation | 22 | 17 | 4 | 1 | 0 |
| b50-02 State registration | 16 | 14 | 2 | 0 | 0 |
| **Total** | **38** | **31** | **6** | **1** | **0** |

The final section has 15 Find/Replace items in three files:
- 8 in b50-01;
- 6 in b50-02;
- 1 in the industry report (§11.75).

The CSV corrections (repo rows LIT-02 and LIT-04, and three b50-01 CSV cells) are notes in §5. They are not applied to any CSV.

## 3. Findings

### 3.1 b50-01, DAF litigation: accept the record, modify the reading

**Confirmed against the opinions**
- **Ninth Circuit.** *Pinkert* (No. 21-16299) was argued 2022-04-11 and filed **2022-09-14**. govinfo MODS gives the same date.
- **Slip-opinion quotes.** All checked quotes are verbatim:
  - slip op. 12: the property-rights holding;
  - slip op. 6: "not legally obligated to comply with the donor's advice";
  - slip op. 11: "refused to listen to his advice" and "final authority … for any other reason".
- **California standing on appeal.** The panel did not reach it (slip op. 13).
- **Bress concurrence.**
  - The concurrence is headed "concurring in part and concurring in the judgment" and begins at slip op. 13.
  - The expressive/reputational rule is at 15. The common-law AG-enforcement rule is at 16.
  - The citation *Herbst v. Univ. of Colo. Found.*, **513 P.3d 388**, 393 (Colo. Ct. App. 2022) is exact. *Herbst* concerns a university foundation, not a DAF.
- **N.D. Cal. ECF 74.**
  - "The fund controls the donation, not the plaintiff" (at 6).
  - The statutory-standing sentence (at 8) and Cal. Corp. Code §5142(a) (at 9).
  - "might be different if the fund broke specific promises" (at 7).
- ***Fairbairn*, ECF 257.**
  - "may have had some duty … given their ongoing advisory rights" (at 18).
  - "need not finally resolve" a duty of care (at 13).
  - Judgment for Fidelity Charitable on the promise claims (at 11) and on negligence (at 22).
- ***Keefer*.**
  - The acknowledgment letter "contains nothing to prove 'exclusive legal control'" (Doc. 79 at 23–24).
  - "strict (not substantial) compliance" (Doc. 86 at 7).
  - $507,964.80 (Claim 1) and alternatives of **at least** $327,520 and $136,875 (Doc. 79 at 34).
- **Georgia.** The suit is in **Fulton County Superior Court**. The AG seeks restitution, **$5,000.00 per FBPA violation** and a **receiver**. The defendants include the successor entity, an executive director and a former board member.
- **CSV.** It has 9 rows, 23 columns and 7 matters; 6 rows are graded P and 3 S. It names no individual. The only surname hit is the AG's name in the release URL slug.

**Contradicted (V50A-13).**
- The md (§3.7) says the pre-gift DAF packet "did state exclusive control" and could not be read with the letter (Doc. 86 at 7). The opinion does not support this.
  - Doc. 79 at 23: the court "does not consider whether the DAF Packet establishes that Pi had 'exclusive legal control'".
  - Doc. 86 at 6–7 concerns reading the DAF Packet with the 2015-06-18 **Assignment of Interest**, not with the letter.
- The same error appears in the notes of CSV row B50-L03 b.

**Holdings overstated (partially confirmed)**
- **Pinkert scope (V50A-06).**
  - §0 item 2 states a general rule: no Article III standing to challenge fees or menus.
  - The majority ruled on the pleaded facts. Pinkert did not allege that he had not agreed to the fees, that they were undisclosed, or that they exceeded what he agreed to (slip op. 7). The court "need not decide" the other theories (slip op. 9).
- **California route (V50A-08).** §0 item 3 presents the California statutory-standing bar without saying it is a district-court holding only.
- **"Forecloses" (V50A-19).**
  - §4.2 says the record "forecloses the ERISA-style excessive-fee class action". It makes such a suit hard to bring in the Ninth Circuit over disclosed, agreed fees.
  - It does not foreclose one generally. The broader rule is the concurrence's.
- **Control paradox (V50A-20).**
  - *Keefer* is a substantiation holding: the written acknowledgment must show exclusive legal control. It does not rule on how much control the sponsor exercised, and it did not reach program agreements.
  - §0 also omits *Keefer*'s independent assignment-of-income ground (V50A-15).

**Unchanged.** The rest of the synthesis is tagged [I] and stays within the record:
- zero donor wins;
- the *Peterson* gap;
- AGs, not donors, as enforcers.

**Repo rows.**
- **LIT-02:** the decision date should be 2022-09-14, and the N.D. Cal. order date (2021-06-17) should be added.
- **LIT-04:** the court should be the Superior Court of Fulton County. Further changes:
  - add the successor entity;
  - the individual is the "executive director", not "CEO";
  - the AG release is now a primary source.

The notes are in §5.

### 3.2 b50-02, state registration: accept the data, modify the framing

**Reproduces exactly.**
- The fresh pull returned 710 CO rows and 29,220 CT rows, with 0 differences across 200 rows × 8 fields.
- **Colorado:**
  - top-50: 17 current (34%; 17/35 = 49% of those found), 14 with notices, 4 withdrawn, 15 not found;
  - small-50: 4 current (8%; 4/9).
- **Connecticut:**
  - top-50: 28 of 50 (26 without low-confidence matches);
  - small-50: 6 of 50 (5 without);
  - no LAPSED, SUSPENDED or DENIED credential in the sample.
- **Secondary counts:** all reproduce (47 sponsors in either registry, 18 current in both, FY mix 18/2/1, 4 withdrawals, 4 CT exempt-from-financial).

**Key sponsors**
- **GOOD in CO:**
  - Fidelity (status date 2026-11-10);
  - NPT (2026-11-09);
  - Schwab Charitable, filed as Donor Advised Charitable Giving Inc. (2026-11-12);
  - Vanguard (2026-07-01).
- **NYCT:** NOTICE 3 (2024-11-16), expired 2024-11-15, latest FY2022. In CT it is ACTIVE IN RENEWAL.
- **UCLA Foundation:**
  - NOTICE 3 dated 2012-11-29, expired **2003-11-15**;
  - its only CO filing is an initial registration with estimates, approved 2002-07-19.

**NOTICE 1 (V50A-25, V50A-26).**
- **The facts are right.** 14 sponsors are at NOTICE 1, all dated 2026-11-16 with a 2026-11-15 due date, and 2026-11-15 was a Sunday.
- **The explanation is weak.**
  - Colorado sends "Expiration notice 1: One day after the SOS due date", so a Monday notice is simply the published schedule.
  - All 14 have FY2024 renewals on file. For 13 of them, the FY2024 payment was processed 2 to 94 days after 2025-11-15, the same extended due date a year earlier; approvals came 2 to 122 days late.
  - The pattern is recurring late filing by these sponsors within the extension cycle, not SOS processing lag.
  - Under CO rules the registration is valid only until the report due date. "Not lapse" is therefore too strong: the registrations are technically expired until the report is filed, though most should clear within weeks.

**Should NOTICE 1 be called delinquent?**
- No. The SOS's own term for charities is *expiration notice*; it uses *delinquent notice* only for campaign reports.
- Recommendation: report the 14 as *recent expiration notice (≤30 days)* and keep *lapsed/delinquent* for the 5 NOTICE 3 records over 30 days old.

**Not found.**
- The study handles this correctly almost everywhere: the framing paragraph, §3.3 "Meaning", §4, and all 118 not-found CSV notes.
- Two places read as compliance verdicts:
  - the headline row "Who is delinquent?";
  - the headline "34% / 8% current" shares, which put not-found sponsors in the denominator without saying so in that row.
- No sentence calls a not-found sponsor non-compliant.

**Low-confidence matches.**
- There are 4 (Morgan Stanley GIFT, Ayco, Signatry, St Luke's), as stated.
- St Luke's (MN) matched a CT-based organization, and the study itself calls it probably a different entity. Yet it is counted in the headline 6 of 50. The defensible small-sample CT figure is 5 of 50.
- Morgan Stanley (CT address IN) and Signatry (KS) are plausibly the same entities. This was not verified.

**Access claims, all confirmed**
- **NY:** the bundle sends `X-Recaptcha-Token` with registry API calls.
- **PA:** robots.txt is `Disallow: /`.
- **WA:**
  - data.wa.gov f9jk-mm39 (created 2015-11-30) says "The Corporations Data Extract feature is no longer available";
  - the catalog search finds no registry dataset;
  - the CCFS page loads Cloudflare Turnstile.
- **CA:** the legacy `Search.aspx` returns 404.

## 4. Accept / modify / reject

| Study | Item | Decision | Reason |
|---|---|---|---|
| b50-01 | Case facts, dates, quotes, pin cites (Pinkert, Fairbairn, Keefer, Georgia) | Accept | All re-matched in the opinions or release |
| b50-01 | Keefer DAF packet "did state exclusive control" (md §3.7, CSV L03 b) | Modify | Court expressly did not decide (Doc. 79 at 23); Doc. 86 at 7 is about the Assignment of Interest |
| b50-01 | §0 item 2, Pinkert standing as a general rule | Modify | Holding limited to disclosed, agreed fees on the pleaded facts |
| b50-01 | §0 item 3, California route | Modify | District court only; not reached on appeal |
| b50-01 | §0 Keefer "because" | Modify | Two independent grounds |
| b50-01 | §4.2 "forecloses" class actions | Modify | Narrow to "hard to bring in the Ninth Circuit" |
| b50-01 | §4.4 control paradox | Modify | Substantiation holding; agreements not addressed |
| b50-01 | Zero donor wins; AGs as enforcers; Peterson gap | Accept | Consistent with the record; tagged [I] where inferential |
| b50-01 | CSV (privacy, counts) | Accept, with three cell notes | Role-only; counts reproduce |
| repo | LIT-02, LIT-04 | Modify (note) | Exact date; Fulton County Superior Court; roles |
| b50-02 | CO/CT shares, lists and secondary counts | Accept | Reproduced exactly from a fresh pull |
| b50-02 | NOTICE 1 classed as delinquent; "filing lag, not lapse" | Modify | Report as recent expiration notice; cause is recurring sponsor late filing |
| b50-02 | Headline shares including not-found | Modify | Add denominator caveat |
| b50-02 | CT small-50 6/50 | Modify | 5/50 without the probable St Luke's false match |
| b50-02 | Access claims (NY, PA, WA, CA) | Accept | All confirmed without bypass |
| b50-02 | Script | Accept | Pure functions reproduce the CSV |

## 5. CSV correction notes (not applied to any CSV)

`data/mission-2026-11-14/daf-litigation-2021plus.csv`
- **LIT-02.**
  - `decision_date`: change `2022-09` to `2022-09-14` (9th Cir. slip op. cover; govinfo MODS dateIssued).
  - `outcome`: add "N.D. Cal. order granting motions to dismiss 2021-06-17 (ECF 74)".
  - Add `https://cdn.ca9.uscourts.gov/datastore/opinions/2022/09/14/21-16299.pdf` and the ECF 74 govinfo PDF as primary sources.
- **LIT-04.**
  - `court`: change "Fulton County, Georgia (court level not stated in source)" to "Superior Court of Fulton County, Georgia".
  - Caption and defendant: by role, "SDG Impact Fund Inc.; SDG Global Impact Fund Inc. (successor entity); executive director; former board member". The release calls the individual "executive director", not CEO.
  - `evidence`: primary (AG release, `https://law.georgia.gov/press-releases/2026-09-25/carr-files-suit-against-sdg-impact-fund`). Relief sought: restitution, $5,000.00 per FBPA violation, receiver.

`data/mission-2026-11-14/daf-litigation-2026-11-20.csv`
- **B50-L03 b, `notes`:** replace with "Court refused to read the June 8, 2015 DAF Packet together with the June 18, 2015 Assignment of Interest (Doc. 86 at 6–7). Doc. 79 at 23 expressly did not decide whether the DAF Packet established exclusive legal control."
- **B50-L03 a, `notes`:** "alternatives $327520.00 and $136875.00" becomes "alternatives of at least $327,520 and at least $136,875".
- **B50-L06, `filed_date`:** "2026-09-25 (AG release date; filing date per release)" becomes "on or before 2026-09-25 (release date; the release gives no filing date)".

`data/mission-2026-11-14/state-registration-2026-11-20.csv`
- No cell is wrong.
- Recommended for the next run: add a CO class `expiration_notice_recent` for NOTICE 1 or 2 with `days_past_due` ≤ 30, and keep `delinquent` for older notices.

## 6. Limits

- **Reporter citations.** 48 F.4th 1051 and 2018 WL 6199684 were not checked; FindLaw and Justia are blocked.
- **Not re-verified.** The *Peterson*, Alaska and T.C. Memo. 2023-34 rows were not re-verified, as the study says.
- ***Keefer* appeal status** was not checked.
- **CO payment dates.** The `paymentprocesseddate` field is used as a proxy for when the sponsor filed. It is not a submission timestamp.
- **Low-confidence CT matches.** Whether Morgan Stanley GIFT and Signatry are the CT-registered entities was not verified by EIN; CT publishes no EIN.
- **MA.** The MA access claim (mass.gov 403, AGO hosts unreachable) was not in the checklist and was not re-tested.

## Exact corrections

### `research/mission-2026-11-14/b50-01-daf-litigation.md`

**Find:** "A donor has no Article III standing to challenge fees, share classes or investment menus, because those are paid from assets the donor gave away (9th Cir. slip op. 12; N.D. Cal. ECF 74 at 6)."
**Replace with:** "A donor who agreed to disclosed fees and a pre-selected investment menu has no Article III standing to challenge them, because they are paid from assets the donor gave away (9th Cir. slip op. 7, 12; N.D. Cal. ECF 74 at 6). The Ninth Circuit ruled on the pleaded facts and left the other injury theories undecided (slip op. 9). [V wave 50A]"

**Find:** "that role belongs to the Attorney General (ECF 74 at 8–9, citing Cal. Corp. Code §5142(a)). [F]"
**Replace with:** "that role belongs to the Attorney General (ECF 74 at 8–9, citing Cal. Corp. Code §5142(a)). This is the district court’s holding only; the Ninth Circuit did not reach it (slip op. 13). [F] [V wave 50A]"

**Find:** "donors lost a DAF deduction because the sponsor's acknowledgment letter did not state exclusive legal control."
**Replace with:** "donors lost a DAF deduction on two independent grounds: the gift was an anticipatory assignment of income (Doc. 79 at 21), and the sponsor’s acknowledgment letter did not state exclusive legal control (Doc. 79 at 23–24). [V wave 50A]"

**Find:** "The pre-gift DAF packet, which did state exclusive control, could not be read together with the letter (Doc. 86 at 7). The claims denied were $507,964.80, with alternatives of $327,520.00 and $136,875.00 (Doc. 79 at 34)."
**Replace with:** "The pre-gift DAF packet could not supplement the acknowledgment letter, and the court expressly did not decide whether the packet established exclusive legal control (Doc. 79 at 23). On reconsideration it also refused to read the packet together with the 2015-06-18 assignment of interest, because the CWA requirement “requires strict (not substantial) compliance” (Doc. 86 at 7). The claims denied were $507,964.80 (Claim 1), with alternative claims for at least $327,520 and at least $136,875 (Doc. 79 at 34). [V wave 50A]"

**Find:** "This forecloses the ERISA-style excessive-fee class action against fee-charging sponsors."
**Replace with:** "In the Ninth Circuit this makes an ERISA-style excessive-fee class action hard to bring over fees that were disclosed and agreed. It does not foreclose one generally: the majority ruled on the pleaded facts (slip op. 7, 9), the broader rule is the Bress concurrence, and California statutory standing was not reached on appeal (slip op. 13). [V wave 50A]"

**Find:** "The statutory control that defeats donor suits is also what the IRS and courts demand, strictly, before allowing the deduction (*Keefer*). [F]"
**Replace with:** "The statutory control that defeats donor suits must also be documented, strictly, before the deduction is allowed: *Keefer* requires the sponsor’s written acknowledgment itself to show exclusive legal control (Doc. 79 at 23–24; Doc. 86 at 7). It is a substantiation holding, not a ruling on how much control the sponsor exercised. [F] [V wave 50A]"

**Find:** "language in their agreements and receipts to reassure donors without putting the deduction at risk."
**Replace with:** "language in their acknowledgments (receipts) without putting the deduction at risk; *Keefer* did not address program agreements (Doc. 79 at 23). [V wave 50A]"

**Find:** "He also restates the common-law rule leaving charitable-trust enforcement to state AGs (slip op. 15–16)."
**Replace with:** "He also restates the common-law rule leaving charitable-trust enforcement to state AGs (slip op. 15–16; the concurrence begins at 13). *Herbst* (at 393) concerns a university foundation, not a DAF sponsor. [V wave 50A]"

### `research/mission-2026-11-14/b50-02-state-registration.md`

**Find:** "15 top-50 and 41 small-sample sponsors have no CO record [C]."
**Replace with:** "15 top-50 and 41 small-sample sponsors have no CO record [C]. The of-sample shares count those sponsors as not current; no record is not evidence of non-compliance (§3.3). [V wave 50A]"

**Find:** "| **Who is delinquent?** | **CT: none** in either frame."
**Replace with:** "| **Which sponsors show an expiration notice?** | **CT: none** in either frame (no LAPSED credential). [V wave 50A]"

**Find:** "That is almost certainly filing lag, not lapse [I]."
**Replace with:** "Colorado sends notice 1 one day after the due date, so a Monday notice after a Sunday due date is the published schedule. The pattern recurs: for 13 of the 14, the FY2024 renewal payment was processed 2 to 94 days after 2025-11-15, the same extended due date a year earlier. The likely cause is late filing by the sponsors within the extension cycle, not SOS processing. The registrations are technically expired until the report is filed, but most should clear within weeks [I]. [V wave 50A]"

**Find:** "  - NOTICE 1, 2 or 3 (and their ESTIMATE variants) → *delinquent*;"
**Replace with:** "  - NOTICE 1, 2 or 3 (and their ESTIMATE variants) → *delinquent*. The CO SOS calls these expiration notices; validation recommends reporting notices up to 30 days old as *expiration notice (recent)* and reserving *lapsed* for older ones; [V wave 50A]"

**Find:** "- **This is a timing artefact of a snapshot five days after a mass due date [I].**"
**Replace with:** "- **This is a timing artefact of a snapshot five days after a mass due date [I].** On this reading the lapsed count to report is 5 (NOTICE 3, more than 30 days), with the 14 recent expiration notices shown separately. [V wave 50A]"

**Find:** "Servant Foundation, Signatry, UCLA Foundation and St Luke's Foundation [F]."
**Replace with:** "Servant Foundation, Signatry, UCLA Foundation and St Luke’s Foundation [F]. St Luke’s (MN) probably matched a different, CT-based organization (§6), so the defensible small-sample CT figure is 5 of 50. [V wave 50A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.75 DAF litigation and sponsors’ state charity registration (validated, wave 50A)\n\n**DAF litigation and sponsors’ state charity registration** (validated, wave 50A). The opinions confirm the 2021+ litigation record. In *Pinkert v. Schwab Charitable Fund* (9th Cir. No. 21-16299, filed 2022-09-14), a donor who had agreed to disclosed fees and a pre-selected investment menu had no Article III standing. The court ruled on the pleaded facts and did not reach California standing. *Fairbairn* (ECF 257, 2021-02-26) ended in judgment for Fidelity Charitable, leaving open only “some duty” tied to advisory rights. *Keefer* (N.D. Tex. 2022) denied a $507,964.80 refund on two independent grounds, one being an acknowledgment that did not show exclusive legal control; the court required “strict (not substantial)” compliance and did not decide whether the DAF packet showed control. The Georgia AG sued SDG Impact Fund in Fulton County Superior Court. A fresh pull of the Colorado and Connecticut registries reproduces the shares exactly (17 of 50 top-50 sponsors current in CO, 28 of 50 in CT). Fourteen of the 19 CO notices are five-day-old NOTICE 1 records that recur with late annual filing, so only 5 registrations count as lapsed. Not found is not non-compliance (repo [`validation-wave50a-report.md`](mission-2026-11-14/validation-wave50a-report.md)). [V wave 50A]\n\n---\n\n## Source register"
