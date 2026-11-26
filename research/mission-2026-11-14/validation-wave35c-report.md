# Validation wave 35C: church recipients of DAF grants

**Date:** 2026-11-19 · **Validator:** independent-validation-agent-wave35c · **Register:** [`data/mission-2026-11-14/validation-register-wave35c.csv`](../../data/mission-2026-11-14/validation-register-wave35c.csv) (22 claims)

**Study checked:** [`b4026-06-church-daf-recipients.md`](b4026-06-church-daf-recipients.md), its CSV [`church-daf-recipients-profile-2026-11-19.csv`](../../data/mission-2026-11-14/church-daf-recipients-profile-2026-11-19.csv) and `scripts/mission_church_recipients.py`.

**What was done**
- **Re-run.** The script was re-run into scratch on the same caches, with `--fetch-outreach`, so all 12 Outreach 100 pages were fetched again. `--dump-block` and `--sample-out` were also written.
- **Independent checks.**
  - The block definition was checked with a separate reader against the BMF and the TEOS index 2019–2026.
  - Concentration and per-church quantiles were recomputed from the block dump with a separate Gini and quantile routine.
  - The GEN centrals were re-derived from the BMF `GROUP`/`AFFILIATION` fields.
  - The IRS data dictionary (eo-info.pdf) was re-fetched.
- **Audit.** Two classification samples were read by hand:
  - the study's own sample (seed 7), which reproduces exactly;
  - a stratified draw of 80 (16 per recipient type, seed 3503).
- **Matching.** All 54 strict and 18 loose Outreach 100 pairs were read.
- **Giving pages.** 8 of the 10 scanned giving pages were re-read with headless Chrome, using the census User-Agent unchanged, after a robots.txt check for each host.
- **Repo search.** The faith-platform direction doc, `grep -i faith` over `direction-*.md` (13 of 33 files match), b40n1202 with its wave-34B corrections, and strategic-synthesis §0 were read.
- **Requests made.** Only to:
  - outreach100.com (robots.txt and 12 list pages);
  - www.irs.gov (robots.txt and eo-info.pdf);
  - the 8 church hosts listed in V35C-17 (robots.txt and one page each).
- **Not done.** No outreach. No crt.sh, certspotter or sec.gov. Nothing was committed or pushed.

Scratch: `/tmp/claude-0/-home-user/ed3d1503-0f0d-5a0d-a5e2-85e6e3196309/scratchpad/v35c/`. It holds `rerun.csv`, `rerun.json`, `block.csv`, `audit80.csv`, `outreach/`, `pages/`, `web/eo-info.pdf`, `robots/`, `tools/` and `corrections.json`.

## Counts

| Claims | confirmed | partially_confirmed | contradicted | unverifiable |
|---|---|---|---|---|
| **22** | **12** | **10** | 0 | 0 |

## Findings

**Holds.**
- **The script reproduces exactly (V35C-01).** The re-run, with freshly fetched Outreach pages, writes 1,617 non-donate rows that are byte-identical to the committed CSV.
- **The block is what it says (V35C-02, 03).** The block is 29,469 recipients and $6,177,546,936, which is 8.34% of $74,073,755,051. A separate reader confirms every EIN is in the BMF with SUBSECTION 03 and FOUNDATION 10, and that none has a 990, 990-EZ or 990-PF row in the index 2019–2026 (887 rows there are 990-T only). The `church_coded_all` figures also reproduce: 30,841 recipients and $7,275.9m.
- **Type shares, block concentration and GEN coverage (V35C-04, 07, 12).**
  - Recipient-type shares: 52.2 / 15.6 / 13.4 / 10.4 / 8.5%.
  - Block concentration: Gini 0.816; top 1% 42.5%; top 10% 74.5%; bottom half 4.2%; LDS 7.5%.
  - GEN coverage: 47.8% of dollars; 357 GENs, all resolving.
  - Each recomputes.
