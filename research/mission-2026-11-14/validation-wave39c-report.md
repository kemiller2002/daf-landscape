# Validation wave 39C: exception-proxy refinements (g0503-0501)

**Validator:** independent-validation-agent-wave39c · **Date:** 2026-11-19 · **Register:** [`validation-register-wave39c.csv`](../../data/mission-2026-11-14/validation-register-wave39c.csv) (24 claims)

**Study checked:** [g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md), `exception-proxy-refined-2026-11-19.csv`, `fiscal-sponsor-ein-list-2026-11-19.csv`, `scripts/mission_exception_refined.py`.

## Counts

| Result | Claims |
|---|---|
| confirmed | 13 |
| partially_confirmed | 8 |
| contradicted | 3 |
| unverifiable | 0 |
| **Total** | **24** |

## Method

- Re-ran the script to scratch with the cached inputs (np cache, Schedule I lines, BMF 2026-11-09, Pub 78, revocation list, e-file index 2021–2026, filtered NCCS archive files, cached directory page). Repo CSVs were backed up and their md5 checked after the run; they were not modified.
- Re-ran the pipeline up to line level in a scratch probe (imports the script unchanged) to decompose components and run sensitivities.
- Re-fetched the Fiscal Sponsor Directory robots.txt and page with the default client user agent; sent HEAD and tail byte-range requests to the NCCS S3 mirror.
- Checked 15+ host→EIN matches against the 2026-11 BMF, Pub 78 and the revocation list, and 11 classified EINs against 8–16 archive snapshots each.
- No crt.sh, certspotter or sec.gov; no outreach; no user-agent changes.

## Findings

1. **Reproduction is exact** (V39C-01, -02). Both CSVs are byte-identical on re-run, and all 16 `base_*` columns match the governing parent CSV in all 167 rows. Every parent column outside the refined flags is unchanged.
2. **Headlines confirmed** (V39C-04 to -07). Core 7.76% / 11.61% (47,228 lines, $10.77bn); new-organisations-only core 6.80% / 11.00%; broad 24.79% / 19.85%; fiscal sponsors 0.44% / 1.94% (4.4×, from 10.7×).
3. **Directory-only component double-counts the excluded hosts** (V39C-08). The 1,965 lines / $557.1m includes the 113 excluded community-foundation / United Way lines ($25.7m). The amount that counts in the headline is **1,852 lines, $531.4m**. With that, 825 + 1,852 + 2 + 4 − 1 marker overlap = 2,682 lines.
4. **Directory page and matching confirmed** (V39C-09, -10). robots.txt is an empty Disallow; the page returns HTTP 200 at 242,714 bytes and parses to the same 413 hosts. The match-method counts reproduce.
5. **Spot checks** (V39C-11). 12 of 15 checked EINs agree with the BMF and Pub 78 by name and city. SPM Disability Justice Fund → Disability Power Bloc is in Oakland, not San Francisco. Five Schedule I–keyed EINs are in neither the BMF nor Pub 78, and Marcus Foster Education Institute was auto-revoked on 15 November 2022. Foundation for National Progress is now The Center for Investigative Reporting, a large operating newsroom.
6. **The three Q-B15 hosts are in the BMF** (V39C-12, contradicted). Their EINs appear as STONIER SCHOLARSHIP INC, OPENCOLLECTIVE FOUNDATION and MULTIPLIER. They were missed by the name regex, not absent from the BMF. The keyed EINs are right.
7. **CF / United Way exclusion** (V39C-13). The figures are confirmed: 15 EINs, 113 lines, $25.7m. The NTEE rule is imperfect:
   - it excludes The Giving Back Fund (T70; $6.85m) and Streams in the Desert Foundation (T31), both fiscal-sponsor hosts;
   - it keeps Communities Foundation of Oklahoma and DAF sponsors such as United Charitable and Givinga.
   - All of this is immaterial.
8. **Large-programme hosts** (V39C-14). 50CAN, Global Impact, NEO Philanthropy and Myriad USA (the directory and BMF name of King Baudouin Foundation US) are 147 lines and $239.8m, and none of those lines is flagged core on another route. Without them:
   - fiscal sponsors are **0.42% / 1.68% (4.0×)**;
   - the core is **7.74% / 11.35%** and the broad 24.77% / 19.59%;
   - the four-national like-for-like sum is about **3.9%** instead of 4.2%.
   - These hosts account for about 40% of the dollar increase from the directory list.
