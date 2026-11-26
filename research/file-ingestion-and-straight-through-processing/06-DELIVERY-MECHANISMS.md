# 06 — Information delivery mechanisms

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26). Evidence ids `FIE-*` resolve in [`data/file-ingestion-2026-11/evidence.csv`](../../data/file-ingestion-2026-11/evidence.csv). Classification: **CONFIRMED** (public source), **INFERRED** (reasoned from confirmed facts), **PROPOSED** (innovation, not observed practice).

## Delivery mechanisms

| Mechanism | Where it is mature | Evidence | Fit for DAF | Recommendation |
|---|---|---|---|---|
| Browser upload | SaaS onboarding, AP portals | Universal | Migration, ad-hoc gift batches, documents | **Initial**, with preview, column mapping, dry-run validation and a control-total check |
| REST/JSON API plus webhooks | Fintech, FDX, custodians' newer APIs | Schwab, Fidelity and Pershing all offer APIs next to files (FIE-B-055/056/057) | Partner giving platforms, CRMs, sponsor systems | **Initial**; webhooks carry file references (signed URLs) plus hashes, not payloads |
| SFTP | Bank EOD (BAI2, NACHA, lockbox), custodian daily files | Schwab offers server SFTP (FIE-B-055); Pershing FTP/email (FIE-B-057) | Bank and custodian batch | **Initial** (managed SFTP endpoint per sponsor, PGP optional, key rotation) |
| MFT (managed file transfer) | Banks, large enterprises | Vendor market; no public cost benchmark retrieved | a new platform's own SFTP plus audit covers most of it | **Conditional** (AS2 or vendor MFT only if a bank requires it) |
| Scheduled pull of government downloads | IRS TEOS, OFAC SLS | Monthly IRS postings; OFAC deltas (FIE-B-044/051) | Charity validation, sanctions | **Initial** |
| Partner download endpoints | Custodian portals (Schwab Advisor Center) | (FIE-B-055) | Fallback when SFTP is unavailable | **Conditional** (RPA-style scraping deferred) |
| Authorized email ingestion | AP invoice inboxes | BEC $2.77B in 2024 (FIE-B-019); wires were BEC targets for 63% of AFP respondents (FIE-B-059); DMARC p=reject ~17.6% (FIE-B-020) | Documents (grant letters, stock transfer forms) | **Conditional**: allow-listed senders, DMARC/SPF/DKIM verdict stored, attachments sandboxed; **never a sole authority for payment or bank-detail changes** (out-of-band verification required) |
| Scanned mail (digital mailroom) | Insurance, AP, nonprofits | ~$2.00 per envelope plus $0.25 per page example (FIE-B-061, inferred); scanner break-even ~5,000 checks/yr (FIE-B-062, inferred) | Mailed gifts and correspondence | **Conditional** (partner with the sponsor's bank lockbox or a mailroom vendor; ingest images plus data) |
| Fax-to-email | Healthcare (CAQH counts fax as "manual") | CAQH manual modes include fax (FIE-B-001) | Rare | **Deferred** (handle as a PDF arriving by email) |

**When APIs beat files.** APIs win for event-level, low-latency needs: gift notifications, grant status (CAQH status inquiry costs $18.18 manual versus $3.68 electronic, FIE-B-004), and intraday balances.

**When files beat APIs.** Files win for bulk, point-in-time institutional cycles: bank prior-day BAI2/camt.053, NACHA origination windows, custodian end-of-day positions, and monthly government snapshots. Here the file is the reconciliation unit, with a header, a trailer and control totals, and it is the system of record for that business date. Custodians offer both channels in parallel (FIE-B-055/056). a new DAF platform should do the same: a file for each authoritative EOD snapshot and an API for deltas, reconciled to each other.

---

## Analysis: one boundary, many channels

**The industry problem.** At the sponsors studied, the same information arrives through parallel channels with
different rules: a gift-of-securities notification by web form, PDF by fax or email, or phone; a grant recommendation
online, by paper form or by advisor email (02, FIE-A-008, FIE-A-034, FIE-A-134). Each channel tends to grow its own
checks, so a control applied online may not apply to the paper path.

**The transferable pattern (INFERRED from AP, healthcare and EDI practice in 04).** Separate *transport* (authenticate
the source, move bytes) from *meaning* (parse, validate, act). Every channel lands bytes in one place with provenance;
one set of parsers and rules runs after that. Healthcare's EFT/ERA reassociation and AP capture platforms work this way.

**Pull versus host.** Banks and custodians already operate file distribution (SFTP, download services, APIs;
FIE-B-055..057, FIE-B-060). A receiving platform can usually *pull* from them instead of hosting an inbound SFTP
service; hosting is needed only for a partner that can only push. Stream B recommended a managed inbound SFTP endpoint
per sponsor from the start; the synthesis treats that as conditional, because pull covers the documented custodians and
avoids operating an Internet-facing file service (recorded as a disagreement in the research ledger).

**Email.** The evidence (BEC losses, low DMARC enforcement) supports treating email as a channel for documents only,
never for instructions; even document intake by email adds spoofing and attachment risk that an authenticated portal
avoids. Stream B rated authorized email ingestion conditional; the synthesis agrees for documents and rejects it for
instructions.
