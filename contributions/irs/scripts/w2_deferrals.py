"""Employer-plan elective deferrals from IRS SOI Form W-2 statistics, TY2008-2020 (latest posted as of 2026-10-06).

Adds AMOUNTS and contribution rates to the participation shares already built by the dc_policy thread
(dc_policy/output/irs_w2_deferral_participation.csv, read-only here).

Outputs (output/):
  w2_deferrals_by_age.csv        Table 2.A (deferrers, Medicare wages, contributions) + Table 1.A (all wage earners, box-1 wages) + Table 2.F (at max)
  w2_deferrals_by_wage_size.csv  Table 2.B + Table 1.B by size of wage income
  w2_deferrals_by_plan_type.csv  Table 7.A (2008-2018) / 4.D (2019-2020) by W-2 box 12 code
  w2_deferrals_totals.csv        national totals incl. Table 5.A/4.B box-1 and box-5 wage totals
Raw: raw/w2/18inallw2.xls (2008-2018), 19in0Xw2all.xlsx, 20in0Xw2all.xlsx. Run: python3 -I w2_deferrals.py
"""
import os, re
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw', 'w2')
OUT = os.path.join(ROOT, 'output')
SOI = 'https://www.irs.gov/pub/irs-soi/'
PART = os.path.join(os.path.dirname(ROOT), '..', 'dc_policy', 'output', 'irs_w2_deferral_participation.csv')
PART = os.path.normpath(os.path.join(ROOT, '..', '..', 'dc_policy', 'output', 'irs_w2_deferral_participation.csv'))

def num(v):
    if isinstance(v, (int, float)) and not pd.isna(v): return float(v)
    if isinstance(v, str):
        s = v.replace(',', '').strip()
        try: return float(s)
        except ValueError: return None
    return None

def sources(table):
    """yield (year, DataFrame-block, url) for a W-2 table across all files."""
    t = table.split('.')[0][-1]  # table group number 1/2/4/5/7
    x = pd.ExcelFile(os.path.join(RAW, '18inallw2.xls'))
    if table in x.sheet_names:
        df = pd.read_excel(x, sheet_name=table, header=None)
        starts = [i for i in range(len(df)) if isinstance(df.iat[i, 0], str) and re.match(r'Table \d\.[A-Z]', df.iat[i, 0].strip())]
        for k, s in enumerate(starts):
            m = re.search(r'Tax Years? (\d{4})', df.iat[s, 0].replace('\n', ' '))
            e = starts[k + 1] if k + 1 < len(starts) else len(df)
            yield (int(m.group(1)) if m else None), df.iloc[s:e].reset_index(drop=True), SOI + '18inallw2.xls'
    for y in (2019, 2020):
        f = f'{y % 100}in0{t}w2all.xlsx'
        p = os.path.join(RAW, f)
        if not os.path.exists(p): continue
        xx = pd.ExcelFile(p)
        if table in xx.sheet_names:
            yield y, pd.read_excel(xx, sheet_name=table, header=None), SOI + f

def body_rows(b):
    """Rows after the column-number row: returns list of (label, values list)."""
    k = next(i for i in range(len(b)) if num(b.iat[i, 1]) == 1 and num(b.iat[i, 2]) == 2)
    out = []
    for i in range(k + 1, len(b)):
        lab = b.iat[i, 0]
        if isinstance(lab, str) and re.match(r'\s*(\[|NOTE|SOURCE|\*|d |N/A)', lab): break
        vals = [num(v) for v in b.iloc[i, 1:]]
        if vals[0] is None: continue
        out.append(('All' if not isinstance(lab, str) or not lab.strip() else lab.strip().replace('\n', ' '), vals))
    return out