9. **Archive use confirmed** (V39C-16, -17). HEAD checks match the stated Last-Modified dates and the 403 months. The 2023-08 file ends in a cut record, and the <90%-of-median rule drops only that month. One caveat: the 2023-06 file is dated mid-June, so the “file M reflects M−1” rule is approximate for the earliest months.
10. **Classification spot checks** (V39C-18). Musical Instrument Museum, Life Covenant Church, BM-A Institute, Telescope Fund, New Leaders, Affordable Housing for Artists and Oyate Group (revocations dated 15 May 2021) and Just Trust all match the archive files. Charter Fund's FY2024 lines see a 2019-12 ruling, not 2005-05; the class is unchanged.
11. **Come and See Foundation is not a true new organisation in the script** (V39C-19, contradicted). All 30 lines ($139.9m) are classed `tc_newly_listed_church`. Its BMF foundation code moved from 16 to 10 in 2025. The fourth-largest true new organisation is Deitch Family Charitable Support Trust ($49.7m, 2022-07).
12. **The church class is label-based** (V39C-20). 2,829 of the 3,047 lines ($342.4m) are BMF churches (foundation code 10). The other 218 lines ($13.7m) are religious organisations with other codes.
13. **SVCF / Further Future confirmed** (V39C-21). The ruling is 2023-03 from the 2023-06 snapshot, and the EIN is absent from both 2022 legacy files. The BMF name changes to Navigation Charitable Fund from the 2024-07 snapshot.
14. **NYCT row transcription** (V39C-22, contradicted). The CSV gives 4.97% (not 4.93%) and core $ 9.13% (not 9.09%).
15. **Propagation** (V39C-24). The old figures (10.7×, 1.30%, 3.6%, 0.47%, 7.4% / 11.0%) stand in gap19, strategic-synthesis §0, FINAL-STATUS and g0401-g0502. They are correct on their own definitions but superseded.

## Exact corrections

### `research/mission-2026-11-14/g0503-0501-exception-proxy-refinements.md`

- **Find:** "- Hosts found only in the Fiscal Sponsor Directory: **1,965 lines, $557.1m**."
- **Replace with:** "- Hosts found only in the Fiscal Sponsor Directory: **1,965 lines, $557.1m**, including the 113 excluded lines ($25.7m) below; 1,852 lines and $531.4m count in the headline [V wave 39C]"

- **Find:** "| Directory-only hosts | 1,965 | $557.1m | 0.32% | 0.60% | 1.9× |"
- **Replace with:** "| Directory-only hosts (incl. 113 excluded community-foundation / United Way lines) | 1,965 | $557.1m | 0.32% | 0.60% | 1.9× |\n| … of which counted in the headline | 1,852 | $531.4m | 0.30% | 0.57% | 1.9× [V wave 39C]"

- **Find:** "plus some hosts with large programmes of their own (50CAN, $94.2m)."
- **Replace with:** "plus some hosts with large programmes of their own (50CAN, $94.2m). Without 50CAN, Global Impact, NEO Philanthropy and Myriad USA (the directory and BMF name of King Baudouin Foundation US), 147 lines and $239.8m, the fiscal-sponsor share is 0.42% / 1.68% (4.0×), the core 7.74% / 11.35% and the broad 24.77% / 19.59% [V wave 39C]"

- **Find:** "For these the script takes the **modal EIN that sponsors reported** on Schedule I lines matching the regex, when it covers at least half of them. This gave 276601178, 814004928 and 912166435."
- **Replace with:** "For these the script takes the **modal EIN that sponsors reported** on Schedule I lines matching the regex, when it covers at least half of them. This gave 276601178, 814004928 and 912166435. Correction: all three EINs are in the 2026-11 BMF, under names the regex does not match (STONIER SCHOLARSHIP INC, OPENCOLLECTIVE FOUNDATION, MULTIPLIER); the hosts are missing by name, not by EIN, and the keyed EINs are right [V wave 39C]"

- **Find:** "  - Come and See Foundation, $139.9m (30 lines), 2022-10;"
- **Replace with:** "  - not Come and See Foundation ($139.9m, 30 lines, 2022-10): the script classes it `tc_newly_listed_church` (church/religious label; BMF foundation code 16 at grant time, 10 from the 2025-01 snapshot), so it is outside the true-new-organisation total [V wave 39C]"

- **Find:** "  - Our American Future Foundation, $118.8m (19), 2022-11."
- **Replace with:** "  - Our American Future Foundation, $118.8m (19), 2022-11;\n  - Deitch Family Charitable Support Trust, $49.7m, 2022-07 [V wave 39C]"

