"""Spend distribution of DAF sponsors by DAF-asset band (FY2024 Form 990 Part IX and Part VII-B contractor lines).
Reads repository CSVs only; prints tables used in research/commercial-opportunity/market-validation/demand-signals-and-process-economics.md.
Usage: python3 -I scripts/commercial_sponsor_spend_distribution.py (from repo root)
"""
import csv,collections,statistics as st
D='data/mission-2026-11-14/'  # run from the repository root
cs=list(csv.DictReader(open(D+'sponsor-cost-structure.csv')))
def f(v):
    try: return float(v)
    except: return None
rows=[x for x in cs if x['fiscal_year']=='2024' and x['size_band_daf_assets']!='z no DAF value' and x['subtype']!='Universities and Healthcare']
print(collections.Counter(x['subtype'] for x in cs).most_common(12))
bands=sorted(set(x['size_band_daf_assets'] for x in rows))
print('PART IX FY2024 by DAF-asset band (all categories ex univ/health)')
print('band|n|median opex ex-invest|median IT l14 (incl zeros)|share IT>0|median outside svcs ex 11f (11a-e,g)|median 11g other fees|median outside-ex-invest share of opex|median IT share of opex')
for b in bands:
    g=[x for x in rows if x['size_band_daf_assets']==b]
    def med(k): 
        v=[f(x[k]) or 0 for x in g]; return st.median(v) if v else None
    out=[]
    for x in g:
        o=sum((f(x[k]) or 0) for k in ['fees_mgmt_l11a','fees_legal_l11b','fees_accounting_l11c','fees_prof_fundraising_l11e','fees_other_l11g'])
        out.append(o)
    oc=[f(x['operating_cost_ex_invest_mgmt']) or 0 for x in g]
    sh=[o/c for o,c in zip(out,oc) if c>0]
    its=[ (f(x['it_l14']) or 0)/c for x,c in zip(g,oc) if c>0]
    print(b,len(g),round(med('operating_cost_ex_invest_mgmt')),round(med('it_l14')),round(sum(1 for x in g if (f(x['it_l14']) or 0)>0)/len(g),2),round(st.median(out)),round(med('fees_other_l11g')),round(st.median(sh),3),round(st.median(its),3),sep='|')
# Contractors join
cc=list(csv.DictReader(open(D+'form990-contractors-harvest-full.csv')))
band={(x['ein'],x['fiscal_year']):x['size_band_daf_assets'] for x in cs}
TECH={'technology_services','daf_tech_admin_vendor','daf_tech_vendor','enterprise_software','giving_platform_or_outsourced_admin','payment_processor','investment_accounting_software','grant_admin_due_diligence'}
CONS={'consulting','philanthropic_advisory','investment_consultant','staffing','administration'}
agg=collections.defaultdict(lambda: collections.Counter())
spons=collections.defaultdict(set); spons_t=collections.defaultdict(set); spons_c=collections.defaultdict(set)
tot_s=collections.defaultdict(set)
miss=0
for x in cc:
    if x['fiscal_year'] not in ('2022','2023','2024'): continue
    b=band.get((x['ein'],x['fiscal_year']))
    if not b: miss+=1; continue
    amt=f(x['compensation']) or 0
    cat=x['vendor_category']
    grp='tech' if cat in TECH else 'consult/admin' if cat in CONS else 'invest' if cat in ('investment_or_financial','financial_firm','investment_manager') else 'other'
    agg[b][grp]+=amt; agg[b]['all']+=amt
    tot_s[b].add(x['ein'])
    if grp=='tech': spons_t[b].add(x['ein'])
    if grp=='consult/admin': spons_c[b].add(x['ein'])
print('unmatched contractor lines',miss)
print('PART VII-B FY2022-24 contractor lines by band: total $, tech $, consult $, invest $, #sponsors w/ any, w/ tech, w/consult')
for b in sorted(agg):
    a=agg[b]
    print(b,round(a['all']/1e6,1),round(a['tech']/1e6,1),round(a['consult/admin']/1e6,1),round(a['invest']/1e6,1),len(tot_s[b]),len(spons_t[b]),len(spons_c[b]),sep='|')
# top tech vendors
tv=collections.Counter(); 
for x in cc:
    if x['vendor_category'] in TECH and x['fiscal_year'] in ('2022','2023','2024'): tv[x['vendor_group']]+=f(x['compensation']) or 0
print([(k,round(v/1e6,1)) for k,v in tv.most_common(15)])
# by sponsor type
ts=collections.defaultdict(collections.Counter)
for x in cc:
    if x['fiscal_year'] in ('2022','2023','2024'):
        cat=x['vendor_category']; grp='tech' if cat in TECH else 'consult/admin' if cat in CONS else 'x'
        ts[x['sponsor_type']][grp]+=f(x['compensation']) or 0; ts[x['sponsor_type']]['all']+=f(x['compensation']) or 0
for k,v in ts.items(): print(k,{a:round(b/1e6,1) for a,b in v.items()})
print('=== CF + National only, contractor lines FY2022-24 ===')
sub={(x['ein'],x['fiscal_year']):x['subtype'] for x in cs}
agg=collections.defaultdict(collections.Counter); S=collections.defaultdict(set); St=collections.defaultdict(set); Sc=collections.defaultdict(set)
for x in cc:
    if x['fiscal_year'] not in ('2022','2023','2024') or x['sponsor_type']=='Single Issue Charity': continue
    b=band.get((x['ein'],x['fiscal_year'])); amt=f(x['compensation']) or 0; cat=x['vendor_category']
    grp='tech' if cat in TECH else 'consult/admin' if cat in CONS else 'invest' if cat in ('investment_or_financial','financial_firm','investment_manager') else 'other'
    k=(x['sponsor_type'],b); agg[k][grp]+=amt; agg[k]['all']+=amt; S[k].add(x['ein'])
    if grp=='tech': St[k].add(x['ein'])
    if grp=='consult/admin': Sc[k].add(x['ein'])
for k in sorted(agg):
    a=agg[k]; print(k,round(a['all']/1e6,1),round(a['tech']/1e6,1),round(a['consult/admin']/1e6,1),round(a['invest']/1e6,1),len(S[k]),len(St[k]),len(Sc[k]),sep='|')
# Part IX CF only FY2024
print('=== CF only FY2024 Part IX ===')
g0=[x for x in cs if x['fiscal_year']=='2024' and x['type']=='Community Foundation' and x['size_band_daf_assets']!='z no DAF value']
for b in sorted(set(x['size_band_daf_assets'] for x in g0)):
    g=[x for x in g0 if x['size_band_daf_assets']==b]
    out=[sum((f(x[k]) or 0) for k in ['fees_mgmt_l11a','fees_legal_l11b','fees_accounting_l11c','fees_prof_fundraising_l11e','fees_other_l11g']) for x in g]
    it=[f(x['it_l14']) or 0 for x in g]
    oc=[f(x['operating_cost_ex_invest_mgmt']) or 0 for x in g]
    p=lambda v,q: sorted(v)[int(q*(len(v)-1))]
    print(b,len(g),round(st.median(oc)),round(st.median(it)),round(p(it,.75)),round(st.median(out)),round(p(out,.75)),round(sum(it)/1e6,1),round(sum(out)/1e6,1),sep='|')
