# Validation wave 41B: filing-break screen, realised tail fees and the coverage gap

**Date:** 2026-11-20 · **Validator:** independent-validation-agent-wave41b · **Register:** [`validation-register-wave41b.csv`](../../data/mission-2026-11-14/validation-register-wave41b.csv) (V41B-01 to V41B-32)

**Studies checked**
1. [`b4427b-b4501-npt-screen-and-realised-fees.md`](b4427b-b4501-npt-screen-and-realised-fees.md): NPT-pattern screen of the DAFRC panel and realised admin-fee rates in the long tail (`scripts/mission_npt_screen_fees.py`, tasks `screen` and `fees`).
2. [`b40n120201-01-coverage-gap-decomposition.md`](b40n120201-01-coverage-gap-decomposition.md): decomposition of the 15.1-point coverage gap and a bounded replacement for the 1/0.849 scaling (`scripts/mission_coverage_gap.py`).

**Method**
- Both scripts were re-run from cache into scratch (`v41b/`) and the outputs compared byte for byte with the repo CSVs.
- 30 Form 990 XMLs were re-fetched from the GivingTuesday mirror of IRS TEOS. Its robots.txt returned 404 at 2026-11-20, so no restriction applies.
- The Licking County Foundation audit was re-fetched after checking its robots.txt, which returned 200 with "User-agent: * Allow: /".
- User agent `research-script/1.0` throughout, unchanged. No logins, forms or outreach. crt.sh, certspotter and sec.gov were not used.
- No repo file other than the two outputs of this wave was written. Nothing was committed.

## 1. Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| 1. NPT screen and realised fees | 17 (V41B-01 to 17) | 14 | 3 | 0 | 0 |
| 2. Coverage gap decomposition | 15 (V41B-18 to 32) | 10 | 5 | 0 | 0 |
| **Total** | **32** | **24** | **8** | **0** | **0** |

## 2. Findings: study 1 (NPT screen and realised fees)

**Reproduction**
- `screen` and `fees` both reproduce their CSVs byte for byte from the q4501 cache (V41B-01, V41B-09).
- The Licking audit quote check reports "verified" for 2024 and 2023.

**Screen counts are right (V41B-02).** The CSV and the report agree on every count:
- 4,633 of 5,963 sponsor-years are tested, holding $849.94bn of filed line 4.
- 101 sponsor-years have a ratio break, 44 show the NPT pattern and 2 are above $250m.
- 29 fail the roll-forward, 9 are consistent with it and 6 are untestable; 24 are spikes and 20 dips.
- The 27 sub-threshold failures net to +$29.2m.
- The one-sided supplement flags nothing above $250m.

**Dechomai Asset Trust FY2021 (V41B-03 to 05)**
- The re-read of XML 202243199349331259 confirms line 4 ($267,690,026) against Part X net assets ($1,148,070,667).
- It confirms the flows: Schedule D contributions $985,904,717 equal Part VIII, Schedule D grants $374,029,609 equal Part IX, and column (b) is zero.
- No other numeric field equals $267,690,026, and no combination of Part X lines comes close.
- The rolls recompute exactly: forward $935.18m, backward $1,148.21m, filed minus the midpoint −$774.00m.
- *Challenge.* The Trust describes itself as a Type I supporting organisation that liquidates non-cash gifts to DAFs "benefiting Dechomai Foundation, Inc.". It paid $365.2m in cash to the Foundation, which DAFRC also lists as a sponsor. The +$774m sensitivity could therefore partly double-count with the Foundation's DAF book, and the study should say so.
- *Minor.* The script docstring says the "fails" verdict needs the two rolls to agree within 10%. The code does not require this, which is why Dechomai is "fails" with `rolls_agree` = 0.

**NPT FY2023 (V41B-06).**
- The three re-fetched NPT returns reproduce both rolls: $28,216.2m / $28,120.1m, and $28,191.8m / $28,156.1m by net-asset change.
- NPT's consolidated net assets ($28,514.3m) are 1.2% above the roll midpoint.

