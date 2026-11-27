# REV2 - Chief financial officer

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV2. Perspective: CFO asked to sign off the capital figures the owner will see, and to say whether the cash numbers would survive an audit committee and a bank's third-party-risk review of a one-founder vendor. Written independently of the other REV2 perspectives. Challenge IDs P3-CHL-REV2001..REV2010 in [adversarial-challenges.csv](../../fragments/REV2/adversarial-challenges.csv).

Method. I read reports [02](../../../02-existing-unbound-economics.md), [03](../../../03-capital-requirements-reconstruction.md), [14](../../../14-commercial-sequencing.md), [16](../../../16-capital-efficient-market-entry.md), [18](../../../18-economic-model-methodology.md) and [19](../../../19-sensitivity-and-stress-analysis.md), the model inputs and the F# engine (`model/src/CompetitiveAdvantageCreation/`). I rebuilt the model in a scratch copy, confirmed `run` reproduces `data/model-outputs/` byte for byte, then re-ran it with single changes. No package file was edited. Every re-run number below is base case, founder-funded, unless stated.

What I checked and found sound: the engine keeps cash and fully loaded separate and fully loaded = cash + non-cash by construction (`Cashflow.fs`); working capital is a receivable produced by arrears billing rather than a lump; channel revenue is netted before recognition; the shared-infrastructure allocation conserves totals; the event "by party" table sums to the system cost ($67 + $30 + $3 + $3 + $15 = $118). The Phase II port reproduces ER-7. The package is also unusually candid about what is assumption. My objections are about what the owner will read as "the number".

## Bottom line

The headline "about $1.0-1.24M cash from a completed Unbound, payback month 62, passes the kill rule" is not a number I would sign. Two of its three supports are model artefacts (a fractional-customer pilot and a knife-edge named-partner test), the contingency in the cash engine does not cover the largest line, and the run stops costing money the instant the kill rule fires. Correcting the artefacts does not change the base cash peak much; it changes the *governance* conclusion: A3 is paused by its own kill rule in the base case.

## 1. The kill-rule pilot is passed by a quarter of a customer (P3-CHL-REV2001, high, model error)

`Cashflow.fs:114` signs `customers_per_year / 12` of a customer each month, and `Sequences.fs:257` treats the first month with *any* go-live as the "referenceable live pilot". In A3 base the first 0.25 of a customer goes live in month 22, inside the 24-month test. A referenceable pilot is one sponsor live on the platform. Requiring a cumulative go-live of one whole customer (one-line change in a copy of `Sequences.fs:257`):

| Sequence (base) | As published | One whole live customer required |
|---|---|---|
| A3 | passes; peak $1.24M | **paused at 24; $846k at risk** |
| B | passes (an $8k/yr API customer); burns $5.78M | **paused at 24; $1.24M at risk** |

All A3 kill-sensitivity variants with the clock at month 0 or derived also flip to "paused". P3-CLM-MOD006 ("A3 passes") and report 14 section 6 ("A3 passes under every cost-center definition tested") do not hold once the pilot means a customer. Proposed change: count a pilot only when cumulative go-live >= 1 *Unbound sponsor* (dedicated E2 stream), regenerate 14/16/19 and the claim.

## 2. "Passes" in the base case is a boundary tie (P3-CHL-REV2002, high, factual presentation / model)

`Sequences.fs:183` pauses when the named-partner month is strictly greater than cost-center month + 6. The base named-partner month (P3-ASM-MOD034) is 6, the cost-center month is 0: the base case passes on equality. The range is triangular 3 / 6 / 12, so 6 is the mode, not a central estimate: P(month > 6) = 36 / 54 = 67% and the median is about 6.8. Setting the base to 7 in a copy: **A3 base is paused at month 6 with $216k at risk**, and the Monte Carlo pause share rises from 75% to 80%. The Monte Carlo already says the median A3 run under the kill rule ends paused with cumulative cash of -$226k ([19](../../../19-sensitivity-and-stress-analysis.md), monte-carlo table). Proposed change: report the kill-rule outcome at the median, not the mode, and lead with the Monte Carlo pause share.

## 3. Contingency does not cover the run (P3-CHL-REV2003, high, model inconsistency)

The cash engine applies contingency to development, one-time and pre-revenue run only (`Cashflow.fs:154`). The first-invoice model applies it to the whole subtotal, live run included (`Capital.fs:64-65`). Report 16 states the narrowing as a choice. It is the wrong choice for a CFO: the lean live run ($465k base, $165k-1.07M, plus the registry) is the largest and least evidenced line, built from unpriced assumptions (P3-ASM-AB010..AB017). Extending the same 25% contingency to the run (copy of `Cashflow.fs:154`):

