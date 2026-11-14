# Donation-processor vendor economics, fraud-loss disclosures, Give Interactive and GiftingNetwork, LPL–Commonwealth, Flipcause

*Queue items P-990-06, P-INF-09, P-BUY-06, P-BUY-03 and P-FAIL-05. Prepared 2026-11-14. Builds on [`vendor-footprint-990-harvest.md`](vendor-footprint-990-harvest.md), [`full-universe-990-harvest-and-corrected-totals.md`](full-universe-990-harvest-and-corrected-totals.md), [`queue-give-interactive-displacement.md`](queue-give-interactive-displacement.md), [`firms-interested-in-daf-organizations.md`](firms-interested-in-daf-organizations.md) and [`failed-daf-startups-deep-research.md`](failed-daf-startups-deep-research.md). Where those files carry "Validation corrections (wave 4) — governing" sections, this note follows them: W4-6 to W4-9 for buyers, and W4-10/W4-11 for Flipcause (Stripe reserve and the Ravyn testimony). Public sources only. No PACER login, no paid databases, and no contact with any party.*

**Data written**
- [`data/mission-2026-11-14/processor-vendor-economics-990.csv`](../../data/mission-2026-11-14/processor-vendor-economics-990.csv): 240 rows. Each row is a vendor line, a processing-cost line or the derived non-grant expense for one sponsor-year, with ratios to grants and contributions.
- [`data/mission-2026-11-14/sponsor-fraud-loss-disclosures.csv`](../../data/mission-2026-11-14/sponsor-fraud-loss-disclosures.csv): 17 rows. These are explicit fraud or theft losses, Part VI line 5 diversion disclosures, and bad-debt or credit-loss lines at processor sponsors, which are labelled as cause undisclosed.
- [`data/mission-2026-11-14/queue-proposals-processor-profiles.csv`](../../data/mission-2026-11-14/queue-proposals-processor-profiles.csv): P-PRC-01 to P-PRC-06.

**Evidence labels:** **[F]** filed or first-party fact; **[R]** reported by press or a third party; **[I]** inference; **[U]** unknown or not found.

---

## 1. Bottom line

1. **Donation processors pay an effective 1–3% of grants for platform and processing, and the largest single line is Benevity at AOGF (P-990-06).**
   - AOGF paid Benevity $29.27m, $33.49m, $45.97m and **$54.45m** in FY3/2022–FY3/2025. That is **1.75%, rising to 2.56% of grants paid**. It also paid BlueSnap about 0.26–0.28% and PayPal 0.03–0.08%, and its "merchant fees" line holds steady at about 0.30% [F].
   - All of AOGF's non-grant cost is **2.90%** of its $2.13bn of grants [F].
   - Benevity's published foundation schedule sets a **2.99% Cause Support Fee capped at $500**, which does not apply to matching gifts or gifts of securities ([Benevity Foundations Fees Schedule, updated 2026-10-01](https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf)) [F]. So the 2.56% is consistent with the schedule applied to most, but not all, volume [I].
2. **Most other processors carry processing cost inside Part IX and name no vendor.**
   - PayPal Charitable Giving Fund: "transaction costs & service fees" were **$12.64m, 1.58% of $798m grants**, in 2024, up from 0.69% in 2022 [F].
   - Blackbaud Giving Fund (YourCause): card, bank/merchant and vetting fees came to **0.80%** in 2025 [F].
   - Network for Good: Bonterra fee 1.13% plus "transaction processing" 2.02%, for **5.20% all-in** in 2024, while grants fell from $429m to $220m (2022–2024) [F].
   - CAF America: CyberGrants rose from $5.41m to **$8.29m (0.61% to 0.83%)** [F].
   - The small workplace-giving funds are far costlier: FrontStream Global Fund pays FrontStream **9.98%** of grants, and Give Back Foundation pays TASC **32.5%** [F].
3. **Fraud losses are almost never itemised (P-INF-09).**
   - Across all **5,272 returns of the 1,512-sponsor universe** (FY2022–25), the only explicit fraud-loss line at a DAF processor is **Givinga Foundation's $316,184 "external bank fraud loss"** (CY2024). That is 2.41% of revenue and 2.85% of grants [F].
   - Part VI line 5 ("significant diversion of assets") was answered Yes on **7 returns (0.13%)**, and on **none** by a National or processor sponsor [F].
   - Three of the seven are payment redirection or business-email compromise (BEC), at the Prosperity Foundation, Washington University and The Nature Conservancy [F].
