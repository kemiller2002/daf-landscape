# Validation wave 41A: open DAF grant record draft (b4013-03-02) and non-cash vendors / DAFpay Network (b40n14-03-b38c-03)

**Validator:** independent-validation-agent-wave41a · **Date:** 2026-11-20 · **Register:** [`validation-register-wave41a.csv`](../../data/mission-2026-11-14/validation-register-wave41a.csv) (31 claims)

**Checked:** [b4013-03-02-daf-grant-record-schema.md](b4013-03-02-daf-grant-record-schema.md), `standards/daf-grant-record/` (schema, 24 vectors, `tools/make_vectors.py`) and `scripts/mission_validate_grant_record.py`; [b40n14-03-b38c-03-noncash-vendors-dpn.md](b40n14-03-b38c-03-noncash-vendors-dpn.md), `noncash-vendor-volumes-2026-11-20.csv` and `scripts/mission_noncash_vendors.py`. Nothing was committed or pushed.

## Counts

| Result | Study 1 (grant record, V41A-01 to -15) | Study 2 (vendors / DPN, V41A-16 to -31) | Total |
|---|---|---|---|
| confirmed | 8 | 11 | 19 |
| partially_confirmed | 6 | 4 | 10 |
| contradicted | 1 | 1 | 2 |
| unverifiable | 0 | 0 | 0 |
| **Total** | **15** | **16** | **31** |

| Items | Accept | Modify | Reject |
|---|---|---|---|
| Proposed corrections in b40n14-03-b38c-03 §5 (15) | 6 | 9 | 0 |

Fourteen further corrections apply to the two studies themselves (C01–C07 for the grant record, C08–C14 for the vendor study), and one summary goes into the industry report (§11.54).

## Method

- **Study 1 re-run.** `python3 -I scripts/mission_validate_grant_record.py . <scratch>/q1303/std/log.jsonl <scratch>/q1332/web/log.jsonl` prints `RESULT: PASS`: 24 of 24 vectors, 55 provenance entries (4 / 19 / 20 / 12), 43 snippets, self-test 12/12.
- **Independent schema check.** jsonschema 4.26.0 is installed in this environment. `Draft202012Validator.check_schema` accepts the schema. Every vector was then validated with that package and its top-level errors compared with `expected_errors`. Keyword use was also reviewed by hand against draft 2020-12.
- **Generator.** `standards/daf-grant-record/tools/make_vectors.py` is identical to the scratchpad copy. Run into a scratch root, it rebuilds all 24 vector files byte for byte.
- **Conversions.** Chariot's cached page (sha256 `8c17df40…`) and Endaoment's OpenAPI 4.88.0 (sha256 `7790bd52…`) were read for the cents, USDC and anonymity fields.
- **Candid.** robots.txt was re-read for taxonomy.candid.org (200; `/content/*`, `/search*`, `/media/*` and others disallowed) and developer.candid.org (200). The developer page was re-fetched (200). The PCS home, Support Strategies and FAQ pages are allowed, but the live re-fetch got a Cloudflare 403 block page. The user agent (`research-script/1.0`) was not changed. The quotes were checked in the study's caches of the same day instead.
- **Study 2 re-run.** The script was re-run on the q1403 caches into a scratch root. Its CSV is byte-identical (md5 `b9e8f49bdae2e5caf7c1bedbf8112893`, 1,687 rows).
- **XML.** Eighteen XMLs were parsed independently, with a separate parser:
  - FreeWill Impact Fund TY2021–24, with Schedule M, Schedule I, Part III, Part IV and the schedules list;
  - DonateStock FY2022–25: 202342659349300229, 202413209349328306, 202542229349300304, and the TEOS member 202632859349300138;
  - GVNGorg TY2021–24, including the amended returns;
  - DPN TY2024–25.
- **Web.** These were re-fetched after robots.txt was checked:
  - thegivingblock.com/annual-report/ (robots allows it);
  - investors.shift4.com robots.txt (it disallows only `/form-submit`) and one results release.
  - The 10-K/10-Q text came from the study's cached IR-site PDFs.
