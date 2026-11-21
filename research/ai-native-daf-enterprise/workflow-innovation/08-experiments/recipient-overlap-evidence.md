# Recipient overlap across the top-50 DAF sponsors: evidence for a shared verification network

**Status:** experiment result. **Retrieved and computed:** 2026-11-20.
**Question:** would a charity-verification record shared across DAF sponsors be reused? If so, how much?
**Script:** [`scripts/workflow_innovation_recipient_overlap.py`](../../../../scripts/workflow_innovation_recipient_overlap.py) (stdlib Python). Rerun with `--xml-dir DIR --fetch`.
**Outputs:** [`data/workflow-innovation/sponsor-recipient-edges-fy2023.csv`](../../../../data/workflow-innovation/sponsor-recipient-edges-fy2023.csv) holds 274,929 sponsor × recipient edges (11.7 MB, uncompressed). [`data/workflow-innovation/recipient-overlap-summary.csv`](../../../../data/workflow-innovation/recipient-overlap-summary.csv) holds every metric below, with a `definition` column.

## Answer

The overlap exists and it is large. These figures cover the 48 top-50 sponsors that itemise grants in their e-file XML, for one fiscal year:

- **71.3% of grant lines and 77.2% of grant dollars went to a charity that at least one other top-50 sponsor also granted to that year.** Lines to charities funded by six or more sponsors were 25.0% of lines and 51.9% of dollars.
- The overlap is concentrated in a small set of charities. Only 40.1% of the 133,763 distinct recipients had two or more top-50 funders, but those recipients received 71.3% of the lines. Most charities (59.9%) were funded by only one top-50 sponsor; they received 28.7% of lines and 22.8% of dollars.
- **A shared record would have avoided 51.3% of the sponsor-by-recipient verifications.** That is 1 − 133,763 distinct recipients ÷ 274,929 sponsor-recipient pairs. The final figure does not depend on the order in which sponsors join.
- **Reuse depends on who joins first.** The table shows the share of the k-th joiner's grant lines whose recipient was already verified by an earlier member:

| k-th joiner | Large sponsors first | Small sponsors first | Random order, mean of 200 |
|---:|---:|---:|---:|
| 2 | 69.4% | 4.3% | 10.0% |
| 5 | 80.9% | 15.0% | 29.8% |
| 10 | 72.3% | 16.6% | 45.8% |
| 20 | 59.3% | 54.0% | 57.9% |
| 48 (all) | 62.9% | 59.7% | 74.5% |

  Fidelity alone holds 71,832 recipients, 54% of all distinct recipients. A network seeded with Fidelity or another national sponsor reaches high reuse from the second member onward. A network of community foundations builds reuse slowly. The overlap does not depend on Fidelity alone: without it, 67.6% of the other 47 sponsors' lines and 70.7% of their dollars still go to recipients funded by at least two of them.

## Method

1. **Universe.** The 50 sponsors with `rank_fy2024 <= 50` (FY2024 DAF assets) in `data/mission-2026-11-14/sponsor-operating-efficiency-2026-11-20.csv` (`record_type=sponsor_year`). All 50 have an FY2023 and an FY2024 object id there.
2. **Return choice.** FY2023 is used as that file labels it, which is the year in which the tax period ends. The tax period ends between 2023-03 and 2023-12 depending on the sponsor. FY2024 is used when the FY2023 return carries no itemised Schedule I Part II. A return counts as attachment-only when it has 1 to 5 lines, none with an EIN, and every name reads like "SEE ATTACHED …". The script records the fiscal year it used for each sponsor.
3. **Fetch.** Each return's public e-file XML comes from the GivingTuesday mirror of IRS TEOS: `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`. The script ran 3 concurrent requests with retries and exponential backoff. 54 files (207 MB) were cached in the session scratchpad and are not committed. Every request succeeded, with no HTTP errors.
4. **Parse.** Every `IRS990ScheduleI/RecipientTable` line (Part II) is read for RecipientEIN, business name, CashGrantAmt and NonCashAssistanceAmt. Amount = cash + non-cash. This is the approach used by `scripts/mission_recipient_sectors.py`. The `local`, `ein9` and `num` helpers are imported from `mission_990_contractors.py`, and `norm_name` from `mission_net_payout.py`.
5. **Exclusions.** These follow prior work (`mission_recipient_sectors.py`):
   - Self-lines, where the recipient EIN equals the filer EIN: 17 lines.
   - DAF-to-DAF lines: 2,885 lines and $4,690.2m. These are lines to a recipient EIN whose decision is `include` in `daf-to-daf-recipient-whitelist.csv`, plus blank-EIN lines whose normalised name matches exactly one whitelisted name.
   - Lines with neither an EIN nor a name: 2 lines.
