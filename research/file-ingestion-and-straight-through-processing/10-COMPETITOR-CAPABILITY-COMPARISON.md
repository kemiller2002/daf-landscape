# 10 — Competitor and platform capability comparison (ingestion)

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26). Public evidence only; absence means *not found publicly*, not *does not exist*.

| Capability | Fidelity Charitable | NPT (GivingPoint, Ren-built) | DAFgiving360 | Ren / iPhi (DFX) | TIFIN Give family | Chariot | Foundant / NPact (CF software) |
|---|---|---|---|---|---|---|---|
| Incoming-securities notification before transfer | Advisor notification (FIE-A-002) | Contribution Agreement required (FIE-A-024) | Not found (site blocks readers) | Not found | Bulk securities upload (BlueGive, FIE-A-093) | n/a | Not documented |
| Unidentified-gift policy published | Rejects wires without account (FIE-A-005) | Not found | Not found | Not found | Not found | n/a | Forum evidence of problem (FIE-A-106) |
| Bulk grant upload | None documented (FIE-A-022) | Not found | Not found | Not found (FIE-A-055) | Bulk attestations (FIE-A-094) | All-or-nothing bulk create API (FIE-A-096) | Grant import (FIE-A-104, FIE-A-109) |
| Document upload channel | GivingCentral Document Upload (FIE-A-008) | Mail/fax/PDF (FIE-A-027, FIE-A-033) | Not found | Not found | Not found | n/a | Not documented |
| Charity eligibility data named | "IRS databases" (FIE-A-015) | Not named | "IRS and federal/state regulators" (FIE-A-039) | Not named | Not named | BMF, Pub 78, 990, OFAC (FIE-A-097) | Not documented |
| Grant payment rail | Stripe/ACH EFT, check (FIE-A-016) | PayPal Grant Payments, check, wire (FIE-A-035) | Mailed check (FIE-A-038) | ACH via Ren (FIE-A-068) | Chariot (FIE-A-092) | Disbursements API (FIE-A-096) | Varies (FIE-A-111) |
| Migration service | n/a (FMR platform) | n/a | n/a | One-time "Data Migration" (FIE-A-050); AEF moved only 2024–26 history (FIE-A-044) | Not found | n/a | Replatforming with blackout (FIE-A-108) |
| Payroll-giving files | Not found | Not found | Not found | Not found | Not found | n/a | Not found; Benevity/YourCause exchange files exist (FIE-A-113..117) |
| Public API for partners | Not found | Not found | DAFpay access (FIE-A-042) | API and SSO services (FIE-A-051) | Multi-custody/platform integration (FIE-A-091) | OAuth + REST (FIE-A-100) | Not documented |

**Reading.** No national sponsor publicly documents the structured, pre-validated intake that adjacent industries
treat as normal (advisor bulk files with control totals, reference-carrying contribution instructions, published
schemas). Chariot is the clearest example of an API-first participant, on the payment side. This is a capability gap
observable from public evidence; operational performance (timeliness, error rates) is not public for anyone.
