# Outstanding work (pick-up list)

**Created:** 2026-11-21. **Scope rule (owner):** this is analysis of what an AI-native DAF company would need to build and how it should work, not an implementation. No new API contracts are written. Completed artifacts are kept.

**How to resume:**
- Work top-down within each group and mark each item `done` here, with the commit.
- Easy items (group A) come first.
- Run `cd models && dotnet test` before committing any model change.

## A. Consistency clean-up (easy; no outside input)

| # | Item | Where | Done when | Status |
|---|---|---|---|---|
| A1 | Map each legal requirement (REG id) to at least one control (CTL id) | `08-governance-and-compliance/reg-control-mapping.csv` | 46 of 50 legal requirements mapped; 4 do not apply to a sponsor; 10 missing controls added (CTL-055 to CTL-064); test added | **done** |
| A2 | Reconcile agent names used in functional areas, workflows and workflow-innovation with the 19-agent catalog | `05-agent-architecture/agent-catalog.csv`; `workflow-innovation/06-agent-opportunities/` | A scan of every document found no unmapped agent name; 4 wordings were added to the mapping table (`workflow-innovation/06-agent-opportunities/agent-opportunity-catalog.md` §3) | **done** |
| A3 | Map functional-area local workflow IDs (WF-A1…WF-N5) to WF-01…WF-24, or list them as sub-workflows | `02-business-capabilities/functional-areas/local-workflow-mapping.csv` | 73 local workflows: 58 mapped to a WF or XW workflow (same as, part of, related), 15 area-local | **done** |
| A4 | Decide on the ~40 proposed events and ~20 interface groups from the cross-enterprise workflows: add to the catalogs or reject with a reason | `workflow-innovation/04-cross-enterprise-workflows/README.md`; `06-data-and-knowledge/events.csv`; `04-enterprise-apis/api-catalog.csv` | Each proposal is marked added or rejected; coverage tests still pass | open |
| A5 | Decide on the interface details raised earlier: batch recommendations, grant verification, party preferences, policy evaluate, shared-determination entity | `04-enterprise-apis/api-catalog.md` | Each is marked added or rejected | open |
| A6 | Apply the adversarial review's design-level maturity downgrades to the design catalog | `workflow-innovation/03-alternative-designs/design-catalog.csv` | Added `audit_verdict` and `maturity_after_audit` for all 45 reviewed designs; 8 downgrades applied; W1–W5 placeholders and 2 missing designs filled from the review | **done** |
| A7 | Cost model assumes 18 agent families; the reconciled catalog has 31. Update `AgentFamilies` and regenerate outputs (agent-owner FTE rises from 4 to 7 at 6 families per owner), then update the headline staffing figures in 09- and 14- | `models/Daf.Enterprise/Economics.fs`; `09-financial-models/`; `14-executive-conclusions/` | Outputs regenerated; documents consistent; tests pass | open |

## B. Analysis that public data or models can support (medium effort; no outside input)

| # | Item | Done when | Status |
|---|---|---|---|
| B1 | Add a determination-reuse parameter (reusable foreign-charity and fiscal-sponsor reviews) to the cost model; rerun sensitivity | Parameter in `Economics.fs`, outputs regenerated, financial doc updated | open |
| B2 | Small-sponsor Schedule I harvest (outside the top 50); rerun the overlap (E7/E7b) and network-economics analyses | New data and results; network conclusions updated | open |
| B3 | Adversarial cases the review asked for: poisoned data load and name collision (E1); adaptive fraudster, correlated AI misses and reviewer automation bias (E2); payee-registry compromise blast radius (E3) | Each case is a test that can fail; results documented | open |
| B4 | Build or explicitly drop the experiments cited but never built: complex-asset queue, contact-volume model, liquidity forecast, policy back-test | Built with results, or removed from the citing documents | open |
| B5 | Charity vetting: improve candidate matching for "which charity is this" (abbreviations, nicknames, addresses) and rerun V1 | Higher share of true answers among candidates, documented | open |
| B6 | Charity vetting: check that genuine sanctions matches are still caught when names are spelled or transliterated differently (V2) | Recall reported | open |
| B7 | Charity vetting: check whether false sanctions alerts fall unevenly by name origin, with a privacy-preserving design and no organization named | Method and result documented | open |
| B8 | Charity vetting: accuracy of extracting figures from charity tax filings, using e-file XML as ground truth | Protocol and baseline documented | open |

## C. Needs outside help or an owner decision (blocked)

| # | Item | Blocked on | Gap ID |
|---|---|---|---|
| C1 | Shadow replay of a sponsor's past grants with timed human review (exception rate, minutes, error rate) | A sponsor partner | GAP-001, GAP-004, GAP-034 |
| C2 | Reconciliation break rates and cost | A sponsor partner | GAP-005 |
| C3 | Executed sponsor–vendor contracts (API and export rights) | Contract access | GAP-002 |
| C4 | Money-transmitter status of an instruction-only operator; reliance on another sponsor's reviews | Counsel | GAP-012; REG-019/020 |
| C5 | Willingness to pay (~$300 per account), partner sponsor-of-record terms, donor acceptance of execution windows | Interviews; owner approval for outreach | GAP-014, GAP-027 |
| C6 | Schwab, Fidelity and BNY Pershing API references | Developer-portal login or NDA | vendor assessment §6 |
| C7 | Vendor confirmations: J.P. Morgan ACH idempotency; Column, Increase and Apex charity-titled accounts; Auth0 and WorkOS federation and MFA behaviour | Vendor documentation or sales contact | vendor assessment §6 |
| C8 | Run an AI matcher on the charity-identification benchmark (V1 referred cases) | Model API access in the environment | charity-vetting-ai §10 |
| C9 | Final Treasury/IRS guidance under §§4966 and 6033 | External event | GAP-008 |

## Log

| Date | Item | Commit |
|---|---|---|
| 2026-11-21 | List created | 2ffeb18 |
| 2026-11-21 | A1 done | bb4f8da |
| 2026-11-21 | A6 done | d00cc9b, 428542d |
| 2026-11-21 | A2 done; A7 added | 215ee5e |
| 2026-11-21 | A3 done | (this commit) |
