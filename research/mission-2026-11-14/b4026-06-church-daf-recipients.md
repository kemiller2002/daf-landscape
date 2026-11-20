# Churches as the unrated block of DAF dollars: who they are, who pays them, and whether their giving pages take DAF grants (P-B40N1202-B43N26-06, with P-B41N15-01)

**Date:** 2026-11-19 · **Task ID:** b4026-06 · **Builds on:** [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md) §4.1 and its "Validation corrections (wave 34B)"; [direction-faith-giving-platforms.md](direction-faith-giving-platforms.md); [direction-nonprofit-donate-pages.md](direction-nonprofit-donate-pages.md)

**Outputs**
- Script: [`scripts/mission_church_recipients.py`](../../scripts/mission_church_recipients.py). It is new. It imports `mission_recipient_basis_eligibility.py` (numerator, BMF join, filing history, rule order) and `mission_donate_page_scan.py` (robots, render, detector) without changing them.
- Data: [`data/mission-2026-11-14/church-daf-recipients-profile-2026-11-19.csv`](../../data/mission-2026-11-14/church-daf-recipients-profile-2026-11-19.csv). 1,677 rows in long format (§6).
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b4026-06.csv`](../../data/mission-2026-11-14/queue-proposals-b4026-06.csv), 5 rows.

Tags: **[F]** computed from filings or the BMF by the script · **[P]** quoted primary source · **[O]** observed on a fetched live page · **[S]** search-result statement · **[I]** inference.

## 0. Answer in brief

- **The block reproduces exactly.** 29,469 recipients and $6,177.5m of DAF-weighted dollars, which is 8.34% of the $74,073.8m top-50 FY2023–24 non-DAF-to-DAF total [F].
- **It is not all congregations.** By name rules, 52.2% of block dollars go to congregations (21,774 recipients, $3,226m). The rest goes to:
  - church-coded ministries and orders, 15.6% (Cru $92.5m, World Literature Crusade $87.9m, Wycliffe, Salvation Army units, Focus on the Family);
  - denominational bodies, 13.4% (the LDS Church $464.2m, USCCB $38.7m, dioceses);
  - schools and seminaries, 8.5%;
  - unclassified names, 10.4% [F/I].
  FOUNDATION 10 is the IRS "Church 170(b)(1)(A)(i)" code [P], not a congregation flag.
- **Concentration is extreme.** Gini 0.816 [F].
  - The top 1% (295 recipients) take 42.5% of dollars and the top 10% (2,947) take 74.5%. The bottom half take 4.2%.
  - The LDS Church alone takes 7.5%.
  - Among congregations only, the top 1% take 29.1% and the top 10% take 66.6% (Gini 0.757) [V wave 35C].
- **Grant size is modest.** Medians [F]:
  - per church, over two years: $39,057 (congregations $37,426) [V wave 35C];
  - per Schedule I line (one sponsor-year's total to one church): $17,479;
  - Schedule I's p10 line is $6,224, close to the $5,000 reporting threshold.
  - Mean per church: $209,629.
- **Faith sponsors send 22.1% of block dollars.** NCF, Servant Foundation (The Signatry) and Thrivent send 18.0%; four Jewish sponsors send 4.1%. Nationals send 74.2% and community foundations 3.1% [F]. These shares are within the top-50 frame. Across all itemising DAFRC panel sponsors plus four non-panel faith sponsors the block is $8,104.5m: faith sponsors send 30.2% (25.1% without the OJC Fund) and nationals 58.8% (b4026-06-01-faith-sponsors-outside-top50.md) [V wave 42B].
  - Faith sponsors hold only 10.0% of all top-50 dollars, so they are over-represented about 2.2× [F].
  - For congregations only the faith share is 21.2%; for all church-coded recipients, including filers, it is 25.7% [F].
  - **By sponsor, Fidelity Charitable is the largest source, at $2,157.9m (34.9%).** DAFgiving360 follows with $995.2m (16.1%), then NCF with $722.5m (11.7%) [F].
- **Denomination.** 47.8% of block dollars carry a group exemption number (357 distinct GENs), all of which resolve to a central organisation in the BMF [F].
  - The largest GENs are USCCB/Catholic (GEN 0928, $764.5m, 3,816 recipients), LDS (5376, $468.4m), PCA (8534, $168.3m), LCMS (1709), UMC (2573) and ELCA (9386).
  - Across all methods [F/I]:
    - generic Christian names: 19.3%;
    - Jewish: 14.5%;
    - Roman Catholic: 13.6%;
    - LDS: 7.6%;
    - Presbyterian/Reformed: 6.0%;
    - Baptist: 5.4%.
- **Geography.** By state [F]:
  - NY 12.3%, CA 10.2%, TX 7.8%, UT 7.8% (almost all LDS), FL 7.1% and CO 6.6% (Colorado Springs ministries).
  - Relative to all top-50 dollars, TX (7.8% vs 4.2%), FL, CO, GA and OK are over-represented; CA, MA and DC are under-represented.
- **Megachurches take little.** 54 of the 107 distinct Outreach 100 "Largest Churches" (2023, 2024) match a block EIN strictly. They hold $138.4m, which is 2.2% of block dollars and 4.3% of congregation dollars [F]. Loose matches raise this to 72 churches and $199.2m (3.2%/6.2%).
  - By grant size, 516 congregations with at least $1m hold 41.1% of congregation dollars [F].
- **Giving pages (P-B41N15-01, partial).** The sample was 50 seeded congregations. Websites were found for 21 of the 40 searched. 14 pages were read (10 giving pages and 4 homepages). **None showed any DAF option**: no DAFpay, no DAF Direct, no sponsor name, no DAF text and no EIN [O].
  - Subsplash appears on 5 of the 14 pages and Pushpay on 3 [O].
  - For comparison, 41.2% (75 of 182) of the top-300 recipients' donate pages show some DAF option, and religion's rate there is 3 of 13, both after the governing wave-24B correction [V wave 35C].

## 1. Method

1. **Numerator and block.**
   - `build_numerator`, `load_bmf`, `load_bmf_extra`, `load_history` and `units_b` are imported from `mission_recipient_basis_eligibility.py` and run on the same caches: `npcache`, `rcp/lines`, `rcp/bmf` and the IRS TEOS index 2019–2026.
   - The block is every recipient whose first failing central-rule reason is `no_efiled_990_church`: in the BMF, SUBSECTION 03, FOUNDATION 10, not a private foundation, not a DAFRC panel sponsor, and no 990/990-EZ/990-PF in the index.
   - The script recomputes 29,469 recipients and $6,177,546,936, matching the committed table.
   - Dollars are DAF-weighted: each sponsor-year's Schedule I lines × its DAF share of grants.
   - Lines are **per sponsor-year per recipient** (Schedule I Part II aggregates every grant to one recipient in one year) and omit recipients at or under $5,000.
2. **Comparison scopes.**
   - `block_congregations`: the block restricted to recipient type `congregation`.
   - `church_coded_all`: all 30,841 FOUNDATION 10 recipients, $7,275.9m (9.8%), whatever their filing status. 996 of them are CN-eligible filers ($749.2m) and 302 have fewer than three e-filed returns ($346.3m).
3. **Recipient type** (`rtype_of`, name rules in order).
   - The types are school/seminary (strict words), denominational body, congregation, school (college/university/institute), then ministry/order; anything else is unclassified.
   - An Outreach 100 match forces `congregation`.
   - **Audit:** in a random 80 block recipients (seed 7), all 72 labelled names read as consistent with their label. A validator's stratified draw (16 per type, seed 3503) found congregation labels right for 16 of 16 and school labels for 13 of 16, but ministry labels for 11 of 16 (2 congregations, 3 ambiguous centres) and denominational-body labels for only 7 of 16: parishes matched SYNOD or CORPORATION SOLE, and orders, Chabad bodies, a school and a social-service centre also landed there. The dollar effect is small, because LDS and dioceses dominate that type; names in it containing PARISH, CHURCH, CONGREGATION or TEMPLE hold $54.4m (0.9% of block) [V wave 35C]. 8 were unclassified, several of which look like congregations ("THE RIVER", "CHRIST CENTRAL"). The congregation share is therefore a lower bound [I].
   - Known mislabels among the top 50 congregations include Fellowship of Catholic University Students ($11.3m, which matches `FELLOWSHIP`) and the Protestant Episcopal Cathedral Foundation (Washington National Cathedral).
4. **Denomination.**
   - (a) **GEN.** The BMF `GROUP` field is the "four-digit internal number assigned to central/parent organizations holding group exemption letters" [P, IRS EO BMF data dictionary]. Each GEN is resolved to the BMF row with that GROUP and AFFILIATION 8 ("parent (group ruling) and is a church") or 6 ("parent… not a church") [P]. That row's name is classified by keyword (`FAMILIES`). 3,964 GENs have a central in the BMF; all 357 GENs in the block resolve.
   - (b) If the GEN gives no specific family, NTEE X22/X30/X40/X50/X70 is used [P, same dictionary].
   - (c) Otherwise the recipient's own name is used.
   - The method is recorded per recipient: GEN central name 42.5% of dollars, own name 38.6%, NTEE 9.8%, none 9.1%.
   - NTEE is blank for 55.1% of block dollars.
5. **Sponsor groups.**
   - **faith_christian:** NCF, Servant Foundation and Thrivent Charitable.
   - **faith_jewish:** Jewish Communal Fund, CJP, JCF San Francisco and JCF Los Angeles.
   - These are the top-50 sponsors that DAFRC types "Religiously-Affiliated", plus Servant Foundation, which DAFRC types National/Standard and the repo lists as faith (direction-sponsor-executive-compensation.md, faith_single_issue). That list also includes DonorsTrust, which is kept here in `other` ($32.9m, 0.5% of block); counting it would raise the faith share to 22.6% [V wave 35C].
   - **national:** all other DAFRC national sponsors.
   - **community_foundation:** community foundations.
   - **other:** Dechomai, DonorsTrust and the two universities.
6. **Megachurches.**
   - The Outreach 100 "Largest Churches in America" lists for 2023 and 2024 were fetched, 6 pages each (`?page=N`, 20 rows a page, 100 and 101 rows). outreach100.com robots.txt is `User-agent: * / Disallow:` (allow all), HTTP 200 for all 12 pages.
   - **Matching:** same state, same abbreviation-expanded city, and every list-name token (after stop words such as CHURCH and INC) present in the BMF name.
     - `strict`: the BMF name adds only COMMUNITY/OF/COUNTY or city/state words.
     - `loose`: any superset.
   - Loose matches include true pairs (Life.Church = LIFE COVENANT CHURCH INC; Saddleback = SADDLEBACK VALLEY COMMUNITY CHURCH; The Summit Church = SUMMIT CHURCH-HOMESTEAD HEIGHTS BAPTIST) and false ones (Woodlands Church → First Baptist Church of the Woodlands; Faith Church → Faith Lutheran). Loose matches are therefore reported only as an upper bound. On reading, 16 of the 18 loose EINs are true pairs, and the two false ones hold $0.9m, so the loose tier (about $198.3m without them) is close to a point estimate. Free Chapel (Gainesville, GA; $8.1m) is a true list church missed because Outreach places it in Florida [V wave 35C].
   - Outreach describes its list as self-reported Lifeway survey data plus Hartford Institute public data [P].
7. **Concentration.** Shares of the top k% by DAF-weighted dollars, Lorenz points at 5% steps (smallest first), and Gini.
8. **Giving pages (P-B41N15-01).**
   - **Sample.** 50 congregations from the block, seeded (20261119). 25 were drawn from the top decile by dollars and 25 from the rest, so the sample is dollar-stratified, not proportional.
   - **Websites.** Churches file no 990, so there is no `WebsiteAddressTxt`. One web search per congregation (name + city + state) was run for 40 of the 50. A URL was used only when a result named it as that congregation's site; the 21 used, with notes, are in `SAMPLE_SITES`. The 10 congregations in `SITE_NOT_SEARCHED` were not searched, for time.
   - **Scan.** The repo census's own `stage_scan` ran in a scratch work directory. It checks robots.txt for every host first (200 parsed for `*`; 404 means no rules; anything else is unreadable and the host is not fetched), loads the homepage and one giving link with headless Chrome, and applies its `detect` (DAFpay/Chariot, DAF Direct, sponsor names and links, DAF text, own EIN, DAF-adjacent processors).
   - A church-platform pattern set was added: Pushpay, Tithe.ly, Subsplash, Planning Center/Church Center, Givelify, Overflow, Realm, Vanco, Kindrid, EasyTithe and an NCF link.
   - The census's `report` stage was not run, because it writes the committed census CSV.
   - The user agent is the census's generic one. There were no logins and no forms.

## 2. Reproduction

```
S=<scratchpad>
python3 scripts/mission_church_recipients.py . --np-cache $S/npcache --lines-cache $S/rcp/lines \
    --bmf-dir $S/rcp/bmf --index-dir $S/irs --outreach-dir $S/q2606/outreach [--fetch-outreach] \
    [--donate-work $S/q2606/donate] [--sample-out FILE] [--dump-block FILE]
