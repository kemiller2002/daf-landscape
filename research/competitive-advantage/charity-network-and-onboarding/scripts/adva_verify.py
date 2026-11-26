"""ADVA independent re-derivation of selected IRS counts. stdlib only."""
import csv, sys, os, datetime as dt, statistics, collections
d=sys.argv[1]
def bmf():
    for f in ('eo1.csv','eo2.csv','eo3.csv','eo4.csv'):
        with open(os.path.join(d,f),newline='',encoding='latin-1') as fh:
            yield from csv.DictReader(fh)
rows={r['EIN']:r for r in bmf()}
p78={}
with open(os.path.join(d,'data-download-pub78.txt'),encoding='latin-1') as fh:
    for l in fh:
        p=l.rstrip('\n').split('|')
        if p[0].isdigit(): p78[p[0]]=p
c3=[r for r in rows.values() if r['SUBSECTION']=='03']
sub=[r for r in c3 if r['AFFILIATION']=='9']
print('c3 subordinates aff9',len(sub),'in pub78',sum(1 for r in sub if r['EIN'] in p78))
notp=[r for r in c3 if r['EIN'] not in p78]
print('c3 not in p78',len(notp),'of which aff9',sum(1 for r in notp if r['AFFILIATION']=='9'),'church fc10',sum(1 for r in notp if r['FOUNDATION']=='10'),
      'neither', sum(1 for r in notp if r['AFFILIATION']!='9' and r['FOUNDATION']!='10'))
# churches overall
print('c3 fc10 total',sum(1 for r in c3 if r['FOUNDATION']=='10'),'fc10 in p78',sum(1 for r in c3 if r['FOUNDATION']=='10' and r['EIN'] in p78))
# filing_req 06 = church not required
# revocation
def pd(s):
    try: return dt.datetime.strptime(s.strip(),'%d-%b-%Y').date()
    except: return None
latest={}
lags=[]
with open(os.path.join(d,'data-download-revocation.txt'),encoding='latin-1') as fh:
    for l in fh:
        p=l.rstrip('\n').split('|')
        if len(p)<12: continue
        rv,po,ri=pd(p[9]),pd(p[10]),p[11].strip()
        if po and po.year==2026 and rv: lags.append((po-rv).days)
        k=p[0]
        if k not in latest or (rv and latest[k][0] and rv>latest[k][0]): latest[k]=(rv,po,ri)
lags.sort()
q=lambda x: lags[int(x*(len(lags)-1))]
print('2026 posting lag n',len(lags),'p10',q(.1),'p50',q(.5),'p90',q(.9),'min',lags[0],'max',lags[-1])
print('lag dist top',collections.Counter(lags).most_common(5))
norein=[e for e,(rv,po,ri) in latest.items() if not ri]
inb=[e for e in norein if e in rows]
print('latest rev no reinstatement still in BMF',len(inb),'also p78',sum(1 for e in inb if e in p78))
# ruling date of those vs revocation date
newer=sum(1 for e in inb if rows[e]['RULING'][:6] and latest[e][0] and rows[e]['RULING'][:6] > latest[e][0].strftime('%Y%m'))
print('of which BMF ruling after revocation date',newer)
