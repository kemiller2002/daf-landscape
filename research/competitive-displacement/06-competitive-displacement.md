# 06 - Competitive displacement

Status: research (2026-11-26; revision 2 after adversarial review, see [20](20-adversarial-review.md)). Public sources only. Registers: [competitors.csv](data/registers/competitors.csv) (16 competitors, CMP-001..016), [trackC-weakness-matrix.csv](data/evidence/trackC-weakness-matrix.csv) (25 candidate weaknesses W01-W25), [trackC-switches.csv](data/evidence/trackC-switches.csv) (44 events S01-S44), notes [trackC-notes.md](data/evidence/trackC-notes.md) (SRC-065). Prior work cited, not repeated: the Ren/TIFIN/Chariot deep dive, Ren contract and fee-share audits, iPhi attrition census (SRC-011), PR #88 report 03 and PR #87 report 13.

**Absence rule.** A feature missing from public pages is recorded as UNKNOWN, never as a limitation.

## 1. Competitor positions (summary)

| Competitor | Role | Primary buyers | Strength that matters to buyers | Public weakness (classified) |
|---|---|---|---|---|
| Ren (DFX, iPhi/Stellar, GivingPoint; RCF related party) | Software + administration + sponsor relationship | National, faith and advisor-distributed sponsors; wealth firms | Distribution: 150+ platform partners (VENDOR-CLAIM); RCF passes ~98% of fundholder fees (VERIFIED, CLM-017); scale; Great Hill capital 2025; **already automated vetting, rapid disbursement and digital payments** (VENDOR-CLAIM, CHL-003) | Narrow template exit terms (W04). Segment behaviour, cause unknown: 5 of 28 iPhi CFs left (~5% a year; overall iPhi ~3% a year, national/faith ~1% a year), which is strong retention, not a weakness (W07 reclassified, CHL-006). Unexplained SOC Type II (2025) vs Type 1 (2026) statements, plausibly a scope change; scope unknown (W09 downgraded, CHL-007). Multi-lineage stack (HYPOTHESIS, W06) |
| TIFIN Give (GiveClear sponsor; Chariot payments) | Advisor-led platform | RIAs, wealth platforms, banks and trust companies via SEI | Shipping velocity: AI assistant (Oct 2025), Chariot (Dec 2025), SEI white label (Jan 2026), Confluence (Feb 2026) | Multi-entity accountability (HYPOTHESIS W18); ledger depth undocumented (UNKNOWN W17) |
| Foundation Source (Vennfi, Giving Place, Pacific Foundation Services) | Consolidating administrator and technology | Private foundations, wealth firms (TIAA), Charityvest | Acquisitions 2024-25; multi-custodial advisor-branded DAFs via BridgeFT | UNKNOWN (SOC reports are restricted-use; absence of a public report is not a weakness, CHL-010) |
| Foundant (CommunitySuite; merged with SmartSimple) | Integrated CF fund accounting + portal | Community foundations | **Wins most observed CF switches** (VERIFIED); 30-day termination for convenience in template | User-review allegations: reporting curve, dated UI (W14) |
| NPact (FIMS, DonorCentral, Foundation Cloud) | Legacy platform owner | Community foundations; AEF (until 2026) | Installed base inherited from Blackbaud 2022 | 3-year term + 90-day notice; deletion 10 business days after hosting; paid export (W04-W05); reduced self-admin (W12) |
| Give Interactive | Platform (Signatry-owned) | Faith and national sponsors | SOC 2 Type 2 and SOC 3 (Sept 2025, scope unstated) | Viability (loss-making; implementation abandonment, HYPOTHESIS W16) |
| GiftingNetwork, akoyaGO, GivingTech, Givinga, Chariot, Daffy for Work, Endaoment, Bonterra, in-house Salesforce builds | Niche platforms and channel entrants | Various | Price transparency (Givinga $12.5k base; Daffy $3 per employee-month); custodian embedding (Endaoment in Altruist) | Mostly UNKNOWN |

## 2. Perspectives

| Perspective | What they value | Ren's position | Opening for an AI-native entrant |
|---|---|---|---|
| Institutional buyer (wealth firm, bank) | Revenue share, brand, adviser retention, low operational burden | Strong: fee-sharing, private label, scale | Weak unless economics match |
| Sponsor executive | Mission, donor experience, cost, board risk | Strong at national/advisor sponsors; weaker at CFs | Integration and verifiable migration at CFs/faith (behaviour, not stated reason) |
| Compliance officer | Defensible vetting, audit trail, sanctions | Adequate (automated vetting claimed; GuideStar Charity Check named in RCF policy) | Provenance-bound replayable decisions (no competitor documents this; SRC-001) |
| CFO / accounting | Single ledger, reconciliation, audit cost | UNKNOWN (ledger unification not publicly documented; W06 is a hypothesis, CHL-009) | Single operational ledger with generated evidence (ADV-007); custodian, bank and GL reconciliation remain (CHL-059) |
| Wealth manager | Integration with custodian/CRM, speed, AUM retention | Strong integrations; advisor-managed investments | Parity at best; Orion/Envestnet slots taken (SRC-032) |
| Operations | Fewer exceptions, no re-keying | Unknown internal efficiency | Prevention-first design ([10](10-zero-touch-administration-economics.md)) |
| Donor | Speed, mobile, history, fees | Adequate; complaints are sponsor-level (grant delays, checks) | Full history after migration; no freeze |
| Charity | Fast electronic payment, no portal burden | 140k+ recipients paid; enrolment history | Never require a charity login; partner rails (parity) |
| Implementation team | Clear data contracts, rehearsal, API | Paid migration add-on; no published outcomes | Rehearsed, reconciliation-gated migration with published outcomes |
| Information security | SOC 2 Type 2 history, scoped reports | Claims conflict (Type II 2025 / Type 1 2026) | **Disadvantage**: an entrant has no SOC history (CLM-040) |

