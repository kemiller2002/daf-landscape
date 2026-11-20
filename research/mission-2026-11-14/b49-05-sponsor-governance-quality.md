# b49-05: Financial-reporting and governance answers of DAF sponsors on Form 990, TY2022–2024

**Date:** 2026-11-20 · **Task:** b49-05 (new direction: sponsor governance quality)

**Outputs**
- [`data/mission-2026-11-14/sponsor-governance-quality-2026-11-20.csv`](../../data/mission-2026-11-14/sponsor-governance-quality-2026-11-20.csv) has 928 rows:
  - 449 `sponsor_year` rows;
  - 138 `schedule_l` rows;
  - 301 `band_item` rows;
  - 40 `comparison` rows.

  The data dictionary is in §7.
- [`data/mission-2026-11-14/queue-proposals-b49-05.csv`](../../data/mission-2026-11-14/queue-proposals-b49-05.csv) holds P-B4905-01 to -05.
- **Script:** [`scripts/mission_sponsor_governance.py`](../../scripts/mission_sponsor_governance.py) is new, uses only the standard library and is written in a functional style. It reuses:
  - from `mission_990_contractors`: the XML and CSV helpers;
  - from `mission_sponsor_compensation`: the DAFRC panel with applied corrections, the top-50 selection, the segment table, the tax-year rule and the TEOS fallback.

