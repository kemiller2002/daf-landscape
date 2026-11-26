"""REN-A1: count the IRS public charity baseline that a DAF charity directory can be seeded from.

Pure functions over the IRS bulk files; I/O only in main(). Python 3 stdlib only.
Inputs (download from IRS, pass the directory as argv[1]):
  https://www.irs.gov/pub/irs-soi/eo1.csv eo2.csv eo3.csv eo4.csv eo_pr.csv eo_xx.csv   (EO BMF extract)
  https://apps.irs.gov/pub/epostcard/data-download-pub78.zip  (unzipped: data-download-pub78.txt)
  https://apps.irs.gov/pub/epostcard/data-download-revocation.zip (unzipped)
Output: metric,value lines on stdout (CSV).
"""
import csv, sys, pathlib
from collections import Counter

BMF_FILES = ("eo1.csv", "eo2.csv", "eo3.csv", "eo4.csv", "eo_pr.csv", "eo_xx.csv")

def bmf_rows(paths):
    for p in paths:
        with open(p, newline="", encoding="latin-1") as fh:
            for row in csv.DictReader(fh):
                yield p.name, row

def pipe_eins(path):
    with open(path, encoding="latin-1") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("|")
            if parts and parts[0].strip().isdigit():
                yield parts[0].strip(), parts

def summarize_bmf(rows):
    eins, by_file, sub03, deduct1, foreign_file = set(), Counter(), set(), set(), set()
    status = Counter()
    for fname, r in rows:
        ein = r["EIN"].strip()
        eins.add(ein); by_file[fname] += 1
        if r["SUBSECTION"].strip() == "03": sub03.add(ein)
        if r["DEDUCTIBILITY"].strip() == "1": deduct1.add(ein)
        if fname == "eo_xx.csv": foreign_file.add(ein)
        status[r["STATUS"].strip()] += 1
    return {"bmf_rows_total": sum(by_file.values()), "bmf_unique_eins": len(eins),
            "bmf_subsection_03_eins": len(sub03), "bmf_deductibility_1_eins": len(deduct1),
            "bmf_eo_xx_international_file_eins": len(foreign_file),
            **{f"bmf_rows_{k}": v for k, v in sorted(by_file.items())}}, eins, sub03

def summarize_pub78(records):
    eins, foreign = set(), set()
    for ein, parts in records:
        eins.add(ein)
        country = parts[4].strip() if len(parts) > 4 else ""
        if country and country.lower() != "united states": foreign.add(ein)
    return {"pub78_unique_eins": len(eins), "pub78_non_us_country_eins": len(foreign)}, eins

def main(d):
    d = pathlib.Path(d)
    bmf, bmf_eins, sub03 = summarize_bmf(bmf_rows([d / f for f in BMF_FILES]))
    p78, p78_eins = summarize_pub78(pipe_eins(d / "data-download-pub78.txt"))
    rev = {e for e, _ in pipe_eins(d / "data-download-revocation.txt")}
    out = {**bmf, **p78,
           "pub78_eins_not_in_bmf": len(p78_eins - bmf_eins),
           "bmf_sub03_not_in_pub78": len(sub03 - p78_eins),
           "union_bmf_pub78_eins": len(bmf_eins | p78_eins),
           "auto_revocation_list_unique_eins": len(rev)}
    w = csv.writer(sys.stdout); w.writerow(["metric", "value"])
    for k, v in out.items(): w.writerow([k, v])

if __name__ == "__main__":
    main(sys.argv[1])
