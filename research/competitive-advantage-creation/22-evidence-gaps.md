# 22 - Evidence gaps

Status: research (2026-11-26). Reconciliation agent (RECON). This report prioritizes all 71 Phase III evidence gaps in [evidence-gaps.csv](data/registers/evidence-gaps.csv) (P3-GAP-) by decision value and cost to close, after both review rounds and model revision 3. No gap is closed here. Closing any gap that needs contact with buyers, partners, auditors, brokers or counsel requires separate owner approval; no expenditure is authorized (DEC-008).

## Answer in brief

1. **Five questions carry almost all the decision value.** Model revision 3 shows that only partner-book licensing pays back, and only when the sponsor performs the deep review or under M5 (`bases.md`, `gate-break-even.md`; [16](16-capital-efficient-market-entry.md)). The five questions:
   - **Who performs and pays for the deep review under licensing** (P3-GAP-RECON001; P3-DEC-MOD005). Single-sponsor break-even is not reached if Echelon performs M1, and is 3,079 accounts ($175k net) if the sponsor does.
   - **Revenue per customer at a named sponsor size, or a partner book** (P3-GAP-MOD003, P3-GAP-AB007, P3-GAP-RECON002). Break-even is 3,079-5,202 single-sponsor accounts, or a 12,457-account partner book with the sponsor performing the review. Only 17 plausible sponsors hold 2,646 accounts or more (revision 2 gave 10,963 accounts under M1 and 3,949 under M5).
   - **Whether a named partner exists and when** (P3-GAP-MOD002, P3-GAP-AB004).
   - **The owner's funding capacity against the cash at risk before the kill rule pauses** (P3-GAP-MOD001, P3-GAP-AB006): $1.38M for A3 and $1.33M for A from today (revision 3).
   - **OD-CDD-02 and auditor acceptance of automated renewal** (P3-GAP-HI003), or an attested risk-tiered review that stays within the ratified wording (P3-GAP-RECON004). With Echelon performing the review, M5 moves A3's peak from $8.26M to $2.52M (revision 3; revision 2 gave $8.70M and $3.46M).
2. **Most priority-A gaps can be closed for $0 to about $5k.** They need an owner statement, a desk calculation, a build ledger, or owner-approved founder conversations. They do not need a budget ([04](04-low-cost-commercial-validation.md), [23](23-commercial-validation-roadmap.md)).
3. **The costly gaps should wait for the cheap ones.** Counsel opinions, SOC reports, a real export rehearsal and insurance quotes cost $5k to $100k or more. They matter only once a named partner and a sponsor of break-even size exist. Payments counsel (P3-GAP-AB003), hosted-programme roles (P3-GAP-CD006) and solicitation registration (P3-GAP-CD013) are the main examples.
4. **28 gaps have low decision value.** They are market-sizing refinements, competitor detail and dates. Close them only if a decision comes to depend on them.

## 1. How the priority is set

| Priority | Meaning | Count |
|---|---|---|
| **A** | Decides whether any DAF-specific spend or cost center should happen at all, or which route; cheap to close ($0 to about $5k, or an owner statement) | 13 |
| **B** | Blocks a G1 commitment or a partner contract; usually needs counsel, an auditor, a real pilot or a year of data | 11 |
| **C** | Sharpens model inputs or a requirement; does not by itself change the route | 19 |
| **D** | Context, market-sizing or competitor detail with low decision value now | 28 |

Decision value follows the model's drivers ([19](19-sensitivity-and-stress-analysis.md), `tornado-sequence-a3.md`). In revision 3 the largest drivers are the review allocation and registry mode, charities in use per account, partner share and licence price (`tornado-sequence-a3.md`, `bases.md`). Cost to close is taken from the register. "Blocking" is the register's own flag, as written by the agent that raised the gap.

## 2. Priority-A gaps: what to close first

