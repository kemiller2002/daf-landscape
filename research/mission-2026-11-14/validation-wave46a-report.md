# Validation wave 46A: non-BMF recipients (b40n1202-b43n26-03) and Foundant docs / NCF donate button (b4222-02-01-01)

**Date:** 2026-11-20 · **Validator:** validator wave 46A · **Register:** [`validation-register-wave46a.csv`](../../data/mission-2026-11-14/validation-register-wave46a.csv) (23 rows, V46A-01 to V46A-23)

**What was done**
- **Study 1.** Re-ran `scripts/mission_non_bmf_recipients.py` twice with `--out` sent to scratch: once without the base pickle (fresh build), and once with `PYTHONHASHSEED=7`. Both CSVs are byte-identical to the committed file. Wrote my own stdlib pass over the raw IRS files (BMF eo1–4/eo_pr/eo_xx, Pub 78, revocation list, e-Postcard, TEOS index 2019–2026). It does not use the study's loaders, and it reproduces every evidence count. Recomputed the revoked-at-grant timing from the revocation file and the cached sponsor lines with my own fiscal-year arithmetic. Spot-checked 28 EINs across all seven categories. Fetched four return XMLs from the GivingTuesday mirror (robots.txt 404): the granting sponsor's FY2023 990 (Schedule I lines and purpose text for the CZ LLCs), Chan Zuckerberg Biohub Inc's FY2023 and FY2024 990s (Schedule R), and NCF's FY2024 990. Read IRS Notice 2012-52 (www.irs.gov robots.txt 200; `/pub/` not disallowed).
- **Study 2.** Read robots.txt for foundant.com, www.foundant.com, help.foundant.com, support.foundant.com, www.ncfgiving.com and secure.ncfgiving.com (2026-11-20 04:08 UTC). Read https://www.ncfgiving.com/guide-to-giving-at-NCF once and https://www.ncfgiving.com/terms-and-disclosures once. Fetched no other NCF page and no sitemap. Grepped research/ and data/ for `secure.ncfgiving.com` and classified every line. web.archive.org was unreachable (connection reset), so no dated copy of the secure-site robots.txt could be read.
- All scripts ran with `python3 -B` (`-I` for parsers of downloaded files). User agent `research-script/1.0`. No outreach, logins or forms. sec.gov, crt.sh and certspotter were not used. No Foundant page and no secure.ncfgiving.com page other than robots.txt was requested.

## Counts

| Study | Rows | confirmed | partially confirmed | contradicted | unverifiable |
|---|---|---|---|---|---|
| 1. Non-BMF recipients (b40n1202-b43n26-03) | 14 | 11 | 2 | 1 | 0 |
| 2. Foundant docs / NCF donate (b4222-02-01-01) | 9 | 7 | 0 | 0 | 2 |
| **Total** | **23** | **18** | **2** | **1** | **2** |

The one "contradicted" row is the parent note's claim (V46A-14), which the study itself overturns. It is not a fault in the study.

## Findings

### Study 1: non-BMF recipients

1. **Every headline number reproduces (V46A-01, -02, -04 to -06, -08 to -10).** The two reruns are byte-identical. My independent pass gives:
   - 22,269 EINs, none in any BMF file;
   - $4,175.4m DAF-weighted;
   - 18,928 with no IRS trace and 3 in Pub 78;
   - 1,613 with a revocation row, 1,441 of them not reinstated;
   - 1,252 in the e-Postcard file and 2,271 in the TEOS index (2,254 990-series).

   My own timing code gives the same revoked-at-grant figures:
   - effective before the fiscal year: $7.237m, 141 EINs, 32 sponsors;
   - of which posted before the fiscal year: $6.328m, 110 EINs, 30 sponsors;
   - after the fiscal year: $65.04m, 1,092 EINs;
   - median 4.13 years from revocation to fiscal-year start; top four sponsors 63.6% of the before-FY dollars.
