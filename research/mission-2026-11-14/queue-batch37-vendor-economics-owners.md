# Queue batch 37 A: Ren's revenue and RCF share (Q-B06), Chariot as a target (P-BUY-08), Foundation Source exit timing (P-BUY-05), JMI in Bloomerang (P-PE-06), the Goldman DAF stack after the Ayco merger (P-VEN-09), and N-PORT lenders to DAF vendors (P-BMG-01)

**Date:** 2026-11-15 · **Recency:** 2021+ evidence only · **No outreach, logins or form submissions.** robots.txt was read on every host before fetching. SEC requests used EDGAR full-text search (`efts.sec.gov`) and `www.sec.gov/Archives` (allowed by robots.txt) with a generic User-Agent, at about 3 requests a second.

**Data written:**
- [`vendor-lenders-nport-2026.csv`](../../data/mission-2026-11-14/vendor-lenders-nport-2026.csv): 267 rows. 251 are N-PORT-P holding lines (Bonterra, legacy CyberGrants, Community Brands/Momentive, and Orion latest-per-filer as context). 16 are no-hit or not-parsed rows.
- [`relationship-graph-edges-additions-21.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-21.csv): EU001–EU016.
- [`queue-proposals-batch37a.csv`](../../data/mission-2026-11-14/queue-proposals-batch37a.csv): P-B37A-01 to P-B37A-03.

**Builds on, and applies the governing corrections of:**
- [queue-bdc-coverage-migrations-goodstack.md](queue-bdc-coverage-migrations-goodstack.md), including the wave-10 corrections (Bonterra 2032 facility at 97.7–99.5% across 13 BDCs).
- [queue-batch32-feeds-owners-codebases.md](queue-batch32-feeds-owners-codebases.md), including the wave-17 and wave-21 corrections.
- [queue-batch33-market-structure.md](queue-batch33-market-structure.md), including the wave-18 and wave-19 corrections. This batch uses the governing Goldman text: a 2021+ GS DAF circular exists only as FireAid Appendix B, and the live stack is the Ren iPhi donor web plus Ayco/GS Wealth Services administration.
- [queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md), including its wave-11 corrections.

**Evidence tags:** **[F]** read from a filing or published page · **[S]** computed by a script from those sources · **[I]** inference · **[X]** third-party estimate, not evidence.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **Q-B06** Ren revenue and RCF share | **Ren's total revenue is not public.** No press, PE or registry source gives a figure. The 2023 Bain round was "near the upper end" of a $75–300m cheque range. Headcount was 350 in 2023, against roughly 410–420 on job-board profiles in 2026 [X].<br>**New: a named-receipts floor.** Across all 1,512 DAFRC sponsors, Form 990 Part VII-B lines naming Ren entities total **$44.98m for TY2024** from 18 sponsors [S]. RCF is **42.7%** of that floor and the two Morgan Stanley programs are **43.0%**. Three customers are therefore **85.8%** of named receipts. RCF's share of *total* Ren revenue is lower by an unknown amount | High (floor); revenue unknown |
| **P-BUY-08** Chariot as a target | **No sign of a sale process.** Chariot Giving Inc. has filed only one Form D: $10,999,978 equity from 59 investors (first sale 2024-04-19). No later raise is on EDGAR to 2026-11-15. Integration breadth grew in 2025–26 (OneCause, now Bonterra, 2025-10-01; TIFIN Give 2025-12-02; Toys for Tots 2026-06-17; Bloomerang to all customers 2026-10). No acquirer is named anywhere | Medium |
| **P-BUY-05** Foundation Source exit timing | **New lender evidence: Audax Private Credit Fund** holds Foundation Source 1st-lien debt (S+5.00%, term loan and DDTL due **2030-09-06**, revolver due 2029-09-06) **at par** at 2026-09-30. It also holds an LP equity stake **marked at 1.38x cost**, down from 1.44x at 2025-12-31. GTCR's release names no fund. Fund XIV closed in May 2023, four months before the deal, so it is the likely vehicle [I]. The 2026 hires (President 2026-03; CTO and Head of Product 2026-09-30) look like a build phase. No banker mandate was found | Medium |
| **P-PE-06** JMI in Bloomerang | **JMI is still invested.** Its portfolio page lists Bloomerang with no exit status line; exited companies carry one. Warburg joined in 2024-02 with three board seats. No 2025–26 control transaction or acquisition was found. The Bloomerang debt (Golub, Monroe) is due Dec 2029. Bloomerang partners with Chariot (DAFpay to all customers, 2026-10) rather than owning a rail | Medium-high |
| **P-VEN-09** GS DAF division of labour | **From the filings:** GS Trust Co (investment, $14.6m), GS & Co ("TECH & INV ADV FEES", $8.08m), Oak Hill (investment, $2.31m), Ayco (admin, $1.03m) and Sapient (technology, $0.82m) are the top five payees for CY2024. GS DAPF has 0 employees. Ren/Stellar runs the iPhi donor web (EA017), but no Stellar line has appeared since CY2022, so it was paid under $824,200 or through another payee. The post-merger CY2025 return is **not yet public** | Medium |
| **P-BMG-01** non-BDC lenders | **Registered funds hold about $212m of funded Bonterra 2032 debt** at 2026-06-30, at 97.71–98.34% of par: Cliffwater Corporate Lending Fund ($140.7m), KKR US Direct Lending Fund-U ($60.7m) and the two Capital Group KKR interval funds ($10.9m). BlackRock Credit Strategies held the legacy 2027 facility (as CyberGrants Holdings, then Bonterra) until 2024-12-31. **No N-PORT holding names Ren, Foundation Source, Benevity, Foundant, Bloomerang, Chariot or any other DAF vendor searched** | High |

---

## 1. Q-B06: Ren's total revenue and RCF's share

### 1.1 Public statements on size

| Source | What it says | Tag |
|---|---|---|
| [Inside INdiana Business, 2023-07-28](https://www.insideindianabusiness.com/?p=149415) | Bain Capital Tech Opportunities led and Valeas participated. The fund "typically invests $75 million to $300 million", and Ren's investment was "near the upper end". 350 employees, about 65% in Indianapolis. Management "continue to be substantial owners". Revenue not disclosed | F (press) |
| [Pulse 2.0 on the Great Hill release, 2025](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/) | "over 150 DAF programs", "more than $175 billion in charitable funding". Bain "will remain a significant shareholder". Houlihan Lokey and Goodwin Procter advised Great Hill. Terms not disclosed | F (press) |
| [Built In](https://builtin.com/company/ren); [LeadIQ](https://leadiq.com/c/renpsg/5a1d991b230000540087bc89) | 419 employees (Built In); revenue "$250M–$500M" (LeadIQ) | X: sales-database estimates, not evidence |
| RCF CY2024 Form 990 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml)) | Officers and directors get $0 from RCF and $0 from related organisations, so there is no Schedule J. Schedule L: Renaissance Administration LLC, $19,225,546, "An officer of RCF is also an officer of Renaissance Administration LLC". Schedule O: Ren "maintains the books and records, prepares tax returns… and provides staff". 0 employees | F |

### 1.2 Named Ren receipts in sponsor 990s (the floor)

Method [S]. The rows come from [`form990-contractors-harvest-full.csv`](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv), a harvest of e-filed returns for all 1,512 FY2024 DAFRC sponsors. The `vendor_group` "Ren (incl. Stellar/iPhi)" covers Renaissance Administration LLC, Renaissance Acquisition Company LLC, RenPSG/Ren PSG/Ren and Stellar Technology Solutions; bare "Renaissance" counts only at Ren's Indianapolis addresses. Part VII-B lists only the **top five** contractors paid over $100k. The floor therefore misses:
- smaller payments and payments ranked below fifth;
- non-sponsor clients (endowments, planned giving, trusts);
- private-label programs paid through RCF.

| Tax year | Sponsors | Named Ren receipts | RCF | RCF share | Morgan Stanley GIFT + US Charitable Gift Trust | Share |
|---|---|---|---|---|---|---|
| 2021 | 11 | $2.93m | not in harvest window | — | — | — |
| 2022 | 24 | $34.00m | $13.49m | 39.7% | $14.49m | 42.6% |
| 2023 | 17 | $35.82m | $15.54m | 43.4% | $15.69m | 43.8% |
| **2024** | **18** | **$44.98m** | **$19.23m** | **42.7%** | **$19.36m** | **43.0%** |
| 2025 | 2 (partial) | $1.28m | not yet filed | — | — | — |

The TY2021 row covers few filings in the harvest window, so do not read it as a trend.

TY2024 payers (each row links its return XML; the rest are in the harvest file):

| Payer | Payee as filed | Service | Amount |
|---|---|---|---|
| Renaissance Charitable Foundation | Renaissance Administration LLC | Administration | 19,225,546 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml)) |
| Morgan Stanley Global Impact Funding Trust | RenPSG | Admin & legal | 14,930,249 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml)) |
| US Charitable Gift Trust | Renaissance Administration LLC | Donor serv/fd acct | 4,430,459 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189349305673_public.xml)) |
| National Christian Charitable Foundation | Stellar Technology Solutions LLC | Software/consulting | 2,495,829 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513109349303201_public.xml)) |
| Jewish Federation of Greater Philadelphia (FYE 8/2025) | Renaissance Administration LLC | Investment administrative srvcs | 500,842 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601679349301260_public.xml)) |
| Stifel Charitable | Renaissance | Ops system & service | 498,305 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542269349303159_public.xml)) |
| 12 others, $118k–$416k each (Cleveland Foundation, Christian Community Foundation, Catholic Community Foundation, Thrivent, T. Rowe Price, ImpactAssets, CF Greater Des Moines, Community Foundation (EIN 58-1723645), Greater Green Bay CF, Goldman Sachs Charitable Gift Fund, JF Greater Seattle, CF Acadiana) | Stellar / Ren | Software and technology | 2,896,577 in total |

**Reading.**
- [S] Three customer relationships (RCF and the two Morgan Stanley programs) make up 85.8% of named Ren receipts in TY2024. Named receipts grew 26% from TY2023 to TY2024, and RCF grew 24%.
- [I] RCF's share of Ren's **total** revenue is below 42.7% by an unknown margin. Ren earns money outside sponsor 990s: endowment and planned-giving platforms, charitable trusts, AEF from 2025–26, and fees below the top-five line.
- [I] Sensitivity only, not an estimate: if Ren's revenue per employee were $150k–$250k, 350–420 staff would imply $53–105m. RCF would then be 18–36% of revenue. The [X] $250–500m figure would need $600k–$1.4m per employee, which is implausible for a services-heavy administrator.
- Morgan Stanley's two programs are as large a dependency as RCF. MS GIFT pays "RenPSG" for "admin & legal" directly.

---

## 2. P-BUY-08: is Chariot a consolidation target?

| Signal | Evidence | Tag |
|---|---|---|
| Capital | One Form D on EDGAR: Chariot Giving Inc. (DE, CIK 2021660). Filed 2024-05-03; equity; $10,999,978 sold, $0 remaining; 59 investors; first sale 2024-04-19; revenue range "Decline to Disclose". Officers/directors listed: the three founders (Serfati, Schneider, Kahane) ([Form D](https://www.sec.gov/Archives/edgar/data/2021660/000202166024000001/primary_doc.xml); [submissions](https://data.sec.gov/submissions/CIK0002021660.json)). Maveron is named as lead by Chariot ([release](https://givechariot.com/resources/insights/chariot-announces-11-million-series-a-investment-round-led-by-maveron)) | F |
| No later raise | EDGAR shows no further Form D to 2026-11-15. A raise under Rule 506 normally files a Form D, but some do not | F (absence) / I |
| Partnerships 2025–26 | OneCause DAFpay integration (2025-10-01; [GlobeNewswire](https://www.globenewswire.com/de/news-release/2025/10/01/3159726/0/en/OneCause-Launches-Integration-with-DAFpay-by-Chariot-Unlocking-Access-to-Billions-in-Donor-Advised-Funds.html)); TIFIN Give on Chariot Disbursements (2025-12-02; [TIFIN](https://tifin.com/news/tifin-and-chariot-partner-to-transform-grant-payments/19418/)); Toys for Tots form (2026-06-17; [Chariot](https://www.givechariot.com/resources/insights/dafpay-by-chariot-now-live-on-toys-for-tots-donation-form)); Bloomerang to all customers (2026-10; repo B33). Repo edges E109–E153 already list DAF-side partners | F |
| Acquirer interest | No 2021+ report of an approach or sale process. OneCause is Bonterra-owned, so Bonterra is both an integrator and a potential buyer [I] | — |

**Reading [I].** Chariot sits on both sides of many platforms: nonprofit CRMs (Bloomerang, Bonterra/OneCause, Gravyty, Give Lively) and DAF providers (Daffy, Charityvest, TIFIN Give, Fidelity's EFT shift). The more neutral it is, the more an acquisition by one CRM would cost it with the others. That argues for a financial or payments-network buyer over Bloomerang or Bonterra. At 2.5 years from the Series A with no new Form D, a Series B or strategic round is the nearer event than a sale. This is unconfirmed.

---

## 3. P-BUY-05: Foundation Source exit timing

| Signal | Evidence | Tag |
|---|---|---|
| Deal | GTCR release 2023-09-13: "GTCR funds"; no fund named; terms undisclosed. Canaccord and Greenberg Traurig advised GTCR; Baird (lead), Lincoln International and K&L Gates advised Foundation Source ([PR Newswire](https://www.prnewswire.com/news-releases/gtcr-announces-acquisition-of-foundation-source-301925653.html)) | F |
| Fund vintage | GTCR Fund XIV final close $11.5bn on 2023-05-23 ([Kirkland](https://kirkland.com/news/press-release/2023/05/kirkland-advises-gtcr-on-closing-of-$11-5-billion-fund-xiv)). Fund XIII ($7.9bn, 2020) was then the prior flagship. Given the timing, Fund XIV is the likely vehicle | I |
| **Debt** | Audax Private Credit Fund 10-Q, 2026-09-30 ([filing](https://www.sec.gov/Archives/edgar/data/2033362/000119312526458521/ck0002033362-20260930.htm)):<br>- 1st Lien Term Loan $13,365,065 and 1st Lien DDTL $4,208,879, both S+5.00%, 9.08%, due **2030-09-06**, fair value = principal;<br>- 1st Lien Revolver $343,575 drawn, due **2029-09-06**;<br>- unfunded revolver $2,233,237.<br>Acquisition date 2024-10-10 (the fund's launch transfer). At 2025-12-31: term loan $13,468,138 and DDTL $4,241,089 at par | F |
| **Equity mark** | Same filing: Class A LP Interests (1,824 units) and Class B LP Interests (1,822,812 units), cost $2,004,694, fair value **$2,765,483 (1.38x)**. At 2025-12-31: $2,880,081 (1.44x) | F / S |
| Leadership | Sabrina Bailey President (2026-03-10, repo CT153); Manu Sood CTO and Hetal Patel new Head of Product (2026-09-30), with "increased focus on AI". Scale at 2025-12-31: 5,600+ PFs, 20,000 DAF accounts, $55bn+ assets ([release](https://foundationsource.com/newsroom/press-releases/foundation-source-appoints-new-technology-and-product-leaders-to-advance-philtech-platform/)) | F |
| Banker mandate / recap | None found in 2026 searches | — |

**Reading [I].**
- A 7-year term loan due 2030-09-06 fits financing struck at the September 2023 buyout. Sponsors usually sell or refinance 1–2 years before maturity, so the debt does not force anything before 2028.
- The lender's equity mark (1.38x on a 2024-10 transfer cost, slightly down in 2026) and the loan at par point to a healthy credit, not a distressed seller.
- New CTO and product hires plus "DAF OS" marketing (repo CT189) suggest GTCR is still building value. A 2027 process is possible on a 4-year hold, but nothing public shows one is under way.
- The repo's private-equity map line 28 ("Not found: lenders to GTCR-era Foundation Source") is superseded for Foundation Source: Audax holds the GTCR-era debt (see §7).

---

## 4. P-PE-06: JMI Equity and Bloomerang

| Signal | Evidence | Tag |
|---|---|---|
| JMI status | [jmi.com/companies](https://www.jmi.com/companies/) (fetched 2026-11-15): Bloomerang is listed with a JMI team (David Greenberg, Larry Contrella, Vincent Prajka) and **no "Status:" line**. Exited holdings carry one, for example "Status: Acquired by Luminate Capital Partners" (Axonify) and "Status: IPO" (Blackbaud). Benevity is also listed without a status line | F |
| Warburg | Release 2024-02-08: Warburg's Andrew Park, Sam Lipsick and Peter Kimmey "join JMI on the Bloomerang board". Contrella (JMI) is quoted as a board member. No split or amount given ([Bloomerang](https://bloomerang.com/news/bloomerang-secures-strategic-investment-from-warburg-pincus)). The "equal owners, combined majority" wording appears only in trade press ([NonProfit Times](https://thenonprofittimes.com/npt_articles/bloomerang-adds-warburg-pincus-as-second-equity-investor/)) | F / press |
| Debt | Golub (6 BDCs) one-stop loans due 12/2029, 98.96–99.01% at 2026-06-30; Monroe Capital Income Plus 100.54% at 2026-09-30, due 2029-12-27 ([bdc-loans-latest-marks.csv](../../data/mission-2026-11-14/bdc-loans-latest-marks.csv)) | F (repo) |
| M&A since 2024 | No acquisition after Qgiv (closed Dec 2023). Bloomerang's news index lists only AI products and reports (Penny, conversational reporting, 2026 Giving Signals, GivingTuesday 2025) ([news](https://bloomerang.com/news/)) | F |
| DAF rail | DAFpay via Chariot for all customers (2026-10; repo B33). No owned DAF payment capability | F |

**Reading [I].**
- A JMI exit would show as a status line or a release; neither exists. JMI's 2020 entry is now about 6 years old, which is long for JMI. The 2024 Warburg round was the partial liquidity event.
- The December 2029 maturity matches a 6-year loan from the Qgiv closing. A control sale before 2028 would need a refinancing or change-of-control repayment; none is visible.
- The P-BUY-08 link: Bloomerang is buying the rail as a partner, not as an owner.

---

## 5. P-VEN-09: the Goldman DAF stack after Ayco merged in

GS DAPF (EIN 31-1774905), CY2024 Form 990 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml)) [F]:
- **Part VII-B top five** (13 contractors over $100k):
  - The Goldman Sachs Trust Company, "INVESTMENT/ADVISORY", $14,603,327;
  - Goldman Sachs & Co LLC, "TECH & INV ADV FEES", $8,078,863;
  - Oak Hill Advisors, "INVESTMENT ADV. SERV", $2,313,978;
  - The Ayco Company LP, "ADMIN. SERVICES", $1,026,306;
  - Sapient Corporation, "TECHNOLOGY SERVICES", $824,200.
- **Part IX:** information technology $2,815,788; "AGENCY FEE" $7,070,047; "BNY MELLON CUSTODY FEE" $108,870; fees for services (other) $2,598,621. 0 employees.
- **Schedule R:** The Ayco Charitable Foundation is a related tax-exempt organisation. Acorn Private Assets LP (Cayman) is wholly owned.

**Series (from the harvest) [F/S]:**

| Year | GS & Co label and amount | Ayco (GS DAPF) | Sapient | Stellar |
|---|---|---|---|---|
| CY2022 | "INVESTMENT/ADVISORY" $5,358,330 | not in top 5 | not in top 5 | $390,398 "SOFTWARE PROVIDER" |
| CY2023 | "TECH & INV ADV FEES" $7,318,240 | $3,234,367 | $449,360 | not in top 5 |
| CY2024 | "TECH & INV ADV FEES" $8,078,863 | $1,026,306 | $824,200 | not in top 5 |

**Ayco Charitable Foundation, CY2024** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543109349303959_public.xml)) [F]:
- Only **one** contractor over $100k: Ayco Company, "ADMIN/INVST ADVISORY", $1,730,728.
- Information technology $533,200.
- In CY2022–23 it paid Stellar $330,735 and $336,481, and GS & Co "TECHNOLOGY SERVICES" $175,200 (CY2023).
- So **Stellar fell below $100k at Ayco in CY2024**.
- The final FY6/2025 return records the 2025-07-01 merger into GS DAPF (repo V19-06). It is in the IRS 2026 TEOS zip and not on gt990datalake.

**Division of labour, as far as filings show:**
- **Investment:** GS Trust Co (largest), GS & Co (partly) and Oak Hill.
- **Administration:** Ayco (falling: $3.23m → $1.03m at GS DAPF).
- **Technology:**
  - Ren/Stellar iPhi runs the donor web (EA017, live 2026);
  - Sapient bills "technology services" (rising);
  - GS & Co's line has been relabelled to include "TECH" since CY2023.

**Reading [I].**
- **Direct Ren payments dropped below disclosure thresholds from CY2023.** At GS DAPF they were under the $824k fifth-place line; at Ayco under $100k.
- **The relabel points to one of two routes.** The GS & Co "tech" fee from CY2023 onward and Sapient's arrival fit either:
  - (a) Ren is now paid through Goldman (GS & Co contracting with Ren and recharging); or
  - (b) Goldman is moving work in-house or to Sapient while keeping iPhi as the portal.
- **Neither route is confirmed.** In both, the GS DAF is "affiliate-administered with Ren software", not "Ren-administered". The CY2025 return (first post-merger; ProPublica lists CY2024 as latest on 2026-11-15) should settle it (P-B37A-02).
- **Payee naming.** "Sapient Corporation" at 40 Water Street, Boston, is Publicis Sapient's US entity. Its ownership was not re-verified this pass.

---

## 6. P-BMG-01: N-PORT holders of DAF-vendor loans

**Method [S].**
- Ran EDGAR full-text search (`forms=NPORT-P`, 2021-01-01 to 2026-11-15) for each name in the no-hit table below plus "Bonterra LLC", "CyberGrants", "Community Brands", "Momentive Software" and "Orion Advisor".
- Fetched every hit's XML and kept `invstOrSec` lines whose name or title matched. Orion was sampled at the latest filing per filer only.
- 57 hits were HTML schedules, not N-PORT XML (mostly SEI and Orion filers), and were skipped.
- Exact-phrase checks were also run over N-CSR/N-CSRS/N-2/424B3/10-K/10-Q.

### 6.1 Bonterra (Apax), latest marks

| Holder (registered fund) | Period | Instruments | Balance | Value | Mark | Source |
|---|---|---|---|---|---|---|
| Cliffwater Corporate Lending Fund | 2026-06-30 | 13 lines: TL, DDTL (two due 2032-10-08), revolver; 2032-03-05 | $190.9m (of which $143.1m at 8.4–8.5% coupons) | $187.7m ($140.7m) | 98.34% | [N-PORT](https://www.sec.gov/Archives/edgar/data/1735964/000173596426000022/primary_doc.xml) |
| KKR US Direct Lending Fund-U | 2026-06-30 | TL 1L 03/25 $49.93m; DDTL 03/25 $5.44m; DDTL 10/25 $13.54m commitment ($6.59m value); revolver $5.45m ($0.97m value) | $74.4m commitments | $61.6m | TL 97.71% | [N-PORT](https://www.sec.gov/Archives/edgar/data/1987990/000119312526371471/primary_doc.xml) |
| Capital Group KKR Multi-Sector (plus) | 2026-06-30 | TL, DDTL, revolver 03/25 | $6.25m | $6.11m | 97.71% | [N-PORT](https://www.sec.gov/Archives/edgar/data/2040318/000094040026035898/primary_doc.xml) |
| Capital Group KKR Core Plus (plus) | 2026-06-30 | TL, DDTL, revolver 03/25 | $4.85m | $4.74m | 97.71% | [N-PORT](https://www.sec.gov/Archives/edgar/data/2040315/000094040026035899/primary_doc.xml) |
| BlackRock Credit Strategies Fund | 2024-12-31 (last) | Legacy TL + Amendment No. 4 (2023) and 5th Amendment (2024) incrementals, due 2027-09-08 | $4.43m | $4.40m | 99.09–100.25% | [N-PORT](https://www.sec.gov/Archives/edgar/data/1752019/000175272425037898/primary_doc.xml) |
| BlackRock Credit Strategies Fund (as Cybergrants Holdings LLC) | 2021-09-30 to 2022-06-30 | TL, DDTL, revolver due 2027-09-08 | $4.0m | $3.96m | 99.03% | [N-PORT](https://www.sec.gov/Archives/edgar/data/1752019/000175272422193798/primary_doc.xml) |

**Findings.**
- **Funded registered-fund exposure is about $212m** at 2026-06-30 [S]. Cliffwater alone is the single largest identified Bonterra lender, larger than any BDC position in the repo files.
- **Marks fell.** The registered funds marked the facility at 99.0–100% in 2025 and 97.71–98.34% at 2026-06-30. This matches the BDC drift in the wave-10 governing text (97.7–99.5%).
- **The DDTL 10/25 is being drawn.** At KKR Fund-U, value as a share of commitment rose from 26.0% (2025-12-31) to 49.2% (2026-03-31) and 48.7% (2026-06-30) [S]. Cliffwater shows new DDTL lines due 2032-10-08. Read: acquisition capacity is being used [I].
- **The CyberGrants-to-Bonterra rename is visible in one fund.** BlackRock's Cybergrants Holdings lines (due 2027-09-08) give way to Bonterra LLC lines with the same maturity from 2022-09-30 [F; rename inference I].
- **Unfunded lines are unclear.** Cliffwater's lines at 0.375–1.0% "annualized rate" (about $47.8m) are probably unfunded commitments carrying commitment fees, yet they show positive value. They are flagged `likely_unfunded_or_fee_line`, not dropped.

### 6.2 Others

- **Community Brands / Momentive:**
  - Cliffwater (2022, 2028 facility, 98.01–99.01%).
  - KKR Credit Opportunities Portfolio (to 2024-04, 99.97%). One KKR line is titled "(MINISTRY BRANDS)" and is flagged as ambiguous.
  - Mercer and SEI (2029 loans, 2024).
  - Western Asset / Legg Mason funds (2031 "CB Buyer Inc" / "Momentive Software" loans, 99.0–99.75%, last seen 2025-04-30).
  - These are association/church software lenders, context only.
- **Orion Advisor Solutions (context):** 51 filers in latest-per-filer sampling. 2026 lines: $50.9m par at 99.5% of par, maturities 2027-09-24 and 2030-09-24 (broadly syndicated).
- **No N-PORT hit** for Ren/RenPSG/Renaissance Philanthropic/Renaissance Administration/Stellar Technology Solutions, Foundation Source, Benevity, Foundant, Bloomerang, Fundraise Up, Submittable, SmartSimple, Givinga, Chariot, Neon One, EverTrue, Network for Good, Daffy, Classy or GoFundMe [F, absence].
- **Hits outside N-PORT:**
  - Foundation Source and Bloomerang appear only in BDC 10-K/10-Q (Audax; Golub/Monroe).
  - "Benevity" appears only in corporate filers' 10-Ks (customers), not lenders.
- **Reading [I]:** Ren's and Benevity's acquisition debt, if any, is held off-EDGAR: bank clubs, private funds or non-US lenders.
- **Blackbaud:** 10,000+ N-PORT hits, nearly all listed equity. Its loan holdings were not isolated (limit).

---

## 7. Corrections to existing repo text (proposed)

1. **[`private-equity-daf-ecosystem-map.md`](private-equity-daf-ecosystem-map.md) line 28** ("Not found: lenders to GTCR-era Foundation Source, Ren, Bonterra and Benevity"):
   - Replace with: "Lenders found: GTCR-era Foundation Source, Audax Private Credit Fund (1L TL/DDTL due 2030-09-06, revolver due 2029-09-06; batch 37A EU007). Bonterra: 13 BDCs plus registered funds (Cliffwater, KKR US Direct Lending Fund-U, Capital Group KKR interval funds; batch 37A EU001–EU004). Not found: Ren, Benevity."
2. **[`bdc-loans-latest-marks.csv`](../../data/mission-2026-11-14/bdc-loans-latest-marks.csv), Foundation Source Class A and Class B rows.**
   - The `par_or_principal` values (1,718 and 1,716,159 at 2024-12-31; 1,824 and 1,822,812 at 2026-09-30) are **unit counts**, not dollars.
   - The equity cost at 2026-09-30 is $2,004,694 against value $2,765,483 (from the 10-Q table).
   - Do not compute a % of par for these rows.
3. **[`DAF-INDUSTRY-REPORT-2026-11.md`](../DAF-INDUSTRY-REPORT-2026-11.md) line 146** ("Ren's corporate revenue, margins and customer concentration are not public"):
   - Append: "Named Ren receipts in sponsor 990s total $44.98m in TY2024. RCF is 42.7% of that and the two Morgan Stanley programs 43.0% (batch 37A §1.2). This is a floor on receipts, not Ren revenue."

## 8. Limits

- Part VII-B lists only the top five contractors over $100k, so the Ren floor misses payments below that line. TY2025 returns are mostly unfiled.
- N-PORT-P is public only for each fund's fiscal-quarter-end month. Q3-2026 filings (2026-09-30) for most funds were not yet public or indexed.
- The 57 HTML-only hits were not parsed.
- "Annualized rate" is used as a funded/unfunded proxy. KKR and Cliffwater report partly unfunded lines differently, so line marks for partly drawn DDTLs and revolvers are not prices.
- gspf.goldman.com disallows non-search crawlers (wave 18), so it was not fetched.
- Several press pages (IBJ, Business Wire) were read through secondary syndication or search results only. They are cited where read.
- Headcount and revenue figures from job boards and sales databases are [X] and are used only for the sensitivity in §1.2.

---

## Source register

| ID | Source | Type | Date | Accessed | URL |
|---|---|---|---|---|---|
| S1 | RCF CY2024 Form 990 (Schedules L, O; Part VII) | IRS e-file XML | CY2024 | 2026-11-15 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml |
| S2 | Form 990 contractor harvest (Ren rows) | repo data | TY2021–25 | 2026-11-15 | ../../data/mission-2026-11-14/form990-contractors-harvest-full.csv |
| S3 | Inside INdiana Business on the Bain round | press | 2023-07-28 | 2026-11-15 | https://www.insideindianabusiness.com/?p=149415 |
| S4 | Pulse 2.0 on the Great Hill investment | press | 2025 | 2026-11-15 | https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/ |
| S5 | Built In / LeadIQ profiles | third-party [X] | 2026 | 2026-11-15 | https://builtin.com/company/ren ; https://leadiq.com/c/renpsg/5a1d991b230000540087bc89 |
| S6 | Chariot Giving Inc. Form D | SEC | 2024-05-03 | 2026-11-15 | https://www.sec.gov/Archives/edgar/data/2021660/000202166024000001/primary_doc.xml |
| S7 | Chariot EDGAR submissions index | SEC | live | 2026-11-15 | https://data.sec.gov/submissions/CIK0002021660.json |
| S8 | Chariot Series A release | company | 2024-08-08 | 2026-11-15 | https://givechariot.com/resources/insights/chariot-announces-11-million-series-a-investment-round-led-by-maveron |
| S9 | OneCause–DAFpay | press release | 2025-10-01 | 2026-11-15 | https://www.globenewswire.com/de/news-release/2025/10/01/3159726/0/en/OneCause-Launches-Integration-with-DAFpay-by-Chariot-Unlocking-Access-to-Billions-in-Donor-Advised-Funds.html |
| S10 | TIFIN–Chariot | press release | 2025-12-02 | 2026-11-15 | https://tifin.com/news/tifin-and-chariot-partner-to-transform-grant-payments/19418/ |
| S11 | Chariot – Toys for Tots | company | 2026-06-17 | 2026-11-15 | https://www.givechariot.com/resources/insights/dafpay-by-chariot-now-live-on-toys-for-tots-donation-form |
| S12 | GTCR acquires Foundation Source | press release | 2023-09-13 | 2026-11-15 | https://www.prnewswire.com/news-releases/gtcr-announces-acquisition-of-foundation-source-301925653.html |
| S13 | GTCR Fund XIV close | law-firm release | 2023-05-23 | 2026-11-15 | https://kirkland.com/news/press-release/2023/05/kirkland-advises-gtcr-on-closing-of-$11-5-billion-fund-xiv |
| S14 | Audax Private Credit Fund 10-Q (Q3 2026) | SEC | 2026-09-30 | 2026-11-15 | https://www.sec.gov/Archives/edgar/data/2033362/000119312526458521/ck0002033362-20260930.htm |
| S15 | Foundation Source CTO/product release | company | 2026-09-30 | 2026-11-15 | https://foundationsource.com/newsroom/press-releases/foundation-source-appoints-new-technology-and-product-leaders-to-advance-philtech-platform/ |
| S16 | JMI portfolio | company | live | 2026-11-15 | https://www.jmi.com/companies/ |
| S17 | Bloomerang–Warburg release | company | 2024-02-08 | 2026-11-15 | https://bloomerang.com/news/bloomerang-secures-strategic-investment-from-warburg-pincus |
| S18 | Bloomerang news index | company | live | 2026-11-15 | https://bloomerang.com/news/ |
| S19 | NonProfit Times on Warburg | press | 2024 | search result only | https://thenonprofittimes.com/npt_articles/bloomerang-adds-warburg-pincus-as-second-equity-investor/ |
| S20 | GS DAPF CY2024 Form 990 | IRS e-file XML | CY2024 | 2026-11-15 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml |
| S21 | Ayco Charitable Foundation CY2024 Form 990 | IRS e-file XML | CY2024 | 2026-11-15 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543109349303959_public.xml |
| S22 | ProPublica GS DAPF filings list | aggregator API | live | 2026-11-15 | https://projects.propublica.org/nonprofits/api/v2/organizations/311774905.json |
| S23 | N-PORT-P filings (all holding rows) | SEC | 2021-09-30 to 2026-08-31 | 2026-11-15 | per-row `source_url` in vendor-lenders-nport-2026.csv |
| S24 | EDGAR full-text search API | SEC | live | 2026-11-15 | https://efts.sec.gov/LATEST/search-index?q=%22Bonterra%20LLC%22&forms=NPORT-P |

## Data dictionary

### `vendor-lenders-nport-2026.csv` (one row per N-PORT holding line, or per no-hit search)

| Field | Meaning |
|---|---|
| `row_id` | NP0001… |
| `row_type` | `holding`; `no_hit` (search returned no N-PORT holding); `not_parsed` (Blackbaud) |
| `vendor_group` | Repo company group (matches `bdc-loans-*.csv` where it overlaps) |
| `borrower_name_as_listed`, `holding_title` | N-PORT `name` and `title`, verbatim |
| `filer_registrant`, `series_name`, `filer_cik` | Registrant, series and CIK |
| `form`, `accession`, `period_end`, `file_date` | Filing identity (`repPdDate` = period end) |
| `asset_cat` | N-PORT asset category (LON loan, DBT debt, EP) |
| `balance`, `units`, `currency` | Principal or commitment (`PA` = principal amount) |
| `value_usd` | Reported fair value in USD (unfunded or partly funded lines can be small or negative) |
| `mark_pct_of_balance` | 100 × value / balance [S]. A price only for fully funded lines |
| `pct_of_fund_nav` | N-PORT `pctVal` |
| `maturity` | N-PORT `maturityDt` |
| `annualized_rate_pct` | N-PORT `annualizedRt` |
| `funded_flag_inferred` | `funded` if rate > 2%; `likely_unfunded_or_fee_line` if ≤ 2%; `unknown` if absent [I] |
| `fair_value_level` | ASC 820 level |
| `is_latest_for_series` | yes = latest period found for that vendor × series |
| `sample_scope` | `all_hits`, or `latest_filing_per_filer_only` (Orion) |
| `efts_query` | Exact-phrase query that found the filing |
| `source_url` | N-PORT primary_doc.xml (or the EFTS query template for no-hit rows) |
| `notes` | Caveats (e.g. Ministry Brands ambiguity) |

### `relationship-graph-edges-additions-21.csv`

The columns are the same as `relationship-graph-edges.csv`. IDs are EU001–EU016, accessed 2026-11-15. `lender` (relationship and source type) and `merged_into` are new relationship types. `lender` follows the bdc-loans data vocabulary.

### `queue-proposals-batch37a.csv`

The format is in `queue-proposals-README.md`. IDs are P-B37A-01 to P-B37A-03; `state` = open.

## Validation corrections (wave 22, 2026-11-15) — governing
Source: [validation-wave22-report.md](validation-wave22-report.md); register `data/mission-2026-11-14/validation-register-wave22.csv`.

1. **§0, P-VEN-09 row.**
   - **Find:** "but no Stellar line has appeared since CY2022, so it was paid under $824,200 or through another payee."
   - **Replace with:** "but no Stellar line has appeared at GS DAPF or Ayco since CY2022, so there it was paid under $824,200 or through another payee. The separate Goldman Sachs Charitable Gift Fund (EIN 11-3813663) still paid Stellar directly ($172,604, FYE 2025-06) [V wave 22]."
2. **§3 table, Fund vintage row.**
   - **Find:** "GTCR Fund XIV final close $11.5bn on 2023-05-23 ([Kirkland]"
   - **Replace with:** "GTCR Fund XIV closed at its $11.5bn hard cap (Kirkland release dated 2023-05-31, no closing day stated; [V wave 22]) ([Kirkland]"
3. **§5, first Reading bullet.**
   - **Find:** "- **Direct Ren payments dropped below disclosure thresholds from CY2023.** At GS DAPF they were under the $824k fifth-place line; at Ayco under $100k."
   - **Replace with:** "- **Direct Ren payments dropped below disclosure thresholds from CY2023 at GS DAPF and Ayco.** At GS DAPF they were under the $824k fifth-place line; at Ayco under $100k. This does not hold for every Goldman-branded sponsor. The Goldman Sachs Charitable Gift Fund (EIN 11-3813663; grant administration by CAF America) paid Stellar Technology Solutions directly $157,430, $150,924, $139,000 and $172,604 for FYE June 2022–2025. It is one of the \"12 others\" in §1.2 [V wave 22]."
4. **§6.1 table, Cliffwater row.**
   - **Find:** "13 lines: TL, DDTL (two due 2032-10-08), revolver; 2032-03-05"
   - **Replace with:** "13 lines: TL, DDTL (three due 2032-10-08, one of them a 1.0% likely-unfunded line), revolver; 2032-03-05 [V wave 22]"
5. **§6.1 Findings, first bullet.**
   - **Find:** "Cliffwater alone is the single largest identified Bonterra lender, larger than any BDC position in the repo files."
   - **Replace with:** "Cliffwater is the largest registered-fund holder. On funded lines ($140.7m) it is second to a BDC, FS KKR Capital Corp ($150.4m par, $149.6m fair value at 2026-09-30 in `bdc-loans-latest-marks.csv`). It is larger only if its roughly $47.8m of likely-unfunded or fee lines are counted ($187.7m) [V wave 22]."
6. **§7, status line (append after item 3).** "Validation wave 22: proposals 1–3 are supported (V22-01, V22-04, V22-05, V22-13). Proposal 1 is applied in `private-equity-daf-ecosystem-map.md` with FS KKR added as the largest funded Bonterra holder; proposal 3 is applied in the industry report."
