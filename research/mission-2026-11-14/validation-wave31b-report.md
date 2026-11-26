# Validation wave 31B: thoroughness pass part B (crt.sh re-sourcing, second-source pass, wealth channels, AI coverage, Clarity/EDF, fee and delivery refresh)

**Date:** 2026-11-19. **Validator:** independent-validation-agent-wave31b.
**Register:** [`validation-register-wave31b.csv`](../../data/mission-2026-11-14/validation-register-wave31b.csv), rows V31B-01 to V31B-42.
**Documents validated:**
- [crtsh-resourcing-2026-11-19.md](crtsh-resourcing-2026-11-19.md) and `crtsh-claims-resourcing.csv` (70 rows), plus the corrections applied in commit `60740ee` (13 queue docs, the industry report and the synthesis) and the certspotter addition to [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md)
- [gap19-second-source-pass.md](gap19-second-source-pass.md) and its 15 inline edits (`git diff 0b2d2f6..HEAD` on the report, synthesis and FINAL-STATUS)
- [gap19-edward-jones-wealth-channels.md](gap19-edward-jones-wealth-channels.md), `wealth-channel-daf-programs-2026-11-19.csv` (11 rows) and `relationship-graph-edges-additions-26.csv` (EZ001–EZ022)
- [gap19-ai-coverage-20-entities.md](gap19-ai-coverage-20-entities.md)
- [gap19-clarity-edf-new-findings.md](gap19-clarity-edf-new-findings.md), `clarity-edf-direction-tags-2026-11-19.csv` (33 rows), and the rows and section appended in commit `f2d5934` to `incentive-map.csv` and [industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md)
- [gap19-fee-and-delivery-refresh.md](gap19-fee-and-delivery-refresh.md), `cf-daf-fee-census-refresh-2026-11-19.csv` (12 rows) and `announced-vs-delivered-refresh-2026-11-19.csv` (42 rows)

**Method:** public sources only. I did not log in, submit forms, solve or bypass CAPTCHAs, make keyed API calls or contact anyone. **I made no request of any kind to crt.sh or certspotter.** I read robots.txt on every host before fetching from it, checking the `*`, ClaudeBot and anthropic-ai groups:
- `dns.google/robots.txt` returns 404 (no rules). I re-ran A lookups for **167 hostnames**: all 139 non-wildcard Give names in the 2026-11-14 snapshot (used as DNS seeds only), 23 other vendor, sponsor and GivingPoint hosts, and 5 random-label wildcard probes.
- `archive.org/robots.txt` allows `/wayback/available`. I read capture metadata for 6 hosts and fetched no captured page.
- `sslmate.com/robots.txt` was read (it disallows `/api` and `/crt` for `*`); `api.certspotter.com/robots.txt` returns 404.
- **`www.sec.gov/robots.txt` returned HTTP 403 to this client, so I fetched nothing from sec.gov.** The Jones Financial and SEI 10-K/10-Q claims are therefore unverifiable here (V31B-21).
- `www.iphiview.com` and `www.stellartechsol.com` disallow `*`, and I fetched nothing beyond their robots.txt.
- Every other host fetched (nptrust.org, prnewswire.com, vanguardcharitable.org, baincapital.com, static1.squarespace.com, cfndaf.donorfirstx.com, apps.sos.wv.gov, oag.ca.gov, projects.propublica.org, edwardjones.com, seic.com, bankofamerica.com, wellsfargoadvisors.com, ncfgiving.com, aefonline.org, renaissancecharitable.org, svcf.org, morganstanley.com, giveinteractive.com, dafdirect.org, pavefinance.com, minneapolisfoundation.org, sff.org, gcfdn.org, intercom.help, giveclear.org, guide.charityvest.org, impactassets.org, altruist.com) allows the paths read. A direct re-fetch of two IRS XML files from the GivingTuesday mirror was refused by this session's permission controls, so the Fidelity, NPT and AOGF Part VII-B values were checked against the repo harvest rows, which carry the XML URLs.

For each claim I formed a verdict from the primary source first and compared it with the documents afterwards. Recomputations used the repo CSVs directly, in my own scripts in scratch.

## Headline

Of 42 claims, **32 are confirmed, 9 partially confirmed and 1 unverifiable. None is contradicted.**

