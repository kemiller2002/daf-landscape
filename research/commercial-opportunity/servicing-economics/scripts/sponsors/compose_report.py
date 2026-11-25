#!/usr/bin/env python3
"""Compose report.jsonl for group SPN from the outputs of build_sponsor_economics.py (deterministic; no network)."""
import json
import math
import os
import sys

import pandas as pd

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
rd = lambda f: pd.read_csv(os.path.join(OUT, f), dtype={"ein": str})  # noqa: E731
E, CA, T, SS, U, SEG, PRM, W = (rd(f) for f in ("sponsor-economics.csv", "customer-attractiveness.csv", "top25-hypotheses.csv",
                                                "self-sustaining-candidates.csv", "unattractive-large.csv", "segment-summary.csv",
                                                "cost-to-serve-parameters.csv", "attractiveness-weights.csv"))
ST = json.load(open(os.path.join(OUT, "summary-stats.json")))
m = lambda x: "n/a" if pd.isna(x) else f"${x/1e6:,.1f}m"  # noqa: E731
b = lambda x: "n/a" if pd.isna(x) else f"${x/1e9:,.2f}bn"  # noqa: E731
pct = lambda x: "n/a" if pd.isna(x) else f"{x:.0%}"  # noqa: E731
n0 = lambda x: "n/a" if pd.isna(x) else f"{x:,.0f}"  # noqa: E731


def table(df, cols, fmts):
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    rows = "".join("| " + " | ".join(f(r[c]) for c, f in zip(cols, fmts)) + " |\n" for _, r in df.iterrows())
    return head + rows


A = E[E["addressable"] == 1]
act = E[(E["status"] == "active") & (E["daf_assets_eoy"] > 0)]
C = ST["concentration"]
P = PRM.set_index("parameter")
sections = []
add = lambda t, md: sections.append({"section": t, "markdown": md})  # noqa: E731

add("Scope, labels and reproducibility", f"""Group SPN, 2026-11-25. Builds a one-row-per-EIN sponsor economics dataset and a customer-attractiveness model **only from existing repository files** (read-only, `/home/user/daf-landscape`, data as committed at access 2026-11-25). No web, no outreach. Labels: [S] repo-sourced value (path in `src_*`/evidence columns), [D] derived by stated arithmetic, [A] assumption (all in `cost-to-serve-parameters.csv` / `attractiveness-weights.csv`, replaceable), [E] estimate.

**Everything economic here is hypothetical servicing revenue on a PROXY for average billable AUA** (`avg_assets_proxy` = (prior-year EOY + latest EOY)/2 [D]); EOY run-rate is shown separately (`rev_20bps_eoy_runrate`). Donor-facing fees are carried only as context (`donor_fee_bps_at_100k_context`), never as servicer revenue. Schedule I recipient rows are never used as grant counts.

**Reproducibility.** `build_sponsor_economics.py` (pure functions, pandas) regenerates all CSV/JSONL outputs; `compose_report.py` regenerates this file. Verified 2026-11-25: three full runs (two fresh empty directories, where default parameter/weight CSVs are written then read back, plus the working directory where they are read) produced byte-identical sha256 for all 12 output files including this report. Cost parameters and weights are read back from their CSVs, so an integrator can replace values and re-run.

Same-model caveat: the classifications, parameters and weights are one analyst-model's choices; re-running them is not independent validation.""")

