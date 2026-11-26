# Validation wave 34A: DAFRC data quality (P-B44N27-01, P-B39N4-02) and top-20 donor-information defaults (P-B44N28-01)

- **Validator:** independent-validation-agent-wave34a, 2026-11-19. Nothing was committed or pushed. There was no outreach, and crt.sh, certspotter and sec.gov were not used.
- **Studies validated:**
  - [b44n27-b39n4-dafrc-data-quality.md](b44n27-b39n4-dafrc-data-quality.md), with `dafrc-corrections-r2-proposed-2026-11-19.csv` and `scripts/mission_dafrc_r2_check.py`;
  - [b44n28-01-donor-info-defaults.md](b44n28-01-donor-info-defaults.md), with `donor-info-defaults-top20-2026-11-19.csv` and `scripts/mission_b44n28_donor_info_build.py`.
- **Register:** [`data/mission-2026-11-14/validation-register-wave34a.csv`](../../data/mission-2026-11-14/validation-register-wave34a.csv) has 38 claims, V34A-01 to V34A-38.
- **Method:**
  - Both scripts were re-run to the scratchpad (`v34a/`).
  - I parsed the cached Form 990 XML myself, with my own parser rather than the study's.
  - I re-fetched 36 sponsor and NPT sources (32 for the donor study, 4 NPT pages and PDFs) with a stdlib fetcher (UA `research-script/1.0`, unchanged). It fetched only when robots.txt allowed both `*` and that UA, and treated a 404 robots.txt as no restriction.
  - A script checks that every Find below occurs exactly once (§ "Find check").

## Summary counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| DAFRC data quality (V34A-01 to -18) | 18 | 13 | 4 | 1 | 0 |
| Donor-information defaults (V34A-19 to -38) | 20 | 12 | 7 | 0 | 1 |
| **Total** | **38** | **25** | **11** | **1** | **1** |

There are 37 Find/Replace items across 10 files, and each Find occurs exactly once.

## Findings

### 1. DAFRC data quality

**Reproduction and filed figures: confirmed.**
- `mission_dafrc_r2_check.py` re-runs to a byte-identical 97-row CSV and an identical JSON summary.
- My own parse of NPT's three returns matches every value the study gives:
  - Schedule D Part I lines 1–4;
  - Part X total assets, net assets, investments and cash;
  - Part VIII and Part IX ties;
  - Part XI unrealized gains;
  - Schedule R (NPT Transatlantic $130.5m/$163.1m/$245.3m as a disregarded entity; NPT UK `ControlledOrganizationInd = 0`).
- Column (b) is absent in all three years.
- The ratios are confirmed: 101.3%, 81.8% and 100.6% of net assets.
- So are the roll-forwards: $28.19bn forward from FY2022, $28.16bn back from FY2024, and $26.29bn from contributions less grants only.
- No amended FY2023 return is in the 2025 or 2026 indexes.
- The 2026-11-19 `index_2026.csv` does hold NPT's FY2025 990 (object 202601289349302480), which the study does not mention. It does not restate FY2023.

**What the study missed on NPT FY2023 (V34A-10, contradicted).**
- The study says NPT's 2023 annual report page has "no asset figure", that no FY2023 statements exist, and that NPT publishes only FY2025 summary statements. All three are wrong.
- The page the study cites (S10) has chart data, in `data-data` attributes rather than visible text, for "charitable assets under management". The figures are $22.13bn for FY22 and **$28.81bn for FY23**. The 2024 page gives $28.82bn for FY23 and $42.94bn for FY24.
- The same page links a two-page "Consolidated Statements" PDF at <https://www.nptrust.org/consolidated-statements-2023/> (created 2024-05-15). At 2023-06-30 it shows:
  - total assets of **$28,876,243k**;
  - investments of $23,169,028k;
  - cash of $5,648,084k;
  - net assets without donor restrictions of **$28,514,324k**.
- Consolidated net assets run 2.4%, 2.1% and 1.9% above the 990's Part X in FY2022, FY2023 and FY2024. That is a steady consolidation margin.
- So Part X is the consistent series, and Schedule D line 4 ($22.84bn, 80.1% of consolidated net assets) is the outlier.
- This answers the study's caveat that "Part X could in principle be the wrong one". It also answers queue item P-B44N27B39N4-01 on first-party evidence, though the PDF shows no auditor's opinion.
- The headline decision stays a policy call. Part X ($27.92bn) is still the conservative replacement.

