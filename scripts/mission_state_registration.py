#!/usr/bin/env python3
"""B50-02: DAF sponsors' state charitable-registration status (public registry data).

Sample (pure, reproducible):
  * top50   -- the 50 rows with size_band_fy2024 == 'top50' in
               data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv
               (corrected FY2024 DAF-asset ranks 1-50).
  * small50 -- a seeded random sample (random.Random(SEED).sample) of 50 EINs
               from the same file with size_band_fy2024 in
               {mid, t10_50, t1_10, t0_1} (FY2024 DAF assets > 0, rank > 50),
               drawn from the EIN-sorted list.

States:
  * Scripted (official open data, Socrata SODA /resource/ endpoints, public-domain
    licence, robots.txt allows /resource/ for '*' and names no Claude agent):
      CO  data.colorado.gov 37wu-kn3g  (Colorado Secretary of State charities
          registrations; joined on FEIN)
      CT  data.ct.gov ngch-56tr        (CT eLicense credentials, Department of
          Consumer Protection; credential 'PUBLIC CHARITY*'; no EIN, so joined on
          normalised legal name)
  * Manual only (not scripted; reason in MANUAL_STATES): CA, NY, PA, MA, WA.

Enforcement notices: cross-reference against the repo's
daf-litigation-2021plus.csv rows whose plaintiff_type is 'state AG', plus the
registry status itself (REVOKED / DENIED / SUSPENDED). Nothing else is checked
by script.

Usage (from the repo root):
  python3 -I scripts/mission_state_registration.py . <cache_dir>
The cache dir holds the raw JSON pulls (fetched if absent). Output:
  data/mission-2026-11-14/state-registration-2026-11-20.csv
A summary (shares by state and frame) is printed to stdout.

Functional style, stdlib only. User agent: research-script/1.0.
"""
import csv
import datetime
import json
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from collections import Counter
from functools import reduce

SEED = 20261120
UA = "research-script/1.0"
RETRIEVED = "2026-11-20"
FRAME_FILE = "data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv"
LIT_FILE = "data/mission-2026-11-14/daf-litigation-2021plus.csv"
OUT_FILE = "data/mission-2026-11-14/state-registration-2026-11-20.csv"
SMALL_BANDS = ("mid", "t10_50", "t1_10", "t0_1")
ROBOT_AGENTS = ("*", "ClaudeBot", "anthropic-ai", "Claude-User", "Claude-Web", "Claude-SearchBot")

CO = {
    "state": "CO",
    "registry": "Colorado Secretary of State, Charities Program (open data 37wu-kn3g)",
    "host": "data.colorado.gov",
    "resource": "/resource/37wu-kn3g.json",
    "page": "https://data.colorado.gov/Business/Registration-of-Charities-Paid-Solicitors-Professio/37wu-kn3g",
}
CT = {
    "state": "CT",
    "registry": "Connecticut Department of Consumer Protection, eLicense credentials (open data ngch-56tr)",
    "host": "data.ct.gov",
    "resource": "/resource/ngch-56tr.json",
    "page": "https://data.ct.gov/Business/State-Licenses-and-Credentials/ngch-56tr",
}

MANUAL_STATES = (
    ("CA", "California AG Registry of Charities and Fundraisers",
     "https://ca-rcf.evokeplatform.com/app/publicPortal/verification",
     "No bulk or open-data file found (oag.ca.gov/charities links only the search; data.ca.gov sitemap has no registry "
     "dataset). Legacy search rct.doj.ca.gov returned HTTP 404. New portal is a session-based single-page app with no "
     "documented public API; its platform bundle ships reCAPTCHA components. Not scripted."),
    ("NY", "New York AG Charities Bureau Registry",
     "https://charities-search.ag.ny.gov/RegistrySearch",
     "Search API calls require an X-Recaptcha-Token header (reCAPTCHA v3), i.e. an anti-automation control; "
     "charitiesnys.com robots.txt returns HTTP 500 (treated as disallowed). No data.ny.gov registry dataset. Not scripted."),
    ("PA", "Pennsylvania DOS Bureau of Corporations and Charitable Organizations",
     "https://www.charities.pa.gov/#/page/searchCharities",
     "www.charities.pa.gov robots.txt is 'User-agent: * / Disallow: /'. No data.pa.gov registry dataset. "
     "Enforcement list on pa.gov is a Coveo-driven search. Not scripted."),
    ("MA", "Massachusetts AG Non-Profit/Public Charities Division",
     "https://www.mass.gov/how-to/search-for-a-public-charity",
     "www.mass.gov robots.txt returns HTTP 403 (treated as disallowed); filings.ago.state.ma.us and "
     "charity.ago.state.ma.us unreachable from this sandbox. Not scripted."),
    ("WA", "Washington Secretary of State, Corporations and Charities Filing System (CCFS)",
     "https://ccfs.sos.wa.gov/#/cftSearch",
     "data.wa.gov holds no charities registry dataset (only a 2015 link to the corporations search; the corporations "
     "data extract is 'no longer available'). CCFS search loads Cloudflare Turnstile (a CAPTCHA). Not scripted."),
)

