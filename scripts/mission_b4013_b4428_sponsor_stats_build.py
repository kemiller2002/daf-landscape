"""P-B4013-01 / P-B4428-03: sponsor-published grant statistics (restricted share; disclosure outcomes).

Usage: python3 -I scripts/mission_b4013_b4428_sponsor_stats_build.py . OUT.csv

Rows are quoted first-party (or flagged secondary / repo-carried) figures collected on 2026-11-19.
The script joins FY2024 national ranks and DAF assets from the league table, computes the derived
values (marked [C]) and prints the summary tables used in the research note. Stdlib only, no mutable
global state.
"""
import csv
import sys
from functools import reduce

LEAGUE = "data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv"
DEFAULTS = "data/mission-2026-11-14/donor-info-defaults-top20-2026-11-19.csv"

FC = "https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/{}-giving-report.pdf"
VC = "https://www.vanguardcharitable.org/news/{}"
SCHWAB = "https://pressroom.aboutschwab.com/press-releases/press-release/{}/default.aspx"
NPT24 = "https://www.nptrust.org/annual-reports/the-2024-annual-report/"
NPT25 = "https://www.nptrust.org/annual-reports/npt-annual-report/"
NPT23 = "https://www.nptrust.org/annual-reports/the-2023-annual-report/"
CH_CY25 = "https://www.givechariot.com/resources/insights/dafgiving360s-2025-results-4-of-our-biggest-takeaways-for-nonprofit-fundraisers"
CH_FY25 = "https://www.givechariot.com/resources/insights/breaking-down-the-dafgiving360-fy25-annual-report"
FC_DEF = "While grant recipients must use grants for charitable purposes and in conformity with Fidelity Charitable's policies and applicable laws, special purposes are conveyed to grant recipients as recommendations, not restrictions."
VC_DEF = "unrestricted granting—defined as a grant given to a nonprofit that can be used for any purpose as directed by the nonprofit"

FIELDS = ["row_id", "task", "sponsor", "ein", "national_rank_fy2024", "fy2024_daf_assets_usd", "metric",
          "period", "period_basis", "value_pct", "value_qualifier", "basis", "numerator", "denominator",
          "definition", "quote", "source_url", "source_date", "source_type", "evidence_label", "robots",
          "sponsor_default", "notes"]