**A candidate mechanism (V34A-07, partially confirmed, [I]).** No line or combination of up to three lines in the FY2023 return equals $22,843,599,245. However, total assets less savings and temporary cash comes to $22,762,967,205. That is $80.6m (0.35%) below the filed value, and the $5.08bn gap is 93% of the $5.48bn cash line. One reading is that line 4 left out cash in FY2023 only. In FY2022 and FY2024 it clearly includes cash. This is not proven.

**Minor wording issues.**
- *The return formula (V34A-06).* As written, the formula gives 145.2% and 118.8%. The stated 45.2% and 18.8% need "− BOY" in the numerator.
- *The paper-submission count (V34A-17).* The 18 rows ($90.43bn, 15 ending in 2023) are rows whose provenance resolves to paper. 21 rows carry a paper flag on at least one metric.

**Top-50 imputed rows: confirmed.**
- My own XML parse checked the 24 sponsors × 4 metrics against `dafrc-corrections-itemized.csv`. 95 cells are R1-applied with the same object id and a value equal to the filed figure.
- The exception is UCLA Foundation's grants:
  - filed `DonorAdvisedFundsGrantsAmt` of **−$120,260,861**;
  - the itemized row is not applied, so the imputed $169,930,257 stays;
  - UCLA's other three metrics are R1-applied.
- Each of the 24 EINs has exactly one FY2024 990 across `index_2025` and the fresh `index_2026`.
- ImpactAssets is −$731,283,079, as stated.
- The R1 asset deltas for the 24 sum to −$2,898,070,191.

**Market totals: unchanged.**
- FY2024 corrected market: $323,269,551,062.
- Corrected top 50: $276,266,253,487 (published: $279,334,361,954).
- Market as published: $327,870,852,179.
- No rank moves.
- The FY2023 sensitivity reproduces: $261.44bn, 14.6% and 23.6% growth, 25.4% payout and HHI 808.

### 2. Donor-information defaults

**Universe and arithmetic: confirmed.**
- The 20 EINs and asset values match the league table (FY2024, `top50`) in rank order. They sum to **$250,629,129,988**, and every share matches.
- `mission_b44n28_donor_info_build.py` reproduces the CSV byte for byte. The study says the script is "kept in the scratchpad", but it is in the repo.
- The bucket totals, the determinable base ($191.20bn) and the DAFgiving360 sensitivities (49.6% and 33.5%) all reproduce.

**Quotes.** I re-fetched 36 sources, all allowed by robots.txt. The CCT 101 guide was also fetched but then discarded (see below). The 36 are:
- Fidelity: 4 sources;
- NPT: 2 sources, plus 2 annual-report pages and 2 statements;
- DAFgiving360 policy;
- Vanguard: 2 sources;
- SVCF;
- MS GIFT: 2 sources;
- AEF: 2 sources;
- RCF: 2 sources;
- NCF: 2 sources;
- BofA: 2 sources;
- CCT application;
- ImpactAssets: 2 sources;
- JCF;
- FFTC;
- GKCCF: 2 sources;
- CJP: 2 sources;
- DAF Direct;
- Chariot: 2 sources.

Every quoted string in the CSV that has a re-fetched source was found verbatim, allowing for PDF line breaks and ® marks. The Fidelity 80/15/5 split (and 83/13/4 for 2020) and the Vanguard "Only 4%" and "Only 5%" strings are confirmed.

The blocks are confirmed:
- `www.dafgiving360.org` robots.txt returns 403;
- `gspf.goldman.com` returns `User-agent: *` with `Disallow: /`;
- `www.raymondjamescharitable.org` returns 403.

**Not verifiable: the CCT quote (V34A-31).**
- `www.cct.org` robots.txt returned a Cloudflare challenge and then 403, so the CCT 101 PDF was discarded unread.
- The donorportal application confirms only the anonymity options.
- "Name only" infers from silence that no address is sent.

**Inconsistencies in how categories were applied.**
1. **DAFgiving360 against NPT (V34A-23).** Both texts list options without a preselection. Under §1.5, NPT is coded "donor chooses; no default stated", but DAFgiving360 is coded "not determinable". The 2024 policy is inside the 2021+ window.
   - The same page also says DAFgiving360 "does not release the account holder's name and contact information to any recipient charity without the account holder's explicit consent". The study records this clause but does not weigh it, and it leans toward withholding when no choice is made.
