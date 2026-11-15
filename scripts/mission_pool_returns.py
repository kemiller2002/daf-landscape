"""Build sponsor-pool-returns CSV from fetched public documents (paths given as args)."""
import csv, json, re, sys
D = sys.argv[1]  # download dir
OUT = sys.argv[2]
NUM = r'(-?\d+\.\d+%?|N/A|na|-)'

def num(x):
    x = x.strip().rstrip('%')
    return None if x in ('N/A', 'na', '-', '') else float(x)

rows = []
def add(**k):
    base = dict(sponsor='', pool='', pool_type='', esg_impact='no', as_of='', period='', pool_return_pct=None,
                benchmark_name='', benchmark_return_pct=None, return_basis='', source_url='', evidence_label='F',
                notes='')
    base.update(k)
    p, b = base['pool_return_pct'], base['benchmark_return_pct']
    base['pool_minus_benchmark_pp'] = round(p - b, 2) if (p is not None and b is not None) else None
    rows.append(base)

# ---------- Fidelity (Pool Performance Summary as of 2026-09-30) ----------
FID_URL = 'https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/monthly-pool-performance-summary.pdf'
lines = open(f'{D}/fid/mpps.txt').read().splitlines()
esg_f = {'Sustainable U.S. Index Access', 'Sustainable U.S. Index', 'Sustainable International Index',
         'Environmental Impact Access', 'Sustainable U.S. Bond Index'}
for i, l in enumerate(lines):
    m = re.match(r'^(\S.*?)\s{2,}(Active|Passive)\s+(.*)$', l)
    if not m:
        continue
    name, mgmt, rest = m.group(1).strip(), m.group(2), m.group(3)
    vals = re.findall(NUM, rest)[:8]
    for j in range(i + 1, min(i + 6, len(lines))):
        bl = lines[j].strip()
        if bl.startswith('Benchmark') or bl.startswith('Composite Benchmark'):
            bm = re.match(r'^(.*?)\s{2,}(-?\d.*)$', bl)
            bname, bvals = bm.group(1).strip(), re.findall(NUM, bm.group(2))[:8]
            break
    for k, per in ((3, '1y'), (4, '3y'), (5, '5y')):
        add(sponsor='Fidelity Charitable', pool=name, pool_type=f'pool ({mgmt.lower()})',
            esg_impact='yes' if name in esg_f else 'no', as_of='2026-09-30', period=f'trailing {per} annualised',
            pool_return_pct=num(vals[k]), benchmark_name=bname.rstrip('*'), benchmark_return_pct=num(bvals[k]),
            return_basis='net of underlying fund expenses and of the Fidelity Charitable annual administrative fee ("Pool results will include a Fidelity Charitable annual administrative fee"); benchmarks not fee-adjusted',
            source_url=FID_URL)

# ---------- Vanguard Charitable (investment performance page, as of 2026-09-30) ----------
VC_URL = 'https://www.vanguardcharitable.org/investments/investments-performance'
VC_COMPOSITE = {
 'Income': 'Composite: 80% Spliced Bloomberg U.S. Aggregate Float Adjusted, 14% Spliced Total Stock Market, 6% Spliced Total International Stock Market',
 'Conservative Growth': 'Composite: 60% Spliced Bloomberg U.S. Aggregate Float Adjusted, 30% Spliced Total Stock Market, 10% Spliced Total International Stock',
 'Moderate Growth': 'Composite: 45% Balanced Composite, 45% Wellington Composite, 10% Spliced Total International Stock (after 2009-12-31)',
 'Growth': 'Composite: 55% Spliced Total Stock Market, 20% Spliced Bloomberg U.S. Aggregate Float Adjusted, 25% Spliced Total International Stock Market (after 2009-12-31)',
 'Wellington': 'Wellington Composite Index (65% S&P 500, 35% Bloomberg U.S. Credit A or Better)',
 'Balanced Index': 'Balanced Composite Index',
}
esg_v = {'ESG U.S. Stock', 'ESG Global Stock', 'Global Positive Impact', 'ESG International Stock'}
for l in open(f'{D}/vc/parsed.jsonl'):
    o = json.loads(l)
    bname = o['bname'] or VC_COMPOSITE.get(o['name'], '')
    asof = '2026-02-28' if o['name'] == 'Private Assets Fund' else '2026-09-30'
    for key, per in (('y1', '1y'), ('y5', '5y')):
        bi = {'y1': 1, 'y5': 2}[key]
        add(sponsor='Vanguard Charitable', pool=o['name'], pool_type=f"investment option ({o['mgmt']})",
            esg_impact='yes' if o['name'] in esg_v else 'no', as_of=asof, period=f'trailing {per}',
            pool_return_pct=num(o[key]), benchmark_name=bname, benchmark_return_pct=num(o['b'][bi]),
            return_basis='as displayed; page footnote: Vanguard Charitable "does not itself charge investment fees"; admin fee page says the 0.60% admin fee is "reflected in the investment option unit values" - whether displayed returns are net of it is not stated',
            source_url=VC_URL, notes='3-year returns not published on this page' + ('; returns last updated 2026-02-28; no benchmark return shown' if o['name']=='Private Assets Fund' else ''))

