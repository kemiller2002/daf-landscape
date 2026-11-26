# 02 — Industry evidence catalog: how information enters DAF sponsors

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26). Evidence ids `FIE-*` resolve in [`data/file-ingestion-2026-11/evidence.csv`](../../data/file-ingestion-2026-11/evidence.csv). Classification: **CONFIRMED** (public source), **INFERRED** (reasoned from confirmed facts), **PROPOSED** (innovation, not observed practice). Sites that block automated readers (DAFgiving360, Goldman Sachs Philanthropy Fund, Foundant, NPact documentation) are evidenced from search snippets only and flagged in the evidence notes. No private file specification was obtained or inferred.

## 1. Per-organisation narratives

### 1.1 Fidelity Charitable (FIE-A-001 to 023)

**Inbound channels.** Fidelity Charitable documents the most complete set of inbound channels of any sponsor.
- **Securities from outside firms:** DTC delivery to DTC 0226, account Z97-000442, "FBO" the Giving Account number (001).
  - An advisor who delivers must then notify Fidelity Charitable, through GivingCentral or the Contribution Form (002). This is Fidelity's "notify us of an incoming gift" step.
  - Alternatively, Fidelity Charitable pulls the assets with a pre-filled Letter of Instruction plus a copy of the donor's latest statement (003).
- **Wires:** to JPMorgan Chase for NFS, FBO Fidelity Charitable, with the memo "CGF#" plus the account number. Fidelity Charitable "does not initiate wires", and a wire "will be rejected if necessary account numbers are not provided" (005). This is the only published control for unidentified wires that we found: **rejection, not a holding account**.
- **Checks:** to a Cincinnati P.O. Box, or to Covington, KY for overnight delivery (006). The repo's geography note treats these as lockbox addresses [INFERRED].
- **EFT:** 1–3 business days (007).
- **Paper:** scanned forms go into GivingCentral "Document Upload", which issues a work-item number immediately. Fax and mail are also published (008). [INFERRED] A work item implies a human processing queue.

**Posting times (CONFIRMED, contribution-timelines page).**

| Asset | Time to transfer | Time to process once received |
|---|---|---|
| Fidelity-held stock | Same day if instructions arrive 15 minutes before market close | — |
| Outside stock | About 2 weeks | 1 business day |
| Outside mutual funds | 4–6 weeks | 1 business day |
| Checks | — | 1 business day |
| Crypto | Varies | — |
| Non-public assets | Varies | — |

**Controls.**
- The **Complex Asset Contribution Form** (010, text extracted; 2025 edition):
  - Trustees must approve every contribution, and none is complete until accepted.
  - The donor certifies ownership and that there is no obligation to sell.
  - The donor obtains the qualified appraisal and files Form 8283; Fidelity Charitable "will not agree to any valuation".
  - Fidelity Charitable files Form 8282 if it sells within 3 years.
  - Costs are recovered, and UBIT is held in an "Escrow Giving Account".
- Restricted stock uses a separate 144/145 form (009).
- **Crypto** runs through a Letter of Understanding and a unique wallet address per gift. The gift is complete only on delivery and acceptance, and Fidelity Charitable gives no fair market value (012).
- **Complex-asset volume** (repo): $2.6bn in 2025, about 500 gifts a year, and 65 days on average from acceptance to liquidity (011).

**Grants.**
- **Recommendations** come in online, by app, by phone or on paper. They can be one-time, future-dated or recurring (014).
  - Advisors in GivingCentral face limits: amounts in $5/$18 increments only, and no full-balance grants.
  - The app can grant "from a list of previously supported organizations". **No bulk grant upload or multi-client advisor function is documented** (022).
- **Review** uses "IRS databases", litigation records, news, and information from donors and grantees. Pub 78, the BMF and auto-revocation are not named (015).
- **Review time** is "10 or more business days" (016).
- **EFT enrolment and remittance** (017, repo):
  - Charities enrol in EFT by PDF form; the ACH queue runs up to 4 weeks.
  - A daily emailed Grant Details Report goes to up to 5 contacts, and a shared inbox is not accepted.
