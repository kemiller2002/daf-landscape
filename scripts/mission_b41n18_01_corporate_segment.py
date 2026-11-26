"""P-B41N18-01: corporate-DAF segment across sponsors that do not publish it.

usage: python3 -I scripts/mission_b41n18_01_corporate_segment.py REPO_ROOT EXTRACT_JSON [--print]
  REPO_ROOT     repo root ('.')
  EXTRACT_JSON  per-return Schedule D values parsed from 990 e-file XML (built by the pass's extract step:
                one dict per return with ein, name, tax_period, sub_year, object_id, url, sched_d{...}).

Writes data/mission-2026-11-14/corporate-daf-segment-2026-11-19.csv with the columns of
corporate-daf-programs-2021-2026.csv (SA01-SA05). Pure functions, stdlib only.
"""
import csv, json, os, sys
from functools import reduce

OUT = 'data/mission-2026-11-14/corporate-daf-segment-2026-11-19.csv'
PROG = 'data/mission-2026-11-14/corporate-daf-programs-2021-2026.csv'
GT = 'https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml'

# sponsor -> (short name, segment, what the narrative/statement read found about a corporate split)
SPONSORS = {
    '510198509': ('Tides Foundation', 'national/cause', 'Sch O and Sch D narrative: no corporate split; mission text names "corporations" among contributors (CY2023-24). Audited FS CY2022-24: no split.'),
    '431634280': ('CAF America', 'national/international', 'Sch O and Sch D narrative: no corporate split; mission names "corporations" (FYE 2024-04, 2025-04). Audited FS FYE 2023-04/2024-04 split DAF net assets by entity (CAF America/CADF/CAF Canada), not by donor type.'),
    '133615533': ('Rockefeller Philanthropy Advisors', 'national/advisory', 'Sch O and Sch D narrative: no corporate split. No annual report or audited FS found in the robots-allowed sitemap.'),
    '237825575': ('National Philanthropic Trust', 'national', 'Sch O and Sch D narrative: no corporate split; Sch O/mission names "companies"/"corporations" as clients. Annual Reports FY23-FY25 (web): no donor-type split.'),
    '205205488': ('Silicon Valley Community Foundation', 'community', 'Sch O/Sch D narrative: no split. Audited FS FY2022-FY2025 publish corporate-advised fund grants (SV rows).'),
    '362167000': ('The Chicago Community Trust', 'community', 'Sch O/Sch D narrative: no split. Website robots.txt returned 403: audited FS and annual report not fetched.'),
    '566047886': ('Foundation For The Carolinas', 'community', 'Sch O/Sch D narrative: no split; Part III text says FFTC "supports personal and corporate philanthropy". Audited FS CY2025: no split.'),
    '431152398': ('Greater Kansas City Community Foundation', 'community', 'Sch O/Sch D narrative: no split. Web: "Hundreds of companies rely on us to organize their philanthropy under one structure: a corporate donor-advised fund" (no count). No audited FS link found.'),
    '133062214': ('The New York Community Trust', 'community', 'Sch O/Sch D narrative: no split; mission names "businesses". 2025 financials and 2025 annual report: assets by fund type (DAF 34%), no corporate type.'),
    '316044264': ('Columbus Foundation', 'community', 'Sch O/Sch D narrative: no split. Sitemap returned no URLs; audited FS not located.'),
    '237315673': ('The Oregon Community Foundation', 'community', 'Sch O/Sch D narrative: no split. robots.txt disallows /assets (where PDFs sit): audited FS not fetched.'),
    '042104021': ('The Boston Foundation', 'community', 'Sch O/Sch D narrative: no split. Audited FS FY2023/FY2025: no split. Company-giving page names corporate DAFs (Bain Capital Relief Fund, IR+M) without counts.'),
    '953510055': ('California Community Foundation', 'community', 'Sch O/Sch D narrative: no split. Website robots.txt returned 403: audited FS not fetched.'),
    '581344646': ('Community Foundation for Greater Atlanta', 'community', 'Sch O/Sch D narrative: no split. Audited FS CY2024: net assets by fund type (donor advised $1,025.4m), no corporate type.'),
}

