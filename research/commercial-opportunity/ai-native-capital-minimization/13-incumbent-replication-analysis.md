# 13: Incumbent replication analysis

**Pass:** COM (part 4). **Data:** [`replication.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/replication.csv) (7 advantages + combination + 4 incumbent responses).

**Integrator conclusions**
- **The previous study's "easily copied" verdict is refined, not reversed.**
- **Each lever alone is copyable in about 6-24 months.** Minimum-touch operations *raise* a bps-priced incumbent's margin, so incumbents will copy them quietly without cutting price.
- **The combination is moderately durable against multi-lineage incumbents.** The combination is a single ledger with evidence-by-default controls, reusable configuration, portability and per-account pricing. An incumbent such as Ren runs an acquisition stack with separate contracts and no observed ledger unification, so transforming its installed base would take about 48-72 months.
- **It is not durable against:**
  - a funded greenfield sub-brand or an acquisition, at about 18-30 months;
  - incumbents that already transform: Vanguard spends $2-6M a year on tech services, Fidelity paid McKinsey $11.8M, and Foundant won 6 of 8 recorded community-foundation migrations.
- Replication scores are analyst judgement (same model family). No incumbent was interviewed.

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Part 4: incumbent replication

Full scores: `replication.csv` (1 = easy for incumbent, 5 = hard; [E] judgement on repo evidence).

| Advantage | Concept | Tech | Org | Capital | Time | Migration | Revenue disruption | Ops disruption | Mean | Months to match (favourable to incumbent / unfavourable) | Revised verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Shared verification network | 1 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1.5 | 6-12 / 18-24 | Weak; network effects favour largest incumbents |
| Integrated accounting + evidence-by-default | 2 | 4 | 3 | 4 | 4 | 4 | 2 | 4 | 3.4 | 18-30 single-codebase / 36-60 multi-lineage | Most durable technical edge vs multi-lineage vendors; entrant has no SOC history |
| Reusable configuration | 1 | 3 | 3 | 2 | 3 | 3 | 2 | 2 | 2.4 | 12-18 / 24-36 | Temporary for new clients; slow for installed base |
| Minimum-touch operations | 1 | 2 | 4 | 2 | 3 | 2 | 1 | 3 | 2.3 | 6-18 / 24-36 | Temporary - bps-priced incumbents gain margin by copying |
| Per-account / payout-neutral pricing | 1 | 1 | 2 | 1 | 1 | 1 | 4 | 1 | 1.5 | 0-6 selective / 12-36 book-wide | Positioning; selective re-tiering is cheap |
| Portability | 1 | 3 | 2 | 2 | 2 | 1 | 3 | 1 | 1.9 | 3-6 contract / 18-30 full-fidelity | Promise copyable; full-fidelity export slower |
| AI-native development | 2 | 3 | 4 | 2 | 3 | 2 | 1 | 2 | 2.4 | 6-12 / 24-48 | Weak and unverified for Echelon (ECH-02; PolyForm NC) |
| **All seven combined** | 2 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 3.9 | 18-30 greenfield or acquisition / 48-72 installed-base transformation | Moderately durable vs transformation; not vs greenfield/acquisition |

**Understanding vs implementing.** Every advantage is conceptually easy (scores 1-2). Implementation difficulty lives in: (1) **legacy architecture** - Ren's platform is an acquisition stack (Blackbaud DAF tech 2011, DonorFirst 2016, Pinkaloo 2021, iPhi/Stellar 2023) with separate MSAs and no observed ledger unification; (2) **customisations and contracts** - per-client order forms/SOWs, 15-day export windows, annual auto-renewal; (3) **cannibalisation** - per-account pricing halves Ren's USCGT revenue (40 -> 20 bps) while leaving MS GIFT unchanged, so incumbents re-tier selectively; (4) **migration risk** - re-platforming their own clients risks the 3-customer concentration (85.8% of named receipts); (5) **assurance dependencies** - SOC reports scoped to existing systems; (6) **customer resistance** - sponsors just migrated (AEF 2026) will not move again soon; (7) **incentives** - minimum-touch ops *raise* a bps incumbent's margin, so they will copy those levers quietly without lowering price.

**Do not assume incumbents cannot transform.** Evidence of capacity: Vanguard Charitable spends $2-6M/yr on tech services; Fidelity $11.8M on consulting; Foundant has won 6 of 8 recorded CF migrations; Schwab rebranded to DAFgiving360; Ren has executed four acquisitions; TIFIN ships agentic AI. The incumbent's best move is not transforming the installed base but **launching a greenfield sub-brand** on modern infrastructure, migrating selectively, or **acquiring** the entrant (repo: six of six DAF-tech exits went to consolidators).

**Responses modelled.** Favourable to the entrant: Ren preoccupied with iPhi/DFX integration and CF attrition to Foundant; Foundant not in BPO; TIFIN focused on adviser distribution; captives are not buyers. Unfavourable: selective re-tiering and waived change orders at renewals (0-6 months); 'managed services' bundled on Stellar at marginal cost; Foundant adds BPO + continuous monitoring for all fund types (CFs prefer one system: Unbound EV-04); channel owners cross-subsidise admin from advisory fees; greenfield competitor or acquisition within 18-30 months. **Net:** the previous 'easily copied' verdict is too strong for the combination against multi-lineage incumbents and about right for each lever alone and for well-funded greenfield responses. The window is roughly 2-4 years, which must be enough to earn SOC history and measured unit cost.

## Limitations and evidence gaps

1. **Value delivered is modelled, not observed.** Bottom-up cost uses the previous activity model (no time study; [A] parameters); top-down uses [A] replaceable shares. No sponsor cost-by-activity data is public.
2. **Donor-fee revenue** is realised only for Fidelity, RCF, JCF, CJP, NCF; others are schedule x realisation [E] (calibration n=3, range 0.38-0.68).
3. **DAF opex allocation by asset share** overstates DAF cost at CFs with large non-DAF endowments and understates it where DAFs are labour-intensive; BofA CGF 990 opex ($70,800) excludes trustee compensation netted elsewhere - its row is unreliable.
4. **Advisor-programme value** sees only the 990 vendor line; affiliate staff (e.g. Ayco, Stifel Trust) is invisible, so value is understated for software-only buyers.
5. **Service-quality value** (turnaround, errors, transparency) is not quantified; it can only be argued, not priced, until measured.
6. **No executed contract, design-partner term, implementation amount or equity arrangement** in DAF is public; search-snippet sources (Foundant POC migration, Blackbaud 10-K, NC ABLE) are quality C and were not read in full.
7. **Replication scores and time-to-match are analyst judgement** from public evidence; incumbents' internal architecture, budgets and plans are unknown.
8. **Same-model reasoning** throughout; prices and structures must be tested in owner-led buyer conversations quoting bps and $/account side by side.
9. Servicer contribution excludes company fixed cost; see previous study's fixed budget ($1.1-1.7M).