# Colorado status vocabulary -> class. Definitions: coloradosos.gov/pubs/charities/FAQ/notices.html
# (expiration notices 1-3 are sent 1, 10 and 18 days after the SOS due/expiration date) and
# FAQ/consumers.html ('expired - may not solicit' or 'suspended' cannot solicit).
CO_CLASS = {
    "GOOD": "current",
    "REMINDER": "current",
    "REMINDER ESTIMATE": "current",
    "EXEMPT": "exempt",
    "NOTICE 1": "delinquent",
    "NOTICE 1 ESTIMATE": "delinquent",
    "NOTICE 2": "delinquent",
    "NOTICE 3": "delinquent",
    "NOTICE 3 ESTIMATE": "delinquent",
    "REVOKED": "revoked",
    "REGISTRATION DENIED": "revoked",
    "WITHDRAWN": "withdrawn",
}
# CT eLicense status -> class (inference; DCP does not publish definitions on the open-data page).
CT_CLASS = {
    "ACTIVE": "current",
    "ACTIVE IN RENEWAL": "current",
    "ACTIVE UNDER REVIEW": "current",
    "APPROVED": "current",
    "PENDING": "pending",
    "LAPSED": "delinquent",
    "INACTIVE": "inactive",
    "CLOSED": "inactive",
    "EXPIRED APPLICATION": "inactive",
    "SUSPENDED": "suspended",
    "DENIED": "revoked",
}
GENERIC_WORDS = {"COMMUNITY", "FOUNDATION", "FUND", "TRUST", "CHARITABLE", "GIFT", "OF", "AND", "FOR", "GREATER"}
SUFFIXES = ("INCORPORATED", "INC", "CORPORATION", "CORP", "CO", "LLC", "LTD", "THE")


# ---------------------------------------------------------------- pure helpers
def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def ein9(ein):
    return re.sub(r"\D", "", ein or "").zfill(9)


def ein_dashed(ein):
    e = ein9(ein)
    return f"{e[:2]}-{e[2:]}"


def norm_name(name):
    s = (name or "").upper().replace("&", " AND ")
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    words = s.split()
    words = words[1:] if words[:1] == ["THE"] else words
    trimmed = reduce(lambda acc, _: acc[:-1] if acc and acc[-1] in SUFFIXES else acc, range(3), words)
    return " ".join(trimmed)


def sponsor_row(frame, rank, r):
    return {
        "sample_frame": frame,
        "sample_order": rank,
        "ein": ein9(r["ein"]),
        "sponsor_name": r["name"],
        "sponsor_category": r["sponsor_category"],
        "size_band_fy2024": r["size_band_fy2024"],
        "fy2024_rank_assets": r["fy2024_rank_assets"],
        "daf_assets_fy2024": r["daf_assets_fy2024"],
        "bmf_state": r["bmf_state"],
    }


def build_sample(frame_rows, seed=SEED, n=50):
    top = sorted((r for r in frame_rows if r["size_band_fy2024"] == "top50"),
                 key=lambda r: int(r["fy2024_rank_assets"]))
    pool = sorted((r for r in frame_rows if r["size_band_fy2024"] in SMALL_BANDS), key=lambda r: ein9(r["ein"]))
    small = sorted(random.Random(seed).sample(pool, n), key=lambda r: int(r["fy2024_rank_assets"] or 10**9))
    return (tuple(sponsor_row("top50", i + 1, r) for i, r in enumerate(top))
            + tuple(sponsor_row("small50", i + 1, r) for i, r in enumerate(small)))


