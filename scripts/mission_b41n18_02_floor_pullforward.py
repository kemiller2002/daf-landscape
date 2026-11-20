"""P-B41N18-02: did the 2026 corporate 1% floor (P.L. 119-21 s.70426) pull corporate DAF contributions into 2025?

usage: python3 -I scripts/mission_b41n18_02_floor_pullforward.py REPO_ROOT [--print]
  REPO_ROOT  repo root ('.')

Writes data/mission-2026-11-14/corporate-floor-pull-forward-2026-11-20.csv.
Every input figure below is quoted from the source in its row (label F = read this pass from the company's
or sponsor's own site; R = repo value or search-index capture, not re-read this pass). Every derived
column is computed here (label C). Pure functions, stdlib only.
"""
import csv, os, sys
from datetime import date

OUT = 'data/mission-2026-11-14/corporate-floor-pull-forward-2026-11-20.csv'

# Statute anchors (P.L. 119-21, govinfo): s.70426(d) "taxable years beginning after December 31, 2025";
# approved July 4, 2025. Ways and Means tax title text released 2025-05-12 (secondary: KPMG/EY alerts).
WM_TEXT = date(2025, 5, 12)
ENACTED = date(2025, 7, 4)

# first day of the first tax year the floor applies to, by fiscal-year end
FLOOR_START = {'calendar': date(2026, 1, 1), 'fye_jan31': date(2026, 2, 1)}