- **Returned grants** (018): checks not cashed within 90 days come back to the Giving Account, and are reissued only if the donor asks.

**Succession.** A copy of the death certificate is faxed in (019).

**Platform.** FMR provides record-keeping, and no third-party DAF platform is visible (021).

### 1.2 National Philanthropic Trust (024–036)

The August 2026 *Funding & Transfer Instructions* PDF (text extracted) gives the clearest public statement of the intake architecture:
- **Notify first.** "Step 1: Notify NPT by submitting a Contribution Agreement", online through GivingPoint or on paper by mail, email or fax.
- **Pooled receipt.** All assets go to "the contribution receipt account owned by NPT" and are "then posted by NPT to the individual donor's DAF account". This is pooled receipt followed by attribution.

Channels:
- Securities: DTC 0221 at UBS. Mutual funds take 4–6 weeks.
- Wires: to UBS, FFC NPT.
- Checks: to a **Bank of America lockbox in Chicago**, with the DAF name and account number on the memo.
- Credit card: 3% fee.
- **No ACH.**
- Physical certificates: sent with a stock power carrying a **medallion guarantee**, mailed under separate cover.
- LOI originals go to the sending custodian, "not to NPT".
- Restricted stock, crypto and alternatives: by phone, with a crypto specialist available.

Controls (from the Contribution Agreement snippet):
- The registered owner and account number are required for each asset.
- The form asks about insider and restricted status.
- NPT "seeks to verify the identity of each person who makes a contribution".

Illiquid assets:
- Diligence takes 2–8 weeks or more.
- NPT charges a cost-based gift processing fee.
- Real estate needs a $25k good-faith deposit, local counsel and a title company, and the property goes into an NPT-owned LLC (033).

Grants:
- Domestic grants clear in 5 business days or less; international grants take up to 8 weeks.
- Payment is by PayPal Grant Payments. An unaccepted grant expires after 14 days and goes out as a check. Grants of $250k or more go by wire (035).

Platform: Ren GivingPoint (036). [INFERRED] Program-specific LOAs (for example BMO) mean several receipt accounts, so one more identifier must be matched.

### 1.3 DAFgiving360 (037–042)

Evidence comes only from search snippets (site blocked).
- **Transfer of Assets form** for non-Schwab or transfer-agent assets:
  - one form for each sending institution;
  - transfer-agent transfers must use this form;
  - Schwab DTC 0164;
  - "typically two to six business days";
  - assets must be "approved by DAFgiving360 and transferred thereto by December 31".
- **Grants:** checks mailed within 7–10 business days (2024 Program Policies, repo) (038).
- **Charity eligibility:** checked against "the IRS and other federal and state regulators". A charity not in the database is researched on request. A temporary-suspension list covers indicted or convicted charities (039).
- **Crypto:** the qualified-appraisal rule above $5,000 is stated (040).
- **Dechomai:** DAFgiving360's grants to Dechomai suggest complex assets are outsourced [INFERRED] (041).

### 1.4 American Endowment Foundation (043–048): migration evidence

The AEF move to Ren gives the best public view of what a DAF replatforming carries over:
- **Announcement:** a press release dated 2026-04-08.
- **Blackout:** 23 March to 6 April 2026.
- **Contributions** were "received and processed during this period without disruption".
- **Recurring recommendations** carried over.
- **Grant history:** only 2024–2026 is visible on the new platform. Older history stays in DonorCentral.
- **New accounts:** advisors could not submit them through Partner Gateway for two weeks.

AEF also:
- launched charity ACH in 2026 through Ren's charity portal, paying by check until a charity is verified (046);
- refers illiquid gifts to Dechomai (047).

### 1.5 Ren / iPhi (049–058)

Ren's *Product Descriptions* (2023-06-12, text extracted) is the only primary document that lists a DAF administrator's intake duties:
- "Receipt letter for contribution";
- "Grant vetting for each grant recommendation" → "Submit vetted grant for staff approval/denial";
- "Monitor receiving and disbursement account for grants and contributions".

It also lists one-time **Data Migration** ("existing accounts and transaction history"), **API Integration Services**, **SSO** and **Cryptocurrency Acceptance** (049–051). **No file specifications are public.** We did not invent them.

