import json
S = []
def sec(t, md): S.append(dict(section=t, markdown=md.strip()))

sec("PRC: Market pricing for DAF administration - summary", """
**Question.** Is 20 bps a year on average billable AUA a credible, competitive price for outsourced, staffed DAF administration? The sponsor keeps legal ownership and reserved decisions. The price excludes custody and investment management.

**Short answer (conditional).** Yes, for programs whose asset-weighted account balances are large, roughly $300k or more on average. There, 20 bps is about **parity with what Ren actually earns at Morgan Stanley GIFT**: 18.4-18.8 bps of average DAF assets in each of CY2022-CY2024, or $685-737 per account-year [D from 990 Part VII-B, A]. It sits below TIFIN Give's list price for accounts under $1M (30 bps) [S, ADV, A]. It is about half of what Ren earns at the small-balance U.S. Charitable Gift Trust: 39-40 bps, $389-429 per account [D, A].

20 bps is **not** a discount price in large-balance programs, so it cannot win on price there. In small-balance programs (about $100k average) it yields only about $200 per account. That is below every observed staffed-admin price per account ($389-$815) and at or below Unbound's own staffed cost estimate ($192-299 per fund). The bps headline therefore needs a per-account floor.

**Five most consequential findings**
1. **Ren/MS GIFT (missed by earlier repo and Unbound work) is the anchor comparable.** Morgan Stanley GIFT has $9.1B of DAF assets, 21,800 accounts and 0 employees. It paid RenPSG $14.93M in CY2024 for 'ADMIN & LEGAL', which is **18.46 bps on average assets and $737 per average account** [D]. The donor circular shows the mechanism: donors pay a 'Third Party Administrator' fee of the greater of $100 or 0.27% up to $2M, falling to 0.09%, assessed on each account. Donors also pay a **separate 7 bps to MSSB** for 'administration services and ongoing maintenance and support of the platform', and up to 3 bps for sponsor general operating expenses [S, A].
2. **Unbound's '33-37 bps outsourced admin' benchmark is biased high.** It used year-end assets (average assets give 38-40 bps). It covers only the two small-to-mid-balance Ren clients, one of them a related party, and it omits MS GIFT. The observed full-service band is **18-40 bps, or about $390-$815 per account-year**. Per-account price is more stable than bps.
3. **Software-only DAF platforms sell at 0.5-9 bps** ($34-$611 per account). Examples: Ren/Stellar at NCF, Thrivent, T. Rowe, Ayco, the Goldman funds and several CFs. Small clients pay what looks like a fixed floor of about $120-175k a year [D, A]. Staffed administration is the scarce, higher-priced layer.
4. **Large national sponsors run in-house for about 14-27 bps all-in**, excluding investment fees. Vanguard Charitable is 18.6 bps ($1,327 per account), Schwab Charitable 19.8 bps ($726), NPT 13.6 bps ($3,463) and Fidelity 26.8 bps [D, A]. At 20 bps a servicer offers those sponsors no saving unless it replaces nearly all of their operating cost, so they are not targets.
5. **Captive and channel economics dominate.** Fidelity pays FMR the donor admin fee net of credits (23.7 bps). BofA pays its trustee bank 56 bps, bundled. Raymond James pays RJ Trust 67 bps including investment management. Banks earn about 60-100 bps of advisory fees on the same assets (MS GIFT advisory up to 1.00%). An incumbent or channel owner can therefore price administration at or below cost.

**Biggest gaps.** No executed servicer contract, minimum, implementation fee or termination price is public; TIFIN's SaaS and implementation amounts are undisclosed. Billable-base definitions are unknown (cash, legacy pools, custom >$100M accounts). Ren's cost to serve is unknown.
""")