- **Not used:** sec.gov, crt.sh and certspotter. There was no outreach.
- **Uniqueness.** A script parsed every item in "Exact corrections" below and counted each Find in its target file, both alone and with earlier items applied in order. All 30 occur exactly once (§ Uniqueness check).

## Findings

### Study 1: draft open DAF grant record

1. **The vectors and the validator hold up.** jsonschema 4.26.0 gives each negative vector exactly its declared `(path, keyword)` errors and nothing else. neg-13 also gives `oneOf`, as the study says. All four positive vectors validate (V41A-01, -02).
2. **The schema is valid 2020-12. The limit stating that no package could be installed is wrong.**
   - All keywords are standard, `$ref` targets resolve locally, and the four `oneOf` branches are mutually exclusive through `facet` const.
   - The metaschema check passes with the jsonschema 4.26.0 package that is already present. The study's §7 limit should be withdrawn (C01).
3. **The conversions are right.**
   - Chariot: 25000 integer cents becomes “250.00” USD (“integer cents in USD (e.g., `25000` = $250.00)”).
   - Endaoment: '1000000' USDC smallest units becomes “1.00” (“(1000000 = 1 USD)”), and the sub-cent value 1.234567 is rejected.
   - Chariot anonymity: `anonymous: false` maps to `full_contact`. Chariot's text says true withholds “the donor's name and contact details”, “per your standard anonymity handling”.
4. **Endaoment's `name_only` mapping is an inference** (V41A-11).
   - `shareMyEmail` controls only the “fund's donor-of-record email”.
   - `recommender` is the “Name of the person recommending the grant”. Nothing says the name reaches the recipient, or that the recommender is the donor of record (C06).
5. **The Candid licence holds, but the up-to-5 rule applies per facet.**
   - The CC BY 4.0 quote and the footer statement are in the cached home page (robots-allowed, fetched 2026-11-20). The live re-fetch was blocked (403), so this rests on the study's own cache (V41A-05).
   - The Support Strategies page and the Subjects page each say grant details “can have up to 5 codes”. The schema's `maxItems: 5` over all facets combined is stricter than Candid's practice (C04, C05).
6. **The developer page was re-fetched live.** It still shows the four codes `SC020000`, `PA020000`, `UA0000` and `TA00`, and still carries no licence statement.
7. **The generator is in the repo, not only in the scratchpad.** §1 and §7 say otherwise (C02, C03, V41A-12).
8. **A regex anchor gap.** Python's `$` matches before a trailing newline, so an EIN with a trailing newline passes both the repo validator and jsonschema. An ECMA-262 validator would reject it (C07). Impossible dates such as 2026-02-31, and 15-digit amounts, also pass, as the study discloses.
9. **Stale provenance note.** pos-02 (status `approved`) inherits the note “Status is pending” for `payment_reference` from the shared Chariot list (`make_vectors.py` line 77).
   - pos-03 carries an on-chain hash while its status is `pending`. The schema allows that.
   - This is cosmetic. Fixing it in the generator would also refresh pos-02. No exact correction is given, to keep the vectors reproducible until the generator is edited.
10. **Labelling is adequate.** “Draft, unendorsed” appears in:
    - the schema title, description and `$comment`;
    - every vector's `status_label`;
    - the doc banner.
    The `$id` is a `urn:x-draft` URN. The limits should add the per-facet cap, the anchor gap and the `name_only` inference (C04, C06, C07).

### Study 2: non-cash vendors and DPN

1. **The FreeWill figures are right.**
   - TY2024 contributions: $11,891,225, all non-cash.
   - Schedule M: crypto $7,628,569 in 648 gifts; securities $4,262,656 in 338.
   - Schedule I: 91 lines, $10,992,875. Part IX line 1: $11,852,523.
   - The Oregon Community Foundation received $5,430,494: 45.67% of intake and 49.40% of Schedule I.
   - DAFRC-sponsor lines total $5,448,657 (49.57%).
2. **The 55,000 bounds arithmetic is right.**
   - Floor: 91 + ⌈859,648 / 5,000⌉ = 263. Ceiling: 648 + 338 = 986.
   - Shares of 55,000: 0.478% to 1.793%, and 1.178% for crypto alone.
   - Intake per claimed nonprofit: $216.2.
   - The comparison stays indicative. FreeWill's 55,000 covers the whole tool, much of which routes stock directly to nonprofits.
