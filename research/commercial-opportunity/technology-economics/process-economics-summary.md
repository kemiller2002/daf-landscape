# Technology and operational economics: what the evidence supports selling

**Date:** 2026-11-20. **Detailed source:** [demand-signals-and-process-economics.md](../market-validation/demand-signals-and-process-economics.md) §3. It contains the 17-process table, built from the repository's AI-economics v2 models with their governing validation corrections applied.

**Reading the figures:**
- [S] marks a scenario output.
- [F/C] marks a figure computed from filings.
- Pools are scenario values, not observed costs.

## 1. Observed anchors

| Anchor | Value | Source |
|---|---|---|
| Operating cost per grant | DAFgiving360 $54.59 · Fidelity Charitable $67.70 · Vanguard Charitable $134 · NPT $419 · GS $574 [F/C] | INV006 |
| Loaded labour rate | 990 median $38.87/h; $57–73/h at sponsors of $250m or more [F/C] | DS anchors |
| Posted salaries | Grants processor $60–65k; grant-operations officer $125–138k [F] | DS hiring |
| Exception load | Core 7.4–7.8% of recipient lines and 11–11.6% of dollars (top 50, FY2023–24) [F/C] | DS anchors |
| AI time saving | Central 7.9%; field evidence 3–13% | DS anchors |
| AI value pool | Large national: $445k a year as an assistant; $1.31m with confidence-gated routing. $1bn community foundation: $69k. $250m community foundation: $18k [S] | DS anchors |
| Inference cost | $0.01–0.60 per case, against about $83 of reviewer time for heavy document review | DS anchors |

## 2. Improve, automate, apply AI, eliminate or leave alone

| Process | Modal winner in the model | What that implies commercially |
|---|---|---|
| Routine charity verification (P06) | **Eliminate**: a continuous status subscription replaces per-grant lookup (P = 0.94) | Sell redesign, not AI |
| Contributions, cash and securities (P02) | **Eliminate**: pre-announced transfers with structured fund references | Sell redesign |
| Grant recommendation intake (P05) | **Eliminate**: structured purpose and attestation at entry | Sell redesign |
| Onboarding and KYC (P01) | Improve manually; reuse custodian or adviser KYC | Sell redesign and integration advice |
| Complex and noncash assets (P03) | **AI-assisted document reading** is competitive (appraisals, Form 8283, LP documents) | The best AI case; low volume, high value |
| Non-standard grantee due diligence (P07) | **AI-assisted** evidence packets | The best AI case; largest per-sponsor pool, about $1.25m in the scenario |
| Grant approval and prohibited-benefit review (P08) | AI may add flags; humans clear them | Governance design, not autonomy |
| All processes at community foundations under $250m | **Leave alone** in 87–100% of runs | Do not sell to them |

## 3. Commercial implications

1. **Lead with redesign, not automation.** Automating a bad process creates little value in the repository's calibrated model. Redesign wins in most processes (DS).
2. **The AI case is narrow**: complex-asset intake and non-standard due diligence. Both are low-volume, document-heavy and high-consequence. Each AI use must specify:
   - accuracy requirements, which are high (valuation, §4943, §4966);
   - error consequences: taxable distributions, mis-substantiation;
   - human-review cost: $55/h compliance time;
   - security: donor PII and financial documents;
   - regulatory exposure: sponsor liability under §§4966 and 4967.
3. **Economics scale with grant volume, not with buyer size.** A $250m community foundation's AI pool of about $18k [S] cannot pay for an AI project with a fixed cost of $150k–750k (INV043). This supports advisory services over software for mid-size sponsors.
4. **Migration and legacy replacement have the most visible cost.** Examples are the 3–5 week grant freezes and AEF's two-year history limit. That is where advisory value is most demonstrable (OF1 and OF6 in [offerings.md](../service-offerings/offerings.md)).
5. **Third-party dependency is a diligence topic.** Ren receives 85.8% of its named 990 receipts from three customers. RCF depends on Ren. That dependency feeds the investor module (OF4) and sponsor risk reviews.

## 4. Unknowns that would change these conclusions

- Measured exception rates and reviewer minutes at any sponsor (repository item Q-N03, blocked).
- Vendor contract terms covering export, transition and renewal (P-CON-01, blocked).
- Actual migration project costs (interview questions Q3 and Q10).