**Conventions**
- **TY** is the year in which the tax period begins (IRS convention).
- **Labels:** **[F]** means a value as filed. **[C]** means a script computation. **[I]** means an inference or classification.
- **Framing:**
  - Every answer here is **self-reported by the filer**. Many Part VI items cover practices that federal tax law does not require. The IRS instructions say: "Although federal tax law generally doesn't mandate particular management structures, operational policies, or administrative practices, every organization is required to answer each question in Part VI" ([i990](https://www.irs.gov/instructions/i990)).
  - A "No" is a description of what the filer reported. It is **not evidence of wrongdoing**, and this note does not imply any.
  - Schedule L transactions are disclosures the form asks for. Their presence is not a finding against anyone.
- **Names:**
  - Sponsors are named.
  - Individuals in Schedule L are not named. The CSV masks them as `[individual]`, and relationship and transaction text is reduced to categories.
- **Access:**
  - Before any fetch, robots.txt was read for each host and logged (§6.2).
  - 296 returns were parsed from XML files that earlier batches had already cached locally. 153 were streamed from the GivingTuesday S3 mirror.
  - No TEOS zip fetches were needed. No requests went to sec.gov. There were no logins, forms or contact.

---

## 0. Bottom line

1. **Coverage is complete [C].**
   - All 150 sponsors in the population filed a full Form 990 in each year: the top 50, plus a seeded random sample of 100 drawn from the 1,429 smaller DAFRC sponsors.
   - That gives 449 returns: TY2022 148, TY2023 150, TY2024 151. Ayco has two TY2024 periods after a fiscal-year change.
   - Every return parsed. No sampled sponsor was a 990-EZ-only filer.
2. **The top 50 report the standard policies almost universally. Missing policies are concentrated among the smallest sponsors [F/C].** These figures use the latest return (TY2024) for each sponsor.
   - **Audits:**
     - All 50 of the top 50 report audited financial statements and an audit committee.
     - In the < $10m DAF-asset band, 37 of 57 (64.9%) report an audit, 3 a compilation or review only, and 17 (29.8%) neither.
   - **Conflict-of-interest policy:** 50/50 in the top 50 against 49/57 (86.0%) in the < $10m band. All 8 sponsors answering "No" are sampled sponsors with < $10m.
   - **Whistleblower policy:** 49/50 against 40/57 (70.2%). Of the 18 "No" answers, 17 come from < $10m sampled sponsors. The one top-50 "No" is American Gift Fund.
   - **Document-retention policy:** 49/50 against 44/57 (77.2%). Of the 14 "No" answers, 13 come from < $10m sampled sponsors; the other is American Gift Fund.
3. **Two questions run the other way: the top 50 answer "No" more often than mid-sized sponsors [F/C].**
   - **Line 11a**, a complete copy of the 990 provided to every voting board member before filing:
     - 41/50 in the top 50 (82%) and 23/30 in the ≥ $1bn band (76.7%) answer "Yes";
     - the $10m–$1bn bands answer "Yes" at 90–94%.
     - Several "No" filers describe a board, committee or emailed-copy review on Schedule O (§3.2). Line 11a counts only a complete copy given to every voting member, so these answers are not in conflict.
   - **Line 15a**, a documented process for setting the top official's pay:
     - 38 of 49 top-50 sponsors answer "Yes". Fidelity Charitable leaves 15a and 15b blank in all three years.
     - **All 11 top-50 sponsors answering "No" report zero employees on Part I line 5** [F]. Examples are GS DAPF, Morgan Stanley GIFT, BofA, Raymond James, Ayco and T. Rowe Price.
     - The instructions count only a process that "the organization (not a related organization or other third party) used". Affiliate-staffed sponsors therefore answer "No" by construction [I].
4. **Excess-benefit transactions are rare and disclosed [F].**
   - Two of 150 sponsors answer "Yes" to Part IV 25a: National Philanthropic Trust (TY2022–2024) and Servant Foundation (TY2022).
   - **NPT's** Schedule L describes de minimis compensation that a third-party investment manager paid to financial advisers connected to DAFs. In TY2024 it was $131.58 for one adviser. NPT reports it as corrected, with repayment plus interest. The section 4958 tax reported on Schedule L line 2 is $439, $473 and $34 for TY2022–2024.
   - **Servant Foundation** reports two donor-advisor transactions "subject to the tax pursuant to IRC section 4958(c)(2)", with $6,494 of tax reported. Both Part I rows are filed with “transaction corrected” = No. [V wave 49A]
5. **Schedule L [F].**
   - 20 of 150 sponsors (11 top-50, 9 sampled) filed Schedule L in at least one year, giving 138 rows.
   - **At commercially affiliated nationals, the large items are the founder's administration contracts:**
     - DAFgiving360 with Charles Schwab & Co: $11.4m in TY2024;
     - Renaissance: $19.2m, paid to Renaissance Administration LLC; the filed relationship is a shared officer (“An officer of RCF is also an officer of Renaissance Administration LLC”), not the founder; [V wave 49A]
     - Raymond James: $14.5m;
     - Vanguard Charitable: $4.0m;
     - US Charitable Gift Trust with three Eaton Vance entities: $7.7m in TY2022.
   - **Elsewhere:**
     - Stanford, a university filer, reports loans to officers and a trustee, plus compensation rows whose relationship it describes in Schedule L Part V;
     - Servant Foundation reports family-member employment;
     - The Signatry reports loans from, and a share sale with, a substantial contributor;
     - small community foundations report board members' firms providing insurance, investment management or legal services.
6. **Link to the compensation and resilience directions [C/I].** Among the top 50:
   - The 9 sponsors whose top officer shows $0 on the 990 (per the compensation direction) all report COI, whistleblower and retention policies and audits. 6 of the 8 that answered 15a said "No".
   - The 5 sponsors whose non-DAF net assets are ≤ 0 (R1 ≤ 0 in the resilience direction) also all report audits, audit committees and COI policies. These are Greater Horizons, NPT, Renaissance, American Gift Fund and Morgan Stanley GIFT.
   - So the governance checklist does not separate the sponsors that the resilience work flags as thin.

---

## 1. Method

### 1.1 Population
- **Top 50:** the 50 largest sponsors by FY2024 end-of-year DAF assets in `dafrc-sponsor-schedule-d-fy2019-2024.csv`, after applied corrections in `dafrc-corrections-itemized.csv` (`applied = 1`). The code is the same as the compensation direction (`top_sponsors`). The smallest top-50 sponsor holds $581m.
- **Sample:**
  - **Frame:** every FY2024 DAFRC row ranked 51 or lower with corrected DAF assets > 0, giving 1,429 EINs. The EINs were sorted, then `random.Random(4905).sample(frame, 100)` was drawn.
  - **Sampled sponsors** range from rank 53 to rank 1,455 and from $13,550 to $536.8m of DAF assets.
  - **By DAFRC type:** 61 community foundations, 34 single-issue charities and 5 nationals.
- **Size bands:** FY2024 corrected DAF assets, fixed before any answers were read:

  | Band | DAF assets | Sponsors (top 50 + sample) |
  |---|---|---|
  | A | ≥ $1bn | 30 (30 + 0) |
  | B | $100m–$1bn | 32 (20 + 12) |
  | C | $10m–$100m | 31 (0 + 31) |
  | D | < $10m | 57 (0 + 57) |

### 1.2 Returns
- Every `RETURN_TYPE = 990` row for the 150 EINs in IRS `index_2023`–`index_2026` was taken, keeping tax years 2022–2024.
  - The index files are local copies from 2026-11-14; index_2026 was refreshed on 2026-11-15.
- Where several submissions exist for one EIN × tax period, the highest OBJECT_ID was kept, so amendments are picked up.
- The script also scans for 990-EZ and 990-PF rows. None was needed, because all 150 sponsors filed a full 990.

### 1.3 Fields read from each return
| Area | Form reference | XML element(s) |
|---|---|---|
| Accounting method | Part XII line 1 | `MethodOfAccountingCashInd` / `AccrualInd` / `OtherInd` (+ description) |
| Compiled or reviewed / audited / audit committee | Part XII 2a / 2b / 2c (+ basis) | `AccountantCompileOrReviewInd`, `FSAuditedInd`, `AuditCommitteeInd`, `*BasisGrp` |
| Single Audit | Part XII 3a / 3b | `FederalGrantAuditRequiredInd`, `FederalGrantAuditPerformedInd` |
| Voting and independent members | Part VI 1a / 1b | `GoverningBodyVotingMembersCnt`, `IndependentVotingMemberCnt` |
| Structure | Part VI 2–8 | family/business relationships, delegation of management, document changes, diversion, members or stockholders (6), members elect (7a) or approve (7b), minutes (8a/8b) |
| 990 provided to the board | Part VI 11a | `Form990ProvidedToGvrnBodyInd`; the 11b process text comes from Schedule O |
| COI policy, annual disclosure, monitoring | Part VI 12a / b / c | `ConflictOfInterestPolicyInd`, `AnnualDisclosureCoveredPrsnInd`, `RegularMonitoringEnfrcInd` |
| Whistleblower / document retention | Part VI 13 / 14 | `WhistleblowerPolicyInd`, `DocumentRetentionPolicyInd` |
| Compensation process | Part VI 15a / 15b | `CompensationProcessCEOInd`, `CompensationProcessOtherInd` |
| Employees and volunteers | Part I lines 5 and 6; Part V 2a | `TotalEmployeeCnt`, `TotalVolunteersCnt`, `EmployeeCnt` |
| Interested-person transactions | Part IV 25a–28c | `EngagedInExcessBenefitTransInd` … `BusinessRlnWith35CtrlEntInd` |
| Schedule L | Parts I–IV, line 2 tax | `DisqualifiedPersonExBnftTrGrp`, `LoansBtwnOrgInterestedPrsnGrp`, `GrntAsstBnftInterestedPrsnGrp`, `BusTrInvolveInterestedPrsnGrp`, `TaxImposedAmt` |
| Schedule O | any entry that cites a Part VI or XII line, or names COI, whistleblower or retention policies | `SupplementalInformationDetail` |

- **Prevalence** (§3) uses each sponsor's latest return. That is TY2024 for all 150.
- **Year-to-year changes** (§3.5) use all 449 returns.
- **Comparison columns:** these are joined by EIN × TY:
  - `ctx_comp_*` from `sponsor-executive-compensation-2021-2025.csv` (`record_type = sponsor_year`);
  - `ctx_res_*` from `sponsor-financial-resilience-2021-2024.csv` (`row_type = sponsor_year`).

### 1.4 Reproduce
```
python3 scripts/mission_sponsor_governance.py . --irs-dir <dir with index_2023..2026.csv> \
    --work-dir <cache dir> --xml-cache <dir(s) holding {object_id}[_public].xml> [--fetch]
```

---

## 2. Coverage

| | Sponsors | Returns TY2022 | TY2023 | TY2024 | Parse failures | No full 990 |
|---|---|---|---|---|---|---|
| Top 50 | 50 | 50 | 50 | 51 | 0 | 0 |
| Sample | 100 | 98 | 100 | 100 | 0 | 0 |

- Two sampled sponsors have no TY2022 990 in the index: Brighter Days Horse Refuge and FBT for a Brighter Tomorrow.
- Ayco filed a calendar 2024 return and a short or changed-year return ending 2025-06. Both count as TY2024; the later one is used as "latest".

---

## 3. Results

### 3.1 Prevalence by size band (latest return, TY2024) [F/C]

- **Cell format:** "Yes / answered (%)". Category rows use the share of all sponsors in the band.
- **Answered counts:**
  - Line 2c is asked only when 2a or 2b is "Yes".
  - Lines 12b and 12c are asked only when 12a is "Yes".
  - Fidelity Charitable left 15a and 15b blank.

| Item | All (150) | Top 50 | Sample (100) | ≥ $1bn (30) | $100m–1bn (32) | $10m–100m (31) | < $10m (57) |
|---|---|---|---|---|---|---|---|
| Accrual method (XII 1) | 132/150 (88.0%) | 48/50 (96%) | 84/100 (84%) | 28/30 (93.3%) | 32/32 (100%) | 28/31 (90.3%) | 44/57 (77.2%) |
| Cash method | 17/150 (11.3%) | 2/50 (4%) | 15/100 (15%) | 2/30 (6.7%) | 0/32 | 3/31 (9.7%) | 12/57 (21.1%) |
| Other method | 1/150 | 0 | 1 | 0 | 0 | 0 | 1/57 ("Modified cash") |
| Audited (XII 2b) | 128/150 (85.3%) | 50/50 (100%) | 78/100 (78%) | 30/30 (100%) | 32/32 (100%) | 29/31 (93.5%) | 37/57 (64.9%) |
| Compiled or reviewed only (2a = Y, 2b = N) | 3/150 (2.0%) | 0 | 3 | 0 | 0 | 0 | 3/57 (5.3%) |
| Neither | 19/150 (12.7%) | 0 | 19 | 0 | 0 | 2/31 (6.5%) | 17/57 (29.8%) |
| Audit committee (XII 2c) | 127/131 (96.9%) | 50/50 | 77/81 (95.1%) | 30/30 | 32/32 | 29/30 (96.7%) | 36/39 (92.3%) |
| Single Audit required (XII 3a) | 12/147 (8.2%) | 5/49 | 7/98 | 1/29 | 5/32 | 4/31 | 2/55 |
| Family or business relationship among officers/directors (VI 2) | 28/150 (18.7%) | 11/50 (22%) | 17/100 (17%) | 6/30 | 6/32 | 5/31 | 11/57 |
| Management delegated to a management company (VI 3) | 9/150 (6.0%) | 6/50 (12%) | 3/100 (3%) | 5/30 (16.7%) | 2/32 | 0/31 | 2/57 |
| Members or stockholders (VI 6) | 11/150 (7.3%) | 2/50 (4%) | 9/100 (9%) | 1/30 | 2/32 | 3/31 | 5/57 |
| Members elect board (VI 7a) | 22/150 (14.7%) | 6/50 | 16/100 | 4/30 | 3/32 | 5/31 | 10/57 |
| Minutes of board (VI 8a) | 150/150 (100%) | 50/50 | 100/100 | 30/30 | 32/32 | 31/31 | 57/57 |
| Minutes of committees (VI 8b) | 135/150 (90.0%) | 45/50 | 90/100 | 26/30 | 29/32 | 30/31 | 50/57 |
| Complete 990 to every voting member before filing (VI 11a) | 133/150 (88.7%) | 41/50 (82%) | 92/100 (92%) | 23/30 (76.7%) | 30/32 (93.8%) | 28/31 (90.3%) | 52/57 (91.2%) |
| COI policy (VI 12a) | 142/150 (94.7%) | 50/50 (100%) | 92/100 (92%) | 30/30 | 32/32 | 31/31 | 49/57 (86.0%) |
| COI annual disclosure (12b) | 139/142 (97.9%) | 50/50 | 89/92 | 30/30 | 32/32 | 31/31 | 46/49 (93.9%) |
| COI regular monitoring (12c) | 140/142 (98.6%) | 50/50 | 90/92 | 30/30 | 32/32 | 31/31 | 47/49 (95.9%) |
| Whistleblower policy (VI 13) | 132/150 (88.0%) | 49/50 (98%) | 83/100 (83%) | 30/30 | 31/32 (96.9%) | 31/31 | 40/57 (70.2%) |
| Document-retention policy (VI 14) | 136/150 (90.7%) | 49/50 (98%) | 87/100 (87%) | 30/30 | 31/32 (96.9%) | 31/31 | 44/57 (77.2%) |
| Compensation process, top official (VI 15a) | 108/149 (72.5%) | 38/49 (77.6%) | 70/100 (70%) | 22/29 (75.9%) | 25/32 (78.1%) | 29/31 (93.5%) | 32/57 (56.1%) |
| Compensation process, other officers (VI 15b) | 80/149 (53.7%) | 34/49 (69.4%) | 46/100 (46%) | 19/29 (65.5%) | 22/32 (68.8%) | 18/31 (58.1%) | 21/57 (36.8%) |
| Joint venture (VI 16a) | 5/150 (3.3%) | 3/50 | 2/100 | 3/30 | 1/32 | 0/31 | 1/57 |

| Median (n; count of zeros) | All | Top 50 | Sample | ≥ $1bn | $100m–1bn | $10m–100m | < $10m |
|---|---|---|---|---|---|---|---|
| Voting members (VI 1a) | 13.5 (150; 1) | 13.5 (50; 1) | 13.5 (100; 0) | 9.5 (30; 0) | 17 (32; 1) | 15 (31; 0) | 11 (57; 0) |
| Independent members (VI 1b) | 13 (150; 4) | 13.5 (50; 1) | 13 (100; 3) | 9 (30; 0) | 17 (32; 1) | 15 (31; 0) | 11 (57; 3) |
| Independent ÷ voting | 1.0 (149; 3) | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 (57; 3) |
| Employees (Part I line 5) | 7 (150; 41) | 70 (50; 15) | 6 (100; 26) | 86 (30; 10) | 43 (32; 8) | 7 (31; 2) | 3 (57; 21) |
| Volunteers (Part I line 6) | 21 (139; 27) | 19 (49; 14) | 25.5 (90; 13) | 7 (29; 11) | 30.5 (32; 4) | 35 (31; 3) | 19 (47; 9) |

**Reading the tables [I]**
- **Independence:**
  - Independence is high nearly everywhere. The median sponsor reports every voting member as independent.
  - Bessemer Giving Fund reports 0 voting members (it is a trust with an institutional trustee).
  - ImpactAssets reports 1 independent member of 6.
  - Four small sampled sponsors report a minority of independent members: Sertoma, Pleasant Hill CF, LegacyTree and Brighter Days.
- **Volunteers:** 11 latest returns leave line 6 blank. The instructions allow a "reasonable estimate", so volunteer counts are not comparable across filers.
- **Employees:** 15 of the top 50 report zero employees. They are BofA, Fidelity Charitable, Bessemer, Ayco, Greater Horizons, Dechomai, US Charitable Gift Trust, T. Rowe Price, GS DAPF, Renaissance, American Gift Fund, Morgan Stanley GIFT, Raymond James, The Signatry and UCLA Foundation. UCLA Foundation's staff are "employees of the Regents of University of California" according to Schedule O.

### 3.2 Sponsors that answer "No" to key policies (latest return, TY2024) [F]

The history column shows the answer for TY2022, TY2023 and TY2024 in order.

**Conflict-of-interest policy (12a = No), 8 sponsors, all sampled with < $10m DAF assets; history NNN unless shown:**
- Commonwealth Charitable Management
- Manifold for Charity
- The Peoples Heartland Foundation
- Bloomington Community Foundation
- Eastmont Community Foundation
- Marion Area Community Foundation
- The Pleasant Hill Community Foundation
- Brighter Days Horse Refuge (NN)

**Whistleblower policy (13 = No), 18 sponsors:**
- **Top 50:** American Gift Fund (NNN).
- **Sample, all < $10m:**
  - University of the Philippines Medical Alumni (foundation)
  - CF of Greater Rome
  - Rice County CF
  - FBT for a Brighter Tomorrow
  - Jewish Community Foundation of NM
  - Manifold for Charity
  - Peoples Heartland
  - Sertoma
  - Bloomington CF
  - Eastmont CF
  - Marion Area CF
  - Park County CF
  - Grace Commons Foundation
  - St Croix Foundation for Community
  - Pleasant Hill CF
  - Social Good Fund
  - Brighter Days Horse Refuge

**Document-retention policy (14 = No), 14 sponsors:**
- **Top 50:** American Gift Fund.
- **Sample, all < $10m:**
  - The Community Foundation of the Northern (name truncated in source)
  - University of the Philippines Medical Alumni
  - CF of Greater Rome
  - FBT for a Brighter Tomorrow
  - JCF of NM
  - Manifold for Charity
  - Peoples Heartland
  - Bloomington CF
  - Eastmont CF
  - Marion Area CF
  - Park County CF
  - Grace Commons
  - Brighter Days

**Complete 990 to every voting member before filing (11a = No), 17 sponsors:**
- **Top 50 (9):**
  - Renaissance
  - BofA Charitable Gift Fund
  - ImpactAssets
  - Foundation For The Carolinas
  - Donors Trust
  - Oregon Community Foundation
  - Boston Foundation
  - JCF of Los Angeles
  - "Community Foundation" (EIN in CSV, rank 41)
- **Sample (8):**
  - Madison CF
  - a Jewish Community Foundation ranked 229
  - Jewish Federation of Nashville
  - FBT for a Brighter Tomorrow
  - Peoples Heartland
  - Eastmont CF
  - Michigan Foundation for Agriculture
  - St Croix Foundation

**Schedule O line 11b texts filed by some of these sponsors [F]:**
- **Foundation For The Carolinas:** "an electronic copy of the final return is sent to each voting member prior to an upcoming board meeting and prior to filing."
- **Madison CF:** "a copy of the final Form 990 (excluding Schedule B and the detail listing of Schedule I) is made available to each member of the Board of Governors prior to filing."
- **Rank-41 Community Foundation:** "distributes the public disclosure copy of the Form 990 to its directors via email prior to filing."
- **JCF of Los Angeles:** "The Public Inspection Copy is then provided to the entire Board for their review and comment prior to signing."
- **Donors Trust:** the 990 "is distributed to all board members after filing."
- **BofA:** "Tax department prepares, reviews and files the Form 990."
- **Renaissance:** the parser found no line 11b entry.

**Why these are not contradictions [I].** Line 11a is "Yes" only if a *complete* copy, including all schedules as filed, reached every voting member *before* filing. Several "No" filers therefore describe a public-disclosure-copy, committee or post-filing review on Schedule O.

**Compensation process for the top official (15a = No):**
- **Top 50 (11):**
  - GS DAPF
  - Morgan Stanley GIFT
  - BofA
  - Greater Horizons
  - Raymond James (YYN)
  - Dechomai
  - Ayco
  - Bessemer
  - The Signatry
  - UCLA Foundation
  - T. Rowe Price
- **Sample:** 30 of 100 sponsors answer "No". Individual names are in the CSV.

**Schedule O explanations of "No" answers [C].**
- Across the 167 "No" answers on the six key items in latest returns (12a, 13, 14, 11a, 15a, 15b), only 12 have a Schedule O entry that cites that line or names that policy.
- The form requires a Schedule O explanation for some "No" answers, such as 8a/8b and 10b. It does not require one for 12a, 13 or 14.
- Examples of explanations that were filed:
  - **BofA (15a):** "Not applicable, trust has corporate trustee."
  - **Bessemer (15):** "The organization does not have policies regarding compensation as it has no employees…"
  - **UCLA Foundation (15a & b):** staff "are employees of the Regents of University of California and receive salary and benefits from the University."

### 3.3 Financial reporting [F]
- **Top 50:**
  - Accounting method: 48 accrual; 2 cash (BofA Charitable Gift Fund and Dechomai Asset Trust).
  - All 50 report audited statements in TY2024.
  - In earlier years, American Gift Fund (TY2022–2023) and National Christian Charitable Foundation (TY2022) answered 2b = "No". The instructions require "No" when the organisation was covered only by consolidated audited statements, so these answers do not by themselves mean "no audit" (P-B4905-02).
- **Sample:** 22 of 100 report no separate audit in TY2024. 19 report neither an audit nor a compilation or review; 3 report a compilation or review only. Of the 22, 20 have < $10m of DAF assets. The other two are First Midwest Charitable Trust ($13.5m) and Jewish Federation of Nashville ($15.0m).

### 3.4 Part IV and Schedule L [F]

**Part IV "Yes" answers (any year TY2022–2024, return count):**

| Line | Returns | Sponsors |
|---|---|---|
| 25a excess benefit, current year | 4 | NPT (3), Servant Foundation (1) |
| 25b prior-year excess benefit not reported | 4 | NPT (3), Servant Foundation (1) |
| 26 loans to/from interested persons | 9 | Renaissance, SVCF, Stanford, The Signatry |
| 27 grants to interested persons | 5 | Gulf Coast CF, Manifold for Charity, Schenectady Foundation |
| 28a business transaction with officer/director | 16 | Believers Stewardship, Central Pennsylvania CF, Raymond James, Renaissance, The Signatry, Tulsa CF, Vanguard Charitable |
| 28b with family member | 7 | Servant Foundation, Stanford, The Signatry |
| 28c with 35%-controlled entity | 20 | Believers Stewardship, Central Pennsylvania CF, Charitable Gift America, Civic Nebraska, DAFgiving360, GiveClear, Schenectady Foundation, US Charitable Gift Trust, Tulsa CF, Univest Foundation |

**Schedule L rows in the latest return (TY2024)**, 16 sponsors. Relationship and transaction labels are script categories [I]:

| Sponsor (rank) | Part / relationship / transaction | TY2024 amount |
|---|---|---|
| National Philanthropic Trust (2) | I / family member of a donor / excess benefit (4958) | not stated in Part I (Part V text: $131.58) |
| DAFgiving360 (3) | IV / founder (Charles Schwab & Co) / brokerage & administrative services | $11,431,175 |
| Vanguard Charitable (4) | IV / founder; affiliate / occupancy & admin; broker commissions | $4,017,439 |
| Silicon Valley CF (6) | II / employee / loan | $500,000 original principal |
| Renaissance (9) | IV / officer / administration services | $19,225,546 |
| Raymond James (19) | IV / founder / admin services & investment management | $14,501,160 |
| Servant Foundation (30) | IV / family members of board members / employee compensation | $198,351 (2 rows) |
| Tulsa CF (40) | IV / trustee / professional services | $72,957 |
| Stanford (42) | II / officers (10) and a trustee (1) / loans; IV / compensation (7) | $4,155,534 loans; $1,782,096 compensation |
| Gulf Coast CF (136) | III / board member; officer / grants | $569,117 |
| Central Pennsylvania CF (474) | IV / board members' firms / investment-management, insurance and legal fees paid; administrative fees received from a scholarship fund | $81,028 |
| Believers Stewardship (492) | IV / founder; controlled entity / compensation; advisory fees | $145,353 |
| Univest Foundation (658) | IV / officer / investment services provided by Univest Corporation or a subsidiary | amount not stated |
| Charitable Gift America (927) | IV / director-owned entity / administrative fees | $480,000 |
| Civic Nebraska (1180) | IV / board member's firm / legislative services | $25,000 |
| Schenectady Foundation (1207) | III / supporting organisation / operating grant; IV / officer / banking | $681,399 |

**Excess-benefit detail (Schedule L Part V text, paraphrased; individuals not named):**
- **NPT, TY2024 return** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml)):
  - In FY2023 NPT "discovered and reported" an excess-benefit transaction. A DAF donor who was a Wells Fargo financial adviser received de minimis compensation from his employer in connection with the investment management of his DAF's assets.
  - A follow-up investigation found four more in FY2024 and a fifth in FY2025.
  - The TY2024 case was $131.58 paid between November 2024 and September 2025. It was repaid with interest (total $137.03). The filing describes each case as "corrected as of the date of filing".