2. **The CZ LLCs are disregarded entities of a public charity (V46A-03).**
   - **The grants.** All $1,594.0m sits on one sponsor's FY2023 Schedule I. The four lines carry IRC section "501(c)(3)" and purpose "Health".
   - **The parent.** Chan Zuckerberg Biohub Inc (EIN 81-1669175) lists all four EINs in Schedule R Part I (disregarded entities) on its FY2023 and FY2024 Forms 990. The entries give Delaware domicile and "MEDICAL RESEARCH" as the activity. Biohub Inc is in the current BMF as a 501(c)(3) with foundation code 12 (hospital or medical research organisation) and in Pub 78 as PC.
   - **What they are not.** The LLCs are not the for-profit CZI LLC. They are not part of the Chan Zuckerberg Initiative Foundation (45-5002209) either; that foundation is a private foundation and appears on the same Schedule R only as a related exempt organisation.
   - **Grants to a non-charity?** No. IRS Notice 2012-52 treats a contribution to a domestic disregarded SMLLC wholly owned by a US charity "as a charitable contribution to a branch or division of the U.S. charity". That notice addresses §170 contributions, so applying it to a DAF distribution is an analogy [I]. On that reading the money went to Biohub Inc.
   - **Consequence for the parent note.** If CN credited these dollars to Biohub Inc, which e-filed full 990s for tax years 2020–2024, the parent's central eligible share would rise from 76.85% to 79.00% [I]. That is an interpretation the owner should decide. CN's own text ("nonprofit subsidiaries", "consolidated subsidiaries") does not settle it.
3. **The parent's 77.3% upper bound falls (V46A-05, -14).**
   - 884 of the 1,213 filing-rule passers ($220.4m) carry final, terminate or dissolve flags on their latest e-filed return. I spot-checked five of them in the header cache. The flags sit on 2025 returns, so these organisations were live when paid but cannot be listed now.
   - The parent's bound computes to (56,926,230,791 + 292,779,371) / 74,073,755,051 = 77.25%, which rounds to 77.2%; "77.3%" came from adding rounded figures.
   - Counting only the 126 unresolved passers ($43.4m) and the 15 new EINs ($9.1m) gives 76.92%. The bound is therefore about 76.9%, which is effectively the central figure.
4. **One mis-keyed DAF-to-DAF line sits in the revoked signal (V46A-08).**
   - **The line.** One line worth $0.876m DAF-weighted names a national DAF sponsor as recipient under an EIN that the revocation list gives to a different, similarly named entity revoked in 2019. The sponsor's own EIN is in the BMF.
   - **Why it matters.** The parent's DAF-to-DAF filter missed it because the EIN was wrong. It is a mis-keyed transfer, not a grant to a revoked charity.
   - **Effect.** Net of it, the posted-before signal is $5.45m rather than $6.33m, and the partial-name sub-bucket is $0.44m rather than $1.32m.
   - **Upper bound.** "No BMF successor" is an upper bound. For example, a charter-school network revoked in 2023 (after-FY bucket) has a "... II" entity in the BMF.
5. **The "600" heuristic is weak but immaterial (V46A-07).**
   - **Size.** It labels 111 EINs ($13.5m, 2.3% of the government bucket). One university accounts for $7.24m of that.
   - **My sample.** In a seeded random 20, two are clearly not governmental: a co-cathedral and a synagogue whose names escape the religious filter. Two more are doubtful. This matches the study's 4 of 20.
   - **Not a government marker.** 5,678 EINs in the current BMF share the digit pattern, 3,614 of them 501(c)(3), mostly churches, trusts and unions.
6. **Small issues.**
   - **Sensitivity count (V46A-13).** The figure varies by one EIN between runs: 2,360 in the author's run, 2,361 in both of mine, with $238.33–238.35m. The CSV stays byte-identical. The capped fuzzy search is order-dependent.
   - **Header cache naming.** The cache field `filer_name` holds the preparer firm's name, not the filer's. It is not used for classification.
7. **The framing passes (V46A-11).**
   - No sponsor is named in the doc, CSV or JSON.
   - The doc says the screen is not evidence of improper grants.
   - It covers retroactive reinstatement, unknown grant dates and expenditure responsibility.
   - Two phrases lean evaluative: "screen of sponsor due diligence" and "the core of the signal". Corrections reword both.

### Study 2: Foundant docs / NCF donate button

1. **Robots claims hold (V46A-15 to -17).**
   - All three Foundant hosts serve `User-agent: ClaudeBot`, `anthropic-ai` and `Claude-Web` groups with `Disallow: /`. The `*` group has `Content-Signal: search=yes,ai-train=no,use=reference`. `Claude-User` is not named. support.foundant.com names no Anthropic token.
   - www.ncfgiving.com allows all paths and declares one sitemap.
   - secure.ncfgiving.com serves the Salesforce template ("robots.txt for sfdc appservers"). It allows `googlebot`, then gives `*` `Disallow: /` except login-parameter URLs. The study omits the googlebot allowance.
