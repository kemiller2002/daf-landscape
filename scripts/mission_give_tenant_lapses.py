#!/usr/bin/env python3
"""P-GIV-06 / P-GIV-07 (batch 30C): Give Interactive tenant identities and lapsed community-foundation tenants.

Reads a saved crt.sh JSON export for %.giveinteractive.com (all certificates, 2021+ used) and computes first and
last certificate dates per tenant label family. Joins a fixed table of public evidence gathered on 2026-11-15
(each row cites its source; nothing here is inferred by the script beyond the CT arithmetic) and the DAFRC FY2024
DAF assets, and reconciles Give's '$40B+ live or in implementation' claim against known clients.

Usage: python3 scripts/mission_give_tenant_lapses.py --crtsh <crt.sh json export>
  (export: https://crt.sh/?q=%25.giveinteractive.com&output=json)
Outputs: data/mission-2026-11-14/give-tenants-lapses-batch30.csv
         data/mission-2026-11-14/give-claim-reconciliation-batch30.csv
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re

DATA = "data/mission-2026-11-14"
DAFRC = f"{DATA}/dafrc-sponsor-schedule-d-fy2019-2024.csv"
OUT = f"{DATA}/give-tenants-lapses-batch30.csv"
OUT_REC = f"{DATA}/give-claim-reconciliation-batch30.csv"

# label regex, sponsor, EIN, question, status 2026-11-15, replacement/current vendor, replacement timing, evidence, confidence, sources
TENANTS = (
    (r"^nhf(-|$)", "unresolved: New Horizons Foundation Inc (Colorado Springs) is the only DAFRC sponsor with initials NHF and DAFs above $10m", "841123082",
     "P-GIV-06", "live Give production host (unidentified)", "", "",
     "Initials match only [I]. New Horizons Foundation (fiscal sponsor + DAF; FY2024 DAF accounts 287; website newhorizonsfoundation.net refused scripted and WebFetch reads); "
     "its TY2023-24 990 XML names no software vendor. National Heritage Foundation Inc (58-2085326) reported $0 assets at end-2022 (repo); New Hampshire CF is on Foundant (excluded). "
     "crt.sh certificates carry no other SAN names", "low (candidate only)",
     "https://projects.propublica.org/nonprofits/organizations/841123082 ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349306440_public.xml ; https://crt.sh/?q=nhf.giveinteractive.com"),
    (r"^jttw(-|$)", "unresolved", "", "P-GIV-06", "live Give production host (unidentified)", "", "",
     "No DAFRC sponsor has initials JTTW (stopwords kept or dropped); web search finds no US organisation using the acronym; certificates are single-name", "none",
     "https://crt.sh/?q=jttw.giveinteractive.com"),
    (r"^tc-innov", "Thrivent Charitable Impact & Investing (weak)", "411802412", "P-GIV-06", "feature host only", "", "",
     "Pattern: '<initials>-innov' hosts exist for vc (Vanguard Charitable), ia (ImpactAssets) and jcf; Thrivent's own hosts are 'thriventcharitable-staging' (2026-08-14) and 'thrivent-sftp.int' (2026-10-05). "
     "crt.sh returned no certificate for tc-innov on 2026-11-15 (certspotter-only in batch 23)", "low",
     "https://crt.sh/?q=thriventcharitable-staging.giveinteractive.com"),
    (r"^(jmacarthurtrust|jmctdaf|jmt-)", "John MacArthur Charitable Trust", "830981937", "P-GIV-06", "live Give production host",
     "", "", "Name match (jmacarthurtrust; 'jmct' + 'daf'). GuideStar/ProPublica: John Macarthur Charitable Trust, Newhall CA, EIN 83-0981937, ruling 2019; the trust page "
     "gracechurch.org/macarthur-trust (search snippet: 'support for the operations, development, and expansion of key partner ministries') now returns 404. No page names Give or a DAF program; not a DAFRC sponsor",
     "medium (unchanged)", "https://www.guidestar.org/profile/83-0981937 ; https://gracechurch.org/macarthur-trust"),
    (r"^(fftc|myfftc)", "Foundation For The Carolinas", "566047886", "P-GIV-07", "lapsed (no live Give certificate after 2024-05-12)",
     "NPact Foundation Cloud Community Portal (fftc.spectrumportal.net) on Blackbaud FE NXT, then GiftingNetwork donor portal (daf.fftc.org)",
     "NPact story 2025-03-07 ('completed in less than eight months'); GiftingNetwork live 2026-07-01",
     "990 CY2023 GIVE INTERACTIVE LLC 'SOFTWARE' $654,500; no Give line CY2024 (5th payee $101,200). myfftc.giveinteractive.com (production-style name) certified 2023-11-07 to 2024-01-06 only. "
     "NPact customer story names FE NXT + RE NXT + Foundation Cloud Grants and Community Portal. GiftingNetwork release (PRLog, 2026-09-23): FFTC 'has been running a new donor portal on the GiftingNetwork platform since July 1, 2026' [V]. "
     "No public statement of why Give was dropped", "medium (sequence); reason unknown",
     "https://projects.propublica.org/nonprofits/organizations/566047886/202433209349318318/full ; https://npact.com/customer-stories/foundation-for-the-carolinas/ ; https://www.prlog.org/13172546-giftingnetworks-donor-portal-live-at-foundation-for-the-carolinas.html"),
    (r"^omahafoundation", "Omaha Community Foundation", "470645958", "P-GIV-07", "lapsed before go-live",
     "Foundant CommunitySuite (omahafoundation.fcsuite.com)", "new fundholder portal launched 2024-07-30; redesigned 2025-03-04",
     "OCF news 2024-07-29: 'we launched a new online fundholder portal'; invitations 'on July 30'; login omahafoundation.fcsuite.com/erp/fundmanager/ [F]. Give hosts last certified 2023-10-31", "high (replacement and date); reason unknown",
     "https://omahafoundation.org/news/ocf-launching-new-online-fundholder-portal-july-30/ ; https://omahafoundation.org/news/your-ocf-online-account-has-a-new-look/"),
    (r"^ocf-", "probably Omaha Community Foundation (self-styled 'OCF'); Oregon CF (also 'OCF', Salesforce MyOCF) not excluded", "470645958", "P-GIV-07",
     "lapsed (sandbox/staging; one ocf-prod certificate 2023-03-24)", "see omahafoundation row", "",
     "Hosts ocf-sandbox / ocf-staging / ocf-prod 2022-04-06 to 2023-12-07 overlap the omahafoundation host (2023-05-03 to 2023-10-31) and end together [I]. "
     "ocf.iphiview.com's 2025-04-20 certificate was one ZeroSSL batch for seven iPhi names; the host is NXDOMAIN and unattributed (repo Ren census): not evidence of a return to Ren", "low-medium",
     "https://omahafoundation.org/news/your-ocf-online-account-has-a-new-look/ ; data/mission-2026-11-14/ren-iphi-tenant-census.csv"),
    (r"^ebcf", "East Bay Community Foundation", "946070996", "P-GIV-07", "lapsed after live use",
     "akoyaGO GOfund (gofund.akoyago.com/eastbay)", "akoyaGO portal 'almost ready' 2025-07-09; Give certificates stop 2026-03-27",
     "Campaign page (modified 2023-11-16) told fund advisors to use the 'Give Interactive donor portal' at ebcf.giveinteractive.com [F]: the only CF where Give is shown live for fundholders. "
     "'Our new donor portal is almost ready' (published 2025-07-09): 'final stages of launching our new and improved donor portal ... addressing a few final technical issues'; site nav now links gofund.akoyago.com/eastbay [F]. "
     "No reason given", "high (sequence); reason unknown",
     "https://www.ebcf.org/donate-to-the-campaign-for-a-just-east-bay/ ; https://www.ebcf.org/our-new-donor-portal-is-almost-ready/"),
    (r"^kzcf", "Kalamazoo Community Foundation", "383333202", "P-GIV-07", "lapsed without visible go-live",
     "Foundation Cloud 'Kalamazoo Connect' (kalfound.spectrumportal.net), already in place", "Kalamazoo Connect upgrade May-June 2023 [S]; Give 2024-06-20 to 2025-10-19",
     "kzcf.org links kalfound.spectrumportal.net (homepage modified 2026-11-12) [F]; a May 2023 notice (search extract; page now 404) took Kalamazoo Connect offline 18-30 May for an upgrade with new-account invitations [S]. "
     "Give was trialled after the Foundation Cloud portal and did not replace it [I]", "medium",
     "https://kzcf.org/ ; https://kalfound.org/news/kalamazoo-connect-and-give-now-page-unavailable-may-18-30"),
    (r"^sdfoundation", "The San Diego Foundation", "952942582", "P-GIV-07", "staging only, lapsed",
     "MySDF on Foundation Cloud (sdfoundation.spectrumportal.net) over Blackbaud RE/FE NXT", "no change observed; Give staging 2025-04-15 to 2025-10-12",
     "Donor resources page links every MySDF login to sdfoundation.spectrumportal.net/accounts/signin [F]; Blackbaud case study (undated) names RE NXT and FE NXT [V]. Give never reached a production host", "medium",
     "https://www.sdfoundation.org/ways-to-give/current-donor-resources ; https://www.casestudies.com/company/blackbaud/case-study/the-san-diego-foundation-customer-case-study"),
)

KNOWN_CLIENTS = (  # (EIN, name, basis) for the $40B+ reconciliation
    ("232888152", "Vanguard Charitable", "contract release 2025-11-04"), ("362167000", "Chicago Community Trust", "cct production host"),
    ("262048480", "ImpactAssets", "production host + announced hub"), ("237174183", "Jewish Communal Fund", "jcf hosts (slug)"),
    ("431890105", "Servant Foundation (The Signatry)", "affiliate, live"), ("825070897", "Signatry Charitable Trust", "affiliate"),
    ("416029402", "Minneapolis Foundation", "staging"), ("411802412", "Thrivent Charitable", "staging"),
    ("751750059", "WaterStone", "live 2026-11-01"), ("842049692", "Stifel Charitable", "staging"),
)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def ct_spans(path):
    with open(path, encoding="utf-8") as fh:
        rows = json.load(fh)
    names = collections.defaultdict(list)
    for r in rows:
        for n in r["name_value"].lower().split("\n"):
            if n.endswith(".giveinteractive.com") and r["not_before"][:4] >= "2021":
                names[n.split(".giveinteractive.com")[0]].append((r["not_before"][:10], r["not_after"][:10]))
    return names


def summarize(names, rx):
    hits = {k: v for k, v in names.items() if re.search(rx, k)}
    if not hits:
        return "", "", "", ""
    first = min(b for v in hits.values() for b, _ in v)
    last = max(b for v in hits.values() for b, _ in v)
    expiry = max(a for v in hits.values() for _, a in v)
    return "; ".join(f"{k} {min(b for b, _ in v)}..{max(b for b, _ in v)}" for k, v in sorted(hits.items())), first, last, expiry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crtsh", required=True)
    a = ap.parse_args()
    names = ct_spans(a.crtsh)
    assets = {r["ein"].zfill(9): float(r["eoy_daf_assets"] or 0) for r in read_csv(DAFRC) if r["fiscal_year_end"] == "2024"}
    rows = []
    for rx, org, ein, q, status, repl, timing, ev, conf, src in TENANTS:
        hosts, first, last, expiry = summarize(names, rx)
        rows.append({"queue_item": q, "label_pattern": rx, "ct_hosts_first_last_issued": hosts, "ct_first_issued": first, "ct_last_issued": last,
                     "ct_last_expiry": expiry, "candidate_org": org, "ein": ein, "fy2024_daf_assets_usd": int(assets.get(ein, 0)) if ein else "",
                     "status_2026_11_15": status, "replacement_or_current_vendor": repl, "replacement_timing": timing,
                     "evidence": ev, "confidence": conf, "sources": src, "retrieved": "2026-11-15"})
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    rec = [{"ein": e, "name": n, "basis": b, "fy2024_daf_assets_usd": int(assets.get(e, 0))} for e, n, b in KNOWN_CLIENTS]
    total = sum(r["fy2024_daf_assets_usd"] for r in rec)
    rec.append({"ein": "", "name": "TOTAL known clients (DAF assets, DAFRC FY2024)", "basis": "", "fy2024_daf_assets_usd": total})
    rec.append({"ein": "", "name": "Gap to Give claim '$40B+ live or in implementation (2025)'", "basis": "https://www.giveinteractive.com/company", "fy2024_daf_assets_usd": 40_000_000_000 - total})
    with open(OUT_REC, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rec[0]))
        w.writeheader()
        w.writerows(rec)
    print(json.dumps({"tenant_rows": len(rows), "known_clients_daf_assets": total, "gap_to_40bn": 40_000_000_000 - total,
                      "spans": {r["label_pattern"]: (r["ct_first_issued"], r["ct_last_issued"]) for r in rows}}, indent=1))


if __name__ == "__main__":
    main()
