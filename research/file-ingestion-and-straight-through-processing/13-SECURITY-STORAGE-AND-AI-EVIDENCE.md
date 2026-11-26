# 13 — Security, storage and AI document-processing evidence

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26). Evidence ids `FIE-*` resolve in [`data/file-ingestion-2026-11/evidence.csv`](../../data/file-ingestion-2026-11/evidence.csv). Classification: **CONFIRMED** (public source), **INFERRED** (reasoned from confirmed facts), **PROPOSED** (innovation, not observed practice). Prices marked *measured* were read from the AWS Price List API or Azure Retail Prices API on 2026-11-26.

## 1. Malware inspection without a custom engine

### 1.1 Options by cloud

| | AWS: GuardDuty Malware Protection for S3 | Azure: Defender for Storage malware scanning | GCP: no native service |
|---|---|---|---|
| Price | Measured: **$0.09/GB** plus **$0.215 per 1,000 objects**. The first 1 GB and 1,000 objects each month are free (FIE-C-001/002). | Measured: **$0.15/GB**, plus a plan meter of $0.0134/hour, about **$9.78 per storage account per month** (FIE-C-006). | Self-hosted ClamAV on Cloud Run. This is Google's own reference architecture (FIE-C-011). |
| Size limit | 100 GB per object. Up to 100k extracted files and nesting depth 100 (FIE-C-003). | 50 GB per blob. Scans time out after 30 minutes to 3 hours (FIE-C-007). | Set by you (ClamAV MaxFileSize/MaxScanSize). |
| Archives | Extracted. Password-protected archives come back as `UNSUPPORTED`. | ZIP and RAR are scanned. | ClamAV unpacks archives. It was hit by Fifield's overlapping-file zip bomb, and the 0.101.3 fix was reported incomplete (FIE-C-013). |
| Result channel | Object tag `GuardDutyMalwareScanStatus`, plus the EventBridge event "Object Scan Result" (FIE-C-004). | Blob index tags, Event Grid, alerts and Log Analytics. **Microsoft says index tags are not tamper-resistant** (FIE-C-009). | You write the result yourself (move between buckets or set metadata). |
| Fail-closed primitive | An AWS-documented bucket policy denies `GetObject` unless the tag is `NO_THREATS_FOUND`. Only GuardDuty may set that tag. | ABAC on index tags, but use Event Grid as the source of truth. If the monthly GB cap (default 10 TB) is reached, scanning **stops** and blobs come back "Not scanned" (FIE-C-008). | Separate unscanned, clean and quarantine buckets. The application can only read from the clean bucket. |
| Engine quality | Amazon engine (proprietary). | The same engine as Microsoft Defender Antivirus. Microsoft notes it misses more on storage scans than on endpoints because there is no MOTW, path or behavior context (FIE-C-010). | ClamAV is materially weaker. One study reports about 60% detection on commodity malware (FIE-C-012, inferred). |
| Rescan | On-demand scan API at the same rates. | On-demand scanning. | A job you build that re-runs after signature updates. |

Scan latency: no vendor publishes an SLA. Treat scanning as asynchronous, taking seconds to minutes (assumed), and design the UI to show a "pending scan" state.

### 1.2 Third-party scanners and CDR
- **VirusTotal or any public multi-scanner is unacceptable.** File contents "may also be shared with premium VirusTotal customers" (FIE-C-016).
- **OPSWAT MetaDefender** offers multi-AV and Deep CDR (Content Disarm and Reconstruction). Pricing is by quote, and CDR and AV count as separate requests. Use **MetaDefender Core self-hosted inside our VPC/VNet** rather than the multi-tenant cloud API (FIE-C-017, inferred).
- Cloudmersive and similar SaaS APIs carry the same confidentiality issue. They would only be acceptable with a contract that keeps data in-region with no retention, or with a self-hosted deployment. Their pricing was not researched.
- **CDR** is the strongest control for PDFs and Office files. OWASP recommends it for documents (FIE-C-018). It costs money and can lose fidelity, so it is optional at MVP. The cheap substitute is "render PDF pages to images or PDF/A in a sandbox" (section 3).

