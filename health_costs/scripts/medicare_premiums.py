"""Medicare Part B premium history vs the average Social Security benefit, and IRMAA reach, from the 2026 Medicare Trustees Report.

Inputs (raw/):
  medicare_trustees/tr2026_table_excerpts.txt   Tables III.C2 (Part B standard premium), V.B3 (enrollment), V.E3 (IRMAA)
  medicare_trustees/2026-expanded-supplementary-tables-figures.zip -> '2026TR Figures.xlsx' sheet II.F2
      (average OASI retired-worker benefit, average Part B+D premium, total Part B+D out-of-pocket = premium + cost sharing,
       average SMI benefit; all monthly, constant 2025 dollars; the sheet title says 2024 dollars but the report text and the
       implied deflator both say 2025, see check below)
  bls/cpiu_CUUR0000SA0.txt  CPI-U annual averages (to put the nominal Part B standard premium in the same constant dollars)
Outputs (output/):
  medicare_partb_vs_ss.csv  year, Part B standard premium (nominal), avg OASI benefit (2025$), shares of benefit
  medicare_irmaa.csv        year, beneficiaries paying IRMAA, Part B enrollment, share
"""
import os, re, zipfile, io
import numpy as np, pandas as pd, openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, '..', 'raw'); OUT = os.path.join(HERE, '..', 'output')
TXT = open(os.path.join(RAW, 'medicare_trustees', 'tr2026_table_excerpts.txt')).read()

def section(name):
    i = TXT.index('## ' + name); j = TXT.find('\n## ', i + 3)
    return TXT[i: j if j > 0 else None]

def num(s):
    return float(s.replace('$', '').replace(',', ''))

def partb_premium():
    out = {}
    for line in section('Table III.C2').splitlines():
        m = re.match(r'^\s+(19[89]\d|20[0-3]\d)\s+\$?([\d.]+)\s', line)
        if m:
            out[int(m.group(1))] = float(m.group(2))
    return pd.Series(out, name='partb_std_premium_nominal')

def enrollment():
    out = {}
    for line in section('Table V.B3').splitlines():
        m = re.match(r'^\s+(19\d\d|20\d\d)\s+([\d,]+)\s+([\d,]+)', line)
        if m:
            out[int(m.group(1))] = num(m.group(3)) * 1e3   # Part B enrollment, persons
    return pd.Series(out, name='partb_enrollment')

def irmaa():
    out = {}
    for line in section('Table V.E3').splitlines():
        m = re.match(r'^\s+(20\d\d)\s+(.*)$', line)
        if m:
            toks = m.group(2).split()
            out[int(m.group(1))] = (num(toks[-2]) * 1e6, num(toks[-1]))   # affected (millions), aggregate ($B)
    d = pd.DataFrame(out, index=['irmaa_payers', 'irmaa_aggregate_billion']).T
    return d

def fig_f2():
    with zipfile.ZipFile(os.path.join(RAW, 'medicare_trustees', '2026-expanded-supplementary-tables-figures.zip')) as z:
        wb = openpyxl.load_workbook(io.BytesIO(z.read('2026TR Figures.xlsx')), data_only=True)
    rows = [r for r in wb['II.F2'].iter_rows(values_only=True) if isinstance(r[0], (int, float))]
    d = pd.DataFrame([r[:5] for r in rows], columns=['year', 'avg_oasi_benefit_2025usd', 'avg_partBD_premium_2025usd',
                                                      'avg_partBD_premium_plus_costshare_2025usd', 'avg_smi_benefit_2025usd'])
    d = d[d.year == d.year.round()]     # drop the 2006.01 row (2006 recomputed with Part D)
    d['year'] = d.year.astype(int)
    return d.set_index('year')

def cpi():
    d = pd.read_csv(os.path.join(RAW, 'bls', 'cpiu_CUUR0000SA0.txt'), sep='\t', header=None,
                    names=['sid', 'year', 'period', 'value', 'fn'])
    d['period'] = d.period.str.strip()
    ann = d[d.period == 'M13'].set_index('year').value.astype(float)
    m26 = d[(d.year == 2026) & (d.period.str.match(r'M(0\d|1[0-2])$'))].value.astype(float)
    ann.loc[2026] = m26.mean()          # 2026: average of months released so far (flagged)
    return ann, len(m26)

def main():
    pb, f2, (c, n26) = partb_premium(), fig_f2(), cpi()
    d = f2.join(pb, how='left')
    defl = c[2025] / c
    d['partb_std_premium_2025usd'] = d.partb_std_premium_nominal * defl.reindex(d.index)
    d['partb_std_pct_of_avg_benefit'] = 100 * d.partb_std_premium_2025usd / d.avg_oasi_benefit_2025usd
    d['partBD_premium_pct_of_avg_benefit'] = 100 * d.avg_partBD_premium_2025usd / d.avg_oasi_benefit_2025usd
    d['partBD_prem_plus_costshare_pct_of_avg_benefit'] = 100 * d.avg_partBD_premium_plus_costshare_2025usd / d.avg_oasi_benefit_2025usd
    d['smi_benefit_pct_of_avg_benefit'] = 100 * d.avg_smi_benefit_2025usd / d.avg_oasi_benefit_2025usd
    d['projected'] = d.index > 2026
    # check: before Part D (<=2005) the Trustees' average SMI premium is the Part B premium, so the implied deflator
    # real/nominal should match CPI-U(2025)/CPI-U(t)
    chk = (d.loc[1985:2005, 'avg_partBD_premium_2025usd'] / d.loc[1985:2005, 'partb_std_premium_nominal']) / defl.loc[1985:2005]
    d = d.loc[1967:2035].round(3)
    d.reset_index().to_csv(os.path.join(OUT, 'medicare_partb_vs_ss.csv'), index=False)
    print('Deflator check 1985-2005 (Trustees implied / CPI-U 2025 base): min %.3f max %.3f' % (chk.min(), chk.max()))
    print(f'CPI-U 2026 = mean of {n26} released months')
    cols = ['partb_std_premium_nominal', 'avg_oasi_benefit_2025usd', 'partb_std_pct_of_avg_benefit',
            'partBD_premium_pct_of_avg_benefit', 'partBD_prem_plus_costshare_pct_of_avg_benefit']
    print(d.loc[[1970, 1980, 1990, 2000, 2005, 2006, 2010, 2015, 2020, 2024, 2025, 2026, 2030, 2035], cols].round(1).to_string())
    # IRMAA
    ir = irmaa().join(enrollment(), how='left')
    ir['pct_of_partb_enrollees'] = 100 * ir.irmaa_payers / ir.partb_enrollment
    ir.index.name = 'year'
    ir['projected'] = ir.index > 2026
    ir.round(3).reset_index().to_csv(os.path.join(OUT, 'medicare_irmaa.csv'), index=False)
    print(ir.dropna().round(2).to_string())
    # premium growth vs benefit growth
    g = lambda s, a, b: 100 * ((s[b] / s[a]) ** (1 / (b - a)) - 1)
    for a, b in [(1990, 2025), (2000, 2025), (2015, 2025)]:
        print(f'{a}-{b} real annual growth: Part B std premium {g(d.partb_std_premium_2025usd, a, b):.2f}%, '
              f'avg OASI benefit {g(d.avg_oasi_benefit_2025usd, a, b):.2f}%')

if __name__ == '__main__':
    main()
