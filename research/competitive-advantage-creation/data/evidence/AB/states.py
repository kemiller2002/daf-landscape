import csv,sys
L,B,H=0,1,2
# per state: dict category -> (cash(l,b,h), econ(l,b,h), asm)
def rec_live(shared=1.0):
    return {
 'maintenance/yr':((40e3,120e3,250e3),(40e3,120e3,250e3),'P3-ASM-AB010;P3-ASM-AB011'),
 'security/yr':((20e3*shared,50e3*shared,120e3*shared),(20e3*shared,50e3*shared,120e3*shared),'P3-ASM-AB012'+('' if shared==1.0 else ';P3-ASM-AB029')),
 'compliance_recurring/yr':((30e3*shared,80e3*shared,180e3*shared),(30e3*shared,80e3*shared,180e3*shared),'P3-ASM-AB013'+('' if shared==1.0 else ';P3-ASM-AB029')),
 'infrastructure/yr':((20e3*shared,45e3*shared,110e3*shared),(20e3*shared,45e3*shared,110e3*shared),'P3-ASM-AB014'+('' if shared==1.0 else ';P3-ASM-AB029')),
 'support/yr':((0,40e3,100e3),(0,40e3,100e3),'P3-ASM-AB015'),
 'insurance/yr':((30e3,70e3,160e3),(30e3,70e3,160e3),'P3-ASM-AB016'),
 'corporate_admin/yr':((25e3,60e3,150e3),(25e3,60e3,150e3),'P3-ASM-AB017'),
}
FOUNDER_PRE=((0,0,60e3),(190356,222482,273473),'P3-ASM-AB018')
FOUNDER_LIVE=((0,60e3,150e3),(190356,222482,273473),'P3-ASM-AB018')
def onetime_first(cac,impl,comp,legal,wc):
    return {'customer_acquisition':(cac,cac,'P3-ASM-AB019'),'implementation':(impl,impl,'P3-ASM-AB020'),
            'compliance_onetime':(comp,comp,'P3-ASM-AB021'),'legal_and_corporate_onetime':(legal,legal,'P3-ASM-AB022'),
            'working_capital':(wc,wc,'P3-ASM-AB023')}