ROWS = (
    dict(row_id='PF01', company='Urban Outfitters', ticker='URBN', fiscal_year='fye_jan31',
         contribution_period='Q4 FY2026 (Nov 2025-Jan 2026)', contribution_date='', amount_usd=46_000_000,
         amount_label='R', vehicle='donor-advised fund (sponsor not named)', form='cash (not stated)',
         cadence='single contribution', pretax_income_usd=None, net_income_usd=464_900_000,
         tax_benefit_usd=None,
         disclosed_motive='Release: adjusted results exclude "a charitable contribution to a donor-advised fund" (non-core). Call [R]: "We intend to use this fund to support our charitable initiatives in the coming years."',
         mentions_floor_or_obbba='N (release)', followup_2026='not checked: investor.urbn.com robots.txt 403; FY2027 releases not reachable on urbn.com',
         evidence_class='timing_consistent_no_stated_tax_motive', label='F (release text); R (amount from repo 10-K row CD04; call quote search-index only)',
         source_url='https://www.urbn.com/blog/fy26-q4-results',
         access_note='investor.urbn.com and urbanoutfittersinc.gcs-web.com robots.txt 403; company blog copy of the GlobeNewswire release read'),
    dict(row_id='PF02', company='Apollo Global Management', ticker='APO', fiscal_year='calendar',
         contribution_period='Q1 2025', contribution_date='2025-02 (month only)', amount_usd=200_000_000,
         amount_label='F', vehicle='Apollo DAF (sponsor not named)', form='1,213,003 newly issued common shares',
         cadence='single issuance; none in 9M 2026', pretax_income_usd=6_677_000_000, net_income_usd=5_401_000_000,
         tax_benefit_usd=None,
         disclosed_motive='"as part of its ongoing commitment to philanthropy" (10-K 2024, 10-Qs 2026)',
         mentions_floor_or_obbba='N (OBBBA cited in 10-K 2025 only for CFC rules)',
         followup_2026='No DAF issuance in 9M 2026: cash-flow line "Issuance of common stock to donor-advised fund" is blank for 2026 and $200m for 9M 2025 (10-Q Q3 2026)',
         evidence_class='predates_proposal_not_floor_driven', label='F',
         source_url='https://ir.apollo.com/sec-filings/content/0001858681-26-000013/apo-20251231.htm',
         access_note='ir.apollo.com robots allow; also 10-K 2024 (0001858681-25-000034), 1Q25 earnings release, 10-Qs Q1-Q3 2026'),
    dict(row_id='PF03', company='Zoom Communications', ticker='ZM', fiscal_year='fye_jan31',
         contribution_period='FY2026 (Feb 2025-Jan 2026)', contribution_date='', amount_usd=20_900_000,
         amount_label='R', vehicle='DAF at an "unaffiliated nonprofit organization" (repo CD06)', form='common shares from FY2020 reserve',
         cadence='draws on a 500,000-share reserve set in FY2020', pretax_income_usd=None, net_income_usd=1_900_100_000,
         tax_benefit_usd=None,
         disclosed_motive='Not read this pass. FY2026 release excludes "expenses related to charitable donation of common stock" from non-GAAP [R, search-index]',
         mentions_floor_or_obbba='unknown', followup_2026='not checked: investors.zoom.us robots.txt 403',
         evidence_class='unverified_legacy_program', label='R',
         source_url='https://investors.zoom.us/node/14156/html',
         access_note='investors.zoom.us robots.txt 403; not fetched. Net income $1,900.1m is from a search-index capture of the FY2026 release'),
    dict(row_id='PF04', company='Circle Internet Group', ticker='CRCL', fiscal_year='calendar',
         contribution_period='Q4 2025', contribution_date='2025-11 (repo CD01, 10-K Note 15)', amount_usd=23_100_000,
         amount_label='R', vehicle='Circle Foundation, a DAF at Fidelity Charitable (2026 proxy, repo)', form='268,239 re-issued treasury shares',
         cadence='"first annual share contribution" of a Pledge 1% schedule (up to 2,682,392 shares over 10 years, repo)',
         pretax_income_usd=None, net_income_usd=None, tax_benefit_usd=None,
         disclosed_motive='"Seeded by Circle\'s Pledge 1% equity commitment" (blog, 2025-12-02); release: "$23 million charge related to our first annual share contribution to the Circle Foundation"',
         mentions_floor_or_obbba='N', followup_2026='Q1-Q3 2026 release narratives name no Circle Foundation charge (tables are images, not read)',
         evidence_class='scheduled_annual_pledge_not_pull_forward', label='F (release, blog); R ($23.1m and share count from repo)',
         source_url='https://www.circle.com/pressroom/circle-reports-fourth-quarter-and-full-fiscal-year-2025-financial-results',
         access_note='circle.com robots allow; s206.q4cdn.com (IR PDFs) robots.txt 403'),
    dict(row_id='PF05', company='BlackRock', ticker='BLK', fiscal_year='calendar',
         contribution_period='Q4 2025', contribution_date='2025-12-10', amount_usd=109_000_000,
         amount_label='F', vehicle='BlackRock Charitable Fund (est. 2013); called "existing donor-advised funds" on the Q4 call [R]',
         form='part of BlackRock\'s Circle stake', cadence='"nonrecurring"',
         pretax_income_usd=7_619_000_000, net_income_usd=None, tax_benefit_usd=29_000_000,
         disclosed_motive='"The Charitable Contribution will add to the long-term funding for BlackRock\'s philanthropic grants and programs"; excluded from as-adjusted results "due to its nonrecurring nature"',
         mentions_floor_or_obbba='N (OBBBA cited only for TCJA extension and international rules)',
         followup_2026='not checked',
         evidence_class='timing_consistent_no_stated_tax_motive', label='F',
         source_url='https://ir.blackrock.com/files/doc_financials/2026/ar/BLK_AR25.pdf',
         access_note='ir.blackrock.com robots allow (crawl-delay 10 honoured); s24.q4cdn.com robots.txt 403'),
    dict(row_id='PF06', company='Unum Group', ticker='UNM', fiscal_year='calendar',
         contribution_period='Q4 2025', contribution_date='', amount_usd=20_000_000,
         amount_label='F', vehicle='not named (not stated to be a DAF)', form='not stated',
         cadence='described as "accelerated"', pretax_income_usd=933_500_000, net_income_usd=None, tax_benefit_usd=4_200_000,
         disclosed_motive='"an expense related to an accelerated charitable contribution of $20.0 million before tax"; reason for acceleration not stated',
         mentions_floor_or_obbba='OBBBA: "We do not expect the OBBBA to have a material impact"; not linked to the contribution',
         followup_2026='not checked',
         evidence_class='self_described_acceleration_motive_unstated', label='F',
         source_url='https://investors.unum.com/files/doc_financials/2025/Unum-Group-2025-Annual-Report.pdf',
         access_note='investors.unum.com robots allow (crawl-delay 10 honoured); s201.q4cdn.com robots.txt 403'),
    dict(row_id='PF07', company='Community Financial System', ticker='CBU', fiscal_year='calendar',
         contribution_period='Q4 2025 (planned in Q3 2025 release)', contribution_date='', amount_usd=600_000,
         amount_label='R', vehicle='direct payment of existing charitable commitments (not a DAF)', form='cash',
         cadence='prepayment of commitments', pretax_income_usd=None, net_income_usd=None, tax_benefit_usd=None,
         disclosed_motive='"As a result of tax law changes enacted under the One Big Beautiful Bill Act that limit the deductibility of charitable contributions beginning in 2026, the Company plans to accelerate the payment of approximately $0.6 million of charitable contribution commitments in the fourth quarter of 2025" [R]',
         mentions_floor_or_obbba='Y', followup_2026='not checked',
         evidence_class='disclosed_floor_motive_non_daf', label='R (search-index capture of the company release; not fetched)',
         source_url='https://s204.q4cdn.com/276330220/files/doc_news/Community-Financial-System-Inc--Reports-Third-Quarter-2025-Results-2025.pdf',
         access_note='s204.q4cdn.com robots.txt 403 (not fetched); ir.cbna.com proxy 502; businesswire.com timed out'),
    dict(row_id='PF08', company='Live Oak Bancshares', ticker='LOB', fiscal_year='calendar',
         contribution_period='Q4 2025', contribution_date='', amount_usd=None,
         amount_label='', vehicle='company donor-advised fund [R]', form='not stated',
         cadence='not stated', pretax_income_usd=142_815_000, net_income_usd=None, tax_benefit_usd=None,
         disclosed_motive='Call [R]: "approximately $11 million of offsets from warrant losses, capitalized software accelerated depreciation, severance, and allocation of funding to our donor advised fund"; the release does not mention it',
         mentions_floor_or_obbba='N (release)', followup_2026='not checked',
         evidence_class='timing_consistent_unverified', label='F (release: no DAF line); R (call quote, search-index only)',
         source_url='https://investor.liveoak.bank/news/news-details/2026/Live-Oak-Bancshares-Inc--Reports-Fourth-Quarter-2025-Results/default.aspx',
         access_note='investor.liveoak.bank robots allow (crawl-delay 10 honoured)'),
    dict(row_id='SA01', company='Fidelity Charitable (sponsor aggregate)', ticker='', fiscal_year='calendar',
         contribution_period='CY2025 vs CY2024', contribution_date='', amount_usd=539_800_000,
         amount_label='F', vehicle='Corporate Giving Accounts', form='grants (no corporate contribution figure published)',
         cadence='556 corporate DAFs in 2025; 518 in 2024', pretax_income_usd=None, net_income_usd=None, tax_benefit_usd=None,
         disclosed_motive='Report ties overall DAF count growth (13.4% to 246,006) to "bunching donations in the face of tax law changes that took effect in 2026"; no such statement for corporate accounts',
         mentions_floor_or_obbba='N (names "tax law changes", not OBBBA or the corporate floor)',
         followup_2026='2027 Giving Report (covering 2026) not yet published',
         evidence_class='sponsor_aggregate_no_contribution_split', label='F',
         source_url='https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf',
         access_note='fidelitycharitable.org robots allow; 2025 report read for 2024 baseline ($525M grants, 518 DAFs)'),
)