**Market sensitivity (V41B-07).**
- The corrected-totals CSV gives $234.79bn (FY2021) and $261.69bn (FY2023).
- Growth recomputes as 38.7% → 39.1%, −2.5% → −2.8%, 12.4% → 14.7% and 26.1% → 23.5%.
- The repo still carries only the Part X-basis FY2023 sensitivity ($261.44bn, 23.6%), and no FY2021 sensitivity.

**Fee figures (V41B-10 to 14)**
- All 7 internal-fee CFs checked match their XMLs or audit to the dollar: Licking, Hutchinson, Decatur, Clinton, Four Way, Monroe and Greene.
  - Hutchinson FY2024 (202523189349310207): "ADMINISTRATIVE FEES RECEIVED FROM NONOPERATING FUNDS 935,785".
  - Decatur FY2021 (202242369349301514): Part XI 354,818, equal to Part V line 1f 354,818.
  - Licking audit: $1,058,361 and $957,643.
- *Greene County.* 21% of its "internal" fee ($68,310) is an EITC grant fee passed straight through, with a matching expense. Without it the rate is 97.6 bps, not 124.2 bps, and the non-publisher median is 101.6 bps rather than 104.5.
- *Licking.* Note 1N of its own posted audit publishes its fee schedule: $250 minimum, graduated from 1% down to 0.1%. So one of the 7 "non-publishers" in fact publishes.

**"Non-publishers charge like publishers" (V41B-16): partially confirmed.**
- *Supported.* Non-publishing tail CFs charge: 7 of 25 disclose internal fees, at about 70–130 bps of total assets.
- *Not supported.* The comparison with publishers rests on one publisher (Hutchinson) on an all-fund basis. The two lowest rates are also the two largest CFs: Licking ($145m of assets, 70 bps) and Hutchinson ($103m, 83 bps). Every CF under $32m realises 102–129 bps, so size explains the gap as well as publication status does.
- The $62.9m figure uses 103.05 bps, the median of all 8 internal-fee CFs including Hutchinson. It applies all-fund rates to DAF assets, so it is a floor-type figure, not a test of the $89.9m CFs-only central.

**Propagation (V41B-17).**
- Four files say the data "do not bound the pool away from zero". For CFs that is now wrong, and those passages should cite the realised-rate evidence.
- The step from the CFs-only pool to the whole tail (non-CFs, $3.08bn) remains untested.

## 3. Findings: study 2 (coverage gap decomposition)

**Reproduction and identity (V41B-18, 19).**
- The cache-only rerun is byte-identical (md5 `6f8e65afae8e419d9fd7aeec71d5f338`) and took about 6 minutes.
- The identity holds row by row (0 mismatches over 2,705 rows) and in total. Σ Dc of $66,442.1m equals the corrected market; less R5 central ($8,031.0m) it equals netted grants of $58,411.06m.
- The FY2024 gap is $8,808.7m (15.08 points) and the unreconciled remainder is $0.

**Components (V41B-20).**
- Every A and B term recomputes from the CSV's raw columns.
- The sub-$5,000 term splits into 89 partial itemisers ($0.81bn) and full itemisers ($1.97bn). 29 sponsor-years are negative (−$54.4m), and itemised lines under $5,000 total $6.75m.

**XML spot-checks (V41B-21 to 23).** Five FY2024 returns match the cache and the CSV exactly for line 1, line 3 and the Schedule I totals, and none has a Schedule I line under $5,000:

| Sponsor | Line 1 | Line 3 | Schedule I |
|---|---|---|---|
| Blackbaud Giving Fund | $541.6m | $10.96m | $41.4m (1,860 rows) |
| NPT | $5,152.6m | $410.6m | $5,143.0m |
| Morgan Stanley GIFT | $1,632.4m | $16.65m | $1,224.6m |
| Omaha CF | $116.0m | $0 | $0.35m (8 rows) |
| DAFgiving360 | $6,564.6m | $59.4m | $6,367.7m |

- Blackbaud itemised $442.8m in FY2023, so its FY2024 shortfall is a filing change. That supports treating it pro rata.
- Morgan Stanley GIFT leaves 25% of line 1 ($408m) unitemised but passes the 50% rule, so it is treated as "small gifts".