st = ST["status_counts"]
add("Universe and dedup method", f"""**Universe.** {ST['n_sponsors_total']:,} EIN rows = 1,594 EINs in the DAFRC 2025 sponsor dataset (`dafrc-sponsor-schedule-d-fy2019-2024.csv`, 8,751 sponsor-years FY2019-2024) + 3 pass-through/digital entities with no Schedule D panel (Bright Funds, Every.org, Goodstack; `pass-through-sponsors-2026.csv`, `digital-sponsor-entities-2026.csv`). The IRS XML harvests (`form990-returns-schedule-d-harvest-full.csv`, `form990-harvest-fy2025-refresh.csv`) contain no EIN outside the DAFRC list.

**Panel construction (per EIN-FY), in order:**
1. DAFRC values, then **2,564 applied corrections** from `dafrc-corrections-itemized.csv` (R1 filed replaces imputed; R2 terminated double count; R3 990 says no DAFs; R4 closed-but-filed adds rows). Rule codes kept per EIN-FY (`corr_rules_latest`, `src_*` = `corrected:R1...`).
2. IRS XML Schedule D Part I fills EIN-FYs absent or blank in DAFRC (FY2022-24: 1 asset fill) and supplies **FY2025** (refresh file preferred over the full harvest for duplicates; one return per EIN-FY = latest `return_ts`; only `xml_status=ok`; returns without Schedule D DAF values kept as a flag, not zero). FY2025 values: 886 EINs with DAF values; 88 FY2025 returns without Schedule D DAF values.
3. League-table corrected values (`daf-sponsor-league-table-fy2021-2025.csv`, value_basis corrected_R1_R4) override if different: **0 overrides needed** (panel equals league table); FY2025 matches `daf-sponsor-league-table-fy2025-refresh.csv` on all 30 filed rows. League correction/imputation flags carried (`league_corrections`, `league_imputed_kept`, `league25_flags`). Cross-check vs `daf-long-tail-sponsors-fy2021-2024.csv` FY2024 assets: 1 mismatch of 1,514 (EIN 721317054, DAFRC blank, long-tail 0, XML $101k; count screened out).
4. **Latest FY** = latest FY whose EOY assets are not DAFRC-imputed (fallback: imputed, flagged `latest_fy_basis`). Latest FY distribution: {ST['latest_fy_counts']}. Prior year = latest-1 (BOY proxy).

**Dedup / entity resolution.** EINs normalised to 9 digits; DAFRC has no duplicate EIN-FY; harvest duplicates (amended/superseding returns: 15 in full harvest, 3 in refresh) resolved by latest timestamp. Name changes: one row per EIN, `name` = latest filed name, `name_variants` lists all. **Mergers/exits** (flagged, never deleted): `merged_into` from R2 Schedule N notes (TIAA Charitable -> Renaissance Charitable Foundation FY2021; Jasper Ridge Charitable Fund -> Fidelity Charitable FY2022; Rusk County CF -> Eau Claire CF FY2023), Schedule N liquidations (`cf-exits-schedule-n-2021-2026.csv`, `cf-consolidation-2021-2026.csv`: e.g. Coastal CF -> San Diego Foundation 2024; National Christian Community Foundation -> NCF), and partial dispositions kept as notes. Related entities kept as separate EINs with `related_group_id` (GKCCF+Greater Horizons; Dechomai Trust+Foundation; Signatry pair; CCF-LA pair; NPT + NPT Charitable Asset Trust; Goldman-affiliated programs [D]).

**Status counts:** {st}. Active = latest FY >= 2023 [A], positive or zero assets, not exited. **Addressable** ({ST['n_addressable']:,}) = active, DAF assets > 0, and not captive in-house affiliate, vendor-captive or app-native in-house platform.""")

dq = ST["data_quality_counts"]
add("Data quality", f"""**Grades** (per EIN, `data_quality` + `data_quality_issues`): A {dq.get('A',0):,} / B {dq.get('B',0):,} / C {dq.get('C',0):,} / D {dq.get('D',0):,}. A = latest and prior filed, accounts pass screen; B = one non-severe issue (most often no prior year so BOY proxy = EOY); C = filed latest with several issues or a suspect count; D = latest assets imputed or missing.

Known issues handled:
- **Imputation**: 241 FY2024 EIN-rows still carry at least one DAFRC-imputed metric after R1-R4 (mostly accounts); latest-FY selection skips imputed assets.
- **Account-count screen** (repo league-table rule): counts > 1,000 averaging < $5/account blanked (3 EINs, e.g. Givinga 1.42m 'accounts' with $1.9m). `daf-reclassification-screen.csv` count-basis changes flagged (e.g. AOGF/Benevity, Give Back Foundation). New flag: <= 5 accounts with >= $5m average (e.g. CCF-LA Supporting Organization reports 1 account / $186m) -> grade C, excluded from top-25.
- **Accounts for costing**: Schedule D screened count; else EOY / segment median balance [E] (14 EINs).
- **Grant counts**: sponsor-published counts only (12 sponsors, `grant-count-denominators-2026-11-20.csv`; unit and period as stated, period mismatch flagged; SVCF count is all SVCF grants, not DAF-only). Elsewhere grant count = accounts x grants_per_account [A]. Calibration [D]: published counts / Schedule D accounts = {', '.join(f'{n[:22]} {v}' for n, v in ST['grant_count_calibration_grants_per_account'])}. Median ~7.3, used as base 7.
- **Non-DAF assets**: `total_assets_eoy` from the same 990 (or cost-structure file) vs DAF assets; `other_funds_*` from FY2025 Schedule D Part I col (b) where parsed; `total_funds_990` (tail CFs). DAF > total assets (consolidation/timing) flagged.
- **Vendor evidence**: 990 Part VII-B lists only top-5 contractors > $100k (floors; absence is not evidence of no vendor). Portal mapping is host/headers evidence (`cf-vendor-map-by-ein-v2.csv`); CT-log-only leads are treated as low. {(A['tech_vendor']!='unknown').sum():,} of {len(A):,} addressable sponsors have some vendor signal; {(A['tech_vendor']=='unknown').sum():,} unknown.
- **Average-AUA proxy**: across addressable sponsors avg proxy = {(A['avg_assets_proxy'].sum()/A['daf_assets_eoy'].sum()):.1%} of EOY (assets grew); billing on EOY run-rate would overstate revenue by ~9%.
- **Fiscal-year mix**: 'FY2025' = tax periods ending in 2025 (Jun-Dec mostly); some sponsors' latest is FY2024 (FY2025 not yet filed/parsed: AEF, RCF, NCF, GS DAF, MS GIFT, BofA among others).""")