| Gap | Why first | Cheapest closure |
|---|---|---|
| P3-GAP-RECON001 who performs the deep review | Decides whether break-even exists at all for a single sponsor, and whether partner-book licensing pays back (P3-DEC-MOD005) | An owner decision ($0); partner and sponsor expectations in V-6/V-2 |
| P3-GAP-RECON002 partner-book economics | The only modelled route with a payback (SEQ-PB, month 76) | Desk partner map (P3-VAL-AB003); V-6 book-size question |
| P3-GAP-MOD003 / P3-GAP-AB007 revenue per customer and customers per year | The top economic driver. At 2,646 accounts ($150k net) A3 loses $8.50M by month 120 with Echelon-performed M1 (`sponsor-size.md`, revision 3; $9.24M in revision 2) | P3-VAL-CE001 desk classification ($0); V-2 nonbinding EOIs with account counts and V-6 term-sheet economics ($0-1k plus approval) |
| P3-GAP-MOD002 / P3-GAP-AB004 named partner, timing and terms | The kill rule's first test; partner share is among the top four drivers | V-6 founder-led conversations (P3-VAL-AB009), after owner approval |
| P3-GAP-MOD001 / P3-GAP-AB006 funding capacity | Sets whether $1.46-1.81M at risk is acceptable; there is no base payback to fund towards (P3-CLM-MOD012) | An owner statement ($0) |
| P3-GAP-CE004 / P3-GAP-AB002 S2-to-S3 cash, hours and date | Decides between A3B and A3X and whether S3 is reached at all; S2 cash is unledgered | Start the build ledger now (P3-DEC-AB003) |
| P3-GAP-MOD005 cost-center definition | Decides when the kill-rule clock starts (OD-P3-03, OD-P3-04; P3-DEC-MOD001) | An owner ruling ($0) |
| P3-GAP-CD010 rate of new institutional programme launches | Decides whether E and G are worth keeping even as adoption routes | Public-record review ($0) |
| P3-GAP-CE001 owner outcome measures and triggers | Needed before any decision moves past "strategically approved" (P3-DEC-CE003) | Owner review of [21](21-commercial-thesis-invalidation.md) |

## 3. Register, prioritized

