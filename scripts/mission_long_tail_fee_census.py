#!/usr/bin/env python3
"""P-B45N33-01: published DAF fee census of a stratified random sample of the long tail (sponsors under $50m).

Stdlib only; functional style (pure transforms; I/O only at the edges: CSV read/write, the optional fetch task).

Tasks
  sample   Draw the stratified random sample (fixed seed) from the 1,240 FY2024 tail sponsors and print it.
  fetch    For every source URL in FEES (below): read robots.txt on the host first (generic user agent
           "research-script/1.0"), log the verdict, and fetch the page only if allowed; PDFs are converted with
           pdftotext. Results are cached in --cache-dir (outside the repository). Needs --fetch to touch the network.
  census   Verify each transcribed quote against the cached text of its source (whitespace-normalised, case-
           insensitive), compute the effective annual admin fee at $25k / $100k / $500k, join the allocated operating
           cost (rules A, G, AM) from long-tail-operating-cost-2026-11-19.csv, write the census CSV and print every
           summary table used in research/mission-2026-11-14/b45n33-01-long-tail-fee-census.md.

Sampling
  Frame: daf-long-tail-sponsors-fy2021-2024.csv rows with size_band_fy2024 in t10_50, t1_10, t0_1, zero (1,240).
  Type (4): community_foundation -> cf; single_issue_other -> single_issue; religious -> faith;
            university_or_hospital, national_standard, donation_processor -> other.
  Strata: type x size band (16 cells, all non-empty). Allocation of n = 60: proportional to stratum size, largest-
  remainder rounding, floor of 1 per stratum. Within a stratum: random.Random(SEED + stratum index).sample() over the
  stratum's rows sorted by EIN, so the draw is reproducible and independent of file order.

Fee computation
  Effective annual admin fee at a constant balance B: tiers ((lower, upper|None, rate_pct), ...) applied 'marginal'
  (each rate on its slice) or 'flat_on_total' (the rate of B's tier on all of B); then max(fee, minimum annual fee)
  plus any flat annual fee. Gift and grant fees are recorded but are not in the effective annual fee (they depend on
  activity); a separate column adds a stated grant/gift percentage at an assumed 10% annual turnover only where the
  schedule has no balance-based fee. bps = fee / B x 1e4.

Usage
  python3 scripts/mission_long_tail_fee_census.py . --task sample
  python3 scripts/mission_long_tail_fee_census.py . --task fetch --cache-dir CACHE --fetch
  python3 scripts/mission_long_tail_fee_census.py . --task census --cache-dir CACHE
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import functools
import html
import json
import math
import os
import random
import re
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from functools import reduce
from typing import Iterable, Mapping, Sequence

DATA = "data/mission-2026-11-14"
LT_CSV = f"{DATA}/daf-long-tail-sponsors-fy2021-2024.csv"
COST_CSV = f"{DATA}/long-tail-operating-cost-2026-11-19.csv"
TOP100_CSV = f"{DATA}/cf-daf-fee-census-2026.csv"
REFRESH_CSV = f"{DATA}/cf-daf-fee-census-refresh-2026-11-19.csv"
OUT_CSV = f"{DATA}/long-tail-fee-census-2026-11-19.csv"
TAIL_BANDS = ("t10_50", "t1_10", "t0_1", "zero")
TYPE_OF = {
    "community_foundation": "cf",
    "single_issue_other": "single_issue",
    "religious": "faith",
    "university_or_hospital": "other",
    "national_standard": "other",
    "donation_processor": "other",
}
TYPES = ("cf", "single_issue", "faith", "other")
SEED = 20261119
N_SAMPLE = 60
BALANCES = (25_000, 100_000, 500_000)
UA = "research-script/1.0"
RETRIEVED = "2026-11-19"
TURNOVER = 0.10  # assumed share of balance granted out a year, used only for grant-fee-only schedules
RATE_2021 = ("published_schedule", "published_no_admin_fee")        # a balance-based admin rate (incl. 0), 2021+ or live
RATE_STATUSES = RATE_2021 + ("published_pre2021",)                 # fee computed (pre-2021 kept apart)
ANY_TERM = RATE_STATUSES + ("partial", "published_unread")          # some fee term or a linked schedule is published
UNKNOWN = ("robots_blocked",)                                       # site not readable within robots rules

# ----------------------------------------------------------------------------- transcription (filled after research)
# Keyed by EIN. status: published_schedule | partial | no_published_fee | no_website_found
# For published/partial: tiers, basis, min_fee, flat_fee, opening_min, gift_fee, grant_fee, grant_fee_pct,
# investment, source_url, source_date, quotes (verbatim strings that must occur in the cached source text).
_NPF = "no_published_fee"
FEES: dict[str, dict] = {
    # ---------------- community foundations
    "911726410": dict(status="published_schedule", website="https://whatcomcf.org/",
        tiers=((0, 500_000, 2.0), (500_000, 1_000_000, 1.5), (1_000_000, 5_000_000, 1.25), (5_000_000, None, 1.0)),
        basis="marginal", opening_min=5_000,
        gift_fee="Gift fee on new gifts to the short-term pool on the same progressive scale (2.00% on first $500k); none on gifts to the long-term pool",
        grant_fee="not stated",
        investment="Pools' expense ratios 'less than 0.3%'; no separate investment management fee; Impact Investment Pool 2% service fee instead of the standard fee",
        source_url="https://whatcomcf.org/financial-oversight/investment-approach-fees/",
        verify_urls=("https://whatcomcf.org/financial-oversight/investment-approach-fees/",
                     "https://whatcomcf.org/wp-content/uploads/2025/12/Non-Endowed-Funds-Terms-and-Conditions-12.2025.pdf"),
        source_date="live 2026-11-19; Non-Endowed Terms & Conditions 'Last Updated: 12/31/2025'",
        quotes=("2.00% on the first $499,999.99 of fund assets", "1.50% on fund amounts between $500,000 to $999,999.99",
                "1.25% on fund amounts between $1 million and $4,999,999.99", "Donor Advised Fund $5,000",
                "Last Updated: 12/31/2025", "Currently, we do not charge a separate investment management fee"),
        notes="Standard (short-term) non-endowed schedule used. Endowed funds and non-endowed funds in the long-term pool are "
              "listed at 1.50% on the first $500k on the same page; the T&C put long-term non-endowed funds on the 2.00% scale "
              "without the gift fee. Homepage is JS-rendered; pages found through the WordPress page sitemap."),
    "481076910": dict(status="published_schedule", website="https://www.hutchcf.org/",
        tiers=((0, 2_000_000, 1.25), (2_000_000, 5_000_000, 0.75), (5_000_000, 15_000_000, 0.5), (15_000_000, None, 0.25)),
        basis="marginal", min_fee=250, opening_min=0,
        gift_fee="none stated", grant_fee="none stated; 'additional fees for extraordinary services, such as special grant processing'",
        investment="not stated in schedule; direct expenses (e.g. stock-sale commissions) charged to the fund",
        source_url="https://hutchcf.org/wp-content/uploads/2025/02/2023-fee-schedules_DAF.pdf",
        verify_urls=("https://hutchcf.org/wp-content/uploads/2025/02/2023-fee-schedules_DAF.pdf",
                     "https://hutchcf.org/attorneysandadvisors/advisor-faq/"),
        source_date="2023 schedule (file name), uploaded 2025-02",
        quotes=("First $2 million 1.25% or $250", "$2 million to $5 million 0.75%", "one-twelfth of the fee per month",
                "There is no minimum amount required to start a fund at Hutchinson Community Foundation",
                "grants cannot be made from a fund until it reaches $10,000"),
        notes="Tier basis not stated; read as marginal ('First $2 million'). No opening minimum, but no grants until the fund reaches $10,000."),
    "751709180": dict(status="published_pre2021", website="https://www.cfwtx.org/",
        tiers=((0, None, 1.0),), basis="flat_on_total", opening_min=5_000,
        gift_fee="none stated", grant_fee="none stated",
        investment="Investment fees charged by the investment advisor, 'tiered based on the type and size of the fund' (rates not published)",
        source_url="https://www.cfwtx.org/_files/ugd/416dfb_6eb9ed0847e14a06b62f37087d507867.pdf",
        verify_urls=("https://www.cfwtx.org/_files/ugd/416dfb_6eb9ed0847e14a06b62f37087d507867.pdf", "https://www.cfwtx.org/advisor-faqs"),
        source_date="'Revised 12/01/16' (live 2026-11-19, linked from /fund-types)",
        quotes=("Donor Advised, Designated, Field of Interest, Unrestricted 1.0%", "Revised 12/01/16",
                "Annual fees are assessed quarterly based on average fund balance",
                "Investment fees are tiered based on the type and size of the fund"),
        notes="Pre-2021 document: kept in the CSV, excluded from the 2021+ fee distribution."),
    "521326014": dict(status="published_unread", website="https://www.cfes.org/", opening_min=5_000,
        gift_fee="not read", grant_fee="not read",
        investment="Non-endowed funds may use the CFES portfolio if a $50,000 balance is kept; otherwise 'in lieu of a fee, CFES sweeps any interest earned'",
        source_url="https://www.cfes.org/createafund",
        verify_urls=("https://www.cfes.org/createafund", "https://www.cfes.org/advisors"),
        source_date="live 2026-11-19",
        quotes=("The minimum to establish a non-endowed fund is $5,000", "in lieu of a fee, CFES sweeps any interest earned",
                "Administrative Fee Schedule"),
        robots="cfes.org allowed; the 'Administrative Fee Schedule' link points to a Google Drive file whose download URL drive.google.com/uc is disallowed by robots.txt",
        notes="Schedule exists (linked from /advisors) but could not be read within robots rules."),
    "752817894": dict(status="robots_blocked", website="https://www.wfacf.org/",
        robots="robots.txt 403 (generic UA): treated as disallowed; nothing fetched", notes="Fee status unknown."),
    "841339670": dict(status="published_schedule", website="https://www.ppcf.org/",
        tiers=((0, 3_000_000, 1.5), (3_000_000, 5_000_000, 1.5), (5_000_000, 10_000_000, 0.75), (10_000_000, None, 0.25)),
        basis="marginal", min_fee=250,
        gift_fee="none stated ('No Fees on Donation' applies to the Impact Fund only)", grant_fee="none stated",
        investment="Own investment manager allowed from a $100,000 fund; investment fees not stated",
        source_url="https://www.ppcf.org/wp-content/uploads/2025/01/Fund-Types-Fee-Structure.pdf",
        verify_urls=("https://www.ppcf.org/wp-content/uploads/2025/01/Fund-Types-Fee-Structure.pdf",
                     "https://www.ppcf.org/wp-content/uploads/2025/01/DAF-vs-PF.pdf"),
        source_date="uploaded 2025-01 (wp-content path)",
        quotes=("First $3 Million 1% or 100 bps 1.5% or 150 bps", "Over $10M 0.25% or 25 bps 0.25% or 25 bps",
                "*Minimum annual fee: $250", "With a fund minimum of $100,000"),
        notes="Non-endowed DAF column used (endowed DAF: 1.00% first $3m, 0.75% next $2m, 0.50% next $5m, 0.25% over $10m). No opening minimum stated."),
    "593182886": dict(status=_NPF, website="https://www.cffound.org/", notes="DAF, fund-options, advisor FAQ and establish-a-fund pages read; no fee or minimum stated."),
    "311760702": dict(status="partial", website="https://www.thelcfoundation.org/", opening_min=25_000,
        grant_fee="none stated; grants under $250 discouraged 'to control the administrative fees we charge all funds'",
        investment="'The cost of investment activities and administering a Donor Advised Fund is paid from the fund's total return' (no rate)",
        source_url="https://www.thelcfoundation.org/file_download/dd22cd34-c547-4cee-990a-5658aa280b4c", source_date="undated PDF (Donor Advised Fund Guide), live 2026-11-19",
        quotes=("A total contribution of at least $25,000 is required to establish this type of fund",
                "The cost of investment activities and administering a Donor Advised Fund is paid from the fund"),
        notes="Fee exists but no rate published."),
    "043401997": dict(status=_NPF, website="https://www.glcfoundation.org/", notes="Types-of-funds and open-a-fund pages read; no DAF fee or DAF minimum (nonprofit agency funds: $10,000)."),
    "341713261": dict(status=_NPF, website="https://www.community-foundation.com/", notes="Fund-options, advisor and establishing-a-fund pages read; minimums referred to but not stated."),
    "680330462": dict(status="partial", website="https://www.communityfound.org/", opening_min=10_000,
        source_url="https://communityfound.org/giving/become-donor/types-of-funds/donor-advised-funds/",
        verify_urls=("https://communityfound.org/giving/become-donor/types-of-funds/donor-advised-funds/",
                     "https://communityfound.org/wp-content/uploads/Terminating-a-Private-Foundation-to-a-Donor-Advised-Fund.doc"),
        source_date="live 2026-11-19 (the .doc is undated)",
        quotes=("Minimum initial gift: $10,000", "The cost to maintain your Donor Advised Fund is low (1.5% or less of Fund balance)"),
        notes="Only a ceiling ('1.5% or less') in an undated .doc; not a schedule, not used in fee calculations."),
    "920139183": dict(status="published_schedule", website="https://www.homerfoundation.org/",
        tiers=((0, 1_000_000, 1.5), (1_000_000, None, 1.25)), basis="marginal", min_fee=150, opening_min=10_000,
        gift_fee="none stated", grant_fee="none stated (project pass-through: $250 plus 1% of funds disbursed)",
        investment="Total return per Investment & Spending Policy #19-01/#20-01; no investment fee stated",
        source_url="https://www.cityofhomer-ak.gov/sites/default/files/fileattachments/memo/72719/01-01_funds_policy_v.1.28.21.pdf",
        source_date="Funds Policy #01-01 v.1.27.21 / 1.28.21 (January 2021)",
        quotes=("Donor Advised 1.5% but not less than $150", "A minimum gift of $10,000 is required to open a named fund",
                "the fees on the amount in excess of $1,000,000.00 will be reduced by .25%"),
        robots="cityofhomer-ak.gov robots.txt 200: allowed",
        notes="Sponsor's own policy, but found only in a City of Homer board packet (third-party host), not on homerfoundation.org."),
    "510173092": dict(status=_NPF, website="https://fourwaycommunityfoundation.org/", notes="Homepage, sitemap and join-a-fund page read; no fee or minimum."),
    "383179612": dict(status=_NPF, website="https://www.micf.org/", notes="Give and donor-portal pages read; no DAF fee."),
    "351859959": dict(status=_NPF, website="https://www.madisonccf.org/", notes="Homepage and sitemap (105 URLs, mostly fund stories) read; no fee page."),
    "311140087": dict(status="robots_blocked", website="https://clintoncountyohiofoundation.org/",
        robots="robots.txt 403 (generic UA): treated as disallowed; nothing fetched", notes="Fee status unknown."),
    "593343026": dict(status=_NPF, website="https://www.cfslc.org/", notes="Donor-advised-funds page read; no fee or minimum."),
    "266394395": dict(status="published_no_admin_fee", website="https://atccf.org/",
        tiers=((0, None, 0.0),), basis="marginal", opening_min=5_000,
        gift_fee="none stated (subsequent contributions of $1,000 or more)", grant_fee="none; minimum grant $250",
        investment="Bank (trustee) investment management fee 0.5% of market value a year, waived in the first year",
        source_url="https://atccf.org/Donor-Options/donor-advised-fund", source_date="live 2026-11-19 (undated page)",
        quotes=("has committed to do the administration of The Community Fund at no charge",
                "assessed at an annual rate of ½ % (one-half percent) of the market value of the Fund", "Minimum initial contribution of $5,000"),
        notes="Admin fee 0; the 0.5% investment fee goes to the Adirondack Trust Company, not the sponsor."),
    "611304905": dict(status="robots_blocked", website="https://www.cfwestky.org/",
        robots="robots.txt 403 (generic UA): treated as disallowed; nothing fetched", notes="Fee status unknown."),
    "311040215": dict(status="published_schedule", website="https://www.athensfoundation.org/",
        tiers=((0, 500_000, 1.5), (500_000, None, 1.0)), basis="flat_on_total", opening_min=10_000,
        gift_fee="none stated ('No startup fees')", grant_fee="none stated", investment="not stated",
        source_url="https://www.athensfoundation.org/create-a-fund",
        verify_urls=("https://www.athensfoundation.org/create-a-fund", "https://www.athensfoundation.org/daf"),
        source_date="live 2026-11-19 (undated page)",
        quotes=("Donor-Advised Fund $10,000 1.5% to $500,000 or 1% for $500,000+", "No startup fees"),
        notes="'1.5% to $500,000 or 1% for $500,000+' read as a band rate on the whole balance (so $500k pays 1.0%); a marginal reading gives 150 bps at $500k."),
    "300752563": dict(status=_NPF, website="https://spccf.org/", notes="Homepage and 2020 handout read; no fee."),
    "390827885": dict(status="partial", website="https://www.cfcwi.org/", opening_min=1_000,
        gift_fee="3% processing fee on credit-card gifts (donor may add it; otherwise absorbed by the fund)", grant_fee="none stated",
        source_url="https://cfcwi.org/new-fund/", verify_urls=("https://cfcwi.org/new-fund/", "https://cfcwi.org/ways-to-give/"),
        source_date="live 2026-11-19",
        quotes=("The minimum to establish a Donor Advised Fund is $1,000", "Credit card transactions require a 3% processing fee"),
        notes="No admin rate published."),
    "351870979": dict(status=_NPF, website="https://dccfound.org/", notes="Homepage, advisor page and sitemap read; no fee."),
    "841374928": dict(status=_NPF, website="https://www.grandfoundation.com/", notes="Grand Foundation (formerly Columbine CF); homepage and policy page read; no DAF fee."),
    "351842404": dict(status=_NPF, website="https://www.jaspernewtonfoundation.org/", notes="Homepage, sitemaps read; /our-funds/ is JS-rendered (82 characters of text)."),
    "382236628": dict(status=_NPF, website="https://cfmonroe.org/", notes="How-to-start-a-fund and advisor pages read; no fee or minimum."),
    "421495980": dict(status="published_unread", website="https://givinggreater.org/", opening_min=2_500,
        grant_fee="none stated; minimum grant $250",
        source_url="https://www.givinggreater.org/_files/ugd/0f7e19_e35188275f7b4f3aaf1a768995e4cc28.pdf",
        verify_urls=("https://www.givinggreater.org/_files/ugd/0f7e19_e35188275f7b4f3aaf1a768995e4cc28.pdf", "https://www.givinggreater.org/giving"),
        source_date="undated DAF guidelines PDF, live 2026-11-19",
        quotes=("$2,500 for a non-endowed fund", "To review the Community Foundation’s Fee Schedule, click here", "The minimum grant amount is $250"),
        robots="givinggreater.org allowed; the fee schedule PDF is on a usrfiles.com host whose robots.txt returns 403 (treated as disallowed)",
        notes="Community Foundation of Greater Muscatine. Schedule exists but could not be read within robots rules."),
    "251881899": dict(status="robots_blocked", website="https://www.cfgcpa.org/",
        robots="robots.txt 403 (generic UA): treated as disallowed; nothing fetched", notes="Fee status unknown."),
    "421285187": dict(status="robots_blocked", website="https://clarindafoundation.com/",
        robots="robots.txt 403 (generic UA): treated as disallowed; nothing fetched", notes="Fee status unknown."),
    "237410312": dict(status=_NPF, website="https://www.capecoralcf.org/", notes="Homepage and sitemap read; no fee page."),
    "842380618": dict(status="no_website_found", notes="NCF child organisation (Catalyst Trust of Indiana); no website on the 990 or found by search."),
    # ---------------- single-issue
    "951644609": dict(status=_NPF, website="https://www.eifoundation.org/", notes="No DAF fee page; site describes fiscally sponsored funds."),
    "911325007": dict(status=_NPF, website="https://pridefoundation.org/", notes="Start-a-fund page describes DAFs; no fee or minimum."),
    "270388708": dict(status=_NPF, website="https://www.greenwoodcf.org/", notes="Greenwood County Community Foundation (DAFRC category single-issue); DAF contribution and advisor pages read; no fee."),
    "752675978": dict(status=_NPF, website="https://www.bsafoundation.org/", notes="Redirects to scoutingamericafoundation.org; page sitemap read; no DAF page."),
    "042104847": dict(status="robots_blocked", website="https://www.williams.edu/",
        robots="robots.txt 403 (generic UA): treated as disallowed; nothing fetched", notes="Fee status unknown."),
    "131624046": dict(status=_NPF, website="https://www.iie.org/", notes="DAF page is about giving to IIE from a DAF; no sponsor DAF terms."),
    "020459470": dict(status=_NPF, website="https://www.manchesterpal.org/", notes="No DAF page."),
    "472525808": dict(status="partial", website="https://globaltrustfunds.org/",
        grant_fee="Fees for grant agreements or international grants; minimum grant $100 (grant form)",
        investment="Investment pools via NPT forms; segregated accounts available",
        source_url="https://globaltrustfunds.org/faqs/",
        verify_urls=("https://globaltrustfunds.org/faqs/", "https://globaltrustfunds.org/wp-content/uploads/2024/07/Grant_recommendation_form.pdf"),
        source_date="live 2026-11-19; forms uploaded 2024-07",
        quotes=("GlobalTrust Funds charges charitable administration fees", "by applying a blended schedule against the average daily balance",
                "The minimum grant recommendation amount is $100.00"),
        notes="Fee basis described; rates not published."),
    "820444885": dict(status="no_website_found", notes="990 website 'N/A'; employee giving fund of Idaho Power."),
    "381359193": dict(status=_NPF, website="https://www.unitedforscmi.org/", notes="No DAF page."),
    "132992977": dict(status=_NPF, website="https://www.astraeafoundation.org/", notes="No DAF page found."),
    "920146538": dict(status=_NPF, website="https://www.bcsfoundation.org/", notes="No DAF page."),
    "930395586": dict(status=_NPF, website="https://www.unitedwaymwv.org/", notes="No DAF page."),
    # ---------------- faith
    "050259003": dict(status="partial", website="https://www.jewishallianceri.org/", opening_min=2_500,
        investment="DAFs 'invested as part of the endowment'; Rhode Island Foundation partnership",
        source_url="https://www.jewishallianceri.org/support-us/giving-options/donor-advised-funds", source_date="live 2026-11-19",
        quotes=("With just $2,500 you can invest your donation",),
        notes="Jewish Federation Foundation. The Alliance's newspaper (Jewish Rhode Island, 2021-11-07 and 2022-11-06) says 'Low administration fee' with no rate."),
    "822189237": dict(status=_NPF, website="https://www.jewishyoungstown.org/", notes="Endowment-opportunities page describes philanthropic funds ('low minimum'); no amount or fee."),
    "453969752": dict(status=_NPF, website="https://christianaidministries.org/biblical-stewardship-services/",
        notes="Live page describes the DAF without fees. A search-indexed page (christianaidministries.org/?p=93032, now 404) said CAM Foundation 'generally' manages DAFs 'without charge'; not verifiable, so not used."),
    "204595721": dict(status=_NPF, website="https://www.ccfmm.org/", notes="Homepage read (links to an FCSuite portal); no fee page."),
    "720779104": dict(status=_NPF, website="https://umf.org/", notes="No DAF fee page; newsletters call the DAF 'cost-effective'."),
    "042104351": dict(status=_NPF, website="https://www.jccns.org/", notes="No DAF page."),
    "510159835": dict(status=_NPF, website="https://www.jewishdesmoines.org/", notes="No DAF page."),
    "382596725": dict(status="no_website_found", notes="990 website 'N/A'."),
    # ---------------- other (university/hospital, national, processor)
    "510515757": dict(status="no_website_found", notes="990 website 'NONE'; ceritypartners.com (the adviser) has no foundation fee page."),
    "486088461": dict(status=_NPF, website="https://www.emporia.edu/foundation-giving/", notes="No DAF page among 485 candidate URLs."),
    "133219917": dict(status=_NPF, website="https://www.sunyorangefoundation.org/", notes="No DAF terms; scholarship funds carry a management fee ('currently .75 basis points')."),
    "362182171": dict(status="robots_blocked", website="https://www.wheaton.edu/",
        robots="robots.txt 403 (generic UA): treated as disallowed; nothing fetched", notes="Fee status unknown."),
    "351635296": dict(status=_NPF, website="https://johnsonmemorialfoundation.org/", notes="No DAF page."),
    "832300241": dict(status="published_schedule", website="https://www.cpp.edu/philanthropy/",
        tiers=((0, None, 2.0),), basis="flat_on_total", opening_min=100_000,
        gift_fee="none stated", grant_fee="none; at least 50% of each year's distributions must go to the Foundation",
        investment="Commingled in the endowment investment pool; no separate fee stated",
        source_url="https://www.cpp.edu/philanthropy/policies/504philanthropic-donorsadvisedfundpolicy.pdf",
        source_date="undated policy (worked example dated June 15, 2021), live 2026-11-19",
        quotes=("two percent (2%) of fund balance annual administrative fee, charged quarterly",
                "a donor must contribute not less than one hundred thousand dollars ($100,000.00)",
                "Not less than fifty percent (50%) of the total amount distributed each year from each DAF account shall be distributed to the Foundation"),
        notes="Cal Poly Pomona Philanthropic Foundation."),
    "200385860": dict(status="partial", website="https://www.cmafohio.org/", opening_min=10_000,
        source_url="https://www.cmafohio.org/create-a-personalized-charitable-fund", source_date="live 2026-11-19 (read by validation wave 34B)",
        quotes=(),
        notes="Fund page lists donor-advised funds with a $10,000 minimum and 'a quarterly administration fee, based on the size of the fund'; no rate published [V wave 34B]."),
    "590974739": dict(status=_NPF, website="https://www.uff.ufl.edu/", notes="No DAF page (endowment minimums only)."),
}

# Official homepages: CFs from cf-vendor-map-by-ein-v2.csv (990 WebsiteAddressTxt); others from the FY2024 990
# WebsiteAddressTxt in the GivingTuesday mirror, or from a web search where the 990 gives none (noted in FEES).
SITES: dict[str, str] = {
    "911726410": "https://www.whatcomcf.org/",
    "481076910": "https://www.hutchcf.org/",
    "751709180": "https://www.cfwtx.org/",
    "521326014": "https://www.cfes.org/",
    "752817894": "https://www.wfacf.org/",
    "841339670": "https://www.ppcf.org/",
    "593182886": "https://www.cffound.org/",
    "311760702": "https://www.thelcfoundation.org/",
    "043401997": "https://www.glcfoundation.org/",
    "341713261": "https://www.community-foundation.com/",
    "680330462": "https://www.communityfound.org/",
    "920139183": "https://www.homerfoundation.org/",
    "510173092": "https://fourwaycommunityfoundation.org/",
    "383179612": "https://www.micf.org/",
    "351859959": "https://www.madisonccf.org/",
    "311140087": "https://clintoncountyohiofoundation.org/",
    "593343026": "https://www.cfslc.org/",
    "266394395": "https://atccf.org/",
    "611304905": "https://www.cfwestky.org/",
    "311040215": "https://www.athensfoundation.org/",
    "300752563": "https://spccf.org/",
    "390827885": "https://www.cfcwi.org/",
    "351870979": "https://dccfound.org/",
    "841374928": "https://www.grandfoundation.com/",
    "351842404": "https://www.jaspernewtonfoundation.org/",
    "382236628": "https://cfmonroe.org/",
    "421495980": "https://givinggreater.org/",
    "251881899": "https://www.cfgcpa.org/",
    "421285187": "https://clarindafoundation.com/",
    "237410312": "https://www.capecoralcf.org/",
    "951644609": "https://www.eifoundation.org/",
    "911325007": "https://pridefoundation.org/",
    "270388708": "https://www.greenwoodcf.org/",
    "752675978": "https://www.bsafoundation.org/",
    "042104847": "https://www.williams.edu/",
    "131624046": "https://www.iie.org/",
    "020459470": "https://www.manchesterpal.org/",
    "472525808": "https://www.globaltrustfunds.org/",
    "381359193": "https://www.unitedforscmi.org/",
    "132992977": "https://www.astraeafoundation.org/",
    "920146538": "https://www.bcsfoundation.org/",
    "930395586": "https://www.unitedwaymwv.org/",
    "050259003": "https://www.jewishallianceri.org/",
    "822189237": "https://www.jewishyoungstown.org/",
    "453969752": "https://christianaidministries.org/biblical-stewardship-services/",  # web search; 990 lists none
    "204595721": "https://www.ccfmm.org/",
    "720779104": "https://umf.org/",
    "042104351": "https://www.jccns.org/",
    "510159835": "https://www.jewishdesmoines.org/",
    "486088461": "https://www.emporia.edu/foundation-giving/",
    "133219917": "https://www.sunyorangefoundation.org/",
    "362182171": "https://www.wheaton.edu/",
    "351635296": "https://johnsonmemorialfoundation.org/",
    "832300241": "https://www.cpp.edu/philanthropy/",
    "200385860": "https://www.cmafohio.org/",
    "590974739": "https://www.uff.ufl.edu/",
}

FEE_LINK = re.compile(r"(?i)fee|donor.?advised|\bdaf\b|fund.?(type|option|polic|agreement|guideline)|polic|"
                      r"open.?a.?fund|start.?a.?fund|create.?a.?fund|ways.?to.?give|giving.?option|types.?of.?funds|"
                      r"advisor|professional|\.pdf$")
FEE_SENT = re.compile(r"(?i)(administrative|admin|management|service|annual)\s+fee|\bfees?\b.{0,60}(%|percent|basis points)|"
                      r"minimum.{0,40}\$\s?[\d,]+|\$\s?[\d,]+.{0,40}(to open|to establish|minimum)|"
                      r"(%|percent).{0,60}(of the fund|balance|market value|assets|per year|annually|of grants|of gifts)")


# ----------------------------------------------------------------------------- pure helpers
def num(x) -> float | None:
    try:
        v = float(str(x).replace(",", "").replace("$", "").strip())
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def fmt(v, nd: int = 1) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


# ----------------------------------------------------------------------------- sampling
def tail_frame(lt_rows: Iterable[Mapping]) -> tuple[dict, ...]:
    return tuple(
        {**r, "type4": TYPE_OF[r["sponsor_category"]]}
        for r in lt_rows
        if r["size_band_fy2024"] in TAIL_BANDS
    )


def strata(frame: Sequence[Mapping]) -> tuple[tuple[tuple[str, str], tuple[dict, ...]], ...]:
    keys = tuple((t, b) for t in TYPES for b in TAIL_BANDS)
    return tuple(
        (k, tuple(sorted((r for r in frame if (r["type4"], r["size_band_fy2024"]) == k), key=lambda r: r["ein"])))
        for k in keys
    )


def allocate(sizes: Sequence[int], n: int) -> tuple[int, ...]:
    """Proportional allocation, floor 1 per non-empty stratum, largest remainder for the rest."""
    total = sum(sizes)
    base = tuple(max(1, math.floor(n * s / total)) if s else 0 for s in sizes)
    rem = n - sum(base)
    order = sorted(range(len(sizes)), key=lambda i: (-(n * sizes[i] / total - math.floor(n * sizes[i] / total)), i))
    bump = frozenset(order[:max(0, rem)])
    return tuple(min(sizes[i], base[i] + (1 if i in bump else 0)) for i in range(len(sizes)))


def draw(frame: Sequence[Mapping], n: int = N_SAMPLE, seed: int = SEED) -> tuple[dict, ...]:
    st = strata(frame)
    alloc = allocate(tuple(len(rows) for _, rows in st), n)
    return tuple(
        {**r, "stratum": f"{k[0]}|{k[1]}", "stratum_N": len(rows), "stratum_n": a, "weight": len(rows) / a}
        for i, ((k, rows), a) in enumerate(zip(st, alloc))
        for r in random.Random(seed + i).sample(rows, a)
    )


# ----------------------------------------------------------------------------- fee engine
def effective_admin_fee(s: Mapping, balance: float) -> float | None:
    tiers = s.get("tiers") or ()
    if not tiers and not s.get("flat_fee") and not s.get("min_fee"):
        return None
    if s.get("basis", "marginal") == "marginal":
        fee = sum(max(0.0, min(balance, up if up is not None else balance) - lo) * r / 100 for lo, up, r in tiers)
    else:
        fee = balance * next((r for lo, up, r in tiers if balance >= lo and (up is None or balance < up)),
                             tiers[-1][2] if tiers else 0) / 100
    return round(max(fee, s.get("min_fee") or 0) + (s.get("flat_fee") or 0), 2)


def bps(fee: float | None, balance: float) -> float | None:
    return None if fee is None else round(fee / balance * 1e4, 1)


def activity_fee_bps(s: Mapping) -> float | None:
    """Grant-fee-only schedules: stated % of grants x assumed turnover, in bps of balance."""
    p = s.get("grant_fee_pct")
    return None if p is None or s.get("tiers") else round(p / 100 * TURNOVER * 1e4, 1)


# ----------------------------------------------------------------------------- statistics
def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float, float] | None:
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def quantiles(xs: Sequence[float]) -> tuple[float, float, float] | None:
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    if len(xs) == 1:
        return xs[0], xs[0], xs[0]
    q = statistics.quantiles(xs, n=4, method="inclusive")
    return q[0], statistics.median(xs), q[2]


def qfmt(xs: Sequence[float], nd: int = 0) -> str:
    q = quantiles(xs)
    n = len([x for x in xs if x is not None])
    return "–" if q is None else f"{q[1]:,.{nd}f} ({q[0]:,.{nd}f}–{q[2]:,.{nd}f}; n={n})"


# ----------------------------------------------------------------------------- network edge (fetch task only)
def cache_key(url: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", url)[:180]


def http_get(url: str, timeout: int = 30) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read(10_000_000)
    except urllib.error.HTTPError as e:
        return e.code, "", b""
    except Exception as e:  # noqa: BLE001 - network edge
        return -1, type(e).__name__, b""


@functools.lru_cache(maxsize=None)
def robots_file(origin: str) -> tuple[int, bytes]:
    code, _, body = http_get(f"{origin}/robots.txt", timeout=20)
    return code, body


def robots_verdict(url: str) -> tuple[str, bool]:
    p = urllib.parse.urlsplit(url)
    code, body = robots_file(f"{p.scheme}://{p.netloc}")
    if code in (401, 403):
        return f"robots.txt {code}: treated as disallowed", False
    if code != 200:
        return f"robots.txt {code}: none published, fetch allowed", True
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(body.decode("utf-8", "ignore").splitlines())
    ok = rp.can_fetch(UA, url)
    return f"robots.txt 200: {'allowed' if ok else 'disallowed'} for {UA}", ok


def to_text(ctype: str, body: bytes) -> str:
    if body[:4] == b"%PDF" or "pdf" in ctype:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(body)
            f.flush()
            r = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, text=True)
            return r.stdout
    t = body.decode("utf-8", "ignore")
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
    return html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))


def fetch_one(cache: str, url: str) -> dict:
    path = os.path.join(cache, cache_key(url) + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    verdict, ok = robots_verdict(url)
    time.sleep(1)
    code, ctype, body = http_get(url) if ok else (None, "", b"")
    rec = {"url": url, "robots": verdict, "allowed": ok, "status": code, "ctype": ctype,
           "text": to_text(ctype, body) if body else "", "retrieved": RETRIEVED}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh)
    return rec


def cached(cache: str, url: str) -> dict | None:
    path = os.path.join(cache, cache_key(url) + ".json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'").replace(" ", " ")).strip().lower()


def verify(cache: str, s: Mapping) -> str:
    quotes = s.get("quotes") or ()
    if not quotes:
        return "no quotes"
    recs = [cached(cache, u) for u in s.get("verify_urls") or (s.get("source_url"),)]
    text = norm(" ".join(r["text"] for r in recs if r))
    if not text:
        return "source not cached (robots or fetch failure)"
    hits = sum(1 for q in quotes if norm(q) in text)
    return f"verified {hits}/{len(quotes)}"


def links(page_html: str, base: str) -> tuple[str, ...]:
    hrefs = re.findall(r"""(?i)href\s*=\s*["']([^"'#]+)""", page_html or "")
    return tuple(dict.fromkeys(urllib.parse.urljoin(base, html.unescape(h)) for h in hrefs))


def same_site(url: str, home: str) -> bool:
    strip = lambda h: re.sub(r"^www\.", "", h.lower())  # noqa: E731
    return strip(urllib.parse.urlsplit(url).netloc) == strip(urllib.parse.urlsplit(home).netloc)


def raw_get(cache: str, url: str) -> dict:
    """Like fetch_one, but keeps the raw HTML too (for link discovery)."""
    path = os.path.join(cache, "raw_" + cache_key(url) + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    verdict, ok = robots_verdict(url)
    time.sleep(1)
    code, ctype, body = http_get(url) if ok else (None, "", b"")
    is_pdf = body[:4] == b"%PDF" or "pdf" in ctype
    rec = {"url": url, "robots": verdict, "allowed": ok, "status": code, "ctype": ctype,
           "html": "" if is_pdf else body.decode("utf-8", "ignore"), "text": to_text(ctype, body) if body else ""}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh)
    return rec


def fee_sentences(text: str) -> tuple[str, ...]:
    parts = re.split(r"(?<=[.;:!?])\s+|\n{2,}", re.sub(r"[ \t]+", " ", text))
    return tuple(dict.fromkeys(p.strip()[:400] for p in parts if FEE_SENT.search(p)))


FEE_TEXT = re.compile(r"(?i)\bfees?\b|minimum|schedule|donor.?advised|\bdaf\b|fund (types|options|agreement)|"
                      r"types of funds|policies|guidelines|open a fund|start a fund|create a fund|establish")


def anchors(page_html: str, base: str) -> tuple[tuple[str, str], ...]:
    found = re.findall(r"""(?is)<a\b[^>]*href\s*=\s*["']([^"'#]+)["'][^>]*>(.*?)</a>""", page_html or "")
    return tuple((urllib.parse.urljoin(base, html.unescape(h)), re.sub(r"<[^>]+>|\s+", " ", t).strip()) for h, t in found)


def score(url: str, text: str) -> int:
    u, t = urllib.parse.unquote(url).lower(), text.lower()
    return (6 * bool(re.search(r"\bfees?\b", t)) + 4 * ("fee" in u and "feed" not in u) + 3 * ("donor" in u or "daf" in u)
            + 2 * bool(re.search(r"donor.?advised|minimum|schedule", t)) + u.endswith(".pdf")
            - 8 * bool(re.search(r"feed|privacy|cookie|event|news|post/|blog|story|stories|career|employment", u)))


def candidates(page: Mapping, home: str) -> tuple[tuple[int, str], ...]:
    an = anchors(page.get("html", ""), page["url"])
    return tuple((score(u, t), u) for u, t in an
                 if u.startswith("http") and (same_site(u, home) and (FEE_LINK.search(urllib.parse.unquote(u)) or FEE_TEXT.search(t))
                                              or (FEE_TEXT.search(t) and re.search(r"(?i)\.pdf|drive\.google|/files?/|uploads|ugd", u))))


def crawl_site(cache: str, ein: str, home: str, max_pages: int = 16) -> dict:
    first = raw_get(cache, home)
    sm = raw_get(cache, urllib.parse.urljoin(home, "/sitemap.xml")) if first["allowed"] else {"html": ""}
    loc_re = r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)"
    sm_all = tuple(re.findall(loc_re, sm.get("html") or ""))
    subs = tuple(u for u in sm_all if u.endswith(".xml") and re.search(r"(?i)page|post-sitemap|sitemap-?\d|pages", u))[:4]
    sm_locs = tuple(u for u in sm_all + tuple(x for sub in subs for x in re.findall(loc_re, raw_get(cache, sub).get("html") or ""))
                    if not u.endswith(".xml"))
    lvl1 = candidates(first, home) + tuple((score(u, ""), u) for u in sm_locs if FEE_LINK.search(urllib.parse.unquote(u)))
    top1 = tuple(dict.fromkeys(u for sc, u in sorted(lvl1, key=lambda x: (-x[0], x[1])) if sc >= 0))[:10]
    pages1 = tuple(raw_get(cache, u) for u in top1)
    lvl2 = tuple(c for p in pages1 for c in candidates(p, home) if c[1] not in top1 and c[1] != home)
    top2 = tuple(dict.fromkeys(u for sc, u in sorted(lvl2, key=lambda x: (-x[0], x[1])) if sc >= 0))[:max_pages - len(top1)]
    pages = pages1 + tuple(raw_get(cache, u) for u in top2)
    hits = tuple((p["url"], sn) for p in (first,) + pages for sn in fee_sentences(p.get("text", "")))
    return {"ein": ein, "home": home, "robots": first["robots"], "home_status": first["status"],
            "n_candidates": len(lvl1) + len(lvl2), "fetched": [p["url"] for p in pages], "hits": hits}