6. **Keys.**
   - The recipient EIN is normalised to 9 digits (`key_type=ein`).
   - A line with no usable EIN (blank or all zeros) is keyed by its normalised name (`key_type=name`; 2,718 lines, 2,587 keys). Name keys match across sponsors only on an exact normalised name; 103 of them do. They make up 1.9% of recipients and have almost no effect on any result; the `ein_keys_only` scope in the summary repeats the distribution without them.
7. **Edges.** Lines are aggregated per sponsor × recipient_key, giving a line count and a dollar total. Some sponsors file several lines for one recipient. Examples: Morgan Stanley GIFT has 15,818 lines for 13,351 recipients, and NYCT has 2,381 lines for 2,014.

### Definitions

- **n_sponsors(r):** the number of parsed top-50 sponsors whose Schedule I lists recipient key r in the year used.
- **Share to ≥2 (≥6):** the share of kept lines or dollars that go to recipients with n_sponsors ≥ 2, meaning at least one other sponsor funds them (≥ 6: at least five others).
- **Reuse curve.** Sponsors join a network one at a time, in one of three orders:
  - descending `rank_fy2024` (large sponsors first);
  - ascending (small sponsors first);
  - 200 random orders (seed 20261120), reported as the mean with p10 and p90.

  For the k-th joiner, `line_share` is the share of its kept lines whose recipient key appears on any of the k−1 earlier members' Schedule I. `recipient_share` is the same share over its distinct recipients, and `dollar_share` over its dollars. `cum_verifications_avoided` = 1 − |union of the first k members' keys| ÷ Σ distinct keys of the first k members.

## Sources

- IRS e-file XML (GivingTuesday mirror of IRS TEOS), retrieved 2026-11-20. The object id of each return is in the coverage table; each id links to its file. The mirror has been used before in this repo (`XML_URL` in `scripts/mission_990_contractors.py`).
- IRS, *Instructions for Schedule I (Form 990)*, revised 12/2024, https://www.irs.gov/instructions/i990si, retrieved 2026-11-20.
- Repo inputs: `data/mission-2026-11-14/sponsor-operating-efficiency-2026-11-20.csv` (universe, ranks, object ids) and `data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv` (DAF-to-DAF exclusions).

## Coverage

- **48 of 50 sponsors were parsed.** 46 use FY2023 and 2 use FY2024.
- **Not parsed (2): Renaissance Charitable Foundation (rank 9) and Bank of America Charitable Gift Fund (rank 11).** Both their FY2023 and FY2024 returns carry a single placeholder line ("See Attached Grant Report" and "SEE ATTACHED LIST OF DISTRIBUTIONS C/O BANK OF AMERICA"). The itemised list is a non-machine-readable attachment. This matches earlier findings in this repo (batch 34; `research/mission-2026-11-14/`). Those placeholder lines carried $552.6m and $825.2m in FY2023.
- **FY2024 fallback (2): Greater Kansas City Community Foundation (rank 16) and Greater Horizons (rank 17).** Their FY2023 returns are attachment-only ("SEE ATTACHED" for $322.1m; "SEE ATTACHMENT" for $852.9m). Their FY2024 returns itemise 2,405 and 3,284 lines.
- **Fidelity Charitable itemises.** Its FY2023 return (tax period ending 2023-06) has 72,328 Part II lines, the largest of any sponsor.
- **Thin but genuine returns.** Dechomai Asset Trust (rank 20) itemises only 3 lines in FY2023. One is $315.3m to the related Dechomai Foundation, which is kept because it is not on the whitelist. The Signatry (rank 35) itemises 6 lines in FY2023, including $25.7m to the whitelisted Servant Foundation, which is excluded. The rule takes FY2023 whenever it itemises, so these thin years stay in the sample.
- **Totals.** Parsed returns: 282,241 Part II lines. Kept: 279,337 lines carrying $37,274.8m, giving 274,929 edges and 133,763 distinct recipients (131,176 EIN keys and 2,587 name keys).
- **Itemised lines versus filed counts.** Across the parsed returns, the itemised lines total 98.7% of the filers' own Part II line 2 + 3 recipient counts (286,074). For ten sponsors the two differ by more than 5%: AEF (12,725 lines against 15,113), NYCT (2,405 against 2,916), Tulsa CF (2,045 against 2,652) and American Gift Fund (1,484 against 1,894) itemise fewer lines than they count; CJP, Donors Trust, Boston Foundation, Stanford and others itemise more.

