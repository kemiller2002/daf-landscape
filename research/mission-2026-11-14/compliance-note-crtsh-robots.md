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

## Correction (2026-11-15, after validation wave 23) — governing
The mention counts in the table above all read 0 because of a counting bug. Corrected counts (including the compliance footer each document now carries):

| Document | crt.sh mentions |
|---|---|
| [direction-patents-security.md](direction-patents-security.md) | 1 |
| [queue-batch30-cf-coverage-give.md](queue-batch30-cf-coverage-give.md) | 8 |
| [queue-batch32-feeds-owners-codebases.md](queue-batch32-feeds-owners-codebases.md) | 15 |
| [queue-batch38-vendors-ledgers-portals.md](queue-batch38-vendors-ledgers-portals.md) | 7 |
| [queue-bdc-coverage-migrations-goodstack.md](queue-bdc-coverage-migrations-goodstack.md) | 5 |
| [queue-cf-vendor-map.md](queue-cf-vendor-map.md) | 6 |
| [queue-community-foundation-rails-portals.md](queue-community-foundation-rails-portals.md) | 8 |
| [queue-donor-export-cf-payments-donorsphere.md](queue-donor-export-cf-payments-donorsphere.md) | 7 |
| [queue-fidelity-chariot-goodstack-vanguard.md](queue-fidelity-chariot-goodstack-vanguard.md) | 4 |
| [queue-give-interactive-displacement.md](queue-give-interactive-displacement.md) | 18 |
| [queue-ledgers-behind-portals.md](queue-ledgers-behind-portals.md) | 10 |
| [queue-npt-givingpoint-fidelity-stack.md](queue-npt-givingpoint-fidelity-stack.md) | 9 |
| [queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md) | 6 |
| [queue-vendor-channel-moves.md](queue-vendor-channel-moves.md) | 19 |
| [queue-watchlist-and-vendor-moves.md](queue-watchlist-and-vendor-moves.md) | 14 |

**Scripts disabled.** crt.sh calls are now refused in `scripts/mission_watchlist.py` (`ct_crtsh` returns status `disabled`), `collect_daf_dns.py` (`--ct` exits), `mission_cf_vendor_map.py` (`ct_tenants` returns empty), `mission_ren_iphi_attrition.py` (falls back to certspotter) and `mission_cf_migrations_goodstack.py` (crt.sh URLs skipped). The 10 `ct_crtsh` rows in `data/mission-2026-11-14/watchlist.csv` are marked disabled. `mission_give_tenant_lapses.py` only reads a saved export and makes no request.

## Validation corrections (wave 23, 2026-11-15) — governing
Source: [validation-wave23-report.md](validation-wave23-report.md); register `data/mission-2026-11-14/validation-register-wave23.csv`.

1. **Affected-documents table (governing replacement of the count column).** Replace the 0 in each row with the case-insensitive counts of "crt.sh":
   - queue-batch30-cf-coverage-give.md 8;
   - queue-batch32-feeds-owners-codebases.md 15;
   - queue-batch38-vendors-ledgers-portals.md 7;
   - queue-bdc-coverage-migrations-goodstack.md 5;
   - queue-cf-vendor-map.md 6;
   - queue-community-foundation-rails-portals.md 8;
   - queue-donor-export-cf-payments-donorsphere.md 7;
   - queue-fidelity-chariot-goodstack-vanguard.md 4;
   - queue-give-interactive-displacement.md 18;
   - queue-ledgers-behind-portals.md 10;
   - queue-npt-givingpoint-fidelity-stack.md 9;
   - queue-ren-iphi-attrition.md 6;
   - queue-vendor-channel-moves.md 19;
   - queue-watchlist-and-vendor-moves.md 14.

   These are the counts as of 2026-11-15, before any compliance footer is appended [V wave 23].
2. **After "Validation reports that mention crt.sh are not listed; they inherit this note."**
   - **Find:** "Validation reports that mention crt.sh are not listed; they inherit this note."
   - **Replace with:** "Validation reports that mention crt.sh are not listed; they inherit this note. Also affected, outside this folder [V wave 23]:\n- `research/iphi-175-client-lead-and-dns-execution-2026-11-11.md` (1 mention).\n- `data/watchlist-snapshots/reports/2026-11-14.md` (10) and the CT snapshots `data/watchlist-snapshots/2026-11-14/ct-*.json`.\n- Scripts that still call crt.sh: `mission_watchlist.py` (`ct_crtsh`), `collect_daf_dns.py`, `mission_cf_vendor_map.py`, `mission_ren_iphi_attrition.py`, `mission_cf_migrations_goodstack.py` and `mission_give_tenant_lapses.py`.\n- `data/mission-2026-11-14/watchlist.csv` still holds 11 `ct_crtsh` checks. Disable them before the next watchlist run, or decision 1 is breached.\n\nCT-derived Give Interactive hostnames that resolve in public DNS (no wildcard; checked 2026-11-15 for cct, jcf-staging, thriventcharitable-staging, stifelcharitable-staging and minneapolisfoundation-staging) stand on DNS for their existence. Their certificate dates and environment stage remain unverified leads. The `robots.txt` content itself was not re-fetched in wave 23."

## Addition (2026-11-19): certspotter — governing
api.certspotter.com serves no robots.txt (404), but its operator SSLMate's robots.txt at sslmate.com disallows `/api` and `/crt` for all crawlers (re-checked 2026-11-19). Following the operator's evident intent, certspotter is treated like crt.sh from this date: no further queries, the watchlist `ct_certspotter` check returns `disabled`, and `mission_ren_iphi_attrition.py` no longer falls back to it. Claims that rest **only** on certspotter results — including the 2026-11-19 monitoring sweep's two new Give Interactive hostnames (thriventcharitable-sandbox2, vanguard-dr-sftp.int) and any batch-23 "certspotter-only" names — are unverified leads unless confirmed by DNS, first-party pages or filings. Re-sourcing of crt.sh-only claims is in [crtsh-resourcing-2026-11-19.md](crtsh-resourcing-2026-11-19.md): of 70 claims, 20 re-sourced, 29 existence-only via DNS, 18 unverified leads, 3 method notes.
