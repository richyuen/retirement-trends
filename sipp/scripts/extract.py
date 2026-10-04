"""Download SIPP 2018-2025 public-use files from Census and extract the retirement-account variables.

Usage: python3 sipp/scripts/extract.py [RAW_DIR] [YEARS...]
  RAW_DIR defaults to /tmp/sipp/raw (kept OUT of the shared folder; zips are deleted after extraction).

Writes
  sipp/data/sipp_persons_dec.parquet   one row per person (December reference-month record), all ages,
                                       needed columns only + annual sum of the monthly retirement-income recode.
  RAW_DIR/../reps/rwYYYY_dec.parquet   December calendar-year replicate weights (REPWGT1-240, float32),
                                       persons 15+ only; ~70-100 MB per year, so kept outside the shared folder.
Source: https://www2.census.gov/programs-surveys/sipp/data/datasets/YYYY/pu YYYY_csv.zip and rwYYYY_csv.zip
SIPP file year t covers calendar (reference) year t-1.
"""
import io, json, os, subprocess, sys, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, '..', 'data')
RAW = sys.argv[1] if len(sys.argv) > 1 else '/tmp/sipp/raw'
YEARS = [int(y) for y in sys.argv[2:]] or list(range(2018, 2026))
REPS = os.path.join(os.path.dirname(os.path.abspath(RAW)), 'reps')
BASE = 'https://www2.census.gov/programs-surveys/sipp/data/datasets/{y}/{f}'
os.makedirs(RAW, exist_ok=True); os.makedirs(REPS, exist_ok=True); os.makedirs(OUTDIR, exist_ok=True)

WANT = [
    # ids / design / demographics
    'SSUID', 'PNUM', 'SPANEL', 'SWAVE', 'MONTHCODE', 'ERESIDENCEID', 'ERELRPE', 'RFAMREF', 'EPNSPOUSE',
    'RIN_UNIV', 'WPFINWGT', 'TAGE', 'TAGE_EHC', 'ESEX', 'EMS', 'RMESR', 'EEVERET',
    # account ownership and end-of-year balances (person level, owner-reported)
    'EOWN_IRAKEO', 'AOWN_IRAKEO', 'EOWN_THR401', 'AOWN_THR401', 'EOWN_PENSION',
    'TIRAKEOVAL', 'AIRAKEOVAL', 'TTHR401VAL', 'ATHR401VAL', 'TVAL_RET', 'THVAL_RET',
    # account-specific withdrawals (SIPP 2021+ = ref year 2020+)
    'EIRA_INC_YN', 'AIRA_INC_YN', 'TIRA_INC_AMT', 'AIRA_INC_AMT',
    'ETHR_INC_YN', 'ATHR_INC_YN', 'TTHR_INC_AMT', 'ATHR_INC_AMT',
    'EMJOB_401', 'EPJOB_401', 'EMJOB_IRA', 'EPJOB_IRA',
    # pre-2021 combined distribution item (SIPP 2018-2020 = ref 2017-2019)
    'ERET_LUMPSUM', 'ARET_LUMPSUM', 'TDRAW_AMT', 'ADRAW_AMT',
    # lump sums and rollovers (programs section)
    'ELMPNOW', 'ELMPTYP1YN', 'TLMPAMT', 'EROLLOVR1', 'EROLLOVR2', 'TROLLAMT', 'EPENLUMP', 'TPENLUMPAMT',
    # other retirement income
    'ERETANY', 'ERETTYP1YN', 'ERETTYP8YN',
    # topcoding: median of the topcoded values (constant on the file; topcoded cases carry the group mean)
    'TIRA_INC_MED', 'TTHR_INC_MED', 'TIRAKEO_MED', 'TTH401_MED', 'TDRAWAMT_MED',
]
MONTHLY_SUM = ['TRETINCAMT']  # monthly recode, summed over the year


def fetch(year, fname):
    path = os.path.join(RAW, fname)
    if not os.path.exists(path):
        print('download', fname, flush=True)
        subprocess.run(['curl', '-sS', '-f', '--retry', '5', '-o', path + '.part', BASE.format(y=year, f=fname)], check=True)
        os.rename(path + '.part', path)
    return path


