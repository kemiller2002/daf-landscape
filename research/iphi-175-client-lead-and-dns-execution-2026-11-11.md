# iPhi client-count lead and DNS execution

Date: 2026-11-11. Status: preliminary, no live DNS response obtained.

The estimate of approximately **175 iPhi clients** is a user-provided investigative lead, not a verified current active-customer count. Determine whether the number means organizations, contracts, licenses, or historical deployments, and the as-of date. The 2023 Ren acquisition of Stellar inherited an existing client base, but the acquired roster and current retention have not been independently verified.

## Implementation

- [DNS/CT collector](../scripts/collect_daf_dns.py): queries Google and Cloudflare DNS-over-HTTPS for CNAME, A, AAAA, NS, and HTTPS, and optionally crt.sh for Ren/Stellar/DonorFirst domain families. Records timestamp, resolver, TTL, responses and errors.
- [GitHub Actions workflow](../.github/workflows/daf-public-dns.yml): manual execution and weekly schedule; stores CSV and run summary as 90-day artifacts. No unreviewed DNS records are committed.
- This environment could not resolve DNS endpoints. The workflow was committed, but no successful live run is claimed.

## Attribution rules

CNAME aliases may indicate vendor infrastructure but do not establish legal supplier, fee payer, authoritative ledger, active contract, or application ownership. CT records may be historical or expired. A missing CNAME does not disprove a vendor relationship.

## Cohort audit

Separate historical Stellar customers, current confirmed iPhi deployments, Ren administration clients, and portal-support relationships. NPT has historical Stellar-hosted material; Morgan Stanley GIFT names RenPSG as administrator; BofA exposes a Ren-linked portal support contact. None independently proves a current iPhi installation.

## Next actions

1. Run the GitHub Actions collector and review the artifact for errors.
2. Correlate actual observed DNS/CT hostnames with documented public portals and sponsor names.
3. Find the original source and date of the approximately 175-client estimate.
4. Build a dated inherited Stellar customer cohort and check current retention individually.
5. Avoid describing 175 as confirmed current Ren customers without independent evidence.