2. **"Donor must choose" against "no default stated" (V34A-22, -36).** The bucket merges two different things:
   - a documented required choice: SVCF and JCF, 5.0% of top-20 assets;
   - no stated default: NPT, AEF and CJP, 20.9%.
   The CSV itself marks NPT and CJP "Y?" and AEF "unknown". The §0 label "No preselected default stated, so the donor chooses" therefore overstates the evidence.
3. **GKCCF against CJP (V34A-33).** GKCCF says the donor "decides what information they want to share", and that the check stub "will likely include the donor's name and contact information (typically an email address)". That is the same no-default, donor-directed pattern as CJP, but GKCCF is coded "fund name only" (withheld). Recoding it would take the withheld share from 17.2% to 16.1%.
4. **MS GIFT (V34A-26).** The fund-name default rests on the 2022 Grantee Guidelines. The live FAQ says "the name of the Account, or Donor as specified during the grant recommendation process", which is AEF-style wording. Under the study's own newest-document rule (the one used for BofA), the coding would weaken. The bucket is kept, at lower confidence.

**The BofA conflict (V34A-30): confirmed.**
- The portal guide (modified 2026-02-23) says "The default is Fund Name Only".
- The 2024 Program Guidelines (Version 3.2024, created 2024-06-05, modified 2024-09-18) say distributions carry "the account name and the name of the Donor or Advisor, unless anonymity is requested".
- Either reading withholds the address, so the withheld share is unchanged.
- The S22 date should note the September 2024 revision.

**RCF recoding (V34A-28): partially confirmed.**
- The DFX guide (2026-10-06) does default to "name, email, and address".
- RCF's Program Circular (created 2026-06-01, modified 2026-07-23) lists options with no default and does not mention email.
- RCF's $5.91bn also covers private-label programs, such as TSA's, which have their own defaults.
- So "full contact for all RCF assets" is an upper bound.

**Is "withheld-by-default does not hold as a rule" fair? (V34A-36, partially confirmed.)**

On documented defaults it is fair:
- withholding is documented for only 17.2% of top-20 assets (22.5% of determinable assets);
- full contact is documented for 33.2% (43.6%);
- no sponsor defaults to anonymous.

But the study's supporting sentence, that most assets "send contact details by default or make the donor choose" (59.1%), counts the 20.9% with no stated default as "make the donor choose". In total, the default is **undocumented for 44.6%** of top-20 assets: 20.9% with no stated default plus 23.7% not determinable.

There is also a plausible reading that runs the other way. If DAFgiving360's consent clause, and the no-default sponsors' forms, mean that nothing is sent without an election, then withholding when no choice is made reaches **54.4%**. So the defensible statement is that **neither rule holds at the top 20**. G12-2's "withheld by default" should be confined to the CF-weighted survey, and the top-20 result should be reported as mixed, with about 45% undocumented. The G12-2 reconsider-trigger is "partly met", as the study says.

**Minor (V34A-37).** "Fund-name defaults (Vanguard, MS GIFT, BofA), which hold 15%" should be 14.3%. The 15.3% figure includes GKCCF.

**Where the repo states the earlier finding (V34A-38).** `grep -rn "withheld donor contact"` finds:
- `gap19-clarity-edf-new-findings.md`: the §3 heading. G12-2 also appears in the §1 row, in §3 steps 6 and 9 and the reconsider-trigger, and in the §7 incentive-map block;
- `industry-incentives-structural-analysis.md`: the 2026-11-19 additions, outcome (E);
- `research-priority-inputs.csv`, `queue-proposals-gap19.csv` and `research-priority-queue.csv`: the P-GAP19-12 task text. This is the historical task wording, and no correction is proposed.

The incentive-map row is `incentive-map.csv`, "Sponsors (donor-data defaults)". The finding is restated in:
- `strategic-synthesis.md` §0 E ("Only 36% of sponsors default to sharing full contact data");
- `strategic-synthesis.md` wave 22–30 (c) item 3 ("Defaults, not donor choice, withhold contact data");
- the report's N27–N30 bullet.

Corrections for all of these are below.

## Exact corrections