3. **Contradicted: “no Schedule D is filed” for FreeWill.**
   - The TY2023 and TY2024 returns attach Schedule D: land and buildings $0, the Part XI–XII reconciliation and a Part XIII note. They have no Part I.
   - The study's own CSV flags `sched_d_present` True for both years.
   - The classification still holds, because R1 tests Schedule D with DAF assets. The wording must say “no Schedule D Part I” (C09, N07, N10). TY2024 is also audited (`FSAuditedInd` 1).
4. **The DonateStock anomaly is confirmed.**
   - FY2023 and FY2024: Part IV line 6 is true and Schedule D shows 33 funds, but `DonorAdvisedFundsContriAmt` and `DonorAdvisedFundsGrantsAmt` are absent. Part VIII shows $5,078,851 and $12,778,129.
   - FY2025: line 6 false, no Schedule D, $25,121,004 of contributions and 2,630 gifts. Schedule M totals $25,120,929, $75 lower.
   - DonateStock Inc was paid $709,796, which is $668,396 + $41,400 and 2.83% of intake.
   - The recipient floors are 361, 319 and 588.
5. **DonateStock's narrative is not repeated word for word.** FY2024 says “in our second fiscal year”. FY2023 and FY2024 both claim “more than 800+ stock donations”, while Schedule M counts 203 and 1,565 (C11).
6. **GVNG.**
   - There is no non-cash income in any year.
   - DonateStock's grants to GVNG are confirmed: $42,631, $113,657, $29,945 and $47,086, which are 2.67%, 6.11% and 1.23% of GVNG's FY2022–24 contributions.
   - But the table column “Grants (IX 1)” holds Part I line 13. Part IX line 1 is $627,900, $641,686, $224,039 and $502,675 (C10).
7. **The bottom line sums two charities, not three.** $11,891,225 + $12,778,129 = $24,669,354 (C08).
8. **The Giving Block contradiction is confirmed, and stronger than stated.**
   - Re-fetched page: “Crypto alone saw an average gift of $11,019 across 22,343 donations”. 22,343 × 11,019 = $246,197,517.
   - “Over $100 million” is a floor, so the 2.46× ratio alone is not decisive.
   - But the same page claims “over $300 million since our founding in 2018” and “66% year-over-year growth”. $246.2m in 2025 plus about $148m in 2024 would already exceed $300m (C13).
9. **The Shift4 claims are confirmed from IR-site PDFs** (robots-allowed; sec.gov not used). They are:
   - “approximately 2,400 charities”;
   - FY2025 volume $209bn (FY2024 $165bn);
   - the volume definitions;
   - an earnout of $10.4m ($2.8m cash, $7.6m equity);
   - “did not have a material impact”;
   - crypto settlement $1.8m, $3.5m and $5.7m;
   - SAB 122.
   The release scan is literally right (0 mentions in 26 releases), but every release is a notice that points to a shareholder letter (C12, N12).
10. **The DPN facts and classification logic are sound.**
    - Line 6 is 0 / false, there is no Schedule D, and `FSAuditedInd` is 0 / false.
    - TY2025: Part IX line 1 $2,178,671; Schedule I 104 lines, $1,324,158.
    - Schedule A: $2,138,755 of $4,140,846 (51.65%) is above the 2% cap of $83,122.
    - DPN's contributions are 0.0044% of corrected FY2024 DAF grants.
    - R1–R4 follow from the filings. R5 (the receipts are DAF grants) rests on DPN's and Chariot's own descriptions, so N01, N02 and N07 now say so.
    - The FY2025 memo-line set mixes DAF wording (DPN, FreeWill) with fiscal-sponsor wording (DonateStock), which C14 and N07 now name.
11. **No data file that feeds market totals carries DPN's EIN 931372175.** It appears only in research CSVs: `dechomai-dafpay-2026-11-19.csv`, the vendor CSV, link health and queue proposals.

## Accept / modify / reject