### Per-sponsor coverage and overlap

"≥2" = recipient also funded by at least one other parsed top-50 sponsor; "≥6" = by at least five others. The object id links to the XML.

| Rank | Sponsor | FY used | Object id | Period end | Part II lines | Kept lines | Distinct recipients | Kept $m | Lines to ≥2-sponsor recipients | $ to ≥2 | Lines to ≥6 | $ to ≥6 |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | FIDELITY INVESTMENTS CHARITABLE GIFT FUND | FY2023 | [202441369349301334](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202441369349301334_public.xml) | 202306 | 72,328 | 71,833 | 71,832 | 9,198.1 | 59.7% | 86.2% | 10.4% | 59.0% |
| 2 | NATIONAL PHILANTHROPIC TRUST | FY2023 | [202431429349301368](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202431429349301368_public.xml) | 202306 | 15,498 | 15,324 | 15,317 | 3,281.6 | 81.6% | 81.1% | 34.4% | 56.9% |
| 3 | DONOR ADVISED CHARITABLE GIVING INC | FY2023 | [202411039349301716](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411039349301716_public.xml) | 202306 | 48,202 | 47,779 | 47,779 | 4,514.1 | 71.1% | 86.3% | 15.3% | 57.8% |
| 4 | VANGUARD CHARITABLE ENDOWMENT PROGRAM | FY2023 | [202441359349309439](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202441359349309439_public.xml) | 202306 | 21,268 | 21,028 | 21,027 | 1,814.8 | 80.5% | 88.3% | 28.6% | 60.0% |
| 5 | GS DONOR ADVISED PHILANTHROPY FUND | FY2023 | [202413109349303336](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413109349303336_public.xml) | 202312 | 6,245 | 6,155 | 6,036 | 1,833.4 | 85.4% | 88.3% | 46.7% | 61.5% |
| 6 | Silicon Valley Community Foundation | FY2023 | [202413129349304911](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413129349304911_public.xml) | 202312 | 3,316 | 3,264 | 3,246 | 4,559.5 | 77.9% | 28.8% | 38.2% | 20.3% |
| 7 | MORGAN STANLEY GLOBAL IMPACT FUNDING TRUST INC | FY2023 | [202403209349313980](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403209349313980_public.xml) | 202312 | 16,056 | 15,818 | 13,351 | 876.2 | 83.0% | 88.1% | 42.3% | 61.5% |
| 8 | AMERICAN ENDOWMENT FOUNDATION | FY2023 | [202442479349301654](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202442479349301654_public.xml) | 202312 | 12,725 | 12,581 | 12,491 | 854.6 | 74.7% | 77.7% | 33.5% | 54.6% |
| 9 | Renaissance Charitable Foundation Inc | none | 202443109349303629 / 202543189349301959 | 202312 / 202412 | attachment only | – | – | – | – | – | – | – |
| 10 | NATL CHRISTIAN CHARITABLE FDN INC | FY2023 | [202443169349306424](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443169349306424_public.xml) | 202312 | 14,557 | 14,453 | 14,453 | 1,854.9 | 64.3% | 75.4% | 15.5% | 42.4% |
| 11 | BANK OF AMERICA CHARITABLE GIFT FD | none | 202520169349301042 / 202503219349318170 | 202312 / 202412 | attachment only | – | – | – | – | – | – | – |
| 12 | The Chicago Community Trust | FY2023 | [202442279349302684](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202442279349302684_public.xml) | 202309 | 3,801 | 3,742 | 3,742 | 1,481.6 | 74.3% | 72.6% | 38.0% | 37.1% |
| 13 | IMPACTASSETSINC | FY2023 | [202443189349305024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443189349305024_public.xml) | 202312 | 2,654 | 2,594 | 2,417 | 226.7 | 80.2% | 80.0% | 42.0% | 44.9% |
| 14 | JEWISH COMMUNAL FUND | FY2023 | [202410969349301036](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202410969349301036_public.xml) | 202306 | 4,340 | 4,304 | 4,304 | 798.2 | 86.2% | 96.0% | 34.1% | 70.4% |
| 15 | FOUNDATION FOR THE CAROLINAS | FY2023 | [202433209349318318](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349318318_public.xml) | 202312 | 1,399 | 1,385 | 1,341 | 507.6 | 66.3% | 85.4% | 30.5% | 66.4% |
| 16 | Greater Kansas City Community Foundation | FY2024 | [202533189349314033](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189349314033_public.xml) | 202412 | 2,405 | 2,372 | 2,367 | 342.1 | 61.6% | 80.7% | 27.6% | 43.9% |
| 17 | Greater Horizons | FY2024 | [202513189349309621](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513189349309621_public.xml) | 202412 | 3,284 | 3,239 | 3,233 | 190.4 | 73.4% | 81.5% | 37.9% | 52.7% |
| 18 | Combined Jewish Philanthropies of Greater Boston Inc | FY2023 | [202421289349303727](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202421289349303727_public.xml) | 202306 | 963 | 956 | 846 | 171.0 | 90.1% | 97.1% | 53.0% | 71.5% |
| 19 | RAYMOND JAMES CHARITABLE ENDOWMENT FUND | FY2023 | [202430469349302713](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202430469349302713_public.xml) | 202303 | 5,810 | 5,735 | 5,735 | 209.3 | 78.5% | 84.7% | 35.5% | 51.5% |
| 20 | DECHOMAI ASSET TRUST | FY2023 | [202413199349316041](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413199349316041_public.xml) | 202312 | 3 | 2 | 2 | 22.1 | 0.0% | 0.0% | 0.0% | 0.0% |
| 21 | THE NEW YORK COMMUNITY TRUST | FY2023 | [202443179349309079](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443179349309079_public.xml) | 202312 | 2,405 | 2,381 | 2,014 | 186.6 | 83.0% | 87.7% | 51.5% | 66.6% |
| 22 | COLUMBUS FOUNDATION | FY2023 | [202443199349305349](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443199349305349_public.xml) | 202312 | 1,789 | 1,768 | 1,720 | 261.4 | 61.4% | 67.9% | 30.0% | 35.5% |
| 23 | Donors Trust Inc | FY2023 | [202423189349304787](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423189349304787_public.xml) | 202312 | 779 | 769 | 635 | 246.2 | 75.6% | 82.1% | 44.2% | 62.1% |
| 24 | THE US CHARITABLE GIFT TRUST | FY2023 | [202431319349304428](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202431319349304428_public.xml) | 202312 | 5,512 | 5,454 | 5,450 | 151.5 | 70.6% | 76.2% | 34.7% | 46.5% |
| 25 | THE AYCO CHARITABLE FOUNDATION | FY2023 | [202413109349304401](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413109349304401_public.xml) | 202312 | 4,178 | 4,128 | 3,900 | 213.1 | 89.1% | 93.3% | 55.4% | 75.2% |
| 26 | The Oregon Community Foundation | FY2023 | [202403129349303815](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403129349303815_public.xml) | 202312 | 2,049 | 2,036 | 2,010 | 187.6 | 47.2% | 50.8% | 13.6% | 18.5% |
| 27 | Boston Foundation Inc | FY2023 | [202401319349302380](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202401319349302380_public.xml) | 202306 | 2,045 | 2,015 | 1,779 | 158.5 | 81.1% | 86.7% | 40.3% | 58.2% |
| 28 | CALIFORNIA COMMUNITY FOUNDATION | FY2023 | [202441359349312719](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202441359349312719_public.xml) | 202306 | 1,936 | 1,908 | 1,908 | 315.2 | 70.9% | 78.7% | 34.3% | 51.8% |
| 29 | THE COMMUNITY FOUNDATION FOR GREATER | FY2023 | [202540559349301329](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202540559349301329_public.xml) | 202312 | 1,328 | 1,308 | 1,308 | 160.9 | 69.8% | 67.6% | 33.2% | 36.2% |
| 30 | Servant Foundation | FY2023 | [202410409349300211](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202410409349300211_public.xml) | 202303 | 2,093 | 2,066 | 2,055 | 448.6 | 75.9% | 93.2% | 31.3% | 56.6% |
| 31 | JEWISH COMMUNITY FEDERATION OF SAN | FY2023 | [202431369349314563](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202431369349314563_public.xml) | 202306 | 1,037 | 1,023 | 1,023 | 93.3 | 91.4% | 94.7% | 61.4% | 74.6% |
| 32 | THE BESSEMER GIVING FUND | FY2023 | [202423199349308562](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423199349308562_public.xml) | 202312 | 1,352 | 1,314 | 1,314 | 109.3 | 86.1% | 91.2% | 54.9% | 75.6% |
| 33 | GREATER HOUSTON COMMUNITY FOUNDATION | FY2023 | [202423209349321922](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423209349321922_public.xml) | 202312 | 1,692 | 1,671 | 1,671 | 177.9 | 69.4% | 87.0% | 31.7% | 60.3% |
| 34 | MARIN COMMUNITY FOUNDATION | FY2023 | [202421369349304932](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202421369349304932_public.xml) | 202306 | 1,189 | 1,173 | 1,173 | 105.3 | 87.0% | 88.5% | 52.9% | 63.3% |
| 35 | THE SIGNATRY CHARITABLE TRUST | FY2023 | [202443209349305764](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443209349305764_public.xml) | 202312 | 6 | 5 | 5 | 0.1 | 80.0% | 90.6% | 60.0% | 65.1% |
| 36 | COMMUNITY FOUNDATION OF NEW JERSEY | FY2023 | [202423209349302727](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423209349302727_public.xml) | 202312 | 1,199 | 1,183 | 1,147 | 58.8 | 76.5% | 76.5% | 41.2% | 51.7% |
| 37 | THE DENVER FOUNDATION | FY2023 | [202433119349303518](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433119349303518_public.xml) | 202312 | 1,155 | 1,130 | 1,080 | 126.2 | 67.7% | 75.7% | 26.7% | 37.9% |
| 38 | JEWISH COMMUNITY FOUNDATION OF LOS ANGELES | FY2023 | [202413189349309986](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413189349309986_public.xml) | 202312 | 992 | 978 | 978 | 114.8 | 87.0% | 94.1% | 42.5% | 62.0% |
| 39 | THE SAN DIEGO FOUNDATION | FY2023 | [202421349349305987](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202421349349305987_public.xml) | 202306 | 1,105 | 1,096 | 1,070 | 116.8 | 61.4% | 73.1% | 24.7% | 35.5% |
| 40 | TULSA COMMUNITY FOUNDATION | FY2023 | [202433209349321258](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349321258_public.xml) | 202312 | 2,045 | 2,031 | 2,005 | 168.1 | 55.4% | 45.3% | 22.2% | 20.6% |
| 41 | COMMUNITY FOUNDATION | FY2023 | [202323129349300447](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202323129349300447_public.xml) | 202304 | 757 | 739 | 717 | 111.7 | 61.6% | 55.6% | 29.5% | 22.3% |
| 42 | THE BOARD OF TRUSTEES OF THE LELAND | FY2023 | [202431949349300033](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202431949349300033_public.xml) | 202308 | 103 | 99 | 90 | 43.7 | 89.9% | 96.6% | 67.7% | 94.2% |
| 43 | AMERICAN GIFT FUND | FY2023 | [202433199349316708](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433199349316708_public.xml) | 202312 | 1,484 | 1,460 | 1,448 | 57.1 | 83.2% | 87.2% | 50.1% | 58.0% |
| 44 | UCLA FOUNDATION | FY2023 | [202411309349304501](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411309349304501_public.xml) | 202306 | 58 | 57 | 57 | 407.3 | 77.2% | 97.8% | 26.3% | 91.3% |
| 45 | THE MINNEAPOLIS FOUNDATION | FY2023 | [202323559349300512](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202323559349300512_public.xml) | 202303 | 1,365 | 1,346 | 1,315 | 86.1 | 74.7% | 84.2% | 32.8% | 50.4% |
| 46 | T ROWE PRICE PROGRAM FOR CHARITABLE | FY2023 | [202321949349300147](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202321949349300147_public.xml) | 202303 | 2,215 | 2,186 | 2,186 | 85.2 | 82.8% | 90.7% | 45.7% | 62.8% |
| 47 | THRIVENT CHARITABLE IMPACT & INVESTING | FY2023 | [202443169349301749](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443169349301749_public.xml) | 202312 | 2,127 | 2,111 | 2,040 | 60.2 | 60.7% | 71.3% | 24.6% | 31.2% |
| 48 | THE SAN FRANCISCO FOUNDATION | FY2023 | [202431359349311628](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202431359349311628_public.xml) | 202306 | 1,546 | 1,517 | 1,510 | 165.7 | 81.5% | 85.7% | 41.9% | 55.1% |
| 49 | COMMUNITY FOUNDATION OF TAMPA BAY INC | FY2023 | [202421349349306297](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202421349349306297_public.xml) | 202306 | 489 | 486 | 471 | 26.5 | 72.4% | 79.9% | 34.6% | 50.9% |
| 50 | SAINT PAUL & MINNESOTA FOUNDATION | FY2023 | [202442349349300824](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202442349349300824_public.xml) | 202312 | 1,357 | 1,335 | 1,331 | 95.0 | 62.9% | 70.5% | 26.7% | 42.0% |

