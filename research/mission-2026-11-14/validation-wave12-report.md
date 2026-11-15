# Validation wave 12: NPT GivingPoint, Fidelity stack, nonprofit-side panel, ledgers, NPact owner

Validator: independent-validation-agent-wave12. Date: 2026-11-15. Register: [`data/mission-2026-11-14/validation-register-wave12.csv`](../../data/mission-2026-11-14/validation-register-wave12.csv) (27 rows).

Method: I formed each verdict from primary sources first: live HTTP fetches and JS bundles, DNS over HTTPS, IRS e-file XML, charity accounts, sponsor PDFs and pages, Texas Comptroller data, and vendor pages. Only then did I read `queue-npt-givingpoint-fidelity-stack.md`, `queue-nonprofit-side-panel.md` and `queue-ledger-segment-npact-owner.md`. I did no outreach, no logins and no authentication attempts.

## Verdicts

| Claim | Verdict | Key finding |
|---|---|---|
| V12-01 13 GivingPoint sites on Ren | **Confirmed, with a DNS nuance** | All 13 sites return 200 with the same IIS-served Angular build. All 13 share WAF id `55fe72368c58/bd2698c5ab04` and have `renpsg.atlassian.net` links in their bundles. Only **8** resolve to the `ren-workload-02` ELB. **5** sites resolve to the Global Accelerator pair 13.248.164.2 / 35.71.183.32: Tolleson, Pitcairn, Transatlantic, Rathbones and ICGF. The NPT sponsor text sits in the JS bundle, not in the server HTML. Transatlantic's copyright names "NPT Transatlantic Limited", not NPT or NPT UK. The claim's list of names also leaves out jpmgiving.org, icgfdaf.org and nptgivingpoint.org. |
| V12-02 NPT IT $5.87m (+$2.22m); no Ren payee; NPT UK tech from NPT US | **Confirmed, except the NPT UK wording** | IT spend was $5,871,282 in FY6/2025 and $3,649,680 in FY6/2024, a rise of $2,221,602. Neither 990 mentions Ren, Stellar or iPhi. NPT UK's 2025 accounts name **two** providers: NPT Transatlantic and NPT US. |
| V12-03 Fidelity $0 IT, 0 employees, FMR SA | **Confirmed** | IT spend $0. Employees 0. Schedule O lists FMR services as "RECORD-KEEPING, SYSTEMS, ADMINISTRATION…". FMR was paid $159,901,679. 73 contractors were paid more than $100k. |
| V12-04 Nonprofit-side panel | **Confirmed** | Fidelity: EFT is free and "not currently" required, but Fidelity is "transitioning grant payments to EFT". Minimum grants: Fidelity $50, DAFgiving360 $50 (from the 2024 policies), NPT $250, MS GIFT $250 (from a search capture), Vanguard $500 (policies dated Jan 9, 2026). Benevity's schedule (Oct 1, 2026) matches the claim exactly. |
| V12-05 NPT no ACH / PayPal; Vanguard PayPal | **Confirmed** | NPT's guide has PDF metadata dated 2026-10-15 but sits at a `/2024/09/` URL. It says "At this time, NPT does not issue payments via ACH transfer". The live Vanguard text reads "now issuing Grant Payments with PayPal". |
| V12-06 AEF DonorCentral → NPact; wildcard | **Confirmed** | Random subdomains return the identical 4,971-byte shell from the same IP. The bundle calls three `*.donor.npact.com` hosts and the `npact-auth` Auth0 tenant. The bundle is generic, so it shows nothing about AEF specifically. |
| V12-07 Ledger families | **Mostly confirmed. NYCT is weak** | Dayton is in the Fund 360 image, which I viewed. Arizona's case study says "legacy, on-premises Blackbaud FIMS". Vermont and JCF San Diego both moved off FIMS. California CF rests on Financial Edge listed as a "preferred" skill in job postings. For NYCT, the only primary text I could read is a "preferred" skill. The "transitioning" sentence is an [R] capture I could not open (403). |
| V12-08 NPact owner signals | **One contradicted, one date wrong** | **BroadWest is not "active".** The Comptroller account status shows Right to Transact "NOT ESTABLISHED" and SOS "NOT REGISTERED". Its dataset code is `U`, not `A`. The "Active Franchise Taxpayers" dataset also holds about 465k forfeited (`N`) rows, so being listed in it does not mean active. The privacy policy carries "Updated January 28, 2026" (not 01-27) and "Last updated August 19, 2026". Hurlock as CEO and the Cambria listing (Dallas, TX) are both confirmed. |

## Side findings

- NPT's guide gives two different account floors: $2,500 in "Grant Minimum" and $1,000 in "Account Balance Minimum for Grants".
- NPT's FY2025 990 reports 9 contractors paid more than $100k, down from 18 in FY2024.
- Cambria places NPact in Dallas, TX. NPact's privacy policy places it in Wakefield, MA.

## Exact corrections

### `research/mission-2026-11-14/queue-npt-givingpoint-fidelity-stack.md`

