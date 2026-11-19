# Second-source pass on the gap audit's headline single-source claims (P-GAP19-03)

**Date:** 2026-11-19. **Queue item:** P-GAP19-03. **Scope:** claims C01–C10 in [thoroughness-gap-audit-2026-11-19.md](thoroughness-gap-audit-2026-11-19.md) §3, plus C12, C16–C19 from C11–C20. C11, C13–C15 and C20 were not attempted.

**Method and limits.**
- I used public sources only. I did no outreach, logins or form submissions.
- I read each host's robots.txt before fetching from it. A robots.txt that returned 404 was treated as having no rules. Three hosts returned 403 for robots.txt, so I fetched nothing from them: `www.dafgiving360.org`, `www.schwabcharitable.org` and `reports.adviserinfo.sec.gov`.
- `www.reninc.com` started returning 403 to page requests partway through the session. I stopped fetching from it.
- I did not use crt.sh. The certificate-log part of C03 is left to the sibling crt.sh re-sourcing pass.
- My attempt to query SEC EDGAR full-text search (`efts.sec.gov`) was blocked by this session's permission controls, so C04's SEC-exhibit route was covered only by web search.
- **Recency:** every new source is dated 2021 or later.
- Machine-readable version: [`gap19-second-source-pass.csv`](../../data/mission-2026-11-14/gap19-second-source-pass.csv).

**Verdict key.**
- **corroborated:** an independent primary document confirms the claim.
- **partly:** a new primary document confirms part of the claim, or narrows it.
- **contradicted:** a new primary document contradicts the claim.
- **still single-source:** no independent document was found, so the claim should carry its basis label.

## 1. Results in brief