| Measure | Published | Contingency on run |
|---|---|---|
| A3 peak cash | $1.24M | $1.44M |
| A3 payback month | 62 | 66 |
| Key figure: cash to self-sufficiency, corrected (fav / base / adv) | $222k / $1.24M / $16.97M | $227k / $1.44M / $22.51M |
| H peak cash | $4.97M | $6.01M |

Proposed change: one contingency base across models 1 and 8, or show run contingency as a separate reserve line.

## 4. The kill rule switches the company off in one month (P3-CHL-REV2004, medium, model omission)

When killed, live customers drop to zero, collections stop and every cost line stops (`Cashflow.fs:112-117`, `:138`, `:142`). A paused vendor with a signed sponsor owes transition assistance and data return, hosting through the notice period, an insurance run-off (cyber and E&O tail), a SOC bridge letter, and counsel. "Cash at risk if paused" therefore understates the exit cost. Proposed change: a wind-down cost (months of live run plus tail premiums) charged at the kill month whenever a customer has signed.

## 5. Pre-tax numbers shown as cash (P3-CHL-REV2005, medium, omission)

There is no income tax, sales and use tax on SaaS (taxable in a number of states), or payroll tax on the founder draw. A3's $11.69M cumulative cash at month 120 is pre-tax; loss carry-forwards shelter early years only. Proposed change: label "pre-tax" everywhere, or add a simple tax line after loss carry-forward.

## 6. Incident retention vanished in the correction (P3-CHL-REV2006, medium, factual)

Agent AB's working-capital line (P3-ASM-AB023, $25-200k) explicitly includes "incident retention". The model replaces that line with the arrears receivable (`Capital.fs:95-96`, `toStream` omits `WorkingCapital`) and nothing else carries a reserve for cyber and E&O deductibles, SLA credits or indemnities. Proposed change: restore a retention reserve as a one-time cash line at first go-live.

## 7. Partner-channel collections and concentration (P3-CHL-REV2007, medium, judgment)

Arrears of 1-4 months (P3-ASM-MOD002) assume Echelon invoices the sponsor. Under partner-first (DEC-001) the partner usually bills, collects and remits on a quarterly statement with dispute holdbacks, so the lag is longer and the counterparty credit is the partner's. The first sponsor is also more than 25% of revenue for years (Phase II 12 §4); the model carries no bad-debt or concentration reserve. Proposed change: partner-remittance lag as its own range (3-6 months), and a concentration reserve until three customers are live.

## 8. Customer funding is booked as if it were free cash (P3-CHL-REV2008, medium, judgment)

The customer-funded variant recovers implementation cost at signing and bills up to three months in advance (`Sequences.fs:152`). In SaaS, implementation fees that are not distinct services are deferred revenue under ASC 606, and advance billing before go-live is a refund liability if the pilot fails or the kill rule fires. The variant is right on cash timing but should not be presented as the "cheapest lever" (P3-CLM-MOD011) without a deferred-revenue and refund note.

## 9. The owner's starting point is S2, not S3 (P3-CHL-REV2009, medium, presentation)

The key figures in [16](../../../16-capital-efficient-market-entry.md) are from S3. Today is S2. From today, sequence A's base is: peak $1.94M, payback month 77, and **paused at month 24** with $1.14M spent. All paybacks are undiscounted. Proposed change: lead the owner summary with the S2 figures, and add a discounted payback at the package's own 10% rate.

## 10. Variable cost shrinks when the partner's share grows (P3-CHL-REV2010, low, model error)

`Cashflow.fs:159` applies `variable_share` to vendor revenue after the partner share. Serving an account does not get cheaper because the partner takes more. In the partner-funded variant (share uplift 0.10) this understates cost. Applying the share to gross revenue: A3 partner-funded m120 falls from $9.87M to $9.33M, and A from $7.16M to $6.71M. This strengthens P3-CLM-MOD011; it does not reverse it.

## Factual and model errors versus judgment

- **Model or factual errors**: REV2001 (fractional pilot), REV2002 (tie at the mode, presented as a pass), REV2003 (inconsistent contingency base), REV2006 (retention dropped), REV2010 (variable on net).
- **Omissions**: REV2004, REV2005.
- **Judgment**: REV2007, REV2008, REV2009.