## Results

### Recipients by number of top-50 sponsors funding them

All keys, 48 sponsors, kept lines:

| Funded by | Recipients | % of recipients | Lines | % of lines | Dollars ($m) | % of dollars |
|---|---:|---:|---:|---:|---:|---:|
| 1 sponsor | 80,096 | 59.9% | 80,252 | 28.7% | 8,503.3 | 22.8% |
| 2 | 24,030 | 18.0% | 48,210 | 17.3% | 3,053.6 | 8.2% |
| 3–5 | 22,058 | 16.5% | 81,016 | 29.0% | 6,361.1 | 17.1% |
| 6–10 | 6,187 | 4.6% | 45,706 | 16.4% | 6,926.5 | 18.6% |
| 11–25 | 1,297 | 1.0% | 19,953 | 7.1% | 7,662.7 | 20.6% |
| 26+ | 95 | 0.1% | 4,200 | 1.5% | 4,767.6 | 12.8% |
| **Total** | **133,763** | | **279,337** | | **37,274.8** | |

- With EIN keys only, the shares change by less than 1 percentage point (`scope=ein_keys_only` in the summary CSV).
- The most widely shared recipients are each funded by 39 to 43 of the 48 sponsors. In order: American National Red Cross (43); Médecins Sans Frontières USA, World Central Kitchen, The Nature Conservancy and St Jude Children's Research Hospital (41 each); Harvard (40); Planned Parenthood Federation of America, US Fund for UNICEF, American Cancer Society, Alzheimer's Association, American Heart Association and International Rescue Committee (39 each).