| Item | Target | Decision | Reason |
|---|---|---|---|
| N01 | `b40n14-b38c-dechomai-dafpay.md` | modify | Figures right; “are grants from DAF sponsors” softened to DPN’s own description (Schedule B redacted) |
| N02 | `queue-batch38-closeout-checks.md` | modify | Same softening of R5 |
| N03 | `queue-batch38-closeout-checks.md` | accept | `FSAuditedInd` 0 (TY2024) and false (TY2025) confirmed |
| N04 | `queue-batch38-closeout-checks.md` | accept | TEOS 05B member read; wave 37B used it |
| N05 | `queue-batch38-closeout-checks.md` | accept | IX 1 $2,178,671; 104 Schedule I lines $1,324,158 confirmed |
| N06 | `queue-fidelity-chariot-goodstack-vanguard.md` | accept | Line 6 “No”, no Schedule D confirmed |
| N07 | `b40n13-03-g1913-03-schema-and-processor-accounts.md` | modify | FreeWill files Schedule D (no Part I) in TY2023–24; DonateStock FY2025 uses fiscal-sponsor, not DAF, wording |
| N08 | `direction-noncash-gift-infrastructure.md` | modify | Figures confirmed; adds the FY2023 XML link (the only link was the FY2024 return) |
| N09 | `direction-noncash-gift-infrastructure.md` | modify | GivingIQ claims “thousands”, not tens of thousands; floors 263 and 588 named |
| N10 | `direction-noncash-gift-infrastructure.md` | modify | “no Schedule D” → “no Schedule D Part I”; 45.7% is of contributions |
| N11 | `direction-noncash-gift-infrastructure.md` | accept | GVNG no non-cash; four grant amounts confirmed |
| N12 | `direction-noncash-gift-infrastructure.md` | modify | Releases are stubs pointing to unread shareholder letters; only the Q3 2026 10-Q was read |
| N13 | `gap19-fy2025-refresh.md` | modify | Keeps the surrounding count (“3 nationals”) consistent by saying why DonateStock is still listed |
| N14 | `noncash-gift-vendors-2026.csv` | modify | 45.7% is of intake, not of grants (45.8% of IX 1, 49.4% of Schedule I) |
| N15 | `noncash-gift-vendors-2026.csv` | accept | All values confirmed; CSV width stays 16 |

## Exact corrections

All values are on one line; `\n` stands for a newline.

### `research/mission-2026-11-14/b40n14-b38c-dechomai-dafpay.md`
- **Find:** "- **Conclusion** [I]: legally, DPN describes itself as a sponsor that takes title. In practice it acts as a pass-through facilitator for Chariot, and its own Part IV answers say it holds no DAFs."
- **Replace with:** "- **Conclusion** [I]: legally, DPN describes itself as a sponsor that takes title. In practice it acts as a pass-through facilitator for Chariot, and its own Part IV answers say it holds no DAFs. For market totals DPN belongs in neither sponsor nor processor totals. It files no Schedule D, so DAFRC’s Schedule D Part I selection rule never admits it, and its $1,199,247 (TY2024) and $2,941,073 (TY2025) of contributions are, on DPN’s own description, grants from DAF sponsors that are already counted in those sponsors’ grants out (Schedule B names are redacted, so this is not confirmed donor by donor). It is reported only as an intermediary memo line (b40n14-03-b38c-03 §3) [b38c-03] [V wave 41A]"

