# 13 — Beneficium public-data economics

**Blocker recorded:** the `kemiller2002/beneficium` repository does not exist or is not accessible to this session (add_repo: "you don't have access"). Per the mission, no replacement repository was created; Beneficium research lives here and its cross-repository requirements are proposals ([24](24-cross-repository-implications.md)).

Registers: [`beneficium-data-sources.csv`](data/registers/beneficium-data-sources.csv) (29 sources, cross-referenced to the existing 68-source register), [`beneficium-dataset-sizing.csv`](data/registers/beneficium-dataset-sizing.csv) (38 sizing assumptions), model parameters [`beneficium-parameters.csv`](data/model-inputs/beneficium-parameters.csv). Notes and sampling log: [beneficium-public-data-notes.md](data/evidence/beneficium-public-data-notes.md).

## 1. Method: bounded, authorised sampling

About **185 MB** downloaded and deleted: BMF `eo1` (49 MB) and the Delaware state file, Publication 78, the automatic revocation list, and one 990 e-file XML zip (2025_10A, 56.5 MB). Everything else sized from HTTP headers. No unrestricted bulk download. Gaps: SAM.gov extracts need an account and API key (not obtained); USAspending not sized directly (mirrors report 145-200 GB zipped; pull matching recipients by API instead); no bulk source for determination letters (per-EIN only).

## 2. What the public data actually is

| Measure | Measured / derived | Prior assumption |
|---|---|---|
| BMF rows (eo1-eo4) | **1,984,891** | "~1.9M" |
| 501(c)(3) organisations | ≈ 1.69M | — |
| Entities in a registry that keeps revoked/removed orgs | ≈ 3.2M | — |
| Structured database (normalised current state + temporal history + extracted 990 facts) | ≈ **10 GB** year one; **17 GB** with indexes | 150 GB |
| 990 e-file XML (IRS now hosts 2019 onward) | 30.3 GB compressed online; ≈ 4.5 GB per filing year | — |
| Total retained after 10 years (raw archive + XML + DB) | ≈ **190 GB** (35 GB - 1.2 TB) | 1 TB raw |
| Update bandwidth | ≈ 3.8 GB/month (0.85-12); IRS republishes whole files | — |
| Processing | ≈ 10 CPU-hours/month | — |

## 3. How much changes

| Population | Changes per month |
|---|---|
| All 501(c)(3): any field | ≈ 237,000 organisations |
| All 501(c)(3): eligibility-relevant field | ≈ **405** |
| Additions and removals | ≈ 15,300 |
| Automatic revocations (all subsections) | ≈ 900 outside August; **38,826 in August 2026** |
| Reinstatements | ≈ 970 |
| Population data-quality exceptions (rule or human) | ≈ 650 |
| 20,000 active recipients: eligibility events | ≈ **67** |
| 20,000 active recipients: human-handled exceptions | ≈ **25** |

Change rates rest on one measured month (low confidence); the August revocation surge is a real seasonal peak that the monitoring design must absorb.

## 4. Incremental value of each source beyond BMF

| Value class | Sources |
|---|---|
| Essential | BMF extract; Publication 78; automatic revocation list; OFAC SDN and consolidated lists |
| High | 990-N; 990 e-file XML and indexes; determination letters (per EIN); 501(p) suspensions; Trade.gov Consolidated Screening List; California AG "may not operate"; group exemption fields |
| Medium | Schedule I / 990-PF grant relationships; historical BMF archives (NCCS; licence check needed); SAM.gov exclusions; Federal Audit Clearinghouse (3.35 GB, nightly); New York and other state registries; religious directories (OCD, paid); IPEDS; Census of Governments |
| Low / redundant | SAM entity registrations; USAspending; state corporate registries; CMS NPPES; fiscal-sponsor directories; charity websites; BMF state files (redundant with eo1-4); IRS SOI extract (redundant) |

