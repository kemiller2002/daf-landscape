# 04. Challenging human intervention

All 57 human activities answer the ten questions in [`activities.csv`](data/inputs/activities.csv). The rendered register with hours at 10 customers is [`data/outputs/activity-register.md`](data/outputs/activity-register.md), and hours at 1, 10 and 100 customers are in [`workload.csv`](data/outputs/workload.csv).

Two gates enforce the rules:
- **V4:** a decision reserved to the sponsor is never assigned to Echelon Foundry. This follows CNV-GOV-004 (vendor staff may not hold A3+ authority) and UNB-CDD-CMF-002.
- **V5:** a required human control never has a zero human share.

## The five areas the mission named
| Activity | Why it exists | Law / contract | Prevent? | Software? | AI? | Who decides | Frequency × time | When it forces staffing |
|---|---|---|---|---|---|---|---|---|
| **Routine grant approval** (ACT-GRT-03) | Exists only until the sponsor board adopts a deterministic grant policy (CNV-GRT-001) | No / partly | **Yes**: policy-conforming grants execute on policy | Yes | Yes (sampling) | Sponsor | Base: 10% post-hoc sampling at 1 min per grant. If every grant is approved individually: 1–2 min per grant | Never Echelon Foundry. At 10 mixed sponsors (about 83k grants), individual approval would add about 1,400 sponsor hours a year |
| **Grant exceptions** (ACT-GRT-01/02) | Nonstandard grantee, purpose, benefit or conflict flags | Exception decisions are reserved (IRC 4966(d)(2)) | Partly (pre-validated rules) | Partly | Yes (dossier) | Preparation: sponsor or Echelon Foundry. **Decision: sponsor** | 5–18% of grants (base 9%) × 15 min preparation + 10 min decision | Under limited operations and full service, exception preparation is the single largest workload: about 2,100 h at 10 sponsors, which forces the first operations hire |
| **Charity re-vetting** (ACT-CHV-01..04) | Eligibility evidence must stay fresh (45-day IRS and 24-hour OFAC staleness limits; 180-day deep-review ceiling) | Partly | **Mostly**: change-driven monitoring. Only 405 of 236,750 monthly BMF changes are eligibility-relevant | Yes: revocation applies a hold deterministically | Yes | Ambiguous cases: **sponsor** | Exceptions 1–5% of grants; deep-review renewals with 0.5–5% needing a person | With change-driven renewal: about 550 h of eligibility exceptions plus under 60 h of monitoring and renewal at 10 sponsors. **With manual 180-day reviews:** about 2,400 h at 10 sponsors, about $210k a year if Echelon Foundry performs them ([06](06-institutional-growth-scenarios.md) §deep review) |
| **Reconciliation** (ACT-REC-01..03) | Daily automated matching leaves breaks; monthly close; independent review | Review and controller sign-off are contract-required (CNV-GOV-003, CNV-FIN-004) | Partly (single ledger) | Matching: yes | Yes (break explanation) | **Sign-off: sponsor controller**. Investigation and preparation: sponsor or Echelon Foundry | Breaks 1–5% of transactions × 10 min; close 4–25 h per sponsor-month; sign-off 1 h per month | Close preparation is per sponsor and adds about 120 h a year per full-service customer |
| **Contribution attribution** (ACT-CTR-01) | Pooled or unidentified receipts | Partly | **Yes**: notification-first intents, fund references | Partly | Yes | No reserved authority | 2–10% of contributions × 20 min | About 355 h at 10 sponsors (limited operations and full service) |
| **Customer support** (ACT-SUP-01/02, ACT-IMP-03) | Sponsor-staff questions (all models); donor contacts (full service only); go-live hypercare | Contract-typical response times | Partly (self-service, proactive status) | — | Yes (grounded answers) | — | Sponsor staff: 12–80 tickets per sponsor a year × 30 min. Donors (full service): 0.2–1.5 contacts per account a year, 30–90% needing a person, × 10 min | Donor support makes full service support-heavy: about 860 h at 10 customers |

## What cannot be automated (by party)
**Sponsor, in every model:**
- grant-exception decisions;
- ambiguous eligibility determinations;
- payment release under dual control;
- monthly reconciliation sign-off;
- OFAC true-match blocking and reporting;
- successor approval;
- complex-gift acceptance;
- board policy adoption and oversight (2.7–7 min per account a year);
- the sponsor's own audit;
- sponsor-side onboarding and migration validation.

**Echelon Foundry:**
- Distinct-person controls: two non-author approvers, two-person break-glass, an incident commander with a backup.
- External audits: SOC 2, and SOC 1 where Echelon Foundry performs controls.
- Pen tests.
- Contracting and counsel.
- Incident response.
- Maintenance of a regulated platform: tax-year and Nacha rule changes, upgrades.
- Under limited operations and full service, a human check on AI-prepared exception dossiers. The dossiers can be prepared by software and AI, but a person must check them before an accountable sponsor official decides.

## Financial controls kept
- **Payment release** stays at two or three distinct sponsor persons (CNV-GOV-003). It is never automated away, and never moved to Echelon Foundry.
- **Reconciliation** sits outside the payment chain, with independent review at least monthly.
- **Control-module change approval** needs two non-authors. No exception is modelled; AI may shorten review but cannot approve (UNB-AI-STD-003).
- **The 180-day deep-review ceiling** is retained, as owner direction OD-CDD-02 requires; change-driven renewal operates within it.