def day(s):
    return (s or "")[:10]


def days_between(a, b):
    try:
        return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
    except ValueError:
        return ""


def co_pick(rows):
    """rows: all CO charitable-organization rows for one FEIN -> summary dict."""
    by_entity = reduce(lambda acc, r: {**acc, r["entityid"]: acc.get(r["entityid"], ()) + (r,)}, rows, {})
    entity_key = lambda rs: (max(day(r.get("statusdate")) for r in rs), max(day(r.get("registrationapproveddate")) for r in rs))
    ent_rows = max(by_entity.values(), key=entity_key)
    latest = max(ent_rows, key=lambda r: (day(r.get("registrationapproveddate")), r.get("documentid", "")))
    fy = max((day(r.get("fiscalyearenddate")) for r in ent_rows if r.get("fiscalyearenddate")), default="")
    renewal_rows = [r for r in ent_rows if r.get("filingtype", "").upper() in ("RENEWAL", "MASTER")]
    last_renewal = max((day(r.get("registrationapproveddate")) for r in renewal_rows), default="")
    status = (latest.get("currentstatus") or "").upper()
    due = day(latest.get("expirationdate")) or day(latest.get("nextrenewalregistrationdate"))
    cls = CO_CLASS.get(status, "unmapped")
    return {
        "days_past_due": days_between(due, RETRIEVED) if cls == "delinquent" and due else "",
        "match_confidence": "high (FEIN)",
        "status_raw": status,
        "status_class": cls,
        "status_date": day(latest.get("statusdate")),
        "latest_fiscal_year_end": fy,
        "latest_filing_year": fy[:4],
        "latest_filing_type": latest.get("filingtype", ""),
        "latest_filing_date": day(latest.get("registrationapproveddate")),
        "last_renewal_or_master_date": last_renewal,
        "next_due_or_expiration": day(latest.get("expirationdate")) or day(latest.get("nextrenewalregistrationdate")),
        "registry_id": latest.get("entityid", ""),
        "registry_name": latest.get("name", ""),
        "match_method": "FEIN exact" + (f"; {len(by_entity)} entity ids, latest-status entity used" if len(by_entity) > 1 else ""),
    }


def co_record(sponsor, co_index):
    rows = co_index.get(ein_dashed(sponsor["ein"]), ())
    return co_pick(rows) if rows else {"status_class": "not_found", "match_method": "FEIN exact (no row)"}


CT_RANK = {"current": 0, "pending": 1, "delinquent": 2, "suspended": 3, "inactive": 4, "revoked": 5}


def ct_names(r):
    return {norm_name(r.get(k, "")) for k in ("name", "businessname", "dba") if r.get(k)}


def ct_index(rows):
    return reduce(lambda acc, r: reduce(lambda a, n: {**a, n: a.get(n, ()) + (r,)}, ct_names(r), acc), rows, {})


def ct_match(sponsor, index):
    key = norm_name(sponsor["sponsor_name"])
    if set(key.split()) <= GENERIC_WORDS:
        return (), "generic name (only generic words), not matched"
    if key in index:
        return index[key], "normalised name exact"
    # IRS e-file names are often truncated: allow a unique-prefix match for long names only.
    cands = [k for k in index if len(key) >= 25 and k.startswith(key + " ")]
    return (index[cands[0]], f"unique prefix of '{cands[0]}' (IRS name truncated)") if len(cands) == 1 else ((), "")