Each **Find** is verbatim and occurs exactly once in its file, and the items apply in the order listed. In a Find or Replace, `\n` means a newline.


### `research/mission-2026-11-14/b44n27-b39n4-dafrc-data-quality.md`

**(a1) Summary (A), recommendation**
- **Find:** "Close the item from NPT's audited FY2023 statements (P-B44N27B39N4-01)."
- **Replace with:** "NPT's own consolidated statements for the year ended 2023-06-30 (https://www.nptrust.org/consolidated-statements-2023/, linked from the 2023 annual report page; PDF created 2024-05-15) report total assets of $28,876,243k and net assets of $28,514,324k. They agree with Part X and the roll-forwards, not with $22.84bn, so P-B44N27B39N4-01 is answered on first-party evidence. Whether to adopt the sensitivity in the headline series remains a repo policy decision [V wave 34A]"

**(a2) §2.2, return formula**
- **Find:** "Return needed in FY2024, measured as (EOY − (contributions − grants)) ÷ BOY:"
- **Replace with:** "Return needed in FY2024, measured as (EOY − (contributions − grants) − BOY) ÷ BOY [V wave 34A]"

**(a3) §2.2, near match for the filed figure**
- **Find:** "So the figure cannot be traced to a mis-keyed neighbouring line."
- **Replace with:** "So the figure cannot be traced to a mis-keyed neighbouring line. One near match is worth recording [I]: total assets less savings and temporary cash ($28,241,290,750 − $5,478,323,545 = $22,762,967,205) is within $80.6m (0.35%) of the filed $22,843,599,245, and the $5.08bn gap is 93% of that cash line. A line 4 that left out cash and temporary investments in FY2023 only would fit. In FY2022 and FY2024, total assets less cash is far below line 4, so cash was included in those years. This is not proven [V wave 34A]"

**(a4) §2.3, annual report page**
- **Find:** "gives grants ("$4.52 billion … during FY23") but no asset figure."
- **Replace with:** "gives grants ("$4.52 billion … during FY23"). Its chart data (in `data-data` attributes, not in the visible text) also give "charitable assets under management" of $22.13bn for FY22 and $28.81bn for FY23. The 2024 page gives $28.82bn for FY23 and $42.94bn for FY24 [V wave 34A]"

**(a5) §2.3, financial statements**
- **Find:** "- No FY2023 financial statements are listed in the nptrust.org sitemap (528 URLs checked)."
- **Replace with:** "- No FY2023 financial statements are listed in the nptrust.org sitemap (528 URLs checked). However, the 2023 annual report page links a two-page "Consolidated Statements" PDF at https://www.nptrust.org/consolidated-statements-2023/ (created 2024-05-15). At 2023-06-30 it shows total assets of $28,876,243k, investments of $23,169,028k, cash of $5,648,084k and net assets without donor restrictions of $28,514,324k. Consolidated net assets run 2.4%, 2.1% and 1.9% above 990 Part X in FY2022–24 (FY2022 $21,759,900k; FY2024 $42,686,748k from https://www.nptrust.org/consolidated-statements-2024-npt/). So Part X is the consistent series and Schedule D line 4 is the outlier. The PDF carries no auditor's opinion [V wave 34A]"

**(a6) §2.4, adoption condition**
- **Find:** "- Adopt it only if NPT's audited FY2023 statements confirm it (P-B44N27B39N4-01)."
- **Replace with:** "- NPT's consolidated FY2023 statements (net assets $28,514,324k) support it. Adopting it in the headline series is a policy decision. Because the consolidated basis covers NPT and its affiliates, Part X ($27,919,223,352) stays the conservative value (P-B44N27B39N4-01) [V wave 34A]"

**(a7) §3.3, paper-row count definition**
- **Find:** "There are 18 FY2024 rows panel-wide with a paper-submission flag, holding $90.43bn."
- **Replace with:** "There are 18 FY2024 rows panel-wide whose provenance resolves to paper submission (a paper flag on at least one metric and no `Imputed` flag), holding $90.43bn. 21 rows carry a paper flag on at least one metric [V wave 34A]."

