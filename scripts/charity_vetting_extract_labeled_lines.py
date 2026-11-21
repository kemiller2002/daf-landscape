#!/usr/bin/env python3
"""Labeled recipient-resolution benchmark from public Form 990 Schedule I Part II lines (charity-vetting-ai deep dive).

Each Schedule I line carries the recipient's free-text name and US address as filed AND the EIN the sponsor filed.
That makes the lines a labeled dataset for the first step of every vetting decision: resolving "who is this?" to a legal
entity. Input: the IRS e-file XML cached by scripts/workflow_innovation_recipient_overlap.py (--xml-dir). Output:
  - <out-dir>/schedule-i-labeled-lines-full.csv (all lines; NOT committed, ~40 MB)
  - data/charity-vetting-ai/resolution-eval-sample.csv (seeded random sample of lines with a 9-digit EIN; committed)
Stdlib only; pure transforms; I/O at the edges.

Usage: python3 -I scripts/charity_vetting_extract_labeled_lines.py --xml-dir DIR --out-dir DIR [--sample 20000]
"""
import argparse, csv, glob, os, random, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_OUT = os.path.join(ROOT, "data", "charity-vetting-ai", "resolution-eval-sample.csv")
FIELDS = ["object_id", "recipient_name", "address", "city", "state", "zip5", "filed_ein", "irc_section", "cash_usd", "purpose"]

def local(tag): return tag.rsplit("}", 1)[-1]

def text(el, name):
    for c in el.iter():
        if local(c.tag) == name and c.text: return c.text.strip()
    return ""

def lines_of(path):
    oid = os.path.basename(path).split("_")[0]
    try: root = ET.parse(path).getroot()
    except ET.ParseError: return []
    out = []
    for el in root.iter():
        if local(el.tag) != "RecipientTable": continue
        name = " ".join(t for t in [text(el, "BusinessNameLine1Txt"), text(el, "BusinessNameLine2Txt")] if t)
        ein = "".join(ch for ch in text(el, "RecipientEIN") if ch.isdigit())
        out.append({"object_id": oid, "recipient_name": name, "address": text(el, "AddressLine1Txt"), "city": text(el, "CityNm"),
                    "state": text(el, "StateAbbreviationCd"), "zip5": text(el, "ZIPCd")[:5], "filed_ein": ein,
                    "irc_section": text(el, "IRCSectionDesc"), "cash_usd": text(el, "CashGrantAmt"), "purpose": text(el, "PurposeOfGrantTxt")})
    return out

def write(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n"); w.writeheader(); w.writerows(rows)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--xml-dir", required=True); ap.add_argument("--out-dir", required=True)
    ap.add_argument("--sample", type=int, default=20000); ap.add_argument("--seed", type=int, default=20261121)
    a = ap.parse_args()
    rows = [r for p in sorted(glob.glob(os.path.join(a.xml_dir, "*.xml"))) for r in lines_of(p)]
    write(os.path.join(a.out_dir, "schedule-i-labeled-lines-full.csv"), rows)
    labeled = [r for r in rows if len(r["filed_ein"]) == 9 and r["recipient_name"] and r["state"]]
    sample = random.Random(a.seed).sample(labeled, min(a.sample, len(labeled)))
    write(SAMPLE_OUT, sample)
    print(f"lines={len(rows)} labeled={len(labeled)} sample={len(sample)} no_ein={sum(1 for r in rows if not r['filed_ein'])}")

if __name__ == "__main__": sys.exit(main())
