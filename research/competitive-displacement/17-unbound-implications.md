# 17 - Unbound implications

Status: research (2026-11-26). **Proposals only.** Unbound owns product requirements and architecture; nothing here is an approved requirement, and no file in `kemiller2002/unbound` was changed by this initiative. Each item is traceable in [cross-repository-implications.csv](data/registers/cross-repository-implications.csv).

| ID | Area | Proposal | Evidence | Type |
|---|---|---|---|---|
| XRI-001 | Convergence OD-M-05 / SPD-CMP-001 | Raise an owner decision to re-test the ratified entry segment; the target segment is the least mobile in the switch record | CLM-015, CLM-016, CLM-027; [07](07-institutional-switching-incentives.md) | Open question for owner |
| XRI-002 | Charities (UNB-KNOW; CNV-GRT-003) | Adopt nine evidence classes with explicit promotion rules: AI-generated and inferred records can never become authoritative facts | [04](04-charity-intelligence-architecture.md) | Requirement candidate |
| XRI-003 | Charities / 180-day decision record | Treat change-driven monitoring + evidence expiry + sample audit as the re-verification method; full repetition costs ~4x | CLM-005; [05](05-charity-registry-economics.md) | Requirement candidate (needs counsel/auditor) |
| XRI-004 | Charity sources | Add trade.gov CSL, FCDO UK Sanctions List (replacing OFSI), Federal Audit Clearinghouse, SAM exclusions; exclude ProPublica, GivingTuesday, OpenSanctions, EMMA from any shared/resold layer | CLM-006, CLM-007, CLM-009; [02](02-charity-intelligence-sources.md), [03](03-charity-data-licensing-and-access.md) | Requirement candidate |
| XRI-005 | Charity knowledge architecture | Archive every IRS and sanctions release from day one | CLM-010 | Architecture note |
| XRI-006 | Instrumentation | Record touch/no-touch, minutes and failure lifecycle per operational event so modelled rates can be replaced by measured ones | [09](09-event-level-operating-model.md) | Requirement candidate |
| XRI-007 | Prevention | Prioritise notification-first contribution intents, validated recommendation forms, pre-validated policy rules and verified destinations above AI exception handling | CLM-011; [10](10-zero-touch-administration-economics.md) | Requirement candidate |
| XRI-008 | Operating modes | Ensure Release 1 can run as **technology-only licensing** with the sponsor or a partner operating exceptions (MD-6/MD-7) | [14](14-alternative-enterprise-models.md), [16](16-commercial-entry-strategy.md) | Requirement candidate (depends on DEC-001) |

## What Unbound should deliberately not build (now)

- A proprietary charity payment network or any requirement that charities log in to be paid (DEC-009; consistent with CNV-LEG-001 and PR #88).
- A ratings or "charity quality" product (licence-restricted inputs; defamation exposure; no buyer evidence).
- A generic ELT engine beyond Transitus phase 1 (PR #89 D-MIT-001: rejected on licence economics).
- Vendor-specific migration packages before a customer-authorised sample exists (D-MIT-002 revised; DEC-011).
- A community-foundation fund-accounting suite to compete with Foundant head-on (non-DAF fund types are out of scope; CF economics rejected in EV-04).
- Custodial administration operations before an anchor (DEC-002).
- Advisor-channel integrations into slots already held (Orion, Envestnet) as an entry bet.

## Conflicts escalated, not resolved

- **OD-M-05 vs switching evidence** (DEC-001).
- **CNV-ECO-004 concentration cap** is breached by every single-customer start in every route; the cap needs a stated transition policy (PR #88 already noted this for administration; it applies equally to licensing).
