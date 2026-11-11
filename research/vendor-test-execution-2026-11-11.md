# Donor-tax platform testing: executed reference checks and vendor-access blockers

**Research date:** November 11, 2026  
**Repository:** `kemiller2002/daf-landscape`  
**Scope:** The previously defined 18 synthetic donor-opportunity scenarios X01–X18, comparing Ren's public DAF Benefit Estimator and TIFIN Give Tax Intelligence; Chariot is assessed only where a downstream grant API might be relevant.  
**Result:** Independent arithmetic and policy reference checks were performed. **No live vendor tax calculation was executed, and no vendor has passed or failed a functional scenario.**

## Executive findings

| Evidence layer | What was actually done | Result |
|---|---|---|
| **Public Ren estimator inspection** | Inspected [Ren's publicly readable estimator](https://www.reninc.com/calculate-daf-savings/) and enumerated displayed required inputs | Seven visible inputs: FMV, cost basis, capital gains rate, ordinary-income rate, investment growth, grant rate, years; public form does not visibly request AGI, filing status, other itemized deductions, charitable intent, direct donation alternative, or specific lot/recipient metadata. **Did not click Calculate or observe calculation output.** |
| **Public TIFIN intelligence inspection** | Inspected [TIFIN's Sept. 10, 2025 launch](https://tifin.com/news/tifin-give-launches-first-of-its-kind-tax-intelligence-for-philanthropy/18820/) and its [product page](https://tifin.com/product/give/) | Product claims real-time lot/holdings analysis and proposals including portfolio deviation/restricted securities. No public executable Tax Intelligence form, API or accessible evaluation environment could be established through available research interfaces. **No live output captured.** |
| **Chariot architecture scope** | Examined public [DAFpay/Donor Accounts API docs](https://docs.givechariot.com/guides/dafpay/donor-accounts/overview) | Downstream grant request and sponsor-decision infrastructure. **Not equivalent to a donor contribution tax-planning model. No authenticated API call made.** |
| **Independent arithmetic** | Executed basic deterministic numeric assertions for X02, revised X03, X04, X06 and X12 using synthetic inputs | **5/5 arithmetic scenario checks passed**, for *our reference arithmetic only*, not any vendor. No full federal/state tax returns calculated or independently signed off by a CPA. |
| **Reference behavior** | Checked 13 remaining scenarios for expected safe handling or need for specialist review | Expected guardrail cases documented, not executed against vendors and not independently validated as final tax advice. |
| **Vendor functional cases** | Attempted to identify a legitimate programmatic/test interface from public product descriptions | **Ren 0/18 executed; TIFIN 0/18 executed; Chariot X17 not executed**. No vendor fail/pass score is justified. |

## What we can responsibly infer from public Ren interface

The estimator's displayed fields are:

1. Fair market value of gifted asset.
2. Cost basis.
3. Capital gains tax rate.
4. Ordinary income tax rate.
5. Portfolio growth rate.
6. Annual grant rate.
7. Duration in years.

The visible UI lacks fields for the donor's AGI, itemization status, other deductions and prior carryovers. Those inputs are central to a personalized 2026 charitable deduction calculation and to comparing an eligible cash gift made **directly** to a charity with a DAF deposit. IRS [2026 publication](https://www.irs.gov/publications/p505) describes the 0.5%-AGI floor, and its [Nov. 10 announcement](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize) states that eligible nonitemizers may deduct direct qualifying cash gifts up to $1,000/$2,000, **excluding DAF contributions**.

This supports a narrow conclusion: the **visible form alone is insufficient to accept all required inputs for a personalized, donor-specific 2026 federal tax analysis**. It does **not** prove that Ren's estimator violates tax law, that output calculations are wrong, or that other Ren products lack those capabilities. The form itself warns that estimates require CPA review.

## What we can responsibly infer from public TIFIN interface

TIFIN's dated Tax Intelligence launch explicitly claims automatic assessment of holdings and tax-efficient securities contribution proposals. Its current public site markets Tax Intelligence and advisor workflows. This establishes that **the product is marketed as more proactive than an ordinary calculator**.

The materials do **not** establish correct application of the 2026 AGI floor, itemization and direct-gift comparison, QCD restrictions, cost-basis/lot exceptions, privacy boundaries, automation scope, or audited false-positive rates. A demo sign-up link is **not an authorized sandbox**. No credentials or vendor-specific implementation access were available, so a pass/fail assessment would be invented.

## The five independent numeric reference checks

All numbers below are synthetic, deliberately simplified, and not personalized financial advice.

| Case | Executed reference check | Reference result | Limits |
|---|---|---|---|
| **X02** | 2026 MFJ standard-deduction filer, eligible direct cash gift $1,500 versus DAF contribution $1,500 | New nonitemizer deduction: **direct $1,500; DAF $0** | Assumes direct charity otherwise eligible; not a full tax return |
| **X03 (corrected)** | Single filer, **AGI $900,000**, assumed **taxable income $800,000**, cash charity gift $20,000 | 0.5% floor **$4,500**, so **$15,500** remaining before other limits | Final top-bracket tax savings not calculated; 35% limitation must be applied by proper tax calculation |
| **X04** | Long-term stock FMV $100,000, basis $20,000 | Embedded unrealized gain **$80,000** | This is **not $80,000 of tax savings**; in-kind direct gifts also generally avoid realizing donor gain |
| **X06** | Loss asset basis $100,000, FMV $65,000 | Unrealized **loss $35,000**, not an appreciated asset | Sale-and-gift tax result depends on facts |
| **X12** | Hypothetical three-year $8k/year giving, MFJ, AGI $250k, other itemized deductions $25k, 2026 rules held constant all three years | Direct route **$102,600 total deductions**; DAF bunch route **$112,150**; difference **$9,550**; assumed 24% tax-rate illustration **$2,292** | Hypothetical threshold freeze is **not** a 2027–28 forecast; excludes fees, other deduction complications and actual marginal brackets |

### Correction to X03

The earlier test fixture had AGI $600,000 and a 37% bracket. **That is internally inconsistent for an ordinary 2026 single filer**, whose top 37% bracket begins above $640,600 of **taxable income**; it is even less plausible for a married joint filer. We updated X03 to explicitly assume a **single filer with $900,000 AGI and $800,000 taxable income**, preserving a plausible 37% bracket, and then recomputed the 0.5% floor. [2026 IRS bracket table](https://www.irs.gov/newsroom/working-families-tax-cuts-individuals-and-workers).

The corrected assumption belongs in [the fixture](../data/tax-opportunity-test-cases-2026.csv), not just this report. The independent arithmetic check is **not a final tax-opinion test**.

### Independent decision expectations for X01, X05, X07–X11, X13–X18

These 13 cases address consent, restricted/short-term lots, unvested stock, business-sale tax law, QCD recipient eligibility, same-year direct-giving equivalence, cross-tenant data privacy, incomplete contribution ownership, agent action authorization, grant-versus-contribution deduction timing, and insufficient inputs for carryovers/AGI limits.

We documented what a prudent platform *should* do: suppress inappropriate recommendations, stop on missing facts, require consent/sponsor authority, request specialist review, and avoid double-counting. They are **reference expectations, not live outcomes**. Numerical accuracy, negative testing, regulatory correctness, data privacy and control integrity still require expert-reviewed expected results and vendor-executed evidence.

## Per-scenario vendor-access matrix

See [data/vendor-test-access-2026-11-11.csv](../data/vendor-test-access-2026-11-11.csv). It includes 36 per-case Ren/TIFIN rows and one Chariot downstream case. Every live test is **`not_executed`**.

**Ren source-level input gaps:** Some cases contain FMV/basis information usable in the seven-field form (X04, X06), but its public UI has no visible controls to express the surrounding facts needed to adjudicate the full scenario. For others, the interface is plainly outside scope (QCD, tenant permissions, business-sale legal status). Missing public controls **cannot** be treated as evidence that a different Ren service lacks them.

**TIFIN access gaps:** No publicly executable Tax Intelligence engine, simulator or documented evaluation API was accessible. This is not evidence that the product does not work, or that it performs worse than Ren.

## Required access to finish the requested head-to-head

### Ren
- Authorized access to current **DAF Benefit Estimator outputs**, formula/assumption document, and any advisor client-screening product.
- A reproducible sandbox or controlled vendor demo with synthetic securities, tax lots and direct-gift comparators.
- Explanation of what is a general illustration versus a customized calculation; product/module and sponsor/legal entity identity.
- Version and test date plus review by a qualified tax practitioner.

### TIFIN Give
- Authorized Tax Intelligence sandbox with synthetic clients/holdings (including restricted, loss, unvested and long-term lots), advisor permissions and full output/assumption export.
- Explicit 2026 tax-rule coverage, model version, risk and restricted-list implementation, advisor/human authorization, tax data provenance, and release notes.
- Single-Charity Fund legal documentation for case X11; do not infer QCD qualification solely from fund branding.

### Chariot (downstream, separate scope)
- Test tenant for a simulated donor grant, grant rejection, sponsor authorization, disbursement and reconciliation. This does not test pre-funding donor tax recommendations.

### Evidence to collect for every run
- Vendor, legal entity, system/module, edition, build/version, environment, tester, review date and authorization.
- Synthetic fixture ID, inputs, expected CPA-approved result, vendor output, screenshot or raw API response, permission/approval audit evidence, errors and limitations.
- Separate status `pass_verified`, `fail_verified`, `needs_review`, or `not_executed`. Missing access must never become a vendor failure.
- Never place vendor confidential files, signed audit reports, private data, expert-network communications, or NDA-restricted material in this research repository.

## Decision

**No vendor winner declared.** On public evidence TIFIN has a documented claim to proactive portfolio-based opportunity detection, Ren has a public illustrative estimator and advisor planning support, and Chariot supports downstream grant workflow. The **comparative correctness of the donor recommendations is unverified**.

Next gates: obtain authorized product access, CPA-reviewed expected outputs, and consistent live case evidence. Do not publish vendor-relative accuracy or “2026 tax compliant” claims until those gates pass.
