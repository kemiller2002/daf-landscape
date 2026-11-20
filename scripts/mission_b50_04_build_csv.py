#!/usr/bin/env python3
"""b50-04: build data/mission-2026-11-14/giving-circles-2026-11-20.csv (stdlib, functional).

Usage: python3 -I scripts/mission_b50_04_build_csv.py . CACHE_DIR [OUT_CSV]
  CACHE_DIR = output dir of mission_b50_04_giving_circles.py (sample.csv, candidates.csv,
              robots-log.csv, text/*.txt; pdfraw/*.txt = `pdftotext` (non-layout) of raw/*.pdf).
Every quote below is checked verbatim (whitespace-normalised; ' ... ' separates fragments)
against the cached text of its source_url; the result goes into quote_check.
Summary counts printed at the end are computed from the rows, not typed.
"""
import csv
import hashlib
import os
import re
import sys
from functools import reduce

OUT_DEFAULT = "data/mission-2026-11-14/giving-circles-2026-11-20.csv"
REPO_990 = "data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv"

FIELDS = ["row_id", "record_type", "entity", "ein", "entity_type", "sample_basis", "cf_rank_fy2024",
          "fy2024_daf_assets_usd", "offering_class", "product_or_program", "vehicle_stated",
          "minimum_quote", "fee_quote", "who_advises_quote", "grant_process_quote", "member_contribution_quote",
          "other_quote", "metric", "value", "unit", "period", "source_url", "source_date", "robots", "fetch_status",
          "quote_check", "retrieved", "notes"]

# offering_class codes (see research doc data dictionary)
#  explicit_gc_fund_product   - sponsor publishes a giving-circle / group fund product with terms
#  hosted_named_circles       - sponsor hosts / administers named circles; generic terms only
#  committee_advised_pooled   - pooled fund advised by a community committee (affinity / giving group)
#  daf_cofunding_program      - sponsor invites existing DAF holders to co-fund slates (not a circle)
#  supports_independent_circle- circle is its own nonprofit; sponsor promotes / partners
#  campaign_feature           - DAF platform feature letting a member rally others; no pooled group fund
#  platform_fiscal_host       - technology platform whose affiliated 501(c)(3) pools and grants
#  guidance_only              - sponsor publishes guidance, no product
#  none_found                 - nothing found by sitemap scan + site-restricted search
#  blocked                    - robots.txt disallowed / unreachable, or server refused the page
#  historical                 - circle converted or product launched pre-2021 / status changed

P = dict  # row literal helper

