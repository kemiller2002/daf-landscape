# Classification and competitive-matrix framework

## Why roles must be separated

A DAF program can present one user experience while several entities perform legally and operationally distinct jobs. The sponsoring public charity owns and controls contributed assets. A for-profit company may provide the portal and operations. A broker or bank may custody cash and investments. A separate service may validate charities, initiate grants, or deliver payments.

Classify the legal and operating roles before comparing brands.

## Entity roles

| Role | Definition | Evidence to seek |
| --- | --- | --- |
| Sponsoring organization | Eligible charitable entity that maintains DAFs, owns/controls contributed assets, approves grants, and bears sponsor-level compliance duties | IRS record, governing documents, program policy, audited statements |
| Program administrator | Performs contribution, grant, recordkeeping, tax-receipt, service, accounting, reporting, or compliance work for a sponsor | Contract/service description, sponsor disclosure, implementation evidence |
| Sponsor operating platform | System of record or workflow platform for fund setup, ledger/subaccounting, investments, grants, statements, and staff controls | Technical/product documentation, demo, architecture and integration evidence |
| Donor/advisor experience | Portal or app for opening accounts, viewing balances, recommending allocations/grants, and retrieving documents | Product documentation and hands-on test |
| Custody/investment infrastructure | Holds cash/securities, supplies investment products or separately managed accounts, executes trades, and returns position/transaction data | Sponsor policy, account documents, custodian disclosure |
| Charity-data/compliance infrastructure | Supplies exempt-status, sanctions, identity, risk, equivalency, expenditure-responsibility, or fraud checks | Data-provider contract, technical docs, control narrative |
| Grant initiation/connectivity | Embeds a DAF option in a nonprofit or fundraising flow and transmits the donor's recommendation to a provider | API docs, flow-of-funds description, provider integration evidence |
| Disbursement/reconciliation | Moves approved grant funds/remittance data and helps a recipient match the payment to donor intent | Banking/payment docs, remittance schema, recipient workflow |
| Nonprofit fundraising layer | Helps nonprofits solicit, attribute, acknowledge, and analyze DAF gifts | Product docs, CRM/fundraising integrations, customer test |

An entity can hold multiple roles. Record each role and its evidence rather than forcing one category.

## Sponsor archetypes

- **Financial-services linked:** separate public charity with important service, custody, brand, or distribution relationships to a financial institution.
- **Independent national:** national sponsor not defined by a single place or cause; may support advisors and complex assets.
- **Community foundation:** place-based public charity offering DAFs among broader community philanthropy services.
- **Mission/single-issue:** sponsor oriented around a cause, institution, faith, investing approach, or donor philosophy.
- **Embedded/private-label sponsor:** sponsor makes its legal and operating infrastructure available under a partner's brand.

These are research labels, not legal classifications. A sponsor may fit more than one.

## Competitive matrix fields

The matrix compares support for:

1. a legal sponsor supplied directly or through a disclosed partner;
2. private/white-label program delivery;
3. outsourced administration;
4. donor/advisor portal;
5. fund accounting or subaccounting;
6. grant workflow and due diligence;
7. contribution processing;
8. complex-asset support;
9. custom or advisor-managed investments;
10. nonprofit checkout or grant initiation;
11. disbursement and reconciliation; and
12. documented APIs or integrations.

### Allowed values

- `yes`: the cited source directly supports the capability.
- `no`: an authoritative source explicitly establishes absence or exclusion.
- `unknown`: not established by reviewed evidence.
- `not_applicable`: outside the offering's identified layer.

`Yes` does not mean the feature was independently tested, performs well, is included in every tier, or is currently available to every customer. Those require demo, contract, implementation, and customer evidence.

## Comparison dimensions for later scoring

Do not score vendors until a common evidence pack exists. Candidate dimensions are:

- legal/operating model clarity;
- workflow coverage and configurability;
- ledger, audit, reconciliation, and control design;
- asset, investment, and custody flexibility;
- grant eligibility and exception handling;
- payment speed, remittance quality, and failed-payment handling;
- data model, APIs, exports, and integration ownership;
- donor, advisor, staff, and nonprofit experience;
- security, availability, business continuity, and assurance reports;
- implementation effort, service model, pricing, and contractual risk; and
- customer evidence by sponsor type and scale.

Each future score should expose its evidence, date, weighting, and unknowns. No overall ranking should be produced from vendor marketing alone.