4. **Give Interactive and GiftingNetwork are competing for the same top-15 community foundations, and neither shows outside capital (P-BUY-06).**
   - Foundation for the Carolinas (FFTC) paid Give $654,500 in CY2023 and left, and it has run on **GiftingNetwork since 2026-07-01** ([PRLog, 2026-09-23](https://www.prlog.org/13172546-giftingnetworks-donor-portal-live-at-foundation-for-the-carolinas.html)) [R/F].
   - The Chicago Community Trust (CCT) portal is "Powered by GiftingNetwork", but Give hosts for CCT reached production in 2025-06.
   - GiftingNetwork has a 990 footprint: Jewish Community Foundation of San Diego paid it $171,500–$359,535 a year for "custodian for investments and back office" (FY6/2022–FY6/2025) [F].
   - Give is 99%-owned by The Signatry Charitable Trust and is loss-making [F].
5. **LPL–Commonwealth (P-BUY-03): there is no public decision, and the "re-bid" framing looks wrong.**
   - The Commonwealth Charitable Fund is still a separate Ren DonorFirstX program: code `CFNDAF`, id 680, with LPL broker-dealer legends, live 2026-11-14 ([portal](https://cfndaf.donorfirstx.com/)) [F].
   - LPL's own channel is the generic Renaissance Charitable Foundation (RCF) portal ([Ren](https://www.reninc.com/lpl-rcf-daf/)) [F].
   - Both programs are Ren/RCF (CFN's sponsor is inferred, edge E034), so consolidating them is a branding and program-code decision, not a vendor change [I].
   - LPL said on 2026-10-28 that conversion was two weeks away, with 83% asset retention ([WealthManagement](https://www.wealthmanagement.com/ibd-news/lpl-lowers-commonwealth-asset-retention-to-83)) [R].
6. **Flipcause (P-FAIL-05): a Chapter 7 liquidation with no distributions or title ruling reported.**
   - The case is D. Del. 25-12246-TMH. It was converted 2026-04-28, the trustee is Jeffrey T. Testa, and the bar date was 2026-07-07 ([Official Form 309D, Doc 228](https://document.epiq11.com/document/getdocumentsbydocket/?docketId=1225685&projectCode=FLX&docketNumber=228)) [F].
   - The assets were sold for **$400,000** to Software4Nonprofits.
   - A proposed Stripe settlement would give the estate about **$550k**, with Stripe's unsecured claim subordinated to nonprofit repayment ([Oakland Voices, 2026-04-23](https://oaklandvoices.us/2026/04/23/flipcause-chapter-7-bankruptcy-conversion-lawsuits/)) [R].
   - No court ruling on title to donations was found [U].

---

## 2. Method

- **Structured extraction.**
  - I re-downloaded the IRS e-file XML from the GivingTuesday mirror (`https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/<object_id>_public.xml`) for 347 returns.
  - These cover the 103 National sponsors (81 Standard and 22 DAFRC "Donation Processor"), plus Pledgeling Foundation, Global Impact and United Way Worldwide, for FY2022–25.
  - Object IDs come from `form990-returns-schedule-d-harvest-full.csv`, plus Givinga's amended CY2024 return 202503179349301975.
  - I parsed:
    - Part I lines 8, 13 and 18;
    - Part IX lines 11a–11g, 14 and 24 (every `OtherExpensesGrp`);
    - Part VI line 5 (`MaterialDiversionOrMisuseInd`);
    - Part VII-B contractors;
    - Schedule D Part I;
    - every free-text element matching fraud, loss or diversion keywords.
  - Scripts were run from the scratchpad and stdlib only (not committed). The extraction logic mirrors `scripts/mission_990_contractors.py`.
- **Full-universe flag scan.** I streamed all **5,272** parsed returns in the harvest, covering 1,512 sponsors. For each I captured `MaterialDiversionOrMisuseInd`, any Part IX other-expense description matching fraud, theft or cyber terms, and any `ExplanationTxt` (Schedule O, D or F supplemental text) matching fraud, theft, embezzlement, misappropriation, cyber-attack, phishing or unauthorized-transfer terms. Hits were reviewed by hand. Schedule I recipient names (such as "… Diversion Initiative") were excluded.
- **Ratios.** Vendor and processing lines are divided by **Part I line 13 (grants paid)**. Schedule D DAF grants are carried alongside and are within about 1% for the large processors. The "derived non-grant expense" is line 18 minus line 13.
- **Limits.**
  - Part VII-B lists only the five largest contractors over $100k.
  - Processors owned by their platform (PayPal, Blackbaud, Givinga, Mightycause) often absorb or net costs, so no vendor line appears.
  - Bad-debt lines may include chargebacks, but no return says so.
  - FY2025 coverage is partial: Vanguard Charitable, Ayco, Endaoment and NPT returns are not yet mirrored.

---

## 3. P-990-06: vendor economics of the donation-processor segment

### 3.1 Vendor payments named in Part VII-B, FY2022–FY2025

Totals are over every return in the CSV. The latest year is shown as a percentage of Part I grants.

| Vendor | Paying sponsors | Σ FY2022–25 | Latest year: amount and % of grants | Notes |
|---|---|---|---|---|
| **Benevity** | AOGF | **$163.18m** | FY3/2025: $54.45m, **2.56%** | Ratios by year: 1.75%, 1.95%, 2.35%, 2.56%. AOGF Part IX line 11a ("management") is $54.69m, which is essentially Benevity ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202641969349302754_public.xml)) |
| **TASC** (Total Administrative Services Corp) | Give Back Foundation | $57.50m | CY2025: $14.21m, **32.5%** | Give Back also books "distribution fees" of $10.59m (24.2%) and pays outreach coordinators. All non-grant cost is 55% of grants ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202631669349300818_public.xml)) |
| **Bonterra** (CyberGrants / Network for Good) | CAF America, Network for Good, CF of Western … | $25.98m | CAF America FY4/2025: $8.29m, 0.83%. NfG 2024: $2.49m, 1.13% | NfG also has "transaction processing" of $4.46m (2.02%) ([NfG 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513039349301631_public.xml); [CAF America 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610489349300906_public.xml)) |
| **BlueSnap** | AOGF | $19.96m | FY3/2025: $5.54m, 0.26% | Flat at 0.26–0.28% |
| **Mightycause** | Mightycause CF, Colorado Gives, Communities Foundation of Texas | $10.95m | Mightycause CF 2024: $2.31m, 2.33% | Plus "transaction costs" of 1.73% ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513159349302051_public.xml)) |
| **FrontStream** | FrontStream Global Fund, United Way Worldwide | $6.68m | FGF FY6/2025: $1.55m, **9.98%** | Rose from 6.29% to 9.98% as grants fell ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611119349300311_public.xml)) |
| **PayPal / Braintree** | AOGF, Pure | $4.56m | Pure 2024: $0.30m, 1.03%. AOGF FY2025: $0.73m, 0.03% | PayPal is **not** a payee of PayPal Charitable Giving Fund |
| **Stripe** | Pledgeling and three community/university foundations | $2.81m | Pledgeling 2024: $0.44m, 1.09% | |
| **GiftingNetwork** (incl. GN PBO Company LLC) | JCF San Diego | $0.93m | FY6/2025: $191,424 | "Custodian for investments and back office" ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611349349307506_public.xml)) |
| **Give Interactive** | FFTC | $0.65m | CY2023 only | Already in the harvest |
| Commercial fundraisers (Charitybuzz, Prizeo, Omaze) | Pledgeling, CAF America | $37.83m | Pledgeling 2024: Charitybuzz $17.85m, **44.3%** | Commercial co-venture economics, not processing |