All sources priced are free to acquire except religious directories (purchase/subscription, UNKNOWN) and commercial enrichment (Candid from $2,750/yr single-user; enterprise API price UNKNOWN; redistribution limits mean it must never be pooled in Beneficium).

## 5. Sources and maintenance by scenario (zero customers)

| Scenario | Connectors | Connector hours/yr (base, range) | Plus operations |
|---|---:|---:|---|
| Public directory only | 5 | 76 (44-172) | ≈ 150 h pipeline ops |
| + historical filings | 7 | 172 | |
| + grant relationship intelligence | 8 | 232 | |
| + continuous regulatory monitoring | 13 (11-20) | 296 (152-1,168) | + monitoring ops |
| + automated verification evidence | 26 (20-33) | 820 (432-2,304) | |

Material breaking format or schema changes across federal sources occur about 3 times a year (1-6). One 990 batch alone carried 8 XML schema versions.

## 6. Zero-customer cost (model)

From [`beneficium-scenarios.csv`](data/model-outputs/beneficium-scenarios.csv) (engineering at $118/h, compliance at $120/h (blend; revised after review ADV-CS-004); owner floor 100 h; counsel 20 h; shared database at 30% of a $150/month floor):

| Scenario | Annual cost, 0 recipients | FTE equivalent |
|---|---:|---:|
| Public directory only | **$57.6k** | ≈ 0.25 |
| + historical filings | $63.6k | |
| + grant relationship intelligence | $66.6k | |
| + continuous regulatory monitoring | **$93.1k** | ≈ 0.46 |
| + automated verification evidence | $131.5k | ≈ 0.7 |
| Full service (adds commercial licence and a charity support desk) | $185.0k | |

**Infrastructure is trivial (< $3k/yr).** Cost is maintenance labour: connectors, pipeline operations, quarantine review, and an accountable owner. Model connector hours use 25 h per connector-year (range 9-58); this slightly overstates the directory tier (125 h vs the measured 76 h) and understates verification (650 h vs 820 h) — within the stated ranges.

## 7. Can public charity intelligence run with no dedicated staff?

**Yes for the public directory and continuous monitoring tiers, with conditions.** 300-450 hours a year (0.2-0.3 FTE) is fractional work. It is not zero:

- three or so breaking source changes a year must be repaired within days, or the evidence goes stale and grants stop (or worse, proceed on stale data);
- the August revocation surge produces tens of thousands of status changes in one batch;
- an accountable owner must exist for source governance, disputes and appeals;
- connector work needs an engineer, not a compliance analyst.

**No for automated verification and above.** 820+ connector hours plus recipient-driven exception work (§[14](14-beneficium-verification-economics.md)) approaches or exceeds one FTE at 50k+ active recipients.

The original $316k registry estimate was driven by a 1.0 FTE steward staffing ratio and a 0.5 FTE charity support desk; neither survives the measured change rates or the principle that charities need not be software users. The original $90-170k minimum is close to the measured zero-customer upkeep plus recipient work at 20k recipients.

## 8. Function ownership (proposed)

| Function | Owner |
|---|---|
| Public acquisition, normalisation, schema-drift handling, history retention | **Beneficium** |
| Identity resolution | Beneficium proposes; **Unbound** confirms merges that move money |
| Regulatory monitoring | Beneficium emits events; Unbound fans out to affected grants |
| Verification at approval and release | **Unbound** using Beneficium evidence |
| Sponsor eligibility decisions and overlays | **Sponsor** (configured in Unbound) |
| Human investigations | Unbound operations under sponsor policy; sponsor decides |
| Charity representative verification | Unbound (Transitus if it hosts charity identity) |
| Payment enrolment; bank ownership verification | **Transitus** / payment provider |
| Fraud investigation | Unbound with payment provider |
| Commercial data | Sponsor or Unbound licence per use; **never pooled** |
| Support | Unbound front line; Beneficium answers source questions |