- **Servant Foundation, TY2022 return** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202410409349300211_public.xml)): two Part I rows, each with relationship "donor advisor" and the description "a transaction occurred with the disqualified person … that was subject to the tax pursuant to IRC section 4958(c)(2)". Schedule L line 2 reports $6,494 of tax.

### 3.5 Stability across TY2022–2024 [C]
- **No change at all:** no sponsor changed its answer on 12a (COI) or line 6 (members).
- **Policy answers:** 2 sponsors changed on 13 (whistleblower), 4 on 14 (document retention), 2 on 11a, 5 on 15a and 5 on 15b.
- **Audit status (2b):** 13 sponsors changed. 11 ended at "Yes" in TY2024 and 2 at "No" (CF of the Northern…, Jewish Federation of Nashville).
- **All 150 sponsors, by year:**

  | Item | TY2022 | TY2023 | TY2024 |
  |---|---|---|---|
  | COI policy | 141/148 | 142/150 | 143/151 |
  | Whistleblower | 130/148 | 132/150 | 133/151 |
  | Document retention | 132/148 | 135/150 | 137/151 |
  | Audited | 119/148 | 123/150 | 129/151 |

---

## 4. Comparison with the compensation and resilience directions [C/I]

The `comparison` rows cover the top 50 and use TY2024.

