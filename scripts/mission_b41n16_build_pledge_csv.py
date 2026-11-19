"""Build data/mission-2026-11-14/daf-pledge-policy-2026-11-19.csv. usage: python3 -I build_pledge_csv.py REPO_ROOT
Pure functions; carries recipient facts from gift-office-daf-policies-2026.csv and applies this pass's reads."""
import csv, os, sys
from collections import Counter

ACC = "2026-11-19"
COLS = ["row_id", "side", "entity", "ein", "rank_basis", "rank", "usd_m", "rule_class", "follows_notice_2017_73_s4",
        "forbids_daf_pledge_payment", "rule_quote", "evidence_label", "source_url", "page_date", "accessed",
        "robots_or_access", "carried_from", "change_vs_repo", "notes"]

# rule_class -> (follows notice, forbids)
CLASS = {
    "allowed_if_no_reference": ("yes", "no"),
    "forbids_any_personal_pledge": ("no", "yes_any_pledge"),
    "forbids_binding_pledge": ("no", "yes_binding_only"),
    "non_binding_intention_only": ("no", "yes_binding_only (books DAF commitments as non-binding intentions)"),
    "non_binding_pledges_only": ("no", "yes_binding_only (supports non-binding pledges)"),
    "not_stated": ("unknown", "unknown"),
    "not_read": ("unknown", "unknown"),
}

# Overrides for recipients from this pass (row_id -> dict)
REC_UPDATES = {
    "GO-02": dict(rule_class="allowed_if_no_reference", change="none (re-confirmed classification from repo [F])"),
    "GO-06": dict(rule_class="allowed_if_no_reference", change="none"),
    "GO-10": dict(rule_class="forbids_any_personal_pledge", label="S",
                  url="https://www.finance.upenn.edu/?p=1101", robots="robots allowed; HTTP 403 to fetch on 2026-11-19",
                  change="none (still [S]: fetch 403)"),
    "GO-11": dict(rule_class="non_binding_intention_only", change="none"),
    "GO-14": dict(rule_class="not_stated", change="none; Columbia-run DAF clause [S] only, external DAF rule not stated"),
    "GO-16": dict(rule_class="forbids_any_personal_pledge", change="none"),
    "GO-19": dict(rule_class="forbids_binding_pledge", label="S",
                  url="https://giving.umich.edu/um/donor-advised-fund", robots="robots allowed; HTTP 403 to fetch on 2026-11-19",
                  change="none (still [S])"),
    "GO-20": dict(rule_class="non_binding_intention_only", label="S", change="none ([S] Arts & Sciences FAQ)"),
    "GO-22": dict(rule_class="non_binding_intention_only", label="F",
                  quote="Pledge / Non-Binding Intention (NBI) Transmittal: 'NBI (Pledge with contingencies, donor-advised fund as legal donor, etc)'",
                  url="https://www.northwestern.edu/financial-operations/policies-procedures/forms/pledgenon-binding-intent-transmittal.pdf",
                  robots="allowed; fetched 200", change="upgraded S->F"),
    "GO-25": dict(rule_class="forbids_any_personal_pledge", change="none"),
    "GO-08": dict(rule_class="not_stated", label="F",
                  quote="DAF page and 'Using Donor-Advised Funds to Support MIT' page read; neither mentions pledges",
                  url="https://giving.mit.edu/donor-advised-funds ; https://giving.mit.edu/planned-giving/corridor/using-donor-advised-funds-support-mit",
                  robots="robots.txt now 200 and allows (was 403 in repo); fetched 200", change="upgraded not_read/S -> not_stated/F"),
    "GO-21": dict(rule_class="not_stated", label="F", quote="Mayo planned-giving DAF page read; no pledge clause",
                  url="https://plannedgiving.mayoclinic.org/donor-advised-funds", robots="allowed; fetched 200",
                  change="upgraded not_read/S -> not_stated/F"),
    "GO-17": dict(rule_class="not_stated", label="F", quote="St. Jude DAF page read; no pledge clause",
                  url="https://www.stjude.org/give/planned-giving/impact-major-gift/donor-advised-funds.html",
                  robots="allowed; fetched 200", change="upgraded not_found/S -> not_stated/F"),
    "GO-18": dict(rule_class="non_binding_intention_only", label="F",
                  quote="'Pledges from individual donors that are likely to be paid in full or part through either a private or family foundation or a donor-advised fund should be written in the form of a non-binding statement of intention'",
                  url="https://policy.usc.edu/gift-acceptance-and-campaign-counting/", page_date="issued 2018-11-15; last reviewed 2021-03-01",
                  robots="allowed; fetched 200", change="upgraded not_found -> non_binding_intention_only [F]"),
    "GO-07": dict(rule_class="not_stated", label="F",
                  quote="give.berkeley.edu FAQ: 'UC Berkeley welcomes gifts from Donor Advised Funds'; no pledge rule for DAFs",
                  url="https://give.berkeley.edu/faq", robots="give.berkeley.edu robots allowed; fetched 200",
                  change="upgraded not_read/R -> not_stated/F (FAQ only; Foundation gift policy not found)"),
    "GO-13": dict(rule_class="not_stated", label="F",
                  quote="Princeton University Gift Policies page: DAFs mentioned (donor identity), pledges via promise letters; no DAF-pledge rule",
                  url="https://alumni.princeton.edu/princeton-university-gift-policies", robots="allowed; fetched 200",
                  change="none (re-read a second Princeton page)"),
    "GO-01": dict(rule_class="not_read", label="R",
                  quote="giving.jhu.edu robots.txt returns 403; 2026 'DAF Policies and Guidelines' PDF not read. Search text did not show a pledge clause",
                  robots="giving.jhu.edu robots.txt 403 on 2026-11-19; not fetched", change="none"),
    "GO-29": dict(rule_class="not_read", label="R", robots="www.nyu.edu robots.txt 403 on 2026-11-19; not fetched", change="none"),
    "GO-05": dict(rule_class="not_read", label="R", robots="give.ucsf.edu robots.txt unreachable (URLError) on 2026-11-19; not fetched", change="none"),
}

