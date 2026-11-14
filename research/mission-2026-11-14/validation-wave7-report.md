# Validation wave 7: community-foundation rails and portals, DAFpay terms, Goodstack, Fidelity export, PE map

**Date:** 2026-11-14. **Validator:** independent-validation-agent-wave7.
**Method:** For each claim I formed a verdict from primary sources first: foundation pages and portal login pages fetched with curl and WebFetch, dafpay.com terms and privacy policy, Goodstack and giftall.org pages, Fidelity Charitable PDFs, IRS e-file XML from the GivingTuesday data lake, and deal press releases. Only then did I read `queue-community-foundation-rails-portals.md`, `queue-fidelity-chariot-goodstack-vanguard.md` and `private-equity-daf-ecosystem-map.md`. I logged in nowhere, submitted no forms and contacted no one.
**Register:** [`data/mission-2026-11-14/validation-register-wave7.csv`](../../data/mission-2026-11-14/validation-register-wave7.csv) has 18 rows covering 7 claims. V7-02 is split by foundation and V7-07 by deal.

## Verdicts

| Claim | Result | Key point |
|---|---|---|
| V7-01 Seattle ACH mandatory from 2026-06-30 | **confirmed** | The EFT page says "Effective June 30, 2026, organizations must be enrolled in ACH Transfer to receive future grant payments." It does not mention DAF grants. |
| V7-02a SPMF moving to Chariot | **confirmed** | The SPMF FAQ ("We are adopting Chariot") and a Chariot post dated Sep 15 say the move happens "this fall", "with a few exceptions". Enrolment is optional and checks remain. The year is inferred from the © 2026 footers. |
| V7-02b CF Greater Atlanta uses Bill.com | **confirmed** | The grantee guide (2025-12) and the Nonprofit Partners page say so. Instant transfer carries a 1% Bill.com fee. |
| V7-02c NHCF uses Checkmint | **confirmed** | The FAQ says the foundation is "moving to an automated check payment service: Checkmint by Citizens Bank". |
| V7-02d CCT mails DAF grant checks | **confirmed** | The FAQ says checks "are then mailed … within five and seven business days". This covers DAF grants only. |
| V7-02e GWCF uses "Blackbaud REPAY" since Sept 2026 | **partially_confirmed** | GWCF says it "partnered with Blackbaud **and** REPAY", which are two companies. "ACH is the default method", with a check fallback. The upgrades were "completed in September 2026". |
| V7-03 Top-40 portal census | **confirmed** | All 15 spot-checks matched: CCT, FFTC, SVCF, Oregon, California CF, Columbus, NHCF, Rhode Island, Cleveland, Minneapolis, SPMF, Greater Houston, Seattle, GWCF and San Diego. The NPact attribution for spectrumportal.net still rests on third-party sources, and the sign-in page loads Blackbaud's checkout script. |
| V7-04 DAFpay Donor Terms and privacy policy | **confirmed** | The effective date (2025-09-24), the 2FA-triggering consent, the US$1,000 cap and the third-party ban are all verbatim. Nothing covers bots, agents or AI. The privacy policy (effective "Janurary 8th, 2025") says both "not stored" and "segmented storage of all Credentials". |
| V7-05 Goodstack and Percent Impact Foundation | **partially_confirmed** | The FY2024 figures are exact: 7,268 DAFs and $1,812,959. **They are superseded:** the FY2025 990 (filed 2026-09-02) reports a $10,772,483 DAF year-end value, 3 DAFs, $11.58m contributions and $12.78m total assets. "Runs" overstates the link: giftall.org calls them "independent charitable foundations" that "work with Goodstack". The six logos are confirmed. |
| V7-06 Fidelity Charitable data export | **confirmed** (absence-based) | The how-to PDF (created 2026-05-26) gives a per-document PDF download only. The guidelines give a "view, but not necessarily modify" privilege. No CSV, API or portability text was found. The only CSV export found is for Fidelity.com brokerage accounts. |
| V7-07a Audax and Foundation Source | **confirmed** | Unitranche, 2020-01-28. This is historical, not a current lender relationship. |
| V7-07b Warburg and Bloomerang | **confirmed** | 2024-02-08. |
| V7-07c Insight and Altruist | **partially_confirmed** | Insight led the Series D (2023-04). Vanguard signed a definitive agreement to acquire Altruist on **2026-08-26**, so Insight's position ends at closing. |
| V7-07d GTCR ~25% of CAPTRUST | **partially_confirmed** | 25% was the 2020 figure. After Carlyle entered on 2023-09-19, GTCR remains a minority investor, but no percentage has been disclosed. |
| V7-07e GA and TPG in Benevity and Creative Planning | **partially_confirmed** | Creative Planning is confirmed by TPG's 2024 release ("joining existing investor General Atlantic"). The Benevity leg rests only on 2020–21 evidence. TPG holds through two different funds: The Rise Fund (Benevity) and TPG Capital (Creative Planning). |
| V7-07f Bain and FreeWill Series B | **confirmed** | The lead was Bain Capital **Double Impact**, $30m, 2022-03-02. |
| V7-07g Bonterra and Deed | **confirmed** | 2026-03-05 (Orrick). |
| V7-07h TA owns Orion and Momentive | **partially_confirmed** | TA owns Momentive Software (the Community Brands carve-out, 2024-07). Orion is **co-owned with Genstar**, which has held an equal stake since 2020. |

## Exact corrections

### `research/mission-2026-11-14/queue-community-foundation-rails-portals.md`