| Top-50 subgroup | n | 15a Yes / No | 15b Yes / No | COI Yes | Whistle Yes | Retention Yes | Audited | Audit committee | VI 3 delegated (Yes) |
|---|---|---|---|---|---|---|---|---|---|
| Top officer paid by sponsor (> $0, compensation CSV) | 38 | 35 / 3 | 32 / 6 | 38 | 38 | 38 | 38 | 38 | 1 |
| Top officer $0 on 990 | 9 | 2 / 6 | 1 / 7 | 9 | 9 | 9 | 9 | 9 | 5 |
| Zero employees (Part I 5) | 15 | 3 / 11 | 2 / 12 | 15 | 14 | 14 | 15 | 15 | 5 |
| R1 ≤ 0 (resilience CSV) | 5 | 3 / 2 | 1 / 4 | 5 | 4 | 4 | 5 | 5 | 1 |
| R1 > 0 | 45 | 35 / 9 | 33 / 11 | 45 | 45 | 45 | 45 | 45 | 5 |

- **Compensation direction** ([direction-sponsor-executive-compensation.md](direction-sponsor-executive-compensation.md) §0) found that most affiliated-commercial sponsors carry no executive pay on their own 990.
  - The governance answers line up with that. The sponsors with $0 top officers or zero employees are the ones answering "No" to 15a/15b and "Yes" to line 3 (management delegated to a management company). Line 3 "Yes" filers are Fidelity Charitable, Dechomai, US Charitable Gift Trust, Renaissance, Thrivent and Raymond James.
  - Their Schedule L entries show the matching founder-firm administration contracts (§3.4).
  - The three sponsors that pay a top officer yet answer 15a "No" are Greater Horizons, The Signatry and UCLA Foundation. The compensation CSV flags all three as `top_officer_paid_by_related_org` [F/C].
  - The 9 "top officer $0" and 38 "paid" counts come from 47 sponsors. BofA, Bessemer and American Gift Fund list only an institutional trustee and have a blank compensation total.