### 1.3 Fail-closed state machine (proposed)
The document states are `RECEIVED → QUARANTINED → SCANNING → (CLEAN | INFECTED | UNSCANNABLE | SCAN_FAILED) → PARSED → AVAILABLE`.
- Only `CLEAN` may move forward.
- `UNSUPPORTED`, `ACCESS_DENIED`, `FAILED`, "Not scanned", "Scan timed out" and ClamAV `Heuristics.Limits.Exceeded.*` all count as **not clean**.
- A PostgreSQL command `ScanTimeout` (via SKIP LOCKED) raises an alert after the SLA, for example 15 minutes. It never auto-releases the file.
- The scan verdict, engine name and verdict time are recorded in PostgreSQL from the event (EventBridge or Event Grid), not from tags alone.
- **Rescans:** a nightly job re-scans files ingested in the last N days (for example 30) through the on-demand API. A file that turns `INFECTED` later becomes `QUARANTINED_RETRO`. This blocks downloads and alerts compliance. The file is **not deleted** if Object Lock retention applies.

**Recommended scanner per cloud:**
- **AWS:** GuardDuty Malware Protection for S3 with tag-based access control (TBAC). This is the lowest-effort and lowest-cost option.
- **Azure:** Defender for Storage on-upload scanning with Event Grid results, plus a raised GB cap.
- **GCP:** the weakest option. Either use ClamAV on Cloud Run (the reference architecture, with weaker detection) as a baseline, or license a commercial engine container. GCP's lack of a native scanner counts against it in the cloud selection.

---

## 2. Storage: PostgreSQL bytea vs object storage

### 2.1 Facts
- bytea and TOAST hold at most 1 GB per value. Values are stored in chunks of about 2 kB, so every byte also flows through WAL, PITR backups, replicas, `pg_dump`, restore time and vacuum (FIE-C-019). Large objects (`pg_largeobject`) avoid the 1 GB limit, but they add orphan and vacuumlo management and fit poorly with managed backup and restore. Not recommended.
- Price per GB-month (FIE-C-020..026):

| | Object storage | Managed PostgreSQL storage | PostgreSQL backup beyond free |
|---|---|---|---|
| AWS | S3 Standard **$0.023** (measured) | RDS gp3 $0.115; **$0.23 Multi-AZ** (inferred) | ~$0.095 (inferred) |
| Azure | Blob Hot LRS **$0.0208**, ZRS $0.026 (measured) | Flexible Server **$0.115**, doubled with HA (measured / inferred) | **$0.095** (measured) |
| GCP | GCS Standard **$0.020** (inferred) | Cloud SQL SSD ~$0.17, doubled with HA (inferred, verify) | ~$0.08 (inferred) |

With HA, PostgreSQL bytes cost about **10x object storage**, before WAL and PITR churn.

- **WORM retention and legal hold exist only in object storage.** All three clouds have a Cohasset assessment against SEC 17a-4(f):
  - **S3 Object Lock in compliance mode.** Not even root can delete before the retain-until date. Legal hold is independent of retention and has no expiry. The new **variable retention (event hold)** suits "retain 7 years after account closure" (FIE-C-027/028).
  - **Azure immutable storage.** Policies must be **locked**. Version-level legal-hold changes are not audited (FIE-C-029).
  - **GCS Bucket Lock / Object Retention Lock**, assessed December 2023 (FIE-C-030).

  DAF sponsors are not normally broker-dealers. Use 17a-4 as a quality bar, not as a legal requirement (inferred).
- Integrity: S3 now applies CRC64NVME by default and supports SHA-256 or SHA-512 additional checksums. A presigned PUT can require `x-amz-checksum-sha256`, so S3 rejects bytes that do not match (FIE-C-031).

### 2.2 Recommendation (proposed)
**Store all file bytes in object storage. Use no size threshold.** PostgreSQL holds metadata, the SHA-256, the state machine, extracted structured data such as parsed CSV rows, and audit records.

Reasons for a single path:
1. One code path for scanning, retention, legal hold and download.
2. Native scanners (GuardDuty and Defender) only watch object stores.
3. WORM cannot be achieved in PostgreSQL.
4. Database backups, restore RTO and replica lag stay small.
5. Cost is about 10x lower.

A "small files in PostgreSQL" threshold would save one object-store round trip. In exchange, it would double the scan, retention and export logic, which is not a simplicity win.

### 2.3 Layout and consistency pattern (proposed)
- **Two buckets/containers per environment:**
  - `ingest-quarantine`: no lock, 7-day lifecycle expiry, scanner attached, no application read.
  - `records`: versioned, Object Lock or immutability on, SSE-KMS / CMK.