Other Ren facts:
- **Charity side:** Ren for Charities offers ACH enrolment covering "25+ donor-advised fund programs at once", and a grants report keyed by Grant ID with a CSV export (053).
- **Attrition:** 6 of 57 iPhi sponsors left between 2023 and 2026, four of them community foundations that moved to Foundant (054).
- **Edward Jones CGF on DFX:** the advisor adds the client, enters the opening contribution and chooses pools, but "the contribution step alone does not start the asset transfer". That is a documented gap between the stated intent and the actual transfer (056).
- **No public Ren bulk-grant or roster-upload documentation** was found (055).

### 1.6 Vanguard Charitable, BofA CGF, Morgan Stanley GIFT, Goldman Sachs Philanthropy Fund (059–070)

**Vanguard Charitable**
- Grants are processed "within a few days" and paid through PayPal (059).
- The contribution-side DTC and notification page **was not found**. The only description of its contribution form is third-party: an account-number section, and a medallion guarantee that "may be" needed [INFERRED, low confidence] (060–061).

**BofA CGF** (2024 guidelines)
- A Donor Application must come with the first contribution.
- New donors "may require additional time".
- Securities are sold the business day after receipt, or once "paperwork in good order" is in.
- Low-priced shares and fractional shares are not accepted.
- The receipt is available only when the proceeds post (062–064).

**MS GIFT**
- Illiquid gifts need prior approval (066).
- When names differ, donors are asked to confirm the recipient's identity, and grants go to the recipient's legal address (067).
- Payment is by ACH through Ren, with a letter (068).

**Goldman Sachs Philanthropy Fund:** robots block. Only secondary grant rules were found (070).

### 1.7 Greater Horizons / GKCCF (071–078)

GKCCF documents a **gate**: donors complete an online check, ACH/wire or securities form, and only then receive transfer details.
- Gifts post in 3–5 business days.
- Mutual funds and unique assets are handled by email.

For **advisor-managed** DAFs:
- Any custodian may be used. The foundation signs the custodian's account forms as owner, under its own tax ID.
- The advisor emails the foundation when a transfer starts.
- Balances are reconciled **monthly**, and the portal shows the prior month-end figure.
- Cash for grants moves by journal at Fidelity or Schwab, with about 2 days' notice, or otherwise by check, wire or ACH.

This is a clear example of custodial data arriving through manual reconciliation rather than a feed.

### 1.8 Independent sponsors: NCF, Daffy, Charityvest, DonorsTrust, The Signatry, TIFIN family (079–095)

- **NCF** is the only sponsor with a published **unidentified-gift policy**. Such gifts go to "a holding account until NCF can identify the giver and fund". If no giver is found, the gift goes to NCF's general fund (079, repo).
- **Daffy** refuses ACATS; only charitable DTC transfers are accepted (082). Its own pages disagree on timing:

  | Asset | Help center | FAQ |
  |---|---|---|
  | Stock | 1–2 days to 2+ weeks | 7–10 days |
  | Crypto | A few hours | 4–5 days |

- **Charityvest** shows each donor in-app DTC instructions (secondary source, 086).
- **DonorsTrust:** no intake form was found (088).
- **The Signatry** states that a notification form "does not initiate the transfer" (089).
- **TIFIN Give:**
  - It documents ACH via Plaid, wires, cards, securities, DAF-to-DAF transfers and complex gifts.
  - It claims "multi-custody support" and SSO.
  - It publishes no public API (090–091).
- **BlueGive / Give RIA**, sister TIFIN-family sponsors, document **bulk securities-contribution CSV uploads** and bulk attestations (093–094). These are the only DAF-sponsor bulk-upload features found.

### 1.9 Chariot (096–102) and PayPal (103)

- **Disbursements API:**
  - It searches organisations by name or EIN.
  - A verification request is used when an organisation is unlisted.
  - A disbursement waits in `awaiting_balance` until funded.
  - Bulk create is **atomic**, and requests carry an Idempotency-Key (096).
