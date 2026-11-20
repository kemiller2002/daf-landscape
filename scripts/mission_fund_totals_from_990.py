#!/usr/bin/env python3
"""P-B45N33-02-01-01: all-fund totals from Form 990 narratives across the whole tail-CF frame, and allocation rule F.
Task id b45n33-02-01-01.

Stdlib only; functional style (pure transforms; I/O only at the edges: CSV/XML reads, the CSV write, and the optional
mirror fetch). Reuses, without modifying them:
  * scripts/mission_tail_cf_fund_counts.py (b45n33-02-01): frame(), robots-checked get()/cached() (all six agents),
    quantiles/qfmt/boot_ci/table helpers, the XML URL template.
  * scripts/mission_long_tail_fee_census.py (via the module above): read_csv, write_csv, num.

Frame
  The 641 tail CFs of long-tail-operating-cost-2026-11-19.csv (group == tail_cf). Bands: $10-50m (t10_50), $1-10m (t1_10),
  under $1m (t0_1 + zero), as in b45n33-02-01.

Returns
  Every FY2022-FY2024 return of those EINs listed in form990-returns-schedule-d-harvest-full.csv or
  sponsor-cost-structure.csv (object ids). One return per EIN-FY: the latest return_ts (as the cost note does).
  XML is read from local caches of the GivingTuesday mirror of IRS e-file XML (--xml-dir: directories of
  {object_id}.xml; --json-cache: directories of get()-style p_<key>.json records). Anything not cached is fetched from
  the mirror only with --fetch, through get() (robots.txt checked for research-script/1.0 and every Claude/anthropic
  agent; logged to <cache>/robots_log.tsv).

Text searched
  Part III: IRS990/MissionDesc (line 1), IRS990/Desc (line 4a), ProgSrvcAccomActy2Grp/Desc, ProgSrvcAccomActy3Grp/Desc,
  ProgSrvcAccomActyOtherGrp/Desc (4b-4d). Schedule O: IRS990ScheduleO/SupplementalInformationDetail/ExplanationTxt.
  Schedule D line 1 column (a) DonorAdvisedFundsHeldCnt is read from the same XML.

Extraction (regex, then rule-based scope classes; see classify())
  Pattern P1 "<qualifier?> N<+?> <0-3 adjectives> funds" and P2 "total (number of)? (active)? funds (under
  management)? to N" / "total under management to N". Each hit is classed:
    all_funds        total of all component funds (used for rule F)
    endowment_only   endowed / endowment funds, or "endowment consists of N funds" (audit-note boilerplate)
    type_specific    a fund-type word among the adjectives or just before (DAF, scholarship, agency, designated, ...)
    new_funds        new / newly established funds this year
    grantmaking      funds that made grants / "grants ... from N funds" / "funds that award"
    other            money, years, financial-statement lines, n < 2 or n > 5,000
  Qualifiers: over / more than / in excess of / "+" -> lower_bound; approximately / about / roughly -> approx;
  nearly / almost / up to -> upper_bound; none -> stated.
  Per return the all_funds total is the largest all_funds hit (flag multi_total when hits differ).
  Per CF: the latest FY (2024, else 2023, else 2022) with an all_funds total, paired with the Schedule D DAF count
  OF THE SAME RETURN (same period, unlike b45n33-02-01, where totals were 2021-2026 and DAF counts FY2024).

Hand check (HANDCHECK below): every CF-level total that feeds rule F was read in context by the analyst and judged
  ok (a statement of the number of all funds the filer holds/administers), or not (with a reason). Precision = ok / n.
  A random sample (seed 2026112002) of hits classed as non-all_funds is also read, to estimate missed totals.

Rule F (same definition as b45n33-02-01): DAF cost = opex_ex_11f (FY2024, cost file) x min(1, DAF funds / all funds);
  per account = / screened DAF accounts; per DAF dollar = / FY2024 DAF assets (bps). Rules A and G are taken from the
  cost file for the same CFs. All allocated figures are inferences [I].

Usage
  python3 -I scripts/mission_fund_totals_from_990.py . --xml-dir DIR [--xml-dir DIR ...] [--json-cache DIR ...]
        [--cache-dir CACHE --fetch] [--task build|hits|sample]
Outputs
  data/mission-2026-11-14/fund-totals-from-990-2026-11-20.csv (one row per tail CF; counts only, no names of funds or
  donors); stdout: the markdown tables used in research/mission-2026-11-14/b45n33-02-01-01-fund-totals-from-990.md
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import random
import re
import statistics
import sys
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Mapping, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name: str, fname: str):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


M = _load("tail_cf_fund_counts", "mission_tail_cf_fund_counts.py")
B = M.B
DATA = "data/mission-2026-11-14"
COST_CSV = f"{DATA}/long-tail-operating-cost-2026-11-19.csv"
HARVEST_CSV = f"{DATA}/form990-returns-schedule-d-harvest-full.csv"
COSTSTRUCT_CSV = f"{DATA}/sponsor-cost-structure.csv"
PRIOR_CSV = f"{DATA}/tail-cf-fund-counts-2026-11-20.csv"
OUT_CSV = f"{DATA}/fund-totals-from-990-2026-11-20.csv"
FYS = ("2024", "2023", "2022")
BANDS = (("$10–50m", ("t10_50",)), ("$1–10m", ("t1_10",)), ("Under $1m", ("t0_1", "zero")))
SAMPLE_SEED = 2026112002
num = B.num

PART_III_TAGS = ("MissionDesc", "Desc")
SCHED_O = "IRS990ScheduleO"

QUAL = r"(?P<qual>over|more than|in excess of|nearly|almost|approximately|approx\.?|about|roughly|up to|the approximate|some)?"
NUM = r"(?P<n>\d{1,3}(?:,\d{3})+|\d+)(?P<plus>\+)?"
P1 = re.compile(rf"(?i)(?<![\d$,.%])(?:{QUAL}\s+)?{NUM}\s+(?P<mods>(?:[a-z][a-z'-]*\s+){{0,3}}?)funds\b")
P2 = (re.compile(rf"(?i)\btotal\s+(?:number\s+of\s+)?(?:active\s+|charitable\s+)?funds\s+(?:under\s+management\s+)?"
                 rf"(?:to|of|is|was|:)\s+{QUAL}\s*{NUM}"),
      re.compile(rf"(?i)\btotal\s+under\s+management\s+to\s+{QUAL}\s*{NUM}(?![\d,.]*\s*million)"))
ALLOWED_MODS = frozenset("""individual charitable component different separate separately identifiable named active
philanthropic unique distinct current total permanent endowed endowment endowments new newly established donor donor-advised
advised designated donor-designated scholarship scholarships agency field-of-interest field of interest unrestricted
custodial fiscal partner special pass-through pass through discretionary temporary donor-directed directed nonprofit
non-profit organizational memorial affiliate restricted non-endowed quasi-endowed corporate miscellaneous fellowship
and named-scholarship""".split())
TYPE_WORDS = re.compile(r"(?i)\b(donor[- ]?advised|advised|designated|scholarships?|agency|field[- ]of[- ]interest|"
                        r"unrestricted|custodial|fiscal|partner|special|pass[- ]?through|discretionary|temporary|"
                        r"donor[- ]directed|nonprofit|non-profit|organizational|memorial|affiliate|restricted|"
                        r"non-endowed|quasi-endowed|corporate|miscellaneous|fellowship)\b")
ENDOW_WORDS = re.compile(r"(?i)\b(endow\w*|permanent)\b")
ENDOW_CTX = re.compile(r"(?i)endowment (net assets )?consists? of|deemed as endowment|as endowment funds|endowment funds of|"
                       r"held on donor'?s behalf|beneficiaries were designated")
TYPE_TOTAL_BEFORE = re.compile(r"(?i)\b(donor[- ]?advised|designated|scholarships?|agency|field[- ]of[- ]interest|endow\w*|"
                               r"custodial|fiscal|partner)\s+funds\b[^.;]{0,70}\(\s*(?:a\s+)?total\s+of\s*$")
ITEM = re.compile(r"(?i)(?<![\d$,.])(?P<n>\d{1,3}(?:,\d{3})*)\s+(?:[a-z][a-z'-]*\s+){1,3}?funds?\b")
SEP = re.compile(r"(?i)\s*,?\s*(?:and|&)?\s*")
SPELLED = re.compile(r"(?i)\b(?:two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|"
                     r"eighty|ninety|hundred|thousand)\b[\w\s,-]{0,40}?\bfunds\b")
NEW_CTX = re.compile(r"(?i)\b(new|newly)\b")
GRANT_BEFORE = re.compile(r"(?i)(grant\w*|award\w*|distribution\w*)\b[^.;]{0,80}\b(from|through|to)\s*$")
GRANT_AFTER = re.compile(r"(?i)^\s*(that|which)\s+(award|hosted|made grants|provided grants|paid)")
FIN_AFTER = re.compile(r"(?i)^\s*(held for|transferred|revenue|expenses|were included|totaling \$)")


def clause_before(text: str, start: int, width: int = 90) -> str:
    seg = text[max(0, start - width):start]
    cut = max(seg.rfind("."), seg.rfind(";"), seg.rfind(":"), seg.rfind("("))
    return seg[cut + 1:] if cut >= 0 else seg


def qual_class(qual: str | None, plus: str | None) -> str:
    q = (qual or "").lower()
    return ("lower_bound" if plus or q in ("over", "more than", "in excess of") else
            "approx" if q.startswith("approx") or q in ("about", "roughly", "the approximate", "some") else
            "upper_bound" if q in ("nearly", "almost", "up to") else "stated")


def classify(text: str, m: re.Match, pattern: str) -> dict:
    """Pure: scope class of one regex hit (see module docstring)."""
    n = int(m.group("n").replace(",", ""))
    mods = (m.groupdict().get("mods") or "").lower().split()
    before = clause_before(text, m.start())
    after = text[m.end():m.end() + 60]
    sent_start = max(text.rfind(".", 0, m.start()), text.rfind(";", 0, m.start())) + 1
    sentence = text[sent_start:m.end() + 120]
    is_year = 1990 <= n <= 2030 and not m.group("qual") and not m.group("plus") and "," not in m.group("n")
    cls = ("other" if n < 2 or n > 5000 or is_year or any(w not in ALLOWED_MODS for w in mods) or FIN_AFTER.search(after)
           or re.search(r"(?i)\$\s*$|\bmillion\b", before[-12:])
           else "new_funds" if any(NEW_CTX.fullmatch(w) for w in mods) or "established" in mods
           else "endowment_only" if any(ENDOW_WORDS.fullmatch(w) for w in mods) or ENDOW_CTX.search(sentence)
           else "type_specific" if TYPE_WORDS.search(" ".join(mods)) or TYPE_TOTAL_BEFORE.search(text[max(0, m.start() - 110):m.start()])
           else "grantmaking" if GRANT_BEFORE.search(before) or GRANT_AFTER.search(after)
           else "all_funds")
    return {"n": n, "qual": qual_class(m.group("qual"), m.group("plus")), "cls": cls, "pattern": pattern,
            "snippet": re.sub(r"\s+", " ", text[max(0, m.start() - 100):m.end() + 100]).strip()}


def type_list_sums(text: str) -> tuple[dict, ...]:
    """P3: a run of >= 4 'N <type> fund(s)' items joined only by commas / 'and' / '&' is summed (sum of types)."""
    items = tuple(ITEM.finditer(text))
    runs = reduce(lambda acc, m: (acc[:-1] + ((acc[-1] + (m,)),) if acc and SEP.fullmatch(text[acc[-1][-1].end():m.start()])
                                  else acc + ((m,),)), items, ())
    return tuple({"n": sum(int(m.group("n").replace(",", "")) for m in run), "qual": "sum_of_types", "cls": "all_funds",
                  "pattern": "P3", "snippet": re.sub(r"\s+", " ", text[max(0, run[0].start() - 100):run[-1].end() + 60]).strip()}
                 for run in runs if len(run) >= 4)


def hits_in(text: str) -> tuple[dict, ...]:
    p3 = type_list_sums(text)
    p2 = tuple(classify(text, m, "P2") for rx in P2 for m in rx.finditer(text))
    p1 = tuple(classify(text, m, "P1") for m in P1.finditer(text))
    return p3 + p2 + p1


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def narratives(root) -> tuple[tuple[str, str], ...]:
    """(part, text) for Part III fields, Schedule O explanations and (extension only) Schedule D Part XIII and Schedule A Part VI explanations."""
    irs990 = next((e for e in root.iter() if local(e.tag) == "IRS990"), None)
    sched_o = next((e for e in root.iter() if local(e.tag) == SCHED_O), None)
    sched_d = next((e for e in root.iter() if local(e.tag) == "IRS990ScheduleD"), None)
    sched_a = next((e for e in root.iter() if local(e.tag) == "IRS990ScheduleA"), None)
    p3 = () if irs990 is None else tuple(
        ("part_iii", (e.text or "").strip()) for e in irs990.iter()
        if local(e.tag) in PART_III_TAGS and (e.text or "").strip())
    so = () if sched_o is None else tuple(
        ("sched_o", (e.text or "").strip()) for e in sched_o.iter() if local(e.tag) == "ExplanationTxt" and (e.text or "").strip())
    sd = () if sched_d is None else tuple(
        ("sched_d_xiii", (e.text or "").strip()) for e in sched_d.iter() if local(e.tag) == "ExplanationTxt" and (e.text or "").strip())
    sa = () if sched_a is None else tuple(
        ("sched_a_vi", (e.text or "").strip()) for e in sched_a.iter() if local(e.tag) == "ExplanationTxt" and (e.text or "").strip())
    return p3 + so + sd + sa


def first_text(root, tag: str) -> str | None:
    return next(((e.text or "").strip() for e in root.iter() if local(e.tag) == tag), None)


def parse_return(oid: str, raw: bytes | None) -> dict:
    if not raw:
        return {"oid": oid, "xml": "missing"}
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return {"oid": oid, "xml": "parse_error"}
    texts = narratives(root)
    hits = tuple({**h, "part": part} for part, t in texts for h in hits_in(t))
    uniq = tuple({(h["part"], h["n"], h["cls"], h["snippet"][:120]): h for h in hits}.values())
    spelled = tuple(re.sub(r"\s+", " ", t[max(0, m.start() - 80):m.end() + 60]) for part, t in texts if part in MAIN_PARTS
                    for m in SPELLED.finditer(t))
    return {"oid": oid, "xml": "ok", "period_end": first_text(root, "TaxPeriodEndDt"), "spelled": spelled,
            "daf_cnt": num(first_text(root, "DonorAdvisedFundsHeldCnt")),
            "other_cnt": num(first_text(root, "FundsAndOtherAccountsHeldCnt")),
            "n_narr": sum(1 for p, _ in texts if p in MAIN_PARTS), "n_narr_ext": sum(1 for p, _ in texts if p not in MAIN_PARTS),
            "hits": uniq}


MAIN_PARTS = ("part_iii", "sched_o")
EXT_PARTS = MAIN_PARTS + ("sched_d_xiii", "sched_a_vi")


def return_total(rec: Mapping, parts: Sequence[str] = MAIN_PARTS) -> dict | None:
    alls = tuple(h for h in rec.get("hits", ()) if h["cls"] == "all_funds" and h["part"] in parts)
    if not alls:
        return None
    best = max(alls, key=lambda h: (h["n"], h["pattern"] == "P2"))
    return {**best, "multi_total": len({h["n"] for h in alls}) > 1}


# ----------------------------------------------------------------------------- I/O edge: locating XML
def load_xml(oid: str, xml_dirs: Sequence[str], json_caches: Sequence[str], cache: str | None, fetch: bool) -> bytes | None:
    url = M.XML_URL.format(oid=oid)
    path = next((os.path.join(d, f"{oid}.xml") for d in xml_dirs if os.path.exists(os.path.join(d, f"{oid}.xml"))), None)
    if path:
        with open(path, "rb") as fh:
            return fh.read()
    rec = next((r for r in (M.cached(c, url) for c in tuple(json_caches) + ((cache,) if cache else ())) if r), None)
    rec = rec or (M.get(cache, url) if fetch and cache else None)
    return (rec or {}).get("html", "").encode("utf-8") or None


# ----------------------------------------------------------------------------- returns per EIN-FY
def returns_index(harvest: Sequence[Mapping], coststruct: Sequence[Mapping], eins: frozenset) -> dict:
    """{(ein, fy): oid} keeping the latest return_ts per EIN-FY."""
    rows = tuple((r["ein"], r["fiscal_year"], r["return_object_id"], r.get("return_ts", ""))
                 for r in tuple(harvest) + tuple(coststruct)
                 if r["ein"] in eins and r["fiscal_year"] in FYS and r.get("return_object_id"))
    return {(ein, fy): oid for ein, fy, oid, _ in sorted(rows, key=lambda t: (t[3], t[2]))}


# ----------------------------------------------------------------------------- hand check
# Analyst's reading, in context, of every CF-level total the extraction selects (main and extension), keyed
# "<object id>|<n>". verdict: ok = states the number of all funds the filer holds/administers; corrected = a total of
# all funds, but the right figure differs (corrected_total given); reject = not an all-funds total.
HANDCHECK: dict[str, tuple[str, int | None, str]] = {
    '202540839349300504|950': ('ok', None, "'TFEC HAS 950 FUNDS' (Sched O)"),
    '202512729349300936|472': ('ok', None, "'ADMINISTERS MORE THAN 472 CHARITABLE FUNDS'"),
    '202433169349300703|300': ('ok', None, "'STEWARDS MORE THAN 300 CHARITABLE FUNDS'"),
    '202533109349300818|160': ('ok', None, "'WE CURRENTLY HOLD 160 FUNDS, THE MAJORITY BEING DONOR ADVISED FUNDS'"),
    '202501789349300425|300': ('ok', None, "'MANAGES OVER 300 FUNDS ESTABLISHED FOR CHARITABLE PURPOSES'"),
    '202501919349300600|50': ('ambiguous', None, "'HAS OVER 50 FUNDS FOR CHARITIES': may mean funds held for charities (agency) rather than all funds"),
    '202511339349301401|300': ('ok', None, "'MANAGES 300 CHARITABLE FUNDS AND MADE 873 GRANTS FROM THOSE FUNDS'"),
    '202512799349300406|400': ('ok', None, "'MANAGES OVER 400 FUNDS' (site figures conflict, see b45n33-02-01 sec 1.3)"),
    '202520569349301027|370': ('ok', None, "'MANAGES OVER 370 DIFFERENT FUNDS'"),
    '202512879349302101|370': ('ok', None, "'BRINGING THE TOTAL NUMBER OF FUNDS TO 370'"),
    '202503189349311980|100': ('ok', None, "'WE MANAGE MORE THAN 100 FUNDS'"),
    '202501719349300820|257': ('corrected', 338, "Filer (CF of the Northern Alleghenies) reports two affiliates: Elk County CF 'TOTAL OF 257 CHARITABLE FUNDS' and McKean County CF 'TOTAL OF 81 FUNDS'; Sched D covers the filer, so total = 257 + 81"),
    '202523179349300617|136': ('ok', None, 'Sum of a complete by-type list: 59 agency, 17 endowment, 42 DAF, 7 corporate advised, 3 scholarship, 1 annuity, 7 pass-through'),
    '202502619349300910|80': ('ok', None, "'SUPPORT TO MORE THAN 80 COMPONENT FUNDS'"),
    '202531289349304033|418': ('ok', None, "'WE CURRENTLY HAVE 418 FUNDS THAT WE MANAGE'"),
    '202513149349300616|75': ('ok', None, "'MANAGES MORE THAN 75 FUNDS ESTABLISHED BY INDIVIDUALS, CORPORATIONS, AND ORGANIZATIONS'"),
    '202543189349303749|300': ('ok', None, "'WITHIN THE FOUNDATION ARE MORE THAN 300 INDIVIDUAL CHARITABLE FUNDS'"),
    '202523149349303412|394': ('ok', None, "'ADMINISTERS 394 FUNDS ... ORGANIZATION-SPECIFIC, DONOR DIRECTED, FIELD OF INTEREST'"),
    '202501359349307550|200': ('ok', None, "'ADMINISTERS OVER 200 FUNDS, PRIMARILY PERMANENT ENDOWMENTS, INCLUDING AGENCY OR DESIGNATED, SCHOLARSHIP, DONOR-ADVISED'"),
    '202413199349305696|350': ('ok', None, "Sched A Part VI: 'HOLDS OVER 350 INDIVIDUAL FUNDS REPRESENTING NEW GIFTS, BEQUESTS, ... PASS-THROUGH FUNDS' (extension)"),
    '202542879349301469|150': ('ok', None, "Sched A Part VI: 'HOLDS OVER 150 INDIVIDUAL FUNDS' (extension)"),
    '202543089349302574|486': ('ok', None, "'managed 486 funds established for charitable purposes during 2024' (no Sched D DAF count in that return)"),
    '202502329349301405|166': ('ok', None, "'MANAGED 166 FUNDS IN 2024 INCLUDING 10 NEW FUNDS'"),
    '202501299349302430|871': ('ok', None, "'CURRENTLY HAS 871 COMPONENT FUNDS'"),
    '202542819349300709|330': ('ok', None, "'HAS OVER 330 ACTIVE FUNDS'"),
    '202442819349300614|293': ('ok', None, "'BRINGING THE TOTAL NUMBER OF ACTIVE FUNDS TO 293'"),
    '202340239349301409|372': ('ok', None, "'WE ADMINISTER 372 ACTIVE COMPONENT FUNDS' (FY2022)"),
    '202500379349300640|500': ('ok', None, "'MANAGES OVER 500 FUNDS'"),
    '202543169349300219|169': ('ok', None, "'WE SERVICED 169 FUNDS AND ISSUED 1,622 GRANTS'"),
    '202503099349301115|158': ('ok', None, "'ADMINISTERS DONATED FUNDS FOR APPROXIMATELY 158 DIFFERENT FUNDS'"),
    '202323129349302842|431': ('ok', None, "'MANAGES 431 CHARITABLE FUNDS' (FY2022)"),
    '202402769349301430|235': ('ok', None, "'HAS 235 FUNDS AS OF YEAR END' (FY2023)"),
    '202532759349300223|225': ('ok', None, "'currently administers over 225 charitable funds'"),
    '202422689349300037|100': ('ok', None, "'ADMINISTERS DONATED FUNDS FOR APPROXIMATELY 100 DIFFERENT FUNDS'"),
    '202523019349300037|200': ('ok', None, "'MANAGES OVER 200 CHARITABLE FUNDS FOR INDIVIDUALS, FAMILIES, AND NONPROFIT ORGANIZATIONS'"),
    '202532979349301558|200': ('ok', None, "'MANAGES OVER 200 FUNDS'"),
    '202413109349303851|180': ('ok', None, "'HAS MORE THAN 180 PHILANTHROPIC FUNDS'"),
    '202502249349300445|600': ('ok', None, "Sched D Part XIII: 'FIDUCIARY OVER MORE THAN 600 INDIVIDUAL FUNDS' (extension)"),
    '202501409349301380|175': ('ok', None, "Sched A Part VI: 'HAS OVER 175 SEPARATELY IDENTIFIABLE FUNDS THAT PROVIDE GRANTS' (extension)"),
    '202512069349301001|211': ('ok', None, "'12 NEW FUNDS WERE OPENED, BRINGING THE TOTAL UNDER MANAGEMENT TO 211'"),
}
# Analyst's reading of a random sample of hits classed as NOT all_funds (key "<object id>|<n>"):
# correct_exclusion or missed_total.
EXCL_CHECK: dict[str, tuple[str, str]] = {
    '202313119349304186|35': ('correct_exclusion', 'fund-type count, not a total'),
    '202322879349301007|388603': ('correct_exclusion', 'money, financial line or non-count'),
    '202402439349301500|262435': ('correct_exclusion', 'money, financial line or non-count'),
    '202323199349306867|19': ('correct_exclusion', 'fund-type count, not a total'),
    '202312939349301031|17': ('correct_exclusion', 'funds added this year'),
    '202532769349301103|533': ('correct_exclusion', 'endowment / endowed funds only'),
    '202442609349300959|19': ('correct_exclusion', 'funds that made grants / hosted rounds'),
    '202523159349300227|100': ('correct_exclusion', 'fund-type count, not a total'),
    '202442989349300349|5': ('correct_exclusion', 'money, financial line or non-count'),
    '202322659349301602|39': ('correct_exclusion', 'endowment / endowed funds only'),
    '202403549349300335|16': ('correct_exclusion', 'funds added this year'),
    '202233559349300233|45': ('correct_exclusion', 'fund-type count, not a total'),
    '202311319349305021|90': ('correct_exclusion', 'fund-type count, not a total'),
    '202323119349303022|14': ('correct_exclusion', 'endowment / endowed funds only'),
    '202523079349302892|4': ('correct_exclusion', 'fund-type count, not a total'),
    '202332499349301958|468469': ('correct_exclusion', 'money, financial line or non-count'),
    '202502759349300825|27': ('correct_exclusion', 'funds added this year'),
    '202412129349301756|39': ('correct_exclusion', 'endowment / endowed funds only'),
    '202412849349300201|15': ('correct_exclusion', 'endowment / endowed funds only'),
    '202543189349301989|139': ('correct_exclusion', 'endowment / endowed funds only'),
    '202322229349301957|96': ('correct_exclusion', 'fund-type count, not a total'),
    '202303149349301690|14': ('correct_exclusion', 'funds added this year'),
    '202323199349306867|30': ('correct_exclusion', 'fund-type count, not a total'),
    '202523179349300617|17': ('correct_exclusion', 'endowment / endowed funds only'),
    '202542659349300709|200': ('correct_exclusion', 'endowment / endowed funds only'),
    '202501349349310815|1283': ('correct_exclusion', 'funds that made grants / hosted rounds'),
    '202543189349301689|39': ('correct_exclusion', 'fund-type count, not a total'),
    '202313199349316406|15': ('correct_exclusion', 'fund-type count, not a total'),
    '202333139349303673|99': ('correct_exclusion', 'fund-type count, not a total'),
    '202312969349301711|10': ('correct_exclusion', 'funds added this year'),
    '202323199349311637|0': ('correct_exclusion', 'money, financial line or non-count'),
    '202303199349307615|100': ('correct_exclusion', 'fund-type count, not a total'),
    '202313039349301591|2022': ('correct_exclusion', 'money, financial line or non-count'),
    '202433189349307648|147': ('correct_exclusion', 'fund-type count, not a total'),
    '202342549349301504|6': ('correct_exclusion', 'funds that made grants / hosted rounds'),
    '202412849349300201|37': ('correct_exclusion', 'fund-type count, not a total'),
    '202423189349302002|735584': ('correct_exclusion', 'money, financial line or non-count'),
    '202303129349301850|304': ('correct_exclusion', 'endowment / endowed funds only'),
    '202502249349300445|96': ('correct_exclusion', 'fund-type count, not a total'),
    '202402979349300330|6': ('correct_exclusion', 'funds added this year'),
}


# ----------------------------------------------------------------------------- build
def band_of(r: Mapping) -> str:
    return next(lbl for lbl, bands in BANDS if r["size_band_fy2024"] in bands)


def pick(c: Mapping, loaded: Sequence[tuple[str, Mapping]], parts: Sequence[str], sfx: str = "") -> dict:
    """Latest FY with an all_funds total in `parts`, the same return's Sched D DAF count, and rule F (pure)."""
    with_total = tuple((fy, r, return_total(r, parts)) for fy, r in loaded
                       if r and r.get("xml") == "ok" and return_total(r, parts))
    fy, rec, tot = with_total[0] if with_total else (None, None, None)
    hc = HANDCHECK.get(f"{rec['oid']}|{tot['n']}") if tot else None
    total = (hc[1] if hc and hc[0] == "corrected" else tot["n"]) if tot else None
    daf = rec.get("daf_cnt") if rec else None
    share = None if not (total and daf is not None) else min(1.0, daf / total)
    use_f = bool(share is not None and c["usable"] == "1" and hc is not None and hc[0] in ("ok", "corrected"))
    opex, accts, dafa = num(c["opex_ex_11f"]), num(c["daf_accounts_fy2024_screened"]), num(c["daf_assets_fy2024"])
    cost_f = opex * share if use_f and opex is not None else None
    base = {
        "total_fy": fy or "", "total_object_id": rec["oid"] if rec else "", "total_period_end": (rec or {}).get("period_end") or "",
        "total_part": tot["part"] if tot else "", "total_pattern": tot["pattern"] if tot else "",
        "n_total_funds_extracted": M.fmt(tot["n"], 0) if tot else "", "n_total_funds": M.fmt(total, 0) if total else "",
        "total_qual": tot["qual"] if tot else "", "multi_total": ("1" if tot["multi_total"] else "0") if tot else "",
        "fys_with_total": ";".join(f for f, _, _ in with_total),
        "sched_d_daf_count_same_return": M.fmt(daf, 0) if daf is not None and tot else "",
        "daf_gt_total": ("1" if daf is not None and total and daf > total else "0") if tot else "",
        "handcheck": hc[0] if hc else ("not_checked" if tot else ""),
        "daf_share_F": M.fmt(share, 4) if use_f else "",
        "daf_cost_alloc_F": M.fmt(cost_f, 0) if cost_f is not None else "",
        "daf_cost_per_account_alloc_F": M.fmt(M.ratio(cost_f, accts), 0) if cost_f is not None and accts else "",
        "daf_cost_bps_daf_assets_alloc_F": M.fmt(M.ratio(cost_f, dafa) * 1e4, 1) if cost_f is not None and dafa else "",
        "opex_per_fund": M.fmt(M.ratio(opex, total), 0) if use_f and opex is not None else "",
    }
    return {k + sfx: v for k, v in base.items()} if sfx else base


