# Validation wave 11: Ren iPhi attrition, net payout, Fidelity outliers, adviser fees, NPact, DAFgiving360 pools

**Validator:** independent-validation-agent-wave11
**Date:** 2026-11-15
**Register:** [`data/mission-2026-11-14/validation-register-wave11.csv`](../../data/mission-2026-11-14/validation-register-wave11.csv), 24 rows

**Rules followed:**
- I used public sources only. I made no logins, form submissions or outreach, and used no credentials.
- I formed each verdict from primary sources first. Only then did I read the three queue documents and compare.
- The queue documents are `queue-ren-iphi-attrition.md`, `queue-net-payout-fidelity-outliers.md` and `queue-adviser-fees-pools-npact.md`.
- I wrote no git commits.

**Scratch outputs:** the reruns wrote to the session scratchpad, so no repo data file was overwritten.

**Access limits:**
- `dafgiving360.org` returns 403.
- `web.archive.org` resets the connection.
- `broadwestpartners.com` gives a proxy 502.
- `reninc.com` returns 403 to curl but is readable through WebFetch.
- `donoradvisedfund.ubs.com` resets the connection.

## Summary of verdicts

| Claim | Verdict | Confidence |
|---|---|---|
| V11-01 Ren iPhi attrition: 6/57 (10.5%), with the six named exits | **Confirmed.** A live rerun reproduces the result exactly, and 8 live spot checks agree (all 6 exits plus CGF active and the ImpactAssets path lapsed) | medium-high |
| V11-02 NPT, J.P. Morgan and ICGF hosts redirect to Ren-hosted GivingPoint sites naming NPT | **Confirmed** | high |
| V11-03 Truist is F&E ClientView; UBS redirects to an NPT program; PNC `/scbf` returns 404 | **Confirmed.** The UBS target does not load, so its NPT sponsorship is inferred | medium-high |
| V11-04 Ren "$48K granted per second" (about $1.5tn a year) | **Confirmed.** Ren's own about page says $35B a year, which suggests a units error | high |
| V11-05 Net payout: 23.9 / 21.5 / 20.8 / 19.0%; nationals 23.8 → 20.9%; 12.1% | **Confirmed by exact reproduction.** One sample-size label is wrong (see corrections) | high |
| V11-06 Fidelity FY2025 Schedule I lines; the $727m outlier text | **Confirmed** | high |
| V11-07 Adviser-fee rules and minimums | **Confirmed, with two qualifiers** (CIAP minimum; NPT $2m non-discretionary) | medium-high |
| V11-08 BroadWest/NPact; Blackbaud 10-Q; Cambria | **Confirmed.** BroadWest's target was Fusion Labs, renamed NPact | medium to high |
| V11-09 DAFgiving360 changed three pool funds on 2026-09-24 | **Confirmed, but only through a search-index capture.** The live page returns 403 | medium |

## Key findings

### V11-01: Ren iPhi attrition

**No cache was shipped.** Neither `~/.cache` nor the repo holds the census cache, so "cached mode" was impossible. I copied `scripts/mission_ren_iphi_attrition.py` with only its four output paths redirected to scratch. I then ran `--task census --fetch` live, which took about 45 minutes.

**The result matches the repo exactly:**
- Population 57: 49 active, 6 migrated, 2 unknown.
- Point estimate 6/57 = 10.53%.
- Wilson 95% interval 4.91–21.12%.
- Dated-only 8.8%; including the unknowns 14.0%.
- The census CSV has the same 76 tenant rows as the repo copy, with zero status differences.

**Circularity.** Four of the six exits (Acadiana, Flint, Arkansas, Yakima) take their status from the repo's own `cf-vendor-migrations-2022-2026.csv`. I therefore checked each destination live:

| Sponsor | Live evidence | Destination |
|---|---|---|
| Acadiana | Homepage fund portal is `cfacadiana.fcsuite.com/erp/portal/fundadvisor`; `cfacadiana.iphiview.com` returns NXDOMAIN | Foundant |
| Flint | `cfgf.iphiview.com/cfgf` is still live with the banner "we are moving to a new system"; homepage links `cfgf.fcsuite.com` | Foundant |
| Arkansas | Homepage links `arcf.fcsuite.com/erp/home`; the legacy iPhi login still returns 200 | Foundant |
| Gulf Coast (Venice) | Homepage links `gulfcoastcf.fcsuite.com/erp/portal`; the iPhi page says "We're moving to a new Donor Portal experience launching soon" | Foundant (in progress) |
| Yakima | `yakimavalleycf.org` links `gofund.akoyago.com/yakimavalleycf`; a stale `yvcf.iphiview.com` link no longer resolves | akoyaGO |
| WaterStone | Legacy iPhi page: "Your Giving Fund now lives in our new WaterStone Donor Portal at waterstone.giveinteractive.com" | Give Interactive |

