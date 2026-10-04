"""Validation of the SIPP extract against published figures.

Usage: python3 sipp/scripts/validate.py
Output: sipp/output/sipp_validation_census_wealth.csv  household ownership rates and conditional medians vs Census
                                                        "Wealth, Asset Ownership, & Debt of Households" tables
                                                        (2022 from SIPP 2023, 2023 from SIPP 2024)
        sipp/output/sipp_vs_irs_ira.csv                 SIPP IRA holders/withdrawers/dollars vs IRS SOI IRA Table 4
                                                        (project file data/irs_derived.json), ref years 2020-2023
"""
import json, os, subprocess
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
DATA = os.path.join(HERE, '..', 'data', 'sipp_persons_dec.parquet')
OUT = os.path.join(HERE, '..', 'output')
TMP = '/tmp/sipp/doc'
os.makedirs(TMP, exist_ok=True)
URL = 'https://www2.census.gov/programs-surveys/demo/tables/wealth/{y}/wealth-asset-ownership/wealth_tables_dy{y}.xlsx'
AGES = {'Total': (0, 200), '55 to 64 years': (55, 64), '65 years and over': (65, 200), '.65 to 69 years': (65, 69),
        '.70 to 74 years': (70, 74), '.75 and over': (75, 200)}


def wmedian(x, w):
    o = np.argsort(x); x, w = x[o], w[o]; c = np.cumsum(w)
    return float(x[np.searchsorted(c, 0.5 * c[-1])])


def households(d, y):
    x = d[d.sipp_year == y].copy()
    x['hh'] = x.SSUID + '_' + x.ERESIDENCEID.astype(str)
    x['ira_o'], x['dc_o'] = x.EOWN_IRAKEO.eq(1), x.EOWN_THR401.eq(1)
    x['ira_v'], x['dc_v'] = x.TIRAKEOVAL.fillna(0), x.TTHR401VAL.fillna(0)
    h = x.groupby('hh').agg(ira_o=('ira_o', 'max'), dc_o=('dc_o', 'max'), ira_v=('ira_v', 'sum'), dc_v=('dc_v', 'sum'))
    rp = x[x.ERELRPE.isin([1, 2])].drop_duplicates('hh').set_index('hh')[['TAGE_EHC', 'WPFINWGT']].join(h)
    rp['any_o'] = rp.ira_o | rp.dc_o
    rp['any_v'] = rp.ira_v + rp.dc_v
    return rp


def census_tables(year):
    p = os.path.join(TMP, f'wealth_tables_dy{year}.xlsx')
    if not os.path.exists(p):
        subprocess.run(['curl', '-sS', '-f', '-o', p, URL.format(y=year)], check=True)
    res = {}
    for tab, kind in (('Table 2', 'pct'), ('Table 1', 'median')):
        t = pd.read_excel(p, sheet_name=tab, header=None)
        hdr = t.iloc[2:4].apply(lambda col: ' '.join(str(v) for v in col)).str.lower().tolist()
        cols = {'any': [i for i, h in enumerate(hdr) if 'retirement accounts' in h][0]}
        cols['ira'] = [i for i, h in enumerate(hdr) if 'ira or keogh' in h][0]
        cols['dc'] = [i for i, h in enumerate(hdr) if '401(k)' in h][0]
        lab = t.iloc[:, 0].astype(str).str.strip()
        for age in AGES:
            r = lab[lab == age].index[0]
            for a, c in cols.items():
                res[(kind, a, age)] = t.iloc[r, c]
    return res


def main():
    d = pd.read_parquet(DATA)
    d = d[d.WPFINWGT > 0]
    rows = []
    for ref in (2022, 2023):
        pub = census_tables(ref)
        hh = households(d, ref + 1)
        for age, (lo, hi) in AGES.items():
            g = hh[hh.TAGE_EHC.between(lo, hi)]
            w = g.WPFINWGT.to_numpy()
            for a in ('any', 'ira', 'dc'):
                own = g[a + '_o'].to_numpy()
                rows.append(dict(ref_year=ref, sipp_year=ref + 1, age_of_householder=age.strip('.'), account=a,
                                 measure='pct_households_owning', sipp=round(100 * np.average(own, weights=w), 1),
                                 census_published=pub[('pct', a, age)]))
                rows.append(dict(ref_year=ref, sipp_year=ref + 1, age_of_householder=age.strip('.'), account=a,
                                 measure='median_value_owners_usd',
                                 sipp=round(wmedian(g.loc[own, a + '_v'].to_numpy(), w[own]), 0),
                                 census_published=pub[('median', a, age)]))
    v = pd.DataFrame(rows)
    v['diff'] = pd.to_numeric(v.sipp) - pd.to_numeric(v.census_published, errors='coerce')
    v.to_csv(os.path.join(OUT, 'sipp_validation_census_wealth.csv'), index=False)
    print(v.to_string())

    # IRS SOI comparison (individual taxpayers; IRS ages at end of tax year, like SIPP's December age)
    irs = json.load(open(os.path.join(ROOT, 'data', 'irs_derived.json')))['age']
    p = d[(d.sipp_year >= 2021)].copy()
    p['ye'] = p.EOWN_IRAKEO.eq(1) & p.TIRAKEOVAL.fillna(0).gt(0) & ~(p.EIRA_INC_YN.isna())
    p['wd'] = p.EIRA_INC_YN.eq(1)
    p['amt'] = np.where(p.wd, p.TIRA_INC_AMT.fillna(0), 0)
    bands = {'60-64': (60, 64), '65-69': (65, 69), '70-74': (70, 74), '75-79': (75, 79), '80+': (80, 200),
             '70+': (70, 200)}
    rows = []
    for y in range(2020, 2024):
        for b, (lo, hi) in bands.items():
            g = p[(p.ref_year == y) & p.ye & p.TAGE_EHC.between(lo, hi)]
            w = g.WPFINWGT
            i = irs[str(y)][b]
            rows.append(dict(ref_year=y, age_band=b,
                             sipp_holders_m=round(w.sum() / 1e6, 2), irs_holders_m=round(i['hn'] / 1e6, 2),
                             sipp_withdrawers_m=round(w[g.wd].sum() / 1e6, 2), irs_withdrawers_m=round(i['wn'] / 1e6, 2),
                             sipp_incidence=round(100 * w[g.wd].sum() / w.sum(), 1), irs_incidence=round(100 * i['wn'] / i['hn'], 1),
                             sipp_withdrawals_bn=round((w * g.amt).sum() / 1e9, 1), irs_withdrawals_bn=round(i['wa'] / 1e6, 1),
                             sipp_balances_bn=round((w * g.TIRAKEOVAL).sum() / 1e9, 0), irs_fmv_bn=round(i['fa'] / 1e6, 0),
                             sipp_rate_same_year=round(100 * (w * g.amt).sum() / (w * g.TIRAKEOVAL).sum(), 2),
                             irs_rate_same_year=round(100 * i['wa'] / i['fa'], 2)))
    r = pd.DataFrame(rows)
    r.to_csv(os.path.join(OUT, 'sipp_vs_irs_ira.csv'), index=False)
    print(r.to_string())


if __name__ == '__main__':
    main()
