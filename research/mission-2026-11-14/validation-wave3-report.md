# Validation wave 3: Ren, NPT, Goldman, Give Interactive

**Date:** 2026-11-14. **Validator:** independent-validation-agent-wave3. **Register:** [`data/mission-2026-11-14/validation-register-wave3.csv`](../../data/mission-2026-11-14/validation-register-wave3.csv) (V3-01 to V3-10).

**Method.** Each claim was re-derived from primary sources before the queue document (`queue-vendor-scope-ren-denominator.md`) and the edges file (`relationship-graph-edges-additions.csv`) were opened. The sources were:
- Live HTTP fetches with `curl` (headers, HTML, the Angular bundles and the `/api/apistatus/version` endpoint).
- DNS resolution with Python `socket`.
- Certificate transparency through crt.sh JSON. crt.sh covers the full history; certspotter shows only currently valid certificates.
- IRS e-file 990 XML, read by object_id from the GivingTuesday 990 data lake mirror and cross-referenced to ProPublica filing pages. ProPublica's own XML download is behind a bot check.

No authenticated pages were accessed.

## Verdicts

| ID | Claim | Result | Key point |
|---|---|---|---|
| V3-01 | GS PWM login is iPhi/Stellar on Ren infrastructure | **confirmed** | Evidence: an `.iPhiSession_gspf` cookie, a Stellar footer, and a CNAME to `ren-workload-02` ELB, which shares IPs with NPT GivingPoint. **New:** the TY2022 990 names Stellar as "software provider" at $390,398. |
| V3-02 | GS PWM 990 shows Ayco $1.03m, GS & Co $8.08m, Sapient $0.82m | **partially confirmed** | The amounts are exact. Sapient is **not** a Goldman affiliate. The largest payee is omitted: GS Trust Co at $14.60m. No Ren line appears in CY2023 or CY2024. |
| V3-03 | GS Gives pays Stellar ~$173k | **confirmed** | $172,604 for FYE 6/2025. Earlier years: $139,000 (FY2024) and $150,924 (FY2023). |
| V3-04 | MS GIFT pays RenPSG $14.93m | **confirmed** | $14,930,249 for "admin & legal". The return also uses C/O RenPSG addresses. |
| V3-05 | NPT GivingPoint is on Ren infrastructure, plus an "NPT iPhi Statuspage" | **confirmed (technology)** | The `npt.iphiview.com` login 301-redirects to `nptgivingpoint.org`. `nptgivingpoint.org` runs on the `ren-workload-02` ELB. The bundle links to `renpsg.atlassian.net`. `iphistatus.reninc.com` is the private Atlassian Statuspage titled "NPT iPhi Statuspage". **No Ren payee appears in NPT's 990 top-5** (the cap is <$221k in FY2025). |
| V3-06 | Ren-evidenced sponsors ≈ $91.0bn ≈ 27.8% | **partially confirmed** | The arithmetic reproduces ($91.02bn = 27.76%). It **omits T. Rowe Price** (REN PSG technology payments in three 990s, $0.60bn), which brings the total to **$91.62bn (27.9%)**. About 69% of the numerator rests on portal or DNS observation alone. |
| V3-07 | Give is Vanguard's recordkeeper; production tenant since ~Aug 2026; login still on Vanguard | **partially confirmed** | The release is confirmed. **The dating is wrong.** `vanguardcharitable.giveinteractive.com` has had certificates since **2026-01-28**, and `vanguard-sandbox` since **2025-08-06**, which is before the announcement. The login is still on `vanguardcharitable.org` (Akamai). |
| V3-08 | Give tenants: Signatry and WaterStone confirmed, others inferred | **partially confirmed** | The identities hold. CCT has had Give hosts since Aug 2024 and a production host since Jun 2025, not "2026-09". Lapsed tenants (FFTC, OCF, Omaha, EBCF, KZCF) show churn. |
| V3-09 | 990s name Ren/Stellar at Stifel, Thrivent, Cleveland, WaterStone, ImpactAssets | **confirmed** | Stifel: $498k / $801k. Thrivent: $270k (Stellar, CY2024) / $479k (Renaissance Acquisition, CY2025). Cleveland: $416k. WaterStone: $295k / $366k. ImpactAssets: $232k. |
| V3-10 | (Validator finding) Give Interactive ownership is unknown | **contradicted** | The Signatry Charitable Trust's CY2024 Schedule R lists **Give Interactive LLC** (EIN 84-4835291) as a related partnership. The Signatry is the direct controlling entity and the general/managing partner, with OwnershipPct 0.99. |

## Discrepancies with the queue document and edges file

1. **T. Rowe Price Program for Charitable Giving was omitted.** It is EIN 31-1709466, with $0.597bn of DAFRC FY2024 assets. Its 990s pay "REN PSG" for "technology": $301,117 (FYE 3/2024), $259,797 (FYE 3/2025) and $271,721 (FYE 3/2026). This is payee-level evidence, stronger than several sponsors that are included.
2. **The Vanguard and CCT tenant dates are too late.** Certspotter shows only currently valid certificates; crt.sh shows first issuance:

   | Host | First certificate |
   |---|---|
   | `vanguard-sandbox` | 2025-08-06 |
   | `vanguardcharitable` (production name) | 2026-01-28 |
   | `cct-sandbox` | 2024-08-12 |
   | `cct` | 2025-06-11 |
   | `impactassets-staging` | 2025-04-29 |

   Read Vanguard as "implementation since mid-2025; production environment provisioned by January 2026; cut-over not observed".