def ct_record(sponsor, index):
    rows, how = ct_match(sponsor, index)
    if not rows:
        return {"status_class": "not_found", "match_method": how or "normalised name (no unique match)"}
    neg_date = lambda d: tuple(-int(x) for x in (d or "0000-00-00").split("-"))
    best = min(rows, key=lambda r: (CT_RANK.get(CT_CLASS.get(r.get("status", ""), "inactive"), 9),
                                    neg_date(day(r.get("expirationdate")))))
    status = best.get("status", "")
    return {
        "status_raw": f"{status} / {best.get('statusreason', '')} ({best.get('credential', '')})",
        "status_class": CT_CLASS.get(status, "unmapped"),
        "status_date": day(best.get("effectivedate")),
        "latest_fiscal_year_end": "",
        "latest_filing_year": "",
        "latest_filing_type": "",
        "latest_filing_date": day(best.get("effectivedate")),
        "last_renewal_or_master_date": "",
        "next_due_or_expiration": day(best.get("expirationdate")),
        "registry_id": best.get("fullcredentialcode", ""),
        "registry_name": best.get("name", ""),
        "match_method": how + (f"; {len(rows)} credentials" if len(rows) > 1 else ""),
        "match_confidence": "medium (name + address state = IRS BMF state)" if best.get("state", "") == sponsor["bmf_state"]
        else f"low (name only; CT address state {best.get('state', '')} vs BMF {sponsor['bmf_state']})",
        "days_past_due": "",
    }


def ag_actions(lit_rows):
    return tuple((norm_name(r["defendant"].split(";")[0]), r["case_id"], r["caption"], r["source_urls"].split(" ; ")[0])
                 for r in lit_rows if r.get("plaintiff_type", "").strip().lower() == "state ag")


def enforcement(sponsor, actions, status_class):
    key = norm_name(sponsor["sponsor_name"])
    hits = [a for a in actions if key and (a[0].startswith(key) or key.startswith(a[0]))]
    from_status = "registry status " + status_class if status_class in ("revoked", "suspended") else ""
    from_lit = "; ".join(f"{a[1]}: {a[2]}" for a in hits)
    return ("; ".join(x for x in (from_status, from_lit) if x) or "none in sources checked",
            "; ".join(a[3] for a in hits))


BLANK = ("match_confidence", "days_past_due", "status_raw", "status_date", "latest_fiscal_year_end", "latest_filing_year", "latest_filing_type",
         "latest_filing_date", "last_renewal_or_master_date", "next_due_or_expiration", "registry_id",
         "registry_name", "match_method")
FIELDS = ("sample_frame", "sample_order", "ein", "sponsor_name", "sponsor_category", "size_band_fy2024",
          "fy2024_rank_assets", "daf_assets_fy2024", "bmf_state", "state", "registry", "access_mode",
          "status_class", *BLANK, "enforcement_notice", "enforcement_source", "source_url", "retrieved", "notes")


def scripted_row(sponsor, cfg, rec, actions):
    enf, enf_src = enforcement(sponsor, actions, rec["status_class"])
    note = {"not_found": "Absent from the registry file; may be exempt or not soliciting in the state (not evidence of non-compliance)",
            "withdrawn": "Registration withdrawn by the registrant per registry status",
            "delinquent": "Registry shows an expiration-notice status (CO: notice 1/2/3 are sent 1/10/18 days after the due date); "
                          "a few days past due usually reflects filing or processing lag"}.get(rec["status_class"], "")
    return {**sponsor, **{k: "" for k in BLANK}, **rec, "state": cfg["state"], "registry": cfg["registry"],
            "access_mode": "scripted_open_data", "enforcement_notice": enf, "enforcement_source": enf_src,
            "source_url": cfg["page"], "retrieved": RETRIEVED, "notes": note}


def manual_row(sponsor, st, actions):
    enf, enf_src = enforcement(sponsor, actions, "")
    return {**sponsor, **{k: "" for k in BLANK}, "state": st[0], "registry": st[1], "access_mode": "manual_only",
            "status_class": "manual_only", "enforcement_notice": enf.replace("none in sources checked", "registry not checked; none in repo litigation file"),
            "enforcement_source": enf_src, "source_url": st[2], "retrieved": RETRIEVED, "notes": st[3]}