# Published corporate splits (first-party documents read this pass). (id, sponsor, year, metric, value, denominator, basis, url, form, date)
PUBLISHED = [
    ('SV2021', 'Silicon Valley Community Foundation', '2021', 'grants', 100e6, 2155e6, 'Corporate-advised funds "made grants of approximately $100,000,000" (2021); donor-advised funds granted ~$2,155,000,000', 'https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2022.pdf', 'Audited financial statements FY2022', '2023'),
    ('SV2022', 'Silicon Valley Community Foundation', '2022', 'grants', 175e6, 2553e6, 'Corporate-advised fund grants ~$175,000,000 (2022); donor-advised ~$2,553,000,000', 'https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2023.pdf', 'Audited financial statements FY2023', '2024'),
    ('SV2023', 'Silicon Valley Community Foundation', '2023', 'grants', 134e6, 4657e6, 'Corporate-advised fund grants ~$134,000,000 (2023); donor-advised ~$4,657,000,000', 'https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2024.pdf', 'Audited financial statements FY2024', '2025'),
    ('SV2024', 'Silicon Valley Community Foundation', '2024', 'grants', 189e6, 3077e6, 'Corporate-advised fund grants ~$189,000,000 (2024); donor-advised ~$3,077,000,000', 'https://www.svcf.org/assets/files/publications/SVCF-CFS-FY25_Updated-Financials.pdf', 'Audited financial statements FY2025', '2026'),
    ('SV2025', 'Silicon Valley Community Foundation', '2025', 'grants', 153e6, 2051e6, 'Corporate-advised fund grants ~$153,000,000 (2025); donor-advised ~$2,051,000,000', 'https://www.svcf.org/assets/files/publications/SVCF-CFS-FY25_Updated-Financials.pdf', 'Audited financial statements FY2025', '2026'),
    ('FC2024', 'Fidelity Charitable', '2024', 'grants', 525e6, 14.9e9, '518 corporate DAFs; corporate grants $525M (24,975 grants, avg $21,024); all grants $14.9 billion (nearly 2.7 million)', 'https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf', 'Giving Report 2025', '2025'),
    ('FC2025', 'Fidelity Charitable', '2025', 'grants', 539.8e6, 18.3e9, '556 corporate DAFs; corporate grants $539.8M (26,036 grants, avg $20,732); all grants $18.3 billion', 'https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf', 'Giving Report 2026', '2026'),
]
AOGF = dict(corp=1390021897, other=935709539, url=GT.format('202642259349301349'))  # FYE 2026-03 Sch D columns [X]

def header(root):
    with open(os.path.join(root, PROG), newline='') as f:
        return next(csv.reader(f))


def latest_per_period(rows):
    """Keep the latest-submitted return per (ein, tax_period) (amended returns supersede)."""
    key = lambda r: (r['ein'], r['tax_period'])
    best = reduce(lambda acc, r: {**acc, key(r): r if key(r) not in acc or r['object_id'] > acc[key(r)]['object_id'] else acc[key(r)]}, rows, {})
    return sorted(best.values(), key=lambda r: (SPONSORS[r['ein']][0], r['tax_period']))


def recency(tp):
    y, m = int(tp[:4]), int(tp[4:])
    return 'in_window' if (y > 2021 or (y == 2021 and m == 12)) else 'in_window_edge'


def num(v):
    return int(v) if v not in (None, '') else None


def nosplit_row(i, r):
    d = r['sched_d']; name, seg, note = SPONSORS[r['ein']]
    cnt, con, gr, eoy = (num(d['DonorAdvisedFundsHeldCnt']), num(d['DonorAdvisedFundsContriAmt']),
                         num(d['DonorAdvisedFundsGrantsAmt']), num(d['DonorAdvisedFundsVlEOYAmt']))
    basis = (f'FORM 990 GIVES NO CORPORATE SPLIT (counts: none; contributions: none; grants: none; fees: none; Sch O and Sch D narrative read). '
             f'Sch D Part I DAF column total: {cnt} DAFs; contributions ${con:,}; grants ${gr:,}; EOY ${eoy:,}')
    tp = r['tax_period']
    return dict(program_id=f'SN{i:02d}', row_type='sponsor_aggregate', company='(all DAFs; corporate share not reported)',
                ticker='', cik='', sponsor=name, sponsor_basis='Form 990 Sch D/Sch O (e-file XML)', fund_name='DAFs incl. any corporate',
                program_type='sponsor_no_corporate_split', year_established='', evidence_year=f'FYE {tp[:4]}-{tp[4:]}',
                amount_usd='', amount_basis=basis, shares='', purpose_tags=seg, pledge_1pct='',
                source_url=GT.format(r['object_id']), source_form='Form 990', source_date=f"filed {r['sub_year']}",
                label='X', recency_flag=recency(tp), notes=note + f' EIN {r["ein"]}; object_id {r["object_id"]}.')


