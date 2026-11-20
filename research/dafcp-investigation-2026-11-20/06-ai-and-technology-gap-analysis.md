# DAFCP: AI and technology gap analysis

**Date:** 2026-11-20. **Data:** [`ai-technology-coverage.csv`](../../data/dafcp-investigation-2026-11-20/ai-technology-coverage.csv) (AT01–AT16). **Evidence:** [DE057–DE060].

## 1. Coverage levels used

Each capability is placed at one of four levels:
- **not mentioned:** the capability does not appear in public text;
- **mentioned:** the capability is named in public text;
- **tool demonstrated:** a product or tool is shown in use;
- **process redesign taught:** students are taught to redesign an operation around the capability.

Where only paid content could settle the question, the row says so.

**Sources reviewed:**
- the DAFCP page and launch release;
- the director's essay and article;
- the 2027 Forum pages and release;
- the full text of the 2025 certificate agenda;
- the CPSI page;
- the College's 2026-11-04 technology-partnership release;
- the College's AI announcements.

## 2. Results

| Capability | Level | Notes |
|---|---|---|
| AI-assisted grant vetting | not mentioned | The grant module names rules and eligible recipients only |
| Automated gift acceptance | not mentioned | Gift acceptance is framed as asset types and valuation |
| Donor-facing AI advisers | not mentioned | — |
| Workflow orchestration | not mentioned | — |
| Data validation and normalisation | not mentioned | — |
| Fraud detection | not mentioned | Ethics covers prohibited transactions, not fraud controls |
| Compliance automation | **mentioned** (generic) | "Applied compliance" appears next to "DAF technology tools"; automation is not stated |
| Explainable decision systems | not mentioned | — |
| Human review and escalation | not mentioned | — |
| Audit trails and decision provenance | not mentioned | — |
| Integration with wealth-management systems | not mentioned | The College's MoneyGuidePro, Holistiplan and fpPathfinder partnerships are not tied to DAFCP [DE059] |
| API-based DAF infrastructure | not mentioned | — |
| Cybersecurity and donor privacy | not mentioned | — |
| Data portability and vendor lock-in | not mentioned | "Succession" concerns fund succession, not moving platforms |
| Operational redesign around AI | not mentioned | — |
| "DAF technology tools" (generic) | **mentioned** | Module 6 bullet; the release says "useful technology resources" |

**Verdict.** In public materials, DAFCP *mentions* technology. There is no evidence that it demonstrates tools or teaches operational redesign. AI is absent from every College DAF material read [DE057]. The 2025 predecessor had no technology session [DE023], and the 2027 Forum's six general-session topics include none [DE058].

**Confidence:**
- that public materials lack AI and operational-technology content: High;
- about what paid Module 6 contains: Low. Settling that is OQ04.

**The College does have AI capability; it is pointed elsewhere.** Its AI work is built around retirement income (RICP): an AI planning tool and a designee chat tool. It describes its mission as strengthening human judgement "in a world of AI" [DE059]. The gap in DAF education is a choice of where to apply that capability, not a lack of it [I].

## 3. Does DAFCP prepare people to operate existing systems or to improve future ones?

**Inference (suggestive, Medium):** it prepares people to **work within existing sponsors' rules and systems**: to recognise legal issues, assess assets and refer to qualified advisers. The programme's own stated aim is to "recognize issues, understand trade-offs, and collaborate effectively with qualified advisors". Evaluating, buying or redesigning DAF technology is not a visible objective. A holder could pass without being able to answer any of these:
- How does a sponsor know a grantee's bank details have not been redirected?
- What data does a nonprofit receive with a DAFpay gift, and can the donor stay anonymous?
- What does it cost to move a fund, with its history, to another sponsor?
- Which grant-review steps are legally required and which are habit?
- What should an AI agent be allowed to do on a donor's fund?

## 4. Comparison with the repository's research on DAF technology providers

The repository already documents these capabilities in the market. The table shows what a DAFCP holder is *not visibly taught*, next to what exists.