| Priority | Gap | What is missing | Why it matters | How to close | Cost to close | Blocking (register) |
|---|---|---|---|---|---|---|
| A | P3-GAP-RECON001 | Who performs and pays for the human deep review under licensing: sponsor staff in Unbound, Echelon as a priced service, or Echelon unpriced (P3-DEC-MOD005) | Sets break-even: not reached with Echelon-performed M1; 3,079 accounts per sponsor if the sponsor performs it; also decides whether partner-book licensing pays back (month 76) | Owner decision; partner and sponsor conversations on whether they expect the review in the licence (V-6, V-2); counsel on reliance | $0 decision; $0-1k plus approval for conversations | Yes for P3-DEC-MOD003 threshold |
| A | P3-GAP-RECON002 | Partner-book economics: existence of a partner whose book of small sponsors can be licensed as one customer, book size in accounts, per-sponsor conversion rate and sponsor conversion labour inside the book | Partner-book licensing (SEQ-PB) is the only modelled route with a payback; its break-even book is 12,457 accounts with sponsor-performed review | V-6 partner conversations with a book-size and conversion question; desk map of partners with sponsor books (P3-VAL-AB003) | $0 desk; $0-1k plus approval | Yes for any partner-book sequence commitment |
| A | P3-GAP-MOD003 | Revenue per customer for Unbound licensing: Phase II ER-7 $150-600k net versus agent FGJ $25-150k gross per sponsor | The most consequential input conflict between agents; A/A3 pay back only at ER-7 values | V-2 pricing interviews and partner term sheets | $0-5k | Yes |
| A | P3-GAP-MOD001 | Owner's available funding capacity and runway for DAF commercialization | Decides whether outside investment is necessary for the modelled peak cash | Owner statement (private; not in this repository) | $0 | Yes |
| A | P3-GAP-MOD002 | Timing of a named partner or design-partner customer (P3-ASM-MOD034) | Drives the kill-rule outcome; the Monte Carlo pause share is dominated by this unevidenced range | V-6 conversations; $0 validation routes (report 04) | $0-5k | Yes |
| A | P3-GAP-CE004 | No estimate of the cash, hours and date to take Unbound from S2 to S3 inside existing operations | Decides whether the thesis is A3 (passes the kill rule) or A (paused in the base case) | Ledger build hours and cash (P3-DEC-AB003) and a completion plan | $0 | yes for sequence choice |
| A | P3-GAP-AB007 | Customers per year and net revenue per customer through a channel are untested Phase II assumptions | Dominant driver; adverse case is never self-sustaining | V-6 then first pilot | $0-100k | yes |
| A | P3-GAP-AB004 | Partner economics (share 30-50%, support split, exclusivity) unknown | Largest driver of revenue per customer and support cost | V-6 term sheet | $0-15k | yes |
| A | P3-GAP-AB006 | No owner figures for founder cash draw, runway or funding route | Sets the cash vs economic gap and the kill-rule capital | Owner statement | $0 | no |
| A | P3-GAP-AB002 | Actual cash and hours spent building Unbound are not ledgered, so sunk cost and agent-assisted productivity are unknown | Determines whether PR #87 M-07 is moot and validates the $1.1-2.4M build range | Compile agent-compute invoices and git/Praxis telemetry per accepted capability | $0 | no |
| A | P3-GAP-CD010 | Institutional demand: rate of new university/hospital DAF programme launches 2021-26 | Core of S1/S4 thesis | 990 Part IV line 6 first-time 'yes' scan for education/health filers | $0 | yes for Sequence E |
| A | P3-GAP-MOD005 | Whether Unbound development spend counts as DAF commercialization for the cost-center clock (P3-ASM-MOD017) | Changes when the kill-rule clock starts for sequences that include development | Owner clarification of OD-P3-04 | $0 | No |
| A | P3-GAP-CE001 | Owner-accepted outcome measures, review cadences and reconsideration triggers for DEC-001..012 do not exist (agent proposals only) | Without accepted failure signals the approved directions cannot be held to a reconsideration rule | Owner accepts or amends (P3-DEC-CE003) | $0 | yes for commitment-level decisions |
| B | P3-GAP-HI003 | Auditor acceptance of machine 180-day renewal plus attribute-sample audit | Without it audit preparation (E22) cannot fall and sponsors may keep human reviews | Desk review of public audit-sampling guidance now; V-9 walkthrough later | $0 now; $0-30k V-9 | Yes for DEC-003 requirements incorporation |
| B | P3-GAP-RECON004 | Whether an attested, machine-assembled evidence pack with a short human attestation satisfies the ratified 'comprehensive review' (RR-REQ-X-007-r1) without OD-CDD-02 | The M1 risk-tiered configuration lowers break-even to 5,202 accounts while staying within the ratified wording, if counsel and an auditor accept it | Counsel question list ($0); V-9 walkthrough ($1k informal; written position later) | $0 now; $15-30k later | No (alternative to OD-CDD-02) |
| B | P3-GAP-AB003 | Which Nacha TPSP functions Unbound performs in a partner-originated model (the TPSP role itself is set by ratified CNV-PAY-001). Revision 2 (2026-11-26, round-1 review): previously 'Nacha TPSP status in a partner-originated model is unresolved' (P3-CHL-REV3019) | Sets the scope of the annual Rules compliance audit (a base obligation, ~$50k/yr Phase II) and fraud-monitoring operation | Payments counsel opinion | $15-100k | yes for G1 |
| B | P3-GAP-CD006 | Counsel view on hosted-programme role allocation, supporting-organization sponsors and credit-union exemption basis | Regulatory exposure of S1/S4 | Counsel review (not authorized spend) | $5-15k (not authorized) | yes for G1 |
| B | P3-GAP-CD013 | Whether contribution-linked revenue shares in hosted, white-label or channel programmes create state professional-fundraiser, fundraising-counsel or commercial co-venturer registration for the partner, institution or Echelon | Unregistered solicitation roles carry state penalties and would change channel terms | Counsel question list per channel model ($0 now); written opinion only once a channel model is chosen; until then price on accounts/flat fees | $0 now; counsel fee later | Yes for any contribution-linked term |
| B | P3-GAP-AB005 | Whether sponsors auditors will require SOC 1 from a licensor | Adds $20-120k/yr | V-9 auditor walkthrough; partner procurement checklist | $0-30k | no |
| B | P3-GAP-EK008 | No Track E advantage is measured because Unbound is not built; all customer-value measures are design targets | Every classification above 'unproven' is provisional | Measure on the first partner pilot (V-3, V-5) | Within existing G1 plan | Yes for any claim of superiority |
| B | P3-GAP-CD011 | Real CAC and onboarding cost per hosted programme | Vendor viability of small programmes | Measure at first host (G1) | Part of pilot | yes for scale |
| B | P3-GAP-FGJ002 | Partner-sourced deal rate and partner sales-cycle length are unknown | Determines whether enablement cost is recovered and whether partner-first is faster | Track from first partner agreement; no earlier source | $0 | Yes for G2 partner-revenue forecasts |
| B | P3-GAP-FGJ004 | Commercial licence terms for Echelon components are "forthcoming" | Blocks both Unbound launch and any component revenue; a partner diligence item | Owner licensing-policy decision (P3-DEC-FGJ001) with counsel review before publication | $0 decision; counsel later | Yes for any commercial use |
| B | P3-GAP-HI007 | Human-relevant eligibility change rate among in-use charities over 12 releases | Phase II 4% vs evidence ~0.3-0.5%; drives registry workload | Archive monthly releases from now; replay | $0; 12 months elapsed | No |
| C | P3-GAP-AB001 | No insurance indications for a payments-adjacent DAF licensor ($5M cyber, tech E&O, D&O, crime) | Insurance is $30-160k/yr of the run rate and a procurement gate | Broker indications at a term sheet (no binding) | $0 (requires owner-approved contact) | no |
| C | P3-GAP-AB008 | Hardening scope from functionally complete to production-ready has no bottom-up estimate | Separates S3 from S2 economics | Security architecture review and DR/accessibility checklist against CNV clauses | $0 desk; $10-40k external review | no |
| C | P3-GAP-AB009 | SOC 2 and pen-test prices are vendor content without auditor quotes | Moderate effect on run rate | Two auditor indications at the $50k tier | $0 | no |
| C | P3-GAP-AB010 | V-3 change rate across 12 archived BMF releases not measured | V-3 pass rule | Run Unbound replay tool over NCCS archive | $0-1k | no |
| C | P3-GAP-CE005 | The applicable licensing walk-away price is unsettled ($73 vs $58.51 vs $21.51) because the achieved cost base is unknown | A price floor set on the wrong cost base either rejects viable deals or accepts unviable ones | Measure the live run rate; restate P3-DEC-EK001 on the measured base | $0 | no |
| C | P3-GAP-EK003 | No public precedent for technology-licence price cuts or renewal discounts in DAF software (pricing opaque) | Price-cut assumptions EK001/EK002 are unanchored | Stayer interviews (V-1) asking what renewal concessions were offered | $0 | No |
| C | P3-GAP-EK004 | Exclusivity and change-of-control terms in TIFIN-SEI, Orion-GiftingNetwork and Altruist-Endaoment deals are not public | Partner-dependency and exclusive-partnership scenarios | Public filings (SEI 10-K/10-Q) and partner conversations | $0 | No |
| C | P3-GAP-EK009 | Win-rate elasticity to incumbent responses has no DAF evidence | Scenario viability depends on it | Win/loss interviews (V-1) including stayers | $0 | No |
| C | P3-GAP-FGJ001 | Revenue-share and fee terms of DAF and wealth-platform channel partnerships and of bank-core marketplaces are not public | Partner-first economics (P3-CLM-FGJ009) rest on generic software benchmarks | Ask in V-6 partner conversations; review any public partner programme agreements | $0 (founder time inside V-6) | No (blocks precision, not direction) |
| C | P3-GAP-HI001 | Exception rates and handling minutes per operational event (no DAF time study) | Every automated/eliminated split and residual depends on them | Synthetic operations now; 90-day time study with a design partner later | $0 now; design partner later | No (direction); yes for SLAs (DEC-010) |
| C | P3-GAP-HI004 | Automated renewal failure rate for tier-2 evidence (central rosters; church and fiscal-sponsor attestations) | Controls the largest variable human line after first-time verification | Test automated retrieval of central-organisation rosters for the largest GENs | $0 | No |
| C | P3-GAP-HI008 | Charity union overlap exponent across sponsors | Dominates multi-sponsor and marginal cost | Compute from 20-sponsor Schedule I replay | $0 | No |
| C | P3-GAP-HI009 | Willingness to pay for a standalone charity evidence service (V-8) | Decides commercial-asset question | Desk price survey now; V-8 when outreach is authorised | $0 now; $10-30k later | No |
| C | P3-GAP-HI010 | Whether Phase II MD fixed cost already includes registry engineering | Double count if registry run cost is added | Trace PR87 fixed-cost build-up | $0 | No |
| C | P3-GAP-HI011 | 2027 group-exemption transition wave (Rev. Proc. 2026-8, transition ends 2027-01-22): volume of GEN terminations, subordinate removals and re-applications in BMF releases | Tier-2 renewal failure, group-exit and identity-dispute rates in 11 and P3-EV-HI012 are steady-state assumptions that will not hold in 2027 | Archive monthly BMF releases now (P3-DEC-HI004) and diff GROUP/subordinate fields from 2026-12 to 2027-06; stress rates several-fold in the model meanwhile | $0 | No (affects 2027 run cost and workload) |
| C | P3-GAP-MOD004 | Vendor variable cost per licensed account for a lean licensor (P3-ASM-MOD003) | Moves break-even accounts and peak cash materially | Measure support minutes and hosting per tenant in a pilot | $0 | No |
| C | P3-GAP-MOD006 | Share of registry engineering and counsel covered by the lean maintenance and corporate-admin budgets (P3-ASM-MOD010) | Adds $0-65k a year (base inputs) to the lean licensor run | Engineering plan that names registry connectors in the maintenance budget | $0 | No |
| C | P3-GAP-RECON003 | Grant frequency per charity in use (distinct 180-day windows with a new approval), which drives demand-driven deep reviews | Demand-driven review frequency (P3-ASM-MOD050, 1.0-1.6 a year) sets the M1 review workload whoever performs it | V-3 replay of Schedule I recipient-year frequency over the 20 parsed sponsors | $0 | No |
| C | P3-GAP-RECON005 | Accredited-auditor quote for the annual Nacha Rules compliance audit and fraud-monitoring operation of a TPSP that holds no funds | The TPSP base line ($30-130k; P3-ASM-MOD040) is unquoted | Indicative quote request once outreach is approved | $0 (requires owner-approved contact) | No |
| D | P3-GAP-CD001 | Reconciled count of US community foundations (CoF 'more than 900' undated vs BMF T31 3,830 vs DAFRC 804) | Sizing hosting/host-sponsor universe | Fetch CoF locator / CF Insights data; filter BMF T31 by filing and assets | $0 | no |
| D | P3-GAP-CD002 | Which banks and trust companies have a branded DAF programme (count) | Sizing bank partner-sponsor displacement vs greenfield | Public bank wealth pages + sponsor 990 Schedule R/O mentions | $0 (time) | no |
| D | P3-GAP-CD003 | NCUA credit-union counts by asset band below/above $1bn | Prospect banding | NCUA call-report data download | $0 | no |
| D | P3-GAP-CD004 | National count of state-chartered trust companies | SEG-007 sizing | CSBS / state regulator lists | $0 | no |
| D | P3-GAP-CD005 | Where GW and MSU hosted programmes went after BNY Mellon CGF termination | Tests host-exit trigger (P3-HYP-CD006) | 990 Schedule I of BNY CGF final return; university pages | $0 | no |
| D | P3-GAP-CD007 | Any accounting/tax-network or insurance-carrier DAF programmes | Completes Track C coverage | Targeted public search | $0 | no |
| D | P3-GAP-CD008 | IRS Form 1023 determination time and formation cost for a new sponsor | S2 time to revenue | IRS processing-time page; public filings | $0 | no |
| D | P3-GAP-CD009 | Whether Foundant built CommunitySuite organically and whether GLM customers converted | Only same-buyer analog for narrow-to-platform | Foundant history; press; 990 Part VII-B vendor lines over time | $0 | no |
| D | P3-GAP-CD012 | Effect of the 2026 proposed interagency third-party risk management guidance (P3-SRC-CD021) on bank, credit-union and trust-company vendor review of a small DAF-technology supplier | Bank/trust/CU routes depend on passing TPRM; the proposal emphasises tailoring by risk and size but final text is unknown | Read the proposal and community-bank guide in full; track the final guidance (expected 2027 per commentators) | $0 | No (bank/trust routes are not initial targets) |
| D | P3-GAP-CE002 | Clarity posture diagrams are inconsistent across three framework files | Posture labels are not reproducible from the diagrams alone | Framework owner clarifies; until then state impact and correctability with every posture | $0 | no |
| D | P3-GAP-CE003 | No independent (other model family or human) review of the posture and diagnostic-sufficiency judgments | EDF calibration guidance treats several lenses from one source as non-independent | Human or different-executor review of report 17 section 5 | $0-5k | no |
| D | P3-GAP-EK001 | Incumbent ledger internals (append-only, bitemporal, replay) are not public for Ren, Foundant, NPact, Give Interactive, TIFIN, Foundation Source | Decides whether EK001/EK011/EK017 are differentiators or parity | Partner-side diligence under NDA; RFP responses observed through a partner; SOC report system descriptions | $0 (via partner diligence) | No |
| D | P3-GAP-EK002 | No SOC report or scope inspected for any incumbent; Ren Type 1 vs Type II statements unexplained | Sizes the attestation gap the entrant must close | Request reports through a prospective partner under NDA | $0 | No |
| D | P3-GAP-EK005 | Date of Fidelity Charitable's 1.00% to 0.60% fee cut not established (source undated) | Precedent timing for fee-response speed | Fetch Fidelity Charitable annual reports or press archive | $0 | No |
| D | P3-GAP-EK006 | Auditor acceptance of continuously generated control evidence is untested | EK003 is the only path to lower audit cost | CPA scoping conversation (V-3 adjacent) | $0 | No |
| D | P3-GAP-EK007 | Ren public API documentation not found (DFX API service mentioned historically, specs unreviewed); Fidelity Charitable public API not found | API parity statement rests partly on adjacent vendors | Partner diligence; developer-portal checks | $0 | No |
| D | P3-GAP-EK010 | Continuous-compliance (GRC automation) tooling market was not sourced in this pass | Would show that evidence collection itself is commodity | Public product documentation search | $0 | No |
| D | P3-GAP-EK011 | Date of Vanguard Charitable's 'up to 45%' fee reduction not verified (secondary summary says 2006) | Precedent quality | Fetch the release or Vanguard Charitable history | $0 | No |
| D | P3-GAP-FGJ003 | No usage telemetry (downloads, inbound licence requests) for Echelon developer components | P3-HYP-FGJ003 revenue range is pure assumption | Read public npm/NuGet download counts and GitHub traffic; publish licence terms and count requests | $0 | No |
| D | P3-GAP-FGJ005 | Number of charitable gift annuity issuers and planned-giving administration market size not established | Needed before ranking planned giving above fiscal sponsorship with confidence | ACGA survey reports; state permit registers (NY DFS lists); IRS Form 5227 counts from SOI | $0 | No |
| D | P3-GAP-FGJ006 | 2025 fiscal-sponsorship state-of-field results not retrieved; software needs of fiscal sponsors not evidenced | P3-HYP-FGJ002 untested | Retrieve published results when available; read the 2023 field scan PDF directly | $0 | No |
| D | P3-GAP-FGJ007 | PG Calc, Kaspick and bank planned-giving administration prices are not public; Kaspick status not verified | Pricing and incumbent structure for the top-ranked adjacency | Public 990 Schedule/contractor disclosures of large charities; vendor pages | $0 | No |
| D | P3-GAP-FGJ008 | Current Salesforce AppExchange revenue share (post-2018) not confirmed | Benchmark currency | Read current AppExchange partner programme documents | $0 | No |
| D | P3-GAP-FGJ009 | Compliance-automation vendor prices are third-party estimates | Context only for compliance-evidence commercialization | Vendor quotes would require outreach (not permitted now) | $0 now; outreach later | No |
| D | P3-GAP-FGJ010 | Signal repository status documents lag its code (277 .fs files, CURRENT-STATE says no slice); maturity of several components inferred from tags only | Component maturity table may understate or overstate | Run builds/tests read-only in a later pass; read HANDOFF.md files | $0 | No |
| D | P3-GAP-HI002 | Whether sponsors already require notification forms that a structured intent would replace | Decides whether attribution prevention is elimination or transfer to donors | Desk review of public sponsor contribution instructions | $0 | No |
| D | P3-GAP-HI005 | Whether California or other states publish a bulk delinquency or may-not-operate list | Determines whether state status can be monitored automatically | Desk check of each state AG open-data and FOIL options | $0 | No |
| D | P3-GAP-HI006 | 990-N release cadence (TEOS page says monthly; Phase II found weekly) | Freshness limits (UNB-CNET-004) depend on it | Observe file Last-Modified over 8 weeks | $0 | No |