# ----------------------------------------------------------------------------- census rows
def census_row(r: Mapping, cost: Mapping, cache: str | None) -> dict:
    s = FEES.get(r["ein"], {"status": "not_researched"})
    fees = {b: effective_admin_fee(s, b) for b in BALANCES} if s["status"] in RATE_STATUSES else {}
    rec = cached(cache, s["source_url"]) if cache and s.get("source_url") else None
    out = {
        "ein": r["ein"], "name": r["name"], "type4": r["type4"], "sponsor_category": r["sponsor_category"],
        "size_band_fy2024": r["size_band_fy2024"], "stratum": r["stratum"], "stratum_N": r["stratum_N"],
        "stratum_n": r["stratum_n"], "weight": fmt(r["weight"], 3),
        "daf_assets_fy2024": r["daf_assets_fy2024"], "accounts_fy2024_screened": r["accounts_fy2024_screened"],
        "avg_account_fy2024": r["avg_account_fy2024"],
        "website": s.get("website", ""), "fee_status": s["status"],
        "in_2021plus_distribution": "yes" if s["status"] in RATE_2021 else "no",
        "fee_basis": s.get("basis", "") if s.get("tiers") else "",
        "admin_tiers": "; ".join(f"{lo:,.0f}-{'' if up is None else f'{up:,.0f}'}: {rt}%" for lo, up, rt in s.get("tiers") or ()),
        "min_annual_fee_usd": fmt(s.get("min_fee")), "flat_annual_fee_usd": fmt(s.get("flat_fee")),
        "opening_min_usd": fmt(s.get("opening_min")), "gift_fee": s.get("gift_fee", ""),
        "grant_fee": s.get("grant_fee", ""), "investment": s.get("investment", ""),
        "source_url": s.get("source_url", ""), "source_date": s.get("source_date", ""),
        "robots": s.get("robots") or (rec or {}).get("robots") or home_robots(cache, r["ein"]), "quote_check": verify(cache, s) if cache and s.get("quotes") else "",
        "notes": s.get("notes", ""),
    }
    fee_cols = {f"admin_fee_usd_{b // 1000}k": fmt(fees.get(b), 0) for b in BALANCES}
    bps_cols = {f"admin_bps_{b // 1000}k": fmt(bps(fees.get(b), b)) for b in BALANCES}
    act = activity_fee_bps(s) if s["status"] in RATE_STATUSES else None
    cost_cols = {
        "usable_cost": cost.get("usable", ""),
        "cost_bps_alloc_A": cost.get("daf_cost_bps_daf_assets_alloc_A", ""),
        "cost_bps_alloc_G": cost.get("daf_cost_bps_daf_assets_alloc_G", ""),
        "cost_bps_alloc_AM": cost.get("daf_cost_bps_daf_assets_alloc_AM", ""),
        "cost_per_account_alloc_A": cost.get("daf_cost_per_account_alloc_A", ""),
        "cost_per_account_alloc_G": cost.get("daf_cost_per_account_alloc_G", ""),
        "cost_per_account_alloc_AM": cost.get("daf_cost_per_account_alloc_AM", ""),
    }
    fee_at_avg = fee_at_balance(s, num(r["avg_account_fy2024"])) if fees else None
    cover = {
        "fee_usd_at_avg_account": fmt(fee_at_avg, 0),
        "fee_bps_at_avg_account": fmt(bps(fee_at_avg, num(r["avg_account_fy2024"])) if fee_at_avg is not None else None),
        **{f"covers_alloc_{k}": coverage(fee_at_avg, num(cost_cols[f"cost_per_account_alloc_{k}"])) for k in ("A", "G", "AM")},
        **{f"coverage_ratio_alloc_{k}": fmt(ratio(fee_at_avg, num(cost_cols[f"cost_per_account_alloc_{k}"])), 2)
           for k in ("A", "G", "AM")},
    }
    return {**out, **fee_cols, **bps_cols, "activity_fee_bps_at_10pct_turnover": fmt(act), **cost_cols, **cover}


