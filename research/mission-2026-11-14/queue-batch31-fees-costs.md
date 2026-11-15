# Adviser fees on DAF assets: AEF's line 11f (P-ADV-02), RIA brochures (P-ADV-01), costs Part IX misses at bank and broker nationals (P-COST-03), California platform registrations (P-B30A-02)

**Date:** 2026-11-15 · **Queue items:** P-ADV-02, P-ADV-01, P-COST-03, P-B30A-02 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs:**
- [`data/mission-2026-11-14/adviser-fee-evidence-2026.csv`](../../data/mission-2026-11-14/adviser-fee-evidence-2026.csv): 28 rows. E01–E21 cover adviser fees; C01–C07 cover the costs Part IX does not show.
- [`data/mission-2026-11-14/queue-proposals-batch31a.csv`](../../data/mission-2026-11-14/queue-proposals-batch31a.csv): P-B31A-01 to P-B31A-03.

**Method and rules.**
- **Sources:** public pages, PDFs and SEC IAPD brochure PDFs only, plus IRS e-file XML from the GivingTuesday mirror.
- **What I did not do:** log in anywhere, submit forms, use registry search tools or contact anyone.
- **Arithmetic:** done in a stdlib script from XML values (Part IX, Schedule D Parts XI–XII, Schedule O, Part VII-B).
- **Recency:** every source is 2023–2026.
- **Labels:** **[F]** first-party document or filing; **[R]** search-engine capture of a page that returned 403; **[3P]** third-party summary; **[C]** my computation; **[I]** my inference.

**Read first and built on:**
- `queue-adviser-fees-pools-npact.md`, with its wave-11 corrections. NPT requires $500k for a discretionary adviser account and $2m for a non-discretionary one. "No numeric cap" is the governing wording.
- `queue-all-in-cost-dafpay-access.md`, with its wave-10 corrections and the adviser-fee update that sets AEF at 0.46%.
- `sponsor-cost-structure-and-sensitivities.md`, with its wave-5 corrections. Operating cost excludes lines 1–4 and 11f.
- `queue-batch30-legal-circulars.md`, with its wave-15 corrections. The DAF-sponsor exclusion conditions are conjunctive, and PL-1 "consulting" means Type E.
- `wealth-captive-terms-2026.csv`.

---

## 0. Headline answers

