"""Income sources of older Americans from CPS ASEC public-use files downloaded from www2.census.gov (no IPUMS).

Usage: python extract.py RAW_DIR      (downloads any missing file into RAW_DIR; needs pandas + pyarrow)
Output: ../data/asec_aged_income_persons.parquet
        every person aged 65+ plus every spouse (any age) of a person aged 65+, with harmonized income components
        (annual dollars, nominal, income year = ASEC year - 1), weights and the keys needed to build SSA-style aged
        units and to merge Census replicate weights (ph_seq, pppos).

Files (same URLs and file choices as ../../../cps/scripts/extract.py, extended back to ASEC 1998, the earliest March
supplement Census still posts under programs-surveys/cps/datasets/):
  legacy processing, fixed width: ASEC 1998-2018 (2014 = two files: 5/8 traditional questions, 3/8 redesigned)
  updated processing, CSV:       ASEC 2017 research file, 2018 bridge file, ASEC 2019-2026 production
Fixed-width positions were read from Census's own dictionaries (techdocs/cpsmarYY.pdf, "D NAME width position"
lines; 2014 also asec2014R_pubuse.dd.txt). They fall in two layouts, identical within each span for every
variable used here: LAYOUT_A for ASEC 1998-2010 and LAYOUT_B for ASEC 2011-2018 (both 2014 files).

Harmonized components (all person-level, nominal $):
  earn      PEARNVAL (wages + nonfarm self-employment + farm; can be negative)
  ss        SS_VAL (Social Security, all types)
  pen_db    defined-benefit pensions = own retirement pensions (legacy RET_SC 1-5 and 8 "other/DK"; updated PEN_VAL1+2,
            sources company, union, federal/state/local govt, military, railroad, other) + survivor pensions
            (SUR_SC 1-5) + disability pensions from an employer/government (DIS_SC 2-6)
  annuity   legacy RET_SC 6 (annuities/paid-up insurance) ; updated ANN_VAL ; both + SUR_SC 9 (annuity survivor pay)
  acct      retirement-account withdrawals: legacy RET_SC 7 (regular payments from IRA/Keogh/401(k));
            updated DST_VAL1+2 (age 58+, all account types; DST_*_YNG for under-58s is not in Census money income)
  int_nonret interest outside retirement accounts (legacy INT_VAL; updated TRDINT_VAL)
  int_ret   interest reported as earned inside retirement accounts (updated RINT_VAL1+2; Census's INT_VAL and PTOTVAL
            include it; not separately identified in legacy files, where the 2014+ redesigned interest question
            may also capture some of it)
  div, rent DIV_VAL, RNT_VAL
  ssi, pa   SSI_VAL, PAW_VAL (public assistance / welfare)
  vet       VET_VAL
  other     PTOTVAL minus everything above (UC, workers' comp, educational assistance, child support, alimony,
            financial assistance, other income, other survivor/disability sources incl. workers' comp, estates/trusts)
  total     PTOTVAL (Census total money income)
"""
import gzip, io, sys, zipfile, urllib.request
from pathlib import Path
import numpy as np, pandas as pd

RAW = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/cps_raw/dl")
OUT = Path(__file__).resolve().parent.parent / "data" / "asec_aged_income_persons.parquet"
B = "https://www2.census.gov/programs-surveys/cps/datasets"
X = "https://www2.census.gov/programs-surveys/demo/datasets/income-poverty/time-series/data-extracts"

