# DAF vendor DNS and CNAME reconnaissance: Ren, Stellar and competitors
**Date:** 2026-11-11
**Status:** Initial passive public-hostname inventory and repeatable verification plan. **Live DNS lookup unavailable** in research runtime; **zero current CNAME records independently verified**. Do not report hostnames as CNAME targets without an actual resolver response.

## Why this investigation matters
Branded portals may expose technical supplier relationships not disclosed in Form 990, 10-K or vendor marketing. DNS aliases are clues, not contracts. A CNAME can identify an application hosting provider, CDN or managed SaaS endpoint, but cannot by itself establish legal administrator, authoritative ledger, service scope, payer, fees, current customer status or code ownership. A direct A/AAAA, proxy or CDN can hide vendor hosting; no CNAME does not disprove a relationship.

## Evidence-bearing hostnames already identified
| Host | Public observation | Interpretation | CNAME verified? |
|---|---|---|---|
| npt.stellartechsol.com | NPT-branded 2020 forms and account guide served on Stellar domain | Historical NPT–Stellar infrastructure relationship | No |
| bofa.donorfirst.org | BofA-branded donor login and reninc.com support contact | Ren-related portal operation/support | No |
| tda.donorfirstx.com | Terms name Renaissance Acquisition Company LLC | DonorFirstX/Ren product association | No |
| demo.stellartechsol.com | Public simulated iPhi product demonstration | Stellar/iPhi platform host | No |
| nptdaf.org | Referenced in NPT contribution documents | NPT account-access entry point; current DNS unknown | No |
| reninc.com | Official Ren site | Vendor corporate domain | No |
| donorfirst.org | Portal domain family | Supplier attribution requires further corroboration | No |
| donorfirstx.com | Portal domain family | Supplier attribution requires further corroboration | No |
| stellartechsol.com | Stellar legacy domain | Acquired by Ren in 2023 | No |

## Expanded competitor domain targets (candidate lookup names, not verified portal deployments)
- NPT: nptrust.org, nptdaf.org
- Ren: reninc.com, donorfirst.org, donorfirstx.com, stellartechsol.com
- Fidelity Charitable: fidelitycharitable.org
- DAFgiving360: dafgiving360.org
- National Christian Foundation: ncfgiving.com
- American Endowment Foundation: aefonline.org
- TIFIN Give: tifin.com
- Chariot: givechariot.com
- Charityvest: charityvest.org
- Foundation Source: foundationsource.com
- BofA, Morgan Stanley, Goldman Sachs: investigate program-specific portals through **public documentation first**; do not guess subdomains or treat parent bank DNS as the DAF stack.

## Repeatable public-DNS workflow
1. Build **documented hostname** candidates from public program portals, linked login buttons, help guides, publicly indexed PDFs, archived site links, certificate-transparency records and vendor case studies. Do not brute-force random customer subdomains.
2. For each exact hostname, query CNAME, A, AAAA, NS, HTTPS/SVCB from two public resolvers, record UTC time, TTL, resolver and full alias chain. For apex domains, absence of a CNAME is normal.
3. Save raw JSON DNS answers and response codes. Distinguish NOERROR/NODATA, NXDOMAIN, SERVFAIL, timeout and alias flattening.
4. Compare CNAME target with Ren/Stellar/DonorFirstX/iPhi, TIFIN, Chariot, Foundation Source, cloud hosting and CDN domains. A CDN alone is not a vendor fingerprint.
5. Independently corroborate via official program documentation, copyright/legal terms, vendor disclosures, current product branding or an authorized supplier confirmation.
6. Grade edges: A = explicit signed/current official supplier attribution; B = official operational disclosure or directly hosted branded portal; C = live DNS alias plus independent corroboration; D = historical document/weak technical association; U = unverified. Do not equate grade with probabilistic certainty.
7. Record historical start/end and acquisition lineage separately. A 2020 Stellar hostname plus 2023 Ren acquisition does not prove an active 2026 Ren contract.
8. Report negative results only as 'no CNAME returned at the observed time by named resolver,' not 'vendor not used.'

## Example repeatable commands (to run in a DNS-enabled environment)
```bash
for host in npt.stellartechsol.com bofa.donorfirst.org tda.donorfirstx.com nptdaf.org; do
  echo "### $host"
  dig @1.1.1.1 +noall +answer "$host" CNAME
  dig @8.8.8.8 +noall +answer "$host" CNAME
  dig @1.1.1.1 +noall +answer "$host" A
done
```
For machine-readable capture use public DNS-over-HTTPS resolvers, preserving the full JSON response and timestamp:
`https://cloudflare-dns.com/dns-query?name=HOST&type=CNAME` with Accept: application/dns-json, or `https://dns.google/resolve?name=HOST&type=CNAME`.

## Proposed output data model
`observation_id,observed_at_utc,hostname,record_type,resolver,rcode,answer_name,answer_value,ttl,cname_chain,source_url,brand,legal_sponsor,vendor_candidate,relationship_kind,independent_corroboration,confidence_grade,valid_from,valid_to,limitations`

## Clarity/EDF interpretation
- **Observation:** Hostname serves a branded document or portal; live DNS answer, when captured, points to a named target.
- **Inference:** The host may be operated or provisioned through that technology supplier.
- **Alternative explanations:** CDN, shared hosting, inherited/retired configuration, white-label reseller, reverse proxy, one-time document hosting, subprocessor rather than administrator.
- **Reconsideration:** New DNS answers, authoritative current supplier disclosures, platform migration evidence.
- **EDF control question:** Does the portal boundary lead to the authoritative fund ledger, or is it merely a view/entry interface? Verify separately.
- **Publication guardrail:** Never infer security vulnerability or customer ownership from public DNS alone.

## Prioritized execution
P0: Collect live DNS responses for the four evidence-bearing hostnames and document NPT/BofA portal chain.
P0: Collect current portal URLs for Morgan Stanley GIFT and Goldman Sachs PWM from official documents.
P1: Build certificate-transparency and archived-hostname dataset for Ren/Stellar/DonorFirst families.
P1: Repeat for Foundation Source, TIFIN Give, Chariot, NPT and Charityvest.
P1: Compare legacy Stellar customer domains with post-acquisition Ren-branded product endpoints; test active versus historical status.
P2: Produce dated vendor–sponsor network with separately evidenced legal, financial and technology relationships.

## Sources
- https://npt.stellartechsol.com/npt/LinkClick.aspx?fileticket=zR5mZ1T9vfE%3D&mid=2534&tabid=656
- https://bofa.donorfirst.org/
- https://tda.donorfirstx.com/Terms%20of%20Service.pdf
- https://demo.stellartechsol.com/iphidemo/
- https://www.reninc.com/blog/ren-bolsters-philanthropic-tech-services-offerings-with-acquisition-of-stellar-technology-solutions/
- https://www.recorddns.com/tools/dns-lookup/
- https://nslookup.online/cname-lookup/

**Explicit limitation:** This document records no verified live DNS records. All candidate CNAME associations remain open until raw DNS responses are captured.