### `research/mission-2026-11-14/queue-batch38-closeout-checks.md`
- **Find:** "  - DPN carries only unclaimed-nonprofit and five named Jewish-giving-platform flows, about $1.2m in TY2024 and $2.9m in TY2025."
- **Replace with:** "  - DPN carries only unclaimed-nonprofit and five named Jewish-giving-platform flows, about $1.2m in TY2024 and $2.9m in TY2025. On DPN’s own description these are DAF grants that it receives and regrants. It answers Part IV line 6 “No” and files no Schedule D, so its flows belong in neither sponsor nor processor totals; adding them would double-count sponsor grants (b40n14-03-b38c-03 §3) [b38c-03] [V wave 41A]"
- **Find:** "  - The only audited slice is DPN (§4)."
- **Replace with:** "  - DPN is the only slice with a public 990 (§4). That 990 is not audited: `FSAuditedInd` is false or 0 in TY2024 and TY2025 (wave 37B) [b38c-03] [V wave 41A]"
- **Find:** "- **DPN TY2025** comes from ProPublica's summary only, since its XML is not yet mirrored."
- **Replace with:** "- **DPN TY2025** was first read from ProPublica’s summary. Its XML is public in IRS TEOS `2026_TEOS_XML_05B` and was read in wave 37B and in b40n14-03-b38c-03; it was still not on the GivingTuesday mirror on 2026-11-20 [b38c-03] [V wave 41A]"
- **Find:** "| Grants paid | — | $831,404 (largest: Chai Lifeline $372,832; Effective Ventures Foundation $155,818) | n/a in summary"
- **Replace with:** "| Grants paid | — | $831,404 (largest: Chai Lifeline $372,832; Effective Ventures Foundation $155,818) | $2,178,671 (TY2025 XML, Part IX line 1; 104 Schedule I lines totalling $1,324,158) [b38c-03] [V wave 41A]"

### `research/mission-2026-11-14/queue-fidelity-chariot-goodstack-vanguard.md`
- **Find:** "That is the same dual role as Chariot (DAFpay Network) and Every.org."
- **Replace with:** "That is the same dual role as Every.org. Chariot’s DAFpay Network is not a comparable DAF sponsor: its mission text says it sponsors DAFs, but it answers Part IV line 6 “No”, files no Schedule D and regrants DAF grants it receives (b40n14-03-b38c-03 §3) [b38c-03] [V wave 41A]"

### `research/mission-2026-11-14/b40n13-03-g1913-03-schema-and-processor-accounts.md`
- **Find:** "4. **Dollars:** keep processors in contribution, grant and asset totals. Flag AOGF's FYE 2026 and BBGF's CY2025 basis changes as breaks in the series (P-G1913-03-03)."
- **Replace with:** "4. **Dollars:** keep processors in contribution, grant and asset totals. Flag AOGF’s FYE 2026 and BBGF’s CY2025 basis changes as breaks in the series (P-G1913-03-03).\n5. **Outside both series:** charities that describe themselves as DAF sponsors or fiscal sponsors but answer Part IV line 6 “No” and file no Schedule D Part I (DAFpay Network TY2024–25, FreeWill Impact Fund TY2021–24, DonateStock Charitable FY2025) report no DAF accounts and add no DAF dollars. FreeWill’s TY2023–24 returns attach a Schedule D, but only its financial-statement reconciliation parts. DPN’s receipts are, on its own description, grants from DAF sponsors, and the other two pass gifts straight through, so they are shown only as an intermediary memo line, never in sponsor or processor totals (b40n14-03-b38c-03 §3) [b38c-03] [V wave 41A]"

