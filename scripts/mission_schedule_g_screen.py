#!/usr/bin/env python3
"""Schedule G / line 11e screen of every parsed DAF-sponsor Form 990 (queue item P-COST-05).

Question: which sponsors besides Givinga look like platforms whose DAF "accounts" and "contributions" are
platform-user records or gross receipts? Two screens over the 5,272 returns parsed for
data/mission-2026-11-14/sponsor-cost-structure.csv:

  S1  Part IX line 11e (professional fundraising fees) > 25% of operating cost (operating cost = Part IX
      total less lines 1-4 and 11f, as defined in sponsor-cost-structure.csv). Read from that CSV; no fetch.
  S2  Schedule G content. Part I line 2b fundraisers (name, activity, gross receipts, amount retained,
      control of funds), Part II event names, Part III gaming income, matched against a keyword list
      (gaming, sweepstakes, raffle, round-up, app, online, platform, payment processing ...).

Stdlib only; functional style (pure transforms, I/O at the edges). Reuses helpers from
scripts/mission_990_contractors.py. The returns are streamed from the GivingTuesday mirror of IRS e-file XML
  https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml
Parsing stops once Part IV shows lines 17, 18 and 19 all "No" (Schedule G not required), or once Schedule G has
closed, so Schedule I of large sponsors is never downloaded in full. Parsed extracts (not raw XML) are cached in
CACHE/extract990g/{oid}.json.

Inputs (read only):
  data/mission-2026-11-14/sponsor-cost-structure.csv    one row per parsed return (object id, Part IX, Sch D)
Outputs:
  data/mission-2026-11-14/schedule-g-screen.csv         one row per flagged return (S1 or S2 or Part IV line 19)
  stdout                                                JSON summary

Usage:
  python3 scripts/mission_schedule_g_screen.py --cache-dir CACHE [--fetch] [--workers 16]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as m990  # noqa: E402

DATA = m990.DATA
COST_CSV = os.path.join(DATA, "sponsor-cost-structure.csv")
OUT_CSV = os.path.join(DATA, "schedule-g-screen.csv")
XML_URL = m990.XML_URL
EXTRACT_VERSION = 1
L11E_SHARE_THRESHOLD = 0.25
GROSS_SHARE_THRESHOLD = 0.10      # Sch G Part I line 2b gross receipts / Part I line 8 total contributions
RETAINED_SHARE_THRESHOLD = 0.25   # amount retained by fundraiser / its gross receipts
DAF_RELEVANT_SHARE = 0.50         # Sch D DAF contributions / Part I total contributions: DAF totals are exposed
num, fmt, local, text_of = m990.num, m990.fmt, m990.local, m990.text_of

PART_IV = ("ProfessionalFundraisingInd", "FundraisingActivitiesInd", "GamingActivitiesInd")
# keyword -> theme. Word-boundary regexes over fundraiser names, activity text and event names.
KEYWORDS = (
    (r"gaming|gambl|casino|bingo|pull[- ]?tab|poker|lotter", "gaming"),
    (r"sweepstake|raffle|\bdrawings?\b|\bprizeo?\b", "sweepstakes/raffle"),
    (r"round[- ]?up|roundup|spare change", "round-up"),
    (r"\bapps?\b|mobile|text[- ]to[- ]give|texting", "app/mobile"),
    (r"on-?line|internet|\bweb\b|web-based|website|e-?commerce|digital|crowdfund|peer[- ]to[- ]peer|\bp2p\b|social media|"
     r"livestream", "online"),
    (r"platform|portal|payments?\b|payment processing|processor|merchant|checkout", "platform/payments"),
    (r"workplace|employee giving|matching gift|payroll", "workplace giving"),
    (r"paypal|benevity|givinga|blackbaud|bonterra|network for good|classy|gofundme|yourcause|cybergrants|"
     r"facebook|meta platforms|tiltify|twitch|pledgeling|change inc|daffy|every\.?org|endaoment|chariot|"
     r"\bamazon\b|\bsquare inc|\bstripe\b|venmo|givelively|give lively|frontstream|givecampus|givegab|omaze|"
     r"jackpocket|fandiem|charitybuzz|golden hearts games|softgiving|brandfluence", "named platform"),
)
KW = tuple((re.compile(p, re.I), theme) for p, theme in KEYWORDS)


def truthy(v: str) -> bool:
    return str(v).strip().lower() in ("1", "true", "x")


# ----------------------------------------------------------------------------- streamed extract
def fundraiser_from(g) -> dict:
    name = " ".join(t for t in (text_of(g, ("OrganizationBusinessName", "BusinessNameLine1Txt")),
                                text_of(g, ("OrganizationBusinessName", "BusinessNameLine2Txt")),
                                text_of(g, ("PersonNm",))) if t)
    return {"name": name.strip(), "activity": text_of(g, ("ActivityTxt",)),
            "control_of_funds": text_of(g, ("FundraiserControlOfFundsInd",)),
            "gross_receipts": num(text_of(g, ("GrossReceiptsAmt",))),
            "retained": num(text_of(g, ("RetainedByContractorAmt",))),
            "net_to_org": num(text_of(g, ("NetToOrganizationAmt",)))}


def sched_g_from(el) -> dict:
    ev = next(iter(el.iter(m990.NS + "FundraisingEventInformationGrp")), None)
    gm = next(iter(el.iter(m990.NS + "GamingInformationGrp")), None)
    events = tuple(t for t in (text_of(ev, (k,)) for k in ("Event1Nm", "Event2Nm")) if t) if ev is not None else ()
    return {"sched_g_present": 1,
            "methods": [local(c.tag) for c in el if local(c.tag).endswith("SolicitationsInd")
                        or local(c.tag) in ("SpecialFundraisingEventsInd", "SolicitationOfNonGovtGrantsInd",
                                            "SolicitationOfGovtGrantsInd")],
            "fundraisers": [fundraiser_from(g) for g in el.iter(m990.NS + "FundraiserActivityInfoGrp")],
            "total_retained": num(text_of(el, ("TotalRetainedByContractorsAmt",))),
            "total_net_to_org": num(text_of(el, ("TotalNetToOrganizationAmt",))),
            "events": list(events),
            "other_events_cnt": num(text_of(ev, ("OtherEventsTotalCnt",))) if ev is not None else None,
            "events_gross_receipts": num(text_of(ev, ("GrossReceiptsTotalAmt",))) if ev is not None else None,
            "gaming_gross_income": num(text_of(gm, ("GamingGrossIncomeAmt",))) if gm is not None else
            num(next((x.text for x in el.iter() if local(x.tag) == "TotalGamingGrossIncomeAmt"), None)),
            "gaming_tags": sorted({local(x.tag) for x in el.iter() if "Gaming" in local(x.tag)
                                   or local(x.tag) in ("BingoInd", "PullTabsInd")})[:12]}


def extract_g_stream(stream) -> dict:
    """Part IV lines 17-19, then Schedule G if any is Yes. Returns as soon as the answer is known."""
    out: dict = {"sched_g_present": 0, "stopped": "eof"}
    for _event, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        if tag == "IRS990":
            out.update({k: text_of(el, (k,)) for k in PART_IV})
            out["part_viii_l1c_fundraising_events"] = num(text_of(el, ("FundraisingAmt",)))
            el.clear()
            if not any(truthy(out[k]) for k in PART_IV):
                return {**out, "stopped": "part_iv_no"}
        elif tag == "IRS990ScheduleG":
            return {**out, **sched_g_from(el), "stopped": "after_sched_g"}
        elif tag.startswith("IRS990Schedule") or tag == "ReturnHeader":
            el.clear()
    return out


def fetch_g(oid: str, cache_dir: str, fetch: bool, retries: int = 2) -> dict:
    path = os.path.join(cache_dir, "extract990g", f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            cached = json.load(fh)
        if cached.get("_v") == EXTRACT_VERSION:
            return cached
    if not fetch:
        return {"xml_status": "not_fetched"}
    url = XML_URL.format(oid=oid)
    req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    out = {"xml_status": "error:none"}
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                out = {**extract_g_stream(resp), "xml_status": "ok"}
            break
        except urllib.error.HTTPError as e:
            out = {"xml_status": f"http_{e.code}"}
            if e.code in (403, 404):
                break
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
            out = {"xml_status": f"error:{type(e).__name__}"}
            time.sleep(2 * (attempt + 1))
    result = {**out, "_v": EXTRACT_VERSION, "xml_url": url}
    if not result["xml_status"].startswith("error"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(result, fh)
    return result


# ----------------------------------------------------------------------------- screening (pure)
def themes_of(texts: Iterable[str]) -> tuple[str, ...]:
    joined = " | ".join(t for t in texts if t)
    return tuple(dict.fromkeys(theme for rx, theme in KW if rx.search(joined)))


def total_contributions(oid: str, cache_dir: str) -> float | None:
    """Part I line 8 (CYContributionsGrantsAmt) from the cached cost extract written by
    scripts/mission_sponsor_cost_structure.py (CACHE/extract990cost/{oid}.json). Read only."""
    path = os.path.join(cache_dir, "extract990cost", f"{oid}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return num((json.load(fh).get("part_i") or {}).get("CYContributionsGrantsAmt"))


def screen_row(r: Mapping, g: Mapping, total_contrib: float | None = None) -> dict:
    opex, l11e = num(r["operating_cost"]), num(r["fees_prof_fundraising_l11e"])
    share = l11e / opex if l11e is not None and opex not in (None, 0) else None
    frs = g.get("fundraisers") or []
    texts = [f["name"] for f in frs] + [f["activity"] for f in frs] + list(g.get("events") or [])
    th = themes_of(texts)
    gross = sum(f["gross_receipts"] or 0 for f in frs)
    retained = sum(f["retained"] or 0 for f in frs)
    controls = any(truthy(f["control_of_funds"]) for f in frs)
    contrib = num(r["daf_contributions"])
    gross_share = gross / total_contrib if total_contrib not in (None, 0) and gross else None
    daf_share = contrib / total_contrib if contrib is not None and total_contrib not in (None, 0) else None
    kept_share = retained / gross if gross else None
    flags = tuple(f for f, on in (
        ("S1_l11e_gt_25pct_opex", share is not None and share > L11E_SHARE_THRESHOLD),
        ("S2_keyword", bool(th)),
        ("S2_gaming_part_iii", truthy(g.get("GamingActivitiesInd", "")) or (g.get("gaming_gross_income") or 0) > 0),
        ("S2_fundraiser_controls_funds", controls),
        ("S2_fundraiser_gross_ge_10pct_daf_contrib", contrib not in (None, 0) and gross >= 0.10 * contrib),
    ) if on)
    tier = ("" if not flags else
            "A_platform_gross_receipts_high_take" if (gross_share or 0) >= GROSS_SHARE_THRESHOLD
            and (kept_share or 0) >= RETAINED_SHARE_THRESHOLD else
            "B_agent_gross_receipts_low_take" if (gross_share or 0) >= GROSS_SHARE_THRESHOLD else
            "C_l11e_heavy_no_gross_agent" if "S1_l11e_gt_25pct_opex" in flags else
            "D_keyword_gaming_or_control_only")
    return {"ein": r["ein"], "sponsor_name": r["sponsor_name"], "category": r["category"],
            "fiscal_year": r["fiscal_year"], "tax_period": r["tax_period"],
            "operating_cost": r["operating_cost"], "l11e_prof_fundraising": r["fees_prof_fundraising_l11e"],
            "l11e_share_of_opex": fmt(round(share, 4)) if share is not None else "",
            "daf_accounts": r["daf_accounts"], "daf_contributions": r["daf_contributions"],
            "daf_assets_eoy": r["daf_assets_eoy"],
            "part_iv_l17_prof_fundraising": g.get("ProfessionalFundraisingInd", ""),
            "part_iv_l18_events": g.get("FundraisingActivitiesInd", ""),
            "part_iv_l19_gaming": g.get("GamingActivitiesInd", ""),
            "sched_g_present": g.get("sched_g_present", 0),
            "sg_fundraiser_count": len(frs),
            "sg_fundraisers": " ; ".join(f"{f['name']} [{f['activity']}] gross={fmt(f['gross_receipts'])} "
                                         f"retained={fmt(f['retained'])} control={f['control_of_funds']}" for f in frs)[:900],
            "sg_fundraiser_gross_total": fmt(gross), "sg_fundraiser_retained_total": fmt(retained),
            "total_contributions_part_i": fmt(total_contrib),
            "daf_contrib_share_of_total_contrib": fmt(round(daf_share, 4)) if daf_share is not None else "",
            "daf_relevant": int(daf_share is not None and daf_share >= DAF_RELEVANT_SHARE),
            "sg_gross_share_of_total_contrib": fmt(round(gross_share, 4)) if gross_share is not None else "",
            "sg_retained_share_of_gross": fmt(round(kept_share, 4)) if kept_share is not None else "",
            "sg_events": " ; ".join(g.get("events") or []),
            "sg_events_gross_receipts": fmt(g.get("events_gross_receipts")),
            "sg_gaming_gross_income": fmt(g.get("gaming_gross_income")),
            "keyword_themes": " ; ".join(th), "flags": " ; ".join(flags), "tier": tier,
            "xml_status": g.get("xml_status", ""), "return_object_id": r["return_object_id"],
            "xml_url": r["xml_url"], "source_url": r["source_url"]}


FIELDS = ("ein", "sponsor_name", "category", "fiscal_year", "tax_period", "operating_cost", "l11e_prof_fundraising",
          "l11e_share_of_opex", "daf_accounts", "daf_contributions", "daf_assets_eoy", "part_iv_l17_prof_fundraising",
          "part_iv_l18_events", "part_iv_l19_gaming", "sched_g_present", "sg_fundraiser_count", "sg_fundraisers",
          "sg_fundraiser_gross_total", "sg_fundraiser_retained_total", "total_contributions_part_i",
          "daf_contrib_share_of_total_contrib", "daf_relevant", "sg_gross_share_of_total_contrib",
          "sg_retained_share_of_gross", "sg_events", "sg_events_gross_receipts",
          "sg_gaming_gross_income", "keyword_themes", "flags", "tier", "xml_status", "return_object_id", "xml_url",
          "source_url")


def summarise(rows: Sequence[Mapping], extracts: Mapping[str, Mapping]) -> dict:
    def count(pred) -> int:
        return sum(1 for r in rows if pred(r))
    st = {}
    for g in extracts.values():
        st[g.get("xml_status", "")] = st.get(g.get("xml_status", ""), 0) + 1
    flagged = tuple(r for r in rows if r["flags"])
    return {"returns_screened": len(rows), "xml_status": st,
            "part_iv_any_yes": count(lambda r: any(truthy(r[k]) for k in ("part_iv_l17_prof_fundraising",
                                                                          "part_iv_l18_events", "part_iv_l19_gaming"))),
            "sched_g_present": count(lambda r: r["sched_g_present"] == 1),
            "with_fundraiser_rows": count(lambda r: r["sg_fundraiser_count"] > 0),
            "flagged_returns": len(flagged),
            "flagged_eins": len({r["ein"] for r in flagged}),
            "by_tier_returns": {t: sum(1 for r in flagged if r["tier"] == t) for t in sorted({r["tier"] for r in flagged})},
            "daf_relevant_abc": sorted({(r["tier"][0], r["sponsor_name"]) for r in flagged
                                        if r["daf_relevant"] and r["tier"][:1] in "ABC"}),
            "by_tier_eins": {t: sorted({r["sponsor_name"] for r in flagged if r["tier"] == t}) if not t.startswith("D")
                             else len({r["ein"] for r in flagged if r["tier"] == t})
                             for t in sorted({r["tier"] for r in flagged})},
            "by_flag": {f: sum(1 for r in flagged if f in r["flags"].split(" ; ")) for f in
                        ("S1_l11e_gt_25pct_opex", "S2_keyword", "S2_gaming_part_iii", "S2_fundraiser_controls_funds",
                         "S2_fundraiser_gross_ge_10pct_daf_contrib")}}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--out", default=OUT_CSV)
    a = ap.parse_args(argv)
    cost = m990.read_csv(COST_CSV)
    oids = tuple(dict.fromkeys(r["return_object_id"] for r in cost))
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        extracts = dict(zip(oids, ex.map(lambda o: fetch_g(o, a.cache_dir, a.fetch), oids)))
    rows = tuple(screen_row(r, extracts.get(r["return_object_id"], {}),
                            total_contributions(r["return_object_id"], a.cache_dir)) for r in cost)
    out = sorted((r for r in rows if r["flags"]), key=lambda r: (r["tier"], r["sponsor_name"], r["fiscal_year"]))
    m990.write_csv(a.out, out, FIELDS)
    print(json.dumps(summarise(rows, extracts), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
