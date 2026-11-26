# W12: account establishment (onboarding)

**Outcome (BO-08–BO-10):** a donor can lawfully open an account: an identified party, an accepted agreement, and the right privileges. This should happen with minimal effort and without re-collecting data the donor or advisor has already verified.

**Evidence: Low.** The repository has no abandonment data. Six of the top 20 sponsors restrict automated access (EV-122). KYC is a risk control, not a BSA mandate, for sponsors (regulatory map §13).

| ID | Type | Mechanism | Decides / when | Authoritative data | Humans | Maturity | INN |
|---|---|---|---|---|---|---|---|
| D-W12-1 | Conventional | Application form (paper or web): identity, successors, investment choice, advisor LOA; staff review; account opened before the first gift | Staff review | Form data | Ops | Observed [I] | — |
| D-W12-2 | Automation-first | Web form with identity-provider check, e-sign and auto-approval for clean cases | Rules | Form plus IdP | Exceptions | L1 | — |
| D-W12-3 | AI-native | Conversational or progressive intake that writes the canonical Party/Account; prefill from advisor APIs; deterministic identity and privilege rules | Policy engine | Canonical record | Client ops on exceptions | L2 (parent PoC: identity gate before account) | INN-25 |
| D-W12-4 | **Radical: no application: the account crystallizes from the first verified intent** | A donor (or the advisor on the donor's behalf) declares a contribution intent. The minimum lawful set (identity at base assurance, agreement acceptance, an acknowledgment address) is collected inside that intent. Everything else (successors, investment election, recognition defaults) is asked *when a decision first needs it*. Investment defaults to a cash or conservative pool until an election is made | The donor's first act *is* the opening, so *timing* changes; policy decides each later step | Canonical record growing over time | Client ops on exceptions | L1 | INN-25 |
| D-W12-5 | Ecosystem: reliance on upstream attestations | Accept signed identity and suitability attestations from the advisor's custodian or a verified identity wallet; step up on risk | Policy plus upstream attestor | Attestation | Ops on mismatch | L1 | INN-24 |

**Constraint pass:**
- **Legal.** Agreement acceptance before advisory privileges is needed (§4966(d)(2) "reasonable expectation" of privileges). The acknowledgment must carry the exclusive-control statement (REG-008). D-W12-4 survives if the agreement is accepted inside the intent.
- **Privacy.** Attestations need consent (REG-048 where applicable).
- **Fraud.** Base-assurance accounts are capped on value until stepped up.

**Perspectives:**
- **Customer advocate:** D-W12-4 removes the biggest barrier.
- **Adversarial:** low-assurance accounts may be used to test stolen identities. Cap grants and transfers until full assurance is reached.
- **Regulatory:** successor gaps at death if never collected. Prompt within N days.

**Unresolved:** upstream attestation liability allocation.

**Experiments:** E5 compares form, progressive and crystallize-at-intent designs on steps, data completeness at first decision and exposure. Abandonment is an assumption, not measured.
**Recommendation:** adopt D-W12-3 plus D-W12-4 with value caps; test D-W12-5.