sec("(a) What each provider actually earns and from whom", """
All amounts are [S] from IRS e-file XML (gt990datalake mirror of IRS TEOS) or audited statements, accessed 2026-11-25. Ratios are [D] (see price-observations.csv for the arithmetic). The **payer** in each row is the sponsor's books; the **economic payer** is usually the donor account through a fee the sponsor assesses.

| Provider | Payer (sponsor) | Period | Payment | Scope as filed | Mechanism / who really pays |
|---|---|---|---:|---|---|
| RenPSG (Ren) | MS GIFT (0 staff) | CY2024 | $14,930,249 | ADMIN & LEGAL | Donor-account TPA fee 27->9 bps tiers, min $100 (circular Sched. C) |
| Renaissance Administration (Ren) | U.S. Charitable Gift Trust (0 staff) | CY2024 | $4,430,459 | Donor serv / fund acct | Donor fee schedule not located; Eaton Vance Trust Co gets $4.12M trust services separately |
| Ren | Renaissance Charitable Foundation (related; 0 staff) | FY2024 | $19,225,546 | Administration | 98% of individual-fundholder admin fee revenue (audited Note 9); retail donor fee 65/35/25/20 bps, $250 min |
| Ren | Stifel Charitable (0 staff) | CY2025 | $801,302 | Ops system & service | Plus Stifel Trust staffing $723,213 and Advent $250,398 |
| Ren / Stellar | NCF, Thrivent, T. Rowe, Ayco, GS CGF, GS DAPF, ImpactAssets, CFs | 2022-25 | $118k-$2.50M | Software / technology | Sponsor or affiliate staffs operations |
| RPSG / RenPSG | Servant Foundation; Bradley Impact Fund | FY2022 | $828,787; $217,199 | Managed services; fund consulting | Partial outsourcing |
| TIFIN Give LLC | GiveClear Foundation (0 staff) | CY2024 | $185,921 | Technical & charitable support | ADV: service fee billed to sponsor on account ADB, 30 bps <=$1M accounts, 10-20 bps >$1M, plus 10/3.34 bps management fee, plus SaaS implementation and subscription |
| CAF America | Goldman Sachs Charitable Gift Fund | FY2025 | $875,665 | Grant administration | Outsourced grant due diligence only |
| Ayco Co LP (GS affiliate) | GS DAPF; Ayco Charitable | CY2024 | $1,026,306; $1,730,728 | Admin; admin + invest advisory | Affiliate |
| FMR LLC affiliates | Fidelity Charitable (0 staff) | FY2025 | $179,875,837 | Admin & recordkeeping | Equal to donor admin fees net of tier credits (Note 7) |
| Bank of America N.A. (trustee) | BofA Charitable Gift Fund (0 staff) | CY2024 | $24,062,159 | Trustee compensation | Bundled; BofA-to-Ren subcontract not public |
| Raymond James Trust N.A. | RJ Charitable (0 staff) | FY2025 | $14,067,248 | Admin svc & inv mgmt | Bundled |
| Charles Schwab & Co; Vanguard Group | Schwab Charitable; Vanguard Charitable | FY2025; FY2024 | $9,825,772; $3,916,396 | Brokerage & admin; occupancy/admin | Partial support; most cost in-house |
| Benevity; CyberGrants | AOGF; CAF America | FY2024-25 | $45.97M-54.45M; $5.41M-8.29M | Processing | Flow-priced (about 2.4% / 0.7% of grants); not AUA-comparable |

**Do not confuse donor fees with servicer revenue.** Fidelity's headline donor fee starts at 60 bps, but FMR's realized take is 23.7 bps of average assets. MS GIFT donors pay 27 bps on small accounts, but Ren's realized take is 18.5 bps. RCF's donor fee starts at 65 bps, but RCF's total admin revenue is 38.7 bps. Donor headline rates overstate servicer economics by about 1.5-2.5x.

**Why MS GIFT's realized 18.5 bps is below its 27 bps first tier.** The average account is $399k, which the schedule prices at 27 bps. The realized take matches the schedule only for accounts of about $10M (18.9 bps). The likely causes are heavy asset concentration in very large accounts, flat or custom pricing above $50M/$100M, or fee sharing. The public filings cannot distinguish these [D, inference].
""")