**DAF-to-DAF residual (V41B-25, 32): partially confirmed.**
- The $1.42bn is the gap between whole-line drops in the numerator ($9,447.5m) and R5 central netting ($8,031.0m).
- R5 central weights each line by the recipient's DAF share of assets; the upper tier (weight 1) nets $9,420.8m. The residual is therefore mostly a tier choice: about $0.03bn against the upper tier.
- Leaving it unallocated is consistent with the frame, and it does not move recipient shares. It does move the "15.1 points" and the "5.4 points can never reach a frame recipient".

**Re-weighting (V41B-30).**
- UCLA, Stanford and CFSEM move as stated, and 63 sponsor-years leave a cap residual.
- "Zeroes 129 default-weight sponsor-years" overstates: 129 is the count of default-weight rows. Only 122 itemising FY2024 sponsor-years have zero corrected DAF grants, 99 of them with w = 1.

**Headline and tightened range (V41B-27, 28): partially confirmed on the range.**
- The central figures are right: 9.16% (8.30–10.15) and 13.71% (12.26–15.22). The grid gives 9.13–9.21 and 13.67–13.79.
- The grid varies only the allocation keys, whose frame shares are all 0.68–0.69, so a narrow range is built in. Wave 40B's 8.4–9.9% spanned whether the gap reaches recipients at all, so "the range tightens" compares unlike ranges.
- An assumption envelope from the CSV's own rows runs from dropping the sub-$5,000 component (about 8.8% / 13.2%, additive) to allocating the DAF-to-DAF residual (9.39% / 14.05%). That is about 8.8–9.4% on 1h and 13.2–14.1% on 1h − 1d − 1e.
- Recommendation: keep the central 9.2% / 13.7% as the replacement for 9.9% / 14.8%, but report it with the assumption envelope. A key-choice range of 0.1 point is not the uncertainty.

**Propagation (V41B-29).** Seven passages still give 9.9% / 14.8% (÷ 0.849) as the upper or scaled figure. The corrections below add the bounded figures and keep the floors.

## Exact corrections

All values are on one line; `\n` stands for a newline.

### `research/mission-2026-11-14/b4427b-b4501-npt-screen-and-realised-fees.md`
- **Find:** "No first-party Dechomai statements were read (P-B4427B4501-01)."
- **Replace with:** "No first-party Dechomai statements were read (P-B4427B4501-01).\n- **Overlap caveat [I].** The return describes the Trust as a Type I supporting organisation that liquidates non-cash gifts to DAFs “benefiting Dechomai Foundation, Inc.” (EIN 06-1676688). Its Schedule I shows a single $365,169,132 cash grant to the Foundation, which DAFRC also lists as a sponsor ($163.5m of FY2021 DAF assets). Whether the two entities' DAF books overlap is untested, so the +$774.0m sensitivity may partly double-count [V wave 41B]"
- **Find:** "   - Every one of the 8 sampled CFs whose filings disclose internal fees charges a realised **70–129 bps of total assets a year**, with one exception: Central Florida, whose disclosed item is partial."
- **Replace with:** "   - Every one of the 8 sampled CFs whose filings disclose internal fees charges a realised **70–129 bps of total assets a year**, with one exception: Central Florida, whose disclosed item is partial. Greene County's 124.2 bps includes $68,310 of EITC grant fees passed straight through (each matched by an equal expense). Its own-fund fee is $250,766, or 97.6 bps, and the non-publisher median becomes 101.6 bps. Licking County's posted audit (note 1N) states its schedule ($250 minimum, graduated from 1% down to 0.1%), so it is not strictly a non-publisher [V wave 41B]"
- **Find:** "is supported in kind: tail CFs that do not publish do charge, at rates similar to those that do."
- **Replace with:** "is supported in kind: tail CFs that do not publish do charge. The comparison with publishers rests on one publisher (Hutchinson) on an all-fund basis, and rates fall with size. The two largest internal-fee CFs, Licking ($145m of average total assets) and Hutchinson ($103m), realise 70 and 83 bps; every CF under $32m realises 102–129 bps. Size explains the gap as well as publication status does, so “at rates similar to those that do” is not established [V wave 41B]"

