# Validation wave 5: independent check of 12 claims (V5-01 to V5-12)

Validator: independent-validation-agent-wave5. Date: 2026-11-14. Register: `data/mission-2026-11-14/validation-register-wave5.csv`.

**Method.** For each claim, a verdict was formed from primary sources first. Those sources were IRS e-file XML (GivingTuesday mirror `gt990datalake-rawdata`, located through the IRS TEOS index), crt.sh, first-party web pages, and a rerun of the repo scripts on a copy of the repository. The repo document making the claim was read only afterwards. ProPublica XML downloads return 403. altruist.com, reninc.com, candid.org and tifin.com also returned 403, and those gaps are noted per claim.

## Verdicts

| ID | Verdict | Confidence | One-line finding |
|---|---|---|---|
| V5-01 Givinga / Golden Hearts | **Partially confirmed** | Figures high; inference low | The Schedule G figures are exact. The "player records" inference is plausible for CY2022 only. The repo's supporting sentence misstates the count path, and another repo document gives a different explanation. |
| V5-02 Givinga counts | **Confirmed** | High | All nine returns match. CY2021 was also amendment-only. CY2019 was 13,192. |
| V5-03 Cost per grant / bps | **Confirmed with caveats** | Medium-high | Part IX numerators match the XML to the dollar for all four sponsors, and the pool bps reproduce. However, the figures are not FY2024, and the definition is more than "total expenses minus grants". |
| V5-04 Corrected DAFRC $323.27bn | **Confirmed** | High | The script rerun reproduces both output files byte-for-byte. Six itemized adjustments match the XML. |
| V5-05 Ren 30 sponsors / $48.55bn | **Confirmed with caveats** | Arithmetic high; meaning medium | The arithmetic and six XML spot checks hold. But the count is cumulative over FY2022–25: only 18 sponsors holding $30.18bn (9.2%) name Ren or Stellar in their latest return. |
| V5-06 ImpactAssets→GiveClear | **Confirmed** | High | Every figure is exact. GiveClear's account count of 228 is identical in both years and looks stale. |
| V5-07 Vanguard–Altruist | **Confirmed** | Medium-high | The deal had not closed as of 2026-11-14. Endaoment as sponsor is confirmed through trade press, because the Altruist page itself returned 403. |
| V5-08 api-give cert | **Confirmed** | High | The certificate dates 2026-02-25, issued the same day as the api-salesforce, api-vgi and auth0 certificates. No wildcard certificate covers the host. |
| V5-09 Daffy agreement | **Confirmed** | High | The quote is exact. The same clause also sets a $10 minimum per recommendation. |
| V5-10 Every.org 990-PF | **Confirmed** | High | Network for Good's share was 73.9% in 2020 and 1.06% in 2024. The 2024 share is a floor. |
| V5-11 SOC scope | **Confirmed with caveats** | Medium | No public report period was found. Foundant comes closest: it names its auditor and the five criteria. Three vendor sites could not be read. |
| V5-12 WaterStone | **Confirmed with correction** | High | Stellar appears from FYE 3/2013, a year earlier than claimed. A legacy Stellar "Open A Fund" link is still live on the new login page. |

## Key evidence and challenges

### V5-01 and V5-02: Givinga