**What holds independently:**
- **crt.sh re-sourcing:**
  - My own DNS run reproduces **89 resolving and 50 NXDOMAIN of the 139 Give names** exactly.
  - DonorSphere (52.138.119.67) and donor-portal.org (165.245.151.118) answer a random label, so both zones have **DNS wildcards**. giveinteractive.com, giveinteractive-clients.com and vanguardcharitable.org have none.
  - EBCF, KZCF, FFTC, myfftc, Omaha and every `ocf-*` Give host is NXDOMAIN, and `sdfoundation-staging` still resolves.
  - Other zones: `api-vgi.vanguardcharitable.org` is a dangling CNAME to an NXDOMAIN ALB; philanthropi.com returns SERVFAIL; vennfi.com returns NOERROR with no A record.
  - Wayback capture metadata matches: The Signatry from 2021-10-27; cct-sandbox 2025-02-23; EBCF from 2023-09-24 to 2026-03-13; KZCF from 2024-09-20 to 2025-02-22; bmodaf.org from 2024-07-31.
  - **The CT-five sum is $9,210,205,573**, so $9.21bn is right and $32.59bn stands. The $6.06bn (Signatry plus CCT) and the 20/29/18/3 classification counts also reproduce.
  - **$36.74bn / $23.90bn / $12.84bn and $3.56bn are exact on the DAFRC sponsor-universe basis.** That basis uses imputed values for ImpactAssets ($3.63bn) and FFTC ($2.95bn). The R1-corrected league table has **$2.90bn and $2.62bn**, which gives a DNS-only tier of **$12.11bn** and lapsed tenants of **$3.23bn**. The documents should state the basis (V31B-06, V31B-08).
  - **All 46 applied corrections are present, with one rendering defect:** a literal `\n` breaks the new "Admissibly dated" table row in `queue-watchlist-and-vendor-moves.md`.
  - Gaps left by the pass: the three §5.14 corrections ($9.81bn → $9.21bn in `queue-batch38-vendors-ledgers-portals.md` and `validation-wave23-report.md`) were not applied, and the synthesis still says "Lost five CF tenants ($4.79bn)" with no qualifier.
  - The `$9.21bn` edits in the report and synthesis are right.
- **Certspotter addition:** accurate. sslmate.com's `*` group disallows `/api` and `/crt`; api.certspotter.com has no robots.txt; the watchlist and both scripts are disabled. Two passages in `crtsh-resourcing-2026-11-19.md` still call the decision open.
- **Second-source pass (re-read at source):**
  - **C01:** NPT's terms (2026-10-29) name no vendor. Ren is not among NPT's five FY2025 contractors (the fifth is Patterson Belknap, $220,927), and nine contractors were paid over $100k.
  - **C02:** the PR Newswire record says "News provided by … SOURCE Give Interactive". Vanguard Charitable's FY2026 statements never mention Give Interactive, show software costs of $0 in both years and a Vanguard fee of $4,243,096, and review subsequent events through October 5, 2026.
  - **C07:** Bain Capital's release of 2023-07-26 says "SOC 2 Type 1".
  - **C08:** the tiers are exactly as stated. One quoted sentence is not verbatim.
  - **C10:** the CCF circular says the program is "offered by Renaissance", and the West Virginia registry lists "Commonwealth Charitable Fund" among RCF's names.
  - **C18:** the AG letter is dated May 21, 2026, has three addressees and 16 signers.
  - **All 15 inline edits are applied and read correctly.** FR-06 leaves "no report is public" next to an older "No report seen", and its new Jul 2023 statement has no link in the synthesis.
- **Edward Jones and wealth channels:**
  - The Form CRS has no charitable text. The IAP wrap brochure has only the two charitable passages the doc quotes.
  - The Edward Jones Charitable Gift Fund terms, the two SEI DAFs, the BofA trustee and administrator text, the Fidelity → Wells Fargo Advisors $3,409,679 payment and the Wells Fargo disclaimer (no NPT) all hold.
  - **AOGF → PNC ($196,447; $148,680; then Citibank) holds, but edge EZ018's "administers" overstates it.** AOGF labels every contractor "ADMINISTRATIVE SVCS", PayPal and BlueSnap included.
  - The Jones Financial 10-K silence could not be re-read (sec.gov robots 403).
- **AI coverage:** I spot-checked 12 of the 20 entities: NCF, NPT, SEI, Morgan Stanley, Edward Jones, AEF, RCF, SVCF, DAF Direct, Give Interactive, Pave and Stellar/iPhi. Every quote, date and absence matched.
  - NCF's page record is dated 2026-08-12 and carries `status:"private"`.
  - The NPT AI-training ban, the TIFIN boilerplate and the SEI/IBM agents post are as quoted.
  - The Morgan Stanley Debrief "at their discretion" step and Edward Jones' AI tool "beginning in 2027" are as quoted.
