# Validation wave 6: bank programs, EFT providers, vendor and channel moves

**Date:** 2026-11-14. **Validator:** independent-validation-agent-wave6.
**Method:** For each claim I formed a verdict from primary sources first: live portals, sponsor PDFs, and IRS e-file XML fetched separately from the GivingTuesday data lake. Only then did I read `queue-bank-programs-and-eft-providers.md` and `queue-vendor-channel-moves.md`. I logged in nowhere, submitted no forms and contacted no one.
**Register:** [`data/mission-2026-11-14/validation-register-wave6.csv`](../../data/mission-2026-11-14/validation-register-wave6.csv) has 10 rows covering 9 claims. V6-09 is split by entity.

## Verdicts

| Claim | Result | Key point |
|---|---|---|
| V6-01 MS GIFT circular, rail, statements, outbound | **confirmed** | Aug 2024 circular is linked from the portal home page. Grants go to the "validated mailing address or banking details". The circular gives "viewing access" only and has no outbound clause. |
| V6-02 BofA CGF | **confirmed** (with an interpretation challenge) | Check only, by the 2024 guidelines, the 8/2024 sheet and the 9/2025 guide. The portal is Ren DonorFirst, with `charitablegiftfund@reninc.com` and `donations_cgf@reninc.com`. Excel export appears on the contribution listing only. The termination clause is quoted correctly. |
| V6-03 GS Philanthropy Fund | **partially_confirmed** | The "only public circular is 2008" claim is **wrong**. Circulars dated Nov 2012 and **Dec 5 2017** are also public on gspf.goldman.com, and all three say grants are paid by check. The donor web is iPhi by Stellar, and stellartechsol.com now redirects to reninc.com. |
| V6-04 GS Gives pays Stellar | **confirmed** | FY2024: $139,000. FY2025: $172,604. Both are "INFORMATION TECHNOLOGY", EIN 11-3813663. |
| V6-05 NCF eGrants and Salesforce | **partially_confirmed** | The quote, the eGrants enrolment and the Salesforce/Skuid login all check out. However, ncfgiving.com page data keys each office to an `iphiDonorWebId`, and NCF pays Stellar. |
| V6-06 PayPal, Chariot, AEF, check-only programs | **partially_confirmed** | NPT's $250k and Vanguard's $10M are confirmed. The Charityvest source says "transitioning" from Aug 2026, not "switched", and Charityvest's own guide still says PayPal. AEF ACH through Ren is confirmed. DAFgiving360's check-only rail rests on its 2024 policies. |
| V6-07 Commonwealth Charitable Fund | **confirmed** | The circular names RCF as sponsor and RenPSG as administrator. On 2026-11-14 the portal still showed `program_id 680` and the LPL legend. The circular is not linked from the portal home page. |
| V6-08 GiftingNetwork at FFTC and CCT, and Give at FFTC | **confirmed** (with an interpretation challenge) | Both portals say "Powered by GiftingNetwork". The CCT PDFs were created 2025-12-02. FFTC's CY2023 return pays Give Interactive $654,500. An older CCT guide **created 2024-02-06** also says GiftingNetwork. |
| V6-09 Fidelity outlier, Vanguard line, DAFgiving360 accounts | **confirmed** | The $430m outlier and "significant transfer activity" are quoted correctly. The Vanguard line is $480,068,133. DAFgiving360 accounts went from 112,188 to 128,497, up 14.54%. The table in the repo has two wrong "largest line" cells. |

## Exact corrections

### `research/mission-2026-11-14/queue-bank-programs-and-eft-providers.md`

1. **Line 38 (P-QCAL-04)**
   - Current: "**Goldman Sachs Philanthropy Fund (PWM):** the only public program document is a Program Circular **last revised August 2008**"
   - Replace with: "**Goldman Sachs Philanthropy Fund (PWM):** three Program Circulars are publicly retrievable from gspf.goldman.com, dated August 2008, November 2012 and **December 5, 2017** ([2017 circular](https://gspf.goldman.com/gspf/Portals/29/docs/2017.11%20GSPF%20Program%20Circular.pdf)) [F]. The latest public version is dated 2017. None is linked from the login page."
2. **Line 51**
   - Current: "**The only public Program Circular is dated 2008.**"
   - Replace with: "**The latest public Program Circular is dated December 5, 2017** (doc 9055278v.19). The 2008 ('Last Revised: August 2008') and November 2012 versions are also still served."
   - Apply the same change in §S1 of the source table (line 333) and add the 2017 circular as a new source row.
3. **Lines 40, 44, 260 and 298**
   - Current: "check, per the 2008 circular; the 2026 rail is unknown", "GS PF (2008)" and "The only terms date from 2008".
   - Replace with: "check, per the 2008, 2012 and 2017 circulars; the 2026 rail is unknown", "GS PF (2017 circular)" and "The latest public terms date from 2017".
4. **Lines 39 and 66 (footer)**
   - Current: "Its footer reads 'iPhi™ ::: Copyright © 2001 - 2026 Stellar Technology Solutions, LLC'" and "© 2001–2026".
   - Add: "The end year '2026' is the page's current-date label (`dnnCURRENTDATE`). The static meta copyright reads '2001-2010'. The Ren attribution rests on Stellar's ownership: stellartechsol.com now redirects to reninc.com."
5. **Line 210 (NCF)**
   - Current: "No Ren DFX or iPhi marker is visible."
   - Replace with: "The login HTML shows no Ren DFX or iPhi marker. However, ncfgiving.com's page data still carries an `iphiDonorWebId` field for every regional office, a legacy Stellar iPhi identifier. Together with the Stellar payment of $2.50m, this means a Ren-owned back-office dependency cannot be ruled out [I]."