PROVIDERS = (
    # ---------------- systematic sample (1-in-3 of top-100 CFs by FY2024 DAF assets) ----------------
    P(rank="1", offering_class="none_found",
      source_url="https://www.siliconvalleycf.org/donor-circle-safety-net",
      notes="10 sitemaps scanned, no circle/collective URLs. A search-indexed legacy 'Donor Circle' URL now serves the generic homepage (no circle text), so no current product could be verified."),
    P(rank="4", offering_class="none_found", notes="9 sitemaps scanned; site-restricted search found no giving-circle page."),
    P(rank="7", offering_class="none_found", notes="2 sitemaps scanned; site-restricted search found only a pre-2021 orientation PDF."),
    P(rank="10", offering_class="blocked", notes="robots.txt unreachable (connection error) => treated as disallowed; nothing fetched."),
    P(rank="13", offering_class="hosted_named_circles", product_or_program="Impact100 Essex (news release on CFNJ site)",
      source_url="https://cfnj.org/news/impact100-essex-awards-100000-grant-to-perinatal-health-equity-initiative/",
      source_date="2025-05-08",
      member_contribution_quote="Impact100 Essex grants are funded by gifts of $1,150 per member, per year.",
      grant_process_quote="was chosen from among four finalists by Impact100 Essex members.",
      notes="Release is published on cfnj.org but does not state whether CFNJ holds the circle's money (fund vs. fiscal sponsor vs. own entity). cfnj.org/impact100essex/ returned 404."),
    P(rank="16", offering_class="hosted_named_circles", product_or_program="GiVE 365",
      source_url="https://cfgm.org/get-involved/give-365/", source_date="live page (2026 theme)",
      member_contribution_quote="Join a giving community that pools $365 per member each year to fund local nonprofits",
      grant_process_quote="Members pool their contributions, select an annual theme, and decide together which nonprofit projects to fund",
      who_advises_quote="Guidance from volunteer leaders, backed by Community Foundation staff, supports GiVE 365",
      notes="Foundation-run circle; no fee or minimum published on the page."),
    P(rank="19", offering_class="hosted_named_circles", product_or_program="Giving circles / collective giving (incl. RMD Giving Circle, pop-up circles)",
      source_url="https://www.minneapolisfoundation.org/giving-circles/", source_date="live page",
      who_advises_quote="The Minneapolis Foundation can provide grantmaking advice, carries out the group’s funding decisions, and ensures that all grant recipients are qualified public charities.",
      grant_process_quote="You and the members of your giving circle will decide together how to invest your pooled resources.",
      member_contribution_quote="Each giving circle decides together how it will raise money for the causes it supports.",
      other_quote="Our support varies based on the needs of each group and can include: Guidance and support with group visioning and program creation; meeting facilitation; marketing tools and guidance; and grant administration and due diligence.",
      notes="Companion page /collective-giving/ lists circles, advisory-committee funds and corporate giving groups. A separate RMD Giving Circle pools IRA gifts (see row for /stories/.../collective-giving-powered-by-iras/ in source register); a fund taking QCDs cannot be a DAF (IRC 408(d)(8)(B)), so at least that circle is held outside DAF form (inference)."),
    P(rank="22", offering_class="hosted_named_circles", product_or_program="The Power of Possible Giving Circle",
      source_url="https://spmcf.org/donors/ways-to-give/pop-giving-circle", source_date="live page (launch event in November)",
      grant_process_quote="A giving circle is a collaborative giving model that brings people together to discuss and decide where to make a pooled gift.",
      who_advises_quote="Members help shape the circle's values, learning experiences and grantmaking, with community voices guiding the way.",
      notes="No minimum, dues or fee quoted on the page (a 'Fund and Fee Information' link is site navigation)."),
    P(rank="25", offering_class="blocked", product_or_program="Giving Circles (Center for Philanthropy)",
      source_url="https://pittsburghfoundation.org/giving-circles",
      notes="robots.txt allows all agents but the server returned HTTP 403 to the page; terms not read. Search snippets describe a Foundation-matched circle programme; not used as evidence."),
    P(rank="28", offering_class="none_found", notes="6 sitemaps scanned; only match is an unrelated named fund ('circle-of-friends-ministry')."),
    P(rank="31", offering_class="committee_advised_pooled", product_or_program="Affinity funds (Black Philanthropy Fund, Latino Impacto Fund, LGBTQ+ Opportunity Fund)",
      source_url="https://www.clevelandfoundation.org/philanthropy-giving/ways-to-give/affinity-funds/overview", source_date="live page (funds launched 2024-2025)",
      minimum_quote="Anyone can make a gift to any affinity fund at any time. There is no giving minimum and donations are pooled.",
      who_advises_quote="Cleveland Foundation affinity fund committees are comprised of at least five members of that community and its allies.",
      grant_process_quote="leveraging contributions through collective giving and committee-advised grantmaking.",
      other_quote="The LGBTQ+ Opportunity Fund is a Cleveland Foundation affinity fund launched in August 2024 with a $3 million endowment",
      notes="Not branded 'giving circle'; collective-giving funds seeded with Foundation endowments. Sitemap scan found no circle URL; page found by site-restricted search."),
    P(rank="34", offering_class="supports_independent_circle", product_or_program="Impact 100 Louisville (separate nonprofit)",
      source_url="https://www.cflouisville.org/impact-100/", source_date="undated (refers to 2021 grant cycle)",
      member_contribution_quote="100+ women donate $1,000 to create a $100,000+ grant that will benefit at least one local nonprofit.",
      other_quote="Impact 100 Louisville, a new Louisville-based nonprofit, is bringing women together to transform lives through collective giving.",
      notes="Circle is its own nonprofit; CF page promotes it. Sitemap match was an unrelated 'winners-circle' story; page found by site-restricted search."),
    P(rank="37", offering_class="hosted_named_circles", product_or_program="WORTH: The Next Generation of Philanthropists (WORTH Endowment Fund)",
      source_url="https://northtexascf.org/collective-giving/", source_date="undated (narrative refers to 2015 and 2018)",
      member_contribution_quote="Each membership of $250 is placed in the WORTH Endowment Fund at the North Texas Community Foundation.",
      other_quote="Membership dollars are matched by our four private investors",
      notes="Page is a first-person member narrative (member not recorded). Evidence date may be pre-2021; terms shown as on the live page."),
    P(rank="40", offering_class="hosted_named_circles", product_or_program="Collective Giving: Impact Funds, giving circles, quarterly urgent-needs",
      source_url="https://cfrichmond.org/give/services/collective-giving/", source_date="live page (cites 'Since 2021')",
      grant_process_quote="Members combine their gifts, learn together, and decide as a group where grants go.",
      minimum_quote="You do not need a fund of your own to give to an Impact Fund or join a giving circle.",
      other_quote="Since 2021, fundholders have given more than $1.8 million to meet nearly 200 requests.",
      notes="The $1.8m figure is the quarterly urgent-needs programme for fundholders (DAF co-funding), not giving circles."),
    P(rank="46", offering_class="hosted_named_circles", product_or_program="Emerging Philanthropists of New Orleans (EPNO), listed under 'collective giving' tag",
      source_url="https://www.gnof.org/tag/collective-giving/", source_date="live tag page",
      notes="Tag archive lists EPNO only; programme terms not retrieved. Other sitemap matches were 'Lee Circle' place-name pages."),
    P(rank="49", offering_class="daf_cofunding_program", product_or_program="Giving Together (proposals shared with DAF holders)",
      source_url="https://www.mainecf.org/2022/07/giving-together-for-good/", source_date="2022-07",
      grant_process_quote="MaineCF's Giving Together program provides donors with DAFs access to proposals so they can support nonprofit organizations and projects that reflect their passions.",
      other_quote="Last year, donors provided local programs nearly $1.7 million through Giving Together.",
      notes="Not a pooled circle: individual DAFs co-fund vetted proposals. Page names individual donors; not recorded."),
    P(rank="52", offering_class="none_found", notes="8 sitemaps scanned; no match; site-restricted search found nothing."),
    P(rank="55", offering_class="hosted_named_circles", product_or_program="21st Century Fund",
      source_url="https://www.cfgb.org/community-change/initiatives/21st-century-fund/",
      notes="Page fetched (HTTP 200) but its static HTML carries no programme text; robots.txt returned an HTML page (treated as no rules). Search snippets describe a member-voted $100,000 award; not used as evidence. Terms not recorded."),
    P(rank="58", offering_class="none_found", notes="5 sitemaps scanned; no match; site-restricted search found nothing."),
    P(rank="61", offering_class="none_found", notes="8 sitemaps; only match is a grantee story whose name contains 'circle'."),
    P(rank="64", offering_class="blocked", notes="robots.txt HTTP 403 => treated as disallowed; nothing fetched."),
    P(rank="67", offering_class="historical", product_or_program="Future Fund of Central New York (former giving circle, now field-of-interest fund)",
      source_url="https://cnycf.org/funds/future-fund-of-central-new-york/", source_date="live page",
      other_quote="After a decade of collaborative giving and grantmaking, facing lapsing membership, the Future Fund transitioned to a field-of-interest fund",
      vehicle="field-of-interest fund (after conversion)",
      notes="Shows a CF-hosted circle converting to a standard fund type when membership lapses."),
    P(rank="70", offering_class="hosted_named_circles", product_or_program="Lowcountry African American Giving Circle (LAAGC)",
      source_url="https://coastalcommunityfoundation.org/special-initiatives/lowcountry-african-american-giving-circle/", source_date="live page",
      member_contribution_quote="Membership options include a $500 annual Community Membership and a $250 Young Professional Membership",
      minimum_quote="A Founding Donor makes a commitment of $5,000 or more to help build the permanent LAAGC Endowment Fund",
      who_advises_quote="Members help shape how resources are invested in the community.",
      vehicle="endowment fund (LAAGC Endowment Fund) plus annual membership pool",
      notes="Staff contact named on page; not recorded."),
    P(rank="73", offering_class="none_found", notes="1 sitemap scanned; no match."),
    P(rank="76", offering_class="daf_cofunding_program", product_or_program="Giving Together (DAF holders co-fund grant slates)",
      source_url="https://vermontcf.org/your-impact/giving-together/", source_date="live page",
      grant_process_quote="Fundholders can recommend a grant to the slate of projects through the VCF portal.",
      other_quote="Giving Together is an opportunity for our donor advised fundholders to join others in supporting collaborative, community-based projects throughout the state.",
      notes="Collective giving through individual DAFs; no pooled group fund."),
    P(rank="79", offering_class="none_found", notes="No robots.txt (404); 8 sitemaps scanned; no match."),
    P(rank="82", offering_class="blocked", notes="robots.txt HTTP 403 => treated as disallowed; nothing fetched."),
    P(rank="85", offering_class="none_found", notes="3 sitemaps scanned; no match."),
    P(rank="88", offering_class="hosted_named_circles", product_or_program="LGBTQ+ Giving Circle Fund",
      source_url="https://www.lancfound.org/lgbtq-giving-circle/", source_date="live page",
      other_quote="Since our creation, the LGBTQ+ Giving Circle has directed over $370,000 across 30 grants",
      who_advises_quote="The LGBTQ+ Giving Circle is a community-driven fund",
      notes="Page appeals for gifts to build the circle's endowment; no minimum or fee quoted."),
    P(rank="91", offering_class="explicit_gc_fund_product", product_or_program="Collective Giving Partners (Collective Giving Handbook 2026)",
      source_url="https://www.idahocf.org/docs/Collective-Giving-Handbook-2026.pdf", source_date="2026 (handbook title)",
      minimum_quote="Non-endowed Purpose: distributing funds into the community immediately. Not intended to last in perpetuity. Minimum to establish fund: $25,000",
      fee_quote="Typically, 2.0% of average daily fund balance with a minimum fee of $500, whichever is greater, plus investment fee of approximately .2%. ... Some funds have fees on contributions (gift fees) between 1%-10% depending on the needs of the fund.",
      who_advises_quote="This relationship allows the Partner to be advisory in nature and ICF to hold the legal status.",
      grant_process_quote="Partner will make all recommendations for grant distribution in accordance with their fund agreement and ICF Grant Making Policy.",
      other_quote="This partnership allows participating community members to avoid the need to establish their own 501(c) (3) nonprofit organization.",
      vehicle="component fund (endowed or non-endowed) with the circle as advisory committee",
      notes="Endowed option: 'Typically, 1.0%-2.0% on the average daily fund balance with minimum fee of $500'. Fees are negotiated: 'The ICF and the Collective Giving Partner will determine a mutually agreed upon fee schedule'."),
    P(rank="94", offering_class="none_found",
      notes="1 sitemap scanned; search-indexed article on a '100s of Women Who Care' circle returned 404 (with and without trailing slash); not verifiable."),
    P(rank="43", offering_class="hosted_named_circles", product_or_program="African American Legacy Fund Giving Circle",
      source_url="https://www.cicf.org/african-american-legacy-fund-of-indianapolis/", source_date="live page",
      vehicle="endowed donor-advised fund (stated)",
      other_quote="The African American Legacy Fund is an endowed donor-advised fund of The Indianapolis Foundation, an affiliate of Central Indiana Community Foundation.",
      who_advises_quote="It then empowers a committee of donors to design a grant-making process and make charitable distributions from the fund",
      grant_process_quote="Members will collaborate to invest pooled resources annually to achieve greater collective impact.",
      notes="Only sampled CF page that names the DAF form for a circle-linked fund. Sitemap 'heritage-circle' matches are unrelated."),
    P(rank="100", offering_class="hosted_named_circles", product_or_program="Giving groups (Loveland Generations, NoCo CARES)",
      source_url="https://nocofoundation.org/donors/collaborative-giving", source_date="live page (cites June 30, 2024)",
      member_contribution_quote="The group has three levels of membership: Diamond ($1,000); Gold ($750); and Silver ($500).",
      grant_process_quote="This giving group solicits grant proposals once a year and gives preference to those who serve Loveland youth.",
      other_quote="A giving group is composed of community-minded people who pool their charitable dollars in a common fund.",
      notes="Sitemap scan found no 'circle' URL (product is called 'giving group'); page found by site-restricted search."),
)