## 3. Competitive displacement matrix (selected; full matrix in evidence file)

| Weakness | Class | Measurable pain? / who | Purchase controller | Changes purchasing? | Unbound can solve? | Incumbent replication | Evidence that would establish advantage |
|---|---|---|---|---|---|---|---|
| W08 Fragmented legacy stacks (separate GL, portal, logins) | VERIFIED (stated switch reason) | Yes; ops, CFO, donor | Sponsor exec | **Yes** (Vermont, CNY, Arizona) | Yes, if it offers the integrated scope the buyer wants (fund accounting for CFs) | Foundant already does it for CFs | Win against Foundant in a CF evaluation |
| W21 Vendor-forced migration calendars (Blackbaud→NPact, re-hosting) | VERIFIED | Yes; exec, ops | Sponsor exec | **Partly** (forced events open windows) | Yes (be present at the window) | N/A | Pipeline built from contract-end calendar (OQ-012) |
| W02/W03/W20 Freezes, re-registration, in-flight loss | VERIFIED | Yes; donors, charities, ops | Sponsor exec | Not observed as a reason | Partly (queued submissions; pre-provisioned identities; in-flight register); short freezes depend on the incumbent delivering the final extract (CHL-074) | 3-6 months at observed incumbent release cadence (CHL-012) | Measured freeze under 5 days on a real migration |
| W01 Truncated history (AEF 2 years) | VERIFIED (default depth; deeper history delivered when contracted: GWCF 7 years, Arizona 26) | Yes; donors, advisers, compliance | Sponsor exec/CFO | Not observed | Yes (legacy partition + roll-forward proof; SRC-001) | **0 months**: incumbents already deliver it when paid (CHL-008) | Full history migrated with per-fund proofs |
| W04/W05 Narrow exit terms, multi-year lock-in | VERIFIED (templates) | Yes; CFO, counsel | Sponsor exec + counsel | Not observed (raises the cost of leaving) | Yes (symmetric exit; trivial) | Trivial | Buyers citing exit terms in selection |
| W22 No published migration outcome metrics | VERIFIED (disclosure) | Unknown | Sponsor exec | Unknown (HYP-003) | Yes | 0-3 months for the promise; incumbents can back it with balance sheet and history (CHL-004) | Selection reasons naming commitments |
| W11 Opaque institutional pricing | VERIFIED (disclosure) | Weak | CFO | No evidence | Yes | Trivial | None expected |
| W07 Ren losing CFs | VERIFIED behaviour | N/A | CF exec | Yes, but to Foundant/akoyaGO | Only with CF fund accounting scope | N/A | Unbound winning a CF |
| W24 Fee-sharing economics | VERIFIED fact; weakness is HYPOTHESIS | Donors pay (indirect) | Wealth firm + sponsor | **Works in Ren's favour** (Commonwealth stayed through LPL conversion) | No without matching economics | N/A | — |
| W25 Grant delays and checks (national sponsors) | ALLEGATION | Donors, charities | Donor (account level) | Donor-level moves observed (DAFgiving360 → Fidelity anecdotes) | Partly (rails) | Low | Donor churn data |
| W09 Differing assurance statements | Unexplained discrepancy; scope unknown | Infosec | Procurement | Not observed (AEF chose Ren anyway) | Only with own SOC history | N/A | — |

## 4. Why an institution keeps an inferior product

Observed or strongly supported:
1. **Revenue alignment**: sponsor-of-record and adviser economics flow to the incumbent (RCF 98% pass-through; adviser compensation 0-100 bps at TIFIN; Morgan Stanley $4.24M as GIFT adviser).
2. **Legal structure**: in advisor programs the assets sit in a vendor-affiliated charity; they can leave only grant by grant with that charity's approval.
3. **Switching cost borne by the buyer**: $170k-846k base TCO (PR #88), staff time, dual running, tail fees ($417,742 JCF payment to Ren for prior portal support).
4. **Risk asymmetry**: freezes and lost history are visible to donors and boards; the gain from a better product is diffuse.
5. **Contract mechanics**: auto-renewal, notice windows, paid export.
6. **Incumbent investment**: Great Hill (Ren), GTCR-backed acquisitions (Foundation Source), SmartSimple merger, TIFIN shipping cadence (CLM-032) mean "inferior" is a moving target.

## 5. Verified versus unverified

- **Verified limitations**: W02-W05, W08, W11-W12, W19-W22 (templates, notices). W01 is a default, not a limit; W07 is segment behaviour with unknown cause; W09 is an unexplained discrepancy (revision 2).
- **Allegations**: W13 (FIMS errors, Arizona self-report), W14, W15, W25.
- **Hypotheses**: W06, W16, W18, W24 as a weakness.
- **Unknown**: W10 (no public attestation for several vendors; restricted-use reports), W17 (TIFIN ledger depth), W06 (ledger unification).
- **Incumbents are ahead on repetition**: Foundant reports 700+ CommunitySuite foundations and has absorbed many FIMS conversions; Ren has migrated several acquired books. Learning economies favour them today (CHL-002).

## 6. Conclusion

Displacement opportunities are real but narrow: **integration-driven re-platforming at community and faith foundations, and vendor-forced windows**. In those, the observed winner is Foundant, an integrated fund-accounting suite, not a DAF-only platform. At national and advisor-distributed sponsors the incumbent advantage is economic and structural, not technical, and no observed switch was driven by a technical weakness an entrant could exploit ([07](07-institutional-switching-incentives.md)).
