"""SCF microdata: retirement-account balances (1989-2022) and withdrawal incidence (2004-2022)
for households whose reference person is 60+, by age band.

Inputs (scf/raw/, downloaded from https://www.federalreserve.gov/econres/scfindex.htm):
  rscfpYYYY.dta  summary extract (Fed bulletin variables; dollars as published by the Fed)
  pYYi6.dta      full public data (X variables), 2004+
  pYY_rw1.dta    replicate weights (999 bootstrap reps, implicate 1), 2004+
Variable definitions follow the Fed's bulletin.macro.txt (scf/raw/):
  IRAKH, THRIFT, FUTPEN, CURRPEN, RETQLIQ = IRAKH+THRIFT+FUTPEN+CURRPEN
  PENACCTWD = IRA/Keogh withdrawals (X6558+X6566+X6574) + annualized withdrawals from
              account-type pensions (current-pension grid X6464.., future-pension grid X6965..)
Withdrawal questions refer to the calendar year before the survey (e.g. SCF 2022 -> 2021).
Point estimates pool the 5 implicates (WGT already divided by 5 in the summary extract).
SEs: bootstrap replicate weights (wt1bK*mmK) on implicate 1, plus (1+1/5) x between-implicate variance.
Run: python3 scf/scripts/scf_analysis.py
"""
from pathlib import Path
import numpy as np, pandas as pd, pyreadstat

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "raw", ROOT / "output"
OUT.mkdir(exist_ok=True)
WAVES = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022]
WD_WAVES = [w for w in WAVES if w >= 2004]
BANDS = [59, 64, 69, 74, 79, 200]
LABELS = ["60-64", "65-69", "70-74", "75-79", "80+"]
SUMVARS = ["y1", "yy1", "wgt", "age", "irakh", "thrift", "futpen", "currpen", "retqliq", "penacctwd"]


def read(path, cols):
    _, meta = pyreadstat.read_dta(str(path), metadataonly=True)
    names = {c.lower(): c for c in meta.column_names}
    use = [names[c] for c in cols if c in names]
    df, _ = pyreadstat.read_dta(str(path), usecols=use)
    df.columns = df.columns.str.lower()
    return df


def full_flags(year):
    """IRA and pension-account withdrawal flags from the full public file."""
    yy = str(year)[2:]
    ira_yes = ["x6557", "x6565", "x6573"]
    ira_amt = ["x6558", "x6566", "x6574"]
    cur = ["x6464", "x6469", "x6474", "x6479"] + (["x6484", "x6489"] if year < 2010 else [])
    fut = ["x6965", "x6971", "x6977", "x6983"] + (["x6989", "x6995"] if year < 2010 else [])
    d = read(RAW / f"p{yy}i6.dta", ["y1", "yy1"] + ira_yes + ira_amt + cur + fut).fillna(0)
    out = pd.DataFrame({"y1": d.y1})
    out["wd_ira"] = (d[ira_yes] == 1).any(axis=1) | (d[ira_amt] > 0).any(axis=1)
    out["wd_pen"] = (d[cur + fut] > 0).any(axis=1)
    out["ira_amt_raw"] = d[ira_amt].clip(lower=0).sum(axis=1)  # nominal, prior calendar year
    return out


def load(year):
    s = read(RAW / f"rscfp{year}.dta", SUMVARS + ["x1", "xx1"]).rename(columns={"x1": "y1", "xx1": "yy1"})  # 1989 uses X1/XX1
    if "penacctwd" not in s:
        s["penacctwd"] = np.nan
    s["imp"] = (s.y1 - s.yy1 * 10).astype(int)
    if year in WD_WAVES:
        s = s.merge(full_flags(year), on="y1", how="left", validate="1:1")
        s["wd_any"] = s.wd_ira | s.wd_pen
    s = s[s.age >= 60].copy()
    s["band"] = pd.cut(s.age, BANDS, labels=LABELS)
    s["pen"] = s.thrift + s.futpen + s.currpen
    s["year"] = year
    return s


def wmedian(x, w):
    o = np.argsort(x)
    x, w = np.asarray(x)[o], np.asarray(w)[o]
    c = np.cumsum(w)
    return x[np.searchsorted(c, c[-1] / 2)] if len(x) else np.nan


