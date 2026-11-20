"""Scan DOJ press releases (public API /api/v1/press_releases.json, robots-allowed) newest-first back to 2021-01-01,
keeping only releases whose title/body matches DAF terms. Stdlib, functional style.
Usage: python3 -I doj_scan.py OUT_JSONL STATE_FILE START_PAGE END_PAGE (END exclusive; stops early at cutoff)"""
import sys, os, json, re, time, ssl, urllib.request, datetime
UA = "research-script/1.0"
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
CUTOFF = 1609459200  # 2021-01-01 UTC
API = "https://www.justice.gov/api/v1/press_releases.json?pagesize=50&sort=date&direction=DESC&page={}"
TERMS = re.compile(r"donor[\s\-]+advised|\bDAFs?\b|charitable gift fund|fidelity charitable|schwab charitable|dafgiving360|"
                   r"vanguard charitable|national philanthropic trust|american endowment foundation|renaissance charitable|"
                   r"national christian foundation|goldman sachs philanthropy fund|global impact funding trust|community foundation", re.I)
STRIP = re.compile(r"<[^>]+>")

def get(page, tries=4):
    req = urllib.request.Request(API.format(page), headers={"User-Agent": UA})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=90, context=CTX) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(5 * (i + 1))
    return None

def ts(rel):
    """Release date as epoch seconds, or None when the API gives no date."""
    d = str(rel.get("date") or "").strip()
    return int(d) if d.isdigit() else None


def keep(rel):
    return ts(rel) is None or ts(rel) >= CUTOFF


def hits(rel):
    text = STRIP.sub(" ", (rel.get("title") or "") + " " + (rel.get("body") or ""))
    found = [m for m in TERMS.finditer(text)]
    snips = [text[max(0, m.start() - 250): m.end() + 250] for m in found[:6]]
    return dict(date=(datetime.datetime.fromtimestamp(ts(rel), datetime.timezone.utc).date().isoformat() if ts(rel) is not None else ""), title=STRIP.sub("", rel.get("title") or ""),
                url=rel.get("url"), component=[c.get("name") for c in (rel.get("component") or []) if isinstance(c, dict)],
                terms=sorted({m.group(0).lower() for m in found}), snippets=snips) if found else None

def main(out, state, start, end):
    page = int(open(state).read()) if os.path.exists(state) else start
    scanned = 0
    while True:
        d = get(page)
        if d is None:
            print("failed page", page, flush=True); break
        res = d.get("results") or []
        if not res: break
        rows = [h for h in map(hits, filter(keep, res)) if h]
        with open(out, "a") as f:
            f.writelines(json.dumps(r) + "\n" for r in rows)
        scanned += sum(1 for r in res if keep(r))
        with open(state, "w") as f: f.write(str(page + 1))
        with open(state + ".count", "a") as f: f.write(f"{page},{len(res)},{sum(1 for r in res if keep(r))},{len(rows)},{min((ts(r) for r in res if ts(r) is not None), default='')}\n")
        if all(ts(r) is not None and ts(r) < CUTOFF for r in res[-5:]) or page + 1 >= end: break
        page += 1
        time.sleep(1)
    print("done at page", page, flush=True)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