sec("(b) Normalized comparison table", """
Average assets = mean of opening and closing Schedule D EOY DAF value; accounts = mean of the two EOY counts. EOY-basis figures are shown for reconciliation with Unbound. Arithmetic is in price-observations.csv `notes` [D].

| Obs | Provider -> sponsor | Category | bps avg assets | bps EOY | $/avg acct-yr | Avg bal/acct | Comparability |
|---|---|---|---:|---:|---:|---:|---|
| O-001 | Ren -> MS GIFT CY24 | staffed admin | **18.46** | 16.39 | **737** | $399k | high |
| O-002/003 | Ren -> MS GIFT CY23/CY22 | staffed admin | 18.83 / 18.39 | 16.92 / 19.21 | 685 / 714 | $364k / $388k | high |
| O-027 | TIFIN -> GiveClear CY24 | staffed admin (tech + services) | 15.4 (unreliable avg) | 8.64 | 815 | n/m | high |
| O-028 | TIFIN ADV list | staffed admin | 30 (<=$1M) / 10-20 (>$1M) | - | $750 at $250k | - | high |
| O-012/013 | Ren -> Stifel CY25/CY24 | ops system & service | 13.3 / 14.1 | 11.3 / 10.1 | 515 / 435 | $387k | medium |
| O-014 | Ren + Stifel Trust + Advent | full admin stack | **29.5** | 25.1 | 1,142 | $387k | high |
| O-008/009 | Ren -> USCGT CY24/CY23 | staffed admin | **40.1** / 39.2 | 37.3 / 36.6 | **429** / 389 | $107k | high |
| O-010 | Ren -> RCF FY24 (related) | bundled | 37.95 | 32.51 | 814 | $214k | medium |
| O-037 | RJ Trust admin share (inferred) | staffed admin | 33.7 | 30.5 | 677 | $201k | medium (D) |
| O-024 | Ayco -> Ayco Charitable | admin + advisory | 15.8 | 14.9 | 318 | $202k | medium |
| O-025 | Ayco -> GS DAPF | staffed admin | 0.95 | 0.81 | 270 | $2.83m | medium |
| O-022 | CAF America -> GS CGF | grant admin only | 15.2 | 13.8 | 1,198 | $789k | medium |
| O-038/039 | RPSG -> Servant; RenPSG -> Bradley | partial | 7.8; 27.9 | 7.2; 19.3 | 427; 1,140 | $545k; $409k | medium |
| O-029 | FMR -> Fidelity | bundled captive | 23.7 | 21.0 | 838 | $353k | medium |
| O-035 | BofA N.A. trustee | bundled | 56.2 | 50.8 | 1,456 | $259k | medium |
| O-036 | RJ Trust | admin + inv mgmt | 66.8 | 60.5 | 1,341 | $201k | low |
| O-031/033/034 | Vanguard / Schwab / NPT self-op | make-vs-buy | 18.6 / 19.8 / 13.7 | 16.4 / 18.5 / 12.0 | 1,327 / 726 / 3,463 | $714k / $367k / $2.54m | medium |
| O-015..026, 043..048 | Ren/Stellar software | software | 0.5-9.3 | - | 34-611 | - | low |
| O-056 | 457 recordkeeping (Voya) | analog | 7 -> 5 | - | 44 -> 31 | $62k | low |
| O-057 | USBFS fund admin | analog | 6/4/3 tiers | - | - | - | low |

**Read-across.**
- **Full staffed admin:** about 15-40 bps, central about 20-30; about $390-$815 per account (central about $650).
- **Software only:** about 1-9 bps; about $35-$300 per account at nationals.
- **bps vs balance:** bps falls with average balance and per-account price is roughly stable. The servicer's cost is account- and transaction-driven, so a bps price alone mismatches cost.
""")