### `research/mission-2026-11-14/b4501-04-tail-fee-pool-revision.md`
- **Find:** "If only CFs charge, the central figure is about $90m. The earlier $92m applied the top-100 CF median (100 bps). The range rests on 6 CF schedules (7 with Cal Poly Pomona) from a 60-sponsor sample in which 11.7% publish a rate, and one publisher charges no admin fee, so the data do not bound the pool away from zero ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04]"
- **Replace with:** "If only CFs charge, the central figure is about $90m. The earlier $92m applied the top-100 CF median (100 bps). The range rests on 6 CF schedules (7 with Cal Poly Pomona) from a 60-sponsor sample in which 11.7% publish a rate, and one publisher charges no admin fee ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04]. Non-publishing tail CFs do charge: 7 of 25 sampled disclose internal fees at a realised 70–129 bps of total assets (FY2022–24). Those all-fund rates applied to tail CF DAF assets give about $63m ($10.7m–$79.0m), a floor-type figure that bounds the CF pool away from zero. The non-CF part ($3.08bn) is untested (b4427b-b4501 §3) [V wave 41B]"
- **Find:** "or about $90m if only CFs charge. That rests on 6–7 published schedules: only 11.7% of 60 sampled tail sponsors publish a rate (wave 30; [b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04]"
- **Replace with:** "or about $90m if only CFs charge. That rests on 6–7 published schedules: only 11.7% of 60 sampled tail sponsors publish a rate (wave 30; [b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04]. Realised internal fees at 8 tail CFs (70–129 bps of total assets, FY2022–24) give about $63m on tail CF DAF assets as a floor-type figure; the whole-tail $138m still rests on untested non-CF charging (b4427b-b4501 §3) [V wave 41B]"

### `research/mission-2026-11-14/direction-long-tail-sponsors.md`
- **Find:** "and one publisher charges no admin fee, so the data do not bound the pool away from zero ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04] [V wave 35A]"
- **Replace with:** "and one publisher charges no admin fee ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04] [V wave 35A]. Non-publishing tail CFs do charge: 7 of 25 sampled disclose internal fees at a realised 70–129 bps of total assets. On tail CF DAF assets those all-fund rates give about $63m ($10.7m–$79.0m), a floor-type figure, so the CF pool is bounded away from zero. Non-CF charging stays unevidenced (b4427b-b4501 §3) [V wave 41B]"

### `research/mission-2026-11-14/strategic-synthesis.md`
- **Find:** "It replaces wave 30's $92m at the top-100 CF median of 100 bps ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04] [V wave 35A]"
- **Replace with:** "It replaces wave 30's $92m at the top-100 CF median of 100 bps ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04] [V wave 35A]. Non-publishing tail CFs do charge (7 of 25 sampled disclose internal fees at 70–129 bps of total assets), giving a floor-type CF pool of about $63m. The CF pool is therefore about $63m–$90m, and the whole-tail $138m still depends on untested non-CF charging (b4427b-b4501 §3) [V wave 41B]"
- **Find:** "a floor that replaces the scaled ≈10% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B]"
- **Replace with:** "a floor that replaces the scaled ≈10% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B]. Allocating the unitemised gap component by component (foreign grants and the DAF-to-DAF residual to no recipient) gives 9.2% on 1h and 13.7% on 1h − 1d − 1e. That is the central case; the assumption envelope is about 8.8–9.4% and 13.2–14.1%, and the sampling CI 8.3–10.2% and 12.3–15.2% ([b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md)) [V wave 41B]"

