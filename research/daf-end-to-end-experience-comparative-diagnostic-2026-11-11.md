# DAF end-to-end experience: comparative diagnostic and field-research design
**Date:** 2026-11-11
**Status:** Research synthesis and falsifiable test design; no new user interviews, production testing or forum posts conducted.

## Four parallel investigations

### A. Vanguard donor journey, benchmarked against Fidelity, DAFgiving360 and NPT
| Stage | Vanguard hypothesis | Benchmark question | Proof required |
|---|---|---|---|
| Open | Minimums and onboarding determine accessibility | What can a new donor do in one session? | Current program terms and public walkthrough |
| Fund | Vanguard brokerage integration can simplify specific-lot transfer | Does in-kind transfer from external brokers work equally well? | Current instructions, dated user experiences |
| Invest | Low-cost pools and affiliated services may matter more than interface | What is the full sponsor + fund + advisory fee? | Dated fee schedules and fund disclosures |
| Recommend | Charity lookup, grant minimums and address editing shape usability | Can donor correct charity location or purpose? | Current documentation or authorized test |
| Approve | Sponsor has legal discretion and compliance obligations | What status visibility is available during review? | Public help, documented user experience |
| Deliver | Historical donor complaints concerned check tracking and reissues | Are EFT/check, delivery and deposit statuses visible today? | Current documentation, 2025–26 reports |
| Confirm | Donor's completed action may differ from recipient's receipt | How is settlement/acknowledgement confirmed? | Recipient-side evidence |
| Resolve | Exception handling may be more valuable than initial UI | Who handles stale checks, returns and incorrect recipients? | Case studies with dates and resolutions |

**Do not extrapolate 2024 Vanguard check-tracking complaints to current 2026 functionality.** The older public evidence establishes a question, not a current defect.

### B. Nonprofit grant reconciliation
Distinguish at least five entities: legal donor (sponsoring charity), donor adviser (potentially anonymous), named DAF account/fund, recipient nonprofit, and transaction/payment. A nonprofit may require legal accounting credit to sponsor while maintaining relationship/soft credit to donor adviser. Model notice, grant approval, payment issue, bank settlement, restricted-purpose classification, receipt/acknowledgement, reconciliation and exceptions as separate events.

**EDF failure tests:** Missing unique payment ID, mismatched donor names, unstructured memo fields, mailed check versus ACH timing, delayed grant notification, returned checks, charity address changes, duplicate donor CRM records, wrong restriction coding, anonymous donor conflicts, lack of resolution owner. Separate system failures from policy decisions and local nonprofit CRM practices.

### C. Provider switching and multi-provider behavior
**Hypotheses:** Donors may maintain Vanguard for appreciated-share contributions and another sponsor for flexible grantmaking. Donor-adviser attachment may be to broker, financial adviser, legal sponsor, charity or interface rather than one platform. Migration cost can involve transfer policies, investments, successor designations, grant history and adviser permissions.

**Tests:** Compare sponsor-to-sponsor transfer policies, minimums, in-kind transfers, closure requirements, investment liquidation, data export, grant-history portability, grant recommendation processing and actual switching anecdotes. Identify multi-homing versus complete migration; never infer retention rates from individual forum stories.

### D. Public feedback outreach
Separate questions for donors, nonprofit finance/development, advisers and DAF operations staff. Seek *one dated event* with stage, expectation, actual outcome, resolution and positive or negative result. Avoid collecting identities, exact balances, account details, beneficiary information or confidential contract data. Check each community's posting rules; moderator approval where appropriate. No outreach conducted.

## Structured evidence capture
`id,source_url,publication_date,access_date,provider,product_version,role,journey_stage,event_type,claim,positive_negative_neutral,resolution,corroboration,alternative_explanation,confidence,open_test`

Evidence grades: **E1** contemporaneous official policy/primary record; **E2** reproducible authorized product observation; **E3** dated first-person report; **E4** secondhand report; **E5** hypothesis. Do not numerically average evidence grades into satisfaction or market-share scores.

## Decision-focused outputs
1. Cross-provider lifecycle feature matrix with missing cells marked unknown.
2. Root-cause taxonomy: sponsor policy, application UX, administrative workflow, custody/investment, payment rail, nonprofit CRM and user misunderstanding.
3. Evidence-coded customer-journey friction map by donor and recipient roles.
4. Switching-cost model separating money, time, legal discretion and data portability.
5. Opportunity prioritization by donor value, nonprofit value, feasibility, legal constraints and uncertainty, not vendor favoritism.

## Preliminary conclusions with limits
- Public reports indicate Vanguard donor funding convenience and separate historical grant-delivery friction; not proof of current comparative superiority/inferiority.
- Recipient attribution/reconciliation is a distinct problem even when donor UX appears successful.
- Multi-provider accounts challenge the assumption that one sponsor controls every donor interaction.
- Negative posts are selection-biased; research must actively seek positive, resolved and recent experiences.

## Public source leads
- Vanguard grant-tracking thread: https://www.reddit.com/r/fatFIRE/comments/1938ysc
- Bogleheads comparison: https://www.bogleheads.org/forum/viewtopic.php?t=410095
- Later Bogleheads comparison: https://www.bogleheads.org/forum/viewtopic.php?t=462376
- Nonprofit CRM attribution: https://www.reddit.com/r/nonprofit/comments/1rr7hqk/how_do_you_track_your_daf_gifts_in_your_crm/
- Vanguard fees and minimums: https://www.vanguardcharitable.org/giving-with-vc/fees-and-minimums
- Fidelity Charitable: https://www.fidelitycharitable.org/
- DAFgiving360: https://www.dafgiving360.org/
- NPT: https://www.nptrust.org/

## Next evidence-gathering tasks
- Verify current 2026 official grant status and payment tracking documentation for all four sponsors.
- Reconcile each sponsor's fee structure at $25k, $100k, $500k, $1m and $5m, including fund expenses.
- Capture recipient remittance examples from public documentation and anonymized voluntary experiences.
- Review current subreddit and Bogleheads.org posting rules before posting; no posts are authorized or submitted by this research.
- Interview multiple roles and record disconfirming cases, then rerun Clarity/EDF conclusions.
