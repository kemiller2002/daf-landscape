#!/usr/bin/env python3
"""Bright Funds Foundation classification and SVCF grant-dollar reconciliation (P-B39N603-02, P-G1913-02-03).

Stage `fetch` (I/O): robots.txt first for every host, then the Form 990 e-file XML returns below from the
GivingTuesday mirror of IRS TEOS (robots.txt 404 = no rules). UA "research-script/1.0"; 1.5 s between requests.
Stage `report` (pure transforms, I/O only at the edges): parses the cached XML, reads repo CSVs, writes the CSV
and prints a JSON summary. Audited-statement and press-release figures are quoted constants with their URLs
(they come from PDF/HTML read by hand; see the research note), never computed here.

Usage
  python3 scripts/mission_bright_funds_svcf.py fetch  . --cache DIR
  python3 scripts/mission_bright_funds_svcf.py report . --cache DIR [--out data/mission-2026-11-14/bright-funds-svcf-2026-11-20.csv]

Stdlib only; functional style.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from typing import Iterable, Mapping

UA = "research-script/1.0"
MIRROR = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml"
BF_EIN, SVCF_EIN, NPT_EIN, VCEP_EIN = "462109112", "205205488", "237825575", "232888152"

RETURNS = (  # (entity, ein, tax_year, object_id, role)
    ("Bright Funds Foundation", BF_EIN, 2023, "202433209349327603", "original"),
    ("Bright Funds Foundation", BF_EIN, 2024, "202543219349326714", "original"),
    ("Bright Funds Foundation", BF_EIN, 2024, "202503459349301950", "amended"),
    ("Silicon Valley Community Foundation", SVCF_EIN, 2023, "202413129349304911", "original"),
    ("Silicon Valley Community Foundation", SVCF_EIN, 2024, "202543149349305759", "original"),
    ("Vanguard Charitable Endowment Program", VCEP_EIN, 2023, "202441359349309439", "original"),
    ("Vanguard Charitable Endowment Program", VCEP_EIN, 2024, "202511349349313096", "original"),
)

SVCF_AUDIT = {2023: "https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2023.pdf",
              2024: "https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2024.pdf"}
SVCF_RELEASE = ("https://www.svcf.org/about/news-media/blog/"
                "silicon-valley-community-foundation-granted-1.54-billion-to-nonprofits-in-2024")
# Quoted (not computed) figures, USD. Audited statements: consolidated, Crowe LLP, years to 31 December.
QUOTED = (
    ("SVCF", 2024, "audited_grants_awarded", 3_187_080_000, SVCF_AUDIT[2024], "Consolidated statement of activities, 'Grants awarded' $3,187,080 (thousands)"),
    ("SVCF", 2023, "audited_grants_awarded", 4_655_917_000, SVCF_AUDIT[2024], "Comparative column, $4,655,917 (thousands)"),
    ("SVCF", 2024, "audited_grants_to_other_daf_sponsors", 1_667_000_000, SVCF_AUDIT[2024], "Note 2: 'included in grants expense are grants in the amount of $1,667,000,000 ... transferred to other donor-advised fund sponsors'"),
    ("SVCF", 2023, "audited_grants_to_other_daf_sponsors", 207_000_000, SVCF_AUDIT[2024], "Note 2 (same sentence, 2023 comparative); also 2023 audit note"),
    ("SVCF", 2024, "audited_contributions_from_other_daf_providers", 500_000_000, SVCF_AUDIT[2024], "Note 2: gifts 'transferred from other donor-advised fund providers'"),
    ("SVCF", 2023, "audited_contributions_from_other_daf_providers", 325_000_000, SVCF_AUDIT[2024], "Note 2 comparative"),
    ("SVCF", 2024, "audited_donor_advised_funds_granted_approx", 3_077_000_000, SVCF_AUDIT[2024], "Note 1 Programs: donor-advised funds 'granted approximately $3,077,000,000'"),
    ("SVCF", 2023, "audited_donor_advised_funds_granted_approx", 4_657_000_000, SVCF_AUDIT[2024], "Note 1 Programs, 2023 comparative"),
    ("SVCF", 2024, "audited_corporate_advised_granted_approx", 189_000_000, SVCF_AUDIT[2024], "Note 1 Programs: corporate-advised funds 'approximately $189,000,000'"),
    ("SVCF", 2023, "audited_corporate_advised_granted_approx", 134_000_000, SVCF_AUDIT[2024], "Note 1 Programs, 2023 comparative"),
    ("SVCF", 2024, "audited_grants_payable_net_eoy", 1_753_467_922, SVCF_AUDIT[2024], "Note 8"),
    ("SVCF", 2023, "audited_grants_payable_net_eoy", 2_067_074_776, SVCF_AUDIT[2024], "Note 8"),
    ("SVCF", 2024, "release_total_grants_preliminary", 1_540_000_000, SVCF_RELEASE, "'In 2024, SVCF distributed $1.54 billion in total grants'; 'Grantmaking figures exclude any distributions made from SVCF into donor advised funds at other institutions'; preliminary, unaudited"),
    ("SVCF", 2024, "release_bay_area_10_counties", 327_000_000, SVCF_RELEASE, "'$327 million supported organizations in 10 Bay Area counties'"),
    ("SVCF", 2024, "release_california_outside_bay_area", 175_000_000, SVCF_RELEASE, "'$175 million'"),
    ("SVCF", 2024, "release_us_outside_california", 874_000_000, SVCF_RELEASE, "'$874 million'"),
    ("SVCF", 2024, "release_grant_count_floor", 14_500, SVCF_RELEASE, "'over 14,500 grants' (a count, not USD)"),
)
CZ_EINS = ("882242512", "882010111", "931478843", "922259616")  # CZ Biohub LLCs (disregarded entities of 81-1669175)
TOP50_NET_FILED, TOP50_NET_DAFW = 78_287_627_404, 74_281_457_270  # b39n6-03 denominators


# ---------------------------------------------------------------- fetch (I/O)
def robots_ok(url: str, log: list) -> bool:
    base = "/".join(url.split("/")[:3])
    rp = urllib.robotparser.RobotFileParser()
    try:
        with urllib.request.urlopen(urllib.request.Request(base + "/robots.txt", headers={"User-Agent": UA}), timeout=30) as r:
            rp.parse(r.read().decode("utf-8", "replace").splitlines())
            code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
        if code in (404, 410):
            log.append({"host": base, "robots": code, "decision": "no rules"})
            return True
        log.append({"host": base, "robots": code, "decision": "unreadable: not fetched"})
        return False
    bots = ("ClaudeBot", "anthropic-ai", "Claude-User", "Claude-Web", "Claude-SearchBot", "*")
    ok = all(rp.can_fetch(b, url) for b in bots)
    log.append({"host": base, "robots": code, "decision": "allowed" if ok else "disallowed"})
    return ok


def fetch(root: str, cache: str) -> None:
    os.makedirs(cache, exist_ok=True)
    log: list = []
    for _, _, _, oid, _ in RETURNS:
        path, url = os.path.join(cache, f"{oid}.xml"), MIRROR.format(oid)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            continue
        if robots_ok(url, log):
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=600) as r, open(path, "wb") as f:
                f.write(r.read())
            time.sleep(1.5)
    print(json.dumps({"robots_log": log}, indent=1))


# ---------------------------------------------------------------- report (pure)
def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def first(root: ET.Element, name: str) -> str:
    return next(((e.text or "").strip() for e in root.iter() if local(e.tag) == name), "")


def num(s: str) -> float:
    try:
        return float(s)
    except (TypeError, ValueError):
        return 0.0


def child(e: ET.Element, name: str) -> str:
    return next(((x.text or "").strip() for x in e.iter() if local(x.tag) == name), "")


def group_total(root: ET.Element, grp: str) -> float:
    return next((num(child(e, "TotalAmt")) for e in root.iter() if local(e.tag) == grp), 0.0)


def sched_i_lines(root: ET.Element) -> tuple[dict, ...]:
    return tuple({"name": child(e, "BusinessNameLine1Txt"), "ein": child(e, "RecipientEIN"),
                  "usd": num(child(e, "CashGrantAmt")) + num(child(e, "NonCashAssistanceAmt")),
                  "purpose": child(e, "PurposeOfGrantTxt")}
                 for e in root.iter() if local(e.tag) == "RecipientTable")


def schedules(root: ET.Element) -> str:
    return ";".join(sorted({local(e.tag) for e in root.iter() if local(e.tag).startswith("IRS990Schedule")}))


def parse_return(path: str) -> dict:
    root = ET.parse(path).getroot()
    lines = sched_i_lines(root)
    return {"tax_period_end": first(root, "TaxPeriodEndDt"), "return_ts": first(root, "ReturnTs"),
            "amended": first(root, "AmendedReturnInd") == "X",
            "part_iv_line6_daf": first(root, "DonorAdvisedFundInd"),
            "schedules": schedules(root),
            "daf_count": first(root, "DonorAdvisedFundsHeldCnt"), "other_count": first(root, "FundsAndOtherAccountsHeldCnt"),
            "sd_l2_daf_contrib": num(first(root, "DonorAdvisedFundsContriAmt")),
            "sd_l2_other_contrib": num(first(root, "FundsAndOtherAccountsContriAmt")),
            "sd_l3_daf_grants": num(first(root, "DonorAdvisedFundsGrantsAmt")),
            "sd_l3_other_grants": num(first(root, "FundsAndOtherAccountsGrantsAmt")),
            "sd_l4_daf_eoy": num(first(root, "DonorAdvisedFundsVlEOYAmt")),
            "ix_l1": group_total(root, "GrantsToDomesticOrgsGrp"), "ix_l2": group_total(root, "GrantsToDomesticIndividualsGrp"),
            "ix_l3": group_total(root, "ForeignGrantsGrp"), "ix_total_expenses": group_total(root, "TotalFunctionalExpensesGrp"),
            "part_i_l13_grants": num(first(root, "CYGrantsAndSimilarPaidAmt")),
            "viii_l1h_contrib": num(first(root, "CYContributionsGrantsAmt")),
            "total_revenue": num(first(root, "CYTotalRevenueAmt")),
            "net_assets_eoy": num(first(root, "NetAssetsOrFundBalancesEOYAmt")),
            "program_text": first(root, "Desc") if first(root, "DonorAdvisedFundInd") == "false" else "",
            "sched_i_n": len(lines), "sched_i_usd": sum(l["usd"] for l in lines), "lines": lines}


def read_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def row(task, entity, ein, period, metric, value, basis, source, note="") -> dict:
    return {"task": task, "entity": entity, "ein": ein, "period": period, "metric": metric,
            "value": value if isinstance(value, str) else (round(value, 6) if isinstance(value, float) and abs(value) < 10 else int(round(value))),
            "basis": basis, "source": source, "note": note}


def bright_rows(ret: Mapping, vcep: Mapping, root: str) -> list[dict]:
    T, E, N = "P-B39N603-02", "Bright Funds Foundation", BF_EIN
    filed = [row(T, E, N, y, m, v, "F", MIRROR.format(oid), note)
             for (y, oid) in ((2023, "202433209349327603"), (2024, "202543219349326714"))
             for (m, v, note) in (
                 ("part_iv_line6_daf_indicator", ret[oid]["part_iv_line6_daf"], "Form 990 Part IV line 6 (DonorAdvisedFundInd)"),
                 ("schedule_d_part_i_present", "yes" if ret[oid]["daf_count"] or ret[oid]["sd_l3_daf_grants"] else "no", "Schedule D filed but Part I blank"),
                 ("schedules_filed", ret[oid]["schedules"], ""),
                 ("viii_l1h_contributions", ret[oid]["viii_l1h_contrib"], ""),
                 ("ix_l1_domestic_org_grants", ret[oid]["ix_l1"], ""),
                 ("ix_l3_foreign_grants", ret[oid]["ix_l3"], ""),
                 ("ix_total_functional_expenses", ret[oid]["ix_total_expenses"], ""),
                 ("schedule_i_part_ii_lines", ret[oid]["sched_i_n"], "count; Schedule I holds only the records-maintained flag"),
                 ("net_assets_eoy", ret[oid]["net_assets_eoy"], ""),
                 ("part_iii_program_text", ret[oid]["program_text"][:240], "first 240 characters"))]
    amended_same = all(ret["202503459349301950"][k] == ret["202543219349326714"][k]
                       for k in ("viii_l1h_contrib", "ix_l1", "ix_l3", "part_iv_line6_daf", "net_assets_eoy"))
    vlines = [(fy, l) for fy, oid in ((2023, "202441359349309439"), (2024, "202511349349313096"))
              for l in vcep[oid]["lines"] if l["ein"] == N]
    pt = next(r for r in read_csv(os.path.join(root, "data/mission-2026-11-14/pass-through-recipients-2026-11-20.csv")) if r["ein"] == N)
    wl = {r["recipient_ein"] for r in read_csv(os.path.join(root, "data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv"))}
    filed_usd, dafw_usd = num(pt["top50_usd_all_filed"]), num(pt["top50_usd_all_daf_weighted"])
    contrib = sum(ret[o]["viii_l1h_contrib"] for o in ("202433209349327603", "202543219349326714"))
    grants = sum(ret[o]["ix_l1"] + ret[o]["ix_l2"] + ret[o]["ix_l3"] for o in ("202433209349327603", "202543219349326714"))
    derived = [
        row(T, E, N, "2024", "amended_return_matches_original", "yes" if amended_same else "no", "C", MIRROR.format("202503459349301950"), "contributions, Part IX 1/3, Part IV 6, net assets"),
        *[row(T, "Vanguard Charitable -> Bright Funds", VCEP_EIN, f"FY{fy}", "schedule_i_line_usd", l["usd"], "F", MIRROR.format(oid), l["purpose"])
          for (fy, l), oid in zip(vlines, ("202441359349309439", "202511349349313096"))],
        row(T, E, N, "FY2023-24", "top50_net_filed_usd", filed_usd, "C (repo)", "data/mission-2026-11-14/pass-through-recipients-2026-11-20.csv", "counted as a final charity recipient"),
        row(T, E, N, "FY2023-24", "top50_net_daf_weighted_usd", dafw_usd, "C (repo)", "data/mission-2026-11-14/pass-through-recipients-2026-11-20.csv", ""),
        row(T, E, N, "FY2023-24", "share_of_top50_net_filed", filed_usd / TOP50_NET_FILED, "C", "b39n6-03 denominator $78,287,627,404", ""),
        row(T, E, N, "FY2023-24", "share_of_top50_net_daf_weighted", dafw_usd / TOP50_NET_DAFW, "C", "b39n6-03 denominator $74,281,457,270", ""),
        row(T, E, N, "TY2023-24", "onward_ratio_grants_to_contrib", grants / contrib, "C", "Part IX 1-3 / Part VIII 1h", ""),
        row(T, E, N, "-", "on_daf_to_daf_whitelist", "yes" if N in wl else "no", "C (repo)", "data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv", ""),
        row(T, E, N, "-", "market_total_effect_usd", 0, "I", "", "no DAF grants filed (Part IV 6 = No), so nothing is double counted; whitelisting would wrongly remove up to the upper-tier amount"),
        row(T, E, N, "-", "whitelist_upper_tier_wrong_removal_usd", filed_usd, "C", "", "upper tier weight 1.0 if included; central weight = grantor share x recipient DAF share of assets (0) = 0"),
        row(T, E, N, "-", "recommended_class", "donation_processor_non_daf (workplace giving); not DAF sponsor; not whitelist", "I", "", ""),
    ]
    return filed + derived


def svcf_rows(ret: Mapping, root: str) -> tuple[list[dict], dict]:
    T, E, N = "P-G1913-02-03", "Silicon Valley Community Foundation", SVCF_EIN
    oids = {2023: "202413129349304911", 2024: "202543149349305759"}
    filed = [row(T, E, N, f"CY{y}", m, ret[oid][k], "F", MIRROR.format(oid), note)
             for y, oid in oids.items()
             for (m, k, note) in (
                 ("sched_d_l1_daf_count", "daf_count", "count"),
                 ("sched_d_l2_daf_contributions", "sd_l2_daf_contrib", ""),
                 ("sched_d_l3_daf_grants", "sd_l3_daf_grants", "DAFRC FY2024 value for SVCF = this line (CY2024)"),
                 ("sched_d_l3_other_funds_grants", "sd_l3_other_grants", ""),
                 ("sched_d_l4_daf_eoy_value", "sd_l4_daf_eoy", ""),
                 ("part_ix_l1_domestic_org_grants", "ix_l1", ""),
                 ("part_ix_l2_individual_grants", "ix_l2", ""),
                 ("part_ix_l3_foreign_grants", "ix_l3", ""),
                 ("part_i_l13_grants_total", "part_i_l13_grants", "= Part IX lines 1-3"),
                 ("schedule_i_part_ii_usd", "sched_i_usd", ""),
                 ("schedule_i_part_ii_lines", "sched_i_n", "count"))
             if not isinstance(ret[oid][k], str) or ret[oid][k]]
    filed = [dict(r, value=int(num(r["value"]))) if r["metric"] == "sched_d_l1_daf_count" else r for r in filed]
    np = {r["fiscal_year"]: r for r in read_csv(os.path.join(root, "data/mission-2026-11-14/net-payout-by-sponsor.csv")) if r["ein"] == N}
    l24, l23 = ret[oids[2024]]["lines"], ret[oids[2023]]["lines"]
    npt24 = sum(l["usd"] for l in l24 if l["ein"] == NPT_EIN)
    cz23 = sum(l["usd"] for l in l23 if l["ein"] in CZ_EINS)
    ff23 = sum(l["usd"] for l in l23 if l["ein"] == "921117448")
    q = {(y, m): v for _, y, m, v, _, _ in QUOTED}
    aud_net24 = q[(2024, "audited_grants_awarded")] - q[(2024, "audited_grants_to_other_daf_sponsors")]
    aud_net23 = q[(2023, "audited_grants_awarded")] - q[(2023, "audited_grants_to_other_daf_sponsors")]
    rel = q[(2024, "release_total_grants_preliminary")]
    geo = q[(2024, "release_bay_area_10_counties")] + q[(2024, "release_california_outside_bay_area")] + q[(2024, "release_us_outside_california")]
    tier = lambda fy, k: num(np[fy][k])
    sd24 = ret[oids[2024]]["sd_l3_daf_grants"]
    ix24 = ret[oids[2024]]["part_i_l13_grants"]
    cnt = q[(2024, "release_grant_count_floor")]
    quoted = [row(T, E, N, f"CY{y}", m, float(v), "Q", src, note) for _, y, m, v, src, note in QUOTED]
    derived = [
        row(T, E, N, "CY2024", "sched_i_line_to_npt", npt24, "F", MIRROR.format(oids[2024]), "single line, purpose 'General Nonprofit Support'"),
        row(T, E, N, "CY2024", "npt_line_share_of_audited_transfers", npt24 / q[(2024, "audited_grants_to_other_daf_sponsors")], "C", "", ""),
        row(T, E, N, "CY2024", "repo_transfers_tier_a_national", tier("2024", "transfers_tier_a"), "C (repo)", "data/mission-2026-11-14/net-payout-by-sponsor.csv", "Schedule I lines to national DAF sponsors"),
        row(T, E, N, "CY2024", "repo_transfers_tier_b", tier("2024", "transfers_tier_b"), "C (repo)", "data/mission-2026-11-14/net-payout-by-sponsor.csv", "adds processors"),
        row(T, E, N, "CY2024", "repo_transfers_tier_c", tier("2024", "transfers_tier_c"), "C (repo)", "data/mission-2026-11-14/net-payout-by-sponsor.csv", "all DAF-sponsor recipients"),
        row(T, E, N, "CY2024", "audited_grants_net_of_daf_transfers", float(aud_net24), "C", SVCF_AUDIT[2024], "audited grants awarded - transfers to other DAF sponsors"),
        row(T, E, N, "CY2024", "release_minus_audited_net", float(rel - aud_net24), "C", "", "preliminary release vs audited; unexplained residual"),
        row(T, E, N, "CY2024", "release_international_implied", float(rel - geo), "C", SVCF_RELEASE, "$1.54bn minus three US geography buckets"),
        row(T, E, N, "CY2024", "part_ix_minus_audited_grants", ix24 - q[(2024, "audited_grants_awarded")], "C", "", "990 (SVCF entity, gross) vs audited consolidated; not decomposed"),
        row(T, E, N, "CY2024", "sched_d_l3_minus_tier_a", sd24 - tier("2024", "transfers_tier_a"), "C", "", "DAF grants net of transfers to national sponsors (DAF-only scope)"),
        row(T, E, N, "CY2024", "part_ix_minus_tier_a", ix24 - tier("2024", "transfers_tier_a"), "C", "", "all-fund grants net of national-sponsor recipients (990 basis)"),
        row(T, E, N, "CY2024", "tier_a_minus_audited_transfers", tier("2024", "transfers_tier_a") - q[(2024, "audited_grants_to_other_daf_sponsors")], "C", "", "repo Schedule I tier A vs audited note"),
        row(T, E, N, "CY2024", "part_ix_minus_tier_c",ix24 - tier("2024", "transfers_tier_c"), "C", "", "all-fund grants net of all DAF-sponsor recipients (990 basis)"),
        row(T, E, N, "CY2024", "avg_grant_dafrc_gross", sd24 / cnt, "C", "", "$3.06bn / 14,500 (g1913-02 figure)"),
        row(T, E, N, "CY2024", "avg_grant_audited_net", aud_net24 / cnt, "C", "", "all funds, net of DAF transfers"),
        row(T, E, N, "CY2024", "avg_grant_release", rel / cnt, "C", "", ""),
        row(T, E, N, "CY2023", "audited_grants_net_of_daf_transfers", float(aud_net23), "C", SVCF_AUDIT[2024], ""),
        row(T, E, N, "CY2023", "sched_i_cz_biohub_llcs", cz23, "F", MIRROR.format(oids[2023]), "four CZ LLC EINs; filed basis (repo $1,594.0m is DAF-weighted)"),
        row(T, E, N, "CY2023", "sched_i_further_future_foundation", ff23, "F", MIRROR.format(oids[2023]), "EIN 92-1117448, purpose 'Sciences'"),
        row(T, E, N, "CY2023", "repo_transfers_tier_c", tier("2023", "transfers_tier_c"), "C (repo)", "data/mission-2026-11-14/net-payout-by-sponsor.csv", ""),
        row(T, E, N, "CY2024", "cz_biohub_llc_lines_cy2024", sum(l["usd"] for l in l24 if l["ein"] in CZ_EINS), "F", MIRROR.format(oids[2024]), "Biohub is a CY2023 item; absent from CY2024 gap"),
    ]
    summary = {"svcf_cy2024_sched_d_l3": sd24, "svcf_cy2024_part_ix_total": ix24, "npt_line": npt24,
               "audited_net_cy2024": aud_net24, "release": rel, "release_minus_audited_net": rel - aud_net24,
               "tier_a_cy2024": tier("2024", "transfers_tier_a"), "cz23": cz23, "ff23": ff23}
    return filed + quoted + derived, summary


def report(root: str, cache: str, out: str) -> None:
    ret = {oid: parse_return(os.path.join(cache, f"{oid}.xml")) for _, _, _, oid, _ in RETURNS}
    bf = bright_rows(ret, ret, root)
    sv, summ = svcf_rows(ret, root)
    rows = bf + sv
    fields = ["task", "entity", "ein", "period", "metric", "value", "basis", "source", "note"]
    with open(os.path.join(root, out), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(json.dumps({"rows": len(rows), **{k: v for k, v in summ.items()},
                      "bright": {f"{r['metric']}:{r['period']}": r["value"] for r in bf}}, indent=1, default=str))


def main(argv: Iterable[str]) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=("fetch", "report"))
    ap.add_argument("root")
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", default="data/mission-2026-11-14/bright-funds-svcf-2026-11-20.csv")
    a = ap.parse_args(list(argv))
    fetch(a.root, a.cache) if a.stage == "fetch" else report(a.root, a.cache, a.out)


if __name__ == "__main__":
    main(sys.argv[1:])