- **Clarity/EDF:**
  - All four outcomes run the full nine-step EDF v0.3 sequence with the guide's Clarity elements: admissibility, posture, reconsideration and monitoring.
  - The claim states and confidence labels are the policy's.
  - Every number traces to its governing document as corrected. For example, 3.6–4.7x is the wave-25A correction, and the Fidelity gaps match R001–R009 and R070–R072.
  - **The Fidelity 5-year-only bound holds** in §5, in the appended `incentive-map.csv` row and in the structural-analysis section. The §1 summary row and the §5 heading drop the bound.
  - The note still says the two files were "not edited", although commit `f2d5934` appended to both.
- **Fee and delivery refresh:**
  - The three new fee schedules match their PDFs. My bps are 100/100/59 (Minneapolis), 100/100/82.5 (SFF) and 95/95/– (Greater Cincinnati).
  - **Medians stay 100/100/67.2. Coverage goes from 34 to 37 schedules and from 43.0% to 46.1% of assets.** The interquartile ranges (100–125, 100–121.9, 48.0–84.4) and the weighted means (99.4/91.2/60.1) reproduce with the census script's quantile method.
  - The status changes are confirmed at source: AVD09 and AVD29 to delivered; AVD02, AVD17 and AVD31 to partial. The merged totals are 17/11/9/2 (39 rows) and 25/14/16/2 (57 rows).

**Ruling on the fee refresh's §4 Find/Replace pairs:**
- **Approved now:** the report §5 table pairs (15 → 17, 10 → 11, 12 → 9, plus the note) and the competitive-history rails pair.
- **Approved only together with merging FR01–FR03 into `cf-daf-fee-census-2026.csv` (P-G09-01):**
  - the line-797 CF summary pair;
  - the `direction-cf-consolidation-fees.md` pairs, which need two additions: "All 33 CFs charge more" → "All 35" and the §3.2 heading n;
  - the "34 published schedules" wording in the EDF note.
- **Daffy pair:** only if AVD42–43 are merged.

## Limits

- **Not re-checked:**
  - sec.gov filings (robots.txt 403), so the JFC and SEI 10-K/10-Q negatives stand on the producing pass.
  - The other three Edward Jones wrap brochures, the Generations agreement and the RCF audits.
  - The Wayback dates of the NPT GivingPoint sites other than BMO.
  - The 8 AI entities not spot-checked: DAFgiving360, Goldman Sachs, JCF, NPact, TIAA, OneAscent, MS GIFT page navigation and BofA newsroom. Most of them are search-only [R] rows in the doc.
  - New AVD rows beyond AVD41 and AVD44.
- **The pinned Clarity and EDF repositories were not re-fetched.** The EDF check is against the repo's application guide, which records the pinned commits. The doc's posture-matrix ambiguity note could not be re-read at source.
- **Filing values** for Fidelity, NPT and AOGF Part VII-B were checked against `form990-contractors-harvest-full.csv` (rows carry the mirror XML URLs), not re-fetched XML.
- **The imputed-versus-filed basis issue (IA, FFTC) predates this pass.** It was inherited from wave 15. I recommend a basis note, not new headline numbers.
- **Pages change.** Every page was read on 2026-11-19.

## Exact corrections

### `research/mission-2026-11-14/queue-watchlist-and-vendor-moves.md`
1. **§ certified-by table (line 109): literal `\n` inserted by the crt19 correction.**
   - **Find:** "| 31.64 | 31.30 |\n| Admissibly dated by 2025-09-30" (the `\n` here is the two literal characters backslash and n in the file)
   - **Replace with:** the same text with those two characters replaced by a real line break, so that "| Admissibly dated by 2025-09-30 (Signatry: Wayback 2021-10-27; CCT: cct-sandbox Wayback 2025-02-23) [crt19] | | | 6.06 | |" becomes its own table row [V wave 31B].

### `research/mission-2026-11-14/queue-batch38-vendors-ledgers-portals.md`
1. **Unapplied crt19 §5.14 #1.**
   - **Find:** "($9.81bn at FY2024)"
   - **Replace with:** "($9.21bn at FY2024; corrected from $9.81bn [crt19; V wave 31B])"

