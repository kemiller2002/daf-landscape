"""P-B39N1-01: build the 2026 docket-submission access table for IRS-2023-0053.

Usage: python3 -I scripts/mission_b39n1_01_docket_2026.py . OUT_CSV

Reads the 13 rows with phase 'post-hearing_2026' from
data/mission-2026-11-14/daf-regs-2023-comments-summary.csv (API metadata, 2026-11-15)
and joins the access log from 2026-11-20 (robots.txt and fetch results, UA
research-script/1.0) plus the 2023-24 submissions by the same organisation
(matched on docket title, listed below). No letter text from 2026 was readable,
so the content fields hold 'not_read'. Prints the counts used in the research note.
Stdlib only; pure functions.
"""
import csv
import os
import sys
from functools import reduce

SUMMARY = "data/mission-2026-11-14/daf-regs-2023-comments-summary.csv"
CHECKED = "2026-11-20"

REGS_PAGE = "403 (CloudFront 'Request blocked'); robots.txt also 403, so no rules readable"
DOWNLOADS = "403 (CloudFront 'Request blocked'); robots.txt also 403, so no rules readable"
NOT_READ = "not_read"

# Organisation key -> (resolved name, basis, hosts checked for a submitter copy and result,
#                      2023-24 docket IDs by the same organisation, 2023-24 baseline source)
ORGS = {
    "AEF": ("American Endowment Foundation", "docket title abbreviation; 2023-24 filings under full name",
            "www.aefonline.org (robots: allow all, crawl-delay 10): post and page sitemaps scanned; WP media API 401; no 2026 letter found",
            "-0017; -0059; -0090; outline -0201", "2023-24 letters not read (regulations.gov blocked); hearing testimony known only from search summary (SS)"),
    "RCF": ("Renaissance Charitable Foundation", "docket title abbreviation; 2023-24 filings under full name",
            "www.rencharitable.org robots: 'User-agent: * Disallow: /' (not fetched); www.reninc.com scanned (no letter)",
            "-0015; -0055; outlines -0195, -0221", "2023-24 letters not read (regulations.gov blocked)"),
    "Ren": ("Ren (DAF administration vendor)", "docket title; repo note on -0251",
            "www.reninc.com (robots: allow except /wp-admin/): blogs, resources, newsroom sitemaps scanned; no letter found",
            "-0088", "2023-24 letter not read (regulations.gov blocked)"),
    "SIFMA": ("Securities Industry and Financial Markets Association", "docket title",
              "www.sifma.org (robots: content-signal comments, no blocking rule for this path): full sitemap (10,276 URLs) scanned; no 2026 DAF letter; 2024 letter read",
              "-0051; outline -0185", "SIFMA letter of 2024-02-08, read from sifma.org (P)"),
    "ABA": ("American Bar Association (section not stated in docket title)", "docket title",
            "www.americanbar.org robots.txt 403 (Cloudflare challenge): not fetched",
            "RPTE Section -0060, -0228; ABA -0179; ABA Tax Section outline -0183", "2023-24 letters not read (regulations.gov and americanbar.org blocked)"),
    "NYSBA": ("New York State Bar Association Tax Section", "docket title",
              "nysba.org (robots: allow except /wp-admin/): Tax Section reports page and master index (to 2026-11-11) read; no 2026 report on s.4966 listed; Report 1489 (2024) read",
              "-0063", "NYSBA Tax Section Report No. 1489, 2024-02-13, read from nysba.org (P)"),
    "KA": ("Kallina (law firm or attorney; docket title 'KA (Emanuel J. Kallina)')", "docket title; 2023-24 filings by the same filer name",
           "no submitter website identified by search", "-0172; outline -0232", "2023-24 letters not read (regulations.gov blocked)"),
    "AC": ("Adler & Colvin (docket title spelled 'Alder and Colvin')", "docket title; repo wave 24A correction",
           "www.adlercolvin.com (robots: allow except /wp-admin/, crawl-delay 10): post and page sitemaps scanned; no 2026 letter; 2024 joint letter URL now 404",
           "-0132 (joint with New Venture Fund)", "2024 joint letter URL on adlercolvin.com returns 404 on 2026-11-20; not read"),
    "CF": ("Council on Foundations (inference)", "repo inference from 'CF (Jenn Holcomb)'",
           "cof.org robots.txt 403 (Cloudflare challenge): not fetched",
           "-0006; -0118; outlines -0193, -0199 (if CF = Council on Foundations)", "2023-24 letters not read (regulations.gov and cof.org blocked)"),
    "MCF": ("Madison Community Foundation (inference)", "repo inference from 'MCF (Bob Sorge)'",
            "madisongives.org (robots: allow all, crawl-delay 10): post, blog and publications sitemaps scanned; no letter found",
            "-0085; outlines -0176, -0180, -0184, -0234 (if MCF = Madison CF)", "2023-24 letters not read (regulations.gov blocked)"),
}

