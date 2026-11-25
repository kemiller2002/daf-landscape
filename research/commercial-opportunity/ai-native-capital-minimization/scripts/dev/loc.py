import subprocess, sys, os, json, re
from collections import Counter
EXT = {'.fs':'F#','.fsx':'F#','.fsi':'F#','.cs':'C#','.ts':'TypeScript','.tsx':'TypeScript','.js':'JavaScript','.mjs':'JavaScript','.cjs':'JavaScript','.css':'CSS','.html':'HTML','.py':'Python','.sh':'Shell','.ps1':'PowerShell','.sql':'SQL','.rs':'Rust','.go':'Go','.svelte':'Svelte','.vue':'Vue','.razor':'Razor','.cshtml':'Razor'}
DOC = {'.md':'Markdown','.json':'JSON','.jsonl':'JSONL','.yaml':'YAML','.yml':'YAML'}
TESTPAT = re.compile(r'(\[<(Fact|Theory|Test|TestCase|Property)\b|\[(Fact|Theory|Test|TestMethod)\b|\btestCase\s+"|\btestProperty\s+"|\btestList\b|^\s*(it|test)\s*\(|\btest\(\s*[\'"`]|\bTest\.|\{\s*Name\s*=\s*"|\bName\s*=\s*"[^"]*"\s*$)')
def files(repo):
    return [f for f in subprocess.run(['git','-C',repo,'ls-files','-z'],capture_output=True,text=True).stdout.split('\0') if f]
def nlines(p):
    try:
        with open(p,'rb') as fh: return sum(1 for l in fh if l.strip())
    except Exception: return 0
def analyse(repo):
    fs = files(repo)
    code = Counter(); docs = Counter(); nfiles=Counter()
    testfiles=0; testcases=0; vendored=0
    for f in fs:
        ext=os.path.splitext(f)[1].lower(); p=os.path.join(repo,f)
        if any(s in f for s in ('node_modules/','vendor/','/dist/','wwwroot/lib/','.min.')): vendored+=1; continue
        if ext in EXT:
            n=nlines(p); code[EXT[ext]]+=n; nfiles[EXT[ext]]+=1
            low=f.lower()
            if re.search(r'(^|/)(tests?|spec|__tests__)(/|$)|\.tests?\.|tests?\.(fs|cs|ts|js|mjs)$|\.spec\.|test[s]?/', low):
                testfiles+=1
                try:
                    with open(p,errors='ignore') as fh: testcases+=sum(1 for l in fh if TESTPAT.search(l))
                except Exception: pass
        elif ext in DOC:
            docs[DOC[ext]]+=nlines(p)
    return dict(repo=os.path.basename(repo), tracked_files=len(fs), code_loc=sum(code.values()), code_by_lang=dict(code.most_common()), code_files=dict(nfiles), doc_loc=dict(docs), test_files=testfiles, test_case_markers=testcases)
print(json.dumps([analyse(r) for r in sys.argv[1:]]))