- **Resilience direction** ([direction-sponsor-financial-resilience.md](direction-sponsor-financial-resilience.md) §0) found that R1 (non-DAF net assets) is ≤ 0 at several nationals.
  - The 5 top-50 sponsors with R1 ≤ 0 in TY2024 are Greater Horizons, NPT, Renaissance, American Gift Fund and Morgan Stanley GIFT. Every one reports audited statements, an audit committee and a COI policy.
  - Their "No" answers are the affiliate-staffing pattern: 15a "No" at Greater Horizons and Morgan Stanley GIFT; 11a "No" at Renaissance. The one exception is American Gift Fund's "No" on 13 and 14.
  - **[I]** The Part VI and XII checklist does not discriminate on balance-sheet thinness among large sponsors, because nearly all of them tick every box. A governance-quality score built on these answers would mostly separate the smallest sponsors from the rest.

---

## 5. Limits
1. **Self-reported answers:**
   - Part VI and XII answers are the filer's own and are not verified by the IRS or by this script.
   - "Yes" says nothing about the quality of a policy. "No" does not mean a practice is absent; it can mean the policy is not adopted organisation-wide, or that a related organisation runs it.
2. **Definitions cut against affiliate-staffed sponsors:**
   - 15a counts only a process the filing organisation itself used.
   - 2b counts only a separate audit.
   - 11a counts only a complete pre-filing copy given to every voting member.
   - Commercial-affiliate and consolidated filers therefore answer "No" by construction (§3.2, §3.3).