PREFIX_TO_ORG = (("AEF", "AEF"), ("RCF", "RCF"), ("Ren", "Ren"), ("SIFMA", "SIFMA"), ("ABA", "ABA"),
                 ("NYSBA", "NYSBA"), ("KA", "KA"), ("Alder", "AC"), ("MCF", "MCF"), ("CF", "CF"))

FIELDS = ("document_id", "posted_date", "submitter_as_titled", "org_key", "submitter_resolved", "resolution_basis",
          "commenter_type", "regulations_gov_url", "attachment_url_tried", "regsgov_page_status", "downloads_status",
          "submitter_copy_search", "access_status", "adviser_managed_ask", "fees_and_advisers", "form_990",
          "meeting_draft_obbba", "quotes_with_pages", "prior_2023_24_ids", "baseline_2023_24_source",
          "evidence_grade", "checked_date")


def read_rows(root):
    with open(os.path.join(root, SUMMARY), newline="", encoding="utf-8") as f:
        return tuple(csv.DictReader(f))


def org_key(title):
    return next((k for p, k in PREFIX_TO_ORG if title.startswith(p)), "")


def build(row):
    key = org_key(row["submitter_as_titled"])
    name, basis, search, prior, base = ORGS[key]
    return {
        "document_id": row["document_id"], "posted_date": row["posted_date"],
        "submitter_as_titled": row["submitter_as_titled"], "org_key": key,
        "submitter_resolved": name, "resolution_basis": basis, "commenter_type": row["commenter_type"],
        "regulations_gov_url": row["regulations_gov_url"],
        "attachment_url_tried": f"https://downloads.regulations.gov/{row['document_id']}/attachment_1.pdf"
                                if row["document_id"] == "IRS-2023-0053-0244" else "not tried (host-level block established on -0244)",
        "regsgov_page_status": REGS_PAGE if row["document_id"] == "IRS-2023-0053-0244" else "not tried (host-level block established on -0244)",
        "downloads_status": DOWNLOADS,
        "submitter_copy_search": search,
        "access_status": "blocked",
        "adviser_managed_ask": NOT_READ, "fees_and_advisers": NOT_READ, "form_990": NOT_READ,
        "meeting_draft_obbba": NOT_READ, "quotes_with_pages": NOT_READ,
        "prior_2023_24_ids": prior, "baseline_2023_24_source": base,
        "evidence_grade": "P (docket metadata via repo API pull 2026-11-15); content none",
        "checked_date": CHECKED,
    }


def counts(rows):
    return reduce(lambda acc, r: {**acc, r["access_status"]: acc.get(r["access_status"], 0) + 1,
                                  "orgs": acc["orgs"] | {r["org_key"]}},
                  rows, {"orgs": frozenset()})


def main(root, out):
    src = tuple(filter(lambda r: r["phase_by_posted_date"] == "post-hearing_2026", read_rows(root)))
    rows = tuple(sorted(map(build, src), key=lambda r: r["document_id"]))
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        tuple(map(w.writerow, rows))
    c = counts(rows)
    by_date = reduce(lambda a, r: {**a, r["posted_date"]: a.get(r["posted_date"], 0) + 1}, rows, {})
    print(f"submissions={len(rows)} organisations={len(c['orgs'])} blocked={c.get('blocked', 0)} readable={c.get('readable', 0)}")
    print("by_posted_date=" + ", ".join(f"{d}:{n}" for d, n in sorted(by_date.items())))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