# ---------- NPT (Investment Descriptions and Performance, NPT FOR IDAP 0926, as of 2026-06-30) ----------
NPT_URL = 'https://www.nptrust.org/investment-descriptions-and-performance-npt/'
npt = [('Broad Social Impact Portfolio', 'impact', 'yes', (11.44, 11.78, 6.15), '5y'),
       ('Conservative Portfolio (actively managed)', 'active', 'no', (7.2, 6.8, 4.9), '7y header / 5y footnote'),
       ('Moderate Portfolio (actively managed)', 'active', 'no', (18.1, 13.8, 8.8), '7y header / 5y footnote'),
       ('Growth Portfolio (actively managed)', 'active', 'no', (22.9, 17.4, 11.3), '7y header / 5y footnote'),
       ('Conservative Portfolio (index)', 'index', 'no', (7.8, 6.8, 4.7), '7y header / 5y footnote'),
       ('Moderate Portfolio (index)', 'index', 'no', (17.2, 13.0, 8.2), '7y header / 5y footnote'),
       ('Growth Portfolio (index)', 'index', 'no', (21.1, 16.3, 11.4), '7y header / 5y footnote')]
for name, typ, esg, v, lab in npt:
    for val, per in zip(v, ('1y', '3y', lab)):
        add(sponsor='National Philanthropic Trust', pool=name, pool_type=f'model portfolio ({typ})', esg_impact=esg,
            as_of='2026-06-30', period=f'trailing {per}', pool_return_pct=val, benchmark_name='none published',
            return_basis='blended model + actual, net of NPT investment advisory fee (0.10%; 0.15% impact) and trading costs, NOT net of NPT charitable admin fee; actual from 2019-11 (impact) / 2021-04 (others)',
            source_url=NPT_URL, notes='No benchmark published, so no difference computed' + ('; third column headed "7-YEAR" but footnote says 1, 3 and 5 years - unresolved' if 'header' in lab else ''))

# ---------- NCF (Quarterly Charitable Investment Report Q3 2026) ----------
NCF_URL = 'https://site.ncfgiving.com/wp-content/uploads/2026/10/Quarterly-Charitable-Investment-Report-Q3-2026.pdf'
for name, v in (('Fixed Income Pool', (-2.1, 3.4, -1.0)), ('Balanced Growth Pool', (8.1, 13.6, 6.7)), ('Equity Pool', (14.3, 19.8, 11.3))):
    for val, per in zip(v, ('1y', '3y', '5y')):
        add(sponsor='National Christian Foundation', pool=name, pool_type='pool (launched 2026-09-01)', as_of='2026-09-30',
            period=f'trailing {per}', pool_return_pct=None, benchmark_name='Composite benchmark (pro forma)', benchmark_return_pct=val,
            return_basis='benchmark only: "Net of NCF investment oversight fee; includes 5% cash allocation"',
            source_url=NCF_URL, notes='Pool return N/A: "new pools launched as of 9/1/2026 and do not have prior performance history"; never inferred')

# ---------- FFTC (Preliminary Investment Performance, as of 2026-09-30) ----------
FF_URL = 'https://www.fftc.org/sites/default/files/documents/FFTC_Performance_Report.pdf'
fl = [l for l in open(f'{D}/fftc/perf.txt').read().splitlines() if l.strip()]
pairs = []
for i, l in enumerate(fl):
    m = re.match(r'^\s{2}(\S.*?)\s{3,}(-?\d.*)$', l)
    if m and not l.startswith('     '):
        bm = re.match(r'^\s{5}(\S.*?)\s{3,}(-?\d.*)$', fl[i + 1])
        pairs.append((m.group(1), re.findall(NUM, m.group(2)), bm.group(1), re.findall(NUM, bm.group(2))))