3. **Sample size:** 100 sampled sponsors. Band C has 31 and band D has 57; no confidence intervals are given. The sample is a simple random draw from DAFRC FY2024 rows. It is not stratified, so it over-represents sponsors with < $10m (P-B4905-01).
4. **Band B mixes groups:** it holds 20 top-50 and 12 sampled sponsors. The "Top 50" and "Sample" columns keep the groups apart.
5. **Schedule O matching:**
   - The script uses regular expressions on `FormAndLineReferenceDesc` (e.g. "PART VI, SECTION B, LINE 15A") plus policy keywords in the text.
   - Filers that cite a line in free text without a reference are missed. "LINE 11-DESCRIPTION" style references are read as line 11 and so count for 11a.
   - Text is truncated to 700 characters in extracts and 900 in the CSV.
6. **Schedule L categories:**
   - Relationship and transaction categories come from keyword rules [I] and can misclassify. For example, the US Charitable Gift Trust rows say only "See Part V below" and are `other_or_unstated`.
   - Names are masked unless the filer typed an organisation name (an org word such as INC, LLC, CO or GROUP appears and no person cue appears). A few business names, such as a law firm named after its partners, are therefore masked. Organisation names that filers typed into Schedule L’s person-name field are also masked and labelled `individual`: the validator found 18 such Part I–IV rows (for example The Vanguard Group Inc, Renaissance Administration LLC and Raymond James Trust NA), so `sl_name_type = individual` overstates rows about natural persons. No natural person’s name appears in the CSV or this note. [V wave 49A]
   - Loan amounts are original principal and repeat across years. Do not sum them across years.
