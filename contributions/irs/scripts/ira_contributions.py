"""IRA contributions from the IRS SOI "Accumulation and Distribution of IRAs" tables, TY2000-2002, 2004-2023.

Outputs (output/):
  ira_contributions_by_type.csv      Table 1 by IRA type + Table 4 all-taxpayer denominators
  ira_contributions_by_age.csv       Table 4 by age (native 5-year bands + harmonised groups)
  ira_contributions_by_type_age.csv  Table 8 by IRA type and age (2017-2021, 2023)
  ira_contributions_at_limit.csv     Tables 5/6: share of traditional / Roth contributors contributing exactly the limit
Needs output/f1040_ira_keogh_deduction_long.csv (run f1040_long.py first) for total wages.
Raw files: raw/ira/ (downloaded by fetch.sh). Run: python3 -I ira_contributions.py
"""
import os, re
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw', 'ira')
OUT = os.path.join(ROOT, 'output')
SOI = 'https://www.irs.gov/pub/irs-soi/'
YEARS = [2000, 2001, 2002] + list(range(2004, 2024))

def fname(y, t):
    if y == 2000: return f'00in0{t}ir.xls'
    if y == 2002: return f'02in{t + 5:02d}ira.xls'   # 2002 numbering: Table 6 = by type, Table 10 = by age
    ext = 'xlsx' if y >= 2017 else 'xls'
    return f'{y % 100:02d}in{t:02d}ira.{ext}'

def T1(y):  # by-type table file
    return fname(y, 1)

def T4(y):  # by-age table file
    if y in (2000, 2001): return fname(y, 5)
    return fname(y, 4) if y != 2002 else '02in10ira.xls'

def num(v):
    if isinstance(v, (int, float)) and not pd.isna(v): return float(v)
    if isinstance(v, str):
        s = v.replace(',', '').replace('*', '').strip()
        try: return float(s)
        except ValueError: return None
    return None

def era(y):
    return 'new SOI methodology (2022+)' if y >= 2022 else 'former SOI methodology (2000-2021)'

TYPES = {'total': 'All IRA types', 'traditional': 'Traditional', 'roth': 'Roth', 'sep': 'SEP', 'simple': 'SIMPLE'}

def type_key(label):
    s = re.sub(r'^\s*\[\d+\]\s*', '', str(label)).strip().lower()
    if s.startswith('total'): return 'total'
    if s.startswith(('note', 'n/a', 'n.a', '[', 'source', '*')): return None
    for k in ('traditional', 'roth', 'sep', 'simple'):
        if k in s: return k
    return None

def read_t1(y):
    df = pd.read_excel(os.path.join(RAW, T1(y)), sheet_name=0, header=None)
    out = {}
    if y <= 2002:   # two stacked panels; panel 1: BOY FMV, contributions, deductible, rollovers; panel 2: conversions, withdrawals, return, EOY FMV
        hdr = ' '.join(str(x) for x in df.iloc[2, :]) + ' ' + ' '.join(str(x) for x in df.iloc[3, :])
        assert 'contributions' in hdr.lower(), hdr
        panel = 0
        for i in range(len(df)):
            k = type_key(df.iat[i, 0]) if isinstance(df.iat[i, 0], str) else None
            if k is None or all(num(v) is None for v in df.iloc[i, 1:]): continue
            if k == 'total': panel += 1
            rec = out.setdefault(k, {})
            if panel == 1:
                rec.update(contrib_n=num(df.iat[i, 3]), contrib_k=num(df.iat[i, 4]), deducted_n=num(df.iat[i, 5]), deducted_k=num(df.iat[i, 6]))
            elif panel == 2:
                rec.update(eoy_n=num(df.iat[i, 7]), eoy_fmv_k=num(df.iat[i, 8]))
    else:
        h = None
        for i in range(6):
            row = [str(x) for x in df.iloc[i]]
            if 'contributions' in row[1].lower(): h = row; break
        assert h and 'deduct' in h[3].lower() and 'fair market' in h[11].lower(), (y, h)
        for i in range(len(df)):
            k = type_key(df.iat[i, 0]) if isinstance(df.iat[i, 0], str) else None
            if k is None or k in out or all(num(v) is None for v in df.iloc[i, 1:]): continue
            out[k] = dict(contrib_n=num(df.iat[i, 1]), contrib_k=num(df.iat[i, 2]), deducted_n=num(df.iat[i, 3]), deducted_k=num(df.iat[i, 4]),
                          eoy_n=num(df.iat[i, 11]), eoy_fmv_k=num(df.iat[i, 12]))
    assert set(TYPES) <= set(out), (y, out.keys())
    return out