def main():
    # ---------- by age
    a2 = {(y, l): (v[0], v[1], v[2], u) for y, b, u in sources('Table 2.A') for l, v in body_rows(b)}
    a1 = {(y, l): (v[0], v[1], u) for y, b, u in sources('Table 1.A') for l, v in body_rows(b)}
    af = {(y, l): (v[0], v[1], v[2], u) for y, b, u in sources('Table 2.F') for l, v in body_rows(b)}
    rows = []
    for (y, l), (n, mw, c, u) in sorted(a2.items()):
        n1, w1, u1 = a1[(y, l)]
        fn, fw, fc, uf = af.get((y, l), (None, None, None, None))
        rows.append(dict(year=y, age=l, wage_earners=n1, wages_box1_k=w1, deferrers=n, deferrers_medicare_wages_k=mw, deferrals_k=c,
                         at_max_n=fn, at_max_deferrals_k=fc,
                         source=f'IRS SOI Form W-2 statistics Tables 1.A, 2.A, 2.F (TY{y}), {u}' + ('' if u1 == u else f' and {u1}')))
    d = pd.DataFrame(rows)
    d['pct_wage_earners_deferring'] = (100 * d.deferrers / d.wage_earners).round(2)
    d['avg_deferral_dollars'] = (1000 * d.deferrals_k / d.deferrers).round(0)
    d['deferral_rate_pct_of_pay_deferrers'] = (100 * d.deferrals_k / d.deferrers_medicare_wages_k).round(2)
    d['deferrals_pct_box1_wages_all'] = (100 * d.deferrals_k / d.wages_box1_k).round(2)
    d['pct_deferrers_at_max'] = (100 * d.at_max_n / d.deferrers).round(2)
    d['note'] = ('Unit = primary/secondary taxpayers on filed returns with W-2 wages. Deferrals = W-2 box 12 codes D,E,F,G,H,S,AA,BB,EE (pre-tax and Roth; employee elective only, '
                 'excludes employer match). deferral_rate = deferrals / Medicare wages (box 5, proxy for gross pay) of deferrers. deferrals_pct_box1_wages_all = deferrals / box-1 wages '
                 'of all wage earners in the group (box 1 excludes pre-tax deferrals, so this slightly overstates the share of gross pay). At max = deferrals at the 402(g) limit '
                 '(incl. catch-up where applicable) per Table 2.F.')
    d.to_csv(os.path.join(OUT, 'w2_deferrals_by_age.csv'), index=False)
    print('Deferral rate among deferrers (% of Medicare wages), by age:')
    print(d.pivot(index='year', columns='age', values='deferral_rate_pct_of_pay_deferrers').to_string())
    print('\nAverage deferral ($), by age:')
    print(d.pivot(index='year', columns='age', values='avg_deferral_dollars').to_string())
    print('\n% of deferrers at the maximum, by age:')
    print(d.pivot(index='year', columns='age', values='pct_deferrers_at_max').to_string())

    # ---------- by wage size
    b2 = {(y, l): (v[0], v[1], v[2], u) for y, b, u in sources('Table 2.B') for l, v in body_rows(b)}
    b1 = {(y, l): (v[0], v[1]) for y, b, u in sources('Table 1.B') for l, v in body_rows(b)}
    rows = []
    for (y, l), (n, mw, c, u) in sorted(b2.items()):
        n1, w1 = b1.get((y, l), (None, None))
        rows.append(dict(year=y, wage_size=l, wage_earners=n1, wages_box1_k=w1, deferrers=n, deferrers_medicare_wages_k=mw, deferrals_k=c,
                         source=f'IRS SOI Form W-2 statistics Tables 1.B and 2.B (TY{y}), {u}'))
    w = pd.DataFrame(rows)
    w['pct_wage_earners_deferring'] = (100 * w.deferrers / w.wage_earners).round(2)
    w['avg_deferral_dollars'] = (1000 * w.deferrals_k / w.deferrers).round(0)
    w['deferral_rate_pct_of_pay_deferrers'] = (100 * w.deferrals_k / w.deferrers_medicare_wages_k).round(2)
    w['note'] = 'Size of wage income bins are nominal dollars (box-1 wage income of the taxpayer). Definitions as in w2_deferrals_by_age.csv.'
    w.to_csv(os.path.join(OUT, 'w2_deferrals_by_wage_size.csv'), index=False)
    print('\nDeferral rate among deferrers by wage size (selected bins):')
    sel = ['$20,000 under $25,000', '$40,000 under $50,000', '$50,000 under $75,000', '$100,000 under $200,000', '$200,000 under $500,000']
    print(w[w.wage_size.isin(sel)].pivot(index='year', columns='wage_size', values='deferral_rate_pct_of_pay_deferrers').to_string())

    # ---------- by plan type
    rows = []
    for y, b, u in sources('Table 7.A'):
        hr = next(i for i in range(6) if num(b.iat[i, 1]) == 2008)
        hdr = [num(v) for v in b.iloc[hr]]
        years = {j: int(v) for j, v in enumerate(hdr) if v and v > 2000}
        for l, v in body_rows(b):
            for j, yy in years.items():
                rows.append(dict(year=yy, plan_type=l.replace('Total [1]', 'All').replace('Total', 'All'), taxpayers=v[j - 1], amount_k=v[j], source=f'IRS SOI Form W-2 statistics Table 7.A (TY2008-2018), {u}'))
    for y, b, u in sources('Table 4.D'):
        for l, v in body_rows(b):
            rows.append(dict(year=y, plan_type=l, taxpayers=v[0], amount_k=v[1], source=f'IRS SOI Form W-2 statistics Table 4.D (TY{y}), {u}'))
    p = pd.DataFrame(rows)
    p['plan_type'] = p.plan_type.replace({'All': 'All elective deferrals'})
    tot = p[p.plan_type == 'All elective deferrals'].set_index('year')['amount_k']
    p['share_of_all_deferral_dollars_pct'] = (100 * p.amount_k / p.year.map(tot)).round(2)
    p['avg_dollars'] = (1000 * p.amount_k / p.taxpayers).round(0)
    p['note'] = 'Taxpayers can appear under several codes; plan-type counts do not sum to the total. Roth 457(b) (code EE) available from 2011.'
    p.to_csv(os.path.join(OUT, 'w2_deferrals_by_plan_type.csv'), index=False)
    p['short'] = p.plan_type.str.extract(r'^(\S+ ?\S*)')[0]
    print('\nShare of deferral dollars by code:')
    print(p.pivot_table(index='year', columns='plan_type', values='share_of_all_deferral_dollars_pct').round(1).to_string()[:3000])

    # ---------- totals with box 1 / box 5
    rows = []
    for tab in ('Table 5.A', 'Table 4.B'):
        for y, b, u in sources(tab):
            lab = [str(x) for x in b[0]]
            i1 = next(i for i, s in enumerate(lab) if s.startswith('Box 1'))
            v1 = b.iloc[i1 + 1] if num(b.iat[i1, 1]) == 1 else b.iloc[i1]
            i5 = next(i for i, s in enumerate(lab) if s.startswith('Box 5'))
            rows.append(dict(year=y, box1_wages_k=num(v1.iloc[3]), box1_taxpayers=num(v1.iloc[2]), medicare_wages_k=num(b.iat[i5, 3]), medicare_taxpayers=num(b.iat[i5, 2]),
                             src_tot=f'IRS SOI Form W-2 statistics {tab} (TY{y}), {u}'))
    t = pd.DataFrame(rows).drop_duplicates('year').set_index('year')
    allage = d[d.age == 'All'].set_index('year')
    t = t.join(allage[['wage_earners', 'wages_box1_k', 'deferrers', 'deferrers_medicare_wages_k', 'deferrals_k', 'at_max_n', 'source']])
    roth = p[p.plan_type.str.startswith('Designated Roth')].groupby('year').amount_k.sum()
    t['roth_deferrals_k'] = roth
    t['roth_share_of_deferrals_pct'] = (100 * t.roth_deferrals_k / t.deferrals_k).round(2)
    t['pct_wage_earners_deferring'] = (100 * t.deferrers / t.wage_earners).round(2)
    t['avg_deferral_dollars'] = (1000 * t.deferrals_k / t.deferrers).round(0)
    t['deferral_rate_pct_of_pay_deferrers'] = (100 * t.deferrals_k / t.deferrers_medicare_wages_k).round(2)
    t['deferrals_pct_all_medicare_wages'] = (100 * t.deferrals_k / t.medicare_wages_k).round(2)
    t['deferrals_pct_all_box1_wages'] = (100 * t.deferrals_k / t.box1_wages_k).round(2)
    t['pretax_deferrals_k'] = t.deferrals_k - t.roth_deferrals_k
    t['deferrals_pct_box1_plus_pretax'] = (100 * t.deferrals_k / (t.box1_wages_k + t.pretax_deferrals_k)).round(2)
    t['pct_deferrers_at_max'] = (100 * t.at_max_n / t.deferrers).round(2)
    if os.path.exists(PART):
        pp = pd.read_csv(PART)
        pa = pp[pp.dimension == 'all'].set_index('year')
        t['check_participation_csv_pct'] = pa['pct_with_elective_deferral']
    t['source'] = t['source'] + '; ' + t['src_tot']
    t = t.drop(columns='src_tot').reset_index().sort_values('year')
    t['note'] = ('deferrals_pct_all_medicare_wages = all elective deferrals / box-5 Medicare wages of all W-2 taxpayers on filed returns (box 5 includes pre-tax deferrals). '
                 'CAUTION: published box-5 totals for TY2008 and TY2012 exceed box 1 by much more than in other years (2012: +$921bn vs +$245-336bn in 2009-2011, 2013-2020), so the Medicare-wage ratio dips in those years; '
                 'deferrals_pct_box1_plus_pretax (= deferrals / (box-1 wages + pre-tax deferrals)) is the steadier gross-pay denominator. '
                 'Coverage: filed individual returns only (non-filers excluded). Private and public employers. TY2021+ W-2 tables not posted as of 2026-10-06 (19in/20in only on the SOI W-2 page; 21in03w2all.xlsx returns 404).')
    t.to_csv(os.path.join(OUT, 'w2_deferrals_totals.csv'), index=False)
    print('\nNational totals:')
    print(t[['year', 'wage_earners', 'deferrers', 'pct_wage_earners_deferring', 'check_participation_csv_pct', 'deferrals_k', 'avg_deferral_dollars',
             'deferral_rate_pct_of_pay_deferrers', 'deferrals_pct_all_medicare_wages', 'deferrals_pct_box1_plus_pretax', 'roth_share_of_deferrals_pct', 'pct_deferrers_at_max']].to_string(index=False))

if __name__ == '__main__':
    main()