def schema(year, kind):
    p = os.path.join(RAW, f'{kind}{year}_schema.json')
    if not os.path.exists(p):
        subprocess.run(['curl', '-sS', '-f', '-o', p, BASE.format(y=year, f=f'{kind}{year}_schema.json')], check=True)
    return json.load(open(p))


def open_member(zpath):
    z = zipfile.ZipFile(zpath)
    name = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
    return z.open(name)


def extract_pu(year):
    sch = schema(year, 'pu')
    names = [v['name'] for v in sch]
    dtypes = {v['name']: ('object' if v['dtype'] == 'string' else 'float64') for v in sch}
    cols = [c for c in WANT + MONTHLY_SUM if c in names]
    zpath = fetch(year, f'pu{year}_csv.zip')
    parts, msum = [], []
    with open_member(zpath) as fh:
        want = set(cols)
        for ch in pd.read_csv(fh, sep='|', usecols=lambda c: c.upper() in want, dtype=str, chunksize=200_000):
            ch.columns = [c.upper() for c in ch.columns]
            ch = ch.astype({c: dtypes[c] for c in ch.columns})
            if 'TRETINCAMT' in ch:
                msum.append(ch.groupby(['SSUID', 'PNUM'])['TRETINCAMT'].agg(['sum', 'count']).reset_index())
            parts.append(ch[ch.MONTHCODE == 12].drop(columns=[c for c in MONTHLY_SUM if c in ch]))
    df = pd.concat(parts, ignore_index=True)
    if msum:
        m = pd.concat(msum).groupby(['SSUID', 'PNUM']).sum().reset_index()
        m.columns = ['SSUID', 'PNUM', 'TRETINCAMT_YR', 'n_months']
        df = df.merge(m, on=['SSUID', 'PNUM'], how='left')
    for c in WANT:
        if c not in df:
            df[c] = np.nan
    df['sipp_year'] = year
    df['ref_year'] = year - 1
    print(year, 'pu rows (Dec persons):', len(df), flush=True)
    return df


def extract_rw(year, keep):
    out = os.path.join(REPS, f'rw{year}_dec.parquet')
    if os.path.exists(out):
        return
    zpath = fetch(year, f'rw{year}_csv.zip')
    sch = schema(year, 'rw')
    names = [v['name'] for v in sch]
    reps = [f'REPWGT{i}' for i in range(1, 241)]
    cols = ['SSUID', 'PNUM', 'MONTHCODE', 'REPWGT0'] + reps
    dt = {c: ('object' if c == 'SSUID' else 'float32') for c in cols}
    dt['PNUM'] = 'float64'; dt['MONTHCODE'] = 'float64'
    parts = []
    with open_member(zpath) as fh:
        want = set(cols)
        for ch in pd.read_csv(fh, sep='|', usecols=lambda c: c.upper() in want, dtype=str, chunksize=100_000):
            ch.columns = [c.upper() for c in ch.columns]
            ch = ch.astype({c: dt[c] for c in ch.columns})
            ch = ch[ch.MONTHCODE == 12]
            ch = ch.merge(keep, on=['SSUID', 'PNUM'], how='inner')
            parts.append(ch)
    rw = pd.concat(parts, ignore_index=True).drop(columns=['MONTHCODE'])
    rw.to_parquet(out, index=False)
    print(year, 'rw rows:', len(rw), flush=True)
    os.remove(zpath)


if __name__ == '__main__':
    allp = []
    for y in YEARS:
        df = extract_pu(y)
        keep = df.loc[df.TAGE_EHC >= 15, ['SSUID', 'PNUM']].drop_duplicates()
        extract_rw(y, keep)
        allp.append(df)
        zp = os.path.join(RAW, f'pu{y}_csv.zip')
        if os.path.exists(zp):
            os.remove(zp)
    out = os.path.join(OUTDIR, 'sipp_persons_dec.parquet')
    new = pd.concat(allp, ignore_index=True)
    if os.path.exists(out) and set(YEARS) != set(range(2018, 2026)):
        old = pd.read_parquet(out)
        new = pd.concat([old[~old.sipp_year.isin(YEARS)], new], ignore_index=True)
    new.to_parquet(out, index=False, compression='zstd')
    print('wrote', out, len(new))