- **Find:** "(ruling 2023-03, present in the 2023-06 BMF with that month)."
- **Replace with:** "(ruling 2023-03, present in the 2023-06 BMF with that month, absent from both 2022 legacy files, and renamed Navigation Charitable Fund in the BMF from the 2024-07 snapshot) [V wave 39C]"

- **Find:** "    - Charter Fund: 2005-05 / 2025-08, $76.8m;"
- **Replace with:** "    - Charter Fund: 2005-05 / 2025-08, $76.8m (its FY2024 lines see 2019-12 in the 2024-07 and 2025-01 snapshots, still before the cutoff) [V wave 39C]"

- **Find:** "| 24 | New York Community Trust | 1.76% | 4.93% | 5.95% → 9.09% |"
- **Replace with:** "| 24 | New York Community Trust | 1.76% | 4.97% | 5.95% → 9.13% [V wave 39C]"

- **Find:** "0.15% non-501(c)(3) IRC text [C]."
- **Replace with:** "0.15% non-501(c)(3) IRC text [C]. Without 50CAN, Global Impact, NEO Philanthropy and Myriad USA the fiscal-sponsor term is 1.82% and the sum ≈3.9% [V wave 39C]"

- **Find:** "The big-4 fiscal-sponsor count share is 0.24%, against 0.04% before [C]."
- **Replace with:** "The big-4 fiscal-sponsor count share is 0.24%, against 0.04% before [C]. Foreign + fiscal-sponsor lines are 0.67% of big-4 lines (0.47% before) [V wave 39C]"

- **Find:** "  - The directory-only $557.1m is therefore an upper bound (P-G0503-01)."
- **Replace with:** "  - The directory-only $557.1m (of which $531.4m counts in the headline) is therefore an upper bound (P-G0503-01); 50CAN, Global Impact, NEO Philanthropy and Myriad USA alone are $239.8m [V wave 39C]"

- **Find:** "  - The community-foundation / United Way exclusion is a judgement. Including those hosts changes the share by +0.02 pp lines and +0.03 pp dollars."
- **Replace with:** "  - The community-foundation / United Way exclusion is a judgement. Including those hosts changes the share by +0.02 pp lines and +0.03 pp dollars. The NTEE rule also excludes The Giving Back Fund (T70; 31 lines, $6.85m) and Streams in the Desert Foundation (T31; $5k), which are fiscal-sponsor hosts, and keeps Communities Foundation of Oklahoma (T30J; $3.58m) and DAF sponsors such as United Charitable and Givinga; all immaterial [V wave 39C]"

- **Find:** "- **Churches:** the 3,047 newly listed church lines ($356.1m) stay in the time-correct flag."
- **Replace with:** "- **Churches:** the 3,047 newly listed church lines ($356.1m) stay in the time-correct flag. The class is label-based: 2,829 of the lines ($342.4m) carry BMF foundation code 10 (church) in the 2026-11 BMF; 218 lines ($13.7m) are religious organisations with other codes, such as yeshivas and church-planting networks, for which a first ruling month can date them [V wave 39C]"

- **Find:** "- The `sponsor_any_*` distributions use the refined broad union."
- **Replace with:** "- The `sponsor_any_*` distributions use the refined broad union.<br>- `avg_usd_flagged_line`, `avg_usd_other_line` and `fiscal_sponsor_any_share_of_sched_i_usd` also follow the refined flags [V wave 39C]"

### `research/mission-2026-11-14/gap19-exception-load-proxy.md`

- **Find:** "- Fiscal-sponsor names: 0.12% of lines vs 1.30% of dollars (**10.7×**)."
- **Replace with:** "- Fiscal-sponsor names: 0.12% of lines vs 1.30% of dollars (**10.7×**); on the EIN-keyed host list (19 Q-B15 hosts plus the Fiscal Sponsor Directory; $92.72bn base) 0.44% vs 1.94% (4.4×), or 0.42% vs 1.68% (4.0×) without 50CAN, Global Impact, NEO Philanthropy and Myriad USA ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 39C]"

- **Find:** "1.96% + 1.50% + 0.15% ≈ **3.6% of dollars**."
- **Replace with:** "1.96% + 1.50% + 0.15% ≈ **3.6% of dollars** (≈4.2% with the EIN-keyed fiscal-sponsor list at 2.10%; ≈3.9% without four directory hosts with large programmes of their own) [V wave 39C]"

- **Find:** "foreign + fiscal-sponsor lines are **0.47%** of big-4 lines."
- **Replace with:** "foreign + fiscal-sponsor lines are **0.47%** of big-4 lines (0.67% with the EIN-keyed fiscal-sponsor list) [V wave 39C]"

