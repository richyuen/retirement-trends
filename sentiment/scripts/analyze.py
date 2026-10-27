"""Time-series tests: consumer sentiment (U. Michigan) vs retirement contributions.

For each contribution series (annual, % of wages or % of people) and each sentiment measure:
  1. Unit roots: ADF and KPSS on levels and first differences
  2. Correlations: levels, detrended levels (linear trend removed), first differences (Pearson, Spearman)
  3. Leads and lags: corr(d contrib_t, d sentiment_{t-k}) for k = -2..2 (k > 0: sentiment leads)
  4. Regression in differences with Newey-West SEs, with and without the change in unemployment
  5. Granger causality in differences (1 lag)
  6. Cointegration: Engle-Granger (both directions) and Johansen trace test
Quarterly check: NIPA employer pension+insurance contributions (% of wages) and personal saving rate.

Outputs in sentiment/output/: tests_annual.csv, leadlag_annual.csv, tests_quarterly.csv, leadlag_quarterly.csv
"""
import os, warnings
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss, coint
from statsmodels.tsa.vector_ar.vecm import coint_johansen

warnings.filterwarnings("ignore")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "output")

# Series, sample window, and years whose first difference is dropped (method breaks / gaps)
ANNUAL = {
    "bea_dc_employee_pct_wages": dict(label="Employee DC contributions, % of all wages (BEA)", start=1984, end=2025, drop_diff=[]),
    "bea_dc_employer_pct_priv_wages": dict(label="Employer DC contributions, % of private wages (BEA)", start=1984, end=2025, drop_diff=[]),
    "bea_all_employer_pension_pct_priv_wages": dict(label="Employer DB+DC contributions, % of private wages (BEA)", start=1960, end=2025, drop_diff=[]),
    "f5500_dc_participant_pct_priv_wages": dict(label="Participant DC contributions, % of private wages (Form 5500)", start=1999, end=2023, drop_diff=[]),
    "f5500_dc_employer_pct_priv_wages": dict(label="Employer DC contributions, % of private wages (Form 5500)", start=1999, end=2023, drop_diff=[]),
    "f5500_dc_total_incl_rollovers_pct_priv_wages": dict(label="All DC contributions incl. rollovers, % of private wages (Form 5500)", start=1975, end=2023, drop_diff=[]),
    "irs_ira_contrib_pct_wages": dict(label="IRA contributions, % of wages (IRS)", start=2000, end=2021, drop_diff=[2004]),
    "irs_pct_taxpayers_contrib_ira": dict(label="Taxpayers contributing to an IRA, % (IRS)", start=2000, end=2021, drop_diff=[2004]),
    "f1040_pct_returns_ira_deduction": dict(label="Returns with IRA deduction, % (Form 1040)", start=1987, end=2023, drop_diff=[]),
    "w2_deferrals_pct_wages": dict(label="W-2 elective deferrals, % of wages (IRS)", start=2008, end=2020, drop_diff=[]),
    "w2_pct_earners_deferring": dict(label="Wage earners making deferrals, % (IRS W-2)", start=2008, end=2020, drop_diff=[]),
}
SENT = {"ics": "Michigan sentiment (ICS)", "ics_expect": "Michigan expectations (ICE)", "ics_current": "Michigan current conditions (ICC)"}