- Keys are `t/{tenant_id}/{document_id}`. The document ID is a UUIDv7 generated server-side. The user's filename is stored only as metadata.
- **Upload flow:**
  1. A PostgreSQL transaction inserts `document(id, tenant, state=AWAITING_UPLOAD, expected_sha256, expected_size)`.
  2. The server issues a presigned PUT or POST that is short-lived (5 minutes or less), bound to the exact key, a content-length range and the checksum.
  3. The client uploads the file to quarantine.
  4. The scan event moves the row to `CLEAN` or `INFECTED`. A worker verifies the SHA-256 and magic bytes, then parses the file in a sandbox.
  5. A worker server-side copies the object to `records/` with retention set, then commits `state=AVAILABLE` with the version ID. The copy is idempotent by key.

  Because records are locked, **nothing enters `records/` until the DB row exists**, so locked orphans cannot occur. Quarantine orphans expire through the lifecycle rule.
- **Reconciliation:** a weekly job compares S3 Inventory, Azure Blob Inventory or GCS Storage Insights against PostgreSQL. It flags `missing_object` (row without object, alert) and `orphan` (object without row, reported, never auto-deleted under lock). A sampled re-hash job checks stored checksums.
- **Encryption:** use SSE-KMS / CMK per environment. Per-tenant KMS keys are optional. S3 Bucket Keys, Azure encryption scopes and GCS CMEK per bucket can provide them, but they add key-count cost and operational burden. Recommendation: one key per environment at MVP, with tenant isolation enforced by key-prefix IAM conditions plus the application's authorization. Revisit if a tenant contract requires crypto-shredding, which also conflicts with WORM.
- **Presigned URL risks:** a presigned URL is a bearer token. It leaks through logs, Referer headers and browser history. Keep TTLs short (60 to 300 seconds), use single-object keys, and add `response-content-disposition=attachment`. Never presign the quarantine bucket for reads.

---

## 3. Parser and file security (.NET)

| Threat | Control (proposed unless cited) |
|---|---|
| Type confusion and polyglots | Allowlist by declared type, **and** magic bytes, **and** a successful parse by the expected parser. Reject when they disagree. Do not use libmagic as the authority, because it reads only the leading bytes and polyglots pass it. OWASP says not to trust Content-Type (FIE-C-018). |
| Zip bombs | A 42 kB file can expand to 5.5 GB, and 46 MB to 4.5 PB, with no recursion (FIE-C-032). ZIP is denied. XLSX and DOCX are ZIP inside, so for XLSX: cap entry count (for example 1,000), total uncompressed bytes (for example 100 MB), per-entry ratio (100:1) and overlapping entries. Count bytes while streaming; never trust header sizes. Reject any entry path containing `..` or starting with `/`, which is zip slip, even though nothing is extracted to disk. |
| XXE / billion laughs | In .NET, `XmlReaderSettings` defaults to `DtdProcessing.Prohibit` and `XmlResolver = null` (FIE-C-037). Set both explicitly anyway, plus `MaxCharactersFromEntities` and `MaxCharactersInDocument`. Do not call `XmlDocument.Load` directly on untrusted input. |
| JSON | `System.Text.Json` defaults to MaxDepth 64 (FIE-C-038). Cap byte length before parsing, deserialize into strict F# DTOs, and reject unknown or duplicate members. |
| CSV | CsvHelper with a fixed column schema, a maximum field length, a maximum row count, and a culture-invariant number and date format. **CSV/formula injection matters on export:** prefix cells starting with `= + - @`, TAB, CR or LF with `'` and quote them (FIE-C-039). |
| XLSX | Accept `.xlsx` only, never `.xlsm` or `.xlsb`. Read values only, using ExcelDataReader or the OpenXML SDK SAX reader. Never evaluate formulas, follow external links or honor DDE. Discard `vbaProject.bin` and externalLink parts. ClosedXML loads the whole DOM into memory, so use it only under the size cap. |
| PDF | Risks are JavaScript, `/Launch`, `/EmbeddedFile`, XFA and `/OpenAction`. Text extraction with PdfPig is fully managed, but still cap pages and time. Use qpdf to normalize, or rasterize pages to PNG / PDF/A in the sandbox for display (a CDR-lite). PDF.js CVE-2024-4367 allowed arbitrary JavaScript on open (FIE-C-035), so even browser viewers need patching and an isolated origin. |
| Images | Run `Image.Identify()` first, which reads dimensions without decoding. Reject anything over N megapixels (for example 50 MP) or with more than one frame. Decode with ImageSharp, using `DecoderOptions.MaxFrames` and a bounded `MemoryAllocator` (FIE-C-036). **Re-encode** to PNG or JPEG, which also strips EXIF and GPS. Native codec CVEs justify isolation: libwebp CVE-2023-4863 (CVSS 8.8, on CISA KEV; FIE-C-033) and ImageTragick (FIE-C-034). Avoid ImageMagick. If you use SkiaSharp, which bundles native Skia and libwebp, keep it patched and sandboxed. |

