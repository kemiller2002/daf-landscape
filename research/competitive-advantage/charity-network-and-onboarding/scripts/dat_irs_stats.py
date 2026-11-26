"""Pure summaries of IRS bulk files (paths passed as args). stdlib only."""
import csv, sys, collections, os, datetime as dt
from functools import reduce

def rows_csv(path):
    with open(path, newline='', encoding='latin-1') as f:
        yield from csv.DictReader(f)

def rows_pipe(path):
    with open(path, encoding='latin-1') as f:
        for line in f:
            line=line.rstrip('\n')
            if line.strip(): yield line.split('|')

def count(it, key): return collections.Counter(key(r) for r in it)

def bmf(d):
    files=[os.path.join(d,f) for f in ('eo1.csv','eo2.csv','eo3.csv','eo4.csv')]
    rows=[r for p in files for r in rows_csv(p)]
    eins=collections.Counter(r['EIN'] for r in rows)
    c3=[r for r in rows if r['SUBSECTION']=='03']
    return {
      'rows':len(rows),'unique_ein':len(eins),'dup_ein':sum(1 for v in eins.values() if v>1),
      'subsection_top':count(rows,lambda r:r['SUBSECTION']).most_common(6),
      'c3_rows':len(c3),
      'c3_foundation':sorted(count(c3,lambda r:r['FOUNDATION']).items()),
      'affiliation':sorted(count(rows,lambda r:r['AFFILIATION']).items()),
      'group_nonzero':sum(1 for r in rows if r['GROUP'] not in ('','0000')),
      'c3_group_nonzero':sum(1 for r in c3 if r['GROUP'] not in ('','0000')),
      'status':sorted(count(rows,lambda r:r['STATUS']).items()),
      'deductibility':sorted(count(rows,lambda r:r['DEDUCTIBILITY']).items()),
      'c3_filing_req':count(c3,lambda r:r['FILING_REQ_CD']).most_common(8),
      'ruling_year_recent':sorted((k,v) for k,v in count(rows,lambda r:r['RULING'][:4]).items() if k>='2020'),
      'ruling_2026_months':sorted((k,v) for k,v in count(rows,lambda r:r['RULING']).items() if k.startswith('2026')),
      'name_maxlen':max(len(r['NAME']) for r in rows),
      'name_len_35':sum(1 for r in rows if len(r['NAME'])>=35),
    }

def pub78(p):
    rows=list(rows_pipe(p))
    return {'rows':len(rows),'unique_ein':len({r[0] for r in rows}),'codes':count(rows,lambda r:r[5] if len(r)>5 else '?').most_common(20),
            'countries':count(rows,lambda r:r[4] if len(r)>4 else '?').most_common(5)}

def parse_d(s):
    try: return dt.datetime.strptime(s,'%d-%b-%Y').date()
    except Exception: return None

def revocation(p):
    rows=list(rows_pipe(p))
    rev=[parse_d(r[9]) for r in rows]; post=[parse_d(r[10]) for r in rows]
    rein=[r[11] for r in rows]
    pm=collections.Counter(d.strftime('%Y-%m') for d in post if d)
    return {'rows':len(rows),'unique_ein':len({r[0] for r in rows}),'with_reinstatement':sum(1 for x in rein if x.strip()),
            'ncols':collections.Counter(len(r) for r in rows).most_common(3),
            'posting_by_year':sorted(collections.Counter(d.year for d in post if d).items())[-8:],
            'posting_months_2025_26':sorted((k,v) for k,v in pm.items() if k>='2025'),
            'rev_by_year':sorted(collections.Counter(d.year for d in rev if d).items())[-6:],
            'max_post':max(d for d in post if d)}

def epostcard(p):
    rows=list(rows_pipe(p))
    return {'rows':len(rows),'unique_ein':len({r[0] for r in rows}),'tax_year':sorted(collections.Counter(r[1] for r in rows).items())[-6:],
            'terminated_T':collections.Counter(r[3] for r in rows).most_common(3)}

def index(p):
    rows=list(rows_csv(p))
    return {'rows':len(rows),'unique_ein':len({r['EIN'] for r in rows}),'types':count(rows,lambda r:r['RETURN_TYPE']).most_common(),
            'batches':sorted(count(rows,lambda r:r['XML_BATCH_ID']).items())}

if __name__=='__main__':
    d=sys.argv[1]
    import pprint
    for name,fn,arg in [('BMF',bmf,d),('PUB78',pub78,os.path.join(d,'data-download-pub78.txt')),
                        ('REVOCATION',revocation,os.path.join(d,'data-download-revocation.txt')),
                        ('EPOSTCARD',epostcard,os.path.join(d,'data-download-epostcard.txt')),
                        ('INDEX2026',index,os.path.join(d,'index_2026.csv')),('INDEX2025',index,os.path.join(d,'index_2025.csv'))]:
        print('==',name); pprint.pprint(fn(arg),width=160)