### `research/mission-2026-11-14/FINAL-STATUS.md`
- **Find:** "- **Tail admin-fee pool.** CFs-only central estimate is about $90m. The whole-tail figure of about $138m is an upper bracket, with a range of $76m–$184m, replacing the $92m hypothetical."
- **Replace with:** "- **Tail admin-fee pool.** CFs-only central estimate is about $90m. The whole-tail figure of about $138m is an upper bracket, with a range of $76m–$184m, replacing the $92m hypothetical. Non-publishing tail CFs do charge (7 of 25 sampled disclose internal fees at 70–129 bps of total assets), giving a floor-type CF pool of about $63m; non-CF charging is untested [V wave 41B]"
- **Find:** "and a sensitivity variant shows FY2023 market assets of $261.44bn."
- **Replace with:** "and a sensitivity variant shows FY2023 market assets of $261.44bn ($261.69bn at the DAF roll-forward midpoint; FY2023→24 growth 23.5% rather than 26.1%). A screen of all 4,633 testable sponsor-years FY2021–24 finds one other filed break above $250m: Dechomai Asset Trust FY2021 ($267.7m filed against $1,148.1m of net assets). Its roll-forward midpoint would add $774.0m, giving an FY2021 market of $234.79bn rather than $234.01bn. Its overlap with Dechomai Foundation is untested, and the headline keeps filed values (b4427b-b4501 §2) [V wave 41B]"
- **Find:** "- **Non-top-50 numerator.** Measured directly, the all-sponsor DAF share of recipient contributions is 8.4–9.9% on line 1h and 12.6–14.8% on 1h−1d−1e."
- **Replace with:** "- **Non-top-50 numerator.** Measured directly, the all-sponsor DAF share of recipient contributions is 8.4–9.9% on line 1h and 12.6–14.8% on 1h−1d−1e. Allocating the coverage gap by component replaces the ÷ 0.849 upper figures with a central 9.2% and 13.7%. The assumption envelope is about 8.8–9.4% and 13.2–14.1%, and the sampling CI 8.3–10.2% and 12.3–15.2%. The 8.4% and 12.6% floors stand as measured-only figures (b40n120201-01) [V wave 41B]"
- **Find:** "(floors; the scaled 15.4% is superseded) [V wave 40B]"
- **Replace with:** "(floors; the scaled 15.4% is superseded) [V wave 40B]. With the coverage gap allocated by component, the committed-frame central figure is 13.7% (assumption envelope about 13.2–14.1%; CI 12.3–15.2%) [V wave 41B]"

### `research/mission-2026-11-14/b44n27-b39n4-dafrc-data-quality.md`
- **Find:** "Carry a flagged sensitivity instead: FY2023 market $261.44bn rather than $256.37bn, and FY2023→24 growth 23.6% rather than 26.1%."
- **Replace with:** "Carry a flagged sensitivity instead: FY2023 market $261.44bn rather than $256.37bn, and FY2023→24 growth 23.6% rather than 26.1%. At the DAF roll-forward midpoint of b4427b-b4501 the figures are $261.69bn and 23.5%. That screen also flags Dechomai Asset Trust FY2021 (+$774.0m; FY2021 $234.79bn rather than $234.01bn) as the only other filed break above $250m [V wave 41B]"

### `research/mission-2026-11-14/b40n120201-01-coverage-gap-decomposition.md`
- **Find:** "- **The range tightens [F/I].** Wave 40B gave 8.4–9.9% on 1h and 12.6–14.8% on 1h − 1d − 1e. The bounded allocation narrows that to **9.1–9.2%** and **13.7–13.8%** (point ranges over allocation choices)."
- **Replace with:** "- **The range tightens [F/I].** Wave 40B gave 8.4–9.9% on 1h and 12.6–14.8% on 1h − 1d − 1e. The bounded allocation narrows that to **9.1–9.2%** and **13.7–13.8%** (point ranges over allocation choices). That grid varies only the keys, whose frame shares are all 0.68–0.69. The assumption envelope, from dropping the sub-$5,000 component (about 8.8% / 13.2%) to allocating the DAF-to-DAF residual (9.39% / 14.05%), is about 8.8–9.4% and 13.2–14.1%. That envelope, not 0.1 point, is the comparison with wave 40B's range [V wave 41B]"
- **Find:** "  - It zeroes 129 FY2024 default-weight sponsor-years that DAFRC records with no DAF grants, such as Campanile Foundation and Give2Asia."
- **Replace with:** "  - It zeroes FY2024 sponsor-years that DAFRC records with no DAF grants, such as Campanile Foundation and Give2Asia. 129 sponsor-years carry the default weight; 122 itemising sponsor-years have zero corrected DAF grants, 99 of them at w = 1 [V wave 41B]"
- **Find:** "The $1.42bn difference is money that went to other panel sponsors and is not netted, for example grants into sponsors' non-DAF funds."
- **Replace with:** "The $1.42bn difference is money that went to other panel sponsors and is not netted, for example grants into sponsors' non-DAF funds. R5 central weights each line by the recipient's DAF share of assets, while the numerator drops whole lines. Against the upper tier (weight 1, $9.42bn) the residual is about $0.03bn, so the 2.4 points is a netting-tier choice. It does not affect recipient shares, because it is never allocated [V wave 41B]"