2. **The quotes are verbatim (V46A-19, -20).**
   - All eight guide passages match the tag-stripped HTML, as do both terms clauses.
   - The guide links to `secure.ncfgiving.com/agreement` twice.
   - The terms define "Public Website" as "ncfgiving.com, and any other public websites owned and operated by NCF". They carry no date beyond the © 2026 footer.
3. **Schedule D matches the raw XML (V46A-21).** Return 202513109349303201 reads: 31,943 DAFs; contributions $2,907,564,434; grants $2,433,041,612. The source register cites ProPublica, but the primary source is the IRS XML.
4. **The sitemap count is unverifiable (V46A-18).** I did not fetch the sitemaps: NCF's terms bar automated extraction, and the brief allowed only the guide and the terms. No cached copy exists in scratch.
5. **The provenance flag is accurate (V46A-22, -23).** The secure-site disallow is current. Its state on 2026-11-14 cannot be known. The b4222 doc says "the carried census row says as much", but the census row does not mention robots. The earliest repo record of the disallow is the batch 35 B robots log (2026-11-15).

## Accept / modify / reject

| Claim | Register | Decision | Note |
|---|---|---|---|
| 22,269 EINs, $4,175.4m; 1,213 / $292.8m pass CN rules | V46A-01 | Accept | Byte-identical; independent sums |
| 18,928 untraced; 3 in Pub 78 | V46A-02 | Accept | Independent pass |
| Four CZ LLCs $1,594.0m; LLC label on name rules | V46A-03 | Modify | Schedule R confirms disregarded entities of Biohub Inc (501(c)(3)); add look-through note |
| 14,772 religious untraced, $1,348.4m | V46A-04 | Accept | Explanation stays [I] |
| 884 of 1,213 terminated; 77.3% too generous | V46A-05 | Modify | State the numbers: 77.25% → 76.92% |
| Government $595.6m | V46A-06 | Accept | Mostly name rules |
| "600" heuristic | V46A-07 | Modify | Add base rate and second sample |
| Revoked before FY $7.24m / 141 / 32; $6.33m | V46A-08 | Modify | $0.88m is a mis-keyed DAF-to-DAF line; core $5.45m |
| $65.0m after FY | V46A-09 | Accept | |
| Typo EINs $46.4m / 569 | V46A-10 | Accept | |
| Revoked framing | V46A-11 | Modify | Two wording changes |
| Spot-checks | V46A-12 | Accept | 28 EINs |
| Sensitivity 2,360 | V46A-13 | Modify | 2,360–2,361 |
| Parent "about 77.3%" upper bound | V46A-14 | Reject | Replace with ~76.9% (and note CZ look-through) |
| Foundant robots | V46A-15 | Accept | |
| secure.ncfgiving.com disallow | V46A-16 | Accept | Note googlebot allow |
| www.ncfgiving.com allows | V46A-17 | Accept | |
| 659 sitemap URLs, 0 donate pages | V46A-18 | Accept as carried (unverified) | Not re-fetched |
| Guide quotes | V46A-19 | Accept | |
| Terms clause | V46A-20 | Accept | |
| Schedule D FY2024 | V46A-21 | Accept | |
| Repo provenance flag | V46A-22 | Modify | Census-row statement wrong; add provenance note |
| Disallow on 2026-11-14 | V46A-23 | Unverifiable | Owner decision |

## NCF Program Agreement provenance (owner decision)

**Status of the robots rule.**
- **Current file.** https://secure.ncfgiving.com/robots.txt, re-read 2026-11-20 04:08 UTC, has `User-agent: *` with `Disallow: /`, allowing only login-parameter URLs. `googlebot` is allowed. The file header reads "robots.txt for sfdc appservers … For use by salesforce.com", so this is the Salesforce platform default.
- **Earliest record.** The earliest repo record of the rule is the batch 35 B robots log in `research/mission-2026-11-14/queue-batch35-access-owners-faith.md`, prepared 2026-11-15. That file also discloses one request to `/agreement` made before robots.txt was read; its content was discarded.
- **The original read.** The study that read the agreement on 2026-11-14 (`queue-sponsor-terms-data-clauses.md`) logs no robots check.
- **What cannot be known.** The template origin suggests the rule predates 2026-11-14 [I]. No dated copy could be read (web.archive.org was unreachable), so the state on 2026-11-14 is **unknown**.

**Affected references.** There are 74 lines (87 occurrences) in 37 files under research/ and data/:

