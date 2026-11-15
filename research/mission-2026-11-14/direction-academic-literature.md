# Academic and policy literature on donor-advised funds, 2021–2026

**Queue item:** P-NEW-ACA-01 (new direction from the owner). **Date:** 2026-11-15. **Recency rule:** works published in 2021 or later. Older work appears only as dated context and is marked as such.

**Outputs**
- This review.
- [`data/mission-2026-11-14/daf-literature-2021-2026.csv`](../../data/mission-2026-11-14/daf-literature-2021-2026.csv): 40 rows. 33 works were reviewed, 6 are listed from metadata only, and 1 is pre-2021 context.
- [`data/mission-2026-11-14/queue-proposals-batch39-n8.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n8.csv): 3 queue proposals.

**Comparison baseline:** [DAF-INDUSTRY-REPORT-2026-11.md](../DAF-INDUSTRY-REPORT-2026-11.md) §1, §3, §6 and §11, read with the governing validation corrections (waves 4 and 18–23). None of those corrections touches the payout, regulation or incentive figures used here. The figures below are the consolidated ones:
- aggregate payout of 23.7–28.4%;
- net payout of 19.0–21.5% (FY2021–24 pooled);
- batch-34 netting: payout falls from 25.9% to 22.8%;
- sponsor medians: about 11–12.5% for sponsors with at least $1m, about 20% for nationals, about 11% for community foundations;
- accounts: 79.5% sit at processors; 2.59m accounts on the strict basis.

---

## 1. Method and compliance

**Discovery**
- Crossref public API (`query.bibliographic` and `query.title`, `from-pub-date:2021-01-01`), about 16 queries. This was the main index.
- WebSearch, used for discovery only.
- The DAF Research Collaborative (DAFRC) research listing.
- The OpenAlex free daily budget for this IP was already used up (HTTP 429). Semantic Scholar returned 429 on every query. Google Scholar was not used.

**Retrieval**
- Every reviewed entry was retrieved in one of three ways: a Crossref record with its abstract, a publisher or repository page, or a downloaded PDF that I read. The `retrieval_evidence` column in the CSV records which.
- No citation comes from memory or from a search snippet alone.
- Where I relied on a secondary report of figures (L30, L31), the row says so.

**robots.txt (checked on every host before fetching)**
- **Hosts that disallow Claude or AI agents, so nothing was fetched from them:** philanthropy.com (ClaudeBot/anthropic-ai `Disallow: /`), theconversation.com (Claude-User/ClaudeBot `Disallow: /`), academiccommons.columbia.edu (anthropic-ai `Disallow: /`) and jstor.org (ClaudeBot).
- **Paths disallowed for all agents, so nothing was fetched from them:** ccc.bc.edu `/content/dam/`, which holds the Andreoni–Madoff 2021 PDF, and michiganfoundations.org `/system/files/documents`, which holds the CMF 2021 PDF.
- **Allowed by robots.txt but blocked by a bot challenge or 403, so not reviewed:** papers.ssrn.com (allowed with crawl-delay 5), scholarworks.gvsu.edu `viewcontent.cgi`, bakerinstitute.org and philanthropyroundtable.org.

No logins, form submissions or outreach.

---

## 2. Headline flags: findings that could change the report's conclusions

| # | Finding | Works | Report text affected | Proposed handling |
|---|---|---|---|---|
| F1 | **Account-level payout evidence exists.** It comes from voluntary samples. The median account pays out about 9% (three-year average), 22% of accounts made no grants in 2020–22, and the mean is 18%. Among CF and religious sponsors only, the four-year median is 11% and 35% of accounts pay out under 5%. | L15 [DAFRC 2024, doi:10.4087/ymfd7624](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf); L13 [DAFRC 2022](https://www.dafresearchcollaborative.org/s/DAFRC-Patterns-and-Trends-Report_Executive-Summary.pdf) | §1: "Fund-level payout is not public" | Keep the sentence for *public filings*, and add that voluntary account samples put the median account at about 9%. This does not contradict the aggregate of 23.7–28.4%: a few large, fast-paying accounts carry the aggregate. Sample representativeness is unknown. |
| F2 | **Sponsor orientation predicts lower payout.** Among national sponsors, websites that stress donor benefits predict larger DAF assets, and the effect runs mostly through *lower payout*, not higher contributions. | L18 [Flannery & Mittendorf 2025, NVSQ, doi:10.1177/08997640251331853](https://doi.org/10.1177/08997640251331853) | §3 incentive table: "asset-based fee alignment … effect on payout unsupported [RT]" | Candidate to move from *unsupported* to *suggestive*, with the caveat that the measure is marketing language, not fee structure, and the result is correlational. Needs a validator decision. |
| F3 | **Community foundations may send the largest share of grants to other DAFs.** In the California AG audit, about 11% of all DAF grants went to other DAFs: 18% at CFs, 10% at commercial sponsors, 5% at mission-based sponsors. | L29 [CA AG 2022](https://oag.ca.gov/system/files/media/donor-advised-funds-overview.pdf) | §1 payout bullet and §11.1, which frame sponsor-to-sponsor transfers as mainly a national-sponsor issue; batch-34 R5 netting | The overall share agrees with the repo's 10–18%. The CF result could mean R5 under-nets CF payout. Queue proposal P-B39N8-02. |
| F4 | **The dispersion of published payout figures is mostly definitional.** IPS reports a 9.7% median sponsor payout using grants ÷ (year-end assets + grants), against NPT's 23.9% aggregate. Leff (2025) calls the spread unresolved. | L28 [IPS 2025](https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf); L20 [Leff 2025](https://nyujlpp.org/wp-content/uploads/2026/02/JLPP_28-1-Leff.pdf) | §1 payout | No conclusion changes. The repo can publish a definition bridge (P-B39N8-01). |

**Nothing found overturns a headline conclusion:**
- No 2021–26 work disputes the size of the DAF market, its concentration by layer, or the vendor findings.
- No causal study of crowd-out or of DAF opening on household giving was found for 2021–26.
- No DAF-specific econometric study of TCJA or OBBBA bunching was found. Walker (2023) is descriptive, and Han–Hungerman–Ottoni-Wilhelm (2024) is about general giving.

---

## 3. Empirical economics and finance

**L01 — Grennan, J. (2022). "Social Change through Financial Innovation: Evidence from Donor-Advised Funds." *Review of Corporate Finance Studies* 11(3):694–735.** [doi:10.1093/rcfs/cfac017](https://doi.org/10.1093/rcfs/cfac017). An earlier SSRN version is [doi:10.2139/ssrn.3925198](https://doi.org/10.2139/ssrn.3925198).
- **Method:** new sponsor data, a classification of DAFs by economic purpose, and conditional correlations.
- **Finding:** growth is fastest among DAFs that offer fintech tools, liquidity transformation of complex assets, and DEI-focused grantmaking. DAFs with an innovative service style grant more to high-inequality areas and in times of need.
- **Relation to repo:** *extends* §2, §5 and §11.2. It supports classifying sponsors by product and technology rather than by legal type.

**L13 — Vance-McMullen, D. & Heist, H. D. (DAFRC, 2022). *Donor-Advised Fund Account Patterns and Trends (2017–2020).*** [PDF](https://www.dafresearchcollaborative.org/s/DAFRC-Patterns-and-Trends-Report_Executive-Summary.pdf)
- **Data:** 13,000 accounts at 21 community foundations and religious sponsors. National sponsors are excluded.
- **Finding:** the median four-year account payout is 11% (13% for spendable DAFs). 35% of accounts pay out under 5% and 13% pay out 50% or more. 10% are endowed.
- **Relation to repo:** *extends* §1 (F1).
- **Note:** secondary sources, including a search summary seen in this run, attribute the 52%/35% split to the 2024 National Study. It belongs to this 2022 report.

**L15 — Heist, Vance-McMullen, Kienker & Williams (DAFRC, 2024). *The National Study on Donor Advised Funds.*** [doi:10.4087/ymfd7624](https://doi.org/10.4087/ymfd7624); [executive summary](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf)
- **Data:** over 50,000 accounts at 111 voluntary programs (nationals, CFs and religious sponsors), with over 600,000 contributions and 2.25m grants, 2014–2022.
- **Payout:** the median three-year payout is 9% (15% excluding inactive accounts) and the mean is 18%. 22% of accounts were inactive in 2020–22, and 45% of those opened in 2020 or later.
- **Timing:** 57% of contributions arrive in Q4, against 32% of grants.
- **Anonymity:** under 4% of grants are anonymous.
- **Spend-down:** 58% of accounts had granted out 100% of their original contribution after eight years.
- **Relation to repo:** *extends* §1 and §3 (F1). Gates Foundation funded.

**L16 — Flannery, H. & Mittendorf, B. (2024/2025). "Reshaping Charity Channels: How Assets Flow into and out of Donor-Advised Funds."** [doi:10.2139/ssrn.4683236](https://doi.org/10.2139/ssrn.4683236); published as a Springer chapter, [doi:10.1007/978-3-031-74994-0_4](https://doi.org/10.1007/978-3-031-74994-0_4).
- **Data:** Form 990, 2020–22.
- **Finding:** DAFs take in disproportionately more noncash gifts. Funds cycle between sponsors. DAF grants tilt toward education and religion and away from human services and health.
- **Relation to repo:** *agrees* on cycling. The repo puts transfers between sponsors at 11.2% of top-50 FY2023 Schedule I dollars, with education at 27.0%, religion 13.1%, human services 13.5% and health 11.7% ([recipient sectors](../../data/mission-2026-11-14/daf-grant-recipient-sectors-top50.csv)). The religion tilt is national-only: 14.1% at nationals against 2.9% at CFs ([recipients direction](direction-recipients-impact-matching.md)). The comparison with other giving channels is new.

**L17 — Flannery & Mittendorf (2025). "Are Donor-Advised Funds Facilitating Opaque Giving to Politically Engaged Charities?" *Nonprofit Policy Forum* 17(1–2):99–130.** [doi:10.1515/npf-2024-0028](https://doi.org/10.1515/npf-2024-0028)
- **Finding:** DAF sponsors grant to politically engaged charities at about 1.7 times the rate of other giving sources, and to anti-government and hate groups at about 3.5 times. DAFs supply more than a quarter of those groups' contributions. The tilt is larger where more sponsor revenue comes from private foundations.
- **Relation to repo:** *extends*. This is a regulatory-pressure topic the repo does not cover (§6, §4 grant review).

**L18 — Flannery & Mittendorf (2025). "Charitable Objectives or Donor Benefits?" *NVSQ* 55(1):57–89.** [doi:10.1177/08997640251331853](https://doi.org/10.1177/08997640251331853)
- **Relation to repo:** see F2.
- **Independence:** Flannery is research director of the IPS Charity Reform Initiative, a reform advocate. The same note applies to L16 and L17.

**L26 — Vance-McMullen, Heist & Walker Eftin (2025). "Give Me Some Slack: Donor Advised Fund Granting During Crises." *NVSQ* 55(5):1113–1144.** [doi:10.1177/08997640251374264](https://doi.org/10.1177/08997640251374264)
- **Finding:** in 2020, larger accounts, accounts with lower prior payout, frequent contributors and non-endowed accounts gave more.
- **Relation to repo:** *extends*. Low payout works partly as a crisis reserve. This tempers a "warehousing" reading of the low account medians in F1.

**L30 — Johnson Center / Plante Moran for the Council of Michigan Foundations (2021). *Analysis of Donor Advised Funds from a Community Foundation Perspective.*** [landing page](https://johnsoncenter.org/resource/report-analysis-of-donor-advised-funds-from-a-community-foundation-perspective/)
- **Data:** about 2,600 DAFs at Michigan community foundations, 2017–2020.
- **Figures (as quoted by IPS 2025, not verified here):** the median account payout in 2018 was 3.1%, against 5.9% for Michigan private foundations. More than a quarter of accounts paid nothing in a given year.
- **Retrieval:** the report PDF is under a robots-disallowed path.

**L31 — Andreoni, J. & Madoff, R. (2021). *Impact of the Rise of Commercial Donor-Advised Funds on the Charitable Landscape 1991–2019.* BC Forum on Philanthropy and the Public Good.**
- **Retrieval:** I fetched a summary in [BC Law Magazine](https://lawmagazine.bc.edu/2021/07/having-her-sway/). The PDF is robots-disallowed.
- **Finding:** working charities missed about $300bn in 2014–18 because giving shifted into DAFs and private foundations.
- **Relation to repo:** *extends*. The estimate is contested and aggregate. The repo's DAF-to-DAF double-counting work bears on any accounting of total giving of this kind.

**L32 — Han, X., Hungerman, D. M. & Ottoni-Wilhelm, M. (2024). "Tax Incentives for Charitable Giving: New Findings from the TCJA." NBER WP 32737.** [nber.org/papers/w32737](https://www.nber.org/papers/w32737) ([doi:10.3386/w32737](https://doi.org/10.3386/w32737))
- **Finding:** the TCJA reduced giving by about $20bn a year, with moderate retiming. The price elasticity is about 0.6 for the average donor and over 2 for the most responsive donors.
- **Relation to repo:** context for §6 (OBBBA). The paper does not mention DAFs.

**C01 (pre-2021 context) — Andreoni & Madoff (2020). "Calculating DAF Payout and What We Learn When We Do It Correctly." NBER WP 27888.** [nber.org/papers/w27888](https://www.nber.org/papers/w27888)
- **Finding:** the industry's flow-based payout formula overstates payout by more than 50%.
- **Relation to repo:** *agrees*. The repo already uses a beginning-assets denominator and nets transfers between sponsors.

---

## 4. Law reviews and policy

**L09 — Colinvaux, R. (2022). "Speeding Up Benefits to Charity by Reforming Gifts to Intermediaries." *Boston College Law Review* 63(8):2621–2666.** [open access](https://reference-global.com/article/10.0000/bcls-j-bclr.50)
- **Argument:** the ACE Act is sound but should also apply to existing DAF accounts. The article asks whether DAFs at mission-driven sponsors, such as CFs, deserve different treatment. It cites $1.26tn held in DAFs and private foundations.
- **Relation to repo:** *agrees* with §6 (the ACE Act is not enacted; there is no payout rule).

**L20 — Leff, B. M. (2025). "Getting Donor-Advised Funds Regulation Right: Closing the Public Support Test Loophole." *NYU J. Legis. & Pub. Pol'y* 28:125.** [full text](https://nyujlpp.org/wp-content/uploads/2026/02/JLPP_28-1-Leff.pdf) ([SSRN doi:10.2139/ssrn.5147592](https://doi.org/10.2139/ssrn.5147592))
- **Argument:** the extra-strict PPA 2006 rules are useful bright lines that lower provider costs. The public-support "conduit" loophole lets donors route gifts through DAFs to privately controlled charities, and forthcoming regulations or legislation should close it. Leff prefers the Notice 2017-73 approach because it preserves retail anonymity. He discusses the November 2023 proposed §4966 rules.
- **Relation to repo:** *extends* §6. Neither §6 nor the regulatory tracker records the public-support issue.

**L12 — Walker, D. (2023). "Donor-Advised Funds in the Wake of the Tax Cuts and Jobs Act." *Columbia J. Tax L.* 14(1):1–29.** [doi:10.52214/cjtl.v14i1.11798](https://doi.org/10.52214/cjtl.v14i1.11798)
- **Argument:** bunching to clear the TCJA standard deduction likely drives most new accounts. For bunchers the problem is fiscal cost, not accumulation of assets.
- **Relation to repo:** *qualifies*.
  - The repo shows reported account counts are dominated by processors.
  - FY2022 account growth flips sign without Givinga.
  - On the strict basis, accounts still grew from 1.12m (FY2021) to 2.59m (FY2024).
  - Walker's premise survives on the corrected series, but the corrected series should replace headline NPT counts in this argument.
  - OBBBA's 0.5%-of-AGI floor strengthens his bunching mechanism from 2026.

**L08 — Gibbons, K. (2022). "Show Me the Money: Addressing the Oversight Gap in Private Foundation Donations to Donor-Advised Funds." *Minnesota Law Review* 106(3):1583 (student note).** [record](https://scholarship.law.umn.edu/minnlrev/vol106/iss3/8/)
- **Argument:** grants from private foundations to DAFs count toward the foundation's 5% payout but carry no time limit and hide the end recipients. Gibbons proposes a federal fix and a state fix.
- **Relation to repo:** *extends*. The repo does not measure inflows from foundations. The CA AG audit (L29) puts them at $1.1–1.7bn a year at 57 sponsors.

**L10 — Brakman Reiser, D. & Dean, S. A. (2023). *For-Profit Philanthropy.* Oxford University Press.** [doi:10.1093/oso/9780190074500.001.0001](https://doi.org/10.1093/oso/9780190074500.001.0001); ch. 3, [doi:10.1093/oso/9780190074500.003.0003](https://doi.org/10.1093/oso/9780190074500.003.0003)
- **Argument:** commercially affiliated sponsors dominate the field (four of the ten largest US charity recipients) and escape the 1969 rules on timing, targeting and transparency.
- **Relation to repo:** *agrees* with §1 and §2.1 (about 39% of assets at three affiliate-linked nationals). The repo adds that sponsor assets are unconcentrated (HHI about 830).

**L03 — Phillips, Dalziel & Sjogren (2021).** *Nonprofit Policy Forum* 12(3):409–441, [doi:10.1515/npf-2020-0061](https://doi.org/10.1515/npf-2020-0061). A comparison of the US, Canada and Australia. Regulation shapes which donor motive dominates. *Extends* the repo's international work.

**L11 — Murray, I. (2023).** *NPF* 14(1):51–76, [doi:10.1515/npf-2022-0031](https://doi.org/10.1515/npf-2022-0031). Proposes procedural "intergenerational justice" duties on sponsor boards instead of a fixed payout rate.

**L25 — Murray, Heist & Stone (2025).** *NPF* 17(1–2):131–160, [doi:10.1515/npf-2024-0024](https://doi.org/10.1515/npf-2024-0024). The policies of the 150 largest sponsors partly reflect those norms. *Extends* §6.

**L06 — Biagi & Hefter (2022).** *J. Philanthropy & Marketing* 28(1), [doi:10.1002/nvsm.1748](https://doi.org/10.1002/nvsm.1748). The legal and ethical risks for charities that receive DAF grants. *Extends*.

**L27 — Nolan-Smith, O. (2026).** *Hatfield Grad. J. Pub. Aff.* 10(1), [doi:10.15760/hgjpa.2026.10.1.9](https://doi.org/10.15760/hgjpa.2026.10.1.9). Recommends a minimum-distribution *regulation* plus IRS guidance confirming sponsors' authority to distribute. Low weight. It *agrees* that no payout rule exists, but practitioner commentary says the regulatory route needs legislation.

**L28 — Collins, DeVaan & Flannery (IPS, 2025). *The Independent Report on DAFs.*** [PDF](https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf)
- **Data:** e-filed 990s, TY2020–23.
- **Payout:** the median sponsor payout was 9.7% in 2023: 9.0% at CFs, 14.5–18.0% at nationals and 83.6% at processors.
- **Account size:** the median sponsor-average account is $135,086 (nationals $390,541; processors $305).
- **DAF-to-DAF:** at least $4.4bn in 2023.
- **Relation to repo:** *agrees* on direction. The levels differ by formula (F4). The repo's FY2023 central R5 figure ($4.05bn) is close to IPS's at least $4.4bn. IPS is an advocacy organisation.

**L29 — California Attorney General (2022). *Donor Advised Funds: An Overview.*** [PDF](https://oag.ca.gov/system/files/media/donor-advised-funds-overview.pdf)
- **Data:** 57 sponsors, 2016–2020.
- **Assets:** $105.3bn.
- **DAF-to-DAF:** about 11% of grants went to other DAFs, with CFs highest at 18%.
- **Foundation inflows:** private-foundation contributions were $1.1–1.7bn a year.
- **Payout distribution:** account grant ratios cluster at the two extremes, below 5% and above 50%.
- **Fees:** administrative fees were $191–267m a year.
- **Relation to repo:** *partly conflicts* (F3). The repo already cites a different CA AG release in §3.

---

## 5. Nonprofit-management research: recipients, intermediaries, community foundations

**L02 — Qu & Paarlberg (2021).** *Administration & Society* 54(5):763–791, [doi:10.1177/00953997211035721](https://doi.org/10.1177/00953997211035721). Ethnic-racial diversity raises DAF contributions at CFs but not unrestricted contributions.

**L19 — Wu, V. C. S. (2024).** *NVSQ* 54(4):773–803, [doi:10.1177/08997640241279057](https://doi.org/10.1177/08997640241279057). Among 482 CFs, a stronger donor-service (DAF) logic goes with broader community-leadership activity. This counters the claim that DAFs crowd out CF mission. *Extends*.

**L04 and L05 — Heist et al. (2021, NVSQ 51(2):327–349, [doi:10.1177/08997640211011248](https://doi.org/10.1177/08997640211011248); 2022, NML 33(4):687–709, [doi:10.1002/nml.21544](https://doi.org/10.1002/nml.21544)).** 48 donor interviews. They describe a four-phase giving process and the "tubs, tanks, towers" strategies, which give a behavioural explanation for the gap between aggregate payout and account medians.

**L21 and L22 — Heist, Shaker, Sumsion et al. (2025).** *Administrative Sciences* 15(4):137, [doi:10.3390/admsci15040137](https://doi.org/10.3390/admsci15040137), and the practitioner report *Reinventing the Cycle*, [doi:10.7912/FS95-BF59](https://doi.org/10.7912/FS95-BF59) ([PDF](https://www.dafresearchcollaborative.org/s/Reinventing-the-Cycle-Adapting-Relationship-Fundraising-for-Donors-Who-Use-DAFs.pdf)).
- **Data:** 46 fundraisers.
- **Finding:** gift processing is a critical stage. Recipient-side challenges include verifying the organisation, identifying the donor, entering grants, acknowledgement and data exchange.
- **Relation to repo:** *agrees* with §4 and §11.3.

**L14 — Heist & Stone (2023). *Self-Regulating Donor Advised Funds.*** [PDF](https://www.dafresearchcollaborative.org/s/Self-Regulating-DAFs_6Jan.pdf). Funded by Philanthropy Roundtable.
- **Inactive accounts:** among the 150 largest sponsors, 83–91% have written inactive-account policies covering over 88% of assets. They intervene after 36 months on average and allow 18 months to respond.
- **Endowed DAFs:** 47% of sponsors offer them.
- **Relation to repo:** *extends* the §3 incentive table. A written policy is not proof of enforcement (see L23).

**L23 — DAFRC (2025). *National Survey of DAF Managers.*** [doi:10.4087/exxe4510](https://doi.org/10.4087/exxe4510); [executive summary](https://www.dafresearchcollaborative.org/s/Executive-Summary-The-National-Survey-of-Donor-Advised-Fund-Managers.pdf)
- **Data:** 128 sponsors, surveyed in 2023.
- **Donor information:** 36% send full donor information with grants by default.
- **Capacity:** 61% report sufficient IT.
- **Competition and activity:** 60% see competition with other sponsors as a barrier. Only 35% put great emphasis on keeping every account active.
- **Relation to repo:** *extends* §4, §5 and §8. The sponsor-reported capacity gaps support the repo's entry-strategy demand thesis.

**L24 — DAFRC (2025). *National Survey of DAF Donors.*** [doi:10.4087/wikf1423](https://doi.org/10.4087/wikf1423); [executive summary](https://www.dafresearchcollaborative.org/s/Executive-Summary-The-National-Survey-of-Donor-Advised-Fund-Donors.pdf)
- **Data:** over 2,100 donors. Average age 67; 96% have net worth over $1m.
- **Giving share:** 48% put over 75% of their giving through a DAF.
- **Advisers:** only 9% use an outside financial adviser to manage DAF investments.
- **Relation to repo:** *qualifies* §6. The sample was recruited through sponsors, so the 9% cannot size the adviser-managed channel that the 2023 proposed "donor-advisor" rule would affect. The repo documents large adviser-led programs.

**L33 — DAFRC (2026). *Financial Planning in the Age of DAFs.*** [executive summary](https://www.dafresearchcollaborative.org/s/260423_DAF_FinancialAdvisor-ExecSum_Print-1.pdf). 669 advisers. Already cited in §11.1 [V]. *Agrees*.

**L07 — Marks, S. (2022).** *The Foundation Review* 14(4), [doi:10.9707/1944-5660.1636](https://doi.org/10.9707/1944-5660.1636). Sponsors face governance barriers to impact investing.

---

## 6. Comparison with the report, by section

| Report section | What the literature says | Verdict |
|---|---|---|
| **§1 Market size and shape** | No 2021–26 work re-estimates the size of the market differently. Brakman Reiser & Dean (L10) and IPS (L28: nationals hold 70% of assets) agree on dominance by affiliated nationals. IPS separates processors when measuring account size, as the repo does (79.5% of accounts at processors). | Agrees |
| **§1 Payout** | The repo reports aggregate payout of 23.7–28.4% (19.0–21.5% net) and sponsor medians of about 11–12.5%. The literature reports a sponsor median of 9.7% (IPS formula), account medians of 9% (DAFRC 2024) and 11% (CF and religious only, 2022), and a Michigan CF figure of 3.1% (secondary). Andreoni–Madoff (C01) and the repo both reject flow-based formulas. | Extends (F1, F4). No conflict once definitions are aligned |
| **§1 / §11.1 Transfers between sponsors** | CA AG (L29): about 11% of grants, CF highest at 18%. IPS: at least $4.4bn in 2023. Flannery–Mittendorf (L16): funds "cycle" between sponsors. | Agrees on size; partly conflicts on who sends them (F3) |
| **§3 Incentives** | Flannery–Mittendorf (L18): a donor-benefit orientation predicts lower payout among nationals. Heist–Stone (L14) and the manager survey (L23): inactive-account policies are almost universal, but active enforcement is a priority for only 35% of sponsors. | Could upgrade one row from *unsupported* to *suggestive* (F2) |
| **§3 Challengers / technology** | Grennan (L01): the fintech-style DAFs grow fastest and grant differently. Manager survey: 39% of sponsors lack sufficient IT. | Extends |
| **§6 Regulation** | Leff (L20): the public-support conduit loophole and Notice 2017-73 are not in the repo tracker. Colinvaux (L09): the ACE Act should cover existing accounts. Walker (L12): bunching and fiscal cost. Gibbons (L08): foundation-to-DAF transfers. Murray (L11, L25): procedural duties. No final rule, consistent with §6 (regulations neither final nor withdrawn). | Agrees; extends with the public-support item |
| **§11 Round-2 findings** | Recipient-side friction (L21, L22, L23) matches §11.3. Political and hate-group recipients (L17) are a monitoring gap for §11.8. | Agrees / extends |

---

## 7. Gaps in the literature (2021–2026)

1. **Crowd-out and additionality.** No household-level causal study of whether opening a DAF raises total giving was found. The evidence is survey-based (L24) or aggregate and contested (L31).
2. **TCJA and OBBBA timing.** No DAF-specific bunching econometrics was found. Walker (L12) is descriptive, and Han et al. (L32) cover giving in general. Essig Aberg (M01) may estimate a DAF tax elasticity but was not reviewable here.
3. **Representative account-level data.** All account-level evidence (L13, L15, L26, L30) comes from voluntary samples, CF-heavy samples, or one state. No study covers the three largest nationals at account level.
4. **Vendors, technology and sponsor operating costs.** No academic work examines the administrator and vendor layer (§2, §5, §11.2). The repository's Form 990 vendor and cost work has no academic counterpart.

---

## 8. Source register

| ID | Source | URL / DOI | Retrieved (2026-11-15) |
|---|---|---|---|
| L01 | Grennan 2022, RCFS | https://doi.org/10.1093/rcfs/cfac017 | Crossref record + abstract |
| L02 | Qu & Paarlberg 2021, Admin & Society | https://doi.org/10.1177/00953997211035721 | Crossref + abstract |
| L03 | Phillips, Dalziel & Sjogren 2021, NPF | https://doi.org/10.1515/npf-2020-0061 | Crossref + abstract |
| L04 | Heist et al. 2021, NVSQ | https://doi.org/10.1177/08997640211011248 | Crossref + abstract |
| L05 | Heist et al. 2022, NML | https://doi.org/10.1002/nml.21544 | Crossref + abstract |
| L06 | Biagi & Hefter 2022, JPM | https://doi.org/10.1002/nvsm.1748 | Crossref + abstract |
| L07 | Marks 2022, Foundation Review | https://doi.org/10.9707/1944-5660.1636 | Crossref + abstract |
| L08 | Gibbons 2022, Minn. L. Rev. | https://scholarship.law.umn.edu/minnlrev/vol106/iss3/8/ (doi:10.24926/265535.4361) | Record page + abstract |
| L09 | Colinvaux 2022, B.C. L. Rev. | https://reference-global.com/article/10.0000/bcls-j-bclr.50 | Publisher page |
| L10 | Brakman Reiser & Dean 2023, OUP | https://doi.org/10.1093/oso/9780190074500.001.0001 | Crossref + abstract |
| L11 | Murray 2023, NPF | https://doi.org/10.1515/npf-2022-0031 | Crossref + abstract |
| L12 | Walker 2023, Colum. J. Tax L. | https://doi.org/10.52214/cjtl.v14i1.11798 | Crossref + abstract; DOI resolution checked |
| L13 | DAFRC Patterns & Trends 2022 | https://www.dafresearchcollaborative.org/s/DAFRC-Patterns-and-Trends-Report_Executive-Summary.pdf | PDF read |
| L14 | Heist & Stone 2023 | https://www.dafresearchcollaborative.org/s/Self-Regulating-DAFs_6Jan.pdf | PDF read |
| L15 | DAFRC National Study 2024 | https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf (doi:10.4087/ymfd7624) | PDF read + Crossref |
| L16 | Flannery & Mittendorf 2024/25 | https://doi.org/10.2139/ssrn.4683236 ; https://doi.org/10.1007/978-3-031-74994-0_4 | Crossref + abstract |
| L17 | Flannery & Mittendorf 2025, NPF | https://doi.org/10.1515/npf-2024-0028 | Crossref + abstract |
| L18 | Flannery & Mittendorf 2025, NVSQ | https://doi.org/10.1177/08997640251331853 | Crossref + abstract |
| L19 | Wu 2024, NVSQ | https://doi.org/10.1177/08997640241279057 | Crossref + abstract |
| L20 | Leff 2025, NYU JLPP | https://nyujlpp.org/wp-content/uploads/2026/02/JLPP_28-1-Leff.pdf | Full text read |
| L21 | Heist, Shaker, Sumsion et al. 2025, Adm. Sci. | https://doi.org/10.3390/admsci15040137 | Crossref + abstract |
| L22 | Shaker, Sumsion & Heist 2025 | https://doi.org/10.7912/FS95-BF59 | PDF read (front matter) |
| L23 | DAFRC Managers 2025 | https://www.dafresearchcollaborative.org/s/Executive-Summary-The-National-Survey-of-Donor-Advised-Fund-Managers.pdf (doi:10.4087/exxe4510) | PDF read + Crossref |
| L24 | DAFRC Donors 2025 | https://www.dafresearchcollaborative.org/s/Executive-Summary-The-National-Survey-of-Donor-Advised-Fund-Donors.pdf (doi:10.4087/wikf1423) | PDF read + Crossref |
| L25 | Murray, Heist & Stone 2025, NPF | https://doi.org/10.1515/npf-2024-0024 | Crossref + abstract |
| L26 | Vance-McMullen, Heist & Walker Eftin 2025, NVSQ | https://doi.org/10.1177/08997640251374264 | Crossref + abstract |
| L27 | Nolan-Smith 2026 | https://pdxscholar.library.pdx.edu/hgjpa/vol10/iss1/7/ (doi:10.15760/hgjpa.2026.10.1.9) | Record page + abstract |
| L28 | IPS 2025 | https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf | PDF read |
| L29 | CA AG 2022 | https://oag.ca.gov/system/files/media/donor-advised-funds-overview.pdf | PDF read |
| L30 | CMF / Johnson Center 2021 | https://johnsoncenter.org/resource/report-analysis-of-donor-advised-funds-from-a-community-foundation-perspective/ | Landing page; figures secondary (via L28) |
| L31 | Andreoni & Madoff 2021 | https://lawmagazine.bc.edu/2021/07/having-her-sway/ | Summary page; PDF robots-blocked |
| L32 | Han, Hungerman & Ottoni-Wilhelm 2024 | https://www.nber.org/papers/w32737 | NBER page |
| L33 | DAFRC Financial Advisors 2026 | https://www.dafresearchcollaborative.org/s/260423_DAF_FinancialAdvisor-ExecSum_Print-1.pdf | PDF read |
| C01 | Andreoni & Madoff 2020 (context) | https://www.nber.org/papers/w27888 | NBER page |
| M01–M06 | Metadata only (Essig Aberg 2024; Flannery & Mittendorf 2025 "When DAFs Draw the Map"; Krueger 2026; Murray 2025 encyclopedia; Vance-McMullen & Heist 2023 chapter; Heisman 2023 encyclopedia) | DOIs in CSV | Crossref records only; content not reviewed |

**Considered but not listed:**
- Beebe 2024 (Baker Institute): HTTP 403.
- Philanthropy Roundtable payout and critique briefs: bot challenge.
- The Conversation pieces by Mittendorf and Flannery: robots-disallowed for Claude.
- Aanestad, Gibbons & Pratt (Minnesota Council of Nonprofits): retrieved, but it dates from 2020 and so falls outside the recency window.
- Trade newsletters (*Major Gifts Report*, *Nonprofit Business Advisor*) found in Crossref: not research.

---

## 9. Data dictionary: `daf-literature-2021-2026.csv`

| Column | Meaning |
|---|---|
| `lit_id` | L## = reviewed 2021+ work; M## = metadata only; C## = pre-2021 context |
| `review_tier` | `reviewed_fulltext`, `reviewed_fulltext_page`, `reviewed_abstract`, `reviewed_landing_page`, `reviewed_landing_page_secondary_figures`, `reviewed_secondary_summary`, `metadata_only_not_reviewed`, `pre2021_context` |
| `strand` | `empirical_economics`, `empirical_finance`, `law_policy`, `nonprofit_management`, `policy_grey_literature`, `unclassified` |
| `authors`, `year`, `title`, `venue_or_publisher` | Bibliographic data as given by Crossref or the source document |
| `doi` | DOI where one exists (blank for reports without one) |
| `url` | The URL actually retrieved (or the DOI link) |
| `retrieval_evidence` | How and when the item was retrieved, and any robots or bot-challenge limits |
| `peer_review_status` | Peer-reviewed journal, law review, student note, working paper, report, regulator audit, etc. |
| `method`, `data_and_period` | Design and data as stated by the source |
| `main_finding` | Finding as stated in the abstract or full text; for metadata-only rows, "not reviewed - no claim made" |
| `repo_sections` | Sections of DAF-INDUSTRY-REPORT-2026-11.md (and repo files) compared |
| `relation_to_repo` | `agrees`, `extends`, `qualifies` (agrees but needs repo correction applied), `partly_conflicts`, `not_assessed` |
| `comparison_note` | The specific comparison with repo figures |
| `headline_flag` | `yes` if it could change a report conclusion or claim state; `no`; `unknown` for unreviewed rows |
| `independence_note` | Funding, advocacy or sample caveats |

**Queue proposals:** see [`queue-proposals-batch39-n8.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n8.csv).
- **P-B39N8-01:** a bridge table across payout definitions.
- **P-B39N8-02:** test the CA AG finding on CF transfers to other DAFs against R5.
- **P-B39N8-03:** review the SSRN-only and blocked works.