**(a8) §4 Limits, NPT statements**
- **Find:** "- **NPT's audited FY2023 statements were not found.** NPT publishes only FY2025 summary statements, and no FY2023 PDF is in its sitemap. The direction of the NPT error is therefore inferred from internal consistency, not confirmed. The Part X figure could in principle be the wrong one, though Part X reconciles exactly through Part XI and the next year's BOY figure."
- **Replace with:** "- **NPT's FY2023 consolidated statements were found by the validator** at https://www.nptrust.org/consolidated-statements-2023/, linked from the 2023 annual report page but absent from the sitemap. They show net assets of $28,514,324k at 2023-06-30, in line with Part X and the roll-forwards, so the error is in Schedule D line 4, not Part X. The two-page PDF carries no auditor's opinion, and it reports no DAF-only figure [V wave 34A]"


### `data/mission-2026-11-14/dafrc-corrections-r2-proposed-2026-11-19.csv`

**(a9) NPT SENS row note**
- **Find:** "corrected_value = filed Part X net assets (lower bound)"
- **Replace with:** "corrected_value = filed Part X net assets (lower bound); NPT consolidated statements at 2023-06-30 report net assets of $28514324k (https://www.nptrust.org/consolidated-statements-2023/) [V wave 34A]"


### `research/mission-2026-11-14/b44n28-01-donor-info-defaults.md`

**(b1) §0 headline**
- **Find:** "**Not as a rule. Most top-20 assets sit at sponsors that either send contact details by default or make the donor choose.**"
- **Replace with:** "**Neither rule holds. Full contact is the documented default for 33.2% of top-20 assets, and withholding (name or fund name only) for 17.2%. The default is undocumented for 44.6%: no default is stated at NPT, AEF and CJP (20.9%), and the five not-determinable sponsors hold 23.7%. A documented required choice covers only 5.0% (SVCF, JCF).** [V wave 34A]"

**(b2) §0 donor-chooses bucket**
- **Find:** "- **No preselected default stated, so the donor chooses:** 5 sponsors with **25.9%** (NPT, SVCF, AEF, JCF, CJP)."
- **Replace with:** "- **Donor must choose (documented: SVCF, JCF, 5.0%) or no default stated (NPT, AEF, CJP, 20.9%):** 5 sponsors with **25.9%**. An unstated default is not evidence that the donor must choose [V wave 34A]"

**(b3) §0 confidence cell**
- **Find:** "| High for the 15 determinable rows (first-party text). The asset shares hinge on DAFgiving360 |"
- **Replace with:** "| High for the 15 determinable rows (first-party text). The asset shares hinge on DAFgiving360. Its 2024 policy lists options without a default, but says it "does not release the account holder's name and contact information to any recipient charity without the account holder's explicit consent", which leans toward withholding when no choice is made [V wave 34A] |"

**(b4) Verdict paragraph**
- **Find:** "At the top 20 that framing is **too strong**:"
- **Replace with:** "At the top 20 that framing is **too strong as a rule, and so is its opposite, because the default is undocumented for 44.6% of top-20 assets**. Specifically [V wave 34A]:"

**(b5) §2 table, DAFgiving360 row**
- **Find:** "**Not determinable.** Live site blocked; the 2024 policy lists 3 options with no default"
- **Replace with:** "**Not determinable.** Live site blocked. The 2024 policy lists 3 options with no default, and under §1.5 that text alone would code "no default stated", as NPT is coded. It adds that DAFgiving360 "does not release the account holder's name and contact information ... without the account holder's explicit consent" [V wave 34A]"

**(b6) §2 table, RCF row**
- **Find:** "| 9 | RCF | 5.91 | **Full contact including email:** "By default … name, email, and address" |"
- **Replace with:** "| 9 | RCF | 5.91 | **Full contact including email:** "By default … name, email, and address" (DFX portal guide). The RCF Program Circular (PDF modified 2026-07-23) lists options with no default, and private-label programs such as TSA's carry their own defaults, so this is an upper bound for RCF's $5.91bn [V wave 34A] |"

**(b7) §2 table, GKCCF row**
- **Find:** "| 16 | GKCCF | 2.57 | **Fund name only:** name and email "encouraged", donor decides |"
- **Replace with:** "| 16 | GKCCF | 2.57 | **Fund name only:** name and email "encouraged", donor decides. GKCCF also says the check stub "will likely include the donor's name and contact information (typically an email address)". Coded the way CJP is, this would be "no default stated", and the withheld share would fall to 16.1% [V wave 34A] |"

