"""MEPS-HC out-of-pocket (OOP) health spending for people 65+, 1996-2024, from raw/meps_slim (see extract_meps.py).

OOP = TOTSLF: payments by the person/family for care received in the year (all service types incl. prescription drugs).
It EXCLUDES insurance premiums (Medicare Part B/D, Medigap, MA, employer retiree plans) and over-the-counter items.
MEPS covers the civilian non-institutionalized population (no nursing-home residents).

Outputs (output/):
  meps_oop_65plus.csv     one row per year: levels (nominal and 2024$ via CPI-U), skew, burden vs income, SEs
  meps_oop_by_age.csv     mean OOP and OOP share of total spending by age group, per year
"""
import os, glob
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, '..', 'raw')
OUT = os.path.join(HERE, '..', 'output')

def cpi():
    d = pd.read_csv(os.path.join(RAW, 'bls', 'cpiu_CUUR0000SA0.txt'), sep='\t', header=None,
                    names=['sid', 'year', 'period', 'value', 'fn'])
    d = d[d.period.str.strip() == 'M13']
    return d.set_index('year')['value'].astype(float)

def wq(x, w, q):
    o = np.argsort(x); x, w = x[o], w[o]; c = np.cumsum(w) / w.sum()
    return x[np.searchsorted(c, q)]

def top_share(x, w, p):
    """share of weighted total held by the top p fraction of people"""
    o = np.argsort(-x); x, w = x[o], w[o]; cw = np.cumsum(w) / w.sum()
    k = np.searchsorted(cw, p)                 # people fully inside top p
    tot = (x * w).sum()
    inside = (x[:k] * w[:k]).sum()
    prev = cw[k - 1] if k > 0 else 0.0
    part = (p - prev) * w.sum() * x[k]         # fractional weight of boundary person
    return (inside + part) / tot

def lin_se(z, w, strat, psu):
    """Taylor-linearization SE of a ratio/mean given influence values z (already scaled by 1/sum(w))."""
    d = pd.DataFrame({'u': w * z, 'h': strat, 'j': psu})
    t = d.groupby(['h', 'j']).u.sum().reset_index()
    v = 0.0
    for h, g in t.groupby('h'):
        n = len(g)
        if n > 1:
            v += n / (n - 1) * ((g.u - g.u.mean()) ** 2).sum()
    return np.sqrt(v)

def se_mean(y, w, s, p):
    m = np.sum(w * y) / w.sum()
    return lin_se((y - m) / w.sum(), w, s, p)

def se_ratio(y, x, w, s, p):
    r = np.sum(w * y) / np.sum(w * x)
    return lin_se((y - r * x) / np.sum(w * x), w, s, p)

