# Processor disbursement rules from public help centres, compared with sponsor rules and linked to complaints

**Queue item:** P-G1913-04 | **Research date:** 2026-11-19 | **Builds on:** [gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md) (complaint records CMP-G1913-001 to -047) and [`sponsor-grant-payment-policies.csv`](../../data/mission-2026-11-14/sponsor-grant-payment-policies.csv) (10 sponsor or rail rows, retrieved 2026-11-14)

**Files written**
- [`data/mission-2026-11-14/processor-disbursement-rules-2026-11-19.csv`](../../data/mission-2026-11-14/processor-disbursement-rules-2026-11-19.csv): 47 rows, one per processor × rule, 17 columns (data dictionary in §8).
- [`data/mission-2026-11-14/queue-proposals-g1913-04.csv`](../../data/mission-2026-11-14/queue-proposals-g1913-04.csv): 6 rows, P-G1913-04-01 to -06.
- This note.

**Coverage:** 8 processors. Benevity/AOGF has 7 rows. YourCause/Blackbaud Giving Fund, For Good (Network for Good), PayPal Giving Fund, Dechomai and Goodstack have 6 each. CyberGrants (Bonterra CGDS) and Every.org have 5 each. Benevity Causes (the nonprofit-facing help centre for AOGF) was blocked, so it is folded into the Benevity rows (§3.1).

---

## 1. Summary

1. **Most of the processor delays that nonprofits complain about are written into the rules.** Two of the seven complaints named in the brief are fully explained by a published rule, four are partly explained and one is not explained (§5).
   - **CMP-G1913-001 (fully explained).** A $75 gift was held about eight months. Benevity's foundation fee schedule says a charity that is not on EFT gets a check only once platform-wide donations "must equal at least $100 (CAD or USD, as applicable)". Smaller balances are swept by check about once every twelve months if they reach $20. Below $20, the donor's advice "may be rejected" ([Fees Schedule, last updated 2026-10-01](https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf)).
   - **CMP-G1913-034 (fully explained).** A returned check was redirected to an employer-chosen charity. YourCause's own help pages describe the whole sequence. A returned check means "we have suspended any further charitable disbursements". The charity must complete registration before a reissue. After a 180-day holding period, donations from employees outside California "redirect automatically to the community's preferred alternate organization" ([email 94](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-email-94.html); [How Stranded Funds Automation Works](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/csrconnect-prod/content/csrc-sfa-redirects.html)).
2. **Benevity's written cadence leaves the timing to the Foundation.** The End User Terms say the Foundation "determines whether and when to make disbursements to Causes". The typical timing is the calendar month after receipt, with exceptions for thresholds and special circumstances ([End User Terms, 2025-12-24](https://benevity.com/legal/end-user-terms-of-use)).
   - This covers the irregular payouts in -006 and -018 and the three-month payout in -009, but only in the sense that the terms allow them. No written rule predicts them.
   - The 14 months in -027 exceeds even the annual sweep.