- **Eligibility database:** built from the IRS BMF, 990 filings, Pub 78 and OFAC. Exceptions, such as churches, need extra documents (097).
- **Claim window:** five business days with three reminder emails, then a check (098). Unclaimed DAFpay Network checks are voided after 90 days (101).
- **DAFpay:** Chariot submits the grant at the sponsor, handling credentials and MFA. "Some DAF providers do not pass the Tracking ID through" (099).
- **PayPal Grant Payments** puts the payment and the donor data in one dashboard (103).

### 1.10 Community-foundation software (104–112)

- **Foundant CommunitySuite** documents CSV template imports for grants (external and fund-to-fund) and for donations (104–105, snippets).
- A **Foundant community thread** confirms that unidentified stock gifts are a recurring CF problem, caused by donors reusing old DTC instructions. The practices reported (106) are:
  - asking donors to give notice before sending;
  - Donor Services alerting Finance;
  - a shared log of ticker, shares and notice date.
- **NPact FIMS/DonorCentral** imports grants by Fund ID or Fund Number, with a grant-type code such as "DA" (109).
- **CSuite:** no public intake documentation was found.
- **Kindsight** appears only as a fundraising-intelligence and AI vendor (112). Its role in DAF intake is **not evidenced**.

### 1.11 Corporate giving (113–119)

- **Benevity** publishes its payroll workflow (113–114):
  1. A deduction file is created each pay cycle and collected from Benevity's managed file transfer.
  2. Payroll (Workday, ADP or SAP) takes the deductions.
  3. The employer sends back a success file.
  4. Benevity runs a post-commit reconciliation report under a "date of intent" rule.
- **YourCause** runs the same two-file exchange over SFTP (116–117):
  - a deduction file from YourCause and an "actuals" file back from the employer;
  - PGP encryption, required for HR files;
  - an HR file that carries a Payroll ID;
  - a reconciliation tool for mismatches.
- **Specs:** field-level specifications are **not public** for either vendor.
- **Matching programs** vary in whether DAF grants qualify (119, repo).

### 1.12 Custodians (120–127)