- **GEN 0928 is correct (V35C-10).**
  - The BMF has one AFFILIATION 8 central for GROUP 0928: EIN 530196617, United States Catholic Conference.
  - eo-info.pdf defines GROUP as the "four-digit internal number assigned to central/parent organizations holding group exemption letters", AFFILIATION 8 as a church parent of a group ruling, and FOUNDATION 10 as "Church 170(b)(1)(A)(i)".
- **Sponsor split (V35C-13, 14).**
  - Faith sponsors send 22.10% of block dollars (17.99% Christian + 4.11% Jewish), against 9.97% of all top-50 dollars, which is 2.2×.
  - Servant Foundation sends 40.0% of its own dollars to the block, NCF 18.4% and Thrivent 39.7%.
  - Fidelity Charitable supplies 34.9% of the block.
- **Outreach 100 (V35C-15).**
  - outreach100.com robots.txt allows all. All 12 pages returned 200, with 101 and 100 rows: 107 distinct churches.
  - 54 EINs match strictly, holding $138,429,642 (2.2% of block, 4.3% of congregation dollars).
  - All 54 strict pairs read as true matches.
- **Giving pages (V35C-17).** All 8 giving pages re-read (Calvary Chapel Edmonds, Sinai Temple, Chesterfield Presbyterian, Cherry Creek Presbyterian, St. Ann Marietta, Compass Bible, First UMC Madison, RockHarbor) were allowed by robots.txt. None shows DAFpay/Chariot, DAF Direct, "donor-advised", "DAF", a sponsor name or an EIN.
  - Three of them (Cherry Creek, Compass and First UMC) take gifts of securities but offer no DAF route.
  - The Wilson upper bound on 0/14 is 21.5%.

**Needs correction.**
1. **Congregation concentration (V35C-08).** The study's own CSV gives the top 1% of congregations 29.1% and the top 10% 66.6%. The text says 28.8% and 66.4%. The Gini of 0.757 is right.
2. **Two other transcription errors (V35C-09, 22).** The congregation median per church is $37,426, not $37,462. Come and See Foundation's type is ministry, not unclassified; "unclassified" is its family.
3. **Classification is uneven by type (V35C-05).**
   - The study's "all 72 consistent" result reproduces, but 63 of those 72 are congregations.
   - In a stratified draw, denominational-body labels are right for only 7 of 16 names and ministry labels for 11 of 16. Parishes match SYNOD or CORPORATION SOLE; orders, Chabad bodies, a school and a social-service centre also land in "denominational body".
   - About 6 or 7 of 16 unclassified names look like congregations.
   - The dollar effect is small, because LDS and dioceses dominate the denominational-body type.
   - The congregation share is a lower bound, as the study says.
4. **Denomination family (V35C-06).**
   - The "other faith…" row is 2.7%, not 3.2%.
   - The table omits the `other_ambiguous` family (1.4% of block, 2.6% of congregations).
   - GEN-based labels are not always authoritative:
     - UMC GEN 2573's BMF central name is truncated, so 64 subordinates ($12.5m) fall to own-name rules.
     - Converge (GEN 2269, Baptist General Conference, $49.7m) is mostly not labelled Baptist.
   - Methodist and Baptist shares are therefore understated by up to about 0.2 and 0.6 points.
5. **The GEN table omits two single-organisation group rulings (V35C-11).** GEN 3864 (Cru, $92.5m) and GEN 4067 (World Literature Crusade, $87.9m) rank 7th and 9th by dollars.
6. **Loose Outreach matches (V35C-16).** 16 of the 18 loose EINs are true pairs. The two false ones hold $0.9m, so the loose tier is close to a point estimate (about $198.3m), not just an upper bound. Free Chapel (GA, $8.1m) is a true list church that is missed because Outreach places it in Gainesville, FL.
7. **Platform counts (V35C-18).** "None detected" is 7 of the 14 pages, not 4.
8. **Stale benchmark (V35C-19).** The study quotes the census's 40.3% and religion's 3 of 14. Both were superseded by the governing wave-24B correction: 75/182 (41.2%), and religion 3 of 13.
9. **Faith-doc comparison (V35C-20).** E1 and E4 are well supported. But "faith sponsors explain at most a fifth" understates the faith share, which is 21–26% depending on scope. The faith doc's E1 count of "2–4 congregations" should become two under this study's rules.
10. **Wider repo (V35C-21).** b40n1202 still says "churches with no e-filed 990: 8.3%". About 4.4 of those 8.3 points are congregations; the rest are ministries (1.3), denominational bodies (1.1, of which LDS 0.6), schools (0.7) and unclassified names (0.9).

