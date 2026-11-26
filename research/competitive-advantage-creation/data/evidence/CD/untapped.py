import csv, sys, os
from collections import defaultdict
bmfdir, panel, out = sys.argv[1], sys.argv[2], sys.argv[3]
sponsors = {r["ein"].zfill(9) for r in csv.DictReader(open(panel))} | (set(open(sys.argv[4]).read().split()) if len(sys.argv)>4 else set())
cats = {
 'higher_ed_B40_B43_B50': lambda r: r['NTEE_CD'][:3] in ('B40','B41','B42','B43','B50'),
 'govt_university_support_fc13': lambda r: r['FOUNDATION']=='13',
 'education_support_B11_B12': lambda r: r['NTEE_CD'][:3] in ('B11','B12'),
 'hospitals_E20_E22_E24': lambda r: r['NTEE_CD'][:3] in ('E20','E21','E22','E24'),
 'health_support_E11_E12': lambda r: r['NTEE_CD'][:3] in ('E11','E12'),
 'community_foundations_T31': lambda r: r['NTEE_CD'].startswith('T31'),
 'public_foundations_T30': lambda r: r['NTEE_CD'].startswith('T30'),
 'federated_giving_T70': lambda r: r['NTEE_CD'].startswith('T70'),
 'religion_support_X11_X12': lambda r: r['NTEE_CD'][:3] in ('X11','X12'),
}
thr = [10e6, 50e6, 100e6, 1e9]
res = defaultdict(lambda: defaultdict(int))
seen=set()
for i in (1,2,3,4):
  with open(os.path.join(bmfdir,f'eo{i}.csv'),newline='',encoding='latin-1') as f:
    for r in csv.DictReader(f):
      if r['SUBSECTION']!='03' or r['FOUNDATION'] in ('02','03','04'): continue
      ein=r['EIN'].zfill(9)
      if ein in seen: continue
      seen.add(ein)
      try: a=float(r['ASSET_AMT'] or 0)
      except: a=0
      for k,fn in cats.items():
        if fn(r):
          for t in thr:
            if a>=t:
              res[k][f'ge{int(t/1e6)}m']+=1
              if ein in sponsors: res[k][f'ge{int(t/1e6)}m_in_daf_panel']+=1
w=csv.writer(open(out,'w',newline=''))
w.writerow(['category','asset_threshold_usd','public_charity_entities','of_which_in_dafrc_sponsor_panel','not_in_panel'])
for k,v in res.items():
  for t in thr:
    key=f'ge{int(t/1e6)}m'
    w.writerow([k,int(t),v[key],v[key+'_in_daf_panel'],v[key]-v[key+'_in_daf_panel']])
    print(k,key,v[key],v[key+'_in_daf_panel'])
