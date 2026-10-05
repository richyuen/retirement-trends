"""SCF 1989-2022: retirement coverage of working-age households and near-retiree balances relative to income.

Inputs: ../scf/raw/rscfpYYYY.dta (Fed summary extract, dollars in 2022 $) and ../scf/raw/pYY_rw1.dta
(999 bootstrap replicate weights, 2004+). Helper functions (read, estimate, load_rw, wmedian) are imported
from ../scf/scripts/scf_analysis.py so SEs are computed exactly as in the scf/ thread
(replicate variance on implicate 1 + 1.2 x between-implicate variance). No SEs before 2004 (no
replicate weights on disk).

Definitions (Fed bulletin.macro.txt):
  RETQLIQ  retirement accounts = IRA/Keogh + DC on current job + DC from past jobs + account plans paying out
  DBPLANT  1 = head or spouse/partner has a DB plan on a current job, or a pension from a past job
           to be received in the future (does NOT include DB pensions already being received)
  acct_or_db = RETQLIQ > 0 or DBPLANT == 1
  INCOME   total family income in the calendar year before the survey (2022 $)
  RACECL4  1 White non-Hispanic, 2 Black non-Hispanic, 3 Hispanic, 4 other/multiple
Ratios: balance-to-income ratio = RETQLIQ / INCOME per household (households with INCOME > 0);
we report the weighted median of household ratios. Income quartiles are weighted cut points of
INCOME within the 55-64 (or 25-64) group in each wave (pooled implicates; held fixed for replicates).
Run: python3 readiness/scripts/scf_readiness.py   (about 2-3 minutes)
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parents[1]
SCF = HERE.parent / "scf"
sys.path.insert(0, str(SCF / "scripts"))
from scf_analysis import read, estimate, load_rw, wmedian  # noqa: E402

RAW, OUT = SCF / "raw", HERE / "output"
WAVES = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022]
VARS = ["y1", "yy1", "x1", "xx1", "wgt", "age", "retqliq", "irakh", "thrift", "futpen", "currpen",
        "dbplant", "dbplancj", "dcplancj", "income", "norminc", "racecl4"]


def load(year):
    s = read(RAW / f"rscfp{year}.dta", VARS).rename(columns={"x1": "y1", "xx1": "yy1"})
    s["imp"] = (s.y1 - s.yy1 * 10).astype(int)
    s = s[(s.age >= 25) & (s.age <= 64)].copy()
    s["acct"] = s.retqliq > 0
    s["db"] = s.dbplant == 1
    s["acct_or_db"] = s.acct | s.db
    s["ratio"] = np.where(s.income > 0, s.retqliq / s.income.where(s.income > 0), np.nan)
    s["band"] = pd.cut(s.age, [24, 34, 44, 54, 64], labels=["25-34", "35-44", "45-54", "55-64"])
    for grp, cond in [("q55", s.age >= 55), ("q2564", s.age >= 25)]:
        g = s[cond]
        cuts = [wq(g.income.values, g.wgt.values, p) for p in (0.25, 0.5, 0.75)]
        s.loc[cond, grp] = 1 + np.searchsorted(cuts, s.loc[cond, "income"].values, side="right")
    return s


def wq(x, w, p):
    o = np.argsort(x); x, w = x[o], w[o]; c = np.cumsum(w)
    return x[np.searchsorted(c, p * c[-1])]


def share(col):
    def prep(d):
        m = d[col].values.astype(bool)
        return lambda w: 100 * w[m].sum() / w.sum()
    return prep


def med(col, cond=None):
    def prep(d):
        m = np.isfinite(d[col].values) & (d.eval(cond).values if cond else True)
        x = d[col].values[m]
        return lambda w: wmedian(x, w[m])
    return prep


def ratio_of_medians(cond=None):
    def prep(d):
        m = d.eval(cond).values if cond else np.ones(len(d), bool)
        b, y = d.retqliq.values[m], d.income.values[m]
        return lambda w: wmedian(b, w[m]) / wmedian(y, w[m])
    return prep


COVER = {"pct_any_ret_acct": share("acct"), "pct_db_plan": share("db"),
         "pct_acct_or_db": share("acct_or_db"), "pct_dc_current_job": share("dcplancj")}
NEAR = {"median_ratio_all": med("ratio"),
        "median_ratio_holders": med("ratio", "retqliq > 0"),
        "median_balance_all": med("retqliq"),
        "median_balance_holders": med("retqliq", "retqliq > 0"),
        "median_income": med("income"),
        "pct_any_ret_acct": share("acct"), "pct_acct_or_db": share("acct_or_db"),
        "pct_ratio_ge1": lambda d: (lambda m: (lambda w: 100 * w[m].sum() / w.sum()))((d.ratio.values >= 1) & np.isfinite(d.ratio.values)),
        "ratio_of_medians_holders": ratio_of_medians("retqliq > 0")}


def run():
    rows = []
    for year in WAVES:
        df = load(year)
        rw = load_rw(year) if year >= 2004 else None
        cells = [("coverage", "25-64", "all", df, COVER)]
        cells += [("coverage", b, "all", g, COVER) for b, g in df.groupby("band", observed=True)]
        cells += [("coverage", "25-64", f"race{int(r)}", g, COVER) for r, g in df.groupby("racecl4")]
        cells += [("coverage", "25-64", f"incq{int(q)}", g, COVER) for q, g in df.groupby("q2564")]
        n55 = df[df.age >= 55]
        cells += [("coverage", "55-64", f"race{int(r)}", g, COVER) for r, g in n55.groupby("racecl4")]
        cells += [("near", "55-64", "all", n55, NEAR)]
        cells += [("near", "55-64", f"incq{int(q)}", g, NEAR) for q, g in n55.groupby("q55")]
        for block, age, group, g, stats in cells:
            n = len(g) / 5
            for name, fn in stats.items():
                est, se = estimate(g, rw, fn)
                rows.append(dict(survey_year=year, block=block, age=age, group=group, stat=name,
                                 estimate=est, se=se, n_records=n))
        print(year, "done", flush=True)
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "scf_readiness_long.csv", index=False, float_format="%.4f")
    return res


if __name__ == "__main__":
    run()