**Interpretation notes.**
- The DonorsTrust grouping is an interpretation, not an error. The faith_single_issue list cited for Servant Foundation also includes DonorsTrust; including it would give a faith share of 22.6%.
- `--dump-block` and the CSV `value` column store dollars to 6 significant figures; `usd_daf_weighted` is exact.

## Exact corrections

Apply in order. Each Find is verbatim and occurs exactly once in its file as it stands on 2026-11-19. In Find and Replace strings, `\n` stands for a newline and `\"` for a literal double quote; every other character is verbatim. The check is described at the end of this section.

### `research/mission-2026-11-14/b4026-06-church-daf-recipients.md`

1. **Find:** "Among congregations only, the top 1% take 28.8% and the top 10% take 66.4% (Gini 0.757)."
   - **Replace with:** "Among congregations only, the top 1% take 29.1% and the top 10% take 66.6% (Gini 0.757) [V wave 35C]."
2. **Find:** "| block_congregations | 21,774 | 0.757 | 8.7% | 28.8% | 66.4% | 20.5% | 5.9% |"
   - **Replace with:** "| block_congregations | 21,774 | 0.757 | 8.7% | 29.1% | 66.6% | 20.5% | 5.9% [V wave 35C] |"
3. **Find:** "(congregations $37,462)"
   - **Replace with:** "(congregations $37,426) [V wave 35C]"
4. **Find:** "| other faith, Orthodox, Muslim, Unitarian, Adventist | 3.2% | 1.9% |"
   - **Replace with:** "| other faith, Orthodox, Muslim, Unitarian, Adventist | 2.7% | 1.9% |\n| ambiguous (temple, congregation, sanctuary etc., no family) | 1.4% | 2.6% [V wave 35C] |"
5. **Find:** "| 2 | Come and See Foundation | CO | unclassified | 135.9 | Servant Foundation |"
   - **Replace with:** "| 2 | Come and See Foundation | CO | ministry (family unclassified) [V wave 35C] | 135.9 | Servant Foundation |"
6. **Find:** "| 1617 | Presbyterian Church (USA) | 404 | 50.4 | 0.8% |"
   - **Replace with:** "| 1617 | Presbyterian Church (USA) | 404 | 50.4 | 0.8% |\n\nTwo single-organisation group rulings rank among these by dollars and are left out of the table: GEN 3864 (Campus Crusade for Christ, 1 recipient, $92.5m, 1.5%) and GEN 4067 (World Literature Crusade, AFFILIATION 6, 1 recipient, $87.9m, 1.4%) [V wave 35C]."
7. **Find:** "GEN central names are authoritative for the 47.8% of dollars with a GEN; elsewhere names are an [I] classification."
   - **Replace with:** "GEN central names are authoritative for most of the 47.8% of dollars with a GEN; elsewhere names are an [I] classification. Two exceptions: the BMF central name for GEN 2573 (UMC) is truncated, so its subordinates fall back to own-name rules (64 recipients, $12.5m, not labelled Methodist), and GEN 2269 (Converge, the Baptist General Conference; $49.7m) has only $12.0m labelled Baptist. Methodist and Baptist shares are therefore understated by up to about 0.2 and 0.6 points [V wave 35C]."
