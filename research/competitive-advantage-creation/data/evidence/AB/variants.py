from routes import sim
# decomposition of ER-7 base at trough
def decomp(build,burn,frm,rev,cust,vs=0.3,cac=40000,lag=6):
    cap,pay,_,_=sim(build,burn,frm,rev,cust,vs,cac,lag=lag)
    # find trough month
    mchurn=0.08/12; live=0; pipe=[]; cum=0; best=(0,0); acc={'build':0,'burn':0,'cac':0,'rev':0}
    rows=[]
    for m in range(1,121):
        s=cust/12 if m>frm else 0; pipe.append(s)
        gl=pipe.pop(0) if len(pipe)>lag else 0
        live=live*(1-mchurn)+gl; r=live*rev/12
        b=build/max(1,frm) if m<=frm else 0
        acc['build']+=b; acc['burn']+=burn; acc['cac']+=s*cac; acc['rev']+=r*(1-vs)
        cum+=r*(1-vs)-burn-b-s*cac
        rows.append((m,cum,dict(acc)))
    t=min(rows,key=lambda x:x[1]); return t
print('ER7 base trough',decomp(1600000,110000,15,300000,3))
print('ER7 fav trough',decomp(900000,80000,12,600000,5))
print('ER7 adv trough',decomp(2200000,160000,24,150000,1))
cases={'low':dict(frm=9,rev=600000,cust=5),'base':dict(frm=15,rev=300000,cust=3),'high':dict(frm=24,rev=150000,cust=1)}
burns={'phase2':{'low':80000,'base':110000,'high':160000},
       'lean_cash':{'low':15500,'base':43000,'high':99000},
       'lean_econ':{'low':15500+15900,'base':43000+18500,'high':99000+22800}}
for bk,bv in burns.items():
  for build_label,build in [('build0',0),('harden',{'low':40000,'base':120000,'high':250000})]:
    for c,cv in cases.items():
      b=build if isinstance(build,int) else build[c]
      for cac in (40000,20000):
        cap,pay,c60,live=sim(b,bv[c],cv['frm'],cv['rev'],cv['cust'],cac=cac)
        print(bk,build_label,c,'cac',cac,'capital %.0f'%cap,'payback',pay,'cum60 %.0f'%c60)