for name, pv, bname, bv in pairs:
    for k, per in ((2, '1y'), (3, '3y'), (4, '5y')):
        add(sponsor='Foundation For The Carolinas', pool=name, pool_type='standard investment pool',
            esg_impact='yes' if name.startswith('ESG') else 'no', as_of='2026-09-30', period=f'trailing {per}',
            pool_return_pct=num(pv[k]), benchmark_name=bname, benchmark_return_pct=num(bv[k]),
            return_basis='preliminary; "net of investment fees"; admin fees charged separately', source_url=FF_URL,
            notes='ESG pool inception 2021-11-30 (pool sheet)' if name.startswith('ESG') else '')
# FFTC calendar-year 2021-2025 from pool sheets
FFS_URL = 'https://www.fftc.org/sites/default/files/documents/All_Pool_Sheets.pdf'
YEARS = ['2026', '2025', '2024', '2023', '2022', '2021']
cal = {}
for p in range(1, 13):
    t = open(f'{D}/fftc/p{p}.txt').read().splitlines()
    for i, l in enumerate(t):
        m = re.match(r'^ ?(Active LTG|Diversified LTG|Income & Growth|Liquid Reserves|Passive LTG|Low Duration F\.I\.) ((?:-?\d+\.\d%\s?){10})$', l)
        if m and i + 1 < len(t):
            b = re.match(r'^ ?Benchmark ((?:-?\d+\.\d%\s?){10})$', t[i + 1])
            if b:
                cal[m.group(1)] = (m.group(2).split(), b.group(1).split())
names = {'Active LTG': 'Active Long-Term Growth', 'Diversified LTG': 'Diversified Long-Term Growth', 'Income & Growth': 'Income & Growth',
         'Liquid Reserves': 'Liquid Reserves', 'Passive LTG': 'Passive Long-Term Growth', 'Low Duration F.I.': 'Low Duration Fixed Income'}
for k, (pv, bv) in cal.items():
    for idx, y in enumerate(YEARS):
        if y == '2026':
            continue
        add(sponsor='Foundation For The Carolinas', pool=names[k], pool_type='standard investment pool', as_of=f'{y}-12-31',
            period=f'calendar year {y}', pool_return_pct=num(pv[idx]), benchmark_name='Benchmark (as labelled on pool sheet)',
            benchmark_return_pct=num(bv[idx]), return_basis='pool sheet "Performance vs. Benchmark"; net of investment fees',
            source_url=FFS_URL, notes='ESG Long-Term Growth calendar rows are chart-only (not text) and were not transcribed')

# ---------- GKCCF (Investment Performance Summary, Dec 2025 and Oct 2026; ESG Oct 2026) ----------
def gk(path, asof, url, width=132):
    t = open(path).read().splitlines()
    out = []
    for l in t:
        s = re.sub(r'\s{2,}', '  ', l[:width]).strip()
        m = re.match(r'^\*?(.+?)\s{2}(-?\d+\.\d+(?:\s+-?\d+\.\d+)*)', s)
        if m:
            out.append((m.group(1).strip(), re.findall(r'-?\d+\.\d+', m.group(2))))
    return out
def emit_gk(path, asof, url, sponsor='Greater Kansas City Community Foundation', esg=False):
    items = gk(path, asof, url, 165 if esg else 132)
    for i, (name, v) in enumerate(items):
        if not (name.endswith(' TR') or name.endswith('Mix') or name.endswith('Social Impact Pool') or name.startswith('Aggressive Risk') and name.endswith('Mix')):
            continue
        if name.startswith(('S&P', 'MSCI', 'USTREAS')):
            continue
        # benchmark = next item
        bname, bv = items[i + 1] if i + 1 < len(items) else ('', [])
        if 'Benchmark' not in bname and 'USTREAS' not in bname:
            continue
        impact = esg and ('Impact' in name or 'ESG' in name)
        if esg and not impact:
            continue  # fixed-income/MM rows repeat the main report
        for k, per in ((3, '1y'), (4, '3y'), (5, '5y')):
            pv_ = num(v[k]) if len(v) > k else None
            bv_ = num(bv[k]) if len(bv) > k else None
            note = 'Performance gross of GKCCF administrative fees, net of investment management fees, brokerage, consulting and transaction costs'
            if impact:
                note += '; impact pools and impact mixes/benchmarks pro forma before 2022-09-30'
                if per in ('5y',):
                    note += ' (5y figure includes pro forma period)'
            if 'Equity Pool' in name or 'Equity Benchmark' in bname:
                note += '; equity pools pro forma before 2019-06-30'
            add(sponsor=sponsor, pool=name.replace(' TR', ''), pool_type='investment mix' if 'Mix' in name else 'investment pool',
                esg_impact='yes' if impact else 'no', as_of=asof, period=f'trailing {per} (compound annual)' if per != '1y' else 'trailing 1y',
                pool_return_pct=pv_, benchmark_name=bname.replace('*', ''), benchmark_return_pct=bv_,
                return_basis=note, source_url=url, notes='' if pv_ is not None else 'pool return blank on report for this period')