seg = SEG[SEG["dimension"].isin(["segment", "all_active", "addressable"])]
add("Segment economics", "All active sponsors with DAF assets > 0 (captives included; see captive rows). Revenue on avg-assets proxy; cost = INCREMENTAL cost-to-serve (base [A] parameters; excludes the servicer's company fixed budget). `sponsor DAF opex/acct` = sponsor's own 990 operating cost allocated to DAFs by asset share (`sponsor-cost-structure.csv`) - a context ceiling, not our cost.\n\n"
    + table(seg, ["group", "n_sponsors", "n_addressable", "daf_assets_eoy_sum", "accounts_sum_screened", "pooled_avg_balance_eoy", "median_sponsor_avg_balance",
                  "rev_20bps_avg_proxy_sum", "margin_pct_20bps_base_pooled", "n_positive_margin_20bps_base", "n_self_sustaining_base", "median_breakeven_bps_base",
                  "median_sponsor_daf_opex_per_account_alloc_990", "pooled_payout_boy", "median_assets_cagr_3y"],
            [str, n0, n0, b, n0, n0, n0, m, pct, n0, n0, lambda x: f"{x:.0f}", n0, pct, pct])
    + f"""
Readings:
- **Nationals + financial affiliates hold most assets but are mostly not buyable.** Captive in-house affiliates (Fidelity, Schwab DAFgiving360, Vanguard) are {C['captive_inhouse_share_assets_active']:.1%} of active DAF assets; all non-addressable sponsors {C['not_addressable_share_assets_active']:.1%}.
- **Community foundations are the economic core of the addressable market**: high average balances (pooled ~$640k), low transaction intensity per $ AUA, and 279 of 783 CFs clear base incremental cost at 20 bps. But only CFs above ~$10m DAF assets ever clear the base $25k per-sponsor fixed cost; the smallest CF with positive base margin has {m(C['min_eoy_assets_positive_margin_base_cf'])} EOY DAF assets.
- **Single-issue 'other', universities/hospitals and donation processors are structurally negative** at 20 bps: small books (median breakeven 200-350+ bps) or tiny balances (processors pooled ~$2k).
- **Sponsor-own DAF opex** (median ~$3.8k/account CFs, ~255 bps of DAF assets by grants allocation) is 1-2 orders above the [A] incremental servicer cost (~$75-90/account). Either sponsors carry much work a servicer would not replace (development, community grantmaking, investment oversight) or the [A] parameters understate DAF admin work. This gap is the single largest open question for the activity-cost agent.""")