| Item | Answer | Confidence |
|---|---|---|
| **P-ADV-02: is AEF's line 11f (0.40–0.46%) a fair measure of the adviser fee?** | **It is a fair measure of the average explicit adviser and manager fee paid per AEF dollar. It is not a measure of what a fee-charging AEF account pays.**<br>- **11f is the audited netted amount.** Schedule D Part XII line 4b equals line 11f in every year: $26.37m, $29.49m and $35.95m. So 11f is exactly the investment expense the audit nets inside investment return.<br>- **Per account:** 11f is $1,876 to $2,254 per account (TY2022–24) [F/C].<br>- **AEF publishes no cap.** Fees are "charged directly to the relevant funds", and advisers are paid "via asset management fees or commissions" [F].<br>- **The audit is not public.** It is "available upon request" (Schedule O), and no split between fee-based, commission and fee-free assets is published.<br>- **What 11f leaves out:** commissions and 12b-1 payments embedded in prices or fund expenses, fund expense ratios, and fees that donors pay outside the DAF (Waverly, Pathstone) [I].<br>- **What 11f includes beyond the adviser fee:** sub-manager, SMA and wrap components [I].<br>- **Fee-charging accounts:** if they pay 1.00%, about 46% of AEF assets are in them. At 0.75% the share is about 62% [C]. | Medium (filing mechanics [F]; composition [I]) |
| **P-ADV-01: what RIAs charge on DAF assets** | **I found eight more 2023–26 documents, five of them first-party. The total is now 15. That is far short of 50, because web search reaches few brochures. Two firms now publish a DAF-specific menu.**<br>- **Davenport (RCF private label):** wrap fee of 1.00% on the first $1m and 0.75% above for SMAs, 0.75% for fund or ETF models, and 0.40/0.30/0.20% for fixed income. RCF's admin fee is charged on top (ADV 2024-03-25) [F].<br>- **Tolleson (NPT-administered):** its general schedule of 0.40–1.00% applies [F].<br>- **Hollencrest:** NPT pays it 5–25 bps for administration [F].<br>- **Pathstone:** either bills the DAF account directly or counts the DAF in the household fee base [F].<br>- **Waverly (2025-09):** the sponsor pays from the DAF, or the donor pays outside it, with the rate set at application [F].<br>- **BMO Family Office:** 0.25% flat for NPT [R].<br>- **Commonwealth:** an RCF revenue share of up to 5 bps [R]. | Medium on terms. Low on a "typical" rate |
| **P-COST-03: costs Part IX misses at bank and broker nationals** | **Part IX shows the admin layer but generally not the fees charged inside the investments.**<br>- **MS GIFT:** visible cost is 28 bps. The visible advisory-type lines are 7.8% of the 1.00% advisory ceiling ($6.3m against $80.9m), and the 0.07% MSSB admin fee has no matching line [C/I].<br>- **GS DAF:** visible cost is 28.7 bps, which is close to the admin-fee upper bound of 26.4 bps. GSAM fund expense ratios of 0.62–0.67% are not on the 990 [C].<br>- **BofA CGF:** 11f is 52 bps and is labelled in part as trustee fees. Fund-level costs of about 0.05–0.17 pp are not shown [C].<br>- **Fidelity:** its affiliate Strategic Advisers states that the Charitable Gift Fund's fund expenses "are not separately itemized or billed" [F].<br>- **Raymond James is the exception.** Its Schedule O says 11a and 11f include affiliate investment-management fees (70–72 bps). | Medium (filings and circulars [F]; netting [I]) |
| **P-B30A-02: California platform (PL) registrations** | **This cannot be answered from published AG material.**<br>- The AG's platform pages publish forms and rules, but no list of registrants. Registrations can be seen only through the Registry Search Tool, which is a form, so it was not used.<br>- No DAF-adjacent vendor page I could read discloses a PL number. The reachable pages were Endaoment's terms, Benevity's legal page and GoFundMe's letter to the AG. Every.org, Daffy, Chariot, Givinga and PayPal returned 403 or 404.<br>- One secondary source, an Oakland Voices analysis of the Registry dated 2025-12-13, reports that **Benevity, Blackbaud and PayPal** registered on time in 2024, and that the Registry listed 274 platforms at 2025-11-30 [3P].<br>- No source gives solicitation types (A–E) or any Type E filing by a white-label DAF portal vendor. | High that published sources are silent; low on the substance |

---

## 1. P-ADV-02: AEF line 11f as an adviser-fee measure

### 1.1 What the filings show

| TY | Line 11f | Sch D Part XII line 4b (netted in the audit) | 11f ÷ avg total assets | DAF accounts | 11f per account | Mean DAF balance | Source |
|---|---|---|---|---|---|---|---|
| 2022 | $26,368,782 | $26,368,782 | 39.6 bps | 14,054 | $1,876 | $443k | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202332499349300338_public.xml) |
| 2023 | $29,490,735 | $29,490,735 | 44.0 bps | 14,706 | $2,005 | $483k | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202442479349301654_public.xml) |
| 2024 | $35,948,715 | $35,948,715 | 46.2 bps | 15,947 | $2,254 | $525k | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml) |

**Reading the filings:**
- **Column and reconciliation [F].** All of 11f sits in the program-service column. Audited expenses are $1,328.2m and 990 expenses are $1,364.2m; the difference is exactly 11f.
- **11f is a booked amount [I].** AEF's auditor (RSM appears in Part VII-B for accounting services) records these fees as netted investment expense. They are fees AEF's books see, not an estimate.
- **Fees not booked can't appear.** Anything AEF's books never see cannot be in 11f. That includes fees a donor pays an adviser directly and costs embedded in fund expense ratios or trade prices.
- **Schedule O adds nothing on fees [F].** It contains no fee or adviser text, only that "financial statements ... [are] available upon request". The audit note itself could not be read without a request, which the mission's rules exclude.