## 4. Gaps added by round-1 review

- **P3-GAP-HI011.** The 2027 group-exemption transition under Rev. Proc. 2026-8 (P3-SRC-HI013).
- **P3-GAP-CD012.** The effect of the proposed interagency TPRM guidance (P3-SRC-CD021).
- **P3-GAP-CD013.** Charitable-solicitation registration for contribution-linked shares.
- **Round 2:**
  - P3-GAP-RECON001: who performs the deep review;
  - P3-GAP-RECON002: partner-book economics;
  - P3-GAP-RECON003: grant frequency per charity, which drives demand-driven reviews;
  - P3-GAP-RECON004: whether an attested risk-tiered review satisfies the ratified wording;
  - P3-GAP-RECON005: a quote for the TPSP audit.
- **P3-GAP-AB003, restated.** Which TPSP functions Unbound performs. The TPSP role itself is no longer a gap, because CNV-PAY-001 sets it.

The deferred model limits in [20](20-adversarial-review.md) §4 are modelling gaps, not evidence gaps, and are not repeated here.

## 5. What closing the A-gaps could change

- **If V-6 finds a partner book of at least 12,457 accounts whose sponsors would perform the deep review themselves,** the partner-book sequence pays back at month 76 uninterrupted (`bases.md`, revision 3). The kill rule would still need a live pilot by month 24.
- **If only single sponsors are found,** no single-sponsor configuration pays back within 120 months in revision 3, even at 10,582 accounts under M5 (`sponsor-size.md`). In revision 2 that case paid back at month 72; the revision-3 cap of 2 reachable plausible sponsors at that size removes the payback. The honest conclusion is then not to open a DAF cost center ([21](21-commercial-thesis-invalidation.md) TI-01).
