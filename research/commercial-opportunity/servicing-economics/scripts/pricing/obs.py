"""Price observations for DAF administration; pure functions, no shared mutation."""
import csv, json, sys

X = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml"

def avg(a, b): return (a + b) / 2

def bps(fee, base): return round(fee / base * 1e4, 2)

def per_acct(fee, n): return round(fee / n, 0)

def flow(fee, a0, a1, n0, n1):
    """fee on average of opening/closing assets and accounts; also EOY basis."""
    A, N = avg(a0, a1), avg(n0, n1)
    return dict(bps_avg=bps(fee, A), usd_acct=per_acct(fee, N), bps_eoy=bps(fee, a1),
                usd_acct_eoy=per_acct(fee, n1), avg_assets=A, avg_accts=N,
                arith=f"{fee:,.0f} / avg({a0:,.0f}, {a1:,.0f}) = {fee:,.0f} / {A:,.0f} = {bps(fee,A)} bps; "
                      f"{fee:,.0f} / avg({n0:,}, {n1:,}) accts = {per_acct(fee,N):,.0f} $/acct-yr; "
                      f"EOY basis {bps(fee,a1)} bps, {per_acct(fee,n1):,.0f} $/EOY acct")

def marginal(balance, tiers, minimum=0):
    """tiers: list of (upper_bound or None, rate_bps). Marginal schedule."""
    fee, lo = 0.0, 0.0
    for hi, r in tiers:
        top = balance if hi is None else min(balance, hi)
        if top > lo: fee += (top - lo) * r / 1e4
        if hi is None or balance <= hi: break
        lo = hi
    return max(fee, minimum)

def sched(tiers, minimum, pts=(100_000, 250_000, 1_000_000, 5_000_000)):
    parts = [f"${p/1e3:,.0f}k: {bps(marginal(p,tiers,minimum),p)} bps / ${marginal(p,tiers,minimum):,.0f}" for p in pts]
    return "; ".join(parts)

MS_TPA = [(2e6, 27), (5e6, 20), (1e7, 15), (2.5e7, 13), (5e7, 11), (None, 9)]
REN_RETAIL = [(5e5, 65), (1e6, 35), (2.5e6, 25), (None, 20)]
FID = [(5e5, 60), (1e6, 30), (2.5e6, 20), (None, 15)]
CV = [(5e5, 60), (1e6, 30), (2.5e6, 20), (5e6, 15), (None, 10)]
BOFA_NOTE = "BofA CGF schedule is 'flat rate applied to first dollar' per repo (90/75/50/35/25/15/12/10 bps); not marginal"