### 3.2 Processors whose processing cost sits in Part IX with no vendor named

Latest return. Each "% of grants" figure divides that cost line by Part I line 13.

| Sponsor | Grants paid | Processing / service lines | All non-grant cost |
|---|---|---|---|
| PayPal Charitable Giving Fund (CY2024) | $797.9m | Transaction costs & service fees $12.64m (**1.58%**). Was 0.69% in 2022 and 0.97% in 2023 | 1.71% ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml)) |
| Blackbaud Giving Fund (CY2025) | $536.4m | Card fees $1.63m (0.30%), bank/merchant $0.96m (0.18%), vetting $0.47m (0.09%) | **0.80%** ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202622529349301602_public.xml)) |
| AOGF (FY3/2025) | $2,125.7m | Merchant fees $6.48m (0.31%) plus the vendor lines above | **2.90%** |
| Network for Good (CY2024) | $220.1m | Transaction processing $4.46m (2.02%) plus Bonterra | **5.20%** |
| CAF America (FY4/2025) | $993.2m | CyberGrants plus staff (141 employees) | 2.85% |
| Mightycause CF (CY2024) | $99.3m | Transaction costs $1.72m plus the Mightycause fee | 4.48% |
| Givinga Foundation (CY2024) | $11.1m | "Cost of service" $1.12m (10.1%), bank/card fees $84.6k, fraud loss $316k | 14.3% |
| Dechomai Asset Trust (CY2024) | $552.3m | No processing line. The sister Dechomai Foundation pays Charitable Solutions LLC ($4.43m, 2024) | 1.23% |

