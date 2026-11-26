import csv, sys, os
bmfdir, panel, extra = sys.argv[1:4]
s = {r['ein'].zfill(9) for r in csv.DictReader(open(panel))} | set(open(extra).read().split())
eh = lambda r: r['FOUNDATION'] in ('12','13') or r['NTEE_CD'][:3] in ('B40','B41','B42','B43','B50','B11','B12','E20','E21','E22','E24','E11','E12')
res={}
seen=set()
for i in (1,2,3,4):
  for r in csv.DictReader(open(os.path.join(bmfdir,f'eo{i}.csv'),newline='',encoding='latin-1')):
    e=r['EIN'].zfill(9)
    if e in seen or r['SUBSECTION']!='03' or r['FOUNDATION'] in ('02','03','04') or not eh(r): continue
    seen.add(e)
    try: a=float(r['ASSET_AMT'] or 0)
    except: a=0
    for t in (10e6,50e6,100e6,1e9):
      if a>=t:
        k=int(t/1e6); res.setdefault(k,[0,0]); res[k][0]+=1; res[k][1]+= e in s
print(res)
