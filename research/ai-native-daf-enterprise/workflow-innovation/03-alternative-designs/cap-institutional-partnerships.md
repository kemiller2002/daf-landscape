# Capability: institutional partnerships (embedded DAF, white-label, API distribution)

**Outcome:** banks, wealth platforms, employers and fintechs can offer DAF capability to their clients without becoming sponsors.

**Evidence:**
- The RCF–Ren white-label spine (industry report §2.2).
- TIFIN Give with GiveClear powers SEI since 2026-10-28.
- Endaoment and Daffy for Developers offer sponsor-of-record APIs (industry report §8).
- The California platform law (AB 488) may reach white-label vendors (EV-094; REG-046).

| ID | Type | Mechanism | Maturity |
|---|---|---|---|
| D-INST-1 | Conventional | Branded program under a national sponsor; vendor portal; bespoke contract | Observed |
| D-INST-2 | Automation-first | Standardized program setup and SSO | L1 |
| D-INST-3 | AI-native | Tenant provisioning by configuration (program, fee schedule, menu, policy parameters); partner APIs and webhooks; evidence exports per partner | L2 (DD-016 design) |
| D-INST-4 | **Radical: program-as-code** | A partner's entire DAF program (agreement, fees, menu, policy parameters, branding) is a versioned configuration artifact that the sponsor's board approves *once as a template class*. New programs instantiate in hours, inside pre-approved parameter bounds; anything outside the bounds goes to the board | L1 |
| D-INST-5 | Ecosystem: sponsor-of-record marketplace | A partner chooses among several sponsors-of-record (national, community foundation, faith-based) on one technical platform; the platform is neutral | L0 |

**Constraint pass:**
- Each program's sponsor must govern it.
- Template-class approval needs board-defined bounds and periodic re-approval (CTL-047 parameter expiry).
- Platform registration laws (REG-046) apply.
- Revenue share must avoid commission-based solicitation (REG-030).

**Perspectives:**
- **Commercial:** D-INST-4 is the Model C/D core and has strong switching costs.
- **Regulatory:** the board cannot delegate away program governance, so bounds must be meaningful.
- **Adversarial:** a misconfigured template replicates across programs.

**Recommendation:** D-INST-3 → D-INST-4; D-INST-5 as a long-term option.