*A. Program Agreement content or `/agreement` citations (33 lines; 13 of them in the b4222-02-01-01 outputs, which quote nothing from the agreement)*
- `data/mission-2026-11-14/sponsor-terms-clauses-2026.csv`: 5 NCF clause rows (credential sharing ×2, aggregator, scraping, liability). These are verbatim quotes.
- `research/mission-2026-11-14/queue-sponsor-terms-data-clauses.md`: lines 55, 83 and 182, the NCF census row, the findings row and source T03.
- `data/mission-2026-11-14/sponsor-terms-census-top20-2026.csv`: rank-10 row, carried from the above.
- `research/mission-2026-11-14/queue-all-in-cost-dafpay-access.md`: lines 151 (two quotes) and 304.
- `data/mission-2026-11-14/delegated-access-routes-2026.csv`: DA11.
- `data/mission-2026-11-14/validation-register-wave9.csv`: one row; `research/mission-2026-11-14/validation-wave9-report.md`: line 133.
- `research/mission-2026-11-14/queue-batch35-access-owners-faith.md`: lines 281 and 287, the robots log and the disclosure.
- Queue lists: `research-priority-inputs.csv` (line 265), `research-priority-queue.csv` (line 579) and `queue-proposals-terms.csv` (line 2). These cite the URL only.
- `citation-link-health-2026-11-19.csv`: the `/agreement` row, marked "not checked".
- **Derivative claims without the URL:**
  - `research/DAF-INDUSTRY-REPORT-2026-11.md` line 580 ("NCF's 2025 Program Agreement bans credential sharing …") and line 536 ("NCF donors, whose terms bar this");
  - `research/mission-2026-11-14/gap19-ai-coverage-20-entities.md` line 67;
  - `data/mission-2026-11-14/sponsor-obbba-tax-page-audit-2026-11-19.csv`, NCF row ("Program Agreement scraping clause covers the Secure Site").

*B. Login-page fingerprints from `secure.ncfgiving.com/` or `/grant` (32 lines)*

These rest on the page title "MyGiving with NCF", `sfdc`/`skuid` resources and `server: sfdcedge` headers. Robots disallows `/`, so these reads were also of a disallowed path.
- **Research notes:**
  - `queue-batch33-market-structure.md` (2 lines);
  - `queue-bank-programs-and-eft-providers.md` (3);
  - `breadth-community-faith-infrastructure-emerging.md` (S09: lines 28, 104, 331);
  - `queue-donor-export-cf-payments-donorsphere.md` (4);
  - `validation-wave6-report.md` (1).
- **Data files:**
  - `validation-register-wave6.csv` (1);
  - `faith-sponsor-platforms-2026.csv` (1);
  - `quadrant-scores-A1-v12a.csv`, `-v12b.csv`, `-v12consensus.csv` (2 each);
  - `quadrant-scores-A1-primary.csv` and `quadrant-scores-A1-consensus.csv` (1 each);
  - `donor-data-export-top10-2026.csv` (1);
  - `bank-program-terms-2026.csv` (1);
  - `relationship-graph-edges-additions-8.csv`, `-additions-18.csv` and `relationship-graph-edges-consolidated-2026-11-19.csv` (1 each; edge ER001, NCF → Salesforce);
  - `breadth-entity-profiles.csv` (1);
  - `citation-link-health-2026-11-19.csv` (3 rows, "not checked").

*C. DNS-only or unchecked links that never touched the host (9 lines)*
- `quadrant-scores-A1-v11.csv`, `-v11blind.csv` and `-v11consensus.csv`;
- `research-priority-inputs.csv` line 96, `research-priority-queue.csv` line 742 and `queue-proposals-quadrant-A1.csv`;
- `breadth-community-faith-infrastructure-emerging.md` lines 27 and 330 (S08, dns.google);
- `citation-link-health-2026-11-19.csv` line 427.

**Options for the owner.** These are not applied here; nothing has been deleted.
1. **Keep with a provenance flag.** Annotate class A and B rows with: "read from a host whose robots.txt disallowed all agents by 2026-11-15; state on the read date unknown". The claims stay usable, and the reader can weigh them.
2. **Re-source class A by a compliant route.** The owner (a person, not an agent) reads the Program Agreement in a browser, or asks NCF for a copy. The quotes are then re-cited to that reading. The public-site terms (www, robots-allowed) can carry the scraping and AI-use point for the public site only. They do not cover credential sharing or third-party access to the Secure Site.
3. **Re-source class B by DNS.** The repo already shows that `secure.ncfgiving.com` CNAMEs to `*.live.siteforce.com`, through dns.google (S08), which never touches the host. That keeps "NCF's portal is hosted on Salesforce". The Skuid and page-title details would then become "carried, unverified".
4. **Downgrade.** Mark class A clauses [R] (carried, not re-verifiable) and keep the industry-report sentence at line 580 only as "NCF's terms, as read in the repo on 2026-11-14".
5. **Remove.** Delete class A quotes and class B fingerprints. This loses the only NCF credential-sharing evidence; option 2 would be needed to restore it.