EXT_KEYS = ("total_fy", "total_object_id", "total_part", "n_total_funds", "total_qual", "sched_d_daf_count_same_return",
            "handcheck", "daf_share_F", "daf_cost_per_account_alloc_F", "daf_cost_bps_daf_assets_alloc_F")


def cf_row(c: Mapping, recs: Mapping[str, Mapping], idx: Mapping, prior: Mapping) -> dict:
    fy_oids = tuple((fy, idx.get((c["ein"], fy))) for fy in FYS)
    loaded = tuple((fy, recs.get(o)) for fy, o in fy_oids if o)
    main = pick(c, loaded, MAIN_PARTS)
    ext = pick(c, loaded, EXT_PARTS, "_ext")
    classes = tuple(h["cls"] for _, r in loaded if r for h in r.get("hits", ()) if h["part"] in MAIN_PARTS)
    p = prior.get(c["ein"], {})
    return {
        "ein": c["ein"], "name": c["name"], "band": band_of(c), "size_band_fy2024": c["size_band_fy2024"],
        "usable_cost": c["usable"], "returns_fy2022_24": sum(1 for _, o in fy_oids if o),
        "returns_xml_ok": sum(1 for _, r in loaded if r and r.get("xml") == "ok"),
        "narrative_fields": sum(r.get("n_narr", 0) for _, r in loaded if r),
        "hits_all_funds": classes.count("all_funds"), "hits_endowment_only": classes.count("endowment_only"),
        "hits_type_specific": classes.count("type_specific"), "hits_new_funds": classes.count("new_funds"),
        "hits_grantmaking": classes.count("grantmaking"), "hits_other": classes.count("other"),
        **main,
        "daf_share_A": c["daf_share_assets"], "daf_share_G": c["daf_share_grants"],
        "opex_ex_11f": c["opex_ex_11f"], "daf_accounts_fy2024_screened": c["daf_accounts_fy2024_screened"],
        "daf_assets_fy2024": c["daf_assets_fy2024"],
        "daf_cost_per_account_alloc_A": c["daf_cost_per_account_alloc_A"], "daf_cost_per_account_alloc_G": c["daf_cost_per_account_alloc_G"],
        "daf_cost_bps_daf_assets_alloc_A": c["daf_cost_bps_daf_assets_alloc_A"], "daf_cost_bps_daf_assets_alloc_G": c["daf_cost_bps_daf_assets_alloc_G"],
        **{k + "_ext": ext[k + "_ext"] for k in EXT_KEYS},
        "prior_02_01_total": p.get("n_total_funds", ""), "prior_02_01_status": p.get("count_status", ""),
    }


