"""Extract persons 50+ from Census CPS ASEC public-use files (www2.census.gov) and harmonize
retirement-income variables across the 2014 questionnaire redesign and 2019 processing change.

Usage: python extract.py RAW_DIR   (downloads missing files into RAW_DIR; needs pandas, pyarrow)
Output: ../data/asec_persons_50plus.parquet

Sources (ASEC year t = income year t-1):
  2010-2018 production files: fixed-width asecYYYY_pubuse.dat.gz; person-record positions are identical
    in every dictionary 2011-2018 (A_AGE 19/2, A_SEX 24/1, MARSUPWT 155/8 w/ 2 implied decimals,
    SS_YN 423/1, SS_VAL 424/5, RET_YN 506/1, RET_SC1 507/1, RET_SC2 508/1, RET_VAL1 509/5, RET_VAL2 514/5).
    2010 uses a different layout (techdocs/cpsmar10.pdf): A_AGE 15/2, A_SEX 20/1, MARSUPWT 66/8,
    SS_YN 290/1, SS_VAL 291/5, RET_YN 366/1, RET_SC1 367/1, RET_SC2 368/1, RET_VAL1 369/5, RET_VAL2 374/5.
  Match keys PH_SEQ 2/5 and PPPOS 7/2 in every legacy layout (2010 included); kept as ph_seq, pppos so the
    replicate-weight files (keyed H_SEQ + PPPOS) can be merged (see se.py).
  2014: two files: 3/8 sample with the redesigned income questions, 5/8 with the traditional ones.
  2017 research file and 2018 bridge file: same samples re-processed with the updated (2019+) system.
  2019-2026 production files: asecpubYYcsv.zip (pppubYY.csv).
"""
import gzip, io, sys, zipfile, urllib.request
from pathlib import Path
import numpy as np, pandas as pd

RAW = Path(sys.argv[1] if len(sys.argv) > 1 else "raw")
OUT = Path(__file__).resolve().parent.parent / "data" / "asec_persons_50plus.parquet"
B = "https://www2.census.gov/programs-surveys/cps/datasets"
X = "https://www2.census.gov/programs-surveys/demo/datasets/income-poverty/time-series/data-extracts"

LEGACY = {  # (asec_year, file_label): filename
    (2010, "production"): f"{B}/2010/march/asec2010_pubuse.dat.gz",
    (2011, "production"): f"{B}/2011/march/asec2011_pubuse.dat.gz",
    (2012, "production"): f"{B}/2012/march/asec2012_pubuse.dat.gz",
    (2013, "production"): f"{B}/2013/march/asec2013_pubuse.dat.gz",
    (2014, "traditional_5x8"): f"{B}/2014/march/asec2014_pubuse_tax_fix_5x8_2017.dat.gz",
    (2014, "redesign_3x8"): f"{B}/2014/march/asec2014_pubuse_3x8_rerun_v2.dat.gz",
    (2015, "production"): f"{B}/2015/march/asec2015_pubuse.dat.gz",
    (2016, "production"): f"{B}/2016/march/asec2016_pubuse_v3.dat.gz",
    (2017, "production"): f"{B}/2017/march/asec2017_pubuse.dat.gz",
    (2018, "production"): f"{B}/2018/march/asec2018_pubuse.dat.gz",
}
NEW = {
    (2017, "research_updated"): f"{X}/2017/cps-asec-research-file/pppub17.csv",
    (2018, "bridge_updated"): f"{X}/2018/cps-asec-bridge-file/pppub18.csv",
    **{(2000 + y, "production"): f"{B}/{2000+y}/march/asecpub{y}csv.zip" for y in range(19, 27)},
}
POS = dict(ph_seq=(2, 5), pppos=(7, 2), age=(19, 2), sex=(24, 1), wt=(155, 8), ss_yn=(423, 1), ss_val=(424, 5),
           ret_yn=(506, 1), ret_sc1=(507, 1), ret_sc2=(508, 1), ret_val1=(509, 5), ret_val2=(514, 5))
POS2010 = dict(ph_seq=(2, 5), pppos=(7, 2), age=(15, 2), sex=(20, 1), wt=(66, 8), ss_yn=(290, 1), ss_val=(291, 5),
               ret_yn=(366, 1), ret_sc1=(367, 1), ret_sc2=(368, 1), ret_val1=(369, 5), ret_val2=(374, 5))