sec("(c) Competitive position at 5/10/15/20/25/30/35 bps", """
Revenue per account at 20 bps: $214 at a $107k average balance (USCGT-like), $428 at $214k (RCF-like), $798 at $399k (MS GIFT-like) [D]. Breakeven bps for a per-account cost C at balance B is C/B x 10,000. At Unbound's staffed cost of $192/$299 per fund, that is 19.2/29.9 bps at $100k, 7.7/12.0 at $250k and 4.8/7.5 at $400k [D].

| Price | What it represents in the observed market | Evidence | Verdict |
|---|---|---|---|
| **5 bps** | The **software-only** band (Ren/Stellar 3-7 bps at NCF, T. Rowe, Ayco, Thrivent); DC recordkeeping 5-7 bps | O-015..023, O-056 | Staffed admin at 5 bps is only viable for ultra-high-balance programs (GS DAPF/Ayco: $270/acct at <1 bps). Otherwise it is predatory or software-only |
| **10 bps** | Software plus light ops (Stifel/Ren 'ops system & service' 10-14 bps EOY; Servant/RPSG 7-8 bps); TIFIN's >$1M tier floor | O-012/013, O-038, O-028 | Undercuts every observed full-service price. Credible only if the sponsor keeps staff (hybrid) or the balance is above $1M |
| **15 bps** | Bottom of full-service: TIFIN >$1M tier mid; Ayco affiliate 15.8; MS GIFT realized EOY-basis 16.4 | O-024, O-028, O-001 | Aggressive full-service price that clearly undercuts Ren at MS GIFT (~3.5 bps or ~19% below) |
| **20 bps** | **About parity with Ren's realized take at MS GIFT (18.4-18.8)**; below TIFIN small-account list (30); ~half of Ren at USCGT (40) and RCF (38); about equal to large nationals' in-house all-in cost (14-27) | O-001..003, O-008, O-010, O-031..034 | **Credible market price**: a parity or modest-premium bid at large-balance programs and a ~50% discount at small-balance programs (where it may be below cost) |
| **25 bps** | Inside the band; TIFIN 10-20 tier ceiling plus mgmt fee; Stifel full stack EOY 25 | O-014, O-028 | Credible at mid-balance programs ($150-300k); a premium over Ren at MS GIFT |
| **30 bps** | TIFIN <=$1M list; MS GIFT TPA 27 + MSSB 7 = 34 total admin on small accounts; Stifel stack 29.5 avg | O-004/005, O-014, O-028 | Price-parity with full-stack incumbents for small/mid balances; no price advantage |
| **35 bps** | Ren at USCGT/RCF effective (33-40); RJ admin share 34 | O-008/009, O-010, O-037 | Incumbent level for $100-200k average-balance programs; only defensible on quality or scope |

The 15-25 bps zone is where a new staffed servicer is price-competitive for $250k+ programs. Below 15 bps a servicer is selling software plus support, not administration.
""")

sec("(d) Tiers, minimums, implementation and exceptional-service charges seen in the market", """
- **Tiered by account balance (marginal), not by sponsor AUA.** Examples: MS GIFT TPA 27/20/15/13/11 bps, 9 bps first-dollar for $50-100M, custom above $100M; RCF 65/35/25/20, custom above $5M; Fidelity 60/30/20/15, flat schedule above $5M down to 11.5 bps; Charityvest 60/30/20/15/10; TIFIN 30 vs 10-20 bps split at $1M [S, A].
- **Program-size tiers.** MSSB admin fee: 7 bps on accounts to $25M, then 3 to 0.5 bps above $25M. USBFS fund admin 6/4/3 bps by fund size [S, A].
- **Per-account minimums.** $100 (MS GIFT TPA, Fidelity, Charityvest); $250 (RCF/Ren); $360 (NCF, $30/month). Community foundations charge $600-$1,750 (Columbus $150/quarter, Atlanta CF $1,000, Myriad USA $1,750; the last two are search snippets, C). Daffy is flat $36-$480 a year [S].
- **Contract-level minimums.** USBFS $60,000 per portfolio plus a CPI escalator (EDGAR exhibit, A). Ren/Stellar small-client lines are flat at about $118-175k a year across years (CF Acadiana, JF Seattle, GS CGF), consistent with a platform floor [D, inference].
- **Implementation / SaaS.** TIFIN Give discloses a 'one-time implementation fee and an ongoing subscription fee' for third-party platform users, amounts undisclosed [S, A]. Foundant lists $250/h consulting and $2,500 per trainer-day [repo, C]. The Ren MSA template has change orders, fees on termination through quarter-end and 1-year auto-renewal with 60-day notice [repo, B]. NCF's Stellar line doubled 2022-2024 and Thrivent's rose 77% on a vendor change, suggesting project fees are embedded [D].
- **Exceptional-service charges.**
  - MS GIFT: $3,500 per grant to an 'Other Grantee Organization' and $2,000 for a second category (2019 circular; the 2024 circular says 'additional fees ... contact the third-party administrator').
  - RCF/Ren: extraordinary-service fees for foreign grants, 509(a)(3) grants, organizations without a 509(a) letter, and fundraising events.
  - NCF: $25 per wired grant.
  - Chariot: Mailroom $1.50 per item; DAFpay Network check surcharge (lesser of $25 or 10%, repo).
- **Channel slices beside the servicer.** MSSB 7 bps admin and up to 3 bps sponsor GOE at MS GIFT. Eaton Vance Distributors was paid $8.19M for 'fundraising' by USCGT.
""")