- **Schwab** uses form APP39630 for in-kind gifts to outside charities (120).
- **Pershing:** charities publish DTC 0443 and ask donors for advance notice (121).
- **Vanguard Brokerage:** online gifts take 1–3 days; gifts to outside firms take 5–7 days (122).
- **Donor identity:** charity forms (for example the American Law Institute's, 2026-08) state that "donor information does not always transmit through the DTC wiring system". This is the root cause of unidentified gifts (123).
- **ACATS** is not the route for gifts (082). Interactive Brokers states the conditions for DTC/DWAC transfers (124).
- **LPL:** only the existence of an RCF LPL program circular was found (126).
- **Fidelity Wealthscape** submissions must carry a G Number (127).

---

## 2. Cross-organisation synthesis

1. **Intake is pooled receipt plus attribution, and the attribution key travels as free text.** This is CONFIRMED at Fidelity Charitable (FBO line) and NPT (FFC field and memo, "receipt account … then posted"). [INFERRED, 131] Every sponsor's unidentified-receipt work comes from that design.
2. **Sponsors manage unidentified receipts in three documented ways.** No major sponsor publishes a policy on unidentified stock gifts.

   | Approach | Who | Evidence |
   |---|---|---|
   | (a) Prevent | NPT, GKCCF, The Signatry; Fidelity Charitable for advisor deliveries | Notification before transfer |
   | (b) Reject | Fidelity Charitable | Wires without account numbers are rejected |
   | (c) Hold, then sweep | NCF | Holding account, then general fund |

   Practitioner evidence (Foundant forum; AASP threads in the repo) shows the problem persists.
3. **Posting times run from same-day to months.**

   | Asset | Time |
   |---|---|
   | Internal or same-custodian stock | Same day |
   | DTC from an outside firm | 2–6 business days (DAFgiving360) to about 2 weeks (Fidelity Charitable) |
   | Mutual funds | 4–6 weeks (Fidelity Charitable, NPT) |
   | Restricted stock | 4–6 weeks (NPT) |
   | Illiquid assets | 2–8+ weeks of diligence (NPT); 65 days on average to liquidity (Fidelity Charitable) |
   | Community-foundation posting | 3–5 business days (GKCCF) |

4. **Grant timing claims:**

   | Sponsor | Stated time |
   |---|---|
   | Vanguard Charitable | "a few days" |
   | TIFIN | 2–5 days |
   | NPT | ≤5 business days |
   | Daffy | Up to 1 week |
   | DAFgiving360 | 7–10 business days to mail |
   | Fidelity Charitable | "10 or more" business days |

5. **Paper, fax and PDF are still first-class channels** at the two largest sponsors (FIE-A-134). The controls are physical: medallion guarantees, wet signatures and statement copies.
6. **Bulk features sit in community-foundation software and TIFIN-family sponsors, not at the national sponsors.**
   - Foundant and NPact offer grant and donation CSV imports.
   - BlueGive and Give RIA offer bulk securities uploads.
   - Fidelity Charitable states it has no multi-client process. No bulk grant tool was found at Ren, NPT or DAFgiving360.
7. **Charity-side data is split between portals and rails.**
   - Fidelity Charitable: emailed report.
   - Ren: portal.
   - PayPal: dashboard.
   - Chariot: per-payer account numbers.

   No top-10 sponsor documents a grant ID in ACH addenda (repo).
8. **Use of IRS data:** only Chariot names the BMF, Pub 78 and OFAC. Sponsors say "IRS databases" (Fidelity Charitable) or "IRS and other federal and state regulators" (DAFgiving360).
9. **Migrations are partial.** AEF moved only 2024–2026 grant history and kept DonorCentral for older records. Ren sells migration as a one-time service and publishes no spec.
10. **Payroll-giving files are a mature, standardised exchange.** Deduction and actuals/success files move over SFTP or MFT with PGP. No DAF sponsor documents receiving such files; the corporate-to-DAF route goes through intermediary charities (AOGF, Bright Funds Foundation) [INFERRED from repo].

### What can be eliminated or redesigned

These are PROPOSED (FIE-A-135 to 142):
- Contribution intents with a unique reference carried in the DTC note, wire memo or a per-intent crypto address. This turns orphan matching into a residual.
- A structured incoming-securities notice: CUSIP, shares, sending DTC number and fund ID.
- Advisor bulk-grant CSV/API at national sponsors.
- Grant IDs in CCD+/CTX addenda or ISO 20022 RmtInf.
- Death-certificate extraction, with human review only of mismatches.
- Daily custodian feeds in place of monthly reconciliation.
- Full-history migration with control totals.
- A payroll-giving remittance schema.

---

## 3. Evidence gaps (honest list)

- **Unidentified stock-gift policies** at Fidelity Charitable, Vanguard Charitable, DAFgiving360, NPT, Morgan Stanley GIFT, BofA and Goldman: not published. NCF is the only sponsor with one.
- **Vanguard Charitable** contribution instructions, DTC number and notification form: not located.
- **DAFgiving360:** primary pages blocked; snippet evidence only. Its 2026 Program Policies were not read.
- **Goldman Sachs Philanthropy Fund:** robots block; essentially no primary evidence.
- **Ren:** no public API, migration file spec, bulk grant or roster upload documentation. The Edward Jones and RCF help articles now return 404.
- **Advisor portals with client-roster upload:** none documented at any national sponsor.
- **Successor and death processes:** only Fidelity Charitable's fax-the-death-certificate step is public. No sponsor lists letters testamentary or trust/entity documents for **account opening**. Fidelity Charitable's organisation application exists, but its contents were not read.
- **Fidelity Charitable crypto custodian** (Coinbase or other): not named publicly.
- **Benevity/YourCause file layouts:** private. The Benevity help page returned 403.
- **Bank verification method for charities** (Plaid, micro-deposits or bank letter) at Fidelity Charitable and Ren: method not public. Chariot cites KYB only.
- **LPL and Pershing DAF-specific intake:** not found.
- **CSuite and Kindsight:** no intake documentation.
- **Sponsor statements of using auto-revocation lists:** none found.
- **Greater Horizons vs GKCCF:** the mapping relies on a Charity Navigator description. GKCCF pages were used.