### `research/mission-2026-11-14/direction-noncash-gift-infrastructure.md`
- **Find:** "    - FY2023: contributions and grants recorded as 0, probably missing data ([990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542229349300304_public.xml))."
- **Replace with:** "    - FY2023 and FY2024: DAFRC records contributions and grants as 0 (source “IRS 990”), but both returns leave Schedule D Part I lines 2–3 blank. Part VIII reports $5,078,851 (FY2023) and $12,778,129 (FY2024) of contributions, all publicly traded securities, and Part IX line 1 reports $5,334,774 and $10,585,357 of grants, so the zero is a blank coded as 0. In FY2025 (return 202632859349300138, filed 2026-10-12) it answered Part IV line 6 “No”, filed no Schedule D, took in $25,121,004 in 2,630 gifts and paid DonateStock Inc $709,796 (2.83%) ([FY2023 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413209349328306_public.xml); [FY2024 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542229349300304_public.xml); b40n14-03-b38c-03 §2.2) [b38c-03] [V wave 41A]"
- **Find:** "   - Everything else is company claims, or small 990 figures such as FreeWill Impact Fund's $5.68m (CY2023)."
- **Replace with:** "   - Everything else is company claims, or small 990 figures. FreeWill Impact Fund took in $5.68m (CY2023) and $11.89m (CY2024, of which $7.63m was crypto in 648 gifts), and DonateStock Charitable $12.78m (FY2024) and $25.12m (FY2025). In the latest year FreeWill Impact Fund paid at least 263 organisations, against FreeWill’s “over 55,000”, and DonateStock Charitable at least 588, against GivingIQ’s “thousands” (its own return says “over 350 organizations”) (b40n14-03-b38c-03 §2) [b38c-03] [V wave 41A]"
- **Find:** "  - FreeWill Impact Fund's total contributions, all channels: CY2021 $1.19m, CY2022 $2.50m, CY2023 $5.68m ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/861218871.json)) [F]."
- **Replace with:** "  - FreeWill Impact Fund’s total contributions, all non-cash: CY2021 $1.19m, CY2022 $2.50m, CY2023 $5.68m, CY2024 $11.89m. Schedule M for CY2024 shows crypto $7,628,569 in 648 gifts and securities $4,262,656 in 338. $5,430,494 (45.7% of contributions) went in one grant to The Oregon Community Foundation. Part IV line 6 is “No” and no Schedule D Part I is filed (the CY2023–24 returns attach a Schedule D for the financial-statement reconciliation only), although Part III says it “OPERATES A DONOR ADVISED FUND” ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/861218871.json); TY2024 XML 202503189349308315; b40n14-03-b38c-03 §2.1) [b38c-03] [V wave 41A]"
- **Find:** "   - Engiven is GVNG's crypto partner."
- **Replace with:** "   - Engiven is GVNG’s crypto partner, but GVNGorg (EIN 81-2446261) reports no non-cash contributions in TY2021–TY2024. The DonateStock partnership is visible only as DonateStock Charitable’s grants to GVNG: $42,631 (FY2022), $113,657 (FY2023), $29,945 (FY2024) and $47,086 (FY2025) (b40n14-03-b38c-03 §2.3) [b38c-03] [V wave 41A]"
- **Find:** "It does not disclose a figure for The Giving Block alone."
- **Replace with:** "It does not disclose a figure for The Giving Block alone. Its FY2025 10-K and Q3 2026 10-Q fold “stock donations” into total volume ($209bn in FY2025), of which The Giving Block’s self-reported “over $100 million” of 2025 crypto would be about 0.048%. Its 26 results press releases from 2020-Q2 to 2026-Q3 never name The Giving Block, but each is a short notice pointing to a shareholder letter, and the letters were not read (their host’s robots.txt returned 403), so that silence is weak evidence. Giving Block Foundation (EIN 92-3363254, ruled 2024-12) has filed no Form 990 yet (b40n14-03-b38c-03 §2.4) [b38c-03] [V wave 41A]"

### `research/mission-2026-11-14/gap19-fy2025-refresh.md`
- **Find:** "DonateStock, which leaves the value blank"
- **Replace with:** "DonateStock, which answers Part IV line 6 “No” and attaches no Schedule D to its FY2025 return (202632859349300138), so it has no FY2025 DAF value; it is counted here because it was a DAFRC sponsor in FY2022–24, but under DAFRC’s Schedule D selection rule it is not an FY2025 DAF sponsor-year, and its $25,121,004 of contributions are pass-through stock gifts (b40n14-03-b38c-03 §2.2) [b38c-03] [V wave 41A]"

### `data/mission-2026-11-14/noncash-gift-vendors-2026.csv`
- **Find:** "CY2024 return filed, no extract"
- **Replace with:** "CY2024 $11.89m (Schedule M: crypto $7.63m in 648 gifts; securities $4.26m in 338 gifts; 45.7% of intake granted to The Oregon Community Foundation) [b38c-03] [V wave 41A]"
- **Find:** "FY2023 33 DAFs, EOY $0.11m; FY2024 33 DAFs, EOY $2.16m"
- **Replace with:** "FY2023 33 DAFs, EOY $0.11m; FY2024 33 DAFs, EOY $2.16m; FY2023-24 Sch. D lines 2-3 blank (DAFRC codes 0) while Part VIII shows $5.08m and $12.78m; FY2025 no Sch. D and line 6 No, contributions $25.12m in 2,630 gifts, $0.71m paid to DonateStock Inc [b38c-03] [V wave 41A]"

