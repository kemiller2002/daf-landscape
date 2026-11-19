#!/usr/bin/env python3
"""Profile the church block of top-50 DAF dollars (P-B40N1202-B43N26-06).

The block  Recipients that scripts/mission_recipient_basis_eligibility.py puts in `no_efiled_990_church`: in the IRS
           EO BMF, SUBSECTION 03, FOUNDATION 10 (church, 170(b)(1)(A)(i)), not a private foundation, not a DAFRC panel
           sponsor, and no Form 990/990-EZ/990-PF in the IRS TEOS e-file index 2019-2026. That run reports 29,469
           recipients and $6.18bn (8.3%) of top-50 FY2023-24 DAF-weighted, non-DAF-to-DAF Schedule I dollars. The
           numerator, BMF join, filing history and rule order are imported from that script, not re-implemented.

Profiles   concentration (top recipients, Lorenz points, top-1%/10% shares, Gini); denomination (BMF GROUP = group
           exemption number, resolved to the central organisation's BMF name where AFFILIATION is 6 or 8, then NTEE
           X-codes, then the recipient's own name, each tagged with its method); size (DAF-weighted dollars per church
           and per Schedule I line, i.e. per sponsor-year-recipient aggregate); geography (BMF STATE); sponsor mix
           (each top-50 sponsor, grouped as Christian faith, Jewish faith, national, community foundation, other);
           megachurches (name + state matching against the Outreach 100 "Largest Churches in America" 2023 and 2024
           lists, cached HTML, plus size tiers by DAF dollars).

A comparison block, `church_coded_all`, is every FOUNDATION 10 recipient whatever its filing status.

Pure functions; I/O only in load/fetch helpers and `main`. Stdlib only.

Usage:
  python3 scripts/mission_church_recipients.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --index-dir IRSDIR --outreach-dir DIR [--fetch-outreach] [--sample-out FILE]
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
import urllib.robotparser
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DATA, _group_by_fast, ein9, read_csv, write_csv, DAFRC_CSV  # noqa: E402
from mission_daf_share_recipient_revenue import load_bmf  # noqa: E402
from mission_daf_to_daf import top_n, TOP_N  # noqa: E402
from mission_recipient_basis_eligibility import build_numerator, load_bmf_extra, load_history, units_b  # noqa: E402
from mission_recipient_sectors import BMF_FILES  # noqa: E402

OUT = os.path.join(DATA, "church-daf-recipients-profile-2026-11-19.csv")
UA = "research-script/1.0"
SEED = 20261119
BLOCK = "no_efiled_990_church"
LDS = "870234341"  # The Church of Jesus Christ of Latter-day Saints (BMF), the largest single recipient
OUTREACH_YEARS = (2023, 2024)
OUTREACH_URL = "https://outreach100.com/largest-churches-in-america/{y}"
OUTREACH_PAGES = 6

# Sponsor groups. Faith sponsors are the top-50 DAFRC sponsors whose DAFRC subtype is "Religiously-Affiliated", plus
# Servant Foundation (The Signatry), which DAFRC types National/Standard but which the repo treats as a faith sponsor
# (direction-sponsor-executive-compensation.md, faith_single_issue list).
FAITH_CHRISTIAN = {"581493949": "NCF", "431890105": "Servant Foundation (The Signatry)",
                   "411802412": "Thrivent Charitable"}
FAITH_JEWISH = {"237174183": "Jewish Communal Fund (NY)", "042103559": "Combined Jewish Philanthropies",
                "941156533": "Jewish Community Federation SF", "956111928": "Jewish Community Foundation LA"}

SIZE_BANDS = ((0, 10_000, "a <$10k"), (10_000, 25_000, "b $10k-25k"), (25_000, 50_000, "c $25k-50k"),
              (50_000, 100_000, "d $50k-100k"), (100_000, 250_000, "e $100k-250k"), (250_000, 1_000_000, "f $250k-1m"),
              (1_000_000, 10_000_000, "g $1m-10m"), (10_000_000, float("inf"), "h >=$10m"))

# Denomination families, tested in order on an upper-case name. First match wins.
FAMILIES = (
    ("latter_day_saints", r"LATTER[ -]DAY|\bLDS\b|DESERET"),
    ("jewish", r"JEWISH|SYNAGOGUE|\bTORAH|CHABAD|LUBAVITCH|YESHIV|\bSHUL\b|KEHIL|\bBETH\b|\bBNAI\b|B NAI|\bANSHE|"
               r"AGUDA|KOLLEL|MESIVTA|TALMUD|\bCHEVRA|\bCONG\b|CONGREGATION (OHR|BETH|BNAI|SHAAR|KEHILAT|AHAVATH|"
               r"ADATH|AHAVAS|EMANU|ISRAEL|SONS|TIFERETH|YESHUA|MACHZIKEI|ZICHRON|BAIS|BES|BNEI)|\bBAIS\b|\bBNEI\b|"
               r"SHAAREI|EMANU[- ]?EL|HEBREW|RABBI"),
    ("muslim", r"ISLAM|MASJID|MOSQUE|MUSLIM|\bQURAN|\bSUNNI|\bSHIA\b"),
    ("eastern_orthodox", r"ORTHODOX|ANTIOCH|COPTIC|ARMENIAN APOSTOLIC"),
    ("roman_catholic", r"CATHOLIC|\bPARISH|ARCHDIOCESE|DIOCESE|\bST\.? [A-Z]+ (ROMAN|R C)|\bR C\b|ROMAN|OUR LADY|"
                       r"BLESSED SACRAMENT|SACRED HEART|IMMACULATE|HOLY (FAMILY|NAME|ROSARY|CROSS|TRINITY CATHOLIC)|"
                       r"\bOF THE ASSUMPTION|CATHEDRAL OF ST|NEWMAN|JESUIT|FRANCISCAN|DOMINICAN|BENEDICTINE|"
                       r"\bOPUS DEI|CARMELITE"),
    ("methodist", r"METHODIST|\bAME\b|A M E|WESLEYAN|NAZARENE"),
    ("episcopal_anglican", r"EPISCOPAL|ANGLICAN"),
    ("lutheran", r"LUTHERAN|\bELCA\b"),
    ("presbyterian_reformed", r"PRESBYTER|\bPCA\b|REFORMED|CHRISTIAN REFORMED|\bPC ?USA\b"),
    ("baptist", r"BAPTIST"),
    ("pentecostal", r"ASSEMBL(Y|IES) OF GOD|PENTECOST|FOURSQUARE|CHURCH OF GOD IN CHRIST|APOSTOLIC|FULL GOSPEL|"
                    r"CHURCH OF GOD\b|VINEYARD"),
    ("adventist", r"ADVENTIST"),
    ("other_named_protestant", r"CONGREGATIONAL|UNITED CHURCH OF CHRIST|\bUCC\b|MENNONITE|BRETHREN|EVANGELICAL FREE|"
                               r"EVANGELICAL COVENANT|CHRISTIAN AND MISSIONARY|CHRISTIAN & MISSIONARY|DISCIPLES OF CHRIST|"
                               r"CHURCH OF CHRIST|CHURCHES OF CHRIST|CALVARY CHAPEL|MORAVIAN|QUAKER|FRIENDS MEETING|"
                               r"SALVATION ARMY|COVENANT CHURCH|BIBLE CHURCH|CHRISTIAN CHURCH|MISSIONARY ALLIANCE"),
    ("unitarian", r"UNITARIAN"),
    ("other_faith", r"BUDDHI|HINDU|\bSIKH|GURDWARA|\bJAIN|ZEN |VEDANTA|TEMPLE OF|BAHA"),
    ("other_christian_generic", r"CHURCH|CHAPEL|MINISTR|FELLOWSHIP|CHRIST|GOSPEL|BIBLE|JESUS|MISSION|EVANGEL|"
                                r"TABERNACLE|WORSHIP|KINGDOM|GRACE|FAITH|COMMUNITY CHURCH"),
    ("other_ambiguous", r"TEMPLE|CONGREGATION|SANCTUARY|SPIRITUAL|RELIGIOUS|MONASTERY|ABBEY|CONVENT|SISTERS"),
)
FAMILY_RX = tuple((f, re.compile(p)) for f, p in FAMILIES)
NTEE_FAMILY = {"X22": "roman_catholic", "X30": "jewish", "X40": "muslim", "X50": "other_faith", "X70": "other_faith"}
STOP = frozenset("THE INC INCORPORATED OF A AN AND CORP CORPORATION CHURCH CHURCHES MINISTRIES MINISTRY CO".split())
SRC = ("Dollars: top-50 DAFRC sponsors' IRS Form 990 Schedule I Part II lines FY2023-24, net of DAF-to-DAF, "
       "DAF-weighted (scripts/mission_recipient_basis_eligibility.py). Church status, GROUP, AFFILIATION, NTEE_CD, STATE: "
       "IRS EO BMF (www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf; field "
       "codes www.irs.gov/pub/foia/ig/tege/eo-info.pdf). Megachurch list: outreach100.com/largest-churches-in-america/"
       "2023 and /2024.")
FIELDS = ("section", "key", "label", "detail", "recipients", "lines", "usd_daf_weighted", "usd_schedule_i",
          "share_of_block_dw", "cum_share_of_block_dw", "value", "note", "source")


# ----------------------------------------------------------------------------- I/O helpers
def load_bmf_rows(bmf_dir: str, keep) -> tuple[dict, ...]:
    """Every BMF row for which keep(row) is true, with the fields this profile uses."""
    def rows(f):
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple({"ein": ein9(r["EIN"]), "name": (r.get("NAME") or "").strip(), "city": (r.get("CITY") or "").strip(),
                          "state": (r.get("STATE") or "").strip(), "group": (r.get("GROUP") or "").strip(),
                          "affiliation": (r.get("AFFILIATION") or "").strip(), "ntee": (r.get("NTEE_CD") or "").strip().upper(),
                          "foundation": (r.get("FOUNDATION") or "").strip(), "ruling": (r.get("RULING") or "").strip(),
                          "filing_req": (r.get("FILING_REQ_CD") or "").strip(), "subsection": (r.get("SUBSECTION") or "").strip()}
                         for r in csv.DictReader(fh) if keep(r))
    return tuple(x for f in BMF_FILES for x in rows(f))


def robots_ok(url: str) -> tuple[bool, str]:
    host = url.split("/")[2]
    rp = urllib.robotparser.RobotFileParser()
    try:
        req = urllib.request.Request(f"https://{host}/robots.txt", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            rp.parse(r.read().decode("utf-8", "replace").splitlines())
        return rp.can_fetch(UA, url), "robots 200"
    except urllib.error.HTTPError as e:
        return (e.code in (404, 410)), f"robots {e.code}"
    except Exception as e:  # noqa: BLE001
        return False, f"robots error {type(e).__name__}"


def fetch_outreach(d: str, years: Sequence[int], pages: int = OUTREACH_PAGES) -> tuple[dict, ...]:
    """Fetch each year's ranked list, 20 churches per page, after a robots.txt check; one request per second."""
    os.makedirs(d, exist_ok=True)

    def one(y, p):
        url = OUTREACH_URL.format(y=y) + (f"?page={p}" if p > 1 else "")
        ok, why = robots_ok(url)
        if not ok:
            return {"url": url, "status": "robots_blocked", "robots": why}
        time.sleep(1)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=40) as r:
            body = r.read()
        with open(os.path.join(d, f"outreach100-{y}-p{p}.html"), "wb") as fh:
            fh.write(body)
        return {"url": url, "status": "ok", "robots": why, "bytes": len(body)}
    return tuple(one(y, p) for y in years for p in range(1, pages + 1))


