"""Parse Vanguard Charitable investments-performance page text (HTML stripped to text) into JSON lines."""
import re,sys,json
t=open(sys.argv[1]).read()
v=r'(-?[\d.]+%|-)'
pat=re.compile(r'Show More Show Less ([^%]{2,120}?) '+v+' '+v+' '+v+' '+v+' '+v+r' \1 Returns Qtr')
bm=re.compile(r'Benchmark Return Returns Qtr '+v+' 1 year '+v+' 5 year '+v+' 10 year '+v)
cat=re.compile(r'(Portfolio Solutions|Portfolio Builders|All Investment Options)')
out=[]
ms=list(pat.finditer(t))
for i,m in enumerate(ms):
    end=ms[i+1].start() if i+1<len(ms) else len(t)
    seg=t[m.end():end]
    b=bm.search(seg)
    mg=re.search(r'Management For more about investment management styles, see our FAQs\. (\w+)',seg)
    ta=re.search(r'Target Allocation ([^M]{0,80}?) Management',seg)
    bn=re.search(r'Benchmark (.{3,260}?) Management For more',seg)
    out.append(dict(name=m.group(1),qtr=m.group(2),y1=m.group(3),y5=m.group(4),y10=m.group(5),er=m.group(6),
      b=b.groups() if b else None, mgmt=mg.group(1) if mg else '', alloc=ta.group(1) if ta else '', bname=bn.group(1) if bn else ''))
seen=set()
for o in out:
    k=o['name']
    if k in seen: continue
    seen.add(k); print(json.dumps(o))