### `research/mission-2026-11-14/validation-wave23-report.md`
1. **Unapplied crt19 §5.14 #2.**
   - **Find:** "($9.81bn at FY2024)"
   - **Replace with:** "($9.21bn at FY2024; corrected from $9.81bn [crt19; V wave 31B])"
2. **Unapplied crt19 §5.14 #3 (C3 row).**
   - **Find:** "$9.81bn of it (CCT $4.65bn, JCF $2.87bn, Minneapolis $0.60bn, Thrivent $0.59bn, Stifel $0.49bn)"
   - **Replace with:** "$9.21bn of it (CCT $4.65bn, JCF $2.87bn, Minneapolis $0.60bn, Thrivent $0.59bn, Stifel $0.49bn; corrected from $9.81bn [crt19; V wave 31B]). ImpactAssets ($3.63bn) is also attributed to Give only through hostnames, because its transition page names no vendor"

### `research/mission-2026-11-14/crtsh-resourcing-2026-11-19.md`
1. **§4, known-clients row: state the value basis.**
   - **Find:** "First-party/filing tier is 59.7% of $40bn |"
   - **Replace with:** "First-party/filing tier is 59.7% of $40bn. Basis: DAFRC sponsor-universe FY2024 values, in which ImpactAssets ($3.63bn) and Signatry ($0.40bn) are imputed; on the R1-corrected league table ImpactAssets is $2.90bn, giving a DNS-only tier of $12.11bn [V wave 31B] |"
2. **§4, lapsed-tenants row: state the value basis.**
   - **Find:** "Omaha ($0.52bn) is an unverified lead. San Diego ($0.71bn) status is unknown: its staging host resolves |"
   - **Replace with:** "Omaha ($0.52bn) is an unverified lead. San Diego ($0.71bn) status is unknown: its staging host resolves. FFTC's $2.95bn is the DAFRC-imputed value; the R1-corrected FY2024 figure is $2.62bn, which makes the three $3.23bn [V wave 31B] |"
3. **§5.15 text: the certspotter decision has been taken.**
   - **Find:** "Certspotter admissibility is open (P-CRT19-02)."
   - **Replace with:** "Certspotter is treated like crt.sh from 2026-11-19, because its operator's robots.txt (sslmate.com) disallows /api; its results are unverified leads (P-CRT19-02 closed by the compliance note) [V wave 31B]."
4. **§6, first bullet.**
   - **Find:** "The admissibility decision is P-CRT19-02."
   - **Replace with:** "The admissibility decision (P-CRT19-02) was taken the same day in compliance-note-crtsh-robots.md: certspotter is no longer used, and its results are unverified leads unless confirmed by DNS, first-party pages or filings [V wave 31B]."

### `research/mission-2026-11-14/strategic-synthesis.md`
1. **Risk/claim table, Give Interactive losses row (line 424): crt19 qualifier missing.**
   - **Find:** "| Give Interactive losses | Lost five CF tenants ($4.79bn) | **One** demonstrated live loss (East Bay, $0.53bn); the $4.79bn is sponsor DAF assets, not Give AUM |"
   - **Replace with:** "| Give Interactive losses | Lost five CF tenants ($4.79bn) | **One** demonstrated live loss (East Bay, $0.53bn). On admissible evidence three CF tenants lapsed (EBCF, FFTC, Kalamazoo; $3.56bn on the DAFRC basis used here); Omaha's tenancy is a CT-only lead and San Diego's staging host still resolves ([crtsh-resourcing-2026-11-19.md](crtsh-resourcing-2026-11-19.md); V wave 31B). The figures are sponsor DAF assets, not Give AUM |"
2. **Assurance-credibility row (FR-06 follow-up): add the source and drop the redundant sentence.**
   - **Find:** "in vendor boilerplate; no report is public. ([AEF/Ren release, Jul 2025]"
   - **Replace with:** "in vendor boilerplate; no report is public. ([Bain Capital/Ren release, Jul 2023](https://www.baincapital.com/news/ren-secures-strategic-growth-investment-led-bain-capital-tech-opportunities); [AEF/Ren release, Jul 2025]"
   - **Find:** " No report seen. ((source: repo inference — no primary URL)) None of 13 vendors"
   - **Replace with:** " None of 13 vendors"

### `research/mission-2026-11-14/gap19-second-source-pass.md`
1. **C08 row: make the quotation verbatim.**
   - **Find:** "\"Each DAF account is assessed an annualized administrative fee of 0.60% … Accounts with assets exceeding $500,000 will receive a quarterly rebate\"."
   - **Replace with:** "\"Each DAF account is assessed an annualized administrative fee of 0.60% of the account balance. Accounts with assets in excess of $500,000 are eligible for a reduced fee in accordance with the tiered schedule\", applied as a \"quarterly rebate for the difference between the tiered fee and\" the 0.60% charged [V wave 31B]."

