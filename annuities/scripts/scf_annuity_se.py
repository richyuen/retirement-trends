"""Standard errors for SCF annuity ownership, households with reference person 65+ and 55-64, 2004-2022.
Method as in ../scf/scripts/scf_analysis.py: 999 bootstrap replicate weights (wt1bK*mmK, pYY_rw1.dta,
implicate 1) for sampling variance, plus (1+1/5) x between-implicate variance (Rubin).
Run: python3 annuities/scripts/scf_annuity_se.py  (slow-ish: reads replicate-weight files)
"""
from pathlib import Path
import numpy as np, pandas as pd, pyreadstat

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT.parent / "scf" / "raw"
rows = []
for year in [2004, 2007, 2010, 2013, 2016, 2019, 2022]:
    yy = str(year)[2:]
    _, m = pyreadstat.read_dta(str(RAW / f"rscfp{year}.dta"), metadataonly=True)
    nm = {c.lower(): c for c in m.column_names}
    s, _ = pyreadstat.read_dta(str(RAW / f"rscfp{year}.dta"), usecols=[nm[c] for c in ["y1", "yy1", "wgt", "age", "annuit"]])
    s.columns = s.columns.str.lower()
    _, m = pyreadstat.read_dta(str(RAW / f"p{yy}i6.dta"), metadataonly=True)
    nm = {c.lower(): c for c in m.column_names}
    f, _ = pyreadstat.read_dta(str(RAW / f"p{yy}i6.dta"), usecols=[nm["y1"], nm["x6815"]])
    f.columns = f.columns.str.lower()
    s = s.merge(f, on="y1")
    s["imp"] = (s.y1 - s.yy1 * 10).astype(int)
    rw, _ = pyreadstat.read_dta(str(RAW / f"p{yy}_rw1.dta"))
    rw.columns = rw.columns.str.lower()
    wt = np.nan_to_num(np.column_stack([rw[f"wt1b{k}"].to_numpy(float, na_value=np.nan) * rw[f"mm{k}"].astype(float).to_numpy(float, na_value=np.nan) for k in range(1, 1000)]))
    rw_idx = pd.Series(range(len(rw)), index=rw.y1.values)
    for g, (lo, hi) in {"55-64": (55, 64), "65+": (65, 200)}.items():
        for var, flag in [("pct_any_annuity", lambda d: d.x6815.values == 1), ("pct_cashvalue_annuity", lambda d: d.annuit.values > 0)]:
            d = s[(s.age >= lo) & (s.age <= hi)]
            est = [100 * d[d.imp == i].wgt.values[flag(d[d.imp == i])].sum() / d[d.imp == i].wgt.sum() for i in range(1, 6)]
            d1 = d[d.imp == 1]
            W = wt[rw_idx.loc[d1.y1.values].values]
            fl = flag(d1)
            reps = 100 * W[fl].sum(0) / W.sum(0)
            v_samp = reps.var(ddof=1)  # variance across the 999 bootstrap replicates
            v_imp = np.var(est, ddof=1)
            rows.append({"year": year, "group": g, "measure": var, "estimate": np.mean(est),
                         "se": np.sqrt(v_samp + 1.2 * v_imp)})
out = pd.DataFrame(rows).round(2)
out.to_csv(ROOT / "output" / "scf_annuity_ownership_se.csv", index=False)
print(out.pivot_table(index=["group", "measure"], columns="year", values=["estimate", "se"]).round(2).to_string())