FIELDS = ("ein", "name", "band", "size_band_fy2024", "usable_cost", "returns_fy2022_24", "returns_xml_ok", "narrative_fields",
          "hits_all_funds", "hits_endowment_only", "hits_type_specific", "hits_new_funds", "hits_grantmaking", "hits_other",
          "total_fy", "total_object_id", "total_period_end", "total_part", "total_pattern", "n_total_funds_extracted",
          "n_total_funds", "total_qual", "multi_total", "fys_with_total", "sched_d_daf_count_same_return",
          "daf_gt_total", "handcheck", "daf_share_F", "daf_share_A", "daf_share_G", "opex_ex_11f",
          "daf_accounts_fy2024_screened", "daf_assets_fy2024", "daf_cost_alloc_F", "daf_cost_per_account_alloc_F",
          "daf_cost_bps_daf_assets_alloc_F", "opex_per_fund", "daf_cost_per_account_alloc_A", "daf_cost_per_account_alloc_G",
          "daf_cost_bps_daf_assets_alloc_A", "daf_cost_bps_daf_assets_alloc_G") + tuple(k + "_ext" for k in EXT_KEYS) + (
          "prior_02_01_total", "prior_02_01_status")


def col(rows: Sequence[Mapping], k: str) -> list:
    return [num(r[k]) for r in rows if num(r[k]) is not None]


