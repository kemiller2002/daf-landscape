# Final status report: DAF research mission (2026-11-14 → 2026-11-15)

**Every count below was computed from the repository, not estimated.** The commands are listed in each row.

## Repository and branch
- **Repository:** `kemiller2002/daf-landscape`. Integration branch `main`.
- **Working branch:** `claude/daf-landscape-research-tdxdiq`. This is the branch the session was authorized to use. Merging to `main` is through **draft PR #20**: https://github.com/kemiller2002/daf-landscape/pull/20. Nothing was force-pushed and no research was deleted.
- **Final commit SHA:** a file cannot contain the SHA of the commit that adds it. The PR #20 description records the head SHA after this file was committed. The parent of the commit that adds this file is `1b8f763`.
- **Pre-existing open PRs:** #1 and #16 are left untouched.

## Counts

| Item | Count | How computed |
|---|---|---|
| Commits added by this mission | 24 (including this file's commit) | `git rev-list --count main..HEAD` |
| Research documents (markdown) | 81 → 96 (+15 mission documents) | `scripts/mission_inventory.py` |
| Words in research documents | ~105.8k → ~164.5k | same |
| Datasets | 60 → 89; data rows 1,119 → 13,658 (8,751 of them are the DAFRC sponsor panel) | same; baseline = state before mission files |
| **Sources reviewed: unique URLs cited across the repository** | **431 → 886** (147 → 288 domains). Mission agents reported about 600 distinct URLs across their files, with overlap. | same. A cited URL is referenced, not necessarily read in full. About 60 mission sources rely on search summaries and are flagged. |
| **Organizations investigated** | **140 distinct organizations** profiled with sourced evidence (graph nodes excluding 25 branded programs, plus the breadth profiles). Deep checklist coverage covers 33 entities. Timeline events cover 57 named companies. | `relationship-graph-nodes.csv` ∪ `breadth-entity-profiles.csv`; coverage matrix |
| **Independently validated findings** | **80 claims checked by non-authoring agents:** 45 confirmed, 25 partially confirmed, 7 contradicted, 3 unable to verify | `validation-register.csv` (22), `-wave2a` (31), `-wave2b` (27) |
| **AI use cases investigated** | **30 inventoried** (13 announced, 7 demonstrated, 8 deployed with evidence, 2 unverified; 10 DAF-direct). 2 more (Bonterra Que, Bonterra Grantmaker) were identified by red team and logged as corrections. 16 operational processes were modelled for AI economics, and 16 AI failure modes registered. | `ai-use-case-inventory.csv`, `ai-process-economics.csv`, `ai-failure-mode-register.csv` |
| **Major hypotheses tested** | **33**: 10 industry beliefs (synthesis §A); 3 entry strategies; 11 structural-vs-habit classifications; 3 EDF diagnoses of observed outcomes; 6 Clarity-only hypotheses (incentives §7). Separately, 39 announced-vs-delivered capability claims were checked. | listed in the cited documents |
| Coverage matrix | 33 entities × 12 checklist items = 396 cells. 56.6% have any investigation (was 55.2% on 29 entities); 8.8% are partially validated or better (was 3.4%); 23 cells are independently corroborated (was 0) | `scripts/mission_coverage.py` |

## Most important new discoveries

The full ranked list with evidence, uncertainty, implications and next actions is in [strategic-synthesis.md §G](strategic-synthesis.md).

1. **Most DAF "accounts" are pass-through processor accounts.** They are 79.5% of accounts and hold 0.9% of assets. Traditional invested accounts number at most 737k.
2. **Software is two markets plus one captive market.** About 39% of assets sit at affiliate-linked nationals. Fully outsourced administration covers ≥6 sponsors holding 9.1% of assets. The community-foundation long tail is on Foundant.
3. **Apparently independent wealth-firm DAFs share one sponsor–vendor spine (RCF + Ren).** Ren's DFX portal also fronts Morgan Stanley GIFT (new), Bank of America's fund and AEF, and Ren-owned iPhi serves the Cleveland Foundation and ImpactAssets.
4. **Ren's ">half of DAF assets" claim is unsupported on public evidence.** Publicly evidenced Ren-linked sponsors hold about 8.7%, and the "$200bn" figure includes non-DAF assets.
5. **The value pool for DAF operations AI is thin, and redesign should precede AI.** The model's "AI ranks last" result is an artifact of its assumptions.
6. **The agentic AI frontier is donor-side**, through TIFIN Give's Louise and Daffy's MCP server. No public evidence shows AI in sponsor-side approval.
7. **Payout splits behind the average.** The median sponsor pays out about 11–12.5%, and about one in five sponsors with ≥$1m pays out under 5%.
8. **Fee pass-through is near-total at RCF.** RCF pays Ren 98% of its individual-fundholder admin-fee revenue. The causal effect on payout is unsupported, and segment medians run against it.
9. **Portability is a legal right with operational lock-in.** No sponsor publishes an outbound transfer policy or offers history portability.
10. **A previously unknown vendor, Give Interactive, holds Vanguard Charitable's DAF recordkeeping.**

## Contradictions and unresolved questions

**Resolved contradictions:**
- **Concentration:** CR3 58% vs 45.5% came from a period mismatch; 45.5% is correct.
- **NPT FY2025 grants:** $6.44bn is the U.S. DAF program; $6.61bn likely includes the U.K.
- **SPLC grant holds:** confirmed by the California AG's release.

**Contradicted prior claims:**
- The Bank of America 10-K evidence of Ren. The only evidence is the portal.
- Chariot's "Fidelity electronic-only by July 2026". Not confirmed; about 67% of Fidelity grants already go by EFT.
- The entrant model's "model-assisted clearing". Reconciled to deterministic clearing only.

**Still unresolved:**
- Ren's denominator for its share claims.
- Ren's SOC 2 Type 1 vs Type 2 statements.
- Sponsor, administrator and technology vendor for the Edward Jones private DAF and Goldman Sachs.
- Give Interactive's scope at Vanguard Charitable.
- Whether sponsor–vendor contracts grant API and data-export rights.
- Real exception rates and handling times anywhere in the market.
- Fund-level payout by fee model.
- Content of the forthcoming §4966/6033 guidance.
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
