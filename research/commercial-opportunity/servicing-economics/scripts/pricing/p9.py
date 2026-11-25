import sys, xml.etree.ElementTree as ET
def strip(t): return t.split('}',1)[-1]
for p in sys.argv[1:]:
    root=ET.parse(p).getroot()
    irs=[e for e in root.iter() if strip(e.tag)=='IRS990']
    if not irs: continue
    out=[]
    for el in irs[0]:
        tg=strip(el.tag)
        if tg.endswith('Grp'):
            tot=[c for c in el if strip(c.tag)=='TotalAmt']
            if tot: out.append((tg,tot[0].text))
    print(p.split('/')[-1], [x for x in out if x[1] and abs(float(x[1]))>0])