def ci(xs, nd=0, pre=""):
    c = M.boot_ci(xs)
    return "–" if c is None else f"{pre}{c[0]:,.{nd}f}–{pre}{c[1]:,.{nd}f}"


def summary_row(label: str, rs: Sequence[Mapping], sfx: str = "") -> list:
    return [label, len(rs), M.qfmt(col(rs, "daf_share_F" + sfx), 3), M.qfmt(col(rs, "daf_share_A"), 3), M.qfmt(col(rs, "daf_share_G"), 3),
            M.qfmt(col(rs, "daf_cost_per_account_alloc_F" + sfx), 0, "$"), M.qfmt(col(rs, "daf_cost_per_account_alloc_A"), 0, "$"),
            M.qfmt(col(rs, "daf_cost_per_account_alloc_G"), 0, "$"),
            M.qfmt(col(rs, "daf_cost_bps_daf_assets_alloc_F" + sfx), 0), M.qfmt(col(rs, "daf_cost_bps_daf_assets_alloc_A"), 0),
            M.qfmt(col(rs, "daf_cost_bps_daf_assets_alloc_G"), 0)]


def weighted_row(fset: Sequence[Mapping], rows: Sequence[Mapping], sfx: str = "") -> list:
    """Band-weighted (post-stratified) medians: weight = frame N of the band / F-set n of the band."""
    w = {lbl: M.ratio(sum(1 for r in rows if r["band"] == lbl), sum(1 for r in fset if r["band"] == lbl) or None) for lbl, _ in BANDS}
    def wm(k, nd=0, pre=""):
        v = M.wmedian([(num(r[k]), w[r["band"]]) for r in fset if num(r[k]) is not None])
        return "–" if v is None else f"{pre}{v:,.{nd}f}"
    return ["All, band-weighted", len(fset), wm("daf_share_F" + sfx, 3), wm("daf_share_A", 3), wm("daf_share_G", 3),
            wm("daf_cost_per_account_alloc_F" + sfx, 0, "$"), wm("daf_cost_per_account_alloc_A", 0, "$"),
            wm("daf_cost_per_account_alloc_G", 0, "$"), wm("daf_cost_bps_daf_assets_alloc_F" + sfx), wm("daf_cost_bps_daf_assets_alloc_A"),
            wm("daf_cost_bps_daf_assets_alloc_G")]