### Pooled shares

| Scope | Lines to ≥2 | Dollars to ≥2 | Recipients with ≥2 | Lines to ≥6 | Dollars to ≥6 | Recipients with ≥6 |
|---|---:|---:|---:|---:|---:|---:|
| All 48 sponsors | 71.3% | 77.2% | 40.1% | 25.0% | 51.9% | 5.7% |
| Without Fidelity (47) | 67.6% | 70.7% | 36.0% | 24.2% | 44.8% | 5.0% |

Across sponsors, the share of lines going to recipients funded by at least two sponsors mostly falls between 55% and 91%. Exceptions:

- Oregon CF has the lowest share among full itemisers: 47.1% of lines and 50.7% of dollars.
- Silicon Valley CF has only 28.8% of dollars to shared recipients against 77.8% of lines. A few very large single-funder lines dominate its dollars; prior work notes that CZ Biohub lines dominate its FY2023 Schedule I.
- Dechomai has 0% to shared recipients, from 2 kept lines.

### Network reuse curve

- k counts the parsed sponsors in order (48 in total). The ranks run 1–50 with ranks 9 and 11 absent, so the descending k = 10 is Chicago Community Trust (rank 12).
- In the descending order, k = 2 is NPT, k = 5 is GS DAPF, k = 20 is Columbus Foundation and k = 48 is Saint Paul & Minnesota Foundation.
- In the ascending order, k = 1 is Saint Paul & Minnesota (rank 50), k = 2 is CF of Tampa Bay, k = 5 is T. Rowe Price, k = 20 is Jewish Community Federation of San Francisco and k = 48 is Fidelity.
- Single-sponsor values swing from one k to the next because each is one sponsor's portfolio. The random-order mean and the cumulative measure are the stable summaries.