## Validation corrections (wave 24B, 2026-11-15) — governing
Source: [validation-wave24b-report.md](validation-wave24b-report.md); register `data/mission-2026-11-14/validation-register-wave24b.csv`.

1. **§2, F1 handling.**
   - **Find:** "Keep the sentence for *public filings*, and add that voluntary account samples put the median account at about 9%."
   - **Replace with:** "Keep the sentence for *public filings*, and add that voluntary account samples put the median account at about 9%. [V wave 24B: confirmed verbatim. The DAFRC 2024 executive summary gives a 9% median, 15% excluding inactive accounts and an 18% mean; 22% of accounts were inactive in 2020–22; 111 programs, including nationals.]"
2. **§2, F2 handling.**
   - **Find:** "Candidate to move from *unsupported* to *suggestive*, with the caveat that the measure is marketing language, not fee structure, and the result is correlational. Needs a validator decision."
   - **Replace with:** "Validator decision (wave 24B): keep the row **Mixed** (Low on effect). Cite this study as correlational evidence that a donor-benefit orientation goes with lower payout among nationals. Do not treat it as evidence on asset-based fees, because the measure is website language, not fee structure."
3. **§2, F3 handling.**
   - **Find:** "The overall share agrees with the repo's 10–18%. The CF result could mean R5 under-nets CF payout. Queue proposal P-B39N8-02."
   - **Replace with:** "The overall share agrees with the repo's 10–18%. The CF figure does not carry over nationally:\n- It is self-reported for 2016-07 to 2020-12 by 57 California-registered sponsors.\n- It does not say whether fund-to-fund transfers inside the same sponsor count as \"grants to other DAFs\".\n- The repo's top-50 Schedule I data put CFs excluding SVCF at 5.1% of FY2023–24 dollars to other DAF sponsors, against 13.7% for nationals; including SVCF, 14.2% [V wave 24B].\n\nQueue proposal P-B39N8-02 tests it."
4. **§2, F4.**
   - **Find:** "Leff (2025) calls the spread unresolved."
   - **Replace with:** "Leff (2025, fn. 95) says the 9.7%–23.9% range \"illustrates disputes over the proper methodology\" and does not resolve it [V wave 24B]."
5. **§6, §3 challengers row.**
   - **Find:** "Manager survey: 39% of sponsors lack sufficient IT."
   - **Replace with:** "Manager survey: 61% of sponsors report sufficient IT (74% policies, 60% budget, 52% staffing) [V wave 24B]."
