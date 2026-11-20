# US court litigation involving DAFs, 2021 onward (b50-01)

**Date:** 2026-11-20 · **Task ID:** b50-01 · **Status:** desk research from public court opinions and public web pages. No outreach, no logins, no PACER, no CourtListener. This is research, not legal advice.

**Builds on:** [`queue-batch29-regulation-litigation-crypto.md`](queue-batch29-regulation-litigation-crypto.md) §2 and [`data/mission-2026-11-14/daf-litigation-2021plus.csv`](../../data/mission-2026-11-14/daf-litigation-2021plus.csv) (rows LIT-01 to LIT-08); the wave-4 correction W4-16 to [`daf-user-complaints-deep-research.md`](daf-user-complaints-deep-research.md); policy work in [`direction-policy-lobbying-obbba.md`](direction-policy-lobbying-obbba.md) and [`regulation-market-structure-portability.md`](regulation-market-structure-portability.md).

**Outputs**
- Data: [`data/mission-2026-11-14/daf-litigation-2026-11-20.csv`](../../data/mission-2026-11-14/daf-litigation-2026-11-20.csv). It has 9 decision-level rows for 7 matters (§7 has the data dictionary).
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b50-01.csv`](../../data/mission-2026-11-14/queue-proposals-b50-01.csv), 6 rows.

**Tags:** **[F]** read in a primary source (court opinion or AG release) · **[S]** secondary or carried from the repo · **[I]** inference.

**Privacy convention:** the CSV names individuals only by role. Case captions appear below only as legal citations.

---

## 0. Answer in brief

- **Private donor suits against sponsors still have a record of zero wins in 2021+.** Two matters were decided:
  - *Pinkert v. Schwab Charitable Fund* was dismissed for lack of standing (N.D. Cal. 2021-06-17) and affirmed by the Ninth Circuit on 2022-09-14 (No. 21-16299).
  - *Fairbairn v. Fidelity Investments Charitable Gift Fund* ended in judgment for the sponsor after a bench trial on 2021-02-26.

  One matter is pending: *Peterson v. Christian Community Foundation (WaterStone)*, D. Colo., filed 2026-01-15. [F/S]
- **What the courts have established:**
  1. Advisory privileges are non-binding. The sponsor "is not legally obligated to comply with the donor's advice" (9th Cir. slip op. 6).
  2. A donor has no Article III standing to challenge fees, share classes or investment menus, because those are paid from assets the donor gave away (9th Cir. slip op. 12; N.D. Cal. ECF 74 at 6).
  3. Under California law, a donor is not among the persons allowed to sue a charitable corporation for mismanagement; that role belongs to the Attorney General (ECF 74 at 8–9, citing Cal. Corp. Code §5142(a)). [F]
- **Two questions remain open:**
  - **Specific promises made to induce a gift.** *Fairbairn* reached trial on this theory but lost on proof (ECF 257 at 11).
  - **Interference with the advisory right itself.** The Ninth Circuit stressed that the donor did not allege the sponsor "refused to listen to his advice" (slip op. 11). *Peterson* is the first 2021+ case to plead that injury. No court has ruled on it. [F/I]
- **The sponsor's "exclusive legal control" also decides tax cases.**
  - In *Keefer v. United States* (N.D. Tex. 2022), donors lost a DAF deduction because the sponsor's acknowledgment letter did not state exclusive legal control. Compliance must be "strict (not substantial)" (Doc. 86 at 7). [F]
  - In T.C. Memo. 2023-34, a pre-sale stock gift to Fidelity Charitable was taxed to the donors as an assignment of income (law-firm alert). [S]
  - **[I] The control that wins the donor a deduction is the same control that defeats the donor's suit.**
- **Enforcement runs through state AGs.** In 2026 the Georgia AG sued a self-described DAF sponsor (SDG Impact Fund) in Fulton County Superior Court, seeking restitution and a receiver. Alaska sued six giving platforms, including PayPal Giving Fund. [F/S]
- **Nothing was verified for three categories:** grants to disputed recipients, estate disputes and divorce disputes. Leads are in §3.4, §3.6 and the queue.

## 1. Method

1. **Repo first.** We grepped `research/` and `data/` for Fairbairn and Pinkert (7 research docs and 14 data files hit) and for 4966 and policy-lobbying. Repo rows LIT-01 to LIT-08 are the baseline.
2. **Robots.** We read robots.txt on every host before fetching from it, with the generic user agent `research-script/1.0`. The full log is in §6.
   - **govinfo.gov** disallows `/app/search/*` and `/search/`. The public search was therefore not used.
   - Package metadata (`/metadata/pkg/<id>/mods.xml`), details pages (`/app/details/<id>`) and PDFs (`/content/pkg/...`) are allowed and were used.
   - api.govinfo.gov (key required) was not used.
3. **Finding cases without govinfo search.**
   - **Known dockets:** we built USCOURTS package IDs (`USCOURTS-<court>-<office>_<yy>-cv-<nnnnn>`) and checked each ID's MODS record for caption, dates and the list of PDFs.
   - **New cases:** we found them with general web search, including `site:govinfo.gov USCOURTS "donor advised fund"`, which surfaced the N.D. Tex. packages. Every hit was then confirmed on govinfo or on an allowed court or AG host.
4. **Reading.** We downloaded opinion PDFs from govinfo (and the Ninth Circuit's own CDN), converted them with `pdftotext -layout`, and read them. Pin cites use the court's page numbers: ECF page for N.D. Cal., Doc. page for N.D. Tex., slip-opinion page for the Ninth Circuit.
5. **Scope.** We included decisions dated 2021-01-01 or later, plus pending 2021+ filings. Pre-2021 decisions appear only as context and are not counted.

## 2. Results

| ID | Matter (citation) | Category | Court · docket | Key dates | Outcome | Grade |
|---|---|---|---|---|---|---|
| B50-L01 a | *Pinkert v. Schwab Charitable Fund* | Fees and investment options | N.D. Cal. 3:20-cv-07657-LB | Order 2021-06-17 | Dismissed: no Article III or Cal. statutory standing | F |
| B50-L01 b | same | same | 9th Cir. No. 21-16299 | Argued 2022-04-11; filed 2022-09-14 | Affirmed on Article III; state standing not reached | F |
| B50-L02 | *Fairbairn v. Fidelity Inv. Charitable Gift Fund* | Sponsor discretion and promises | N.D. Cal. 3:18-cv-04881-JSC | Trial Oct 2020; opinion 2021-02-26 | Judgment for sponsor on all claims | F |
| B50-L03 a/b | *Keefer v. United States* | Tax: DAF acknowledgment | N.D. Tex. 3:20-cv-00836-B | 2022-07-06; reconsideration denied 2022-08-10 | Refund denied | F |
| B50-L04 | T.C. Memo. 2023-34 | Tax: pre-sale gift to DAF | U.S. Tax Court | 2023-03-15 | Gain taxed to donors; deduction lost | S |
| B50-L05 | *Peterson v. Christian Community Found.* | Successor advisor | D. Colo. 1:26-cv-00179 | Filed 2026-01-15 | Pending; MTD briefed | S (repo) |
| B50-L06 | Georgia AG v. SDG Impact Fund | State AG | Fulton Cty. Super. Ct. | Release 2026-09-25 | Pending | F (release) |
| B50-L07 | Alaska AG v. six platforms incl. PayPal Giving Fund | State AG | Alaska state court | 2026-03-10 | Pending | S (repo) |

**Counts [C, from the CSV]:**
- **7 matters in 9 rows.**
- **Evidence grades:** 6 rows rest on primary sources read in this pass; 3 rest on secondary sources or are carried from the repo.
- **Kind of matter:** 3 private suits against a sponsor (2 closed for the sponsor, 1 pending); 2 tax cases; 2 AG actions.

**Screened out** (read, but not DAF donor–sponsor litigation):
- **[F] *Al-Tamimi v. Adelson*, D.D.C. 1:16-cv-00445.** The 2023 and 2024 opinions on govinfo contain no "donor" or "charit" hits. The remaining charity defendants are "friends of" organisations, not DAF sponsors.
- **[F] *The Charitable DAF Fund LP v. Highland Capital Management LP*, N.D. Tex. 3:21-cv-03129.** This is a bankruptcy appeal. "DAF" is part of the entity's name; the case is not a §4966 donor dispute.
- **[F] A Wisconsin Court of Appeals divorce opinion** (No. 2022AP2151, 2024-05-31) has no DAF or charity content.
- **[S] NCF Charitable Trust v. Florida.** This is a state tax dispute. A press search summary says the suit was dropped. It was not verified and is not a donor dispute.

## 3. Findings by category

### 3.1 Sponsor fees and investment options: *Pinkert*

- **The claim.** A donor-advisor sued Schwab Charitable, its board and investment committee, and Charles Schwab & Co. He alleged excessive affiliate custody and brokerage fees and retail share classes chosen where cheaper institutional classes were available (ECF 74 at 1–4). [F]
- **District court (2021-06-17).**
  - "The fund controls the donation, not the plaintiff" (ECF 74 at 6).
  - No case supports treating "the right to designate investments (in pre-selected funds) and donations" as a property interest that confers standing (at 7).
  - Under California law, only the AG, the corporation, its members, its directors or officers, or a person with a "reversionary, contractual, or property interest" may sue for breach of a charitable trust (at 8–9, Cal. Corp. Code §5142(a)). [F]
- **Ninth Circuit (2022-09-14).** The court rejected four injury theories:
  - property right in advising;
  - reputation;
  - expression;
  - the need to contribute more.

  The reputation, expression and contribution theories failed because none was alleged as actual or imminent (slip op. 9–10). The property theory failed because the Program Policies give the sponsor "final authority … for any other reason" (slip op. 11). Fees and the investment menu were disclosed and agreed at the time of the gift (slip op. 12). [F]
- **Concurrence (Judge Bress).** He would hold outright that expressive or reputational injuries tied to DAF spending never confer standing. He also restates the common-law rule leaving charitable-trust enforcement to state AGs (slip op. 15–16). He cites *Herbst v. Univ. of Colo. Found.*, 513 P.3d 388 (Colo. Ct. App. 2022): donor status alone is "insufficient to give him standing." That is Colorado authority, the same state as *Peterson*. [F]
- **Repo correction.** Repo row LIT-02 dates the appeal decision "2022-09". The slip opinion is dated **2022-09-14**. The 48 F.4th 1051 cite was not re-verified. [F]

### 3.2 Sponsor discretion and donor promises: *Fairbairn* and successors

- **The dispute.** The donors alleged that the sponsor made promises to induce a gift of about 1.93 million shares of Energous stock in late 2017, then broke them in liquidating the shares (ECF 257 at 1, 4). [F]
- **Holding (2021-02-26).**
  - The alleged promises were not proven, except a 10%-of-volume promise, which was kept (at 11).
  - Reliance was not reasonable (at 11).
  - The court did not decide whether a duty of care exists (at 13). Assuming one exists, it was not breached (at 22).
  - "Fidelity Charitable's written policies gave it room to make judgments as to how and when to sell" (at 16–17).
  - "While it still may have had some duty to [the donors] given their ongoing advisory rights, that duty is not the same as the duty an advisor owes a client" (at 18). [F]
- **[I] Two openings for donors.** The court found that two special-relationship factors favoured the donors (at 13) and allowed for "some duty" arising from advisory rights (at 18). These are the main judicial openings for donors in the 2021+ record. Neither became a holding.
- **Successors.** *Pinkert* is the only 2021+ decision to apply *Fairbairn*, and it distinguished it: the result "might be different if the fund broke specific promises" (ECF 74 at 7, 10). No other 2021+ decided case on sponsor discretion was found.

### 3.3 Successor-advisor disputes: *Peterson* (pending)

- **[S, carried from repo LIT-01]** The plaintiff is the successor advisor of a family DAF with a reported balance of $21,071,102 at 2023-12-31. The claims are contract, implied covenant, negligent misrepresentation, the Colorado CPA, accounting, a declaration on the legal status of advisory privileges, and transfer of the fund. The motion to dismiss was fully briefed by 2026-05-26.
- **What this pass checked.** We checked govinfo: there is no USCOURTS package for 1:26-cv-00179 (the metadata request redirected), which means no published opinion yet. RECAP, the repo's earlier source, is now treated as off-limits, so the docket status was **not re-verified**.
- **[I] Why it matters.** *Peterson* pleads the injury the Ninth Circuit said was missing in *Pinkert*: a refusal to act on advice. *Herbst*, Colorado appellate authority cited in the *Pinkert* concurrence, cuts against donor standing.
- **Unverified lead (not in the CSV).** A search summary described *Formanek v. Howard* (Tenn. Ct. App.): the advisor was removed after the donor's death, and the trial court held the fund agreement was a completed gift, not a contract. No allowed source confirmed it (§6). See queue P-B5001-02.

### 3.4 Grants to disputed recipients

**No 2021+ litigation was found.**
- The 2026 SPLC grant holds at the three largest sponsors drew multistate AG letters. The repo records these as complaints and discretion items, not lawsuits (see [`gap19-complaints-with-denominators.md`](gap19-complaints-with-denominators.md)).
- *Al-Tamimi* (D.D.C.) involved charities funding contested causes, but no DAF sponsor (§2).
- **[I]** *Pinkert*'s reading of "final authority … for any other reason" (slip op. 11) suggests that a donor suit over a hold would face the same standing barrier. A recipient charity's standing has not been tested. See queue P-B5001-06.

### 3.5 State AG actions

- **Georgia (F).** The AG filed in Fulton County Superior Court against SDG Impact Fund Inc., its successor SDG Global Impact Fund Inc., its executive director and a former board member.
  - **Allegations:** illegal distribution of charitable assets and misleading donors. The release says SDGIF "purports to operate as a 501(c)(3) sponsoring organization for donor-advised funds."
  - **Relief sought:** restitution, a $5,000 civil penalty per Fair Business Practices Act violation, and a receiver.
  - **Repo correction:** this corrects the court field of LIT-04, which said "court level not stated."
- **Alaska (S, carried).** The suits filed 2026-03-10 against six platforms include PayPal Giving Fund. law.alaska.gov now returns 403 for robots.txt, so it was not re-fetched. The defendant list stays open under P-G1913-05.
- **Pre-2021 context only:** the NY AG's 2020 PayPal Charitable Giving Fund settlement (repo R23).

### 3.6 Estate and divorce disputes involving DAF assets

**No 2021+ decision was verified.**
- The Wisconsin divorce opinion we could read had no DAF content.
- Iowa (No. 23-1522) and New Jersey (A-1568-22) appellate opinions surfaced in search, but both hosts are off-limits (§6).
- Practitioner articles say, without citing cases, that a DAF funded before a divorce is generally outside the marital estate and that the real dispute is over who serves as advisor. That is commentary, not a holding. See queue P-B5001-05.
- T.C. Memo. 2023-34 is captioned "Estate of …" only because the taxpayer died. It is a tax case, not an estate dispute.

### 3.7 Tax cases where the sponsor's control decided the outcome (added category)

- **Keefer (F).** The donors gave a 4% hotel LP interest to a DAF at The Pi Fund in 2015. The refund suit failed on two independent grounds:
  - the gift was an anticipatory assignment of income (Doc. 79 at 21);
  - the acknowledgment letter "contains nothing to prove 'exclusive legal control'", so §170(f)(18) was not satisfied (at 23–24).

  The pre-gift DAF packet, which did state exclusive control, could not be read together with the letter (Doc. 86 at 7). The claims denied were $507,964.80, with alternatives of $327,520.00 and $136,875.00 (Doc. 79 at 34). Whether there was an appeal was not verified (P-B5001-03).
- **T.C. Memo. 2023-34 (S).** The deduction for stock gifted to Fidelity Charitable before a sale was lost (about $3.3m per the alert), and the gain was taxed to the donors (P-B5001-04).

## 4. Synthesis: donor rights against sponsors, and the link to policy

1. **Advisory-only status is law, not just a contract term.**
   - Both *Pinkert* courts anchor the donor's position in the statute: the DAF definition (§4966(d)(2)(A)(iii), "advisory privileges") and the deduction condition (§170(f)(18)(B), "exclusive legal control").
   - The Ninth Circuit reads them together: the donor "can advise …, but the sponsoring organization is not legally obligated to comply" (slip op. 6). [F]
   - Sponsor program policies repeat this, and courts take the policies into account: *Pinkert* incorporated them by reference, and the Ninth Circuit supplemented the record with them (ECF 74 at 3 n.7; slip op. 11 n.2). [F]
2. **Standing is the gate, and it is closed for general mismanagement claims.**
   - Fee, share-class, investment-menu and prudence claims fail because the donor no longer has an interest in the money (Article III), and because California routes charitable-trust enforcement to the AG (§5142(a)). [F]
   - **[I]** This forecloses the ERISA-style excessive-fee class action against fee-charging sponsors. That is the litigation risk the repo's fee and affiliate analyses would otherwise have to price.
3. **Open lanes are narrow and fact-specific.** Courts have left room for:
   - (a) specific pre-gift promises (*Fairbairn*: allowed in 2018, lost at trial in 2021);
   - (b) refusal to consider advice, the *Pinkert* gap, now tested by *Peterson*;
   - (c) a possible but undecided duty of care in handling a donor's gift (*Fairbairn* at 13, 18). [F/I]
4. **The control paradox.**
   - The statutory control that defeats donor suits is also what the IRS and courts demand, strictly, before allowing the deduction (*Keefer*). [F]
   - **[I]** Sponsors cannot soften "exclusive legal control" language in their agreements and receipts to reassure donors without putting the deduction at risk. Donor protections therefore have to come from transparency, portability and AG oversight, not from enforceable donor rights.
5. **Who actually polices sponsors: AGs, not donors.**
   - The Bress concurrence restates the common-law rule (slip op. 16), and the 2021+ enforcement record matches it: Georgia (receiver, restitution), Alaska (consent to use charity names), and earlier the NY AG's PPGF settlement. [F/S]
   - **[I]** Commercially, enforcement risk for sponsors is regulatory and reputational, concentrated at small or novel sponsors (SDG) and platform-type sponsors (PPGF). The large national sponsors show none in the 2021+ record.
6. **Link to the repo's policy work** ([`direction-policy-lobbying-obbba.md`](direction-policy-lobbying-obbba.md); [`regulation-market-structure-portability.md`](regulation-market-structure-portability.md)):
   - **The 2023 rule proposal and the courts use the same term differently.** The proposed §4966 regulations (REG-142338-07, docket IRS-2023-0053) are still proposed. The 2023 NPRM's broad definition treats "advisory privileges" as arising from a donor-advisor relationship, using them as the trigger for tax status. The courts treat the same privileges as legally non-binding. **[I]** A final rule would define who holds advisory privileges for tax purposes. It would not, by itself, make them enforceable against sponsors. Still, a regulatory definition of the privilege and of who the "donor-advisor" is (for example, successors) could be cited by plaintiffs like *Peterson* as evidence of "reasonable expectations" under an implied-covenant theory.
   - **The 2026–27 Priority Guidance Plan item** ("§§4966 and 6033 regarding certain donor advised fund arrangements") is the live regulatory vehicle. A §6033 reporting element would add transparency, which is the remedy the courts leave to regulators.
   - **Lobbying.** Sponsors' LDA activity on the §4966 proposal (Fidelity, SIFMA and others; repo LDA dataset) is aimed at the regulatory channel. That is consistent with litigation posing little threat to them. [I]
   - **Portability.** No court has ordered a fund moved to another sponsor. *Peterson* requests it. **[I]** Until a court does, portability rests on sponsor policy alone (see [`regulation-market-structure-portability.md`](regulation-market-structure-portability.md)).

## 5. Limits

- **Discovery coverage is incomplete.** govinfo search is disallowed by robots, so federal cases were found by web search and known dockets. govinfo USCOURTS also holds only opinions courts choose to publish there: unpublished orders, dockets and complaints are missing.
- **State courts are under-covered.** Several state court hosts are off-limits: Tennessee (JS challenge), Iowa (disallows ClaudeBot) and New Jersey (403). No state-court DAF decision was read.
- ***Peterson* and Alaska were not re-verified.** Both rows carry repo data originally built from sources this pass treats as off-limits or did not refetch.
- **The Tax Court opinion was not read.** B50-L04 rests on a law-firm alert.
- **Filing dates.** For older federal cases, filing dates are year-only, taken from docket numbers. govinfo MODS records hold no filing date.
- **Reporter citations not re-verified:** 48 F.4th 1051 and 2018 WL 6199684.
- **Search summaries named cases we could not confirm.** Those cases (*Formanek*; the NCF trust tax suit) are reported only as leads.

## 6. Robots and access log (2026-11-20, UA `research-script/1.0`)

| Host | robots.txt | Decision |
|---|---|---|
| www.govinfo.gov | 200; `*` group; disallows `/app/search/*`, `/search/`; no Claude-specific group | Used `/metadata/pkg/`, `/app/details/`, `/content/pkg/` only |
| api.govinfo.gov | 500 | Not used (also needs key) |
| cdn.ca9.uscourts.gov / www.ca9.uscourts.gov | 200; `Allow: /` (cdn disallows only newsletters) | Used for 21-16299 slip opinion |
| www.cand.uscourts.gov | 301 | Not used (not needed) |
| www.courtlistener.com | 403 | Disallowed per brief; RECAP not used |
| caselaw.findlaw.com | 403 | Disallowed; not used |
| law.justia.com | 403 | Disallowed; not used |
| www.njcourts.gov | 200 (`*` allows); opinion PDF returned 403 | Blocked; not retried |
| www.wicourts.gov | 404 (no robots file) | One opinion read; no DAF content |
| www.iowacourts.gov | 200; disallows ClaudeBot, anthropic-ai, Claude-Web | Blocked; not fetched |
| www.tncourts.gov / tncourts.gov | JS challenge page, not robots | Treated as disallowed |
| www.ustaxcourt.gov | 200; disallows /admin/ only | Not needed |
| dawson.ustaxcourt.gov | App shell HTML, not robots | Not used |
| law.georgia.gov | 200; standard Drupal disallows | Used press-release pages |
| law.alaska.gov | 403 | Treated as disallowed; not fetched |
| www.ag.state.mn.us | 200; disallows press-release paths | Not fetched |
| oag.ca.gov | 200 | Not needed this pass |
| www.naepc.org | 200; `*` no disallows | Read (WebFetch) |
| www.saxwa.com | 200; disallows /wp/wp-admin/ | Read (WebFetch) |
| www.mcguirewoods.com | 200; no Claude group | Read (WebFetch) |
| www.philanthropyroundtable.org | 200; WebFetch returned 403 | Not read |
| www.financial-planning.com | Disallows ClaudeBot, anthropic-ai, Claude-Web | Not fetched |
| www.currentfederaltaxdevelopments.com | Disallows ClaudeBot, anthropic-ai | Not fetched |
| sec.gov, crt.sh, certspotter, off-limits list | n/a | Not used |

## 7. Data dictionary: `daf-litigation-2026-11-20.csv`

| Column | Meaning |
|---|---|
| case_id | `B50-Lnn`, one per matter |
| decision_seq | a, b, … for successive decisions in the same matter |
| case_label_entity_level | Entity-level label. Individuals appear by role only |
| category | One of the brief's categories, plus "tax" where the sponsor's control decided a tax case |
| court, court_level | Court name and tier |
| docket_number | Docket or citation as printed by the court or govinfo |
| filed_date | Filing date. "Year from docket number" when the exact date is not verified |
| decision_date | Date of the decision in this row (ISO). "none" for pending matters |
| decision_type | Kind of ruling and ECF/Doc number |
| plaintiff_role | Role of the plaintiff (e.g. donor-advisor, successor advisor, state AG) |
| defendant_entities_and_roles | Defendants at entity level; individuals by role |
| claims | Causes of action |
| outcome | Disposition |
| key_holding_quote | Short verbatim quote from the opinion (or a secondary quote, flagged) |
| pin_cite | Page cite using the court's pagination (ECF/Doc/slip op.) |
| status_as_of_2026-11-20 | Closed, pending, or appeal status unknown |
| daf_sponsor_involved | Sponsor party or non-party sponsor whose role mattered |
| evidence_grade | P = primary read this pass; S = secondary or carried from repo |
| primary_url | Primary source URL (govinfo PDF, court CDN, AG release), or a statement that none was reachable |
| secondary_urls | Supporting URLs, separated by " ; " |
| repo_crossref | Related repo rows or docs |
| notes | Corrections, caveats and figures quoted from the opinion |

## 8. Source register

| ID | Source | Date | URL |
|---|---|---|---|
| G1 | *Pinkert*, N.D. Cal. order (ECF 74) | 2021-06-17 | https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_20-cv-07657/pdf/USCOURTS-cand-3_20-cv-07657-0.pdf |
| G2 | govinfo package, *Pinkert* N.D. Cal. | 2021-06-18 ingest | https://www.govinfo.gov/app/details/USCOURTS-cand-3_20-cv-07657 |
| G3 | *Pinkert*, 9th Cir. slip opinion No. 21-16299 | 2022-09-14 | https://cdn.ca9.uscourts.gov/datastore/opinions/2022/09/14/21-16299.pdf |
| G4 | govinfo package, 9th Cir. 21-16299 | 2022-09-14 | https://www.govinfo.gov/app/details/USCOURTS-ca9-21-16299 |
| G5 | *Fairbairn*, opinion following bench trial (ECF 257) | 2021-02-26 | https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_18-cv-04881/pdf/USCOURTS-cand-3_18-cv-04881-7.pdf |
| G6 | govinfo package, *Fairbairn* (8 opinions 2018–2021) | 2021-03-01 ingest | https://www.govinfo.gov/app/details/USCOURTS-cand-3_18-cv-04881 |
| G7 | *Keefer*, memorandum opinion (Doc. 79) | 2022-07-06 | https://www.govinfo.gov/content/pkg/USCOURTS-txnd-3_20-cv-00836/pdf/USCOURTS-txnd-3_20-cv-00836-0.pdf |
| G8 | *Keefer*, reconsideration denied (Doc. 86) | 2022-08-10 | https://www.govinfo.gov/content/pkg/USCOURTS-txnd-3_20-cv-00836/pdf/USCOURTS-txnd-3_20-cv-00836-1.pdf |
| G9 | *Al-Tamimi* opinions (screened out) | 2023-02-09; 2024-02-23 | https://www.govinfo.gov/app/details/USCOURTS-dcd-1_16-cv-00445 |
| G10 | *Charitable DAF Fund LP v. Highland* (screened out) | 2022-09-02 | https://www.govinfo.gov/app/details/USCOURTS-txnd-3_21-cv-03129 |
| A1 | Georgia AG, "Carr Files Suit Against SDG Impact Fund" | 2026-09-25 | https://law.georgia.gov/press-releases/2026-09-25/carr-files-suit-against-sdg-impact-fund |
| C1 | Wisconsin Ct. App. No. 2022AP2151 (screened out) | 2024-05-31 | https://www.wicourts.gov/ca/opinion/DisplayDocument.pdf?content=pdf&seqNo=808056 |
| S1 | McGuireWoods alert on T.C. Memo. 2023-34 | 2023-03-20 | https://www.mcguirewoods.com/client-resources/Alerts/2023/3/timing-is-critical-for-gift-of-appreciated-stock-to-avoid-capital-gain-from-sale-of-company |
| S2 | Sax LLP on *Peterson* | 2026-03-16 | https://www.saxwa.com/news/who-really-controls-your-daf/ |
| S3 | NAEPC newsletter on *Peterson*, *Styles*, *Fairbairn*, *Pinkert* | 2026 (issue 2) | https://www.naepc.org/events/newsletter/2/2026 |
| R1 | Repo litigation baseline (LIT-01 to LIT-08) | 2026-11-15 | data/mission-2026-11-14/daf-litigation-2021plus.csv |
| R2 | Repo policy work (§4966 NPRM status, PGP, LDA) | 2026-11-15 | research/mission-2026-11-14/direction-policy-lobbying-obbba.md |