```
- Without `--donate-work`, the `donate_scan:*` rows are omitted. A full run takes about 1 minute, plus about 3 minutes to render.
- Page renders are cached in the work directory. robots.txt is re-checked on every run, so the scan statuses can change between runs. One host changed: svac-cma.org returned robots HTTP 409 on the final run.

## 3. Results

### 3.1 What the block contains (recipient type, `block:recipient_type`)

| Type | Recipients | DAF-weighted $m | Share of block $ | Mean $ per recipient | Faith-sponsor share of the type's $ |
|---|---|---|---|---|---|
| congregation | 21,774 | 3,226.0 | 52.2% | 148,159 | 21.2% |
| ministry_or_order | 2,219 | 963.3 | 15.6% | 434,122 | 41.9% |
| denominational_body | 1,051 | 824.9 | 13.4% | 784,863 | 4.7% |
| unclassified | 2,907 | 641.0 | 10.4% | 220,493 | 25.8% |
| school_or_seminary | 1,518 | 522.3 | 8.5% | 344,102 | 14.2% |

The faith-sponsor column is Christian plus Jewish faith sponsors, from `block:rtype_x_sponsor_group` [F]. **Faith sponsors are most important for parachurch ministries, not congregations** [F]: Christian faith sponsors alone send 40.4% of ministry dollars, against 17.3% of congregation dollars.

### 3.2 Concentration (`block:concentration`, `block:lorenz`)

| Scope | n | Gini | Top 0.1% | Top 1% | Top 10% | Top 100 | Bottom 50% |
|---|---|---|---|---|---|---|---|
| block | 29,469 | 0.816 | 22.4% | 42.5% | 74.5% | 31.7% | 4.2% |
| block_congregations | 21,774 | 0.757 | 8.7% | 29.1% | 66.6% | 20.5% | 5.9% [V wave 35C] |
| church_coded_all | 30,841 | 0.833 | — | — | — | — | — |

Lorenz points for the block (smallest first; cumulative share of dollars): 50% of churches → 4.2%; 80% → 15.2%; 90% → 25.5%; 95% → 36.1% [F].

**Top block recipients (DAF-weighted, FY2023–24 combined)** [F]:

| # | Recipient (BMF) | State | Type | $m | Largest sponsor |
|---|---|---|---|---|---|
| 1 | The Church of Jesus Christ of Latter-day Saints | UT | denominational body | 464.2 | Fidelity |
| 2 | Come and See Foundation | CO | ministry (family unclassified) [V wave 35C] | 135.9 | Servant Foundation |
| 3 | Campus Crusade for Christ (Cru) | FL | ministry | 92.5 | NCF |
| 4 | World Literature Crusade | CO | ministry | 87.9 | Servant Foundation |
| 5 | Wycliffe Bible Translators | FL | ministry | 42.5 | NCF |
| 6 | The Salvation Army (GA) | GA | ministry | 41.7 | Fidelity |
| 7 | United States Catholic Conference | DC | denominational body | 38.7 | Goldman Sachs DAF |
| 8 | Amidei Zion of Bobov | NY | unclassified | 38.0 | Fidelity |
| 9 | Focus on the Family | CO | ministry | 37.6 | NCF |
| 10 | Kollel International | NJ | school | 34.4 | Fidelity |
| 11 | Life Covenant Church (Life.Church) | OK | congregation | 29.7 | Servant Foundation |

The top 50, with GEN, family and sponsor counts, are in `block:top_recipient` and `block_congregations:top_recipient`. The largest congregations are Life.Church ($29.7m), Congregation Ohr Torah ($27.3m), Venture Church Naples ($16.4m), North Point Ministries ($15.6m) and Congregation Emanu-El SF ($14.5m).

### 3.3 Size (`size_band`, `size_quantile_*`)

| Per church, FY2023–24 | <$10k | $10–25k | $25–50k | $50–100k | $100–250k | $250k–1m | $1–10m | ≥$10m |
|---|---|---|---|---|---|---|---|---|
| Block recipients | 4,206 | 6,935 | 5,598 | 4,754 | 4,243 | 2,844 | 846 | 43 |
| Share of block $ | 0.5% | 1.9% | 3.3% | 5.5% | 10.8% | 21.5% | 31.7% | 24.9% |
| Congregations | 3,098 | 5,252 | 4,316 | 3,558 | 3,090 | 1,944 | 504 | 12 |
| Share of congregation $ | 0.7% | 2.8% | 4.8% | 7.8% | 15.0% | 27.8% | 35.2% | 5.8% |

- **Per church:** p10 $8,354; p25 $15,751; median $39,057; p75 $110,616; p90 $319,807; p99 $2.34m [F].
- **Per Schedule I line:** median $17,479; p90 $100,000. For congregations the line median is $17,233 and the mean is $49,741 [F].
- Churches average 1.97 sponsors, and 57.5% have exactly one sponsor [F].
- These figures are not per-grant sizes. Fidelity reports an implied ≈ $2,815 average religion grant (repo, faith doc §3). One Schedule I line sums all grants from one sponsor in a year.

### 3.4 Denomination (`denomination_family`, `gen`, `ntee`)

**Largest group exemption numbers in the block** (central organisation's BMF name) [F]:

| GEN | Central organisation (BMF) | Recipients | $m | Share |
|---|---|---|---|---|
| — | none | 13,239 | 3,224.9 | 52.2% |
| 0928 | United States Catholic Conference | 3,816 | 764.5 | 12.4% |
| 5376 | The Church of Jesus Christ of Latter-day Saints | 8 | 468.4 | 7.6% |
| 8534 | Presbyterian Church in America | 649 | 168.3 | 2.7% |
| 1709 | Lutheran Church Missouri Synod | 1,282 | 100.6 | 1.6% |
| 2573 | General Council on Finance & Admin. of the UMC | 838 | 93.7 | 1.5% |
| 9386 | Evangelical Lutheran Church in America | 1,268 | 92.1 | 1.5% |
| 1678 | General Council of the Assemblies of God | 656 | 79.6 | 1.3% |
| 1729 | Evangelical Free Church of America | 436 | 66.8 | 1.1% |
| 3741 | Protestant Episcopal Church in the USA | 447 | 51.9 | 0.8% |
| 1617 | Presbyterian Church (USA) | 404 | 50.4 | 0.8% |

Two single-organisation group rulings rank among these by dollars and are left out of the table: GEN 3864 (Campus Crusade for Christ, 1 recipient, $92.5m, 1.5%) and GEN 4067 (World Literature Crusade, AFFILIATION 6, 1 recipient, $87.9m, 1.4%) [V wave 35C].

**Family, block and congregations** [F, by method in §1.4]:

| Family | Block $ share | Congregation $ share |
|---|---|---|
| other Christian (generic name) | 19.3% | 27.6% |
| Jewish | 14.5% | 12.3% |
| Roman Catholic | 13.6% | 7.9% |
| unclassified | 11.2% | 0.2% |
| other named Protestant (EFCA, C&MA, Covenant, Bible church, etc.) | 8.8% | 12.7% |
| Latter-day Saints | 7.6% | <0.1% |
| Presbyterian/Reformed | 6.0% | 10.6% |
| Baptist | 5.4% | 8.8% |
| Lutheran | 3.7% | 5.8% |
| Pentecostal | 2.6% | 4.2% |
| Methodist | 2.0% | 3.6% |
| Episcopal/Anglican | 1.2% | 2.0% |
| other faith, Orthodox, Muslim, Unitarian, Adventist | 2.7% | 1.9% |
| ambiguous (temple, congregation, sanctuary etc., no family) | 1.4% | 2.6% [V wave 35C] |

- **Catholic dollars are thin per parish.** 2,576 Catholic congregations average $98k [F]. The Catholic total is held up by the USCCB, dioceses, orders and schools.
- **Faith-sponsor share by family** [F]:
  - Christian faith sponsors send 30% of generic-Christian dollars, 33% of Pentecostal, 22% of Baptist, 20% of Presbyterian and 17% of Lutheran, but only 2% of Catholic.
  - Jewish faith sponsors send 24% of Jewish-family dollars.

### 3.5 Sponsor mix (`sponsor`, `sponsor_group`)

| Sponsor group | Block $m | Share of block $ | Group's share of all top-50 $ | Share of group's own $ going to the block | Congregations: share |
|---|---|---|---|---|---|
| national | 4,584.9 | 74.2% | 71.2% | 8.7% | 76.1% |
| faith_christian | 1,111.5 | 18.0% | 6.6% | 22.7% | 17.4% |
| faith_jewish | 254.0 | 4.1% | 3.4% | 10.2% | 3.8% |
| community_foundation | 194.2 | 3.1% | 18.0% | 1.5% | 2.7% |
| other | 33.0 | 0.5% | 0.8% | 5.5% | 0.1% |

**By sponsor** (block $m; share of the sponsor's own DAF-weighted dollars that go to the block) [F]:
- Fidelity 2,157.9 (10.6%)
- DAFgiving360 995.2 (9.9%)
- NCF 722.5 (18.4%)
- Servant Foundation 343.7 (40.0%)
- Vanguard 331.0 (7.7%)
- NPT 269.7 (3.7%)
- Morgan Stanley GIFT 218.7 (10.6%)
- AEF 163.8 (9.1%)
- Goldman Sachs 163.4 (3.7%)
- JCF NY 149.6 (8.8%)
- Raymond James 84.5 (18.5%)
- JCF LA 81.6 (36.1%)
- US Charitable Gift Trust 67.2 (19.5%)
- Thrivent 45.4 (39.7%)

Among community foundations, SVCF sends 0.5% and Chicago 1.1%.

**Answer to the faith-versus-other question** [F]:
- Faith sponsors (Christian and Jewish) send **22.1%** of block dollars, **21.2%** of congregation dollars and **25.7%** of all church-coded dollars.
- Non-faith sponsors send the rest: nationals about three-quarters and community foundations 3%, within the top-50 frame; across all itemising panel sponsors nationals send about three-fifths (58.8%; 63.1% without the OJC Fund) [V wave 42B].
- Because faith sponsors outside the top-50 frame are missing (WaterStone, NCF affiliates, Catholic and Jewish community foundations), the true faith share of all DAF dollars to churches is likely higher [I]. P-B4026-06-01 tested this: 30.2% across all itemising panel sponsors (33.7% adding only faith sponsors outside the top 50). About half of the added $1,080.3m is one Brooklyn pass-through sponsor, the OJC Fund ($545.3m), which ranks 22nd by FY2023 DAF grants but 284th by DAF assets; without it the all-panel share is 25.1% [V wave 42B].

### 3.6 Megachurches (`megachurch`, `outreach100_match`)

| Tier | Recipients | $m | Share of block $ | Share of congregation $ |
|---|---|---|---|---|
| Outreach 100 2023/24, strict match | 54 | 138.4 | 2.2% | 4.3% |
| Outreach 100, strict or loose | 72 | 199.2 | 3.2% | 6.2% |
| Congregations with ≥$1m DAF-weighted | 516 | 1,325.0 | — | 41.1% |
| Congregations with ≥$250k | 2,460 | 2,222.4 | — | 68.9% |
| Top 100 congregations by $ | 100 | 661.6 | — | 20.5% |

- 107 distinct churches appear on the two lists. 72 match a block EIN (54 strictly). None matches a FOUNDATION 10 EIN outside the block: the `church_coded_all` match counts equal the block's.
- Large list churches get little from top-50 DAFs. Examples [F]:
  - Lakewood Church (#3–4): $0.73m;
  - Church of the Highlands (#2): $9.6m;
  - North Point (#5–11): $15.6m;
  - Life.Church (#1, loose): $29.7m.
- Dream City Church, The Church of Eleven22, LCBC and Free Chapel did not match by name. "Free Chapel Worship Center Inc" (GA, $8.1m) is in the block, but the Outreach list places the church in Gainesville, FL, so the city rule rejects it.
- **The DAF-heavy congregations are mostly affluent suburban or urban churches and synagogues, not the largest by attendance** [I]. Examples are Venture Church Naples, Perimeter, Ohr Torah, Emanu-El, B'nai Jeshurun and Central Synagogue.

### 3.7 Giving pages of 50 seeded congregations (P-B41N15-01; `donate_scan:*`)

| Status | n |
|---|---|
| Giving page scanned | 10 |
| Homepage only (no give/donate link found) | 4 |
| Homepage unreachable (Life.Church HTTP 403; hillspringchurch.cloversites.com 404; fbcjax.com → firstbaptist.com timeout) | 3 |
| robots.txt unreadable, not fetched (newcovenantbible.org, dmgospelassembly.org: network error; tbdcheshire.org: 406; svac-cma.org: 409) | 4 |
| Searched, no site named in results | 19 |
| Not searched (time) | 10 |

- **No host disallowed the pages by robots.txt.** Every site was checked before fetching.
- **0 of 14 pages read (10 giving, 4 homepages) show any DAF option.** That covers DAFpay/Chariot, DAF Direct, sponsor names, "donor-advised"/"DAF" text and an own-EIN display [O]. The 95% Wilson upper bound on 0/14 is 21.5% [I].
- **Platforms on the 14 pages:** Subsplash 5, Pushpay 3, Planning Center 1, other form vendors 3, none detected 7 (3 of the 10 giving pages and all 4 homepages) [O] [V wave 35C].
  - The scanned giving pages are on Subsplash (Calvary Chapel Edmonds, Cherry Creek Presbyterian, Christ Central Durham, Wellspring), Pushpay (Chesterfield Presbyterian, RockHarbor, Compass Bible with Planning Center) and own forms (Sinai Temple, St. Ann Marietta, First UMC Madison).
  - The faith doc found that none of these platforms offers a DAF grant rail [O, repo]. Subsplash publishes DAF instructions for congregations, but none of the four Subsplash pages showed them.
- **Comparison.** The top-300 donate-page census, as corrected in wave 24B, found 41.2% (75/182) with any DAF option overall and 3 of 13 for religion (all parachurch, no DAFpay) [V wave 35C]. For congregations in the church block the rate observed is 0 of 14.
- Detail is in `donate_scan:congregation`. Each row has its site, its source note, the giving URL, the flags and the robots result.

## 4. How this relates to the faith-platform direction doc

[direction-faith-giving-platforms.md](direction-faith-giving-platforms.md) argued that religion's low donate-page DAF rate reflects six things:
- E1: the scan sees parachurch ministries, not congregations;
- E2: many small grants;
- E3: faith sponsors pay churches by sponsor-initiated ACH or check;
- E4: church platforms have no DAF rail;
- E5: legal-status friction;
- E6: dues and tithes go through church channels.

This study tests several of those points directly:

- **E1 confirmed and extended.** Even the "church" block is 48% non-congregational by dollars (§3.1). The congregations themselves were not covered by the earlier scan, and the first direct read of their pages finds no DAF option on any of 14 (§3.7) [F/O].
- **E2 partly.** Schedule I lines to congregations have a median of $17k and p10 of $6.4k, and 57.5% of churches have one sponsor (§3.3). Small per-grant sizes cannot be seen in Schedule I [F/I].
- **E3 quantified.** Faith sponsors send 21–26% of church dollars within the top 50, against 10% of all top-50 dollars; across all itemising panel sponsors they send 30.2% of block dollars and 31.8% of church-coded dollars (25.1% of the block without the OJC Fund) [V wave 42B]. Servant Foundation and Thrivent send about 40% of their own dollars to this block (§3.5).
  - But **about three-quarters of top-50 church DAF dollars come from national sponsors**, led by Fidelity and DAFgiving360; across all itemising panel sponsors the national share is about three-fifths (58.8%) [V wave 42B]. Those are sponsors that are reached through DAFpay or sponsor links.
  - So "faith sponsors pay without a donate page" explains about a fifth to a quarter of the dollars within the top 50 (22.1% of the block, 25.7% of all church-coded dollars) [I] [V wave 35C], and about three-tenths across all itemising panel sponsors (30.2% and 31.8%; b4026-06-01) [V wave 42B].
  - Most church DAF money arrives from nationals with no visible DAF option on the church's page. That fits portal-initiated grants by donors who already know the church's EIN and address [I].
- **E4 consistent.** Every platform detected on the scanned pages (Subsplash, Pushpay, Planning Center) is one the faith doc found has no DAF grant rail [O].
- **E5.** No church in the sample showed its EIN, which national sponsors' grant forms ask for [O].
- **Rating context.** The block is the 8.3 points of DAF dollars that Charity Navigator cannot rate because churches file no 990. The faith doc notes ECFA/MinistryWatch as the only raters covering some ministries. Their coverage of the block's ministries (Cru, Wycliffe, Focus, Navigators) could be checked; congregations remain unrated [I].

## 5. Limits

1. **Top-50 frame only.** Sponsors outside the 50 largest by DAF assets are absent, including WaterStone, NCF affiliates and most Jewish and Catholic foundations (b4026-06-01 adds them: block $8,104.5m, faith share 30.2%; ranking by assets also omits high-throughput sponsors such as the OJC Fund, 22nd by FY2023 DAF grants and 284th by DAF assets) [V wave 42B]. Renaissance and BofA do not itemise Schedule I. DAF-weighting assumes each sponsor-year's DAF share applies to all its lines.
2. **Schedule I lines.** They aggregate per recipient-year and omit recipients at or under $5,000. Church grants sit close to that threshold, so the dollar total and the small-church count are understated by an unknown amount (proposal 05).
3. **Name rules.** Recipient type and denomination family come from keyword rules on BMF names. GEN central names are authoritative for most of the 47.8% of dollars with a GEN; elsewhere names are an [I] classification. Two exceptions: the BMF central name for GEN 2573 (UMC) is truncated, so its subordinates fall back to own-name rules (64 recipients, $12.5m, not labelled Methodist), and GEN 2269 (Converge, the Baptist General Conference; $49.7m) has only $12.0m labelled Baptist. Methodist and Baptist shares are therefore understated by up to about 0.2 and 0.6 points [V wave 35C]. Known mislabels are listed in §1.3.
4. **"Church" means the IRS code.** FOUNDATION 10 includes auxiliaries, conventions and schools. The BMF is the 2026-11 extract and is applied to FY2023–24 dollars.
5. **Megachurch matching** is name + city + state against one public list. Legal names that differ from brand names are missed, and loose matches include errors. Outreach's list is self-reported and partly secondary data [P].
6. **Giving pages.** The test is small and partial: n = 14 pages read, with websites found by search for only 21 of 40 searched congregations. Congregations with findable websites may differ from those without. The sample is dollar-stratified (half from the top decile), not proportional. Static detection cannot see options shown only after interaction, such as a "DAF" method inside a Pushpay modal; the census has the same limit.
7. **Search-sourced URLs** are [S]. Some come from third-party directories (svac-cma.org, sfefc.org, dmgospelassembly.org, rockharbor.tv, newcovenantbible.org) and are not confirmed by the church.

## 6. Data dictionary: `church-daf-recipients-profile-2026-11-19.csv`

Long format. Each row is one statistic or one entity.

| Field | Meaning |
|---|---|
| `section` | `<scope>:<table>`. Scopes are `block` (29,469 `no_efiled_990_church`), `block_congregations` (block ∩ type congregation), `church_coded_all` (all FOUNDATION 10 recipients) and `donate_scan`. Tables: `summary`, `concentration`, `lorenz`, `top_recipient`, `recipient_type`, `rtype_x_sponsor_group`, `denomination_family`, `denomination_method`, `gen_coverage`, `gen`, `ntee`, `size_band`, `size_quantile_church`, `size_quantile_line`, `state`, `sponsor`, `sponsor_group`, `megachurch`, `family_x_sponsor_group`, `outreach100_match`, `summary`/`congregation` (donate_scan) |
| `key` | Row key: statistic name, EIN, GEN, family, state, band, sponsor EIN, `family\|sponsor_group`, `YEAR#rank` (Outreach) or Lorenz x |
| `label` | Name (recipient BMF name, GEN central-organisation name, sponsor DAFRC name, Outreach church name) |
| `detail` | Context. top_recipient: city, state, type, GEN, family, sponsor count, top sponsor. gen: central EIN and family. state: that state's share of all top-50 dollars. sponsor: group. donate_scan: stratum, site, giving URL |
| `recipients` | Count of recipients (for Outreach rows, 1 = matched) |
| `lines` | Schedule I lines (sponsor-year × recipient) |
| `usd_daf_weighted` | FY2023–24 DAF-weighted Schedule I dollars, rounded |
| `usd_schedule_i` | The same before DAF-weighting |
| `share_of_block_dw` | Share of the scope's DAF-weighted dollars |
| `cum_share_of_block_dw` | Cumulative share (top_recipient by rank, size_band ascending, Lorenz) |
| `value` | The statistic. For group rows it is the mean $ per recipient unless `note` says otherwise. sponsor: share of the sponsor's own dollars going to the scope. sponsor_group: share of the group's own dollars. `*_x_sponsor_group`: share of that family or type's dollars sent by the group. outreach100_match: matched EIN. donate_scan: scan status |
| `note` | Definition of `value`, Outreach match tier and BMF name, or donate-scan flags, platforms, robots result and site source |
| `source` | Primary sources for the row |

