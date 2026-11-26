"""REN-A1: distinct Schedule I recipients (grants > $5,000) across Ren-serviced sponsors' TY2024 Form 990 XML,
and their coverage by the IRS EO BMF and Pub 78. Pure functions; I/O in main(). Python 3 stdlib only.
Usage: python3 -I this.py <dir with {object_id}.xml> <dir with IRS eo*.csv and data-download-pub78.txt> OBJECT_ID[=LABEL] ...
XML source: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml (IRS TEOS mirror).
"""
import csv, re, sys, pathlib
NS = re.compile(r'\{[^}]*\}')

def recipients(xml_text):
    sched = re.search(r'<IRS990ScheduleI\b.*?</IRS990ScheduleI>', xml_text, re.S)
    if not sched: return []
    rows = re.findall(r'<RecipientTable>(.*?)</RecipientTable>', sched.group(0), re.S)
    def one(r):
        ein = re.search(r'<RecipientEIN>(\d+)</RecipientEIN>', r)
        amt = re.search(r'<CashGrantAmt>(\d+)</CashGrantAmt>', r)
        country = re.search(r'<ForeignAddress>', r)
        return (ein.group(1) if ein else None, int(amt.group(1)) if amt else 0, bool(country))
    return [one(r) for r in rows]

def load_eins(irs_dir):
    bmf = set()
    for f in ("eo1.csv","eo2.csv","eo3.csv","eo4.csv","eo_pr.csv","eo_xx.csv"):
        with open(irs_dir / f, newline="", encoding="latin-1") as fh:
            bmf.update(r["EIN"].strip() for r in csv.DictReader(fh))
    with open(irs_dir / "data-download-pub78.txt", encoding="latin-1") as fh:
        p78 = {l.split("|")[0].strip() for l in fh if l[:1].isdigit()}
    return bmf, p78

def summarize(label, rows, bmf, p78):
    eins = {e for e, _, _ in rows if e}
    return {"label": label, "rows": len(rows), "rows_without_ein": sum(1 for e,_,_ in rows if not e),
            "foreign_address_rows": sum(1 for *_, f in rows if f), "distinct_eins": len(eins),
            "eins_in_bmf": len(eins & bmf), "eins_in_pub78": len(eins & p78),
            "eins_in_neither": len(eins - bmf - p78), "cash_total": sum(a for _, a, _ in rows)}, eins

def main(xml_dir, irs_dir, specs):
    xml_dir, irs_dir = pathlib.Path(xml_dir), pathlib.Path(irs_dir)
    bmf, p78 = load_eins(irs_dir)
    out, all_eins = [], []
    for s in specs:
        oid, _, label = s.partition("=")
        summ, eins = summarize(label or oid, recipients((xml_dir / f"{oid}.xml").read_text(errors="ignore")), bmf, p78)
        out.append(summ); all_eins.append(eins)
    union = set().union(*all_eins)
    inter = set.intersection(*all_eins) if all_eins else set()
    w = csv.DictWriter(sys.stdout, fieldnames=list(out[0].keys())); w.writeheader(); [w.writerow(r) for r in out]
    print(f"union_distinct_eins,{len(union)}\nintersection_distinct_eins,{len(inter)}\nunion_in_bmf,{len(union & bmf)}\nunion_in_pub78,{len(union & p78)}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
