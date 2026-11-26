"""Cross-file consistency checks (pure functions; paths as args)."""
import csv, sys, os, collections, datetime as dt
D=sys.argv[1]
def pipe(p):
    with open(p,encoding='latin-1') as f:
        return [l.rstrip('\n').split('|') for l in f if l.strip()]
bmf={}
for fn in ('eo1.csv','eo2.csv','eo3.csv','eo4.csv'):
    with open(os.path.join(D,fn),newline='',encoding='latin-1') as f:
        for r in csv.DictReader(f): bmf[r['EIN']]=r
p78={r[0]:r for r in pipe(os.path.join(D,'data-download-pub78.txt'))}
rev=pipe(os.path.join(D,'data-download-revocation.txt'))
c3={e:r for e,r in bmf.items() if r['SUBSECTION']=='03'}
out={}
out['c3_in_bmf']=len(c3)
out['c3_in_pub78']=sum(1 for e in c3 if e in p78)
out['c3_not_in_pub78_by_affil']=collections.Counter(c3[e]['AFFILIATION'] for e in c3 if e not in p78).most_common()
out['c3_not_in_pub78_by_found']=collections.Counter(c3[e]['FOUNDATION'] for e in c3 if e not in p78).most_common(8)
out['c3_affil9_in_pub78']=sum(1 for e,r in c3.items() if r['AFFILIATION']=='9' and e in p78)
out['c3_affil9']=sum(1 for r in c3.values() if r['AFFILIATION']=='9')
out['pub78_not_in_bmf']=sum(1 for e in p78 if e not in bmf)
out['pub78_not_in_bmf_codes']=collections.Counter(p78[e][5] for e in p78 if e not in bmf).most_common(6)
def d(s):
    try: return dt.datetime.strptime(s,'%d-%b-%Y').date()
    except: return None
# latest revocation row per EIN
lat={}
for r in rev:
    e=r[0]; rd=d(r[9])
    if e not in lat or (rd and lat[e][0] and rd>lat[e][0]): lat[e]=(rd,r[11].strip(),d(r[10]))
unrein={e for e,v in lat.items() if not v[1]}
out['revoked_unreinstated']=len(unrein)
out['unreinstated_in_bmf']=sum(1 for e in unrein if e in bmf)
out['unreinstated_in_pub78']=sum(1 for e in unrein if e in p78)
out['reinstated_in_pub78']=sum(1 for e,v in lat.items() if v[1] and e in p78)
# latency: posting minus revocation date for 2026 postings
lags=sorted((v[2]-v[0]).days for e,v in lat.items() if v[0] and v[2] and v[2].year==2026)
out['posting_lag_days_2026_p10_p50_p90']=(lags[len(lags)//10],lags[len(lags)//2],lags[9*len(lags)//10]) if lags else None
# name compare
trunc=sum(1 for e in p78 if e in bmf and len(p78[e][1])>70)
out['pub78_names_over70_also_in_bmf']=trunc
out['bmf_status']=collections.Counter(r['STATUS'] for r in c3.values()).most_common()
import pprint; pprint.pprint(out,width=150)