AGE_PAT = re.compile(r'(under \d+|\d+ under \d+|\d+ and over|\d+ under 70.?|70.? and over|all taxpayers|no age)', re.I)

def read_t4(y):
    """Return list of (age_label, taxpayers, eligible, contrib_n, contrib_k, eoy_n, eoy_fmv_k)."""
    df = pd.read_excel(os.path.join(RAW, T4(y)), sheet_name=0, header=None)
    rows = {}
    if y <= 2002:   # panel 1: total, pension, eligible, BOY FMV n/a, contributions n/a, deductible; panel 2: rollovers ... EOY n/a in cols 8,9
        panel = 0
        for i in range(len(df)):
            lab = df.iat[i, 0]
            if not isinstance(lab, str) or not AGE_PAT.search(lab.replace('…', '')): continue
            lab = re.sub(r'[.…]+$', '', lab.replace('…', '')).strip().rstrip(',').strip()
            if lab.lower().startswith('all taxpayers'): panel += 1; lab = 'All taxpayers'
            if panel == 1:
                rows[lab] = dict(taxpayers=num(df.iat[i, 1]), eligible=num(df.iat[i, 3]), contrib_n=num(df.iat[i, 6]), contrib_k=num(df.iat[i, 7]))
            elif panel == 2 and lab in rows:
                rows[lab].update(eoy_n=num(df.iat[i, 8]), eoy_fmv_k=num(df.iat[i, 9]))
    else:
        h = None
        for i in range(6):
            row = [str(x).replace('\n', ' ') for x in df.iloc[i]]
            if 'contributions' in row[4].lower(): h = row; break
        assert h and 'eligible' in h[3].lower() and 'fair market' in h[14].lower(), (y, h)
        for i in range(len(df)):
            lab = df.iat[i, 0]
            if not isinstance(lab, str) or not AGE_PAT.search(lab): continue
            if lab.strip().startswith('['): continue
            lab = lab.strip()
            if lab.lower().startswith('all taxpayers'): lab = 'All taxpayers'
            if num(df.iat[i, 1]) is None: continue
            rows[lab] = dict(taxpayers=num(df.iat[i, 1]), eligible=num(df.iat[i, 3]), contrib_n=num(df.iat[i, 4]), contrib_k=num(df.iat[i, 5]),
                             eoy_n=num(df.iat[i, 14]), eoy_fmv_k=num(df.iat[i, 15]))
    assert 'All taxpayers' in rows, y
    return rows

def harmonise(lab):
    """Map native 5-year bands to comparable groups."""
    s = lab.lower()
    m = re.match(r'(\d+) under (\d+)', s)
    lo = 0 if s.startswith('under') else (int(m.group(1)) if m else int(re.match(r'(\d+)', s).group(1)) if re.match(r'(\d+)', s) else None)
    if s.startswith('no age') or lo is None: return None
    if lo < 25: return 'Under 25'
    if lo < 35: return '25-34'
    if lo < 45: return '35-44'
    if lo < 55: return '45-54'
    if lo < 60: return '55-59'
    if lo < 65: return '60-64'
    if lo < 70: return '65-69'
    return '70+'