Two notes on these checks:
- **Acronym trap.** `yvcf.org` is the *Yampa* Valley CF, which also uses Foundant. Do not use it for Yakima.
- **Interpretation challenge.** Gulf Coast's new portal is still "launching soon", so counting it as an exit is a judgement call. The strict figure is 5/57 = 8.8%. The 57 is the set of sponsors the census could find, not Ren's client list.

### V11-02: NPT-family hosts

Each host 301-redirects to its own GivingPoint site:
- `npt.iphiview.com/npt/` → `nptgivingpoint.org`
- `jpmc.iphiview.com/jpmc/` → `jpmgiving.org`. The label is `jpmc`; `jpm` and `jpmorgan` are NXDOMAIN.
- `icgf.iphiview.com/icgf/` → `icgfdaf.org`

**Evidence that the sites are Ren-hosted:**
- The `www.` names of nptgivingpoint and jpmgiving CNAME to `ren-workload-02-public-…elb.amazonaws.com`.
- `icgfdaf.org` shares the iPhi Global Accelerator IPs (13.248.164.2 / 35.71.183.32).

**Evidence that the sites name NPT:**
- All three JS bundles say "GivingPoint is a registered trademark of National Philanthropic Trust", carry "© … National Philanthropic Trust", and link `renpsg.atlassian.net`.
- The J.P. Morgan and ICGF bundles say the fund is "offered in conjunction with (the) National Philanthropic Trust (NPT)".

### V11-03: bank hosts

- **Truist:** "Welcome to F&E ClientView". MetaAuthor is Truist Financial Corporation; the copyright meta is "2010 by Stellar Technology Solutions"; the footer says ©2021.
- **UBS:** the host 301-redirects to `donoradvisedfund.ubs.com` (67.216.67.101), which reset the connection on every attempt.
- **PNC:** the host 301-redirects to `/scbf`, which returns 404.

### V11-04: Ren "$48K per second"

The figure is live on `reninc.com/payments/` under "Ren by the Numbers": "$48K Granted to charities per second".
- At calendar-year seconds, $48K × 31.536m s = **$1.514tn a year**.
- At business hours only, it is $0.348tn.

**Contradiction on Ren's own site.** `reninc.com/about-ren/` says "$35B Granted to charities annually". That is about $1.1K per second or $66.6K per minute, so the per-second figure is most likely a mislabelled per-minute number.

### V11-05: net payout

**Reproduction.**
- I ran `scripts/mission_net_payout.py` with `--fetch` and `--out-dir` set to scratch. It parsed 7,559 returns: 6,161 ok and 19 with no 990.
- The resulting `net-payout-by-sponsor.csv` is **byte-identical** to the repo copy.
- I recomputed the pools independently from the sponsor rows.

**Recomputed pools (itemised Schedule I):**

| Sample | Sponsor-years | Gross | Net tier A | Net tier B | Net tier C | Tier-A transfer share |
|---|---|---|---|---|---|---|
| Excluding processors | 3,373 | 23.93% | 21.50% | 20.80% | 18.96% | — |
| National sponsors | 204 | 23.78% | 20.91% | — | — | 12.08% |

**Schedule I lines checked against the XML (all match):**
- SVCF FY2024 → NPT: $1,591,322,838
- Vanguard Charitable FY2024 → ImpactAssets: $308,265,198
- Fidelity FY2023 → Johns Hopkins: $831,883,460

### V11-06: Fidelity FY2025

Source: object 202601389349301700, tax period ending 2025-06-30.

| Recipient | Amount |
|---|---|
| National Philanthropic Trust | $346,816,520 |
| Johns Hopkins University | $340,345,791 (non-cash $131,374,056) |
| ImpactAssets | $203,706,502 |
| GS DAF Philanthropy Fund for Wealth Management (EIN 31-1774905) | $159,883,562 |

Two notes on these lines:
- **Not Goldman Sachs Charitable Gift Fund.** That fund (EIN 11-3813663) received only $287,548.
- **Largest line.** Vanguard Charitable received $480.1m, the largest line in the return.

**Giving Report.** The 2026 Giving Report PDF says: "Significant outlier granting totaling $727 million was removed from calculations for the average grant size on page 6 and granting by charitable sector on page 9."

### V11-07: adviser fees

**Fidelity CIAP.** The overview PDF (created 2025-04) states the "$100,000 minimum balance requirement". But that overview is the version "For firms that clear or custody with Fidelity Investments", and the advisor guide says the minimum "vary[ies] by firm".

**NPT.** The guide (2024-09) sets a $500,000 minimum for discretionary segregated accounts and **$2 million for non-discretionary** accounts. It says "A different fee schedule may apply". No cap is given.

**AEF.** TY2024 line 11f is $35,948,715. Divided by average total assets of $7.778bn, that is **0.462%**. On end-of-year assets it is 0.427%; on beginning-of-year assets, 0.503%.

**RCF.** The UBS circular says each DAF "may carry its own fees". No cap is given.

**Vanguard Charitable.** The policies page offers only an access-only "interested party" role and says "does not itself charge investment fees". There is no adviser-managed language.

