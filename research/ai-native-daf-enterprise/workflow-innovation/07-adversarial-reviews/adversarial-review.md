# Adversarial review of the workflow-innovation program

**Reviewer:** an independent agent that did not write the register, the designs, the workflows or the experiments. **Date:** 2026-11-20.
**Posture:** I tried to disprove each claim. Where a claim survived, I say so.
**Machine-readable verdicts:** [`verdicts.csv`](verdicts.csv). It has one row for each innovation the authors recommend as Adopt or Test, one for INN-35, and one for each forwarded design.

## 1. Method

1. **Scope.**
   - Every register row with recommendation `Adopt…` or `Test`: 31 rows. INN-35 is also reviewed because its rejection rests on E2.
   - Every design marked `forwarded`, either in [`design-catalog.csv`](../03-alternative-designs/design-catalog.csv) or in the §7 "Forwarded to experiments" tables of W1–W5.
   - No "proposed additions" to the register exist in `03-alternative-designs/README.md`. A search for INN-39 and higher, "proposed addition" and similar terms returned nothing. The designs reference INN-01…38 only.
2. **The brief's 13 questions.** Each was applied to each item. The per-innovation sections (§4) record only the questions that bite. The CSV records the decisive objection.
3. **Code audit.**
   - I read every line of `models/Daf.Experiments/{Sim,Experiments,Migration,ExperimentReport}.fs` and `models/Daf.Enterprise.Tests/ExperimentTests.fs`.
   - I ran the suite: 16/16 experiment tests pass (`dotnet test --filter ExperimentTests`).
   - I then ran a sensitivity script (scratchpad, not committed) against the built `Daf.Experiments.dll`. It changed one assumption at a time. Its results appear in §5 as **[R]** (reviewer re-run).
4. **Overlap audit.**
   - Read [`recipient-overlap-evidence.md`](../08-experiments/recipient-overlap-evidence.md) and [`recipient-overlap-summary.csv`](../../../../data/workflow-innovation/recipient-overlap-summary.csv) (reuse-curve rows).
   - Not re-harvested.
5. **Cross-document checks.** These compare the register with the designs, the XW workflows, the API and agent catalogs, the reference architecture, parent controls ([`controls.csv`](../../08-governance-and-compliance/controls.csv)), DD decisions ([`DECISION-LOG.md`](../../DECISION-LOG.md)) and REG rows ([`regulatory-applicability-matrix.csv`](../../08-governance-and-compliance/regulatory-applicability-matrix.csv)).
6. **Clarity/EDF conventions** ([guide](../../../mission-2026-11-14/clarity-edf-application-guide.md)).
   - Experiment claims take EDF claim states: *internal-demonstration*, *suggestive*, *unsupported*, *contradicted*, *falsified*.
   - Confidence uses the five qualitative labels.
   - EDF diagnosis is not applied, because no item here is an observed operating outcome.
   - The overlap harvest is an observation about filings, not about verification work.

**Verdict scale:** SURVIVES; SURVIVES WITH MODIFICATIONS (SWM, with the modifications stated); DOES NOT SURVIVE (as stated); INSUFFICIENT EVIDENCE.

**Maturity test** ([methodology §5](../00-methodology/methodology.md)):
- L2 needs evidence for the *mechanism's premise*, not for the problem.
- L3 needs an executable experiment *including adversarial cases*.

I downgrade an item where evidence of the problem was cited as evidence of the mechanism, or where the cited experiment does not exist or does not test the mechanism.

## 2. Summary verdict table