sec("(e) Is 20 bps credible? Conditional answer with ranges", """
**Credible as a list price for comparable scope if all of the following hold:**
1. The asset-weighted average balance is at least about $250-400k. At $399k, 20 bps = $798 per account, slightly above Ren's $737 at MS GIFT.
2. Scope matches Ren-at-MS-GIFT: portal, contributions, grant processing and due diligence support, fund accounting, donor service, tax/regulatory support. Custody, investment management and legal sponsorship are excluded.
3. Exceptions are billed separately.
4. A per-account floor applies, of the order of $250-400 a year (market minimums $100-360; observed full-service per-account prices start at $389).

**Ranges [E: method = observed band, weighted to O-001/O-008/O-014/O-028].**

| Average balance per account | Competitive staffed-admin price | 20 bps outcome |
|---|---|---|
| >= $1M | 10-20 bps (TIFIN >$1M tier; MS GIFT realized) | 20 bps is at or above market; expect pressure to 12-15 |
| $250k-1M | 15-30 bps; central about 20 | Market-level |
| $100-250k | 30-40 bps, or $390-500 per account (USCGT, RCF, RJ admin share) | 20 bps is a deep discount, likely below cost ($200-500 per account) |
| < $100k | Per-account pricing ($250-430) or 40+ bps | 20 bps not viable without a floor |

**Not credible as a discount weapon at large-balance programs.** Ren already earns about 18.5 bps at MS GIFT, so 20 bps is not cheaper there. The case must rest on service, control evidence, AI-driven exception handling and portability, not price. Large self-operated nationals already spend 14-27 bps all-in. Fidelity and Schwab gain from affiliate investment revenue. Neither group is a price-led target.

**Not proven:** willingness to pay, actual billable-base definitions, and whether Ren's 18.5 bps includes concessions the public cannot see. This assessment is same-model reasoning (A-PRC-010).
""")

sec("(f) What the price must include or exclude to be comparable", """
**To compare with Ren at MS GIFT/USCGT (the high-comparability set), include:**
- Donor/adviser portal and white-label (TIFIN fee is 'Administrative, Technology and Services').
- Contribution intake, including non-cash (MS GIFT markets 'no-fee evaluations' of complex assets).
- Grant recommendation intake, charity verification and payment execution.
- Fund accounting and record-keeping, statements and tax receipts.
- Donor and adviser service desk.
- Regulatory and Schedule D support (USCGT lists tax; MS GIFT 'ADMIN & LEGAL').
- Audit support and SOC reporting.

**Exclude or price separately:**
- Investment management/advice (MSSB about 60-100 bps; TIFIN 10/3.34 bps management fee).
- Custody and trustee services (Eaton Vance Trust Co $4.12M at USCGT).
- Legal sponsorship, board and final grant approval (sponsor retained; MS GIFT GOE up to 3 bps).
- Distribution/fundraising payments (Eaton Vance Distributors $8.19M).
- Channel platform fee (MSSB 7 bps).
- Implementation/migration (TIFIN one-time fee; Ren change orders).
- Exceptional grants: foreign, expenditure responsibility, 509(a)(3), events ($2,000-3,500 per grant at MS GIFT 2019).
- Payment-network pass-throughs (Chariot, check printing/mail at $1.50 per item).

**Denominator definition must be explicit:**
- Average daily or month-end balance (MS GIFT TPA uses month-end per account; MSSB uses average monthly; TIFIN uses average daily).
- Whether cash/sweep and legacy pools are billable.
- Treatment of accounts above $50M/$100M (flat or custom at MS GIFT).
- Whether the fee is billed to the sponsor or to donor accounts. MS GIFT TPA and RCF are effectively donor-billed; TIFIN bills the sponsor 'Client' on account balances.
- Annual CPI or minimum escalators (USBFS precedent).

A 20 bps quote excluding the portal or the payments rail is not comparable to Ren at 18.5. A 20 bps quote including custody or investment advice would be well below market.
""")

