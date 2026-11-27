import csv, sys, math
out = sys.argv[1]
V = {'low':120,'base':247,'high':370}          # per-account all-in program cost incl licence
F = {'partner_hosted':{'low':5000,'base':10000,'high':15000},
     'existing_charity':{'low':13000,'base':25000,'high':40000},
     'new_sponsor':{'low':60000,'base':90000,'high':140000}}
B = [50000,133000,250000]
f = [0.006,0.010,0.015]
rows=[]
for host,fx in F.items():
  for fk,fv in fx.items():
    for vk,vv in V.items():
      for b in B:
        for r in f:
          m=b*r-vv
          n = math.ceil(fv/m) if m>0 else None
          rows.append(dict(host_model=host,fixed_case=fk,fixed_usd=fv,var_case=vk,var_usd=vv,avg_balance=b,fee_rate=r,
            margin_per_acct=round(m,2),breakeven_accounts=n if n else 'never',
            breakeven_aua_usd=n*b if n else 'never'))
with open(out,'w',newline='') as fh:
  w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows:
  if r['fixed_case']==r['var_case'] or (r['fixed_case']=='base' and r['var_case']=='base'):
    if r['fixed_case']=='base' or r['avg_balance']==133000:
      print(r['host_model'],r['fixed_case'],r['var_case'],r['avg_balance'],r['fee_rate'],r['breakeven_accounts'],r['breakeven_aua_usd'])