8. **Find:** "all 72 labelled names read as consistent with their label."
   - **Replace with:** "all 72 labelled names read as consistent with their label. A validator's stratified draw (16 per type, seed 3503) found congregation labels right for 16 of 16 and school labels for 13 of 16, but ministry labels for 11 of 16 (2 congregations, 3 ambiguous centres) and denominational-body labels for only 7 of 16: parishes matched SYNOD or CORPORATION SOLE, and orders, Chabad bodies, a school and a social-service centre also landed there. The dollar effect is small, because LDS and dioceses dominate that type; names in it containing PARISH, CHURCH, CONGREGATION or TEMPLE hold $54.4m (0.9% of block) [V wave 35C]."
9. **Find:** "Loose matches are therefore reported only as an upper bound."
   - **Replace with:** "Loose matches are therefore reported only as an upper bound. On reading, 16 of the 18 loose EINs are true pairs, and the two false ones hold $0.9m, so the loose tier (about $198.3m without them) is close to a point estimate. Free Chapel (Gainesville, GA; $8.1m) is a true list church missed because Outreach places it in Florida [V wave 35C]."
10. **Find:** "and the repo lists as faith (direction-sponsor-executive-compensation.md, faith_single_issue)."
   - **Replace with:** "and the repo lists as faith (direction-sponsor-executive-compensation.md, faith_single_issue). That list also includes DonorsTrust, which is kept here in `other` ($32.9m, 0.5% of block); counting it would raise the faith share to 22.6% [V wave 35C]."
11. **Find:** "Subsplash 5, Pushpay 3, Planning Center 1, other form vendors 3, none detected 4 [O]."
   - **Replace with:** "Subsplash 5, Pushpay 3, Planning Center 1, other form vendors 3, none detected 7 (3 of the 10 giving pages and all 4 homepages) [O] [V wave 35C]."
12. **Find:** "For comparison, 40.3% of the top-300 recipients' donate pages show some DAF option, and religion's rate there is 3 of 14."
   - **Replace with:** "For comparison, 41.2% (75 of 182) of the top-300 recipients' donate pages show some DAF option, and religion's rate there is 3 of 13, both after the governing wave-24B correction [V wave 35C]."
13. **Find:** "The top-300 donate-page census found 40.3% with any DAF option overall and 3 of 14 for religion (all parachurch, no DAFpay)."
   - **Replace with:** "The top-300 donate-page census, as corrected in wave 24B, found 41.2% (75/182) with any DAF option overall and 3 of 13 for religion (all parachurch, no DAFpay) [V wave 35C]."
14. **Find:** "So \"faith sponsors pay without a donate page\" explains at most a fifth of the dollars [I]."
   - **Replace with:** "So \"faith sponsors pay without a donate page\" explains about a fifth to a quarter of the dollars (22.1% of the block, 25.7% of all church-coded dollars) [I] [V wave 35C]."

### `research/mission-2026-11-14/b40n1202-b43n26-recipient-basis-and-rating-eligibility.md`

1. **Find:** "  - churches with no e-filed 990: 8.3%;"
   - **Replace with:** "  - church-status organisations (BMF FOUNDATION 10) with no e-filed 990: 8.3%. By name rules about 4.4 points of this are congregations; ministries and orders are 1.3, denominational bodies 1.1 (the LDS Church alone 0.6), schools 0.7 and unclassified names 0.9 (b4026-06) [V wave 35C];"
2. **Find:** "go to church-status organisations with no e-filed 990 [V wave 34B]."
   - **Replace with:** "go to church-status organisations with no e-filed 990 [V wave 34B]. Only about 4.4 of those 8.3 points go to congregations by name rules; the rest go to ministries, denominational bodies, schools and unclassified names ([b4026-06-church-daf-recipients.md](b4026-06-church-daf-recipients.md)) [V wave 35C]."

### `research/mission-2026-11-14/direction-faith-giving-platforms.md`

1. **Find:** "None of the congregations was scanned: LDS had no donate link, Life.Church was unreachable, and the others had no website."
   - **Replace with:** "None of the congregations was scanned: LDS had no donate link, Life.Church was unreachable, and the others had no website. Under the name rules of [b4026-06-church-daf-recipients.md](b4026-06-church-daf-recipients.md), two of the four are congregations (Life.Church, Ohr Torah); LDS is the denominational central and Amidei Zion of Bobov is unclassified. That study then read 14 pages of 50 seeded church-block congregations (10 giving pages, 4 homepages): none showed a DAF option (95% upper bound 21.5%), and a wave-35C re-read of 8 giving pages confirmed this [V wave 35C]."