- **Find:** "is **about 7% of recipient lines and 10–11% of dollars** on the core definition. The broad definition gives 20–25%."
- **Replace with:** "is **about 7% of recipient lines and 10–11% of dollars** on the core definition. The broad definition gives 20–25%. With the EIN-keyed fiscal-sponsor list and time-correct rulings the core is 7.76% / 11.61% (6.80% / 11.00% counting only true new organisations as recent) and the broad 24.79% / 19.85% ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 39C]"

- **Find:** "| Fiscal-sponsor name | 740 | $1.21bn | 0.12% | 1.30% | +1.18 | 10.72× |"
- **Replace with:** "| Fiscal-sponsor name | 740 | $1.21bn | 0.12% | 1.30% | +1.18 | 10.72× (EIN-keyed list on $92.72bn: 2,682 lines, $1.80bn, 0.44% / 1.94%, 4.4×) [V wave 39C]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "  - The like-for-like non-standard share is about 3.6% of the four largest nationals' FY2023–24 dollars."
- **Replace with:** "  - The like-for-like non-standard share is about 3.6% of the four largest nationals' FY2023–24 dollars; about 4.2% with the EIN-keyed fiscal-sponsor list (3.9% without 50CAN, Global Impact, NEO Philanthropy and Myriad USA) ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 39C]"

- **Find:** "That proxy measures recipients, not review ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md); wave 32A)."
- **Replace with:** "With the EIN-keyed fiscal-sponsor list and time-correct rulings the core is 7.76% / 11.61% (6.80% / 11.00% counting only true new organisations as recent) and the broad 24.79% / 19.85% ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)). That proxy measures recipients, not review ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md); wave 32A). [V wave 39C]"

- **Find:** "The review-need proxy (11.0% of top-50 dollars; 10.96% corrected)"
- **Replace with:** "The review-need proxy (11.0% of top-50 dollars; 10.96% corrected; 11.61% with the EIN-keyed fiscal-sponsor list and time-correct rulings) [V wave 39C]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "- **Exception-load proxy.** Across the top 50 sponsors, 7.4% of recipient lines and 11.0% of dollars need non-routine review."
- **Replace with:** "- **Exception-load proxy.** Across the top 50 sponsors, 7.4% of recipient lines and 11.0% of dollars need non-routine review. With the EIN-keyed fiscal-sponsor list and time-correct rulings it is 7.76% / 11.61% (6.80% / 11.00% counting only true new organisations as recent), or 7.74% / 11.35% if four hosts with large programmes of their own are not counted as fiscal sponsors [V wave 39C]"

### `research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md`

- **Find:** "name-rule fiscal-sponsor matching"
- **Replace with:** "name-rule fiscal-sponsor matching (replaced by an EIN-keyed host list in [g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md), which moves the core to 7.76% / 11.61%) [V wave 39C]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.50 Exception proxy refinements (validated, wave 39C)\n\n**Exception proxy refinements** (validated, wave 39C). An independent re-run reproduces both CSVs byte for byte. Keying fiscal sponsors by EIN (the 19 Q-B15 hosts plus 413 Fiscal Sponsor Directory hosts; 347 EINs) and dating rulings with archived monthly IRS BMF files (NCCS mirror, 2023-06 to 2026-07, truncated 2023-08 dropped) moves the top-50 core review-need proxy from 7.41% / 10.96% to 7.76% / 11.61% of lines / dollars, or 6.80% / 11.00% counting only true new organisations as recent. The broad proxy is 24.79% / 19.85%. Fiscal sponsors rise from 0.12% / 1.31% to 0.44% / 1.94% (4.4×, not 10.7×). Four directory hosts with large programmes of their own (50CAN, Global Impact, NEO Philanthropy, Myriad USA) carry $239.8m; without them fiscal sponsors are 0.42% / 1.68% and the core 7.74% / 11.35%. The four-national like-for-like share rises from about 3.6% to 4.2% of dollars (3.9% without those hosts). Come and See Foundation ($139.9m) is classed a newly listed church, not a new organisation. The proxy measures recipients, not observed review (repo [`validation-wave39c-report.md`](mission-2026-11-14/validation-wave39c-report.md)) [V wave 39C]\n\n---\n\n## Source register"

## Not changed

- The governing parent figures (7.41% / 10.96%, 25.08% / 19.72%) remain correct on their own definitions. The corrections add the refined values next to them rather than replacing them.
- The report's wave-32A paragraph (“reproduces at 3.6%”) is left as is. The new §11.50 carries the refined figure.