## 7. Source register

| ID | Source | Accessed | Used for | Tag |
|---|---|---|---|---|
| S1 | IRS Form 990 Schedule I Part II, top-50 DAFRC sponsors FY2023–24, via the repo caches (GivingTuesday mirror of IRS TEOS e-file XML; [IRS TEOS index](https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv)) | caches 2026-11-14/15 | dollars | F |
| S2 | [IRS EO BMF extract](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf) (eo1–eo4, eo_pr, eo_xx; repo cache) | 2026-11-14 | FOUNDATION, GROUP, AFFILIATION, NTEE_CD, STATE, CITY | F |
| S3 | [IRS EO BMF data dictionary, eo-info.pdf](https://www.irs.gov/pub/foia/ig/tege/eo-info.pdf): GEN definition; AFFILIATION 6/8/9; FOUNDATION 10 "Church 170(b)(1)(A)(i)"; NTEE X20–X99 | 2026-11-19 (robots allow) | definitions | P |
| S4 | [Outreach 100 Largest Churches 2023](https://outreach100.com/largest-churches-in-america/2023) and [2024](https://outreach100.com/largest-churches-in-america/2024), pages 1–6 | 2026-11-19 (robots allow all) | megachurch list; method note (Lifeway survey + Hartford Institute) | P |
| S5 | `b40n1202-b43n26-recipient-basis-and-rating-eligibility.md` §4.1 and the wave 34B corrections | repo | block definition, 29,469 / $6.18bn | R |
| S6 | `direction-faith-giving-platforms.md` §0, §3–4 (E1–E6; platform DAF support; Fidelity religion benchmark) | repo | §4 comparison | R |
| S7 | `direction-nonprofit-donate-pages.md` and `scripts/mission_donate_page_scan.py` (robots rules, render, detector; 40.3% any-DAF; religion 3/14) | repo | method and benchmark | R |
| S8 | `direction-sponsor-executive-compensation.md` (faith_single_issue sponsor list) | repo | sponsor grouping | R |
| S9 | Web search results, 2026-11-19, one per congregation (40 queries); the URLs used and their notes are in `SAMPLE_SITES` in the script. Examples: [sinaitemple.org](https://www.sinaitemple.org/), [compasschurch.org](https://www.compasschurch.org/), [fumc.org](https://fumc.org/), [life.church](https://life.church/) | 2026-11-19 | congregation websites | S |
| S10 | Congregation websites and giving pages listed in `donate_scan:congregation` (robots.txt checked first for each host) | 2026-11-19 | DAF-option flags, platforms | O |