**(b8) §3 sensitivity bullet**
- **Find:** "  - Either way, **no reading makes contact-withholding the asset-weighted majority** unless all five "donor chooses" sponsors effectively send no contact data."
- **Replace with:** "  - Either way, **no reading makes contact-withholding the asset-weighted majority** unless the "donor chooses" sponsors effectively send no contact data. That condition is not remote. If DAFgiving360's explicit-consent clause means no contact without an election, and NPT, AEF and CJP likewise send none unless it is chosen, withholding when no choice is made would cover 33.5% + 20.9% = 54.4% of top-20 assets. The asset-weighted answer is therefore open, not settled against withholding [V wave 34A]"

**(b9) §3.1 recommended wording**
- **Find:** "Recommended wording: "defaults vary; roughly a third to a half of top-20 assets default to full contact, about a sixth to a third withhold it, and no top-20 sponsor defaults to anonymous""
- **Replace with:** "Recommended wording: "defaults vary. A documented full-contact default covers 33–50% of top-20 assets and a documented withholding default 17–34%; both ranges turn on DAFgiving360. The default is undocumented for the rest, and no top-20 sponsor defaults to anonymous" [V wave 34A]"

**(b10) §4 fund-name share**
- **Find:** "  - fund-name defaults (Vanguard, MS GIFT, BofA), which hold 15% of top-20 assets;"
- **Replace with:** "  - fund-name defaults (Vanguard, MS GIFT, BofA), which hold 14.3% of top-20 assets (15.3% with GKCCF; BofA's 2024 Program Guidelines would make it name only) [V wave 34A];"

**(b11) §1 method, script location**
- **Find:** "Asset shares are computed by script (`build.py`, kept in the scratchpad) as each sponsor's `daf_assets_eoy` over the top-20 total."
- **Replace with:** "Asset shares are computed by script ([`scripts/mission_b44n28_donor_info_build.py`](../../scripts/mission_b44n28_donor_info_build.py), which reproduces the CSV byte for byte) as each sponsor's `daf_assets_eoy` over the top-20 total [V wave 34A]."

**(b12) §8 source register, S22 date**
- **Find:** "| S22 | BofA CGF, Program Guidelines 2024 | 2024-06-05 |"
- **Replace with:** "| S22 | BofA CGF, Program Guidelines 2024 (Version 3.2024) | 2024-06-05 (PDF modified 2024-09-18) [V wave 34A] |"


### `data/mission-2026-11-14/donor-info-defaults-top20-2026-11-19.csv`

**(b13) DAFgiving360 row, change_vs_repo**
- **Find:** "unchanged; default still unobserved"
- **Replace with:** "unchanged; default still unobserved (2024 policy: no release of name and contact information without explicit consent; by the NPT coding rule this text alone would read 'no default stated') [V wave 34A]"


### `research/mission-2026-11-14/gap19-clarity-edf-new-findings.md`

**(c1) §1 results table, G12-2 outcome**
- **Find:** "| G12-2 | Most surveyed sponsors do not pass full donor contact data to nonprofits by default |"
- **Replace with:** "| G12-2 | Most surveyed sponsors (DAFRC, n=128, 86% CFs) do not pass full donor contact data to nonprofits by default. At the FY2024 top 20, a full-contact default is documented for 33.2% of assets and a withholding default for 17.2%; 44.6% is undocumented (P-B44N28-01) [V wave 34A] |"

**(c2) §3 heading**
- **Find:** "## 3. G12-2. Withheld donor contact data by default"
- **Replace with:** "## 3. G12-2. Donor contact data withheld by default at most surveyed (CF-weighted) sponsors; mixed at the top 20 [V wave 34A]"

**(c3) §3 step 6, not observed**
- **Find:** "   - *Not observed:* the defaults at the top-20 national sponsors (open queue item P-B44N28-01)."
- **Replace with:** "   - *Observed (P-B44N28-01, 2026-11-19):* first-party text exists for 15 of the top 20 (76.3% of FY2024 top-20 assets).\n     - Full contact is the stated default at Fidelity, RCF, NCF, ImpactAssets and FFTC (33.2%).\n     - Name or fund name only at Vanguard, MS GIFT, BofA, CCT and GKCCF (17.2%).\n     - A required choice at SVCF and JCF (5.0%).\n     - No stated default at NPT, AEF and CJP (20.9%).\n     - DAFgiving360, GS DAF and Raymond James are blocked by robots, and Greater Horizons and Dechomai publish nothing relevant (23.7%).\n     - No top-20 sponsor defaults to anonymous [V wave 34A]"

