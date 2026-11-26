# P-B4428-04: Bank of America Charitable Gift Fund, program terms vs portal guide

Task ID: b4428-04. Retrieved 2026-11-20. Queue item: P-B4428-04 (rank 87, `research-priority-queue.csv`).

## 1. Answer

| Question | Answer | Confidence |
|---|---|---|
| **Is there a newer Program Guidelines that resolves the conflict?** | **A newer version exists, and it does not resolve the conflict.**<br>- **Version 8.2025** of the Program Guidelines is served on the DonorFirst portal at `/pdf/bofa/CGF Program Guidelines.pdf` (PDF dated 2025-09-08).<br>- It keeps the 2024 sentence word for word: "Distributions are accompanied by information specifying the account name and the name of the Donor or Advisor, unless anonymity is requested."<br>- `bankofamerica.com/philanthropic/` serves only `Program_Guidelines_2024.pdf` (Version 3.2024). The 2021, 2022, 2023, 2025 and 2026 filenames return 404. | High (both PDFs read; the 8.2025 text is OCR) |
| **Which document governs?** | **The Program Guidelines.** They state "The following Guidelines govern the Bank of America Charitable Gift Fund and donor-advised funds established with the Charitable Gift Fund, including the handling of ... grant recommendations". Only the Trust Document ranks above them. The portal guide has no governing language, and it lists "CGF Program Guidelines" among the donor forms. | High (text) |
| **What does a charity receive, on paper?** | Under the governing text:<br>- a check "bearing the name of Bank of America Charitable Gift Fund";<br>- the **account (fund) name**;<br>- the **name of the Donor or Advisor**;<br>- no address or email;<br>- anonymity only if the donor asks for it. | High (text) |
| **What does the grant screen send by default?** | Under the portal guide (PDF modified 2026-02-23):<br>- the acknowledgement "will be displayed on the check";<br>- "The default is Fund Name Only";<br>- the donor can choose "Remain Anonymous" or a saved custom acknowledgement, which may include names and a street address. | High (text). What actually gets printed is **not observed** |
| **Net reading** | **The conflict is real and current. Both documents agree on the fund name, opt-in anonymity and no default address. They disagree on the donor/advisor name.** The governing terms promise it; the screen the donor uses does not add it by default. | Medium |
| **Effect on the repo's coding** | - BofA rank 11 holds $4.73bn, 1.89% of top-20 assets (`donor-info-defaults-top20-2026-11-19.csv`).<br>- Under b44n28-01's rule, the newest document that describes the donor's screen wins, so the default stays **"fund name only"**, now at **medium** confidence.<br>- The governing-text reading is "name only" (fund plus donor/advisor).<br>- Both readings withhold address and email, so the 17.2% withheld share does not change (as V34A-30 found). Only the split between name only and fund name only moves. | High arithmetic |

## 2. Method

1. **Queue text.** Read from `data/mission-2026-11-14/research-priority-queue.csv` (P-B4428-04). It asks for the 2024 Program Guidelines to be reconciled with the 2025-26 portal guide ("The default is Fund Name Only"), using any newer Program Guidelines PDF on bankofamerica.com.
2. **Repo context.** Ran `grep -ril "Charitable Gift Fund|donorfirst"` over `research/` and `data/`. Read the BofA passages in:
   - b44n28-01 (§3, S21–S22);
   - b4428-02 (BOA-01, §3.2);
   - b4013-02 (S18);
   - b4013-b4428 (row 9);
   - validation waves 34A (V34A-30), 35B (V35B-12) and 36C;
   - `bofa-charitable-gift-fund-10k-ren-relationship-2026-11-11.md`.
   No earlier file cites Version 8.2025 or the portal path for the guidelines.
3. **Robots.txt.** Checked every host before fetching. The user agent was `research-script/1.0` throughout.