def home_robots(cache: str | None, ein: str) -> str:
    """robots verdict logged when the sponsor's homepage was crawled (read from the cache; never fetches)."""
    path = os.path.join(cache or "", "raw_" + cache_key(SITES.get(ein, "")) + ".json")
    if not cache or ein not in SITES or not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as fh:
        rec = json.load(fh)
    return f"homepage {SITES[ein]}: {rec['robots']}; HTTP {rec['status']}"


def fee_at_balance(s: Mapping, bal: float | None) -> float | None:
    return None if not bal else effective_admin_fee(s, bal)


def ratio(a, b) -> float | None:
    return a / b if a is not None and b else None


def coverage(fee: float | None, cost: float | None) -> str:
    return "" if fee is None or not cost else ("yes" if fee >= cost else "no")


FIELDS = (
    "ein", "name", "type4", "sponsor_category", "size_band_fy2024", "stratum", "stratum_N", "stratum_n", "weight",
    "daf_assets_fy2024", "accounts_fy2024_screened", "avg_account_fy2024", "website", "fee_status",
    "in_2021plus_distribution", "fee_basis",
    "admin_tiers", "min_annual_fee_usd", "flat_annual_fee_usd", "opening_min_usd", "gift_fee", "grant_fee",
    "investment", "admin_fee_usd_25k", "admin_fee_usd_100k", "admin_fee_usd_500k", "admin_bps_25k",
    "admin_bps_100k", "admin_bps_500k", "activity_fee_bps_at_10pct_turnover", "usable_cost", "cost_bps_alloc_A",
    "cost_bps_alloc_G", "cost_bps_alloc_AM", "cost_per_account_alloc_A", "cost_per_account_alloc_G",
    "cost_per_account_alloc_AM", "fee_usd_at_avg_account", "fee_bps_at_avg_account", "covers_alloc_A",
    "covers_alloc_G", "covers_alloc_AM", "coverage_ratio_alloc_A", "coverage_ratio_alloc_G",
    "coverage_ratio_alloc_AM", "source_url", "source_date", "robots", "quote_check", "notes",
)