SUPPLEMENT = (
    P(entity="TRIANGLE COMMUNITY FOUNDATION INC", ein="", rank="59", entity_type="community_foundation",
      sample_basis="purposive_supplement (repo CF list; found by web search for 'giving circle fund')",
      offering_class="explicit_gc_fund_product", product_or_program="Giving Circle Fund",
      source_url="https://trianglecf.org/wp-content/uploads/2026/01/Giving-Circles-one-pager-1.pdf", source_date="2026-01 (upload path)",
      minimum_quote="make an irrevocable contribution of $10,000 to open a non-endowed fund. ... Giving Circles with a balance of less than $10,000 are considered on a case-by-case basis in consultation with Foundation staff.",
      fee_quote="Annual administrative fee of 1% of fund balance or a minimum of $300 per year",
      who_advises_quote="Fund advisors recommend grants and they are processed through the Foundation",
      member_contribution_quote="Contribution amounts can vary, from $10 to $25,000 or more – Giving Circle organizers decide",
      other_quote="Access to fund via Donor Portal, and donations can be made online (minimum online contribution of $100)",
      vehicle="non-endowed fund",
      notes="Clearest CF giving-circle fund term sheet found. The HTML set-up page indexed by search now 404s."),
    P(entity="Sacramento Region Community Foundation", ein="", rank="81", entity_type="community_foundation",
      sample_basis="purposive_supplement (search snippet lists 'Giving Circle' among fee-schedule fund types)",
      offering_class="blocked", source_url="https://www.sacregcf.org/fees",
      notes="robots.txt HTTP 403 => treated as disallowed; fee schedule not read."),
)