| Capability area | What the market already does (repository evidence) | DAFCP public coverage |
|---|---|---|
| Donor-facing and agentic AI | TIFIN Give's Louise claims to execute donor requests such as recurring grants and stock contributions. Daffy exposes an MCP server with `make_donation` and `cancel_donation`. Chariot exposes an MCP connector over nonprofit gift records ([direction-ai-product-census.md](../mission-2026-11-14/direction-ai-product-census.md), AIP01–AIP07) | none |
| AI governance rule | "AI may add a flag, never clear one". Penalties attach to the sponsor and to knowing managers, so "AI approval" is a category error ([ai-governance-failure-modes.md](../mission-2026-11-14/ai-governance-failure-modes.md)) | none; Module 1 teaches the underlying §§4966/4967 liability |
| Agent identity and delegation | Daffy records adviser actions as the Organizer's own and disclaims checking designee authority ([queue-batch36-agent-terms-controls.md](../mission-2026-11-14/queue-batch36-agent-terms-controls.md); [batch 37C §6](../mission-2026-11-14/queue-batch37-controls-education.md)) | none |
| Charity vetting and grant approval | Ren "Automatic Charity Vetting", with no AI label; benchmark designs ([batch-2b-ren-tifin-chariot-charity-vetting-infrastructure-2026-11-12.md](../batch-2b-ren-tifin-chariot-charity-vetting-infrastructure-2026-11-12.md); [daf-discretionary-grant-review-policy-explainability-audit-2026-11-12.md](../daf-discretionary-grant-review-policy-explainability-audit-2026-11-12.md)) | "grantmaking rules and eligible recipients" (legal only) |
| Integrated administration vs advisor stack | Ren: fund accounting, administration and payments. TIFIN Give: advisor stack with GiveClear as sponsor. Chariot: disbursements partner ([ren-tifin-chariot-deep-dive-2026-11-11.md](../ren-tifin-chariot-deep-dive-2026-11-11.md)) | none |
| Grant lifecycle and data | DonorFirstX/iPhi grant lifecycle trace; draft open DAF grant record ([ren-iphi-donorfirstx-grant-lifecycle-evidence-trace-2026-11-12.md](../ren-iphi-donorfirstx-grant-lifecycle-evidence-trace-2026-11-12.md); [b4013-03-02-daf-grant-record-schema.md](../mission-2026-11-14/b4013-03-02-daf-grant-record-schema.md); [direction-data-standards-interoperability.md](../mission-2026-11-14/direction-data-standards-interoperability.md)) | none |
| Payment-redirection and fraud controls | No sponsor publishes a call-back before bank-detail changes. Chariot and PayPal rails keep bank details away from sponsors ([queue-batch37-controls-education.md](../mission-2026-11-14/queue-batch37-controls-education.md) §1; [b49-04-fraud-diversion-controls.md](../mission-2026-11-14/b49-04-fraud-diversion-controls.md)) | none |
| Portability and lock-in | AEF's migration left donors with two years of directly accessible history; migration acceptance runbook ([revenue-retention-and-switching-2026-11-11.md](../revenue-retention-and-switching-2026-11-11.md); [migration-runbook-2026.md](../migration-runbook-2026.md)) | none |
| Assurance | SOC 2 public-assurance assessment ([soc2-assessment-2026-11-11.md](../soc2-assessment-2026-11-11.md)) | none |
| Noncash infrastructure | Noncash processors and vendors ([direction-noncash-gift-infrastructure.md](../mission-2026-11-14/direction-noncash-gift-infrastructure.md)) | **legal and valuation side well covered**; operational side not named |
| AI-native entry | Simulation of an AI-native sponsor entrant ([ai-native-entrant-simulation.md](../mission-2026-11-14/ai-native-entrant-simulation.md)) | none |

**Where DAF technology education happens instead.** An independent DAF Giving Summit ran sessions with Ren on using AI to reduce administrative work, and with Endaoment and Charityvest on digital-first DAFs ([DE060], [R]). Technology vendors are absent from the College's channel [DE040]. Professional canon and technology change are developing **in separate venues** [I].

## 5. Implications

1. **A competence gap with practical consequences.** Professionals who hold the only DAF-specific designation are not visibly equipped to assess any of the following:
   - agentic donor tools;
   - grant-payment controls;
   - data flows to grantees;
   - platform portability.

   These are the areas where the repository finds the most operational risk and change.
2. **An opening for complementary education.** Our research could supply evidence-based technology and operations content: control checklists, failure modes, a grant-record schema, migration tests. This content complements a credential instead of competing with it ([10](10-strategic-scenarios-and-recommendations.md)).
3. **Watch-points that would change this verdict:**
   - Module 6 is found to demonstrate platforms;
   - the College extends its RICP AI tools or planning-software integrations to DAFCP;
   - DAF technology vendors become Forum sponsors or speakers.


---

## Syllabus corrections (2026-11-20) — governing

Source: [dafcp-syllabus-findings.md](../education/dafcp-syllabus-findings.md); evidence DE074–DE083. The syllabi were read under the [owner decision on robots.txt](../education/owner-decision-robots-2026-11-20.md).

- **Verified at syllabus level (DE079).** The DAFCP syllabus contains no AI learning objective. AI appears only in a student-conduct policy. CLO7 covers "the responsible use of technology tools".
- **Required reading.** The textbook's publisher description lists "AI, blockchain, and digital platforms" as a theme. So the **required reading mentions AI**, while the **course objectives do not**.
- **CAP is the same.** The CAP syllabi show the same pattern (DE083).
