# Final status report: DAF research mission (2026-11-14 → 2026-11-15)

**Every count below was computed from the repository, not estimated.** The commands are listed in each row.

## Repository and branch
- **Repository:** `kemiller2002/daf-landscape`. Integration branch `main`.
- **Working branch:** `claude/daf-landscape-research-tdxdiq`. This is the branch the session was authorized to use. Merging to `main` is through **draft PR #20**: https://github.com/kemiller2002/daf-landscape/pull/20. Nothing was force-pushed and no research was deleted.
- **Final commit SHA:** a file cannot contain the SHA of the commit that adds it. The PR #20 description records the head SHA after this file was committed. The parent of the commit that adds this file is `1b8f763`.
- **Pre-existing open PRs:** #1 and #16 are left untouched.

## Counts (refreshed after round 2, 2026-11-14)

Round 1 is the original mission. Round 2 covers citations, the research queue, deep research, the quadrants and validation waves 3–4.

| Item | Count | How computed |
|---|---|---|
| Commits added on the branch | 62 before this refresh | `git rev-list --count main..HEAD` |
| Research documents (markdown) | 81 → 121 | `scripts/mission_inventory.py` |
| Words in research documents | ~105.8k → ~268k | same |
| Datasets | 60 → 177; 1,119 → 57,229 data rows | Most rows are machine-harvested panels: the DAFRC sponsor panel, Form 990 harvests for 1,512 sponsors, and the entry/exit panel |
| **Sources: curated unique URLs** | **1,744** curated (1,304 cited in narrative documents plus 440 more in curated CSVs). Baseline: 431. | Inventory script. A further ~17,700 URLs are machine-harvested IRS e-file and filing links in the bulk datasets; they are counted separately and not as "sources reviewed". The total including bulk is 19,468 across 509 domains. |
| **Organizations investigated** | **~300 distinct organizations** with sourced evidence: graph nodes, breadth profiles, 89 interested firms and 50 failed or retreated ventures, after de-duplication. **1,512 sponsors** have machine-parsed Form 990 data. **33 entities** have deep checklist coverage. | Normalized-name union of `relationship-graph-nodes`, `breadth-entity-profiles`, `daf-interested-firms` and `failed-daf-startups`; plus `form990-harvest-sponsor-universe-full.csv` |
| **Independently validated findings** | **103 claims** checked by non-authoring agents: 59 confirmed, 33 partially confirmed, 8 contradicted, 3 unable to verify | `validation-register*.csv`: waves 1 (22), 2A (31), 2B (27), 3 (10 incl. 1 new finding), 4 (13) |
| **Evidence Quadrant reproducibility** | 43 providers in 5 areas, two blind scorers. 67% exact cell agreement; 99.7% within 1 point. 18 positions reproduced, 18 adjudicated, 7 insufficient evidence | `quadrant-calibration.md` |
| **AI use cases investigated** | **30 inventoried** (10 DAF-direct) plus 2 identified by red team. Also: agentic-integration controls for 8 services, 16 processes modelled, 16 failure modes | `ai-use-case-inventory.csv`, `agentic-integration-controls.csv` |
| **Major hypotheses tested** | **33** in round 1, plus round 2 tests: Fidelity EFT-only (not in effect); Give Interactive systematic displacement (not yet: 2 migrations); Ren share claim (footprint ~28% software, 14.8% 990-paid; 60% unreachable); sponsor mortality (0.2–1.5%/yr); entrant data access without vendor consent (live access no; batch export yes); anti-passthrough clause spread (NPact only). That is **39** in total. | listed in the cited documents |
| Complaints corpus / failure cases | 244 records (149 complaints, 16 mixed, 79 praise) and 50 venture cases | `daf-user-complaints-corpus.csv`, `failed-daf-startups.csv` |
| Research queue | 50 questions done, 1 blocked (needs vendor outreach), 128 open, re-ranked by expected information value; agents add proposals through `queue-proposals-*.csv` | `research-priority-queue.csv` |
| Coverage matrix | 33 entities × 12 items = 396 cells. 62.1% have any investigation (round 1: 56.6%). 12.6% are partially validated or better (round 1: 8.8%). 28 cells are independently corroborated. | `scripts/mission_coverage.py` |

