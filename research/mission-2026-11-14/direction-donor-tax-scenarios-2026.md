# Donor tax scenarios for 2026: direct gift vs DAF vs private foundation (P-NEW-TAX-01)

**Prepared 2026-11-15. Desk research and illustrative modelling only. NOT TAX ADVICE.** The households are stylised, the model covers federal income tax only, and **state and local tax effects are excluded**. No one was contacted. Nothing was logged into or submitted.

**Labels.** **[F]** the cited source states it. **[C]** our computation (script output). **[I]** interpretation or judgment.

**Files.**
- Script: [`scripts/mission_tax_scenarios.py`](../../scripts/mission_tax_scenarios.py). Stdlib only, pure functions. It runs self-checks against the Rev. Proc. tables and the 35% cap identity before writing anything.
- Scenarios: [`data/mission-2026-11-14/donor-tax-scenarios-2026.csv`](../../data/mission-2026-11-14/donor-tax-scenarios-2026.csv). 279 rows: one row per scenario-year plus one `total` row for each of the 63 scenarios.
- Sensitivity: [`data/mission-2026-11-14/donor-tax-scenarios-2026-sensitivity.csv`](../../data/mission-2026-11-14/donor-tax-scenarios-2026-sensitivity.csv) (36 rows, tests S1–S5).
- Parameters with citations, excluded items and stylised inputs: [`data/mission-2026-11-14/donor-tax-parameters-2026.csv`](../../data/mission-2026-11-14/donor-tax-parameters-2026.csv).
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-batch42-n20.csv`](../../data/mission-2026-11-14/queue-proposals-batch42-n20.csv) (P-B42N20-01 to -03).

**Repo context read first.**
- [`direction-policy-lobbying-obbba.md`](direction-policy-lobbying-obbba.md) §3.1, including its wave 24A governing corrections. None of the corrections touches the tax mechanics. Every mechanic in its §3.1 was re-checked against the statute below, and none conflicts.
- [`regulation-market-structure-portability.md`](regulation-market-structure-portability.md) Q-B09.
- [`../donor-tax-personas-2026.md`](../donor-tax-personas-2026.md). Its worked example uses a flat 24% rate and no tax engine. This note replaces that example with a full computation but does not change its persona ranking.

**Access and robots.txt.** We read robots.txt on every host before fetching from it.
- **Fetched:** govinfo.gov (`/content/` allowed); irs.gov (`/pub/` and `/newsroom/` allowed); law.cornell.edu (allowed, with crawl-delay 10 s honoured); ecfr.gov (API allowed).
- **Not fetched:**
  - jct.gov disallows ClaudeBot and anthropic-ai.
  - congress.gov (and therefore CRS reports) disallows Claude user agents.
  - **No JCT or CRS document was used.** The statute text and IRS guidance are the primary sources.
- uscode.house.gov allowed fetching, but it is "operating in a temporary format" and returned 404 for section pages, so the Code was read on LII instead.

---

## 1. Answer in brief

| Question | Finding |
|---|---|
| Does a DAF give a bigger deduction than a direct gift? | **No, not in the same year for the same asset.** For itemizers, the DAF and the direct gift produce identical tax in every scenario where the donor itemizes (H2 and H3 itemized rows; all H4 rows) [C]. |
| Where does a DAF *lose*? | **Non-itemizers, and households near the threshold, giving cash.**<br>– **H1 (non-itemizer):** a direct cash gift saves **$720 over 3 years** through the $2,000 non-itemizer deduction. The same cash to a DAF or a private foundation saves **$0** [C], because §170(p) excludes DAF gifts and covers only §170(b)(1)(A) organizations [F].<br>– **H2 (near the threshold):** the standard deduction plus $2,000 ($34,200) beats itemizing ($33,500), so direct cash saves **$1,440** against **$936** for annual DAF gifts [C]. |
| Where does bunching pay? | **Near the standard-deduction threshold.**<br>– **H2:** putting 3 years of giving ($30,000) into 2026 saves **$5,112**, against $1,440 for annual direct giving: **+$3,672** [C].<br>– **H3 (37% bracket):** bunching only avoids two years of the 0.5% floor: **+$3,500** [C].<br>– **Bunching is not DAF-specific:** a direct prepaid gift gives the same tax result. What the DAF adds is the ability to spread grants to charities over the later years [I]. |
| 35% cap | **H3:** each deductible charitable dollar saves exactly **$0.35**, not $0.37 (37% × (1 − 2/37)). The 0.5% floor then cuts the annual saving per dollar given to **0.315** [C]. |
| Capital gains | **Giving long-held stock in kind instead of selling it and giving the cash** is worth:<br>– H2: **$4,541** over 3 years;<br>– H3: **$28,770** over 3 years;<br>– H4: **$191,157** on a $1m gift (basis 20%) [C].<br>This holds equally for direct, DAF and private-foundation gifts of **listed** stock (§170(e)(5)).<br>**For H1 it is worth $0, or negative:** H1's gains sit in the 0% band, and only *cash* qualifies for the non-itemizer deduction [C]. |
| AGI limits | These limits bind only for H4 in our set.<br>– **Stock to a private foundation (20% limit):** $663k is allowed in 2026 and $337k is carried forward. It is used up by 2031 at a $1m gift, but **$447k is never used at a $1.5m gift** [C].<br>– **DAF (30% limit):** nothing is left unused until the gift reaches $2m ($407k unused) [C]. |
| Private foundation costs | **1.39% excise** applies to the PF's net investment income, including gain on selling donated stock at the donor's carryover basis [F]. For H4 that is **$11,120** if the $1m of 20%-basis stock is sold [C]. The annual drag is **$556 at a 4% return** on $1m (illustrative return) [C]. The 5% minimum payout comes to **$38,880–$50,000** on $1m [C]. DAFs have neither the excise tax nor a payout rule [F, by absence from §§4940/4942, which apply to private foundations]. |

---

## 2. Method

### 2.1 Household profiles

All households file jointly. **Every value below is a stylised input, not a sourced fact.**

| ID | Profile | Wages/yr | Other itemized/yr | Intended giving | Horizon | Other |
|---|---|---|---|---|---|---|
| H1 | Non-itemizer, moderate income | $90,000 | $12,000 | $2,000/yr | 2026–28 | — |
| H2 | Itemizer near the threshold, 24% bracket | $300,000 | $25,000 | $10,000/yr | 2026–28 | — |
| H3 | Itemizer, 37% bracket | $1,000,000 | $40,000 | $50,000/yr | 2026–28 | — |
| H4 | High income with a liquidity event | $400,000 | $40,000 | $1,000,000 once, in 2026 | 2026–31 (contribution year + 5 carryforward years) | $3,000,000 long-term gain in 2026 from selling a separate *investment* position, so NIIT applies |

- The donated stock is listed, held long term and has a basis of **20% of FMV**. S1 varies the basis from 0% to 100%.
- "Other itemized" is taken *after* any SALT-cap limit; the SALT-cap mechanics are not modelled.

### 2.2 Grid

There are **63 scenarios**:
- **Assets:** (i) cash; (ii) stock given in kind; plus a reference case, stock sold and the cash proceeds given.
- **Vehicles:** (a) direct gift to a public charity; (b) a DAF at a public-charity sponsor; (c) a private non-operating foundation, not a §170(b)(1)(F) conduit.
- **Timing:**
  - H1–H3: `annual` (equal gift each year) and `bunched_y1` (three years of giving in 2026).
  - H4: `oneoff_y1`.

The baseline is the same household with no gift and no sale. 2026 parameters are **held flat** for 2027 onward (see §5).

### 2.3 Formulas

These are implemented exactly as below in the script. Section references are to the IRC.
1. **AGI** = wages + long-term gain. **Contribution base** = AGI (§170(b)(1)(H)).
2. **§170 category:**
   - cash to a public charity or DAF → (G), 60%;
   - stock to a public charity or DAF → (C), 30%;
   - cash to a PF → (B), 30%;
   - stock to a PF → (D), 20%.
3. **Allowed before the floor** = min(current gifts + live carryovers, limit × CB). Current-year gifts are absorbed first, then carryovers, oldest first. Carryovers expire after 5 years.
4. **0.5% floor:** allowed = pre-floor − min(pre-floor, 0.005 × CB). The amount lost to the floor is carried forward **only in a year with a percentage-limit excess** (§170(d)(1)(C)).
5. **§68 (35% cap):** reduction = 2/37 × min(itemized deductions, max(0, AGI − $768,700)). Taxable income before §68 plus itemized deductions equals AGI, which gives this form. It is applied after all other limits.
6. **Standard path:** $32,200 + min($2,000, cash given *directly* to a public charity), with no 0.5% floor (§170(p); §63(b)(4)).
7. The household takes whichever path, itemized or standard, gives the lower tax.
8. **Regular tax** (§1(h) with §1(j)(5)): gains are stacked on top of ordinary taxable income. 0% applies up to $98,900 of taxable income, 15% up to $613,700, and 20% above that. Ordinary income uses the 2026 joint schedule.
9. **NIIT** = 3.8% × min(net investment income, AGI − $250,000). Itemized deductions do not reduce it.
10. **Private-foundation measures** are reported per vehicle, not as donor tax:
    - excise if the donated stock is sold = 1.39% × (FMV − carryover basis);
    - annual excise = 1.39% × illustrative return × gift;
    - minimum distribution = 5% × gift − excise. This assumes zero growth, with year-end FMV standing in for the average.

**Self-checks in the script:**
- Tax at $211,400 is $35,932, and tax at $768,700 is $206,583.50, both matching Rev. Proc. 2025-32 Table 1.
- An extra $1,000 of itemized deductions deep in the 37% bracket saves exactly $350.

---

## 3. Parameter table (all verified in primary text on 2026-11-15)

| Parameter | Value used | Primary source (pinpoint) |
|---|---|---|
| 2026 joint rate schedule | 10/12/22/24/32/35/37% with breakpoints at $24,800 / $100,800 / $211,400 / $403,550 / $512,450 / $768,700 | [Rev. Proc. 2025-32 §4.01 Table 1](https://www.irs.gov/pub/irs-drop/rp-25-32.pdf) |
| Standard deduction, joint | $32,200 | Rev. Proc. 2025-32 §4.14(1) |
| Capital-gains rate amounts, joint | 0% up to $98,900; 15% up to $613,700 (taxable income) | Rev. Proc. 2025-32 §4.03; [§1(h)(1), §1(j)(5)](https://www.law.cornell.edu/uscode/text/26/1) |
| NIIT | 3.8%; $250,000 joint threshold, not indexed | [§1411(a)(1), (b)(1)](https://www.law.cornell.edu/uscode/text/26/1411) |
| 35% cap | §68: reduce by 2/37 × lesser of (itemized deductions, or taxable income + itemized deductions above the start of the 37% bracket); applied last | [P.L. 119-21 §70111](https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm) |
| 0.5% floor | 0.5% of contribution base. Applied first to (D) gifts, then (C), (B), (E), (A), (G). Floor amounts carry forward only from years with a percentage-limit excess | P.L. 119-21 §70425(a) (new §170(b)(1)(I), §170(d)(1)(C)) |
| 60% cash limit | Made permanent | P.L. 119-21 §70425(b)(1) (§170(b)(1)(G)(i)) |
| 30% limit for capital-gain property to public charities (including DAF sponsors) | 30% | [§170(b)(1)(C)(i)](https://www.law.cornell.edu/uscode/text/26/170) |
| Cash to a non-operating PF | 30% (lesser of 30%, or 50% less (A)/(G) gifts) | §170(b)(1)(B) |
| Capital-gain property to a non-operating PF | 20% (lesser of 20%, or 30% less (C) gifts) | §170(b)(1)(D)(i) |
| Carryforward | 5 years | §170(b)(1)(B), (C)(ii), (D)(ii), (G)(ii); §170(d)(1)(A) |
| Listed stock to a PF valued at FMV | The §170(e)(1)(B)(ii) reduction is switched off for qualified appreciated stock (listed; donor and family hold at most 10% of the company) | §170(e)(5) |
| Non-itemizer deduction | $1,000 single / $2,000 joint, permanent. Cash only, to §170(b)(1)(A) organizations; not to 509(a)(3) organizations; **not to establish or maintain a DAF**. No 0.5% floor. Taken in addition to the standard deduction | P.L. 119-21 §70424, §70425(a)(3); §170(p); [§63(b)(4)](https://www.law.cornell.edu/uscode/text/26/63); [IR-2026-135](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize); [Pub. 6196](https://www.irs.gov/pub/irs-pdf/p6196.pdf) |
| PF excluded from the non-itemizer deduction | Non-operating PFs are not §170(b)(1)(A) organizations unless they are §170(b)(1)(F) conduits or pooled funds. Pub. 6196's eligible codes are PC, POF, 50%/60% and FED, with no PF code | §170(b)(1)(A)(vii), (F); Pub. 6196 |
| PF excise | **1.39%** of net investment income. **Not amended by P.L. 119-21**: a text search of the enacted Act finds §4940 only as a cross-reference in new §4968(f) | [§4940(a)](https://www.law.cornell.edu/uscode/text/26/4940); P.L. 119-21 text |
| PF gain basis | The donor's carryover basis (Part II of Subchapter O) | [26 CFR 53.4940-1(f)(2)(i)(B)](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-D/part-53/subpart-B/section-53.4940-1) |
| PF payout | 5% of the FMV of non-charitable-use assets, less §4940 and income taxes (distributable amount) | [§4942(d), (e)(1)](https://www.law.cornell.edu/uscode/text/26/4942) |
| Effective date | Taxable years beginning after Dec 31, 2025 (§§70111, 70424, 70425) | P.L. 119-21 |

**Parameters requested or relevant but not verified, and therefore excluded:**
- **State and local tax**, excluded by design.
- **2027 and later inflation adjustments.** We did not check whether a 2027 Rev. Proc. has been issued, so 2026 values are held flat.
- **The 1.5% cash set-aside and other §4942 adjustments** in the regulations: not read.
- **Sponsor and PF administrative, legal and set-up fees.** These are not tax parameters. See [`all-in-cost-comparison-2026.csv`](../../data/mission-2026-11-14/all-in-cost-comparison-2026.csv) for DAF fees.
- **AMT, credits, §199A, the tips/overtime/senior deductions and the SALT phase-down.**
- **How carryovers are treated in a year the donor takes the standard deduction.** The rule was not read. The script flags any such row; none occurs in the base grid.

---

## 4. Results

The full detail is in the CSVs. Totals are over the horizon, in dollars [C]. "vs direct" compares each scenario with the direct gift of the same asset on the `annual` or `oneoff` timing.

| Scenario | Gift | Tax saving | Saving per $ | vs direct | Years itemized | Notes |
|---|---|---|---|---|---|---|
| H1 cash, direct, annual | 6,000 | **720** | 0.12 | 0 | 0 | Non-itemizer deduction, $2,000 × 12% |
| H1 cash, DAF, annual | 6,000 | **0** | 0 | −720 | 0 | DAF excluded from §170(p) |
| H1 cash, PF, annual | 6,000 | 0 | 0 | −720 | 0 | PF is not a §170(b)(1)(A) organization |
| H1 cash, DAF, bunched | 6,000 | 0 | 0 | −720 | 0 | $12,000 + $6,000 itemized is still below $32,200 |
| H1 stock in kind, any vehicle | 6,000 | 0 | 0 | 0 | 0 | Gain falls in the 0% band; stock is not "cash" for §170(p) |
| H2 cash, direct, annual | 30,000 | **1,440** | 0.048 | 0 | 0 | Standard + $2,000 ($34,200) beats itemizing ($33,500) |
| H2 cash, DAF or PF, annual | 30,000 | 936 | 0.031 | −504 | 3 | Itemizes by $1,300/yr |
| H2 cash, DAF / PF / direct prepaid, bunched | 30,000 | **5,112** | 0.170 | +3,672 | 1 | One itemized year, then two standard years |
| H2 stock in kind, any vehicle, annual | 30,000 | 936 | 0.031 | 0 | 3 | Plus $4,541 against selling first (DAF or PF) |
| H3 any asset, any vehicle, annual | 150,000 | **47,250** | 0.315 | 0 | 3 | $45,000/yr × 35% after the floor and §68 |
| H3 any asset, any vehicle, bunched | 150,000 | 50,750 | 0.338 | +3,500 | 3 | Two fewer years of the $5,000 floor |
| H3 stock in kind vs sell-then-give | — | +28,770 | — | — | — | Gains avoided at 20% + 3.8% NIIT |
| H4 cash or stock, direct or DAF, one-off | 1,000,000 | **218,599** | 0.219 | 0 | 6 | 2026 deduction mostly offsets gains taxed at 20% (§68 then trims it); NIIT is untouched |
| H4 stock in kind, PF, one-off | 1,000,000 | 238,458 | 0.238 | +19,859 | 6 | 20% limit: $337k carried forward into 2027–31 at 24–32% ordinary rates. PF excise if sold: $11,120 |
| H4 stock in kind vs sell-then-give (direct or DAF) | — | +191,157 | — | — | — | 800k gain × (20% + 3.8%), plus interactions |

**Reading [I].**
1. **The DAF exclusion from §170(p) is the only rule that makes the DAF *worse* than a direct gift, at equal timing.** It matters only for households that do not itemize. That means 2 of the 4 profiles in the base case, and the bottom of the H2 range in S2.
2. **Bunching is the DAF's tax argument, and it is narrow.**
   - It pays most when other itemized deductions plus giving sit near $32,200.
   - S2 shows the gain for H2: **$72** when other itemized deductions are $10,000, **$3,672** at $25,000, and **$720** at $40,000, by which point the household itemizes every year anyway.
   - For H1, even $8,000/yr bunched into a DAF saves less ($402) than giving cash directly each year ($720) (S5).
3. **The 35% cap and the 0.5% floor apply the same way to all three vehicles.** They do not favour any of them.
4. **The PF's higher 2026 deduction for H4 is an artefact of timing, not an advantage.**
   - The 20% limit pushes deductions into years where they offset ordinary income rather than 20% gains.
   - A DAF donor could get the same result by spreading contributions on purpose.
   - The PF result also comes with the 1.39% excise, the 5% payout and administrative costs the model does not count.
5. **Stock in kind is the largest lever in every case where gains are taxable.** It works for any vehicle that accepts listed stock. It is not specific to DAFs.

### Sensitivity (`donor-tax-scenarios-2026-sensitivity.csv`)

| Test | Range | Result [C] |
|---|---|---|
| S1 basis of donated stock | 0 / 20 / 50 / 100% of FMV | Gain from giving in kind vs sell-then-give:<br>– H2: 5,676 / 4,541 / 2,838 / 0<br>– H3: 35,963 / 28,770 / 17,981 / 0<br>– H4: 238,946 / 191,157 / 119,473 / 0 |
| S2 H2 other itemized deductions | $10k / 20k / 25k / 30k / 40k | DAF bunching gain over annual direct cash: 72 / 2,472 / 3,672 / 1,776 / 720 |
| S3 H4 gift size, stock in kind | $0.5m / 1m / 1.5m / 2m | DAF unused at end of 2031: 0 / 0 / 0 / 407k<br>PF unused: 0 / 0 / 447k / 947k<br>PF saving stops growing above $1.5m (251,658) |
| S4 PF return (illustrative, not sourced) | 0 / 4 / 8% | Annual 1.39% excise on $1m: 0 / 556 / 1,112 |
| S5 H1 annual gift | $1k / 2k / 5k / 8k | Direct annual: 360 / 720 / 720 / 720<br>DAF bunched: 0 / 0 / 0 / 402 (itemizes in 1 of 3 years only at $8k) |

---

## 5. Limitations

- **Not tax advice.** These are stylised households filing jointly, with one gift type per scenario. Mixed gifts in one year interact through the §170(b) ordering rules, and the script does not model that.
- **State and local income tax are excluded.** Many states do not follow §170(p), §68 or the 0.5% floor.
- **AMT, credits, §199A, the tips/overtime/senior deductions and SALT-cap mechanics are not modelled.** "Other itemized" is a fixed input.
- **2026 brackets and the standard deduction are held flat for 2027–2031.** Indexed values would change the bunching results slightly. See P-B42N20-02.
- **Two statutory readings are interpretations [I]. No IRS form instructions or regulations for them were found or read:**
  1. The 0.5% floor is applied to carryovers absorbed in later years.
  2. Floor-disallowed amounts carried forward are dated to the current year.
  
  These readings affect only H4 PF and the S3 rows. Because of reading (2), the CSV's total `floor_disallowed` column counts floor amounts that later come back as deductions, so it is a gross figure.
- **Net investment income.** We treat H4's 2026 gain as investment gain (NIIT applies). Gain from selling an active business could be outside NIIT under §1411(c)(4), which was not read.
- **DAF and PF fees, investment returns, charity-side timing and grant behaviour are not modelled.** The PF measures are mechanical illustrations.
- **The "direct" vehicle assumes a §509(a)(1)/(2) public charity that accepts listed stock.** Many small charities route stock gifts through a DAF or a broker. This is an access issue, not a tax issue.
- **Excluded parameters:** see §3.

## Validation corrections (wave 27, 2026-11-15) — governing
Source: [validation-wave27-report.md](validation-wave27-report.md); register `data/mission-2026-11-14/validation-register-wave27.csv`.

1. **§1, AGI limits row, PF.**
   - **Find:** "It is used up by 2031 at a $1m gift, but **$447k is never used at a $1.5m gift** [C]."
   - **Replace with:** "It is used up by 2031 at a $1m gift, but **$447k is never used at a $1.5m gift** [C]. This figure rests on the two floor/carryover readings in §5 [I]. If the 0.5% floor is not applied to carryovers absorbed in later years, it is about $437k [V wave 27]."
2. **§1, AGI limits row, DAF.**
   - **Find:** "nothing is left unused until the gift reaches $2m ($407k unused) [C]."
   - **Replace with:** "nothing is left unused until the gift reaches $2m ($407k unused; about $397k under the alternative floor reading in §5) [C/I; V wave 27]."
3. **§5, interpretations paragraph.**
   - **Find:** "These readings affect only H4 PF and the S3 rows."
   - **Replace with:** "These readings affect only H4 PF and the S3 rows. Under the alternative reading, the S3 unused amounts fall by about $10k each (PF $447k → about $437k; DAF $407k → about $397k). The $663k/$337k 2026 split does not change [V wave 27]."