def published_row(p):
    pid, sp, yr, metric, val, den, basis, url, form, date = p
    share = val / (den + val) if sp.startswith('Silicon') else val / den
    sb = 'audited statements' if sp.startswith('Silicon') else 'sponsor report'
    dtxt = 'share of donor-advised + corporate-advised grants' if sp.startswith('Silicon') else 'share of all Fidelity Charitable grants'
    return dict(program_id=pid, row_type='sponsor_aggregate', company='(all corporate accounts)', ticker='', cik='', sponsor=sp,
                sponsor_basis=sb, fund_name='Corporate advised funds' if sp.startswith('Silicon') else 'Corporate Giving Account',
                program_type='sponsor_corporate_program', year_established='', evidence_year=yr, amount_usd=f'{val:.0f}',
                amount_basis=f'{basis}. Corporate {dtxt}: {share:.2%} [C]', shares='', purpose_tags='published corporate split (grants only)',
                pledge_1pct='', source_url=url, source_form=form, source_date=date, label='F', recency_flag='in_window',
                notes='Counts, contributions, assets and fees by corporate vs individual: not published' if sp.startswith('Silicon')
                else 'Corporate DAF assets, contributions and fees: not published')


def shares():
    sv = {p[2]: p[4] / (p[5] + p[4]) for p in PUBLISHED if p[0].startswith('SV')}
    fc = {p[2]: p[4] / p[5] for p in PUBLISHED if p[0].startswith('FC')}
    return sv, fc


def estimates(rows):
    sv, fc = shares()
    obs = list(sv.values()) + list(fc.values())
    lo, hi = min(obs), max(obs)
    # FY2024 as in daf-sponsor-league-table-fy2021-2025.csv: FYE 2024-12, 2024-09 (CCT), 2024-06 (NPT, TBF, CCF), 2024-04 (CAF)
    pick = {'510198509': '202412', '431634280': '202404', '133615533': '202412', '237825575': '202406', '362167000': '202409',
            '566047886': '202412', '431152398': '202412', '133062214': '202412', '316044264': '202412', '237315673': '202412',
            '042104021': '202406', '953510055': '202406', '581344646': '202412'}
    base = [r for r in rows if pick.get(r['ein']) == r['tax_period']]
    g = sum(num(r['sched_d']['DonorAdvisedFundsGrantsAmt']) for r in base)
    pub24 = ((525e6 + 189e6), (14.9e9 + 3077e6 + 189e6))
    pub25 = ((539.8e6 + 153e6), (18.3e9 + 2051e6 + 153e6))
    with_aogf = ((pub25[0] + AOGF['corp']), (pub25[1] + AOGF['corp'] + AOGF['other']))
    return dict(obs_lo=lo, obs_hi=hi, n_base=len(base), base_grants=g, base_lo=g * lo, base_hi=g * hi,
                pooled24=pub24[0] / pub24[1], pooled25=pub25[0] / pub25[1], pooled25_aogf=with_aogf[0] / with_aogf[1],
                pub25_corp=pub25[0], with_aogf_corp=with_aogf[0], base_eins=sorted(r['ein'] for r in base))


def estimate_rows(e):
    common = dict(row_type='estimate', company='(segment estimate)', ticker='', cik='', sponsor_basis='computed', fund_name='',
                  year_established='', shares='', pledge_1pct='', source_form='computed', source_date='2026-11-19', recency_flag='in_window')
    return [
        dict(common, program_id='SE01', sponsor='Fidelity Charitable + SVCF (published splits)', program_type='pooled_published_share',
             evidence_year='2024', amount_usd=f'{525e6 + 189e6:.0f}', amount_basis=f'Pooled corporate share of grants, CY2024: {e["pooled24"]:.2%} [C]',
             purpose_tags='bounded estimate', source_url='rows FC2024, SV2024', label='C', notes='Grants only; no published asset split at either sponsor'),
        dict(common, program_id='SE02', sponsor='Fidelity Charitable + SVCF (published splits)', program_type='pooled_published_share',
             evidence_year='2025', amount_usd=f'{e["pub25_corp"]:.0f}', amount_basis=f'Pooled corporate share of grants, CY2025: {e["pooled25"]:.2%} [C]',
             purpose_tags='bounded estimate (lower bound for the with-data set)', source_url='rows FC2025, SV2025', label='C', notes='Grants only'),
        dict(common, program_id='SE03', sponsor='Fidelity Charitable + SVCF + AOGF DAF column', program_type='pooled_published_share',
             evidence_year='2025 / FYE 2026-03', amount_usd=f'{e["with_aogf_corp"]:.0f}',
             amount_basis=f'Pooled share if the whole AOGF Sch D DAF column ($1,390.0m) is corporate: {e["pooled25_aogf"]:.2%} [C] (upper bound for the with-data set)',
             purpose_tags='bounded estimate (upper bound)', source_url=AOGF['url'] + '; rows FC2025, SV2025', label='C',
             notes='AOGF Sch O also places "other fund structures" in the DAF column (wave 26), so the column is an upper bound on corporate'),
        dict(common, program_id='SE04', sponsor='13 sponsors without a published split', program_type='extrapolated_share',
             evidence_year='FY2024 (Sch D)', amount_usd=f'{e["base_lo"]:.0f}',
             amount_basis=(f'[I] Applying the observed single-year corporate grant shares at Fidelity and SVCF, CY2021-2025 '
                           f'({e["obs_lo"]:.2%} to {e["obs_hi"]:.2%}), to the 13 sponsors\' FY2024 Sch D DAF grants (${e["base_grants"]/1e9:.2f}bn) gives '
                           f'${e["base_lo"]/1e6:,.0f}m to ${e["base_hi"]/1e6:,.0f}m of corporate DAF grants'),
             purpose_tags='extrapolation [I]', source_url='SN rows (FY2024 returns); SV/FC rows', label='I',
             notes='amount_usd is the low end. Assumes these sponsors\' corporate mix lies within the Fidelity/SVCF range; Tides (Pledge 1% partner) and GKCCF ("hundreds of companies") may sit above it'),
    ]