**What the Schedule G returns show:**
- **CY2022 original:** Golden Hearts Games (GHG) had gross receipts of $15,434,278 and retained $13,221,986 (85.7%). GHG is 81% of Schedule G gross and 44.8% of the $34,461,745 in contributions.
- **CY2022 amended:** GHG had gross receipts of $18,150,728 and retained $15,320,211 (84.4%).
- **GHG was the largest fundraiser only in CY2022:**
  - In CY2021 the largest was SoftGiving ($5.08m against GHG's $3.72m).
  - In CY2023 the largest was Brandfluence ($4.37m), which shares SoftGiving's Atlanta address.
- **CY2024:** there is no Schedule G, and line 11e is $6,462.
- **GHG's nature:** GHG's site today calls itself a "free-to-play casino" with "Official Sweepstakes Rules", so the label "charity sweepstakes casino" is supported.

**Why the inference falls short.** The account count fell to 955,569 in CY2023, when GHG receipts dropped to $3.42m. It then rose by 465,442 to 1,421,011 in CY2024, a year with no Schedule G fundraiser at all. "Dormant records carried forward" cannot explain a rise. Separately, `queue-assurance-everyorg-givinga-monitoring.md` (P-INF-01) attributes the count to employer-provisioned employee accounts, which contradicts `sponsor-cost-structure-and-sensitivities.md`.

### V5-03: cost per grant and bps

**Recomputed operating cost** (total functional expenses, minus grants on lines 1–3, line 4 and line 11f), checked against the XML:

| Sponsor | Operating cost | Matches CSV numerator |
|---|---|---|
| Fidelity Charitable | $203,086,532 | Yes |
| DAFgiving360 | $87,351,879 | Yes |
| National Philanthropic Trust | $66,886,539 | Yes |
| Vanguard Charitable | $36,023,935 | Yes |

**Recomputed pool bps:**
- National-Standard: 32.2 bps on the asset allocation and 32.7 bps on the grant allocation.
- Community foundations: 127.2 bps on the asset allocation and 177.0 bps on the grant allocation.

**Caveats:**
- **Periods.** Three of the four sponsors use FY Jun-2025 returns, and the grant counts are CY2025 or FY Jun-2026.
- **Fidelity components.** Fidelity's operating cost includes $15.6m of "other charitable investment advisor program" and $5.7m of taxes. Excluding these gives about $59 per grant.
- **Period-matched Fidelity.** Fidelity reports 2.7m grants in CY2024 and 3.0m in CY2025. Using the average of about 2.85m gives about $71 per grant.
- **DAFgiving360 count.** Applying the repo's own +21% growth figure gives an FY2025 count of about 1.32m and about $66 per grant.
- **Vanguard.** Vanguard's FY Jun-2025 990 (object 202621329349306657) is in the IRS index but not yet in the mirror. Its 18-month period gap can therefore be closed later.

### V5-04: corrected DAFRC total

- FY2024 assets move from $327,870,852,179 to **$323,269,551,062**, a change of −$4.601bn (−1.403%).
- By rule: R1 contributes −$4.882bn (637 rows), R3 −$42.5m (19 rows) and R4 +$322.7m (2 rows).
- Spot checks against filed Schedule D Part I values all match:
  - AEF: $8,377,997,971
  - GS DAPF: $12,640,914,117
  - Dechomai: $1,432,172,839
  - ImpactAssets: $2,896,880,396
  - Donors Fund (R4, amended return): $315,757,385
  - Oracle Health Foundation (R3): line 6 = No, Schedule D Part I blank

### V5-05: Ren footprint

- **Recomputation:** 30 EINs hold $48.549bn of $327.871bn, which is 14.81%. The "Russian Renaissance Restaurant" false positive is correctly excluded.
- **Six Part VII-B lines confirmed in the XML:** GS CGF, MS GIFT, NCF, ImpactAssets, Stifel and GS DAPF.
- **Caveats on meaning:**
  - The 30 are sponsors named in any FY2022–25 return. Only **18 sponsors holding $30.18bn (9.2%)** name Ren or Stellar in their latest parsed return.
  - GS DAPF holds $11.84bn, 24% of the numerator, but appears in FY2022 only.
  - On the corrected denominator the share is 15.0%.
  - The numerator uses DAFRC asset values, some of them imputed.

### V5-12: WaterStone

- WaterStone's Part VII-B names Stellar in every e-filed return from FYE 3/2013 ($121,482) through FYE 3/2025.
- The login page is confirmed: "If you haven't logged in since November 1, 2026…".
- The page's "Open A Fund" button still links to `iphi.stellartechsol.com`.

## Exact corrections

1. **`research/mission-2026-11-14/sponsor-cost-structure-and-sensitivities.md`, §6 line 27.**
   - Replace: "**[I]** The 1.5m "accounts" are most plausibly player and app-user records."
   - With: "**[I]** The account unit is undefined. For CY2022, game and app-user records (GHG, SoftGiving) are the most consistent reading. Employer-provisioned employee accounts are an alternative candidate (see P-INF-01). Neither is confirmed."

2. **Same file, line 217.**
   - Replace: "and the persistence of the 1.42m count in CY2024 after the fundraiser lines vanish (dormant records carried forward)."
   - With: "but not the path of the count. It fell to 955,569 in CY2023, as GHG receipts dropped to $3.42m, then rose by 465,442 to 1,421,011 in CY2024 with no Schedule G fundraiser. Carried-forward dormant records cannot produce that rise, so the CY2024 count needs another source (for example, employer programs)."

3. **Same file, line 25.** After "as Givinga's largest "online fundraising" agent", insert "in CY2022 (SoftGiving was larger in CY2021 and Brandfluence in CY2023)".

4. **`research/mission-2026-11-14/queue-assurance-everyorg-givinga-monitoring.md`, P-INF-01.**
   - Replace: "**[I]** The 1.4m most plausibly counts employee accounts provisioned by employer programs, most with near-zero balances ($1.37 average)."
   - With: "**[I]** The unit is undefined. Candidates are employer-provisioned employee accounts and game/app-user records from Schedule G fundraisers (Golden Hearts Games, SoftGiving/Brandfluence; see sponsor-cost-structure-and-sensitivities.md §6). Average balance is $1.37."

5. **`sponsor-cost-structure-and-sensitivities.md`, line 10.**
   - Replace: "operating cost (total functional expenses minus grants, excluding investment-management fees)"
   - With: "operating cost (total functional expenses minus grants on lines 1–3, member benefits on line 4 and investment-management fees on line 11f)"

6. **Same file, after the table in §4.4.**
   - Add: "Fidelity's $203.1m includes $15.6m of 'other charitable investment advisor program' and $5.7m of taxes (about $59 per grant without them). Against a period-matched count of about 2.85m (average of CY2024 and CY2025) the figure is about $71. Vanguard's FY Jun-2025 990 (object 202621329349306657) is in the IRS index but not yet mirrored; use it when it is."
   - Wherever these figures are cited as "FY2024", relabel them "latest 990 (FY Jun-2024/25)".

7. **`research/mission-2026-11-14/full-universe-990-harvest-and-corrected-totals.md`, line 141.**
   - Replace: "Ren's 990-evidenced reach is **14.8% of DAFRC assets**. It is a floor:"
   - With: "Ren's 990-evidenced reach is **14.8% of DAFRC assets** cumulatively: 30 sponsors named in any FY2022–25 return. Only 18 sponsors holding $30.18bn (9.2%) name Ren or Stellar in their latest parsed return; GS DAPF ($11.84bn) appears in FY2022 only. On corrected FY2024 assets the cumulative share is 15.0%. It is a floor for current use only in the sense that Part VII-B lists just the top five contractors over $100k:"
   - Apply the same qualifier to `strategic-synthesis.md` and `FINAL-STATUS.md` ("14.8% 990-paid").

8. **`research/mission-2026-11-14/queue-give-interactive-displacement.md`, line 60.**
   - Replace: "Stellar in **every year FYE 3/2014–3/2025**, rising from $119,943 to $366,469"
   - With: "Stellar in **every e-filed year FYE 3/2013–3/2025**, from $121,482 (FYE 3/2013) to $366,469. The new login page's 'Open A Fund' button still links to iphi.stellartechsol.com (2026-11-14)."

9. **`research/mission-2026-11-14/queue-watchlist-and-vendor-moves.md`, line 28 (P-VEN-08).** After "GiveClear as a whole reported **228 DAFs and $215.3m**", add: "The count of 228 is identical to CY2023's despite 8.7× asset growth, so treat it as unreliable."

10. **`queue-assurance-everyorg-givinga-monitoring.md`, P-QA2-04.** After "falling to 1.1% in 2024 [C]", add: "This is a floor, because CY2024 reports $6.58m in aggregate to recipients under $25k."

11. **`queue-assurance-everyorg-givinga-monitoring.md`, P-QA1-04.** After "Foundant, Give Interactive, Chariot, Blackbaud, Benevity", add: "(Foundant names its auditor, Linford & Co, and all five Trust Services Criteria, but not the period)". Also add: "reninc.com, candid.org and tifin.com returned 403 to the wave-5 validator."

No corrections are needed for V5-02, V5-04, V5-06 (numbers), V5-07, V5-08, V5-09 or V5-10 (numbers).
