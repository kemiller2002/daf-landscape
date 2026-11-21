"""GSA CALC ceiling-rate percentiles for consulting labour categories (benchmark for DAF advisory pricing).
Queries the public GSA CALC v3 API. Usage: python3 -I scripts/commercial_gsa_rate_benchmarks.py
"""
import json, urllib.request, urllib.parse, statistics, sys
def fetch(kw, pages=20, size=100):
    out=[]
    for p in range(1,pages+1):
        u="https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?"+urllib.parse.urlencode({"keyword":kw,"page":p,"page_size":size,"exclude":""})
        try:
            d=json.load(urllib.request.urlopen(u,timeout=60))
        except Exception as e:
            print("err",e,file=sys.stderr);break
        h=d["hits"]["hits"]
        if not h: break
        out+= [x["_source"] for x in h]
        total=d["hits"]["total"]["value"]
        if len(out)>=total: break
    return out, total
def q(v,p):
    v=sorted(v); k=(len(v)-1)*p; f=int(k); c=min(f+1,len(v)-1); return v[f]+(v[c]-v[f])*(k-f)
for kw in ["senior consultant","management consultant","principal consultant","engagement manager"]:
    rows,total=fetch(kw)
    for label,filt in [("all",lambda r:True),("SIN541611",lambda r:"541611" in (r.get("sin") or ""))]:
        v=[r["current_price"] for r in rows if r.get("current_price") and filt(r)]
        if len(v)>=5:
            print(f"{kw}|{label}|n={len(v)} of total_hits={total}|p25={q(v,.25):.0f}|median={q(v,.5):.0f}|p75={q(v,.75):.0f}|p90={q(v,.9):.0f}")