| Host | robots.txt | Claude/Anthropic group? | Result |
|---|---|---|---|
| bofa.donorfirst.org | 404 (no file) | n/a | fetched |
| www.bankofamerica.com | 200 | No; `*` disallows /global, /signin, /deposits/*.pdf and similar, not /philanthropic | fetched |
| privatebank.bankofamerica.com → www.privatebank.bankofamerica.com | 301 → 200 | No; `*` disallows `*.pdf` and some paths | HTML only. No PDFs requested. One article returned **403** (see Limits) |
| business.bankofamerica.com | 200 | No | not needed |
| web.archive.org | **no response** (status 000, twice) | unknown | **not fetched** (P-B442804-04) |

   No host's terms forbidding automated extraction were met. The Ren DonorFirst Terms of Service PDF has no scraping clause (grep "automat|scrap|crawl|robot|harvest").
4. **Discovery.**
   - Read the portal root (`bofa.donorfirst.org/`) for linked PDFs. It links the guide, *Making the Most of your CGF Account*, *CGF Outside Asset Transfer Instructions* and the Terms of Service.
   - Probed `Program_Guidelines_<year>.pdf` for 2021–2026 and four other filenames on www.bankofamerica.com/philanthropic/. Only 2024 returned 200.
   - The guide's form list names "CGF Program Guidelines", so the same name was probed under `/pdf/bofa/` and `/pdf/BOFA/` on the portal. Both returned the same file (SHA-1 `eda15c55…`). The portal root does not link it publicly; it was found by URL probe.
   - Read the Private Bank sitemap entries for charitable pages, and the BofA philanthropic overview, gift-fund overview, FAQ and resources pages.
5. **Text extraction.**
   - The 2024 guidelines and the guide were read with `pdftotext -layout`.
   - The 8.2025 guidelines and *Making the Most* have font-encoded text layers. They were rendered with `pdftoppm` (300 dpi for the guidelines, 200 dpi for *Making the Most*) and OCR'd with `tesseract`.
   - Version 3.2024 and Version 8.2025 were compared word by word (`difflib`; similarity 0.986). The only substantive changes are in the description of the principal-preservation investment objective, plus "faxed" becoming "mailed or" on one line. The grant-distribution, anonymity and modification passages are unchanged.
6. No logins, forms or outreach. Nothing behind the portal login was seen.

## 3. The conflicting passages (verbatim)

**A. Program Guidelines, Version 3.2024.**
- URL: https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf
- Dates: PDF created 2024-06-05, modified 2024-09-18; server Last-Modified 2024-10-22.
- p.3, "Grant Distributions and Confirmations": "Grants are issued via checks bearing the name of Bank of America Charitable Gift Fund. Checks will only be delivered directly to the legal mailing address for the recipient charity via the United States Postal Service first class mail. Distributions are accompanied by information specifying the account name and the name of the Donor or Advisor, unless anonymity is requested."
- p.3, "Anonymous Grants": "Donors and Advisors may request that any grant be made anonymously. In such cases, both the Donors and Advisor names and the name of the donor-advised fund can remain anonymous."

**B. Program Guidelines, Version 8.2025 (newer; OCR).**
- URL: https://bofa.donorfirst.org/pdf/bofa/CGF%20Program%20Guidelines.pdf
- Dates: PDF created and modified 2025-09-08; server Last-Modified 2025-09-08 20:27:35 GMT.
- p.3: the same two passages, word for word, including "Distributions are accompanied by information specifying the account name and the name of the Donor or Advisor, unless anonymity is requested."
- p.7, "Modification": "In the event of any inconsistency between the terms of these Program Guidelines and the Trust Document, the terms of the Trust Document will govern. ... All modifications to the Trust Document or the Program Guidelines will govern both existing and new donor-advised fund accounts. The Charitable Gift Fund is currently administered by Bank of America Private Bank."

**C. Guide to Navigating Your Donor Advised Fund (portal guide).**
- URL: https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf
- Dates: PDF created 2025-11-14, modified 2026-02-23; server Last-Modified 2026-02-26.
- p.23, "Recommend a Grant - Acknowledgements": "Acknowledgement (to whom the charity might want to write a thank you note) • This will be displayed on the check • You can select to Remain Anonymous • You can create and save custom acknowledgements • The default is Fund Name Only".
  - The screenshot callout reads "Fund name will appear here".
  - The sample custom acknowledgements show two personal names and a street address (example data).
- p.20, "Recommend a Grant – Details": "Default lists just the Fund Name with the grant, e.g. “My DAF”". This is a callout split across lines in the PDF.
- p.34, "Donor Resources - Forms": "Available forms include: ... CGF Program Guidelines ...".

**D. Supporting first-party pages (live 2026-11-20).**
- BofA gift-fund overview (https://www.bankofamerica.com/philanthropic/gift-fund-overview/): "Personalize your account name. Make anonymous grant recommendations to protect your privacy."
- Private Bank DAF page (https://www.privatebank.bankofamerica.com/solutions/donor-advised-fund.html): "Receive recognition for your donations or maintain anonymity to protect your privacy".
- *Making the Most of your CGF Account* (portal PDF, 2025-09-08; OCR): no acknowledgement text. It says the fund "sends all grant checks via USPS first class mail directly to the legal address of the receiving charity."

## 4. Which governs, and what the charity gets

- **Hierarchy (from the documents' own text):** Trust Document > Program Guidelines > everything else.
  - The guidelines say they "govern" grant recommendations, and that modifications to them "govern both existing and new donor-advised fund accounts".
  - The portal guide is a 38-page slide walkthrough with no governing language, and it points donors to the guidelines.
  - Nothing in the guide claims to change the guidelines. The guidelines have not been revised to match the guide: Version 8.2025 predates the guide's creation (2025-11-14) by about two months.
- **Points of agreement:**
  - The check is drawn in the name of Bank of America Charitable Gift Fund and mailed to the charity's legal address.
  - The fund (account) name is shown by default.
  - Anonymity is opt-in and can hide both the donor/advisor names and the fund name.
  - Neither document sends the donor's address or email by default. In the guide, an address reaches the charity only through a custom acknowledgement.
- **Point of conflict:** whether the **donor/advisor name** goes with the grant by default.
  - Guidelines: yes ("the name of the Donor or Advisor, unless anonymity is requested").
  - Guide: no ("The default is Fund Name Only").
- **Can they be read together?** Only partly, and only by inference [I]:
  - The guidelines' "information specifying the account name and the name of the Donor or Advisor" could be met if the account name contains the donor's name. The overview invites donors to "Personalize your account name".
  - It could also be met if a separate grant notice, not the check acknowledgement field, carries the advisor name. The guide says only that the acknowledgement "will be displayed on the check". It does not describe any separate charity-facing letter.
  - Neither reading is shown by a document, so the conflict is recorded as unresolved, not reconciled.
- **Practical answer:**
  - A charity is *entitled under the governing terms* to the fund name plus the donor/advisor name unless the donor opts for anonymity.
  - The *screen default the donor sees* puts only the fund name on the check.
  - Which one describes the printed check is not observed in any 2021+ public source found here (P-B442804-01).

## 5. Implications for repo files (proposals only; no existing file edited)

- `donor-info-defaults-top20-2026-11-19.csv`, rank 11: keep `default_bucket = fund name only`, but add to the detail field: "Program Guidelines Version 8.2025 (2025-09-08) still say account name and Donor or Advisor name unless anonymity is requested; coded by screen per newest-donor-screen rule; medium confidence (P-B4428-04)".
- b44n28-01 §6 ("BofA's two documents conflict; the newer portal guide was used"). Suggested replacement: "BofA's governing Program Guidelines (Version 8.2025, September 2025) name the account and the donor or advisor; its portal guide (February 2026) defaults the check acknowledgement to the fund name only. The screen default is used; both withhold address and email (b4428-04)."
- b4428-02 BOA-01 and S16: cite Version 8.2025 at the portal path as well as Version 3.2024.
- The same policy-text vs screen-default split appears at RCF (circulars vs the 2023–24 guide). A separate `policy_text_bucket` column would stop a single code from hiding it (P-B442804-02).

## 6. Limits

- **Charity-side output not observed.** No 2021+ check image, stub description or charity statement for BofA CGF was found. Both readings are documentary.
- **OCR.** The Version 8.2025 quotes come from OCR of a font-encoded PDF. They were checked by eye against the 2024 text layer and matched word for word, but small OCR errors elsewhere in that file are possible. The diff noise ("40f", "i e.") is OCR.
- **Version history.** Only Versions 3.2024 and 8.2025 were read. web.archive.org did not respond, so earlier versions and earlier guides were not checked (P-B442804-04). "8.2025" may mean August 2025, but that is not stated.
- **Discovery by probe.** The 8.2025 PDF was found by guessing the path from the form name in the guide. It is not linked from the public portal root and may be linked only behind login.
- **Blocked page.** https://www.privatebank.bankofamerica.com/articles/the-bank-of-america-charitable-gift-fund.html returned HTTP 403 to the script client. It is robots-allowed. The user agent was not changed, and the page was not read (P-B442804-05).
- **Trust Document.** It ranks above the guidelines but is not public, so it was not read.
- **Screen vs print.** The guide is a 2025-26 walkthrough with example screenshots. The live screen behind login, and any per-account override, were not seen.

## 7. Data dictionary: `data/mission-2026-11-14/bofa-cgf-conflict-2026-11-20.csv`

There are 12 rows, one per quoted passage.

| Column | Meaning |
|---|---|
| `row_id` | BCC-01 … BCC-12 |
| `document` | Document title and where it is hosted |
| `version` | Version label printed in the document, or a format note |
| `url` | Primary URL fetched |
| `robots_status` | robots.txt result for that host and path |
| `http_status` | HTTP status of the fetch on 2026-11-20 |
| `pdf_created_utc`, `pdf_modified_utc` | PDF metadata dates (`pdfinfo`); blank for HTML |
| `server_last_modified_gmt` | HTTP Last-Modified header; blank where not sent |
| `sha1` | SHA-1 of the downloaded file |
| `text_method` | pdftotext, OCR or HTML text |
| `document_role` | Governing program terms, portal how-to, marketing page or portal FAQ |
| `passage_topic` | What the passage covers |
| `verbatim_quote` | The passage as printed. Bullets are joined with " • " where the PDF lays them out as a list |
| `fund_name_to_charity`, `donor_name_to_charity`, `address_to_charity` | What the passage implies reaches the charity by default; blank if the passage does not address it |
| `anonymity` | How anonymity works under that passage |
| `retrieved` | Retrieval date |

## 8. Source register

| ID | Source | Date | URL |
|---|---|---|---|
| S1 | BofA CGF Program Guidelines, Version 3.2024 | PDF 2024-06-05 / 2024-09-18; server 2024-10-22 | https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf |
| S2 | BofA CGF Program Guidelines, Version 8.2025 (portal copy; same file at /pdf/BOFA/) | PDF 2025-09-08; server 2025-09-08 | https://bofa.donorfirst.org/pdf/bofa/CGF%20Program%20Guidelines.pdf |
| S3 | BofA CGF Guide to Navigating Your Donor Advised Fund | PDF 2025-11-14 / 2026-02-23; server 2026-02-26 | https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf |
| S4 | Making the Most of your CGF Account | PDF 2025-09-08 | https://bofa.donorfirst.org/pdf/bofa/Making%20the%20Most%20of%20your%20CGF%20Account.pdf |
| S5 | BofA DonorFirst portal root (PDF links) | live 2026-11-20 | https://bofa.donorfirst.org/ |
| S6 | DonorFirst Terms of Service (checked for scraping terms) | PDF 2025-05-20; server 2026-02-10 | https://bofa.donorfirst.org/Terms%20of%20Service.pdf |
| S7 | BofA Philanthropic Solutions, Charitable Gift Fund overview | live 2026-11-20 | https://www.bankofamerica.com/philanthropic/gift-fund-overview/ |
| S8 | BofA Private Bank, Donor-advised fund | live 2026-11-20 | https://www.privatebank.bankofamerica.com/solutions/donor-advised-fund.html |
| S9 | Repo: top-20 donor-info defaults (BofA row 11; $4,733,931,424; share 0.0189) | 2026-11-19 | data/mission-2026-11-14/donor-info-defaults-top20-2026-11-19.csv |
| S10 | Repo: V34A-30 BofA conflict validation | 2026-11-19 | data/mission-2026-11-14/validation-register-wave34a.csv |
| S11 | Repo: b44n28-01 and b4428-02 BofA coding | 2026-11-19 | research/mission-2026-11-14/b44n28-01-donor-info-defaults.md; research/mission-2026-11-14/b4428-02-ren-private-label-defaults.md |

Queue proposals: `data/mission-2026-11-14/queue-proposals-b4428-04.csv` (5 rows).
