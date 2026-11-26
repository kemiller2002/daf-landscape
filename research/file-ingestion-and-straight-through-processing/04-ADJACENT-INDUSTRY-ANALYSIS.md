# 04 — Adjacent industry practices and their transfer to DAF administration

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26). Evidence ids `FIE-*` resolve in [`data/file-ingestion-2026-11/evidence.csv`](../../data/file-ingestion-2026-11/evidence.csv). Classification: **CONFIRMED** (public source), **INFERRED** (reasoned from confirmed facts), **PROPOSED** (innovation, not observed practice).

## Practices in adjacent industries

| Industry | Mature practice | Measured evidence | Transfer to DAF |
|---|---|---|---|
| Banking / treasury | Prior-day BAI2 or camt.053 auto-reconciled to the ledger; exception queues | Vendor-reported auto-match of 85–95% on structured bank data; no verified independent survey (FIE-B-015, inferred) | **High.** Gift receipts and cleared grants against bank activity. Target ≥90% auto-match on ACH and wire, lower on checks |
| Payments | Tracker-based STP (Swift gpi); ISO 20022 structured remittance | gpi: ~60% credited within 30 minutes, ~100% within 24 hours (FIE-B-016); Fedwire, CHIPS and FedNow are ISO 20022 (FIE-B-026/027/029) | Medium. Use structured remittance; give donors and grantees status tracking |
| ACH origination | Batch and file control totals; entry hash; return and NOC processing; 2026 fraud monitoring | Rules (FIE-B-031–034) | **High** and mandatory |
| Custody / brokerage | Daily files plus APIs; custodian as book of record | (FIE-B-055–057) | High for investment pools; the custodian is the authority |
| Fund administration | NAV control, 4-eyes on price overrides, break management | No public benchmarks retrieved | High. Pool unitization and reconciliation to custodian |
| Insurance (ACORD) | Industry-owned standards, paid licensing (forms EUL since 2020; memberships based on revenue) | (FIE-B-042) | Low as a format; useful as a governance pattern |
| Payroll | Fixed calendars, NACHA batches, pre-notes, prior-period reconciliation | Not measured this session | Medium. Prenote / micro-deposit style account verification for new grantees |
| AP / invoice automation | Capture, classify, extract, match, route exceptions, approve | Ardent: $9.40 average versus $2.78 best-in-class per invoice; exceptions 14% versus 9%; cycle 9.2 versus 3.1 days (FIE-B-008/009, inferred). APQC: top quartile ≤$2.07, median $5.83, bottom ≥$10 (FIE-B-010, inferred, dated) | **High.** Grant requests and inbound gift documents follow the same capture-to-approval pipeline |
| AR / cash application | Remittance matching, ML that improves with tenure | Billtrust ~88.5% envelope / 93.9% line match (FIE-B-012); HighRadius 72–75% under 6 months rising to 91–93% after 24 months (FIE-B-013); 44% of organizations have little automation (FIE-B-014). All inferred / vendor | **High.** Matching inbound gifts to donors and funds. Expect a cold start for new sponsors |
| Mortgage servicing (MISMO) | Reference data model, licensed (~$2,500 per year membership, inferred) | (FIE-B-041) | Low. Pattern only |
| Healthcare (X12 835/837, CAQH CORE) | Operating rules on top of standards; EFT plus ERA reassociation via trace numbers; auto-posting | Average $7.93 manual versus $3.39 electronic; remittance $6.24 versus $3.03; ERA 89% electronic; auto-post targets 90–95% (FIE-B-001–007, FIE-B-063) | **Very high.** Reassociating an ACH/EFT payment with its remittance through a trace number is the same problem as matching a gift to its donor and fund or a grant to its acknowledgement. Copy the CORE idea of a trace number on payment and remittance |
| Government / tax (IRS MeF) | Schema-versioned XML, business rules, acknowledgements, annual DIFFs | 93% of individual returns e-filed in 2025 (FIE-B-022); 990 family e-file mandatory (FIE-B-050) | High. Handle schema evolution by tax year; acknowledgements for every submission |
| Regulatory reporting | Versioned taxonomies, validation rules before submission | Pattern | Medium. 990 Schedule D aggregates, state filings |
| EDI trading partners | Partner profiles, mapping, certification testing | 8–12 weeks per partner traditionally; 7–10 days on mapping alone (FIE-B-021, inferred) | **High as a warning.** Sponsor onboarding must be measured in days. Use self-service mapping with AI-proposed column maps, validated against sample files |
| Enterprise data migration | Staged extract, transform and load, reconciliation reports, parallel run | Pattern | **High.** Moving sponsors off incumbent DAF systems is the first deal-blocker |