### 1.2 AEF's published adviser-fee policy

| Document | What it says | Label |
|---|---|---|
| [2023 Program Description](https://air-original.imgix.net/678d90a0-ec95-45e2-9126-674089482adb.pdf?ixlib=react-9.5.4) | "Professional investment management fees, commissions, transaction expenses, etc. are charged directly to the relevant funds." The admin fee is tiered ("Contact your financial advisor for details"). Pass-through funds pay "up to 1.0%". AEF "accrues no benefits from brokerage services, commissions, finder fees, or product sales" | F |
| [FAQs for Trusted Advisors](https://www.aefonline.org/thought-leadership/faqs-trusted-advisors/) | "Investment advisors receive compensation via asset management fees or commissions in much the same way advisors are paid for managing their client's personal investments." | F (undated) |
| [Referral program](https://www.aefonline.org/thought-leadership/philanthropic-advisory-firm-referral-program/) | Above $250,000, AEF "may allow donors to recommend partial payment from their funds" to philanthropic advisors. Below that, donors pay them directly in full | F (undated) |
| [Investment policy page](https://www.aefonline.org/investments/) | Policy effective 2023-11-17. It covers roles and oversight, with no fee terms | F |
| [One-pager](https://advisorwelcome.aefonline.org/wp-content/uploads/2024/09/AEF_DAFSummaryOnePager_V1.11.pdf) | As of 2023-12-31: 14K DAFs, nearly 6K adviser partners, over 2.5K firms | F |

**No cap, range or default rate is published.** AEF's adviser-fee "policy" is pass-through: whatever the adviser charges its personal clients, in fees or commissions, is charged to the fund.

### 1.3 Is 0.46% fair?

**What pushes the true adviser fee above 11f [I]:**
- Commission-paid advisers. Trade commissions are usually built into cost basis and proceeds, not booked as expense, and 12b-1 trails sit inside fund expense ratios.
- Donor-paid and household billing. Waverly's 2025 brochure lets donors pay outside the DAF; Pathstone counts DAF assets in the household fee base.
- Zero-fee DAFs. These pull the average down, but they are part of the average-dollar measure.

**What pushes 11f above a pure adviser fee [I]:**
- SMA, sub-manager and TAMP fees.
- Wrap-fee custody and trading components.
- Any philanthropic-adviser payments under the referral program, if they are booked as 11f. Their line is not disclosed.

**Sensitivity [C] (TY2024 ratio 0.462%).** The table assumes every other account pays nothing through 11f.

| Fee paid by fee-charging accounts | Share of AEF assets those accounts must hold |
|---|---|
| 0.50% | 92% |
| 0.75% | 62% |
| 1.00% | 46% |
| 1.25% | 37% |
| 1.50% | 31% |

**Verdict:**
- **Average AEF dollar:** use 0.40–0.46% as the fund-borne explicit adviser and manager cost. Treat it as a floor on all-in investment cost, because fund expense ratios and embedded commissions are excluded.
- **Typical fee-charging account:** the evidence fits 0.75–1.00%. The 1.00% illustrative case in `all-in-cost-comparison-2026.csv` remains reasonable for that case.
- **Trend:** the ratio rose 6.6 bps over TY2022–24, while per-account 11f rose 20% and mean balance rose 19% [C].

### 1.4 The same test for RCF (0.23%)

- **Filing [F]:** TY2024 11f is $11,694,030, all in the management column. Schedule D Part XII line 4b nets the same amount, which is 23.2 bps of average assets and $453 per account ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml)).
- **Schedule O [F]:** it says only that Ren keeps the books. It has nothing on fees.
- **Why it stays weak [I]:**
  - RCF combines donor-directed fund-menu accounts with advisor-managed accounts at many brokerages, including the Davenport, UBS, RBC and Ameriprise private labels.
  - Davenport's wrap fee (§2) would be billed at the brokerage. Whether it reaches RCF's books depends on each custodian's arrangement.
- **Conclusion:** keep RCF at "flag only".

---

## 2. P-ADV-01: RIA disclosures added in this batch

| Firm | Sponsor or channel | DAF fee disclosure | Date | Source | Label |
|---|---|---|---|---|---|
| Davenport & Company | RCF (Davenport Donor Advised Program) | **DAF-specific wrap:**<br>- SMAs: 1.00% on the first $1m, 0.75% above.<br>- FundAdvisor, ETF and Charitable Allocation: 0.75%.<br>- Fixed income: 0.40/0.30/0.20%.<br>- Minimums: $50k (models), $1m (SMAs).<br>- "will incur a Renaissance Charitable Foundation annual administration fee" on top. | 2024-03-25 | [ADV 2A (Stephens-hosted copy)](https://www.stephens.com/uploads/shared/transactions-pdf/Davenport-Company-LLC-Form-ADV-2024-0708.pdf) | F |
| Tolleson Private Wealth Mgmt | NPT (Tolleson Donor-Advised Fund) | "NPT has engaged TPWM to provide investment advisory services and manage the underlying assets". General schedule 0.40–1.00% | 2026-01 | [ADV 2A](https://www.tollesonwealth.com/wp-content/uploads/2026/02/Tolleson-Part-2A-of-Form-ADV-January-2026-Final.pdf) | F |
| Hollencrest Capital Mgmt | NPT (administrative services) | "HCM receives 5 to 25 basis points of the total assets introduced to NPT by the third parties". It also "helps to facilitate payments to third-party advisers" | 2025-03-20 / 07-10 | [ADV 2A](https://www.hollencrest.com/wp-content/uploads/2025/10/HCM-ADV-Brochure-Part-2A-20250320-Part-2B-20250710.pdf) | F |
| Pathstone Family Office | DAF sponsors not named | Either an "asset-based advisory fee within the charitable account", or no DAF-specific fee with the DAF included "in the investment advisory client's asset base" | 2025-03-31 | [ADV 2A](https://pathstone.com/wp-content/uploads/2025/10/Pathstone-Family-Office-Part-2A-Form-ADV-03.31.25-1.pdf) | F |
| Waverly Advisors | Fidelity, DAFgiving360 and others | The fee is paid by the sponsor "out of the assets" where sponsor documents contemplate an adviser. Otherwise the donor pays outside the DAF. Rates are "set at the time that the donor advised fund application is completed" | 2025-09-23 | [ADV 2A](https://waverly-advisors.com/wp-content/uploads/Waverly-ADV-Part-2A-Brochure-9.23.2025-FINAL.pdf) | F |
| Strategic Advisers (Fidelity) | Fidelity Charitable pools | The fee is "negotiated on a case-by-case basis" and paid "out of the aggregate NCS administrative services fee" | 2025-03-31 | [IAPD brochure](https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=971078) | F |
| BMO Family Office | NPT (BMO DAF program) | Flat 0.25% a year | 2023-09 | [PDF (403)](https://uswealth.bmo.com/media/uploads/2023/09/05/bmofo-adv-2a_92023_final.pdf) | R |
| Commonwealth Financial | RCF | The RCF administrator shares up to 5 bps (or $5 a quarter on minimum-fee accounts) | live | [page (403)](https://www.commonwealth.com/for-clients/disclosure/revenue-sharing) | R |
| Bay Harbor Wealth Mgmt | DAFgiving360 | DAF advisory up to 1%; admin up to 0.6% | n/d | [getwarmer summary](https://www.getwarmer.com/firms/bay-harbor-wealth-management-llc) | 3P |

**Combined with the seven earlier documents (`adviser-fees-observed-2026.csv`) [I]:**
- **DAF-specific menus:** two firms publish one, Redhawk for DAFgiving360 and Davenport for RCF. Both top out at 0.75–1.00% for equity strategies, with lower fixed-income rates.
- **General schedules:** where the DAF falls under a firm's general schedule, the ceiling is 1.0–2.0%.
- **Payments a donor never sees:** a separate layer of sponsor-paid administration and referral payments runs to NPT and RCF intermediaries. Hollencrest receives 5–25 bps and Commonwealth up to 5 bps. Donors do not see these as adviser fees.
- **Why web search falls short:** it does not reach the long tail of brochures, so the 50-firm target needs an IAPD-driven method. P-ADV-01 stays open, and P-B31A-01 is the complementary sponsor-side route.

---

## 3. P-COST-03: costs Part IX does not show at bank and broker nationals

TY2024 is used unless noted. Basis points are of Part I average total assets. Fee terms come from `wealth-captive-terms-2026.csv` and the cited circulars.

| Sponsor | Visible Part IX (operating cost incl. 11f) | Published donor-borne stack | What is outside Part IX | Source |
|---|---|---|---|---|
| **MS GIFT** (mean account $418k) | 28.1 bps:<br>- RenPSG $14.93m (18.5 bps)<br>- 11f "Morgan Stanley investment advisor" $4.24m (5.2 bps)<br>- "FA commissions and misc." $2.03m (2.5 bps) | - TPA 0.27%, tiering down<br>- MSSB admin 0.07%<br>- Charitable admin ≤0.03%<br>- MS advisory ≤1.00% (part shared with the FA)<br>- Fund and SMA fees | **Advisory fee:** the 1.00% ceiling is $80.9m, and visible advisory-type lines are 7.8% of it.<br>**MSSB admin:** at most $5.7m, with no matching line.<br>**Fund and SMA expenses:** unquantified [C/I] | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml); [circular](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf) |
| **GS DAF** (mean account $3.06m) | 28.7 bps:<br>- 11f 16.4 bps<br>- ex-11f 12.3 bps | - Admin 0.60% marginal, tiering to 0.03%<br>- GSAM funds 0.62–0.67%<br>- Third-party allocation: 0.55% plus 0.30–0.33% expense ratios<br>- Index: 0.10% plus 0.02–0.04%<br>- Passive up to 0.50%<br>- IMAP up to 0.50% plus 0.57–1.03% | **Admin layer:** the upper bound at the mean account is 26.4 bps ($28.6m), close to visible cost, so Part IX shows the admin layer.<br>**Not shown:** all fund expense ratios and IMAP manager fees [C] | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml); [circular (FireAid App. B)](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf) |
| **BofA CGF** (mean account $265k) | 52.0 bps, almost all in 11f:<br>- "Bank of America trustee fees" $9.62m (program column)<br>- $14.44m (management column) | - Admin 0.90–0.10%, flat from the first dollar<br>- 0.12% investment management<br>- Estimated total investment fees 0.17–0.29% | Fund-level costs of about 0.05–0.17 pp [C] | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml); [fee schedule](https://www.bankofamerica.com/content/documents/philanthropic/cgf_fee_schedule.pdf) |
| **Raymond James CEF** (FY Mar-2024) | 72.9 bps (11a + 11f = 69.6) | Schedule O: 11a and 11f "include amounts paid to Raymond James Trust N.A. and Raymond James & Associates ... for managing the investments" | Fund expense ratios only | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202520499349301607_public.xml) |
| **U.S. Charitable Gift Trust** | 98.0 bps; Part VII-B "fundraising" $8.19m (41.7 bps) | Eaton Vance / Morgan Stanley entities provide investment, administrative and fundraising services (Schedule O). No current fee schedule found | Eaton Vance and Calvert fund expense ratios, unquantified | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189349305673_public.xml) |
| **GS Charitable Gift Fund** (FY Jun-2024) | 23.5 bps, no 11f | not retrieved | All investment cost [I] | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511119349301416_public.xml) |
| **Fidelity Charitable** (for reference) | 11a $179.9m; 11f $84.3m; line 24 CIAP-labelled $15.6m (FY Jun-2025) | Strategic Advisers: the CGF "will pay the mutual fund expenses ... These expenses are not separately itemized or billed" | Pool fund expense ratios, by Fidelity's own statement | [IAPD brochure](https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=971078); [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) |

**Reading [C/I]:**
1. **Two different gaps.**
   - **Bank and trust captives** (GS, BofA, RJ) put the admin layer and some affiliate investment fees on Part IX. Only fund-level expense is missing. At BofA that is about 0.05–0.17 pp; at GS it is up to about 0.67 pp in GSAM funds, or more in IMAP.
   - **Broker captives where the FA is paid by an advisory fee** (MS GIFT) show very little of that fee. At MS GIFT up to about 1 pp per dollar may sit outside Part IX.
2. **The nationals-versus-community comparison is not like-for-like.**
   - Community-foundation Part IX operating cost (196 bps median) includes the staff who run their pools. The nationals' 18–66 bps excludes in-fund and in-account investment cost.
   - On the evidence here, a fair all-in comparison adds roughly 5–70 bps for bank captives and up to about 100+ bps for advisory-fee broker accounts.
   - Community-foundation pool fees (11f and in-fund) would also have to be added to their side.
   - These are bounds, not point estimates. A pool-weighted calculation is proposed as P-B31A-02.
3. **Schedule D Part XI/XII flags netting only sometimes.**
   - AEF, RCF and RJ report the 11f add-back; MS GIFT, GS DAF and BofA report none.
   - So the absence of a reconciling item does not prove that no fees were netted [I].

---

## 4. P-B30A-02: California charitable fundraising platform registrations

| Check | Result | Source | Label |
|---|---|---|---|
| AG platforms page | Forms PL-1 to PL-4, regulations and FAQs. **No list of registered platforms.** Filing moved to the new Online Filing Service (late August 2026) | [oag.ca.gov/charities/pl](https://oag.ca.gov/charities/pl) (read 2026-11-15) | F |
| AG Registry statuses page | Defines entity and registration statuses for the Registry **Search Tool**. No downloadable list | [oag.ca.gov/charities/content/info](https://oag.ca.gov/charities/content/info) | F |
| Registry Search Tool | Form-based; **not used** (mission rule) | — | — |
| Vendor pages | No PL number or CFP-registration statement found on the pages that loaded: Endaoment terms, Benevity legal, and GoFundMe's 2026-03 reply to the CA AG multistate letter, which describes PayPal Giving Fund disclosures but no registration number. Every.org terms and disclosures, PayPal Giving Fund policies (403), and Daffy, Chariot and Givinga terms (404) could not be read | [Endaoment](https://endaoment.org/terms); [Benevity](https://benevity.com/legal); [GoFundMe letter](https://www.gofundme.com/c/wp-content/uploads/2026/03/Response-CA-AG-Multistate-Letter.pdf) | F (absence) |
| Secondary analysis of the Registry | "The Registry listed 274 charitable fundraising platforms as of Nov. 30, 2025". Benevity, Blackbaud and PayPal registered on time in 2024; Bonterra (after buying OneCause) is among those with no annual report. Daffy, Every.org, Chariot, Endaoment, Givinga and Ren are not mentioned | [Oakland Voices, 2025-12-13](https://oaklandvoices.us/2025/12/13/california-donation-fundraising-platform-compliance-attorney-general/) | 3P |

**Conclusion:**
- **Not answerable from published sources.** The question cannot be answered from published AG lists or PDFs, because none exist for platforms, or from vendor disclosures, because none were found.
- **What the record shows:** the only registration facts are third-party reports that Benevity and Blackbaud registered. Benevity is in the queue's candidate list; Blackbaud is DAF-adjacent through its legacy DonorCentral business.
- **What remains unknown:** solicitation types and any Type E (consulting) registration by a white-label DAF portal vendor.
- **What it would take:** a person viewing Registry records, or a records request. Both are outside this mission's rules, so the item should be closed as "blocked by method", not retried.

---

## 5. Suggested repo updates (not applied)

1. **`all-in-cost-comparison-2026.csv`, AEF rows 23–25.**
   - Keep the 0.46% "average dollar" basis.
   - Add a note: "11f = audit-netted fees (Schedule D Part XII line 4b). It excludes embedded commissions, fund expense ratios and donor-paid fees. A fee-charging account most likely pays 0.75–1.00%."
2. **`adviser-fees-observed-2026.csv`.**
   - Add Davenport, Tolleson, Hollencrest, Pathstone, Strategic Advisers, and BMO (R).
   - Replace the Waverly 2025-03-28 URL with the 2025-09-23 version.
3. **`sponsor-cost-structure-and-sensitivities.md` §4.3.** Footnote that national Part IX ratios exclude in-fund and in-account investment cost. Cite C01–C07 in the new CSV.
4. **P-B30A-02.** Change the state to "blocked by method (registry is form-only)".

---

## 6. Source register

| ID | Source | URL | Date | Label |
|---|---|---|---|---|
| S01 | AEF Form 990 TY2024 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml | filed 2025 | F |
| S02 | AEF Form 990 TY2023 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202442479349301654_public.xml | filed 2024 | F |
| S03 | AEF Form 990 TY2022 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202332499349300338_public.xml | filed 2023 | F |
| S04 | AEF 2023 Program Description | https://air-original.imgix.net/678d90a0-ec95-45e2-9126-674089482adb.pdf?ixlib=react-9.5.4 | 2023 | F |
| S05 | AEF FAQs for Trusted Advisors | https://www.aefonline.org/thought-leadership/faqs-trusted-advisors/ | live, undated | F |
| S06 | AEF philanthropic advisory referral program | https://www.aefonline.org/thought-leadership/philanthropic-advisory-firm-referral-program/ | live, undated | F |
| S07 | AEF investments / policy page | https://www.aefonline.org/investments/ | policy eff. 2023-11-17 | F |
| S08 | AEF one-pager | https://advisorwelcome.aefonline.org/wp-content/uploads/2024/09/AEF_DAFSummaryOnePager_V1.11.pdf | PDF 2024-05-03 | F |
| S09 | RCF Form 990 TY2024 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml | filed 2025-11-14 | F |
| S10 | Davenport ADV 2A | https://www.stephens.com/uploads/shared/transactions-pdf/Davenport-Company-LLC-Form-ADV-2024-0708.pdf | 2024-03-25 | F |
| S11 | Tolleson ADV 2A | https://www.tollesonwealth.com/wp-content/uploads/2026/02/Tolleson-Part-2A-of-Form-ADV-January-2026-Final.pdf | 2026-01 | F |
| S12 | Hollencrest ADV 2A/2B | https://www.hollencrest.com/wp-content/uploads/2025/10/HCM-ADV-Brochure-Part-2A-20250320-Part-2B-20250710.pdf | 2025 | F |
| S13 | Pathstone ADV 2A | https://pathstone.com/wp-content/uploads/2025/10/Pathstone-Family-Office-Part-2A-Form-ADV-03.31.25-1.pdf | 2025-03-31 | F |
| S14 | Waverly ADV 2A | https://waverly-advisors.com/wp-content/uploads/Waverly-ADV-Part-2A-Brochure-9.23.2025-FINAL.pdf | 2025-09-23 | F |
| S15 | Strategic Advisers ADV 2A (IAPD) | https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=971078 | 2025-03-31 | F |
| S16 | BMO Family Office ADV 2A | https://uswealth.bmo.com/media/uploads/2023/09/05/bmofo-adv-2a_92023_final.pdf | 2023-09 | R (403) |
| S17 | Commonwealth revenue-sharing disclosure | https://www.commonwealth.com/for-clients/disclosure/revenue-sharing | live | R (403) |
| S18 | Bay Harbor summary | https://www.getwarmer.com/firms/bay-harbor-wealth-management-llc | n/d | 3P |
| S19 | MS GIFT 990 TY2024 XML; Donor Circular | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml ; https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf | 2025; Aug 2024 | F |
| S20 | GS DAF 990 TY2024 XML; circular (FireAid App. B) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml ; https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf | 2025 | F |
| S21 | BofA CGF 990 TY2024 XML; fee schedule | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml ; https://www.bankofamerica.com/content/documents/philanthropic/cgf_fee_schedule.pdf | 2025; 2024 | F |
| S22 | Raymond James CEF 990 FY Mar-2024 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202520499349301607_public.xml | 2024 | F |
| S23 | U.S. Charitable Gift Trust 990 TY2024 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189349305673_public.xml | 2025 | F |
| S24 | GS Charitable Gift Fund 990 FY Jun-2024 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511119349301416_public.xml | 2025 | F |
| S25 | Fidelity Charitable 990 FY Jun-2025 and FY Jun-2024 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml | 2026; 2025 | F |
| S26 | CA AG Charitable Fundraising Platforms page | https://oag.ca.gov/charities/pl | live 2026-11-15 | F |
| S27 | CA AG Registry statuses | https://oag.ca.gov/charities/content/info | live | F |
| S28 | Oakland Voices Registry analysis | https://oaklandvoices.us/2025/12/13/california-donation-fundraising-platform-compliance-attorney-general/ | 2025-12-13 | 3P |
| S29 | GoFundMe response to CA AG multistate letter | https://www.gofundme.com/c/wp-content/uploads/2026/03/Response-CA-AG-Multistate-Letter.pdf | 2026-03 | F (vendor) |
| S30 | Endaoment terms; Benevity legal | https://endaoment.org/terms ; https://benevity.com/legal | live | F |
| S31 | Repo cost extract | data/mission-2026-11-14/sponsor-cost-structure.csv | TY2022–25 | F (derived) |

---

## 7. Data dictionary: `adviser-fee-evidence-2026.csv`

| Column | Meaning |
|---|---|
| evidence_id | E = adviser-fee evidence (P-ADV-01/02); C = costs not shown in Part IX (P-COST-03) |
| queue_item | Queue item(s) the row answers |
| sponsor | DAF sponsor the evidence concerns |
| program_or_channel | Program, private label or account type |
| entity | RIA or firm; "(sponsor-wide)" for 990 aggregates; "(program rule)" for sponsor rules |
| evidence_type | `ADV 2A`, `990 Sch D Part XII`, `990 ratio`, `990 Part IX`, `990 Schedule O`, `program document`, `sponsor web page`, `sizing`, `sensitivity`, `third-party ADV summary`, `firm disclosure page` |
| finding | What the source says (quotes ≤40 words) or what was computed |
| metric_value / metric_unit | Headline number and its unit. Blank where the finding is qualitative |
| period | Tax year, fiscal year or document period |
| source_url | Primary URL(s), separated by " ; " |
| source_date | Cover date, PDF date or filing year |
| evidence_label | F / R / 3P / C / I, as defined at the top. "F / C" means a filed number with my arithmetic |
| retrieved | Date read (2026-11-15) |
| notes | Caveats and cross-references |

Ratios use Part I average total assets. Accounts and DAF assets are Schedule D year-end figures from `sponsor-cost-structure.csv`. The GS admin-fee bound applies the marginal schedule to the mean account. Because the schedule is concave, this bounds the aggregate from above (Jensen's inequality), ignoring minimum fees.

## Validation corrections (wave 16, 2026-11-15) — governing
Source: [validation-wave16-report.md](validation-wave16-report.md); register `data/mission-2026-11-14/validation-register-wave16.csv`.

1. **Line 29 (§0, P-ADV-02).** Replace "Schedule D Part XII line 4b equals line 11f in every year" with "Schedule D Part XII line 4a ('investment expenses not included on Form 990, Part VIII, line 7b') equals line 11f in every year".
2. **Line 40 (§1.1 table header).** Replace "Sch D Part XII line 4b (netted in the audit)" with "Sch D Part XII line 4a (netted in the audit)".
3. **Line 93 (§1.4).** Replace "Schedule D Part XII line 4b nets the same amount" with "Schedule D Part XII line 4a nets the same amount".
4. **Line 175 (§5 item 1).** Replace "(Schedule D Part XII line 4b)" with "(Schedule D Part XII line 4a)". Part XII line 4b is "Other": BofA CGF's TY2024 Schedule O uses it for "RECOVERIES … GRANT ADJ" [V wave 16].
5. **Line 106 (§2, Davenport row).**
   - Replace: "Minimums: $50k (models), $1m (SMAs)."
   - With: "Minimums: $50k (allocation models and the FundAdvisor/ETFAdvisor SMA models), $1m (Core Leaders, Value & Income, Equity Opportunities and Fixed Income SMAs)."
