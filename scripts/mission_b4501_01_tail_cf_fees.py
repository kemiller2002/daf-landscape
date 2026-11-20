#!/usr/bin/env python3
"""P-B4501-01: enlarge the tail community-foundation (CF) fee sample. Task id b4501-01.

Wrapper around scripts/mission_long_tail_fee_census.py (task b45n33-01), which is imported and NOT modified. Reused from
it unchanged: the frame (tail_frame), the strata (strata), the allocation rule (allocate), the robots-checked crawler
(crawl_site / raw_get / fetch_one, user agent "research-script/1.0"), the fee engine (effective_admin_fee, bps), the
quote verifier (verify), Wilson intervals and the original 60-row draw (draw), whose 31 CFs are excluded here.

Sampling (same seed scheme, CF strata only)
  Frame: the 641 tail CFs (base tail_frame, type4 == cf), strata cf x {t10_50, t1_10, t0_1, zero} at the SAME stratum
  index as the base (0..3). The original draw's 31 CFs are removed. n = 60 is allocated over the four remaining strata
  with the base allocate() (proportional, floor 1, largest remainder). Within stratum i:
  random.Random(SEED_EXT + i).sample(remaining rows sorted by EIN, a_i), SEED_EXT = 20261120 (base: 20261119 + i).
  Homepages: cf-vendor-map-by-ein-v2.csv `homepage` (from the 990 WebsiteAddressTxt), as in the base census.

Tasks
  sample   print the extension draw (stratum, N, n, EIN, name, homepage)
  crawl    base.crawl_site for every drawn CF with a homepage (robots.txt read and logged before any page); --fetch
           required to touch the network; cache in --cache-dir (outside the repo). Writes crawl_summary_ext.json there.
  fetch    base.fetch_one for every verify URL in FEES_EXT (robots-checked) -- needs --fetch.
  hits     print the fee sentences and candidate URLs found per sponsor from the cache (for transcription).
  robots   print the robots.txt verdict logged for every host touched (from the cache; never fetches).
  census   verify quotes, compute fees, write data/mission-2026-11-14/tail-cf-fee-sample-2026-11-20.csv and print every
           table used in research/mission-2026-11-14/b4501-01-tail-cf-fee-sample.md (medians with seeded bootstrap).

Usage (cache outside the repo):
  python3 -I scripts/mission_b4501_01_tail_cf_fees.py . --task sample
  python3 -I scripts/mission_b4501_01_tail_cf_fees.py . --task crawl --cache-dir CACHE --fetch
  python3 -I scripts/mission_b4501_01_tail_cf_fees.py . --task fetch --cache-dir CACHE --fetch
  python3 -I scripts/mission_b4501_01_tail_cf_fees.py . --task census --cache-dir CACHE
"""
from __future__ import annotations

import argparse
import concurrent.futures
import glob
import importlib.util
import json
import os
import random
import re
import statistics
import sys
import urllib.parse
from typing import Mapping, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))