def report(rows: Sequence[Mapping], recs: Mapping, idx: Mapping) -> str:
    fset = tuple(r for r in rows if r["daf_share_F"])
    with_tot = tuple(r for r in rows if r["n_total_funds"])
    all_hits = tuple(h for r in recs.values() for h in r.get("hits", ()) if h["part"] in MAIN_PARTS)
    ext_hits = tuple(h for r in recs.values() for h in r.get("hits", ()) if h["part"] not in MAIN_PARTS)
    spelled = tuple(x for r in recs.values() for x in r.get("spelled", ()))
    by_cls = {k: sum(1 for h in all_hits if h["cls"] == k) for k in
              ("all_funds", "endowment_only", "type_specific", "new_funds", "grantmaking", "other")}
    xml_status = {k: sum(1 for r in recs.values() if r.get("xml") == k) for k in ("ok", "missing", "parse_error")}
    checked = tuple(r for r in with_tot if r["handcheck"] and r["handcheck"] != "not_checked")
    ok = sum(1 for r in checked if r["handcheck"] in ("ok", "corrected"))
    ok_strict = sum(1 for r in checked if r["handcheck"] == "ok")
    out = []
    out.append("## Coverage\n")
    out.append(M.table(["Item", "Value"], [
        ["Tail CFs in frame", len(rows)], ["EIN-FY returns FY2022–24 indexed", len(idx)],
        ["XML ok / missing / parse error", f"{xml_status['ok']} / {xml_status['missing']} / {xml_status['parse_error']}"],
        ["Narrative fields searched (Part III + Sched O)", sum(r.get("n_narr", 0) for r in recs.values())],
        ["Regex hits, Part III + Sched O (deduplicated within return and part)", len(all_hits)],
        *[[f"  class {k}", v] for k, v in by_cls.items()],
        ["Returns with an all_funds total", sum(1 for r in recs.values() if return_total(r))],
        ["Extension: Sched D Part XIII + Sched A Part VI fields searched", sum(r.get("n_narr_ext", 0) for r in recs.values())],
        ["Extension: regex hits / all_funds hits", f"{len(ext_hits)} / {sum(1 for h in ext_hits if h['cls'] == 'all_funds')}"],
        ["Extension: CFs with a total (any part)", sum(1 for r in rows if r["n_total_funds_ext"])],
        ["Spelled-out number + 'funds' phrases in Part III + Sched O (read by hand)", len(spelled)],
        ["CFs with an all_funds total (any FY)", len(with_tot)],
        ["  of which hand-check ok / corrected / ambiguous / reject", " / ".join(
            str(sum(1 for r in checked if r["handcheck"] == v)) for v in ("ok", "corrected", "ambiguous", "reject"))],
        ["  missing a same-return Sched D DAF count", sum(1 for r in with_tot if not r["sched_d_daf_count_same_return"])],
        ["  cost row not usable", sum(1 for r in with_tot if r["usable_cost"] != "1")],
        ["CFs in the rule-F set (hand-check ok, usable cost row, Sched D count present)", len(fset)],
    ]))
    out.append("\n\n## CFs with a total, by band\n")
    out.append(M.table(["Band", "Frame N", "With total", "Share of band", "Rule-F set", "Lower-bound totals (F set)"], [
        [lbl, sum(1 for r in rows if r["band"] == lbl), sum(1 for r in with_tot if r["band"] == lbl),
         M.fmt(M.ratio(sum(1 for r in with_tot if r["band"] == lbl), sum(1 for r in rows if r["band"] == lbl)), 3),
         sum(1 for r in fset if r["band"] == lbl), sum(1 for r in fset if r["band"] == lbl and r["total_qual"] == "lower_bound")]
        for lbl, _ in BANDS]))
    out.append("\n\n## Rule F against A and G (same CFs) [I]\n")
    head = ["Band", "n", "Share F", "Share A", "Share G", "F $/acct", "A $/acct", "G $/acct", "F bps", "A bps", "G bps"]
    out.append(M.table(head, [summary_row(lbl, tuple(r for r in fset if r["band"] == lbl)) for lbl, _ in BANDS]
                       + [summary_row("All", fset), weighted_row(fset, rows)]))
    fa = [M.ratio(num(r["daf_share_F"]), num(r["daf_share_A"])) for r in fset if num(r["daf_share_A"])]
    fg = [M.ratio(num(r["daf_share_F"]), num(r["daf_share_G"])) for r in fset if num(r["daf_share_G"])]
    fext = tuple(r for r in rows if r["daf_share_F_ext"])
    out.append("\n\n## Extension: adding Sched D Part XIII and Sched A Part VI text [I]\n")
    out.append(M.table(head, [summary_row(lbl, tuple(r for r in fext if r["band"] == lbl), "_ext") for lbl, _ in BANDS]
                       + [summary_row("All", fext, "_ext")]))
    amb = tuple(r for r in rows if r["handcheck"] == "ambiguous")
    out.append("\n\nAmbiguous totals (excluded from the F set): " + "; ".join(
        f"{r['ein']} total {r['n_total_funds']}, DAFs {r['sched_d_daf_count_same_return']}, share "
        f"{M.fmt(min(1.0, num(r['sched_d_daf_count_same_return']) / num(r['n_total_funds'])), 3)}" for r in amb))
    out.append("\n\n## Robustness [C]\n")
    sens = (("Exact or approx totals only (drop lower/upper bounds)", tuple(r for r in fset if r["total_qual"] in ("stated", "approx"))),
            ("FY2024 totals only (same period as opex)", tuple(r for r in fset if r["total_fy"] == "2024")),
            ("Drop DAF count > total", tuple(r for r in fset if r["daf_gt_total"] != "1")),
            ("Drop multi-total returns", tuple(r for r in fset if r["multi_total"] != "1")))
    out.append(M.table(head, [summary_row(l, rs) for l, rs in sens]))
    out.append("\n\n" + M.table(["Statistic", "Value"], [
        ["Bootstrap 95% CI, median share F", ci(col(fset, "daf_share_F"), 3)],
        ["Bootstrap 95% CI, median F $/acct", ci(col(fset, "daf_cost_per_account_alloc_F"), 0, "$")],
        ["Bootstrap 95% CI, median F bps", ci(col(fset, "daf_cost_bps_daf_assets_alloc_F"), 0)],
        ["Per-CF F ÷ A: median (IQR)", M.qfmt([x for x in fa if x is not None], 2)],
        ["F > A at", f"{sum(1 for x in fa if x and x > 1)} of {len(fa)}"],
        ["Per-CF F ÷ G: median (IQR)", M.qfmt([x for x in fg if x is not None], 2)],
        ["Opex per fund (whole org)", M.qfmt(col(fset, "opex_per_fund"), 0, "$")],
        ["Total funds, F set", M.qfmt(col(fset, "n_total_funds"), 0)],
        ["Sched D DAFs, F set", M.qfmt(col(fset, "sched_d_daf_count_same_return"), 0)],
        ["Rule A whole frame (usable)", f"{M.qfmt(col(rows, 'daf_cost_per_account_alloc_A'), 0, '$')}; {M.qfmt(col(rows, 'daf_cost_bps_daf_assets_alloc_A'), 0)} bps"],
        ["Rule G whole frame (usable)", f"{M.qfmt(col(rows, 'daf_cost_per_account_alloc_G'), 0, '$')}; {M.qfmt(col(rows, 'daf_cost_bps_daf_assets_alloc_G'), 0)} bps"],
        ["Share A whole frame", M.qfmt(col(rows, "daf_share_A"), 3)],
    ]))
    out.append("\n\n## Qualifiers and parts (CFs with a total)\n")
    out.append(M.table(["total_qual", "n"], [[q, sum(1 for r in with_tot if r["total_qual"] == q)]
                                              for q in ("stated", "lower_bound", "approx", "upper_bound")]))
    out.append("\n\n" + M.table(["part", "n"], [[p, sum(1 for r in with_tot if r["total_part"] == p)] for p in ("part_iii", "sched_o")]))
    out.append("\n\n" + M.table(["FY of total", "n"], [[f, sum(1 for r in with_tot if r["total_fy"] == f)] for f in FYS]))
    prior = tuple(r for r in rows if r["prior_02_01_status"])
    out.append("\n\n## Overlap with the b45n33-02-01 sample (60 CFs)\n")
    out.append(M.table(["EIN", "Name", "Prior status", "Prior total", "990 total (FY, qual)"], [
        [r["ein"], r["name"], r["prior_02_01_status"], r["prior_02_01_total"],
         f"{r['n_total_funds']} ({r['total_fy']}, {r['total_qual']})" if r["n_total_funds"] else "–"]
        for r in prior if r["n_total_funds"] or r["prior_02_01_total"]]))
    out.append("\n\n## Hand check (every CF-level total)\n")
    out.append(M.table(["Verdict", "n"], [[v, sum(1 for r in with_tot if r["handcheck"] == v)]
                                          for v in sorted({r["handcheck"] for r in with_tot})]))
    out.append(f"\n\nPrecision (CF-level totals; ok or corrected = an all-funds statement): {ok}/{len(checked)}"
               + (f" = {ok / len(checked):.3f}" if checked else "")
               + f"; figure right as extracted (ok only): {ok_strict}/{len(checked)}")
    if checked:
        lo, hi = wilson(ok, len(checked))
        out[-1] = out[-1] + f" (Wilson 95% for the first ratio {lo:.3f}–{hi:.3f})"
    ex = tuple(EXCL_CHECK.values())
    if ex:
        miss = sum(1 for v, _ in ex if v == "missed_total")
        out.append(f"\n\nExcluded-hit sample: {miss} missed totals of {len(ex)} read.")
    out.append("\n\n## Spelled-out phrases read by hand (Part III + Sched O)\n")
    out.append("\n".join(f"- {x[:200]}" for x in sorted(set(spelled))))
    ext_checked = tuple(r for r in rows if r["handcheck_ext"] and r["handcheck_ext"] != "not_checked")
    out.append(f"\n\nExtension totals hand-checked: {sum(1 for r in ext_checked if r['handcheck_ext'] in ('ok', 'corrected'))}"
               f"/{len(ext_checked)} ok or corrected.")
    return "\n".join(out)


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    s = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (c - s) / d, (c + s) / d


