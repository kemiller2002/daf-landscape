# W4: Complex noncash contribution acceptance and liquidation

This covers private company stock, real estate, LP and LLC interests, restricted public stock, crypto and other noncash assets.

**Outcomes:**
- BO-04: accept or decline on policy.
- BO-05: value and liquidate prudently.
- BO-07: Form 8283 donee acknowledgment and Form 8282 reporting.
- BO-17: excess business holdings avoided (§4943(e)).

**Evidence:**
- The work is specialist and frequently outsourced to non-cash processors ([`b40n14-03-b38c-03-noncash-vendors-dpn.md`](../../../mission-2026-11-14/b40n14-03-b38c-03-noncash-vendors-dpn.md); [`direction-noncash-gift-infrastructure.md`](../../../mission-2026-11-14/direction-noncash-gift-infrastructure.md)).
- In the parent twin, one specialist is a concentration risk: complex gifts ×2 → 336 days over SLA (simulated).
- **No public volume or time data exists.**

## 1. First principles

| Element | Necessary content |
|---|---|
| **Information** | What the asset is; title and transferability; liabilities (environmental, debt, capital calls, UBTI); valuation basis (qualified appraisal obtained by the donor above $5,000); liquidity path; relationship of the donor to the issuer (excess business holdings, prohibited benefit on sale) |
| **Authority** | A named specialist or gift-acceptance committee accepts or declines; an officer signs Form 8283 Part V; Form 8282 is filed on disposition within 3 years (regulatory map) |
| **Resources** | Specialists; outside appraisers (donor-paid); liquidation counterparties; legal documents |
| **Actions** | Screen; diligence; accept or decline; take title; value for books; liquidate or hold; file 8282 if applicable |

**Irreducible:** a fiduciary acceptance judgment for genuinely novel assets.
**Reducible:** repeated diligence on recurring asset *classes*, document loops, and the specialist's role in routine liquidations.

## 2. Inversion findings

| Prompt | Finding |
|---|---|
| Eliminate? | Not for novel assets. For recurring classes, *bespoke* review can be replaced by class underwriting rules |
| Begin before the request? | Yes. Donors and advisors can get a binding-in-principle class answer before the transfer process starts, using pre-underwritten term sheets |
| External partner? | Yes. Non-cash processors already exist; liquidation partners can pre-commit |
| No form? | Structured gift packets from advisors and attorneys can replace PDFs |

## 3. Designs

| # | Design | Mechanism | Who decides | When | Authoritative data | Human roles | Controls | Cost drivers | Experience | Maturity | INN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | **Conventional baseline** | Donor or advisor calls; specialist gathers documents by email; legal review; committee for large gifts; broker or buyer found per asset | Specialist / committee | After donor approaches | Case file (PDFs) | Specialist end to end | Committee approval; 8283 signature | Specialist hours per gift; outside counsel | Weeks; many document loops | Observed (via non-cash vendor research) | — |
| D2 | **Automation-first** | Intake portal, checklist, e-signature, document reminders | Specialist | Same | Portal case | Specialist | Same | Somewhat lower | Fewer emails | L1 | — |
| D3 | **AI-native (parent)** | Document extraction agent builds a dossier (title, liabilities, valuation, relationships); specialist decides; deterministic 8283/8282 tracking | Specialist (H) | Same | Dossier plus decision record | Specialist | Flag-only AI; 8282 deadline monitor | Specialist hours reduced [A] | Faster; status visible | L1 | — |
| D4 | **Radical: pre-underwritten class term sheets** | The unit of work becomes the asset *class*. For each recurring class (restricted public stock with a 144 path; LP interests on known secondary platforms; residential real estate meeting environmental screens; listed crypto via an approved liquidity provider), an underwriting rule set issues an instant indicative acceptance with a standard document packet and a pre-arranged liquidation route. The specialist handles only rule exceptions and the final acceptance above a threshold | Rule for indicative class acceptance; specialist for final acceptance above threshold and exceptions | Before the transfer starts | Class rule set (versioned, committee-approved) plus case facts | Specialist designs class rules and handles exceptions | Committee-approved rules; seeded-error sampling; 4943(e) holdings check by rule | Rule maintenance; specialist exceptions | Advisor gets an answer in minutes for standard classes | L1 | INN-11, INN-13 |
| D5 | **Externalized / ecosystem: partner processor plus liquidity partners** | Accepted-class gifts are processed by a non-cash processor, with pre-committed liquidity partners under standing agreements; the sponsor keeps accept/decline authority and signs filings | Sponsor specialist (decision); partner (execution) | Same | Sponsor decision record; partner execution records | Sponsor specialist; partner staff | Vendor oversight; conflict-of-interest checks on liquidity partners | Partner fees (often % of asset) | Depends on partner; broad asset coverage | L1 | INN-12, INN-28 |
| D6 | **Shared specialist pool across sponsors (extra)** | Pooled specialists serve many sponsors under each sponsor's delegation, smoothing lumpy demand | Each sponsor's delegate | Same | Each sponsor's records | Pooled specialists | Tenant isolation | Utilization | Faster in peaks | L1 | INN-28 |

