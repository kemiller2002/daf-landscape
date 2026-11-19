"""Build data/mission-2026-11-14/sponsor-obbba-tax-page-audit-2026-11-19.csv. usage: python3 -I build_obbba_csv.py REPO_ROOT CHECKS_JSON"""
import csv, json, os, sys
from collections import Counter

COLS = ["rank_fy2024", "sponsor", "ein", "fy2024_daf_assets_usd_bn", "pages_read", "page_dates", "access_status",
        "states_daf_excluded_from_nonitemizer", "daf_exclusion_quote", "states_0_5pct_floor", "floor_quote",
        "states_35pct_cap", "cap_quote", "nonitemizer_amounts_stated", "calculator_url", "calculator_models_floor",
        "calculator_models_cap", "calculator_models_nonitemizer_170p", "worked_example_ids", "worked_example_check",
        "errors_or_overstatements", "vs_repo_H1_H3", "evidence_label", "accessed"]

ROWS = [
    dict(rank_fy2024=1, sponsor="Fidelity Charitable", ein="110303001",
         pages_read="https://www.fidelitycharitable.org/articles/obbb-tax-reform.html ; https://www.fidelitycharitable.org/articles/tax-smart-moves-year-end.html ; https://www.fidelitycharitable.org/content/dam/fc-public/docs/advisors/obbb-impact-on-charitable-planning-presentation.pdf",
         page_dates="undated live pages (article cites law signed July 4, 2025; year-end page refers to 'before 2026 ends')", access_status="robots allowed; all fetched 200",
         states_daf_excluded_from_nonitemizer="yes",
         daf_exclusion_quote="'This provision is not indexed for future inflation, and donations to donor-advised fund sponsors and some private foundations are ineligible for the deduction.'",
         states_0_5pct_floor="yes", floor_quote="'... only claim a tax deduction to the extent that their qualified contributions exceed 0.5% of their adjusted gross income (AGI). For example, a couple with an AGI of $300,000 can only deduct charitable donations in excess of $1,500.'",
         states_35pct_cap="yes", cap_quote="'caps the tax benefit of itemized charitable deductions at 35% for those in the 37% marginal tax bracket ... donating $1,000 would see the value of their deduction limited to $350 when previously it was $370'",
         nonitemizer_amounts_stated="$1,000 / $2,000; 'not indexed'", calculator_url="none found (two guessed URLs 404)",
         calculator_models_floor="n/a", calculator_models_cap="n/a", calculator_models_nonitemizer_170p="n/a",
         worked_example_ids="FC-EX1; FC-EX2; FLOOR-EX", worked_example_check="all arithmetic correct",
         errors_or_overstatements="none found; advisor deck labels the cap '2% deduction limitation' (37%->35%) and lists the 1% corporate floor separately (correct)",
         vs_repo_H1_H3="$0.35 per $ at 37% equals repo H3 per-dollar value before the floor; deck example ($200k gift, $2.5m AGI) = (200,000-12,500) x 35% = $65,625, same formula as repo H3",
         evidence_label="F"),
    dict(rank_fy2024=2, sponsor="National Philanthropic Trust", ein="237825575",
         pages_read="https://www.nptrust.org/philanthropic-resources/philanthropist/the-right-moves-right-now/ ; https://www.nptrust.org/philanthropic-resources/philanthropist/what-tax-reform-means-for-charitable-giving-in-2026/ ; https://www.nptrust.org/philanthropic-resources/philanthropist/navigating-charitable-giving-in-the-wake-of-new-tax-reform/",
         page_dates="", access_status="NOT FETCHED: NPT Terms of Use ban robots/scripts for any purpose (repo convention); search-engine text only",
         states_daf_excluded_from_nonitemizer="yes [S]", daf_exclusion_quote="[S] search text: gifts to DAFs, private foundations and supporting organizations are excluded ('The Right Moves, Right Now')",
         states_0_5pct_floor="yes [S]", floor_quote="[S] search text only", states_35pct_cap="not verified", cap_quote="",
         nonitemizer_amounts_stated="[S] $1,000 / $2,000", calculator_url="not checked", calculator_models_floor="not checked", calculator_models_cap="not checked",
         calculator_models_nonitemizer_170p="not checked", worked_example_ids="", worked_example_check="not checked", errors_or_overstatements="not checked",
         vs_repo_H1_H3="not checked", evidence_label="S"),
    dict(rank_fy2024=3, sponsor="DAFgiving360 (Schwab Charitable)", ein="311640316",
         pages_read="https://www.dafgiving360.org/tax-law-changes ; https://www.dafgiving360.org/tax-2026 ; https://advisorservices.schwab.com/insights-hub/perspectives/charitable_tax_strategies ; bunching calculator component p-577835bb.entry.js",
         page_dates="undated live pages; calculator disclosure code (1026-F22Y)", access_status="robots allowed; all fetched 200 (dafgiving360.org was 403 in earlier repo passes)",
         states_daf_excluded_from_nonitemizer="yes", daf_exclusion_quote="'Note: The deduction excludes donor-advised fund (DAF) contributions.'",
         states_0_5pct_floor="yes", floor_quote="'... will need to exceed a 0.5% floor before they can claim that donation as an itemized deduction.' tax-2026: '$300,000 ... in excess of $1,500'",
         states_35pct_cap="yes", cap_quote="'If you're in the 37% federal income tax bracket, the value of your charitable deduction benefits is now capped at 35% ... 35 cents for every dollar'",
         nonitemizer_amounts_stated="$1,000 / $2,000 'with inflation adjustments over time'",
         calculator_url="https://www.dafgiving360.org/maximize-your-impact/tax-calculator (bunching calculator)",
         calculator_models_floor="no (no AGI input; savings = deduction x bracket rate)", calculator_models_cap="no (37% bracket uses 0.37)",
         calculator_models_nonitemizer_170p="no (standard path = standard deduction only)",
         worked_example_ids="SCH-EX1; FLOOR-EX", worked_example_check="arithmetic correct",
         errors_or_overstatements="States the $1,000/$2,000 non-itemizer amounts adjust for inflation; 26 USC 170(p) as amended by P.L. 119-21 s.70424 has no inflation adjustment (Fidelity says 'not indexed'). Same sentence on advisorservices.schwab.com. Bunching calculator omits the 0.5% floor and the 35% cap that its own article describes",
         vs_repo_H1_H3="Calculator port: H1 $0 (repo DAF $0); H2 annual $2,016 vs repo $936, bunched $5,472 vs $5,112; H3 annual $55,500 vs repo $47,250 (+$8,250, +17.5%)",
         evidence_label="F"),
    dict(rank_fy2024=4, sponsor="Vanguard Charitable", ein="232888152",
         pages_read="https://www.vanguardcharitable.org/charitable-tax-deductions ; https://www.vanguardcharitable.org/charitable-tax-center ; https://www.vanguardcharitable.org/news/could-2025-budget-reconciliation-bill-impact-your-giving ; https://www.vanguardcharitable.org/blog/charitable-bunching-under-obbba-when-it-makes-sense-and-when-it-doesnt ; calculator JS bundle",
         page_dates="tax-deductions page 'Last reviewed August 2026'; others undated", access_status="robots allowed; all fetched 200 (User Agreement bot clause covers the Secure Site only)",
         states_daf_excluded_from_nonitemizer="yes", daf_exclusion_quote="'... you may newly qualify for a $1,000 (single) or $2,000 (joint) deduction on cash gifts to a public charity, though donor-advised fund gifts don't qualify' ; Tax Center FAQ: 'Contributions to donor-advised funds and most private foundations are excluded from this provision.'",
         states_0_5pct_floor="yes", floor_quote="'only giving above a 0.5%-of-AGI threshold is eligible' ; '$200,000 ... the first $1,000 ... is not deductible'",
         states_35pct_cap="yes", cap_quote="'In the 37% bracket, deduction value is capped at 35 cents per dollar, down from 37.'",
         nonitemizer_amounts_stated="$1,000 / $2,000", calculator_url="https://www.vanguardcharitable.org/charitable-tax-center (Tax Calculator)",
         calculator_models_floor="yes (AGI_CHARITABLE_FLOOR_PCT=0.005)", calculator_models_cap="yes (37% input replaced by 0.35)",
         calculator_models_nonitemizer_170p="no (correct for a DAF gift; no direct-gift comparison)",
         worked_example_ids="VC-EX1; VC-EX2; VC-EX3; FLOOR-EX",
         worked_example_check="VC-EX1 arithmetic wrong: stated $9,490/yr, $28,470 annual, $29,125 bunched, +$655; at the stated 35% rate these are $12,775, $38,325, $40,775 and +$2,450 (stated figures imply 26% and 25%). VC-EX2 and VC-EX3 correct",
         errors_or_overstatements="VC-EX1 arithmetic; calculator reports (all itemized deductions - standard deduction) x rate, so for donors whose other itemized deductions exceed the standard deduction it attributes that excess to the gift",
         vs_repo_H1_H3="Calculator port: H1 $0 = repo; H2 annual $936 = repo, bunched $5,112 = repo; H3 annual $55,440 vs repo $47,250 (attributes ($40,000-$32,200) x 35% = $2,730/yr of other deductions to the gift)",
         evidence_label="F"),
    dict(rank_fy2024=5, sponsor="Goldman Sachs Philanthropy Fund", ein="311774905", pages_read="", page_dates="",
         access_status="NOT READ: gspf.goldman.com robots.txt disallows all user agents. Parent-firm page https://www.goldmansachs.com/what-we-do/ayco/insights/year-end-tax-planning read for context only (states $1,000/$2,000, 0.5% floor, 35% cap; no DAF exclusion sentence)",
         states_daf_excluded_from_nonitemizer="not read", daf_exclusion_quote="", states_0_5pct_floor="not read", floor_quote="", states_35pct_cap="not read", cap_quote="",
         nonitemizer_amounts_stated="", calculator_url="", calculator_models_floor="not read", calculator_models_cap="not read", calculator_models_nonitemizer_170p="not read",
         worked_example_ids="", worked_example_check="", errors_or_overstatements="", vs_repo_H1_H3="", evidence_label="R"),
    dict(rank_fy2024=6, sponsor="Silicon Valley Community Foundation", ein="205205488",
         pages_read="https://www.svcf.org/about/news-media/blog/new-tax-rules-and-the-potential-impact-on-your-clients-philanthropy ; https://www.svcf.org/about/news-media/blog/2026-tax-updates-what-advisors-should-know",
         page_dates="page metadata 2026-01-16/2026-01-20 and 2026-02-09/2026-07-08", access_status="robots allowed; fetched 200",
         states_daf_excluded_from_nonitemizer="yes", daf_exclusion_quote="'... may deduct up to $1,000 in cash donations to qualified charities, excluding donations to donor advised funds and private foundations.'",
         states_0_5pct_floor="yes", floor_quote="'... only to the extent their total giving exceeds 0.5% of adjusted gross income (AGI)'",
         states_35pct_cap="yes", cap_quote="'... won't receive a tax benefit higher than 35 cents per dollar donated.'",
         nonitemizer_amounts_stated="$1,000 (single filer only stated)", calculator_url="none found", calculator_models_floor="n/a", calculator_models_cap="n/a", calculator_models_nonitemizer_170p="n/a",
         worked_example_ids="", worked_example_check="no numeric worked example", errors_or_overstatements="none found; joint $2,000 not stated", vs_repo_H1_H3="no example to compare", evidence_label="F"),
    dict(rank_fy2024=7, sponsor="Morgan Stanley Global Impact Funding Trust (MS GIFT)", ein="527082731",
         pages_read="https://www.morganstanley.com/articles/donor-advised-funds-tax-benefits-for-charitable-giving ; https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-tax-savings.pdf ; https://www.morganstanley.com/campaigns/wealth-management/gift ; parent: https://www.morganstanley.com/articles/tax-efficient-charitable-giving",
         page_dates="undated; MS GIFT tax-savings PDF shows 2025 only", access_status="robots allowed; fetched 200",
         states_daf_excluded_from_nonitemizer="implicit only", daf_exclusion_quote="DAF article footnote: 'This deduction is only available if you elect to itemize your deductions.' No sentence on the non-itemizer deduction. Parent article: non-itemizers 'deduct up to $1,000 ($2,000 ...) for qualified cash donations' with no DAF exclusion",
         states_0_5pct_floor="yes", floor_quote="'... only be able to claim an income tax deduction to the extent that their qualified contributions exceed 0.5% of the donor's AGI.'",
         states_35pct_cap="yes", cap_quote="'... capped at 35 percent, even for taxpayers in the 37 percent marginal tax bracket.' Parent article states the 2/37 rule exactly",
         nonitemizer_amounts_stated="parent page only: $1,000 / $2,000", calculator_url="none found", calculator_models_floor="n/a", calculator_models_cap="n/a", calculator_models_nonitemizer_170p="n/a",
         worked_example_ids="", worked_example_check="no numeric worked example",
         errors_or_overstatements="DAF article: 'Amounts disallowed under this rule carry over for up to five taxable years' overstates s.170(d)(1)(C), which carries floor amounts forward only from years with a percentage-limit excess (parent article states this correctly)",
         vs_repo_H1_H3="no example to compare", evidence_label="F"),
    dict(rank_fy2024=8, sponsor="American Endowment Foundation", ein="341747398",
         pages_read="https://www.aefonline.org/thought-leadership/charitable-bunching-for-financial-advisors/",
         page_dates="page metadata 2026-10-22", access_status="robots allowed; fetched 200",
         states_daf_excluded_from_nonitemizer="yes", daf_exclusion_quote="'From 2026, non-itemizers can deduct up to $1,000 in gifts ($2,000 for joint filers), but DAF contributions do not qualify under Section 70424 of OBBBA.'",
         states_0_5pct_floor="yes", floor_quote="'... itemizers can deduct only the charitable giving above 0.5% of AGI, under Section 70425 ...'",
         states_35pct_cap="not on page read", cap_quote="", nonitemizer_amounts_stated="$1,000 / $2,000",
         calculator_url="none found", calculator_models_floor="n/a", calculator_models_cap="n/a", calculator_models_nonitemizer_170p="n/a",
         worked_example_ids="AEF-EX1", worked_example_check="arithmetic correct ($52,500; $96,600 vs $116,900; +$20,300; ~$4,900 = $4,872 at 24%)",
         errors_or_overstatements="Annual baseline gives the couple the bare $32,200 standard deduction; if the $12,000/yr were given as direct cash, s.170(p) adds $2,000/yr, so the bunching gain over direct annual giving is $14,300 of deductions / $3,432 tax, not $4,872",
         vs_repo_H1_H3="Same structure as repo H2 ($300k AGI, 24%); repo H2 shows the same effect: bunching beats annual DAF by $4,176 but annual direct cash by only $3,672",
         evidence_label="F"),
    dict(rank_fy2024=9, sponsor="Renaissance Charitable Foundation", ein="352129262",
         pages_read="https://www.reninc.com/blog/what-every-advisor-needs-to-know-about-charitable-deductions-in-2026/ ; https://renaissancecharitable.org/blog/obbba-guide-for-complex-asset-pre-liquidity-clients/",
         page_dates="", access_status="NOT FETCHED: Renaissance site terms bar scraping without written authorization (repo); search-engine text only",
         states_daf_excluded_from_nonitemizer="yes [S]", daf_exclusion_quote="[S] search text: 'up to $1,000 ($2,000 married). DAFs do not qualify.'",
         states_0_5pct_floor="yes [S]", floor_quote="[S] example: $500,000 AGI, floor $2,500", states_35pct_cap="yes [S]", cap_quote="[S]",
         nonitemizer_amounts_stated="[S] $1,000 / $2,000", calculator_url="not checked", calculator_models_floor="not checked", calculator_models_cap="not checked", calculator_models_nonitemizer_170p="not checked",
         worked_example_ids="FLOOR-EX", worked_example_check="[S] floor arithmetic correct", errors_or_overstatements="[S] one page reportedly says floored amounts carry forward five years; not verified", vs_repo_H1_H3="", evidence_label="S"),
    dict(rank_fy2024=10, sponsor="National Christian Foundation", ein="581493949",
         pages_read="https://site.ncfgiving.com//wp-content/uploads/2026/08/OBBBA.pdf ; https://www.ncfgiving.com/stories/obbba",
         page_dates="PDF upload path 2026/08", access_status="robots allowed; fetched 200 (Program Agreement scraping clause covers the Secure Site)",
         states_daf_excluded_from_nonitemizer="yes", daf_exclusion_quote="'... for cash gifts made to churches and public charities (but not to Giving Funds or Supporting Organizations).' (NCF calls its DAFs Giving Funds)",
         states_0_5pct_floor="yes", floor_quote="'individuals can only deduct charitable gifts that exceed 0.5% of their adjusted gross income (AGI)'",
         states_35pct_cap="yes", cap_quote="'lowering their tax benefit in the highest tax bracket from 37% to 35%'",
         nonitemizer_amounts_stated="$1,000 / $2,000", calculator_url="none found", calculator_models_floor="n/a", calculator_models_cap="n/a", calculator_models_nonitemizer_170p="n/a",
         worked_example_ids="", worked_example_check="no numeric worked example", errors_or_overstatements="none found", vs_repo_H1_H3="no example to compare", evidence_label="F"),
]


def main(root, checks):
    lt = {r["ein"]: r for r in csv.DictReader(open(os.path.join(root, "data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv")))
          if r["fiscal_year"] == "2024" and r["row_type"] == "top50"}
    rows = [{**r, "fy2024_daf_assets_usd_bn": round(float(lt[r["ein"]]["daf_assets_eoy"]) / 1e9, 2), "accessed": "2026-11-19"} for r in ROWS]
    assert [int(lt[r["ein"]]["rank_assets"]) for r in rows] == list(range(1, 11))
    out = os.path.join(root, "data/mission-2026-11-14/sponsor-obbba-tax-page-audit-2026-11-19.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); list(map(w.writerow, rows))
    for k in ["states_daf_excluded_from_nonitemizer", "states_0_5pct_floor", "states_35pct_cap", "evidence_label"]:
        print(k, dict(Counter(r[k] for r in rows)))
    print("assets read F: $bn", round(sum(r["fy2024_daf_assets_usd_bn"] for r in rows if r["evidence_label"] == "F"), 2),
          "of", round(sum(r["fy2024_daf_assets_usd_bn"] for r in rows), 2))


if __name__ == "__main__":
    main(sys.argv[1], json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None)
