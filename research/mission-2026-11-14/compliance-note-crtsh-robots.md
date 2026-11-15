# Compliance note: crt.sh robots.txt (2026-11-15)

**Finding.** `https://crt.sh/robots.txt` reads `User-agent: *` / `Disallow: /` (re-checked 2026-11-15). Earlier batches queried crt.sh, the public Certificate Transparency search, by script to find vendor tenant hostnames. Those queries did not comply with crt.sh's robots.txt. Batch 38A sent four more queries before checking; it discarded their results.

**Decision (governing from this date).**
1. No further crt.sh queries by any agent in this repository.
2. Claims that rest **only** on crt.sh certificate data are downgraded to *unverified-lead* status. They must not be used for scoring or headline counts until re-sourced from an admissible route: a live first-party page or portal footer whose robots.txt permits access, public DNS resolution (not a crawl), vendor or sponsor publications, or filings.
3. Claims corroborated by another admissible source stand on that source.
4. Historical text is preserved (no deletion). This note governs how it is read.

**Affected documents** (contain crt.sh references; count of mentions):

| Document | crt.sh mentions |
|---|---|
| [queue-batch30-cf-coverage-give.md](queue-batch30-cf-coverage-give.md) | 0 |
| [queue-batch32-feeds-owners-codebases.md](queue-batch32-feeds-owners-codebases.md) | 0 |
| [queue-batch38-vendors-ledgers-portals.md](queue-batch38-vendors-ledgers-portals.md) | 0 |
| [queue-bdc-coverage-migrations-goodstack.md](queue-bdc-coverage-migrations-goodstack.md) | 0 |
| [queue-cf-vendor-map.md](queue-cf-vendor-map.md) | 0 |
| [queue-community-foundation-rails-portals.md](queue-community-foundation-rails-portals.md) | 0 |
| [queue-donor-export-cf-payments-donorsphere.md](queue-donor-export-cf-payments-donorsphere.md) | 0 |
| [queue-fidelity-chariot-goodstack-vanguard.md](queue-fidelity-chariot-goodstack-vanguard.md) | 0 |
| [queue-give-interactive-displacement.md](queue-give-interactive-displacement.md) | 0 |
| [queue-ledgers-behind-portals.md](queue-ledgers-behind-portals.md) | 0 |
| [queue-npt-givingpoint-fidelity-stack.md](queue-npt-givingpoint-fidelity-stack.md) | 0 |
| [queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md) | 0 |
| [queue-vendor-channel-moves.md](queue-vendor-channel-moves.md) | 0 |
| [queue-watchlist-and-vendor-moves.md](queue-watchlist-and-vendor-moves.md) | 0 |

Validation reports that mention crt.sh are not listed; they inherit this note.

**Follow-up.** Queue item P-CMP-CRT-01 asks for each affected claim to be re-sourced or marked unverified-lead.
