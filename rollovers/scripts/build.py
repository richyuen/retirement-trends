"""Rollover trend tables. Run from retirement-withdrawals/: python rollovers/scripts/build.py
Inputs (all already in the project): irs/output/irs_soi_ira_2004_2023_current.json (IRS SOI Tables 1 and 4,
June 2026 vintage), contributions/admin/raw/bea/NipaDataA.txt (BEA Table 7.25, all-sector DC plans),
Form 5500 private DC benefits (notes/rollovers.md table L, DOL Abstract Table A1), ICI 1996-2002 traditional
rollovers (notes/rollovers.md table A), Vanguard HAS 2025/2026 figures (typed in below from the PDFs)."""
import csv, json, os
B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(B, 'rollovers', 'output')

irs = json.load(open(os.path.join(B, 'irs/output/irs_soi_ira_2004_2023_current.json')))
bea = {}
for r in csv.reader(open(os.path.join(B, 'contributions/admin/raw/bea/NipaDataA.txt'))):
    if r[0] == 'Y353RC':
        bea[int(r[1])] = float(r[2].replace(',', '')) / 1000  # $bn
f5500 = {2000: 213531, 2001: 182210, 2002: 178740, 2003: 167048, 2004: 192888, 2005: 217985, 2006: 260340,
         2007: 294105, 2008: 265095, 2009: 241351, 2010: 287282, 2011: 299335, 2012: 333843, 2013: 385872,
         2014: 428359, 2015: 450554, 2016: 454947, 2017: 493986, 2018: 550691, 2019: 599081, 2020: 703607,
         2021: 776879, 2022: 715955, 2023: 783697}  # $m, private DC benefits disbursed (incl. direct rollovers)
ici_trad = {1996: 114.0, 1997: 121.5, 1998: 160.0, 1999: 199.9, 2000: 225.6, 2001: 187.8, 2002: 204.4}

rows = []
for y in range(1996, 2024):
    trad = allt = s60 = None
    if str(y) in irs['t1']:
        t1 = irs['t1'][str(y)]
        trad = t1['trad']['ra'] / 1e6
        allt = (t1['total']['ra'] if 'total' in t1 else irs['age'][str(y)]['all']['ra']) / 1e6
    elif y in ici_trad:
        trad = ici_trad[y]
    if str(y) in irs['age']:
        a = irs['age'][str(y)]
        s60 = (a['all']['ra'] - a['u60']['ra']) / a['all']['ra'] * 100
    if trad is None:
        continue
    b = bea.get(y); f = f5500.get(y)
    rows.append(dict(year=y, trad_ira_rollovers_bn=round(trad, 1),
                     all_ira_rollovers_bn=round(allt, 1) if allt else '',
                     bea_dc_outflows_bn=round(b, 1) if b else '',
                     form5500_private_dc_benefits_bn=round(f / 1000, 1) if f else '',
                     trad_pct_of_bea=round(100 * trad / b, 1) if b else '',
                     trad_pct_of_form5500=round(100 * trad / (f / 1000), 1) if f else '',
                     age60plus_share_of_rollover_dollars=round(s60, 1) if s60 else '',
                     irs_series=('ICI tabulation of IRS SOI' if y < 2004 else
                                 'IRS SOI old method' if y < 2022 else 'IRS SOI new method (break)')))
with open(os.path.join(OUT, 'ira_rollovers_vs_dc_outflows.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# IRS rollovers by age: incidence per 100 IRA holders and dollars as % of the age group's IRA assets
age_rows = []
for y in sorted(irs['age']):
    a = irs['age'][y]
    for g in ['u60', '60-64', '65-69', '70-74', '75-79', '80+', 'all']:
        d = a[g]
        age_rows.append(dict(year=int(y), age=g, rollover_taxpayers=d['rn'], rollover_k=d['ra'],
                             share_of_rollover_dollars=round(100 * d['ra'] / a['all']['ra'], 1),
                             per100_ira_holders=round(100 * d['rn'] / d['hn'], 1),
                             pct_of_yearend_ira_assets=round(100 * d['ra'] / d['fa'], 2)))
with open(os.path.join(OUT, 'irs_rollovers_by_age.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(age_rows[0])); w.writeheader(); w.writerows(age_rows)

# Vanguard How America Saves: participants with termination dates in the year (status at year end)
yrs = list(range(2015, 2026))
has = {  # HAS 2025 Fig 116 (2015-2024) and HAS 2026 Fig 116 (2016-2025); identical where they overlap
 'people_remain':   [51, 50, 51, 48, 46, 49, 52, 51, 48, 49, 46],
 'people_rollover': [20, 19, 18, 18, 18, 19, 18, 16, 18, 21, 25],
 'people_cash':     [28, 30, 30, 33, 34, 31, 29, 32, 33, 29, 28],
 'assets_remain':   [56, 59, 61, 56, 60, 63, 61, 61, 61, 59, 58],
 'assets_rollover': [37, 35, 34, 37, 34, 32, 34, 33, 33, 35, 36],
 'assets_cash':     [5, 5, 4, 6, 5, 4, 4, 5, 5, 5, 5]}
with open(os.path.join(OUT, 'vanguard_has_terminators.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['termination_year'] + list(has))
    for i, y in enumerate(yrs):
        w.writerow([y] + [has[k][i] for k in has])
with open(os.path.join(OUT, 'vanguard_has_by_age_60s_70s.csv'), 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['termination_year', 'age', 'people_remain', 'people_rollover', 'people_cash', 'people_installments',
                'assets_remain', 'assets_rollover', 'assets_cash', 'source'])
    w.writerow([2024, '60s', 42, 34, 22, 1, 51, 46, 2, 'HAS 2025 Fig 117'])
    w.writerow([2024, '70s', 29, 32, 26, 12, 40, 55, 4, 'HAS 2025 Fig 117'])
    w.writerow([2024, 'all', 49, 21, 29, 0, 59, 35, 5, 'HAS 2025 Fig 117'])
    w.writerow([2025, '60s', 40, 36, 22, 1, 49, 48, 2, 'HAS 2026 Fig 117'])
    w.writerow([2025, '70s', 27, 35, 27, 10, 40, 55, 4, 'HAS 2026 Fig 117'])
    w.writerow([2025, 'all', 46, 25, 28, 0, 58, 36, 5, 'HAS 2026 Fig 117'])
print('\n'.join(f"{r['year']} trad {r['trad_ira_rollovers_bn']} all {r['all_ira_rollovers_bn']} BEA {r['bea_dc_outflows_bn']} "
                f"%BEA {r['trad_pct_of_bea']} %5500 {r['trad_pct_of_form5500']} 60+ {r['age60plus_share_of_rollover_dollars']}" for r in rows))