def load_base():
    spec = importlib.util.spec_from_file_location("lt_fee_census", os.path.join(HERE, "mission_long_tail_fee_census.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = load_base()
DATA = B.DATA
VMAP_CSV = f"{DATA}/cf-vendor-map-by-ein-v2.csv"
REALISED_CSV = f"{DATA}/tail-realised-fees-all-2026-11-20.csv"
OUT_CSV = f"{DATA}/tail-cf-fee-sample-2026-11-20.csv"
SEED_EXT = 20261120
N_EXT = 60
N_BOOT = 10_000
BOOT_SEED = 4501
RETRIEVED = "2026-11-20"

# ----------------------------------------------------------------------------- transcription (filled after research)
# Same structure as base FEES. status: published_schedule | published_no_admin_fee | published_pre2021 |
# published_unread | partial | no_published_fee | no_website_found | robots_blocked | bot_challenge | site_unreachable
# (bot_challenge: the host answers research-script/1.0 with a "please wait while your request is being verified" page;
#  site_unreachable: TLS failure or HTTP 5xx on every page. Both are unknown, like robots_blocked.)
_NPF = "no_published_fee"
FEES_EXT: dict[str, dict] = {
    # ================= cf|t10_50
    "450336015": dict(status=_NPF, notes="DAF pages, giving options and advisor pages read (and sitemap-listed pages): no DAF fee or minimum."),
    "586033468": dict(status=_NPF, notes="Wix site; the 11 sitemap pages include services and donate (read): no DAF fee or minimum."),
    "522395867": dict(status="published_unread", website="https://www.juneaucf.org/",
        source_url="https://www.juneaucf.org/advisors/",
        source_date="live 2026-11-20; linked 'Philanthropic Fund Fee Schedule 2025' (wp-content upload 2025-02)",
        quotes=("Funds at the Community Foundation have a modest administrative fee", "Philanthropic Fund Fee Schedule 2025"),
        notes="Advisor page links Philanthropic-Fund-Fee-Schedule-2025.pdf; robots.txt allows it, but the host returned a bot-verification "
              "page ('Please wait while your request is being verified') instead of the PDF, so no rate could be read."),
    "386095474": dict(status="partial", website="https://www.lenaweecommunityfoundation.com/", opening_min=10_000,
        source_url="https://lenaweecommunityfoundation.com/establish-a-fund/", source_date="live 2026-11-20",
        quotes=("Funds begin with a minimum of $10,000",),
        notes="Opening minimum only (all fund types). Several pages and the advisor guide PDF returned a bot-verification page."),
    "351990305": dict(status="published_schedule", website="https://www.dccommunityfoundation.org/",
        tiers=((0, None, 1.0),), basis="marginal", opening_min=10_000,
        gift_fee="Non-endowed: one-time 1% fee on contributions", grant_fee="not stated",
        investment="Graystone Consulting pools; investment fees not stated",
        source_url="https://www.dccommunityfoundation.org/s/Donor-Advised-Fund-Options-szda.pdf", source_date="undated PDF, live 2026-11-20",
        quotes=("Non-Endowed Funds: One-time 1% fee on contributions", "annual 1% on fund balance (assessed monthly)",
                "Starting minimum $10,000", "Endowed Funds: 1% on assets up to $1 million; scales down for higher balances"),
        notes="Non-endowed DAF used (1% a year plus a 1% gift fee, excluded from the effective fee). Endowed DAF: $25,000 minimum, "
              "1% to $1m, 'scales down' above (unquantified): also 100 bps at all three balances."),
    "840794536": dict(status="published_schedule", website="https://www.yvcf.org/",
        tiers=((0, 1_000_000, 1.0), (1_000_000, 5_000_000, 0.75), (5_000_000, 10_000_000, 0.5), (10_000_000, None, 0.25)),
        basis="marginal", min_fee=250, gift_fee="not stated", grant_fee="not stated",
        investment="Investment management fees separate (DAF policy, board approved May 17, 2024)",
        source_url="https://yvcf.org/wp-content/uploads/2022/10/Professional-Services-Fee-Structure_10.25.22.pdf",
        verify_urls=("https://yvcf.org/wp-content/uploads/2022/10/Professional-Services-Fee-Structure_10.25.22.pdf",
                     "https://yvcf.org/wp-content/uploads/2025/12/DAF-Policies-and-Procedures-051724.pdf"),
        source_date="'10/25/22' (fee structure); DAF policy 'Board Approved May 17, 2024' points to it",
        quotes=("Donor Advised Funds $250 For the first $1 million", "Next $4 million ($1 million to $5 million)",
                "10/25/22", "Board Approved May 17, 2024"),
        notes="Marginal reading of 'For the first $1 million / Next $4 million ...'. Effective 100 bps at all three balances."),
    "311768219": dict(status="site_unreachable", website="https://www.knoxcf.org/",
        notes="Homepage readable; every inner page (advisor FAQs, DAF FAQs, types of funds, policies) returned HTTP 500 on 2026-11-20."),
    "821388190": dict(status="published_schedule", website="https://www.horizoncfnky.org/",
        tiers=((0, 1_000_000, 1.0), (1_000_000, 2_500_000, 0.8), (2_500_000, None, 0.6)), basis="marginal", min_fee=250,
        opening_min=25_000, gift_fee="not stated", grant_fee="not stated",
        investment="'Investment and credit card fees are not included in the Community Support Fees'",
        source_url="https://horizoncfnky.org/how-to-get-involved/types-of-giving/designated-funds/designated-funds-fee-schedule/",
        verify_urls=("https://horizoncfnky.org/how-to-get-involved/types-of-giving/designated-funds/designated-funds-fee-schedule/",
                     "https://horizoncfnky.org/wp-content/uploads/2024/01/2025-Portfolio_Options_Fee_Schedule.pdf"),
        source_date="page modified 2025-07-18; '2025-Portfolio_Options_Fee_Schedule.pdf'",
        quotes=("Fund minimum: $25,000 (Donor Advised Funds", "100 basis points (1%) on the first $1 million",
                "on the value between $1 million and $2.5 million", "on the value above $2.5 million",
                "All funds are subject to an annual $250 minimum fee"),
        notes="One Community Support Fee schedule covers DAFs, designated and scholarship funds."),
    "251407396": dict(status="partial", website="https://www.comm-foundation.org/", opening_min=0,
        source_url="https://www.comm-foundation.org/professional-advisors", verify_urls=("https://www.comm-foundation.org/professional-advisors",
                                                                                          "https://www.comm-foundation.org/"),
        source_date="live 2026-11-20", quotes=("Our administrative fees are among the lowest", "NO MINIMUMS TO SET UP A FUND"),
        notes="Fee described but not quantified; no minimum to open a fund."),
    "411429402": dict(status="partial", website="https://www.dsacommunityfoundation.com/", opening_min=25_000,
        source_url="https://www.dsacommunityfoundation.com/giving/how-to-open-a-fund", source_date="live 2026-11-20 (now Boreal Waters CF)",
        quotes=("The minimum contribution to establish a Donor-Advised Fund is $25,000",), notes="Opening minimum only."),
    "237041310": dict(status="partial", website="https://www.bryanareafoundation.org/", opening_min=100_000,
        source_url="https://www.bryanareafoundation.org/wp-content/uploads/2026/08/7-1-2026-DONOR-Handbook.pdf",
        source_date="Donor Handbook dated 7-1-2026 (upload 2026-08)",
        quotes=("The minimum gift to establish a Donor Advised Fund is $100,000",
                "including the names of investment manager, investment and administrative fees"),
        notes="Opening minimum; fees available on request only."),
    "416017740": dict(status="partial", website="https://www.rochesterarea.org/", opening_min=10_000,
        source_url="https://rochesterarea.org/giving/start-a-new-fund/", source_date="live 2026-11-20",
        quotes=("Donor advised funds can be created with a minimum gift of $10,000",), notes="Opening minimum only."),
    "251380549": dict(status=_NPF, notes="Funds, donors, component-fund and FAQ pages read: no DAF fee or minimum."),
    "237310660": dict(status="published_schedule", website="https://www.hafoundation.org/",
        tiers=((0, None, 1.75),), basis="marginal", gift_fee="not stated", grant_fee="not stated",
        investment="Investment advisers' fee about 0.61%, netted in returns",
        source_url="https://hafoundation.org/ways-to-support/giving-start-a-fund/", source_date="live 2026-11-20 (undated page)",
        quotes=("The fee for most funds is currently 1.75% of the fund balance", "This fee is approximately .61%"),
        notes="'Most funds' rate applied to DAFs; scholarship (2%) and agency (tiered from 1.5%) funds differ."),
    "363309554": dict(status="no_website_found", notes="No homepage in cf-vendor-map (990 WebsiteAddressTxt blank); web search found only third-party listings."),
    "314446189": dict(status="published_schedule", website="https://marioncommunityfoundation.org/",
        tiers=((0, None, 1.0),), basis="marginal", gift_fee="not stated", grant_fee="not stated", investment="not stated",
        source_url="https://marioncommunityfoundation.org/resources/advisor-toolkit/", source_date="live 2026-11-20 (undated page)",
        quotes=("a administrative fee rate of 1.0% for all fund types",),
        notes="990 homepage www.marioncommunityfoundation.org fails TLS (certificate name mismatch); the bare domain was robots-checked and read."),
    "481022361": dict(status="published_schedule", website="https://wichitafoundation.org/",
        tiers=((0, 50_000, 2.0), (50_000, 250_000, 1.5), (250_000, 2_500_000, 1.0), (2_500_000, 5_000_000, 0.75),
               (5_000_000, 10_000_000, 0.5), (10_000_000, 25_000_000, 0.35), (25_000_000, None, 0.25)),
        basis="marginal", min_fee=200, gift_fee="not stated", grant_fee="not stated", investment="not stated",
        source_url="https://wichitafoundation.org/giving-and-investing/become-a-fund-holder",
        verify_urls=("https://wichitafoundation.org/giving-and-investing/become-a-fund-holder",
                     "https://wichitafoundation.org/assets/uploads/documents/WF_Support_Fee.pdf"),
        source_date="live 2026-11-20 (undated page and PDF)",
        quotes=("Charitable Funds $10,000 to $50,000 2.0%", "$50,000 to $250,000 1.5%", "$250,001 to $2,500,000 1.0%",
                "Note: Charitable Funds below $10,000 = $200 fee", "Total Annual Fees $1,750"),
        notes="'Charitable Funds' scale. The PDF's worked examples ($1,750 at $100k, $6,500 at $500k) are reproduced by charging 2.0% "
              "on the first $50k with a $200 floor."),
    "383649922": dict(status="bot_challenge", website="https://www.sturgisfoundation.org/",
        notes="robots.txt allows; homepage and advisor page returned a bot-verification page."),
    "371372729": dict(status=_NPF, notes="DAF, funds (77k chars), advisor and endowment pages read: no DAF fee or minimum."),
    # ================= cf|t1_10
    "351640051": dict(status=_NPF, notes="Squarespace site; donors page and sitemap read: no DAF fee or minimum."),
    "383087756": dict(status=_NPF, notes="DAF page and all 'our funds' pages read: no DAF fee or minimum."),
    "474252695": dict(status="published_schedule", website="https://www.cffgr.org/",
        tiers=((0, 1_000_000, 1.5), (1_000_000, 5_000_000, 1.0), (5_000_000, None, 0.75)), basis="marginal", min_fee=250,
        opening_min=5_000, gift_fee="Optional 'Foundation Sustainer' contribution (suggested around 5%)", grant_fee="not stated",
        investment="ETF portfolio (investment policy 12/2025); fees not stated",
        source_url="https://www.cffgr.org/s/Support-Fees-Minimums-12-2025.pdf", source_date="'November 2025' (file name 12-2025)",
        quotes=("$5,000 minimum initial gift", "$250 minimum annual fee", "Each semi-annual fee equals half of", "1 of 1 November 2025"),
        notes="1.5% on the first $1m, 1.0% to $5m, 0.75% above; $1,000 minimum balance."),
    "237372791": dict(status="published_schedule", website="https://www.yscf.org/",
        tiers=((0, None, 0.5),), basis="marginal", gift_fee="0.50% on gifts requested to be granted immediately", grant_fee="not stated",
        investment="not stated separately",
        source_url="https://www.yscf.org/wp-content/uploads/2026/06/YSCF-Investment-Fee-Policy-2026-adopted.pdf",
        source_date="'Effective: June 2026 | Revised 2026 | Board Approved: June 22, 2026'",
        quotes=("3 Donor Advised Funds 0.50% annually; assessed quarterly (0.125%", "Board Approved: June 22, 2026"),
        notes="DAF tier 3. Endowment and spend-down field-of-interest funds pay 2%."),
    "341792862": dict(status="bot_challenge", website="https://www.eriefoundation.org/",
        notes="robots.txt allows; homepage returned a bot-verification page, so nothing could be read."),
    "201485011": dict(status="partial", website="https://www.placercf.org/", opening_min=10_000,
        source_url="https://www.placercf.org/create-a-fund", source_date="live 2026-11-20",
        quotes=("The current minimum to establish a Donor Advised Fund is $10,000",), notes="Opening minimum only."),
    "042103944": dict(status="published_schedule", website="https://brooklinecommunity.org/",
        tiers=((0, None, 1.5),), basis="marginal", min_fee=250, opening_min=5_000, gift_fee="not stated", grant_fee="not stated",
        investment="Investment policy approved 2024-11-19; fees not stated",
        source_url="https://brooklinecommunity.org/fund-fee-policy/", source_date="live 2026-11-20 (policies page updated 2026-01-21)",
        quotes=("Donor-Advised Fund $10,000 for endowed $5,000 for non-endowed 1.5% annually and applied quarterly $750 minimum for endowed $250 minimum for non-endowed",),
        notes="Non-endowed DAF used ($250 minimum fee). Endowed: $10,000 to open, $750 minimum fee (300 bps at $25k). robots.txt on www "
              "timed out during the crawl; re-read 2026-11-20 (200, allowed) before use."),
    "873682838": dict(status="site_unreachable", website="https://greatertaylorfoundation.org/",
        notes="TLS failure (self-signed certificate) on robots.txt and homepage; TLS verification was not disabled."),
    "251813245": dict(status=_NPF, notes="Ways to give, advisors, our-funds (98k chars) read: no DAF fee or minimum."),
    "237227875": dict(status=_NPF, notes="Give and advisor pages read: no DAF fee or minimum."),
    "351811149": dict(status=_NPF, notes="Donor-advisor pages and fund list read: no DAF fee or minimum."),
    "943205217": dict(status="partial", website="https://www.kitsapfoundation.org/",
        source_url="https://www.kitsapfoundation.org/_files/ugd/a04714_d96affbd6e424ba3afe5b2e89d652998.pdf", source_date="undated PDF, live 2026-11-20",
        quotes=("A list of fees is available upon request",), notes="Fees exist but are 'available upon request'."),
    "239031005": dict(status=_NPF, notes="Give and advise pages read: no DAF fee or minimum."),
    "936022916": dict(status="published_schedule", website="https://www.bcfgives.org/",
        tiers=((0, 2_000_000, 1.25), (2_000_000, None, 0.75)), basis="marginal", gift_fee="none stated ('no set-up fee')",
        grant_fee="not stated", investment="Investment management fee 'currently 0.20%'",
        source_url="https://bcfgives.org/wp-content/uploads/2025/04/BCF-Donor-Advised-Fund-Fund-Agreement-Template.pdf",
        source_date="DAF agreement template uploaded 2025-04",
        quotes=("Annual Fees Charged to Donor Advised Funds of Benton Community Foundation", "The first $2,000,000 1.25% per annum",
                "Additional amounts >$2,000,000 .75% per annum", "The fee is currently 0.20%"),
        notes="Schedule A of the DAF agreement. Named funds need $15,000 (types-of-funds page); not recorded as the DAF minimum."),
    "391711388": dict(status="bot_challenge", website="https://www.cfsw.org/",
        notes="robots.txt allows; homepage returned a bot-verification page."),
    "351814927": dict(status="published_schedule", website="https://www.wicf-inc.org/",
        tiers=((0, None, 1.0),), basis="marginal", gift_fee="not stated", grant_fee="not stated", investment="not stated",
        source_url="https://www.wicf-inc.org/administrative-fees", source_date="live 2026-11-20 (undated page)",
        quotes=("Annual Rate: 1%", "Based on the market value of each fund on December 31 of the preceding year"),
        notes="One rate for every fund."),
    "351839759": dict(status=_NPF, notes="Giving, fund list and ways-to-give pages read: no DAF fee or minimum."),
    "911572414": dict(status="published_schedule", website="https://www.skagitcf.org/",
        tiers=((0, 100_000, 2.0), (100_000, 500_000, 1.75), (500_000, None, 1.5)), basis="flat_on_total",
        gift_fee="non-invested funds: fee charged per gift", grant_fee="not stated", investment="not stated",
        source_url="https://www.skagitcf.org/uploads/1/5/1/2/15121716/about_scf_fund_types.pdf", source_date="undated PDF, live 2026-11-20",
        quotes=("SCF Community Support Fees", "$10k-$99k $100k-$499k $500k+", "2% 1.75% 1.5%",
                "The administrative fees listed are total annual fees, assessed quarterly"),
        notes="Read as a band rate on the whole balance (table by balance). Marginal reading: 200 / 200 / 180 bps at $25k / $100k / $500k."),
    "341837854": dict(status="published_no_admin_fee", website="https://newbremenfoundation.org/",
        tiers=((0, None, 0.0),), basis="marginal", gift_fee="none ('no start up costs')", grant_fee="not stated", investment="not stated",
        source_url="https://www.newbremenfoundation.org/faq", source_date="live 2026-11-20 (undated page)",
        quotes=("There are no start up costs to establish a fund", "so there is no cost to maintain the fund"),
        notes="'Currently the Foundation underwrites its fund fees': 0% for every fund."),
    "391819945": dict(status="partial", website="https://www.cfdunncounty.org/",
        source_url="https://www.cfdunncounty.org/", verify_urls=("https://www.cfdunncounty.org/", "http://cfdunncounty.org/give/"),
        source_date="live 2026-11-20", quotes=("with low administrative fees",), notes="Fee described, not quantified."),
    "810791445": dict(status=_NPF, notes="Wix site; fund-your-passion, why-give and DAF blog post read: no DAF fee or minimum."),
    "205502851": dict(status=_NPF, notes="No robots.txt (404); giving and funds pages read: no DAF fee or minimum."),
    "300254793": dict(status=_NPF, notes="Get-started and funds pages read: no fee. The FAQ page returned a bot-verification page."),
    "351857065": dict(status=_NPF, notes="Donors, we-hold-funds and advisor pages read: no DAF fee or minimum."),
    "201838372": dict(status="no_website_found", notes="No homepage in cf-vendor-map; web search found issuu brochures and third-party listings only (not read)."),
    "363569968": dict(status=_NPF, notes="DAF, open-a-fund and advisor pages read: no fee; 'little or no minimum' and no minimum balance (not a stated term)."),
    # ================= cf|t0_1
    "842084322": dict(status="partial", website="https://www.marthasvineyardcf.org/", opening_min=25_000,
        source_url="https://marthasvineyardcf.org/donors/donors-faqs/", source_date="live 2026-11-20",
        quotes=("The minimum amount to establish a new endowed or non-endowed fund is $25,000",), notes="Opening minimum only."),
    "367146151": dict(status="no_website_found", notes="No homepage in cf-vendor-map; web search found only third-party listings."),
    "475029315": dict(status="bot_challenge", website="https://www.rhinelandercommunityfoundation.com/",
        notes="robots.txt allows; homepage, established-funds and FAQ pages returned a bot-verification page (one short page read, no fee)."),
    "204265927": dict(status="no_website_found", notes="No homepage in cf-vendor-map (a realty-holding affiliate by name)."),
    "237019029": dict(status="partial", website="https://www.albionfoundation.org/", opening_min=10_000,
        source_url="https://albionfoundation.org/donate/establish-a-fund/", source_date="live 2026-11-20",
        quotes=("The Foundation allocates an administrative distribution annually based on the total assets",
                "Minimum principal: $10,000 Scholarship Funds"),
        notes="Admin charge described, not quantified; DAF minimum principal $10,000 (to begin grants, within three years)."),
    "476024770": dict(status=_NPF, website="https://www.merrick-foundation.org/",
        notes="Homepage, fund list and fund-types page (merrickfoundation.org) read: no DAF fee or minimum."),
    "200194557": dict(status="partial", website="https://www.dublinfoundation.org/",
        source_url="https://www.dublinfoundation.org/resources/establishing-a-donor-advised-fund/",
        verify_urls=("https://www.dublinfoundation.org/resources/establishing-a-donor-advised-fund/",),
        source_date="live 2026-11-20", quotes=("contributing an agreed minimum amount (e.g., $25,000)",),
        notes="Minimum given only as an example ('e.g., $25,000'), so opening_min is left blank. The corporate-fund page mentions 'a nominal annual fee'."),
    "351889139": dict(status="partial", website="https://www.cfpartner.org/", opening_min=25_000,
        source_url="https://www.cfpartner.org/funds", source_date="live 2026-11-20 (minimums stated as effective 2012)",
        quotes=("Donor Advised, Scholarships, and Named Funds- A minimum gift of $25,000",
                "determined in accordance with the then current fee schedule"),
        notes="990 homepage cfpartner.org fails TLS (name mismatch); www.cfpartner.org robots-checked and read. Fee schedule referred to, not published."),
    "630864276": dict(status=_NPF, notes="Squarespace site; give page read: no DAF fee or minimum."),
    "841246756": dict(status="published_schedule", website="https://www.broomfieldfoundation.org/",
        tiers=((0, None, 1.5),), basis="marginal", gift_fee="not stated", grant_fee="not stated", investment="not stated",
        source_url="https://www.broomfieldfoundation.org/about/faqs", source_date="live 2026-11-20 (undated page)",
        quotes=("Most Donor Advised Funds are charged an annual fee of 1.5%, although some exceptions apply",),
        notes="'Most' DAFs; exceptions unstated."),
    "841128761": dict(status="robots_blocked", website="http://www.montrosecf.com/",
        notes="robots.txt (read over http; https fails TLS) is 'User-agent: * Disallow: /', so nothing was fetched."),
    "363324526": dict(status=_NPF, notes="Static site; home, about and donate pages read: no DAF fee or minimum."),
    "466040496": dict(status="no_website_found", notes="No homepage in cf-vendor-map; web search found only third-party listings."),
    "391585271": dict(status="partial", website="https://statelinecf.org/", opening_min=20_000,
        source_url="https://statelinecf.org/give/", source_date="live 2026-11-20",
        quotes=("$20,000 minimum to open a donor-advised fund",), notes="Opening minimum only; DAFs are endowed."),
    # ================= cf|zero
    "860250582": dict(status=_NPF, notes="Squarespace site; donor and ways-to-give pages read: no DAF fee or minimum."),
}


# ----------------------------------------------------------------------------- sampling
def cf_strata(frame: Sequence[Mapping]):
    """(stratum index in the base 16-cell list, key, rows sorted by EIN) for the four CF strata."""
    return tuple((i, k, rows) for i, (k, rows) in enumerate(B.strata(frame)) if k[0] == "cf")


def draw_ext(frame: Sequence[Mapping], exclude: frozenset, n: int = N_EXT, seed: int = SEED_EXT) -> tuple[dict, ...]:
    st = tuple((i, k, rows, tuple(r for r in rows if r["ein"] not in exclude)) for i, k, rows in cf_strata(frame))
    alloc = B.allocate(tuple(len(rem) for *_, rem in st), n)
    return tuple(
        {**r, "stratum": f"{k[0]}|{k[1]}", "stratum_N": len(rows), "stratum_N_remaining": len(rem), "stratum_n": a,
         "stratum_n_orig": len(rows) - len(rem), "weight": len(rows) / a, "weight_pooled": len(rows) / (a + len(rows) - len(rem))}
        for (i, k, rows, rem), a in zip(st, alloc)
        for r in random.Random(seed + i).sample(rem, a)
    )


def homepages(vmap_rows: Sequence[Mapping]) -> dict:
    return {r["ein"]: r["homepage"].strip() for r in vmap_rows if r.get("homepage", "").strip()}


def original_sample(frame):
    return B.draw(frame)


# ----------------------------------------------------------------------------- statistics
def median(xs: Sequence[float]) -> float | None:
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def boot_median(xs: Sequence[float], n_boot: int = N_BOOT, seed: int = BOOT_SEED, alpha: float = 0.05):
    """Percentile bootstrap of the median: (median, lo, hi)."""
    xs = [x for x in xs if x is not None]
    if len(xs) < 2:
        return (xs[0], xs[0], xs[0]) if xs else None
    rng = random.Random(seed)
    meds = sorted(statistics.median(rng.choices(xs, k=len(xs))) for _ in range(n_boot))
    return statistics.median(xs), meds[int(alpha / 2 * n_boot)], meds[int((1 - alpha / 2) * n_boot) - 1]


def boot_share(flags: Sequence[bool], n_boot: int = N_BOOT, seed: int = BOOT_SEED, alpha: float = 0.05):
    flags = list(flags)
    if not flags:
        return None
    rng = random.Random(seed)
    sh = sorted(sum(rng.choices(flags, k=len(flags))) / len(flags) for _ in range(n_boot))
    return sum(flags) / len(flags), sh[int(alpha / 2 * n_boot)], sh[int((1 - alpha / 2) * n_boot) - 1]


def weighted_median(pairs: Sequence[tuple[float, float]]) -> float | None:
    """Lower weighted median of (value, weight) pairs."""
    ps = sorted((v, w) for v, w in pairs if v is not None)
    if not ps:
        return None
    half = sum(w for _, w in ps) / 2
    cum = [sum(w for _, w in ps[:j + 1]) for j in range(len(ps))]
    return next(v for (v, _), c in zip(ps, cum) if c >= half)


def bfmt(t, nd: int = 0) -> str:
    return "–" if t is None else f"{t[0]:,.{nd}f} ({t[1]:,.{nd}f}–{t[2]:,.{nd}f})"


def sfmt(k: int, n: int, flags=None) -> str:
    w = B.wilson(k, n)
    if w is None:
        return "–"
    b = boot_share(flags) if flags is not None else None
    return (f"{k}/{n} = {w[0]*100:.1f}% (Wilson {w[1]*100:.1f}–{w[2]*100:.1f}%"
            + (f"; bootstrap {b[1]*100:.1f}–{b[2]*100:.1f}%)" if b else ")"))


# ----------------------------------------------------------------------------- census rows
def host_of(url: str) -> str:
    return urllib.parse.urlsplit(url).netloc.lower()


def cached_raw(cache: str | None, url: str) -> dict | None:
    if not cache or not url:
        return None
    path = os.path.join(cache, "raw_" + B.cache_key(url) + ".json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def home_log(cache: str | None, home: str) -> str:
    rec = cached_raw(cache, home)
    return "" if rec is None else f"homepage {home}: {rec['robots']}; HTTP {rec['status']}"


def ext_row(r: Mapping, home: str, realised: Mapping, cache: str | None) -> dict:
    s = FEES_EXT.get(r["ein"], {"status": "not_researched"})
    rate = s["status"] in B.RATE_STATUSES
    fees = {b: B.effective_admin_fee(s, b) for b in B.BALANCES} if rate else {}
    rec = B.cached(cache, s["source_url"]) if cache and s.get("source_url") else None
    avg = B.num(r["avg_account_fy2024"])
    fee_avg = B.fee_at_balance(s, avg) if rate else None
    return {
        "ein": r["ein"], "name": r["name"], "sample": "ext_b4501_01", "stratum": r["stratum"],
        "size_band_fy2024": r["size_band_fy2024"], "stratum_N": r["stratum_N"], "stratum_n_orig": r["stratum_n_orig"],
        "stratum_n_ext": r["stratum_n"], "weight_ext": B.fmt(r["weight"], 3), "weight_pooled": B.fmt(r["weight_pooled"], 3),
        "daf_assets_fy2024": r["daf_assets_fy2024"], "accounts_fy2024_screened": r["accounts_fy2024_screened"],
        "avg_account_fy2024": r["avg_account_fy2024"], "website": s.get("website") or home,
        "fee_status": s["status"], "in_2021plus_distribution": "yes" if s["status"] in B.RATE_2021 else "no",
        "fee_basis": s.get("basis", "") if s.get("tiers") else "",
        "admin_tiers": "; ".join(f"{lo:,.0f}-{'' if up is None else f'{up:,.0f}'}: {rt}%" for lo, up, rt in s.get("tiers") or ()),
        "min_annual_fee_usd": B.fmt(s.get("min_fee")), "flat_annual_fee_usd": B.fmt(s.get("flat_fee")),
        "opening_min_usd": B.fmt(s.get("opening_min")), "gift_fee": s.get("gift_fee", ""), "grant_fee": s.get("grant_fee", ""),
        "investment": s.get("investment", ""),
        **{f"admin_bps_{b // 1000}k": B.fmt(B.bps(fees.get(b), b)) for b in B.BALANCES},
        "fee_bps_at_avg_account": B.fmt(B.bps(fee_avg, avg) if fee_avg is not None else None),
        "realised_capture": realised.get("capture", ""), "realised_internal_bps_ta": realised.get("internal_bps_ta", ""),
        "realised_visible_bps_ta": realised.get("visible_bps_ta", ""), "realised_pool_rate_bps": realised.get("pool_rate_bps", ""),
        "source_url": s.get("source_url", ""), "source_date": s.get("source_date", ""),
        "robots": s.get("robots") or (rec or {}).get("robots") or home_log(cache, s.get("website") or home),
        "quote_check": B.verify(cache, s) if cache and s.get("quotes") else "", "notes": s.get("notes", ""),
    }


FIELDS = ("ein", "name", "sample", "stratum", "size_band_fy2024", "stratum_N", "stratum_n_orig", "stratum_n_ext", "weight_ext",
          "weight_pooled", "daf_assets_fy2024", "accounts_fy2024_screened", "avg_account_fy2024", "website", "fee_status",
          "in_2021plus_distribution", "fee_basis", "admin_tiers", "min_annual_fee_usd", "flat_annual_fee_usd", "opening_min_usd",
          "gift_fee", "grant_fee", "investment", "admin_bps_25k", "admin_bps_100k", "admin_bps_500k", "fee_bps_at_avg_account",
          "realised_capture", "realised_internal_bps_ta", "realised_visible_bps_ta", "realised_pool_rate_bps",
          "source_url", "source_date", "robots", "quote_check", "notes")

NO_SCHEDULE = ("partial", "no_published_fee", "no_website_found")       # site (or its absence) read: no fee schedule public
UNKNOWN_EXT = ("robots_blocked", "bot_challenge", "site_unreachable")


def is_rate(r):
    return r["fee_status"] in B.RATE_2021


def known(r):
    return r["fee_status"] not in UNKNOWN_EXT


# ----------------------------------------------------------------------------- report
def report(ext: Sequence[Mapping], orig_cf: Sequence[Mapping], frame_cf: Sequence[Mapping], realised_all: Sequence[Mapping]) -> str:
    out = []
    T = B.table
    # T1 design
    by = {}
    for r in ext:
        by.setdefault(r["stratum"], []).append(r)
    out.append("## E1 Extension design\n\n" + T(
        ("Stratum", "Frame N", "Original n", "Remaining", "Extension n", "Weight (ext)", "Weight (pooled)"),
        ((k, rs[0]["stratum_N"], rs[0]["stratum_n_orig"], int(rs[0]["stratum_N"]) - int(rs[0]["stratum_n_orig"]), len(rs),
          rs[0]["weight_ext"], rs[0]["weight_pooled"]) for k, rs in sorted(by.items(), key=lambda kv: B.TAIL_BANDS.index(kv[0].split("|")[1])))))
    # E2 status
    sts = ("published_schedule", "published_no_admin_fee", "published_pre2021", "published_unread", "partial",
           "no_published_fee", "no_website_found", "robots_blocked", "bot_challenge", "site_unreachable")
    groups = (("Extension (60)", ext), ("Original CFs (31)", orig_cf), ("Pooled CFs (91)", tuple(ext) + tuple(orig_cf))) + tuple(
        (f"ext band {b}", tuple(r for r in ext if r["size_band_fy2024"] == b)) for b in B.TAIL_BANDS)
    out.append("## E2 Fee status\n\n" + T(("Group", "n") + sts,
                                         ((g, len(rs)) + tuple(sum(r["fee_status"] == s for r in rs) for s in sts) for g, rs in groups)))
    # E3 rates
    def rate_rows():
        for g, rs in groups:
            kn = [r for r in rs if known(r)]
            yield (g, sfmt(sum(map(is_rate, rs)), len(rs), [is_rate(r) for r in rs]),
                   sfmt(sum(map(is_rate, kn)), len(kn), [is_rate(r) for r in kn]),
                   sfmt(sum(r["fee_status"] in B.ANY_TERM for r in rs), len(rs), [r["fee_status"] in B.ANY_TERM for r in rs]),
                   sfmt(sum(r["fee_status"] in NO_SCHEDULE for r in kn), len(kn), [r["fee_status"] in NO_SCHEDULE for r in kn]),
                   sfmt(sum(r["fee_status"] in NO_SCHEDULE + UNKNOWN_EXT for r in rs), len(rs),
                        [r["fee_status"] in NO_SCHEDULE + UNKNOWN_EXT for r in rs]))
    out.append("## E3 Found-schedule rate and no-public-schedule share\n\n" + T(
        ("Group", "2021+ rate found (all)", "2021+ rate found (readable sites)", "Any fee term or linked schedule",
         "No public fee schedule (readable sites)", "No public fee schedule incl. unreadable"), rate_rows()))
    pooled = tuple(ext) + tuple(orig_cf)
    w_ext = sum(float(r["weight_pooled"]) * is_rate(r) for r in pooled) / sum(float(r["weight_pooled"]) for r in pooled)
    out.append(f"Design-weighted 2021+ rate, pooled 91 CFs (weights N/(n_orig+n_ext)): {w_ext*100:.1f}%")
    # E4 medians
    def bpsv(r, b):
        return B.num(r[f"admin_bps_{b // 1000}k"])
    sets = (("Extension only", [r for r in ext if is_rate(r)]), ("Original 6", [r for r in orig_cf if is_rate(r)]),
            ("Pooled", [r for r in pooled if is_rate(r)]),
            ("Pooled, excl. 0% schedules", [r for r in pooled if is_rate(r) and (bpsv(r, 100_000) or 0) > 0]))
    out.append("## E4 Effective annual admin fee, bps: median (95% percentile bootstrap, 10,000 draws, seed 4501)\n\n" + T(
        ("Set", "n", "$25k", "$100k", "$500k", "IQR $100k", "Design-weighted median $25k / $100k / $500k"),
        ((g, len(rs)) + tuple(bfmt(boot_median([bpsv(r, b) for r in rs])) for b in B.BALANCES)
         + (B.qfmt([bpsv(r, 100_000) for r in rs]),
            " / ".join(B.fmt(weighted_median([(bpsv(r, b), float(r.get("weight_pooled") or r.get("weight") or 1)) for r in rs]), 0)
                       for b in B.BALANCES)) for g, rs in sets)))
    # E5 schedules
    out.append("## E5 Extension CFs publishing any fee term\n\n" + T(
        ("EIN", "Sponsor", "Band", "Status", "Tiers", "Min fee $", "Opening min $", "$25k", "$100k", "$500k", "Realised internal bps", "Source date", "Quotes"),
        ((r["ein"], r["name"][:40], r["size_band_fy2024"], r["fee_status"], r["admin_tiers"] or "–", r["min_annual_fee_usd"] or "–",
          r["opening_min_usd"] or "–", r["admin_bps_25k"] or "–", r["admin_bps_100k"] or "–", r["admin_bps_500k"] or "–",
          r["realised_internal_bps_ta"] or "–", r["source_date"], r["quote_check"] or "–")
         for r in ext if r["fee_status"] in B.ANY_TERM)))
    # E6 opening minimums
    om = lambda rs: [B.num(r["opening_min_usd"]) for r in rs if r["opening_min_usd"] != ""]  # noqa: E731
    out.append("## E6 Opening minimum (where stated): median (bootstrap 95%)\n\n" + T(
        ("Set", "n stating", "Median $"), ((g, len(om(rs)), bfmt(boot_median(om(rs)))) for g, rs in
                                            (("Extension", ext), ("Original CFs", orig_cf), ("Pooled", pooled)))))
    # E7 pools
    out.append(pool_section(pooled, frame_cf, realised_all, bpsv))
    return "\n\n".join(out)


def pool_section(pooled, frame_cf, realised_all, bpsv) -> str:
    """Schedule-ceiling CF pool at the pooled median schedule (each CF at its own avg account) vs the realised pool."""
    T = B.table
    rates = [r for r in pooled if is_rate(r)]
    assets = sum(B.num(r["daf_assets_fy2024"]) or 0 for r in frame_cf)
    med100 = median([bpsv(r, 100_000) for r in rates])
    bm = boot_median([bpsv(r, 100_000) for r in rates])
    real = [r for r in realised_all if r.get("part") == "B_tail_cf"]
    real_pool = sum(B.num(r["pool_central_usd"]) or 0 for r in real)
    # realised vs published, for every sampled CF with a 2021+ rate and an observed internal rate
    pairs = [(r["name"][:34], bpsv(r, 100_000), B.num(r.get("realised_internal_bps_ta", ""))) for r in rates]
    obs = [(n, p, q) for n, p, q in pairs if q is not None]
    return ("## E7 Fee pools (tail CFs, FY2024 DAF assets)\n\n" + T(
        ("Measure", "Value"),
        (("Tail CF DAF assets FY2024 (641 CFs)", f"${assets/1e6:,.1f}m"),
         ("Realised all-fund pool, b4427b-0405 (sum of pool_central_usd; unchanged by this sample)", f"${real_pool/1e6:,.1f}m"),
         ("Pooled published median at $100k, bps (bootstrap 95%)", bfmt(bm)),
         ("Flat schedule ceiling at the pooled $100k median", f"${assets*med100/1e4/1e6:,.1f}m" if med100 is not None else "–"),
         ("Flat schedule ceiling, bootstrap bounds", f"${assets*bm[1]/1e4/1e6:,.1f}m–${assets*bm[2]/1e4/1e6:,.1f}m" if bm else "–")))
        + "\n\nPublishers with an observed realised internal rate (b4427b-0405):\n\n"
        + T(("Sponsor", "Published bps at $100k", "Realised internal bps of total assets"),
            ((n, B.fmt(p, 0), B.fmt(q, 1)) for n, p, q in obs)))


# ----------------------------------------------------------------------------- tasks
def robots_log(cache: str) -> tuple[tuple[str, str, str], ...]:
    recs = []
    for p in sorted(glob.glob(os.path.join(cache, "*.json"))):
        if p.endswith("crawl_summary_ext.json"):
            continue
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
        if isinstance(d, dict) and "robots" in d and "url" in d:
            recs.append((host_of(d["url"]), d["robots"], d["url"]))
    first = {}
    for h, v, u in recs:
        first.setdefault(h, (h, v, u))
    return tuple(sorted(first.values()))


def all_urls() -> tuple[str, ...]:
    return tuple(dict.fromkeys(u for s in FEES_EXT.values() for u in (s.get("verify_urls") or (s.get("source_url"),)) if u))


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--task", choices=("sample", "crawl", "fetch", "hits", "robots", "census"), required=True)
    ap.add_argument("--cache-dir")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--ein", action="append", default=[])
    ap.add_argument("--url", action="append", default=[])
    a = ap.parse_args(argv)
    os.chdir(a.root)
    frame = B.tail_frame(B.read_csv(B.LT_CSV))
    orig = original_sample(frame)
    orig_cf_eins = frozenset(r["ein"] for r in orig if r["type4"] == "cf")
    ext = draw_ext(frame, orig_cf_eins)
    hp = homepages(B.read_csv(VMAP_CSV))
    if a.task == "sample":
        print("stratum|N|N_remaining|n_ext|ein|name|daf_assets_fy2024|homepage")
        print("\n".join(f"{r['stratum']}|{r['stratum_N']}|{r['stratum_N_remaining']}|{r['stratum_n']}|{r['ein']}|{r['name']}|"
                        f"{r['daf_assets_fy2024']}|{hp.get(r['ein'], '')}" for r in ext))
        return 0
    if a.task in ("crawl", "fetch") and not (a.fetch and a.cache_dir):
        print(f"{a.task} needs --fetch and --cache-dir", file=sys.stderr)
        return 2
    if a.task == "crawl":
        os.makedirs(a.cache_dir, exist_ok=True)
        targets = [(r["ein"], hp[r["ein"]]) for r in ext if r["ein"] in hp and (not a.ein or r["ein"] in a.ein)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            res = list(ex.map(lambda t: B.crawl_site(a.cache_dir, *t), targets))
        with open(os.path.join(a.cache_dir, "crawl_summary_ext.json"), "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("\n".join(f"{r['ein']}\t{r['home_status']}\t{r['robots']}\t{r['n_candidates']}\t{len(r['hits'])}\t{r['home']}" for r in res))
        return 0
    if a.task == "fetch":
        os.makedirs(a.cache_dir, exist_ok=True)
        recs = [B.fetch_one(a.cache_dir, u) for u in (a.url or all_urls())]
        print("\n".join(f"{r['status']}\t{r['robots']}\t{len(r['text'])}\t{r['url']}" for r in recs))
        return 0
    if a.task == "robots":
        print("host\tverdict\tfirst_url")
        print("\n".join("\t".join(t) for t in robots_log(a.cache_dir)))
        return 0
    if a.task == "hits":
        with open(os.path.join(a.cache_dir, "crawl_summary_ext.json"), encoding="utf-8") as fh:
            res = json.load(fh)
        for c in res:
            if a.ein and c["ein"] not in a.ein:
                continue
            print(f"=== {c['ein']} {c['home']} | {c['robots']} | HTTP {c['home_status']} | fetched {len(c['fetched'])}")
            print("  pages: " + " ".join(c["fetched"]))
            for u, sn in c["hits"]:
                print(f"  - [{u}] {sn}")
        return 0
    realised = {r["ein"]: r for r in B.read_csv(REALISED_CSV)}
    rows = tuple(ext_row(r, hp.get(r["ein"], ""), realised.get(r["ein"], {}), a.cache_dir) for r in ext)
    B.write_csv(OUT_CSV, rows, FIELDS)
    orig_rows = tuple(r for r in B.read_csv(B.OUT_CSV) if r["type4"] == "cf")
    orig_cf = tuple({**r, "realised_internal_bps_ta": realised.get(r["ein"], {}).get("internal_bps_ta", "")} for r in orig_rows)
    frame_cf = tuple(r for r in frame if r["type4"] == "cf")
    print(report(rows, orig_cf, frame_cf, tuple(realised.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