### `research/mission-2026-11-14/b4013-03-02-daf-grant-record-schema.md`
- **Find:** "The schema itself was not validated against the 2020-12 metaschema, because no package could be installed (P-B4013-03-02-04)."
- **Replace with:** "The schema was later checked against the 2020-12 metaschema with the jsonschema 4.26.0 package already present in the environment (Draft202012Validator.check_schema): it passes, and the same package reproduces the expected (instance path, keyword) errors for all 20 negative vectors and accepts the 4 positive ones (P-B4013-03-02-04 can close) [V wave 41A]"
- **Find:** "- **The vector generator is in the scratchpad** (`q1332/make_vectors.py`), which may be cleared. The vector files themselves are self-contained."
- **Replace with:** "- **The vector generator is in the repo** at `standards/daf-grant-record/tools/make_vectors.py`, identical to the scratchpad copy; re-running it rebuilds all 24 vector files byte for byte. The vector files themselves are self-contained [V wave 41A]"
- **Find:** "   - The vector files were written by a one-off generator (scratchpad `q1332/make_vectors.py`). Each vector is self-contained."
- **Replace with:** "   - The vector files were written by a one-off generator, kept in the repo as `standards/daf-grant-record/tools/make_vectors.py`. Each vector is self-contained [V wave 41A]"
- **Find:** "  - Text alone is allowed because both DAF APIs carry only free text. A schema that required a code would reject every converted Endaoment record unless the converter guessed a code."
- **Replace with:** "  - Text alone is allowed because both DAF APIs carry only free text. A schema that required a code would reject every converted Endaoment record unless the converter guessed a code.\n  - Candid states the up-to-5 rule separately for each facet: the Subjects and the Support Strategies pages each say grant details “can have up to 5 codes”. A cap of five codes across all facets is therefore stricter than Candid’s practice; v0.2 should cap codes per facet [V wave 41A]"
- **Find:** "  - Endaoment `shareMyEmail` (default false) together with a `recommender` name maps to `name_only`."
- **Replace with:** "  - Endaoment `shareMyEmail` (default false) together with a `recommender` name maps to `name_only`. This is an inference: the OpenAPI says `shareMyEmail` controls only whether to share “the fund's donor-of-record email”, and describes `recommender` as the “Name of the person recommending the grant” without saying that the name reaches the recipient or that the recommender is the donor of record [V wave 41A]"
- **Find:** "Manual entries cannot be recomputed, only reviewed."
- **Replace with:** "Manual entries cannot be recomputed, only reviewed.\n- **Regex anchors.** The validator and jsonschema 4.26.0 both use Python’s `re.search`, where `$` also matches before a final newline, so an EIN or currency code followed by one trailing newline character passes; an ECMA-262 validator would reject it. Implementations should reject control characters or match the whole string [V wave 41A]"

### `standards/daf-grant-record/schema-v0.1.json`
- **Find:** "Up to 5 PCS codes, following Candid's rule for grant details ('not required; can have up to 5 codes')."
- **Replace with:** "Up to 5 PCS codes in total. Candid's rule for grant details ('not required; can have up to 5 codes') is stated per facet on its Subjects and Support Strategies pages, so this total cap is stricter than Candid's practice [V wave 41A]"