def main():
    c = cpi(); base = c[2024]
    rows, agerows = [], []
    for f in sorted(glob.glob(os.path.join(RAW, 'meps_slim', 'meps_fyc_*.csv.gz'))):
        d = pd.read_csv(f)
        yr = int(d.year.iloc[0])
        d = d[d.wt > 0].copy()
        for col in ['oop', 'totexp', 'pinc']:
            d[col] = d[col].astype(float)
        # family (CPS-definition) income and OOP: sum over members of DUID x CPSFAMID
        d['fkey'] = d.duid.astype(str) + '_' + d.famid.astype(str)
        g = d.groupby('fkey')
        d['fam_inc_sum'] = g.pinc.transform('sum')
        d['fam_oop'] = g.oop.transform('sum')
        finc = d['faminc'].astype(float) if 'faminc' in d and d['faminc'].notna().any() else d['fam_inc_sum']
        d['finc'] = finc
        d['burden'] = np.where(d.finc > 0, d.fam_oop / d.finc.where(d.finc > 0), np.nan)
        hi10 = np.where(d.finc > 0, d.burden > 0.10, d.fam_oop > 0)   # income<=0 with OOP>0 counted as high burden
        hi20 = np.where(d.finc > 0, d.burden > 0.20, d.fam_oop > 0)
        d['hi10'] = hi10.astype(float); d['hi20'] = hi20.astype(float)
        a = d[d.age >= 65]
        y, w = a.oop.values, a.wt.values
        s, p = a.varstr.values, a.varpsu.values
        defl = base / c[yr]
        fam_check = np.nan
        if 'faminc' in d and d['faminc'].notna().any():
            fam_check = np.average(np.isclose(d.faminc, d.fam_inc_sum, atol=1), weights=d.wt)
        rows.append({
            'year': yr, 'n_65plus': len(a), 'pop_65plus_m': w.sum() / 1e6,
            'mean_oop_nominal': np.average(y, weights=w), 'se_mean_oop_nominal': se_mean(y, w, s, p),
            'mean_oop_2024usd': np.average(y, weights=w) * defl,
            'median_oop_2024usd': wq(y, w, 0.5) * defl, 'p90_oop_2024usd': wq(y, w, 0.9) * defl,
            'p99_oop_2024usd': wq(y, w, 0.99) * defl,
            'mean_totexp_2024usd': np.average(a.totexp, weights=w) * defl,
            'pct_any_oop': 100 * np.average(y > 0, weights=w),
            'oop_pct_of_total_spending': 100 * np.sum(w * y) / np.sum(w * a.totexp),
            'top10_share_oop_pct': 100 * top_share(y, w, 0.10), 'top1_share_oop_pct': 100 * top_share(y, w, 0.01),
            'top50_share_oop_pct': 100 * top_share(y, w, 0.50),
            'top10_share_totexp_pct': 100 * top_share(a.totexp.values, w, 0.10),
            'agg_oop_pct_of_agg_person_income': 100 * np.sum(w * y) / np.sum(w * a.pinc),
            'se_agg_oop_pct_income': 100 * se_ratio(y, a.pinc.values, w, s, p),
            'median_family_burden_pct': 100 * wq(a.burden.fillna(np.inf).values, w, 0.5),
            'pct_family_oop_gt10pct_income': 100 * np.average(a.hi10, weights=w),
            'se_pct_gt10': 100 * se_mean(a.hi10.values, w, s, p),
            'pct_family_oop_gt20pct_income': 100 * np.average(a.hi20, weights=w),
            'under65_mean_oop_2024usd': np.average(d[(d.age < 65) & (d.age >= 0)].oop, weights=d[(d.age < 65) & (d.age >= 0)].wt) * defl,
            'under65_pct_family_oop_gt10pct_income': 100 * np.average(d[(d.age < 65) & (d.age >= 0)].hi10,
                                                                      weights=d[(d.age < 65) & (d.age >= 0)].wt),
            'faminc_source': 'FAMINC' if 'faminc' in d and d['faminc'].notna().any() else 'sum of member TTLP',
            'share_persons_faminc_eq_member_sum': fam_check,
        })
        for lab, lo, hi in [('0-64', 0, 64), ('65-74', 65, 74), ('75-84', 75, 84), ('85+', 85, 200)]:
            b = d[(d.age >= lo) & (d.age <= hi)]
            agerows.append({'year': yr, 'age': lab, 'mean_oop_2024usd': np.average(b.oop, weights=b.wt) * defl,
                            'mean_totexp_2024usd': np.average(b.totexp, weights=b.wt) * defl,
                            'oop_pct_of_total': 100 * np.sum(b.wt * b.oop) / np.sum(b.wt * b.totexp)})
    r = pd.DataFrame(rows).round(3)
    r.to_csv(os.path.join(OUT, 'meps_oop_65plus.csv'), index=False)
    pd.DataFrame(agerows).round(2).to_csv(os.path.join(OUT, 'meps_oop_by_age.csv'), index=False)
    show = ['year', 'n_65plus', 'mean_oop_2024usd', 'median_oop_2024usd', 'oop_pct_of_total_spending',
            'top10_share_oop_pct', 'agg_oop_pct_of_agg_person_income', 'pct_family_oop_gt10pct_income', 'se_pct_gt10']
    print(r[r.year.isin([1996, 2000, 2005, 2010, 2015, 2019, 2020, 2021, 2022, 2023, 2024])][show].round(1).to_string(index=False))
    print('FAMINC = sum of member TTLP (weighted share of persons), years with FAMINC:',
          r.share_persons_faminc_eq_member_sum.dropna().round(3).agg(['min', 'max']).tolist())

if __name__ == '__main__':
    main()
