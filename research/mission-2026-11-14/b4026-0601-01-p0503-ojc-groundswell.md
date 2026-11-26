# OJC Fund Schedule I audit and Groundswell's Schedule D accounts (P-B4026-06-01-01, P-P0503-1915-02)

**Date:** 2026-11-20 · **Task ID:** b4026-0601-01-p0503 · **Status:** desk research from public filings and public web pages only; no outreach, no logins.

**Builds on:** [b4026-06-01-faith-sponsors-outside-top50.md](b4026-06-01-faith-sponsors-outside-top50.md) and its wave-42B corrections ([validation-wave42b-report.md](validation-wave42b-report.md)); [g1915b-04-line6-vs-schedule-d.md](g1915b-04-line6-vs-schedule-d.md), [prop-0503-1915-propagation.md](prop-0503-1915-propagation.md) and their corrections ([validation-wave39b-report.md](validation-wave39b-report.md), [validation-wave40a-report.md](validation-wave40a-report.md)).

**Outputs**
- Script: [`scripts/mission_ojc_groundswell.py`](../../scripts/mission_ojc_groundswell.py). New. It imports `mission_faith_sponsors_outside.py` and modifies nothing.
- Data: [`data/mission-2026-11-14/ojc-groundswell-audit-2026-11-20.csv`](../../data/mission-2026-11-14/ojc-groundswell-audit-2026-11-20.csv). 303 rows, long format (§7).
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b4026-0601-01-p0503.csv`](../../data/mission-2026-11-14/queue-proposals-b4026-0601-01-p0503.csv), 6 rows.

Tags: **[F]** read from a filing or the BMF · **[C]** computed by the script · **[P]** quoted primary web source · **[I]** inference.

## 0. Answer in brief

**(A) The OJC Fund (EIN 113618879)**

- **Its church-block recipients are all church-status organisations.** This holds by construction: every block recipient is BMF SUBSECTION 03 and FOUNDATION 10, with no e-filed 990. The audit also checks other BMF fields. 99.6% of OJC's block dollars go to EINs with filing-requirement code 06 (church, not required to file) and 99.8% to deductibility code 1. 95.7% go to New York EINs and 3.6% to New Jersey. 59.2% go to NTEE X30 (Judaism) and 25.9% to EINs with no NTEE code [F][C].
- **Its lines are not pass-throughs to other DAF sponsors or federations.** Of $720.5m of positive FY2023–24 Schedule I dollars on 6,419 lines:
  - 0.23% ($1.62m) goes to DAF sponsors that the frame already nets out: Friends of Mosdot Goor, The Donors' Fund, PEF Israel Endowment Funds and Fidelity Charitable.
  - 0.07% ($0.47m) goes to other DAFRC panel members. These are mainly operating charities that also host DAFs, such as Agudath Israel of America, Amudim and Yeshiva University.
  - 0.008% ($59k) goes to recipients with federation names.
  - None of these recipients is in the church block [C].
- **But "church-status" is not the same as "congregation".** An Orthodox-aware name rule types OJC's $545.3m of block dollars (DAF-weighted) as follows:
  - **38.9%** to congregations (1,110 recipients; 41.6% if recipients are typed by their BMF names, which is the basis the faith-share variants below use) [V wave 43B]
  - **25.9%** to yeshivas and schools (585);
  - **16.5%** to chesed or relief funds (217);
  - 1.5% to communal umbrella bodies (21);
  - 17.2% to names the rule cannot type (517).

  The base study's own rules (no Outreach override) give 44.7% congregation, 19.4% school and 32.2% unclassified [C][I].
- **OJC is itself partly downstream of other DAF sponsors.** Ten panel sponsors' Schedule I lines pay OJC $54.0m over FY2023–24. That is 7.4% of OJC's $734.5m of Schedule D DAF contributions. PayPal Charitable Giving Fund pays $44.4m and Fidelity Charitable $7.3m. The frame nets these lines out of the payers, so there is no double count. They do shift attribution [C].
- **Faith share with flagged lines excluded** [C]:

  | Block faith share | S2 (top 50 + all faith) | S3 (all panel + non-panel faith) | S3 nationals' share |
  |---|---|---|---|
  | Central (b4026-06-01) | 33.7% | **30.2%** | 58.8% |
  | OJC inflow share reattributed to non-faith | 33.1% | 29.7% | — |
  | Drop OJC lines to yeshiva/school names | 32.4% | 29.0% | 59.8% |
  | Drop OJC lines to yeshiva/school and chesed-fund names | 31.6% | **28.2%** | 60.5% |
  | Keep only OJC lines to congregation names | 30.7% | **27.3%** | 61.2% |
  | Drop OJC entirely (published sensitivity) | 28.3% | 25.1% | 63.1% |
  | Symmetric: drop every sponsor's yeshiva/school and chesed-fund block lines | 32.7% | 29.2% | 59.5% |
  | Symmetric: every sponsor, congregation names only | 25.8% | 23.0% | 66.6% |

  **Reading.** "About three-tenths" survives as an upper figure. The central figure for church-status block dollars stays 30.2%. The OJC-only variants filter one sponsor and not the others, so 27–30% is a sensitivity range, not a restatement; the symmetric congregations-only figure is 23.0% [V wave 43B] The low end confines OJC to congregation-named recipients, and 25.1% applies without OJC at all. On a congregations-only basis applied to every sponsor, the faith share is about 23%, against 26.6% under the base rules [C][I].

**(B) Groundswell Charitable Foundation (EIN 871530516)**

- **The 12,808 accounts are individual giving accounts, one DAF per registered user, mostly employees of client companies. They are not employer or campaign funds.**
  - The Foundation's terms of use say: "Your Contributions will be held by the Foundation in a Donor Advised Fund account for you." [P]
  - The accounts are funded by the user (ACH, card, payroll deposit, DAF-to-DAF transfer) and by the employer, which "may directly contribute funds to your DAF … in connection with a matching campaign or in recognition of a cause" [P].
  - The account stays with the user after a job change [P].
- **They are DAFs in the legal sense and meet DAFRC's selection rule.**
  - The amended TY2024 return reports them in Schedule D Part I column (a) and answers Yes to Schedule D lines 5 and 6, the DAF-specific disclosures [F].
  - The terms state that the Foundation "operates all DAFs in compliance with" IRC 4966 and 4967 [P].
  - Employer-funded dollars still fit IRC 4966(d)(2)(A)(iii): the advisory privilege may be held by "any person appointed or designated by such donor" [P].
  - Only Part IV line 6 answers "No", which contradicts the return's own Schedule D [F][I].
- **In size they are processor-like accounts, not traditional DAFs** [C]:
  - year-end value averages $787 per account;
  - contributions average $757 per account;
  - Part IX grants are $348 per account;
  - Part III reports "over 26,000 individual grants" to "approximately 4,850 unique nonprofit recipients", so the average grant is at most about $172.
- **Separate funds.** Groundswell also sells corporate DAFs and employee assistance funds. The return reports 5 column (b) "funds and other accounts" holding $465,493, kept apart from the 12,808. Some corporate DAFs may sit inside column (a); the filing does not split them out [F][I].

## 1. Method

### 1.1 Part A: OJC Fund

1. **Frame.** `build_frame` rebuilds the b4026-06-01 frame with the same imported functions and caches as `mission_faith_sponsors_outside.main`:
   - DAFRC panel and weights;
   - `q120201/lines` for OJC and other panel sponsors, and `rcp/lines` for the top 50;
   - the `q2661` cache for non-panel faith sponsors;
   - the `rcp/bmf` BMF and the TEOS index history.
   - It reproduces the published figures exactly: S2 faith share 0.33698 and S3 0.30178; block $7,257,803,422 and $8,104,486,444; OJC block $545,325,747 on 4,077 lines to 2,394 recipients, equal to the CSV's `block:sponsor` row. A cache-only rerun of the base script gave a byte-identical copy of `faith-sponsors-church-dollars-2026-11-20.csv` (md5 e497f4ac…).
2. **OJC lines.** These are the FY2023 return (period ending 2023-06, oid 202411369349313111, 3,009 lines) and the FY2024 return (2024-06, oid 202521359349314057, 3,410 lines). The frame's DAF weights are 0.99824 and 0.98738.
3. **Buckets (first match wins).**
   - `daf_sponsor_netted`: the frame's DAF-to-DAF flag.
   - `daf_sponsor_not_netted`: a DAFRC panel EIN, or a DAF-sponsor name pattern (`DAF_RX`).
   - `federation`: `FED_RX`.
   - `church_block`.
   - `church_coded_not_block`: FOUNDATION 10 but files a 990.
   - `bmf_SS_FF`: other BMF SUBSECTION/FOUNDATION pairs.
   - `no_bmf_match`.
4. **Block sub-types (`FINE_RX`, first match wins).** The rule is the base study's `RTYPES` extended for Orthodox names, tested in this order:
   1. **school_yeshiva:** adds MOSDOT/MOSDOS, UTA, TORAH VYIRAH, BNOS, KOLEL, INSTITUTIONS.
   2. **chesed_or_relief_fund:** KEREN, CHESED/CHASDEI, GEMACH, TZEDAKAH spellings, EZRA, REFUAH, HATZOLAH, ACHIEZER, YAD, MIFAL, FUND and others.
   3. **communal_umbrella:** CENTRAL CONGREGATIONS, CENTRAL UTA, VAAD, AGUDA, COUNCIL, ASSOCIATION.
   4. **congregation:** the base congregation words plus KHAL, BAIS/BEIS/BETH, OHEL, ADAS, MINYAN, NUSACH.
   5. **unclassified.**
   - Chesed and school words are tested before congregation words. So "CONGREGATION AHAVAS TZDOKAH VCHESED" and "CONG REFUAH HELPLINE MRS LANDAU" count as funds, and "CONG KOLEL …" counts as school. The base study types these as congregations.
5. **Other measures.**
   - **Overlap:** for each OJC block recipient, the S3 dollars from all other sponsors.
   - **Inflows:** every positive line in any frame sponsor-year whose recipient EIN is 113618879.
6. **Recomputed faith share.** Each variant removes lines from both the numerator and the denominator (§0 table). The reattribution variant instead moves 7.358% of OJC's block dollars from faith to non-faith and leaves the denominator unchanged.

### 1.2 Part B: Groundswell

- **Return.** The script reads the amended TY2024 Form 990 (oid 202640289349301029) from the GivingTuesday mirror and records 23 tags. It also extracts the Part III text, the Schedule O amended-return explanation and Schedule R, and computes the derived ratios.
- **Web pages.** It reads seven www.groundswell.io pages (`faq`, `legal/terms`, `products/giving`, `pricing`, `employee-assistance`, `daf`, `phaas`) and records 17 verbatim snippets. All 17 were found.
- **Statute.** IRC 4966 was read on Cornell LII to quote the DAF definition.

### 1.3 Run, reproducibility and robots log

```
S=<scratchpad>
python3 scripts/mission_ojc_groundswell.py . --np-cache $S/npcache --lines-cache-top50 $S/rcp/lines \
  --lines-cache $S/q120201/lines --bmf-dir $S/rcp/bmf --index-dir $S/irs --outreach-dir $S/q2606/outreach \
  --np-work $S/q2661 --work $S/qojc [--fetch]
