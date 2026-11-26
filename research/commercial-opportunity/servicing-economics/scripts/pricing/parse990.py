import sys, re, json, glob, os
import xml.etree.ElementTree as ET

def strip(tag): return tag.split('}',1)[-1]

def find_text(root, name):
    for el in root.iter():
        if strip(el.tag)==name: return (el.text or '').strip()
    return ''

def groups(root, name):
    return [el for el in root.iter() if strip(el.tag)==name]

def child_text(el, *names):
    for sub in el.iter():
        if strip(sub.tag) in names and (sub.text or '').strip(): return sub.text.strip()
    return ''

def parse(path):
    root = ET.parse(path).getroot()
    rid = os.path.basename(path).split('.')[0]
    out = dict(rid=rid,
        ein=find_text(root,'EIN'), name=find_text(root,'BusinessNameLine1Txt'),
        period_end=find_text(root,'TaxPeriodEndDt'), period_begin=find_text(root,'TaxPeriodBeginDt'),
        daf_cnt=find_text(root,'DonorAdvisedFundsHeldCnt'),
        daf_contrib=find_text(root,'DonorAdvisedFundsContriAmt'),
        daf_grants=find_text(root,'DonorAdvisedFundsGrantsAmt'),
        daf_eoy=find_text(root,'DonorAdvisedFundsVlEOYAmt'),
        net_assets_boy=find_text(root,'NetAssetsOrFundBalancesBOYAmt'),
        net_assets_eoy=find_text(root,'NetAssetsOrFundBalancesEOYAmt'),
        total_rev=find_text(root,'CYTotalRevenueAmt'), total_exp=find_text(root,'CYTotalExpensesAmt'),
        grants_paid=find_text(root,'CYGrantsAndSimilarPaidAmt'),
    )
    out['psr']=[(child_text(g,'Desc','BusinessCd'),child_text(g,'TotalRevenueColumnAmt')) for g in groups(root,'ProgramServiceRevenueGrp')]
    out['contractors']=[(child_text(g,'BusinessNameLine1Txt','PersonNm','BusinessNameLine1'),child_text(g,'ServicesDesc'),child_text(g,'CompensationAmt')) for g in groups(root,'ContractorCompensationGrp')]
    p9={}
    for nm in ['FeesForServicesManagementGrp','FeesForServicesInvstMgmntFeesGrp','FeesForServicesOtherGrp','FeesForServicesAccountingGrp','FeesForServicesLegalGrp','InformationTechnologyGrp','TotalFunctionalExpensesGrp','SalariesOtherCompEmplBnftGrp','OtherSalariesAndWagesGrp','OfficeExpensesGrp']:
        g=groups(root,nm)
        if g: p9[nm]=child_text(g[0],'TotalAmt')
    out['p9']=p9
    out['p9_other']=[(child_text(g,'Desc'),child_text(g,'TotalAmt')) for g in groups(root,'OtherExpensesGrp')]
    out['emp_cnt']=find_text(root,'TotalEmployeeCnt')
    # Schedule L business transactions
    out['schedL']=[(child_text(g,'BusinessNameLine1Txt','PersonNm'),child_text(g,'RelationshipDescriptionTxt'),child_text(g,'TransactionAmt'),child_text(g,'TransactionDesc')) for g in groups(root,'BusTrInvolveInterestedPrsnGrp')]
    out['other_rev']=[(child_text(g,'Desc'),child_text(g,'TotalRevenueColumnAmt')) for g in groups(root,'OtherRevenueMiscGrp')]
    return out

if __name__=='__main__':
    for p in sorted(glob.glob(sys.argv[1]+'/*.xml')):
        try: print(json.dumps(parse(p)))
        except Exception as e: print(json.dumps({'rid':p,'err':str(e)}))