Class C needs no action. The b4222-02-01-01 study used no agreement clause and gets only the provenance note below.

## Exact corrections

### `research/mission-2026-11-14/b40n1202-b43n26-03-non-bmf-recipients.md`

**Find:** "  - The subsidiary category's label (LLC, disregarded) rests on name rules [I]."
**Replace with:** "  - The subsidiary category's label (LLC, disregarded) rests on name rules [I]. For the four CZ EINs (99% of the bucket's dollars) validation confirmed it from Schedule R: they are disregarded entities of Chan Zuckerberg Biohub Inc (EIN 81-1669175), a BMF-listed 501(c)(3), and not for-profit entities (§3.2). [V wave 46A]"

**Find:** "At most about $43m of the $293m (0.06 points of top-50 dollars) looks like live organisations that CN might list [I]."
**Replace with:** "At most about $43m of the $293m (0.06 points of top-50 dollars) looks like live organisations that CN might list [I]. In numbers: the parent’s bound, ($56.93bn + $292.8m) ÷ $74.07bn, is 77.25%, which rounds to 77.2%, not 77.3%. Counting only the 126 unresolved passers ($43.4m) and the 15 new EINs ($9.1m) gives 76.92%, so the bound falls to about 76.9%, the central figure. [V wave 46A]"

**Find:** "A single-member LLC owned by a 501(c)(3) is normally disregarded for tax purposes and has no BMF row of its own [I]. The parent's Schedule R would confirm this (P-B40N1202-B43N2603-02)."
**Replace with:** "A single-member LLC owned by a 501(c)(3) is normally disregarded for tax purposes and has no BMF row of its own [I]. Validation read the parent’s Schedule R (P-B40N1202-B43N2603-02 answered). Chan Zuckerberg Biohub Inc (EIN 81-1669175) lists all four EINs in Schedule R Part I (disregarded entities) on its FY2023 and FY2024 Forms 990 (returns 202423199349303562 and 202513219349324416), with Delaware domicile and ‘MEDICAL RESEARCH’ as the activity. Biohub Inc is a BMF-listed 501(c)(3) (foundation code 12, medical research organisation; Pub 78 PC). The sponsor’s FY2023 Schedule I lines give IRC section ‘501(c)(3)’ and purpose ‘Health’. The LLCs are not the for-profit CZI LLC. The Chan Zuckerberg Initiative Foundation (45-5002209, a private foundation) appears on the same Schedule R only as a related exempt organisation. IRS Notice 2012-52 treats a contribution to a domestic disregarded SMLLC wholly owned by a US charity ‘as a charitable contribution to a branch or division of the U.S. charity’. By analogy [I], these DAF grants went to a charity, not to a non-charity. If CN credited them to Biohub Inc, the parent’s central eligible share would be about 79.0% rather than 76.9% [I]. [V wave 46A]"

**Find:** "- $1.32m (11 EINs): partial name match."
**Replace with:** "- $1.32m (11 EINs): partial name match. $0.88m of it is a single line naming a national DAF sponsor as recipient under an EIN that the revocation list gives to a different, similarly named entity revoked in 2019; the sponsor’s own EIN is in the BMF. That is a mis-keyed DAF-to-DAF transfer that the parent’s filter missed, not a grant to a revoked charity. Net of it, the posted-before signal is $5.45m. [V wave 46A]"

**Find:** "This is the core of the signal."
**Replace with:** "This is the residual that a public-data screen would flag. ‘No BMF successor’ is an upper bound, because a successor that files under a changed name is not matched. [V wave 46A]"

**Find:** "public-data screen of sponsor due diligence, not evidence of improper grants.**"
**Replace with:** "public-data screen, not evidence of improper grants or of any lapse in a sponsor’s diligence.** [V wave 46A]"