LEGACY = {
    (1998, "production"): f"{B}/1998/march/mar98supp.cps.gz",
    (1999, "production"): f"{B}/1999/march/mar99supp.cps.gz",
    (2000, "production"): f"{B}/2000/march/mar00supp.cps.gz",
    (2001, "production"): f"{B}/2001/march/mar01supp.dat.gz",
    (2002, "production"): f"{B}/2002/march/mar02supp.dat.gz",
    (2003, "production"): f"{B}/2003/march/asec2003.pub.gz",
    (2004, "production"): f"{B}/2004/march/asec2004.pub.gz",
    (2005, "production"): f"{B}/2005/march/asec2005_pubuse.pub.gz",
    (2006, "production"): f"{B}/2006/march/asec2006_pubuse.pub.gz",
    (2007, "production"): f"{B}/2007/march/asec2007_pubuse_tax2.dat.gz",
    (2008, "production"): f"{B}/2008/march/asec2008_pubuse.dat.gz",
    (2009, "production"): f"{B}/2009/march/asec2009_pubuse.dat.gz",
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
# (position, width) from cpsmar98 ... cpsmar10 (identical in all 13 dictionaries)
LAYOUT_A = dict(ph_seq=(2, 5), pppos=(7, 2), a_lineno=(9, 2), age=(15, 2), sex=(20, 1), a_maritl=(17, 1),
    a_spouse=(18, 2), wt=(66, 8), wkswork=(171, 2), pearnval=(448, 8), ss_val=(291, 5), ssi_val=(819, 5),
    paw_val=(305, 5), vet_val=(317, 5), sur_sc1=(323, 2), sur_sc2=(325, 2), sur_val1=(327, 5), sur_val2=(332, 5),
    dis_sc1=(346, 2), dis_sc2=(348, 2), dis_val1=(350, 5), dis_val2=(355, 5), ret_sc1=(367, 1), ret_sc2=(368, 1),
    ret_val1=(369, 5), ret_val2=(374, 5), int_val=(386, 5), div_val=(393, 5), rnt_val=(399, 5), ptotval=(440, 8))
# cpsmar11 ... cpsmar18 and asec2014R_pubuse.dd.txt (identical)
LAYOUT_B = dict(ph_seq=(2, 5), pppos=(7, 2), a_lineno=(11, 2), age=(19, 2), sex=(24, 1), a_maritl=(21, 1),
    a_spouse=(22, 2), wt=(155, 8), wkswork=(258, 2), pearnval=(588, 8), ss_val=(424, 5), ssi_val=(433, 5),
    paw_val=(445, 5), vet_val=(457, 5), sur_sc1=(463, 2), sur_sc2=(465, 2), sur_val1=(467, 5), sur_val2=(472, 5),
    dis_sc1=(486, 2), dis_sc2=(488, 2), dis_val1=(490, 5), dis_val2=(495, 5), ret_sc1=(507, 1), ret_sc2=(508, 1),
    ret_val1=(509, 5), ret_val2=(514, 5), int_val=(526, 5), div_val=(533, 6), rnt_val=(540, 5), ptotval=(580, 8))
COMP = ["earn", "ss", "pen_db", "annuity", "acct", "int_nonret", "int_ret", "div", "rent", "ssi", "pa", "vet", "other"]


def fetch(url):
    name = url.rsplit("/", 1)[1]
    if "cps-asec-research-file" in url: name = "research2017_" + name
    if "cps-asec-bridge-file" in url: name = "bridge2018_" + name
    p = RAW / name
    if not p.exists():
        RAW.mkdir(parents=True, exist_ok=True); urllib.request.urlretrieve(url, p)
    return p


def read_legacy(path, pos):
    cols = list(pos); sl = [(s - 1, s - 1 + n) for s, n in pos.values()]
    rows = []
    with gzip.open(path, "rt", encoding="latin-1") as f:
        for line in f:
            if line[0] != "3": continue          # person records
            rows.append([int(line[a:b]) for a, b in sl])
    d = pd.DataFrame(rows, columns=cols); d["wt"] = d.wt / 100
    return d


def slot(d, sc, val, codes):
    """sum of the two source slots (sc1/val1, sc2/val2) whose source code is in codes"""
    return sum(np.where(d[f"{sc}{i}"].isin(codes), d[f"{val}{i}"], 0) for i in (1, 2))


def harmonize_legacy(d):
    o = pd.DataFrame({k: d[k] for k in ["ph_seq", "pppos", "a_lineno", "age", "sex", "a_maritl", "a_spouse", "wt",
                                        "wkswork"]})
    o["earn"] = d.pearnval; o["ss"] = d.ss_val
    o["pen_own"] = slot(d, "ret_sc", "ret_val", [1, 2, 3, 4, 5, 8])
    o["pen_survdis"] = slot(d, "sur_sc", "sur_val", [1, 2, 3, 4, 5]) + slot(d, "dis_sc", "dis_val", [2, 3, 4, 5, 6])
    o["pen_db"] = o.pen_own + o.pen_survdis
    o["annuity"] = slot(d, "ret_sc", "ret_val", [6]) + slot(d, "sur_sc", "sur_val", [9])
    o["acct"] = slot(d, "ret_sc", "ret_val", [7])
    o["int_nonret"] = d.int_val; o["int_ret"] = 0
    o["div"] = d.div_val; o["rent"] = d.rnt_val; o["ssi"] = d.ssi_val; o["pa"] = d.paw_val; o["vet"] = d.vet_val
    o["total"] = d.ptotval
    return o


def read_new(path):
    cols = ["PH_SEQ", "PPPOS", "A_LINENO", "A_AGE", "A_SEX", "A_MARITL", "A_SPOUSE", "MARSUPWT", "WKSWORK",
            "PEARNVAL", "SS_VAL", "SSI_VAL", "PAW_VAL", "VET_VAL", "SUR_SC1", "SUR_SC2", "SUR_VAL1", "SUR_VAL2",
            "DIS_SC1", "DIS_SC2", "DIS_VAL1", "DIS_VAL2", "PEN_VAL1", "PEN_VAL2", "ANN_VAL", "DST_VAL1", "DST_VAL2",
            "INT_VAL", "TRDINT_VAL", "RINT_VAL1", "RINT_VAL2", "DIV_VAL", "RNT_VAL", "PTOTVAL"]
    if path.suffix == ".zip":
        z = zipfile.ZipFile(path); fh = z.open(next(n for n in z.namelist() if "pppub" in n))
    else:
        fh = open(path, "rb")
    d = pd.read_csv(fh, usecols=cols); d.columns = d.columns.str.lower()
    d = d.rename(columns={"a_age": "age", "a_sex": "sex", "marsupwt": "wt"})
    if d.wt.max() > 1e5: d["wt"] = d.wt / 100
    return d


def harmonize_new(d):
    o = pd.DataFrame({k: d[k] for k in ["ph_seq", "pppos", "a_lineno", "age", "sex", "a_maritl", "a_spouse", "wt",
                                        "wkswork"]})
    o["earn"] = d.pearnval; o["ss"] = d.ss_val
    o["pen_own"] = d.pen_val1 + d.pen_val2
    o["pen_survdis"] = slot(d, "sur_sc", "sur_val", [1, 2, 3, 4, 5]) + slot(d, "dis_sc", "dis_val", [2, 3, 4, 5, 6])
    o["pen_db"] = o.pen_own + o.pen_survdis
    o["annuity"] = d.ann_val + slot(d, "sur_sc", "sur_val", [9])
    o["acct"] = d.dst_val1 + d.dst_val2
    o["int_nonret"] = d.trdint_val; o["int_ret"] = d.rint_val1 + d.rint_val2
    assert (d.int_val == o.int_nonret + o.int_ret).all()
    o["div"] = d.div_val; o["rent"] = d.rnt_val; o["ssi"] = d.ssi_val; o["pa"] = d.paw_val; o["vet"] = d.vet_val
    o["total"] = d.ptotval
    return o


def keep_aged(o):
    """persons 65+ and their spouses (A_SPOUSE = spouse's A_LINENO within the household)"""
    o = o[o.age >= 15].copy()
    old = o[o.age >= 65]
    sp = old.loc[old.a_spouse > 0, ["ph_seq", "a_spouse"]].rename(columns={"a_spouse": "a_lineno"}).drop_duplicates()
    o = o.merge(sp.assign(is_sp=True), on=["ph_seq", "a_lineno"], how="left")
    return o[(o.age >= 65) | o.is_sp.fillna(False).astype(bool)].drop(columns="is_sp")


def finish(o, yr, lab, system):
    known = o[[c for c in COMP if c != "other"]].sum(axis=1)
    o["other"] = o.total - known
    o["asec_year"], o["income_year"], o["file"], o["system"] = yr, yr - 1, lab, system
    neg = (o.other < 0) & (o.age >= 65)
    print(yr, lab, "rows", len(o), "65+ wt(M)", round(o.loc[o.age >= 65, "wt"].sum() / 1e6, 2),
          "other<0 among 65+:", int(neg.sum()), flush=True)
    return o


def main():
    parts = []
    for (yr, lab), url in LEGACY.items():
        o = harmonize_legacy(read_legacy(fetch(url), LAYOUT_A if yr <= 2010 else LAYOUT_B))
        parts.append(finish(keep_aged(o), yr, lab, "legacy"))
    for (yr, lab), url in NEW.items():
        o = harmonize_new(read_new(fetch(url)))
        parts.append(finish(keep_aged(o), yr, lab, "updated"))
    a = pd.concat(parts, ignore_index=True)
    for c in a.columns:
        if a[c].dtype == "float64" and c != "wt" and (a[c] % 1 == 0).all(): a[c] = a[c].astype("int64")
    OUT.parent.mkdir(parents=True, exist_ok=True); a.to_parquet(OUT, index=False)
    print("wrote", OUT, len(a))


if __name__ == "__main__":
    main()