**Reading the numbers [I].**
- **Two cost structures.**
  - Processors owned by a payments or software parent (PayPal, Blackbaud) show **0.6–1.7%** all-in.
  - Independent foundations that rent a platform (AOGF/Benevity, NfG/Bonterra, Mightycause, FrontStream) show **2.3–10%**.
  - The difference is the platform's take, which Benevity publishes as up to 2.99% per gift.
- **The Benevity take is rising faster than volume.** AOGF grants grew 27% from FY2022 to FY2025, while Benevity's fee grew 86%.
- **Comparison with DAF administration contracts.** RCF paid Renaissance Administration $19.2m and MS GIFT paid RenPSG $14.9m (see `vendor-footprint-990-harvest.md`). That is less than half of AOGF's single Benevity line.
- **Order of magnitude.** On about $4.67bn of grants across AOGF, PayPal CGF, Blackbaud GF, NfG and CAF America in their latest years, identified platform and processing payments are about **$98m (about 2.1%)** [I, sum of the CSV lines above]. The components are AOGF $67.2m, PayPal CGF $12.6m, CAF America $8.3m, NfG $7.0m and Blackbaud GF $3.1m.

---

## 4. P-INF-09: fraud-loss and diversion disclosures

Full rows with object IDs are in `sponsor-fraud-loss-disclosures.csv`.

| Sponsor (type) | Year | Disclosure | Amount | Vector |
|---|---|---|---|---|
| **Givinga Foundation** (National, processor) | CY2024 | Part IX line 24, "External bank fraud loss", 100% management & general. Part VI line 5 = No. No narrative ([amended 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml); [original](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202522379349301497_public.xml)) | **$316,184** (2.41% of revenue; 3.7x its bank/card fees) | Bank, unspecified |
| Prosperity Foundation (Single Issue) | CY2023 | Part VI line 5 = Yes. A $900,000 endowment wire to the Community Foundation for Greater New Haven was diverted by an email impersonating the community foundation; $399,155 recovered ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521259349300817_public.xml)) | $500,845 net | Wire / BEC |
| Horizons Foundation (Single Issue) | FY6/2024 | Part IX line 24, "Cyber Crime Expenses" ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521359349317122_public.xml)) | $249,593 | Cyber, unspecified |
| Washington University | FY6/2024 | Part VI line 5 = Yes. A supplier payment was misdirected by a third party ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202531349349312818_public.xml)) | $565,787 | ACH redirection |
| The Nature Conservancy | FY6/2025 | Part VI line 5 = Yes. A vendor's email was compromised and used to change bank details ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611349349310061_public.xml)) | $524,983 | BEC |
| Community Foundation of North Texas | CY2024 | Part VI line 5 = Yes. Assets were diverted at a closely held equity holding, which was written to zero ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523179349304792_public.xml)) | $3,832,745 | Investee-level |
| Yale; Johns Hopkins | FY2022, FY2024 | Internal employee diversion | $40.5m; $0.506m; $1.76m | Procurement / p-card |
| Chapel & York US Foundation | CY2022 | Part XI line 9, "Fraudulent charges – unrefundable" | $11,251 | Card |

**Bad-debt lines at processors (cause undisclosed; not evidence of fraud):**
- AOGF "Other / bad debts": $5k (FY2022), $28k (FY2023), **$1.00m (FY2024)**, $9k (FY2025).
- PayPal CGF bad debt: $34k, $38k and $1k.
- Pure "write off A/R": $451,732 (2024).
- Charity Bridge Fund credit loss: $12,973.

**Implications [I].**
- **Disclosed external fraud on pass-through rails is rare and small relative to volume.** Givinga's loss is material only because Givinga is small. At AOGF scale, even the FY2024 bad-debt spike is 0.05% of grants.
- **The 990 is a weak detector.** Part VI line 5 targets "diversion", and filers apply it mainly to insider theft and BEC. Card chargebacks and bank-fraud reversals are netted into fees or bad debt.
- **The pattern that is disclosed is payment redirection, not card fraud.** That is the relevant control for any DAF grant-disbursement or agentic payment design (proposal P-PRC-06).
- **Flipcause (§7) shows the larger loss mode is operator insolvency and commingling, not external fraud.**

---

## 5. P-BUY-06: Give Interactive and GiftingNetwork profiles