**Share of the k-th joiner's grant lines already verified by earlier members**

| k | Descending (large first) | Ascending (small first) | Random mean (p10–p90) |
|---:|---:|---:|---:|
| 1 | 0.0% | 0.0% | 0.0% (0.0–0.0) |
| 2 | 69.4% | 4.3% | 10.0% (0.7–21.8) |
| 3 | 60.4% | 3.8% | 17.8% (3.1–35.6) |
| 5 | 80.9% | 15.0% | 29.8% (9.6–58.2) |
| 10 | 72.3% | 16.6% | 45.8% (24.8–72.6) |
| 15 | 71.7% | 24.9% | 52.8% (32.1–76.6) |
| 20 | 59.3% | 54.0% | 57.9% (36.8–78.6) |
| 25 | 80.6% | 13.2% | 62.0% (41.2–80.7) |
| 30 | 86.1% | 50.4% | 66.9% (47.9–85.2) |
| 40 | 89.9% | 32.3% | 71.7% (57.4–86.0) |
| 48 (all) | 62.9% | 59.7% | 74.5% (61.4–87.0) |

**Share of the k-th joiner's distinct recipients already verified**

| k | Descending | Ascending | Random mean (p10–p90) |
|---:|---:|---:|---:|
| 2 | 69.4% | 4.2% | 9.6% (0.7–21.8) |
| 5 | 80.5% | 15.0% | 29.1% (9.2–58.1) |
| 10 | 72.3% | 15.5% | 45.0% (24.1–72.6) |
| 20 | 58.5% | 54.0% | 57.3% (36.5–77.7) |
| 48 (all) | 62.9% | 59.7% | 73.9% (60.4–87.0) |