## Most important new discoveries

The full ranked list with evidence, uncertainty, implications and next actions is in [strategic-synthesis.md §G](strategic-synthesis.md).

1. **Most DAF "accounts" are pass-through processor accounts.** They are 79.5% of accounts and hold 0.9% of assets. ([DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)) Traditional invested accounts number at most 737k. ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`regulation-market-structure-portability.md`](../../research/mission-2026-11-14/regulation-market-structure-portability.md))
2. **Software is two markets plus one captive market.** About 39% of assets sit at affiliate-linked nationals. ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFgiving360 FY2025 results](https://www.dafgiving360.org/press-release/fiscal-year-2025-results); [Vanguard Charitable FY2025 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../../data/mission-2026-11-14/validation-register-wave2b.csv)) Fully outsourced administration covers ≥6 sponsors holding 9.1% of assets. ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`regulation-market-structure-portability.md`](../../research/mission-2026-11-14/regulation-market-structure-portability.md)) The community-foundation long tail is on Foundant. ([Foundant CommunitySuite page](https://www.foundant.com/products/communitysuite/); [Tech Impact CF software landscape](https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf))
3. **Apparently independent wealth-firm DAFs share one sponsor–vendor spine (RCF + Ren).** ([RCF FAQ](https://renaissancecharitable.org/faqs/); [Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/); [Ameriprise RCF portal](https://ampf.donorfirstx.com/); [RBC RCF portal](https://rbcrcf.donorfirstx.com/); [Ren LPL RCF page](https://www.reninc.com/lpl-rcf-daf/); [Ren UBS RCF page](https://www.reninc.com/why-ubs-advisors-choose-rcf/); [SEI Giving Fund portal](https://sei.donorfirstx.com/); [MDRT Global Gift Fund portal](https://mdrt.donorfirstx.com/); repo [`relationship-graph-edges.csv`](../../data/mission-2026-11-14/relationship-graph-edges.csv)) Ren's DFX portal also fronts Morgan Stanley GIFT (new), Bank of America's fund and AEF ([MS GIFT donor portal](https://msgift.donorfirstx.com/); [BofA Charitable Gift Fund portal](https://bofa.donorfirst.org/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)), and Ren-owned iPhi serves the Cleveland Foundation and ImpactAssets. ([Cleveland Foundation iPhi portal](https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx); [ImpactAssets homepage (iPhi log-in)](https://impactassets.org/))
4. **Ren's ">half of DAF assets" claim is not reachable on public evidence, though Ren's footprint is about three times earlier estimates.** ([Ren homepage](https://www.reninc.com/); [Great Hill investment in Ren (Pulse 2.0)](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/)) On public evidence, sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**. The full Form 990 harvest (all 1,512 sponsors) finds Ren/Stellar named by 30 sponsors holding $48.55bn (14.8%) in any FY2022–25 return, but only 18 sponsors holding $30.18bn (9.2%) in their latest return [V wave 5], and about 5% (RCF, MS GIFT) on Ren-paid administration. Nearly half of the 28% is NPT, evidenced by hosting (iPhi login redirect, shared Ren load balancer, Ren-hosted "NPT iPhi Statuspage") rather than a disclosed contract ([MS GIFT 990 via GivingTuesday mirror; Goldman PWM portal gspf.goldman.com; NPT GivingPoint](validation-wave3-report.md)). Ren's "60%+"/"about half" claims remain unreachable without Fidelity Charitable, DAFgiving360 or Vanguard Charitable, none of which shows a Ren vendor; Vanguard chose Give Interactive. (Earlier estimates: 8.7% → 9.0% → 28% after NPT and Goldman evidence.) ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../../data/mission-2026-11-14/validation-register-wave2b.csv)) <!-- CITE-CHECK RESOLVED 2026-11-14 (text corrected): Validator V2B-05 recomputed $29.65bn = 9.04% for RCF, AEF, MS GIFT and BofA from DAFRC FY2024 (all imputed); the 8.7% ($28.5bn) figure was only partially confirmed. Not changed. -->, and the "$200bn" figure includes non-DAF assets. ([AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
5. **The value pool for DAF operations AI is thin, and redesign should precede AI.** The model's "AI ranks last" result is an artifact of its assumptions. ([Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing); [BLS compliance officers (May 2025)](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm); [BLS ECEC June 2026](https://www.bls.gov/news.release/ecec.nr0.htm); repo [`ai-process-economics.csv`](../../data/mission-2026-11-14/ai-process-economics.csv); repo [`validation-register-wave2a.csv`](../../data/mission-2026-11-14/validation-register-wave2a.csv))
6. **The agentic AI frontier is donor-side**, through TIFIN Give's Louise and Daffy's MCP server. ([TIFIN Give Louise release](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); [Daffy MCP docs](https://docs.daffy.org/agents/mcp)) No public evidence shows AI in sponsor-side approval. (repo [`ai-use-case-inventory.csv`](../../data/mission-2026-11-14/ai-use-case-inventory.csv); repo [`validation-register-wave2a.csv`](../../data/mission-2026-11-14/validation-register-wave2a.csv))
7. **Payout splits behind the average.** The median sponsor pays out about 11–12.5%, and about one in five sponsors with ≥$1m pays out under 5%. ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`derived-metrics.csv`](../../data/mission-2026-11-14/derived-metrics.csv); repo [`scripts/mission_daf_metrics.py`](../../scripts/mission_daf_metrics.py))
8. **Fee pass-through is near-total at RCF.** RCF pays Ren 98% of its individual-fundholder admin-fee revenue. ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); [RCF FY2023 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2023RCFAuditedFinancialStatements.pdf); repo [`rcf-ren-audited-admin-payments-2020-2024.csv`](../../data/rcf-ren-audited-admin-payments-2020-2024.csv)) The causal effect on payout is unsupported, and segment medians run against it. ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../../data/mission-2026-11-14/validation-register-wave2b.csv))
9. **Portability is a legal right with operational lock-in.** No sponsor publishes an outbound transfer policy or offers history portability. ([GTCF DAF transfer instructions](https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf); [Daffy help: closing an account](http://help.daffy.org/en/articles/6520234-how-do-i-close-my-daffy-account); [AEF DonorCentral sunset notice](https://engage.aefonline.org/dc-sunset/); repo [`sponsor-transfer-portability-terms.csv`](../../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv))
10. **A previously unknown vendor, Give Interactive, holds Vanguard Charitable's DAF recordkeeping.** ([Give Interactive / Vanguard Charitable release](https://www.giveinteractive.com/post/vanguard))

## Contradictions and unresolved questions

**Resolved contradictions:**
- **Concentration:** CR3 58% vs 45.5% came from a period mismatch; 45.5% is correct. ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../../data/mission-2026-11-14/validation-register-wave2b.csv))
- **NPT FY2025 grants:** $6.44bn is the U.S. DAF program; $6.61bn likely includes the U.K. ([NPT FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/); [NonProfit Times on NPT FY2025](https://thenonprofittimes.com/?p=215695))
- **SPLC grant holds:** confirmed by the California AG's release. ([California AG release](https://oag.ca.gov/node/623769))

**Contradicted prior claims:**
- The Bank of America 10-K evidence of Ren. The only evidence is the portal. ([SEC full-text search, BofA filings](https://efts.sec.gov/LATEST/search-index?q=%22Charitable%20Gift%20Fund%22&ciks=0000070858); [BofA CGF Form 990 TY2024](https://projects.propublica.org/nonprofits/organizations/46010342/202503219349318170/full); [BofA Charitable Gift Fund portal](https://bofa.donorfirst.org/))
- Chariot's "Fidelity electronic-only by July 2026". Not confirmed; about 67% of Fidelity grants already go by EFT. ([Chariot on Fidelity's 2026 Giving Report](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report); [Fidelity Charitable nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html))
- The entrant model's "model-assisted clearing". Reconciled to deterministic clearing only. (repo [`validation-register-wave2a.csv`](../../data/mission-2026-11-14/validation-register-wave2a.csv); repo [`ai-governance-failure-modes.md`](../../research/mission-2026-11-14/ai-governance-failure-modes.md))

**Still unresolved:**
- Ren's denominator for its share claims. ([Ren homepage](https://www.reninc.com/); [Great Hill investment in Ren (Pulse 2.0)](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/))
- Ren's SOC 2 Type 1 vs Type 2 statements. ([AEF/Ren release, Jul 2025](https://www.aefonline.org/thought-leadership/american-endowment-foundation-selects-ren-as-a-strategic-partner-to-expand-philanthropy-drive-innovation-and-foster-growth-in-financial-services/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
- Sponsor, administrator and technology vendor for the Edward Jones private DAF and Goldman Sachs. ([Edward Jones elevated wealth management release](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management))
- Give Interactive's scope at Vanguard Charitable. ([Give Interactive / Vanguard Charitable release](https://www.giveinteractive.com/post/vanguard))
- Whether sponsor–vendor contracts grant API and data-export rights.
- Real exception rates and handling times anywhere in the market.
- Fund-level payout by fee model.
- Content of the forthcoming §4966/6033 guidance. ([IRS 2026-2027 Priority Guidance Plan](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf))
- Builders of the NCF and SVCF Salesforce portals.
- Funding and AI evidence for Endaoment, Goodstack, Every.org and Grantable.

## Research coverage and limitations
- **Public sources only.** No vendor demos, contracts, interviews or sponsor operational data were obtained.
- **Search and archive limits.** The shared web-search budget was exhausted mid-mission. Several sites blocked automated access (Every.org, JCF, the Chicago Community Trust and GKCCF portals, dafgiving360.org, tifin.com, congress.gov). The Wayback Machine could only confirm that snapshots exist, not show their content.
- **Scenario numbers.** All AI and entrant cost figures are labelled scenarios. The red team showed that the rankings depend on unsourced amenability and redesign-share assumptions.
- **Coverage denominator.** The coverage matrix covers a purposive set of 33 entities. 18 of them still have a majority of checklist items not investigated, mostly wealth channels other than Edward Jones, faith and community sponsors, and new vendors.
- **Validation ceiling.** Validation is independent of the authoring agent but uses the same model family. Under the EDF claim policy this is cross-agent checking, not cross-executor reproducibility.

## Highest-value next investigations
Ranked by expected information value in `research-priority-queue.csv` (open questions only):
1. **Q-N02:** Give Interactive's scope at Vanguard Charitable and its client list.
2. **Q-B04:** Goldman Sachs and Morgan Stanley GIFT administration and technology stack.
3. **Q-N01:** Ren's share-claim denominator, including whether NPT is counted through Stellar/iPhi.
4. **Q-N04:** API and data-export rights in sponsor–vendor contracts. This is the gating question for any entrant.
5. **Q-N05:** spend limits and authority separation in TIFIN Louise and Daffy MCP.
6. **Q-B18:** whether Givinga and DAF Direct are multi-sponsor infrastructure.
7. **Q-N03:** a sponsor time-and-motion study of exception rate, handling minutes and QA. It ranks lower only because public availability is low. It is the gating evidence for every AI-economics conclusion and should be pursued through an authorized partner.

---

## Source register

Every external URL cited inline in this document, deduplicated, in order of first citation. Dates are publication or access dates as recorded in the repository's workstream source registers and validation registers.

- DAFRC Updated Analysis memo (Apr 2026; accessed 2026-11-14): https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf
- DAFRC Updated Analysis dataset (Spring 2026; accessed 2026-11-14): https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx
- Fidelity Charitable FY2025 audited statements (FYE 2025-06-30): https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf
- DAFgiving360 FY2025 results (2025-07-29): https://www.dafgiving360.org/press-release/fiscal-year-2025-results
- Vanguard Charitable FY2025 financial statements (FYE 2025-06-30): https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf
- Foundant CommunitySuite page (accessed 2026-11-14): https://www.foundant.com/products/communitysuite/
- Tech Impact CF software landscape (Jul 2022): https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf
- RCF FAQ (live 2026-11-14): https://renaissancecharitable.org/faqs/
- Edward Jones Charitable Gift Fund portal (live 2026-11-14): https://edwardjones.donorfirstx.com/
- Ameriprise RCF portal (live 2026-11-14): https://ampf.donorfirstx.com/
- RBC RCF portal (live 2026-11-14): https://rbcrcf.donorfirstx.com/
- Ren LPL RCF page (live 2026-11-14): https://www.reninc.com/lpl-rcf-daf/
- Ren UBS RCF page (live 2026-11-14): https://www.reninc.com/why-ubs-advisors-choose-rcf/
- SEI Giving Fund portal (live 2026-11-14): https://sei.donorfirstx.com/
- MDRT Global Gift Fund portal (live 2026-11-14): https://mdrt.donorfirstx.com/
- MS GIFT donor portal (live 2026-11-14): https://msgift.donorfirstx.com/
- BofA Charitable Gift Fund portal (live 2026-11-14): https://bofa.donorfirst.org/
- AEF/Ren release, Apr 2026 (2026-04-08): https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/
- Cleveland Foundation iPhi portal (accessed 2026-11-14): https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx
- ImpactAssets homepage (iPhi log-in) (accessed 2026-11-14): https://impactassets.org/
- Ren homepage (live 2026-11-14): https://www.reninc.com/
- Great Hill investment in Ren (Pulse 2.0) (2025-10-28): https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/
- Anthropic API pricing (read 2026-11-14): https://platform.claude.com/docs/en/about-claude/pricing
- BLS compliance officers (May 2025) (accessed 2026-11-14): https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm
- BLS ECEC June 2026 (released 2026-09-09): https://www.bls.gov/news.release/ecec.nr0.htm
- TIFIN Give Louise release (2025-10-27): https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html
- Daffy MCP docs (accessed 2026-11-14): https://docs.daffy.org/agents/mcp
- RCF FY2024 audited statements (FYE 2024-12-31; accessed 2026-11-14): https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf
- RCF FY2023 audited statements (FYE 2023-12-31; accessed 2026-11-14): https://renaissancecharitable.org/wp-content/uploads/2026/01/2023RCFAuditedFinancialStatements.pdf
- GTCF DAF transfer instructions (2026-05-18): https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf
- Daffy help: closing an account (2026-04-02): http://help.daffy.org/en/articles/6520234-how-do-i-close-my-daffy-account
- AEF DonorCentral sunset notice (2026-10-31): https://engage.aefonline.org/dc-sunset/
- Give Interactive / Vanguard Charitable release (2025-11-04): https://www.giveinteractive.com/post/vanguard
- NPT FY2025 annual report (FY ended 2025-06-30): https://www.nptrust.org/annual-reports/npt-annual-report/
- NonProfit Times on NPT FY2025 (2025-12-01): https://thenonprofittimes.com/?p=215695
- California AG release (2026-05-22): https://oag.ca.gov/node/623769
- SEC full-text search, BofA filings (run 2026-11-14): https://efts.sec.gov/LATEST/search-index?q=%22Charitable%20Gift%20Fund%22&ciks=0000070858
- BofA CGF Form 990 TY2024 (e-filed 2025-11-17): https://projects.propublica.org/nonprofits/organizations/46010342/202503219349318170/full
- Chariot on Fidelity's 2026 Giving Report (2026-03-24): https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report
- Fidelity Charitable nonprofit FAQ (live 2026-11-14): https://www.fidelitycharitable.org/nonprofits/faqs.html
- AEF/Ren release, Jul 2025 (2025-07-23): https://www.aefonline.org/thought-leadership/american-endowment-foundation-selects-ren-as-a-strategic-partner-to-expand-philanthropy-drive-innovation-and-foster-growth-in-financial-services/
- Edward Jones elevated wealth management release (2025): https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management
- IRS 2026-2027 Priority Guidance Plan (2026-09-29): https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf
