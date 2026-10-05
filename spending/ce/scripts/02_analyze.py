"""Build analysis tables from output/ce_age_long.csv (BLS CE, LB04 age of reference person)
and output/cpi_u_annual.csv (CPI-U CUUR0000SA0 annual avg). Real values in 2024 dollars.
All inputs are BLS published means per consumer unit (CU); per-person = mean / mean CU size
(item 980010), a ratio of means, not a mean of per-person spending.
"""
import pandas as pd, pathlib
OUT = pathlib.Path(__file__).resolve().parents[1] / 'output'
d = pd.read_csv(OUT / 'ce_age_long.csv')
cpi = pd.read_csv(OUT / 'cpi_u_annual.csv').set_index('year').cpi_u
BASE = 2024
defl = cpi.loc[BASE] / cpi
P = d.pivot_table(index=['item_code', 'year'], columns='age_group', values='value')
AG = ['All CUs', '55-64', '65+', '65-74', '75+']

def s(item, ag):
    try:
        return P.loc[item][ag]
    except KeyError:
        return pd.Series(dtype=float)

# ---- T1: totals, real, per person, ratios, spending/income
rows = []
for y in range(1984, 2025):
    r = {'year': y, 'cpi_u': cpi.loc[y]}
    for ag in AG:
        tot = s('TOTALEXP', ag).get(y); sz = s('980010', ag).get(y)
        ib = s('INCBEFTX', ag).get(y); ia = s('INCAFTTX', ag).get(y)
        r[f'exp_nominal_{ag}'] = tot
        r[f'exp_real{BASE}_{ag}'] = None if pd.isna(tot) else round(tot * defl.loc[y])
        r[f'cu_size_{ag}'] = sz
        r[f'exp_real{BASE}_per_person_{ag}'] = None if pd.isna(tot) or pd.isna(sz) else round(tot * defl.loc[y] / sz)
        r[f'exp_pct_income_before_tax_{ag}'] = None if pd.isna(tot) or pd.isna(ib) else round(100 * tot / ib, 1)
        r[f'exp_pct_income_after_tax_{ag}'] = None if pd.isna(tot) or pd.isna(ia) else round(100 * tot / ia, 1)
    for ag in ['65-74', '75+', '65+']:
        a, b = r[f'exp_nominal_{ag}'], r['exp_nominal_55-64']
        r[f'ratio_{ag}_to_55-64'] = None if pd.isna(a) else round(a / b, 3)
        a, b = r[f'exp_real{BASE}_per_person_{ag}'], r[f'exp_real{BASE}_per_person_55-64']
        r[f'ratio_per_person_{ag}_to_55-64'] = None if a is None else round(a / b, 3)
    rows.append(r)
t1 = pd.DataFrame(rows)
t1.to_csv(OUT / 't1_total_spending_by_age.csv', index=False)

# ---- T2: budget shares (% of total average annual expenditures)
CATS = {'FOODTOTL': 'Food', 'FOODHOME': 'Food at home', 'FOODAWAY': 'Food away from home',
        'HOUSING': 'Housing', 'SHELTER': 'Shelter', 'UTILS': 'Utilities, fuels, public services',
        'TRANS': 'Transportation', 'VEHPURCH': 'Vehicle purchases',
        'HEALTH': 'Healthcare', 'HLTHINSR': 'Health insurance', 'MEDSERVS': 'Medical services',
        'DRUGS': 'Drugs', 'MEDSUPPL': 'Medical supplies', '580901': 'Medicare payments (Part B etc.)',
        '580907': 'Medicare prescription drug premiums',
        'ENTRTAIN': 'Entertainment', 'CASHCONT': 'Cash contributions',
        'INSPENSN': 'Personal insurance and pensions', 'PENSIONS': 'Retirement, pensions, Social Security',
        'LIFEINSR': 'Life and other personal insurance', 'APPAREL': 'Apparel and services',
        'EDUCATN': 'Education', 'PERSCARE': 'Personal care', 'READING': 'Reading',
        'TOBACCO': 'Tobacco', 'ALCBEVG': 'Alcoholic beverages', 'MISC': 'Miscellaneous'}
rows = []
for it, name in CATS.items():
    for ag in AG:
        v = s(it, ag); t = s('TOTALEXP', ag)
        for y, val in v.dropna().items():
            rows.append({'item_code': it, 'category': name, 'age_group': ag, 'year': y,
                         'nominal': val, f'real{BASE}': round(val * defl.loc[y]),
                         'share_of_total_pct': round(100 * val / t.loc[y], 2),
                         'series_id': f'CXU{it}LB04{dict(zip(["All CUs","55-64","65+","65-74","75+"],["01","06","07","08","09"]))[ag]}M'})
t2 = pd.DataFrame(rows)
t2.to_csv(OUT / 't2_budget_shares_long.csv', index=False)
main = ['Housing', 'Transportation', 'Food', 'Healthcare', 'Personal insurance and pensions',
        'Cash contributions', 'Entertainment', 'Apparel and services']
w = t2[t2.category.isin(main + ['Health insurance'])].pivot_table(index=['age_group', 'year'], columns='category', values='share_of_total_pct')
w = w[main + ['Health insurance']]
w['Healthcare: insurance as % of healthcare'] = (100 * t2[t2.category == 'Health insurance'].set_index(['age_group', 'year']).nominal
                                              / t2[t2.category == 'Healthcare'].set_index(['age_group', 'year']).nominal).round(1)
w.reset_index().to_csv(OUT / 't2_budget_shares_wide.csv', index=False)