**Share of the k-th joiner's dollars already verified**

| k | Descending | Ascending | Random mean (p10–p90) |
|---:|---:|---:|---:|
| 2 | 73.0% | 3.7% | 16.3% (0.8–41.1) |
| 5 | 83.7% | 23.3% | 40.1% (10.3–75.9) |
| 10 | 67.4% | 8.0% | 57.8% (29.3–85.4) |
| 20 | 66.4% | 69.4% | 67.0% (40.0–89.1) |
| 48 (all) | 70.5% | 86.2% | 81.0% (67.9–96.0) |

**Cumulative share of per-sponsor verifications avoided after k members**

| k | Descending | Ascending | Random mean (p10–p90) |
|---:|---:|---:|---:|
| 2 | 12.2% | 1.1% | 2.8% (0.4–5.6) |
| 5 | 37.2% | 7.5% | 10.0% (4.9–15.0) |
| 10 | 44.5% | 14.9% | 19.8% (12.9–27.2) |
| 20 | 47.5% | 20.4% | 32.2% (25.4–39.6) |
| 30 | 49.8% | 26.6% | 41.0% (36.2–46.2) |
| 40 | 50.5% | 32.7% | 47.2% (43.6–50.0) |
| 48 (all) | 51.3% | 51.3% | 51.3% |