| Verdict | Claims |
|---|---|
| Corroborated | C08 (DAFgiving360 fees), C10 (RCF sponsors the Commonwealth Charitable Fund), C18 (AG action on SPLC holds), C19 (DAF-to-DAF volume, order of magnitude) |
| Partly | C05 (no sponsor-side AI), C06 (Daffy part only), C07 (SOC 2 type drift, now three statements), C09 (Edward Jones confirms an unnamed third-party administrator) |
| Still single-source | C01 (NPT on Ren), C02 (Give Interactive at Vanguard Charitable), C03 (Give "$40B+"; the non-crt.sh part), C04 (contractual closure), C16 and C17 (no CY2025 990s posted yet) |
| Contradicted | none |
| Internal fix only | C12 (a stale range sits beside the repository's own map) |

Two findings change the headline documents:
1. **C10 is already confirmed in the repository, but the report and synthesis still say "inferred".** The Commonwealth program circular and the West Virginia charity registry both name RCF as sponsor. Batch work had already upgraded edge E034 to EF001 ([queue-vendor-channel-moves.md](queue-vendor-channel-moves.md) §1). The report's §2.2 sentence and synthesis line 73 were never updated.
2. **C02 rests on a release that Give Interactive itself issued.** The PR Newswire record reads "news provided by Give Interactive" and ends "SOURCE Give Interactive". Vanguard Charitable's FY2026 audited statements (FYE 2026-06-30, subsequent events reviewed through 2026-10-05) do not mention Give Interactive, a recordkeeping change or any software commitment. Top-10 finding #10 should therefore carry a vendor-claim label.

## 2. Claim table

| # | Original claim (governing doc) and its source | New source(s) checked (date) | What the new source says | Verdict |
|---|---|---|---|---|
| C01 | About 28% of FY2024 DAF assets use Ren, and nearly half of that is NPT, on hosting evidence (report §3; FINAL-STATUS #4; synthesis A4 and #7). Source: [validation-wave3-report.md](validation-wave3-report.md) hosting evidence. | (a) [NPT Terms of Use/Privacy Policy](https://www.nptrust.org/privacy-policy/), "Last Updated: October 29, 2026"<br>(b) [NPT "Five Things to Know about NPT GivingPoint"](https://www.nptrust.org/philanthropic-resources/philanthropist/five-things-to-know-about-npt-givingpoint-a-conversation-with-chris-adams-svp-of-it-solutions-and-cybersecurity/) (2021-02-12)<br>(c) [NPT Form 990 FY2025, Part VII-B](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/full), via the repo harvest<br>(d) [NPT "For Financial Institutions"](https://www.nptrust.org/advisors-and-institutions/for-financial-institutions/) (accessed 2026-11-19)<br>(e) web search for NPT on reninc.com | (a) The policy names no processor or technology vendor. Data is shared with "financial service partners, associated organizations and agents" and with "employees, agents, contractors and other third parties on a 'need to know' basis".<br>(b) GivingPoint is "the result of a two-year development and implementation project" and is "built using modern APIs". No builder is named.<br>(c) Nine contractors were paid over $100k. Ren is not among the five listed, and the fifth is paid $220,927. If Ren were reported as an independent contractor, it received at most $220,927; more likely it is booked elsewhere (see [queue-npt-givingpoint-fidelity-stack.md](queue-npt-givingpoint-fidelity-stack.md) §4).<br>(d) The page markets "enterprise-scale infrastructure" and names no vendor.<br>(e) No Ren page naming NPT was found. | **Still single-source** (hosting inference) |
| C02 | Give Interactive holds Vanguard Charitable's DAF recordkeeping (report §2.1 and wave-3 note; FINAL-STATUS #10; synthesis #8). Source: [Give Interactive release](https://www.giveinteractive.com/post/vanguard) (2025-11-04). | (a) [PR Newswire record of the release](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html) (2025-11-04)<br>(b) [Vanguard Charitable FY2026 audited financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf) (FYE 2026-06-30; subsequent events to 2026-10-05)<br>(c) [Vanguard Charitable privacy policy](https://www.vanguardcharitable.org/company-policies/privacy-policy) (Last Updated 2023-05-16) | (a) The release says "news provided by Give Interactive" and "SOURCE Give Interactive". It quotes CIO Chris Bennett. Its only scope wording is "to modernize and scale its donor-advised fund recordkeeping function". It gives no go-live date.<br>(b) No mention of Give Interactive, a platform change or a software commitment. Software capitalised in FY2026 and FY2025 was $0. The related-party note says The Vanguard Group still provides "investment recordkeeping and administrative services" for $4,243,096 (FY2025: $4,014,052). Program expenses rose from $26.35m to $34.46m (+30.8%) and management and general from $8.59m to $11.33m (+31.9%). Both are consistent with an implementation but do not prove one.<br>(c) The policy names no vendors; it refers only to "third-party technology vendors". | **Still single-source** (vendor-issued release with a counterparty quote) |
| C03 | Give's "$40B+" matches its known clients: $41.80bn, or $32.59bn without certificate-log hosts (synthesis §C and vendor concentration). | (a) [Give Interactive homepage](https://www.giveinteractive.com/) (accessed 2026-11-19)<br>(b) repo [`form990-contractors-harvest-full.csv`](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv) (5,074 payee lines, TY2021–25) | (a) Still says "Powering philanthropic organizations across $40+ billion in charitable assets".<br>(b) Only one sponsor 990 names Give Interactive as a top-5 contractor: Foundation for the Carolinas, CY2023, $654,500 ([990](https://projects.propublica.org/nonprofits/organizations/566047886/202433209349318318/full)). FFTC is a lapsed client. Vanguard Charitable's $27.01bn is 83% of the $32.59bn and rests on C02. The crt.sh part was not examined (sibling pass). | **Still single-source** (vendor claim; depends on C02) |
| C04 | Donor data and automation are contractually closed (top-10 #1). Source: public vendor templates and donor terms. | (a) web search of SEC exhibits for DAF services agreements<br>(b) [Commonwealth Charitable Fund program circular](https://cfndaf.donorfirstx.com/pdf/CFNDAF/Program%20Circular.pdf) (Last-Modified 2024-12-13) | (a) No executed DAF platform or administration agreement was found in SEC exhibits. The hits were mutual-fund and adviser agreements, for example [FS Specialty Lending Fund advisory agreement](https://www.sec.gov/Archives/edgar/data/2065812/000110465925103244/tm2529568d1_ex10-1.htm) (2025-10-28), which is unrelated. EDGAR full-text search could not be run.<br>(b) RCF "has retained RenPSG … to perform certain accounting and administrative functions". This confirms that a contract exists but says nothing of data or automation terms. | **Still single-source** (inference from templates) |
| C05 | No public evidence of AI in sponsor-side approval or eligibility (report §7; synthesis §B). | (a) [Fidelity Charitable "Grant review and due diligence process"](https://www.fidelitycharitable.org/faqs/all/grant-review-due-diligence-process.html) and [granting due diligence](https://www.fidelitycharitable.org/legal/granting-due-diligence.html) (© 2026)<br>(b) [Fidelity Charitable privacy policy](https://www.fidelitycharitable.org/legal/privacy-policy.html)<br>(c) Vanguard Charitable privacy policy (2023-05-16)<br>(d) NPT terms and privacy (2026-10-29) | (a) "a team of experts following a due diligence process for each grant recommendation". The review "takes into consideration data from a variety of sources, ranging from IRS databases and public records regarding litigation and governmental proceedings". No AI or automation is mentioned.<br>(b) and (c) No mention of AI, machine learning or automated decisions.<br>(d) AI appears only as a prohibited use of site content ("generative artificial intelligence ('AI') tool … training"), plus the data-subject right "not to be subject to automated decision making and profiling". DAFgiving360 was not checked (robots.txt 403). | **Partly** (the absence holds across three of the four largest sponsors' first-party policy pages; it is still an absence finding) |
| C06 | Daffy's MCP server exposes `make_donation` with no documented cap; TIFIN Louise executes donor requests (report §7). | (a) [Daffy MCP docs](https://docs.daffy.org/agents/mcp), re-read 2026-11-19<br>(b) [Daffy AI Agents overview](https://docs.daffy.org/agents) (2026-11-19)<br>(c) [TIFIN Louise launch on tifin.com](https://tifin.com/news/tifin-give-launches-louise-the-ai-platform-for-philanthropy/19124/) (seen in search, 2025-10-27) | (a) The tool list reads "make_donation Donate to a charity by EIN. Moves real money". It warns that an API key "can move money in your fund". No amount limit, daily cap or confirmation step is documented.<br>(b) No limits are documented.<br>(c) The only first-party description of Louise is TIFIN's own release. No help-centre or ADV disclosure was found. | **Partly** (Daffy re-confirmed in its own primary docs; Louise is still vendor-only) |
| C07 | Ren SOC 2 is "Type 2" (Jul 2025) and "Type 1" (Apr 2026) (report §5; synthesis risk table; FINAL-STATUS open items). | [Bain Capital release "Ren Secures Strategic Growth Investment Led by Bain Capital Tech Opportunities"](https://www.baincapital.com/news/ren-secures-strategic-growth-investment-led-bain-capital-tech-opportunities) (2023-07-26) | "the company holds a SOC 2 Type 1 certification". The full sequence in Ren-supplied boilerplate is Type 1 (Jul 2023), Type 2 (Jul 2025), Type 1 (Apr 2026). Ren's sitemap (373 URLs, read 2026-11-19) has no trust, security or SOC page. No audit report or bridge letter is public. | **Partly** (a third statement widens the drift; all are vendor boilerplate) |
| C08 | DAFgiving360 charges 0.60% on the first $500k, with tiers (report §3). Source: a search snippet of a page that returned 403. | [DAFgiving360 Program Policies, "Updated December 2024"](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) (PDF created 2024-11-06, modified 2024-12-12; the copy is hosted on a third-party Squarespace site) | Page 9 tier table: first $500,000 at 0.60%; next $500,000 at 0.30%; next $1,500,000 at 0.20%; next $2,500,000 at 0.15%; next $5,000,000 at 0.13%; next $5,000,000 at 0.12%; $15,000,000 and beyond at 0.10%. "Each DAF account is assessed an annualized administrative fee of 0.60% … Accounts with assets exceeding $500,000 will receive a quarterly rebate". | **Corroborated** (first-party policy document; a 2025–26 edition was not found) |
| C09 | Edward Jones: Ren's back-office role is "inferred only"; the private DAF has no known sponsor; "$2.9bn" is unverifiable (report §2.2). | (a) [Edward Jones flyer "Edward Jones Charitable Gift Fund: A convenient way to make a lasting impact"](https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/res-13116-a.pdf) (ANG-13116H-A; © 2026; PDF created 2026-01-08; expires 2027-03-31)<br>(b) [EJ portal Terms of Service PDF](https://edwardjones.donorfirstx.com/Terms%20of%20Service.pdf) (Last-Modified 2026-02-10)<br>(c) the program-circular path `/pdf/EJDAF/Program Circular.pdf` (HTTP 404) | (a) "A third-party administrator is responsible for day-to-day operations of the DAF. As part of their services, they ensure the charity you support is approved by the IRS before fulfilling your grant request". No administrator is named, and the flyer never names Renaissance.<br>(b) "Agreement between user and Renaissance Acquisition Company LLC … (collectively 'Ren')". Ren operates the portal.<br>(c) No EJ circular was found (portal program code EJDAF, id 1630). The $2.9bn figure and the private-DAF sponsor are unchanged. | **Partly** (an unnamed third-party administrator is confirmed; Ren as that administrator is still inferred) |
| C10 | RCF sponsors the Commonwealth Charitable Fund (report §2.2; synthesis line 73: "Commonwealth sponsorship by RCF inferred"). Source: graph edge E034, inferred. | (a) [CCF Program Circular](https://cfndaf.donorfirstx.com/pdf/CFNDAF/Program%20Circular.pdf), re-fetched 2026-11-19 (Last-Modified 2024-12-13)<br>(b) [West Virginia Secretary of State charity record for RCF](https://apps.sos.wv.gov/business/charities/detail.aspx?OrgID=3767) (accessed 2026-11-19) | (a) "The Commonwealth Charitable Fund (CCF) is a donor-advised fund (DAF) program offered by Renaissance Charitable Foundation Inc." and "The Foundation has retained RenPSG of Indianapolis, Indiana, to perform certain accounting and administrative functions".<br>(b) The record for "Renaissance Charitable Foundation, Inc." lists "Commonwealth Charitable Fund" among its other names. | **Corroborated** (sponsor document plus a regulator record) |
| C12 | "Licensed DAF software at 31–94% of sponsors"; Foundant "700+" (report §1 table). | Internal: [queue-cf-vendor-map.md](queue-cf-vendor-map.md) | The repository's own EIN-level map (Foundant at 361 of 803 foundations, 45%; 481 mapped) is already quoted in the same cell. The 31–94% range is the stale part. | **Internal fix** |
| C16 | Daffy holds $2bn (Sep 2026, company-reported). | [ProPublica API, Daffy Charitable Fund, EIN 86-3177440](https://projects.propublica.org/nonprofits/organizations/863177440) (2026-11-19) | The latest filing listed is the CY2024 990 (received 2026-03-02; no parsed data). No CY2025 return is posted. | **Still single-source** (re-check when the CY2025 990 posts) |
| C17 | Charityvest 2025 results (contributions doubled; 48,744 grants). | [ProPublica API, Charityvest, EIN 81-2771871](https://projects.propublica.org/nonprofits/organizations/812771871) (2026-11-19) | The latest filing is the CY2024 990. No CY2025 return is posted. | **Still single-source** |
| C18 | The California AG release names Fidelity, Vanguard and DAFgiving360 as restricting SPLC grants; persistence unknown (report §4). | [Multistate AG letter to the three sponsors](https://oag.ca.gov/system/files/attachments/press-docs/2026-05-21%20SPLC%20-%20DAF%20Letter.pdf) (2026-05-21) | The letter is sent "VIA CERTIFIED MAIL" to Fidelity Investments Charitable Gift Fund, Donor Advised Charitable Giving, Inc. and Vanguard Charitable Endowment Program. It concerns "the decision … to stop or restrict payments to the Southern Poverty Law Center". It is signed by 16 attorneys general: MN (Ellison, first signer), CA, CO, CT, DE, HI, IL, ME, MD, NV, MA, NY, OR, VT, VA and WA. Whether the holds persisted is still not shown. | **Corroborated** (the restriction as of May 2026; persistence unknown) |
| C19 | About $7.5bn moved sponsor-to-sponsor in 2024 (report §4), citing Inequality.org only. | Internal: report Batch 34 (wave 19), from Schedule I lines in [`daf-to-daf-flows-990.csv`](../../data/mission-2026-11-14/daf-to-daf-flows-990.csv) | Netting under rule R5, central tier, removes $8.03bn in FY2024 (lower and upper tiers across FY2021–24: $3.32–6.95bn and $4.88–9.42bn a year). | **Corroborated** (same order of magnitude; primary 990 basis) |

## 3. Find/Replace corrections

Each "Find" string was checked to occur exactly once in each file named. R is `research/DAF-INDUSTRY-REPORT-2026-11.md`, S is `research/mission-2026-11-14/strategic-synthesis.md` and F is `research/mission-2026-11-14/FINAL-STATUS.md`.

**FR-01 (C01; R line 147, S line 22, F line 152).** The same sentence appears in all three files.
- Find: `Nearly half of the 28% is NPT, evidenced by hosting (iPhi login redirect, shared Ren load balancer, Ren-hosted "NPT iPhi Statuspage") rather than a disclosed contract`
- Replace: `Nearly half of the 28% is NPT, evidenced by hosting (iPhi login redirect, shared Ren load balancer, Ren-hosted "NPT iPhi Statuspage") rather than a disclosed contract **[I: hosting inference, single-source]**. A 2026-11-19 second-source pass found no NPT filing, privacy-policy processor list, product article or Ren page naming Ren as NPT's vendor; Ren is not among NPT's five listed FY2025 contractors (the fifth is paid $220,927) ([gap19-second-source-pass.md](mission-2026-11-14/gap19-second-source-pass.md) C01)`
- In S and F, the link path is `gap19-second-source-pass.md`.

**FR-02 (C02; R line 68).**
- Find: `Vanguard Charitable selected **Give Interactive** for DAF recordkeeping (Nov 2025 release)`
- Replace: `Vanguard Charitable selected **Give Interactive** for DAF recordkeeping, per a release issued by Give Interactive (Nov 2025) that quotes Vanguard Charitable's CIO **[vendor claim]**. Vanguard Charitable's FY2026 audited statements (FYE 2026-06-30) do not mention it, and go-live is unobserved`

**FR-03 (C02; F line 158).**
- Find: `**A previously unknown vendor, Give Interactive, holds Vanguard Charitable's DAF recordkeeping.**`
- Replace: `**A previously unknown vendor, Give Interactive, says it holds Vanguard Charitable's DAF recordkeeping [vendor claim; not in Vanguard Charitable's FY2026 audited statements].**`

**FR-04 (C10; R line 71 and S line 73).**
- Find: `LPL/Commonwealth (Commonwealth sponsorship by RCF inferred)`
- Replace: `LPL/Commonwealth (RCF sponsorship confirmed by the CCF program circular and the West Virginia charity registry)`

**FR-05 (C07; R line 195).**
- Find: `both in Ren's own boilerplate; no report has been seen **[V]**`
- Replace: `both in Ren's own boilerplate, and Bain Capital's July 2023 investment release says "Type 1"; no report has been seen and Ren publishes no trust page **[V; vendor claim]** ([Bain Capital/Ren release, Jul 2023](https://www.baincapital.com/news/ren-secures-strategic-growth-investment-led-bain-capital-tech-opportunities))`

**FR-06 (C07; S line 80).**
- Find: `Ren's SOC 2 type stated as Type 2 (Jul 2025) then Type 1 (Apr 2026) in vendor boilerplate.`
- Replace: `Ren's SOC 2 type stated as Type 1 (Jul 2023), Type 2 (Jul 2025), then Type 1 (Apr 2026) in vendor boilerplate; no report is public.`

**FR-07 (C08; R line 122 and S, citation).**
- Find: `[DAFgiving360 fees and minimums](https://www.dafgiving360.org/features/fees-and-minimums)`
- Replace: `[DAFgiving360 Program Policies, Dec 2024](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf)`

**FR-08 (C08; R line 998 and S, source register).**
- Find: `- DAFgiving360 fees and minimums (accessed 2026-11-14 (search snippet; page 403)): https://www.dafgiving360.org/features/fees-and-minimums`
- Replace: `- DAFgiving360 Program Policies, "Updated December 2024" (first-party PDF hosted on a third-party site; fee table p. 9; accessed 2026-11-19): https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf`

**FR-09 (C09; R line 84).**
- Find: `| Ren back-office administration for Edward Jones specifically | Inferred only | RCF pays Ren under an audited contract, but nothing names Ren for Edward Jones`
- Replace: `| Ren back-office administration for Edward Jones specifically | Inferred only (partly corroborated) | Edward Jones's 2026 flyer says "a third-party administrator is responsible for day-to-day operations" but does not name it; the portal's terms are an agreement with Renaissance Acquisition Company LLC ("Ren"); RCF pays Ren under an audited contract, but nothing names Ren for Edward Jones ([Edward Jones Charitable Gift Fund flyer, 2026](https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/res-13116-a.pdf); [EJ portal Terms of Service](https://edwardjones.donorfirstx.com/Terms%20of%20Service.pdf))`

**FR-10 (C05; R line 219).**
- Find: `- **There is no public evidence of AI in sponsor-side approval or eligibility determination.**`
- Replace: `- **There is no public evidence of AI in sponsor-side approval or eligibility determination** (an absence finding; on 2026-11-19 the grant-review and privacy pages of Fidelity Charitable, Vanguard Charitable and NPT disclosed no AI or automated grant review; DAFgiving360 was not checked).`

**FR-11 (C18; R line 163).**
- Find: `Persistence of those holds is unknown ((source: repo inference — no primary URL)).`
- Replace: `Sixteen attorneys general, led by Minnesota, wrote to the three sponsors on 2026-05-21 about the decision "to stop or restrict payments" to SPLC ([multistate AG letter](https://oag.ca.gov/system/files/attachments/press-docs/2026-05-21%20SPLC%20-%20DAF%20Letter.pdf)). Whether the holds persisted is not shown in any public record found.`

**FR-12 (C19; R line 170).**
- Find: `- About $7.5bn moved sponsor-to-sponsor in 2024 ([Inequality.org on DAF-to-DAF giving](https://inequality.org/article/daf-to-daf-giving-2024/)).`
- Replace: `- Netting sponsor-to-sponsor transfers on filed 990s removes $8.03bn in FY2024 (rule R5, central tier; Batch 34, §11), consistent with Inequality.org's advocacy estimate of about $7.5bn ([Inequality.org on DAF-to-DAF giving](https://inequality.org/article/daf-to-daf-giving-2024/)).`

**FR-13 (C19; S line 158).**
- Find: `about $7.5bn moved in 2024 anyway`
- Replace: `about $8bn moved in FY2024 anyway ($8.03bn netted from filed 990s, central tier; Inequality.org estimates $7.5bn)`

**FR-14 (C12; R line 52).**
- Find: `Licensed DAF software at 31–94% of sponsors`
- Replace: `Licensed DAF software at 31–94% of sponsors (vendor self-reports and an older survey; superseded by the repository map below)`

**FR-15 (C03; S line 462).**
- Find: `without them it is $32.59bn (wave 23).`
- Replace: `without them it is $32.59bn (wave 23), of which $27.01bn is Vanguard Charitable, which rests on Give's own release; no current client names Give in a 990 contractor line.`

C04, C06, C16 and C17 need no wording change. Their present labels ("templates and donor terms", "[V]" docs, "company-reported") already state the basis.

## 4. Source register

Access date is 2026-11-19 unless stated. Robots.txt was read first for every host.

| Ref | Source | Date of document | URL |
|---|---|---|---|
| S01 | NPT Terms of Use/Privacy Policy | Last updated 2026-10-29 | https://www.nptrust.org/privacy-policy/ |
| S02 | NPT, "Five Things to Know about NPT GivingPoint" | 2021-02-12 | https://www.nptrust.org/philanthropic-resources/philanthropist/five-things-to-know-about-npt-givingpoint-a-conversation-with-chris-adams-svp-of-it-solutions-and-cybersecurity/ |
| S03 | NPT, For Financial Institutions | accessed 2026-11-19 | https://www.nptrust.org/advisors-and-institutions/for-financial-institutions/ |
| S04 | NPT Form 990 FY2025 (Part VII-B, via repo harvest) | FYE 2025-06-30 | https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/full |
| S05 | PR Newswire: Vanguard Charitable partners with Give Interactive (issuer: Give Interactive) | 2025-11-04 | https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html |
| S06 | Vanguard Charitable FY2026 audited financial statements | FYE 2026-06-30; subsequent events to 2026-10-05 | https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf |
| S07 | Vanguard Charitable privacy policy | Last updated 2023-05-16 | https://www.vanguardcharitable.org/company-policies/privacy-policy |
| S08 | Give Interactive homepage | accessed 2026-11-19 | https://www.giveinteractive.com/ |
| S09 | Foundation for the Carolinas Form 990 CY2023 (Give Interactive $654,500) | CY2023 | https://projects.propublica.org/nonprofits/organizations/566047886/202433209349318318/full |
| S10 | Commonwealth Charitable Fund Program Circular | Last-Modified 2024-12-13 | https://cfndaf.donorfirstx.com/pdf/CFNDAF/Program%20Circular.pdf |
| S11 | West Virginia SOS charity record, Renaissance Charitable Foundation | accessed 2026-11-19 | https://apps.sos.wv.gov/business/charities/detail.aspx?OrgID=3767 |
| S12 | Fidelity Charitable grant review and due diligence process | © 2026 | https://www.fidelitycharitable.org/faqs/all/grant-review-due-diligence-process.html |
| S13 | Fidelity Charitable granting due diligence | © 2026 | https://www.fidelitycharitable.org/legal/granting-due-diligence.html |
| S14 | Fidelity Charitable privacy policy | © 2026 | https://www.fidelitycharitable.org/legal/privacy-policy.html |
| S15 | Daffy MCP server docs | accessed 2026-11-19 | https://docs.daffy.org/agents/mcp |
| S16 | Daffy AI Agents overview | accessed 2026-11-19 | https://docs.daffy.org/agents |
| S17 | TIFIN Give Louise launch (tifin.com; seen in search, not fetched) | 2025-10-27 | https://tifin.com/news/tifin-give-launches-louise-the-ai-platform-for-philanthropy/19124/ |
| S18 | Bain Capital: Ren secures strategic growth investment | 2023-07-26 | https://www.baincapital.com/news/ren-secures-strategic-growth-investment-led-bain-capital-tech-opportunities |
| S19 | Ren sitemap index (373 URLs; no trust or security page) | accessed 2026-11-19 | https://www.reninc.com/sitemap_index.xml |
| S20 | DAFgiving360 Program Policies, "Updated December 2024" | PDF created 2024-11-06; modified 2024-12-12 | https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf |
| S21 | Edward Jones Charitable Gift Fund flyer, ANG-13116H-A | © 2026; created 2026-01-08; expires 2027-03-31 | https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/res-13116-a.pdf |
| S22 | Edward Jones portal Terms of Service (Ren) | Last-Modified 2026-02-10 | https://edwardjones.donorfirstx.com/Terms%20of%20Service.pdf |
| S23 | SEC exhibit returned by search (unrelated; shows the route was tried) | 2025-10-28 | https://www.sec.gov/Archives/edgar/data/2065812/000110465925103244/tm2529568d1_ex10-1.htm |
| S24 | Multistate AG letter on SPLC restrictions | 2026-05-21 | https://oag.ca.gov/system/files/attachments/press-docs/2026-05-21%20SPLC%20-%20DAF%20Letter.pdf |
| S25 | ProPublica Nonprofit Explorer API, Daffy Charitable Fund | accessed 2026-11-19 | https://projects.propublica.org/nonprofits/api/v2/organizations/863177440.json |
| S26 | ProPublica Nonprofit Explorer API, Charityvest | accessed 2026-11-19 | https://projects.propublica.org/nonprofits/api/v2/organizations/812771871.json |
| R1 | Repo: Form 990 contractor harvest | — | data/mission-2026-11-14/form990-contractors-harvest-full.csv |
| R2 | Repo: Schedule D and return harvest (contractor counts, Part IX IT) | — | data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv |
| R3 | Repo: Commonwealth upgrade of E034 to EF001 | 2026-11-14 | research/mission-2026-11-14/queue-vendor-channel-moves.md §1 |
| R4 | Repo: NPT–Ren payment trail | 2026-11-15 | research/mission-2026-11-14/queue-npt-givingpoint-fidelity-stack.md §4 |

**Hosts not fetched** (robots.txt returned 403): `www.dafgiving360.org`, `www.schwabcharitable.org` and `reports.adviserinfo.sec.gov`. `www.reninc.com` returned 403 to pages partway through the session, and I stopped requesting it. EDGAR full-text search was blocked by a session permission control.