### `research/mission-2026-11-14/b40n12-daf-share-of-recipient-revenue.md`
- **Find:** "and dividing the first by all-sponsor coverage (0.849) gives 9.9% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B]"
- **Replace with:** "and dividing the first by all-sponsor coverage (0.849) gives 9.9% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B]. Allocating the gap by component instead (foreign grants and the DAF-to-DAF residual to no recipient) gives 9.2% (assumption envelope about 8.8–9.4%; CI 8.3–10.2%) on 1h and 13.7% on 1h − 1d − 1e ([b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md)) [V wave 41B]"
- **Find:** "the independent figure (≈10–15% pooled) brackets Chariot's 12.6%."
- **Replace with:** "the independent figure (≈10–15% pooled) brackets Chariot's 12.6%. With every itemising sponsor measured and the gap allocated by component, the figures are 9.2% (1h) and 13.7% (1h − 1d − 1e), which still bracket 12.6% (b40n120201-01) [V wave 41B]"

### `research/mission-2026-11-14/b40n1202-b43n26-recipient-basis-and-rating-eligibility.md`
- **Find:** "scaled by all-sponsor coverage the same-recipient figure is 14.8% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B]"
- **Replace with:** "scaled by all-sponsor coverage the same-recipient figure is 14.8% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B]. With the gap allocated by component instead, it is 13.7% (assumption envelope about 13.2–14.1%; CI 12.3–15.2%), and ≥$100m is 7.4% ([b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md)) [V wave 41B]"

### `research/mission-2026-11-14/b40n1202-01-non-top50-numerator.md`
- **Find:** "Leaving the 15.1% unitemised gap unassigned takes 1h to 8.4% (−1.5 points), so the direct figures are floors."
- **Replace with:** "Leaving the 15.1% unitemised gap unassigned takes 1h to 8.4% (−1.5 points), so the direct figures are floors. Allocating the gap by component (foreign grants and the DAF-to-DAF residual to no recipient) gives 9.2% on 1h and 13.7% on 1h − 1d − 1e. The assumption envelope is about 8.8–9.4% and 13.2–14.1% (b40n120201-01) [V wave 41B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.55 Filing-break screen, realised tail fees and the coverage gap (validated, wave 41B)\n\n**Filing-break screen, realised tail fees and the coverage gap** (validated, wave 41B). A screen of 4,633 testable DAFRC sponsor-years FY2021–24 finds 44 whose Schedule D DAF value breaks from the sponsor's own net-asset ratio while flows stay consistent. Only two exceed $250m. NPT FY2023 is understated by about $5.3bn. Dechomai Asset Trust FY2021 files $267.7m against $1,148.1m of net assets; its overlap with Dechomai Foundation is untested. As a sensitivity, the roll-forward midpoints give $234.79bn for FY2021 and $261.69bn for FY2023; the headline keeps filed values. Non-publishing tail community foundations do charge. Seven of 25 sampled disclose internal fees at a realised 70–129 bps of total assets, which implies a floor-type CF fee pool of about $63m. The comparison with publishers rests on one publisher and is confounded by size. Allocating the FY2024 coverage gap by component (foreign grants 3.0 points and DAF-to-DAF 2.4 points to no recipient) gives a recipient DAF share of 9.2% on line 1h and 13.7% on 1h − 1d − 1e, replacing 9.9% and 14.8%. The assumption envelope is about 8.8–9.4% and 13.2–14.1% [V wave 41B]\n\n---\n\n## Source register"