**Redhawk (DAFgiving360).** Advisory fee of 0.00, 0.25, 0.50 or 0.75%, plus a 0.25% Redhawk administration fee; "administration fee plus the advisory fee cannot exceed 1.0%". A further 0.25% portfolio-management fee sits outside that cap.

### V11-08: NPact ownership

- **BroadWest.** The 2021-04-28 Trident World Ventures release, seen through search-index captures and reprinted by CB Insights, says: "On December 30, 2020 … BroadWest Partners completed its acquisition of … Fusion Labs". The company was then renamed NPact. CB Insights' own deal date is 2021-04-28.
- **Blackbaud.** The Q3 2022 10-Q says: "On September 9, 2022, we sold … FIMS … and DonorCentral NXT solutions to Fusion Laboratories, LLC for cash proceeds of approximately $6.4 million".
- **Cambria.** `cambriagroup.com/portfolio/npact` lists NPact (Dallas): "Developer of grant management and donor-advised fund management software…".

### V11-09: DAFgiving360 pools

A search-index capture of `dafgiving360.org/investment-options` says DAFgiving360 "updated three core account investment pool funds effective September 24, 2026". It names FFICX as the new fund for the Large Cap Equity Managed Pool. The other two swaps were not independently seen.

## Exact corrections

### `research/mission-2026-11-14/queue-net-payout-fidelity-outliers.md`

**§1, Q-N06 row (line 34).** The sample size quoted next to the ex-processor percentages belongs to the all-sponsor sample, which includes processors.
- Replace "Pooled FY2021–24, sponsors with itemised Schedule I (n = 3,421 sponsor-years, 1,018 sponsors, $831bn beginning DAF assets):"
- With "Pooled FY2021–24, sponsors with itemised Schedule I (all sponsors n = 3,421 sponsor-years, 1,018 sponsors, $831bn beginning DAF assets; excluding processors n = 3,373, 1,002 sponsors, $825.8bn):"

**§1, Q-N06 row, tier C.** Optionally make the rounding explicit: "19.0% (tier C)" → "19.0% (tier C; 18.96%)".

**§1, P-VCM-03 row.** Replace "GS PF $159.9m" with "GS DAF Philanthropy Fund for Wealth Management (EIN 31-1774905) $159.9m". This avoids confusion with Goldman Sachs Charitable Gift Fund (EIN 11-3813663), which received only $0.29m.

### `research/mission-2026-11-14/queue-ren-iphi-attrition.md`

**Line 283, reproducibility.** Append: "No cache directory is committed with the repo, so an independent rerun must use `--fetch`. Wave 11's live rerun on 2026-11-15 reproduced the census exactly (76 rows, 0 status differences)."

**§1 item 1, bounds.** Add: "Four of the six exits are classified from `cf-vendor-migrations-2022-2026.csv`. All four destinations were re-verified live in wave 11. Gulf Coast's new portal is still 'launching soon', so the strict dated-exit figure (5/57 = 8.8%) is the conservative headline."

**§6, $48K-per-second bullet (line 235).** Add: "Ren's own about page states '$35B Granted to charities annually' (about $1.1K per second, or about $66.6K per minute). The '$48K per second' is therefore most likely a per-minute figure mislabelled [I]."

**Line 65, Yakima row.** No change is needed. Add a caution to the method notes: "`yvcf.org` is the Yampa Valley CF, not Yakima. Yakima is at `yakimavalleycf.org`."

### `research/mission-2026-11-14/queue-adviser-fees-pools-npact.md`

**§1.1, NPT row (line 48).** The minimum applies only to discretionary accounts.
- Replace "**$500,000** (segregated account)"
- With "**$500,000** (discretionary segregated account); **$2 million** for non-discretionary adviser accounts (Guide p.27)"

**§0 NPT bullet.** Replace "adviser-managed (segregated) accounts are available only above $500,000" with "adviser-managed (segregated) accounts need $500,000 if discretionary, or $2 million if non-discretionary".

**§1.1, Fidelity CIAP row (line 44).** Add to the minimum cell: "The $100,000 figure is from the overview 'For firms that clear or custody with Fidelity Investments'. The advisor guide says the minimum balance requirement varies by firm."

**§0 headline, P-ACC-03.** Reword "No sponsor in scope caps the fee" to "No sponsor in scope publishes a numeric cap. Fidelity caps the fee relative to the firm's own standard schedule."

**§0, P-ACC-02 row.** Keep the row's [R] label. Add: "The live page returns 403. Wave 11 confirmed the 2026-09-24 date and FFICX only through a search capture. PAXIX→CBAIX and PSHIX→BSBIX were not independently seen."

### `data/mission-2026-11-14/adviser-fees-observed-2026.csv`

**Row "National Philanthropic Trust, Segregated account (adviser-proposed custom portfolio)".** In `fee_schedule`, replace "Available to DAFs over $500,000." with "Available to DAFs over $500,000 (discretionary); the minimum is $2 million for non-discretionary accounts (Guide p.27)."
