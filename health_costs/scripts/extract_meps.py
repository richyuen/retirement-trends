"""Extract a slim person-level file from each MEPS-HC Full Year Consolidated (FYC) file, 1996-2024.

Input : zips downloaded by fetch_meps.sh into $MEPS_CACHE (default ./meps_cache)
Output: raw/meps_slim/meps_fyc_<year>.csv.gz  (all persons, standardized column names)
Columns: year, dupersid, duid, famid (CPSFAMID), age, wt, oop (TOTSLF), totexp (TOTEXP),
         mcr_paid (TOTMCR), rx_oop (RXSLF), pinc (TTLP person total income), faminc (FAMINC, CPS family income; missing 1996),
         mcrev (ever Medicare in year; 1=yes), varstr, varpsu (within-year design vars)
"""
import os, re, sys, zipfile, tempfile, shutil
import pandas as pd, pyreadstat

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'raw', 'meps_slim')
CACHE = os.environ.get('MEPS_CACHE', './meps_cache')
FILES = {1996: 12, 1997: 20, 1998: 28, 1999: 38, 2000: 50, 2001: 60, 2002: 70, 2003: 79, 2004: 89, 2005: 97,
         2006: 105, 2007: 113, 2008: 121, 2009: 129, 2010: 138, 2011: 147, 2012: 155, 2013: 163, 2014: 171,
         2015: 181, 2016: 192, 2017: 201, 2018: 209, 2019: 216, 2020: 224, 2021: 233, 2022: 243, 2023: 251, 2024: 256}

def pick(cols, *cands):
    s = {c.upper(): c for c in cols}
    for c in cands:
        if c.upper() in s:
            return s[c.upper()]
    return None

def one(year, num):
    yy = f'{year % 100:02d}'
    out = os.path.join(OUT, f'meps_fyc_{year}.csv.gz')
    if os.path.exists(out):
        return pd.read_csv(out, nrows=1).shape
    stata = num >= 201
    zp = os.path.join(CACHE, f'h{num}{"dta" if stata else "ssp"}.zip')
    tmp = tempfile.mkdtemp(dir=os.environ.get('TMPDIR', '/tmp'))
    try:
        with zipfile.ZipFile(zp) as z:
            name = z.namelist()[0]; z.extract(name, tmp)
        path = os.path.join(tmp, name)
        if stata:
            reader = pyreadstat.read_dta
        else:
            reader = lambda f, **k: pyreadstat.read_xport(f, encoding='latin1', **k)
        _, meta = reader(path, metadataonly=True)
        cols = meta.column_names
        m = {
            'dupersid': pick(cols, 'DUPERSID'), 'duid': pick(cols, 'DUID'), 'famid': pick(cols, 'CPSFAMID'),
            'age': pick(cols, f'AGE{yy}X'), 'agelast': pick(cols, 'AGELAST'),
            'wt': pick(cols, f'PERWT{yy}F', f'WTDPER{yy}'),
            'oop': pick(cols, f'TOTSLF{yy}'), 'totexp': pick(cols, f'TOTEXP{yy}'), 'mcr_paid': pick(cols, f'TOTMCR{yy}'),
            'rx_oop': pick(cols, f'RXSLF{yy}'),
            'pinc': pick(cols, f'TTLP{yy}X', 'TTLPNX'), 'faminc': pick(cols, f'FAMINC{yy}'),
            'mcrev': pick(cols, f'MCREV{yy}', 'MCREVER'),
            'varstr': pick(cols, 'VARSTR', f'VARSTR{yy}'), 'varpsu': pick(cols, 'VARPSU', f'VARPSU{yy}'),
        }
        use = [v for v in m.values() if v]
        df, _ = reader(path, usecols=use)
        df = df.rename(columns={v: k for k, v in m.items() if v})
        if 'age' in df and 'agelast' in df:
            df['age'] = df['age'].where(df['age'] >= 0, df['agelast'])
        elif 'agelast' in df:
            df['age'] = df['agelast']
        df = df.drop(columns=[c for c in ['agelast'] if c in df])
        df.insert(0, 'year', year)
        os.makedirs(OUT, exist_ok=True)
        df.to_csv(out, index=False, compression='gzip')
        missing = [k for k, v in m.items() if v is None]
        print(year, f'h{num}', df.shape, 'missing:', missing)
        return df.shape
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == '__main__':
    yrs = [int(a) for a in sys.argv[1:]] or sorted(FILES)
    for y in yrs:
        one(y, FILES[y])
