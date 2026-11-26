# 21 - Evidence gaps

Status: research (2026-11-26; revision 2 after adversarial review, see [20](20-adversarial-review.md)). Open questions are tracked in [open-questions.csv](data/registers/open-questions.csv) (OQ-001..020). Gaps are ranked by how much a resolution would move the commercial decision.

## 1. Decision-critical gaps

| Rank | Gap | Why it matters | Current state | Resolution (cost) |
|---|---|---|---|---|
| 1 | **Why institutions choose and leave vendors** (win/loss) | The entire displacement thesis and DEC-001 | Behaviour observed (44 events); reasons stated in a handful | V-1 interviews with switchers and stayers ($10-30k; OQ-001) |
| 2 | **Customer acquisition cost and sales cycle** | Capital swings most on acquisition speed | No published CAC in any segment (CLM-026) | Own pipeline instrumentation; partner disclosure (OQ-013) |
| 3 | **Channel partner appetite** | Gates the cheapest self-sustaining route (ER-7) | None tested | V-6 conversations ($5-15k; OQ-006) |
| 4 | **Price acceptance** per account and per bps | Licensing vs administration economics | List prices only | V-2 price test ($20-60k; OQ-002) |
| 5 | **Measured exception rates and handling minutes** | Event model and registry costs rest on them | Replay proxies; assumptions | V-3 replay harness ($30-80k); V-7 time study ($20-60k) (OQ-003, OQ-011) |
| 6 | **Auditor acceptance** of change-driven re-vetting and generated evidence | Removes periodic re-review and lowers audit cost | Untested | Auditor walkthrough ($0-30k; OQ-004) |
| 7 | **A real incumbent export** | Migration claims, history depth, adapter reuse | None obtained | V-4 under MSA + DPA ($40-160k; OQ-005) |
| 8 | **Why satisfied sponsors stay** (stayers' reasons) | The buyer the strategy must convert | Not sampled in revision 1 (CHL-091) | V-1 stayers |
| 9 | **Partner economics from the partner's side** | Whether a partner licenses rather than builds or acquires | Precedents point to acquisition (CLM-025) | V-6 (CHL-084) |
| 10 | **Measured name-match alert rates and exception classes** | Registry labour (CHL-048, CHL-049) | Assumptions | Screen a real 20k list against CSL/SAM/FAC |

## 2. Secondary gaps

| Gap | Note |
|---|---|
| Candid Charity Check price and terms (OQ-008) | Incumbent for paid eligibility evidence |
| Whether a licensing vendor is a Nacha TPSP (OQ-009) | Legal: counsel |
| Sharing of sponsor-confirmed resolutions (OQ-010) | Legal and contractual |
| Ren's actual SOC status and scope (OQ-015) | Public claims conflict |
| UBS programme sponsor (OQ-016) | Reconcile prior repository classification |
| Echelon commercial licence terms (OQ-017) | Carried from PR #87 |
| Reusable share of migration mappings (OQ-018) | Only a vendor claim exists (SAP 70%) |
| Share of contributions convertible to structured intents (OQ-019) | Largest prevention lever on attribution |
| Donor-level switching for grant speed (OQ-020) | Donor pain vs institutional purchase |
| Industry-average balance (~$141k) vs target-segment Schedule D averages (CHL-083) | bps viability |
| Serviceable account count by sponsor band (CHL-082) | Licensing ceiling |
| Bottom-up CAC and vendor-viability requirements of buyers (CHL-015, CHL-020) | Sales cycle and capital |
| Final status of the 2023 proposed 4966 regulations (CHL-042) | Advisor-channel economics |

## 3. Sources not verified in this session

- Blocked or unreachable: Florida Sunbiz, Ireland and New Zealand regulator sites, cfo.gov (outside the session's network allowlist), the UN list XML (404), Open990 (TLS/530), Foundant support (403).
- Read through secondary copies: ProPublica licence (search-index copy), Alkami 10-K (mirror), single-audit threshold (secondary), OpenSanctions price (2022 article).
- Vendor claims not independently checked: Ren scale and partner counts, Foundant SOC 2 Type 2 scope, Givinga and GivingTech launch times.

## 4. Model limitations

- Correlation is represented only by a simple common-quantile mixture (ρ=0.5); the true dependence structure is unknown.
- Fixed costs per mode are assumptions anchored to PR #86/#87, not quotes.
- Entry-route customer acquisition rates are assumptions with no market evidence.
- The registry model sizes stewardship by workload; it does not model dispute volume separately.
- Same model family produced, reviewed and integrated the research (no independent validation).