NATIONAL = (
    P(entity="Thrivent Charitable Impact & Investing (Thrivent Charitable)", ein="", entity_type="national_sponsor",
      offering_class="explicit_gc_fund_product", product_or_program="Giving circle fund",
      source_url="https://thriventcharitable.thrivent.com/steps-giving/givingcircles", source_date="live page",
      vehicle="donor-advised fund (stated)",
      minimum_quote="A giving circle can be established with as little as $200/person using gifts of cash or publicly traded securities or other assets. (giving circle fund minimum applies.)",
      who_advises_quote="We will establish your fund based on the type of giving circle selected and send it to the chair/fund advisor for signing.",
      grant_process_quote="As a group, members make decisions on what organizations to grant to and witness the change their charitable gifts make.",
      other_quote="Donors make gifts to an IRS-qualified public charity, in this case Thrivent Charitable Impact & Investing (in the form of a donor-advised fund), and receive potential charitable tax deductions.",
      notes="The fund-level minimum is referred to but not stated; fee not stated on the page. Overview page: 'Your giving circle is in the form of a donor-advised fund'."),
    P(entity="Fidelity Charitable", ein="", entity_type="national_sponsor", offering_class="guidance_only",
      product_or_program="Article 'The power of giving circles' + webinar",
      source_url="https://www.fidelitycharitable.org/articles/the-power-of-giving-circles.html", source_date="live page (reprint, cites 2024 report)",
      other_quote="Philanthropy Together is a grantee of the Fidelity Charitable Catalyst Fund.",
      grant_process_quote="learn more about the power of giving circles and how to leverage your Fidelity Charitable Giving Account for deeper impact in your community",
      notes="No group/circle account product; points donors to Philanthropy Together and the Grapevine directory. Article names circle leaders; not recorded."),
    P(entity="Daffy Charitable Fund", ein="86-3177440", entity_type="national_sponsor", offering_class="campaign_feature",
      product_or_program="Daffy Campaigns ('Giving circle' campaign option)",
      source_url="https://www.daffy.org/resources/daffy-campaigns-updates", source_date="2025-08-28",
      other_quote="Giving circle: Invite family, friends, or coworkers to rally around a shared list of nonprofits.",
      grant_process_quote="Campaigns can include up to 15 charities in a single fundraiser. Organizers can allow donors to choose which charity to support, or split donations evenly across all selected organizations.",
      notes="grant_process_quote is from help.daffy.org/en/articles/8538853-what-is-a-daffy-campaign. Gifts flow to the named charities; no jointly advised pooled fund found. No separate 'Daffy groups' product found."),
    P(entity="Groundswell (Groundswell Charitable Foundation)", ein="", entity_type="national_sponsor", offering_class="campaign_feature",
      product_or_program="Employer campaigns and employee fundraisers (no circle product found)",
      source_url="https://www.groundswell.io/products/giving", source_date="live page",
      other_quote="Rally your workforce around specific causes or disaster relief efforts with time-bound giving campaigns.",
      notes="Searched site and FAQ; no giving-circle or group-fund product. Campaigns are employer-run."),
    P(entity="Grapevine / Grapevine Giving Foundation", ein="87-2389502", entity_type="platform", offering_class="platform_fiscal_host",
      product_or_program="Giving circles on Grapevine",
      source_url="https://help.grapevine.org/fees-for-using-grapevine", source_date="live help page",
      fee_quote="Grapevine does not charge platform fees for online donations made on Grapevine (via Credit/Debit Card or Bank Transfer). ... for off-platform donations such as checks, Donor Advised Fund grants, wire transfers, and ACH payments, Grapevine charges a 3% platform fee",
      other_quote="Credit and Debit cards via Stripe: 2.2% + $0.30 (3.5% for AmEx; +1.5% for non-US cards).",
      vehicle="pooled at Grapevine Giving Foundation (501(c)(3)); 990 Schedule D reports 1 DAF",
      notes="A second help page (is-grapevine-free) says 'We don't charge your circle or your nonprofit partners any platform fees or administrative fees' and lists international cards at 3.2% + 30c, so the two pages differ on non-US card pricing and on whether any platform fee applies. Before Nov 2022 a third-party fiscal sponsor held funds (blog 2022-11-09)."),
    P(entity="Global Impact (Growfund)", ein="52-1273585", entity_type="national_sponsor", offering_class="historical",
      product_or_program="Growfund for Giving Circles (launched pre-2021)",
      source_url="data/mission-2026-11-14/tier-b-daf-exit-reasons.csv",
      notes="Repo 990 reads: Global Impact answered DAF line 6 'Yes' FY2023-24 and 'No' in FY2025; 'Growfund still described in FY2024 Part III, not in FY2025'. Launch coverage is pre-2021, so no current terms recorded."),
)