def summarise(rows):
    keyed = Counter((r["state"], r["sample_frame"], r["status_class"]) for r in rows)
    states = sorted({r["state"] for r in rows if r["access_mode"] == "scripted_open_data"})
    frames = ("top50", "small50", "all")
    count = lambda st, fr, cls: sum(v for (s, f, c), v in keyed.items() if s == st and (fr == "all" or f == fr) and c == cls)
    total = lambda st, fr: sum(v for (s, f, c), v in keyed.items() if s == st and (fr == "all" or f == fr))
    classes = sorted({c for (_, _, c) in keyed})
    sel = lambda st, fr: [r for r in rows if r["state"] == st and (fr == "all" or r["sample_frame"] == fr)]
    extra = lambda st, fr: {
        "current_excl_low_confidence_match": sum(1 for r in sel(st, fr) if r["status_class"] == "current" and not r["match_confidence"].startswith("low")),
        "delinquent_le30d_past_due": sum(1 for r in sel(st, fr) if r["status_class"] == "delinquent" and r["days_past_due"] != "" and int(r["days_past_due"]) <= 30),
        "delinquent_gt30d_past_due": sum(1 for r in sel(st, fr) if r["status_class"] == "delinquent" and (r["days_past_due"] == "" or int(r["days_past_due"]) > 30)),
    }
    return tuple({"state": st, "frame": fr, "n": total(st, fr), **{c: count(st, fr, c) for c in classes}, **extra(st, fr),
                  "share_current_of_sample": round(count(st, fr, "current") / total(st, fr), 3),
                  "share_current_of_found": round(count(st, fr, "current") / max(1, total(st, fr) - count(st, fr, "not_found")), 3)}
                 for st in states for fr in frames)


# ---------------------------------------------------------------------- I/O
def robots_check(host, path):
    rp = urllib.robotparser.RobotFileParser()
    req = urllib.request.Request(f"https://{host}/robots.txt", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as resp:
        body = resp.read().decode("utf-8", "replace")
    rp.parse(body.splitlines())
    named = [a for a in ROBOT_AGENTS[1:] if a.lower() in body.lower()]
    verdicts = {a: rp.can_fetch(a, f"https://{host}{path}") for a in ROBOT_AGENTS}
    return all(verdicts.values()), {"host": host, "path": path, "named_claude_agents": named, "verdicts": verdicts}


def get_json(host, resource, params):
    url = f"https://{host}{resource}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    time.sleep(1.0)  # Socrata robots Crawl-delay: 1
    return data


def cached(path, thunk):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    data = thunk()
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    return data


def fetch_co(feins):
    chunks = [feins[i:i + 40] for i in range(0, len(feins), 40)]
    where = lambda ch: "fein in (" + ",".join(f"'{f}'" for f in ch) + ") and registranttypeabbr='Charitable Organization'"
    return reduce(lambda acc, ch: acc + get_json(CO["host"], CO["resource"], {"$where": where(ch), "$limit": 50000}), chunks, [])


def fetch_ct():
    sel = "credentialid,name,businessname,dba,fullcredentialcode,credential,status,statusreason,active,issuedate,effectivedate,expirationdate,state"
    return get_json(CT["host"], CT["resource"], {"$select": sel, "$where": "credential like 'PUBLIC CHARITY%'", "$limit": 100000})


def main(argv):
    root, cache = argv[1], argv[2]
    os.makedirs(cache, exist_ok=True)
    robots = [robots_check(c["host"], c["resource"]) for c in (CO, CT)]
    print(json.dumps([r[1] for r in robots], indent=1))
    if not all(r[0] for r in robots):
        sys.exit("robots.txt disallows a scripted source; stopping")
    sample = build_sample(read_csv(os.path.join(root, FRAME_FILE)))
    actions = ag_actions(read_csv(os.path.join(root, LIT_FILE)))
    co_rows = cached(os.path.join(cache, "co_37wu-kn3g_sample.json"),
                     lambda: fetch_co(sorted({ein_dashed(s["ein"]) for s in sample})))
    ct_rows = cached(os.path.join(cache, "ct_ngch-56tr_public_charity.json"), fetch_ct)
    co_idx = reduce(lambda acc, r: {**acc, r.get("fein", ""): acc.get(r.get("fein", ""), ()) + (r,)}, co_rows, {})
    ct_idx = ct_index(ct_rows)
    rows = tuple(
        row
        for s in sample
        for row in (scripted_row(s, CO, co_record(s, co_idx), actions),
                    scripted_row(s, CT, ct_record(s, ct_idx), actions),
                    *(manual_row(s, st, actions) for st in MANUAL_STATES))
    )
    with open(os.path.join(root, OUT_FILE), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"raw rows: CO {len(co_rows)}, CT {len(ct_rows)}; output rows {len(rows)} -> {OUT_FILE}")
    print(json.dumps(summarise(rows), indent=1))


if __name__ == "__main__":
    main(sys.argv)