## 4. Constraint ledger

| Constraint | Dies | Modified | Survives |
|---|---|---|---|
| **Legal** (8283 Part V signature; 8282; 4943(e); quid-pro-quo and prohibited benefit on sale back to related parties) | "Rules accept and sign everything" | D4: rules give *indicative* acceptance only; final acceptance and signatures stay human above threshold; related-party buyers blocked by rule plus person | D2–D6 |
| **Fiduciary** | Liquidation to conflicted partners without price checks | D5: price discovery and committee-approved partner list | D4, D5 modified |
| **Accounting** | — | Book value from appraisal or sale; restricted holdings tracked | All |
| **Privacy / security** | — | Gift documents contain sensitive financial data; access-controlled | All |
| **Economic** | D1 for small complex gifts (cost > value) | Minimum-size thresholds by class | D3–D6 |
| **Operational** | Single specialist (twin concentration) | D5/D6 pooling, or a partner below about 50k accounts (parent twin finding) | D4–D6 |
| **Human acceptance** | — | Advisors and attorneys must use packets (D4) | D4 partial |

## 5. Analogies

- T3: insurance underwriting.
- T4: shared services and reinsurance.
- T9: structured document exchange.
- T15: marketplaces for liquidity.

## 6. Creative competition

| Perspective | Position |
|---|---|
| **Inventor** | Publish the class term sheets openly, so advisors self-qualify before calling: a "rate card" for complex gifts |
| **Enterprise architect** | D4 needs an `AssetClassPolicy` entity and a case state machine (`ComplexAssetCase`, noted by the workflows fork); 8282 deadlines are calendar events |
| **Economist** | The value is concentrated in a few large gifts; specialist cost is per gift. Class rules pay off only if classes truly recur, and volume data is absent |
| **Regulatory specialist** | Excess business holdings and liabilities are where acceptance errors become expensive; class rules must encode the §4943(e) test and environmental screens, with human final say above thresholds |
| **Adversarial reviewer** | The "standard class" label invites adverse selection: donors with problem assets will present them as standard. Pre-committed liquidity partners may underpay. D4 moves work into rule maintenance |
| **Customer advocate** | Advisors value speed and certainty most; a quick "no" is better than a slow one |
| **Commercial strategist** | Non-cash processors already sell D5. Differentiation lies in D4's speed plus decision evidence, sold to sponsors without specialists (Model C) |

**Disagreements:** *Adversarial vs Inventor* on adverse selection with public rate cards. Proposed mitigation: indicative answers are conditional on diligence outcomes. Unresolved without data.

**Unresolved:** asset-class recurrence; specialist hours; partner pricing.

## 7. Forwarded to experiments

| Candidate | Experiment | Metric |
|---|---|---|
| D3 vs D4 vs D6 | **E5** complex-asset queue simulation (class mix, specialist hours [A], pooled vs single specialist) | Time to decision; days over SLA; specialist hours |
| Cost | **E11** | |