sec("(g) Incumbent competitive-response options and cost to match 20 bps", """
[D] = 0.002 x average DAF assets minus current payment.
- **Ren at MS GIFT:** already below 20 bps. At 20 bps MS GIFT would pay $16.17M vs $14.93M actual, so Ren needs **no price cut** to match.
- **Ren at USCGT:** matching 20 bps would cut revenue from $4.43M to $2.21M (**-$2.22M a year, -50%**).
- **Ren at RCF (related):** -$9.09M, but this is not contestable: the related-party board overlap and 98% fee share mean RCF is captive.
- **Stifel full stack (Ren + Stifel Trust + Advent) at 20 bps:** -$0.57M a year across three suppliers. Ren alone (13.3 bps) is already below 20.

**Response options, cheapest first:**
1. **Do nothing in large-balance programs.** Ren is at about 18.5 bps.
2. **Re-tier rather than cut.** Lower small-account tiers and keep minimums ($100-250 per account), or reprice exceptions. This defends small-balance programs at low cost because small accounts are few in asset terms.
3. **Bundle software at marginal cost.** Ren/Stellar already sells software at 3-7 bps. Adding 'managed services' lets Ren hit any staffed-admin price while keeping implementation, change-order and exit friction (MSA renewal/termination clauses).
4. **Cross-subsidize from investment economics.**
   - TIFIN earns management fees (10/3.34 bps) and model-sponsorship fees (ADV Item 14) and can drop its service fee from 30 to 10-20 bps.
   - Bank channels earn about 60-100 bps advisory on the same assets (MS GIFT advisory up to 1.00%) plus a 7 bps MSSB admin slice. They can absorb administration cost to keep assets.
   - Fidelity, Schwab and Vanguard affiliates earn fund fees.
5. **In-source.** Large nationals already self-operate at about 14-27 bps (Vanguard, Schwab, NPT, Fidelity).

**Implication.** Price alone does not dislodge Ren, the captives or the channels. The entrant's price must be paired with demonstrable lower exception cost, portability (data export, no termination fee), sponsor-controlled evidence, and minimums that protect unit economics at small balances.
""")

sec("(h) Evidence gaps and quality notes", """
1. **No executed servicer contract is public.** Not available: MS GIFT-RenPSG, USCGT-Renaissance Administration, BofA-Ren, Stifel-Ren, GiveClear-TIFIN; minimums, SLAs, implementation and termination fees; billable-base definitions. Ren's MSA is an unsigned template.
2. **Why MS GIFT's realized take (18.5 bps) is below the 27 bps first tier** (asset concentration vs custom deals vs sharing) cannot be resolved publicly. Needs MS GIFT account-size distribution (not published).
3. **Average vs year-end assets.** Only two points per year. Distortions:
   - GiveClear grew 8x, so its 15.4 bps average is unreliable; EOY gives 8.6 bps.
   - Stifel grew 2.3x.
   - FY2025 returns for MS GIFT, USCGT and RCF are not yet in the IRS index as of this run.
4. **Part VII-B limits.** It lists only the top-5 contractors over $100k, so smaller vendor lines are invisible. Ayco's Stellar line vanished in 2024. Lines may embed implementation or project work (NCF doubling).
5. **Scope labels are terse** ('ADMIN & LEGAL', 'OPS SYSTEM & SERVICE', 'PAYMENT PROCESSING'). Scope mapping is inference (B/D).
6. **Not found:** donor fee schedule for the U.S. Charitable Gift Trust; BofA trustee split between admin and investment; TIFIN SaaS/implementation amounts; Foundation Source's take from Charityvest/TIAA; Chariot Disbursements grantmaker fee.
7. **Searches with no result:** no procurement record or board minute disclosing a DAF administration contract price was found (one extended search). Several hosts (philanthropy.org, ProPublica PDF downloads, NAPA/PSCA) returned 403.
8. **Ren's cost to serve and margin are unknown.** Without them the cost floor of the incumbent response cannot be bounded.
9. **Analog comparables** (DC recordkeeping $31-44 per participant; fund admin 3-6 bps plus $60k minimum) are structurally different. They are used only for contract-form precedent and the per-account cost shape.
10. **Same-model reasoning is not independent validation.** Validate via 3-5 RFP-style quotes or design-partner terms (public-only constraint means this could not be done here).
11. **Correction to the repo.** `research/audited-revenue-and-client-cohorts-2026-11-11.md` says no TIFIN-specific payment was established. GiveClear's CY2024 990 Part VII-B shows Tifin Give LLC $185,921 (EV-PRC-014).
""")

for s in S: print(json.dumps(s))