emit_gk(f'{D}/gk/dec25.txt', '2025-12-31', 'https://www.growyourgiving.org/wp-content/uploads/2026/01/Investment-Performance-Summary-Dec-2025-GKCCF.pdf')
emit_gk(f'{D}/gk/oct26.txt', '2026-10-31', 'https://www.growyourgiving.org/wp-content/uploads/2026/11/Investment-Performance-Summary-Oct-2026-GKCCF.pdf')
emit_gk(f'{D}/gk/esg_oct26.txt', '2026-10-31', 'https://www.growyourgiving.org/wp-content/uploads/2026/11/ESG-Investment-Performance-Summary-Oct-2026-GKCCF.pdf', esg=True)

# ---------- CJP (Donor Advised Funds report as of 2026-09-30) ----------
CJP_URL = 'https://www.cjp.org/hubfs/DAF_Report.pdf?hsLang=en'
cjp = [('Fixed Income Fund', 'no', (-1.8, 3.6, -0.1), 'Bloomberg Aggregate', (-1.9, 4.1, -0.6), 'ER 0.1%'),
       ('Sustainable Fund', 'yes', (4.9, None, None), 'none shown', (None, None, None), 'ER 0.6%; inception 2023-12-01; no benchmark row in table'),
       ('Diversified Fund', 'no', (11.4, 15.6, 7.8), '60% MSCI ACWI, 40% Bloomberg Aggregate', (9.1, 14.7, 6.7), 'ER 0.5%'),
       ('Equity Fund', 'no', (11.7, 16.6, 8.0), '100% MSCI ACWI', (16.5, 21.8, 11.6), 'ER 0.5%'),
       ('US Equity Index Fund', 'no', (12.5, None, None), 'S&P 500', (15.7, 22.9, 13.8), 'ER 0.1%; inception 2025-06-20; 1y gap to S&P 500 as published - not explained in the report'),
       ('Jewish Community Endowment Pool (JCEP)', 'no', (12.7, 16.1, 10.1), '60% MSCI ACWI, 40% Bloomberg Int Treasury', (9.8, 14.4, 7.3), 'ER 1.5%; DAF minimum $500,000 total, $100,000 in JCEP; net of investment management fees but not program admin or partnership-level admin expenses'),
       ('Money Market Fund', 'no', (3.5, 4.4, 3.6), '91 Day T-Bill', (3.6, 4.5, 3.7), 'ER 0.2%')]
for name, esg, pv, bname, bv, note in cjp:
    for a, b, per in zip(pv, bv, ('1y', '3y', '5y')):
        add(sponsor='Combined Jewish Philanthropies (CJP)', pool=name, pool_type='DAF investment option', esg_impact=esg,
            as_of='2026-09-30', period=f'trailing {per}' + (' annualised' if per != '1y' else ''), pool_return_pct=a,
            benchmark_name=bname, benchmark_return_pct=b,
            return_basis='"net of investment management and custodial fees, but not DAF program administrative fees"',
            source_url=CJP_URL, notes=note)

cols = ['row_id', 'sponsor', 'pool', 'pool_type', 'esg_impact', 'as_of', 'period', 'pool_return_pct', 'benchmark_name',
        'benchmark_return_pct', 'pool_minus_benchmark_pp', 'return_basis', 'source_url', 'evidence_label', 'retrieved', 'notes']
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for i, r in enumerate(rows, 1):
        r['row_id'] = f'R{i:03d}'
        r['retrieved'] = '2026-11-15'
        w.writerow({c: ('' if r.get(c) is None else r.get(c)) for c in cols})
print(len(rows), 'rows')
