import json
def a(i, st, v, u, lo, hi, basis, evs, sens):
    return dict(assumption_id=f"A-PRC-{i:03d}", statement=st, value=str(v), unit=u, low=str(lo), high=str(hi), basis=basis, evidence_ids=evs, sensitivity=sens)
L = [
 a(1,"Average of opening and closing Schedule D EOY DAF value approximates average billable AUA for a year",1,"ratio to true daily average",0.9,1.1,"Only two points per year are public; distorted when assets jump (GiveClear 8x, Stifel 2.3x). Billable base may exclude cash/legacy pools or custom >$100M accounts",["EV-PRC-003","EV-PRC-014"],"high"),
 a(2,"Market price for comparable full staffed outsourced DAF administration (excl. custody, investment mgmt, legal sponsorship), expressed on average assets",20,"bps",15,40,"MS GIFT/Ren 18.4-18.8; TIFIN list 10-30; Stifel stack 29.5; USCGT/Ren 39-40; RCF/Ren 38 (related party). Low end applies to high-balance programs",["EV-PRC-003","EV-PRC-008","EV-PRC-010","EV-PRC-015"],"high"),
 a(3,"Market price for comparable staffed administration expressed per account-year",650,"USD/account-yr",390,815,"Ren: USCGT $389-429, Stifel $435-515 (partial), MS GIFT $685-737, RCF $814, TIFIN/GiveClear $815",["EV-PRC-003","EV-PRC-008","EV-PRC-010","EV-PRC-012","EV-PRC-014"],"high"),
 a(4,"Software-only DAF platform price at national/faith sponsors",5,"bps",1,9,"Ren/Stellar Part VII-B lines; per-account $34-$611; behaves like fixed minimum ~$120-175k for small clients",["EV-PRC-013"],"medium"),
 a(5,"Self-operated all-in non-grant, non-investment cost of large national sponsors",19,"bps",13.6,26.8,"Vanguard 18.6, Schwab 19.8, NPT 13.6, Fidelity 26.8 (FMR admin + other). Make-vs-buy ceiling for those sponsors",["EV-PRC-017","EV-PRC-018","EV-PRC-019","EV-PRC-020"],"high"),
 a(6,"A servicer price must carry a per-account floor because cost is account-driven",250,"USD/account-yr minimum",100,400,"Market minimums $100 (MS TPA, Fidelity, Charityvest), $250 (RCF), $360 (NCF); Ayco charges $270/acct at <1 bps; staffed cost $192-299/fund (Unbound 05a)",["EV-PRC-004","EV-PRC-011","EV-PRC-023"],"high"),
 a(7,"Sponsor-channel affiliate retains an admin/platform slice alongside the servicer",7,"bps",0,12,"MS GIFT MSSB 7 bps; Stifel Trust staffing ~12 bps; Fidelity/Schwab/Vanguard affiliates",["EV-PRC-005","EV-PRC-012"],"medium"),
 a(8,"Part VII-B contractor amounts are exact for named top-5 contractors >$100k but may bundle project/implementation work",1,"ratio",0.8,1.0,"NCF Stellar line doubled 2022-2024; Thrivent +77% on vendor change",["EV-PRC-013"],"medium"),
 a(9,"Exceptional services (foreign/expenditure-responsibility grants, complex assets, events) are priced outside the bps fee",3500,"USD per exceptional grant (2019 MS GIFT)",500,3500,"MS GIFT $3,500/$2,000 (2019), RCF extraordinary-service clause, NCF $25/wire",["EV-PRC-006","EV-PRC-011"],"medium"),
 a(10,"Same-model reasoning: the price band synthesis in this report is produced by one model; it is not independent validation of Unbound or the 20bps hypothesis",0,"n/a","","","Requires external validation by RFP quotes or design-partner contracts",[],"high"),
]
for x in L: print(json.dumps(x))