### `research/mission-2026-11-14/gap19-clarity-edf-new-findings.md`
1. **§1 table, G12-4 outcome: restore the 5-year bound.**
   - **Find:** "| G12-4 | Fidelity's published pool returns trail their benchmarks by about its first-tier admin fee |"
   - **Replace with:** "| G12-4 | Fidelity's asset-allocation pools trail their composites over 5 years by about its first-tier admin fee (0.58–0.76 pp); its Money Market pool trails by 0.65 pp in every window. Over 1 and 3 years the asset-allocation pools are mostly above their composites [V wave 31B] |"
2. **Rules followed: the files have since been edited.**
   - **Find:** "This task's write scope does not include those files, so §7 gives the rows ready to append. They are not governing until a validator accepts them."
   - **Replace with:** "§7 gives the rows. They were appended to both files in the same commit (`f2d5934`) and were accepted by validation wave 31B."
3. **§7 heading.**
   - **Find:** "## 7. Rows ready to append to `incentive-map.csv` (not applied; not governing)"
   - **Replace with:** "## 7. Rows appended to `incentive-map.csv` (applied 2026-11-19; validated, wave 31B)"
4. **Line 72 schedule count:** apply the fee refresh's "34 → 37 published schedules" wording only together with the census merge (see the `direction-cf-consolidation-fees.md` subsection).

### `research/mission-2026-11-14/direction-cf-consolidation-fees.md`
Apply all of the following **together with merging FR01–FR03 into `data/mission-2026-11-14/cf-daf-fee-census-2026.csv` (P-G09-01)**, not before. The values are validated (V31B-39).
1. The four pairs in [gap19-fee-and-delivery-refresh.md](gap19-fee-and-delivery-refresh.md) §4 item 4, as written.
2. **Added:**
   - **Find:** "### 3.2 Effective annual admin fee, published schedules (n=34; n=33 at $10m)"
   - **Replace with:** "### 3.2 Effective annual admin fee, published schedules (n=37; n=35 at $10m; refreshed 2026-11-19 [V wave 31B])"
3. **Added:**
   - **Find:** "All 33 CFs charge more."
   - **Replace with:** "All 35 CFs charge more [V wave 31B]."

### `research/mission-2026-11-14/competitive-history-timelines.md`
1. The rails pair in [gap19-fee-and-delivery-refresh.md](gap19-fee-and-delivery-refresh.md) §4 item 5 is **approved as written**. The Charityvest guide says grants go "electronically through Chariot or by weekly check" [V wave 31B].

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **§5 delivery table: approved as proposed (V31B-40).**
   - **Find:** "| Evidence of delivery | 15 |" · **Replace with:** "| Evidence of delivery | 17 |"
   - **Find:** "| Partial | 10 |" · **Replace with:** "| Partial | 11 |"
   - **Find:** "| No public evidence yet | 12 |" · **Replace with:** "| No public evidence yet | 9 |"
   - **Find:** "| Contradicted | 2 |" · **Replace with:** "| Contradicted | 2 |\n\nRe-checked 2026-11-19: 5 status changes, all upward (repo [`announced-vs-delivered-refresh-2026-11-19.csv`](../data/mission-2026-11-14/announced-vs-delivered-refresh-2026-11-19.csv)) [V wave 31B]." (here `\n` means a line break)
