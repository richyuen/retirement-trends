"""Work among retired people, unconditional on account withdrawals: CPS ASEC 2010-2026 (Census public-use files).

Usage: python3 cps_work_after_retirement.py RAW_DIR   (missing raw files are downloaded into RAW_DIR)
2019-2026: asecpubYYcsv.zip (with replicate weights, so SEs). 2010-2018: fixed-width production files, no SEs
(2014 = traditional 5/8 file). Positions from cpsmar10/cpsmar15/cpsmar18 (2011-2018 identical): PEMLR 218,
PRWKSTAT 220/2, WORKYN 251, HRSWK 268/2, SS_YN 423, RESNSS1 429, RESNSS2 430; 2010: PEMLR 705, PRWKSTAT 707/2,
WORKYN 165, HRSWK 181/2, SS_YN 290, RESNSS1 882, RESNSS2 883. The withdrawer split is 2019+ only.
Output: ../output/cps_work_after_retirement.csv (long: year, group, measure, pct, se, n)

"Retired" = received Social Security as a retired worker in the prior year
(SS_YN=1 and RESNSS1 or RESNSS2 = 1 "retired"), aged 62+ at the March interview. No condition on
account withdrawals; the withdrawer/non-withdrawer split (DST_YN) is a separate contrast.
Current work (March reference week, basic CPS): employed = PEMLR 1-2; usually part time = PRWKSTAT 6-10,
usually full time = PRWKSTAT 2-5 (the BLS "usually full/part time" split).
Prior-year work (same year as the benefit): worked = WORKYN 1; part time = HRSWK < 35.
SEs: successive-difference replication with the 160 replicate weights in each zip, Var = 4/160 * sum (t_r - t_0)^2.
"""
import sys, zipfile, urllib.request
from pathlib import Path
import numpy as np, pandas as pd

RAW = Path(sys.argv[1] if len(sys.argv) > 1 else "raw")
OUT = Path(__file__).resolve().parent.parent / "output" / "cps_work_after_retirement.csv"
B = "https://www2.census.gov/programs-surveys/cps/datasets"
COLS = ["PH_SEQ", "PPPOS", "A_AGE", "A_SEX", "MARSUPWT", "PEMLR", "PRWKSTAT", "WORKYN", "HRSWK", "WKSWORK",
        "SS_YN", "RESNSS1", "RESNSS2", "DST_YN", "PEN_YN", "RSNNOTW"]

def load(y):
    p = RAW / f"asecpub{y % 100}csv.zip"
    if not p.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(f"{B}/{y}/march/asecpub{y % 100}csv.zip", p)
    z = zipfile.ZipFile(p)
    pp = next(n for n in z.namelist() if "pppub" in n)
    rw = next(n for n in z.namelist() if "repwgt" in n)
    d = pd.read_csv(z.open(pp), usecols=COLS)
    d = d[d.A_AGE >= 55].copy()
    r = pd.read_csv(z.open(rw))
    r.columns = r.columns.str.upper()
    r = r.rename(columns={"H_SEQ": "PH_SEQ"})
    d = d.merge(r, on=["PH_SEQ", "PPPOS"], how="left", validate="1:1")
    assert d.PWWGT0.notna().all(), "unmatched replicate weights"
    assert np.allclose(d.PWWGT0, d.MARSUPWT, atol=0.01) or np.allclose(d.PWWGT0, d.MARSUPWT / 100, atol=0.01)
    return d

LEG = {2010: "2010/march/asec2010_pubuse.dat.gz", 2011: "2011/march/asec2011_pubuse.dat.gz",
       2012: "2012/march/asec2012_pubuse.dat.gz", 2013: "2013/march/asec2013_pubuse.dat.gz",
       2014: "2014/march/asec2014_pubuse_tax_fix_5x8_2017.dat.gz", 2015: "2015/march/asec2015_pubuse.dat.gz",
       2016: "2016/march/asec2016_pubuse_v3.dat.gz", 2017: "2017/march/asec2017_pubuse.dat.gz",
       2018: "2018/march/asec2018_pubuse.dat.gz"}
POS = dict(A_AGE=(19, 2), A_SEX=(24, 1), MARSUPWT=(155, 8), PEMLR=(218, 1), PRWKSTAT=(220, 2), WORKYN=(251, 1),
           HRSWK=(268, 2), SS_YN=(423, 1), RESNSS1=(429, 1), RESNSS2=(430, 1))
POS10 = dict(A_AGE=(15, 2), A_SEX=(20, 1), MARSUPWT=(66, 8), PEMLR=(705, 1), PRWKSTAT=(707, 2), WORKYN=(165, 1),
             HRSWK=(181, 2), SS_YN=(290, 1), RESNSS1=(882, 1), RESNSS2=(883, 1))