# ----------------------------------------------------------------------------- report (pure: rows -> markdown)
def has_rate(r: Mapping) -> bool:
    return r["fee_status"] in RATE_2021


def any_term(r: Mapping) -> bool:
    return r["fee_status"] in ANY_TERM


def any_rate(r: Mapping) -> bool:
    return r["fee_status"] in RATE_STATUSES


def known(r: Mapping) -> bool:
    return r["fee_status"] not in UNKNOWN


def pct(t) -> str:
    return "–" if t is None else f"{t[0]*100:.1f}% ({t[1]*100:.1f}–{t[2]*100:.1f}%)"


def kn(rs: Sequence[Mapping], pred) -> str:
    k = sum(1 for r in rs if pred(r))
    return f"{k}/{len(rs)} = {pct(wilson(k, len(rs)))}"


def weighted_share(rows: Sequence[Mapping], pred) -> float | None:
    w = sum(num(r["weight"]) for r in rows)
    return None if not w else sum(num(r["weight"]) for r in rows if pred(r)) / w


def table(head: Sequence[str], body: Iterable[Sequence]) -> str:
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] +
                      ["| " + " | ".join(str(c) for c in b) + " |" for b in body])


def parse_tiers(txt: str) -> tuple[tuple[float, float | None, float], ...]:
    """'0-1,000,000: 0.6%; 1,000,000-: 0.35%' -> ((0, 1e6, 0.6), (1e6, None, 0.35)) (top-100 census format)."""
    parts = re.findall(r"([\d,]+)-([\d,]*):\s*([\d.]+)%", txt or "")
    return tuple((num(lo), num(hi) if hi else None, float(rt)) for lo, hi, rt in parts)