SPONSORS = [  # rank_fy2024_assets, entity, ein, rule_class, quote, label, url, page_date, robots, carried, change, notes
    (1, "Fidelity Charitable", "110303001", "non_binding_pledges_only",
     "'Grant recommendations can be made in support of non-legally binding pledges ... select \"Pledge (non-binding)\" from the grant use menu'",
     "F", "https://www.fidelitycharitable.org/faqs/all/grant-pledge.html", "live 2026-11-19 (page shows 2026 year-end banner)",
     "allowed; fetched 200", "GO-S1", "none", "Program Guidelines PDF read: no pledge clause; general 'more than incidental benefit' screen"),
    (2, "National Philanthropic Trust", "237825575", "allowed_if_no_reference",
     "[S] grantmaking-rules page (search text in repo): a grant may fulfil a personal pledge but NPT cannot reference it",
     "S", "https://www.nptrust.org/what-is-a-donor-advised-fund/grantmaking-rules/", "", "not fetched: NPT Terms of Use ban robots/scripts for any purpose (repo)",
     "GO-S4", "none", ""),
    (3, "DAFgiving360 (Schwab Charitable)", "311640316", "forbids_binding_pledge",
     "2024 Program Policies, 'Enforceable pledges': 'No grant can be used to relieve an individual of a legally binding pledge.'",
     "F (2024 edition, third-party-hosted copy)",
     "https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf",
     "2024 edition (upload 2025-03)", "static1.squarespace.com robots 404 = no rules; dafgiving360.org program-policies page now 200 but body has no policy text",
     "GO-S2", "upgraded not_read -> forbids_binding_pledge (2024 edition)", "2026 edition not located"),
    (4, "Vanguard Charitable", "232888152", "forbids_binding_pledge",
     "Impermissible purposes include 'Fulfillment of legally binding pledges or other obligations.'", "F",
     "https://www.vanguardcharitable.org/sites/default/files/2026-01/policies_and_guidelines_january_2026_011326_final_0.pdf",
     "2026-01", "allowed (repo read)", "GO-S3", "none (not re-read)", ""),
    (5, "Goldman Sachs Philanthropy Fund", "311774905", "not_read", "", "R", "https://gspf.goldman.com/", "",
     "gspf.goldman.com robots.txt disallows all user agents; not fetched", "", "new row", ""),
    (6, "Silicon Valley Community Foundation", "205205488", "not_stated",
     "Advised Fund Agreement read: non-binding recommendations and 'incidental' benefit limits; no pledge clause", "F",
     "https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf", "2025-08-22 (repo)", "allowed; fetched 200", "", "new row", ""),
    (7, "Morgan Stanley Global Impact Funding Trust (MS GIFT)", "527082731", "forbids_binding_pledge",
     "Impermissible: 'A grant to fulfill a legally binding pledge or other agreement. In some instances, however, MS GIFT might enter into a grant agreement with a charity to make a grant.' Language to avoid includes 'Pledge'",
     "F", "https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf",
     "undated (no year printed)", "allowed; fetched 200", "", "new row", "Also asks for further inquiry where a grant may fulfil 'a prior personal pledge'"),
    (8, "American Endowment Foundation", "341747398", "allowed_if_no_reference",
     "'Donors may recommend a grant to fulfill a pledge to a charitable organization provided ... AEF makes no reference to the existence of the pledge ... The donor does not receive any benefit that is more than incidental ... '",
     "F", "https://aefonline.org/wp-content/uploads/2025/03/AEF_05_GrantingGuidelines_V1.6.pdf ; https://advisorwelcome.aefonline.org/granting-guidelines",
     "2025-03 (V1.6)", "allowed; fetched 200", "", "new row", "Mirrors Notice 2017-73 s.4's three conditions; an older AEF FAQ (search text) reportedly said the opposite; not read (host unreachable)"),
    (9, "Renaissance Charitable Foundation", "352129262", "not_read", "", "U",
     "", "", "not fetched: Renaissance site terms bar scraping without written authorization (repo); search found no pledge rule", "", "new row", ""),
    (10, "National Christian Foundation", "581493949", "forbids_binding_pledge",
     "Grants can't be used to provide you: '... Fulfillment of legally binding pledges ...'", "F",
     "https://www.ncfgiving.com/guide-to-giving-at-NCF", "live 2026-11-19", "allowed; fetched 200", "", "new row", ""),
    (11, "Bank of America Charitable Gift Fund", "046010342", "not_stated",
     "Guide to Navigating Your Donor Advised Fund read; no pledge clause found", "F",
     "https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf", "", "robots 404 = no rules; fetched 200", "", "new row", ""),
    (12, "The Chicago Community Trust", "362167000", "not_stated",
     "Donor Portal FAQ read; no pledge clause found", "F", "https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf", "",
     "allowed; fetched 200; cct.org policy pages not fetched (repo: robots unreadable)", "", "new row", ""),
    (13, "ImpactAssets", "262048480", "not_read", "", "U", "", "", "Program Circular 403 (repo); FAQ URL tried 404", "", "new row", ""),
    (14, "Jewish Communal Fund", "237174183", "not_stated",
     "Policy Guide (Aug 2024) read: grants nonbinding; no 'more than incidental benefit' grants; no pledge clause found", "F",
     "https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf", "2024-08", "allowed; fetched 200", "", "new row", ""),
    (15, "Foundation For The Carolinas", "566047886", "not_read", "", "U", "", "",
     "not fetched: FFTC website terms bar robots/automatic devices (repo)", "", "new row", ""),
]