def adf_p(x, trend):
    x = pd.Series(x).dropna()
    if len(x) < 10: return np.nan
    return adfuller(x, regression=trend, autolag="AIC", maxlag=min(4, len(x) // 4))[1]


def kpss_p(x, trend):
    x = pd.Series(x).dropna()
    if len(x) < 10: return np.nan
    return kpss(x, regression=trend, nlags="auto")[1]


def pear(a, b):
    d = pd.concat([a, b], axis=1).dropna()
    if len(d) < 6: return np.nan, np.nan, len(d)
    r, p = stats.pearsonr(d.iloc[:, 0], d.iloc[:, 1]); return r, p, len(d)


def detrend(s):
    s = s.dropna(); t = np.arange(len(s))
    b = np.polyfit(t, s.values, 1); return pd.Series(s.values - np.polyval(b, t), index=s.index)


def diffs(s, drop, freq_step=1):
    d = s.diff()
    # only keep differences across consecutive periods
    idx = s.index.to_series()
    if freq_step == 1 and pd.api.types.is_numeric_dtype(idx):
        d[idx.diff() != 1] = np.nan
    d[d.index.isin(drop)] = np.nan
    return d


def johansen_trace(df, det):
    if len(df) < 15: return np.nan, np.nan, np.nan, np.nan
    r = coint_johansen(df.values, det_order=det, k_ar_diff=1)
    # trace stats for r=0 and r<=1 with 5% critical values; rejecting both = each series stationary (rank 2)
    return float(np.real(r.lr1[0])), r.cvt[0, 1], float(np.real(r.lr1[1])), r.cvt[1, 1]


def run(y, x, u, drop, maxlag, nw_lags, excl=()):
    """y: contribution series, x: sentiment, u: unemployment. Same index."""
    df = pd.concat([y.rename("y"), x.rename("x"), u.rename("u")], axis=1)
    lv = df[["y", "x"]].dropna()
    res = dict(n_levels=len(lv), first=lv.index.min(), last=lv.index.max())
    res["adf_p_y_level_trend"] = adf_p(lv.y, "ct"); res["adf_p_x_level"] = adf_p(lv.x, "c")
    res["kpss_p_y_level_trend"] = kpss_p(lv.y, "ct"); res["kpss_p_x_level"] = kpss_p(lv.x, "c")
    dy, dx, du = diffs(df.y, drop), diffs(df.x, drop), diffs(df.u, drop)
    for e in excl:  # robustness: drop these periods' differences (e.g. COVID)
        if e in dy.index: dy[e] = np.nan
    res["adf_p_dy"] = adf_p(dy, "c"); res["adf_p_dx"] = adf_p(dx, "c")
    # correlations
    res["r_levels"], res["p_levels"], _ = pear(lv.y, lv.x)
    ols = sm.OLS(lv.y, sm.add_constant(lv.x)).fit()
    res["levels_ols_r2"] = ols.rsquared
    res["levels_ols_durbin_watson"] = sm.stats.durbin_watson(ols.resid)
    res["r_detrended"], res["p_detrended"], _ = pear(detrend(lv.y), detrend(lv.x))
    res["r_diff"], res["p_diff"], res["n_diff"] = pear(dy, dx)
    dd = pd.concat([dy, dx], axis=1).dropna()
    res["spearman_diff"] = stats.spearmanr(dd.iloc[:, 0], dd.iloc[:, 1])[0] if len(dd) > 5 else np.nan
    # best lead/lag
    ll = []
    for k in range(-maxlag, maxlag + 1):
        r, p, n = pear(dy, dx.shift(k))
        ll.append(dict(k=k, r=r, p=p, n=n))
    # regression in differences, sentiment current + lagged, +/- unemployment
    reg = pd.concat([dy.rename("dy"), dx.rename("dx"), dx.shift(1).rename("dx_l1"), du.rename("du")], axis=1).dropna()
    if len(reg) >= 10:
        for name, cols in [("reg", ["dx", "dx_l1"]), ("reg_ctrl", ["dx", "dx_l1", "du"])]:
            m = sm.OLS(reg.dy, sm.add_constant(reg[cols])).fit(cov_type="HAC", cov_kwds={"maxlags": nw_lags})
            # coefficient scaled to a 10-point rise in sentiment
            res[f"{name}_b_dx_per10"] = 10 * m.params["dx"]; res[f"{name}_p_dx"] = m.pvalues["dx"]
            res[f"{name}_b_dxl1_per10"] = 10 * m.params["dx_l1"]; res[f"{name}_p_dxl1"] = m.pvalues["dx_l1"]
            res[f"{name}_n"] = int(m.nobs); res[f"{name}_r2"] = m.rsquared
            if "du" in cols:
                res[f"{name}_b_du"] = m.params["du"]; res[f"{name}_p_du"] = m.pvalues["du"]
        # Granger (1 lag) in differences, both directions: F-test on the other variable's lag
        for nm, a, b in [("granger_p_sent_to_contrib", dy, dx), ("granger_p_contrib_to_sent", dx, dy)]:
            g = pd.concat([a.rename("a"), a.shift(1).rename("a_l1"), b.shift(1).rename("b_l1")], axis=1).dropna()
            if len(g) >= 10:
                res[nm] = sm.OLS(g.a, sm.add_constant(g[["a_l1", "b_l1"]])).fit().pvalues["b_l1"]
    # cointegration
    if len(lv) >= 12:
        res["eg_p_y_on_x_const"] = coint(lv.y, lv.x, trend="c")[1]
        res["eg_p_y_on_x_trend"] = coint(lv.y, lv.x, trend="ct")[1]
        res["eg_p_x_on_y_const"] = coint(lv.x, lv.y, trend="c")[1]
        (res["johansen_trace_r0_const"], res["johansen_cv5_const"],
         res["johansen_trace_r1_const"], res["johansen_cv5_r1_const"]) = johansen_trace(lv, 0)
        (res["johansen_trace_r0_trend"], res["johansen_cv5_trend"],
         res["johansen_trace_r1_trend"], res["johansen_cv5_r1_trend"]) = johansen_trace(lv, 1)
    return res, ll


def main():
    ann = pd.read_csv(os.path.join(OUT, "annual_panel.csv"), index_col="year")
    rows, llrows = [], []
    for col, spec in ANNUAL.items():
        sub = ann.loc[spec["start"]:spec["end"]]
        for s, slabel in SENT.items():
            if s != "ics" and spec["start"] < 1978:
                sub_s = sub.loc[1978:]
            else:
                sub_s = sub
            for variant, excl in [("all", ()), ("excl_2020_21", (2020, 2021))]:
                res, ll = run(sub_s[col], sub_s[s], sub_s["unrate"], spec["drop_diff"], maxlag=2, nw_lags=2, excl=excl)
                rows.append(dict(series=col, series_label=spec["label"], sentiment=s, variant=variant, **res))
                for d in ll:
                    llrows.append(dict(series=col, sentiment=s, variant=variant, **d))
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(OUT, "tests_annual.csv"), index=False, float_format="%.4f")
    pd.DataFrame(llrows).to_csv(os.path.join(OUT, "leadlag_annual.csv"), index=False, float_format="%.4f")

    # ---- quarterly ----
    qp = pd.read_csv(os.path.join(OUT, "quarterly_panel.csv"), index_col="quarter")
    qrows, qll = [], []
    for col, lab in [("nipa_emp_pension_insurance_pct_wages", "Employer pension + insurance contributions, % of wages (BEA, quarterly)"),
                     ("personal_saving_rate", "Personal saving rate, % of disposable income (BEA, quarterly)")]:
        for start in ["1960Q1", "1978Q1", "1990Q1"]:
            sub = qp.loc[start:"2026Q2"]
            covid = tuple(f"{y}Q{q}" for y in (2020, 2021) for q in range(1, 5))
            for variant, excl in [("all", ()), ("excl_2020_21", covid)]:
                res, ll = run(sub[col], sub["ics"], sub["unrate"], [], maxlag=4, nw_lags=4, excl=excl)
                qrows.append(dict(series=col, series_label=lab, sentiment="ics", sample_start=start, variant=variant, **res))
                for d in ll:
                    qll.append(dict(series=col, sample_start=start, variant=variant, **d))
    pd.DataFrame(qrows).to_csv(os.path.join(OUT, "tests_quarterly.csv"), index=False, float_format="%.4f")
    pd.DataFrame(qll).to_csv(os.path.join(OUT, "leadlag_quarterly.csv"), index=False, float_format="%.4f")

    pd.set_option("display.width", 250)
    keep = ["series", "n_levels", "first", "last", "r_levels", "levels_ols_durbin_watson", "r_detrended", "p_detrended", "r_diff", "p_diff",
            "reg_ctrl_b_dx_per10", "reg_ctrl_p_dx", "reg_ctrl_b_dxl1_per10", "reg_ctrl_p_dxl1", "eg_p_y_on_x_const", "eg_p_y_on_x_trend",
            "johansen_trace_r0_const", "johansen_cv5_const", "adf_p_y_level_trend", "kpss_p_x_level", "adf_p_x_level", "adf_p_dy"]
    print(t[(t.sentiment == "ics") & (t.variant == "all")][keep].round(3).to_string())
    print(pd.DataFrame(qrows)[["series", "sample_start"] + keep[1:]].round(3).to_string())


if __name__ == "__main__":
    main()
