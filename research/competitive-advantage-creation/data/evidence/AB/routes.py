# Replica of Phase II Routes.fs (REV2) for scenario exploration; not durable model code.
import itertools
def sim(build,burn,frm,rev,cust,vs=0.3,cac=40000,churn=0.08,lag=6,horizon=120,recurring=True,extra_upfront=0.0):
    mchurn=churn/12; bm=max(1.0,frm); live=0.0; pipe=[]; cum=0.0; cums=[]; nets=[]
    for m in range(1,horizon+1):
        signing = cust/12 if m>frm else 0.0
        pipe=pipe+[signing]
        if len(pipe)>lag: gl=pipe[0]; pipe=pipe[1:]
        else: gl=0.0
        live=live*(1-mchurn)+gl
        revenue= live*rev/12 if recurring else gl*rev
        bs = build/bm if m<=bm else 0.0
        net= revenue*(1-vs)-burn-bs-signing*cac - (extra_upfront if m==1 else 0)
        cum+=net; cums.append(cum); nets.append(net)
    trough=min([0.0]+cums); tm=cums.index(trough) if trough<0 else 0
    pay=next((i+1 for i in range(tm,len(cums)) if cums[i]>=0),None)
    return -trough,pay,cums[59],live
if __name__=='__main__':
    # reproduce ER-7 base and favourable/adverse
    print('ER7 base',sim(1600000,110000,15,300000,3))
    print('ER7 fav',sim(900000,80000,12,600000,5))
    print('ER7 adv',sim(2200000,160000,24,150000,1))
    print('ER4 base',sim(1600000,135000,18,810000,1,vs=0.15,cac=125000))
    print('ER5 base',sim(1940000,190000,18,2000000,0.6,vs=0.35,cac=125000))