def recipient_row(go, upd):
    rc = upd.get("rule_class", "not_stated" if go["pledge_rule"].startswith("not_stated") else "not_read")
    f, b = CLASS[rc]
    return {"row_id": "PL-" + go["row_id"], "side": "recipient", "entity": go["entity"], "ein": go["ein"],
            "rank_basis": "rank among top-50-sponsor FY2023-24 DAF recipients (repo gift-office scan)",
            "rank": go["daf_rank_2023_24"], "usd_m": go["daf_grant_usd_m_fy2023_24"], "rule_class": rc,
            "follows_notice_2017_73_s4": f, "forbids_daf_pledge_payment": b,
            "rule_quote": upd.get("quote", go["pledge_evidence"] or go["pledge_rule"]),
            "evidence_label": upd.get("label", go["evidence_label"]),
            "source_url": upd.get("url", go["source_urls"]), "page_date": upd.get("page_date", go["page_date"]),
            "accessed": ACC if ("url" in upd or "quote" in upd) else go["accessed"],
            "robots_or_access": upd.get("robots", go["robots_status"]), "carried_from": go["row_id"],
            "change_vs_repo": upd.get("change", "none (carried; not re-read)"), "notes": ""}


def sponsor_row(t):
    rank, ent, ein, rc, q, lab, url, pdate, rob, car, chg, notes = t
    f, b = CLASS[rc]
    return {"row_id": f"PL-S{rank:02d}", "side": "sponsor", "entity": ent, "ein": ein,
            "rank_basis": "FY2024 DAF assets rank (daf-sponsor-league-table-fy2021-2025.csv)", "rank": str(rank), "usd_m": "",
            "rule_class": rc, "follows_notice_2017_73_s4": f, "forbids_daf_pledge_payment": b, "rule_quote": q,
            "evidence_label": lab, "source_url": url, "page_date": pdate, "accessed": ACC if lab.startswith("F") else "",
            "robots_or_access": rob, "carried_from": car, "change_vs_repo": chg, "notes": notes}