FIDELITY = dict(dafs_2024=518, dafs_2025=556, grants_2024=525_000_000, grants_2025=539_800_000,
                all_dafs_growth_pct=13.4)


def pct(n, d):
    return '' if n is None or not d else f'{100 * n / d:.2f}'


def ratio(n, d):
    return '' if n is None or not d else f'{n / d:.2f}'


def days_before_floor(row):
    d = row['contribution_date']
    if len(d) != 10:
        return ''
    y, m, dd = map(int, d.split('-'))
    return str((FLOOR_START[row['fiscal_year']] - date(y, m, dd)).days)


def timing_vs_bill(row):
    d = row['contribution_date']
    if d.startswith('2025-02'):
        return 'before Ways and Means text (2025-05-12)'
    if row['contribution_period'].startswith(('Q4 2025', 'Q4 FY2026')):
        return 'after enactment (2025-07-04), last pre-floor tax year'
    return 'pre-floor tax year; exact date not known' if row['fiscal_year'] in FLOOR_START and row['row_id'] != 'SA01' else ''


def derive(row):
    pre, amt = row['pretax_income_usd'], row['amount_usd']
    extra = dict(
        floor_first_applies=FLOOR_START[row['fiscal_year']].isoformat() if row['row_id'] != 'SA01' else '2026-01-01 (calendar-year donors)',
        days_before_floor=days_before_floor(row),
        timing_vs_bill=timing_vs_bill(row),
        contribution_pct_pretax=pct(amt, pre),
        contribution_pct_net_income=pct(amt, row['net_income_usd']),
        multiple_of_1pct_pretax=ratio(amt, pre * 0.01 if pre else None),
        tax_benefit_rate_pct=pct(row['tax_benefit_usd'], amt),
    )
    return {**row, **extra}