| ID | Title (short) | Authors' rec. | Verdict | Claimed → justified maturity |
|---|---|---|---|---|
| INN-01 | Recipient passport | Adopt | SURVIVES (small increment over DD-012) | L2 → L2 |
| INN-02 | Cross-sponsor verification network | Test | INSUFFICIENT EVIDENCE | L1 (L2 if overlap) → overlap premise L2; value premise L1 |
| INN-03 | Pre-verified universe | Adopt | SWM | L2 → L2 |
| INN-04 | Reusable determinations | Adopt | SWM | L2 → **L1** |
| INN-05 | Policy-as-code approval | Adopt | SURVIVES | L3 → L3 |
| INN-06 | Acceptance sampling replaces per-item review | Test | **DOES NOT SURVIVE** as stated | L1 → **L0** (contradicted in the authors' own model) |
| INN-07 | Verified payee registry | Test | INSUFFICIENT EVIDENCE | L1 → L1 |
| INN-08 | Structured remittance with grant ID | Adopt | SURVIVES | L1 → L1 |
| INN-09 | Daily netting | Test | SWM | L1 → L1 |
| INN-11 | Pre-underwritten asset acceptance | Test | SWM | L1 → L1 (its experiment does not exist) |
| INN-14 | Zero-ticket servicing | Adopt | SWM; recommend **Test** | L1 → L1 |
| INN-15 | Invisible advisor-embedded DAF | Adopt | SWM | L2 → **L1** |
| INN-16 | Scoped delegation tokens | Adopt | SURVIVES | L3 → **L2** |
| INN-17 | DAF transfer protocol | Test | SWM | L1 → L1 |
| INN-18 | Always-migrated record (replay) | Adopt | SWM | L2 → L2 (E8 cannot raise it) |
| INN-19 | Spend-down horizons | Test | SURVIVES as a field pilot | L1 → L1 |
| INN-20 | Evidence ledger, auto audit package | Adopt | SWM | L3 partial → L3 partial (emission only) |
| INN-21 | Policy compiler with back-testing | Adopt | SWM | L3 partial → **L1** |
| INN-22 | Continuous close | Adopt | SWM | L2 → **L1** |
| INN-23 | Per-donor contribution references | Adopt | SWM | L1 → L1 |
| INN-24 | Upstream KYC attestation reliance | Test | INSUFFICIENT EVIDENCE | L1 → L1 |
| INN-25 | Account at first intent | Test | SWM | L1 → L1 |
| INN-26 | Donor agents as capped principals | Adopt | SURVIVES | L3 → L3 (narrow: caps and confirmation) |
| INN-27 | Pipeline liquidity planning | Adopt | SWM | L2 → **L1** |
| INN-28 | Shared specialist pool | Test | SWM (reframe) | L1 → L1 |
| INN-30 | Digital twin as management system | Adopt | SWM | L3 (sim) → **L1** |
| INN-31 | Outcome teams, no departments | Adopt | SWM; recommend **Test** | L1 → L1 |
| INN-32 | Board assurance, expiring parameters | Adopt | SURVIVES | L1 → L1 |
| INN-33 | Evidence-graded discovery | Test | SWM | L1 → L1 |
| INN-36 | Shared compliance policy packs | Test | SWM | L1 → L1 |
| INN-37 | Year-end surge smoothing | Test | INSUFFICIENT EVIDENCE | L1 → L1 |
| INN-35 | Pay-first (authors reject) | Reject | Agree with rejection; E2 does not show it | L0 → L0 |

**Counts over the 31 Adopt/Test innovations:**

| Verdict | Count |
|---|---|
| SURVIVES | 7 |
| SURVIVES WITH MODIFICATIONS | 19 |
| DOES NOT SURVIVE | 1 |
| INSUFFICIENT EVIDENCE | 4 |

The 45 forwarded designs are in the CSV:

| Verdict | Designs |
|---|---|
| SURVIVES | 13 |
| SURVIVES WITH MODIFICATIONS | 28 |
| INSUFFICIENT EVIDENCE | 4 |

Most inherit the verdict of their innovation. Design-specific findings are in §4.32.

## 3. The five most serious objections

1. **The experiments mostly restate their parameters.**
   - E5 is a table of assumed values passed through `(1−a)^steps`.
   - E10's flag-only arm hard-codes `EscapedDefects = 0` (`Experiments.fs` l.632).
   - E8 replays one log through the *same* engine twice and asserts equality (`Migration.fs` l.68–69; test l.129).
   - E9 is a hand-written truth table (`Experiments.fs` l.561–581) that the test then reads back.
   - E4's entire continuous-vs-month-end saving comes from an unsourced `MinutesPerAgeDay = 2.0`. With it set to 0 [R], both modes cost 367 h.
   - Several L2/L3 claims cite these experiments.
2. **The network effect is measured on the wrong unit, and its cold start is severe.**
   - The 51.3% "verifications avoided" counts sponsor×recipient pairs. Reuse is concentrated in large, stable, multi-funded public charities, which are the cheapest to verify from free IRS and OFAC bulk files.
   - The costly evidence is left out of Schedule I Part II: bank-account verification, foreign equivalency determinations (foreign grants are on Schedule F), and fiscal-sponsor reviews.
   - The early value of the network depends on Fidelity-class sponsors, which gain least:
     - With small sponsors first, the 2nd joiner reuses 4.3% of lines.
     - In a random order, the 2nd joiner reuses 10.0%.
     - Only with large sponsors first does the 2nd joiner reach 69.4%.
   - E1 then applies the network-wide 51.3% as a constant to *one* sponsor (`Experiments.fs` l.88, l.155). The evidence file itself says this is order-dependent.
3. **INN-06 (no per-item review; acceptance sampling only) is falsified by the authors' own E2.**
   - `RulesSamplingNoAi` lets 1,069 defects escape. `ManualReviewAll` lets 704 escape, and the AI-native design 404 ([`e2-approval-architectures.csv`](../08-experiments/results/e2-approval-architectures.csv)).
   - Hypothesis H-08 ("equal or better control effectiveness than two-person review") still stands in [`contrarian-hypotheses.md`](../02-creative-hypotheses/contrarian-hypotheses.md) l.21. INN-06 is still "Test".
4. **The AI-native control advantage in E2 is built in by its parameters.**
   - Assumed AI recall is 0.6/0.7/0.5. Assumed human routine catch is 0.3/0.5/0.2. These give the AI-native arm its lower escape count.
   - With AI recall set equal to human catch [R], AI-native lets 651 escape and `RulesPlusManualAll` 646.
   - With a 1-minute routine spot check instead of 6 minutes [R], manual review costs 15,306 h against AI-native's 15,383 h.
   - Under the authors' own prompt-injection scenario, AI-native escapes rise from 404 to 696, about the same as manual review (704).
   - The policy-as-code part (INN-05) is solid. The "AI makes control better" part is unsupported.
5. **Shared operating infrastructure moves control outside the sponsor without saying who carries the liability.**
   - INN-07 and AO-07 (payee registry): payee creation and changes move to a third-party operator. That falls outside CTL-004 and CTL-006 and is in tension with DD-008 ("never build payment rails").
   - INN-28 (pooled specialists): the people deciding are not the sponsor's officers or employees. That sits badly with DD-003 and with the §4966 fund-manager concept (REG-001).
   - INN-36 (shared policy packs): one misreading of the law spreads to every adopting sponsor.
   - Each introduces a single point whose failure hits many sponsors at once. None of the experiments models that blast radius. W3 §7 promised "blast radius of one hijack"; it was not computed.

## 4. Per-innovation findings

Each section uses the same shorthand:
- **Q-n** is brief question n.
- **[R]** is a reviewer re-run.
- An EV, REG, CTL or DD id refers to a row in the parent registers.

### 4.1 INN-01 Recipient verification passport (Adopt, L2): SURVIVES

- **Q1 (eliminates or moves).** It eliminates repeat lookups. But it is the parent decision DD-012 ("continuous eligibility monitoring replaces per-grant lookups") under a new name. The increment over the parent design is small.
- **Q12 (replicability).** Commodity. The authors' own AO-01 row names Candid Charity Check, Chariot and Ren as alternatives.
- **E1 shows nothing about accuracy.** Every automated architecture has the same escapes by construction: all use `caughtIrs` (l.146–156). The ops reduction from 100,000 to 9,759 counts machine reads of a local copy of public data against per-grant API calls. That is a vendor-pricing difference, not an architectural one. Human minutes are 0 in both arms.
- **Q9 (unusual transactions).** Name collisions and poisoned loads were promised as E1 adversarial cases (W1 §7) and were not built.
- **Verdict:** sound and cheap, but not novel. L2 is justified: grant recurrence (about 12.5 grants per recipient at Fidelity) supports the premise directly.

### 4.2 INN-02 Cross-sponsor verification network (Test): INSUFFICIENT EVIDENCE

**What the overlap evidence shows (claim state: suggestive, confidence Medium for the overlap itself):** recipients recur across top-50 sponsors.

**Method problems**
1. **The Schedule I Part II threshold excludes the long tail.** Part II lists only recipients that received more than $5,000 in aggregate from that filer. That is the long tail where per-dollar verification cost is highest. The direction of the bias is ambiguous: a recipient below $5,000 at one sponsor is also invisible as a repeat.
2. **A "line" is close to a recipient, not a grant.** Fidelity reports 72,328 lines for 71,832 recipients, against about 900k grants implied by 12.5 grants per recipient. So "71.3% of grant lines" is a pair-weighted figure, not grant-weighted.
3. **Top 50 only, and one year.** Fiscal years end between 2023-03 and 2024-12. Renaissance (rank 9) and Bank of America (rank 11) are missing. Their placeholder lines carried $1.38bn. Both are adviser-channel programs whose recipients may overlap more with Fidelity, Schwab and Vanguard. Their absence biases the overlap in an unknown direction.
4. **EIN-less lines** (2,718 lines, 1.9% of recipients) match only on exact names. This is immaterial, as the authors say.
5. **Foreign grants appear on Schedule F**, not Schedule I. The recipients where shared determinations would add most value are therefore out of sample.

**Why the network-effect interpretation is not justified**
- **"Already verified" does not mean "reusable".** Rev. Proc. 2018-32 reliance (REG-019) needs status as of the grant date, with the BMF date stated. A record verified by sponsor A in February must be refreshed for sponsor B in November, from the same free public source. The shared part is a cache of public data.
- **Reuse is concentrated on the easiest recipients.** Recipients with six or more funders take 51.9% of dollars but are only 4.6% of recipients (6–10 funders bucket plus higher).
- **Cold start.**
  - The value curve is non-monotone and depends on order. With large sponsors first, reuse peaks at 80.9% (k=5), then falls to 59.3% (k=20) and ends at 62.9% (k=48).
  - Fidelity holds 54% of distinct recipients, so the network depends on recruiting Fidelity, which needs it least.
  - Free-riding: the contributor's "credits" do not compensate the largest contributor in any modeled way.
- **The overlap does not test the valuable layer.** Bank-verification attestations and determinations carry liability and confidentiality questions (API-12 counsel flag).

**Other questions**
- **Q6, Q4.** A poisoned record propagates to every member. That makes it a correlated failure.
- **Q13.** No authority is needed to run the network. But reliance on a third party's record needs counsel (REG-019, REG-020).

**What would change my mind:** evidence that bank-verification or determination work, not the BMF lookup, is duplicated across sponsors, and that a national sponsor would contribute. This could come from partner data on payee-verification minutes per recipient, or from ED overlap in an NGOsource-type repository [K: such ED repositories already exist, which also answers Q12].

**Maturity:** the overlap premise is L2. The network's value premise stays L1.

### 4.3 INN-03 Pre-verified universe (Adopt, L2): SWM

- **Q2 and Q10 (hidden review cost; cost at scale).** "All Pub 78 plus past payees" is on the order of 1.5–2M entities [K]. Combined with INN-34, every OFAC list change fuzzy-screens the whole universe. That generates many more alerts for a sanctions officer than screening the 10–30k recipients a sponsor actually pays.
- **Modification:** keep the universe for eligibility status, which is a cheap exact-match bulk load. Run continuous sanctions screening only on active payees and past recipients. Screen the long tail on demand.
- **Q9:** churches without e-filed 990s (8.3% of top-50 dollars to church-status recipients) still need a manual or enrollment path.

### 4.4 INN-04 Reusable non-routine determinations (Adopt, L2 → L1): SWM

- **Q13 / law (REG-002).** Expenditure responsibility under §4945(h), as applied by §4966, is *per grant*: a pre-grant inquiry, a written agreement and reports for each grant. Only the pre-grant inquiry is plausibly reusable.
- **Law (REG-020).** ED reliance for DAFs rests on Notice 2006-109 and the proposed regulations. Reuse within one sponsor is plausible. Reuse across sponsors needs counsel.
- **Q5/Q9.** Stale determinations are the failure mode, and they are not modeled. In E2's `EcosystemSharedDeterminations`, reuse changes minutes only (l.285), so "no rise in escapes" holds by construction (test l.81).
- **Why L1.** The premise is cited as "12.5 grants/recipient at Fidelity". That is all-recipient recurrence, not recurrence of *exception* recipients. W2 itself says "reuse factor unmeasured".
- **Modification:** limit scope to ED and fiscal-sponsor reviews. Measure the reuse factor on exception history before claiming L2.

### 4.5 INN-05 Risk-tiered policy-as-code approval (Adopt, L3): SURVIVES

- The parent PoC (`PolicyTests.fs`, `JourneyTests.fs`) tests the deterministic path, referrals, staleness, sanctions and SoD.
- E2's canary arm claims silent rule failures are detected on day 1. That is set by fiat: the window is shrunk to one day (l.251) and detection is set to day *a* (l.310). It is not simulated.
- **Modification:** implement known-answer canary grants (CTL-046 extension) as real tests through the policy engine. Count the misconfiguration window under realistic canary coverage. Canaries catch only the rule types they exercise.

### 4.6 INN-06 Acceptance sampling instead of per-item review (Test, L1 → L0): DOES NOT SURVIVE as stated

- **In-model evidence:** escapes are 1,069 for sampling only, 704 for review of every grant and 404 for AI flags. Sampling is the worst non-pay-first architecture.
- Sampling is detective. Every sampled defect has already been paid (Q6). It is useful as CTL-049-style *monitoring on top of* rules and AI flags, not as the substitute for per-item review that H-08 claims.
- The methodology defines L1 as "no contradicting evidence known". The authors' own E2 contradicts the claim, so the claim as stated is L0 (EDF claim state: falsified in the model).

### 4.7 INN-07 Verified payee registry (Test, L1): INSUFFICIENT EVIDENCE

- **Q3, Q4, Q6.**
  - Payee creation moves from the sponsor (CTL-006: the payee creator cannot approve) to the recipient and a third-party operator.
  - A registry compromise redirects payments from *every* member sponsor. E3 does not model that blast radius.
- **Q13 and DD-008.**
  - The registry must never touch funds (REG-043).
  - Operating a multi-sponsor payee directory is close to the "build payment rails" line in DD-008. At minimum it needs an explicit DD amendment.
- **Q12.** Chariot, PayPal Giving Fund and bank account-validation networks [K] are incumbents.
- **E3 is driven by its parameters.**
  - The fraud benefit comes entirely from `RegistryCatch 0.95` against `CallbackCatch 0.7`.
  - The cost benefit beyond netting comes from `CheckShareRegistry 0.10` against 0.33.
  - At parity [R], registry and netting are identical: $93,339 and 14.4 uncaught changes.

### 4.8 INN-08 Structured remittance with grant ID (Adopt, L1): SURVIVES

- It is low cost and already parent DD-018.
- **Q9.** Recipient banks often do not show CCD+ or CTX addenda to small nonprofits [K]. E3's `RecipientMinutesWithKey 0.5` assumes delivery. Keep the API retrieval path that INN-08 already names.

### 4.9 INN-09 Daily netting (Test, L1): SWM

**What E3 shows:** a real reduction in payment count, from 100,000 to 61,367 (mechanism: distinct recipient-days).

**Interactions that are not modeled**
- **(a) Dual control and caps.** Netting raises payment size. That crosses CTL-005 dual-control thresholds and `PerRecipientDailyCap` more often, which adds hidden human approvals (Q2).
- **(b) Idempotency keys (E9) on a mutable batch.** If one grant is held or cancelled after the batch forms, the retried payment differs. A per-payment key then either blocks a legitimate payment or fails to deduplicate.
- **(c) Returns.** One return now unwinds several grants from several donors' funds.
- **(d) Recipients.** Each grant still needs its own acknowledgment and attribution.

**Modification:** the batch is formed after all holds clear, at a fixed cut-off. The key is derived from the sorted grant-id set. Netting is optional per recipient.

### 4.10 INN-11 Pre-underwritten asset acceptance (Test, L1): SWM

- **Pointer error.** The validation "E5 complex-asset queue simulation" does not exist: E5 is onboarding. W4 §7 has the same error.
- **Q9.** This domain is all unusual transactions: environmental liability, UBTI, LP capital calls and §4943 (REG-006).
- **Modification:** the indicative acceptance is non-binding. Final acceptance stays with a person for every gift. Class rules are approved by the committee and expire (CTL-047).

### 4.11 INN-14 Zero-ticket servicing (Adopt, L1): SWM; recommend Test

- Its experiment, the "E6 contact model", was not built: E6 is specialist pooling. The register already labels it "assumption-driven".
- **Q11.** Older or vulnerable donors and complex estates need a staffed human channel. The single inbound channel "something is wrong" is an accessibility and complaint risk.
- **Q5.** Grounded answers can still hallucinate.
- **Modification:** keep a staffed, findable human path. Measure the share of status contacts before deciding to adopt.

### 4.12 INN-15 Invisible advisor-embedded DAF (Adopt, L2 → L1): SWM

- **Contradiction.** The register and XW-18 say L2. The same design, D-W7-4, is L1 in the catalog.
- **Why L1.** The premise ("channel-led growth") is marked [I] (inferred) in the register's own evidence column.
- **Q7 and Q12 (lock-in, reversed).** The sponsor becomes dependent on platforms whose owners run competing sponsors (Schwab, Fidelity, Vanguard).
- **Q13.** Proposed REG-034 would make managing advisers donor-advisors. REG-030 and REG-033 also apply.
- **Modification:** keep the sponsor-of-record decision path and a direct donor channel. Treat this as a distribution test, not an "Adopt".

### 4.13 INN-16 Scoped delegation tokens (Adopt, L3 → L2): SURVIVES

- The cited PoC evidence is INV-A6 (`AuthorityInvariantTests.fs` l.67, l.82). It tests agent caps and confirmation only.
- There are no tests of revocation, expiry, advisor scopes or token theft. L3 needs adversarial cases. OAuth is a strong premise, so the item is L2.
- D-W7-3 is "forwarded: E5", which is the onboarding experiment and the wrong pointer.

### 4.14 INN-17 DAF transfer protocol (Test, L1): SWM

- **Q11 and Q13.** It needs adoption by incumbents, which have every incentive to refuse (EV-121). The organization has no standard-setting authority. A transfer remains a discretionary grant by the sending sponsor.
- **Q6.** Transfer-out after account takeover is a cash-out path to a sponsor where the attacker controls advisory privileges. D-W6-3 lists step-up authentication and cooling-off. Keep them mandatory.

### 4.15 INN-18 Always-migrated record (Adopt, L2): SWM

- **E8 is tautological.** The "target system" is the same `Journey.run` (Migration.fs l.68–69). The test asserts the determinism of one function (l.129).
- The baseline is a straw man. D-W8-2 already carries old history as documents, which E8 omits.
- The real failure, semantic mismatch with a *different* vendor schema, is untested.
- L2 rests on EV-037 (AEF kept two years). **Modification:** replay into an independently written target schema before claiming L3.

### 4.16 INN-19 Spend-down horizons (Test, L1): SURVIVES as a field pilot

- **Q10 incentive conflict.** Asset fees fall as grants rise. The register says so.
- A field pilot is the only valid test, and the authors acknowledge this (D-W9-4).

### 4.17 INN-20 Evidence ledger and auto audit package (Adopt, L3 partial): SWM

- Evidence emission is tested in the parent PoC.
- **Q8.** Auditors still test IT general controls and re-perform. "Evidence costs nothing extra" ignores ledger completeness controls.
- D-W10-3 is "forwarded: E2 evidence completeness", but E2 has no such metric.
- **Modification:** add an obligation-to-evidence coverage test that fails when a control emits no evidence.

### 4.18 INN-21 Policy compiler with back-testing (Adopt, L3 partial → L1): SWM

- No back-test, compiler or generated-prose code exists in `models/`. A search for "backtest|back-test" finds only E8.
- CTL-009 and DD-011 are control specifications, not experiments. The decision-table engine belongs to INN-05.
- **Q5/Q8.** Faithful compilation of a mis-specified policy is the failure mode. Counsel review stays the bottleneck.

### 4.19 INN-22 Continuous close (Adopt, L2 → L1): SWM

- **Contradiction with the ladder.** The register's evidence column says "GAP-005 (no data)". A gap cannot support L2.
- **E4.**
  - The whole effect is the assumed age penalty.
  - Continuous mode detects at age 0 by definition (l.427).
  - Transient timing breaks from T+1 settlement, the main cost of real continuous reconciliation, are not modeled.
  - With a missing-feed alarm, breaks inside an outage are treated as detected after one day (l.424). An alarm detects the outage, not the breaks, which stay invisible until the feed returns. That is a modeling error.
- **Modification:** model timing breaks and outage backfill. Keep CTL-048 monthly attestation, as the authors do.

### 4.20 INN-23 Per-donor contribution references (Adopt, L1): SWM

- This works for ACH, wire and virtual accounts.
- DTC securities deliveries carry free-text references that brokers often drop [K]. Determinism for securities needs D-SEC-5 sub-accounts, which have a per-account cost at scale (Q10).
- **Modification:** adopt for cash; test for securities.

### 4.21 INN-24 Upstream KYC attestation reliance (Test, L1): INSUFFICIENT EVIDENCE

- **Q13.** The BSA reliance provisions cover only covered financial institutions. A sponsor is not BSA-covered (REG-038), so there is no legal reliance framework, and liability allocation is contractual.
- No transferable custodian attestation product is evidenced.
- E5 *assumes* the ecosystem option has higher fraud (0.85 detection). It is a table, not a test.

### 4.22 INN-25 Account at first intent (Test, L1): SWM

- **Q13.** The §170(f)(18) acknowledgment (REG-008) and acceptance of the agreement must come before the gift is accepted. The design says so.
- **Q6.** Contributions are irrevocable. Accepting stolen funds from an unverified person leaves the sponsor holding tainted assets.
- **Modification:** cap contributions until identity is verified, and require step-up before the first grant (the authors' "value caps").

### 4.23 INN-26 Donor agents as capped principals (Adopt, L3): SURVIVES (narrow)

- L3 holds only for cap and confirmation enforcement (INV-A6).
- **Q6.** Social engineering of the donor, who confirms above the cap, is not tested.

### 4.24 INN-27 Pipeline liquidity planning (Adopt, L2 → L1): SWM

- The twin evidence ("a 30-day outage in surge exhausts a 2% buffer") supports *having a buffer*. It does not support pipeline *forecasting*, which is not modeled.
- The cited "E6 liquidity" does not exist. D-INV-3, XW-16 and XW-31 repeat the pointer.

### 4.25 INN-28 Shared specialist pool (Test, L1): SWM (reframe)

**E6 contradicts the stated benefit, surge capacity.**
- At equal FTE, the shared pool has 145 sponsor-days over SLA against 144 for separate pools. All sponsors surge in the same December, so pooling cannot absorb the surge.
- The minimum-FTE gain (35 → 33) is mostly granularity. Separate pools must staff whole FTEs per sponsor (`Math.Floor(fte/sponsors)`, l.535).
- [R] With 2 sponsors: 14 vs 14. With 20 sponsors: 160 vs 133. The benefit is *indivisibility for small sponsors*.

**Other questions**
- **Q3, Q13.** Pooled staff are not the sponsor's officers or employees. DD-003 requires that only a sponsor human creates an instruction, and the §4966 fund-manager concept (REG-001) needs counsel.
- **Q8.** Confidentiality and conflicts across tenants.
- E6 also assumes the same throughput across 5 different policies, with no switching cost.

**Modification:** recast as fractional specialist capacity for small sponsors (D-ORG-5), with named sponsor delegation.

### 4.26 INN-30 Digital twin as management system (Adopt, L3 simulated → L1): SWM

- The twin is an L3 artifact. "Managing by the twin" is an L1 practice: the twin has never been back-tested against any real organization.
- **Q5.** A model trusted beyond its validity.
- **Modification:** label every twin output as simulated, as the authors do, and require calibration before staffing decisions.

### 4.27 INN-31 Outcome teams, no departments (Adopt, L1): SWM; recommend Test

- **Q3.** Segregation of duties (CTL-006) and the controller's independence (CTL-048) are commonly carried by reporting lines.
- **Modification:** "no departments" must keep independent controller, CRCO and treasury lines. L1 does not justify "Adopt".

### 4.28 INN-32 Board assurance with expiring parameters (Adopt, L1): SURVIVES

- This is largely parent CTL-047.
- The Q11 risk is information overload. Directors need curated deltas, which the design already approves.

### 4.29 INN-33 Evidence-graded discovery (Test, L1): SWM

- **Q8, Q13.** Neutrality and consumer-protection exposure.
- Fairness monitoring needs church-status and small-recipient coverage. 8.3% of top-50 dollars go to church-status recipients without e-filed 990s.
- **Modification:** disclose ranking criteria, and do not rank by outcome claims.

### 4.30 INN-36 Shared compliance policy packs (Test, L1): SWM

- **Q4.** Correlated error, a monoculture of interpretation.
- **Modification:** each adopter needs independent review by its own counsel, and state-law parameters must be explicit. The authors keep each board responsible, which is necessary but not sufficient.

### 4.31 INN-37 Year-end surge smoothing (Test, L1): INSUFFICIENT EVIDENCE

- **E6 smoothing violates causality.** It moves half of the December excess into November (l.496–497). December recommendations do not exist in November.
- An execution window *defers* work, into January. That changes recipients' receipt timing (Q11) and was not modeled.
- At equal staffing, smoothing *doubled* days over SLA, from 144 to 284.

### 4.32 Forwarded designs (summary; details in the CSV)

**Inherit the verdict of their innovation**

| Designs | Innovation |
|---|---|
| D-W1-3, D-W2-3 | INN-05 |
| D-W1-4 | INN-01/03/34 |
| D-W1-5 | INN-02 |
| D-W2-4 | INN-04 (L2 → L1) |
| D-W2-5, D-W4-6 | INN-28 |
| D-W3-3 | INN-08; the payment gate is L3 in JourneyTests |
| D-W3-4 | INN-07/09/10 (split it: netting SWM, registry insufficient, pull claiming Watch) |
| D-W4-4 | INN-11 |
| D-W5-3, D-W5-4 | INN-14 |
| D-W5-6 | INN-26 |
| D-W6-5 | INN-17 |
| D-W7-3 | INN-16 (L3 → L2) |
| D-W7-4 | INN-15 |
| D-W8-3 | INN-18 |
| D-W9-4 | INN-19 |
| D-W10-3 | INN-20 |
| D-W10-5 | INN-36 |
| D-W11-3 | INN-22 (L2 → L1) |
| D-W11-4 | INN-23 |
| D-W12-4 | INN-25 |
| D-W12-5 | INN-24 |
| D-INV-3 | INN-27 (L2 → L1) |
| D-ORG-3 | INN-30/31 (L3 sim → L1) |
| D-GOV-3 | INN-32 |
| D-PI-3 | INN-33 |

**Own findings**
- **D-W6-3 (L2 → L1).** EV-121 evidences the *problem*: slow, cash-only transfers. It does not evidence the mechanism. E2, E8 and E9 do not test transfers.
- **D-W12-3 (L2 → L1).** "Parent PoC identity gate" tests the gate. It is not evidence that conversational intake raises completion.
- **D-SEC-3 (L2 → L1).** Free-text references on DTC deliveries.
- **D-INST-3 (L2 → L1).** "DD-016 design" is a decision, not evidence.
- **D-CASH-4 (pull debit), SWM.** A consumer ACH debit can be returned as unauthorized for up to 60 days under Nacha rules (REG-044) [K]. Granting from a pulled contribution before that window closes risks a loss. Hold grants or cap amounts until the window passes. The cap file mentions only stolen accounts.
- **D-ORG-5, SWM.** This is the valid version of pooling.
- **D-W7-5 (L0).** INSUFFICIENT EVIDENCE.
- **D-ACQ-4 (L1).** INSUFFICIENT EVIDENCE: E11 does not exist.
- **D-W8-6, D-W10-6, D-INV-4, D-INST-4, D-ACQ-3, D-PI-5, D-W9-3.** These survive at L1 with the modest modifications given in the CSV.

## 5. Experiment audit

| Exp. | What the code does | Assumption-driven or modeling error | Missing adversarial cases | Do the tests assert something? | Status |
|---|---|---|---|---|---|
| **E1** verification | Zipf grants; eligibility-change days; publication lag | Escapes are identical across all automated archs by construction (shared `caughtIrs`). "Ops" counts machine reads, so passport vs per-grant is a pricing artifact. Latencies are hard-coded constants (86,400 / 2 / 0.01 s). The network arm multiplies by a constant 0.513, while evidence says per-joiner reuse is 4–81% depending on order. Ineligibility 0.5% of recipients/yr gives 0.49% of grants ineligible, against the cited 0.082% of dollars revoked (6× high, ranking unchanged) | Poisoned refresh, name collision, stale record after change (promised in W1 §7) | Weak. `diff < auto` and `network < diff` are arithmetic consequences of the definitions | internal-demonstration; network arm **invalid** as built |
| **E2** approval | Seeded defects; rules, AI and human catch probabilities; 8 architectures | Ranking set by `AiRecall` vs `HumanRoutineCatch`. [R] at parity, AI-native 651 vs RulesPlusManual 646. Hours set by `MinutesRoutineReview 6`; [R] at 1 min, 15,306 vs 15,383. Canary detection day and 1-day window set by fiat. PayFirst charges sampling minutes only on defective grants (l.293: `&& isDefect`), a cost bug. PayFirst is a straw man that ignores the passport lookup INN-35 assumes. `ManualReviewAll` "misconfig detected day 105" is meaningless, since there is no rule to break. Errors are independent per grant, with no adaptive adversary | Adaptive fraudster; correlated AI misses; reviewer automation bias (CTL-046 exists but is not modeled) | Partly. "eco escapes = native" and "canary detects day 100" are tautologies; "rules catch revoked ≤15%" is loose | internal-demonstration; best of the set; control-effectiveness claims unsupported |
| **E3** disbursement | Distinct recipient-days for netting; assumed cost and catch parameters | The netting count is mechanistic and fine. Registry fraud and check-share gains are pure parameters ([R] parity removes them). The baseline fraud formula `×S…/S` cancels and is a no-op. Returns-affected is the same 500 in every design, so "netting widens impact" is definitional | Registry compromise blast radius (promised W3 §7); addenda stripped by bank | Trivial | internal-demonstration (netting); registry arm **invalid** as evidence |
| **E4** reconciliation | Daily break counts; age at detection; age penalty | 100% of the saving comes from unsourced `MinutesPerAgeDay`. [R] at 0, both 367 h. Continuous age = 0 by definition. "Poisson" is a rounded uniform (wrong variance). The alarm case treats outage breaks as found in 1 day (error) | Transient timing breaks; false-positive breaks; outage backfill | Tautological (`c.Mean < m.Mean`) | **invalid** as evidence for INN-22 benefits |
| **E5** onboarding | `(1−a)^steps` over a hand-entered table | Output = input. Fraud and completeness are asserted per design | Synthetic identity; attestation fraud | No test exists | **not an experiment** (scenario table) |
| **E6** pooling, smoothing | Fluid queue; uniform noise; synchronized December surge | Pooling gain mostly integer-FTE granularity. Smoothing moves future demand into the past (causality error). No cross-policy switching cost | Correlated surges across sponsors are modeled, which is honest; tenant-confidentiality overhead is not | Pooling ≤ separate is guaranteed by subadditivity; smoothing test passes by construction | pooling: suggestive only for small-sponsor indivisibility; smoothing arm **invalid** |
| **E8** migration | Same log through the same engine twice; balance-forward with 2-year cut-off | The equality assertion is determinism of one function. The straw-man baseline omits "history as documents" | Heterogeneous target schema; event-version drift | Tautological | **invalid** as evidence for INN-18 beyond specification |
| **E9** crash recovery | Hand-coded table of executions per (design, crash) | The result is the table. "Bank deduplicates on key" is load-bearing and assumed; ACH networks have no end-to-end idempotency key, so dedupe depends on the originating bank's API | Key expiry window; netted batch recomposition (INN-09); partial bank acceptance | Reads the table back | valid as a **specification** of required semantics, not a test |
| **E10** AI triage | Irwin–Hall scores; threshold auto-close vs flag-only | Flag-only escapes hard-coded to 0 (l.632), inconsistent with E2's 0.95 human catch. [R] that alone implies about 48 escapes of 967. Dossier saving 45 → 30 min assumed | Automation bias from the dossier itself; adversarial evasion | "Flag-only escapes none" is tautological; "auto-close escapes some" is true for any overlapping classifier | supports DD-005 directionally; **flag-only arm invalid** |

The overlap harvest (E7) is the program's one piece of external evidence. Its method problems are in §4.2. The script is reproducible and its documentation is honest about coverage.

## 6. Contradictions found

1. **INN-15** is L2 in the register and in XW-18, but D-W7-4 is L1 in the catalog.
2. **INN-02 and XW-07** still read "L1 (L2 if E7)" after E7 was run. Meanwhile E1 already consumes E7's 51.3% as a parameter (`Experiments.fs` l.88). Also, the evidence document says reuse depends on join order, while E1 uses a constant.
3. **Experiments referenced but absent or mislabeled:**
   - INN-11, W4 and XW-14 point to "E5 complex-asset queue"; E5 is onboarding.
   - INN-14, W5 and XW-23 point to an "E6 contact model".
   - INN-27, D-INV-3, XW-16 and XW-31 point to "E6 liquidity".
   - D-W7-3 points to "E5".
   - INN-21 and XW-24 point to an "E2 back-test".
   - D-W10-3 points to "E2 evidence completeness".
   - E11, cited by about 10 items (XW-05, 07, 08, 10, 11, 18, 25, 28; D-ACQ-4, D-INV-4; W1–W5 cost rows), has no code or results.
   - W1 §7 promised E1 adversarial cases; W2 §7 promised "stale-determination escapes"; W3 §7 promised "blast radius of one hijack". None was built.
4. **H-08 against E2:** see §3, objection 3.
5. **INN-22 at L2 with "GAP-005 (no data)"** as its evidence. Similar ladder misuse: D-INST-3 "L2 (DD-016 design)", D-W12-3 "L2 (parent PoC identity gate)", D-INV-3 "L2 (twin)".
6. **INN-21 "L3 (partial)"** with no back-test or compiler code.
7. **INN-16 "L3"** with only cap tests.
8. **DD-008** ("never build payment rails") against AO-07, INN-07 and INN-10 (a two-sided, multi-sponsor payee registry and recipient-pull claiming). CTL-004 and CTL-006 assume payee data is created inside the sponsor.
9. **DD-003, REG-001** against INN-28 and XW-10 (pooled non-employee deciders).
10. **REG-002** against INN-04's "ER pre-qualification" reuse (ER is per grant).
11. **INN-34's "less screening work"** against INN-03's universe of all Pub 78 organizations (§4.3).
12. **The human-reviewer model differs across experiments:** 0.95 catch in E2, perfect in E10.
13. **INN-37's narrative** ("pre-clear known recipients in November") against E6's implementation (moves December arrivals into November).
14. **Problem evidence presented as mechanism evidence.** These are L1/L0 ideas shown as further along: D-W6-3 (EV-121), INN-15 ([I]), INN-27 (a buffer, not a forecast). No document claims L4, and the methodology's caveats ("L3 = works in a model") are stated consistently, which is to the authors' credit.

## 7. Maturity downgrades

**Innovations**

| Item | Claimed | Justified | Reason |
|---|---|---|---|
| INN-04 | L2 | L1 | Exception-recipient recurrence not evidenced; ER is per grant |
| INN-06 | L1 | L0 | Contradicted by E2 |
| INN-15 | L2 | L1 | [I] premise; catalog says L1 |
| INN-16 | L3 | L2 | Revocation, expiry and theft untested |
| INN-21 | L3 partial | L1 | No compiler or back-test code |
| INN-22 | L2 | L1 | GAP-005 is "no data"; E4 is assumption-driven |
| INN-27 | L2 | L1 | Forecasting not modeled; E6 liquidity absent |
| INN-30 | L3 (sim) | L1 | As a management practice, uncalibrated |

**Designs**

| Item | Claimed | Justified |
|---|---|---|
| D-W2-4 | L2 | L1 |
| D-W6-3 | L2 | L1 |
| D-W7-3 | L3 | L2 |
| D-W11-3 | L2 | L1 |
| D-W12-3 | L2 | L1 |
| D-SEC-3 | L2 | L1 |
| D-INV-3 | L2 | L1 |
| D-INST-3 | L2 | L1 |
| D-ORG-3 | L3 (sim) | L1 |

**Recommendation changes:** INN-14 and INN-31 move from Adopt to Test.

## 8. What would change my mind

| Claim | Evidence that would overturn my objection |
|---|---|
| Network value (INN-02) | Partner data showing that bank-verification and determination minutes per recipient are material and duplicated across sponsors, plus a national sponsor's willingness to contribute. Or a random-order reuse curve weighted by verification *cost* rather than by pair count |
| AI-native escapes fewer defects (E2) | Measured AI recall on seeded related-party and benefit cases (CTL-046 data) that exceeds measured reviewer recall on routine grants. Today both are [A] |
| Continuous close is cheaper (INN-22) | Measured relation between break age and investigation minutes (GAP-005), and a timing-break rate under T+1 feeds |
| Sampling can replace review (INN-06) | A model run in which sampling-only escapes ≤ review-all escapes under the authors' own defect rates. Under the current parameters that requires the sampling rate to rise far above 2%, which erases the cost case |
| Pooling absorbs surges (INN-28) | Evidence that sponsors' peaks are not synchronized (they are all December, by the authors' own assumption) |
| Replay migration (INN-18) | Replay into an independently written schema with zero loss on the invariants |
| Reusable determinations (INN-04) | A measured reuse factor on exception history, plus counsel's view on ED reuse under Notice 2006-109 |
| Delegation tokens at L3 (INN-16) | Tests for revocation, expiry, scope escalation and a stolen-token replay |