1. **Line 84**
   - Current: "**Greater Washington CF (#38): Blackbaud REPAY**, live since September 2026."
   - Replace with: "**Greater Washington CF (#38): REPAY (payments partner, alongside Blackbaud Financial Edge NXT)**. GWCF says it 'partnered with Blackbaud and REPAY' in 'systems transformation upgrades completed in September 2026'."
2. **Line 90**
   - Current: "(Bill.com, Blackbaud REPAY, Citizens Checkmint)"
   - Replace with: "(Bill.com, REPAY, Citizens Checkmint)"
3. **Line 30**
   - Current: "**NPact Foundation Cloud (spectrumportal.net): 3**"
   - Replace with: "**Foundation Cloud on spectrumportal.net (NPact per third-party sources [R]): 3**"
   - Optionally add to line 111: "The GWCF sign-in page loads `payments.blackbaud.com/Checkout/bbCheckout.2.0.js` [F]."
4. **Line 29**
   - Current: "**2 are check-only:** Chicago Community Trust (DAF grants are mailed checks)"
   - Replace with: "**2 document checks only:** Chicago Community Trust (for DAF grants; discretionary-grant rail not documented)"
5. **Line 73 (SPMF row).** Append: "Chariot's own post (dated 'Sep 15', © 2026) says the move is expected 'with a few exceptions' ([Chariot](https://givechariot.com/resources/insights/enrolling-with-chariot-for-electronic-grant-payments-from-the-saint-paul--minnesota-foundation)) [V]. The year of 'this fall' is inferred from the footers."

### `research/mission-2026-11-14/queue-fidelity-chariot-goodstack-vanguard.md`

1. **Line 28**
   - Current: "Goodstack's donation rails run through its own DAF-style foundations."
   - Replace with: "Goodstack's donation rails run through partner foundations that its Donation Delivery Policy names as exclusive recipients. The US foundation describes itself as one of a 'stack of independent charitable foundations' that 'work with Goodstack, a technology company' ([giftall.org](https://www.giftall.org/))."
2. **Line 28**
   - Current: "reported **7,268 DAFs and $1.81m year-end DAF value for FY2024** [F]."
   - Replace with: "reported **7,268 DAFs and $1.81m year-end DAF value for FY2024**. Its FY2025 return (filed 2026-09-02) reports **$10,772,483 year-end DAF value, $11,582,483 DAF contributions, $1,660,000 DAF grants and 3 DAFs** (an apparent change in how accounts are counted), with total assets of $12,779,329 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602459349300235_public.xml)) [F]."
3. **Line 150**
   - Current: "**Goodstack runs DAF-style sponsors itself.**"
   - Replace with: "**Goodstack routes donations exclusively through affiliated DAF-style foundations, which present themselves as independent.**"
4. **Line 161.** After "revenue of $268,231", add: "CY2024 revenue was $3,116,428 and CY2025 revenue $16,344,032 (ProPublica)."
5. **Line 162**
   - Current: "Its DAF operation is minor in dollar terms."
   - Replace with: "Its DAF operation is small but grew about 6x in 2025 ($10.8m year-end DAF value)."
6. **Line 94 (agent row).** Append: "Note: the Terms do make Chariot itself the donor's authorized actor ('you hereby authorize Chariot to take the following actions on your behalf'). 'No agent clause' means no clause on third-party or AI agents."
7. **Line 27.** Add the privacy policy's effective date: "Privacy Policy effective 'Janurary 8th, 2025' (sic)."

### `research/mission-2026-11-14/private-equity-daf-ecosystem-map.md`

1. **Line 13**
   - Current: "Altruist backer)"
   - Replace with: "Altruist backer, led the 2023 Series D; Vanguard agreed to acquire Altruist on 2026-08-26, pending)"
2. **Line 17**
   - Current: "also took **25% of CAPTRUST** in 2020"
   - Replace with: "also took **25% of CAPTRUST** in 2020 and stayed a minority investor when Carlyle joined (2023-09-19; current stake undisclosed) ([CAPTRUST](https://www.captrust.com/carlyle-joins-gtcr-as-captrust-investor/))"
   - Apply the same change to line 175 ("CAPTRUST (25%)" → "CAPTRUST (25% in 2020)") and line 236 ("25% of CAPTRUST" → "a CAPTRUST minority stake (25% in 2020)").
3. **Line 18**
   - Current: "**General Atlantic** and **TPG** each hold both"
   - Replace with: "**General Atlantic** and **TPG** each hold both (Benevity stakes evidenced only at the 2020–21 Hg deal; TPG via The Rise Fund at Benevity and TPG Capital at Creative Planning)"
4. **Line 19**
   - Current: "**TA Associates** owns Orion"
   - Replace with: "**TA Associates** co-owns Orion with Genstar (equal stakes since 2020)"
   - Apply the same change to line 178 ("Orion; Momentive" → "Orion (with Genstar); Momentive").
5. **Line 24.** Append: "(historical facility; probably refinanced at GTCR's 2023 buyout, not a current lender)."

No correction is needed for Warburg/Bloomerang, Bain Capital Double Impact/FreeWill or Bonterra/Deed.

## Notes on recency
- Pre-2021 facts used only as history: Audax 2020, GTCR 2020 and the GA Creative Planning entry in 2020. For GA, the 2024 TPG release confirms it is still an investor.
- The Benevity GA and TPG legs have no evidence after 2021. Treat them as medium confidence until a 2024+ cap-table source is found.