# (row_id, task, ein, metric, period, period_basis, value_pct, qualifier, basis, numerator, denominator,
#  definition, quote, url, source_date, source_type, label, robots, notes)
RAW = [
    # ---------------- (A) restricted vs unrestricted: Fidelity Charitable (count of grant recommendations)
    ("A-FC-2019", "A", "110303001", "share_where_needed_most", "2019", "calendar", 60, "exact", "grant recommendations (count implied; unit not stated)", "", "all grant recommendations",
     "Grant use designated 'where needed most' vs a specific fund, campaign or other use; " + FC_DEF,
     "Sixty-three percent of grant recommendations were designated “where needed most,” compared to 60 percent in 2019.", FC.format(2021), "2021-02-16 (PDF created)", "sponsor annual report", "F", "allowed (200)", "Pre-2021 period, 2021 source; context only"),
    ("A-FC-2020", "A", "110303001", "share_where_needed_most", "2020", "calendar", 63, "exact", "grant recommendations (count implied; unit not stated)", "", "all grant recommendations",
     "As A-FC-2019", "Sixty-three percent of grant recommendations were designated “where needed most,” compared to 60 percent in 2019.", FC.format(2021), "2021-02-16 (PDF created)", "sponsor annual report", "F", "allowed (200)", "Same value in the 2026 report's 2020 column"),
    ("A-FC-2021", "A", "110303001", "share_where_needed_most", "2021", "calendar", 64, "exact", "grant recommendations (count implied; unit not stated)", "", "all grant recommendations",
     "As A-FC-2019", "64% of grant recommendations were designated “where needed most”", FC.format(2022), "2022-02-14 (PDF created)", "sponsor annual report", "F", "allowed (200)", ""),
    ("A-FC-2022", "A", "110303001", "share_where_needed_most", "2022", "calendar", 63, "exact", "grant recommendations (count implied; unit not stated)", "", "all grant recommendations",
     "As A-FC-2019", "63% of grant recommendations were designated “where needed most”", FC.format(2023), "2024-04-15 (PDF created; report covers 2022)", "sponsor annual report", "F", "allowed (200)", ""),
    ("A-FC-2023", "A", "110303001", "share_where_needed_most", "2023", "calendar", 63, "exact", "grant recommendations (count implied; unit not stated)", "", "all grant recommendations",
     "As A-FC-2019", "of grant recommendations were designated “where needed most” 63%", FC.format(2024), "2024-03-06 (PDF created)", "sponsor annual report", "F", "allowed (200)",
     "Same page also says 'over two-thirds opted to make unrestricted grants', which conflicts with 63%"),
    ("A-FC-2024", "A", "110303001", "share_where_needed_most", "2024", "calendar", 64, "exact", "grant recommendations (count implied; unit not stated)", "", "all grant recommendations",
     "As A-FC-2019", "Designated “where needed most” 64%", FC.format(2025), "2025-02-19 (PDF created)", "sponsor annual report", "F", "allowed (200)", "Same value in the 2026 report's 2024 column"),
    ("A-FC-2025", "A", "110303001", "share_where_needed_most", "2025", "calendar", 64, "exact", "grant recommendations (count implied; unit not stated)", "", "all grant recommendations",
     "As A-FC-2019", "Designated “where needed most” 63% 64% 64%", FC.format(2026), "2026-04-21 (PDF created)", "sponsor annual report", "F", "allowed (200)", "Columns are 2020, 2024, 2025; sidebar: 'Nearly two-thirds of grant recommendations were designated “where needed most”'"),
    # ---------------- NPT (count; fiscal year Jul-Jun)
    ("A-NPT-FY15", "A", "237825575", "share_unrestricted", "FY2015", "fiscal Jul-Jun", 13, "exact", "grant count ('share of volume')", "", "all grants",
     "'Unrestricted' grant; NPT Schedule I: if the advisor does not recommend a specific purpose, NPT awards the grant as unrestricted (except ER grants)",
     "A decade ago, that share was just 13%.", NPT25, "2026-09-10 (page modified)", "sponsor annual report (web)", "F", "allowed (200)", "Pre-2021 period, 2026 source; chart data FY15,FY20,FY25 = 13,63,66"),
    ("A-NPT-FY20", "A", "237825575", "share_unrestricted", "FY2020", "fiscal Jul-Jun", 63, "exact", "grant count ('share of volume')", "", "all grants",
     "As A-NPT-FY15", "data-category=\"FY15,FY20,FY25,\" data-data=\"13,63,66,\"", NPT25, "2026-09-10 (page modified)", "sponsor annual report (web chart attribute)", "F", "allowed (200)", "Chart 'UNRESTRICTED GRANTS | SHARE OF VOLUME'"),
    ("A-NPT-FY21", "A", "237825575", "share_unrestricted", "FY2021", "fiscal Jul-Jun", 70, "exact", "grants (unit not stated)", "", "all grants",
     "'unrestricted and had no special provisions or requirements attached' (search-snippet wording)", "",
     "https://www.nptrust.org/?p=6867", "", "search snippet of sponsor page (now 404)", "R", "allowed (200) but page returns 404; archive.org unreachable",
     "UNVERIFIED: search-engine snippet only; not used in any computed figure"),
    ("A-NPT-FY23", "A", "237825575", "share_unrestricted", "FY2023", "fiscal Jul-Jun", 50, "more than", "grant recommendations (count implied)", "", "all grant recommendations",
     "As A-NPT-FY15", "more than half of all grant recommendations were unrestricted", NPT23, "2024-03-12 (published)", "sponsor annual report (web)", "F", "allowed (200)",
     "Same page: 'the majority of grants were unrestricted or designated toward general operating support'"),
    ("A-NPT-FY24", "A", "237825575", "share_unrestricted", "FY2024", "fiscal Jul-Jun", 47, "exact", "grant count", "", "130,875 grants",
     "As A-NPT-FY15", "47% of grants were unrestricted, providing flexibility and agency to nonprofits.", NPT24, "2026-09-10 (page modified)", "sponsor annual report (web)", "F", "allowed (200)",
     "Also 'Nearly half of all grants were unrestricted'. 19-point gap to FY25 is unexplained by the sponsor"),
    ("A-NPT-FY25", "A", "237825575", "share_unrestricted", "FY2025", "fiscal Jul-Jun", 66, "exact", "grant count ('share of volume')", "105909", "159543",
     "As A-NPT-FY15", "In FY25, 105,909 grants, or 66% of the total, were unrestricted", NPT25, "2026-09-10 (page modified)", "sponsor annual report (web)", "F", "allowed (200)",
     "Grant total 159,543 from the same report's sector table"),
    # ---------------- DAFgiving360 (count)
    ("A-D360-FY2022", "A", "311640316", "share_no_purpose_specified", "FY2022", "fiscal Jul-Jun", 72, "exact", "grants (count implied)", "", "all grants",
     "'grants not designated for a specific purpose'", "These unrestricted grants have reached 72% of the total",
     SCHWAB.format("2022/Schwab-Charitable-Donors-Granted-4.7-Billion-to-Charity-in-Fiscal-Year-2022"), "2022-07-19", "sponsor release on affiliate (Schwab) pressroom", "F", "allowed (200, crawl-delay 10)", "dafgiving360.org itself is robots-blocked (403)"),
    ("A-D360-CY2023", "A", "311640316", "share_no_purpose_specified", "2023", "calendar", 71, "exact", "grant recommendations (count implied)", "", "all grant recommendations",
     "'did not specify a purpose so organizations could use the grants where needed most'",
     "71% of donors’ grant recommendations did not specify a purpose so organizations could use the grants where needed most.",
     SCHWAB.format("2024/Schwab-Charitable-Donors-Grant-Over-6-Billion-to-Charity-in-2023"), "2024-01-23", "sponsor release on affiliate (Schwab) pressroom", "F", "allowed (200, crawl-delay 10)", ""),
    ("A-D360-FY2024", "A", "311640316", "share_no_purpose_specified", "FY2024", "fiscal Jul-Jun", 72, "exact", "grants (count implied)", "", "all grants",
     "As A-D360-CY2023", "Seventy-two percent of grants in the fiscal year did not specify a purpose, so organizations could use the grants where needed most.",
     SCHWAB.format("2024/DAFgiving360-Donors-Give-More-Than-6.6B-to-Charities-in-Fiscal-Year-2024"), "2024-07-23", "sponsor release on affiliate (Schwab) pressroom", "F", "allowed (200, crawl-delay 10)", ""),
    ("A-D360-FY2025-repo", "A", "311640316", "share_unrestricted", "FY2025", "fiscal Jul-Jun", 70, "at least ('70%+')", "unstated", "", "unstated",
     "unstated", "", "https://www.dafgiving360.org/press-release/fiscal-year-2025-results", "2025-07-29", "repo-carried (sponsor release, not re-read)", "R", "blocked (robots.txt 403)",
     "Carried from ai-economics-replacement-analysis.md P05 and validation-wave35a V35A-37/38"),
    ("A-D360-FY2025-sec", "A", "311640316", "share_unrestricted", "FY2025", "fiscal Jul-Jun", 72, "exact", "unclear ('of the overall giving')", "", "unstated",
     "unstated", "There was a 20% year-over-year increase in the number of unrestricted grants, which now account for 72% of the overall giving from DAFgiving360 accounts.",
     CH_FY25, "2025-08-04 (Chariot post 'Aug 4')", "secondary (Chariot summary of sponsor report)", "S", "allowed (200)", "Secondary; basis (count vs dollars) ambiguous"),
    ("A-D360-CY2025-sec", "A", "311640316", "share_unrestricted", "2025", "calendar", 74, "exact", "grants (count implied)", "", "~1.5 million grants",
     "unstated", "74% of grants were unrestricted and 38% of all grants from DAFgiving360 were set up as recurring",
     CH_CY25, "2026-02-12 (Chariot post 'Feb 12')", "secondary (Chariot summary of sponsor release)", "S", "allowed (200)", "Secondary; sponsor release (2026-01-27) is robots-blocked"),
    # ---------------- Vanguard Charitable (mostly dollars)
    ("A-VC-CY2020", "A", "232888152", "share_unrestricted", "2020", "calendar", 42, "exact", "grant dollars", "", "grant dollars",
     VC_DEF, "In 2021, more than half of all giving was unrestricted, up from 42% of grant dollars in 2020.",
     VC.format("vanguard-charitable-donors-build-record-charitable-giving-year-granting-total-over-178-billion"), "2022-01-25", "sponsor release", "F", "allowed (200)", "Pre-2021 period, 2022 source"),
    ("A-VC-CY2021", "A", "232888152", "share_unrestricted", "2021", "calendar", 50, "more than", "giving (dollars implied by comparison)", "", "grant dollars",
     VC_DEF, "In 2021, more than half of all giving was unrestricted, up from 42% of grant dollars in 2020.",
     VC.format("vanguard-charitable-donors-build-record-charitable-giving-year-granting-total-over-178-billion"), "2022-01-25", "sponsor release", "F", "allowed (200)", ""),
    ("A-VC-2022-12", "A", "232888152", "share_unrestricted", "as of 2022-12", "snapshot", 50, "more than", "grants recommended (count implied)", "", "grants recommended",
     VC_DEF, "Today, more than half of the grants recommended by Vanguard Charitable donors are unrestricted",
     VC.format("vanguard-charitable-celebrates-25-years-and-15-billion-granted"), "2022-12-08", "sponsor release", "F", "allowed (200)", ""),
    ("A-VC-CY2022", "A", "232888152", "share_unrestricted", "2022", "calendar", 50, "more than", "grant dollars", "", "grant dollars",
     VC_DEF, "over half of dollars granted by Vanguard Charitable donors were unrestricted",
     VC.format("vanguard-charitable-donors-set-new-granting-record-despite-economic-challenges"), "2023-01-25", "sponsor release", "F", "allowed (200)", ""),
    ("A-VC-2023-04", "A", "232888152", "share_unrestricted", "annual, as of 2023-04", "snapshot", 50, "more than", "grant dollars", "", "dollars granted annually",
     VC_DEF, "now representing more than half the dollars granted annually",
     VC.format("unrestricted-giving-increased-over-past-5-years"), "2023-04-26", "sponsor release", "F", "allowed (200)", "Also: unrestricted granting grew 150% over five years and 580% over a decade"),
    ("A-VC-FY2023", "A", "232888152", "share_unrestricted", "FY2023", "fiscal Jul-Jun", 50, "more than", "grants recommended (count implied)", "", "all grants recommended",
     VC_DEF, "More than 50% of all grants recommended by Vanguard Charitable donors in fiscal year 2023 were unrestricted.",
     VC.format("vanguard-charitable-FY23-granting-record"), "2023-08-10", "sponsor release", "F", "allowed (200)", ""),
    ("A-VC-CY2023", "A", "232888152", "share_unrestricted", "2023", "calendar", 50, "more than", "grant dollars", "", "total dollars granted",
     VC_DEF, "More than half of the total dollars granted by donors were unrestricted",
     VC.format("vanguard-charitable-donors-granted-2-billion-2023"), "2024-01-30", "sponsor release", "F", "allowed (200)", ""),
    ("A-VC-FY2024", "A", "232888152", "share_unrestricted", "FY2024", "fiscal Jul-Jun", 48.3, "exact", "grant dollars", "", "grant dollars",
     VC_DEF, "more than half of grant dollars (51.7%) were unrestricted, an increase from 48.3% last year",
     VC.format("vanguard-charitable-donors-deepen-their-impact-driving-another-year-record-granting"), "2025-08-25", "sponsor release", "F", "allowed (200)", "FY2024 releases (2024-08-27, 2025-02-04) give no share"),
    ("A-VC-FY2025", "A", "232888152", "share_unrestricted", "FY2025", "fiscal Jul-Jun", 51.7, "exact", "grant dollars", "", "grant dollars",
     "'given without limitations or designations regarding their use' (wire wording); " + VC_DEF, "more than half of grant dollars (51.7%) were unrestricted, an increase from 48.3% last year",
     VC.format("vanguard-charitable-donors-deepen-their-impact-driving-another-year-record-granting"), "2025-08-25", "sponsor release", "F", "allowed (200)", ""),
    ("A-VC-CY2025", "A", "232888152", "share_unrestricted", "2025", "calendar", 50, "about ('half')", "grants (label) / $2bn (dollars)", "2.0e9", "3.9e9",
     VC_DEF, "half of all grants issued last year were unrestricted, accounting for $2 billion",
     VC.format("vanguard-charitable-2025-record-granting"), "2026-03-02", "sponsor release", "F", "allowed (200)", "Dollar share computed from rounded $2bn / $3.9bn"),
    # ---------------- (B) disclosure outcomes: Fidelity (grants)
    *[(f"B-FC-{yr}-{cat}", "B", "110303001", f"share_{cat}", str(yr), "calendar", v, "exact", "grants (count implied)", "", "all grants",
       {"full_contact": "Included donor name and address", "fund_name_only": "Included Giving Account name only", "anonymous": "Anonymous"}[cat],
       q, FC.format(rep), d, "sponsor annual report", "F", "allowed (200)", n)
      for (yr, rep, d, vals, q, n) in [
          (2020, 2021, "2021-02-16 (PDF created)", (83, 13, 4), "only four percent of grants are completely anonymous", "Shares read from chart labels 83% / 13% / 4%"),
          (2021, 2022, "2022-02-14 (PDF created)", (82, 14, 4), "• 82% Includes donor name and address • 14% Includes Giving Account name only • 4% Anonymous", ""),
          (2022, 2023, "2024-04-15 (PDF created; report covers 2022)", (81, 15, 4), "• 81% Includes donor name and address • 15% Includes Giving Account name only • 4% Anonymous", ""),
          (2023, 2024, "2024-03-06 (PDF created)", (81, 15, 4), "96% of grants included the account name or the recommending donors’ names and addresses", "Chart: 81% / 15% / 4%"),
          (2024, 2025, "2025-02-19 (PDF created)", (80, 15, 5), "Included donor name and address 80% Included Giving Account name only 15% Anonymous 5%", ""),
          (2025, 2026, "2026-04-21 (PDF created)", (80, 15, 5), "Included donor name and address 83% 80% 80%", "Columns 2020, 2024, 2025; anonymous row '4% 5% 5%'"),
      ]
      for cat, v in zip(("full_contact", "fund_name_only", "anonymous"), vals)],
    ("B-FC-FAQ-anon", "B", "110303001", "share_anonymous", "undated (live)", "snapshot", 4, "exact", "grants (count implied)", "", "all grants",
     "Anonymous", "Only 4% of Fidelity Charitable grants are made anonymously.",
     "https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html", "live page, read 2026-11-19", "sponsor web page", "F", "allowed (200)", "Stale relative to the 2025 report's 5%"),
    # ---------------- Vanguard
    ("B-VC-anon-4", "B", "232888152", "share_anonymous", "undated (live)", "snapshot", 4, "exact", "grants (count implied)", "", "all grants",
     "completely anonymous", "Only 4% of grants are completely anonymous.",
     "https://www.vanguardcharitable.org/nonprofit-organizations", "live page, read 2026-11-19", "sponsor web page", "F", "allowed (200)", "Same page also states 5% (B-VC-anon-5)"),
    ("B-VC-anon-5", "B", "232888152", "share_anonymous", "undated (live)", "snapshot", 5, "exact", "grants (count implied)", "", "all grants",
     "completely anonymous", "Anonymous granting: Only 5% of grants are completely anonymous",
     "https://www.vanguardcharitable.org/nonprofit-organizations", "live page, read 2026-11-19", "sponsor web page", "F", "allowed (200)", "Fact box next to '$20 billion and growing' granted"),
    # ---------------- NPT (snippets only)
    ("B-NPT-FY20", "B", "237825575", "share_non_anonymous", "FY2020", "fiscal Jul-Jun", 96, "exact", "grants (unit not stated)", "", "all grants",
     "Non-Anonymous Grants", "", "https://www.nptrust.org/ (FY20 annual report page, now 404)", "", "search snippet of sponsor page", "R", "allowed (200) but page 404",
     "UNVERIFIED: search snippet only. Implies about 4% anonymous"),
    ("B-NPT-FY21", "B", "237825575", "share_donors_identified", "FY2021", "fiscal Jul-Jun", 97, "exact", "donors (not grants)", "", "donors",
     "'chose to include identifying information in their grantmaking'", "", "https://www.nptrust.org/?p=6867", "", "search snippet of sponsor page (now 404)", "R", "allowed (200) but page 404",
     "UNVERIFIED: search snippet only; a donor share, not a grant share"),
    ("B-NPT-qual", "B", "237825575", "qualitative", "undated (live)", "snapshot", "", "qualitative", "grants", "", "",
     "", "The majority of grants from donor-advised funds are not anonymous.", "https://www.nptrust.org/for-charities/", "live page, read 2026-11-19", "sponsor web page", "F", "allowed (200)", "No current NPT split published"),
    # ---------------- AEF and GKCCF (qualitative)
    ("B-AEF-qual", "B", "341747398", "qualitative", "2025", "snapshot", "", "qualitative", "donors", "", "",
     "", "most DAF donors opt against remaining anonymous.", "https://advisorwelcome.aefonline.org/wp-content/uploads/2025/03/AEF_Difference_Fact-Sheet_2025.pdf", "2025-03-03 (PDF created)", "sponsor fact sheet", "F", "allowed (200)",
     "Policy-argument context; unclear whether it describes AEF donors or DAF donors generally"),
    ("B-GKCCF-qual", "B", "431152398", "qualitative", "undated (live)", "snapshot", "", "qualitative", "donors", "", "",
     "", "It's rare for donors to choose to grant anonymously", "https://www.growyourgiving.org/nonprofits/knowledge-hub/", "per repo (b44n28-01)", "repo-carried sponsor web page", "R", "allowed per repo log", "Community foundation, outside the national top 15"),
]

