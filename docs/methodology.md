# Research methodology

## Unit of analysis

The default unit is a legal entity, not a brand or product. A product or brand receives its own record only when that is necessary to explain the market. Relationships among a public-charity sponsor, for-profit administrator, custodian, and payment vendor are recorded rather than collapsed into a single “platform.”

## Evidence hierarchy

| Grade | Evidence | Typical use |
| --- | --- | --- |
| A | Statute, regulator guidance, IRS data, court or government record | Legal definitions, status, regulatory requirements |
| B | Audited financials, Form 990, governing policy, program circular, contract, technical documentation | Legal entity facts, operating rules, specific capabilities |
| C | Dated first-party announcement or current official product page | Vendor-reported products, relationships, positioning |
| D | Reputable independent research or reporting with transparent method | Corroboration, market context, customer perspective |
| E | Directory, unsourced list, social post, anecdote | Discovery only; not sufficient for a verified field |

The initial baseline uses grades A-C. Later work should use grade D to test vendor-reported capabilities and collect customer outcomes.

## Confidence

- **High:** a direct, specific grade A or B source, or two consistent primary sources, supports the exact claim and the entity/date match is clear.
- **Medium:** a current grade C source or a single primary source supports the claim, but independent corroboration, a filing check, or product testing remains.
- **Low:** ambiguous, stale, indirect, or conflicting. Low-confidence statements remain hypotheses or notes and are not presented as verified facts.

Confidence is claim-specific. A sponsor's legal status can be high confidence while a feature claim from the same organization is medium confidence.

## Claim states

| State | Meaning |
| --- | --- |
| Verified fact | Directly supported by cited evidence at the stated confidence |
| Vendor-reported capability | Verified as a current vendor representation; operation and performance not independently tested |
| Hypothesis | Testable proposition with evidence still required |
| Unknown | No conclusion; research incomplete |
| Superseded | Once correct, but replaced by a rebrand, acquisition, policy, or product change |

## Fact-check procedure

1. Confirm the current legal/brand name and source date.
2. Decompose the proposed statement into atomic claims.
3. Find the strongest available primary source for each claim.
4. Check whether the source speaks about the legal entity, an affiliate, a partner, or only a product brand.
5. Preserve material qualifiers such as “through a partner,” “if enabled,” or “vendor-reported.”
6. Search for a contradictory current source.
7. Assign evidence grade, confidence, and review date.
8. Enter the claim only after its source ID exists.

## Freshness

Suggested maximum review intervals:

| Claim type | Re-check interval |
| --- | --- |
| Law, regulation, tax guidance | On rulemaking/change and at least annually |
| Legal status, ownership, partnerships, product availability | 90 days |
| Pricing, minimums, fees, limits | 30 days |
| Product capabilities and integrations | 90 days |
| Historical event with a fixed date | No routine expiry; verify source availability annually |
| Scale metrics and market share | At every new reporting period |

## Quantitative claims

Do not compare figures until all rows share:

- the same fiscal/calendar period;
- a defined unit and denominator;
- consistent inclusion/exclusion rules;
- the same treatment of affiliates and white-label programs; and
- a source that distinguishes assets, contributions, grants, accounts, donors, and recipient organizations.

Vendor statements such as “largest,” “leading,” or “powers X%” are excluded from normalized conclusions until the denominator and independent support are known.

## Conflicts and corrections

When sources conflict, keep both in the register, state the conflict in notes, lower confidence, and avoid choosing the more convenient number. Corrections should update the affected row and explain the change in the commit or pull request. Do not reuse a source ID for a different document.

## Known baseline limitations

- Sponsor legal status has primarily been checked against official policy, legal, or audited materials; a systematic IRS TEOS pass is still open.
- The IRS 2026-2027 Priority Guidance Plan lists a guidance project under sections 4966 and 6033. The baseline does not treat the 2023 proposed section 4966 regulations as final.
- Product capabilities are first-party representations, not hands-on validation.
- Coverage is purposive rather than exhaustive.
- No normalized pricing, customer count, asset, revenue, or market-share comparison is included.
- Private contracts, implementation quality, and downstream infrastructure dependencies remain largely unobserved.