dist = pd.DataFrame(ST["balance_distribution"])
add("Distribution of accounts and balances", "Active sponsors with a screened account count, banded by sponsor-level average EOY balance:\n\n"
    + table(dist, ["sponsor_avg_balance_band", "n_sponsors", "accounts", "share_accounts", "daf_assets_eoy", "share_assets", "n_addressable", "n_positive_margin_20bps_base"],
            [str, n0, n0, pct, b, pct, n0, n0])
    + f"""
- **Small-account tail**: sponsors averaging < $10k hold **61% of all reported accounts but 0.1% of assets** - almost entirely pass-through/processor programs (AOGF/Benevity, PayPal, workplace funds). None has positive margin at 20 bps; their economics are per-transaction, not bps. Sponsors averaging $10k-50k (184, mostly small single-issue/faith) are also uniformly negative.
- **Concentrated high value**: sponsors averaging $250k-5m hold ~90% of assets with ~30% of accounts; 28 sponsors average >= $5m (often few-fund supporting/legacy vehicles; counts need checking).
- **Market concentration**: top 4 sponsors = {C['top4_share_assets_active']:.1%} of active DAF assets, top 10 = {C['top10_share_assets_active']:.1%}, top 50 = {C['top50_share_assets_active']:.1%}. Within the addressable set, top 10 = {C['addressable_top10_share_of_addressable_assets']:.1%} and top 50 = {C['addressable_top50_share_of_addressable_assets']:.1%} of addressable assets - a servicer's revenue pool is a few dozen sponsors.
- Volatility: median 3-yr asset CAGR ~7% (CFs) to ~19% (independent nationals); YoY volatility is in `assets_yoy_vol` per sponsor (most CFs < 15%; small sponsors very noisy).""")

F = float(P.at["self_sustain_fixed_cost_usd", "base"])
ssa = SS[(SS["addressable"] == 1) & (SS["self_sustaining_base"] == 1)]
clean = ssa[(ssa["captive_status"] == "none_found") & (ssa["recent_migration"] == 0)]
add("Who could sustain the company alone", f"""**Threshold (parameter `self_sustain_fixed_cost_usd`)**: a sponsor 'self-sustains' a lean servicer if 20 bps x avg-assets proxy - base incremental cost-to-serve >= **${F:,.0f}** = the lean fixed budget hypothesis in `daf-servicer-bottom-up-operating-budget-2026-11-25.md` (a hypothesis, not a measured cost). That needs roughly >= $0.65-0.7bn average DAF AUA at a CF-like balance mix.

- All sponsors passing at base: {int(SS['self_sustaining_base'].sum())} (low cost {int(SS['self_sustaining_low_cost'].sum())}, high cost {int(SS['self_sustaining_high_cost'].sum())}; after a 30% asset shock {int(SS['self_sustaining_after_shock'].sum())}).
- Addressable and passing at base: {len(ssa)}; of which unconstrained (no captive/affiliate flag) and not recently migrated: **{len(clean)}**.
- Unconstrained, passing at base: {', '.join(clean['name'].str.title().head(30))}.
- Robust to both high cost and a 30% shock (unconstrained): {', '.join(clean[(clean['self_sustaining_high_cost']==1)&(clean['self_sustaining_after_shock']==1)]['name'].str.title())}.

**Interpretation.** 'Could sustain' is arithmetic, not likelihood. Every one of these is a single-client dependency (one sponsor = 25-100%+ of a $5m [A] business; `concentration_share_of_X`), several sit on newly signed platforms, and the largest (NPT, ~20x threshold) would never pay 20 bps on $50bn+ - [A] judgment: a flat bps price is unlikely to hold above roughly $1-2bn and would need tiering or a cap (open question for the pricing agent). A one-sponsor company fails on that sponsor's exit; the realistic model is a portfolio of 5-15 mid-sized CF/faith sponsors, not an anchor.""")