def rows():
    R = []
    def add(**k): R.append(k)
    # --- sponsor -> servicer payments, 990 Part VII-B (amount = floor? no: named line exact) ---
    f = flow(14_930_249, 7_062_576_748, 9_109_107_748, 18_724, 21_800)
    add(obs_id="PRC-O-001", provider="Ren (RenPSG)", payer="Morgan Stanley Global Impact Funding Trust (sponsor; funded by donor-account TPA fee)", payee="RenPSG",
        service_scope="Full back-office DAF administration: online portal, contribution & grant processing, accounting/record-keeping, grant due diligence support ('ADMIN & LEGAL'); sponsor has 0 employees; investment advice by MSSB separately",
        scope_category="staffed_admin", fee_basis="990 Part VII-B payment; underlying donor-account TPA tier schedule (PRC-O-004)", fee_value=14_930_249, fee_unit="USD/yr",
        denominator_basis="avg of FY2023 & FY2024 Schedule D EOY DAF value; avg EOY DAF count", f=f, minimum_fee="$100/account (TPA schedule)", tiers="27/20/15/13/11/9 bps by account balance",
        period="FY2024 (CY)", source=X.format("202503239349300435")+" ; prior "+X.format("202403209349313980"), quality="A",
        comp="high", notes="Single most comparable observation: unaffiliated outsourced administrator to a 0-employee bank-channel sponsor. Avg balance/acct $399k.")
    f = flow(11_949_715, 5_629_724_104, 7_062_576_748, 16_178, 18_724)
    add(obs_id="PRC-O-002", provider="Ren (RenPSG)", payer="MS GIFT", payee="RenPSG", service_scope="as PRC-O-001", scope_category="staffed_admin",
        fee_basis="990 Part VII-B", fee_value=11_949_715, fee_unit="USD/yr", denominator_basis="avg EOY FY2022/FY2023 DAF value and count", f=f,
        minimum_fee="$100/account", tiers="as PRC-O-004", period="FY2023", source=X.format("202403209349313980")+" ; "+X.format("202302999349301010"), quality="A", comp="high",
        notes="Stable ~18.5-18.8 bps across 3 years")
    f = flow(10_815_853, 6_133_745_382, 5_629_724_104, 14_125, 16_178)
    add(obs_id="PRC-O-003", provider="Ren (RenPSG)", payer="MS GIFT", payee="RenPSG", service_scope="as PRC-O-001", scope_category="staffed_admin",
        fee_basis="990 Part VII-B", fee_value=10_815_853, fee_unit="USD/yr", denominator_basis="avg EOY FY2021 (DAFRC dataset) / FY2022 (XML) DAF value and count", f=f,
        minimum_fee="$100/account", tiers="as PRC-O-004", period="FY2022", source=X.format("202302999349301010")+" ; FY2021 EOY from data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv", quality="A", comp="high", notes="Down-market year (assets fell) yet bps stable")
    add(obs_id="PRC-O-004", provider="MS GIFT third-party administrator (Ren)", payer="Donor DAF account (assessed monthly on month-end balance)", payee="Third-party administrator",
        service_scope="Online Portal, contributions, grant recommendations and payments, administrative/accounting/record-keeping", scope_category="staffed_admin",
        fee_basis="Marginal tiers on account month-end balance", fee_value="27/20/15/13/11 bps; 9 bps first-dollar $50-100M; custom >=$100M", fee_unit="bps/yr per account",
        denominator_basis="per-account balance", f=dict(bps_avg=sched(MS_TPA,100), usd_acct="see bps cell", arith="marginal(balance) per tier; min $100"),
        minimum_fee="greater of $100 or 0.27%", tiers="$0-2M 0.27%; next to $5M 0.20%; to $10M 0.15%; to $25M 0.13%; to $50M 0.11%; $50-100M 0.09% first dollar; >$100M custom",
        period="Donor Circular PDF created 2024-08-22", source="https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf (Schedule C p15)", quality="A", comp="high",
        notes="DONOR-paid schedule that funds the servicer; at a $399k average balance it implies 27 bps, but realized servicer take is 18.5 bps of sponsor avg assets => asset mix skewed to >$2M accounts and/or custom deals. Separate MSSB 7 bps and charitable admin fee <=3 bps.")
    add(obs_id="PRC-O-005", provider="Morgan Stanley Smith Barney", payer="Donor DAF account", payee="MSSB (sponsor-channel affiliate)",
        service_scope="'administration services and ongoing maintenance and support of the platform'", scope_category="bundled",
        fee_basis="tiered on account average monthly balance", fee_value="7 bps to $25M; above: 7 bps first $25M + 3/2/1.5/1/0.5 bps by program size", fee_unit="bps/yr",
        denominator_basis="per-account avg balance", f=dict(bps_avg="7.0 (accounts <$25M)", usd_acct="$70 per $100k", arith="0.07% x balance"),
        minimum_fee="none stated", tiers="see fee_value", period="2024 circular", source="MS GIFT Donor Circular Schedule C p15 (as PRC-O-004)", quality="A", comp="low",
        notes="Shows the distribution channel retains ~7 bps of 'admin' for itself even when a TPA does the work; a new servicer at 20 bps must fit beside this.")
    add(obs_id="PRC-O-006", provider="MS GIFT (sponsor)", payer="Donor DAF account", payee="MS GIFT general operating expenses", service_scope="pro rata audit, operational, technology, legal, regulatory, registration costs", scope_category="legal_sponsorship",
        fee_basis="pro rata, capped", fee_value="<=3", fee_unit="bps/yr", denominator_basis="account balance", f=dict(bps_avg="<=3", usd_acct="", arith="cap 0.03%"),
        minimum_fee="", tiers="", period="2024 circular", source="as PRC-O-004", quality="A", comp="none", notes="Retained sponsor responsibility cost ceiling; sponsor-side costs are tiny when servicer does the work.")
    add(obs_id="PRC-O-007", provider="MS GIFT TPA", payer="Donor DAF account", payee="TPA/MS GIFT", service_scope="Grants to Other Grantee Organizations (non-501c3/foreign; expenditure responsibility)", scope_category="manual",
        fee_basis="per grant", fee_value=3500, fee_unit="USD/grant (2019 circular; 2024 circular says 'additional fees ... contact the third-party administrator')", denominator_basis="per exceptional grant",
        f=dict(bps_avg="", usd_acct="", arith="flat"), minimum_fee="", tiers="$2,000 for a second category (2019)", period="2019 (amount); 2024 (existence)",
        source="https://msgiftuat.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf p7 (June 2019); current circular p8", quality="B", comp="medium", notes="Exceptional-service pricing outside the bps fee")
    f = flow(4_430_459, 1_021_698_718, 1_188_558_132, 9_917, 10_740)
    add(obs_id="PRC-O-008", provider="Renaissance Administration LLC (Ren)", payer="The U.S. Charitable Gift Trust (Eaton Vance/Morgan Stanley channel; 0 employees)", payee="Renaissance Administration LLC",
        service_scope="Donor service / fund accounting / tax (Part VII 'DONOR SERV/FD ACCT'); trustee services separately to Eaton Vance Trust Co ($4.12m) and asset mgmt to Eaton Vance Mgmt",
        scope_category="staffed_admin", fee_basis="990 Part VII-B (reported in Part IX accounting-fees line)", fee_value=4_430_459, fee_unit="USD/yr", denominator_basis="avg EOY DAF value/count FY2023-FY2024", f=f,
        minimum_fee="unknown", tiers="unknown (donor schedule not located)", period="FY2024", source=X.format("202533189349305673")+" ; "+X.format("202431319349304428"), quality="A", comp="high",
        notes="Small-balance program (avg $107k/acct) -> high bps; per-account $429 is the better comparator. Sponsor also pays Eaton Vance Distributors 'fundraising' $8.19m.")
    f = flow(3_741_525, 885_067_379, 1_021_698_718, 9_344, 9_917)
    add(obs_id="PRC-O-009", provider="Renaissance Administration LLC (Ren)", payer="U.S. Charitable Gift Trust", payee="Renaissance Administration LLC", service_scope="as PRC-O-008", scope_category="staffed_admin",
        fee_basis="990 Part VII-B", fee_value=3_741_525, fee_unit="USD/yr", denominator_basis="avg EOY FY2022/FY2023", f=f, minimum_fee="unknown", tiers="unknown", period="FY2023",
        source=X.format("202431319349304428")+" ; "+X.format("202341359349318454"), quality="A", comp="high", notes="")
    f = flow(19_225_546, 4_219_774_900, 5_913_566_776, 21_426, 25_824)
    add(obs_id="PRC-O-010", provider="Ren (Renaissance Administration / Renaissance Acquisition Co)", payer="Renaissance Charitable Foundation (related party)", payee="Ren",
        service_scope="Contribution & grant processing, accounting, reporting, donor service, regulatory/tax reporting, charitable planning; RCF has 0 employees",
        scope_category="bundled", fee_basis="98% of administrative fee revenue from individual fundholder accounts (audited Note 9)", fee_value=19_225_546, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF value/count FY2023-FY2024", f=f, minimum_fee="$250/account (donor schedule)", tiers="donor 65/35/25/20 bps (PRC-O-011)", period="FY2024",
        source="https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf Note 9; "+X.format("202543189349301959"), quality="A", comp="medium",
        notes="Related-party fee-share: servicer captures ~all sponsor economics (RCF admin fee revenue $19.62m = 38.7 bps of avg DAF assets). Price is the donor fee, not an arm's-length servicer price.")
    add(obs_id="PRC-O-011", provider="Renaissance Charitable Foundation / Ren Direct retail", payer="Donor DAF account", payee="RCF (98% passed to Ren)",
        service_scope="Retail Ren DAF administration", scope_category="bundled", fee_basis="marginal tiers on account value", fee_value="65/35/25/20 bps; >$5M contact", fee_unit="bps/yr",
        denominator_basis="per-account balance", f=dict(bps_avg=sched(REN_RETAIL,250), usd_acct="see bps cell", arith="marginal tiers, $250 min"), minimum_fee="$250/account/yr",
        tiers="0-500k 0.65%; 500k-1M 0.35%; 1-2.5M 0.25%; 2.5-5M 0.20%", period="accessed 2026-11-25", source="https://www.reninc.com/ren-direct/ ; AMPF circular https://www.reninc.com/wp-content/uploads/2026/05/AMPF-Program-Circular-11-24.pdf", quality="A",
        comp="low", notes="DONOR fee, not servicer price; useful as ceiling of what the Ren bundle extracts per account.")
    f = flow(801_302, 493_554_856, 708_360_865, 1_316, 1_793)
    add(obs_id="PRC-O-012", provider="Ren ('RENAISSANCE')", payer="Stifel Charitable Inc (0 employees)", payee="Ren", service_scope="'OPS SYSTEM & SERVICE' (platform + operations services); staffing & facilities separately from Stifel Trust Co ($723k), Advent interface ($250k)",
        scope_category="staffed_admin", fee_basis="990 Part VII-B", fee_value=801_302, fee_unit="USD/yr", denominator_basis="avg EOY DAF FY2024/FY2025", f=f, minimum_fee="unknown", tiers="unknown", period="FY2025 (CY)",
        source=X.format("202642609349301859")+" ; "+X.format("202542269349303159"), quality="A", comp="medium", notes="Partial outsourcing: sponsor-affiliate supplies staff. Fast-growing program (+43% assets).")
    f = flow(498_305, 215_663_069, 493_554_856, 977, 1_316)
    add(obs_id="PRC-O-013", provider="Ren", payer="Stifel Charitable", payee="Ren", service_scope="as PRC-O-012", scope_category="staffed_admin", fee_basis="990 Part VII-B", fee_value=498_305, fee_unit="USD/yr",
        denominator_basis="avg EOY FY2023/FY2024", f=f, minimum_fee="unknown", tiers="unknown", period="FY2024", source=X.format("202542269349303159"), quality="A", comp="medium",
        notes="Avg is distorted by +129% asset jump in year; EOY basis lower")
    f = flow(801_302 + 723_213 + 250_398, 493_554_856, 708_360_865, 1_316, 1_793)
    add(obs_id="PRC-O-014", provider="Ren + Stifel Trust Co + Advent (stack)", payer="Stifel Charitable", payee="multiple", service_scope="Combined administration stack: platform/ops (Ren) + staffing & facilities (Stifel Trust) + interface software (Advent)",
        scope_category="bundled", fee_basis="sum of three Part VII-B lines", fee_value=801_302 + 723_213 + 250_398, fee_unit="USD/yr", denominator_basis="avg EOY DAF FY2024/FY2025", f=f, minimum_fee="", tiers="",
        period="FY2025", source=X.format("202642609349301859"), quality="B", comp="high", notes="Closest analogue of what a staffed servicer would replace at a mid-size bank-channel sponsor; excludes $2.97m investment management and $1.07m accounting fees.")
    f = flow(2_495_829, 4_996_956_535, 5_683_681_676, 29_988, 31_943)
    add(obs_id="PRC-O-015", provider="Stellar Technology Solutions (Ren/iPhi)", payer="National Christian Charitable Foundation (285 employees)", payee="Stellar", service_scope="Software/consulting; sponsor staffs operations in-house",
        scope_category="software", fee_basis="990 Part VII-B", fee_value=2_495_829, fee_unit="USD/yr", denominator_basis="avg EOY DAF FY2023/FY2024", f=f, minimum_fee="unknown", tiers="unknown", period="FY2024",
        source=X.format("202513109349303201"), quality="A", comp="low", notes="Line rose from $1.20m (2022) to $2.50m (2024): may include project/implementation work")
    f = flow(270_307, 487_520_202, 594_270_055, 7_786, 8_346)
    add(obs_id="PRC-O-016", provider="Stellar (Ren)", payer="Thrivent Charitable Impact & Investing", payee="Stellar", service_scope="Technology services; admin staff via Thrivent Financial ($4.79m) and own payroll",
        scope_category="software", fee_basis="990 Part VII-B", fee_value=270_307, fee_unit="USD/yr", denominator_basis="avg EOY DAF", f=f, minimum_fee="unknown", tiers="unknown", period="FY2024", source=X.format("202512589349301891"), quality="A", comp="low", notes="")
    f = flow(479_172, 594_270_055, 700_414_467, 8_346, 9_198)
    add(obs_id="PRC-O-017", provider="Renaissance Acquisition Co (Ren)", payer="Thrivent Charitable", payee="Ren", service_scope="Technology services", scope_category="software", fee_basis="990 Part VII-B", fee_value=479_172, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF", f=f, minimum_fee="unknown", tiers="unknown", period="FY2025", source=X.format("202612669349300236"), quality="A", comp="low", notes="+77% vs 2024 Stellar line (rebrand/migration or scope change)")
    f = flow(6_017_074, 594_270_055, 700_414_467, 8_346, 9_198)
    add(obs_id="PRC-O-018", provider="Thrivent Financial (affiliate)", payer="Thrivent Charitable", payee="Thrivent Financial", service_scope="'ADMIN & MANAGEMENT SERVICES' to an entity that also runs gift annuities/trusts and life-insurance gift programs",
        scope_category="bundled", fee_basis="990 Part VII-B", fee_value=6_017_074, fee_unit="USD/yr", denominator_basis="avg EOY DAF (net assets avg $872m would give ~69 bps)", f=f, minimum_fee="", tiers="", period="FY2025",
        source=X.format("202612669349300236"), quality="B", comp="low", notes="Affiliate cost allocation, scope wider than DAF; shows faith/affiliate programs carry high admin cost per DAF")
    f = flow(259_797, 596_807_813, 645_496_766, 4_232, 4_343)
    add(obs_id="PRC-O-019", provider="Ren PSG", payer="T. Rowe Price Program for Charitable Giving", payee="Ren PSG", service_scope="Technology", scope_category="software", fee_basis="990 Part VII-B", fee_value=259_797, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF FY2024/FY2025 (FYE Mar)", f=f, minimum_fee="unknown", tiers="unknown", period="FY2025 (FYE 2025-03-31)", source=X.format("202501959349302200"), quality="A", comp="low", notes="Stable $212k-$301k 2022-2025")
    f = flow(1_426_947, 596_807_813, 645_496_766, 4_232, 4_343)
    add(obs_id="PRC-O-020", provider="T. Rowe Price Associates (affiliate)", payer="T. Rowe Price Program", payee="T. Rowe Price Associates", service_scope="'INVESTMENT MGMT, ADMIN' (bundled affiliate)", scope_category="bundled",
        fee_basis="990 Part VII-B", fee_value=1_426_947, fee_unit="USD/yr", denominator_basis="avg EOY DAF", f=f, minimum_fee="", tiers="", period="FY2025", source=X.format("202501959349302200"), quality="B", comp="low",
        notes="Combined with Ren tech: ~27 bps all-in admin+inv mgmt supplier cost; sponsor also has $460k salaries")
    f = flow(172_604, 517_203_120, 636_396_163, 699, 763)
    add(obs_id="PRC-O-021", provider="Stellar (Ren)", payer="Goldman Sachs Charitable Gift Fund", payee="Stellar", service_scope="Information technology", scope_category="software", fee_basis="990 Part VII-B", fee_value=172_604, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF", f=f, minimum_fee="unknown (small program: per-account cost high => likely platform minimum)", tiers="unknown", period="FY2025 (FYE Jun)", source=X.format("202611249349302616"), quality="A", comp="low",
        notes="$139k-$173k flat across 4 years while accounts grew => behaves like a fixed minimum")
    f = flow(875_665, 517_203_120, 636_396_163, 699, 763)
    add(obs_id="PRC-O-022", provider="Charities Aid Foundation America", payer="Goldman Sachs Charitable Gift Fund", payee="CAF America", service_scope="Grant administration (outsourced grant due diligence/processing)", scope_category="staffed_admin",
        fee_basis="990 Part VII-B", fee_value=875_665, fee_unit="USD/yr", denominator_basis="avg EOY DAF", f=f, minimum_fee="unknown", tiers="unknown", period="FY2025", source=X.format("202611249349302616"), quality="A", comp="medium",
        notes="Rose from $217k (FY2022) to $876k: grant-volume / international mix driven; outsourced grant admin alone ~15 bps here")
    f = flow(336_481, 923_448_659, 1_035_684_715, 5_181, 5_293)
    add(obs_id="PRC-O-023", provider="Stellar (Ren)", payer="The Ayco Charitable Foundation", payee="Stellar", service_scope="Software provider", scope_category="software", fee_basis="990 Part VII-B", fee_value=336_481, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF", f=f, minimum_fee="unknown", tiers="unknown", period="FY2023", source=X.format("202413109349304401"), quality="A", comp="low", notes="Not listed in FY2024 return (below top-5/$100k or moved)")
    f = flow(1_730_728, 1_035_684_715, 1_158_002_128, 5_293, 5_585)
    add(obs_id="PRC-O-024", provider="The Ayco Company LP (Goldman affiliate)", payer="The Ayco Charitable Foundation (0 employees)", payee="Ayco Co LP", service_scope="'ADMIN/INVST ADVISORY'", scope_category="bundled",
        fee_basis="990 Part VII-B", fee_value=1_730_728, fee_unit="USD/yr", denominator_basis="avg EOY DAF", f=f, minimum_fee="", tiers="", period="FY2024", source=X.format("202543109349303959"), quality="B", comp="medium",
        notes="Affiliate staffed admin + investment advisory at ~16 bps / $319 per account")
    f = flow(1_026_306, 8_870_260_766, 12_640_914_117, 3_461, 4_134)
    add(obs_id="PRC-O-025", provider="The Ayco Company LP (Goldman affiliate)", payer="GS Donor Advised Philanthropy Fund (0 employees)", payee="Ayco Co LP", service_scope="'ADMIN. SERVICES' for ultra-high-balance accounts (avg ~$2.8m/acct)",
        scope_category="staffed_admin", fee_basis="990 Part VII-B", fee_value=1_026_306, fee_unit="USD/yr", denominator_basis="avg EOY DAF CY2023/CY2024", f=f, minimum_fee="", tiers="", period="FY2024 (CY)", source=X.format("202503109349303645"), quality="B", comp="medium",
        notes="Affiliate price ~1 bps but $270/account: admin cost scales with accounts, not assets. GS Trust Co ($14.6m) and GS & Co tech & inv adv ($8.1m) separate.")
    f = flow(390_398, 8_619_061_131, 7_457_452_054, 2_615, 3_030)
    add(obs_id="PRC-O-026", provider="Stellar (Ren)", payer="GS Donor Advised Philanthropy Fund", payee="Stellar", service_scope="Software provider", scope_category="software", fee_basis="990 Part VII-B", fee_value=390_398, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF", f=f, minimum_fee="unknown", tiers="unknown", period="FY2022", source=X.format("202312859349302266"), quality="A", comp="low", notes="By 2024 'Sapient' $824k technology listed instead")
    f = flow(185_921, 25_584_648, 215_283_755, 228, 228)
    add(obs_id="PRC-O-027", provider="TIFIN Give LLC", payer="GiveClear Foundation (0 employees)", payee="TIFIN Give", service_scope="'Technical and Charitable Support Services' (platform + admin services; GiveClear approves grants; Chariot disburses)",
        scope_category="staffed_admin", fee_basis="990 Part VII-B", fee_value=185_921, fee_unit="USD/yr", denominator_basis="avg of BOY net assets (proxy for opening DAF value, $25.6m) and EOY DAF value; EOY count only",
        f=f, minimum_fee="unknown", tiers="ADV: 30 bps <=$1M accts; 10-20 bps >$1M", period="FY2024", source=X.format("202533199349302978"), quality="B", comp="high",
        notes="Assets grew 8x in year, so the average is unreliable: plausible range 8.6 bps (EOY) to ~15 bps; per-account $815 on 228 accounts. Repo notes had said no TIFIN payment found; it is in Part VII-B.")
    add(obs_id="PRC-O-028", provider="TIFIN Give (SEC RIA)", payer="DAF sponsor ('Client'), billed on each DAF account's average daily balance", payee="TIFIN Give",
        service_scope="'Administrative, Technology and Services Fee' + separate investment Management Fee; SaaS implementation + subscription for third-party platform users", scope_category="staffed_admin",
        fee_basis="bps of account average daily balance, by account size", fee_value="30 bps (accounts <=$1M); 10-20 bps (>$1M); + mgmt fee 10 bps / 3.34 bps", fee_unit="bps/yr",
        denominator_basis="per-account average daily balance", f=dict(bps_avg="30 (<=$1M); 10-20 (>$1M); 40 incl. mgmt fee small accts", usd_acct="$300 per $100k; $750 at $250k", arith="0.30% x balance"),
        minimum_fee="none disclosed; 'negotiable'", tiers="2 tiers by account size", period="ADV 2A dated 2026-09-04 (unchanged from 2025-03-31)",
        source="https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=1057059 (CRD 313261) ; https://tifin.com/wp-content/uploads/TIFIN-Give-Part-2A-of-Form-ADV-Brochure-2025.pdf", quality="A", comp="high",
        notes="Closest public LIST PRICE to the proposed offer. AUM $30.9m discretionary, $342m under advisement at 12/31/2025 (tiny vs Ren). Fees 'negotiable'; implementation and subscription amounts undisclosed; also earns model-sponsorship fees.")
    f = flow(179_875_837, 66_199_578_792, 85_481_718_948, 204_614, 224_884)
    add(obs_id="PRC-O-029", provider="FMR LLC affiliates (National Charitable Services etc.)", payer="Fidelity Charitable (0 employees)", payee="FMR LLC", service_scope="Administration/recordkeeping/donor service (brokerage/custody via Fidelity Brokerage Services; investment management fees separate $84.3m)",
        scope_category="bundled", fee_basis="Audited Note 7: amount equal to donor admin fees net of tier price credits; 990 Part IX line 11a", fee_value=179_875_837, fee_unit="USD/yr", denominator_basis="avg EOY DAF FY2024/FY2025",
        f=f, minimum_fee="$100/account (donor)", tiers="donor 60/30/20/15 ... (PRC-O-050)", period="FY2025 (FYE 2025-06-30)",
        source=X.format("202601389349301700")+" ; https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf Note 7", quality="A", comp="medium",
        notes="Part VII-B shows FMR $159.9m (cash basis/other split). Captive: affiliate also earns fund management. Market leader's effective admin price ~24 bps.")
    f = flow(3_916_396, 16_843_946_406, 21_949_164_416, 26_643, 27_660)
    add(obs_id="PRC-O-030", provider="The Vanguard Group (founder)", payer="Vanguard Charitable", payee="Vanguard Group", service_scope="Occupancy and administrative support/recordkeeping (Schedule L); Vanguard Charitable has 119 employees and other tech vendors",
        scope_category="bundled", fee_basis="Schedule L business transaction", fee_value=3_916_396, fee_unit="USD/yr", denominator_basis="avg EOY DAF FY2023/FY2024", f=f, minimum_fee="", tiers="", period="FY2024 (FYE Jun)",
        source=X.format("202511349349313096"), quality="A", comp="low", notes="Partial support service only; affiliate earns fund fees on 35/37 pools")
    f = flow(3_093_447_365 - 3_057_423_430, 16_843_946_406, 21_949_164_416, 26_643, 27_660)
    add(obs_id="PRC-O-031", provider="Vanguard Charitable (self-operated)", payer="Vanguard Charitable", payee="own staff + vendors (UST Global, Slalom, Salesforce, Vanguard)", service_scope="ALL non-grant operating cost (staff, IT, legal, marketing, governance); no investment-mgmt line",
        scope_category="bundled", fee_basis="Part IX total expenses minus grants (lines 1-3)", fee_value=3_093_447_365 - 3_057_423_430, fee_unit="USD/yr", denominator_basis="avg EOY DAF", f=f, minimum_fee="", tiers="", period="FY2024",
        source=X.format("202511349349313096"), quality="A", comp="medium", notes="Make-vs-buy benchmark: in-house all-in cost of a top-5 sponsor ~19 bps / $1,327 per account")
    f = flow(9_825_772, 40_935_691_414, 47_352_597_100, 112_188, 128_497)
    add(obs_id="PRC-O-032", provider="Charles Schwab & Co (founder)", payer="Schwab Charitable / DAFgiving360 (226 employees)", payee="Charles Schwab & Co", service_scope="Brokerage & administrative services", scope_category="bundled",
        fee_basis="990 Part VII-B (Schedule L shows $11,431,175)", fee_value=9_825_772, fee_unit="USD/yr", denominator_basis="avg EOY DAF FY2024/FY2025", f=f, minimum_fee="", tiers="", period="FY2025 (FYE Jun)",
        source=X.format("202611199349300601"), quality="A", comp="low", notes="Affiliate charge is a small slice; most cost is in-house")
    f = flow(9_021_577_700 - 8_872_852_963 - 61_372_858, 40_935_691_414, 47_352_597_100, 112_188, 128_497)
    add(obs_id="PRC-O-033", provider="Schwab Charitable (self-operated)", payer="Schwab Charitable", payee="own staff + vendors", service_scope="All non-grant operating cost EXCLUDING line 11f investment management fees ($61.4m); includes advertising $6.9m, UBIT $2.2m",
        scope_category="bundled", fee_basis="Part IX total - grants - line 11f", fee_value=9_021_577_700 - 8_872_852_963 - 61_372_858, fee_unit="USD/yr", denominator_basis="avg EOY DAF", f=f, minimum_fee="", tiers="", period="FY2025",
        source=X.format("202611199349300601"), quality="A", comp="medium", notes="Make-vs-buy benchmark ~20 bps / $726 per account")
    f = flow(6_575_730_481 - 6_415_072_479 - 93_771_463, 42_119_335_128, 55_895_378_438, 17_940, 20_691)
    add(obs_id="PRC-O-034", provider="National Philanthropic Trust (self-operated)", payer="NPT", payee="own staff (310) + vendors", service_scope="All non-grant operating cost excluding investment management fees ($93.8m); includes foreign tax, bank charges",
        scope_category="bundled", fee_basis="Part IX total - grants - line 11f", fee_value=6_575_730_481 - 6_415_072_479 - 93_771_463, fee_unit="USD/yr", denominator_basis="avg EOY DAF FY2024/FY2025", f=f, minimum_fee="", tiers="", period="FY2025 (FYE Jun)",
        source=X.format("202601289349302480"), quality="A", comp="medium", notes="Large-balance national (avg $2.5m/acct): ~14 bps but $3,463 per account")
    f = flow(24_062_159, 3_826_325_338, 4_733_931_424, 15_208, 17_840)
    add(obs_id="PRC-O-035", provider="Bank of America N.A. (corporate trustee)", payer="Bank of America Charitable Gift Fund (0 employees)", payee="Bank of America N.A.", service_scope="Trustee compensation; BofA Private Bank administers, Ren donorfirst portal behind it (subcontract unknown); essentially all non-grant expense",
        scope_category="bundled", fee_basis="990 Part VII-A institutional trustee reportable compensation", fee_value=24_062_159, fee_unit="USD/yr", denominator_basis="avg EOY DAF CY2023/CY2024", f=f, minimum_fee="donor $25k account minimum",
        tiers="donor 90/75/50/35/25/15/12/10 bps (flat first-dollar) + 12 bps inv mgmt", period="CY2024", source=X.format("202503219349318170")+" ; "+X.format("202520169349301042"), quality="B", comp="medium",
        notes="Bundled trustee+admin (+ possibly investment); sponsor fee schedule largely flows to the bank. BofA's payment to Ren not public.")
    f = flow(14_067_248, 1_885_934_923, 2_324_759_320, 9_714, 11_262)
    add(obs_id="PRC-O-036", provider="Raymond James Trust N.A. (founder)", payer="Raymond James Charitable Endowment Fund (0 employees)", payee="RJ Trust", service_scope="'ADMIN SVC & INV MGMT' bundled", scope_category="bundled",
        fee_basis="990 Part VII-B (Sched L $14,501,160)", fee_value=14_067_248, fee_unit="USD/yr", denominator_basis="avg EOY DAF FYE Mar-2024/Mar-2025", f=f, minimum_fee="", tiers="", period="FY2025 (FYE 2025-03-31)",
        source=X.format("202630489349300743")+" ; "+X.format("202520499349301607"), quality="A", comp="low", notes="Bundled with investment management")
    f = flow(7_098_777, 1_885_934_923, 2_324_759_320, 9_714, 11_262)
    add(obs_id="PRC-O-037", provider="Raymond James Trust N.A. (admin portion proxy)", payer="Raymond James Charitable", payee="RJ Trust (inferred)", service_scope="Part IX line 11a 'management' fees; inferred admin share of RJ Trust bundle (line 11f inv mgmt $8.33m)",
        scope_category="staffed_admin", fee_basis="990 Part IX line 11a", fee_value=7_098_777, fee_unit="USD/yr", denominator_basis="avg EOY DAF", f=f, minimum_fee="", tiers="", period="FY2025", source=X.format("202630489349300743"), quality="D", comp="medium",
        notes="Inference: 11a+11f = 15.43m vs RJ entities 14.71m; mapping 11a to admin is an assumption")
    f = flow(828_787, 962_967_262, 1_153_914_245, 1_672, 2_213)
    add(obs_id="PRC-O-038", provider="Renaissance Philanthropic Solutions Group (Ren)", payer="Servant Foundation (44 employees)", payee="RPSG", service_scope="'MANAGED SERVICES' (partial outsourcing; sponsor staffed)", scope_category="staffed_admin",
        fee_basis="990 Part VII-B", fee_value=828_787, fee_unit="USD/yr", denominator_basis="avg EOY DAF FYE Mar-2021/Mar-2022", f=f, minimum_fee="", tiers="", period="FY2022 (FYE 2022-03-31)", source=X.format("202320469349302877"), quality="A", comp="medium", notes="")
    f = flow(217_199, 43_484_042, 112_324_015, 165, 216)
    add(obs_id="PRC-O-039", provider="RenPSG", payer="Bradley Impact Fund (6 employees)", payee="RenPSG", service_scope="'FUND CONSULTING'", scope_category="staffed_admin", fee_basis="990 Part VII-B", fee_value=217_199, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF", f=f, minimum_fee="", tiers="", period="FY2022", source=X.format("202323199349323507"), quality="B", comp="medium", notes="Small sponsor: ~$1,100/acct and ~28 bps => effective minimum fee behaviour")
    f = flow(500_842, 392_802_045, 432_290_493, 257, 254)
    add(obs_id="PRC-O-040", provider="Renaissance Administration LLC", payer="Jewish Federation of Greater Philadelphia", payee="Renaissance Administration", service_scope="'INVESTMENT ADMINISTRATIVE SRVCS' (endowment/foundation admin, not DAF-only)", scope_category="staffed_admin",
        fee_basis="990 Part VII-B", fee_value=500_842, fee_unit="USD/yr", denominator_basis="avg total NET ASSETS (DAF only $123m)", f=f, minimum_fee="", tiers="", period="FY2025 (FYE Aug)", source=X.format("202601679349301260"), quality="B", comp="low",
        notes="Per-account figure uses DAF count only and overstates; bps on net assets ~12")
    f = flow(155_909, 80_293_378, 88_360_079, 53, 53)
    add(obs_id="PRC-O-041", provider="Ren", payer="Jewish Federation of Greater Seattle", payee="Ren", service_scope="'ENDOWMENT PLATFORM SERVICE'", scope_category="software", fee_basis="990 Part VII-B", fee_value=155_909, fee_unit="USD/yr",
        denominator_basis="avg total NET ASSETS", f=f, minimum_fee="", tiers="", period="FY2025", source=X.format("202601359349310185"), quality="B", comp="low", notes="Small client floor ~$135-157k/yr 2022-2025 => platform minimum")
    f = flow(379_358, 383_552_124, 384_080_065, 280, 283)
    add(obs_id="PRC-O-042", provider="Renaissance", payer="Greater Miami Jewish Federation", payee="Renaissance", service_scope="'FOUNDATION ADMIN SVC'", scope_category="staffed_admin", fee_basis="990 Part VII-B", fee_value=379_358, fee_unit="USD/yr",
        denominator_basis="avg total NET ASSETS", f=f, minimum_fee="", tiers="", period="FY2023 (FYE Jun)", source=X.format("202421369349315457"), quality="B", comp="low", notes="")
    f = flow(366_469, 536_840_914, 674_316_911, 1_018, 1_227)
    add(obs_id="PRC-O-043", provider="Stellar (Ren)", payer="Christian Community Foundation (WaterStone; 26 employees)", payee="Stellar", service_scope="Computer & software", scope_category="software", fee_basis="990 Part VII-B", fee_value=366_469, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF", f=f, minimum_fee="", tiers="", period="FY2025 (FYE Mar)", source=X.format("202610409349301411"), quality="A", comp="low", notes="")
    f = flow(118_458, 121_124_940, 133_529_927, 455, 471)
    add(obs_id="PRC-O-044", provider="Stellar (Ren)", payer="Community Foundation of Acadiana", payee="Stellar", service_scope="Software support/technology for all fund types", scope_category="software", fee_basis="990 Part VII-B", fee_value=118_458, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF (net assets avg $158m => 7.5 bps)", f=f, minimum_fee="", tiers="", period="FY2024", source=X.format("202503169349308100"), quality="B", comp="low", notes="Flat ~$118-124k: floor price for a small CF")
    f = flow(203_595, 312_724_905, 350_752_697, 988, 1_044)
    add(obs_id="PRC-O-045", provider="Ren Technology Services", payer="Community Foundation of Greater Des Moines", payee="Ren", service_scope="Software services (all fund types)", scope_category="software", fee_basis="990 Part VII-B", fee_value=203_595, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF (net assets avg $840m => 2.4 bps)", f=f, minimum_fee="", tiers="", period="FY2024", source=X.format("202503149349303740"), quality="B", comp="low", notes="")
    f = flow(416_391, 408_359_695, 493_328_839, 674, 690)
    add(obs_id="PRC-O-046", provider="Stellar (Ren)", payer="The Cleveland Foundation", payee="Stellar", service_scope="Hosting & customizations - software licence (all fund types)", scope_category="software", fee_basis="990 Part VII-B", fee_value=416_391, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF (net assets $2.87b => ~1.5 bps)", f=f, minimum_fee="", tiers="", period="FY2024", source=X.format("202543189349305969"), quality="B", comp="low", notes="")
    f = flow(311_878, 37_197_551, 42_967_492, 149, 157)
    add(obs_id="PRC-O-047", provider="Stellar (Ren)", payer="Catholic Community Foundation (EIN 38-3941057)", payee="Stellar", service_scope="'PAYMENT PROCESSING' (label; likely platform)", scope_category="payments", fee_basis="990 Part VII-B", fee_value=311_878, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF (net assets avg $93m => 33 bps)", f=f, minimum_fee="", tiers="", period="FY2024", source=X.format("202533179349310063"), quality="B", comp="low", notes="Outlier; scope label unclear")
    f = flow(232_315, 2_717_438_439, 2_896_880_396, 2_083, 2_197)
    add(obs_id="PRC-O-048", provider="Stellar (Ren)", payer="ImpactAssets", payee="Stellar", service_scope="Technology services", scope_category="software", fee_basis="990 Part VII-B", fee_value=232_315, fee_unit="USD/yr",
        denominator_basis="avg EOY DAF", f=f, minimum_fee="", tiers="", period="FY2024", source=X.format("202543169349307999"), quality="A", comp="low", notes="")
    add(obs_id="PRC-O-049", provider="Benevity", payer="American Online Giving Foundation", payee="Benevity", service_scope="Workplace-giving processing ('ADMINISTRATIVE SVCS')", scope_category="payments", fee_basis="990 Part VII-B vs DAF grants",
        fee_value=45_968_145, fee_unit="USD/yr", denominator_basis="Schedule D DAF grants FYE Mar-2024 ($1,950,227,494); assets not meaningful (pass-through)", f=dict(bps_avg="n/a (2.36% of grant flow)", usd_acct=round(45_968_145/720_545), arith="45,968,145/1,950,227,494 = 2.36% of grants; /720,545 accounts = $64"),
        minimum_fee="", tiers="", period="FY2024 (FYE 2024-03-31)", source=X.format("202440469349301209") if False else "data/mission-2026-11-14/form990-contractors-harvest-full.csv (AOGF FY2024 row) ; IRS XML via return_object_id in that file", quality="B", comp="none",
        notes="Flow-priced processing; FY2025 payment $54.45m. Not comparable to AUA pricing.")
    add(obs_id="PRC-O-050", provider="Fidelity Charitable (donor fee)", payer="Donor", payee="Fidelity Charitable (passed to FMR net of credits)", service_scope="Retail DAF admin", scope_category="bundled", fee_basis="marginal tiers, average balance",
        fee_value="60/30/20/15 bps (<$5M); flat schedule >=$5M down to 11.5 bps at $75-100M", fee_unit="bps/yr", denominator_basis="per-account balance", f=dict(bps_avg=sched(FID,100), usd_acct="see bps cell", arith="marginal tiers, $100 min"),
        minimum_fee="$100/yr", tiers="see fee_value", period="accessed 2026-11-14 (repo)", source="https://www.fidelitycharitable.org/giving-account/what-it-costs.html ; data/mission-2026-11-14/sponsor-fee-schedules.csv", quality="A", comp="none",
        notes="DONOR fee. Effective realized 23.7 bps (PRC-O-029) vs 60 bps headline => headline donor fees overstate sponsor economics ~2.5x")
    add(obs_id="PRC-O-051", provider="Charityvest (sponsor) / Foundation Source (tech)", payer="Donor (invested accounts only)", payee="Charityvest Inc.", service_scope="Retail DAF admin; cash accounts free", scope_category="bundled", fee_basis="marginal tiers",
        fee_value="60/30/20/15/10 bps; custom >$10M", fee_unit="bps/yr", denominator_basis="per-account balance", f=dict(bps_avg=sched(CV,100), usd_acct="see bps cell", arith="marginal tiers, $100 min"), minimum_fee="$100/yr (invested)", tiers="see fee_value",
        period="accessed 2026-11-25", source="https://pcadafguide.foundationsource.com/how-client-fees-work", quality="A", comp="none", notes="Page inconsistently also says 'starting at 45bps'. Foundation Source's take from Charityvest not public.")
    add(obs_id="PRC-O-052", provider="Columbus Foundation -> Foundant", payer="Columbus Foundation", payee="Foundant Technologies", service_scope="Operating platform services (all ~3,400 component funds)", scope_category="software", fee_basis="990 Part VII-B / total funds",
        fee_value=344_614, fee_unit="USD/yr", denominator_basis="~3,400 component funds (audited statements per Unbound evb)", f=dict(bps_avg="n/a", usd_acct=101, arith="344,614/3,400 = $101 per fund-year"), minimum_fee="", tiers="quote-only list price",
        period="TY2024", source="/home/user/unbound/requirements/convergence/2026-11-24-master/data/evidence-backlog/evb-market-prices-rails.jsonl", quality="B", comp="low", notes="Community-foundation software per-fund anchor (repo-derived, not re-fetched)")
    add(obs_id="PRC-O-053", provider="Foundant professional services", payer="Sponsor", payee="Foundant", service_scope="Implementation/training/consulting rate card", scope_category="implementation", fee_basis="hourly / per day",
        fee_value="$250/h consulting; $2,500 per trainer-day onsite; new-admin training $500-2,500; optimization $1,000-1,750", fee_unit="USD", denominator_basis="per engagement", f=dict(bps_avg="", usd_acct="", arith=""),
        minimum_fee="", tiers="", period="2025-26 (repo)", source="/home/user/daf-landscape/research/commercial-opportunity/competitive-landscape/competition-and-pricing.md:164", quality="C", comp="medium", notes="Only public DAF/CF vendor services rate card found")
    add(obs_id="PRC-O-054", provider="Daffy", payer="Donor / employer", payee="Daffy Charitable Fund", service_scope="Consumer DAF membership; Daffy for Work employer plan", scope_category="bundled", fee_basis="flat monthly per fund",
        fee_value="$0-40/month donor; $3/employee/month (Daffy for Work)", fee_unit="USD/month", denominator_basis="per fund", f=dict(bps_avg="n/a", usd_acct="36-480", arith="$3-40 x 12"), minimum_fee="", tiers="Supporter/Contributor/Family/Benefactor/Philanthropist",
        period="2026", source="https://help.daffy.org/en/articles/6323771-what-are-daffy-s-membership-fees ; Unbound evb jsonl", quality="B", comp="none", notes="Per-account pricing precedent: $36-480/fund-yr all-in donor price")
    add(obs_id="PRC-O-055", provider="Chariot", payer="Nonprofit (DAFpay) / grantmaker (Disbursements)", payee="Chariot", service_scope="DAFpay checkout 2.9%; Components $199/mo + 2.9%; Mailroom $50/mo + $1.50/item; Disbursements fee to grantmaker not public", scope_category="payments",
        fee_basis="transaction % / subscription", fee_value="2.9%", fee_unit="% of donation", denominator_basis="per transaction", f=dict(bps_avg="n/a", usd_acct="n/a", arith=""), minimum_fee="", tiers="Enterprise custom",
        period="accessed 2026-11-25", source="https://www.givechariot.com/chariot-pricing", quality="A", comp="none", notes="Payments are a separately priced layer; a servicer must decide whether grant-payment rails are inside its 20 bps")
    add(obs_id="PRC-O-056", provider="Voya (recordkeeper) - Nashville & Davidson County 457 plan", payer="Plan participants/plan", payee="Voya", service_scope="DC plan recordkeeping incl. trust/custody (outsourcing analog, not DAF)", scope_category="staffed_admin",
        fee_basis="fixed % of plan assets", fee_value="0.07% -> 0.05% (post 2025-10-01)", fee_unit="bps/yr", denominator_basis="plan assets $505.5m / 8,096 participants (avg $62.4k)",
        f=dict(bps_avg="7 -> 5", usd_acct="44 -> 31", arith="355,621/8,096 = $44; 0.05% x 505.5m / 8,096 = $31"), minimum_fee="", tiers="", period="2024-2025",
        source="https://www.nashville.gov/sites/default/files/2025-11/Nashville_2025_DC_Plan_Fee_Survey.pdf p6", quality="A", comp="low", notes="Outsourcing analog: per-account recordkeeping price $31-44; NEPC 2025 survey median $42/participant (down 26% from $57 in 2016, same deck)")
    add(obs_id="PRC-O-057", provider="U.S. Bancorp Fund Services", payer="Fund (BDC)", payee="USBFS", service_scope="Fund administration & fund accounting (compliance, SEC/financial/tax reporting) (outsourcing analog, not DAF)", scope_category="staffed_admin",
        fee_basis="tiered bps on gross assets per fund", fee_value="6.0 / 4.0 / 3.0 bps (first $250m / next $250m / above $500m)", fee_unit="bps/yr", denominator_basis="gross assets per fund",
        f=dict(bps_avg="3-6", usd_acct="n/a", arith=""), minimum_fee="$60,000 per entity portfolio; annual CPI escalator", tiers="see fee_value", period="form of agreement dated 2018-03-01",
        source="https://www.sec.gov/Archives/edgar/data/1719606/000121390019004827/f10k2018ex10-2_pharoscap.htm", quality="A", comp="low", notes="Commercial template precedent: tiered bps + contractual minimum + CPI + 'extraordinary services quoted separately'")
    add(obs_id="PRC-O-058", provider="RCF extraordinary services", payer="Donor account", payee="RCF/Ren", service_scope="Foreign grants, 509(a)(3) grants, orgs without 509(a) letter, fundraising events", scope_category="manual", fee_basis="additional fees, amount not stated",
        fee_value="unstated", fee_unit="", denominator_basis="per event", f=dict(bps_avg="", usd_acct="", arith=""), minimum_fee="", tiers="", period="2023 circular (posted 2026-05)",
        source="https://www.reninc.com/wp-content/uploads/2026/05/AMPF-Program-Circular-11-24.pdf p6", quality="A", comp="medium", notes="Market norm: exceptions priced outside the bps fee")
    add(obs_id="PRC-O-059", provider="National Christian Foundation (donor fee extras)", payer="Donor", payee="NCF", service_scope="Minimum fee and wire-grant fee", scope_category="manual", fee_basis="flat", fee_value="$30/month minimum ($360/yr); $25 per wired grant",
        fee_unit="USD", denominator_basis="per account / per grant", f=dict(bps_avg="", usd_acct=360, arith="30x12"), minimum_fee="$360/yr", tiers="", period="accessed 2026-11-14 (repo)", source="https://www.ncfgiving.com/fees/ ; data/mission-2026-11-14/sponsor-fee-schedules.csv", quality="B", comp="none", notes="")
    return R

COLS = ["obs_id","provider","payer","payee","service_scope","scope_category","fee_basis","fee_value","fee_unit","denominator_basis","implied_bps_avg_assets","implied_usd_per_account_year",
        "minimum_fee","tiers","period","source_url_or_path","quality","comparability_to_20bps_staffed_admin","notes"]

def to_csv_row(r):
    f = r["f"]
    note = r["notes"]
    if "arith" in f and f["arith"]: note = (note + " | [D] " + f["arith"]).strip(" |")
    return dict(obs_id=r["obs_id"], provider=r["provider"], payer=r["payer"], payee=r["payee"], service_scope=r["service_scope"], scope_category=r["scope_category"],
                fee_basis=r["fee_basis"], fee_value=r["fee_value"], fee_unit=r["fee_unit"], denominator_basis=r["denominator_basis"],
                implied_bps_avg_assets=f.get("bps_avg",""), implied_usd_per_account_year=f.get("usd_acct",""), minimum_fee=r["minimum_fee"], tiers=r["tiers"],
                period=r["period"], source_url_or_path=r["source"], quality=r["quality"], comparability_to_20bps_staffed_admin=r["comp"], notes=note)

if __name__ == "__main__":
    out = sys.argv[1]
    data = rows()
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader()
        for r in data: w.writerow(to_csv_row(r))
    json.dump([dict(id=r["obs_id"], prov=r["provider"][:40], cat=r["scope_category"], comp=r["comp"], **{k:v for k,v in r["f"].items() if k!="arith"}) for r in data], open(out+".summary.json","w"), indent=0, default=str)
    print(len(data))
