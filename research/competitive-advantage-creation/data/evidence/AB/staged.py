def staged(onetime,pre_run,pre_m,live_run,rev,cust,vs=0.3,cac=0.0,lag=6,churn=0.08,founder_pre=0,founder_live=0,cont=0.0,horizon=120):
    mch=churn/12; live=0; pipe=[]; cum=-onetime*(1+cont); cums=[]
    for m in range(1,horizon+1):
        s=cust/12 if m>pre_m else 0; pipe.append(s)
        gl=pipe.pop(0) if len(pipe)>lag else 0
        live=live*(1-mch)+gl; r=live*rev/12
        run=(pre_run+founder_pre)/12 if m<=pre_m else (live_run+founder_live)/12
        cum+= r*(1-vs)-run*(1+cont)-s*cac; cums.append(cum)
    t=min(cums); tm=cums.index(t); pay=next((i+1 for i in range(tm,120) if cums[i]>=0),None)
    return round(-t/1e3),pay,round(-cums[pre_m+lag+18-1]/1e3) if pre_m+lag+18<=120 else None
# S3: onetime = dev + first-customer one-time (cac in onetime only for first)
cfg={'low':dict(one=40e3+15e3+35e3+20e3+20e3+25e3,pre=30e3,pm=9,live=165e3,rev=600e3,cust=5,fp=0,fl=0,cont=0.15,cac=15e3,lag=3),
     'base':dict(one=120e3+30e3+75e3+45e3+60e3+75e3,pre=105e3,pm=15,live=465e3,rev=300e3,cust=3,fp=0,fl=60e3,cont=0.25,cac=30e3,lag=6),
     'high':dict(one=250e3+60e3+150e3+100e3+150e3+200e3,pre=280e3,pm=24,live=1070e3,rev=150e3,cust=1,fp=60e3,fl=150e3,cont=0.40,cac=60e3,lag=9)}
for k,c in cfg.items():
    for label,(fp,fl) in {'cash':(c['fp'],c['fl']),'econ':({'low':190356,'base':222482,'high':273473}[k],)*2}.items():
        print('S3',k,label,staged(c['one'],c['pre'],c['pm'],c['live'],c['rev'],c['cust'],cac=c['cac'],lag=c['lag'],founder_pre=fp,founder_live=fl,cont=c['cont']))
# cross: base costs with adverse revenue / and base revenue but 1 customer/yr
c=cfg['base']
print('base costs, 1 cust/yr',staged(c['one'],c['pre'],c['pm'],c['live'],300e3,1,cac=30e3,founder_live=60e3,cont=.25))
print('base costs, 2 cust/yr 200k',staged(c['one'],c['pre'],c['pm'],c['live'],200e3,2,cac=30e3,founder_live=60e3,cont=.25))
print('base costs, revenue high case',staged(c['one'],c['pre'],c['pm'],c['live'],150e3,1,cac=30e3,founder_live=60e3,cont=.25))
print('high costs base revenue',staged(cfg['high']['one'],280e3,24,1070e3,300e3,3,cac=60e3,lag=9,founder_pre=60e3,founder_live=150e3,cont=.4))
print('base costs vs .15',staged(c['one'],c['pre'],c['pm'],c['live'],300e3,3,vs=.15,cac=30e3,founder_live=60e3,cont=.25))
# kill at month 24 for high case: cumulative at month 24