# each statistic is fn(d) -> f(w): masks/values are prepared once per group, then evaluated per weight vector
def share(num, den):
    def prep(d):
        dm = d.eval(den).values; nm = dm & d.eval(num).values
        return lambda w: 100 * w[nm].sum() / w[dm].sum()
    return prep


def median_of(var, cond):
    def prep(d):
        m = d.eval(cond).values; x = d[var].values[m]
        return lambda w: wmedian(x, w[m])
    return prep


def ratio(num, den, cond):
    def prep(d):
        m = d.eval(cond).values; a = d[num].values[m]; b = d[den].values[m]
        return lambda w: 100 * (a * w[m]).sum() / (b * w[m]).sum()
    return prep


def total(var, scale=1e9):
    def prep(d):
        x = d[var].values
        return lambda w: (x * w).sum() / scale
    return prep


def popn(cond):
    def prep(d):
        m = d.eval(cond).values
        return lambda w: w[m].sum() / 1e6
    return prep


def estimate(df, rw, fn):
    """Pooled point estimate + total SE (replicate sampling var on implicate 1 + (1+1/5) x imputation var)."""
    point = fn(df)(df.wgt.values)  # WGT is already divided by 5, so all rows pooled = average over implicates
    if rw is None:
        return point, np.nan
    imps = [fn(g)(g.wgt.values * 5) for _, g in df.groupby("imp")]
    i1 = df[df.imp == 1]
    f1 = fn(i1)
    W = rw.reindex(i1.y1.values).to_numpy()  # columns: 999 replicate weights already multiplied by mm
    reps = np.array([f1(W[:, k]) for k in range(W.shape[1])])
    reps = reps[np.isfinite(reps)]
    return point, float(np.sqrt(np.var(reps, ddof=1) + 1.2 * np.var(imps, ddof=1)))


def load_rw(year):
    yy = str(year)[2:]
    r = read(RAW / f"p{yy}_rw1.dta", ["y1"] + [f"wt1b{k}" for k in range(1, 1000)] + [f"mm{k}" for k in range(1, 1000)]).set_index("y1")
    return pd.DataFrame({k: np.nan_to_num(r[f"wt1b{k}"].to_numpy(float) * r[f"mm{k}"].to_numpy(float)) for k in range(1, 1000)}, index=r.index)


def run():
    stats_bal = {
        "hh_millions": popn("age >= 60"),
        "pct_with_any_ret_acct": share("retqliq > 0", "age >= 60"),
        "pct_with_ira": share("irakh > 0", "age >= 60"),
        "pct_with_dc_pension_acct": share("pen > 0", "age >= 60"),
        "median_ret_acct_if_any": median_of("retqliq", "retqliq > 0"),
        "median_ira_if_any": median_of("irakh", "irakh > 0"),
        "aggregate_ret_acct_bn": total("retqliq"),
        "aggregate_ira_bn": total("irakh"),
    }
    stats_wd = {
        "wd_any_per100_holders": share("wd_any", "retqliq > 0"),
        "wd_penacctwd_per100_holders": share("penacctwd > 0", "retqliq > 0"),
        "wd_ira_per100_ira_holders": share("wd_ira", "irakh > 0"),
        "wd_pen_per100_pen_holders": share("wd_pen", "pen > 0"),
        "wd_any_pct_all_hh": share("wd_any", "age >= 60"),
        "median_wd_if_any": median_of("penacctwd", "penacctwd > 0"),
        "wd_dollar_rate_pct": ratio("penacctwd", "retqliq", "retqliq > 0"),
        "aggregate_wd_bn": total("penacctwd"),
    }
    rows = []
    for year in WAVES:
        df = load(year)
        rw = load_rw(year) if year in WD_WAVES else None
        stats = dict(stats_bal, **(stats_wd if year in WD_WAVES else {}))
        groups = [("60+", df)] + [(b, g) for b, g in df.groupby("band", observed=True)]
        for band, g in groups:
            for name, fn in stats.items():
                est, se = estimate(g, rw, fn)
                rows.append(dict(survey_year=year, ref_year=year - 1, age_band=band, stat=name, estimate=est, se=se))
        print(year, "done", flush=True)
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "scf_estimates_long.csv", index=False, float_format="%.4f")
    return res


if __name__ == "__main__":
    run()