2. **Find:** "- **Inference:** this probably keeps DAF options off congregation pages."
   - **Replace with:** "- **Inference:** this probably keeps DAF options off congregation pages. The 14 congregation pages later read (b4026-06) showed Subsplash (5), Pushpay (3) and Planning Center (1), with no platform detected on 7, and none showed a DAF option [O] [V wave 35C]."
3. **Find:** "A DAFpay widget on a church page would serve mainly donors at national sponsors [I]."
   - **Replace with:** "A DAFpay widget on a church page would serve mainly donors at national sponsors [I]. In the top-50 church block, nationals send 74.2% of DAF-weighted dollars and the seven faith sponsors 22.1%, against the faith sponsors' 10.0% of all top-50 dollars (b4026-06) [V wave 35C]."

### `research/mission-2026-11-14/strategic-synthesis.md`

1. **Find:** "and 11 of 14 grant-delay records predate the rule versions read ([g1913-processor-disbursement-rules.md](g1913-processor-disbursement-rules.md); wave 33A) [V wave 34S]."
   - **Replace with:** "and 11 of 14 grant-delay records predate the rule versions read ([g1913-processor-disbursement-rules.md](g1913-processor-disbursement-rules.md); wave 33A) [V wave 34S]. Congregations are the extreme case. Church-status recipients with no e-filed 990 take 8.3% of top-50 DAF dollars, about half of it congregations, three-quarters of it from national sponsors; none of 14 congregation giving pages read showed a DAF option ([b4026-06-church-daf-recipients.md](b4026-06-church-daf-recipients.md)) [V wave 35C]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

Waves 35A and 35B may insert §11.36 and §11.37 first (§11.36 is already present on 2026-11-19). The Find anchor stays unique either way, so this item applies after them.

1. **Find:** "\n---\n\n## Source register"
   - **Replace with:** "\n### 11.38 Church recipients of DAF grants (validated, wave 35C)\n\n**Church recipients of DAF grants** (validated, wave 35C). Church-status recipients with no e-filed 990 (IRS BMF FOUNDATION 10, \"Church 170(b)(1)(A)(i)\") take $6,177.5m of top-50 FY2023–24 DAF-weighted Schedule I dollars, 8.34% of $74,073.8m, across 29,469 recipients. By name rules only 52.2% of that reaches congregations. The rest goes to ministries and orders (15.6%), denominational bodies (13.4%, mostly the LDS Church's $464.2m), schools (8.5%) and unclassified names (10.4%); denominational-body labels are the least reliable. Dollars are concentrated: the Gini is 0.816, the top 1% of recipients take 42.5% and the bottom half 4.2%, and the median church receives $39,057 over two years. Seven faith sponsors send 22.1% of these dollars, against their 10.0% of all top-50 dollars. National sponsors send 74.2%, led by Fidelity Charitable at 34.9%. The 54 Outreach 100 megachurches that match strictly take only $138.4m (2.2%). None of 14 congregation pages read showed a DAF option (95% upper bound 21.5%); Subsplash and Pushpay were the usual platforms (repo [`validation-wave35c-report.md`](mission-2026-11-14/validation-wave35c-report.md)) [V wave 35C]\n\n---\n\n## Source register"

**Check.** `v35c/tools/checkfinds.py` parses every Find in this section, unescapes `\n` and `\"`, and counts its occurrences in the target file as it stands when this report was finished. Every Find occurred exactly once (21 of 21). It then applied all 21 replacements in order to scratch copies; each Find was still unique when its turn came. The industry-report anchor `\n---\n\n## Source register` occurs once whether or not §11.37 has been inserted, because waves 35A and 35B insert their sections above that anchor.
