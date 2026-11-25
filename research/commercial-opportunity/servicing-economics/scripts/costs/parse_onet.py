import re,sys,glob,os,json
def parse(path):
    s=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',open(path,encoding='utf-8').read()))
    title=re.search(r'Local Wages[^-]*-?\s*([^|]*)',s)
    t=re.search(r'(\d\d-\d{4}\.\d\d) - ([^\.]*?) (Bright Outlook )?(Local|Wages)',s)
    m=re.search(r'Annual High \(90%\) United States \$([\d,]+) \$([\d,]+) \$([\d,]+) \$([\d,]+) \$([\d,]+)',s)
    src=re.search(r'Bureau of Labor Statistics (\d{4}) wage data',s)
    soc=os.path.basename(path)[5:12]
    vals=[int(x.replace(',','')) for x in m.groups()] if m else None
    return {"soc":soc,"title":t.group(2) if t else None,"year":src.group(1) if src else None,"p10_p25_p50_p75_p90":vals}
d=sys.argv[1]
rows=[parse(p) for p in sorted(glob.glob(os.path.join(d,'onet_*.html')))]
print(json.dumps(rows,indent=0))