PRE_RUN=((30e3,105e3,280e3),(30e3,105e3,280e3),'P3-ASM-AB024')
STD_FIRST=onetime_first((15e3,30e3,60e3),(35e3,75e3,150e3),(20e3,45e3,100e3),(20e3,60e3,150e3),(25e3,75e3,200e3))
states=[
 ('S1','Unbound does not exist (no requirements)',dict(sunk=((0,0,0),(0,0,0)),dev=((300e3,700e3,1400e3),(1500e3,2150e3,4000e3)),pre=(18,27,42),first=STD_FIRST,shared=1.0)),
 ('S2','Requirements and architecture exist (today)',dict(sunk=((10e3,30e3,60e3),(100e3,200e3,400e3)),dev=((250e3,600e3,1200e3),(1350e3,1940e3,3600e3)),pre=(15,24,36),first=STD_FIRST,shared=1.0)),
 ('S3','Functionally complete, not production-hardened',dict(sunk=((260e3,630e3,1260e3),(1450e3,2140e3,4000e3)),dev=((40e3,120e3,250e3),(150e3,350e3,600e3)),pre=(9,15,24),first=STD_FIRST,shared=1.0)),
 ('S4','Production-ready, no customers',dict(sunk=((300e3,750e3,1510e3),(1600e3,2490e3,4600e3)),dev=((10e3,40e3,120e3),(30e3,100e3,250e3)),pre=(9,15,24),first=STD_FIRST,shared=1.0)),
 ('S5','Successful pilot (one referenceable live sponsor)',dict(sunk=((550e3,1500e3,3500e3),(2100e3,3500e3,6500e3)),dev=((0,60e3,200e3),(50e3,300e3,600e3)),pre=(0,0,0),first=onetime_first((5e3,20e3,40e3),(35e3,75e3,150e3),(0,15e3,60e3),(0,15e3,50e3),(25e3,75e3,200e3)),shared=1.0)),
 ('S6','Reusable onboarding packages exist',dict(sunk=((600e3,1600e3,3700e3),(2200e3,3700e3,6900e3)),dev=((0,40e3,150e3),(30e3,200e3,500e3)),pre=(0,0,0),first=onetime_first((5e3,20e3,40e3),(10e3,30e3,80e3),(0,15e3,60e3),(0,15e3,50e3),(25e3,75e3,200e3)),shared=1.0)),
 ('S7','Operates on Echelon shared infrastructure (cost shared with >=1 other revenue-bearing product)',dict(sunk=((600e3,1600e3,3700e3),(2200e3,3700e3,6900e3)),dev=((0,40e3,150e3),(30e3,200e3,500e3)),pre=(0,0,0),first=onetime_first((5e3,20e3,40e3),(10e3,30e3,80e3),(0,15e3,60e3),(0,15e3,50e3),(25e3,75e3,200e3)),shared=0.6)),
]
GOLIVE=(3,6,9)
CONT=(0.15,0.25,0.40)
OPP=(0.05,0.10,0.15)
rows=[];tot={}
for sid,name,d in states:
    R=[]
    R.append(('sunk_cost (USD one-time; sunk, excluded from incremental)',)+d['sunk']+('P3-ASM-AB001',))
    R.append(('incremental_development (USD one-time)',)+d['dev']+('P3-ASM-AB002;P3-ASM-AB003',))
    for k,(c,e,a) in d['first'].items(): R.append((k+' (USD one-time)',c,e,a))
    R.append(('pre_revenue_run_rate/yr (all recurring before first contract)',)+PRE_RUN)
    R.append(('duration_pre_revenue_months (months, not USD)',d['pre'],d['pre'],'P3-ASM-AB025'))
    R.append(('duration_golive_to_first_invoice_months (months, not USD)',GOLIVE,GOLIVE,'P3-ASM-AB026'))
    live=rec_live(d['shared'])
    for k,(c,e,a) in live.items(): R.append((k,c,e,a))
    fp = FOUNDER_PRE if d['pre'][1]>0 else FOUNDER_LIVE
    R.append(('founder_compensation/yr',fp[0],fp[1],fp[2]))
    # totals to first invoice (cash), per level
    cash=[];econ=[]
    for i in range(3):
        one=d['dev'][0][i]+sum(v[0][i] for v in d['first'].values())
        onee=d['dev'][1][i]+sum(v[1][i] for v in d['first'].values())
        pre=PRE_RUN[0][i]*d['pre'][i]/12
        liver=sum(v[0][i] for v in live.values())*GOLIVE[i]/12
        fcash=FOUNDER_PRE[0][i]*d['pre'][i]/12+FOUNDER_LIVE[0][i]*GOLIVE[i]/12
        sub=one+pre+liver+fcash
        cont=CONT[i]*sub
        c=sub+cont
        months=d['pre'][i]+GOLIVE[i]
        fe=FOUNDER_PRE[1][i]*months/12
        opp=OPP[i]*c*months/12/2
        e=onee+pre+liver+cont+fe+opp
        cash.append(c);econ.append(e)
        if i==0: contv=[None]*3; 
    R.append(('contingency (USD one-time; % of incremental cash to first invoice: 15/25/40)',
              tuple(round(CONT[i]*(cash[i]/(1+CONT[i]))) for i in range(3)),tuple(round(CONT[i]*(cash[i]/(1+CONT[i]))) for i in range(3)),'P3-ASM-AB027'))
    R.append(('economic_opportunity_cost/yr (capital charge on incremental cash; cash 0)',(0,0,0),tuple(round(OPP[i]*cash[i]) for i in range(3)),'P3-ASM-AB028'))
    tot[sid]=(cash,econ)
    for r in R: rows.append((sid,name)+r)
with open(sys.argv[1],'w',newline='') as f:
    w=csv.writer(f); w.writerow(['state_id','state','cost_category','cash_low','cash_base','cash_high','economic_low','economic_base','economic_high','assumption_ids'])
    for sid,name,cat,c,e,a in rows: w.writerow([sid,name,cat]+[round(x) if isinstance(x,float) else x for x in c]+[round(x) if isinstance(x,float) else x for x in e]+[a])
for k,(c,e) in tot.items(): print(k,'cash to first invoice',[round(x/1e3) for x in c],'econ',[round(x/1e3) for x in e])
