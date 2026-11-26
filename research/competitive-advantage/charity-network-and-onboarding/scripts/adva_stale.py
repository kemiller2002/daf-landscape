"""ADVA: proxy for BMF address/record staleness: TAX_PERIOD of latest return on file, c3 rows. stdlib."""
import csv,sys,os,collections
d=sys.argv[1]; c=collections.Counter(); n=0
for f in ('eo1.csv','eo2.csv','eo3.csv','eo4.csv'):
    for r in csv.DictReader(open(os.path.join(d,f),newline='',encoding='latin-1')):
        if r['SUBSECTION']!='03': continue
        n+=1; tp=r['TAX_PERIOD'].strip()
        y=int(tp[:4]) if tp[:4].isdigit() else 0
        k='blank' if not y else ('<=2021' if y<=2021 else str(y))
        c[k]+=1
print(n, sorted(c.items()))