6. **Line 157 (BofA termination)**
   - Keep the wording, and add: "The guidelines do not bar ordinary grants to another sponsor. 'Qualified Organization' covers 509(a)(1), (2) and (3) public charities, which includes national DAF sponsors. This clause is the only *explicit* DAF-to-DAF wording, not an exclusive permission [I]."
7. **Line 44 (Charityvest)**
   - Current: "Charityvest (from Aug 2026, replacing PayPal)"
   - Replace with: "Charityvest (transitioning from Aug 2026, per Chariot; Charityvest's own charity guide still describes PayPal Grant Payments)"

### `research/mission-2026-11-14/queue-vendor-channel-moves.md`

1. **Line 23 (P-PRC-04) and line 89 (CCT row)**
   - Current: "CCT's GiftingNetwork portal documents were created 2025-12-02, after Give's CCT production host (2025-06-11). This argues against an imminent Give cut-over at CCT [I]."
   - Replace with: "CCT's current GiftingNetwork portal documents were created 2025-12-02. An earlier CCT guide at `donorportal.cct.org/ma/docs/cct/DonorPortalUserGuide.pdf` (created 2024-02-06) already says 'Powered by The GiftingNetwork'. GiftingNetwork was therefore CCT's documented front end at least 16 months before Give's CCT production host (2025-06-11). The Dec 2025 refresh fits continued incumbency, not a new deployment [I]."
   - Line 89's third column: change "Whether it ran GiftingNetwork from day one is [U]" to "GiftingNetwork documented by 2024-02-06 [F]".
2. **Line 135 (table "Largest single Schedule I line")**
   - DAFgiving360 FY2024: replace "—" with "Johns Hopkins $517.4m".
   - Fidelity FY2024: replace "JHU $273.1m" with "Memorial Sloan-Kettering $219.7m".
   - Fidelity's FY2024 grant to JHU was $95.5m. The $273.1m is not in the filed FY2024 XML.
3. **Line 149**
   - Current: "The FY2024 maximum line is $273.1m"
   - Replace with: "The FY2024 maximum line is $219.7m (Memorial Sloan-Kettering)".
   - The conclusion still holds.
4. **Line 24, item (4)**
   - Current: "can only sit in its FY2025 Vanguard line"
   - Replace with: "most likely sits in its FY2025 Vanguard line. It is the only FY2025 Schedule I line of $430m or more, and no FY2024 line reaches that amount [I, strong]. The report does not name the recipient or say it was a DAF-to-DAF grant."
5. **Line 36 (sponsor confirmed)**
   - Add: "The circular is not linked from the portal home page, which links only the 2022 Donor User Guide."

## Issues found beyond the claims

- **GS PF:** a December 2017 circular exists. Use it in place of the 2008 text for any terms-based scoring (P-BNK-01, line 298). It changes the date but not the check rail.
- **NCF / Ren:** the `iphiDonorWebId` keys in NCF's site data support counting NCF as a Ren (Stellar) back-office customer edge of uncertain scope in A1.
- **Fidelity → NPT** was $346.8m in FY2025 (FY2024: $153.3m). This is a second large DAF-to-DAF line that the repo does not discuss.

## Sources (accessed 2026-11-14)

- [MS GIFT portal](https://msgift.donorfirstx.com/) · [circular](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf)
- [BofA 2024 guidelines](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf) · [BofA portal](https://bofa.donorfirst.org/) · [Navigating guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf) · [Making the Most](https://bofa.donorfirst.org/pdf/bofa/Making%20the%20Most%20of%20your%20CGF%20Account.pdf)
- [GSPF donor web](https://gspf.goldman.com/gspf/) · [2008 circular](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&tabid=111&mid=554&forcedownload=true) · [2012 circular](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=2PilKgnPYjA%3D&tabid=111&mid=554&forcedownload=true) · [2017 circular](https://gspf.goldman.com/gspf/Portals/29/docs/2017.11%20GSPF%20Program%20Circular.pdf)
- GS Gives XML: [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511119349301416_public.xml) · [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611249349302616_public.xml)
- NCF: [guide](https://www.ncfgiving.com/guide-to-giving-at-NCF) · [EFT sign-up](https://www.ncfgiving.com/eft-charity-sign-up/) · [support FAQ](https://www.ncfgiving.com/support) · [login](https://secure.ncfgiving.com/)
- [NPT guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) · [Vanguard release (NonProfit PRO copy)](https://nonprofitpro.com/article/vanguard-charitable-launches-electronic-granting-solution) · [Chariot on Charityvest](https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner) · [Charityvest guide](https://guide.charityvest.org/for-charities/overview) · [AEF charities](https://www.aefonline.org/charities/) · [DAFgiving360 2024 policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf)
- Commonwealth: [CFNDAF portal](https://cfndaf.donorfirstx.com/) · [circular](https://cfndaf.donorfirstx.com/pdf/CFNDAF/Program%20Circular.pdf)
- [FFTC portal](https://myfftc.org/) · [CCT portal](https://donorportal.cct.org/) · [CCT guide 2025](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-User-Guide.pdf) · [CCT guide 2024](https://donorportal.cct.org/ma/docs/cct/DonorPortalUserGuide.pdf) · [FFTC CY2023 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349318318_public.xml)
- [Fidelity 2025 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) · Fidelity XML [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml) / [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) · DAFgiving360 XML [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541069349300729_public.xml) / [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml)