7. **University and federation filers:** Stanford and UCLA Foundation answer for the whole institution, not a DAF programme.
8. **Index vintage:** the index_2026 copy is from 2026-11-15. Late-filed or amended TY2024 returns after that date are not included.

---

## 6. Source register and access log

### 6.1 Sources
| Source | URL | Use |
|---|---|---|
| DAFRC Annual DAF Report 2025 – Updated Analysis dataset (via repo CSV) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Population, FY2024 DAF assets, types |
| IRS Form 990 e-file indexes | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv (likewise 2023–2025) | Return selection (local copies) |
| GivingTuesday 990 data lake mirror (per-return XML) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml (object IDs in CSV `object_id`; e.g. [NPT TY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml), [Fidelity Charitable TY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml), [Servant Foundation TY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202410409349300211_public.xml)) | All field values |
| IRS Instructions for Form 990 (2024) | https://www.irs.gov/instructions/i990 | Definitions of lines 11a, 11b, 15, 2b, 1b, Part I line 6; Part VI preamble quote |
| Repo: compensation direction | [direction-sponsor-executive-compensation.md](direction-sponsor-executive-compensation.md); `data/mission-2026-11-14/sponsor-executive-compensation-2021-2025.csv` | `ctx_comp_*` columns, segment table |
| Repo: resilience direction | [direction-sponsor-financial-resilience.md](direction-sponsor-financial-resilience.md); `data/mission-2026-11-14/sponsor-financial-resilience-2021-2024.csv` | `ctx_res_*` columns |

### 6.2 robots.txt log (checked 2026-11-20, user agent `research-script/1.0`)
| Host | Result | Action |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 NoSuchKey (no robots file) | Allowed; 153 XML GETs, plus 2 re-reads of Schedule L text |
| apps.irs.gov | 302 to www.irs.gov/404 (no robots file) | No requests made; local index copies used; TEOS fallback not triggered |
| www.irs.gov | 200. No group for ClaudeBot, anthropic-ai, Claude-User, Claude-Web or Claude-SearchBot. `*` disallows only search, admin and user paths | Fetched /instructions/i990 once |
| sec.gov | not contacted | per task |