**Sandboxing (proposed, platform facts inferred):** parse in a **separate worker process or container with no network egress**, a read-only root filesystem, a non-root user, CPU, memory and time limits, and seccomp's default profile. Options by cloud:
- AWS: Lambda (Firecracker microVM) or ECS Fargate in a subnet without NAT, plus an S3 VPC endpoint.
- Azure: Container Apps job in an NSG-locked subnet with a private endpoint.
- GCP: Cloud Run job (gVisor in gen1, microVM in gen2) with `--vpc-egress=all-traffic` and no NAT.

This keeps the "component monolith". The parser is a second deployable of the same F# code, invoked through the PostgreSQL command queue. It needs no broker.

**Safe browser presentation (proposed; FIE-C-040):**
- Serve downloads only from a **separate download origin**, such as a different registrable domain, through short-lived presigned URLs.
- Set `Content-Disposition: attachment`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy: sandbox; default-src 'none'` and `Cross-Origin-Resource-Policy: same-site`.
- Use an exact `Content-Type` taken from the server-verified type, not the type the uploader declared.
- Previews show the **re-encoded raster** rather than the original PDF.

---

## 4. AI document processing

### 4.1 Price per 1,000 pages (first tier)
| Capability | AWS Textract (measured, FIE-C-041) | Azure Document Intelligence (measured, FIE-C-042) | Google Document AI (inferred, FIE-C-044) |
|---|---|---|---|
| OCR / read | $1.50 | $1.50 | $1.50 (Enterprise OCR) |
| Layout | $4 | $10 | (Layout parser not verified) |
| Expense / receipt / invoice | $10 (AnalyzeExpense) | $10 (prebuilt) | not verified |
| ID | $25 (AnalyzeID, first 100k) | $10 (prebuilt) | not verified |
| Queries / query fields | $15 | +$10 add-on | n/a |
| Forms (key-value) | $50 | included in Layout / prebuilt | $30 (Form Parser) |
| Custom | Adapters ~$25 for Queries + custom (verify) | $30 | $30 (Custom Extractor) |
| **US check** | no prebuilt (use Queries) | **prebuilt-check.us, $10** | not verified |
| **Bank statement** | no prebuilt | **prebuilt-bankStatement, $10** | not verified |
| W-9 / IRS determination letter | none | **none** (has W-2, 1099, 1098 and others) | none verified |

**LLM extraction (Claude, inferred from the cached price list, FIE-C-045):**
- Prices per million tokens (input / output): Haiku 5.5 $0.10 / $0.50; Sonnet 5.5 $2 / $10; Opus 5.5 $4 / $20.
- Assuming about 2,500 input and 500 output tokens per page, that is roughly **$0.50 (Haiku), $10 (Sonnet) and $20 (Opus) per 1,000 pages**. Thinking tokens add to this on Opus 5.5, where thinking is always on and effort defaults to medium. Measure the real token count with `count_tokens`.
- **Data residency:**
  - Use **Amazon Bedrock** (AWS), **Microsoft Foundry "Hosted on Azure" deployments** (Azure), or **Vertex AI** (GCP) so documents stay inside the chosen cloud.
  - On Anthropic's first-party API, inputs and outputs are deleted within 30 days. **Zero data retention (ZDR) is available by agreement.** Fable and Mythos "covered models" always require 30-day retention, so do not use them for donor documents (FIE-C-046).
  - Batch (50% discount) and the Files API are first-party only (FIE-C-047).

**Accuracy evidence is thin.** No independent benchmark was found for checks or remittances, W-9s or determination letters. Vendor-run studies show:
- Handwriting: Azure 86.6%, Google 84.5%, Textract 84.1% on 183 pages.
- Multi-page bank statements: a 91% vs 64% spread between engines.
- LLMs lead on clean handwriting.

All of these are inferred, from small vendor samples (FIE-C-048). **Recommendation:** build a labeled test set of 200 to 500 de-identified documents per type and measure **field-level** exact-match accuracy before choosing an engine.

### 4.2 Prompt injection and authority (proposed, grounded in FIE-C-049/050)
- OWASP LLM01:2025 covers indirect and multimodal injection, for example instructions hidden in an image or PDF, and says there is "no foolproof prevention". EchoLeak (CVE-2025-32711, CVSS 9.3) showed one crafted email causing data exfiltration through an LLM that had data access. The OWASP page fetched for this research itself contained an embedded instruction block.
- Controls:
  1. The extractor gets **no tools, no network, and no tenant data** beyond the single document.
  2. Output must match a **strict JSON schema** (structured outputs). Free text is never executed or rendered as HTML.
  3. **Deterministic validation** runs after extraction: EIN checksum and format, ABA routing checksum, amount ranges, a check that the date is not in the future, cross-footing against the CSV or bank feed, and payee matching against the allowlisted charity registry (IRS Pub 78 / BMF).
  4. The LLM output is only a **proposal**. Any movement of money or change of grant status requires a human approval or a rule-engine decision on validated fields.
  5. Document text goes in a clearly delimited user-content block. The system prompt states that document content is data. Log every extraction with its model version.
- **Confidence calibration pitfalls (inferred):**
  - Textract and Azure confidence scores are per-word or per-field OCR scores, not the probability that the business field is correct.
  - LLM self-reported confidence is poorly calibrated.
  - Set thresholds empirically on the test set for each field and engine. Route anything below threshold, or any validator failure, to human review, and track the precision of the auto-accept path over time.

---

## 5. Cost table (US East / us-central1, list prices, first tier)
Assumptions: average file 0.5 MB; average document 2 pages; no free tiers; egress excluded.

| Cost item | AWS | Azure | GCP |
|---|---|---|---|
| Scan, per GB | **$0.09** (measured) | **$0.15** (measured) | ClamAV compute about $0.05–0.10/GB marginal (inferred) |
| Scan, per 1,000 files | **$0.26** (0.5 GB × $0.09 + $0.215) | **$0.075** + ~$9.78 per account per month fixed | about $0.05 + about $50–150 per month warm instance + ops (inferred) |
| Object storage, per GB-month | $0.023 | $0.0208 LRS / $0.026 ZRS | $0.020 (inferred) |
| Object storage, per 1,000 files-month | $0.0115 (+$0.005 one-time PUT) | $0.0104 | $0.010 |
| The same bytes in HA PostgreSQL, per GB-month | $0.23 (inferred) | ~$0.23 (inferred, HA doubled) | ~$0.34 (inferred) |
| Plain OCR, per 1,000 pages | $1.50 | $1.50 | $1.50 (inferred) |
| Prebuilt check or bank statement, per 1,000 pages | n/a (Queries $15) | $10 | not verified |
| Per 1,000 documents (2 pages) with OCR plus structured extraction | Textract Queries ≈ **$30** | prebuilt ≈ **$20** | Custom Extractor ≈ **$60** (inferred) |
| Claude extraction, per 1,000 pages (in-cloud partner pricing may differ) | Bedrock (verify), ≈ $0.50 Haiku 5.5 / $10 Sonnet 5.5 at first-party rates | Foundry at first-party rates: ≈ $0.50 / $10 | Vertex (verify) |

**Conclusion:** scanning and storage cost fractions of a cent per file. AI extraction is the only material per-document cost ($0.02–$0.06 per document), and engineering time will dominate all of these.

---

## 6. Open items and verification needed
- Cloud SQL storage and backup prices, and Document AI specialized processors: the pages did not render.
- RDS gp3 and backup prices come from secondary sources.
- Bedrock and Vertex Claude per-token prices; Claude 5.5-series availability on each platform.
- ClamAV 1.4 default limits; a primary source for the Splunk detection study.
- Whether Defender's "Standard Transactions" meter applies under the per-account plan.
- ImageSharp v3 licensing (split license) for a commercial SaaS. If it does not fit, use SkiaSharp, sandboxed.
- Legal review of the GPLv2 position if container images containing ClamAV are distributed.