def fetch(url):
    p = RAW / (url.rsplit("/", 1)[1] if "data-extracts" not in url else url.split("/")[-3] + "_" + url.rsplit("/", 1)[1])
    if not p.exists():
        RAW.mkdir(parents=True, exist_ok=True); urllib.request.urlretrieve(url, p)
    return p

def read_legacy(path, pos=POS):
    rows = []; a0 = pos["age"][0] - 1
    with gzip.open(path, "rt", encoding="latin-1") as f:
        for line in f:
            if line[0] != "3": continue  # person records
            if int(line[a0:a0+2]) < 50: continue
            rows.append([int(line[s-1:s-1+n]) for s, n in pos.values()])
    d = pd.DataFrame(rows, columns=list(pos)); d["wt"] = d.wt / 100
    return d

def read_new(path):
    cols = ["PH_SEQ","PPPOS","A_AGE","A_SEX","MARSUPWT","SS_YN","SS_VAL","PEN_YN","PEN_SC1","PEN_SC2","PEN_VAL1","PEN_VAL2",
            "ANN_YN","ANN_VAL","DST_YN","DST_SC1","DST_SC2","DST_VAL1","DST_VAL2",
            "DST_YN_YNG","DST_SC1_YNG","DST_SC2_YNG","DST_VAL1_YNG","DST_VAL2_YNG","PNSN_VAL","RETCB_YN"]
    if path.suffix == ".zip":
        z = zipfile.ZipFile(path); name = next(n for n in z.namelist() if "pppub" in n)
        fh = z.open(name)
    else:
        fh = open(path, "rb")
    d = pd.read_csv(fh, usecols=cols)
    d.columns = d.columns.str.lower()
    d = d.rename(columns={"a_age": "age", "a_sex": "sex", "marsupwt": "wt"})
    d = d[d.age >= 50].copy()
    if d.wt.max() > 1e5: d["wt"] = d.wt / 100   # some CSVs keep 2 implied decimals
    return d

def harmonize_legacy(d):
    has = lambda c: (d.ret_sc1 == c) | (d.ret_sc2 == c)
    val = lambda m: np.where(d.ret_sc1.isin(m), d.ret_val1, 0) + np.where(d.ret_sc2.isin(m), d.ret_val2, 0)
    d["any_ret"] = d.ret_yn == 1
    d["acct_wd"] = has(7)                                   # regular payments from IRA/Keogh/401(k)
    d["db_pension"] = d.ret_sc1.between(1, 5) | d.ret_sc2.between(1, 5)
    d["annuity"] = has(6)
    d["acct_wd_val"] = val([7]); d["ret_val"] = d.ret_val1 + d.ret_val2
    return d

def harmonize_new(d):
    d["dst_any"] = (d.dst_yn == 1) | (d.dst_yn_yng == 1)
    d["acct_wd"] = d.dst_any
    d["db_pension"] = d.pen_yn == 1
    d["annuity"] = d.ann_yn == 1
    d["any_ret"] = d.acct_wd | d.db_pension | d.annuity
    d["acct_wd_val"] = d.dst_val1 + d.dst_val2 + d.dst_val1_yng + d.dst_val2_yng
    d["ret_val"] = d.pen_val1 + d.pen_val2 + d.ann_val + d.acct_wd_val
    return d

def main():
    parts = []
    for (yr, lab), url in LEGACY.items():
        d = harmonize_legacy(read_legacy(fetch(url), POS2010 if yr == 2010 else POS)); d["system"] = "legacy"
        d["asec_year"], d["file"] = yr, lab; parts.append(d); print(yr, lab, len(d), round(d.wt.sum()/1e6, 1))
    for (yr, lab), url in NEW.items():
        d = harmonize_new(read_new(fetch(url))); d["system"] = "updated"
        d["asec_year"], d["file"] = yr, lab; parts.append(d); print(yr, lab, len(d), round(d.wt.sum()/1e6, 1))
    a = pd.concat(parts, ignore_index=True)
    a["income_year"] = a.asec_year - 1
    a["ss_recip"] = a.ss_yn == 1
    for c in a.columns:
        if a[c].dtype == "float64" and c != "wt" and a[c].notna().all() and (a[c] % 1 == 0).all(): a[c] = a[c].astype("int64")
    OUT.parent.mkdir(parents=True, exist_ok=True); a.to_parquet(OUT, index=False); print("wrote", OUT, len(a))

if __name__ == "__main__":
    main()