port = A[(A["captive_status"] == "none_found") & (A["recent_migration"] == 0) & A["daf_assets_eoy"].between(1e8, 1.5e9) & (A["margin_20bps_base"] > 0)].merge(CA[["ein", "score_base"]], on="ein")
add("Attractive portfolio members", f"""Addressable, unconstrained, not recently migrated, $100m-$1.5bn EOY DAF assets, positive base margin: **{len(port)} sponsors**, {b(port['daf_assets_eoy'].sum())} EOY, {m(port['rev_20bps_avg_proxy'].sum())} hypothetical 20 bps revenue on the avg proxy, median score {port['score_base'].median():.1f}. By segment: {port['segment'].value_counts().to_dict()}. By platform signal: {port['tech_vendor'].str.slice(0,24).value_counts().head(8).to_dict()}.

Why this band: 20 bps revenue per sponsor ~$0.2-3m (no single one > ~60% of a $5m business), average balances $200k-1m (low cost per $), packaged platforms (Foundant, Ren/iPhi, akoyaGO, Foundation Cloud, GiftingNetwork) with known data export paths, and documented peer attrition from Ren/iPhi and Blackbaud/Foundation Cloud (`cf-vendor-migrations-2022-2026.csv`, `ren-iphi-attrition-summary.json`). Coverage arithmetic [D]: median member base margin at 20 bps = {m(port['margin_20bps_base'].median())} (median EOY {b(port['daf_assets_eoy'].median())}); covering the ${F:,.0f} fixed budget needs ~{math.ceil(F/port['margin_20bps_base'].median())} median members, ~{math.ceil(F/port['margin_20bps_after_shock_base'].median())} after a 30% shock, and ~{math.ceil(F/port['margin_20bps_after_shock_base'].median())+2} to also survive losing the largest client (+2 [A]) - before sales cost, onboarding (median {m(port['onboarding_cost_base'].median())} per sponsor [A]) and the per-account cost uncertainty.

**Weights and model** (`attractiveness-weights.csv`, 15 dimensions; base weights): revenue 0.14, contribution margin 0.13, contractual/captive 0.10, switching evidence 0.07, service workload 0.07, transaction intensity 0.06, strategic 0.06, evidence 0.06, complexity/config/migration/sales cycle 0.05 each, non-DAF accounting 0.04, concentration 0.04, accounts 0.03. AUA enters only through revenue and strategic size (<= ~0.16 combined). Sensitivity: Spearman vs equal/revenue-heavy/risk-heavy/cost-heavy weights {ST['sensitivity']['spearman_base_vs_equal']}/{ST['sensitivity']['spearman_base_vs_revenue_heavy']}/{ST['sensitivity']['spearman_base_vs_risk_heavy']}/{ST['sensitivity']['spearman_base_vs_cost_heavy']}; top-25 overlap {ST['sensitivity']['top25_overlap_base_vs_equal']}/{ST['sensitivity']['top25_overlap_base_vs_revenue_heavy']}/{ST['sensitivity']['top25_overlap_base_vs_risk_heavy']}/{ST['sensitivity']['top25_overlap_base_vs_cost_heavy']} of 25; 30 one-at-a-time (+/-50%) runs give `rank_oat_min/max` and `share_oat_runs_in_topn` per sponsor. High Spearman is inflated by the long stable tail; top-25 overlap is the meaningful stability measure.""")

U2 = U.copy()
add("Unattractive large sponsors", f"""Active sponsors with EOY DAF assets >= $1bn [A] that are economically or structurally unattractive ({len(U2)}; concentration alone does not qualify). Full reasons in `unattractive-large.csv`.\n\n"""
    + table(U2[["name", "daf_assets_eoy", "captive_status", "score_base", "reasons"]].assign(reasons=U2["reasons"].str.slice(0, 170)),
            ["name", "daf_assets_eoy", "captive_status", "score_base", "reasons"], [lambda x: str(x).title()[:42], b, str, lambda x: "" if pd.isna(x) else f"{x:.1f}", str])
    + "\nPattern: the largest AUA is either owned (FMR, Schwab, Vanguard, Ren/RCF), affiliated to wealth firms that already outsource to Ren (GS, MS, US Charitable Gift Trust), newly re-platformed (AEF on Ren 2026; Vanguard + Give Interactive 2025), custom-built (NCF, GKCCF, SVCF/Salesforce), or CFs where DAFs are a minority of a multi-fund ledger (NYCT, Columbus, California, Oregon CFs). Large AUA is a poor proxy for winnable, servable revenue.")