NOT_FOUND = {  # top-15 nationals without a published figure; reason recorded
    "311774905": "blocked: gspf.goldman.com robots 'Disallow: /'",
    "527082731": "none found: morganstanley.com/gift page and 'MS GIFT grantmaking' PDF (2024-10-01) read; annual-report URLs 2021-2025 return 404",
    "341747398": "none found for (A); qualitative only for (B) (B-AEF-qual)",
    "352129262": "none found (web search; Ren/RCF portal guides read in b4428-02 carry no outcome data)",
    "046010342": "none found (web search)",
    "262048480": "none found: impact reports give grant counts (13,500 in 2024) but no purpose or disclosure split (web search)",
    "200849590": "none found (b44n28-01: no public grant-letter text)",
    "593652538": "blocked: raymondjamescharitable.org robots 403",
    "260724604": "none found (b44n28-01: no relevant text)",
    "311663020": "none found (web search)",
    "141782466": "none found (web search)",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def nationals(root):
    rows = [r for r in read_csv(f"{root}/{LEAGUE}")
            if r["fiscal_year"] == "2024" and r["row_type"] == "top50" and r["type"] == "National"]
    ranked = sorted(rows, key=lambda r: -float(r["daf_assets_eoy"]))
    return {r["ein"]: {"rank": i + 1, "name": r["name"], "assets": float(r["daf_assets_eoy"])}
            for i, r in enumerate(ranked[:15])}


def defaults(root):
    return {r["ein"]: r["default_category"] for r in read_csv(f"{root}/{DEFAULTS}")}


SPONSOR_NAMES = {"110303001": "Fidelity Charitable", "237825575": "National Philanthropic Trust",
                 "311640316": "DAFgiving360", "232888152": "Vanguard Charitable",
                 "341747398": "American Endowment Foundation", "431152398": "Greater Kansas City Community Foundation"}


def to_row(raw, nat, dfl):
    (rid, task, ein, metric, period, pbasis, val, qual, basis, num, den, defin, quote, url, sdate, stype, label, robots, notes) = raw
    n = nat.get(ein, {})
    return {"row_id": rid, "task": task, "sponsor": SPONSOR_NAMES.get(ein, n.get("name", "")), "ein": ein,
            "national_rank_fy2024": n.get("rank", ""), "fy2024_daf_assets_usd": f"{n['assets']:.0f}" if n else "",
            "metric": metric, "period": period, "period_basis": pbasis, "value_pct": val, "value_qualifier": qual,
            "basis": basis, "numerator": num, "denominator": den, "definition": defin, "quote": quote,
            "source_url": url, "source_date": sdate, "source_type": stype, "evidence_label": label,
            "robots": robots, "sponsor_default": dfl.get(ein, "") if task == "B" else "", "notes": notes}


def not_found_rows(nat):
    return [{**{k: "" for k in FIELDS}, "row_id": f"X-{v['rank']:02d}", "task": "A+B", "sponsor": v["name"], "ein": ein,
             "national_rank_fy2024": v["rank"], "fy2024_daf_assets_usd": f"{v['assets']:.0f}", "metric": "none published",
             "value_qualifier": "not found" if reason.startswith("none") else "blocked",
             "evidence_label": "B" if reason.startswith("blocked") else "absent", "notes": reason}
            for ein, v in sorted(nat.items(), key=lambda kv: kv[1]["rank"]) for reason in [NOT_FOUND.get(ein)] if reason]


def computed(nat):
    total = sum(v["assets"] for v in nat.values())
    covered_a = {"110303001", "237825575", "311640316", "232888152"}
    covered_b = {"110303001", "232888152"}
    share = lambda s: sum(nat[e]["assets"] for e in s) / total
    fc = {2020: (83, 13, 4), 2021: (82, 14, 4), 2022: (81, 15, 4), 2023: (81, 15, 4), 2024: (80, 15, 5), 2025: (80, 15, 5)}
    return {
        "top15_national_assets_bn": round(total / 1e9, 2),
        "share_top15_assets_with_restriction_figure": round(share(covered_a), 4),
        "share_top15_assets_with_firstparty_disclosure_split_or_anon_share": round(share(covered_b), 4),
        "npt_fy25_unrestricted_share": round(105909 / 159543, 4),
        "npt_fy24_implied_unrestricted_grants": round(0.47 * 130875),
        "npt_fy24_to_fy25_change_pts": 66 - 47,
        "vc_cy2025_dollar_share_from_rounded": round(2.0 / 3.9, 4),
        "fc_full_contact_change_2020_2025_pts": fc[2025][0] - fc[2020][0],
        "fc_sum_check": {y: sum(v) for y, v in fc.items()},
        "fc_kept_default_upper_bound_2025": fc[2025][0],
        "fc_departed_default_lower_bound_2025": fc[2025][1] + fc[2025][2],
        "vc_departed_default_lower_bound_range": (4, 5),
        "vc_kept_default_upper_bound_range": (95, 96),
        "fc_where_needed_most_range_2020_2025": (min(63, 64, 63, 63, 64, 64), max(63, 64, 63, 63, 64, 64)),
        "fc_specific_use_share_2025": 100 - 64,
    }


def main(argv):
    root, out = argv[1], argv[2]
    nat, dfl = nationals(root), defaults(root)
    rows = [to_row(r, nat, dfl) for r in RAW] + not_found_rows(nat)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("\n".join(f"{v['rank']:>2} {e} {v['name']} {v['assets']/1e9:.2f}" for e, v in sorted(nat.items(), key=lambda kv: kv[1]["rank"])))
    print("\n".join(f"{k}: {v}" for k, v in computed(nat).items()))
    counts = reduce(lambda acc, r: {**acc, r["evidence_label"]: acc.get(r["evidence_label"], 0) + 1}, rows, {})
    print(f"rows: {len(rows)}; by label: {counts}")


if __name__ == "__main__":
    main(sys.argv)