# ---- T3: pandemic window 2017-2024, real 2024$ and index 2019=100 (65+, 65-74, 75+, 55-64)
pw = t2[(t2.year >= 2017) & t2.age_group.isin(['55-64', '65+', '65-74', '75+'])]
tot = pd.DataFrame([{'item_code': 'TOTALEXP', 'category': 'Total expenditures', 'age_group': ag, 'year': y,
                     f'real{BASE}': round(s('TOTALEXP', ag).loc[y] * defl.loc[y]), 'share_of_total_pct': 100.0}
                    for ag in ['55-64', '65+', '65-74', '75+'] for y in range(2017, 2025)])
pw = pd.concat([tot, pw])[['item_code', 'category', 'age_group', 'year', f'real{BASE}', 'share_of_total_pct']]
base = pw[pw.year == 2019].set_index(['item_code', 'age_group'])[f'real{BASE}']
pw['index_2019_eq_100'] = [round(100 * r[f'real{BASE}'] / base.loc[(r.item_code, r.age_group)], 1) for _, r in pw.iterrows()]
pw.to_csv(OUT / 't3_pandemic_2017_2024.csv', index=False)

# ---- T4: income sources, share of income before taxes
SRC = {'900000': 'Wages and salaries', 'SFEMPINC': 'Self-employment income',
       'RETIRINC': 'Social Security, private and government retirement',
       '900030': 'Social Security and railroad retirement (2010+)',
       '900040': 'Pensions and annuities (2010-2013)',
       '900170': 'Retirement, survivors, and disability income (2013+)',
       'INDIVRNT': 'Interest, dividends, rental and other property income',
       '900180': 'Interest and dividends (2013+)',
       'WELFARE': 'Public assistance, SSI, SNAP', 'OTHREGIN': 'Unemployment/workers comp/veterans/regular contributions',
       'OTHBNFTS': 'Unemployment, workers comp, veterans (to 2012)', 'REGCONT': 'Regular contributions for support (to 2012)',
       'OTHRINC': 'Other income'}
rows = []
for it, name in SRC.items():
    for ag in AG:
        v = s(it, ag); ib = s('INCBEFTX', ag)
        for y, val in v.dropna().items():
            rows.append({'item_code': it, 'source': name, 'age_group': ag, 'year': y, 'nominal': val,
                         f'real{BASE}': round(val * defl.loc[y]),
                         'share_of_income_before_tax_pct': round(100 * val / ib.loc[y], 1),
                         'income_method': 'complete income reporters only' if y <= 2003 else 'imputed, all CUs'})
t4 = pd.DataFrame(rows)
t4.to_csv(OUT / 't4_income_sources_long.csv', index=False)

# ---- T5: pseudo-cohorts: same birth cohorts observed 10 and 20 years later (per person, real)
rows = []
for y0 in range(1984, 2005):
    r = {'cohort_55_64_in': y0}
    for lag, ag in [(0, '55-64'), (10, '65-74'), (20, '75+')]:
        y = y0 + lag
        if y <= 2024:
            tot = s('TOTALEXP', ag).get(y); sz = s('980010', ag).get(y)
            r[f'{ag}_year'] = y
            r[f'{ag}_real{BASE}_per_CU'] = round(tot * defl.loc[y])
            r[f'{ag}_real{BASE}_per_person'] = round(tot * defl.loc[y] / sz)
    r['ratio_65-74_to_55-64_per_person'] = round(r[f'65-74_real{BASE}_per_person'] / r[f'55-64_real{BASE}_per_person'], 3) if f'65-74_real{BASE}_per_person' in r else None
    r['ratio_75+_to_55-64_per_person'] = round(r[f'75+_real{BASE}_per_person'] / r[f'55-64_real{BASE}_per_person'], 3) if f'75+_real{BASE}_per_person' in r else None
    rows.append(r)
pd.DataFrame(rows).to_csv(OUT / 't5_pseudo_cohorts.csv', index=False)

# ---- T6: older-CU characteristics (homeownership, mortgage, earners, CU size)
rows = []
for it, name in {'980010': 'Persons per CU', '980030': 'Earners per CU', '980020': 'Mean age of reference person',
                 'HOMEOWN': 'Percent homeowner', '980230': 'Percent homeowner with mortgage',
                 '980240': 'Percent homeowner without mortgage', '980260': 'Percent renter',
                 'CONSUNIT': 'Number of CUs (thousands)'}.items():
    for ag in AG:
        for y, val in s(it, ag).dropna().items():
            rows.append({'item_code': it, 'measure': name, 'age_group': ag, 'year': y, 'value': val})
pd.DataFrame(rows).to_csv(OUT / 't6_cu_characteristics.csv', index=False)
# ---- T7: full age profile (all LB04 bands), real 2024$ per CU and per person, selected years
rows = []
for y in [1984, 1990, 2000, 2007, 2019, 2024]:
    for ag in ['Under 25', '25-34', '35-44', '45-54', '55-64', '65-74', '75+', '65+', 'All CUs']:
        tot = s('TOTALEXP', ag).get(y); sz = s('980010', ag).get(y)
        if tot is None or pd.isna(tot):
            continue
        rows.append({'year': y, 'age_group': ag, f'exp_real{BASE}_per_CU': round(tot * defl.loc[y]),
                     'cu_size': sz, f'exp_real{BASE}_per_person': round(tot * defl.loc[y] / sz),
                     'index_per_CU_55_64_eq_100': round(100 * tot / s('TOTALEXP', '55-64').loc[y], 1)})
pd.DataFrame(rows).to_csv(OUT / 't7_age_profile_selected_years.csv', index=False)
print('done')