The summary CSV has every k from 1 to 48 for all four metrics and all three orders.

## Limitations

- **Universe.** The sample is top-50 sponsors only, and only those that itemise in the XML (48). Renaissance and BofA CGF together held $1.38bn of FY2023 Schedule I grants in attachments and are missing. With sponsors outside the top 50, most of them community foundations, overlap per sponsor would rise. The curve would also gain many small portfolios with mostly local recipients, as the ascending order hints. This study does not measure that.
- **Reporting threshold.** The IRS Schedule I instructions (rev. 12/2024) say to "enter information only for each recipient domestic organization or domestic government that received more than $5,000 aggregate of grants or assistance from the organization during the tax year." Two consequences:
  - The threshold is per recipient, aggregated over the tax year, and set at more than $5,000. A recipient whose total from a sponsor that year was $5,000 or less does not appear, so every count here undercounts small recipients and small sponsor-recipient relationships. Overlap among charities that receive only small grants is invisible.
  - The instructions ask for one line per recipient. Some filers still split a recipient across several lines, which is why lines exceed distinct recipients for some sponsors. Line-based shares therefore weight those sponsors' repeat lines; the recipient-based shares do not.
- **Domestic only.** Schedule I covers domestic organisations and governments. Foreign grants go on Schedule F and are not here, so overlap among international recipients is understated, for example where one sponsor's intermediary is the same as another's.
- **One fiscal year.** Fiscal years are not aligned: tax periods end between 2023-03 and 2023-12, and two sponsors use the year ending 2024-12. Recipients that one sponsor funds in alternate years are counted as unshared. A multi-year panel would show more reuse, because a verification would stay valid for some period.
- **Itemised lines versus declared counts.** Several filers' itemised lines differ from their own Part II recipient counts (see Coverage). The XML may be incomplete for AEF, NYCT, Tulsa and American Gift Fund.
- **EIN-less lines.** 2,718 lines (1.0%) have no usable EIN. They are matched across sponsors only on an exact normalised name, which understates their overlap. The effect on results is under 1 percentage point.
- **EIN identity is not verification identity.** An EIN can cover a national charity and many chapters or projects. Fiscal-sponsor EINs and university EINs, which stand for many departments, also merge recipients that different checks would treat separately. Conversely, affiliates with separate EINs (local Red Cross regions, separately incorporated chapters) are counted as different recipients.
- **DAF and non-DAF grants are mixed.** Community-foundation, university (Stanford, UCLA) and federation returns include non-DAF grants on Schedule I. The edge list holds all Schedule I lines except DAF-to-DAF and self-lines, not DAF grants only.
- **Related-party lines** that are not on the DAF-to-DAF whitelist are kept, for example Dechomai Asset Trust to Dechomai Foundation.

## What the curve shows and does not show

**Shows.** The curve measures the potential for reuse: how often a charity one sponsor must check was also granted to by another top-50 sponsor in the same year. Pooled across the 48 sponsors, about half of all sponsor-recipient checks (51.3%) are repeats of checks another sponsor made. For any sponsor joining a mature network, roughly 60% to 75% of its lines would be to already-verified recipients. Order matters a great deal. A network seeded by national sponsors delivers reuse at once (69% at k = 2). A network of community foundations reaches comparable reuse only after about 20 members, and that reuse comes from the national sponsors joining last.

**Does not show:**

- **That sponsors would share.** Overlap is a precondition, not evidence of willingness to share. Competitive, liability and data-licensing concerns are not measured.
- **The cost saved per reuse.** Per-sponsor verification is often already outsourced to a common vendor (IRS Pub 78/BMF lookups, Candid/GuideStar, OFAC screening). Much of the "verification" is then already shared through those vendors, so the extra saving from a sponsor network is the residual: enhanced due diligence, grant-purpose review and expenditure-responsibility files. Its cost per recipient is not measured here.
- **Validity over time.** A record that is reused must still be current. The single-year snapshot does not show how quickly verifications expire or how often recipients change status.
- **Causation or network dynamics.** The curve is an accounting of overlap in one year's filings. It does not model join incentives, free-riding, or growth in members beyond the top 50.