def top100_schedule(r: Mapping) -> dict:
    return {"tiers": parse_tiers(r["admin_tiers"]), "basis": r["fee_basis"] or "marginal",
            "min_fee": num(r["min_annual_fee_usd"]), "flat_fee": num(r["flat_annual_fee_usd"])}


def share_at_or_below(xs: Sequence[float | None], cut: float) -> str:
    v = [x for x in xs if x is not None]
    k = sum(1 for x in v if x <= cut)
    return f"{k}/{len(v)} = {pct(wilson(k, len(v)))}"


def report(rows: Sequence[Mapping], top100: Sequence[Mapping], frame: Sequence[Mapping],
           cost_all: Sequence[Mapping] = ()) -> str:
    groups = (("All 60", rows),) + tuple((t, tuple(r for r in rows if r["type4"] == t)) for t in TYPES) + \
             tuple((f"band {b}", tuple(r for r in rows if r["size_band_fy2024"] == b)) for b in TAIL_BANDS)
    design = table(("Stratum (type|band)", "Frame N", "Sample n", "Weight N/n"),
                   ((k, sum(1 for f in frame if f"{f['type4']}|{f['size_band_fy2024']}" == k),
                     sum(1 for r in rows if r["stratum"] == k),
                     next((r["weight"] for r in rows if r["stratum"] == k), "")) for k in dict.fromkeys(r["stratum"] for r in rows)))
    statuses = ("published_schedule", "published_no_admin_fee", "published_pre2021", "published_unread", "partial",
                "no_published_fee", "no_website_found", "robots_blocked")
    status = table(("Group", "n") + statuses,
                   ((g, len(rs)) + tuple(sum(r["fee_status"] == st for r in rs) for st in statuses) for g, rs in groups))
    rate = table(("Group", "2021+ admin rate published (k/n, Wilson 95%)", "Any rate incl. pre-2021",
                  "Any fee term or linked schedule", "2021+ rate, readable sites only", "Design-weighted 2021+ rate"),
                 ((g, kn(rs, has_rate), kn(rs, any_rate), kn(rs, any_term), kn(tuple(filter(known, rs)), has_rate),
                   fmt((weighted_share(rs, has_rate) or 0) * 100) + "%") for g, rs in groups))
    pub = tuple(r for r in rows if has_rate(r))
    fees = table(("Sponsors with a 2021+ rate", "n", "$25k bps", "$100k bps", "$500k bps", "Min annual fee $ (where stated)"),
                 ((g, len(rs), qfmt([num(r["admin_bps_25k"]) for r in rs]), qfmt([num(r["admin_bps_100k"]) for r in rs]),
                   qfmt([num(r["admin_bps_500k"]) for r in rs]), qfmt([num(r["min_annual_fee_usd"]) for r in rs]))
                  for g, rs in (("All", pub), ("CFs", tuple(r for r in pub if r["type4"] == "cf")),
                                ("Non-CF", tuple(r for r in pub if r["type4"] != "cf")))))
    opening = table(("Group", "Opening minimum stated", "Opening minimum $"),
                    ((g, f"{sum(r['opening_min_usd'] != '' for r in rs)}/{len(rs)}", qfmt([num(r["opening_min_usd"]) for r in rs]))
                     for g, rs in (("All 60", rows), ("CFs", tuple(r for r in rows if r["type4"] == "cf")))))
    t100_all = tuple(r for r in top100 if r["status"] != "national_comparator")
    t100 = tuple(r for r in t100_all if r["status"] == "published_schedule")
    t100_fee = {b: [bps(effective_admin_fee(top100_schedule(r), b), b) for r in t100] for b in BALANCES}
    t100_any = sum(r["status"] != "not_found" and r["status"] != "no_rates_published" for r in t100_all)
    tail_cf = tuple(r for r in rows if r["type4"] == "cf")
    cfpub = tuple(r for r in tail_cf if has_rate(r))
    comp = table(("Measure", "Tail CFs (this sample)", "Top-100 CFs (cf-daf-fee-census-2026.csv, as filed)"),
                 (("CFs", len(tail_cf), len(t100_all)),
                  ("2021+ balance-based schedule published", kn(tail_cf, has_rate), f"{len(t100)}/{len(t100_all)} = {pct(wilson(len(t100), len(t100_all)))}"),
                  ("Any fee term / schedule (incl. pre-2021, partial)", kn(tail_cf, any_term),
                   f"{t100_any}/{len(t100_all)} = {pct(wilson(t100_any, len(t100_all)))}"),
                  ("Admin bps at $25k", qfmt([num(r["admin_bps_25k"]) for r in cfpub]), qfmt(t100_fee[25_000])),
                  ("Admin bps at $100k", qfmt([num(r["admin_bps_100k"]) for r in cfpub]), qfmt(t100_fee[100_000])),
                  ("Admin bps at $500k", qfmt([num(r["admin_bps_500k"]) for r in cfpub]), qfmt(t100_fee[500_000])),
                  ("Min annual fee $ (where stated)", qfmt([num(r["min_annual_fee_usd"]) for r in cfpub]),
                   qfmt([num(r["min_annual_fee_usd"]) for r in t100])),
                  ("Opening minimum $ (where stated)", qfmt([num(r["opening_min_usd"]) for r in tail_cf]),
                   qfmt([num(r["min_opening_usd"]) for r in t100]))))
    perr = table(("EIN", "Sponsor", "Type|band", "Status", "Tiers", "Min fee $", "Opening min $", "$25k", "$100k", "$500k", "Source date"),
                 ((r["ein"], r["name"], r["stratum"], r["fee_status"], r["admin_tiers"] or "–", r["min_annual_fee_usd"] or "–",
                   r["opening_min_usd"] or "–", r["admin_bps_25k"] or "–", r["admin_bps_100k"] or "–", r["admin_bps_500k"] or "–",
                   r["source_date"] or "–") for r in rows if any_term(r)))
    cov_rows = tuple(r for r in rows if r["fee_usd_at_avg_account"] != "")

    def cov_line(k: str, rs: Sequence[Mapping]):
        q = quantiles([num(r[f"coverage_ratio_alloc_{k}"]) for r in rs])
        return (k, len(rs), f"{sum(r[f'covers_alloc_{k}'] == 'yes' for r in rs)} of {len(rs)}",
                "–" if q is None else f"{q[1]:.2f} ({q[0]:.2f}–{q[2]:.2f})")
    cov = table(("Rule", "n with fee and allocated cost", "Fee >= allocated cost per account", "Fee / cost, median (IQR)"),
                tuple(cov_line(k, tuple(r for r in cov_rows if r[f"covers_alloc_{k}"] != "")) for k in ("A", "G", "AM")))
    cov_detail = table(("EIN", "Sponsor", "Status", "Avg account $", "Fee at avg $", "Fee bps", "Cost bps A / G / AM",
                        "Cost per account A / G / AM $", "Covers A/G/AM"),
                       ((r["ein"], r["name"], r["fee_status"], fmt(num(r["avg_account_fy2024"]), 0), r["fee_usd_at_avg_account"],
                         r["fee_bps_at_avg_account"],
                         " / ".join(fmt(num(r[f"cost_bps_alloc_{k}"]), 0) or "–" for k in ("A", "G", "AM")),
                         " / ".join(fmt(num(r[f"cost_per_account_alloc_{k}"]), 0) or "–" for k in ("A", "G", "AM")),
                         "/".join(r[f"covers_alloc_{k}"] or "–" for k in ("A", "G", "AM"))) for r in cov_rows))
    cost_cmp = table(("Group", "n", "Rule A bps", "Rule G bps", "AM bps", "Rule A $/account"),
                     ((g, len(rs), qfmt([num(r["cost_bps_alloc_A"]) for r in rs]), qfmt([num(r["cost_bps_alloc_G"]) for r in rs]),
                       qfmt([num(r["cost_bps_alloc_AM"]) for r in rs]), qfmt([num(r["cost_per_account_alloc_A"]) for r in rs]))
                      for g, rs in (("Sampled CFs, 2021+ rate published", cfpub),
                                    ("Sampled CFs, no 2021+ rate", tuple(r for r in tail_cf if not has_rate(r))),
                                    ("Sampled non-CF", tuple(r for r in rows if r["type4"] != "cf")))))
    cf_cost = tuple(r for r in cost_all if r.get("group") == "tail_cf" and r.get("usable") == "1")
    med100 = (quantiles([num(r["admin_bps_100k"]) for r in cfpub]) or (None, None, None))[1]
    cuts = tuple(dict.fromkeys(c for c in (100.0, med100, 200.0) if c is not None))
    pop = table(("All usable tail CFs in the cost study", *[f"cost <= {c:g} bps" for c in cuts]),
                tuple((f"Rule {k}", *[share_at_or_below([num(r[f"daf_cost_bps_daf_assets_alloc_{k}"]) for r in cf_cost], c) for c in cuts])
                      for k in ("A", "G", "AM")))
    return "\n\n".join((
        "## T1 Sample design", design, "## T2 Fee status by group", status,
        "## T3 How often fees are published (k/n, Wilson 95% interval)", rate,
        "## T4 Effective annual admin fee, bps of balance: median (p25-p75; n)", fees, opening,
        "## T5 Tail CFs vs top-100 CF census (top-100 recomputed at the same balances)", comp,
        "## T6 Sponsors publishing any fee term", perr,
        "## T7 Published fee at the sponsor's own FY2024 average account vs allocated operating cost per account", cov, cov_detail,
        "## T8 Allocated operating cost of the sampled sponsors (long-tail cost study)", cost_cmp,
        "## T9 Share of all tail CFs whose allocated cost per DAF dollar is at or below a given fee "
        "(100 bps = top-100 median; middle cut = this sample's tail-CF median at $100k)", pop))