```

- `--fetch` was used once. Two later cache-only runs gave byte-identical CSVs (md5 2e3b9e89…). In cache-only mode the script reports the last logged robots check.
- Every request used the user agent `research-script/1.0`. The checks are logged in `$S/qojc/robots-log.tsv`:

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404, no rules (2026-11-20T01:59:33Z) | Groundswell XML (68,035 bytes) |
| www.groundswell.io | 200; `User-agent: *` with an empty `Disallow:` | 7 pages read by the script, plus 6 more read by hand (home, products/donor-advised-fund, blog employee-DAF guide, blog DAFs-for-financial-wellness, about-us, eaf/lausd) |
| www.law.cornell.edu | 200; no Disallow for /uscode/ | 26 U.S.C. §4966 |
| archive.org | 200; disallows only /control/ and /report/ | Wayback availability API only. A 2024-12-11 snapshot of the FAQ exists |
| web.archive.org | no response (HTTP 000) | **Not used.** Without a robots answer, no archived page was read |

- **Not used:** sec.gov, crt.sh and certspotter. OJC's XMLs were not re-fetched; the validator's wave-42B copies were used only to quote OJC's Part III text.

## 2. Results: OJC Fund

### 2.1 Where OJC's Schedule I dollars go (FY2023–24) [C]

| Bucket | Recipients | Lines | Schedule I $ | Share |
|---|---|---|---|---|
| Church block (FOUNDATION 10, no e-filed 990) | 2,394 | 4,077 | 549,453,233 | 76.26% |
| Public charity, FOUNDATION 15 (170(b)(1)(A)(vi)) | 732 | 1,148 | 90,916,954 | 12.62% |
| No match in the 2026-11 BMF | 476 | 746 | 59,305,569 | 8.23% |
| School, FOUNDATION 11 | 155 | 247 | 10,290,953 | 1.43% |
| FOUNDATION 16 (509(a)(2)) | 72 | 104 | 3,948,633 | 0.55% |
| Church-coded but files a 990 | 20 | 35 | 2,766,663 | 0.38% |
| DAF sponsor, netted in frame | 4 | 7 | 1,622,794 | 0.23% |
| Private foundation, FOUNDATION 04 | 27 | 39 | 1,592,607 | 0.22% |
| DAFRC panel member, not netted | 5 | 8 | 472,397 | 0.07% |
| Federation name | 2 | 4 | 59,479 | 0.01% |
| FOUNDATION 03 and 12 | 3 | 4 | 36,349 | 0.01% |
| **Total** | | **6,419** | **720,465,631** | 100% |

- **Itemised DAF-sponsor and federation lines.** All 19 are in `ojc:passthrough_line`. The largest is Friends of Mosdot Goor ($464,537 and $418,839), which is a DAFRC panel member. The two federation-named recipients are New York United Jewish Association and the Federation of Jewish Communities of the CIS.
- **Private foundations.** $1.59m goes to FOUNDATION 04 private foundations. Under IRC 4966(c) such grants need expenditure responsibility [I]. This audit does not test whether it was exercised.

### 2.2 Who the church-block recipients are [C][I]

| Fine type | Recipients | DAF-weighted $ | Share of OJC block |
|---|---|---|---|
| congregation | 1,110 | 212,335,737 | 38.94% |
| school_yeshiva | 585 | 141,346,360 | 25.92% |
| unclassified | 517 | 93,788,630 | 17.20% |
| chesed_or_relief_fund | 217 | 89,802,811 | 16.47% |
| communal_umbrella | 21 | 8,052,209 | 1.48% |

- **The largest recipients** are:
  - Keren Mugein Imoisheya ($14.1m, chesed fund, ruled 1998);
  - Congregation Chonen Vnosen ($12.4m, ruled 2015);
  - United Talmudical Academy of Kiryas Joel ($6.2m);
  - Zichron Menachem ($6.2m, unclassified);
  - Binyan Yerushlaim ($6.1m);
  - Congregation Ahavas Tzdokah Vchesed ($5.8m);
  - Chasdei Meshilam ($5.8m);
  - Mosdot Botoshan ($5.5m);
  - Central Congregations of Yetev Lev D'Satmar ($5.3m).

  The top 100 are in `ojc:block_top_recipient`.
- **Ruling year.** 22.0% of block dollars go to EINs ruled in 2018 or later (731 recipients), 17.9% to 2010–17, 22.1% to 2000–09 and 38.0% earlier [F]. A church does not need a ruling to be exempt, so the ruling year shows when status was confirmed, not when the body was founded.

### 2.3 Overlap and inflows [C]

- **Shared recipients.** 1,261 of OJC's 2,394 block recipients also receive S3 lines from other sponsors. They take 74.5% of OJC's block dollars ($406.1m), and other sponsors send them $573.3m. The main other payers are:
  - Fidelity Charitable: 1,119 of these recipients, $285.2m;
  - PayPal Charitable Giving Fund: 157, $50.7m;
  - Jewish Communal Fund: 294, $49.6m;
  - Jewish Community Foundation of Los Angeles: 108, $48.0m;
  - Vanguard Charitable: 164, $43.0m;
  - NPT: 213, $37.8m.
- **OJC-only recipients.** 1,133 recipients (25.5% of OJC's block dollars) get no other sponsor's itemised line.
- **Inflows to OJC.** Panel sponsors' grants to OJC total $54,043,136 on 19 lines from 10 sponsors:
  - PayPal Charitable Giving Fund: $16,713,701 (its FY2023) and $27,678,081 (its FY2024);
  - Fidelity Charitable: $4,196,228 and $3,147,749;
  - American Endowment Foundation: $1,119,727;
  - others under $0.4m each.
  - Sponsor fiscal years differ from OJC's (years ending June), so the 7.36% ratio to OJC's DAF contributions is approximate.

### 2.4 Faith share recomputed

- See the §0 table. Detailed rows are `faith_share:block` (16 rows) and `faith_share:block_fine_type` (block dollars by fine type and faith flag, for every sponsor).
- **What drives the symmetric congregations-only figure (23.0% in S3).** Faith sponsors send 13.2% of S3 block dollars to congregation names and non-faith sponsors 44.2%. Faith sponsors also send 12.2% to unclassified names, against 17.2% from non-faith sponsors [C].

### 2.5 OJC's own description [F]

- **Mission (FY2024 Part I and Part III):** "To maintain a donor advised fund by honoring our commitment to fundholders by providing services to make their charitable giving administratively efficient, and personally rewarding."
- **Schedule I Part I grant monitoring:** "The organization performs ongoing reviews of grantees to ensure that they are properly recognized tax-exempt entities…"
- **Schedule D lines 5 and 6:** both answered Yes. The return reports 5,976 DAFs.

## 3. Limits

1. **The name rule is an inference.** It types recipients by name only. Many Hebrew names are opaque (Toirem, Sifrei Algazi, Binyan Yerushlaim), and "CONG" prefixes are used by yeshivas and chesed funds as well as synagogues. The fine rule and the base rule type many of the same names differently (§2.2 against §0). No recipient's website or charter was read. P-B40601P0503-04 proposes a hand-validated sample.
2. **Church status is taken from the 2026-11 BMF**, applied to FY2023–24 grants, as in the base. FOUNDATION 10 covers churches and also "conventions or associations of churches" and integrated auxiliaries. The IRS does not test a church's self-classification at filing. The BMF code is the IRS's record, not an audit.
3. **"Pass-through" here means grants to DAF sponsors or federations.** Whether a chesed fund or yeshiva re-grants the money cannot be seen: church-status bodies do not file 990s.
4. **Inflow attribution is partial.** Only panel sponsors' itemised lines are counted. Gifts to OJC from donors' other DAFs below $5,000 per sponsor-year, or from non-panel sponsors, are missed.
5. **The 476 no-BMF EINs** (8.2% of dollars) are outside the block. Whether they are revoked, terminated or mis-keyed is open (P-B40601P0503-01).
6. **Caveats carried over.** All b4026-06 and b4026-06-01 caveats apply: no unitemised money, sponsor-level DAF weights, and BofA and Renaissance absent.

## 4. Results: Groundswell

### 4.1 What the amended TY2024 return says [F]

| Item | Value |
|---|---|
| Amended / e-filed | `AmendedReturnInd` X; `ReturnTs` 2026-01-28T13:35:16-06:00; tax period ending 2024-12-31; formed 2021 |
| Part IV line 6 (`DonorAdvisedFundInd`) | 0 (No) |
| Schedule D Part I col. (a) | 12,808 held; contributions $9,691,912; grants blank; EOY $10,084,314 |
| Schedule D Part I col. (b) | 5 held; contributions blank; EOY $465,493 |
| Schedule D lines 5, 6 (`DisclosedOrgLegCtrlInd`, `DisclosedForCharitablePrpsInd`) | 1, 1 (Yes, Yes) |
| Cash, non-interest-bearing, EOY | $10,549,807, equal to (a) + (b) EOY [C] |
| Contributions; grants (Part IX line 1) | $11,750,787; $4,463,378 |
| Staff | 0 employees, 5 volunteers. Schedule R: related taxable company Groundswell Giving Inc ("developer and operator of proprietary software platform"); "amounts payable to GWG" $473,877 |
| Part III | "disbursed $4,463,378 in grants at the advice of donors. Over 26,000 individual grants were made, constituting approximately 4,850 unique nonprofit recipients" |
| Schedule O | The amendment added the Part I values. It labels the $10,084,314 as "line 3", although the e-file tag is the year-end value (line 4). Grants were $4.46m, so the e-file tag is right [I] |

### 4.2 What the platform says (pages retrieved 2026-11-20) [P]

- **FAQ:**
  - "Groundswell accounts are powered by a donor-advised fund, or a DAF."
  - "Employees can contribute funds to their account, companies match those funds, and then the funds can be donated to their chosen nonprofits."
  - "A Groundswell account is theirs forever - even if they leave their current company."
  - Funding is "via bank account/ACH, split deposits with their payroll provider, debit/credit card, and DAF-to-DAF transfer"; "a minimum amount of $5 is required for each transaction".
- **Terms of use** (Last Updated Date: July 6, 2026):
  - "Your Contributions will be held by the Foundation in a Donor Advised Fund account for you".
  - "DAFs are component funds of the Foundation; they are not separate legal entities."
  - The Foundation "operates all DAFs in compliance with Internal Revenue Code … Sections 4966 and 4967".
  - An Authorized Employer "may directly contribute funds to your DAF … (for example, in connection with a matching campaign or in recognition of a cause)".
  - Payroll contributions "shall remain in your DAF" after employment ends.
  - Users must "annually recommend Distributions in an amount that totals at least five percent (5%)" of prior year-end assets.
  - The tax receipt covers contributions "not including any Employer Contributions or gifts from others".
- **Products:**
  - "Groundswell offers each employee their own donor-advised fund (DAF)" (products/giving).
  - "Create and manage multiple corporate Donor-Advised Funds (DAFs)" (products/giving).
  - Employee assistance funds that employees "support … directly from their Groundswell personal giving accounts" (employee-assistance).
- **Statute** (26 U.S.C. §4966(d)(2)(A)): a DAF is a fund "separately identified by reference to contributions of a donor or donors", "owned and controlled by a sponsoring organization", and "with respect to which a donor (or any person appointed or designated by such donor) has, or reasonably expects to have, advisory privileges".

### 4.3 Classification [I]

| Question | Answer | Basis |
|---|---|---|
| Individual accounts or employer/campaign funds? | **Individual accounts.** There is one DAF per registered user, mostly employees, and employer matches or gifts are deposited into the employee's DAF | FAQ, terms §3.1 and §4.1(c), products/giving |
| DAFs in the IRC 4966(d)(2) sense? | **Yes.** They are separately identified, owned by the Foundation, and advised by the user. For employer-funded dollars the employee is the "person appointed or designated by such donor" | terms §3.1–3.3; statute |
| DAFs in the DAFRC sense? | **They meet DAFRC's selection rule**: Schedule D Part I(a) filed with at least $1 of DAF assets (technical appendix, per g1915b-04 §1 item 4). Whether DAFRC's manual vetting would admit Groundswell is unknown, since its returns arrived after the 2025 cut-off (wave 39B) | return; g1915b-04 |
| Comparable to traditional DAF accounts? | **No, processor-like.** $787 average balance; grants ≤ $172 on average; about 2 grants per account; columns (a) and (b) together equal the non-interest-bearing cash balance exactly | §4.1 |
| Is the line 6 "No" right? | **No.** It contradicts the return's own Schedule D Part I(a) and lines 5–6 | return |

- **Corporate DAFs.** "Multiple corporate DAFs" are sold, and the 5 column (b) accounts may be employee assistance funds or corporate funds. The filing gives no way to separate corporate DAFs from the 12,808. The platform offers “each employee their own donor-advised fund”, while corporate DAFs are a separate add-on, so most of the 12,808 are likely employee accounts [I]. The employer and employee split of the $9.69m of contributions is not public, because Schedule B is restricted.
- **Timing of the web evidence.** The terms are a 2026 version. The 2024 versions were not read, because web.archive.org gave no robots answer.

## 5. Implications

- The b4026-06-01 headline "about 30%" of church-block DAF dollars from faith sponsors is the central figure for church-status recipients. Report about 30%, with 27–29% if OJC’s non-congregation recipients are discounted, 23% on a congregations-only basis for every sponsor, and 25.1% without OJC [V wave 43B] It rests on church-status recipients, of which about two-fifths of OJC's dollars go to yeshivas and chesed funds rather than congregations.
- OJC is "pass-through" in the asset sense (DAF assets $34.5m against $385.7m of DAF grants). It is not a conduit to other sponsors.
- Groundswell's accounts can stay in DAF account totals, as they are DAFs. They should be tagged as employer-platform micro-accounts, alongside processor accounts (P-B40601P0503-06).

## Exact corrections

### `research/mission-2026-11-14/b4026-06-01-faith-sponsors-outside-top50.md`

- **Find:** "76.4% of its own DAF-weighted dollars go to the block, mostly Orthodox congregations, yeshivas and chesed funds."
- **Replace with:** "76.4% of its own DAF-weighted dollars go to the block. Every block recipient is church-status in the BMF (FOUNDATION 10; filing-requirement code 06 for 99.6% of the dollars), but by name only 38.9% of its block dollars go to congregations; 25.9% go to yeshivas and schools, 16.5% to chesed or relief funds, 1.5% to communal umbrella bodies and 17.2% to names the rule cannot type. Its lines are not pass-throughs: 0.30% of its Schedule I dollars go to DAF sponsors, other DAFRC panel members or federations, none of them in the block (b4026-0601-01-p0503-ojc-groundswell.md) [ojc-gs]"

- **Find:** "Without the OJC Fund the figures are 25.1% (S3) and 28.3% (S2) [F]."
- **Replace with:** "Without the OJC Fund the figures are 25.1% (S3) and 28.3% (S2) [F]. Keeping only the OJC Fund’s congregation-named recipients gives 27.3% (S3) and 30.7% (S2); dropping only its yeshiva and chesed-fund lines gives 28.2% and 31.6%, so 27–30% is the defensible S3 range (b4026-0601-01-p0503-ojc-groundswell.md) [ojc-gs]"

- **Find:** "Any error in its Schedule I moves the faith share by up to about 5 points."
- **Replace with:** "Any error in its Schedule I moves the faith share by up to about 5 points. An audit of all 6,419 lines (b4026-0601-01-p0503-ojc-groundswell.md) finds no pass-through to DAF sponsors or federations in the block, but 42.4% of its block dollars go to yeshiva/school and chesed-fund names. About 7.4% of its FY2023–24 DAF contributions arrive as grants from other panel sponsors, mainly PayPal Charitable Giving Fund ($44.4m); reattributing that share lowers the S3 faith share from 30.2% to 29.7% [ojc-gs]"

### `research/mission-2026-11-14/b4026-06-church-daf-recipients.md`

- **Find:** "without it the all-panel share is 25.1% [V wave 42B]"
- **Replace with:** "without it the all-panel share is 25.1% [V wave 42B]. Its Schedule I sends 0.30% to DAF sponsors, other panel members or federations and none of that reaches the block, but only 38.9% of its block dollars go to congregation-named recipients; limited to those, the all-panel share is 27.3% (b4026-0601-01-p0503-ojc-groundswell.md) [ojc-gs]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "(25% without the OJC Fund, a pass-through sponsor)"
- **Replace with:** "(25% without the OJC Fund, a pass-through sponsor in the asset sense whose Schedule I goes to church-status Orthodox bodies, not to other DAF sponsors; 27% if only its congregation-named recipients count) [ojc-gs]"

- **Find:** "its accounts average $787, which raises the same comparability caveat as processor accounts."
- **Replace with:** "its accounts average $787, which raises the same comparability caveat as processor accounts. They are DAFs in the legal sense and meet DAFRC’s Schedule D Part I(a) rule: one DAF per user, mostly employees, funded by the user and by employer matches (b4026-0601-01-p0503-ojc-groundswell.md) [ojc-gs]"

- **Find:** "(average $787 per account)"
- **Replace with:** "(average $787 per account; per-employee DAFs funded by employees and employer matches, so DAFs but processor-like in size) [ojc-gs]"

### `research/mission-2026-11-14/prop-0503-1915-propagation.md`

- **Find:** "Whether they are DAFs in the DAFRC sense is not settled here (queue P-P0503-1915-02)."
- **Replace with:** "P-P0503-1915-02 settles the DAF question: the accounts are individual DAFs (one per registered user, mostly employees of client companies), funded by the user’s ACH, card, payroll or DAF-to-DAF deposits and by employer matches or gifts; the Foundation’s terms say it operates all DAFs under IRC 4966 and 4967, and Schedule D lines 5 and 6 answer Yes. They meet DAFRC’s Schedule D Part I(a) selection rule and are processor-like in size, not employer or campaign funds (b4026-0601-01-p0503-ojc-groundswell.md) [ojc-gs]"

- **Find:** "**Groundswell's sponsor status is inference.**"
- **Replace with:** "**Groundswell's sponsor status is now documented** (b4026-0601-01-p0503-ojc-groundswell.md): its terms hold contributions “in a Donor Advised Fund account for you” and its TY2024 Schedule D answers lines 5 and 6 Yes; only Part IV line 6 says No [ojc-gs]"

- **Find:** "as the only likely sponsor among the outside-panel rows [I]."
- **Replace with:** "as the only likely sponsor among the outside-panel rows [I]. P-P0503-1915-02 confirms it from the filing and the terms of use [ojc-gs]"

### `research/mission-2026-11-14/g1915b-04-line6-vs-schedule-d.md`

- **Find:** "Except for Groundswell and possibly Samaritan Bethany, these are operating charities using the DAF column [I], as batch 38 found."
- **Replace with:** "Except for Groundswell and possibly Samaritan Bethany, these are operating charities using the DAF column [I], as batch 38 found. Groundswell is a DAF sponsor on its own documents: one DAF per user, mostly employees, funded by the user and by employer matches, with Schedule D lines 5 and 6 answered Yes (b4026-0601-01-p0503-ojc-groundswell.md) [ojc-gs]"

### `research/mission-2026-11-14/queue-batch37-filing-questions.md`

- **Find:** "It does not quite: the average is above $500."
- **Replace with:** "It does not quite: the average is above $500. Its accounts are per-user DAFs under its terms of use, funded by employees and by employer matches; its TY2024 grants average at most about $172 (over 26,000 grants, $4.46m) (b4026-0601-01-p0503-ojc-groundswell.md) [ojc-gs]"

## 6. Source register

| # | Source | URL | Accessed | Used for | Tag |
|---|---|---|---|---|---|
| S1 | OJC Fund Form 990 FY2023 (period ending 2023-06), Schedule I/D | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411369349313111_public.xml (read via the q120201 line cache and npcache extract) | caches 2026-11-19; wave-42B copy | lines, weights, DAF contributions | F |
| S2 | OJC Fund Form 990 FY2024 (period ending 2024-06) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521359349314057_public.xml | as S1 | lines, mission text, Schedule D lines 5–6 | F |
| S3 | Other panel sponsors' Schedule I FY2023–24 (frame caches) | mirror pattern https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml; index https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv | caches | overlap, inflows to OJC | F |
| S4 | IRS EO BMF extract | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf | repo cache 2026-11-14 | SUBSECTION, FOUNDATION, filing requirement, deductibility, ruling, NTEE | F |
| S5 | IRS EO BMF data dictionary | https://www.irs.gov/pub/foia/ig/tege/eo-info.pdf | via base study | FOUNDATION and filing-requirement codes | P |
| S6 | DAFRC Annual DAF Report 2025 dataset | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx (repo copy) | repo | panel, faith subtype | F |
| S7 | Groundswell Charitable Foundation amended TY2024 Form 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640289349301029_public.xml | 2026-11-20 | §4.1 | F |
| S8 | Groundswell FAQ | https://www.groundswell.io/faq | 2026-11-20 | account model, funding | P |
| S9 | Groundswell terms of use (Last Updated July 6, 2026) | https://www.groundswell.io/legal/terms | 2026-11-20 | DAF per user, employer contributions, 4966 | P |
| S10 | Groundswell product pages | https://www.groundswell.io/products/giving ; https://www.groundswell.io/employee-assistance ; https://www.groundswell.io/phaas ; https://www.groundswell.io/pricing | 2026-11-20 | per-employee DAF, corporate DAFs, EAF | P |
| S11 | 26 U.S.C. §4966 | https://www.law.cornell.edu/uscode/text/26/4966 | 2026-11-20 | DAF definition | P |
| S12 | Repo: b4026-06-01, wave 42B, g1915b-04, prop-0503-1915, waves 39B/40A | repo | repo | base figures, DAFRC selection rule | R |

## 7. Data dictionary: `ojc-groundswell-audit-2026-11-20.csv`

| Column | Meaning |
|---|---|
| `section` | Row family (see below) |
| `scenario` | FY2023 / FY2024 / FY2023-24 for OJC rows; S2_… or S3_… for faith-share rows; TY2024 or retrieval date for Groundswell rows |
| `key` | Bucket, fine type, variant name, recipient or sponsor EIN, XML tag, derived-measure name, page path or host |
| `label` | Recipient or sponsor name; for `faith_share:block`, the variant description |
| `detail` | Recipient: city, state, BMF SUBSECTION/FOUNDATION, NTEE, ruling, base rtype. Passthrough: whether in the DAFRC panel. Faith share: national share, or the inflow ratio and the shifted dollars |
| `category` | Bucket or fine type (`congregation`, `school_yeshiva`, `chesed_or_relief_fund`, `communal_umbrella`, `unclassified`) or attribute name |
| `recipients`, `lines` | Distinct recipients; Schedule I lines |
| `usd_schedule_i` | Positive Schedule I dollars, unweighted |
| `usd_daf_weighted` | The same × the frame's DAF weight (OJC 0.99824 FY2023, 0.98738 FY2024) |
| `share` | `ojc:bucket`: share of OJC Schedule I $. `ojc:block_*`: share of OJC block dw. `faith_share:block`: block dw kept ÷ central block dw. `faith_share:block_fine_type`: share of central block dw |
| `value` | `faith_share:block`: faith share of block dw. `ojc:return`: DAF weight. `ojc:block_top_recipient`: other sponsors' S3 dw to the recipient. `ojc:inflow_total`: inflow ÷ OJC DAF contributions. `gs:*`: tag value, derived figure, text or snippet |
| `note` | Definition of the row |
| `source` | Primary source(s) or URL |

**Sections:**
- `ojc:return`, `ojc:bucket`, `ojc:block_fine_type`, `ojc:block_base_rtype`, `ojc:block_bmf_attr`;
- `ojc:block_overlap`, `ojc:block_overlap_sponsor`, `ojc:block_top_recipient` (top 100), `ojc:passthrough_line`;
- `ojc:inflow_from_panel_sponsor`, `ojc:inflow_total`;
- `faith_share:block`, `faith_share:block_fine_type`;
- `gs:xml_tag`, `gs:derived`, `gs:text`, `gs:robots`, `gs:web_snippet`.