### Practices to adopt (proposed for a new DAF platform)

1. **Control totals on every batch.** Record count, amount sums per currency and type, and a hash, modeled on NACHA batch and file control. Reject or quarantine any batch where they do not match.
2. **Duplicate file detection.** Check the SHA-256 of the raw bytes, a business key (sender, file date, file ID modifier and sequence, as NACHA does), and a semantic near-duplicate check on row sets. Duplicate bank files and duplicate ACH files are classic incidents.
3. **Immutable raw landing zone.** Store every inbound object byte-for-byte with its provenance (channel, sender authentication verdict, received time). Parse into versioned staging, then promote. Reprocessing should mean replaying from raw.
4. **Exception-based operations.** Run STP by default and route by confidence. Measure the touchless rate per channel, the way CAQH reports electronic adoption by mode. Benchmarks to aim for: ≥90% auto-match on electronic receipts (inferred from AR and bank-rec vendors); exceptions ≤10% (Ardent best-in-class 9%; others 22%).
5. **Document classification and extraction.** Classify (grant letter, stock transfer LOA, W-9, IRS determination letter, 990, trust document), then extract, check against authoritative data (BMF, Pub 78, OFAC), and send to human review below a confidence threshold. Keep the decision trace.
6. **Schema evolution.** Use versioned parsers per partner and format version, and contract tests against stored sample files. Handle IRS MeF annual DIFFs, ISO 20022 message versions, and bank BAI2 type-code tables as data, not code.
7. **Data quality management.** Normalize EINs and routing numbers and verify check digits. Encode known dataset defects as rules, such as the 2020 revocation-date errors (FIE-B-045) and the BMF address being the HQ address. Diff government snapshots month to month.
8. **Operational recovery.** Make reprocessing idempotent using file and batch keys. Track the EOD cycle (missing-file alerts on the expected arrival schedule). Use a return and NOC feedback loop. Support reversal and reissue of grant payments.
9. **Partner onboarding automation.** Offer self-service sample-file upload, AI-suggested mapping, a validation report and a sandbox certification run. Target days, not the 8–12 EDI weeks.
10. **Payment-instruction controls.** These support an Originator's risk-based fraud-monitoring obligation under the Nacha Rules (Phase 2 effective 2026-06-19, practically 2026-06-22; FIE-B-034) and are backed by the BEC/AFP evidence; the rule requires risk-based processes, not these specific controls. Bank-detail changes need out-of-band verification and dual approval, and email is never sufficient on its own.

---

## Gaps and caveats

- I did not verify these and labeled them inferred or left them out: BAI2's current official spec hosting and status; Bloomberg and ICE evaluated-pricing terms; NY Charities Bureau bulk data; Envestnet/Yodlee, Orion, Addepar and Black Diamond specs; MFT cost benchmarks; an RDC adoption share; an independent bank-reconciliation auto-match survey; NACHA C-code details and the exact current R-code list (paid Rules).
- The Ardent, APQC, Billtrust, HighRadius and DMARC figures come from secondary or vendor sources.
- The CAQH numbers are primary, read from the PDF tables, and cover labor cost only, not system cost.
- No DAF-specific STP or cost benchmark exists in public sources. The 5–20% exception tail (widened from 5–15% after review) is a proposed planning assumption.

