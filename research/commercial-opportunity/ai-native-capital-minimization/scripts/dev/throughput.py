import subprocess, sys, json, re, os, csv
from collections import Counter
CODE = {'.fs','.fsx','.fsi','.cs','.ts','.tsx','.js','.mjs','.cjs','.css','.html','.py','.sh','.ps1','.sql','.rs'}
AGENT_AUTH = re.compile(r'claude|anthropic|openai|chatgpt|codex|copilot|gemini|devin|cursor', re.I)
BOT = re.compile(r'\[bot\]|github-actions', re.I)
TRAILER = re.compile(r'co-authored-by:.*(claude|anthropic|openai|chatgpt|codex|copilot|gemini)', re.I)
SESS = re.compile(r'(claude\.ai/code/session_[A-Za-z0-9]+)')
SEP='\x1e'
def log(repo):
    out = subprocess.run(['git','-C',repo,'log','--no-renames','--numstat','--date=iso-strict',f'--format={SEP}%H|%P|%an|%ae|%aI|%cI%n%B%x1f'],capture_output=True,text=True,errors='ignore').stdout
    commits=[]
    for chunk in out.split(SEP)[1:]:
        head, _, rest = chunk.partition('\n')
        h,parents,an,ae,ad,cd = head.split('|',5)
        body, _, stats = rest.partition('\x1f')
        rows=[l.split('\t') for l in stats.strip().splitlines() if l.count('\t')==2]
        def s(pred): 
            a=sum(int(r[0]) for r in rows if r[0].isdigit() and pred(r[2])); d=sum(int(r[1]) for r in rows if r[1].isdigit() and pred(r[2])); return a,d
        ca,cdl = s(lambda p: os.path.splitext(p)[1].lower() in CODE and 'node_modules' not in p)
        aa,ad2 = s(lambda p: True)
        commits.append(dict(h=h, merge=len(parents.split())>1, an=an, ae=ae, date=ad[:10], cdate=cd[:10], body=body, code_add=ca, code_del=cdl, all_add=aa, all_del=ad2))
    return commits
def cat(c):
    who = c['an']+' '+c['ae']
    if BOT.search(who): return 'bot'
    if AGENT_AUTH.search(who): return 'agent_author'
    if TRAILER.search(c['body']) or SESS.search(c['body']): return 'human_author_agent_trailer'
    return 'human_no_agent_signal'
def summarise(repo):
    cs = log(repo); nm=[c for c in cs if not c['merge']]
    cats = Counter(cat(c) for c in cs)
    days = sorted({c['date'] for c in cs})
    sess = {m for c in cs for m in SESS.findall(c['body'])}
    authors = Counter(cat(c) if cat(c)!='human_no_agent_signal' and cat(c)!='human_author_agent_trailer' else 'human' for c in cs)
    hid = len({c['an'].lower() for c in cs if cat(c) in ('human_no_agent_signal','human_author_agent_trailer')})
    agent_signal = sum(1 for c in cs if cat(c) in ('agent_author','human_author_agent_trailer') or (cat(c)!='bot' and TRAILER.search(c['body'])))
    ca=sum(c['code_add'] for c in nm); cd=sum(c['code_del'] for c in nm)
    aa=sum(c['all_add'] for c in nm); ad=sum(c['all_del'] for c in nm)
    head = subprocess.run(['git','-C',repo,'rev-parse','--short','HEAD'],capture_output=True,text=True).stdout.strip()
    shallow = subprocess.run(['git','-C',repo,'rev-parse','--is-shallow-repository'],capture_output=True,text=True).stdout.strip()
    span = (int(subprocess.run(['date','-d',days[-1],'+%s'],capture_output=True,text=True).stdout)-int(subprocess.run(['date','-d',days[0],'+%s'],capture_output=True,text=True).stdout))//86400+1 if days else 0
    return dict(repo=os.path.basename(repo.rstrip('/')), rev=head, shallow=shallow, first_commit=days[0] if days else '', last_commit=days[-1] if days else '', calendar_span_days=span,
        commits=len(cs), merge_commits=len(cs)-len(nm), active_days=len(days),
        agent_authored_commits=cats['agent_author'], human_commits_with_agent_trailer=cats['human_author_agent_trailer'],
        human_commits_no_agent_signal=cats['human_no_agent_signal'], bot_commits=cats['bot'],
        pct_commits_agent_signal=round(100*agent_signal/len(cs),1) if cs else 0,
        distinct_human_author_names=hid, distinct_claude_sessions=len(sess),
        code_lines_added=ca, code_lines_deleted=cd, all_lines_added=aa, all_lines_deleted=ad,
        code_added_per_active_day=round(ca/len(days)) if days else 0, net_code_per_active_day=round((ca-cd)/len(days)) if days else 0,
        commits_per_active_day=round(len(cs)/len(days),1) if days else 0)
rows=[summarise(r) for r in sys.argv[2:]]
with open(sys.argv[1],'w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