def regulator_row():
    return {"row_id": "PL-R1", "side": "regulator", "entity": "IRS Notice 2017-73 s.4 (reference)", "ein": "", "rank_basis": "", "rank": "", "usd_m": "",
            "rule_class": "allowed_if_no_reference", "follows_notice_2017_73_s4": "yes", "forbids_daf_pledge_payment": "no",
            "rule_quote": "Sponsor makes no reference to the pledge; no other more-than-incidental benefit; no s.170 deduction claimed. 's.7: Taxpayers may rely on the rules described in section 4 until additional guidance is issued.' Status 2026-11-19: not superseded (see doc s.2)",
            "evidence_label": "F", "source_url": "https://www.irs.gov/pub/irs-drop/n-17-73.pdf", "page_date": "2017-12 (subject document)",
            "accessed": ACC, "robots_or_access": "irs.gov /pub/ allowed", "carried_from": "GO-R1", "change_vs_repo": "status check added", "notes": ""}


def main(root):
    gos = [r for r in csv.DictReader(open(os.path.join(root, "data/mission-2026-11-14/gift-office-daf-policies-2026.csv"))) if r["side"] == "recipient"]
    top30 = sorted(gos, key=lambda r: int(r["daf_rank_2023_24"]))[:30]
    rows = [recipient_row(g, REC_UPDATES.get(g["row_id"], {})) for g in top30] + list(map(sponsor_row, SPONSORS)) + [regulator_row()]
    out = os.path.join(root, "data/mission-2026-11-14/daf-pledge-policy-2026-11-19.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); list(map(w.writerow, rows))
    tally = lambda side: Counter(r["rule_class"] for r in rows if r["side"] == side)
    usd = lambda cls: round(sum(float(r["usd_m"]) for r in rows if r["side"] == "recipient" and r["rule_class"] in cls), 1)
    print(len(rows), "rows;", "recipients", dict(tally("recipient")), "sponsors", dict(tally("sponsor")))
    print("recipient $m by class:", {c: usd([c]) for c in CLASS}, "total", usd(list(CLASS)))
    print("labels recipients:", dict(Counter(r["evidence_label"][:1] for r in rows if r["side"] == "recipient")))
    print("changed rows:", sum(1 for r in rows if not r["change_vs_repo"].startswith("none")))


if __name__ == "__main__":
    main(sys.argv[1])