**Find:** "about 4 of 20 sampled cases look non-governmental [I]."
**Replace with:** "about 4 of 20 sampled cases look non-governmental [I]. Validation drew another random 20 of the 111. Two are clearly not governmental: a co-cathedral and a synagogue, whose names escape the religious filter. Two more are doubtful. The digit pattern is not a government marker: 5,678 EINs in the current BMF share it, 3,614 of them under 501(c)(3), mostly churches, trusts and unions. The rule moves only $13.5m (2.3% of the government bucket), and one university is $7.24m of that. [V wave 46A]"

**Find:** "Sensitivity: 2,360 of these EINs ($0.24bn) carry a name that matches exactly one same-state BMF EIN (902 exact, 1,458 fuzzy)."
**Replace with:** "Sensitivity: 2,360–2,361 of these EINs ($0.24bn) carry a name that matches exactly one same-state BMF EIN (902 exact, 1,458–1,459 fuzzy). The count varies by one EIN between runs (two validation reruns gave 2,361, with $238.33m and $238.35m), while the CSV stays byte-identical, because the capped fuzzy search is order-dependent. [V wave 46A]"

### `research/mission-2026-11-14/b40n1202-b43n26-recipient-basis-and-rating-eligibility.md`

**Find:** "These may be new or recently re-listed organisations [I], so the upper bound on eligibility is about 77.3% [I]."
**Replace with:** "These may be new or recently re-listed organisations [I], so the upper bound on eligibility is about 77.3% [I]. b40n1202-b43n26-03 shows most are not: 884 of the 1,213 ($220.4m) filed a final return or reported terminating or dissolving. Only 126 unresolved ($43.4m) and 15 new EINs ($9.1m) look live, which puts the bound at about 76.9% (76.92%; the original bound computes to 77.25%). Separately, the four CZ LLCs are disregarded entities of Chan Zuckerberg Biohub Inc (EIN 81-1669175), a BMF-listed 501(c)(3), on its FY2023–24 Schedule R. Credited to that parent, the central share would be about 79.0% [I]. [V wave 46A]"

### `research/mission-2026-11-14/b4222-02-01-01-foundant-docs-ncf-donate.md`

**Find:** "That host's robots.txt disallows `/` for all agents, and the carried census row says as much."
**Replace with:** "That host's robots.txt disallows `/` for all agents. The carried census row does not record this. The earliest repo record of the disallow is the batch 35 B robots log (queue-batch35-access-owners-faith.md, prepared 2026-11-15). [V wave 46A]"

**Find:** "Queue P-B4222-020101-03 asks the owner to review them."
**Replace with:** "Queue P-B4222-020101-03 asks the owner to review them.\n- **Provenance note (validation).** secure.ncfgiving.com/robots.txt was re-read on 2026-11-20 at 04:08 UTC. It is the Salesforce platform template (‘robots.txt for sfdc appservers’): `googlebot` is allowed, and `*` is disallowed on `/` except login-parameter URLs. The 2026-11-14 study that read the agreement logged no robots check, so whether the disallow applied that day cannot be known. The Wayback Machine was unreachable from the validation session. 74 lines in 37 files under research/ and data/ cite the host, for Program Agreement clauses and for login-page fingerprints. The options are left to the owner (validation-wave46a-report.md). [V wave 46A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.67 Non-BMF recipients resolved; NCF agreement provenance (validated, wave 46A)\n\n**Non-BMF recipients resolved; NCF agreement provenance** (validated, wave 46A). The non-BMF study re-runs byte for byte, and an independent pass over the raw IRS files reproduces its counts: 22,269 EINs ($4,175.4m DAF-weighted), 18,928 with no IRS trace and 3 in Pub 78. The four CZ LLCs ($1,594.0m) are disregarded entities of Chan Zuckerberg Biohub Inc (EIN 81-1669175), a BMF-listed 501(c)(3), on its FY2023–24 Schedule R. They are not for-profit. Credited to that parent, the central eligibility share would be about 79.0% rather than 76.9% [I]. 884 of the 1,213 filing-rule passers have since filed final or terminating returns, so the parent’s ‘about 77.3%’ upper bound falls to about 76.9%. EINs revoked before the grant year received $7.24m; $0.88m of that is one national sponsor named under a wrong EIN. The ‘600’ EIN rule is weak but moves only $13.5m. The Foundant and NCF robots, quote and Schedule D claims hold. 74 repo lines cite secure.ncfgiving.com, whose robots.txt now disallows all agents; its state on 2026-11-14 cannot be known, so the owner decides (repo [`validation-wave46a-report.md`](mission-2026-11-14/validation-wave46a-report.md)) [V wave 46A]\n\n---\n\n## Source register"