---

## 7. Data dictionary: `sponsor-governance-quality-2026-11-20.csv`

The `record_type` column separates five row kinds.

### 7.1 Every row type
| Column | Meaning |
|---|---|
| `record_type` | `sponsor_year` (one per return), `no_full_990` (none in this run), `schedule_l` (one per Schedule L Part I–IV row), `band_item` (prevalence by group or band, latest return), `comparison` (top-50 cross-tabs, §4) |
| `ein`, `sponsor_name`, `group` | Identity; `group` = `top50` or `sample` |
| `rank_fy2024`, `fy2024_daf_assets`, `size_band` | DAFRC FY2024 rank and corrected DAF assets; band A–D (§1.1) |
| `dafrc_type`, `dafrc_subtype`, `segment` | DAFRC classification; segment from the compensation direction table (community_foundation, affiliated_commercial, …) |
| `frame_size` | Sampling-frame size (1,429), sample rows only |

### 7.2 `sponsor_year` rows
| Column | Meaning |
|---|---|
| `tax_year`, `tax_period`, `object_id`, `index_year` | Return identity (TY = year the period begins) |
| `xml_status`, `xml_source` | `ok`; mirror URL (prefixed `local_cache:` when read from a cached copy of that URL) |
| `amended` | Return header amended flag (Y/N/blank) |
| `total_assets_eoy`, `total_expenses` | Part X line 16 (EOY); Part I line 18 (current year) |
| `xii_1_method`, `xii_1_other_desc` | cash / accrual / other (pipe-joined if several boxes) |
| `assurance_level` | audited (2b = Y); compiled_or_reviewed (2a = Y, 2b = N); none_reported (2b = N, 2a = N) |
| `xii_2a_basis`, `xii_2b_basis` | separate / consolidated / both |
| `xii_*`, `vi_*`, `iv_*` Y/N columns | Answers to the lines named in the column (list in script `YN_ITEMS`); blank = not answered |
| `vi_1a_voting_members`, `vi_1b_independent_members`, `independent_share` | Counts and ratio |
| `i_5_employees`, `i_6_volunteers`, `v_2a_w2_employees` | Part I lines 5 and 6; Part V line 2a |
| `sched_l_present`, `n_sched_l_rows`, `sl_i_tax_imposed` | Schedule L attached; Part I–IV row count; Schedule L line 2 section 4958 tax on disqualified persons |
| `n_key_policy_no`, `n_key_policy_no_explained` | Count of "No" on 12a, 13, 14, 11a, 15a, 15b; how many of those have a matching Schedule O entry |
| `so_no_<item>` | Schedule O text (≤ 900 chars) matching that item when the answer is "No" |
| `so_vi_11b_review_process` | Schedule O line 11b text (≤ 400 chars) |
| `so_vi_refs` | Part VI or XII lines that Schedule O cites |
| `ctx_comp_top_officer_comp_total`, `ctx_comp_flag_affiliate_pay`, `ctx_comp_staff_cost_l5_10` | From the compensation CSV (top 50 only), same EIN × TY |
| `ctx_res_sponsor_group`, `ctx_res_months_opcost_r1`, `ctx_res_quality_flags` | From the resilience CSV (top 100 sponsors), same EIN × TY |

### 7.3 `schedule_l` rows
| Column | Meaning |
|---|---|
| `sl_part` | I_excess_benefit / II_loans / III_grants_assistance / IV_business_tr |
| `sl_name`, `sl_name_type` | Organisation name as filed, or `[individual]` (also when a person's name was typed in the business-name field, and when an organisation was typed in the person-name field; see §5 item 6) | [V wave 49A]
| `sl_relationship` | Category: family_member, donor_or_donor_advisor, substantial_contributor, founder_or_creator, controlled_or_affiliated_entity, board_member_trustee_director, officer_or_key_employee, employee, other_or_unstated |
| `sl_description` | Category. Parts I–III are fixed (excess_benefit_4958 / loan / grant_or_assistance). Part IV is keyword-coded: compensation, admin_or_management_services, investment_brokerage_custody, professional_services, sale_or_donation_of_assets, grant_or_fiscal_sponsorship, sponsorship_or_event, interest_or_loan, other_or_unstated |
| `sl_amount`, `sl_amount_field` | First amount in the row and its XML element (e.g. TransactionAmt, OriginalPrincipalAmt, CashGrantAmt) |
| `sl_corrected_ind` | Part I "transaction corrected" (Y/N) |

### 7.4 `band_item` and `comparison` rows
| Column | Meaning |
|---|---|
| `band` | all / top50 / sample / A_ge_1bn / B_100m_1bn / C_10m_100m / D_lt_10m (or a §4 subgroup name for `comparison`) |
| `item`, `form_ref` | Column name (or `column=value` for categories, `median_<column>` for medians); form line |
| `n_sponsors`, `n_yes`, `n_no`, `n_blank`, `pct_yes_of_answered` | Counts; for category rows `n_yes` is the count with that value and the % is of `n_sponsors` |
| `median`, `n_zero` | Medians for count columns and number of zeros |