add("Top 25 hypotheses with caveats", """**These are desk hypotheses for validation, NOT sales leads**; no willingness to pay, mandate, budget or buying intent is inferred. Ranked by base score among addressable sponsors excluding recent migrations, custom in-house builds and data-quality C/D.\n\n"""
    + table(T, ["hypothesis_rank", "name", "segment", "daf_assets_eoy", "accounts_for_cost", "rev_20bps_avg_proxy", "margin_pct_20bps_base", "tech_vendor", "share_oat_runs_in_topn", "rank_risk_heavy"],
            [n0, lambda x: str(x).title()[:40], str, b, n0, m, pct, lambda x: str(x)[:26], lambda x: f"{x:.2f}", n0])
    + """
Caveats common to all rows: avg-AUA proxy; [A] cost parameters (cost per account likely understated, see segment economics); 990 vendor lines are floors; CF DAF books sit inside multi-fund operations (fund accounting, scholarships, endowments) that a DAF-only servicer must integrate with; no evidence of willingness to outsource administration (CFs historically buy software, not outsourced servicing). Per-row `main_uncertainties` and `reasons_to_doubt` in `top25-hypotheses.csv`. Weight-sensitive rows (in top 25 in < 90% of one-at-a-time runs): """ + (", ".join(f"{r['name'].title()} {r['share_oat_runs_in_topn']:.2f}" for _, r in T[T['share_oat_runs_in_topn'] < 0.9].iterrows()) or "none") + ". Rows falling below rank 50 under risk-heavy weights (concentration/contract weight up): " + (", ".join(f"{r['name'].title()} -> {int(r['rank_risk_heavy'])}" for _, r in T[T['rank_risk_heavy'] > 50].iterrows()) or "none") + ".")

excl = E[E["captive_status"] != "none_found"]
add("Exclusions: captives, recent migrations, in-house platforms", f"""**Not addressable (excluded from scoring)**: {', '.join(sorted(excl[excl['captive_status'].isin(['captive_inhouse_affiliate','vendor_captive','inhouse_platform_app_native'])]['name'].str.title()))}. Basis per row in `captive_basis` (e.g. Fidelity: FMR administrative services per FY2025 audited statements Note 7, `sponsor-audit-notes.csv`; AOGF: Benevity management services agreement; RCF: Renaissance Administration LLC $19.2m TY2024).

**Addressable but penalised (contractual/captive score 0.25-0.6)**: financial-institution affiliates that outsource to Ren or have unknown platforms (GS DAF, GS Charitable Gift Fund, MS GIFT, US Charitable Gift Trust, Ayco, T. Rowe Price, Stifel, BofA, Raymond James, Bessemer, BNY Mellon) and name-inferred bank programs [D]; NCF (custom Salesforce build). Their decision sits with the parent's vendor strategy.

**Recent migrations (<= 24 months [A]) - penalised and excluded from top 25**: {'; '.join(f"{r['name'].title()}: {r['mig_to']} ({r['mig_date']})" for _, r in E[E['recent_migration']==1].iterrows())}. Sources: `cf-vendor-migrations-2022-2026.csv` events (B) and `prospects-sponsors.csv` PS02/PS04/PS12 (C). A new platform contract is a 3-5 year lock-in [A]; these become windows only at renewal.""")

add("Limitations", """- **Cost-to-serve is parametric [A]**: per-account $25, per-grant $6, per-contribution $10, fixed $25k/sponsor (base) are placeholders sized to reconcile with the $75/fund-year hypothesis; no observed servicer activity costs were available. Sponsors' own 990 DAF-allocated opex is far higher. Replace with the activity-cost agent's values (`cost-to-serve-parameters.csv`) and re-run.
- **Contribution counts unknown**: no public per-sponsor contribution counts in repo; contributions_per_account is pure [A]. Grant counts published for only 12 sponsors (mostly nationals).
- **Average billable AUA is a two-point proxy**; intra-year flows, fee-billing conventions and fiscal-year mismatches are ignored.
- **Price realism**: a flat 20 bps on multi-billion books is not a credible price; revenue for the largest sponsors is an upper bound.
- **Vendor/captive evidence is incomplete**: top-5 contractor floors, portal hosts, CT-log leads; 834 addressable sponsors have no vendor signal. Captive classification of bank/wealth programs by name is [D].
- **Buying signals** only where repo evidence exists (prospects-sponsors.csv challenges, dated migrations); hiring signals not linked by EIN. Absence of a signal is not evidence of satisfaction.
- **Non-DAF complexity** uses total assets and limited fund-count data; complex-asset flags only capture Dechomai inflows and processors (no noncash-by-sponsor data parsed).
- **Not validated externally**: no web spot-check was run in this pass; cross-file consistency checks only (league table, long-tail panel). Same-model reasoning is not independent validation.""")

with open(os.path.join(OUT, "report.jsonl"), "w") as f:
    for s in sections:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")
print(len(sections), "sections")