**(c4) §3 step 9, diagnostic sufficiency**
- **Find:** "   - Not enough to say the national sponsors behave like the CF-heavy survey sample."
- **Replace with:** "   - P-B44N28-01 shows that, as a rule, the top 20 do not behave like the CF-heavy survey sample. By count, 5 of 15 determinable sponsors default to full contact, close to DAFRC's 36%. But only 5 of 15 withhold, against DAFRC's 59% for name or fund name only [V wave 34A]"

**(c5) §3 reconsider trigger**
- **Find:** "  - P-B44N28-01 shows the top-20 nationals already default to full contact. The problem would then be CF-specific and the entrant's edge smaller."
- **Replace with:** "  - P-B44N28-01 shows the top-20 nationals already default to full contact. The problem would then be CF-specific and the entrant's edge smaller. **Outcome (validated, wave 34A): partly met.**\n    - Fidelity, RCF, NCF, ImpactAssets and FFTC default to full contact (33.2% of top-20 assets).\n    - Vanguard, MS GIFT, BofA, CCT and GKCCF do not (17.2%).\n    - The default is undocumented for 44.6%, including DAFgiving360 (16.3%).\n    - The classification stays mixed, leaning habit [V wave 34A]"

**(c6) §7 incentive-map row text (code block)**
- **Find:** "Reconsider if top-20 national defaults (P-B44N28-01) differ or a privacy/4967 ruling appears.""
- **Replace with:** "Top-20 check (P-B44N28-01; wave 34A): full-contact default 33.2% of FY2024 top-20 assets; withholding default 17.2%; 44.6% undocumented. Reconsider if a privacy/4967 ruling appears. [V wave 34A]""


### `data/mission-2026-11-14/incentive-map.csv`

**(c7) row 'Sponsors (donor-data defaults)', notes field (unquoted, so no commas)**
- **Find:** "G12-2. Leaning habit: variation under one federal regime. Reconsider if top-20 national defaults (P-B44N28-01) differ or a privacy/4967 ruling appears."
- **Replace with:** "G12-2. Leaning habit: variation under one federal regime. Top-20 check (P-B44N28-01; wave 34A): full-contact default 33.2% of FY2024 top-20 assets; withholding default 17.2%; 44.6% undocumented. Reconsider if a privacy/4967 ruling appears. [V wave 34A]"


### `research/mission-2026-11-14/industry-incentives-structural-analysis.md`

**(c8) Additions (2026-11-19), outcome E**
- **Find:** "withheld donor contact data by default (E)"
- **Replace with:** "withheld donor contact data by default in the CF-weighted DAFRC survey (E). At the FY2024 top 20 the default is mixed: full contact covers 33.2% of assets, withholding 17.2%, and 44.6% is undocumented, per [b44n28-01-donor-info-defaults.md](b44n28-01-donor-info-defaults.md) [V wave 34A]"


### `research/mission-2026-11-14/strategic-synthesis.md`

**(d1) §0 E, nonprofit identity data**
- **Find:** "- **Nonprofit identity and remittance data.** Only 36% of sponsors default to sharing full contact data ([direction-nonprofit-side-experience.md](direction-nonprofit-side-experience.md); wave 29)."
- **Replace with:** "- **Nonprofit identity and remittance data.** Only 36% of sponsors in the CF-weighted DAFRC survey default to sharing full contact data ([direction-nonprofit-side-experience.md](direction-nonprofit-side-experience.md); wave 29). At the FY2024 top 20 the default is mixed. Full contact is documented for 33.2% of assets (Fidelity, RCF, NCF, ImpactAssets, FFTC) and withholding for 17.2%; the rest is undocumented ([b44n28-01-donor-info-defaults.md](b44n28-01-donor-info-defaults.md)) [V wave 34A]"

**(d2) Wave 22–30 (c) item 3**
- **Find:** "Defaults, not donor choice, withhold contact data (wave 29)."
- **Replace with:** "Defaults, not donor choice, withhold contact data at most sponsors in the CF-weighted survey (wave 29). At the top 20, Fidelity and four others preselect full contact, and Vanguard, MS GIFT and BofA default to fund name only (wave 34A) [V wave 34A]."