def norm(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def sha(url):
    return hashlib.sha1(url.encode()).hexdigest()[:16]


def read_text(cache, url):
    paths = (os.path.join(cache, "text", sha(url) + ".txt"), os.path.join(cache, "pdfraw", sha(url) + ".txt"))
    texts = tuple(open(p, encoding="utf-8", errors="replace").read() for p in paths if os.path.exists(p))
    return norm(" ".join(texts))


QUOTE_FIELDS = ("minimum_quote", "fee_quote", "who_advises_quote", "grant_process_quote",
                "member_contribution_quote", "other_quote")
ALT_SOURCES = {"https://www.daffy.org/resources/daffy-campaigns-updates":
               ("https://help.daffy.org/en/articles/8538853-what-is-a-daffy-campaign",)}


def check_quotes(cache, row):
    url = row.get("source_url", "")
    if not url.startswith("http"):
        return "n/a (repo file)" if url else "no page (sitemap scan / search only)"
    text = " ".join((read_text(cache, url),) + tuple(read_text(cache, u) for u in ALT_SOURCES.get(url, ())))
    frags = tuple(norm(f) for k in QUOTE_FIELDS for f in row.get(k, "").split(" ... ") if f.strip())
    if not frags:
        return "no quotes"
    ok = tuple(f for f in frags if f in text)
    return f"verified {len(ok)}/{len(frags)}" + ("" if len(ok) == len(frags) else " MISSING: " + " | ".join(f[:60] for f in frags if f not in text))


def robots_lookup(log_rows, url):
    hits = [r for r in log_rows if r["url"] == url]
    return (hits[-1]["robots"], hits[-1]["status"]) if hits else ("", "")


def provider_row(cache, log_rows, sample_by_rank, cands_by_rank, i, spec):
    s = sample_by_rank.get(spec.get("rank", ""), {})
    c = cands_by_rank.get(spec.get("rank", ""), {})
    url = spec.get("source_url", "")
    rb, st = robots_lookup(log_rows, url)
    base = {k: "" for k in FIELDS}
    row = {**base, **{k: v for k, v in spec.items() if k in FIELDS},
           "row_id": f"GC-{i:03d}", "record_type": "provider",
           "entity": spec.get("entity") or s.get("name", ""),
           "ein": spec.get("ein") or s.get("ein", ""),
           "entity_type": spec.get("entity_type", "community_foundation"),
           "sample_basis": spec.get("sample_basis", "systematic_1in3_top100_cf (cf-vendor-map-by-ein-v2.csv)" if s else ""),
           "cf_rank_fy2024": spec.get("rank", ""),
           "fy2024_daf_assets_usd": s.get("fy2024_daf_assets_usd", ""),
           "vehicle_stated": spec.get("vehicle", "not stated"),
           "robots": rb or (c.get("robots", "") + (f"; sitemaps_read={c.get('sitemaps_read')}" if c else "")),
           "fetch_status": st or ("sitemap scan only" if c else ""),
           "retrieved": "2026-11-20"}
    return {**row, "quote_check": check_quotes(cache, row)}


def sizing_rows(cache, root):
    def r(i, metric, value, unit, period, url, quote, notes=""):
        row = {**{k: "" for k in FIELDS}, "row_id": f"GS-{i:03d}", "record_type": "sizing_metric",
               "metric": metric, "value": value, "unit": unit, "period": period, "source_url": url,
               "other_quote": quote, "retrieved": "2026-11-20", "notes": notes}
        return {**row, "quote_check": check_quotes(cache, row)}

    IA = "https://johnsoncenter.org/wp-content/uploads/2024/04/in-abundance-an-analysis-of-the-thriving-landscape-of-collective-giving-in-the-u-s.pdf"
    RC = "https://johnsoncenter.org/wp-content/uploads/2026/02/rooted-in-community-the-infrastructure-powering-collective-giving.pdf"
    GV = "https://www.grapevine.org/about"
    base = (
        r(1, "US collective giving groups (cumulative population estimate)", "4000", "groups (\"nearly\")", "2017-2023", IA,
          "Between 2017 and 2023, nearly 4,000 collective giving groups mobilized approximately 370,000 philanthropists to donate more than $3.1 billion"),
        r(2, "Participants", "370000", "people (\"approximately\")", "2017-2023", IA, "nearly 4,000 collective giving groups mobilized approximately 370,000 philanthropists"),
        r(3, "Dollars donated by collective giving groups", "3100000000", "USD (\"more than\")", "2017-2023", IA, "to donate more than $3.1 billion"),
        r(4, "Prior landscape (2017 study, quoted in 2024 report)", "1600", "groups", "to 2016", IA,
          "found that more than 150,000 philanthropists within 1,600 groups had distributed approximately $1.29 billion",
          "Pre-2021 baseline quoted inside a 2024 report; context only."),
        r(5, "Group survey responses", "543", "groups", "survey fielded early 2023", IA, "a total of 543 responses to the group survey and 1,406 for the member survey"),
        r(6, "Host or fiscal agent: community foundation", "42", "% of groups", "2023 survey", RC, "Forty-two percent of giving circles are hosted by community foundations"),
        r(7, "Host or fiscal agent: technology platform (e.g. Grapevine)", "24", "% of groups", "2023 survey", RC, "followed by technology platforms such as Grapevine (24%)"),
        r(8, "Host or fiscal agent: nonprofit organisation", "7", "% of groups", "2023 survey", RC, "nonprofit organizations (7%)"),
        r(9, "Host or fiscal agent: women's fund", "3", "% of groups", "2023 survey", RC, "or women’s funds (3%)"),
        r(10, "No fiscal sponsor (self-managed, incl. own 501(c)(3) or informal)", "24", "% of groups", "2023 survey", RC,
          "While 24% of groups operate independently without a fiscal sponsor"),
        r(11, "Hosted by CF or women's fund (money managed by host)", "45", "% of groups", "2023 survey", IA,
          "45% of collective giving groups were hosted by either a community foundation or women’s fund, which managed donations and disbursements",
          "Consistent with GS-006 + GS-009 (42 + 3)."),
        r(12, "Groups with paid staff support", "47", "% of groups", "2023 survey", IA, "47% of groups had paid-staff support"),
        r(13, "Grapevine: total donations since 2020", "60000000", "USD (\"over\")", "2020-2026", GV,
          "Since 2020, the Grapevine platform has granted over $60,000,000 to organizations across the country."),
        r(14, "Grapevine: members", "100000", "members (\"100,000+\")", "as of 2026-11", GV, "100,000+ Members join one of thousands of Giving Circles across the country"),
        r(15, "Grapevine: circles (per Grapevine Giving Foundation page)", "1100", "giving circles", "undated page", "https://www.grapevine.org/about-us/grapevine-giving-foundation",
          "we've enabled over 84,000 members across 1,100 Giving Circles", "Homepage counter reads '1K+ Total Grapevines'. Different pages, different dates."),
    )
    return base + gv_990_rows(root, len(base))


def gv_990_rows(root, offset):
    """Grapevine Giving Foundation Schedule D Part I (DAF) values from the repo's 990 harvests."""
    def load(p):
        return [r for r in csv.DictReader(open(os.path.join(root, p))) if r["ein"] == "872389502"]
    rows = load(REPO_990)
    by_fy = {r["fiscal_year"]: r for r in rows}
    fys = sorted(by_fy)
    metrics = (("sched_d_daf_count", "DAF count (Sched D line 1a)", "funds"),
               ("sched_d_daf_contributions", "Contributions to DAFs", "USD"),
               ("sched_d_daf_grants", "Grants from DAFs", "USD"),
               ("sched_d_daf_eoy_value", "DAF value end of year", "USD"))
    out = [{**{k: "" for k in FIELDS}, "record_type": "sizing_metric",
            "metric": f"Grapevine Giving Foundation 990: {label}", "value": by_fy[fy][col], "unit": unit,
            "period": f"FY{fy}", "source_url": by_fy[fy]["source_url"], "quote_check": f"computed from {REPO_990}",
            "retrieved": "repo harvest", "notes": "Schedule D Part I; blank = not reported in the harvest row"}
           for fy in fys for col, label, unit in metrics]
    return tuple({**r, "row_id": f"GS-{offset + i + 1:03d}"} for i, r in enumerate(out))


def summarise(rows):
    prov = [r for r in rows if r["record_type"] == "provider"]
    sample = [r for r in prov if r["sample_basis"].startswith("systematic")]
    count = lambda rs, key: reduce(lambda acc, r: {**acc, r[key]: acc.get(r[key], 0) + 1}, rs, {})
    return dict(sample_n=len(sample), sample_by_class=count(sample, "offering_class"),
                all_by_class=count(prov, "offering_class"),
                quote_failures=[r["row_id"] for r in rows if "MISSING" in r["quote_check"]])


def derived(rows):
    get = lambda rid: float(next(r["value"] for r in rows if r["row_id"] == rid))
    groups, dollars = get("GS-001"), get("GS-003")
    shares = {k: get(k) / 100 for k in ("GS-006", "GS-007", "GS-008", "GS-009", "GS-010")}
    return dict(
        illustrative_groups_by_host={k: round(groups * v) for k, v in shares.items()},
        share_check_sum_pct=round(sum(shares.values()) * 100, 1),
        avg_dollars_per_group_2017_2023=round(dollars / groups),
        avg_annual_flow_7yr=round(dollars / 7),
        grapevine_fy2023_daf_contrib_share_of_avg_annual_flow_pct=round(100 * get("GS-021") / (dollars / 7), 2),
    )


def main(argv):
    root, cache = argv[1], argv[2]
    out = os.path.join(root, argv[3] if len(argv) > 3 else OUT_DEFAULT)
    sample = list(csv.DictReader(open(os.path.join(cache, "sample.csv"))))
    cands = list(csv.DictReader(open(os.path.join(cache, "candidates.csv"))))
    log_rows = list(csv.DictReader(open(os.path.join(cache, "robots-log.csv"))))
    s_by = {r["rank"]: r for r in sample}
    c_by = {r["rank"]: r for r in cands}
    specs = PROVIDERS + SUPPLEMENT + NATIONAL
    missing = sorted(set(s_by) - {p["rank"] for p in PROVIDERS})
    assert not missing, f"sample ranks without a row: {missing}"
    prov = tuple(provider_row(cache, log_rows, s_by, c_by, i + 1, sp) for i, sp in enumerate(specs))
    rows = prov + sizing_rows(cache, root)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {out}")
    print(summarise(rows))
    print(derived(rows))


if __name__ == "__main__":
    main(sys.argv)
