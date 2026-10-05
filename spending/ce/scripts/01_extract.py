"""Extract BLS Consumer Expenditure Survey (CE) published means by age of reference person.

Source: BLS LABSTAT time-series database, survey 'cx'
  https://download.bls.gov/pub/time.series/cx/  (cx.series, cx.data.1.AllData)
Series id pattern: CXU{item}{demographics}{characteristics}M, e.g. CXUTOTALEXPLB0407M
  demographics LB04 = age of reference person; characteristics 01 all CUs, 06 55-64,
  07 65+, 08 65-74, 09 75+.
CPI-U all items, U.S. city average, annual average (series CUUR0000SA0, period M13):
  https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems
Raw files are expected in /tmp/ce_raw (download with curl -A 'research <email>').
Writes output/ce_age_long.csv, output/ce_series_list.csv and output/cpi_u_annual.csv.
"""
import pandas as pd, pathlib

RAW = pathlib.Path('/tmp/ce_raw')
OUT = pathlib.Path(__file__).resolve().parents[1] / 'output'

ITEMS = ['TOTALEXP', 'FOODTOTL', 'FOODHOME', 'FOODAWAY', 'HOUSING', 'SHELTER', 'OWNDWELL',
         'RNTDWELL', 'UTILS', 'HHOPER', 'HHFURNSH', 'TRANS', 'VEHPURCH', 'GASOIL', 'GASFUEL',
         'HEALTH', 'HLTHINSR', 'MEDSERVS', 'DRUGS', 'MEDSUPPL', '580901', '580907',
         'ENTRTAIN', 'CASHCONT', 'INSPENSN', 'PENSIONS', 'LIFEINSR', 'APPAREL', 'EDUCATN',
         'PERSCARE', 'READING', 'TOBACCO', 'ALCBEVG', 'MISC',
         'INCBEFTX', 'INCAFTTX', 'PERSTAX', '900000', 'SFEMPINC', 'RETIRINC', 'INDIVRNT',
         'OTHRINC', 'WELFARE', 'OTHREGIN', 'OTHBNFTS', 'REGCONT', '900030', '900040',
         '900050', '900080', '900170', '900180', '900190', '900200',
         '980010', '980020', '980030', '980060', 'CONSUNIT', 'HOMEOWN', '980230', '980240',
         '980260']
AGES = {'01': 'All CUs', '02': 'Under 25', '03': '25-34', '04': '35-44', '05': '45-54',
        '06': '55-64', '07': '65+', '08': '65-74', '09': '75+'}

ser = pd.read_csv(RAW / 'cx.series', sep='\t', dtype=str)
ser.columns = [c.strip() for c in ser.columns]
ser = ser.apply(lambda s: s.str.strip())
ser = ser[(ser.demographics_code == 'LB04') & ser.item_code.isin(ITEMS)
          & ser.characteristics_code.isin(AGES)]
keep = set(ser.series_id)

dat = pd.read_csv(RAW / 'cx.data.1.AllData', sep='\t', dtype=str)
dat.columns = [c.strip() for c in dat.columns]
dat = dat.apply(lambda s: s.str.strip())
dat = dat[dat.series_id.isin(keep)]
dat = dat.merge(ser[['series_id', 'item_code', 'characteristics_code', 'series_title']], on='series_id')
dat['age_group'] = dat.characteristics_code.map(AGES)
dat['value'] = pd.to_numeric(dat.value, errors='coerce')
dat['year'] = dat.year.astype(int)
ser[['series_id', 'item_code', 'characteristics_code', 'series_title', 'begin_year', 'end_year']].sort_values('series_id').to_csv(OUT / 'ce_series_list.csv', index=False)
dat = dat[['series_id', 'item_code', 'age_group', 'year', 'value', 'footnote_codes']]
dat.sort_values(['item_code', 'age_group', 'year']).to_csv(OUT / 'ce_age_long.csv', index=False)
print(len(dat), 'rows; years', dat.year.min(), dat.year.max())

cpi = pd.read_csv(RAW / 'cu.data.1.AllItems', sep='\t', dtype=str)
cpi.columns = [c.strip() for c in cpi.columns]
cpi = cpi.apply(lambda s: s.str.strip())
cpi = cpi[(cpi.series_id == 'CUUR0000SA0') & (cpi.period == 'M13')]
cpi = cpi.assign(year=cpi.year.astype(int), cpi_u=pd.to_numeric(cpi.value))[['year', 'cpi_u']]
cpi[cpi.year >= 1984].to_csv(OUT / 'cpi_u_annual.csv', index=False)