def load_legacy(y):
    import gzip
    p = RAW / LEG[y].rsplit("/", 1)[1]
    if not p.exists():
        urllib.request.urlretrieve(f"{B}/{LEG[y]}", p)
    pos = POS10 if y == 2010 else POS; a0 = pos["A_AGE"][0] - 1; rows = []
    with gzip.open(p, "rt", encoding="latin-1") as f:
        for line in f:
            if line[0] != "3" or int(line[a0:a0 + 2]) < 55: continue
            rows.append([int(line[s - 1:s - 1 + n]) for s, n in pos.values()])
    d = pd.DataFrame(rows, columns=list(pos)); d["MARSUPWT"] = d.MARSUPWT / 100
    d["DST_YN"] = 0; d["PWWGT0"] = d.MARSUPWT
    return d

def flags(d):
    f = pd.DataFrame(index=d.index)
    f["ss_retired"] = (d.SS_YN == 1) & ((d.RESNSS1 == 1) | (d.RESNSS2 == 1))
    f["emp"] = d.PEMLR.isin([1, 2])
    f["emp_pt"] = f.emp & d.PRWKSTAT.between(6, 10)
    f["emp_ft"] = f.emp & d.PRWKSTAT.between(2, 5)
    f["worked_py"] = d.WORKYN == 1
    f["worked_py_pt"] = f.worked_py & (d.HRSWK < 35)
    f["worked_py_ft"] = f.worked_py & (d.HRSWK >= 35)
    f["nilf_retired"] = d.PEMLR == 5
    f["acct_wd"] = d.DST_YN == 1
    return f

def band(a):
    return pd.cut(a, [61, 64, 69, 74, 200], labels=["62-64", "65-69", "70-74", "75+"])

def se(t):
    return np.sqrt(4 / 160 * ((t[1:] - t[0]) ** 2).sum()) if len(t) > 1 else np.nan

def main():
    rows = []
    for y in range(2010, 2027):
        legacy = y < 2019
        d = load_legacy(y) if legacy else load(y); f = flags(d)
        W = ["PWWGT0"] if legacy else [f"PWWGT{i}" for i in range(161)]
        wt = d[W].to_numpy()
        age62 = d.A_AGE >= 62
        groups = {
            "ss_retired_62+": f.ss_retired & age62,
            "ss_retired_65+": f.ss_retired & (d.A_AGE >= 65),
            "all_65+": d.A_AGE >= 65,
            "all_62+": age62,
            "not_ss_retired_62+": ~f.ss_retired & age62,
            "ss_retired_62+_withdrawer": f.ss_retired & age62 & f.acct_wd,
            "ss_retired_62+_nonwithdrawer": f.ss_retired & age62 & ~f.acct_wd,
            "ss_retired_62+_men": f.ss_retired & age62 & (d.A_SEX == 1),
            "ss_retired_62+_women": f.ss_retired & age62 & (d.A_SEX == 2),
        }
        b = band(d.A_AGE)
        for lab in ["62-64", "65-69", "70-74", "75+"]:
            groups[f"ss_retired_{lab}"] = f.ss_retired & (b == lab)
        if legacy:
            groups = {k: v for k, v in groups.items() if "withdrawer" not in k}
        measures = {
            "pct_employed": ("emp", None), "pct_employed_pt": ("emp_pt", None), "pct_employed_ft": ("emp_ft", None),
            "pt_share_of_employed": ("emp_pt", "emp"),
            "pct_worked_prior_year": ("worked_py", None), "pct_worked_prior_year_pt": ("worked_py_pt", None),
            "pct_worked_prior_year_ft": ("worked_py_ft", None), "pt_share_of_prior_year_workers": ("worked_py_pt", "worked_py"),
        }
        for g, gm in groups.items():
            gm = gm.to_numpy()
            pop = wt[gm].sum(0)
            rows.append(dict(asec_year=y, group=g, measure="population_m", value=pop[0] / 1e6,
                             se=se(pop) / 1e6, n=int(gm.sum())))
            if g.startswith("all_"):
                s = wt[gm & f.ss_retired.to_numpy()].sum(0) / pop
                rows.append(dict(asec_year=y, group=g, measure="pct_ss_retired", value=100 * s[0],
                                 se=100 * se(s), n=int(gm.sum())))
            for m, (num, den) in measures.items():
                dm = gm if den is None else gm & f[den].to_numpy()
                t = wt[gm & f[num].to_numpy()].sum(0) / wt[dm].sum(0)
                rows.append(dict(asec_year=y, group=g, measure=m, value=100 * t[0],
                                 se=100 * se(t), n=int(dm.sum())))
        print(y, "SS-retired 62+: n", int(groups["ss_retired_62+"].sum()), "| PRWKSTAT codes among employed:",
              sorted(d.PRWKSTAT[f.emp].unique()))
    o = pd.DataFrame(rows); o["income_year"] = o.asec_year - 1
    o = o[["asec_year", "income_year", "group", "measure", "value", "se", "n"]].round({"value": 2, "se": 2})
    OUT.parent.mkdir(parents=True, exist_ok=True); o.to_csv(OUT, index=False); print("wrote", OUT, len(o))
    s = o[o.group.isin(["ss_retired_62+", "all_65+", "ss_retired_62+_withdrawer", "ss_retired_62+_nonwithdrawer"])]
    print(s.pivot_table(index=["group", "measure"], columns="asec_year", values="value").round(1).to_string())

if __name__ == "__main__":
    main()