# ----------------------------------------------------------------------------- tasks
def task_sample(sample: Sequence[Mapping]) -> str:
    lines = ["stratum|stratum_N|stratum_n|ein|name|daf_assets_fy2024"]
    return "\n".join(lines + [f"{r['stratum']}|{r['stratum_N']}|{r['stratum_n']}|{r['ein']}|{r['name']}|{r['daf_assets_fy2024']}"
                              for r in sample])


def all_urls() -> tuple[str, ...]:
    return tuple(dict.fromkeys(u for s in FEES.values() for u in (s.get("verify_urls") or (s.get("source_url"),)) if u))


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--task", choices=("sample", "crawl", "fetch", "census"), required=True)
    ap.add_argument("--cache-dir")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--url", action="append", default=[])
    a = ap.parse_args(argv)
    os.chdir(a.root)
    sample = draw(tail_frame(read_csv(LT_CSV)))
    if a.task == "sample":
        print(task_sample(sample))
        return 0
    if a.task == "crawl":
        os.makedirs(a.cache_dir, exist_ok=True)
        targets = [(e, SITES[e]) for e in (a.url or [r["ein"] for r in sample]) if SITES.get(e)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            res = list(ex.map(lambda t: crawl_site(a.cache_dir, *t), targets))
        with open(os.path.join(a.cache_dir, "crawl_summary.json"), "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("\n".join(f"{r['ein']}\t{r['home_status']}\t{r['robots']}\t{r['n_candidates']}\t{len(r['hits'])}" for r in res))
        return 0
    if a.task == "fetch":
        if not (a.fetch and a.cache_dir):
            print("fetch needs --fetch and --cache-dir", file=sys.stderr)
            return 2
        os.makedirs(a.cache_dir, exist_ok=True)
        recs = [fetch_one(a.cache_dir, u) for u in (a.url or all_urls())]
        print("\n".join(f"{r['status']}\t{r['robots']}\t{len(r['text'])}\t{r['url']}" for r in recs))
        return 0
    cost = {r["ein"]: r for r in read_csv(COST_CSV)}
    rows = tuple(census_row(r, cost.get(r["ein"], {}), a.cache_dir) for r in sample)
    write_csv(OUT_CSV, rows, FIELDS)
    print(report(rows, read_csv(TOP100_CSV), tail_frame(read_csv(LT_CSV)), tuple(cost.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