### `research/mission-2026-11-14/b40n14-03-b38c-03-noncash-vendors-dpn.md`
- **Find:** "- The three charities that file show **$24.7m of combined FY2024 intake** (FreeWill Impact Fund $11.9m, DonateStock Charitable $12.8m)"
- **Replace with:** "- The two vendor-affiliated charities with non-cash intake show **$24.7m of combined FY2024 intake** (FreeWill Impact Fund $11.9m, DonateStock Charitable $12.8m; GVNGorg’s $2.4m of cash contributions is not included) [V wave 41A]"
- **Find:** "yet Part IV line 6 is 0 and no Schedule D is filed [F]"
- **Replace with:** "yet Part IV line 6 is 0 and no Schedule D Part I is filed [F]. The TY2023 and TY2024 returns do attach a Schedule D, but only with its financial-statement reconciliation parts (the study’s own CSV flags `sched_d_present` True for both years); TY2024 is also the first year with `FSAuditedInd` 1 [V wave 41A]"
- **Find:** "Non-cash (VIII 1g) | Grants (IX 1)"
- **Replace with:** "Non-cash (VIII 1g) | Grants (Part I line 13; Part IX line 1 is $627,900, $641,686, $224,039 and $502,675) [V wave 41A]"
- **Find:** "word for word, so it is not a yearly count [F]."
- **Replace with:** "almost word for word (FY2024 says “in our second fiscal year”), and the FY2023 and FY2024 versions both claim “more than 800+ stock donations” while Schedule M counts 203 and 1,565, so it is not a yearly count [F] [V wave 41A]"
- **Find:** "- **Earnings releases.** 26 releases (2020-Q2 to 2026-Q3) contain 0 mentions of “Giving Block”, “stock donation” or “crypto” [C]."
- **Replace with:** "- **Earnings releases.** 26 releases (2020-Q2 to 2026-Q3) contain 0 mentions of “Giving Block”, “stock donation” or “crypto” [C]. Each release is only a short notice that the results were posted in a shareholder letter or on the Financials page, and the letters were not read [B], so this zero is weak evidence [V wave 41A]"
- **Find:** "  - Count × average = **$246,197,517**, 2.46× the headline [C]."
- **Replace with:** "  - Count × average = **$246,197,517**, 2.46× the headline [C].\n  - The same page says The Giving Block has processed “over $300 million since our founding in 2018” and reports “66% year-over-year growth from 2024 to 2025”. If 2025 were $246.2m, 2024 would be about $148m and the two years alone would exceed $300m, so the product cannot be the 2025 crypto total. “Over $100 million” is a floor, so the 2.46× ratio by itself is not a contradiction [V wave 41A]"
- **Find:** "of self-described DAF charities with no Schedule D."
- **Replace with:** "of self-described DAF or fiscal-sponsor charities with no Schedule D Part I. [V wave 41A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.54 Open DAF grant record draft; non-cash vendors and DAFpay Network (validated, wave 41A)\n\n**Open DAF grant record draft; non-cash vendors and DAFpay Network** (validated, wave 41A). The draft, unendorsed DAF grant record (JSON Schema 2020-12, 13 fields, 9 required) passes an independent check: jsonschema 4.26.0 accepts it against the 2020-12 metaschema and reproduces the declared result for all 24 test vectors, and the repo generator rebuilds them byte for byte. Chariot’s 25000 cents become “250.00” and Endaoment’s 1000000 USDC micro-units become “1.00”. Candid’s CC BY 4.0 statement and its up-to-5-codes rule are confirmed, but Candid states the rule per facet, so the schema’s cap of five codes in total is stricter; Endaoment’s “name_only” mapping is an inference. The non-cash filings hold: FreeWill Impact Fund took in $11,891,225 in TY2024 ($7,628,569 crypto in 648 gifts) and paid at least 263 organisations, 0.48–1.79% of the 55,000 claimed; DonateStock Charitable took in $25,121,004 in FY2025. FreeWill does attach a Schedule D, without Part I. The Giving Block’s 22,343 × $11,019 = $246.2m also conflicts with its “over $300 million since 2018”, and Shift4’s results releases are stubs, so their silence proves little. DPN stays outside sponsor and processor totals, as a memo line. [V wave 41A]\n\n---\n\n## Source register"

## Uniqueness check

`<scratch>/v41a/build/check.py` (and the parser run on this file) counts each Find in its target file alone and after earlier items are applied in order: 30 of 30 occur exactly once. After C05 the schema is still valid JSON and passes the 2020-12 metaschema; after N14–N15 every row of `noncash-gift-vendors-2026.csv` still has 16 columns.

## Limits

- The Candid PCS pages could not be re-fetched live (Cloudflare 403 with the unchanged user agent); quotes rest on the study's same-day cache.
- Shift4 shareholder letters (cloudfront host, robots 403) and sec.gov were not read; Shift4 claims rest on IR-site PDF text cached by the study.
- Chariot and Endaoment pages were not re-fetched; the 2026-11-19 caches were used (hashes match the vectors).
- Corrections were not applied; other agents may edit the target files before they are.