3. **The 180-day Benevity void in the brief could not be verified.** The Benevity Causes help centre (causeshelp.benevity.org) and helpcenter.benevity.org returned HTTP 403 to a generic client, although robots.txt allows /hc/ articles.
   - Readable Benevity pages say only that a charity with "a series of uncashed checks with outstanding donations" can be deactivated ([nonprofit eligibility](https://benevity.com/nonprofit-eligibility)).
   - The 180 days therefore rests on the complainant in CMP-G1913-002.
4. **The help pages read for this note do not state the For Good compliance or tax holds the brief refers to.**
   - The terms (last updated 2026-09-01) say ForGood will make a grant "as long as You satisfy ForGood's legal requirements". They also say ForGood may suspend an account "for any other reason whatsoever" and may re-grant "for any reason".
   - None of these clauses sets a hold duration or describes a compliance timeout ([terms](https://www.forgood.org/legal-pages/terms-conditions)).
   - The old Network for Good help centre (intercom.help/networkforgood) now returns 404 on every article URL tried.
   - So -037, -040 and -041 are only partly explained.
   - One written rule cuts the other way. It says ForGood "shall disburse any donations … at least every twelve (12) months", with a minimum disbursement amount of $9.51. A $50 balance unpaid after a year (-039) would breach the current rule, but the record dates from 2024-07-01, before these terms (2026-09-01), and "went to another entity" fits the re-grant clause. It is coded unverified [V wave 33A]
5. **Processors and sponsors differ in four structural ways** (§4):
   - **Thresholds.** Benevity ($100 check, $20 sweep), For Good ($9.51; Every.org's page says $10.00), Every.org (via ForGood) and Goodstack (amount unstated) hold small balances. None of the 10 sponsor rows records a minimum.
   - **Batching.** Processors pay in monthly batches: Benevity in the month after receipt, For Good on the 15th, PayPal Giving Fund (PPGF) around the 25th. YourCause and CyberGrants follow a schedule each corporate client sets, typically monthly or quarterly. Sponsors pay per grant within days.
   - **Void windows.** Processor windows run from 120 days (YourCause) to 180 days (CGDS) and 6 months (For Good). The sponsor rows show 90 days (Fidelity, BlueGive, Chariot DAFpay Network) and 14 days for an unaccepted PayPal grant at NPT.
   - **Redirection target.** YourCause and CGDS redirect to an organization chosen by the employer or client. PPGF, Goodstack, For Good and Benevity redirect to a charity they choose themselves, usually one in a similar cause area. Among the sponsors, Fidelity returns the funds to the donor's Giving Account and reissues only at the donor's request. Only Chariot's DAFpay Network may regrant to a similar cause.
6. **Fees withheld range from 0% to 5% before card and check fees:**
   - Blackbaud Giving Fund, PPGF (enrolled charities) and Every.org (Stripe or PayPal): 0%.
   - Every.org via ForGood: 1.50%.
   - Benevity/AOGF: 2.99%, capped at $500 (the cap does not apply to matches or securities), plus a manual check fee of the higher of $35 or 8%, up to $125, after a charity's second check.
   - CGDS: 2.97% in the US, 3.47% in Canada (capped at $250 per gift) and 5% for international programmes. The deck notes that "Employees are not notified of these fees".
   - Dechomai: 1–3% (average 1.2–1.4%) with a minimum fee of $10,000.
   - For Good: processing costs are "disclosed to You at the time we distribute"; no rate is published.
   - The sponsor CSV records no fee deducted from grants for any of its rows.
7. **The written rules change without notice, and some contradict themselves:**
   - PPGF's check deadline for unenrolled charities fell from "within 90 days" (2022-03-15 version) to "within 45 days of the end of the month" (2025-01-01 version).
   - YourCause's payment-status page calls a check stale after "over 90 days"; its other pages give 120 days.
   - For Good's FAQ gives both "up to 8 weeks" and "up to 4-6 weeks" for EFT approval.
   - Dechomai's policy sets a $100,000 minimum initial donation, while its FAQ says there is no minimum size.

---

## 2. Method

### 2.1 Sources and scope
- **Official pages only.** We used help-centre articles, terms, policy pages and the processors' own published PDFs. Review sites, blogs and press coverage were not used as evidence.
  - Search-engine summaries were used only to find URLs. Every quoted fragment was then read from our own fetch of the page, and every quote in the CSV was re-checked by script against the cached text (47 rows, 0 misses).
  - The two CyberGrants documents are client training decks hosted on bonterratech.com. They are official, but they are not help-centre pages; the CSV notes this. They contain the client's funding bank-account numbers, which are not reproduced here.
- **Date fields.** `page_stated_date` is the date the page states about itself. `http_last_modified` is the server's Last-Modified header, where one was sent. Help-centre pages state no date, so the header is the only date available for them.
- **Comparison.** The comparison uses [`sponsor-grant-payment-policies.csv`](../../data/mission-2026-11-14/sponsor-grant-payment-policies.csv), read in full: 10 rows covering Fidelity Charitable, DAFgiving360, Vanguard Charitable, NPT, Daffy, Charityvest, AssetMark Charitable, BlueGive, Chariot Disbursements and Chariot DAFpay Network.
- **Complaint linkage.** We used the record text in [`daf-user-complaints-corpus-additions-2026-11-19.csv`](../../data/mission-2026-11-14/daf-user-complaints-corpus-additions-2026-11-19.csv). Each record was coded against the rule that governs it:
  - **full:** the rule predicts the reported outcome;
  - **partial:** the rule permits it, or explains part of it;
  - **not explained:** no written rule predicts it;
  - **contradicted:** the written rule predicts a different outcome;
  - **unverified:** the rule could not be read.
- **Complainant privacy.** We name no complainants and no small nonprofits.

### 2.2 Robots and access log
A stdlib fetcher was used, with user agent `research-script/1.0`. It read each host's robots.txt before the first fetch. A 4xx response for robots.txt was treated as allowed only for 404 and 410.

| Host | robots.txt | Fetch result |
|---|---|---|
| go.benevity.com | 200, allowed | 200 (fee schedule, registration guide, platform guidelines, MSA) |
| benevity.com | 200, allowed | 200 (End User Terms, nonprofit eligibility, nonprofits, sitemap) |
| causes.benevity.org | 200, allowed | 200, but the Terms of Use page is a shell that loads its text from privacyportal-cdn.onetrust.com |
| privacyportal-cdn.onetrust.com | **400** | **not fetched.** Treated as disallowed. A change to RFC 9309 handling (4xx = unrestricted) was refused by the session's permission classifier; see P-G1913-04-04 |
| causeshelp.benevity.org | 200, allows /hc/ articles | **403** (blocked) |
| helpcenter.benevity.org | 200, allowed | **403** (blocked) |
| www.aogf.org | 200, allowed | 200, but a parked "lander" redirect, not AOGF's site. No AOGF-owned site was found |
| webfiles-sc1.blackbaud.com (YourCause NPOconnect and CSRconnect help) | 404 (no file) | 200 on 16 pages; 404 on one production CSRconnect FAQ (the QA copy was read, and is flagged as QA) |
| blackbaudgivingfund.org | 200, allowed | 200 |
| www.yourcause.com, www.blackbaud.com | 200, allowed | 200 (the terms page is a shell with no disbursement text) |
| www.forgood.org, www.networkforgood.com, www.bonterratech.com | 200, allowed | 200. The charitable solicitation disclosures are identical on all three domains |
| intercom.help (/networkforgood/) | 200, allowed | **404** on all 7 URLs (help centre retired) |
| bonterratech.com, status.bonterratech.com | 200, allowed | 200 |
| www.paypal.com | 200, allowed | **403** on all 6 cshelp and policy URLs (blocked) |
| www.paypalobjects.com | 200, allowed | 200 (delivery policies dated 2025-01-01 and 2022-03-15); 404 on 4 guessed file names |
| dechomai.org | 200, allowed | 200 (policies page, its wp-json record, FAQ, terms) |
| support.every.org | 200, allowed | 200 |
| goodstack.org | 200, allowed | 200 |

---

## 3. Results by processor

Full rows, quotes and URLs are in the CSV. The fragments quoted below are verbatim.

### 3.1 Benevity / American Online Giving Foundation (AOGF), including Benevity Causes
| Rule | What the official text says | Source |
|---|---|---|
| Threshold | A check is sent only once platform-wide donations to a non-EFT charity "must equal at least $100". Smaller amounts are "swept" annually if at least $20. Below $20, the donor advice "may be rejected" and the donor may be offered another charity | Fees Schedule, last updated 2026-10-01 |
| Cadence | The Foundation "determines whether and when to make disbursements". Payment is typically in the month after receipt, with exceptions "when minimum donation/disbursement thresholds or maximum limits apply" | End User Terms §6.7, 2025-12-24 |
| Undeliverable | A charity can be deactivated for "a series of uncashed checks with outstanding donations". **No void period was found; the help centre returned 403** | nonprofit-eligibility page (Last-Modified 2026-11-18) |
| Vetting | The charity must keep valid charitable status and is screened daily against sanctions lists. Portal applications are "typically reviewed within 30 days". During Appeals and Remediation, "disbursements to the nonprofit are paused" | registration guide (Last-Modified 2026-03-06); eligibility page |
| Redirection | Where a recommendation cannot be followed, "the Foundation will make the determination of the Cause". It may, but need not, allow an alternate recommendation. For deactivated charities, the foundation partners "will credit their given account" | End User Terms §6.8; eligibility page |
| Fee | Cause Support Fee of 2.99%, capped at $500 (the cap does not apply to matches or securities). AOGF card fee 2.95%; PayPal 1.99% + $0.49 for US accounts. FX markup 1.50%. Manual check fee is the higher of $35 or 8%, up to $125, and starts after a charity's second check. Client agreements can override all of these | Fees Schedule |

### 3.2 YourCause / Blackbaud Giving Fund (BBGF)
| Rule | What the official text says | Source |
|---|---|---|
| Threshold | None published on the pages read | — |
| Cadence | "The disbursement schedules are set by the client. Most client disburse monthly or quarterly." The BBGF FAQ adds that payments are "generally made within five to seven days of being funded" | NPOconnect FAQ; CSRconnect BBGF FAQ (Last-Modified 2026-11-16) |
| Undeliverable | A returned check suspends all further disbursements "until a valid disbursement address is provided". A reissue is possible only once a check has been outstanding more than 45 days, and the replacement comes "within the next 60 to 90 days". Checks void at 120 days (the payment-status page says stale after "over 90 days") | email 94; Check Reissues; About Payment Status |
| Registration before payment | To claim the donations, "it is required that a representative of the organization complete the registration". The charity must then update its address and contact support. Compliance agreements and vetting also apply. ACH review is "typically within 72 business hours" | emails 92 and 94; Receive Donations FAQ; Set Up ACH |
| Redirection | Stranded Funds Automation holding periods: stale check 240 days, undeliverable check 180, ineligible charity 90, ACH return 30, revoked or payee-returned 0. After that, employee donations from donors outside California "redirect automatically to the community's preferred alternate organization". Donors in California, and company dollars where the employer allows it, get 30 days to choose | How Stranded Funds Automation Works; SFA overview |
| Fee | "The Blackbaud Giving Fund does not charge donors for their grant activity" (card fees excluded) | CSRconnect BBGF FAQ |

The SFA FAQ (read in its QA copy, because the production URL returned 404) cites US H.R. 1 (2025) and California AB 488 as the reason SFA is required. It also says charities get reminder emails at 45 and 90 days and donors at 90 days.

### 3.3 Network for Good / For Good (Bonterra)
| Rule | What the official text says | Source |
|---|---|---|
| Threshold | Checks go out only once aggregate donations total "at least $9.51, net of processing costs". Below that, funds may be held, but ForGood "shall disburse … at least every twelve (12) months" | Terms, 2026-09-01; disclosures, 2026-09-01 |
| Cadence | Payment is "within thirty (30) days after the end of each month" (terms), "typically within fifteen (15) days" (disclosures), and "generally on the 15th" (FAQ) | as above; FAQ (Last-Modified 2026-11-16) |
| Undeliverable | ForGood may re-grant if checks are not cashed "within 6 months of the date of issue". No reissue window is published | Terms |
| Vetting | ForGood will make a grant "as long as You satisfy ForGood's legal requirements". The charity must be a 501(c)(3) public charity, and its address is validated through GuideStar. EFT applications are manually reviewed: "up to 8 weeks" in one FAQ answer, "4-6 weeks" in another. Accounts may be suspended "for any other reason whatsoever" | Terms; FAQ |
| Redirection | ForGood "retains the right to re-grant donations to another charity for any reason", including loss of good standing, an OFAC listing or uncashed checks. Donor-facing pages say it may pick an alternate charity or ask the donor | Terms; disclosures |
| Fee | The grant is made "less any amounts retained by ForGood for processing costs, which shall be disclosed to You at the time we distribute". No rate is published; Every.org's help centre states 1.50% | Terms; Every.org |

**Compliance or tax holds:** no page read states one. Every article URL on the retired help centre (intercom.help/networkforgood) returned 404, so nothing from it is used.

### 3.4 PayPal Giving Fund / PayPal Charitable Giving Fund
These rows come from the Donation Delivery Policy only (last updated 2025-01-01, PDF on paypalobjects.com). The live policy page, the Nonprofit Certification Policy, the Donor Terms and the cshelp articles on www.paypal.com all returned 403.

| Rule | What the official text says | Source |
|---|---|---|
| Threshold | None stated | Delivery Policy 2025-01-01 |
| Cadence | Enrolled charities are paid "on or around the 25th day of each month", nearly always 10–40 days after receipt. Unenrolled charities get a check "within 45 days of the end of the month" of the donation; the 2022-03-15 version said "within 90 days" | Delivery Policies 2025-01-01 and 2022-03-15 |
| Undeliverable | If "a check is returned or is not cashed within the time period specified on the check", PPGF may remove the charity from its directory and reassign the funds | Delivery Policy |
| Vetting | Enrolment is governed by the Nonprofit Certification Policy (blocked). Unenrolled charities are paid only after PPGF has "verified the charity's identity and conducted an appropriate level of due diligence", and after contact attempts by email, letter and phone | Delivery Policy |
| Redirection | PPGF first asks the donor. Otherwise it gives the funds to a charity "that operates in a similar cause area", or else to one with a broad humanitarian mission, favouring enrolled charities | Delivery Policy |
| Fee | Enrolled charities receive payments "quickly and free of charge" | Delivery Policy |

### 3.5 Dechomai
Dechomai's Policies and Procedures page (WordPress record last modified 2024-04-07) ends at section 3.1, although it refers to sections 4.4–4.5. Its payout, undeliverable-grant and redirection rules are therefore **not published**.

The FAQ covers the following:
- **Fee:** 1–3% (average 1.2–1.4%), with "a minimum fee of $10,000".
- **Timing:** grants follow the asset sale, which takes "anywhere from a couple of weeks to a few years". About a third of assets sell within 6 months, a third in 6–24 months and a third after 24 months.
- **Vetting:** due diligence applies to the asset, not to the grantee.

The policy's "$100,000" minimum initial donation conflicts with the FAQ's "no minimum size". No disbursement complaint about Dechomai appears in the additions file.

### 3.6 Further processors (time allowed)
- **CyberGrants / Bonterra CGDS** (training decks, uploaded 2025-01 and 2025-03):
  - **Cadence:** monthly ("most common") or quarterly batches. After funding, ACH takes 1–3 days and a check 1–2 weeks.
  - **Void:** "Checks go stale after 180 days."
  - **Vetting:** organizations are verified via the IRS Business Master File.
  - **Redirection:** by default, redirected funds go to "the default organization that the client has selected in their contract". Under the Donor Choice option, donors get 10 days.
  - **Funds a charity cannot receive** go back to the client as a credit memo.
  - **Fee:** 2.97% in the US and 3.47% in Canada, capped at $250 per gift; 5% for international programmes. The deck notes that "Employees are not notified of these fees".
  - **Operations:** a status-page postmortem (posted 2026-02-04) says missing 2026 dates in the scheduling calendar delayed January 2026 disbursement cycles. This was an operational failure, not a policy.
- **Every.org** (page updated 2026-10-23):
  - **Cadence:** Stripe pays weekly at 0%, PayPal Grants every 4–5 weeks at 0%, and ForGood every 4–6 weeks at 1.50%. Every.org covers the ForGood fee for donations made from bank accounts.
  - **Threshold:** the ForGood route needs a balance "exceeding $10.00".
  - **Undeliverable:** an unaccepted PayPal grant is "returned to us when the grant expires" and Every.org tries again.
- **Goodstack** (delivery and undeliverable-donation policies effective 2024-11-15; charity terms effective 2026-06-22):
  - **Cadence and threshold:** charities are paid monthly once a minimum is reached. The minimum is not stated. Everything is paid after 12 months regardless.
  - **Undeliverable:** unclaimed charities are contacted "typically over a 30-day period", then sent a cheque.
  - **Redirection:** the donor is asked first; otherwise the funds go to a similar charity, or else to a "wide-ranging" one.
  - **Fee:** payouts are "net any applicable fees"; no rate is given.
- **Benevity Causes:** this is the nonprofit portal for the Benevity foundations, so it is covered under §3.1. Its help centre was blocked.

---

## 4. Comparison with sponsor rules

| Dimension | Sponsors (sponsor-grant-payment-policies.csv, 10 rows) | Processors (this CSV) |
|---|---|---|
| Payout threshold | None recorded in any row | Benevity $100 check / $20 annual sweep; For Good $9.51 ($10.00 per Every.org) with a 12-month backstop; Goodstack minimum unstated, 12-month backstop. YourCause, PPGF and CGDS: none published |
| Cadence | Per grant. Fidelity: review 10+ business days, then Stripe/ACH 1–2 days. DAFgiving360: check mailed in 7–10 business days. NPT: 3–5 days. Daffy: up to a week. AssetMark: median 2 days | Monthly batch: Benevity in the month after receipt, For Good on the 15th, PPGF around the 25th, Goodstack monthly. YourCause and CGDS follow client-set monthly or quarterly schedules. Every.org via Stripe is weekly |
| Void / expiry | 90 days (Fidelity, BlueGive, Chariot DPN checks); 14 days for an unaccepted NPT PayPal grant | 120 days (YourCause; 90 on one page); 180 days (CGDS); 6 months before re-grant (For Good); "time period specified on the check" (PPGF); Benevity unverified |
| Registration before payment | Not required. Sponsors fall back to a mailed check to the 990 address or the latest validated address (Fidelity, NPT, Daffy, Charityvest, AssetMark, Chariot) | YourCause requires registration before reissuing a returned check, and suspends other payments meanwhile. Benevity, For Good and Every.org offer EFT only after an application review. Goodstack pays only after onboarding or, failing that, by cheque |
| Undelivered funds go to | Fidelity: back to the donor's Giving Account, reissued only at donor request. BlueGive: redeposited. Chariot DPN: may contact the donor or regrant to a similar cause | An employer or client default organization (YourCause, CGDS), or a charity the processor chooses (PPGF, Goodstack, For Good, Benevity), usually one in a similar cause area |
| Fee withheld from grant | None recorded | 0% (BBGF, PPGF enrolled, Every.org via Stripe or PayPal) up to 5% (CGDS international). Card and check fees come on top |

**Reading.** The sponsor rows describe one donor, one grant and one charity, and when a payment fails the money stays with the donor's account. The processor rules describe pooled employee or platform money paid out in batches. When a payment fails, the processor or the employer decides where the money goes. That difference is why several processor complaints come from donors who are surprised by the result (-001, -034) rather than by a delay.

---

## 5. Link to complaint findings

### 5.1 The seven records named in the brief
| Record | Complaint (paraphrase) | Governing rule (CSV row) | Fit |
|---|---|---|---|
| CMP-G1913-001 | A $75 gift (June 2026) held until a February 2027 payout because the charity was below the check threshold | $100 check threshold with an annual sweep (BEN-01); check fee (BEN-07) | **full** |
| CMP-G1913-006 | Monthly matched-gift payouts held for months at the intermediary's discretion | "whether and when" discretion clause (BEN-02); thresholds (BEN-01) | partial |
| CMP-G1913-009 | Funds arrived after about 3 months against a two-month ETA | Typical payment in the month after receipt, with exceptions (BEN-02) | partial |
| CMP-G1913-018 | Monthly payouts became bi- and tri-monthly | Threshold accumulation, if the charity was check-paid (BEN-01); discretion (BEN-02) | partial |
| CMP-G1913-027 | Gifts marked "completed" undelivered for 14 months; unexpected fees | No written rule predicts 14 months; fees are in the schedule (BEN-06) | **not explained** (timing); partial (fees) |
| CMP-G1913-034 | Returned check; no reissue without registration; gift redirected to an employer-chosen charity | Suspension and registration-before-reissue (YC-03, YC-04); SFA redirection (YC-05) | **full** |
| CMP-G1913-037 | Compliance documents unreviewed; automated timeout closed the account and blocked disbursement | "as long as You satisfy ForGood's legal requirements"; suspension "for any other reason" (NFG-04). No timeout rule was found | partial |

### 5.2 Other additions-file records the rules bear on
- **Partly explained:** -036 (Blackbaud check not reissued after about three months). Reissue eligibility starts at 45 days and the replacement takes 60–90 days (YC-03), so the rule permits the wait but does not predict it, and the record's YourCause attribution is inferred [V wave 33A]
- **Partly explained:**
  - -019: held pending information (Benevity's paused-disbursement rule, BEN-04).
  - -021: registration refused for 3 months, against a typical review of 30 days (BEN-04).
  - -007 and -012: EFT verification (BEN-04).
  - -035: a Blackbaud account problem (YC-04).
  - -038: EFT enrolment taking 6 months, against a stated "up to 8 weeks" (NFG-04).
  - -040: duplicate of -037.
  - -041: $6,400 held since 2024 over a tax issue. The rules allow a re-grant but set no maximum hold (NFG-05).
  - -043: monthly checks four months late. The cadence fits (NFG-02), but the 45-day reissue is not a written For Good rule (NFG-03).
- **Unverified:** -039. Under today's $9.51 minimum and 12-month backstop (NFG-01, terms of 2026-09-01) a $50 balance should be paid within a year. The record is from 2024-07-01, the rule then in force was not read, and the re-grant clause (NFG-05) fits "went to another entity" [V wave 33A]
- **Unverified:** -002 (a 180-day void with no reissue). The Benevity void rule could not be read (BEN-03).
- **Not explained:** -010, -016 and -020 (Benevity funds shown as due or sent but not received). No rule addresses them.

### 5.3 Count over all 14 grant-delay records in the additions file
| Fit | Records | n |
|---|---|---|
| full | -001 | 1 |
| partial | -006, -009, -018, -019, -037, -040, -041, -043 | 8 |
| not explained | -010, -016, -020, -027 | 4 |
| unverified | -039 | 1 | [V wave 33A]

These are the 9 Benevity and 5 Network for Good grant-delay records; the counts come from the additions CSV's `category` field.

**Implication for "policy (structural) vs operations (fixable)".**
- The two clearest cases (-001 and -034) are policy. The gap19 note coded -001 as fixable; on this evidence it is a structural threshold rule.
- The "partial" group is mostly discretion clauses. They make delay permissible without making it predictable.
- The not-explained records (4 of 14) are operational failures measured against the processors' current written rules; -039 needs the 2024 rule text [V wave 33A]

---

## 6. Limits

- **Blocked pages.** The Benevity Causes help centre (403) is where Benevity's void period and reissue rules would normally sit. PayPal's Nonprofit Certification Policy and Donor Terms (403) were not read either. Rows that depend on them are marked `unverified` or `read; ... blocked`.
- **Retired help centre.** Network for Good's help articles return 404. The For Good rows rest on terms, disclosures and an FAQ, which may leave out operating rules such as compliance windows.
- **Rules can be overridden.** Benevity's schedule says client master agreements supersede it. YourCause and CGDS schedules and redirect targets are set per client. The CSV therefore records defaults, not the terms any given employer programme uses.
- **No dates on help-centre pages.** YourCause and For Good FAQ pages state no update date, so `http_last_modified` is only a server timestamp. Many YourCause pages share 2026-11-16, which looks like a site rebuild date rather than a content date.
- **Complaint fit is our judgement.** It rests on single-review paraphrases. 11 of the 14 grant-delay records predate the rule versions they are coded against (Benevity terms 2025-12-24, fee schedule 2026-10-01; For Good terms 2026-09-01); only -001, -037 and -040 come after them [V wave 33A] A "full" fit means the written rule would produce the reported outcome; it does not mean the account is verified.
- **Coverage.** There are no disbursement complaints about Dechomai, PPGF, CGDS, Every.org or Goodstack in the additions file, so their rules are documented here without being linked to any complaint.

---

## 7. Open questions
The details are in [`queue-proposals-g1913-04.csv`](../../data/mission-2026-11-14/queue-proposals-g1913-04.csv):
- -01: Benevity help-centre void and reissue text.
- -02: PPGF certification policy and terms.
- -03: For Good's successor help centre, and any hold rules.
- -04: an operator decision on robots.txt 4xx handling.
- -05: rule-fit coding for the full corpus.
- -06: quarterly policy-diff tracking.

---

## 8. Data dictionary: `processor-disbursement-rules-2026-11-19.csv`
| Column | Meaning |
|---|---|
| row_id | Stable identifier `<PROCESSOR>-<nn>` (BEN, YC, NFG, PPGF, DEC, CGDS, EVO, GSK) |
| processor | Brand the nonprofit or donor sees |
| disbursing_entity | The 501(c)(3) or fund that legally makes the grant, as named on the source page |
| rule_type | One of `payout_threshold`, `payout_cadence`, `undeliverable_gift`, `vetting_registration`, `redirection`, `fee_withheld` |
| rule_summary | Our paraphrase of the written rule |
| value | Headline number from the rule (blank if none is stated). Ranges are written as `a-b` |
| unit | Unit and qualifier for `value` |
| short_quote | Verbatim fragment of 25 words or fewer from `source_url`. Checked by script against the cached page text |
| source_url | Official page or PDF |
| page_stated_date | Date the page states about itself ("Last updated", "Effective Date", page datetime), or `not stated` |
| http_last_modified | Server Last-Modified header date at fetch, blank if not sent |
| retrieved | Fetch date (2026-11-19) |
| access_status | `read`; `read; not stated` (page read, rule absent); or `read; <page> blocked` |
| sponsor_comparison | The matching sponsor-side rule from sponsor-grant-payment-policies.csv, by rule_type |
| complaints_explained | CMP-G1913 record ids this rule bears on (semicolon-separated) |
| explanation_fit | `full`, `partial`, `not explained`, `contradicted`, `unverified`, `context`, `none in corpus` or `n/a`, as defined in §2.1 |
| notes | Caveats, inconsistencies, second-hand values |

---

## 9. Source register
| # | Processor | Document | Stated date | URL |
|---|---|---|---|---|
| S1 | Benevity/AOGF | Foundations Fees Schedule | 2026-10-01 | https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf |
| S2 | Benevity/AOGF | End User Terms of Use | 2025-12-24 | https://benevity.com/legal/end-user-terms-of-use |
| S3 | Benevity | Nonprofit Eligibility and Guidelines | not stated (LM 2026-11-18) | https://benevity.com/nonprofit-eligibility |
| S4 | Benevity | How to Register Your Nonprofit on the Benevity Causes Portal | not stated (LM 2026-03-06) | https://go.benevity.com/hubfs/website/npo/How-to-Register-Your-Nonprofit-on-the-Benevity-Causes-Portal.pdf |
| S5 | Benevity Causes | Help-centre article (blocked, 403) | — | https://causeshelp.benevity.org/hc/en-us/articles/360001149426-What-charitable-foundations-does-Benevity-work-with-granting-disbursing-entities |
| S6 | Benevity Causes | Causes Terms of Use (shell page; text not fetched, §2.2) | — | https://causes.benevity.org/terms-of-use |
| S7 | YourCause/BBGF | Check Reissues | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-giving-check-reissues.html |
| S8 | YourCause/BBGF | Email 94, returned payment | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-email-94.html |
| S9 | YourCause/BBGF | Email 92, outstanding donations | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-email-92.html |
| S10 | YourCause/BBGF | How Stranded Funds Automation Works | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/csrconnect-prod/content/csrc-sfa-redirects.html |
| S11 | YourCause/BBGF | Stranded Funds Automation | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/csrconnect-prod/content/give-stranded-funds-automation.html |
| S12 | YourCause/BBGF | SFA FAQ (QA copy) | LM 2026-10-14 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/csrconnect-qa/content/give-stranded-funds-faq.html |
| S13 | YourCause/BBGF | About Payment Status | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-giving-about-payment-statuses.html |
| S14 | YourCause/BBGF | What Do I Need to Do to Receive Donations? | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-faq-how-to-receive-donations.html |
| S15 | YourCause/BBGF | Pending Disbursement Timeline | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-faq-when-will-pending-donations-be-processed.html |
| S16 | YourCause/BBGF | Set Up ACH Direct Deposit | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-disbursement-ach-direct-deposit.html |
| S17 | YourCause/BBGF | Become a Nonprofit Administrator | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-registration.html |
| S18 | BBGF | Frequently Asked Questions (CSRconnect help) | LM 2026-11-16 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/csrconnect-prod/content/the-blackbaud-giving-fund-frequently-asked-questions.html |
| S19 | BBGF | FAQ (blackbaudgivingfund.org) | modified 2026-03-05 | https://blackbaudgivingfund.org/about/frequently-asked-questions/ |
| S20 | For Good | Terms & Conditions | 2026-09-01 | https://www.forgood.org/legal-pages/terms-conditions |
| S21 | For Good | Charitable Solicitation Disclosures (same text on networkforgood.com and bonterratech.com) | 2026-09-01 | https://www.forgood.org/legal-pages/charitable-solicitation-disclosures |
| S22 | For Good | FAQ | not stated (LM 2026-11-16) | https://www.forgood.org/faq |
| S23 | PPGF | Donation Delivery Policy | 2025-01-01 | https://www.paypalobjects.com/marketing/web25/us/paypal-giving-fund/policy-updates/ppgf-us-delivery-01012025.pdf |
| S24 | PPGF | Donation Delivery Policy (prior version) | 2022-03-15 | https://www.paypalobjects.com/marketing/web25/us/paypal-giving-fund/policy-updates/ppgf-us-delivery-03152022.pdf |
| S25 | PPGF | Nonprofit Certification Policy (blocked, 403) | — | https://www.paypal.com/us/paypal-giving-fund/policies/nonprofit-certification-policy |
| S26 | Dechomai | Policies and Procedures | modified 2024-04-07 | https://dechomai.org/policies-and-procedures/ |
| S27 | Dechomai | FAQs | not stated | https://dechomai.org/faqs/ |
| S28 | CyberGrants | Overview of CGDS (training deck) | upload 2025-01 | https://bonterratech.com/wp-content/uploads/2025/01/6.-Overview-of-CGDS.pdf |
| S29 | CyberGrants | Understanding CGDS (training deck) | upload 2025-03 | https://bonterratech.com/wp-content/uploads/2025/03/Understanding-CGDS.pdf |
| S30 | CyberGrants | Status incident: CGDS Grant Payment Delays | 2026-01-20 to 2026-02-04 | https://status.bonterratech.com/incidents/5wmc2dgmxdsj |
| S31 | Every.org | Disbursements overview | 2026-10-23 | https://support.every.org/hc/en-us/articles/360061887233-Disbursements-overview |
| S32 | Goodstack | Donation Delivery Policy | 2024-11-15 | https://goodstack.org/legal/donation-delivery-policy |
| S33 | Goodstack | Undeliverable Donation Policy | 2024-11-15 | https://goodstack.org/legal/undeliverable-donation-policy |
| S34 | Goodstack | Global Charity Donation Terms | 2026-06-22 | https://goodstack.org/legal/global-charity-donation-terms |
| S35 | Network for Good | Retired help centre (404 on all article URLs) | — | https://intercom.help/networkforgood/en/ |

LM = HTTP Last-Modified header.