def excluded_sample(recs: Mapping, n: int = 40) -> tuple[tuple[str, dict], ...]:
    pool = sorted(((o, h) for o, r in recs.items() for h in r.get("hits", ())
                   if h["cls"] in ("endowment_only", "type_specific", "grantmaking", "other", "new_funds")),
                  key=lambda t: (t[0], t[1]["n"], t[1]["snippet"]))
    return tuple(random.Random(SAMPLE_SEED).sample(pool, min(n, len(pool))))


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--xml-dir", action="append", default=[])
    ap.add_argument("--json-cache", action="append", default=[])
    ap.add_argument("--cache-dir")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--task", default="build", choices=("build", "hits", "sample"))
    a = ap.parse_args(argv)
    os.chdir(a.root)
    if a.cache_dir:
        os.makedirs(a.cache_dir, exist_ok=True)
    cost = B.read_csv(COST_CSV)
    fr = M.frame(cost)
    eins = frozenset(r["ein"] for r in fr)
    idx = returns_index(B.read_csv(HARVEST_CSV), B.read_csv(COSTSTRUCT_CSV), eins)
    recs = {o: parse_return(o, load_xml(o, a.xml_dir, a.json_cache, a.cache_dir, a.fetch)) for o in sorted(set(idx.values()))}
    prior = {r["ein"]: r for r in B.read_csv(PRIOR_CSV)} if os.path.exists(PRIOR_CSV) else {}
    rows = tuple(cf_row(c, recs, idx, prior) for c in sorted(fr, key=lambda r: r["ein"]))
    if a.task == "hits":
        for r in rows:
            for sfx, parts in (("", MAIN_PARTS), ("_ext", EXT_PARTS)):
                o = r["total_object_id" + sfx]
                t = return_total(recs[o], parts) if o else None
                if t and not (sfx and o == r["total_object_id"] and t["n"] == num(r["n_total_funds_extracted"] or 0)):
                    print(f"{o}|{t['n']}\t{sfx or 'main'}\t{r['ein']}\t{r['name']}\tFY{r['total_fy' + sfx]}\t{t['qual']}\t"
                          f"multi={t['multi_total']}\tdaf={r['sched_d_daf_count_same_return' + sfx]}\t{t['part']}\t{t['snippet']}")
        return 0
    if a.task == "sample":
        for o, h in excluded_sample(recs):
            print(f"{o}|{h['n']}\t{h['cls']}\t{h['snippet']}")
        return 0
    B.write_csv(OUT_CSV, rows, FIELDS)
    print(report(rows, recs, idx))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
