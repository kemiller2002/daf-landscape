# Questions requiring owner decisions

This program does not decide consequential business, legal or policy questions. Each item below names the decision authority, the options, the program's recommendation, and what is blocked until it is decided. "Blocks" means the dependent requirements should not move past *Proposed* status.

| ID | Question | Authority | Options | Program recommendation | Blocks |
|---|---|---|---|---|---|
| OD-01 | Can a board-delegated, version-pinned policy be the sponsor's approval of each routine grant? | Sponsor board + GC [C] | Yes with conditions · batch human approval · per-grant human | Seek opinion; until then treat DD-004 as a hypothesis | DD-004 routine path; headcount model; TVCTL-09 |
| OD-02 | Which sanctions false-positive classes may a deterministic rule clear? | CRCO + GC | None · enumerated classes with QA sampling | Enumerated classes; a model never clears | TVC-006 resolution |
| OD-03 | On donor or sole-advisor death, what happens to sponsor-approved, unpaid grants? | Sponsor board + GC | Complete · hold for successor · cancel | Complete (sponsor's own decision); suspend standing recommendations | GR-8; CW-11 |
| OD-04 | Provisional credit limit for reversible contributions, and acknowledgment timing | CFO + GC [C] | 0 · per-donor limit · full credit | Per-donor limit, default 0 for new donors; acknowledgment timing per counsel | CON-1..3; TVCTL-03 |
| OD-05 | Valuation haircut rates by asset class for reservable capacity | CFO + Investment Committee | Rates per class | Set with back-test against historical drawdowns | FI-05 |
| OD-06 | Is reservation atomic with approval? | CFO + product owner | Atomic (approval fails on capacity) · separate (approved-pending-capacity) | Atomic for routine path; separate for human-approved large grants | FI-08 UX |
| OD-07 | When is a percentage grant fixed? | CFO + product owner [P] | At approval · at liquidation | At approval | FI-10; W02 copy |
| OD-08 | Priority among approved grants in an over-committed fund | Sponsor board [P] | Approval order · pro rata · sponsor discretion | Approval order, with case review | FI-12 |
| OD-09 | Destination and tax-reporting treatment of a recipient refund | CFO + GC [C] | Back to fund · sponsor general · redirect | Counsel | FI-20; CW-25 |
| OD-10 | Fee vs grant priority when a fund is over-committed | CFO [P] | Fee first · grants first | Fee accrual reduces capacity (FI-25), which makes this rare; decide anyway | FI-26 |
| OD-11 | Destination of trailing receipts after closure | Sponsor board [P] | Successor fund · sponsor unrestricted · original grantee | Per agreement; default sponsor policy | FI-35 |
| OD-12 | Retention schedule per record class, and precedence over privacy deletion | GC [C] | — | Counsel | Ontology retention classes; CW-35 |
| OD-13 | Funding mechanism: currency reservation with haircut vs cash sleeve | CFO + Investment Committee + advisor partners | 1C · 1D · 1E (pool buffer) · hybrid | **Open: no program recommendation.** Rev 1 recommended a hybrid; the architecture and economics reviews dispute it and prefer 1E + 1C (alternatives §1) | State model simplification |
| OD-14 | Agent-originated grant confirmation rule | Product owner + CRCO | Confirm above cap · confirm new recipients · confirm all | Confirm new recipients always, plus caps | TVC-026 |
| OD-15 | Single requirements body: merge `docs/` and `research/ai-native-daf-enterprise/` requirement IDs? | Product owner | Merge · cross-reference map · keep separate | Cross-reference map now; merge before any implementation | TVF-030 |
| OD-16 | Technology commitments in requirement text (Limen, Forma, Folio, WASM) | Product owner + architecture owner | Keep · move to ADR-gated candidate list | Move to candidate list | TVC-002 |
| OD-17 | Delegation-of-authority values (grant approval and write-off thresholds) | Sponsor board | One DoA table | One table as data | TVC-004/005 |
| OD-18 | Reconciliation accountability outside the Controller | CFO + Audit Committee | — | Yes | TVC-028 |
| OD-19 | Grant recognition point (ASC 958 promise to give) and period/tax-year attribution of late, cross-year and Unknown items | CFO + external CPA [C] | At approval · at notification to the charity · at payment | CPA opinion; does notifying the charity at approval create an unconditional promise? | FI facts 2–12 timing; Schedule D; TIME-3 |
| OD-20 | Error-cost and loss-bearer policy: misdirected or forged payments, provider insolvency (PA-8 `Lost`), inter-fund errors | Sponsor board + CFO | Fund bears · sponsor bears · party at fault | Party at fault makes the fund whole; the donor's fund never silently bears sponsor or vendor error | GR-12; FI-38; PA-8 |
| OD-21 | Who may delegate to AI agents (donor only, or advisors too), and who confirms agent requests | Product owner + CRCO | Donor only · donor + primary advisor | Donor only, until the confirmation-independence rule (TVC-041) is designed | TVC-041; DD-017/021 |
| OD-22 | Standing-data authority: may any human edit payee, authority, ledger or policy data outside domain commands (break-glass)? | CTO + CRCO + Audit Committee | Never · break-glass with dual control | Never directly. Break-glass only through a domain command with dual control, and every authoritative change matched to a command event before payment (round 2 S-9) | TVF-139; catastrophic path 1 |