3. **GS PWM labelling and value.**
   - Sapient Corporation is an unrelated technology contractor, not a Goldman affiliate.
   - The DAFRC FY2024 row ($11.84bn) differs from the program's own CY2024 Schedule D figure ($12.64bn). The queue document uses both in different places.
   - Stellar appears on the TY2022 990 ($390,398, "software provider") and then disappears. In the same years, the GS & Co line becomes "tech & inv adv fees". That pattern is consistent with Ren being paid through GS & Co, but it is not proven.
4. **Earlier-year Ren lines are missing.** The queue cites only CY2025 for Thrivent and FYE 3/2025 for WaterStone. Thrivent also paid Stellar $270,307 in CY2024, and WaterStone paid Stellar $295,428 in FYE 3/2024. Neither changes the verdicts.
5. **Give Interactive ownership was missed.** The repo lists Give's "funding/ownership" as open. The Signatry's Schedule R answers it, subject to confirming the ownership percentage. This makes Vanguard's recordkeeper an affiliate of a competing faith-based DAF sponsor, which matters for the synthesis's data-rights and conflict points.
6. **Minor.** The GS footer year "2026" is a server-rendered date control; the static meta copyright reads 2001–2010. The `auth-npt-*.stellartechsol.com` certificates were not re-checked because crt.sh timed out.

## Interpretation challenges

- **Shared hosting is not administration.** NPT and GS PWM evidence shows Ren *builds and hosts the donor portal*. It does not show that Ren is book of record, fund accountant or administrator. NPT's 990 has no Ren line among the top five in either year (the fifth-highest payees received $345,954 in FY2024 and $220,927 in FY2025). That is implausibly small for a sole recordkeeper of a $42–56bn program, unless Ren is paid as a licence expense outside Part VII-B or paid by someone else.
- **A load-balancer name is weak alone.** The `ren-workload-02` name is chosen by the operator. Here it is corroborated by iPhi session cookies, DotNetNuke iPhi URL patterns, Stellar footers, Ren Jira links in the build and a Ren-domain status page. Treat the technology attribution as strong and any statement about contracts as unknown.
- **A certificate or tenant is not a customer.** Five Give tenants lapsed. Slugs such as `cct`, `jcf`, `nhf` and `jttw` are labels the vendor chose. Only The Signatry and WaterStone link to Give from their own sites.
- **Payee lines vary by kind.** Ren lines of $0.2–0.8m at Stifel, Thrivent, Cleveland, ImpactAssets, WaterStone, T. Rowe and GS Gives are software, hosting or licence fees. Only RCF ($19.2m) and MS GIFT ($14.9m, "admin & legal") look like outsourced administration.

## Ren share by evidence tier (DAFRC FY2024, denominator $327.87bn)

| Tier | Sponsors | $bn | Cumulative share |
|---|---|---|---|
| Administration (Ren paid for admin) | RCF, MS GIFT | 15.06 | 4.6% |
| + 990 names a Ren entity as payee (any service) | + ImpactAssets, T. Rowe, Thrivent, WaterStone/CCF, GS Gives, Stifel, Cleveland | 21.92 | 6.7% |
| + first-party platform statement | + AEF | 31.40 | 9.6% |
| + portal/DNS observation | + NPT, GS PWM, BofA | 90.47 | 27.6% |
| + iPhi community-foundation long tail | + Minneapolis, Arkansas, Gulf Coast, Stanislaus, Marion | 91.62 | 27.9% |

NPT alone is 46% of the top-line numerator. About $6.5bn of the numerator (ImpactAssets, Minneapolis, Thrivent, Stifel, WaterStone) shows Give Interactive implementation. WaterStone's live login is already on Give.

## Recommended wording for the synthesis

**Ren share.**
> "On public evidence, sponsors holding about 28% of FY2024 DAF assets ($91.6bn of $327.9bn, DAFRC) use Ren technology in some form. Only about 7% ($21.9bn) rests on Form 990 payments to a Ren entity, and only about 5% (RCF and Morgan Stanley GIFT, $15.1bn) on Ren-paid administration. Nearly half of the 28% is a single sponsor, NPT, evidenced by hosting rather than by a disclosed contract. Ren's '60%+' and 'about half' claims are not reachable without Fidelity Charitable, DAFgiving360 or Vanguard Charitable. None of those shows a Ren vendor, and Vanguard has chosen Give Interactive."

**NPT.**
> "NPT's GivingPoint donor portal is built and hosted by Ren. The evidence is: an iPhi-domain login redirect; hosting on the same Ren-named AWS load balancer as Goldman's iPhi site; Ren Jira references in the production bundle; and a Ren-hosted 'NPT iPhi Statuspage'. Neither NPT nor Ren has said so publicly. NPT's FY2024–FY2025 Form 990s list no Ren entity among the top contractors. Whether Ren also performs NPT's recordkeeping or administration is unknown."

**Goldman.**
> "Goldman runs two DAF programs. Both use Ren/Stellar software, and both are administered outside Ren. The $12.6bn PWM fund's donor site is Ren's iPhi. Its Form 990 named Stellar as software provider in 2022. In 2023–2024 it pays Goldman entities (GS Trust Co $14.6m; GS & Co $8.1m for 'tech & inv adv fees'; Ayco $1.0m for admin services) and an outside technology firm (Sapient, $0.8m). The $0.6bn GS Gives employee fund pays Stellar about $173k a year for IT and CAF America for grant administration. Count Goldman in Ren's software footprint, not its administration footprint."

**Give Interactive (add).**
> "Vanguard Charitable selected Give Interactive for recordkeeping (Nov 2025). A Vanguard sandbox existed by Aug 2025 and a production-named environment by Jan 2026, but donors still log in on Vanguard's domain. Per The Signatry's 2024 Form 990 Schedule R, Give Interactive LLC is a related partnership controlled by The Signatry Charitable Trust, so a DAF sponsor controls the vendor that keeps another sponsor's records."