- §P-REN-03 census (line 30) and §P-QA1-02 (line 37): replace "Every live site is either on the `ren-workload-02` ELB or on the iPhi Global Accelerator pair" with "8 live sites resolve to the `ren-workload-02` ELB (44.223.132.165 / 54.88.200.68). 5 (Tolleson, Pitcairn, NPT Transatlantic, Rathbones, ICGF) resolve to an AWS Global Accelerator pair (13.248.164.2 / 35.71.183.32) whose reverse DNS is generic AWS. Its attribution to Ren/iPhi is [I], from the identical build, the shared WAF id and the Ren Jira links." Make the same change to "Ren operates the AWS layer (WAF, ELB, Global Accelerator)": mark Global Accelerator as [I].
- Line 62 (method) and the `hosting_observed` dictionary entry (line 215): rename "iPhi Global Accelerator pair" to "Global Accelerator pair (Ren/iPhi attribution inferred)".
- Line 166 (b): replace "both buy technology *from* NPT US" with "NPT UK's 2025 accounts say administration, MIS and technology are provided by NPT Transatlantic **and** NPT US. Transatlantic's accounts say they are provided by Buzzacott LLP and NPT US."
- Line 168: replace "its UK accounts say technology is provided *by NPT US*" with "its UK accounts say technology is provided by NPT Transatlantic and NPT US (NPT US is Transatlantic's sole shareholder)".
- Sponsor-text criterion (line 60): add "(rendered client-side from the bundle; Transatlantic's copyright names NPT Transatlantic Limited, charity 1153376)".

### `research/mission-2026-11-14/queue-nonprofit-side-panel.md`

- Line 32 (P-BNK-05): replace the quote "is now issuing grants through PayPal" with the live text "is now issuing Grant Payments with PayPal" ([Vanguard](https://www.vanguardcharitable.org/nonprofit-organizations), fetched 2026-11-15).
- Line 91: replace "**No sponsor requires EFT.**" with "**No sponsor checked requires EFT today.** Fidelity says it does 'not currently require EFT' but is 'transitioning grant payments to EFT' under a digital-first policy."
- Line 110: add "(2024 policy document; no 2025/26 version checked)" after the DAFgiving360 $50 cite.
- Line 111: replace "MS GIFT: $250 (repo)" with "MS GIFT: $250 ([MS GIFT FAQ](https://www.morganstanley.com/gift), search capture 2026)".
- Lines 97 and 157 (NPT guide cite): add "URL path is /2024/09/ but PDF metadata is 2026-10-15".

### `research/mission-2026-11-14/queue-ledger-segment-npact-owner.md`

- Line 33 (P-ADV-04 signal 1) and line 158: replace "BroadWest Partners LLC is still an active Texas franchise taxpayer" with "BroadWest Partners LLC still has a Texas franchise-tax account (taxpayer 32086573816, FEI 842739126, 5580 Peterson Ln Ste 200, Dallas). Its Comptroller status is **Right to Transact: NOT ESTABLISHED; SOS: NOT REGISTERED** ([Comptroller](https://comptroller.texas.gov/data-search/franchise-tax/32086573816)), and its dataset code is `U`, not `A`. The 'Active Franchise Taxpayers' dataset includes forfeited (`N`) and `U` rows, so being listed in it does not show active status." Downgrade signal (1) from evidence of continuing ownership to "an entity record exists".
- Line 162: replace "Privacy Policy (updated 2026-01-27)" with "Privacy Policy (update of January 28, 2026; current version 'Last updated August 19, 2026')".
- Line 31, line 84, line 130 and line 141 (NYCT): mark "migration in progress" as resting on an [R] capture (philanthropynewyork.org, 403). The only primary text read, the JobTarget posting of 2026-08-01, lists Sage Intacct/Salesforce as a "preferred" skill. Lower NYCT to **low-medium** and do not count it in the SF_INTACCT $2.32bn family total without a caveat.
- Line 144 (California CF): replace "(posted 2026-06-25)" with "(posted 2026-06-08 per job id and search captures)", and add "Financial Edge appears only as a 'preferred' skill".
- Line 160: add "Cambria gives the location as Dallas, TX. NPact's privacy policy gives Wakefield, MA."

### `data/mission-2026-11-14/npt-givingpoint-programs-2026.csv`

- `hosting_observed` for GP04, GP08, GP09, GP11 and GP12: replace "AWS Global Accelerator pair 35.71.183.32 / 13.248.164.2 (iPhi IPs)" with "AWS Global Accelerator pair 35.71.183.32 / 13.248.164.2 (generic AWS reverse DNS; Ren/iPhi attribution [I] from shared build, WAF id and Ren Jira link)".

## Sources (primary, fetched 2026-11-15)

- The 13 GivingPoint bundles (URLs in the register); [dns.google](https://dns.google/resolve?name=www.jpmgiftfund.org&type=CNAME)
- NPT 990 XML [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml) and [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml); Fidelity [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml)
- NPT UK and NPT Transatlantic 2025 accounts ([1181128](https://opencharities.uk/ew/1181128/files/2025-06-30-accounts.md), [1153376](https://opencharities.uk/ew/1153376/files/2025-06-30-accounts.html))
- [NPT guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf); [Fidelity FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html); [Vanguard nonprofits](https://www.vanguardcharitable.org/nonprofit-organizations) and [policies](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines); [Benevity fees](https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf); [DAFgiving360 2024 policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf)
- [aef.donorcentral.com bundle](https://aef.donorcentral.com/main.18637f992cb04132.js)
- [Foundation Partners products-1](https://fdnpartners.com/products-1); [JCF SD story](https://fdnpartners.com/jewish-community-foundation-success-story); [ACF case study](https://www.casestudies.com/company/sage-intacct/case-study/community-foundation-saves-over-24k-with-sage-intacct); [VCF portal](https://vermontcf.org/donor-portal/); [NYCT JobTarget](https://www.jobtarget.com/jobs/jt-ytfwftg0iq/director-investment-operations-and-treasury-new-york-city-new-york)
- [Texas Comptroller status](https://comptroller.texas.gov/data-search/franchise-tax/32086573816); [data.texas.gov](https://data.texas.gov/resource/9cir-efmm.json?taxpayer_number=32086573816); [NPact privacy](https://npact.com/privacy-policy/); [NPact about](https://npact.com/about/); [Cambria](https://cambriagroup.com/portfolio/npact)
