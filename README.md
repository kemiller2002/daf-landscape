# DAF Landscape

Independent, evidence-led research on the U.S. donor-advised fund (DAF) ecosystem, technology, platform capabilities, and third-party assurance.

**Research cut-off:** 2026-11-11. **Status:** baseline public-source assessment, not an audit, penetration test, product evaluation, or investment recommendation.

## Start here

1. [SOC 2 assurance assessment](research/soc2-assessment-2026-11-11.md) — vendor assertions, missing evidence, and security diligence.
2. [DAF technology capability assessment](research/capabilities-2026-11-11.md) — what the relevant platforms and sponsors publicly offer.
3. [Technology and control workflow](research/technology-control-map.md) — systems, decision authority, and operational risk boundaries.
4. [Assurance methodology](docs/methodology.md) — evidence grading, limitations, and verification standards.
5. Machine-readable registers: [assurance](data/assurance.csv), [capabilities](data/capabilities.csv), and [sources](data/sources.csv).
6. [Next diligence steps](research/next-steps.md).

## Essential distinctions

- A **DAF sponsor** is the charitable organization with legal responsibility for DAF assets and grants. Its donor portal may be proprietary or outsourced.
- A **platform administrator** operates software and/or administrative services for institutions and sponsors.
- **Connectivity/payment infrastructure** may initiate, authenticate, track, or disburse grants but does not thereby become the sponsoring charity.
- A **SOC 2 Type II vendor statement** is **not** an auditor report. We have not obtained or examined any vendor's SOC 2 report in this baseline.
- An organization that uses a vendor with a SOC report is **not automatically itself covered**. Exact audited systems, time periods, auditor opinion, exceptions, subservice organizations and complementary user entity controls must be checked.

## Initial findings

- **Ren at reninc.com:** April 8, 2026 sponsor-hosted announcement states SOC 2 **Type I**. Do not conflate with the unrelated tryren.com company, which advertises Type II. No current Ren Type II audit report reviewed. [Source](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/).
- **Chariot:** its official security page states SOC 2 **Type II**, with report materials available on request; no report reviewed. [Source](https://help.givechariot.com/onboarding/trust-and-safety/security).
- **TIFIN Give:** its official 2024 announcement asserts SOC 2 security compliance without specifying type or report dates; no report reviewed. [Source](https://tifin.com/news/tifin-give-expands-its-reach-as-a-leading-technology-powered-philanthropy-platform-for-wealth-enterprises-2/).
- **AEF:** AEF states its DAF platform is powered by Ren; this establishes a technology relationship, not audit coverage of AEF. [Source](https://engage.aefonline.org/dc-sunset/).
- **Other sponsors:** no applicable public SOC 2 report was located within this scoped review. This is an evidence gap, **not** a finding of noncompliance.

## Research boundaries

Use only public information or material separately authorized for disclosure. Do **not** store private expert-network invitations, client identities, screening questions, third-party proprietary information, private audit reports, credentials, or former-employer confidential knowledge here. Public research conclusions must be traceable to an accessible dated source. Record disagreements and uncertainty rather than resolve them through speculation.

## Roadmap

- Obtain permissible current report metadata and permissioned reports for Ren, TIFIN Give, and Chariot; verify audit period, report scope, opinion, exceptions, subservice carve-outs and CUECs.
- Assess direct sponsor technology versus outsourced stack; map API, ledger, payments, identity, grantee verification, and reconciliation owners.
- Confirm competitive selection criteria through documented RFPs, public product demonstrations, program requirements, and authorized interviews.
- Build evidence-backed cost/operational comparisons; avoid unsupported vendor rankings.