def fidelity_checks(f):
    return dict(
        corporate_daf_growth_pct=f'{100 * (f["dafs_2025"] / f["dafs_2024"] - 1):.1f}',
        corporate_grant_growth_pct=f'{100 * (f["grants_2025"] / f["grants_2024"] - 1):.1f}',
        all_dafs_growth_pct=f'{f["all_dafs_growth_pct"]:.1f}',
    )


COLS = ('row_id', 'company', 'ticker', 'fiscal_year', 'floor_first_applies', 'contribution_period', 'contribution_date',
        'days_before_floor', 'timing_vs_bill', 'amount_usd', 'amount_label', 'vehicle', 'form', 'cadence',
        'pretax_income_usd', 'net_income_usd', 'contribution_pct_pretax', 'contribution_pct_net_income',
        'multiple_of_1pct_pretax', 'tax_benefit_usd', 'tax_benefit_rate_pct', 'disclosed_motive',
        'mentions_floor_or_obbba', 'followup_2026', 'evidence_class', 'label', 'source_url', 'access_note')


def to_csv_row(r):
    return {k: ('' if r.get(k) is None else r.get(k)) for k in COLS}


def main(root, show):
    rows = tuple(map(derive, ROWS))
    path = os.path.join(root, OUT)
    with open(path, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(map(to_csv_row, rows))
    summary = dict(rows=len(rows), fidelity=fidelity_checks(FIDELITY),
                   classes=sorted({r['evidence_class'] for r in rows}),
                   disclosed_floor_motive=[r['row_id'] for r in rows if r['mentions_floor_or_obbba'] == 'Y'])
    print(path, summary)
    if show:
        print('\n'.join(f"{r['row_id']} {r['ticker']}: pct_pretax={r['contribution_pct_pretax']} pct_ni={r['contribution_pct_net_income']} "
                        f"x1pct={r['multiple_of_1pct_pretax']} taxrate={r['tax_benefit_rate_pct']} days={r['days_before_floor']} | {r['timing_vs_bill']}"
                        for r in rows))


if __name__ == '__main__':
    main(sys.argv[1], '--print' in sys.argv[2:])
