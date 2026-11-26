import json, subprocess, sys, os, re
from collections import Counter, defaultdict
from datetime import datetime
base='/home/user/echelon-components'
tot=Counter(); mids=Counter(); obs=defaultdict(list); per=[]
for r in sorted(os.listdir(base)):
    fs=[f for f in subprocess.run(['git','-C',f'{base}/{r}','ls-files'],capture_output=True,text=True).stdout.splitlines() if re.search(r'telemetry/executions/.*\.json$',f)]
    if not fs: continue
    durs=[]; costed=0; tok=0; cost=0.0
    for f in fs:
        try: d=json.load(open(f'{base}/{r}/{f}'))
        except Exception: continue
        try:
            s=datetime.fromisoformat(d['startedAt'].replace('Z','+00:00')); e=datetime.fromisoformat((d.get('finalizedAt') or d['startedAt']).replace('Z','+00:00')); durs.append((e-s).total_seconds())
        except Exception: pass
        has=False
        for m in d.get('metrics',[]):
            mids[m['id']]+=1
            if re.search(r'cost|token',m['id']) and m.get('value') is not None:
                obs[m['id']].append((r,m['value'],m.get('quality'),m.get('unit')))
                has=True
                if m['id'].startswith('cost') : cost+=float(m['value'] or 0)
        costed+=has
    per.append((r,len(fs),costed,round(sum(durs)/3600,1),round(sorted(durs)[len(durs)//2]/60,1) if durs else None, round(cost,2)))
print('repo records records_with_cost_or_token_metric sum_exec_hours median_exec_min sum_cost_metric')
for p in per: print(*p)
print(mids.most_common(40))
for k,v in obs.items(): print(k,len(v),v[:5])