**(d3) NPT FY2023 statements**
- **Find:** "- NPT FY2023: its audited statements would settle whether $22.84bn is a filer error"
- **Replace with:** "- NPT FY2023: NPT's consolidated statements at 2023-06-30 (net assets $28,514,324k; total assets $28,876,243k) are consistent with Part X ($27.92bn), not with the $22.84bn Schedule D value, which is therefore very likely a filer error [V wave 34A]"

**(d4) Corrections table, NPT FY2023 row**
- **Find:** "A real filed value, **most likely a filer error** [I]. Part X net assets are $27.92bn."
- **Replace with:** "A real filed value, **very likely a filer error**. Part X net assets are $27.92bn, and NPT's consolidated statements report $28.51bn at 2023-06-30 [V wave 34A]."


### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**(e1) §11 N27–N30, NPT bullet**
- **Find:** "NPT's FY2023 Schedule D value ($22.84bn against $27.92bn of net assets) is a real filed figure, most likely a filer error."
- **Replace with:** "NPT's FY2023 Schedule D value ($22.84bn against $27.92bn of net assets) is a real filed figure, very likely a filer error: NPT's consolidated statements report $28.51bn of net assets at 2023-06-30 [V wave 34A]."

**(e2) §11 N27–N30, defaults bullet**
- **Find:** "Only 36% of sponsors default to full contact data, and 35% to fund name only (DAFRC, 128 sponsors, 86% community foundations)."
- **Replace with:** "Only 36% of sponsors default to full contact data, and 35% to fund name only (DAFRC, 128 sponsors, 86% community foundations). At the FY2024 top 20, full contact is the documented default for 33.2% of assets and withholding for 17.2%, and 44.6% is undocumented [V wave 34A]."

**(e3) New §11.34. Insert before the Source register.**
- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.34 Data quality and donor data (validated, wave 34A)\n\n<the paragraph below>\n\n---\n\n## Source register"
- *(The paragraph already ends with the tag. Do not add a second one.)*

New subsection text:

> **Data quality and donor data** (validated, wave 34A). A round-2 check of DAFRC's FY2024 panel found nothing left to replace. All 24 top-50 sponsors with imputed rows already carry R1 values equal to their filed FY2024 Form 990s in 95 of 96 cells; UCLA Foundation's grants, filed as −$120,260,861, keep the imputed $169.9m. The FY2024 market ($323.27bn) and corrected top 50 ($276.27bn) are unchanged. NPT's FY2023 Schedule D value ($22.84bn) is 81.8% of its Part X net assets ($27.92bn), against 101.3% and 100.6% in the adjacent years, and NPT's own consolidated statements report $28.51bn of net assets at 2023-06-30, so it is very likely a filer error. Using Part X would put FY2023 at $261.44bn and FY2023–24 growth at 23.6%, not 26.1%; the headline keeps the filed value. At the FY2024 top 20 ($250.63bn), full contact is the documented default for 33.2% of assets, led by Fidelity, and name or fund name only for 17.2%. For 44.6% the default is undocumented, and no sponsor defaults to anonymous. The survey finding that sponsors withhold donor contact data by default does not hold as a rule at the nationals, and neither does its opposite (repo [`validation-wave34a-report.md`](mission-2026-11-14/validation-wave34a-report.md)) [V wave 34A]


## Find check

`v34a/build/check_finds.py` (scratchpad) reads every Find/Replace item and counts each Find in its target file. It then applies the items in order and recounts. Result: **37 items, 37 found exactly once, 0 sequential conflicts**. After the simulated application, the three edited CSVs keep their row and column counts (98×24, 21×33, 39×9). `v34a/build/check_report_finds.py` re-parses this report's **Find** lines and gives the same result.

## Limits

- **NPT statements.** The consolidated statements are a two-page summary with no auditor's opinion and no DAF-only line. They settle which 990 line is inconsistent, not the exact DAF value.
- **Blocked sources.** DAFgiving360, GS DAF and Raymond James were not read (robots), nor was the CCT 101 guide (Cloudflare challenge, then 403). GS's 2008 circular was not checked.
- **What "default" means.** Coding rests on published text, as in the study. No logged-in screens were seen.
- **The cash-omission reading (V34A-07)** is an inference from a near match, not a proven mechanism.
