"""CMS National Health Expenditure (NHE) personal health care (PHC) spending by age, 2002-2020 (every 2 years; latest release).

Input : raw/nhe_age/ageandgendercsvfiles.zip  ('age and Sex major age group.csv' = $ millions by payer x service x age;
        'age and Sex percap major group.csv' = per capita $ by service x age)
        raw/bls/cpiu_CUUR0000SA0.txt (CPI-U, to express in 2024 dollars)
Output: output/nhe_65plus.csv  per year: per-capita PHC 65+ (nominal, 2024$), ratio to 19-64, 65+ share of PHC,
        payer shares of 65+ PHC (Medicare, Medicaid, private insurance, out-of-pocket, other), OOP per capita 65+,
        nursing-home share of 65+ OOP.
"""
import os, zipfile, io
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, '..', 'raw'); OUT = os.path.join(HERE, '..', 'output')

def main():
    z = zipfile.ZipFile(os.path.join(RAW, 'nhe_age', 'ageandgendercsvfiles.zip'))
    agg = pd.read_csv(io.BytesIO(z.read('age and Sex major age group.csv')))
    pc = pd.read_csv(io.BytesIO(z.read('age and Sex percap major group.csv')))
    c = pd.read_csv(os.path.join(RAW, 'bls', 'cpiu_CUUR0000SA0.txt'), sep='\t', header=None)
    c = c[c[2].str.strip() == 'M13'].set_index(1)[3].astype(float)
    years = [y for y in agg.columns if y.isdigit()]
    A = lambda payer, svc, age: agg[(agg.Payer == payer) & (agg.Service == svc) & (agg['Age Group'] == age) & (agg.Sex == 'Total')][years].iloc[0].astype(float)
    P = lambda svc, age: pc[(pc.Service == svc) & (pc['Age Group'] == age) & (pc.Sex == 'Total')][years].iloc[0].astype(float)
    T = 'Total Personal Health Care'; NH = 'Nursing Care Facilities and Continuing Care Retirement Communities'
    tot65 = A('Total', T, '65+'); pc65 = P(T, '65+'); pop65 = tot65 / pc65 * 1e6
    r = pd.DataFrame(index=[int(y) for y in years])
    r.index.name = 'year'
    r['phc_per_capita_65plus_nominal'] = pc65.values
    r['phc_per_capita_65plus_2024usd'] = pc65.values * (c[2024] / c.reindex(r.index)).values
    r['ratio_65plus_to_19_64_per_capita'] = (pc65 / P(T, '19-64')).values
    r['share_of_all_phc_65plus_pct'] = (100 * tot65 / A('Total', T, 'Total')).values
    r['pop65_implied_m'] = (pop65 / 1e6).values
    for payer, lab in [('Medicare', 'medicare'), ('Medicaid', 'medicaid'), ('Private health Insurance', 'private_ins'),
                       ('Out-of-Pocket', 'oop'), ('Other Payers and Programs', 'other')]:
        r[f'payer_share_{lab}_pct'] = (100 * A(payer, T, '65+') / tot65).values
    oop65 = A('Out-of-Pocket', T, '65+')
    r['oop_per_capita_65plus_nominal'] = (oop65 * 1e6 / pop65).values
    r['oop_per_capita_65plus_2024usd'] = r.oop_per_capita_65plus_nominal * (c[2024] / c.reindex(r.index)).values
    r['nursing_home_share_of_65plus_oop_pct'] = (100 * A('Out-of-Pocket', NH, '65+') / oop65).values
    r = r.round(2)
    r.reset_index().to_csv(os.path.join(OUT, 'nhe_65plus.csv'), index=False)
    print(r[['phc_per_capita_65plus_nominal', 'phc_per_capita_65plus_2024usd', 'ratio_65plus_to_19_64_per_capita',
             'share_of_all_phc_65plus_pct', 'payer_share_medicare_pct', 'payer_share_oop_pct',
             'oop_per_capita_65plus_2024usd', 'nursing_home_share_of_65plus_oop_pct']].round(1).to_string())
    g = 100 * ((r.phc_per_capita_65plus_2024usd[2020] / r.phc_per_capita_65plus_2024usd[2002]) ** (1 / 18) - 1)
    g19 = 100 * ((r.phc_per_capita_65plus_2024usd[2018] / r.phc_per_capita_65plus_2024usd[2002]) ** (1 / 16) - 1)
    print(f'real growth per capita 65+ PHC: 2002-2020 {g:.2f}%/yr, 2002-2018 {g19:.2f}%/yr')

if __name__ == '__main__':
    main()