def main():
    w = pd.read_csv(os.path.join(OUT, 'f1040_ira_keogh_deduction_long.csv')).set_index('year')
    trows, arows = [], []
    for y in YEARS:
        t1 = read_t1(y); t4 = read_t4(y)
        allt = t4['All taxpayers']
        # consistency: Table 1 total contributors == Table 4 all-taxpayer contributors
        if abs(t1['total']['contrib_n'] - allt['contrib_n']) > 2:
            print(f'  note {y}: Table1 total contributors {t1["total"]["contrib_n"]:.0f} vs Table4 {allt["contrib_n"]:.0f}')
        for k, rec in t1.items():
            if k not in TYPES: continue
            wages = w.at[y, 'wages_k'] if y in w.index else None
            trows.append(dict(year=y, ira_type=TYPES[k], contributors=rec['contrib_n'], contributions_k=rec['contrib_k'],
                              deducted_n=rec.get('deducted_n'), deducted_k=rec.get('deducted_k'), eoy_owners=rec.get('eoy_n'), eoy_fmv_k=rec.get('eoy_fmv_k'),
                              all_taxpayers=allt['taxpayers'], taxpayers_eligible=allt['eligible'], f1040_wages_k=wages,
                              method_era=era(y), source=f'IRS SOI IRA Table 1 (by type of plan), TY{y}, {SOI}{T1(y)}; all taxpayers from Table 4/age table {SOI}{T4(y)}; wages from SOI Table 1.4/historical Table 1 (see f1040_ira_keogh_deduction_long.csv)'))
        for lab, r in t4.items():
            arows.append(dict(year=y, age_native=lab, age_group=('All' if lab == 'All taxpayers' else harmonise(lab)), **r,
                              method_era=era(y), source=f'IRS SOI IRA table by age of taxpayer, TY{y}, {SOI}{T4(y)}'))
    t = pd.DataFrame(trows)
    t['pct_all_taxpayers_contributing'] = (100 * t.contributors / t.all_taxpayers).round(2)
    t['pct_owners_contributing'] = (100 * t.contributors / t.eoy_owners).round(2)
    t['avg_contribution_dollars'] = (1000 * t.contributions_k / t.contributors).round(0)
    t['contrib_pct_eoy_fmv'] = (100 * t.contributions_k / t.eoy_fmv_k).round(3)
    t['contrib_pct_f1040_wages'] = (100 * t.contributions_k / t.f1040_wages_k).round(3)
    t['note'] = ('Unit = taxpayers (persons; spouses counted separately). Contributors = taxpayers with any contribution to that IRA type during the tax year (from Form 5498); '
                 'SEP/SIMPLE contributions include employer contributions. Owners = taxpayers with a year-end FMV > 0 of that type. Total row counts each taxpayer once. '
                 'pct_all_taxpayers = contributors / all primary+secondary taxpayers on filed returns. Wages = salaries and wages on Form 1040 (excludes pre-tax 401(k) deferrals). '
                 'TY2003 not published. TY2022-23 are a new SOI series (June 2026 revision; matched sample adds Forms W-2): not strictly comparable with 2021 and earlier.')
    t.to_csv(os.path.join(OUT, 'ira_contributions_by_type.csv'), index=False)
    print('IRA contributions by type (contributors, $bn, % of taxpayers, % of owners, avg $):')
    p = t.pivot_table(index='year', columns='ira_type', values=['contributors', 'pct_all_taxpayers_contributing', 'pct_owners_contributing', 'avg_contribution_dollars'])
    tt = t[t.ira_type == 'All IRA types'].set_index('year')
    print(pd.DataFrame({'contrib_M': (tt.contributors / 1e6).round(2), 'amt_bn': (tt.contributions_k / 1e6).round(1), 'pct_tax': tt.pct_all_taxpayers_contributing,
                        'pct_own': tt.pct_owners_contributing, 'pct_fmv': tt.contrib_pct_eoy_fmv, 'pct_wages': tt.contrib_pct_f1040_wages,
                        'trad%tax': p['pct_all_taxpayers_contributing']['Traditional'], 'roth%tax': p['pct_all_taxpayers_contributing']['Roth'],
                        'trad_avg': p['avg_contribution_dollars']['Traditional'], 'roth_avg': p['avg_contribution_dollars']['Roth']}).to_string())

    a = pd.DataFrame(arows)
    a = a[~a.age_native.str.lower().str.startswith('no age')]
    g = a[a.age_group.notna()].groupby(['year', 'age_group', 'method_era', 'source'], as_index=False)[['taxpayers', 'eligible', 'contrib_n', 'contrib_k', 'eoy_n', 'eoy_fmv_k']].sum(min_count=1)
    g['age_native'] = 'harmonised'
    a['age_native_flag'] = 'native'
    g['age_native_flag'] = 'harmonised'
    a2 = pd.concat([a[a.age_native != 'All taxpayers'].assign(age_group=a.age_native), g[g.age_group != 'All'], g[g.age_group == 'All'].assign(age_group='All')], ignore_index=True)
    a2 = a2.rename(columns={'age_native_flag': 'grouping', 'contrib_n': 'contributors', 'contrib_k': 'contributions_k', 'eoy_n': 'eoy_owners', 'eoy_fmv_k': 'eoy_fmv_k'})
    a2['pct_taxpayers_contributing'] = (100 * a2.contributors / a2.taxpayers).round(2)
    a2['pct_owners_contributing'] = (100 * a2.contributors / a2.eoy_owners).round(2)
    a2['avg_contribution_dollars'] = (1000 * a2.contributions_k / a2.contributors).round(0)
    a2['contrib_pct_eoy_fmv'] = (100 * a2.contributions_k / a2.eoy_fmv_k).round(3)
    bad = (a2.year == 2022) & a2.age_group.isin(['20 under 25', '25 under 30', 'Under 25', '25-34'])
    a2.loc[bad, ['pct_owners_contributing', 'contrib_pct_eoy_fmv']] = None
    a2['note'] = ('TY2022: year-end owners/FMV for 20-24 are published as 0 and appear combined into 25-29, so owner-based rates for these groups are blanked. ' if False else '') + ('All IRA types combined (each taxpayer once). Taxpayers = primary+secondary taxpayers on filed returns in the age group. Owners = year-end FMV > 0. '
                  'Native bands change: under-15/15-19 merged to under-20 from TY2022. Through TY2019 traditional contributions were barred at 70.5+ (SECURE Act removed the age cap from TY2020). '
                  'Harmonised groups sum native bands. TY2022+ new SOI series.')
    a2.loc[bad, 'note'] = 'TY2022 Table 4 shows 0 year-end owners/FMV at 20-24 (apparently combined into 25-29 for disclosure); owner-based rates blanked for these groups. ' + a2.loc[bad, 'note']
    a2 = a2[['year', 'grouping', 'age_group', 'taxpayers', 'eligible', 'contributors', 'contributions_k', 'eoy_owners', 'eoy_fmv_k', 'pct_taxpayers_contributing',
             'pct_owners_contributing', 'avg_contribution_dollars', 'contrib_pct_eoy_fmv', 'method_era', 'source', 'note']]
    a2 = a2.sort_values(['grouping', 'age_group', 'year'])
    a2.to_csv(os.path.join(OUT, 'ira_contributions_by_age.csv'), index=False)
    h = a2[a2.grouping == 'harmonised']
    print('\n% of all taxpayers contributing to any IRA, by age:')
    print(h.pivot(index='year', columns='age_group', values='pct_taxpayers_contributing').to_string())
    print('\n% of IRA owners contributing, by age:')
    print(h.pivot(index='year', columns='age_group', values='pct_owners_contributing').to_string())

    # ---------------- Table 8: by type and age (2017-2021, 2023; 2022 file not posted)
    t8 = []
    for y in range(2017, 2024):
        f = os.path.join(RAW, fname(y, 8))
        if not os.path.exists(f) or os.path.getsize(f) < 5000:
            continue
        try:
            df = pd.read_excel(f, sheet_name=0, header=None)
        except Exception:
            continue
        r2 = next(i for i in range(6) if any('Traditional IRA plans' in str(x) for x in df.iloc[i]))
        hdr2 = [str(x).strip() for x in df.iloc[r2]]
        starts = {j: type_key(s.split(' IRA')[0] if 'IRA' in s else s.split(' plans')[0]) for j, s in enumerate(hdr2) if j > 0 and s != 'nan'}
        hdr3 = [str(x) for x in df.iloc[r2 + 1]]
        for i in range(4, len(df)):
            lab = df.iat[i, 0]
            if not isinstance(lab, str) or not AGE_PAT.search(lab) or lab.startswith('[') or num(df.iat[i, 1]) is None: continue
            for j0, k in starts.items():
                assert 'contributions' in hdr3[j0].lower() and 'fair market' in hdr3[j0 + 3].lower(), (y, hdr3[j0], hdr3[j0 + 3])
                t8.append(dict(year=y, ira_type=TYPES[k], age=lab.strip(), contributors=num(df.iat[i, j0]), contributions_k=num(df.iat[i, j0 + 1]),
                               eoy_owners=num(df.iat[i, j0 + 3]), eoy_fmv_k=num(df.iat[i, j0 + 4]), method_era=era(y),
                               source=f'IRS SOI IRA Table 8 (by type of plan and age), TY{y}, {SOI}{fname(y, 8)}'))
    t8 = pd.DataFrame(t8)
    t8['pct_owners_contributing'] = (100 * t8.contributors / t8.eoy_owners).round(2)
    t8['avg_contribution_dollars'] = (1000 * t8.contributions_k / t8.contributors).round(0)
    t8['note'] = 'Owners = taxpayers with year-end FMV > 0 of that type. TY2022 Table 8 not posted (link 404 on 2026-10-06). Age bands differ by year (top band 70+ in 2023).'
    t8.to_csv(os.path.join(OUT, 'ira_contributions_by_type_age.csv'), index=False)
    print('\nTable 8 years:', sorted(t8.year.unique()))
    print(t8[t8.age.str.startswith('All')].pivot(index='year', columns='ira_type', values='pct_owners_contributing').to_string())

    # ---------------- Tables 5/6: contributing exactly the limit
    LIM = pd.read_csv(os.path.join(OUT, 'contribution_limits.csv')).set_index('year')
    lim = []
    for y in range(2004, 2024):
        for t, typ in ((5, 'Traditional'), (6, 'Roth')):
            f = fname(y, t)
            if y == 2004: f = {5: '04in06ira.xls', 6: '04in07ira.xls'}[t]
            df = pd.read_excel(os.path.join(RAW, f), sheet_name=0, header=None)
            title = str(df.iat[0, 0])
            assert typ.lower() in title.lower() and 'size of contribution' in title.lower() or 'by age' in title.lower(), (y, f, title)
            hdr = None
            for i in range(6):
                row = [str(x).replace('\n', ' ') for x in df.iloc[i]]
                if any(s.strip().startswith('Exactly') for s in row): hdr = row; break
            if hdr is None:
                continue
            ex = {}
            for j, s in enumerate(hdr):
                m = re.match(r'\s*Exactly \$([\d,]+)', s)
                if m: ex[j] = int(m.group(1).replace(',', ''))
            allr = next(i for i in range(len(df)) if isinstance(df.iat[i, 0], str) and df.iat[i, 0].strip().lower().startswith('all taxpayers'))
            tot_n = num(df.iat[allr, 1])
            base_limit = int(LIM.at[y, 'ira_limit']); catch_limit = int(LIM.at[y, 'ira_max_50plus'])
            assert base_limit in ex.values() and catch_limit in ex.values(), (y, typ, ex)
            jb = [j for j, v in ex.items() if v == base_limit][0]; jc = [j for j, v in ex.items() if v == catch_limit][0]
            n_at = (num(df.iat[allr, jb]) or 0) + (num(df.iat[allr, jc]) or 0)
            lim.append(dict(year=y, ira_type=typ, contributors=tot_n, at_regular_limit=num(df.iat[allr, jb]), at_catchup_limit=num(df.iat[allr, jc]),
                            regular_limit=base_limit, catchup_total_limit=catch_limit, pct_at_limit=round(100 * n_at / tot_n, 2), method_era=era(y),
                            source=f'IRS SOI IRA Table {"5" if typ == "Traditional" else "6"} (contributions by size and age), TY{y}, {SOI}{f}'))
    lim = pd.DataFrame(lim)
    lim['note'] = ('pct_at_limit = taxpayers contributing exactly the regular IRA limit or exactly the limit + age-50 catch-up (limits from contribution_limits.csv, matched to the "Exactly $X" columns), '
                   '/ all contributors of that type (any age; under-50s cannot use the catch-up). Excludes those below the limit because of income phase-outs or earned income.')
    lim.to_csv(os.path.join(OUT, 'ira_contributions_at_limit.csv'), index=False)
    print('\nShare of contributors at the limit:')
    print(lim.pivot(index='year', columns='ira_type', values='pct_at_limit').join(lim[lim.ira_type == 'Traditional'].set_index('year')[['regular_limit', 'catchup_total_limit']]).to_string())

if __name__ == '__main__':
    main()