| | **Give Interactive LLC** | **GiftingNetwork LLC** |
|---|---|---|
| Entity / HQ | EIN 84-4835291; Overland Park, KS (FFTC 990 address) [F] | Morristown, NJ (site footer "© 2026 GiftingNetwork LLC") [F]. A related "GN PBO Company LLC" was paid by JCF San Diego in FY2022 [F] |
| Ownership | **The Signatry Charitable Trust holds 99%**, per Schedule R in every return CY2020–CY2024. The trust is general/managing partner from CY2023 ([990 CY2024](https://projects.propublica.org/nonprofits/organizations/825070897/202543189349315279/full)) [F] | Founder-led. Founder and CEO is Eric Swerdlin, who "founded and led Swerdlin White Huber, acquired by Bank of New York in 1999" ([giftingnetwork.com](https://www.giftingnetwork.com/)) [F, self-described]. ZoomInfo gives a 2016 founding [R, unverified]. Owners otherwise [U] |
| Outside funding | None found [U]. Loss-making: the trust's 990-T books Give partnership losses of −$494,509 (CY2023) and −$2,718,246 (CY2024) [F] | None found. The ZoomInfo funding field is blank ([ZoomInfo](https://www.zoominfo.com/c/giftingnetwork-llc/467181694)) [U] |
| Leadership | CEO Lucas Cherry ([Pulse 2.0, 2026-07-21](https://pulse2.com/give-interactive-launches-fund-of-funds-platform-for-daf-sponsors-and-private-foundations/)) [R]. LinkedIn lists 11–50 staff | Eric Swerdlin |
| Customer count | Not disclosed. The repo timeline tracks 10 sponsors ([`give-interactive-client-timeline.csv`](../../data/mission-2026-11-14/give-interactive-client-timeline.csv)) | Not disclosed. The "200K+ advisors" figure is Orion/Envestnet reach, not customers [F] |
| Named sponsors | **Vanguard Charitable** (announced 2025-11, [PR Newswire](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html)). **WaterStone** cut over 2026-11-01. ImpactAssets in dual tenancy. Minneapolis, Thrivent and Stifel at staging. CCT production host 2025-06-11. The Signatry (affiliate). **Lapsed:** FFTC, OCF, Omaha, EBCF, KZCF, San Diego Foundation (all from `queue-give-interactive-displacement.md`) | **FFTC**: live 2026-07-01, "approximately 3,000 funds", "nearly $5 billion" ([PRLog](https://www.prlog.org/13172546-giftingnetworks-donor-portal-live-at-foundation-for-the-carolinas.html)). **CCT**: portal "Powered by GiftingNetwork" ([donorportal.cct.org](https://donorportal.cct.org/)). **JCF San Diego**: 990 payee FY2022–25 [F]. FY2024 DAFRC DAF assets of these three: $4.65bn + $2.95bn + $0.54bn = **$8.13bn** |
| 990 payments seen | FFTC $654,500 (CY2023, "software") — the only one in the 1,512-sponsor universe | JCF San Diego: $171,500 (FY6/2022, as GN PBO Company LLC); $212,232 (FY2023); $359,535 (FY2024); $191,424 (FY2025) [F]. FFTC and CCT returns after go-live are not yet filed |
| Products | DAF ledger and administration; fund-of-funds multi-layer NAV (2026-07); "Give Legacy Fund" perpetual giving (2026-08-24, per [Windsor Drake](https://windsordrake.com/market-intelligence/product-launches/give-interactive-product-launch-2026-08-24)) [R] | White-label DAF SaaS plus back office; "DAF Network" (custodian-agnostic: Fidelity, Schwab, Goldman Sachs custody); GiftingPension pooled income funds; private-foundation back office. Partners: Charitable Solutions LLC and Planned Giving Interactive ([DAF Network page](https://www.giftingnetwork.com/daf-network.html)) [F] |
| Distribution | Direct to sponsors | Orion, from 2025-08-18 ([Business Wire](https://www.businesswire.com/news/home/20250818952704/en/Orion-and-GiftingNetwork-Partner-to-Enhance-Charitable-Giving-Solutions-for-Advisors-and-Clients)); Envestnet ([integration page](https://www.envestnet.com/integrations/giftingnetwork)) |
| Contract terms | None public [U] | None public [U]. Its site says advisors who introduce sponsors can "earn on that relationship" [F] |

**Assessment as PE add-on targets [I].**
- **They compete head-to-head.** FFTC moved Give → (gap) → GiftingNetwork. At CCT, GiftingNetwork is the incumbent and Give is in implementation. A buyer of either should expect churn among the same top-15 community foundations.
- **Give is not a normal founder-sale target.** Control sits with a charitable trust that also runs a competing sponsor (The Signatry). Any sale is a disposition of charitable assets at fair value, and Vanguard Charitable, as anchor customer, would care about change-of-control terms (see P-GIV-04).
- **GiftingNetwork is a conventional founder-led LLC.** It has advisor-channel distribution and a link to Charitable Solutions LLC, the administrator paid $4.43m by Dechomai Foundation in 2024. Its scale evidence is thin: one 990 payee at about $0.2–0.36m a year.

---

## 6. P-BUY-03: LPL, the Commonwealth Charitable Fund and the LPL RCF channel

- **State on 2026-11-14 [F].**
  - `cfndaf.donorfirstx.com` is live and says "Welcome to your login experience for your Commonwealth Charitable Fund."
  - Its page configuration names program code `CFNDAF` (program_id 680).
  - The page source credits "Renaissance, powered by RenPSG … Renaissance Administration LLC".
  - Its footer reads "Securities and advisory services offered through LPL Financial … Commonwealth is a trade name of LPL Financial."
  - LPL's legacy DAF channel uses the generic RCF portal `rcf.donorfirstx.com`, and RCF must be the account owner ([Ren LPL page](https://www.reninc.com/lpl-rcf-daf/)).
- **Sponsor.** CFN's sponsor is RCF, inferred from CapShift's Commonwealth page (graph edge E034). If that is right, **both LPL-linked programs are the same sponsor on the same Ren stack** [I].
- **Economics.** Commonwealth's former revenue-sharing disclosure was summarised by a search index as "up to 5 basis points … or $5 per quarter" from Renaissance's affiliated administrator. That page now redirects to `lpl.com/commonwealth.html`, which returned 403, so the figure is **not verified first-hand** [R]. LPL's general disclosures do not name Renaissance ([LPL legal disclosures](https://www.lpl.com/disclosures/legal-disclosures.html)) [U]. For context, RCF paid Renaissance Administration $19.2m (see the vendor-footprint note).
- **Timing.**
  - Closing was 2025-08-01 ([SEC 8-K exhibit](https://www.sec.gov/Archives/edgar/data/1397911/000119312525171084/d810447dex991.htm)).
  - On 2026-10-28, LPL said advisor conversion was "two weeks away", with asset retention guided down to about 83% ([WealthManagement](https://www.wealthmanagement.com/ibd-news/lpl-lowers-commonwealth-asset-retention-to-83)) [R].
- **Answer [I].**
  - No public statement says whether LPL will re-bid, merge or keep both.
  - Evidence favours **keeping both in the near term**. The CFN program survived 15 months after closing with LPL legends already applied, and merging two RCF programs would need no vendor or sponsor change.
  - The live risk to Ren is not a re-bid. It is advisor and asset attrition: Commonwealth advisors who left for other broker-dealers take their DAF clients' advice relationships with them. Whether RCF accounts follow is [U].
  - Proposal P-PRC-05 tracks the post-conversion portal.

---

## 7. P-FAIL-05: Flipcause bankruptcy status

Governing corrections W4-10 and W4-11 apply. The Stripe reserve is $1.45M per Flipcause's filings and under $1M (about $790k) per Stripe's objection. Ravyn's testimony that donations belonged to Flipcause is the debtor's position, not a court finding.

| Date | Event | Source |
|---|---|---|
| 2025-11 | California AG cease-and-desist | [CA AG](https://oag.ca.gov/news/press-releases/attorney-general-bonta-warns-fundraising-platform-flipcause-immediately-stop-its) |
| 2025-12-19 | Chapter 11 filed, D. Del. 25-12246 (Judge Thomas M. Horan). Liabilities about $30.5m, including more than $29m owed to about 3,200 nonprofits; cash about $70k | [Doc 228](https://document.epiq11.com/document/getdocumentsbydocket/?docketId=1225685&projectCode=FLX&docketNumber=228); [Oakland Voices 2026-02-25](https://oaklandvoices.us/2026/02/25/flipcause-bankruptcy-sale-nonprofit-repayment-missing-donations/) |
| 2026-01-13/14 | Chapter 11 trustee ordered after the AG's motion; Jeffrey Testa appointed 2026-01-22 | [Bloomberg Law](https://news.bloomberglaw.com/bankruptcy-law/bankrupt-fundraising-platform-flipcause-gets-trustee-takeover); Oakland Voices |
| 2026-01-28 | Creditors' committee formed (Sweet Relief $1.2m, 805 UndocuFund $352.5k and others) | Oakland Voices 2026-02-25 |
| 2026-03-17/18 | Sale to Software4Nonprofits approved for **$400,000**, the only bid | [Oakland Voices 2026-03-09](https://oaklandvoices.us/2026/03/09/flipcause-software4nonprofits-sold-bankruptcy/) |
| 2026-04 | Trustee settlements. **Grand Avenue Investments**: secured claim capped at $825k, $250k paid now, $575k from S4NP revenue share, $375k made unsecured and behind charities, claims against Ravyn assigned to the estate. **Stripe**: about **$550k** to the estate now, Stripe's unsecured claims behind nonprofit repayment. Carve-out reserve: $400k for Chapter 11 professionals and $300k for the Chapter 7 trustee. Objections from nonprofits seeking an accounting of Stripe-held donor funds | [Oakland Voices 2026-04-23](https://oaklandvoices.us/2026/04/23/flipcause-chapter-7-bankruptcy-conversion-lawsuits/) |
| 2026-04-28 | Converted to Chapter 7 "after sale, creditor deal" | [Law360](https://www.law360.com/bankruptcy/articles/2470713) |
| 2026-05-18 | Form 309D notice. Chapter 7 trustee Jeffrey T. Testa (McCarter & English); §341 meeting 2026-06-25; **proof-of-claim deadline 2026-07-07** (government units 2026-10-26) | [Doc 228](https://document.epiq11.com/document/getdocumentsbydocket/?docketId=1225685&projectCode=FLX&docketNumber=228) |
| 2026-05-26 | Creditors' counsel: the trustee "has been given the authority to try to claw back some of that money for the nonprofits"; no recoveries yet | [Boise State Public Radio](https://www.boisestatepublicradio.org/news/2026-05-26/flipcause-bankruptcy-charities-nonprofit-idaho) |

**Answers.**
- **Creditor recoveries [U].** No distribution to nonprofits has been reported through 2026-11-14. A search for Sept–Nov 2026 coverage found nothing new.
  - Arithmetic [I]: known estate inflows are about $0.4m (sale) plus about $0.55m (Stripe), less a $0.7m carve-out and Grand Avenue's $0.25m cash. Before avoidance recoveries, that leaves almost nothing for more than $29m of nonprofit claims.
  - Insider transfers of about $3.8m are the main upside.
- **Ruling on title to donations [U].** No ruling was found. Nonprofits argued constructive trust, which experts called a "long shot", and the judge and the California deputy AG voiced concern about the debtor's ownership claim (Oakland Voices 2026-02-25). Nonprofits are scheduled as **general unsecured creditors**.
- **Stripe reserve.** It was held from 2025-12. A settlement gives the estate about $550k and subordinates Stripe's claim. Whether the court entered the 9019 order is [U] from free sources: Law360's headline cites a "creditor deal", but the text is paywalled.
- **Docket access.** CourtListener's API requires authentication (HTTP 403), and the Epiq docket is a JavaScript application. Only Doc 228 was retrieved directly.

---

## 8. Source register

| ID | Source | Date | Used for |
|---|---|---|---|
| S1 | IRS e-file XML, GivingTuesday mirror (object IDs in both CSVs) | FY2022–25 | §3, §4 |
| S2 | [AOGF 990 FY3/2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202641969349302754_public.xml) | 2026 | Benevity, BlueSnap, merchant fees |
| S3 | [PayPal CGF 990 CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml) | 2025 | Transaction costs |
| S4 | [Givinga 990 CY2024 (amended)](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml) | 2025-11 | Fraud loss |
| S5 | [Benevity Foundations Fees Schedule](https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf) | 2026-10-01 | 2.99% Cause Support Fee; AOGF merchant fees |
| S6 | [PRLog: GiftingNetwork live at FFTC](https://www.prlog.org/13172546-giftingnetworks-donor-portal-live-at-foundation-for-the-carolinas.html) | 2026-09-23 | FFTC go-live |
| S7 | [giftingnetwork.com](https://www.giftingnetwork.com/); [DAF Network](https://www.giftingnetwork.com/daf-network.html) | live 2026-11-14 | GiftingNetwork profile |
| S8 | [JCF San Diego 990 FY6/2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611349349307506_public.xml) | 2026 | GiftingNetwork payee |
| S9 | [Pulse 2.0: Give fund-of-funds](https://pulse2.com/give-interactive-launches-fund-of-funds-platform-for-daf-sponsors-and-private-foundations/) | 2026-07-21 | Give CEO and product |
| S10 | [Windsor Drake: Give Legacy Fund](https://windsordrake.com/market-intelligence/product-launches/give-interactive-product-launch-2026-08-24) | 2026-08-24 | Give product |
| S11 | [Signatry Charitable Trust 990 CY2024](https://projects.propublica.org/nonprofits/organizations/825070897/202543189349315279/full) | 2025 | Give ownership and losses |
| S12 | [cfndaf.donorfirstx.com](https://cfndaf.donorfirstx.com/) | live 2026-11-14 | CFN program |
| S13 | [Ren: LPL RCF DAF](https://www.reninc.com/lpl-rcf-daf/) | live | LPL channel |
| S14 | [WealthManagement: LPL 83% retention](https://www.wealthmanagement.com/ibd-news/lpl-lowers-commonwealth-asset-retention-to-83) | 2026-10-28 | Conversion timing |
| S15 | [Flipcause Doc 228, Form 309D](https://document.epiq11.com/document/getdocumentsbydocket/?docketId=1225685&projectCode=FLX&docketNumber=228) | 2026-05-18 | Case facts |
| S16 | [Oakland Voices 2026-04-23](https://oaklandvoices.us/2026/04/23/flipcause-chapter-7-bankruptcy-conversion-lawsuits/); [2026-02-25](https://oaklandvoices.us/2026/02/25/flipcause-bankruptcy-sale-nonprofit-repayment-missing-donations/); [2026-03-09](https://oaklandvoices.us/2026/03/09/flipcause-software4nonprofits-sold-bankruptcy/) | 2026 | Settlements, sale, committee |
| S17 | [Law360](https://www.law360.com/bankruptcy/articles/2470713); [Bloomberg Law](https://news.bloomberglaw.com/bankruptcy-law/bankrupt-fundraising-platform-flipcause-gets-trustee-takeover); [Boise State Public Radio](https://www.boisestatepublicradio.org/news/2026-05-26/flipcause-bankruptcy-charities-nonprofit-idaho) | 2026 | Conversion, trustee, clawbacks |
| S18 | Washington University, TNC, Prosperity, CFNT, Horizons, Yale and JHU 990s (links in §4 and the CSV) | FY2022–25 | Fraud and diversion |

---

## 9. Data dictionary

### `processor-vendor-economics-990.csv`
| Field | Meaning |
|---|---|
| sponsor_ein, sponsor_name | Filer (DAFRC name where available) |
| dafrc_type, dafrc_subtype | DAFRC classification (`Donation Processor` marks the 22 processors) |
| fiscal_year, tax_period_end, return_object_id | Return identity. The fiscal year follows the harvest convention (period-end year) |
| cost_line_type | `part_vii_b_contractor` (Part VII-B line), `part_ix_line_24_other` (Part IX "other expenses" line matching processing, bank, card, merchant, transaction, distribution, cost-of-service, vetting, bad-debt or fraud terms), or `derived_non_grant_expense` (Part I line 18 minus line 13) |
| payee_or_line | Contractor name or Part IX description, as filed |
| vendor_group, vendor_role | Normalised vendor and role (blank for Part IX lines) |
| services_or_description | Part VII-B services text or Part IX description |
| amount_usd | Amount as filed |
| part_i_grants_paid, sched_d_daf_grants, part_i_contributions, part_i_total_expenses | Same-return context. Blank for vendor rows taken from the earlier harvest at non-processor sponsors |
| pct_of_part_i_grants, pct_of_contributions | amount ÷ context × 100 |
| source_xml_url, filing_page_url | XML on the GivingTuesday mirror; ProPublica page |
| notes | Caveats: amended or duplicate rows (Givinga CY2024 appears twice, so do not sum both), ratios that are not meaningful (Kiva lends rather than grants; wind-down years) |

### `sponsor-fraud-loss-disclosures.csv`
| Field | Meaning |
|---|---|
| category | `explicit_fraud_loss`, `diversion_of_assets` (Part VI line 5) or `bad_debt_cause_undisclosed` |
| form_location | Where on the return the item appears |
| part_vi_line5_diversion_flag | `MaterialDiversionOrMisuseInd` as filed (1/true = Yes) |
| amount_usd, amount_recovered_usd | As disclosed. Blank if not stated |
| rail_or_vector | Payment rail or attack vector as described. "Inferred" where noted |
| total_revenue_usd, amount_pct_of_revenue | Part I line 12 context (blank for universities) |
| processor_relevance | high / medium / low / none: relevance to pass-through DAF rails |
| other fields | As in the economics CSV |

### `queue-proposals-processor-profiles.csv`
Format per [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md). Prefix `P-PRC-`.