2. **Daffy bullet:** apply the fee refresh's §4 item 2 only if AVD42–43 are merged into `announced-vs-delivered.csv`.
3. **Line 797 CF fee summary:** apply the fee refresh's §4 item 3 only together with the census merge (P-G09-01).
4. **New subsection after §11.27.** Add "### 11.28 Thoroughness pass part B (validated, wave 31B)", containing the paragraph below. If §11.28 is already taken, use the next free number.

   > **Thoroughness pass part B (validated, wave 31B).**
   > - **crt.sh re-sourcing (DNS re-run of 167 hosts on 2026-11-19; no crt.sh or certspotter request).**
   >   - Of 139 Give Interactive hostnames, 89 still resolve. donorsphere.org and donor-portal.org answer any label (DNS wildcards), so their certificate-only tenant labels count for nothing.
   >   - Give's nine known clients hold $36.74bn of FY2024 DAF assets on DNS evidence. Only $23.90bn (Vanguard Charitable, The Signatry and WaterStone) rests on first-party or filing evidence. These figures use the DAFRC values; with ImpactAssets at its filed $2.90bn, the DNS-only part is $12.1bn.
   >   - The five clients discovered from certificate logs hold $9.21bn, not $9.81bn. Without them the total is $32.59bn.
   >   - On admissible evidence Give lost three community-foundation tenants (East Bay, Carolinas and Kalamazoo, $3.56bn on DAFRC values), not five.
   >   - Only $6.06bn of tenants (The Signatry and CCT) is dated before September 2025.
   >   - Certspotter is no longer used, because its operator's robots.txt disallows its API.
   > - **Second sources.**
   >   - Give Interactive's Vanguard Charitable mandate rests on a release Give issued. Vanguard Charitable's FY2026 audited statements do not mention it and show no software capitalised.
   >   - RCF's sponsorship of the Commonwealth Charitable Fund is confirmed by its circular and the West Virginia registry.
   >   - Bain Capital's 2023 release adds a third Ren SOC 2 statement ("Type 1").
   >   - DAFgiving360's tiered fee is confirmed in its December 2024 Program Policies.
   >   - Sixteen attorneys general wrote to Fidelity Charitable, DAFgiving360's sponsor and Vanguard Charitable on 2026-05-21 about SPLC payment restrictions.
   > - **Wealth channels.**
   >   - The Edward Jones Form CRS and advisory brochure name no DAF; its private DAF's sponsor is still undisclosed. The 10-K negatives were not re-read (sec.gov robots).
   >   - SEI runs two DAFs: RCF (Ren) and GiveClear (TIFIN Give).
   >   - Bank of America N.A. is the Charitable Gift Fund's sole trustee, and BofA Private Bank administers it.
   >   - Fidelity Charitable paid Wells Fargo Advisors $3.41m for investment management in FY2025.
   >   - Wells Fargo's live pages no longer name NPT.
   >   - AOGF's PNC payments ($196k, $149k) are labelled like all its contractors and do not show DAF administration.
   > - **AI.** Twelve of the 20 entities were re-read. None documents AI in grant approval or money movement. NCF's AI site search is the one donor-facing feature. Parent-firm AI (Morgan Stanley, SEI, Edward Jones) is not tied to the DAF programs.
   > - **Clarity/EDF.** The four new outcomes follow the EDF v0.3 sequence and alter no validated number. Fidelity's fee-sized shortfall holds only over five years for its active asset-allocation pools, and in every window for Money Market.
   > - **Fees and delivery.**
   >   - Minneapolis, San Francisco and Greater Cincinnati now have 2025–26 fee schedules.
   >   - The CF medians stay 100 / 100 / 67 bps at $100k / $1m / $10m, so the 1.7x / 2.2x / 3.6–4.7x ratios stand. Coverage rises to 37 schedules and 46% of top-100 CF DAF assets once the census is merged.
   >   - Of 39 announced-vs-delivered items, 17 are delivered, 11 partial, 9 without evidence and 2 contradicted (was 15 / 10 / 12 / 2).
   >   - 18 newer announcements add 8 delivered, 3 partial and 7 without evidence. The ImpactAssets DAF hub, promised for 2026-09-08, is overdue.

## Data-file notes (not .md; for the owning agent)

- **`relationship-graph-edges-additions-26.csv`, EZ018:** change `relationship_type` from `administers` to a neutral service-provider type (for example `service_provider`), and `status` from `historically_confirmed` to `historically_confirmed (payee; scope not stated)`. AOGF labels Benevity, BlueSnap, PayPal and Citibank "ADMINISTRATIVE SVCS" too (V31B-27).
- **`cf-daf-fee-census-2026.csv`:** merge FR01–FR03 (bps 100/100/59, 100/100/82.5, 95/95/blank) under P-G09-01. Then apply the conditional .md corrections above.
- **`announced-vs-delivered.csv`:** merge the 24 re-check statuses and AVD40–AVD57 from the refresh CSV. No value changes.
- **`crtsh-claims-resourcing.csv`:** no value changes. Consider a basis note on CRT19-026 (IA imputed) and on the lapsed-tenant row (FFTC imputed).
- **`clarity-edf-direction-tags-2026-11-19.csv`, `wealth-channel-daf-programs-2026-11-19.csv`, `cf-daf-fee-census-refresh-2026-11-19.csv`:** no value changes.