def read_outreach(d: str, years: Sequence[int], pages: int = OUTREACH_PAGES) -> dict:
    def one(y, p):
        f = os.path.join(d, f"outreach100-{y}-p{p}.html")
        if not os.path.exists(f):
            return ()
        with open(f, encoding="utf-8", errors="replace") as fh:
            return parse_outreach(fh.read(), y)
    return {y: tuple({(r["rank"], r["name"]): r for p in range(1, pages + 1) for r in one(y, p)}.values()) for y in years}


# ----------------------------------------------------------------------------- pure: parsing and classification
def page_text(raw: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    return "\n".join(x.strip() for x in t.split("\n") if x.strip())


ROW_RX = re.compile(r"(?m)^(\d{1,3})\n(.+)\n(.+?), ([A-Z]{2})\n(?:- .*\n)?(?:●.*\n)+Attendance\n([\d,]+)")


def parse_outreach(raw: str, year: int) -> tuple[dict, ...]:
    """Ranked rows: rank, name, city, state, attendance."""
    return tuple({"year": year, "rank": int(m.group(1)), "name": m.group(2).strip(), "city": m.group(3).strip(),
                  "state": m.group(4), "attendance": int(m.group(5).replace(",", ""))}
                 for m in ROW_RX.finditer(page_text(raw)))


def norm_tokens(name: str) -> frozenset:
    s = re.sub(r"\(.*?\)", " ", name.upper().replace("&", " AND ").replace(".", " ").replace("'", ""))
    return frozenset(t for t in re.findall(r"[A-Z0-9]+", s) if t not in STOP)


def family_of(name: str) -> str:
    u = name.upper()
    return next((f for f, rx in FAMILY_RX if rx.search(u)), "unclassified")


def centrals_by_gen(rows: Sequence[Mapping]) -> dict:
    """GEN -> central organisation (AFFILIATION 8 church central preferred, then 6)."""
    by = _group_by_fast((r for r in rows if r["affiliation"] in ("6", "8") and r["group"] not in ("", "0000")),
                        lambda r: r["group"])
    return {g: sorted(v, key=lambda r: (r["affiliation"] != "8", r["ein"]))[0] for g, v in by.items()}


def denomination(b: Mapping, centrals: Mapping) -> dict:
    gen = b["group"] if b["group"] not in ("", "0000") else ""
    c = centrals.get(gen) if gen else None
    via_gen = family_of(c["name"]) if c else "unclassified"
    via_ntee = NTEE_FAMILY.get(b["ntee"][:3], "")
    via_name = family_of(b["name"])
    fam, how = ((via_gen, "gen_central_name") if via_gen not in ("unclassified", "other_christian_generic", "other_ambiguous")
                else (via_ntee, "ntee_x_code") if via_ntee
                else (via_name, "own_name") if via_name not in ("unclassified",)
                else (via_gen, "gen_central_name") if c else ("unclassified", "none"))
    return {"gen": gen, "gen_central": c["name"] if c else ("(GEN without central in BMF)" if gen else ""),
            "gen_central_ein": c["ein"] if c else "", "family": fam, "family_method": how}


def sponsor_group(e: str, panel: Mapping) -> str:
    if e in FAITH_CHRISTIAN:
        return "faith_christian"
    if e in FAITH_JEWISH:
        return "faith_jewish"
    seg = panel[e]["segment"]
    return {"national": "national", "community_foundation": "community_foundation"}.get(seg, "other")


# Recipient type from the BMF name, tested in order (first match wins). FOUNDATION 10 covers more than congregations:
# the IRS code is "Church 170(b)(1)(A)(i)", which also takes in conventions or associations of churches, church
# schools and integrated auxiliaries. A strict or loose Outreach 100 match overrides to `congregation`.
RTYPES = (
    ("school_or_seminary", r"SCHOOL|ACADEMY|YESHIV|SEMINARY|KOLLEL|MESIVTA|TALMUD|\bPREP\b|BAIS YAAKOV|BETH JACOB|"
                           r"BAIS MEDRASH|BETH MEDRASH|CHEDER|DAY CARE|PRESCHOOL"),
    ("denominational_body", r"DIOCESE|ARCHDIOCESE|ARCHBISHOP|\bBISHOP|CONFERENCE|CONVENTION|SYNOD|PRESBYTERY|"
                            r"ASSOCIATION|UNION OF|COUNCIL|GENERAL ASSEMBLY|HEADQUARTERS|TERRITOR|"
                            r"DISTRICT|PROVINCE|ECCLESIASTICAL|CORPORATION SOLE|\bLATTER[ -]DAY"),
    ("congregation", r"CHURCH|PARISH|CONGREGATION|SYNAGOGUE|\bTEMPLE|MASJID|MOSQUE|CHAPEL|TABERNACLE|\bSHUL\b|"
                     r"CATHEDRAL|BASILICA|\bCONG\b|ANSHE|BETH |\bBNAI|B NAI|AHAVAS|AHAVATH|EMANU|SHAAR|ISLAMIC CENTER|"
                     r"GURDWARA|MANDIR|\bKEHIL|MINYAN|FELLOWSHIP\b|ASSEMBLY\b|MEETING HOUSE|FRIENDS MEETING|IGLESIA|"
                     r"TEMPLO|IGREJA|EGLISE|WORSHIP CENTER|HOUSE OF PRAYER|GATHERING"),
    ("school_or_seminary", r"COLLEGE|UNIVERSITY|INSTITUTE"),
    ("ministry_or_order", r"MINISTR|CRUSADE|MISSION|FOUNDATION|INTERNATIONAL|TRANSLATORS|SOCIETY|NAVIGATORS|"
                          r"SALVATION ARMY|\bORDER\b|FATHERS|SISTERS|BROTHERS|MONASTERY|ABBEY|PRIORY|CONVENT|"
                          r"LEGION|CAMPUS|OUTREACH|RADIO|MEDIA|FUND\b|CHARIT|CHESED|CHASODIM|CHASDEI|GEMILU|TZEDAK|"
                          r"\bRELIEF|PUBLISH|BIBLE|GOSPEL|FAMILY|CENTER|CENTRE|HOUSE"),
)
RTYPE_RX = tuple((t, re.compile(p)) for t, p in RTYPES)


def rtype_of(name: str, megachurch: bool) -> str:
    u = name.upper()
    return "congregation" if megachurch else next((t for t, rx in RTYPE_RX if rx.search(u)), "unclassified")


def size_band(v: float) -> str:
    return next(b for lo, hi, b in SIZE_BANDS if lo <= v < hi)


def lorenz(vals_desc: Sequence[float]) -> dict:
    """Top-k shares and Gini from values sorted descending."""
    n, tot = len(vals_desc), sum(vals_desc)
    asc = sorted(vals_desc)
    gini = (2 * sum((i + 1) * v for i, v in enumerate(asc)) / (n * tot) - (n + 1) / n) if n and tot else None
    cum = lambda k: sum(vals_desc[:k]) / tot  # noqa: E731
    return {"n": n, "total": tot, "gini": gini,
            "top": {p: cum(max(1, round(n * p))) for p in (0.001, 0.01, 0.05, 0.10, 0.20, 0.50)},
            "topk": {k: cum(k) for k in (1, 10, 100, 1000) if k <= n},
            "bottom": {p: 1 - cum(n - round(n * p)) for p in (0.50, 0.80)}}


def quantiles(vals: Sequence[float], qs=(0.1, 0.25, 0.5, 0.75, 0.9, 0.99)) -> dict:
    s = sorted(vals)
    return {q: s[min(len(s) - 1, int(q * len(s)))] for q in qs} if s else {}


CITY_ABBR = {"MT": "MOUNT", "S": "SOUTH", "N": "NORTH", "E": "EAST", "W": "WEST", "SPGS": "SPRINGS", "BCH": "BEACH",
             "GDNS": "GARDENS", "ST": "SAINT", "FT": "FORT", "HTS": "HEIGHTS", "WDM": "WEST DES MOINES"}
STATE_NAMES = {"AL": "ALABAMA", "AZ": "ARIZONA", "AR": "ARKANSAS", "CA": "CALIFORNIA", "CO": "COLORADO", "FL": "FLORIDA",
               "GA": "GEORGIA", "HI": "HAWAII", "IL": "ILLINOIS", "IN": "INDIANA", "IA": "IOWA", "KS": "KANSAS",
               "KY": "KENTUCKY", "LA": "LOUISIANA", "MD": "MARYLAND", "MI": "MICHIGAN", "MN": "MINNESOTA",
               "MS": "MISSISSIPPI", "MO": "MISSOURI", "NV": "NEVADA", "NJ": "NEW JERSEY", "NM": "NEW MEXICO",
               "NY": "NEW YORK", "NC": "NORTH CAROLINA", "OH": "OHIO", "OK": "OKLAHOMA", "OR": "OREGON",
               "PA": "PENNSYLVANIA", "SC": "SOUTH CAROLINA", "TN": "TENNESSEE", "TX": "TEXAS", "UT": "UTAH",
               "VA": "VIRGINIA", "WA": "WASHINGTON", "WI": "WISCONSIN"}


def norm_city(c: str) -> str:
    return " ".join(" ".join(CITY_ABBR.get(t, t) for t in re.findall(r"[A-Z]+", c.upper())).split())


def match_outreach(out_rows: Sequence[Mapping], cands: Sequence[Mapping]) -> tuple[dict, ...]:
    """Match each Outreach 100 church to BMF recipients with the same state and the same (abbreviation-expanded)
    city whose name contains every list-name token (after stop words).
    tier `strict`: the BMF name adds nothing but COMMUNITY, OF, COUNTY or geography (city or state words);
    tier `loose`: any other superset, e.g. LIFE COVENANT CHURCH for Life.Church (listed for checking, not headline).
    Ties: strict first, then the larger DAF total."""
    by_place = _group_by_fast(cands, lambda c: (c["state"], norm_city(c["city"])))

    def tier(o, c):
        ot = norm_tokens(o["name"])
        if not ot or not ot <= c["tokens"]:
            return ""
        geo = frozenset(re.findall(r"[A-Z]+", norm_city(o["city"]) + " " + STATE_NAMES.get(o["state"], "") + " " + o["state"]))
        return "strict" if (c["tokens"] - ot) <= (geo | {"COMMUNITY", "OF", "COUNTY"}) else "loose"

    def one(o):
        pool = by_place.get((o["state"], norm_city(o["city"])), ())
        hits = tuple((t, c) for c in pool for t in [tier(o, c)] if t)
        best = sorted(hits, key=lambda tc: (tc[0] != "strict", -tc[1]["dw"]))
        return {**o, "match": best[0][1] if best else None, "tier": best[0][0] if best else "", "n_hits": len(hits)}
    return tuple(one(o) for o in out_rows)


# ----------------------------------------------------------------------------- pure: profile rows
def mk(section, key, label="", detail="", recipients="", lines="", dw="", si="", share="", cum="", value="", note=""):
    return {"section": section, "key": key, "label": label, "detail": detail, "recipients": recipients, "lines": lines,
            "usd_daf_weighted": round(dw) if isinstance(dw, float) else dw,
            "usd_schedule_i": round(si) if isinstance(si, float) else si,
            "share_of_block_dw": round(share, 5) if isinstance(share, float) else share,
            "cum_share_of_block_dw": round(cum, 5) if isinstance(cum, float) else cum,
            "value": round(value, 5) if isinstance(value, float) else value, "note": note, "source": SRC}


def grouped(section: str, recs: Sequence[Mapping], key, tot: float, label=lambda k, v: "", detail=lambda k, v: "",
            limit: int | None = None) -> list:
    by = _group_by_fast(recs, key)
    ordered = sorted(by.items(), key=lambda kv: -sum(r["dw"] for r in kv[1]))[:limit]
    return [mk(section, k, label(k, v), detail(k, v), len(v), sum(r["n_lines"] for r in v), sum(r["dw"] for r in v),
               sum(r["si"] for r in v), sum(r["dw"] for r in v) / tot, value=sum(r["dw"] for r in v) / len(v),
               note="value = mean DAF-weighted $ per recipient")
            for k, v in ordered]


def profile(block: Sequence[Mapping], lines: Sequence[Mapping], all_lines_dw: float, panel: Mapping, state_all: Mapping,
            sponsor_all: Mapping, label: str) -> list:
    tot = sum(r["dw"] for r in block)
    vals = sorted((r["dw"] for r in block), reverse=True)
    L = lorenz(vals)
    ranked = sorted(block, key=lambda r: -r["dw"])
    line_dw = [l["dw"] for l in lines]
    q_church, q_line = quantiles(vals), quantiles(line_dw)
    pre = label + ":"
    summary = [
        mk(pre + "summary", "recipients", value=len(block)),
        mk(pre + "summary", "usd_daf_weighted", dw=tot, value=tot),
        mk(pre + "summary", "share_of_all_top50_dw", value=tot / all_lines_dw, note="denominator: all top-50 non-DAF-to-DAF DAF-weighted $ incl. blank-EIN lines"),
        mk(pre + "summary", "schedule_i_lines", value=len(lines)),
        mk(pre + "summary", "gini", value=L["gini"]),
        mk(pre + "summary", "mean_dw_per_church", value=tot / len(block)),
        mk(pre + "summary", "mean_dw_per_line", value=sum(line_dw) / len(line_dw)),
        mk(pre + "summary", "sponsors_per_church_mean", value=sum(r["n_sponsors"] for r in block) / len(block)),
        mk(pre + "summary", "share_churches_one_sponsor", value=sum(r["n_sponsors"] == 1 for r in block) / len(block)),
    ] + [mk(pre + "size_quantile_church", f"p{int(q * 100)}", value=v, note="DAF-weighted $ per church, FY2023-24 combined") for q, v in q_church.items()] \
      + [mk(pre + "size_quantile_line", f"p{int(q * 100)}", value=v, note="DAF-weighted $ per Schedule I line (one sponsor-year's aggregate to one recipient; Schedule I omits recipients at or under $5,000)") for q, v in q_line.items()]
    conc = ([mk(pre + "concentration", f"top_{p * 100:g}pct", detail=f"{max(1, round(L['n'] * p))} churches", value=s, share=s) for p, s in L["top"].items()]
            + [mk(pre + "concentration", f"top_{k}", value=s, share=s) for k, s in L["topk"].items()]
            + [mk(pre + "concentration", f"bottom_{p * 100:g}pct", value=s, share=s) for p, s in L["bottom"].items()])
    pts = [i / 20 for i in range(1, 21)]
    asc = sorted(vals)
    lor = [mk(pre + "lorenz", f"{p:.2f}", detail="cumulative share of churches, smallest first", value=sum(asc[:round(len(asc) * p)]) / tot,
              cum=sum(asc[:round(len(asc) * p)]) / tot) for p in pts]
    cum_top = [sum(r["dw"] for r in ranked[:i + 1]) / tot for i in range(min(50, len(ranked)))]
    top = [mk(pre + "top_recipient", r["ein"], r["name"], f"{r['city']}, {r['state']}; {r['rtype']}; GEN {r['gen'] or '-'}; {r['family']}; "
              f"sponsors {r['n_sponsors']}; top sponsor {r['top_sponsor']}", 1, r["n_lines"], r["dw"], r["si"], r["dw"] / tot, cum_top[i],
              value=r["dw"], note=("Outreach 100 " + r["outreach"]) if r["outreach"] else "")
           for i, r in enumerate(ranked[:50])]
    rtyp = grouped(pre + "recipient_type", block, lambda r: r["rtype"], tot)
    rt_sg = [mk(pre + "rtype_x_sponsor_group", f"{t}|{g}", dw=v, share=v / tot, value=v / sum(r["dw"] for r in block if r["rtype"] == t),
                note="value = share of this recipient type's DAF-weighted $ sent by this sponsor group")
             for t in sorted({r["rtype"] for r in block})
             for g in ("faith_christian", "faith_jewish", "national", "community_foundation", "other")
             for v in [sum(l["dw"] for l in lines if l["rtype"] == t and l["group"] == g)] if v]
    fam = grouped(pre + "denomination_family", block, lambda r: r["family"], tot)
    fam_m = grouped(pre + "denomination_method", block, lambda r: r["family_method"], tot)
    gen = grouped(pre + "gen", block, lambda r: r["gen"] or "(none)", tot,
                  label=lambda k, v: v[0]["gen_central"] if k != "(none)" else "no group exemption number",
                  detail=lambda k, v: (f"central EIN {v[0]['gen_central_ein']}; family {v[0]['family'] if k != '(none)' else '-'}"), limit=40)
    gen_cov = [mk(pre + "gen_coverage", k, value=v) for k, v in (
        ("share_dw_with_gen", sum(r["dw"] for r in block if r["gen"]) / tot),
        ("share_recipients_with_gen", sum(1 for r in block if r["gen"]) / len(block)),
        ("share_dw_gen_central_resolved", sum(r["dw"] for r in block if r["gen_central_ein"]) / tot),
        ("distinct_gens", len({r["gen"] for r in block if r["gen"]})),
        ("share_dw_ntee_x", sum(r["dw"] for r in block if r["ntee"].startswith("X")) / tot),
        ("share_dw_ntee_blank", sum(r["dw"] for r in block if not r["ntee"]) / tot))]
    ntee = grouped(pre + "ntee", block, lambda r: r["ntee"][:3] or "(blank)", tot, limit=15)
    size = sorted(grouped(pre + "size_band", block, lambda r: size_band(r["dw"]), tot), key=lambda r: r["key"])
    size = [{**r, "cum_share_of_block_dw": round(sum(x["share_of_block_dw"] for x in size[:i + 1]), 5)} for i, r in enumerate(size)]
    states = grouped(pre + "state", block, lambda r: r["state"] or "(blank)", tot,
                     detail=lambda k, v: f"state share of all top-50 DAF-weighted $ (named EINs in BMF): {state_all.get(k, 0):.4f}")
    by_sp = _group_by_fast(lines, lambda l: l["sponsor"])
    sp = sorted(({"e": e, "dw": sum(l["dw"] for l in v), "si": sum(l["si"] for l in v), "n": len({l["rec"] for l in v}), "lines": len(v)}
                 for e, v in by_sp.items()), key=lambda d: -d["dw"])
    spon = [mk(pre + "sponsor", d["e"], panel[d["e"]]["name"], sponsor_group(d["e"], panel), d["n"], d["lines"], d["dw"], d["si"], d["dw"] / tot,
               value=(d["dw"] / sponsor_all[d["e"]]) if sponsor_all[d["e"]] else "", note="value = share of this sponsor's own top-50-frame DAF-weighted $ that goes to this block")
            for d in sp]
    by_g = _group_by_fast(sp, lambda d: sponsor_group(d["e"], panel))
    gtot = {g: sum(sponsor_all[e] for e in sponsor_all if sponsor_group(e, panel) == g) for g in by_g}
    alltot = sum(sponsor_all.values())
    spg = [mk(pre + "sponsor_group", g, ", ".join(sorted(panel[d["e"]]["name"][:28] for d in v)[:8]),
              f"group share of all top-50 DAF-weighted $: {gtot[g] / alltot:.4f}", len({l['rec'] for d in v for l in by_sp[d['e']]}),
              sum(d["lines"] for d in v), sum(d["dw"] for d in v), sum(d["si"] for d in v), sum(d["dw"] for d in v) / tot,
              value=(sum(d["dw"] for d in v) / gtot[g]) if gtot[g] else "", note="value = share of the group's own DAF-weighted $ that goes to this block")
           for g, v in sorted(by_g.items(), key=lambda kv: -sum(d["dw"] for d in kv[1]))]
    tiers = [("outreach100_matched_strict", lambda r: r["outreach_strict"]),
             ("outreach100_matched_strict_or_loose", lambda r: bool(r["outreach"])), ("dw_ge_1m", lambda r: r["dw"] >= 1e6),
             ("dw_ge_250k", lambda r: r["dw"] >= 2.5e5), ("top_100_by_dw", lambda r: r["ein"] in top100),
             ("top_100_ex_lds", lambda r: r["ein"] in top100x)]
    top100 = frozenset(r["ein"] for r in ranked[:100])
    top100x = frozenset(r["ein"] for r in [x for x in ranked if x["ein"] != LDS][:100])
    mega = [mk(pre + "megachurch", k, recipients=len(s), dw=sum(r["dw"] for r in s), si=sum(r["si"] for r in s),
               share=sum(r["dw"] for r in s) / tot, value=sum(r["dw"] for r in s) / tot)
            for k, f in tiers for s in [tuple(r for r in block if f(r))]]
    fam_by_sg = [mk(pre + "family_x_sponsor_group", f"{fm}|{g}", dw=v, share=v / tot, value=v / sum(r["dw"] for r in block if r["family"] == fm),
                     note="value = share of this family's DAF-weighted $ sent by this sponsor group")
                 for fm in sorted({r["family"] for r in block})
                 for g in ("faith_christian", "faith_jewish", "national", "community_foundation", "other")
                 for v in [sum(l["dw"] for l in lines if l["family"] == fm and l["group"] == g)] if v]
    return summary + conc + lor + top + rtyp + rt_sg + fam + fam_m + gen_cov + gen + ntee + size + states + spon + spg + mega + fam_by_sg


def seeded_sample(block: Sequence[Mapping], n: int, seed: int) -> tuple[dict, ...]:
    """Dollar-stratified seeded sample of congregations: n/2 from the top decile by DAF $, n/2 from the rest."""
    ranked = sorted(block, key=lambda r: (-r["dw"], r["ein"]))
    k = max(1, len(ranked) // 10)
    rng = random.Random(seed)
    top, rest = sorted(ranked[:k], key=lambda r: r["ein"]), sorted(ranked[k:], key=lambda r: r["ein"])
    return tuple({**r, "stratum": s} for s, pool in (("top_decile", top), ("rest", rest))
                 for r in rng.sample(pool, min(n // 2, len(pool))))


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True)
    ap.add_argument("--outreach-dir", required=True)
    ap.add_argument("--fetch-outreach", action="store_true")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--sample-out", default="", help="write the seeded 50-congregation sample (JSON) here")
    ap.add_argument("--sample-n", type=int, default=50)
    ap.add_argument("--dump-block", default="", help="write every block recipient (CSV, for audit) here")
    a = ap.parse_args(argv)

    fetchlog = fetch_outreach(a.outreach_dir, OUTREACH_YEARS) if a.fetch_outreach else ()
    N = build_numerator(a)
    panel, nums, ann, wts = N["panel"], N["nums"], N["ann"], N["weights"]
    bmf = load_bmf(a.bmf_dir, frozenset(nums))
    extra = load_bmf_extra(a.bmf_dir, frozenset(bmf))
    hist = load_history(a.index_dir, frozenset(nums))
    units = units_b(nums, {}, bmf, extra, hist, panel)
    reason = {u["key"]: u["reason"] for u in units}
    flat = tuple({"rec": r["ein"], "sponsor": k[0], "fy": k[1], "si": r["amount"], "dw": r["amount"] * wts.get(k, 1.0)}
                 for k, rs in ann.items() for r in rs if not r["d2d"] and r["amount"] > 0)
    all_dw = sum(l["dw"] for l in flat)
    named = tuple(l for l in flat if l["rec"])
    church_eins = frozenset(e for e, b in bmf.items() if b["foundation"] == "10")
    rows_bmf = load_bmf_rows(a.bmf_dir, lambda r: (r.get("AFFILIATION") or "").strip() in ("6", "8")
                             or ein9(r["EIN"]) in church_eins)
    centrals = centrals_by_gen(rows_bmf)
    info = {r["ein"]: r for r in rows_bmf if r["ein"] in church_eins}
    state_tot = _group_by_fast((l for l in named if l["rec"] in bmf), lambda l: bmf[l["rec"]]["state"])
    named_bmf_dw = sum(l["dw"] for l in named if l["rec"] in bmf)
    state_all = {s: sum(l["dw"] for l in v) / named_bmf_dw for s, v in state_tot.items()}
    sponsor_all = {e: sum(l["dw"] for l in v) for e, v in _group_by_fast(flat, lambda l: l["sponsor"]).items()}

    outreach = read_outreach(a.outreach_dir, OUTREACH_YEARS)
    out_rows = tuple(r for y in OUTREACH_YEARS for r in outreach[y])

    def recs(eins: frozenset) -> tuple:
        ls = tuple(l for l in named if l["rec"] in eins)
        by = _group_by_fast(ls, lambda l: l["rec"])

        def one(e, v):
            b = info[e]
            d = denomination(b, centrals)
            sp = _group_by_fast(v, lambda l: l["sponsor"])
            top_sp = max(sp, key=lambda s: sum(l["dw"] for l in sp[s]))
            return {**b, **d, "dw": sum(l["dw"] for l in v), "si": sum(l["si"] for l in v), "n_lines": len(v),
                    "n_sponsors": len(sp), "top_sponsor": panel[top_sp]["name"][:30], "tokens": norm_tokens(b["name"]),
                    "reason": reason.get(e, "")}
        rs = tuple(one(e, v) for e, v in by.items())
        m = match_outreach(out_rows, rs)
        tag = {e: [f"{x['year']} #{x['rank']} ({x['tier']})" for x in v]
               for e, v in _group_by_fast((x for x in m if x["match"]), lambda x: x["match"]["ein"]).items()}
        rs2 = tuple({**r, "outreach": "; ".join(tag.get(r["ein"], [])),
                     "outreach_strict": any("strict" in t for t in tag.get(r["ein"], [])),
                     "rtype": rtype_of(r["name"], r["ein"] in tag)} for r in rs)
        fam = {r["ein"]: (r["family"], r["rtype"]) for r in rs2}
        ls2 = tuple({**l, "family": fam[l["rec"]][0], "rtype": fam[l["rec"]][1], "group": sponsor_group(l["sponsor"], panel)}
                    for l in ls)
        return rs2, ls2, m

    block_eins = frozenset(e for e in church_eins if reason.get(e) == BLOCK)
    blk, blk_lines, blk_match = recs(block_eins)
    allc, allc_lines, allc_match = recs(church_eins)
    rows = (profile(blk, blk_lines, all_dw, panel, state_all, sponsor_all, "block")
            + profile(tuple(r for r in blk if r["rtype"] == "congregation"),
                      tuple(l for l in blk_lines if l["rtype"] == "congregation"), all_dw, panel, state_all, sponsor_all,
                      "block_congregations")
            + profile(allc, allc_lines, all_dw, panel, state_all, sponsor_all, "church_coded_all"))
    match_rows = [mk("block:outreach100_match", f"{x['year']}#{x['rank']}", x["name"], f"{x['city']}, {x['state']}; attendance {x['attendance']}",
                     1 if x["match"] else 0, dw=x["match"]["dw"] if x["match"] else 0.0,
                     value=x["match"]["ein"] if x["match"] else "",
                     note=(f"{x['tier']}: matched BMF {x['match']['name']} ({x['match']['city']}); hits {x['n_hits']}"
                           if x["match"] else "no block match"))
                  for x in blk_match]
    allc_m = {(x["year"], x["rank"]): x for x in allc_match}
    match_rows_all = [mk("church_coded_all:outreach100_match", f"{x['year']}#{x['rank']}", x["name"], f"{x['city']}, {x['state']}",
                         1 if x["match"] else 0, dw=x["match"]["dw"] if x["match"] else 0.0, value=x["match"]["ein"] if x["match"] else "",
                         note=(f"{x['tier']}: matched BMF {x['match']['name']} ({x['match']['city']}); reason {x['match']['reason']}" if x["match"] else "no match"))
                      for x in allc_m.values()]
    write_csv(a.out, rows + match_rows + match_rows_all, FIELDS)

    if a.dump_block:
        write_csv(a.dump_block, sorted(blk, key=lambda r: -r["dw"]), ("ein", "name", "city", "state", "rtype", "family",
                  "family_method", "gen", "gen_central", "ntee", "dw", "si", "n_lines", "n_sponsors", "top_sponsor", "outreach"))
    if a.sample_out:
        smp = seeded_sample(tuple(r for r in blk if r["rtype"] == "congregation"), a.sample_n, SEED)
        with open(a.sample_out, "w", encoding="utf-8") as fh:
            json.dump([{k: r[k] for k in ("ein", "name", "city", "state", "dw", "family", "gen", "gen_central", "rtype", "stratum", "outreach")} for r in smp], fh, indent=1)

    check = {"block_recipients": len(blk), "block_dw": round(sum(r["dw"] for r in blk)),
             "block_share_all": sum(r["dw"] for r in blk) / all_dw, "all_dw": round(all_dw),
             "church_coded_all_recipients": len(allc), "church_coded_all_dw": round(sum(r["dw"] for r in allc)),
             "church_coded_reason_mix": {k: (len(v), round(sum(r["dw"] for r in v))) for k, v in _group_by_fast(allc, lambda r: r["reason"]).items()},
             "outreach_rows": {y: len(v) for y, v in outreach.items()},
             "outreach_matched_block": {t: sum(1 for x in blk_match if x["tier"] == t) for t in ("strict", "loose")},
             "outreach_distinct_eins_block": {t: len({x["match"]["ein"] for x in blk_match if x["tier"] == t}) for t in ("strict", "loose")},
             "outreach_matched_church_coded": {t: sum(1 for x in allc_match if x["tier"] == t) for t in ("strict", "loose")},
             "centrals": len(centrals), "fetchlog": fetchlog}
    print(json.dumps(check, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