def named_rows():
    common = dict(row_type='company_program', ticker='', cik='', sponsor_basis='sponsor page', year_established='', amount_usd='',
                  shares='', pledge_1pct='', source_form='sponsor web page', label='F')
    return [
        dict(common, program_id='CN01', company='DoorDash', sponsor='Silicon Valley Community Foundation', fund_name='(not named)',
             program_type='corporate_advised_fund', evidence_year='2025 donor story (page dated 2024-04-23)',
             amount_basis='"DoorDash to establish a corporate advised fund with SVCF"', purpose_tags='home-delivery cost support for nonprofit partners',
             source_url='https://www.svcf.org/annual-reports/donor-2025/donor-stories-2025-26-doordash', source_date='2024-04-23',
             recency_flag='in_window', notes='Not in CD01-CD49 (not found by the EDGAR pass)'),
        dict(common, program_id='CN02', company='eBay (eBay Foundation)', sponsor='Silicon Valley Community Foundation', fund_name='eBay Foundation corporate advised fund',
             program_type='corporate_advised_fund', year_established='2008', evidence_year='2021-2023',
             amount_basis='"eBay Foundation, which has had a corporate advised fund at SVCF since 2008"', purpose_tags='foundation brand on a corporate advised fund',
             source_url='https://www.svcf.org/annual-reports/donor/donor-stories-ebay', source_date='2023-10-05',
             recency_flag='in_window', notes='Not in CD01-CD49'),
        dict(common, program_id='CN03', company='Bain Capital', sponsor='The Boston Foundation', fund_name='Bain Capital Relief Fund',
             program_type='corporate_daf', evidence_year='undated page (live 2026-11-19)',
             amount_basis='"the Bain Capital Relief Fund, a corporate Donor Advised Fund (DAF)"', purpose_tags='disaster relief',
             source_url='https://www.tbf.org/donors/company-giving', source_date='live 2026-11-19', recency_flag='in_window_edge',
             notes='Private company; page undated, so the fund date is not established'),
        dict(common, program_id='CN04', company='Income Research + Management', sponsor='The Boston Foundation', fund_name='(not named)',
             program_type='corporate_daf', evidence_year='undated page (live 2026-11-19)',
             amount_basis='"Why One Firm Chose a DAF for Its Corporate Philanthropy" (IR+M considered a private foundation)', purpose_tags='private-foundation alternative',
             source_url='https://www.tbf.org/donors/company-giving', source_date='live 2026-11-19', recency_flag='in_window_edge',
             notes='Private company'),
    ]


def build(root, extract_path):
    rows = latest_per_period(json.load(open(extract_path)))
    cols = header(root)
    e = estimates(rows)
    out = ([nosplit_row(i + 1, r) for i, r in enumerate(rows)] + list(map(published_row, PUBLISHED))
           + estimate_rows(e) + named_rows())
    with open(os.path.join(root, OUT), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); list(map(w.writerow, out))
    return e, len(out), len(rows)


if __name__ == '__main__':
    e, n, nr = build(sys.argv[1], sys.argv[2])
    print(json.dumps(dict(e, rows_written=n, returns=nr), indent=1, default=str))
